#!/usr/bin/env python3
"""Lab 25 / derive.py — every derived number in Chapter 25."""
import json, datetime
out = {}
# Tool schema cost in the prefix (ch18): 20 tools × ~90 tokens = 1,800; per-class trimming to 9 tools
out["tools_total"] = 20; out["tokens_per_tool_schema"] = 90; out["schema_tokens_all"] = 1800; out["tools_per_class"] = 9; out["schema_tokens_per_class"] = 810
out["schema_saving_pct"] = round(100 * (1 - 810 / 1800))
# Code-execution pattern (Anthropic Nov 2025): example 150,000 tokens → 2,000 (98.7% reduction) — recorded vendor claim
out["anthropic_code_exec_example_before"] = 150000; out["anthropic_code_exec_example_after"] = 2000; out["anthropic_code_exec_reduction_pct"] = 98.7
# Scenario: history query 100 rows × 80 tokens = 8,000 raw vs in-sandbox filter returns 5 rows = 400 (ch19)
out["scenario_raw_result"] = 8000; out["scenario_filtered"] = 400; out["scenario_reduction_pct"] = 95
# Risk classes for the scenario's 8 tools
out["risk_classes"] = {"read": 4, "validate": 1, "draft_write": 1, "submit_write_gated": 1, "notify_external": 1}
# Credentials: short-lived token lifetime 15 min → exposure window if leaked; vs static key months
out["token_lifetime_min"] = 15; out["static_key_lifetime_days_illustrative"] = 180; out["exposure_ratio"] = round(180 * 24 * 60 / 15)
# Sandbox: ephemeral per task; startup ~0.2–1.0 s (illustrative); 1,500 tasks/month → sandbox-hours negligible
out["sandbox_startup_s_range"] = [0.2, 1.0]
# Egress: default deny; allow-list of 3 hosts (gateway, broker, CMMS)
out["egress_allowlist"] = ["gateway", "historian-broker", "cmms-api"]
# MCP: JSON-RPC 2.0; methods tools/list, tools/call, resources/list, resources/read, prompts/list; transports stdio + streamable HTTP (spec, vendor/primary)
out["mcp_methods"] = ["initialize", "tools/list", "tools/call", "resources/list", "resources/read", "prompts/list", "prompts/get"]
# Tool-call failure arithmetic: 11 tool calls per task; per-call transient failure 2% → P(no failure) 0.80; with retry 99.5% (ch21)
out["p_task_no_tool_failure_2pct_11calls"] = round(0.98 ** 11, 3)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
