#!/usr/bin/env python3
"""Lab 13 — Failure science of models. Runs the chapter's code (failure.py, extracted verbatim). Reproduces: the
scoring-rule table (guessing dominates under binary grading; abstaining wins below the threshold under penalties); the
plant's abstention threshold from costs; ECE and selective-prediction coverage/accuracy for a simulated calibrated model
and an overconfident one (seed 13, 20,000 questions); and the harness_confidence routing on the four signal combinations."""
import json, sys, subprocess, datetime, numpy as np
from failure import expected_score, answer_threshold, ece, selective, harness_confidence
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(13); ok = True
for p in (0.2, 0.5, 0.8):
    for pen, key in ((0.0, "binary"), (1.0, "penalized_t0.5"), (3.0, "penalized_t0.75")):
        got = round(expected_score(p, pen), 2); exp = d[f"{key}_expected_score_guess_p{p}"]; m = abs(got - exp) < 1e-9; ok &= m
    print(f"p={p}: binary {expected_score(p,0):+.2f}  penalty1 {expected_score(p,1):+.2f}  penalty3 {expected_score(p,3):+.2f}  {'OK' if ok else 'MISMATCH'}")
t = answer_threshold(150, 6); m = abs(t - d["answer_only_if_p_correct_above"]) < 1e-9; ok &= m; print(f"abstention threshold at $150/$6: {t:.3f} (chapter {d['answer_only_if_p_correct_above']}) {'OK' if m else 'MISMATCH'}")
N = 20000; conf = rng.beta(2, 1.2, N); correct = rng.random(N) < conf; correct2 = rng.random(N) < conf**2
e1, e2 = ece(conf, correct), ece(conf, correct2); m = abs(e1 - d["ece_calibrated"]) < 0.01 and abs(e2 - d["ece_overconfident"]) < 0.02; ok &= m
print(f"ECE calibrated {e1:.4f} (chapter {d['ece_calibrated']}); overconfident {e2:.4f} (chapter {d['ece_overconfident']}) {'OK' if m else 'MISMATCH'}")
for thr in (0.5, 0.7, 0.9):
    cov, acc = selective(conf, correct, thr); m = abs(cov - d[f"selective_coverage_t{thr}"]) < 0.02 and abs(acc - d[f"selective_accuracy_t{thr}"]) < 0.02; ok &= m
    print(f"selective t={thr}: coverage {cov:.3f} accuracy {acc:.3f} (chapter {d[f'selective_coverage_t{thr}']}, {d[f'selective_accuracy_t{thr}']}) {'OK' if m else 'MISMATCH'}")
cov, acc = selective(conf, correct2, 0.7); m = abs(acc - d["overconf_accuracy_t0.7"]) < 0.02; ok &= m; print(f"overconfident t=0.7 accuracy {acc:.3f} (chapter {d['overconf_accuracy_t0.7']}) {'OK' if m else 'MISMATCH'}")
routes = {(False, True, True): "abstain", (True, False, True): "repair", (True, True, True): "answer", (True, True, False): "review"}
rt_ok = all(harness_confidence(*k) == v for k, v in routes.items()); ok &= rt_ok; print("harness_confidence routing:", rt_ok)
json.dump({"ece": [e1, e2], "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 13:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
