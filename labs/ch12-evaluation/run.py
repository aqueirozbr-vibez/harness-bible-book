#!/usr/bin/env python3
"""Lab 12 — Evaluation science. Runs the chapter's statistics (evalstats.py, extracted verbatim). Reproduces: the Wilson
interval table; the paired-bootstrap power to detect 0.80 vs 0.85 at n = 100 / 300 / 1,000; Cohen's κ on a constructed
100-item judge-vs-human set with the chapter's marginals and agreement; Krippendorff's α equals κ-like agreement on the same
data for two raters; and that a bootstrap interval on identical systems includes zero."""
import json, sys, subprocess, datetime, numpy as np
from evalstats import wilson, paired_bootstrap, cohen_kappa, krippendorff_alpha_nominal, power_to_detect
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(12); ok = True
for n in (20, 100, 300, 1000):
    lo, hi = wilson(int(0.8 * n), n); exp = d[f"wilson95_p0.8_n{n}"]; m = abs(lo - exp[0]) < 0.002 and abs(hi - exp[1]) < 0.002; ok &= m
    print(f"Wilson n={n:4d} p=0.80: ({lo:.3f}, {hi:.3f})  chapter {exp}  {'OK' if m else 'MISMATCH'}")
for n in (100, 300, 1000):
    pw = power_to_detect(n, 0.80, 0.85, corr=0.5, trials=200, rng=rng); exp = d[f"power_paired_0.80_vs_0.85_n{n}"]; m = abs(pw - exp) < 0.12; ok &= m
    print(f"power n={n:4d} (0.80 vs 0.85): {pw:.2f}  chapter {exp}  {'OK' if m else 'MISMATCH'}")
# kappa example: construct 100 items with marginals 60/40 (judge) and 65/35 (human) and 85% agreement
judge = np.array([1]*60 + [0]*40); human = judge.copy()
# make exactly 15 disagreements: flip 10 judge-1 → human 0? we need human marginal 65/35: human ones = 65 → human has 5 more ones than judge
# start human = judge; flip 5 of judge's 0s to 1 (human ones 65) and flip 5 of judge's 1s to 0 then 5 of judge's 0s to 1 again → 15 disagreements, human ones = 60-5+10 = 65
human[60:65] = 1; human[0:5] = 0; human[65:70] = 1
po = np.mean(judge == human); k = cohen_kappa(judge, human); exp = d["kappa_example"]; m = abs(po - 0.85) < 1e-9 and abs(k - exp) < 0.005; ok &= m
print(f"kappa example: agreement {po:.2f}, marginals judge {judge.mean():.2f} human {human.mean():.2f}, kappa {k:.3f} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
alpha = krippendorff_alpha_nominal(np.vstack([judge, human]).astype(float)); print(f"Krippendorff alpha on the same two raters: {alpha:.3f} (close to kappa: {abs(alpha - k) < 0.02})"); ok &= abs(alpha - k) < 0.02
a = (rng.random(300) < 0.8).astype(int); lo, hi, pt = paired_bootstrap(a, a, iters=2000, rng=rng); print(f"identical systems bootstrap: ({lo:.3f}, {hi:.3f}) includes 0: {lo <= 0 <= hi}"); ok &= lo <= 0 <= hi
json.dump({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 12:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
