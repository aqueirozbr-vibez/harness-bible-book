#!/usr/bin/env python3
"""Lab 22 / derive.py — every derived number in Chapter 22 (loop arithmetic)."""
import json, datetime
def step_success(p, q, cap):           # P(step eventually passes) with first-try p, repair success q, at most cap repairs
    return p + (1-p)*(1-(1-q)**cap)
def expected_calls(p, q, cap):          # expected model calls per step (1 attempt + repairs), counting repairs until pass or cap
    e = 1.0; fail = (1-p)
    for r in range(1, cap+1):
        e += fail                       # a repair call happens if still failing
        fail *= (1-q)
    return e
out = {}
for cap in (0, 1, 3, 5):
    out[f"step_pass_p60_q50_cap{cap}"] = round(step_success(0.60, 0.50, cap), 3)
    out[f"calls_p60_q50_cap{cap}"] = round(expected_calls(0.60, 0.50, cap), 2)
steps = 11
for cap in (0, 3):
    ps = step_success(0.60, 0.50, cap); out[f"task_pass_11steps_cap{cap}"] = round(ps**steps, 3)
ps = step_success(0.95, 0.50, 3); out["task_pass_11steps_p95_q50_cap3"] = round(ps**steps, 3)
# context growth: base B tokens per iteration; uncompacted history adds g tokens per prior iteration
B, g = 6000, 1500
for m in (4, 8, 16):
    unc = m*B + g*m*(m-1)//2; comp = m*(B+g)   # compacted: one summary of ~g tokens carried
    out[f"tokens_{m}_iters_uncompacted"] = unc; out[f"tokens_{m}_iters_compacted"] = comp
    out[f"ratio_{m}"] = round(unc/comp, 2)
# cost of one runaway loop: 200 iterations uncompacted at frontier fresh-input price
m = 200; unc = m*B + g*m*(m-1)//2; out["runaway_200_iters_tokens"] = unc; out["runaway_200_iters_usd_at_1.25"] = round(unc/1e6*1.25, 2)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
