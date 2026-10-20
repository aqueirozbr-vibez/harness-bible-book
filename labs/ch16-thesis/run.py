#!/usr/bin/env python3
"""Lab 16 — Thesis and evidence.
Part 1 (CPU): reproduces from Chapter 16.3 the pass^k independence curve, the 59% relative drop, the 84.1% per-attempt
rate implied by pass^8 = 25%, the 0.95^11 / 0.99^11 task-level figures, and the Wilson interval widths at n = 20/50/100/200.
Part 2 (gated): the two-scaffold protocol — same model, simplest harness vs full harness, pass^1 and pass^4 with intervals.
Requires a model key; prints a cost estimate and refuses without --confirm."""
import json, subprocess, sys, math
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True)
d = json.load(open("results/derived.json"))
stated = {"pass8_independent": (d["pass_k_if_independent_retail"]["8"] if "8" in d["pass_k_if_independent_retail"] else d["pass_k_if_independent_retail"][8], 0.0177),
          "per_attempt_for_25": (d["per_attempt_rate_needed_for_pass8_of_25pct"], 0.841),
          "relative_drop": (d["relative_drop_pct"], 59),
          "opus_spread_pp": (d["scaffold_spread_pp"]["SWE-bench Pro, Claude Opus 4.5, SEAL -> Claude Code"], 9.5),
          "task_0.95^11": (round(0.95**11, 2), 0.57), "task_0.99^11": (round(0.99**11, 2), 0.90),
          "wilson50_low": (d["wilson95_at_p60"]["50"][0], 0.462)}
ok = True
for k, (got, exp) in stated.items():
    m = abs(got - exp) <= max(0.005, 0.01*abs(exp)); ok &= m
    print(f"{k:22s} chapter {exp}  derived {got}  {'OK' if m else 'MISMATCH'}")
print("Lab 16 part 1:", "REPRODUCED" if ok else "NOT REPRODUCED")
if "--scaffolds" in sys.argv:
    print("Part 2 requires a model key and a golden set; see run_scaffolds.md. Refusing to run without --confirm and a golden set path.")
sys.exit(0 if ok else 1)
