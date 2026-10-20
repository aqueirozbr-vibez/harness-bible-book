#!/usr/bin/env python3
"""Lab 29 — Observability and audit. Runs the chapter's Ledger (ledger.py, extracted verbatim) over 200 simulated tasks
shaped like the scenario (13 spans, 11 tool calls with decisions, 12 transitions, 1 intervention, 1 diff).
Reproduces: 49 records per task; chain verifies and a tampered record is detected; strip_text removes every content
event and no attribute; completeness reports a component that forgot to record; replay reconstructs a task by step;
cost_by attributes 100% when tags come from the task record and reports the untagged share when they do not."""
import json, random, sys, datetime, subprocess
from ledger import Ledger, EVIDENTIARY
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(29); L = Ledger(); N = 200; ok = True
def emit_task(L, tid, forget_decision_at=None, untag=False):
    tags = {} if untag else {"use_case": "maintenance", "team": "EA&D", "env": "prod"}
    L.emit("span", tid, step=0, op="plan", model="frontier", route="planner", tokens=800, cost=0.01, text="PLAN PROMPT TEXT", **tags)
    for s in range(1, 12):
        L.emit("span", tid, step=s, op="act", model="small" if s <= 3 else "frontier", route="router", tokens=500, cost=0.003, text="STEP PROMPT", **tags)
        if s != forget_decision_at: L.emit("decision", tid, step=s, effect="allow", rule="read_in_unit", principal="tech-4471", actor="maintenance-agent")
        L.emit("tool_call", tid, step=s, tool="read" if s < 8 else "submit_work_order", args_hash="a1", result_hash="r1")
        L.emit("transition", tid, step=s, frm="Verify", to="Submit")
    L.emit("span", tid, step=6, op="repair", model="frontier", route="router", tokens=400, cost=0.004, text="REPAIR", **tags)
    L.emit("transition", tid, step=6, frm="Verify", to="Repair")
    L.emit("intervention", tid, step=8, action="approval", by="supervisor-S", reason="scheduled for day shift", wait_h=14.33)
    L.emit("diff", tid, step=8, key=f"{tid}/8", before=None, after="WO created")
for t in range(N): emit_task(L, f"t{t}")
per_task = len(L.records)/N; print(f"records per task: {per_task:.0f} (chapter: {d['records_per_task']})"); ok &= per_task == d["records_per_task"]
good, msg = L.verify_chain(); print("chain:", msg); ok &= good
import copy; tampered = copy.deepcopy(L); tampered.records[[i for i,r in enumerate(tampered.records) if r["kind"]=="decision"][5]]["effect"] = "deny"
bad, msg2 = tampered.verify_chain(); print("after tampering a decision record:", msg2); ok &= not bad
n_text = sum(1 for r in L.records if r["kind"]=="span" and r["events"]); attrs_before = sum(len(r) for r in L.records)
L.strip_text(); n_text_after = sum(1 for r in L.records if r["kind"]=="span" and r["events"]); attrs_after = sum(len(r) for r in L.records)
print(f"text events before/after strip: {n_text}/{n_text_after}; attribute count unchanged: {attrs_before==attrs_after}"); ok &= n_text_after==0 and attrs_before==attrs_after
comp = L.completeness("t0"); print("completeness t0:", comp); ok &= comp["missing_decision"]==[] and comp["missing_span"]==[]
emit_task(L, "forgetful", forget_decision_at=8); comp2 = L.completeness("forgetful"); print("completeness with a forgetful component:", comp2); ok &= comp2["missing_decision"]==[8]
rp = L.replay("t0"); print(f"replay t0: {len(rp)} steps; step 6 records: {[r['kind'] for r in rp[6]]}"); ok &= 6 in rp and any(r["kind"]=="transition" and r["to"]=="Repair" for r in rp[6])
totals, untagged = L.cost_by("use_case", "team"); print(f"attribution by (use_case, team): {dict(totals)}; untagged share {untagged:.3f}"); ok &= untagged < 0.005
emit_task(L, "untagged", untag=True); _, untagged2 = L.cost_by("use_case", "team"); print(f"after one untagged task, untagged share {untagged2:.4f} > 0: {untagged2>0}"); ok &= untagged2 > 0
json.dump({"tasks": N, "records_per_task": per_task, "chain": good, "tamper_detected": not bad, "strip_ok": n_text_after==0, "completeness_gap_found": comp2["missing_decision"],
           "untagged_share": untagged, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 29:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
