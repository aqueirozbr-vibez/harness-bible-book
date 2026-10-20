#!/usr/bin/env python3
"""Lab 11 — Quantization, distillation, small models. Runs the chapter's quantizer (quant.py, extracted verbatim) on a
4,096×4,096 Gaussian weight matrix (seed 11) at 8 and 4 bits, per-tensor and per-group (g=128), with and without 0.01%
outliers at 50×. Reproduces the 11.3 error table, the effective bits per weight, the layer-output error, the memory table,
and the substitution saving."""
import json, sys, subprocess, datetime, numpy as np
from quant import quantize, relative_rms_error, inject_outliers, output_error, substitution_compute
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(11); ok = True
w = (rng.standard_normal((4096, 4096)) * 0.02).astype(np.float32); w_out = inject_outliers(w, 1e-4, 50.0, rng)
for label, mat in (("", w), ("_with_outliers", w_out)):
    for bits in (8, 4):
        for g, key in ((None, "per_tensor"), (128, "g128")):
            wq, eff = quantize(mat, bits, g); e = relative_rms_error(mat, wq); exp = d[f"rel_rms_err_{bits}bit_{key}{label}"]
            m = abs(e - exp) < 0.02; ok &= m
            print(f"{bits}-bit {key:10s}{label:15s} rel RMS err {e:6.4f} (chapter {exp})  eff bits {eff:.3f}  {'OK' if m else 'MISMATCH'}")
# layer output error at 8-bit g128 vs 4-bit g128 on random activations
x = rng.standard_normal((64, 4096)).astype(np.float32)
for bits in (8, 4):
    wq, _ = quantize(w, bits, 128); print(f"layer output error y=xW at {bits}-bit g128: {output_error(w, wq, x):.4f}")
# memory table
for name, N in (("8B", 8.03e9), ("70B", 70.6e9)):
    for bits in (16, 8, 4):
        got = round(N * bits / 8 / 1e9); exp = d[f"weights_GB_{name}_{bits}bit"]; m = got == exp; ok &= m
print("memory table reconciles:", ok)
s = substitution_compute(11, 9, 8.03e9, 70.6e9); m = s["saving_pct"] == d["task_compute_saving_pct"]; ok &= m
print(f"substitution: task compute {s['all_large']} → {s['mixed']} units, saving {s['saving_pct']}% (chapter {d['task_compute_saving_pct']}%) {'OK' if m else 'MISMATCH'}")
json.dump({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 11:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
