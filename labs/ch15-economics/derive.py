#!/usr/bin/env python3
"""Lab 15 / derive.py — every derived number in Chapter 15."""
import json, datetime
out = {}
P = {"in": 1.25, "cached": 0.125, "out": 10.0, "small_in": 0.25, "small_cached": 0.025, "small_out": 2.0}   # $/M, Sep 2026 list (vendor)
# Effective input price under cache hit rate h on the cacheable share s of the prompt
def blended_in(h, s): return (1 - s) * P["in"] + s * (h * P["cached"] + (1 - h) * P["in"])
for h in (0.0, 0.5, 0.9, 1.0):
    out[f"blended_input_price_h{h}_s0.67"] = round(blended_in(h, 4000/6000), 4)
# Anthropic cache write surcharge: 1.25x (5-min) / 2x (1-h). Break-even reuse count n: n*in > write + n*cached → n > write/(in - cached)
for w, key in ((1.25, "5min"), (2.0, "1h")):
    out[f"cache_breakeven_reuses_{key}"] = round(w * P["in"] / (P["in"] - P["cached"]), 2)
# Batch API: 50% off; share of workload that can wait b → blended discount
for b in (0.2, 0.5): out[f"blended_discount_batch_share_{b}"] = round(0.5 * b, 2)
# Price trajectory: GPT-4 (Mar 2023) $30 in / $60 out (8K) vs GPT-5 (Aug 2025) $1.25 / $10 — ratios (vendor historical)
out["gpt4_2023_in"] = 30; out["gpt4_2023_out"] = 60; out["gpt5_2025_in"] = 1.25; out["gpt5_2025_out"] = 10
out["input_price_ratio_2023_to_2025"] = round(30 / 1.25, 1); out["output_price_ratio_2023_to_2025"] = round(60 / 10, 1)
# Routing: expected cost per query when share r goes small; quality retention with a classifier of accuracy a on "hard" prevalence q
def route_cost(r): return r * (P["small_in"] * 2000 + P["small_cached"] * 4000 + P["small_out"] * 400) / 1e6 + (1 - r) * (P["in"] * 2000 + P["cached"] * 4000 + P["out"] * 400) / 1e6
out["cost_per_query_all_frontier"] = round(route_cost(0), 5); out["cost_per_query_all_small"] = round(route_cost(1), 5)
for r in (0.5, 0.7, 0.9): out[f"cost_per_query_route_{r}"] = round(route_cost(r), 5); out[f"saving_route_{r}_pct"] = round(100 * (1 - route_cost(r) / route_cost(0)))
# Silent degradation: hard queries misrouted to small = q * (1 - a); if small fails hard queries at rate f, added task failures = q*(1-a)*f
for a in (0.8, 0.95): out[f"misrouted_hard_share_q0.3_a{a}"] = round(0.3 * (1 - a), 3); out[f"added_failure_q0.3_a{a}_f0.5"] = round(0.3 * (1 - a) * 0.5, 3)
# RouteLLM headline vs independent: 85% (MT-Bench) vs ~35% realistic (recorded)
out["routellm_mtbench_saving_pct"] = 85; out["independent_realistic_saving_pct"] = 35
# Self-host break-even from ch10: fp8-all fallback $0.27/M at 70% util vs API blended; volume where 2×H100 ($4,365/mo) < API bill at cost per query (config B ch37 $0.009)
out["api_cost_per_query_B"] = 0.009; out["selfhost_monthly_compute"] = 4365
out["breakeven_queries_per_month"] = int(4365 / 0.009)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
