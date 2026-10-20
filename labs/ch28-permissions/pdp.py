import os, json, time, hashlib, urllib.request
from dataclasses import dataclass, field

RESTRICTED_ZONES = {"Z3", "Z7"}
TOOL_META = {"search_documents": {"risk": "read", "unit": "U3"},
             "validate_work_order": {"risk": "read", "unit": "U3"},
             "preview_work_order": {"risk": "read", "unit": "U3"},
             "submit_work_order": {"risk": "write", "unit": "U3"}}

@dataclass
class Decision:
    effect: str; rule: str; reason: str = ""; obligations: list = field(default_factory=list); trace_id: str = ""

class PolicyDenied(Exception):
    def __init__(self, d: Decision): super().__init__(d.reason); self.decision = d

def _local_pdp(req: dict) -> Decision:
    """Mirror of the Rego bundle; fail-closed by construction."""
    tool, args, ctx, p = req["tool"], req["args"], req["context"], req["principal"]
    meta = TOOL_META.get(tool["name"])
    if meta is None:
        return Decision("deny", "unknown_tool", "Tool is not registered.")
    if meta["risk"] == "write" and ctx.get("writes_so_far", 0) >= 3:
        return Decision("deny", "write_budget", "Write budget for this task is exhausted; escalate to a human.")
    if tool["name"] == "submit_work_order":
        if not ctx.get("validated"):
            return Decision("deny", "validate_before_submit", "Run validate_work_order before submit_work_order.")
        if args.get("zone") in RESTRICTED_ZONES:
            ap = ctx.get("approval") or {}
            if ap.get("role") == "supervisor" and ap.get("expires", 0) > ctx["time"]:
                return Decision("allow", "restricted_zone_write_approved")
            return Decision("escalate", "restricted_zone_write",
                            "Work-order submission for zone Z3 requires supervisor approval. Request approval; do not resubmit.",
                            ["approver:supervisor", "ttl:3600"])
        return Decision("allow", "write_with_role") if "writer" in p["roles"] else \
               Decision("deny", "write_role_required", "Submission requires the writer role.")
    if meta["risk"] == "read" and p["unit"] == meta["unit"]:
        return Decision("allow", "read_in_unit")
    return Decision("deny", "default_deny", "No policy permits this call.")

def _opa_pdp(req: dict) -> Decision:
    body = json.dumps({"input": req}).encode()
    r = urllib.request.Request(os.environ["OPA_URL"] + "/v1/data/harness/tools/decision",
                               data=body, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(r, timeout=0.5) as resp:      # timeout → exception → deny
        d = json.load(resp)["result"]
    return Decision(d["effect"], d["rule"], d.get("reason", ""), d.get("obligations", []))

def decide(req: dict) -> Decision:
    try:
        d = _opa_pdp(req) if os.environ.get("OPA_URL") else _local_pdp(req)
    except Exception as e:                                   # fail closed on any PDP failure
        d = Decision("deny", "pdp_unavailable", f"Policy engine unavailable ({type(e).__name__}); call refused.")
    d.trace_id = hashlib.sha256(json.dumps(req, sort_keys=True).encode()).hexdigest()[:12]
    return d

AUDIT = []
def guard(tool_name: str):
    def wrap(fn):
        def inner(*, principal, actor, context, **args):
            req = {"principal": principal, "actor": actor,
                   "tool": {"name": tool_name, "risk": TOOL_META.get(tool_name, {}).get("risk", "unknown")},
                   "args": args, "context": context}
            t0 = time.perf_counter(); d = decide(req); dt = time.perf_counter() - t0
            AUDIT.append({"trace_id": d.trace_id, "tool": tool_name, "effect": d.effect, "rule": d.rule,
                          "principal": principal["id"], "actor": actor["id"], "latency_ms": dt * 1e3,
                          "prev_hash": AUDIT[-1]["hash"] if AUDIT else "0"})
            AUDIT[-1]["hash"] = hashlib.sha256(json.dumps(AUDIT[-1], sort_keys=True).encode()).hexdigest()
            if d.effect != "allow":
                raise PolicyDenied(d)
            return fn(**args)
        return inner
    return wrap

@guard("submit_work_order")
def submit_work_order(order_id: str, zone: str, permit: str) -> str:
    return f"created {order_id}"


def verify_chain(records):
    prev = "0"
    for i, r in enumerate(records):
        expected = dict(r); h = expected.pop("hash")
        if expected["prev_hash"] != prev:
            return False, f"record {i}: prev_hash mismatch"
        if hashlib.sha256(json.dumps(expected, sort_keys=True).encode()).hexdigest() != h:
            return False, f"record {i}: hash mismatch"
        prev = h
    return True, f"{len(records)} records verified"


GOLDEN = [
  ({"principal":{"id":"t1","roles":["technician","writer"],"unit":"U3"},"actor":{"id":"maintenance-agent"},
    "tool":{"name":"submit_work_order","risk":"write"},"args":{"order_id":"WO-1","zone":"Z1","permit":"none"},
    "context":{"validated":True,"writes_so_far":0,"time":1000}}, "allow"),
  ({"principal":{"id":"t1","roles":["technician"],"unit":"U3"},"actor":{"id":"maintenance-agent"},
    "tool":{"name":"submit_work_order","risk":"write"},"args":{"order_id":"WO-2","zone":"Z3","permit":"hot_work"},
    "context":{"validated":True,"writes_so_far":0,"time":1000}}, "escalate"),
  ({"principal":{"id":"t1","roles":["technician"],"unit":"U3"},"actor":{"id":"maintenance-agent"},
    "tool":{"name":"submit_work_order","risk":"write"},"args":{"order_id":"WO-3","zone":"Z3","permit":"hot_work"},
    "context":{"validated":False,"writes_so_far":0,"time":1000}}, "deny"),
  ({"principal":{"id":"t9","roles":["technician"],"unit":"U7"},"actor":{"id":"maintenance-agent"},
    "tool":{"name":"search_documents","risk":"read"},"args":{"q":"seal"},
    "context":{"time":1000}}, "deny"),
]

def test_golden():
    for req, expected in GOLDEN:
        assert decide(req).effect == expected, (req["tool"]["name"], expected, decide(req).effect)
