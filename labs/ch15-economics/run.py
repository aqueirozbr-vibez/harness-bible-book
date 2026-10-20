#!/usr/bin/env python3
"""Lab 15 — Economics of models. Runs the chapter's pricing code (economics.py, extracted verbatim) and reproduces every
figure in 15.3: blended input price by hit rate, cache break-even reuses, batch blending, routed cost and saving by share,
silent-degradation arithmetic, and the self-host crossover. Also checks consistency with ch37: configuration B's per-query
cost ($540 / 60,000 = $0.009) equals query_cost with cached prefix at the scenario's shape plus the reasoning share."""
import json, sys, subprocess, datetime
from economics import blended_input_price, cache_breakeven_reuses, batch_blended_discount, query_cost, routed_cost, silent_degradation, selfhost_crossover
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
ok = True
for h in (0.0, 0.5, 0.9, 1.0):
    got = round(blended_input_price(h, 4000/6000), 4); exp = d[f"blended_input_price_h{h}_s0.67"]; m = abs(got - exp) < 1e-6; ok &= m; print(f"blended input @ hit {h}: {got} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
for w, key in ((1.25, "5min"), (2.0, "1h")):
    got = round(cache_breakeven_reuses(w), 2); exp = d[f"cache_breakeven_reuses_{key}"]; m = abs(got - exp) < 0.01; ok &= m; print(f"cache break-even @ {w}x write: {got} reuses (chapter {exp}) {'OK' if m else 'MISMATCH'}")
for b in (0.2, 0.5):
    got = batch_blended_discount(b); exp = d[f"blended_discount_batch_share_{b}"]; m = abs(got - exp) < 1e-9; ok &= m
for r in (0.0, 0.5, 0.7, 0.9, 1.0):
    got = round(routed_cost(r), 5); key = "cost_per_query_all_frontier" if r == 0 else "cost_per_query_all_small" if r == 1 else f"cost_per_query_route_{r}"; exp = d[key]; m = abs(got - exp) < 1e-5; ok &= m
    print(f"routed {int(r*100):3d}%: ${got:.5f} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
for a in (0.8, 0.95):
    got = round(silent_degradation(0.3, a, 0.5), 3); exp = d[f"added_failure_q0.3_a{a}_f0.5"]; m = abs(got - exp) < 1e-6; ok &= m; print(f"silent degradation @ router {a}: +{got} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
got = int(selfhost_crossover(4365, 0.009)); exp = d["breakeven_queries_per_month"]; m = got == exp; ok &= m; print(f"self-host crossover: {got:,} queries/month (chapter {exp:,}) {'OK' if m else 'MISMATCH'}")
# ch37 consistency: config B per query = (2000*1.25 + 4000*0.125 + 600*10)/1e6 with 600 = 400 + 0.1*2000 reasoning
b = query_cost(2000, 4000, 600, "frontier"); print(f"ch37 config B per query: ${b:.4f} (ch37: $540/60,000 = $0.0090)"); ok &= abs(b - 0.009) < 1e-6
json.dump({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 15:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
