#!/usr/bin/env python3
"""Lab 10 / derive.py — every derived number in Chapter 10."""
import json, datetime
out = {}
# H100 SXM (NVIDIA datasheet): HBM3 3.35 TB/s; FP16 dense tensor ~989 TFLOP/s (vendor). Llama 3 70B: 70.6B params, 320 KB/token KV (ch04)
BW, FLOPS = 3.35e12, 989e12
N = 70.6e9; bytes16 = 2 * N; bytes8 = N; kv = 320e3
out["weights_GB_fp16"] = round(bytes16 / 1e9); out["weights_GB_fp8"] = round(bytes8 / 1e9)
# Decode floor at batch 1: time to read all weights once per token
out["decode_floor_ms_fp16_1gpu_bw"] = round(bytes16 / BW * 1e3, 1); out["decode_floor_tps_fp16_1gpu_bw"] = round(BW / bytes16, 1)
out["decode_floor_ms_fp8"] = round(bytes8 / BW * 1e3, 1); out["decode_floor_tps_fp8"] = round(BW / bytes8, 1)
# With 2 GPUs tensor-parallel: aggregate bandwidth 2×BW (weights split) → floor halves
out["decode_floor_ms_fp16_2gpu"] = round(bytes16 / (2 * BW) * 1e3, 1); out["decode_floor_tps_fp16_2gpu"] = round(2 * BW / bytes16, 1)
# Compute per token 2N FLOPs; batch crossover where compute time = memory time: B* = (bytes/BW) / (2N/FLOPS)
compute_time_per_token = 2 * N / FLOPS; mem_time = bytes16 / BW
out["compute_ms_per_token_fp16"] = round(compute_time_per_token * 1e3, 3)
out["batch_crossover_fp16"] = round(mem_time / compute_time_per_token)
# arithmetic intensity needed = FLOPS/BW (FLOP per byte)
out["ridge_point_flop_per_byte"] = round(FLOPS / BW)
# Throughput vs batch (memory-bound region): tokens/s ≈ B × (BW/bytes) up to crossover
for B in (1, 8, 32, 128): out[f"decode_tps_batch{B}_fp16_2gpu"] = round(min(B, out["batch_crossover_fp16"]) * 2 * BW / bytes16)
# KV capacity: 2×80 GB minus weights, at 6K context (scenario) and 32K
free = 160e9 - bytes16
out["free_GB_after_weights_2x80"] = round(free / 1e9)
for ctx in (6000, 32768): out[f"max_concurrent_seqs_ctx{ctx}"] = int(free / (kv * ctx))
# Prefill: 8K prompt FLOPs = 2N×8192 (+attention, ch04); time at full tensor throughput
out["prefill_8k_s_at_989TFLOPs"] = round(2 * N * 8192 / FLOPS, 2); out["prefill_8k_s_at_40pct_util"] = round(2 * N * 8192 / (0.4 * FLOPS), 2)
# Speculative decoding: draft proposes k tokens with acceptance rate a; expected accepted per verify = (1 - a^(k+1)) / (1 - a)
def spec(a, k): return (1 - a**(k + 1)) / (1 - a)
for a in (0.6, 0.8, 0.9):
    for k in (3, 5): out[f"spec_expected_tokens_a{a}_k{k}"] = round(spec(a, k), 2)
# Cost per token at utilization u: GPU $/h ÷ (tokens/s achievable × u × 3600)
rate = 2.99 * 2  # 2 H100 $/h (RunPod on-demand, ch37)
tps_max = out["decode_tps_batch32_fp16_2gpu"]
for u in (0.1, 0.4, 0.7): out[f"usd_per_M_tokens_at_util_{u}"] = round(rate / (tps_max * u * 3600) * 1e6, 2)
# PagedAttention: prior systems 20.4–38.2% KV utilization (Kwon 2023); block size 16 tokens → worst-case waste per sequence ≤ 15 tokens
out["paged_block_tokens"] = 16; out["paged_max_waste_tokens_per_seq"] = 15
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)

# KV-bound reality: at 6K context, concurrency caps at 9 sequences on 2×80 GB → decode throughput and cost at that batch
B_kv = out["max_concurrent_seqs_ctx6000"]; tps_kv = B_kv * 2 * BW / bytes16
out["decode_tps_kv_capped_ctx6000"] = round(tps_kv)
for u in (0.4, 0.7): out[f"usd_per_M_tokens_kv_capped_util_{u}"] = round(rate / (tps_kv * u * 3600) * 1e6, 2)
# FP8 weights + FP8 KV: weights 71 GB, KV 160 KB/token → concurrency at 6K
free8 = 160e9 - bytes8; out["max_concurrent_seqs_ctx6000_fp8_all"] = int(free8 / (kv / 2 * 6000))
out["decode_tps_kv_capped_fp8_all"] = round(out["max_concurrent_seqs_ctx6000_fp8_all"] * 2 * BW / bytes8)
out["usd_per_M_tokens_fp8_all_util_0.7"] = round(rate / (out["decode_tps_kv_capped_fp8_all"] * 0.7 * 3600) * 1e6, 2)
json.dump(out, open("results/derived.json","w"), indent=2)
print("kv-capped:", out["decode_tps_kv_capped_ctx6000"], out["usd_per_M_tokens_kv_capped_util_0.7"], "fp8-all:", out["max_concurrent_seqs_ctx6000_fp8_all"], out["decode_tps_kv_capped_fp8_all"], out["usd_per_M_tokens_fp8_all_util_0.7"])
