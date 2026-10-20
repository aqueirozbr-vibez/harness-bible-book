#!/usr/bin/env python3
"""Lab 09 / derive.py — every derived number in Chapter 09."""
import json, datetime, math
from math import comb
out = {}
# Reasoning tokens billed at output rate (ch37: frontier output $10/M). Scenario: 400 visible output tokens; reasoning adds R tokens.
for R in (0, 500, 2000, 8000):
    cost = (400 + R) * 10 / 1e6; out[f"cost_per_query_usd_reasoning_{R}"] = round(cost, 4); out[f"cost_multiplier_reasoning_{R}"] = round((400 + R) / 400, 1)
# Latency at 50 tokens/s decode (ch04 illustrative): seconds per query
for R in (0, 2000, 8000): out[f"latency_s_at_50tps_reasoning_{R}"] = round((400 + R) / 50, 1)
# Monthly bill for the scenario if every query reasons at R vs 10% escalation (ch37)
q = 60000
out["monthly_output_usd_all_queries_R2000"] = round(q * (400 + 2000) * 10 / 1e6); out["monthly_output_usd_10pct_escalation_R2000"] = round(q * (400 + 0.1 * 2000) * 10 / 1e6)
# Self-consistency: majority of k independent samples each correct with prob p
def majority(p, k):
    return sum(comb(k, i) * p**i * (1-p)**(k-i) for i in range((k // 2) + 1, k + 1))
for p in (0.6, 0.7):
    for k in (1, 5, 11, 21): out[f"majority_p{p}_k{k}"] = round(majority(p, k), 3)
# Best-of-N with a perfect verifier: P(at least one correct) = 1 - (1-p)^N ("coverage")
for p in (0.3, 0.6):
    for N in (1, 4, 16, 64): out[f"coverage_p{p}_N{N}"] = round(1 - (1-p)**N, 3)
# Best-of-N with an imperfect verifier: precision v (P(verifier accepts | correct)=v, accepts wrong with prob w)
def bestofN_imperfect(p, N, v, w):
    # probability that the first accepted sample is correct, assuming independent samples; if none accepted, pick random → p
    acc_c = p * v; acc_w = (1 - p) * w; acc = acc_c + acc_w
    if acc == 0: return p
    p_none = (1 - acc) ** N
    return (1 - p_none) * (acc_c / acc) + p_none * p
for w in (0.0, 0.2, 0.5): out[f"bestof16_p0.3_v0.9_w{w}"] = round(bestofN_imperfect(0.3, 16, 0.9, w), 3)
# Reasoning sandwich: 11-step task, high effort on plan + verify (2 steps) at 2,000 tokens, low elsewhere at 0
steps = 11
out["sandwich_reasoning_tokens_per_task"] = 2 * 2000; out["all_high_reasoning_tokens_per_task"] = steps * 2000
out["sandwich_saving_pct"] = round(100 * (1 - (2 * 2000) / (steps * 2000)))
# Sequential vs parallel compute: k samples in parallel cost k× tokens, same latency; one long chain costs 1× tokens, k× latency (illustrative framing)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
