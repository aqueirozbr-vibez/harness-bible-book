#!/usr/bin/env python3
"""Lab 30 / derive.py — every derived number in Chapter 30."""
import json, datetime, math
out = {}
# Anthropic multi-agent research post (2025): agents ~4× chat tokens; multi-agent ~15× chat tokens (recorded, vendor)
out["agent_over_chat_x"] = 4; out["multiagent_over_chat_x"] = 15; out["multiagent_over_single_agent_x"] = round(15 / 4, 2)
# Scenario single-agent task tokens (ch19 compacted): 78,000 per task; multi-agent at 3.75× → 292,500
single = 78000; out["single_task_tokens"] = single; out["multi_task_tokens_at_3.75x"] = int(single * 15 / 4)
# Cost at config C blended (~$0.009/query ≈ per-task model cost $0.24 from ch37 anatomy? use ch37: monthly C $238 / 1,500 tasks = $0.159 per task)
per_task_single = 238 / 1500; out["single_task_cost_C"] = round(per_task_single, 3); out["multi_task_cost_C"] = round(per_task_single * 15 / 4, 3)
out["monthly_C_single"] = 238; out["monthly_C_multi_all_tasks"] = round(238 * 15 / 4)
# ch37 recorded: multi-agent 15× token multiplier → $3,564 at config C (that figure used 15× over single, an upper bound); here 3.75× over agent is the post's ratio
out["ch37_multi_15x_over_single_usd"] = 3564
# Parallel speedup: 3 independent sub-tasks of 40 s each → wall 40 s vs 120 s sequential; coordination overhead 10 s
out["sequential_s"] = 120; out["parallel_wall_s"] = 40 + 10; out["speedup_x"] = round(120 / 50, 1)
# Delegation break-even: multi-agent justified if quality gain ΔQ × value per task > extra tokens cost. Extra cost per task = 0.159×2.75 = $0.437; at $150 per wrong task (ch26), ΔQ > 0.437/150
extra = per_task_single * (15 / 4 - 1); out["extra_cost_per_task_multi"] = round(extra, 3); out["breakeven_quality_gain_pts_at_150_per_failure"] = round(100 * extra / 150, 2)
# Correlated-error reduction from independent workers: two independent checkers each missing a defect with prob 0.2 → both miss 0.04; if correlated (same family) miss ~0.15
out["two_independent_miss"] = 0.04; out["two_correlated_miss_illustrative"] = 0.15
# Permission intersection: parent scope {P-101-U3, P-102-U3}, delegation scope {P-101-U3, P-104-U2} → child scope {P-101-U3}
out["intersection_example"] = {"parent": ["P-101-U3", "P-102-U3"], "delegation": ["P-101-U3", "P-104-U2"], "child": ["P-101-U3"]}
# MAST (Cemri et al. 2025): 14 failure modes in 3 categories: specification/system design, inter-agent misalignment, task verification/termination (recorded)
out["mast_modes"] = 14; out["mast_categories"] = 3
# Budget carve-out: parent budget 13 calls; child gets 4 → parent retains 9
out["parent_calls"] = 13; out["child_calls"] = 4
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
