#!/usr/bin/env python3
"""Lab 04 — Attention in depth.
Reproduces (1) the quadratic scaling of attention time with sequence length and
(2) the KV-cache bytes per token for Llama 3 8B/70B/405B from Chapter 04, Section 04.3.
CPU only. Synthetic random Q/K/V with a fixed seed (labelled synthetic). Runtime ~1-3 min.
Exit code 1 if either reproduction is outside tolerance."""
import time, json, sys, platform, datetime
import numpy as np

SEED = 4
rng = np.random.default_rng(SEED)

def attention(Q, K, V, causal=True):
    h, n, dk = Q.shape
    group = h // K.shape[0]
    K = np.repeat(K, group, axis=0); V = np.repeat(V, group, axis=0)
    scores = Q @ K.transpose(0, 2, 1) / np.sqrt(dk)
    if causal:
        mask = np.triu(np.ones((n, n), dtype=bool), k=1)
        scores = np.where(mask, -np.inf, scores)
    scores -= scores.max(axis=-1, keepdims=True)
    w = np.exp(scores); w /= w.sum(axis=-1, keepdims=True)
    return w @ V

# ---------- Part 1: time vs sequence length ----------
dk, h = 128, 1
lengths = [256, 512, 1024, 2048, 4096]
reps = 5
times = {}
for n in lengths:
    Q = rng.standard_normal((h, n, dk), dtype=np.float32)
    K = rng.standard_normal((h, n, dk), dtype=np.float32)
    V = rng.standard_normal((h, n, dk), dtype=np.float32)
    attention(Q, K, V)  # warm-up
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter(); attention(Q, K, V); ts.append(time.perf_counter() - t0)
    times[n] = float(np.median(ts))
    print(f"n={n:5d}  median attention time {times[n]*1000:8.1f} ms")
logn = np.log(np.array(lengths, dtype=float)); logt = np.log(np.array([times[n] for n in lengths]))
slope, intercept = np.polyfit(logn, logt, 1)
# bootstrap CI on the slope over the 5 repetitions is not available from medians; report fit residual instead
resid = logt - (slope * logn + intercept)
print(f"\nfitted exponent (slope of log t vs log n): {slope:.2f}   max |residual| {abs(resid).max():.2f}")
ok_exp = 1.7 <= slope <= 2.3
print("chapter states: quadratic (exponent 2). ", "REPRODUCED" if ok_exp else "NOT REPRODUCED", "(tolerance 1.7–2.3)")

# ---------- Part 2: KV cache bytes per token ----------
llama3 = {  # Dubey et al. 2024, Table 3
    "Llama 3 8B":   dict(layers=32,  q_heads=32,  kv_heads=8, head_dim=128),
    "Llama 3 70B":  dict(layers=80,  q_heads=64,  kv_heads=8, head_dim=128),
    "Llama 3 405B": dict(layers=126, q_heads=128, kv_heads=8, head_dim=128),
}
chapter = {"Llama 3 8B": 131072, "Llama 3 70B": 327680, "Llama 3 405B": 516096}
ok_kv = True
print("\nKV cache bytes per token (FP16, 2 bytes):")
for name, a in llama3.items():
    b = a["layers"] * a["kv_heads"] * a["head_dim"] * 2 * 2
    nogqa = a["layers"] * a["q_heads"] * a["head_dim"] * 2 * 2
    match = b == chapter[name]; ok_kv &= match
    print(f"  {name:13s} {b:9,d} B = {b/1024:6.0f} KB   without GQA {nogqa/1024:6.0f} KB   chapter {chapter[name]:9,d}  {'OK' if match else 'MISMATCH'}")

# ---------- Part 3: GQA vs MHA output equivalence check ----------
n = 512
Q = rng.standard_normal((8, n, dk), dtype=np.float32)
K = rng.standard_normal((2, n, dk), dtype=np.float32); V = rng.standard_normal((2, n, dk), dtype=np.float32)
gqa = attention(Q, K, V)
mha = attention(Q, np.repeat(K, 4, axis=0), np.repeat(V, 4, axis=0))
same = np.allclose(gqa, mha)
print(f"\nGQA (8 query heads, 2 KV heads) equals MHA with broadcast KV: {same}")

meta = dict(timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat(), python=platform.python_version(),
            numpy=np.__version__, cpu=platform.processor() or platform.machine(), seed=SEED,
            exponent=round(float(slope),3), times_s=times, kv_ok=ok_kv, gqa_equiv=bool(same))
json.dump(meta, open("results/run.json","w"), indent=2)
print("\nresults/run.json written")
sys.exit(0 if (ok_exp and ok_kv and same) else 1)
