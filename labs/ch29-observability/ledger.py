import json, hashlib, time
from collections import defaultdict

EVIDENTIARY = {"decision", "tool_call", "intervention", "diff"}

class Ledger:
    """Collects the seven record types; chains the evidentiary ones; serves replay, export, and attribution."""
    def __init__(self):
        self.records = []; self.head = "0"

    def emit(self, kind: str, task_id: str, **fields):
        rec = {"kind": kind, "task_id": task_id, "ts": time.time(), **fields}
        if kind == "span":                       # text is a droppable event, never a span attribute
            rec["events"] = [{"name": "content", "text": fields.pop("text", "")}] if "text" in fields else []
            rec.pop("text", None)
        if kind in EVIDENTIARY:
            rec["prev_hash"] = self.head
            rec["hash"] = hashlib.sha256(json.dumps(rec, sort_keys=True).encode()).hexdigest()
            self.head = rec["hash"]
        self.records.append(rec)
        return rec

    def verify_chain(self):
        prev = "0"
        for i, r in enumerate(r for r in self.records if r["kind"] in EVIDENTIARY):
            body = dict(r); h = body.pop("hash")
            if body["prev_hash"] != prev: return False, f"record {i}: prev_hash mismatch"
            if hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest() != h: return False, f"record {i}: hash mismatch"
            prev = h
        return True, "chain verified"

    def strip_text(self):
        """Collector-side redaction: drop content events, keep every attribute."""
        for r in self.records:
            if r["kind"] == "span": r["events"] = []

    def replay(self, task_id: str):
        """Reconstruction: the task's records in order, joined by step."""
        recs = sorted((r for r in self.records if r["task_id"] == task_id), key=lambda r: r["ts"])
        by_step = defaultdict(list)
        for r in recs: by_step[r.get("step", -1)].append(r)
        return dict(by_step)

    def completeness(self, task_id: str):
        """Every tool call must have a decision record and a span; report gaps."""
        recs = [r for r in self.records if r["task_id"] == task_id]
        calls = {r["step"] for r in recs if r["kind"] == "tool_call"}
        decided = {r["step"] for r in recs if r["kind"] == "decision"}
        spanned = {r["step"] for r in recs if r["kind"] == "span"}
        return {"tool_calls": len(calls), "missing_decision": sorted(calls - decided), "missing_span": sorted(calls - spanned)}

    def cost_by(self, *keys):
        """Attribution: sum cost over any combination of tag keys; report untagged share."""
        totals = defaultdict(float); untagged = 0.0; total = 0.0
        for r in self.records:
            if r["kind"] != "span": continue
            total += r.get("cost", 0.0)
            if all(k in r for k in keys): totals[tuple(r[k] for k in keys)] += r.get("cost", 0.0)
            else: untagged += r.get("cost", 0.0)
        return dict(totals), (untagged / total if total else 0.0)
