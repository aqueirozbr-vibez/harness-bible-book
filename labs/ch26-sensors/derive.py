#!/usr/bin/env python3
"""Lab 26 / derive.py — every derived number in Chapter 26."""
import json, datetime
out = {}
# Layered detection under independence: defect classes and per-sensor detection rates (illustrative design values)
# sensors: schema (catches structural defects), domain rule (catches rule violations), citation check, grader (inferential)
d = {"schema": 0.99, "domain_rule": 0.95, "citation": 0.98, "grader": 0.70}
# a defect of a given class is detectable only by sensors that target it; chain detection for a defect targeted by k sensors:
def chain(rates): 
    p = 1.0
    for r in rates: p *= (1 - r)
    return 1 - p
out["detect_structural_schema_only"] = d["schema"]
out["detect_rule_violation_rule_plus_grader"] = round(chain([d["domain_rule"], d["grader"]]), 4)
out["detect_semantic_grader_only"] = d["grader"]
out["detect_semantic_two_graders_indep"] = round(chain([0.70, 0.70]), 3)
out["detect_semantic_two_graders_corr_note"] = "independence overstates; same-family graders share blind spots"
# cost of a chain: cheap-first ordering. Per-sensor cost (ms, USD): schema 1 ms/$0; rule 1 ms/$0; citation 5 ms/$0; grader 3000 ms/$0.004
cost = {"schema": (1, 0.0), "domain_rule": (1, 0.0), "citation": (5, 0.0), "grader": (3000, 0.004)}
# fail-fast: if a cheap sensor fails, later sensors are skipped. Expected cost with p_fail per sensor on a typical draft
pf = {"schema": 0.10, "domain_rule": 0.15, "citation": 0.08, "grader": 0.20}
def expected_cost(order):
    ms = usd = 0.0; survive = 1.0
    for s in order:
        ms += survive * cost[s][0]; usd += survive * cost[s][1]; survive *= (1 - pf[s])
    return round(ms, 1), round(usd, 5), round(survive, 4)
out["cost_cheap_first"] = expected_cost(["schema", "domain_rule", "citation", "grader"])
out["cost_grader_first"] = expected_cost(["grader", "schema", "domain_rule", "citation"])
# false-positive economics: FP triggers a repair (1 model call ~ $0.02 illustrative); FN lets a defect reach the gate (reviewer 6 min at $60/h = $6) or production (work order rework, illustrative $150)
out["cost_fp_usd"] = 0.02; out["cost_fn_reviewer_usd"] = 6.0; out["cost_fn_rework_usd"] = 150.0
# break-even FP rate for a sensor with detection rate r on defect prevalence q, if FN cost is C_fn and FP cost C_fp:
# expected saving per output = q*r*C_fn - (1-q)*fp*C_fp  -> sensor worth running while fp < q*r*C_fn / ((1-q)*C_fp)
for q in (0.05, 0.20):
    for r, name in ((0.95, "rule"), (0.70, "grader")):
        out[f"max_fp_rate_q{q}_{name}_vs_reviewer"] = round(q*r*6.0/((1-q)*0.02), 1)
# coverage arithmetic: acceptance criteria 8 fields + 3 rules = 11 criteria; sensors cover 9 → coverage
out["criteria_total"] = 11; out["criteria_with_sensor"] = 9; out["coverage_pct"] = round(100*9/11, 1)
# task-level: with a sensor chain per step at 0.95 detection and repair at 0.50 (ch22), escaped defects per 1000 steps at 15% defect rate
out["escaped_per_1000_steps_15pct_defect_95_detect"] = int(1000*0.15*(1-0.95))
out["escaped_per_1000_steps_15pct_defect_70_detect"] = int(1000*0.15*(1-0.70))
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
