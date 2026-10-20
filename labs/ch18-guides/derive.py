#!/usr/bin/env python3
"""Lab 18 / derive.py — every derived number in Chapter 18."""
import json, datetime
out = {}
# Stable prefix composition (scenario: 4,000 cached tokens): system guide, tool schemas, reference chunks
comp = {"system_guide": 800, "task_class_guide": 400, "tool_schemas": 1800, "reference_chunks": 1000}
out["prefix_composition"] = comp; out["prefix_total"] = sum(comp.values()); out["cache_min"] = 1024
out["prefix_over_min_x"] = round(sum(comp.values()) / 1024, 1)
# Cost of the prefix per query at fresh vs cached (frontier $1.25 / $0.125 per M)
out["prefix_cost_fresh_usd"] = round(4000 * 1.25 / 1e6, 5); out["prefix_cost_cached_usd"] = round(4000 * 0.125 / 1e6, 5)
out["prefix_monthly_fresh"] = round(60000 * 4000 * 1.25 / 1e6); out["prefix_monthly_cached"] = round(60000 * 4000 * 0.125 / 1e6)
# Examples: each worked example ~250 tokens; 3 examples = 750 tokens in the prefix (cached) vs in the dynamic part (fresh)
out["example_tokens_each"] = 250; out["three_examples_tokens"] = 750
out["three_examples_monthly_if_fresh"] = round(60000 * 750 * 1.25 / 1e6); out["three_examples_monthly_if_cached"] = round(60000 * 750 * 0.125 / 1e6)
# Rule growth: each rule ~30 tokens; 12 rules = 360; 60 rules = 1,800 (prefix share)
for n in (12, 30, 60): out[f"rules_{n}_tokens"] = n * 30; out[f"rules_{n}_share_of_4000_pct"] = round(100 * n * 30 / 4000, 1)
# Pairing: rules with a sensor / total (ch26 principle). Scenario: 12 rules, 9 with sensors
out["rules_total"] = 12; out["rules_with_sensor"] = 9; out["rules_enforced_pct"] = 75
# Prefix drift: one changed byte at position p invalidates cache for tokens after p; expected cached tokens lost if a timestamp sits at position 200 of 4000
out["drift_timestamp_at_200_cached_tokens_lost"] = 3800; out["drift_loss_pct"] = 95
# Two-scaffold spread on guides alone (ch16): the plant measures; no number claimed here
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
