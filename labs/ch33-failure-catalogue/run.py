#!/usr/bin/env python3
"""Lab 33 — Failure catalogue. Runs the chapter's detectors (detectors.py, extracted verbatim). For each of the fifteen
modes: a clean reference input (must not fire) and an injected input (must fire, naming the mode). Also: the sixteenth
invariant (no write tool may target the historian/controller in the registry) and the "seven chapters" count of F01
across the book's failure tables."""
import json, sys, subprocess, datetime, glob, os, re
import detectors as D
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
task = {"scope": {"P-101-U3"}, "external_comms": False, "plan_tools": {"read_procedure", "draft_work_order"}}
cases = [
 ("F01", lambda: D.detect_citation({"citations": [{"doc": "MP-0417", "rev": 7, "span": "hot-work permit is required"}]}), lambda: D.detect_citation({"citations": [{"doc": "MP-0417", "rev": 7, "span": "torque to 60 Nm"}]})),
 ("F02", lambda: D.detect_identity({"text": "Replace seal on P-101-U3"}, task), lambda: D.detect_identity({"text": "Replace seal on P-107-U3"}, task)),
 ("F03", lambda: D.detect_citation({"citations": [{"doc": "MP-0417", "rev": 7}]}), lambda: D.detect_citation({"citations": [{"doc": "MP-0417", "rev": 6}]})),
 ("F04", lambda: D.detect_intent({"name": "read_procedure"}, task), lambda: D.detect_intent({"name": "notify"}, task)),
 ("F05", lambda: D.detect_intent({"name": "draft_work_order", "asset": "P-101-U3"}, task), lambda: D.detect_intent({"name": "draft_work_order", "asset": "P-102-U3"}, task)),
 ("F06", lambda: D.detect_routing((-0.01, 0.02)), lambda: D.detect_routing((-0.06, -0.02))),
 ("F07", lambda: D.detect_window({"results": 900, "history": 500}, {"results": 1000, "history": 600}), lambda: D.detect_window({"results": 8000, "history": 500}, {"results": 1000, "history": 600})),
 ("F08", lambda: D.detect_memory({"provenance": ["t1"], "reviewed_by": "r"}), lambda: D.detect_memory({"provenance": [], "reviewed_by": None})),
 ("F09", lambda: D.detect_repair(2, 3, True), lambda: D.detect_repair(2, 3, False)),
 ("F10", lambda: D.detect_duplicate([{"idempotency_key": "t/6"}, {"idempotency_key": "t/8"}]), lambda: D.detect_duplicate([{"idempotency_key": "t/8"}, {"idempotency_key": "t/8"}])),
 ("F11", lambda: D.detect_grader(0.71, 0.05), lambda: D.detect_grader(0.54, 0.05)),
 ("F12", lambda: D.detect_gate(240, 0.9), lambda: D.detect_gate(18, 0.9)),
 ("F13", lambda: D.detect_abstention({"value": None, "refused": False}, corpus_answers=False), lambda: D.detect_abstention({"value": "60 Nm"}, corpus_answers=False)),
 ("F14", lambda: D.detect_cache("h1", "h1", 0.9), lambda: D.detect_cache("h1", "h2", 0.0)),
 ("F15", lambda: D.detect_secret(["[result read#1] rows"]), lambda: D.detect_secret(["system: use key tok_0123456789abcdef"])),
]
ok = True; rows = []
for mode, clean, injected in cases:
    c, i = clean(), injected(); good = (c is None) and (i is not None and i.startswith(mode.split("/")[0]) or (i is not None and mode in i))
    rows.append((mode, c, i)); ok &= good
    print(f"{mode}: clean → {c}; injected → {i}  [{'ok' if good else 'FAIL'}]")
# sixteenth invariant
REGISTRY_WRITE_TOOLS = {"draft_work_order": "cmms-draft", "submit_work_order": "cmms-api"}
violation = [t for t, host in REGISTRY_WRITE_TOOLS.items() if host in ("historian", "dcs", "plc", "sis")]
print("sixteenth invariant: write tools targeting OT:", violation or "none"); ok &= not violation
# 'seven chapters' count: chapters whose failure tables mention citation failures
n = sum(1 for f in glob.glob(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "book", "part*", "ch*.md")) if re.search(r"\| [^|]*(citation|cited)[^|]*\|", open(f).read(), flags=re.I) and "## " in open(f).read() and re.search(r"## \d\d?\.5 Failure", open(f).read()))
print(f"chapters with a citation-related failure row: {n} (chapter cites this count)"); ok &= n >= 20
print(f"catalogue: {d['count']} modes; deterministic {d['deterministic_detection']}; inferential/human {d['needs_inferential_or_human']}; before {d['total_before']} → after {d['total_after']} per 1,000 (illustrative)")
json.dump({"rows": rows, "citation_chapters": n, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 33:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
