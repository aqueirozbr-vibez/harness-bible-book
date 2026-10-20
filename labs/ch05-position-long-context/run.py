#!/usr/bin/env python3
"""Lab 05 — Positional encoding and long context. Runs the chapter's RoPE code (rope.py, extracted verbatim).
Reproduces: (1) the relative-position identity — the rotated dot product depends only on m − n, to floating-point
precision, for random q, k, positions, and shifts; (2) the wavelength table at bases 10,000 and 500,000 (05.3);
(3) position-interpolation scales and NTK-aware bases; (4) the fill-vs-retrieve arithmetic (477×, 42 GB, $9,830 vs $450);
(5) that RoPE is length-preserving (rotation), so it changes no token's norm."""
import json, sys, subprocess, datetime, numpy as np
from rope import apply_rope, relative_score, wavelengths, ntk_base
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(5); ok = True; hd = 128
# 1. relative-position identity
maxdev = 0.0
for _ in range(200):
    q = rng.standard_normal(hd); k = rng.standard_normal(hd)
    m, n, s = int(rng.integers(0, 4000)), int(rng.integers(0, 4000)), int(rng.integers(0, 100000))
    a = relative_score(q, k, m, n); b = relative_score(q, k, m + s, n + s); maxdev = max(maxdev, abs(a - b))
print(f"relative-position identity: max |score(m,n) − score(m+s,n+s)| = {maxdev:.2e}"); ok &= maxdev < 1e-6
# absolute position matters when the difference changes
q = rng.standard_normal(hd); k = rng.standard_normal(hd)
print("score changes when m − n changes:", abs(relative_score(q, k, 10, 3) - relative_score(q, k, 10, 4)) > 1e-6); ok &= abs(relative_score(q, k, 10, 3) - relative_score(q, k, 10, 4)) > 1e-6
# 2. wavelengths
for base, key in ((10_000, "10000"), (500_000, "500000")):
    wl = wavelengths(hd, base)
    checks = [(f"base {base} longest", round(float(wl[-1])), d[f"rope_base_{key}_longest_wavelength"]),
              (f"base {base} pairs > 8192", int((wl > 8192).sum()), d[f"rope_base_{key}_pairs_with_wavelength_over_8192"]),
              (f"base {base} pairs > 131072", int((wl > 131072).sum()), d[f"rope_base_{key}_pairs_with_wavelength_over_131072"])]
    for name, got, exp in checks:
        m_ = got == exp; ok &= m_; print(f"{name:28s} chapter {exp}  computed {got}  {'OK' if m_ else 'MISMATCH'}")
# 3. extension parameters
for s, key in ((4, "4"), (16, "16")):
    got = round(ntk_base(10_000, s, hd)); exp = d[f"ntk_base_from_10000_scale_{key}"]; m_ = got == exp; ok &= m_
    print(f"NTK base for scale {s:2d}:            chapter {exp}  computed {got}  {'OK' if m_ else 'MISMATCH'}")
# 4. fill vs retrieve
for name, got, exp in (("ratio 128K/6K attention", d["ratio_128k_over_6k"], 477), ("KV GB at 128K", d["kv_GB_128k"], 41.9), ("monthly $ fill", d["monthly_input_usd_fill_128k"], 9830), ("monthly $ retrieve", d["monthly_input_usd_retrieve_6k_fresh"], 450)):
    m_ = abs(got - exp) <= 1; ok &= m_; print(f"{name:28s} chapter {exp}  derived {got}  {'OK' if m_ else 'MISMATCH'}")
# 5. norm preservation
x = rng.standard_normal((64, hd)); y = apply_rope(x, np.arange(64, dtype=float))
print("rotation preserves norms:", np.allclose(np.linalg.norm(x, axis=1), np.linalg.norm(y, axis=1))); ok &= np.allclose(np.linalg.norm(x, axis=1), np.linalg.norm(y, axis=1))
json.dump({"identity_maxdev": maxdev, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 05:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
