#!/usr/bin/env python3
"""Lab 06 — Scale. Runs the chapter's code (scale.py, extracted verbatim). Reproduces: (1) 6·N·D for Llama 3.1 405B
equals Meta's disclosed 3.8e25 to the stated precision; (2) the compute-optimal tokens-per-parameter ratio implied by
Hoffmann et al.'s published Approach-3 constants at 1e21 / 1e23 / 1e25 FLOPs (50 / 78 / 123) — which does NOT match the
paper's ~20 headline, as the chapter reports; (3) the over-training comparison at Llama 3 8B's compute; (4) the MoE
memory-vs-compute table; (5) tokens per parameter for the documented runs."""
import json, sys, subprocess, datetime
from scale import compute_optimal, train_flops, moe_split, chinchilla_loss
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
ok = True
# 1. 6ND reconciliation
f = train_flops(405.9e9, 15.6e12); dev = 100*(f-3.8e25)/3.8e25; print(f"Llama 3.1 405B 6ND = {f:.3e} vs Meta 3.8e25: {dev:+.2f}%"); ok &= abs(dev) < 1
# 2. published-constant optimum
for C, exp in ((1e21, 50.0), (1e23, 77.6), (1e25, 122.7)):
    l, N, D, r = compute_optimal(C); m = abs(r - exp) < 0.5; ok &= m
    print(f"C={C:.0e}: optimal tokens/param {r:6.1f} (chapter {exp})  N={N:.2e} D={D:.2e}  {'OK' if m else 'MISMATCH'}")
print("→ published Approach-3 constants imply 50–123, not ~20; see Epoch AI 2024 replication (chapter 06.2)")
# 3. over-training at 8B compute
C8 = train_flops(8.03e9, 15e12); l_opt, N_opt, D_opt, _ = compute_optimal(C8); l8 = chinchilla_loss(8.03e9, 15e12)
print(f"at Llama 3 8B compute {C8:.2e}: fit-optimal N={N_opt:.2e} D={D_opt:.2e} loss {l_opt:.3f}; 8B on 15T loss {l8:.3f}; serve-cost ratio {N_opt/8.03e9:.1f}x")
ok &= abs(l_opt - 1.923) < 0.002 and abs(l8 - 1.948) < 0.002 and abs(N_opt/8.03e9 - 4.4) < 0.15
# 4. MoE table
for name, tot, act, mem_exp, fl_exp in (("DeepSeek-V3", 671e9, 37e9, 1342, 74), ("Mixtral 8x7B", 46.7e9, 12.9e9, 93, 26), ("Llama 4 Maverick", 400e9, 17e9, 800, 34)):
    s = moe_split(tot, act); m = round(s["memory_GB"]) == mem_exp and round(s["flops_per_token"]/1e9) == fl_exp; ok &= m
    print(f"{name:18s} memory {s['memory_GB']:6.0f} GB  {s['flops_per_token']/1e9:4.0f} GFLOP/token  ratio {s['total_over_active']:5.1f}  {'OK' if m else 'MISMATCH'}")
# 5. tokens per parameter
for name, N, D, exp in (("GPT-3", 175e9, 300e9, 1.7), ("Chinchilla", 70e9, 1.4e12, 20.0), ("Llama 3 8B", 8.03e9, 15e12, 1868.0)):
    r = round(D/N, 1); m = abs(r - exp) < 0.5; ok &= m; print(f"{name:12s} tokens/param {r:7.1f} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
json.dump({"llama405_6ND_dev_pct": dev, "published_fit_ratios": [50.0, 77.6, 122.7], "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 06:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
