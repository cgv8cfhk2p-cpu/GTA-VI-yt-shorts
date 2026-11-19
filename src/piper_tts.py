# -*- coding: utf-8 -*-
"""Voz Piper (VITS) ejecutada con onnxruntime + espeak-ng para los fonemas."""
import json

import numpy as np
import onnxruntime as ort


class Piper:
    def __init__(self, onnx_path, noise=0.667, noise_w=0.8):
        self.cfg = json.load(open(onnx_path + ".json"))
        self.sr = self.cfg["audio"]["sample_rate"]
        self.ids = self.cfg["phoneme_id_map"]
        self.voice = self.cfg.get("espeak", {}).get("voice", "es")
        so = ort.SessionOptions()
        so.intra_op_num_threads = 4
        self.sess = ort.InferenceSession(onnx_path, so, providers=["CPUExecutionProvider"])
        self.noise, self.noise_w = noise, noise_w
        from phonemizer.backend import EspeakBackend
        try:
            import espeakng_loader
            from phonemizer.backend.espeak.wrapper import EspeakWrapper
            EspeakWrapper.set_library(espeakng_loader.get_library_path())
            EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
        except Exception:
            pass
        self.backend = EspeakBackend(self.voice, preserve_punctuation=True, with_stress=True,
                                     language_switch="remove-flags")

    def phonemes(self, text):
        return self.backend.phonemize([text], strip=True)[0]

    def synth(self, text, length_scale=1.0):
        ph = self.phonemes(text)
        seq = list(self.ids["^"]) + list(self.ids["_"])
        for ch in ph:
            if ch in self.ids:
                seq += list(self.ids[ch]) + list(self.ids["_"])
        seq += list(self.ids["$"])
        x = np.array([seq], dtype=np.int64)
        feeds = {"input": x, "input_lengths": np.array([x.shape[1]], dtype=np.int64),
                 "scales": np.array([self.noise, length_scale, self.noise_w], dtype=np.float32)}
        if "sid" in [i.name for i in self.sess.get_inputs()]:
            feeds["sid"] = np.array([0], dtype=np.int64)
        audio = self.sess.run(None, feeds)[0].squeeze()
        return audio.astype(np.float32), self.sr
