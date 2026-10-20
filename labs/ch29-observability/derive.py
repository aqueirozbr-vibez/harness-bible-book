#!/usr/bin/env python3
"""Lab 29 / derive.py — every derived number in Chapter 29."""
import json, datetime
out = {}
# Records per task (scenario): 13 model/tool calls -> spans; 11 tool calls -> tool-call logs + policy decisions; ~12 loop transitions; 1 approval; 1 diff
spans, tool_logs, decisions, transitions, interventions, diffs = 13, 11, 11, 12, 1, 1
records = spans + tool_logs + decisions + transitions + interventions + diffs
out["records_per_task"] = records
# bytes: metadata-only records ~600 B; raw prompt/completion text as span events ~ (6000+400 tokens ≈ 25 KB per model call at ~4 chars/token)
meta_bytes = records * 600; text_bytes = spans * 6400 * 4
out["metadata_bytes_per_task"] = meta_bytes; out["raw_text_bytes_per_task"] = text_bytes
tasks_per_month = 1500   # ch37 scenario resolved tasks
out["metadata_GB_per_month"] = round(meta_bytes*tasks_per_month/1e9, 4)
out["raw_text_GB_per_month"] = round(text_bytes*tasks_per_month/1e9, 3)
out["raw_text_GB_per_year"] = round(text_bytes*tasks_per_month*12/1e9, 2)
# Sampling: if traces are sampled at rate s, P(the one incident trace was kept) = s; P(all of an incident's 5 tasks kept) = s^5
for s in (0.1, 0.5, 1.0):
    out[f"p_incident_trace_kept_s{s}"] = s; out[f"p_all5_kept_s{s}"] = round(s**5, 4)
# Attribution coverage: chargeback threshold 80%; with 5 cost tags each independently present at 95%, P(all present) 
out["p_all5_tags_present_at_95_each"] = round(0.95**5, 3)
# Hash chain verification cost: SHA-256 over ~600 B records; ~1e6 hashes/s CPU illustrative -> 49 records/task * 1500 tasks
out["hashes_per_month"] = records*tasks_per_month
out["verify_seconds_per_month_at_1e6_per_s"] = round(records*tasks_per_month/1e6, 3)
# Replay: task reconstruction reads 49 records; at 1 ms per record (DB fetch) -> 49 ms; audit export of a month
out["replay_ms_per_task_at_1ms_per_record"] = records
out["export_month_seconds_at_1ms_per_record"] = round(records*tasks_per_month/1000, 1)
# Retention: LGPD/EU AI Act windows vary; illustrative 6 months hot, 5 years cold for decision records (metadata only)
out["cold_retention_metadata_GB_5y"] = round(meta_bytes*tasks_per_month*12*5/1e9, 2)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
