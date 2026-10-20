#!/usr/bin/env python3
"""Lab 03 — The transformer block. Runs the chapter's NumPy decoder block (block.py, extracted verbatim) forward on
random weights at Llama 3 8B dimensions for a short sequence (shape and residual checks), then reconciles count_params
against the published Llama 3 totals: 8.03B, 70.6B, 405.9B (Dubey et al. 2024). Reproduces every figure in 03.3 within
0.1%. Also checks the causal mask (changing a later token does not change an earlier position's output) and the
GQA broadcast (kv_heads dividing heads)."""
import json, sys, subprocess, datetime, numpy as np
from block import block, init_block, count_params
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(3); ok = True
# forward pass at 8B dims on 16 tokens (d=4096 is fine on CPU for n=16)
p = init_block(4096, 32, 8, 128, 14336, rng); x = rng.standard_normal((16, 4096)).astype(np.float32)
y = block(x, p); print("forward shape in/out:", x.shape, y.shape); ok &= y.shape == x.shape
# residual: with the output projections zeroed, the sub-blocks contribute nothing and the block is the identity
p0 = dict(p); p0["Wo"] = np.zeros_like(p["Wo"]); p0["W2"] = np.zeros_like(p["W2"])
ident = np.allclose(block(x, p0), x); print("block is identity when sub-blocks contribute zero (residual stream):", ident); ok &= ident
print("block adds a non-zero update with real weights:", not np.allclose(y, x)); ok &= not np.allclose(y, x)
# causal mask: perturb token 12, positions 0..11 unchanged
x2 = x.copy(); x2[12] += 1.0; y2 = block(x2, p)
causal = np.allclose(y[:12], y2[:12]) and not np.allclose(y[12:], y2[12:]); print("causal mask holds:", causal); ok &= causal
# parameter reconciliation
CFG = {"Llama 3 8B": (32, 4096, 32, 8, 128, 14336, 128256, 8.03e9), "Llama 3 70B": (80, 8192, 64, 8, 128, 28672, 128256, 70.6e9), "Llama 3 405B": (126, 16384, 128, 8, 128, 53248, 128256, 405.9e9)}
for name, (L, dm, h, kv, hd, dff, V, pub) in CFG.items():
    c = count_params(L, dm, h, kv, hd, dff, V); diff = 100*(c["total"]-pub)/pub
    match_derive = c["total"] == d[name]["total"]; ok &= abs(diff) < 0.1 and match_derive
    print(f"{name:13s} counted {c['total']/1e9:8.3f}B  published {pub/1e9:6.2f}B  diff {diff:+.2f}%  matches derive.py: {match_derive}")
print("FFN share of layer (70B):", d["Llama 3 70B"]["ffn_share_of_layer"], "%")
json.dump({"shape_ok": bool(y.shape == x.shape), "causal": bool(causal), "reconciliation": {k: d[k]["vs_published_pct"] for k in CFG},
           "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 03:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
