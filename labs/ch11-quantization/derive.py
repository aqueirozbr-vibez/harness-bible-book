#!/usr/bin/env python3
"""Lab 11 / derive.py — every derived number in Chapter 11."""
import json, datetime, numpy as np
rng = np.random.default_rng(11); out = {}
# Memory by precision
for name, N in (("8B", 8.03e9), ("70B", 70.6e9), ("405B", 405.9e9)):
    for bits in (16, 8, 4): out[f"weights_GB_{name}_{bits}bit"] = round(N * bits / 8 / 1e9)
# Group-wise quantization overhead: per group of g weights, one fp16 scale (+ optional fp16 zero-point): extra bits per weight
for g in (32, 64, 128): out[f"overhead_bits_per_weight_g{g}_scale_only"] = round(16 / g, 3); out[f"effective_bits_4bit_g{g}"] = round(4 + 16 / g, 3)
# Uniform symmetric quantization error on Gaussian weights: step = 2*max/(2^b - 1); error ~ uniform in [-step/2, step/2]; RMS = step/sqrt(12)
def quant_err(bits, w, groups=None):
    """Symmetric scheme identical to the chapter's quantize(): levels = 2^(b-1) - 1."""
    levels = 2**(bits - 1) - 1
    if groups is None:
        scale = np.abs(w).max() / levels; q = np.clip(np.round(w / scale), -levels, levels) * scale
    else:
        wg = w.reshape(-1, groups); scale = np.abs(wg).max(axis=1, keepdims=True) / levels; q = (np.clip(np.round(wg / scale), -levels, levels) * scale).reshape(-1)
    return float(np.sqrt(np.mean((q - w)**2)) / np.sqrt(np.mean(w**2)))
w = rng.standard_normal(4096 * 4096).astype(np.float32) * 0.02
for bits in (8, 4):
    out[f"rel_rms_err_{bits}bit_per_tensor"] = round(quant_err(bits, w), 4); out[f"rel_rms_err_{bits}bit_g128"] = round(quant_err(bits, w, 128), 4)
# with outliers: 0.01% of weights at 50x typical magnitude (LLM.int8 phenomenon)
w_out = w.copy(); idx = rng.choice(w.size, size=w.size // 10000, replace=False); w_out[idx] *= 50
for bits in (8, 4):
    out[f"rel_rms_err_{bits}bit_per_tensor_with_outliers"] = round(quant_err(bits, w_out), 4); out[f"rel_rms_err_{bits}bit_g128_with_outliers"] = round(quant_err(bits, w_out, 128), 4)
# Decode floor scaling: bytes per parameter → floor (ch10: fp16 2 GPUs 21.1 ms for 70B)
for bits, ms in ((16, 21.1), (8, 10.55), (4, 5.28)): out[f"decode_floor_ms_70B_2gpu_{bits}bit"] = ms
# Distillation cost: teacher generates 50,000 examples × 800 tokens at frontier output $10/M; student LoRA hours negligible
out["distill_teacher_tokens"] = 50000 * 800; out["distill_teacher_usd_at_10_per_M"] = round(50000 * 800 / 1e6 * 10)
# SLM substitution: routine steps (9 of 11) on an 8B at ~1/9 of 70B per-token compute; relative task compute
out["routine_steps"] = 9; out["compute_ratio_8B_over_70B"] = round(8.03 / 70.6, 3)
out["task_compute_all_70B"] = 11 * 1.0; out["task_compute_9_on_8B"] = round(9 * 8.03 / 70.6 + 2 * 1.0, 2); out["task_compute_saving_pct"] = round(100 * (1 - (9 * 8.03 / 70.6 + 2) / 11))
# Belcak et al. 2025: SLMs 10–30× cheaper to run for agent subtasks (primary claim; recorded, not derived)
out["belcak_cost_ratio_range"] = [10, 30]
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
