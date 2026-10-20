#!/usr/bin/env python3
"""Lab 12 / derive.py — every derived number in Chapter 12."""
import json, datetime, math, numpy as np
rng = np.random.default_rng(12); out = {}
def wilson(p, n, z=1.96):
    d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d; return round(c-h,3), round(c+h,3)
for n in (20, 50, 100, 300, 1000):
    for p in (0.8, 0.95): out[f"wilson95_p{p}_n{n}"] = wilson(p, n); out[f"wilson95_halfwidth_p{p}_n{n}"] = round((wilson(p,n)[1]-wilson(p,n)[0])/2, 3)
# Power to detect 0.80 vs 0.85 (paired, same items) by simulation: correlation between systems rho on item difficulty
def power(n, p1, p2, trials=2000, corr=0.5):
    hits = 0
    for _ in range(trials):
        # shared item difficulty via latent; sample correlated Bernoullis
        z = rng.standard_normal(n); u1 = rng.standard_normal(n); u2 = rng.standard_normal(n)
        a = corr*z + math.sqrt(1-corr**2)*u1; b = corr*z + math.sqrt(1-corr**2)*u2
        from math import erf, sqrt
        t1 = np.quantile(rng.standard_normal(100000), p1); t2 = np.quantile(rng.standard_normal(100000), p2)  # thresholds
        x1 = (a < t1).astype(int); x2 = (b < t2).astype(int)
        diff = x2 - x1
        boots = [np.mean(rng.choice(diff, n, replace=True)) for _ in range(200)]
        lo = np.quantile(boots, 0.025)
        hits += lo > 0
    return round(hits/trials, 2)
for n in (100, 300, 1000): out[f"power_paired_0.80_vs_0.85_n{n}"] = power(n, 0.80, 0.85, trials=300)
# Cohen's kappa worked example: 100 items, judge vs human; agreement 85%, expected by chance from marginals 0.6/0.4 vs 0.65/0.35
po = 0.85; pe = 0.6*0.65 + 0.4*0.35; out["kappa_example_po"] = po; out["kappa_example_pe"] = round(pe,3); out["kappa_example"] = round((po-pe)/(1-pe), 3)
# Zheng et al. 2023: GPT-4 judge 85% agreement (non-tie) vs 81% human-human
out["zheng_gpt4_agreement_pct"] = 85; out["zheng_human_human_pct"] = 81
# Contamination (ch07): P(all 100 clean) at 1% leak
out["p_clean_100_at_1pct"] = round(0.99**100, 3)
# Golden-set size for the plant: 100 per step class × 11 classes = 1,100 items; per language 2× 
out["golden_items_11_classes_100_each"] = 1100; out["golden_items_two_languages"] = 2200
# Cost of one golden-set run at scenario per-query cost (~$0.009 config C, ch37) with k=4
out["golden_run_usd_2200_items_k4_at_0.009"] = round(2200*4*0.009, 2)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
