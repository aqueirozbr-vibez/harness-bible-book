#!/usr/bin/env python3
"""Lab 27 / derive.py — every derived number in Chapter 27."""
import json, datetime, math
out = {}
# Grader cost: artifact ~400 tokens + rubric 300 + criteria output 120 lines → per grading call on small tier (ch15 prices)
out["grader_call_tokens_in"] = 1200; out["grader_call_tokens_out"] = 120
out["grader_cost_small_usd"] = round((1200 * 0.25 + 120 * 2.0) / 1e6, 5); out["grader_cost_frontier_usd"] = round((1200 * 1.25 + 120 * 10.0) / 1e6, 5)
# Both orders for pairwise: 2 calls
out["pairwise_both_orders_cost_small"] = round(2 * out["grader_cost_small_usd"], 5)
# Calibration set: 200 human-labelled items per quarter; κ interval width approx via bootstrap in lab; here: expected κ SE ≈ sqrt(po(1-po)/(n(1-pe)^2)) illustrative
po, pe, n = 0.85, 0.53, 200; se = math.sqrt(po * (1 - po) / (n * (1 - pe) ** 2)); out["kappa_se_n200_approx"] = round(se, 3); out["kappa_example"] = round((po - pe) / (1 - pe), 3)
# Position bias arithmetic: if a grader prefers position A with prob b when items are equal, judging both orders and requiring agreement removes it; disagreement rate = 2b(1-b)? Under pure bias, single-order accuracy on equal pairs = 0.5; both-orders flags inconsistency
out["position_bias_note"] = "both orders, agreement required; disagreements → tie or human"
# CI regression gate: golden set 300 items per class × 4 attempts; cost per class run at $0.009 (ch37 config C ~) → per gate run for 11 classes
out["ci_items_per_class"] = 300; out["ci_attempts"] = 4; out["ci_cost_per_class_run"] = round(300 * 4 * 0.009, 2); out["ci_cost_full_run_11_classes"] = round(11 * 300 * 4 * 0.009)
# Gate threshold: fail if pass rate falls below (baseline − half-width) with n=300 at 80% → half-width 4.5 (ch12)
out["gate_halfwidth_n300_p80"] = 4.5
# Benchmarks (recorded): SWE-bench Verified 500 items; τ-bench pass^k (ch16: retail pass^1 60.4%, pass^8 <25%); AgentDojo 97 tasks / 629 cases; GAIA 466 questions, 3 levels, humans ~92% vs GPT-4 with plugins ~15% (Mialon 2023)
out["swe_bench_verified_items"] = 500; out["tau_bench_retail_pass1"] = 60.4; out["tau_bench_retail_pass8_lt"] = 25
out["agentdojo_tasks"] = 97; out["agentdojo_cases"] = 629; out["gaia_questions"] = 466; out["gaia_levels"] = 3; out["gaia_human_pct"] = 92; out["gaia_gpt4_plugins_pct"] = 15
# Zheng: 85% grader–human vs 81% human–human; JudgeBiasBench: frontier >50% error on hard bias items (brief); RAND 2026: no judge uniformly reliable
out["zheng_agreement"] = [85, 81]; out["judgebiasbench_error_gt"] = 50
# Grader retirement threshold κ 0.6; report Krippendorff α ≥ 0.80 as "reliable" convention
out["kappa_retire"] = 0.6; out["alpha_reliable"] = 0.80
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
