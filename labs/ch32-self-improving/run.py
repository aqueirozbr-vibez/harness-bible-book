#!/usr/bin/env python3
"""Lab 32 — Self-improving harnesses. Runs the chapter's code (improve.py, extracted verbatim). (1) Mines a synthetic
month of failure events (seed 32) into ranked clusters and reproduces the chapter's ranking order. (2) Runs three branches
against a 500-item golden set with a 20% holdout: a real fix (raises pass on the cluster's items, dev and holdout), an
overfit fix (raises pass only on the development items it was shown), and a neutral edit — and shows the merge rule
merging the first, rejecting the second on the holdout, and rejecting the third for no gain. (3) A safety-class branch
that clears the gate is routed to safety review, not merged. (4) Version bumps."""
import json, sys, subprocess, datetime, numpy as np
from improve import mine, run_branch, merge_decision, bump, SAFETY_REVIEW
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(32); ok = True
# 1. mining
counts = {"description": 38, "citation_currency": 22, "permit_rule": 9, "parts_bom": 14, "abbreviation": 31}
events = [{"criterion": k, "step": "draft", "cls": "work_order", "lang": "pt"} for k, n in counts.items() for _ in range(n)]
ranked = mine(events, {"description": 0.9, "citation_currency": 1.0, "permit_rule": 1.0, "parts_bom": 1.0, "abbreviation": 0.8})
order = [r["cluster"][0] for r in ranked]; scores = [r["score"] for r in ranked]
print("ranked clusters:", list(zip(order, scores)))
chap = [x["cluster"].split(" (")[0] for x in d["cluster_ranking"]]; ok &= scores == [68.4, 66.0, 45.0, 28.0, 24.8]
# 2. branches on a 500-item golden set; 120 items exhibit the description cluster; holdout 20%
n = 500; holdout = rng.choice(n, int(0.2 * n), replace=False); exhibit = rng.choice(n, 120, replace=False)
base = (rng.random(n) < 0.84).astype(int); base[exhibit] = (rng.random(120) < 0.55).astype(int)
def real_fix():   # raises pass on exhibiting items everywhere (dev and holdout)
    b = base.copy(); fixed = rng.random(n) < 0.7; b[exhibit] = np.where(fixed[exhibit], 1, b[exhibit]); return b
def overfit_fix():  # raises pass only on exhibiting items in the development set
    b = base.copy(); dev_ex = np.setdiff1d(exhibit, holdout); b[dev_ex] = np.where(rng.random(len(dev_ex)) < 0.7, 1, b[dev_ex]); return b
def neutral():     # fresh draws from the same per-item probabilities
    b = base.copy(); flip = rng.random(n) < 0.05; b[flip] = (rng.random(flip.sum()) < 0.84).astype(int); return b
results = {}
for name, fn, cls in [("symptom_field (real)", real_fix, "template_field"), ("guide_rule (overfit)", overfit_fix, "guide"), ("wording (neutral)", neutral, "guide")]:
    r = run_branch(base, fn(), holdout, rng=rng); dec = merge_decision(r, cls, unaffected_regressed=False); results[name] = (r, dec)
    print(f"{name:22s} dev {r['dev']['diff']:+.3f} [{r['dev']['lo']:+.3f},{r['dev']['hi']:+.3f}]  holdout {r['holdout']['diff']:+.3f} [{r['holdout']['lo']:+.3f},{r['holdout']['hi']:+.3f}]  → {dec['verdict']}: {dec['reason']}")
ok &= results["symptom_field (real)"][1]["verdict"] == "merge" and results["guide_rule (overfit)"][1]["verdict"] == "reject" and "overfit" in results["guide_rule (overfit)"][1]["reason"] and results["wording (neutral)"][1]["verdict"] == "reject"
# 3. safety class
r = run_branch(base, real_fix(), holdout, rng=rng); dec = merge_decision(r, "policy_bundle", False); print("policy-bundle branch with a real gain →", dec["verdict"]); ok &= dec["verdict"] == "safety_review"
# 4. versions
v = "1.4.0"; v1 = bump(v, "minor"); v2 = bump(v1, "patch"); v3 = bump(v2, "major"); print(f"versions: {v} → {v1} (minor) → {v2} (patch) → {v3} (major)"); ok &= (v1, v2, v3) == ("1.5.0", "1.5.1", "2.0.0")
print(f"expected gain from the top fix: rejection rate {d['rejection_rate_before_pct']}% → {d['rejection_rate_after_top_fix_pct']}%; branch cost k=3 ${d['branch_cost_k3']}")
json.dump({"ranking": list(zip(order, scores)), "branches": {k: v[1] for k, v in results.items()}, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 32:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
