#!/usr/bin/env python3
"""Lab 28 — Permissions, policy, security.
Reproduces from Chapter 28: (1) zero false-deny and zero false-allow on the golden set of benign and forbidden
tool calls; (2) in-process PDP decision latency p50/p95/p99 over 1,000 synthetic requests (chapter target: p99 < 10 ms);
(3) fail-closed behavior when the engine is unavailable; (4) audit chain verification and tamper detection.
CPU only; no model, no network. Set OPA_URL to also measure a sidecar (optional)."""
import time, json, random, statistics, platform, datetime, sys, copy
import pdp   # the chapter's reference implementation, extracted verbatim

random.seed(28)
ok = True

# 1. Golden set (from the chapter) + generated near-twins
golden = list(pdp.GOLDEN)
base = {"principal":{"id":"t1","roles":["technician","writer"],"unit":"U3"},"actor":{"id":"maintenance-agent"},
        "tool":{"name":"submit_work_order","risk":"write"},"args":{"order_id":"WO-9","zone":"Z1","permit":"none"},
        "context":{"validated":True,"writes_so_far":0,"time":1000}}
golden.append((copy.deepcopy(base),"allow"))
twin=copy.deepcopy(base); twin["context"]["writes_so_far"]=3; golden.append((twin,"deny"))              # budget exhausted
twin=copy.deepcopy(base); twin["principal"]["roles"]=["technician"]; golden.append((twin,"deny"))           # no writer role
twin=copy.deepcopy(base); twin["args"]["zone"]="Z7"; golden.append((twin,"escalate"))                       # restricted zone
twin=copy.deepcopy(base); twin["args"]["zone"]="Z7"; twin["context"]["approval"]={"role":"supervisor","expires":2000}; golden.append((twin,"allow"))
twin=copy.deepcopy(base); twin["args"]["zone"]="Z7"; twin["context"]["approval"]={"role":"supervisor","expires":900}; golden.append((twin,"escalate"))  # expired approval
twin=copy.deepcopy(base); twin["tool"]={"name":"delete_everything","risk":"destructive"}; golden.append((twin,"deny"))  # unknown tool
fd=fa=0
for req,exp in golden:
    got=pdp.decide(req).effect
    if exp=="allow" and got!="allow": fd+=1
    if exp!="allow" and got=="allow": fa+=1
    if got!=exp: print("  MISMATCH", req["tool"]["name"], req["args"], "expected", exp, "got", got)
print(f"golden set: {len(golden)} cases, false-deny {fd}, false-allow {fa}")
ok &= (fd==0 and fa==0)

# 2. Latency over 1,000 synthetic requests spanning all rules
reqs=[]
tools=list(pdp.TOOL_META)+["unknown_tool"]
for i in range(1000):
    r=copy.deepcopy(base); r["tool"]={"name":random.choice(tools),"risk":"write"}
    r["args"]["zone"]=random.choice(["Z1","Z3","Z7"]); r["context"]["validated"]=random.random()<0.7
    r["context"]["writes_so_far"]=random.randint(0,4); r["principal"]["unit"]=random.choice(["U3","U7"])
    reqs.append(r)
lat=[]
for r in reqs:
    t0=time.perf_counter(); pdp.decide(r); lat.append((time.perf_counter()-t0)*1e3)
lat.sort(); p50=statistics.median(lat); p95=lat[int(0.95*len(lat))-1]; p99=lat[int(0.99*len(lat))-1]
print(f"in-process PDP latency ms: p50 {p50:.4f}  p95 {p95:.4f}  p99 {p99:.4f}  (chapter target p99 < 10 ms)")
ok &= p99 < 10

# 3. Fail-closed: point OPA_URL at a dead port
import os
os.environ["OPA_URL"]="http://127.0.0.1:9"
d=pdp.decide(base); print("engine unavailable →", d.effect, d.rule)
ok &= d.effect=="deny"
del os.environ["OPA_URL"]

# 4. Audit chain: run guarded tool, verify, tamper, re-verify
pdp.AUDIT.clear()
for req,_ in golden[:6]:
    try: pdp.submit_work_order(principal=req["principal"], actor=req["actor"], context=req["context"], **req["args"]) if req["tool"]["name"]=="submit_work_order" else None
    except pdp.PolicyDenied: pass
good,msg=pdp.verify_chain(pdp.AUDIT); print("audit chain:", msg)
tampered=copy.deepcopy(pdp.AUDIT); tampered[1]["effect"]="allow"
bad,msg2=pdp.verify_chain(tampered); print("after tampering record 1:", msg2)
ok &= good and not bad

json.dump({"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),"python":platform.python_version(),
           "golden_cases":len(golden),"false_deny":fd,"false_allow":fa,"latency_ms":{"p50":p50,"p95":p95,"p99":p99},
           "fail_closed":d.effect=="deny","chain_verified":good,"tamper_detected":not bad},
          open("results/run.json","w"),indent=2)
print("results/run.json written"); sys.exit(0 if ok else 1)
