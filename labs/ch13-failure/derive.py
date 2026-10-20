#!/usr/bin/env python3
"""Lab 13 / derive.py — every derived number in Chapter 13."""
import json, datetime, numpy as np
rng = np.random.default_rng(13); out = {}
# Scoring-rule incentive: binary grading (+1 correct, 0 wrong or abstain) → guessing dominates abstaining for any p>0.
# Penalized grading (+1 correct, -t/(1-t) wrong, 0 abstain) → answer only if confidence p > t.
def expected_score(p, wrong_penalty): return p * 1 + (1 - p) * (-wrong_penalty)
for p in (0.2, 0.5, 0.8):
    out[f"binary_expected_score_guess_p{p}"] = round(expected_score(p, 0.0), 2)
    out[f"penalized_t0.5_expected_score_guess_p{p}"] = round(expected_score(p, 1.0), 2)   # t=0.5 → penalty 1
    out[f"penalized_t0.75_expected_score_guess_p{p}"] = round(expected_score(p, 3.0), 2)  # t=0.75 → penalty 3
out["threshold_rule"] = "answer iff confidence > t; abstain otherwise"
# Kalai et al. 2025: singleton rate bound — fraction of facts appearing once in training lower-bounds hallucination on those facts (recorded claim)
# Selective prediction: model with calibrated confidence; accuracy vs coverage when abstaining below a threshold
N = 20000
conf = rng.beta(2, 1.2, N)                       # skewed toward high confidence
correct = rng.random(N) < conf                  # calibrated: P(correct)=conf
for t in (0.0, 0.5, 0.7, 0.9):
    mask = conf > t; out[f"selective_coverage_t{t}"] = round(mask.mean(), 3); out[f"selective_accuracy_t{t}"] = round(correct[mask].mean(), 3)
# Miscalibrated (overconfident): true P(correct) = conf^2
correct2 = rng.random(N) < conf**2
for t in (0.0, 0.7, 0.9):
    mask = conf > t; out[f"overconf_accuracy_t{t}"] = round(correct2[mask].mean(), 3)
# ECE with 10 bins for calibrated vs overconfident
def ece(conf, correct, bins=10):
    e = 0.0
    for i in range(bins):
        m = (conf >= i/bins) & (conf < (i+1)/bins)
        if m.sum(): e += m.mean() * abs(correct[m].mean() - conf[m].mean())
    return round(float(e), 4)
out["ece_calibrated"] = ece(conf, correct); out["ece_overconfident"] = ece(conf, correct2)
# Cost of a confident wrong answer vs an abstention in the scenario (ch26 costs): wrong work order reaches production $150; abstention routes to human $6
out["cost_wrong_usd"] = 150; out["cost_abstain_usd"] = 6; out["breakeven_confidence_to_answer"] = round(6 / 150, 3)   # answer if P(wrong)*150 < 6 → P(correct) > 0.96
out["answer_only_if_p_correct_above"] = round(1 - 6/150, 3)
# Zheng/Sharma etc. recorded figures: none needed beyond citations
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
