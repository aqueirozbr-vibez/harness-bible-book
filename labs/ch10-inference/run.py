#!/usr/bin/env python3
"""Lab 10 — Inference engineering. Runs the chapter's serving model (serving.py, extracted verbatim) for the plant's
two-H100 Llama 3 70B fallback at fp16 and fp8 and reproduces every figure in 10.3 (floor, crossover, capacity, throughput,
cost per token, speculative gains, prefill time). Then simulates cache allocation for 500 random-length sequences:
contiguous reservation at maximum length versus 16-token paging — the waste gap PagedAttention removes (labelled simulation)."""
import json, sys, subprocess, datetime, random
from serving import serving_model, speculative_gain, prefill_seconds
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
ok = True; BW, FL = 3.35e12, 989e12
m16 = serving_model(70.6e9, 2, 320e3, 2, 80, BW, FL, 6000, 2.99)
m8 = serving_model(70.6e9, 1, 160e3, 2, 80, BW, FL, 6000, 2.99)
m32k = serving_model(70.6e9, 2, 320e3, 2, 80, BW, FL, 32768, 2.99)
checks = [("fp16 weights GB", round(m16["weights_GB"]), d["weights_GB_fp16"]), ("fp16 floor ms (2 GPU)", round(m16["decode_floor_ms"], 1), d["decode_floor_ms_fp16_2gpu"]),
          ("crossover batch", m16["batch_crossover"], d["batch_crossover_fp16"]), ("free GB", round(m16["free_GB"]), d["free_GB_after_weights_2x80"]),
          ("max seqs @6K fp16", m16["max_concurrent_seqs"], d["max_concurrent_seqs_ctx6000"]), ("max seqs @32K fp16", m32k["max_concurrent_seqs"], d["max_concurrent_seqs_ctx32768"]),
          ("tps kv-capped fp16", round(m16["decode_tps_at_max_batch"]), d["decode_tps_kv_capped_ctx6000"]), ("$/M @70% fp16", round(m16["usd_per_M_tokens"][0.7], 2), d["usd_per_M_tokens_kv_capped_util_0.7"]),
          ("max seqs @6K fp8 all", m8["max_concurrent_seqs"], d["max_concurrent_seqs_ctx6000_fp8_all"]), ("tps fp8 all", round(m8["decode_tps_at_max_batch"]), d["decode_tps_kv_capped_fp8_all"]),
          ("$/M @70% fp8 all", round(m8["usd_per_M_tokens"][0.7], 2), d["usd_per_M_tokens_fp8_all_util_0.7"]),
          ("spec a=0.8 k=3", round(speculative_gain(0.8, 3), 2), d["spec_expected_tokens_a0.8_k3"]), ("spec a=0.9 k=5", round(speculative_gain(0.9, 5), 2), d["spec_expected_tokens_a0.9_k5"]),
          ("prefill 8K @40%", round(prefill_seconds(70.6e9, 8192, FL, 0.4), 2), d["prefill_8k_s_at_40pct_util"])]
for name, got, exp in checks:
    mtch = abs(got - exp) <= max(0.011, 0.005 * abs(exp)); ok &= mtch; print(f"{name:24s} chapter {exp!s:>8}  model {got!s:>8}  {'OK' if mtch else 'MISMATCH'}")
# paging simulation
random.seed(10); max_len = 8192; block = 16; lengths = [random.randint(500, max_len) for _ in range(500)]
contiguous = 500 * max_len; used = sum(lengths); paged = sum(((L + block - 1) // block) * block for L in lengths)
util_contig = used / contiguous; util_paged = used / paged
print(f"cache utilization, 500 sequences 500–8192 tokens: contiguous-at-max {util_contig:.1%}  paged(16) {util_paged:.1%}  (Kwon et al. measured 20–38% in prior systems)")
ok &= util_contig < 0.6 and util_paged > 0.99
json.dump({"fp16": m16, "fp8": m8, "util_contiguous": util_contig, "util_paged": util_paged, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2, default=str)
print("Lab 10:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
