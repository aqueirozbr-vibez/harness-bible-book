#!/usr/bin/env python3
"""Lab 30 — Multi-agent systems. Runs the chapter's code (multiagent.py, extracted verbatim). One task (the parts
reconciliation inside the work-order task) run single-agent and multi-agent (one delegated child) — tokens and calls
compared; a simulated quality comparison with correlated vs independent checkers (stub, labelled; seed 30). Three injected
failures: (1) a delegation that tries to widen scope → intersection clamps it; (2) a child summary that leaks context and
cites outside scope → refused by the parent's sensors; (3) a child attempting a submit and a notify → denied by the
narrowest-scope policy. Also the budget carve-out and the chapter's multiplier arithmetic."""
import json, sys, subprocess, datetime, random
from multiagent import TaskRecord, delegate, check_summary, policy_allows, run_single, run_multi
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(30); ok = True
# tokens: single = 13 steps; multi = 9 parent steps + 1 child of 4 steps + 2 coordination calls
single = run_single(list(range(13))); multi = run_multi(list(range(9)), [list(range(4))])
print(f"tokens: single {single['tokens']:,} ({single['calls']} calls); multi {multi['tokens']:,} ({multi['calls']} calls); ratio {multi['tokens']/single['tokens']:.2f}× (Anthropic average 3.75×; this decomposition is small and non-overlapping)")
ok &= multi["tokens"] > single["tokens"] and multi["tokens"] / single["tokens"] < 1.5
# 1. scope intersection
parent = TaskRecord("t-2207", "tech-4471", "maintenance-agent v7", {"P-101-U3", "P-102-U3"}, "draft", False, "general", 13)
child = delegate(parent, {"P-101-U3", "P-104-U2"}, "reconciliation-specialist v3", 4, "t-2207/c1")
print(f"intersection: child scope {sorted(child.scope)} (chapter {d['intersection_example']['child']}); parent budget now {parent.budget_calls} (chapter {d['parent_calls']-d['child_calls']}); child action {child.allowed_action}; comms {child.external_comms}")
ok &= child.scope == {"P-101-U3"} and parent.budget_calls == 9 and child.allowed_action == "draft" and not child.external_comms
try: delegate(parent, {"P-101-U3"}, "x", 20, "t-2207/c2"); ok = False
except ValueError as e: print("over-budget delegation refused:", e)
# 2. summary contract
good = {"answer": "4 parts not in BOM; 2 out of stock", "support": ["P-101-U3#bom#12", "P-101-U3#stock#7"], "signals": ["sensor"], "not_found": [], "cost_calls": 4}
leaky = {"answer": "x" * 2000, "support": ["P-104-U2#bom#1"], "signals": [], "not_found": [], "cost_calls": 6}
r_good, r_leaky = check_summary(good, child), check_summary(leaky, child); print("good summary accepted:", r_good["ok"]); print("leaky summary refused:", r_leaky["problems"])
ok &= r_good["ok"] and (not r_leaky["ok"]) and len(r_leaky["problems"]) >= 3
# 3. child attempting submit / notify / out-of-scope read
tests = [("submit", "P-101-U3#WO-1", False), ("notify", "vendor", False), ("read", "P-104-U2#hist", False), ("read", "P-101-U3#hist", True)]
res = [policy_allows(child, a, t) == exp for a, t, exp in tests]; print("child policy: submit denied, notify denied, out-of-scope read denied, in-scope read allowed:", all(res)); ok &= all(res)
# quality: correlated vs independent checkers on 5,000 artifacts with a defect present 30% of the time
N = 5000; defects = [random.random() < 0.3 for _ in range(N)]
miss_corr = sum(1 for dft in defects if dft and random.random() < 0.15) / max(1, sum(defects))       # two same-family checkers: shared blind spot ~15%
miss_ind = sum(1 for dft in defects if dft and random.random() < 0.2 and random.random() < 0.2) / max(1, sum(defects))
print(f"defects missed by both checkers: correlated {miss_corr:.3f} (chapter ~{d['two_correlated_miss_illustrative']}); independent {miss_ind:.3f} (chapter {d['two_independent_miss']})")
ok &= miss_ind < miss_corr
# multiplier arithmetic
print(f"multiplier: {d['multiagent_over_single_agent_x']}× → scenario task {d['single_task_tokens']:,} → {d['multi_task_tokens_at_3.75x']:,} tokens; ${d['single_task_cost_C']} → ${d['multi_task_cost_C']}; break-even ΔQ {d['breakeven_quality_gain_pts_at_150_per_failure']} pts")
json.dump({"single": single, "multi": multi, "child_scope": sorted(child.scope), "miss": [miss_corr, miss_ind], "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 30:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
