#!/usr/bin/env python3
"""Lab 05 / derive.py — every derived number in Chapter 05."""
import json, datetime, math
out = {}
hd = 128
# RoPE: theta_i = base^(-2i/hd); wavelength_i = 2π / theta_i
for base in (10_000, 500_000):
    thetas = [base ** (-2*i/hd) for i in range(hd//2)]
    wl = [2*math.pi/t for t in thetas]
    out[f"rope_base_{base}_shortest_wavelength"] = round(wl[0], 2); out[f"rope_base_{base}_longest_wavelength"] = round(wl[-1])
    out[f"rope_base_{base}_pairs_with_wavelength_over_8192"] = sum(1 for w in wl if w > 8192)
    out[f"rope_base_{base}_pairs_with_wavelength_over_131072"] = sum(1 for w in wl if w > 131072)
# position interpolation: to serve L' > L_train, scale positions by L_train/L'
out["pi_scale_8k_to_32k"] = 8192/32768; out["pi_scale_8k_to_128k"] = 8192/131072
# NTK-aware base scaling: base' = base * s^(hd/(hd-2)) for scale s
for s in (4, 16):
    out[f"ntk_base_from_10000_scale_{s}"] = round(10_000 * s ** (hd/(hd-2)))
# Attention score arithmetic vs retrieval: from ch04, n²·d per layer (masked). 70B: d=8192, L=80
d, L = 8192, 80
def score_macs(n): return n*n*d*L
out["score_macs_6k"] = score_macs(6000); out["score_macs_128k"] = score_macs(131072); out["ratio_128k_over_6k"] = round(score_macs(131072)/score_macs(6000))
# KV cache at 320 KB/token (ch04): 6K vs 128K per sequence, GB
out["kv_GB_6k"] = round(320e3*6000/1e9, 2); out["kv_GB_128k"] = round(320e3*131072/1e9, 1)
# Cost: fill 128K per query vs retrieve 6K, at frontier fresh input $1.25/M (ch37), 60,000 queries/month, all fresh
out["monthly_input_usd_fill_128k"] = round(60000*131072/1e6*1.25); out["monthly_input_usd_retrieve_6k_fresh"] = round(60000*6000/1e6*1.25)
# NoLiMa (Modarressi et al. 2025) figures reproduced in ch04: GPT-4o 99.3 -> 69.7 (32K) -> 56 (128K); relative
out["nolima_gpt4o_32k_relative"] = round(69.7/99.3, 3); out["nolima_gpt4o_128k_relative"] = round(56/99.3, 3)
# "effective length" definition used by NoLiMa: longest length at which score >= 85% of short-context baseline
out["nolima_effective_threshold_pct"] = 85
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
