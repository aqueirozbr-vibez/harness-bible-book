#!/usr/bin/env python3
"""Lab 23 — Model layer, routing, gateways. Runs the chapter's code (routing.py, extracted verbatim) on a simulated golden
set (seed 23): 300 items across the scenario's step classes, each with a hidden difficulty and per-tier pass probabilities
(stubs, labelled). Reproduces: (1) task-cost arithmetic (all-F low / sandwich / all-F high) and the 14% / 78% savings;
(2) cascade routing with a deterministic verifier — saving and retention with paired-bootstrap intervals; (3) classifier
routing at 80% and 95% accuracy — silent degradation visible in retention; (4) the gateway's hard cap stopping a runaway
loop and its fallback engaging when the frontier is unavailable; (5) the availability arithmetic."""
import json, sys, subprocess, datetime, numpy as np
from routing import call_cost, ROUTING_TABLE, Gateway, route_classifier, route_cascade, savings_and_retention
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(23); ok = True
# 1. task-cost arithmetic
allF_low = 11 * call_cost("F"); sandwich = 9 * call_cost("S") + 2 * call_cost("F", reasoning=2000); allF_high = 11 * call_cost("F", reasoning=2000)
s1, s2 = round(100 * (1 - sandwich / allF_low)), round(100 * (1 - sandwich / allF_high))
print(f"task cost: all-F low ${allF_low:.4f}  sandwich ${sandwich:.4f}  all-F high ${allF_high:.4f}; savings {s1}% / {s2}% (chapter {d['routed_vs_all_F_low_saving_pct']}% / {d['routed_vs_all_F_high_saving_pct']}%)")
ok &= s1 == d["routed_vs_all_F_low_saving_pct"] and s2 == d["routed_vs_all_F_high_saving_pct"]
# 2. golden set: classes with difficulty; small passes easy at 0.95, hard at 0.5; frontier passes easy 0.97, hard 0.9
classes = ["retrieve", "draft", "validate", "submit", "report"] * 60; n = len(classes)
hard = rng.random(n) < 0.3
pF = np.where(hard, 0.90, 0.97); pS = np.where(hard, 0.50, 0.95)
passF = rng.random(n) < pF; passS_first = rng.random(n) < pS
costF = np.array([call_cost("F")] * n); passBase = passF
# cascade: verifier = deterministic sensor that detects a small-tier failure with prob 0.95 (sensor catch rate)
sensor_catch = 0.95; caught = (~passS_first) & (rng.random(n) < sensor_catch)
tier_used = np.where(passS_first | (~caught), "S", "F")
cost_casc = np.where(tier_used == "S", call_cost("S"), call_cost("S") + call_cost("F"))
pass_casc = np.where(tier_used == "S", passS_first, rng.random(n) < pF)          # escalated items get the frontier's chance
res = savings_and_retention(costF, cost_casc, passBase.astype(int), pass_casc.astype(int), rng=rng)
esc = float((tier_used == "F").mean())
print(f"cascade: escalation {esc:.2f}; saving {res['saving_pct'][0]}% (95% {res['saving_pct'][1]}–{res['saving_pct'][2]}); retention diff {res['retention_diff'][0]} ({res['retention_diff'][1]} to {res['retention_diff'][2]})")
ok &= res["saving_pct"][1] > 0 and res["retention_diff"][1] <= 0 <= res["retention_diff"][2] or res["retention_diff"][0] > -0.03
# 3. classifier routing at two accuracies
for acc in (0.8, 0.95):
    tiers = np.array([route_classifier("draft", bool(h), acc, rng) for h in hard])
    cost_cl = np.where(tiers == "S", call_cost("S"), call_cost("F")); pass_cl = np.where(tiers == "S", rng.random(n) < pS, rng.random(n) < pF)
    r = savings_and_retention(costF, cost_cl, passBase.astype(int), pass_cl.astype(int), rng=rng)
    print(f"classifier acc {acc}: routed-to-S {float((tiers=='S').mean()):.2f}; saving {r['saving_pct'][0]}% ({r['saving_pct'][1]}–{r['saving_pct'][2]}); retention diff {r['retention_diff'][0]} ({r['retention_diff'][1]} to {r['retention_diff'][2]})")
    if acc == 0.8: ok &= r["retention_diff"][0] < -0.02          # silent degradation visible
# 4. gateway cap and fallback
gw = Gateway(task_budget_usd=0.05, availability={"F": True, "S": True, "ONSITE": True}); n_calls = 0
try:
    while True: gw.call("F", "plan", lambda t: "ok", reasoning=2000); n_calls += 1
except RuntimeError as e: print(f"runaway loop stopped by cap after {n_calls} high-effort calls: {e}")
ok &= n_calls == 1
gw2 = Gateway(0.5, {"F": False, "S": True, "ONSITE": True}); out = gw2.call("F", "plan", lambda t: t); print(f"frontier unavailable → served by {out}; recorded fell_back={gw2.calls[-1]['fell_back']}"); ok &= gw2.calls[-1]["fell_back"]
# 5. availability
print(f"API 99.9% → {d['api_downtime_min_per_month_3nines']} min/month down; with on-site 99%: {d['effective_availability_with_onsite_99pct']}"); ok &= abs(d["effective_availability_with_onsite_99pct"] - 0.99999) < 1e-9
json.dump({"cascade": res, "escalation": esc, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 23:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
