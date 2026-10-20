#!/usr/bin/env python3
"""Lab 17 / derive.py — every derived number in Chapter 17."""
import json, datetime
out = {}
# Ask vs guess: a clarification costs one human round-trip (technician answers in ~2 min at $60/h = $2) + delay;
# a guess on an ambiguous request fails with probability g; a failed guess costs a repair loop (~$0.02 tokens) if a sensor catches it,
# or reaches the gate ($6 reviewer) or production ($150) if not. Sensor catch rate c on ambiguity-caused defects.
cost_clarify = 2.0; cost_repair = 0.02; cost_gate = 6.0; cost_prod = 150.0
def expected_guess_cost(g, c, reach_prod=0.1):
    # if guess wrong (g): caught by sensor with prob c → repair; else reaches gate; of those, reach_prod slip to production
    return g * (c * cost_repair + (1 - c) * ((1 - reach_prod) * cost_gate + reach_prod * cost_prod))
for g in (0.2, 0.5):
    for c in (0.5, 0.9):
        out[f"expected_guess_cost_g{g}_c{c}"] = round(expected_guess_cost(g, c), 3)
out["cost_clarify"] = cost_clarify
# break-even ambiguity probability at which asking is cheaper than guessing (c=0.9): solve g*(0.9*0.02 + 0.1*(0.9*6+0.1*150)) = 2
per_wrong = 0.9 * cost_repair + 0.1 * (0.9 * cost_gate + 0.1 * cost_prod)
out["cost_per_wrong_guess_c0.9"] = round(per_wrong, 3); out["breakeven_g_ask_vs_guess_c0.9"] = round(cost_clarify / per_wrong, 3)
per_wrong5 = 0.5 * cost_repair + 0.5 * (0.9 * cost_gate + 0.1 * cost_prod)
out["cost_per_wrong_guess_c0.5"] = round(per_wrong5, 3); out["breakeven_g_ask_vs_guess_c0.5"] = round(cost_clarify / per_wrong5, 3)
# Scenario intake mix (illustrative): 2,000/day — 60% technician chat, 25% CMMS webhook, 10% scheduled, 5% API
out["intake_mix"] = {"technician_chat": 0.60, "cmms_webhook": 0.25, "scheduled": 0.10, "api": 0.05}
out["daily_requests"] = 2000
# Acceptance criteria for the P-101 task: 8 fields + 3 rules = 11; machine-checkable 9 (ch26) → 82%
out["criteria_total"] = 11; out["criteria_checkable"] = 9; out["criteria_coverage_pct"] = round(100 * 9 / 11, 1)
# Clarification rate target: if ambiguity prevalence a and intake resolves share s of it by structure, residual clarifications = a*(1-s)
for a in (0.3,):
    for s in (0.0, 0.5, 0.8): out[f"clarification_rate_a{a}_s{s}"] = round(a * (1 - s), 3)
# Intent validation: actions outside the task's declared scope; if injected/off-scope actions occur at rate i per task and intent check catches share k
for k in (0.9, 0.99): out[f"offscope_reaching_tools_i0.02_k{k}"] = round(0.02 * (1 - k), 4)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
