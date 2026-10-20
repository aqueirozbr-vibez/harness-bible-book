#!/usr/bin/env python3
"""Lab 33 / derive.py — every derived number in Chapter 33."""
import json, datetime
out = {}
# The fifteen modes: id, name, family, consequence (1-5), primary detection layer, owning chapter(s)
modes = [
 ("F01","Confabulated citation","model", 4, "citation sensor (deterministic)", [13,20,26]),
 ("F02","Wrong equipment identity","representation", 5, "register + scope filter (deterministic)", [1,2,14,17]),
 ("F03","Stale revision cited","knowledge", 4, "currency filter + citation sensor", [7,20]),
 ("F04","Injection via tool result","security", 5, "intent validation + policy engine + egress", [25,28]),
 ("F05","Scope drift / unplanned action","control", 4, "plan conformance + intent validation", [17,22]),
 ("F06","Silent routing degradation","economics", 3, "retention interval per class", [15,23]),
 ("F07","Window flooding / context rot","context", 3, "assembler budget + tokens-per-step alarm", [19]),
 ("F08","Poisoned memory recurrence","memory", 4, "provenance at filing + citation sensor", [24]),
 ("F09","Retry as repair / repair loop","loop", 2, "repair cap + attempt histogram", [21,22]),
 ("F10","Duplicate write on retry","durability", 4, "idempotency key + diff sensor", [21]),
 ("F11","Uncalibrated grader","evaluation", 3, "quarterly κ + override rate", [27]),
 ("F12","Rubber-stamped approval","human", 4, "seeded items + time floor", [31]),
 ("F13","Wrong abstention (over- or under-refusal)","model", 3, "abstention threshold + golden probes", [8,13]),
 ("F14","Cache-breaking prefix drift","economics", 2, "cache hit-rate alarm + byte diff", [15,18]),
 ("F15","Credential exposure","security", 5, "secret scanner (deterministic)", [25,28]),
]
out["modes"] = [{"id":i,"name":n,"family":f,"consequence":c,"detection":d,"chapters":ch} for i,n,f,c,d,ch in modes]
out["count"] = len(modes)
out["by_family"] = {}
for i,n,f,c,d,ch in modes: out["by_family"][f] = out["by_family"].get(f,0)+1
# detection-layer split: deterministic-only vs needs inferential/human
det_only = ["F01","F02","F03","F04","F05","F07","F08","F09","F10","F14","F15"]; out["deterministic_detection"] = len(det_only); out["needs_inferential_or_human"] = 15 - len(det_only)
out["consequence_5"] = sum(1 for m in modes if m[3]==5); out["mean_consequence"] = round(sum(m[3] for m in modes)/15, 2)
# Illustrative before/after rates per 1,000 tasks (before = no harness component; after = with)
before_after = {"F01":(60,2),"F02":(150,3),"F03":(60,1),"F04":(40,0),"F05":(30,0),"F06":(80,8),"F07":(50,2),"F08":(90,0),"F09":(70,10),"F10":(5,0),"F11":(120,25),"F12":(100,15),"F13":(40,12),"F14":(300,10),"F15":(3,0)}
out["per_1000_before_after_illustrative"] = before_after
out["total_before"] = sum(v[0] for v in before_after.values()); out["total_after"] = sum(v[1] for v in before_after.values())
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items():
    if k!="modes": print(k, v)
