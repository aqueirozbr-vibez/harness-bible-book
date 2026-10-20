#!/usr/bin/env python3
"""Lab 27 — Graders and agent evaluation. Runs the chapter's code (graders.py, extracted verbatim). A simulated grader
(stub, labelled) with a true accuracy per criterion plus injected position bias (prefers the first candidate) and verbosity
bias (prefers longer artifacts). Reproduces: (1) calibration — κ per criterion against human labels on 200 items with the
chapter's example marginals; a low-accuracy criterion is retired below 0.6; (2) pairwise both-orders — a position-biased
grader yields ties on equal pairs instead of a spurious winner; (3) the CI gate — a real 5-point regression is blocked,
a no-change candidate merges, on 300 items with a paired-bootstrap interval."""
import json, sys, subprocess, datetime, numpy as np
from graders import grade, pairwise_both_orders, cohen_kappa, calibrate, ci_gate
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(27); ok = True
# 1. calibration: two criteria; human labels; grader with accuracy 0.9 (c1) and 0.72 (c2), plus verbosity bias
n = 200; human = {"c1": (rng.random(n) < 0.6).astype(int), "c2": (rng.random(n) < 0.5).astype(int)}
length = rng.integers(200, 800, n)
def grader_verdict(cid, i, acc):
    correct = rng.random() < acc; v = human[cid][i] if correct else 1 - human[cid][i]
    if length[i] > 650 and rng.random() < 0.15: v = 1          # verbosity bias: long artifacts nudged to pass
    return v
verd = {"c1": np.array([grader_verdict("c1", i, 0.90) for i in range(n)]), "c2": np.array([grader_verdict("c2", i, 0.72) for i in range(n)])}
rep = calibrate(verd, human); print("calibration:", rep); ok &= rep["c1"]["status"] == "ok" and rep["c2"]["status"] == "retire"
# chapter's κ example: construct exactly (po .85, marginals .6/.4 vs .65/.35)
judge = np.array([1]*60 + [0]*40); hum = judge.copy(); hum[60:65] = 1; hum[0:5] = 0; hum[65:70] = 1
k = cohen_kappa(judge, hum); print(f"κ example: {k:.3f} (chapter {d['kappa_example']})"); ok &= abs(k - d["kappa_example"]) < 0.005
# verbosity check: pass rate vs length on items where human says fail
fails = human["c1"] == 0; long_ = length > 650
print(f"verbosity bias visible: grader pass rate on human-fail items, long {verd['c1'][fails & long_].mean():.2f} vs short {verd['c1'][fails & ~long_].mean():.2f}")
# 2. pairwise both orders with position bias: on equal pairs, single-order picks A 80% of the time; both-orders yields ties
def biased_pair(a, b, criterion): return "A" if rng.random() < 0.8 else "B"       # equal candidates; pure position bias
single = sum(biased_pair({}, {}, "c") == "A" for _ in range(500)) / 500
both = [pairwise_both_orders({"id": "a"}, {"id": "b"}, "c", biased_pair) for _ in range(500)]; ties = both.count("tie") / 500
print(f"equal pairs: single-order picks first {single:.2f}; both-orders ties {ties:.2f} (winners {1-ties:.2f} are noise)"); ok &= single > 0.7 and ties > 0.5
# 3. CI gate on 300 items
p_item = np.clip(rng.beta(6, 1.2, 300), 0.3, 0.99)                                                  # per-item pass probability, mean ≈ 0.83
base = (rng.random(300) < p_item).astype(int)
same = (rng.random(300) < p_item).astype(int)                                                         # same system, fresh draws: expected diff 0
reg = base.copy(); idx = rng.choice(np.where(base == 1)[0], 18, replace=False); reg[idx] = 0          # −6 points
g_same, g_reg = ci_gate(base, same, rng=rng), ci_gate(base, reg, rng=rng)
print(f"gate no-change: diff {g_same['diff']} [{g_same['lo']}, {g_same['hi']}] → {g_same['verdict']}; gate −6pt: diff {g_reg['diff']} [{g_reg['lo']}, {g_reg['hi']}] → {g_reg['verdict']}")
ok &= g_same["verdict"] == "merge" and g_reg["verdict"] == "block"
# costs
print(f"CI cost per class run ${d['ci_cost_per_class_run']}; full 11 classes ${d['ci_cost_full_run_11_classes']}; grader call small ${d['grader_cost_small_usd']}")
json.dump({"calibration": rep, "ties": ties, "gate": [g_same, g_reg], "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 27:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
