#!/usr/bin/env python3
"""Lab 26 — Sensors and verification. Runs the chapter's sensor chain (sensors.py, extracted verbatim) on a synthetic
golden set (seed 26) of 2,000 work-order drafts: 60% correct, 40% with exactly one seeded defect, one class per sensor.
Reproduces: 0 false positives on correct drafts; per-sensor false-negative rate on its target defect = 0; cheap-first
ordering stops defective drafts before the (simulated) grader; every failure message names the field and the fix and
contains no artifact text beyond field names and values."""
import random, json, statistics, sys, datetime, subprocess
from sensors import run_chain, WORK_ORDER_SENSORS, Sensor
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True)
random.seed(26); N = 2000
REFS = {"procedures": {"MP-0417": {"current_rev": 7, "hazard_class": "H"}, "MP-0099": {"current_rev": 3, "hazard_class": "M"}},
        "bom": {"SEAL-88", "GASKET-12", "BOLT-M16"}, "zones": {"Z1", "Z2", "Z3", "Z7"}}
def good():
    proc = random.choice(list(REFS["procedures"]))
    return {"order_id": f"WO-{random.randint(1000,9999)}", "equipment_tag": "P-101", "zone": random.choice(list(REFS["zones"])),
            "description": "seal leak", "procedure_ref": proc, "procedure_rev": REFS["procedures"][proc]["current_rev"],
            "parts": random.sample(sorted(REFS["bom"]), 2), "permit_type": {"H":"hot_work","M":"cold_work"}[REFS["procedures"][proc]["hazard_class"]]}
DEFECTS = {
 "schema": lambda a: (a.pop("permit_type"), a)[1],
 "zone_registered": lambda a: dict(a, zone="Z9"),
 "citation": lambda a: dict(a, procedure_rev=a["procedure_rev"]-1),
 "permit_rule": lambda a: dict(a, permit_type="none"),
 "parts_in_bom": lambda a: dict(a, parts=a["parts"]+["OBSOLETE-1"]),
}
# simulated grader as the expensive last sensor: passes everything (we only measure whether it is reached)
grader = Sensor("grader", 3000, lambda a, r: (True, ""))
chain = WORK_ORDER_SENSORS + [grader]
fp = 0; n_good = 0; fn = {k: 0 for k in DEFECTS}; n_def = {k: 0 for k in DEFECTS}; reached_grader = 0; n_defective_total = 0
msgs = []
for _ in range(N):
    a = good()
    if random.random() < 0.6:
        n_good += 1; v = run_chain(chain, a, REFS)
        if any(not x.ok for x in v): fp += 1
    else:
        k = random.choice(list(DEFECTS)); n_def[k] += 1; n_defective_total += 1
        a = DEFECTS[k](dict(a)); v = run_chain(chain, a, REFS)
        failed = [x for x in v if not x.ok]
        if not failed or failed[0].sensor != k: fn[k] += 1
        else: msgs.append((k, failed[0].message))
        if any(x.sensor == "grader" for x in v): reached_grader += 1
print(f"correct drafts {n_good}: false positives {fp}")
for k in DEFECTS: print(f"  {k:16s} defective {n_def[k]:4d}  false negatives {fn[k]}")
print(f"defective drafts reaching the grader under cheap-first fail-fast: {reached_grader} of {n_defective_total}")
# message rule: names the field, under 300 chars, no artifact free-text ("seal leak") leaked into the message
rule_ok = all(("`" in m and len(m) < 300 and "seal leak" not in m) for _, m in msgs)
print(f"messages name a field, are under 300 chars, and carry no artifact free text: {rule_ok} ({len(msgs)} messages)")
# ordering: verify sensors executed cheap-first
order = [s.name for s in sorted(chain, key=lambda s: s.cost)]
print("execution order:", order)
ok = fp == 0 and all(v == 0 for v in fn.values()) and reached_grader == 0 and rule_ok and order[-1] == "grader"
json.dump({"n": N, "false_positives": fp, "false_negatives": fn, "reached_grader_when_defective": reached_grader,
           "message_rule": rule_ok, "order": order, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()},
          open("results/run.json","w"), indent=2)
print("Lab 26:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
