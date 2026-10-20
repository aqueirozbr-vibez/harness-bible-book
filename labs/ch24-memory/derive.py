#!/usr/bin/env python3
"""Lab 24 / derive.py — every derived number in Chapter 24."""
import json, datetime
out = {}
# Memory budget per step (ch19): 150 tokens → facts at ~35 tokens each
out["memory_budget_tokens"] = 150; out["fact_tokens"] = 35; out["facts_per_step"] = 150 // 35
# Recurrence: a wrong fact in the store, retrieved into a step with prob p (relevance); across a task of 11 steps, P(at least once)
for p in (0.2, 0.5): out[f"p_wrong_fact_surfaces_in_task_p{p}"] = round(1 - (1 - p) ** 11, 3)
# Without provenance check, the wrong fact persists across tasks; with a provenance check that rejects facts lacking a source with prob c
for c in (0.0, 0.9, 1.0): out[f"expected_tasks_touched_per_100_c{c}"] = round(100 * (1 - (1 - 0.2) ** 11) * (1 - c), 1)
# Consolidation ratio: 1,500 tasks/month → episodes; facts extracted per task ~0.3 (most tasks add nothing durable); review accepts 70%
out["episodes_per_month"] = 1500; out["candidate_facts_per_month"] = round(1500 * 0.3); out["accepted_facts_per_month"] = round(1500 * 0.3 * 0.7)
# Store sizes: assets 8,000 × ~5 durable facts = 40,000 semantic facts; procedural: ~50 skills/templates; episodic: 1,500/month × 12 = 18,000 episodes/year
out["semantic_facts_est"] = 8000 * 5; out["episodic_per_year"] = 1500 * 12; out["procedural_items"] = 50
# Lifetimes (illustrative policy): working = task; episodic = 12 months then summarized; semantic = until superseded, reviewed annually; procedural = versioned, no expiry
out["lifetimes"] = {"working": "task", "episodic": "12 months, then summary", "semantic": "until superseded; annual review", "procedural": "versioned; no expiry"}
# Privacy: personal data in episodes (technician names) → retention 30 days for text, metadata-only after (ch29); facts about people: none stored
out["episode_text_retention_days"] = 30
# Poisoning: one wrong fact per 1,000 accepted at review (illustrative error rate) → 12/year; provenance + supersession catches on next revision
out["review_error_rate_per_1000"] = 1
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
