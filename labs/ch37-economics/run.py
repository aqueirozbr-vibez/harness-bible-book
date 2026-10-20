#!/usr/bin/env python3
"""Lab 37 — reproduces Table 37.1 and the break-even figures from Chapter 37 by running derive.py
and checking against the chapter's stated values. Optional: --gateway export.csv re-runs the anatomy on real usage."""
import json, subprocess, sys
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True)
d = json.load(open("results/derived.json"))
stated = {"A": 810, "B": 540, "C": 238, "D": 5675, "saving_A_to_C_pct": 70.7, "breakeven_vs_B_x": 10.5, "breakeven_vs_C_x": 23.9, "C_total_route70": 305, "D_total_ops2.0": 8731, "saving_A_to_C_route70_pct": 62.4}
ok = True
for k, v in stated.items():
    got = round(d[k]["total"]) if k in ("A","B","C","D") else d[k]
    match = abs(got - v) <= max(1, 0.01 * v); ok &= match
    print(f"{k}: chapter {v}  derived {got}  {'OK' if match else 'MISMATCH'}")
print("Lab 37:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
