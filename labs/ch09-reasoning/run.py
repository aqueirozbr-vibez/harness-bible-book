#!/usr/bin/env python3
"""Lab 09 — Reasoning and test-time compute. Runs the chapter's code (reasoning.py, extracted verbatim) and checks it
against Monte Carlo simulation (seed 9, 20,000 trials): majority-vote accuracy, coverage, and best-of-N with an imperfect
verifier; then reproduces the 09.3 tables and the reasoning-sandwich allocation for the P-101 task."""
import json, sys, subprocess, datetime, random
from reasoning import majority_vote_accuracy, coverage, best_of_n, allocate_effort, EFFORT
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(9); T = 20000; ok = True
def sim_majority(p, k): return sum(sum(random.random() < p for _ in range(k)) > k // 2 for _ in range(T)) / T
def sim_coverage(p, n): return sum(any(random.random() < p for _ in range(n)) for _ in range(T)) / T
def sim_bestofn(p, n, tpr, fpr):
    hits = 0
    for _ in range(T):
        chosen = None
        samples = [random.random() < p for _ in range(n)]
        for c in samples:
            if (c and random.random() < tpr) or ((not c) and random.random() < fpr): chosen = c; break
        if chosen is None: chosen = random.choice(samples)
        hits += chosen
    return hits / T
for p, k in ((0.6, 5), (0.6, 21), (0.7, 11)):
    f, s = majority_vote_accuracy(p, k), sim_majority(p, k); m = abs(f - s) < 0.015 and abs(f - d[f"majority_p{p}_k{k}"]) < 1e-3; ok &= m
    print(f"majority p={p} k={k:2d}: formula {f:.3f}  simulated {s:.3f}  chapter {d[f'majority_p{p}_k{k}']}  {'OK' if m else 'MISMATCH'}")
for p, n in ((0.3, 4), (0.3, 16)):
    f, s = coverage(p, n), sim_coverage(p, n); m = abs(f - s) < 0.015; ok &= m
    print(f"coverage p={p} n={n:2d}: formula {f:.3f}  simulated {s:.3f}  {'OK' if m else 'MISMATCH'}")
for w in (0.0, 0.2, 0.5):
    f, s = best_of_n(0.3, 16, 0.9, w), sim_bestofn(0.3, 16, 0.9, w); m = abs(f - s) < 0.02 and abs(f - d[f"bestof16_p0.3_v0.9_w{w}"]) < 1e-3; ok &= m
    print(f"best-of-16 p=0.3 tpr=0.9 fpr={w}: formula {f:.3f}  simulated {s:.3f}  chapter {d[f'bestof16_p0.3_v0.9_w{w}']}  {'OK' if m else 'MISMATCH'}")
steps = [("read0","routine"),("read1","routine"),("read2","routine"),("plan","plan"),("draft","routine"),("validate","routine"),("permit","verify"),("preview","routine"),("submit","routine"),("notify","routine"),("report","routine")]
a = allocate_effort(steps); m = a["reasoning_tokens"] == d["sandwich_reasoning_tokens_per_task"] and a["all_high_tokens"] == d["all_high_reasoning_tokens_per_task"]; ok &= m
print(f"sandwich: {a['reasoning_tokens']} reasoning tokens vs all-high {a['all_high_tokens']} (saving {100*(1-a['reasoning_tokens']/a['all_high_tokens']):.0f}%) {'OK' if m else 'MISMATCH'}")
for R, exp in ((2000, 6.0), (8000, 21.0)):
    got = (400 + R) / 400; m = abs(got - exp) < 0.05; ok &= m; print(f"cost multiplier at {R} reasoning tokens: {got:.1f}× (chapter {exp}) {'OK' if m else 'MISMATCH'}")
json.dump({"trials": T, "sandwich": a, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 09:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
