#!/usr/bin/env python3
"""Lab 19 / derive.py — every derived number in Chapter 19."""
import json, datetime
out = {}
# Per-step budget (scenario): 6,000 tokens = 4,000 stable prefix + 2,000 dynamic
out["window_per_step"] = 6000; out["prefix"] = 4000; out["dynamic"] = 2000
out["dynamic_split"] = {"retrieved_chunks": 1000, "compacted_history": 400, "memory_facts": 150, "task_and_step": 250, "instruction": 200}
# Uncompacted history growth: each iteration adds ~1,500 tokens (ch22); window at iteration k = 6000 + 1500*(k-1)
for k in (1, 4, 8, 16): out[f"uncompacted_window_iter{k}"] = 6000 + 1500 * (k - 1)
out["uncompacted_growth_x_iter16"] = round((6000 + 1500 * 15) / 6000, 1)
# Compacted: history replaced by a 400-token summary → window constant 6,000
out["compacted_window_any_iter"] = 6000
# Tokens per task: 11 steps + 1 plan + 1 repair = 13 calls; uncompacted sum vs compacted
unc = sum(6000 + 1500 * (k - 1) for k in range(1, 14)); out["tokens_per_task_uncompacted_13_calls"] = unc; out["tokens_per_task_compacted_13_calls"] = 13 * 6000
out["compaction_saving_pct"] = round(100 * (1 - 13 * 6000 / unc))
# Chunk position: with prefix 4,000 and chunks placed right after, chunk start = 4000/window; uncompacted at iter 16 with history before chunks → chunks pushed to middle
out["chunk_start_fraction_compacted"] = round(4000 / 6000, 2)
out["chunk_start_fraction_uncompacted_iter16_history_first"] = round((4000 + 1500 * 15) / (6000 + 1500 * 15), 2)
# Tool-result trimming: raw CMMS query 100 rows × 80 tokens = 8,000; filtered 5 rows = 400; summary 150
out["raw_tool_result_tokens"] = 8000; out["filtered_tool_result_tokens"] = 400; out["summary_tool_result_tokens"] = 150
out["trim_ratio_raw_to_filtered"] = 20
# Cost: fresh tokens per task (dynamic only, prefix cached) compacted vs uncompacted at $1.25/M
out["fresh_cost_per_task_compacted"] = round(13 * 2000 * 1.25 / 1e6, 4); out["fresh_cost_per_task_uncompacted"] = round((unc - 13 * 4000) * 1.25 / 1e6, 4)
out["monthly_fresh_compacted_1500_tasks"] = round(1500 * 13 * 2000 * 1.25 / 1e6); out["monthly_fresh_uncompacted_1500_tasks"] = round(1500 * (unc - 13 * 4000) * 1.25 / 1e6)
# Effective-length budget rule (ch05): window ≤ measured effective length; retrieved ≤ 1/3 of dynamic budget? state: retrieved ≤ half of dynamic
out["retrieved_share_of_dynamic_pct"] = 50
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
