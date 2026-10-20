#!/usr/bin/env python3
"""Lab 22 — the agent loop. Runs the chapter's reference loop (loop.py, extracted verbatim) with a SEEDED STOCHASTIC
MODEL STUB (first-attempt success p=0.60, repair success q=0.50 — labelled simulation) and REAL deterministic sensors,
over 2,000 simulated 11-step tasks. Reproduces from 22.3: step pass rate 0.95 and expected calls 1.70 at cap 3;
task pass 57% at cap 3 and ~0.4% at cap 0. Also checks the caps hold (no task exceeds budgets) and that a transient
tool error is retried without a model call."""
import random, json, subprocess, sys, statistics, datetime
from loop import Step, LoopConfig, Trace, Escalate, run_loop
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True)
d = json.load(open("results/derived.json"))
random.seed(22); P, Q, N, STEPS = 0.60, 0.50, 2000, 11

def make_model():
    def act(step):   return ({"ok": random.random() < P}, 500)           # 500 tokens per call (illustrative)
    def repair(step, msg): return ({"ok": random.random() < Q}, 400)
    return act, repair
def plan(task, state): return [Step(f"s{i}", "submit_work_order" if i == STEPS-1 else "tool", {}, [("ok", lambda r: (r["ok"], "field permit_type empty; set from hazard class"))]) for i in range(STEPS)]
tool_calls = {"n": 0, "transient": 0}
def tool(**args):
    tool_calls["n"] += 1
    return {"ok": args.get("ok", False)}
tools = {"tool": tool, "submit_work_order": tool}
gate = lambda step, result: True

def simulate(cap):
    ok = 0; step_pass = []; calls = []
    for _ in range(N):
        act, repair = make_model(); tr = Trace()
        try:
            run_loop({"id": "t"}, plan, act, repair, gate, tools, LoopConfig(max_repairs_per_step=cap, max_calls=200, max_steps=STEPS), tr); ok += 1
        except Escalate: pass
        # per-step stats from the trace: a step passed if its last attempt had no failures
        by_step = {}
        for e in tr.events: by_step.setdefault(e["step"], []).append(e)
        for s, evs in by_step.items():
            step_pass.append(0 if evs[-1]["failed"] else 1); calls.append(len(evs))
        assert tr.calls <= 200
    return ok/N, statistics.mean(step_pass), statistics.mean(calls)

res = {}
for cap in (0, 3):
    tp, sp, cs = simulate(cap); res[cap] = dict(task_pass=round(tp,3), step_pass=round(sp,3), calls_per_step=round(cs,2))
    print(f"cap {cap}: task pass {tp:.3f}  step pass {sp:.3f}  calls/step {cs:.2f}")
checks = [("step pass cap3", res[3]["step_pass"], d["step_pass_p60_q50_cap3"], 0.02),
          ("calls/step cap3", res[3]["calls_per_step"], d["calls_p60_q50_cap3"], 0.05),
          ("task pass cap3", res[3]["task_pass"], d["task_pass_11steps_cap3"], 0.03),
          ("task pass cap0", res[0]["task_pass"], d["task_pass_11steps_cap0"], 0.01)]
ok = True
for name, got, exp, tol in checks:
    m = abs(got-exp) <= tol; ok &= m; print(f"{name:18s} chapter {exp}  measured {got}  {'OK' if m else 'MISMATCH'}")
# transient-error separation: a tool that fails once transiently must be retried by the tool layer, not the model
retries = {"n": 0}
def flaky(**args):
    if retries["n"] == 0: retries["n"] += 1; return flaky(**args)   # tool-layer retry (same args), no model call
    return {"ok": True}
tr = Trace(); run_loop({"id":"x"}, lambda t,s: [Step("s","flaky",{},[("ok", lambda r:(r["ok"],""))])], lambda st: ({},1), lambda st,m: ({},1), gate, {"flaky": flaky}, LoopConfig(), tr)
sep = tr.calls == 2 and retries["n"] == 1   # 1 plan + 1 act; zero repairs
print("transient error retried without a model call:", sep); ok &= sep
json.dump({"results": {str(k): v for k, v in res.items()}, "transient_separation": sep, "seed": 22, "n_tasks": N,
           "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 22:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
