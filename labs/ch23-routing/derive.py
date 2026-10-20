#!/usr/bin/env python3
"""Lab 23 / derive.py — every derived number in Chapter 23."""
import json, datetime, math
out = {}
P = {"F": {"in": 1.25, "cached": 0.125, "out": 10.0}, "S": {"in": 0.25, "cached": 0.025, "out": 2.0}}   # frontier / small, $/M (ch15)
def q(tier, fresh=2000, cached=4000, o=400, reasoning=0): p = P[tier]; return (fresh * p["in"] + cached * p["cached"] + (o + reasoning) * p["out"]) / 1e6
out["cost_F"] = round(q("F"), 5); out["cost_S"] = round(q("S"), 5); out["cost_F_high_effort"] = round(q("F", reasoning=2000), 5)
# Step-class routing table for the 11-step task (scenario): 9 routine → S at low effort; plan and permit → F at high effort
task_cost_all_F_low = 11 * q("F"); task_cost_routed = 9 * q("S") + 2 * q("F", reasoning=2000); task_cost_all_F_high = 11 * q("F", reasoning=2000)
out["task_cost_all_frontier_low"] = round(task_cost_all_F_low, 4); out["task_cost_routed_sandwich"] = round(task_cost_routed, 4); out["task_cost_all_frontier_high"] = round(task_cost_all_F_high, 4)
out["routed_vs_all_F_low_saving_pct"] = round(100 * (1 - task_cost_routed / task_cost_all_F_low)); out["routed_vs_all_F_high_saving_pct"] = round(100 * (1 - task_cost_routed / task_cost_all_F_high))
# Cascade: try S, verify with a sensor (deterministic), escalate on failure. Expected cost = c_S + e × c_F, e = escalation rate
for e in (0.1, 0.3, 0.5): out[f"cascade_cost_e{e}"] = round(q("S") + e * q("F"), 5); out[f"cascade_saving_e{e}_pct"] = round(100 * (1 - (q("S") + e * q("F")) / q("F")))
# Classifier routing: expected cost with routed share r; silent degradation (ch15): hard share h, accuracy a, small fail on hard f
out["classifier_route_cost_r0.7"] = round(0.7 * q("S") + 0.3 * q("F"), 5)
# Fallback availability: API uptime 99.9% (3 nines) → 43.8 min/month down; with on-site fallback covering, effective availability = 1 - (1-0.999)(1-0.99)
out["api_downtime_min_per_month_3nines"] = round(30 * 24 * 60 * 0.001, 1)
out["effective_availability_with_onsite_99pct"] = round(1 - 0.001 * 0.01, 5)
# Version pinning: providers deprecate models on ~12-month cycles (vendor policy; illustrative cadence) → quarterly candidate runs
out["deprecation_cycle_months_illustrative"] = 12
# Gateway overhead: proxy adds ~5-20 ms per call (illustrative); vs model call ~ seconds
out["gateway_overhead_ms_illustrative"] = [5, 20]
# Savings CI: paired bootstrap over 300 golden items — width depends on per-item cost variance; the lab computes it
out["golden_items"] = 300
# Vendor headline vs measured (ch15): 85 vs ~35
out["routellm_headline_pct"] = 85; out["independent_realistic_pct"] = 35
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
# Sensitivity (REDTEAM): sandwich saving vs all-frontier-high at reasoning budgets 500/1000/2000
for r in (500, 1000, 2000):
    sand = 9 * q("S") + 2 * q("F", reasoning=r); allF = 11 * q("F", reasoning=r); out[f"sandwich_saving_pct_r{r}"] = round(100 * (1 - sand / allF))
json.dump(out, open("results/derived.json","w"), indent=2)
