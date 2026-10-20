#!/usr/bin/env python3
"""Lab 24 — Memory. Runs the chapter's Memory (memory.py, extracted verbatim). Four classes exercised: working memory
written per transition and closed into an episode; consolidation over 200 synthetic episodes (seed 24) with a proposer
that emits a true fact and, for one asset, a confabulated one; document check; sampled review. Then the recurrence
measurement of 24.3: a wrong fact about P-101 injected (a) with provenance enforcement off and (b) on; 100 subsequent
tasks about P-101, 11 steps each, retrieval probability 0.2 per step; tasks touched counted. Also supersession,
retirement, and the documents-win rule."""
import json, sys, subprocess, datetime, random
from datetime import date, timedelta
from memory import Memory, Fact
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(24); rng = random; ok = True
docs = {"P-101": {"procedure MP-0417 rev 7 applies", "hazard class H"}, "P-204": {"procedure MP-0420 rev 3 applies"}}
M = Memory(docs)
# working → episodic
for t in range(200):
    tid = f"t{t}"; asset = "P-101" if t % 2 == 0 else "P-204"
    M.write_working(tid, "plan", ["read", "draft", "submit"]); M.write_working(tid, "step_3", {"status": "ok", "result_id": f"r{t}"})
    M.close_task(tid, {"asset": asset, "outcome": "approved", "note": "coupling spacer non-standard" if (asset == "P-101" and t % 10 == 0) else ""})
print(f"episodes: {len(M.episodic)}; working memory cleared: {len(M.working) == 0}"); ok &= len(M.episodic) == 200 and not M.working
# consolidation: proposer emits a true fact for episodes with the note, and a document-stated fact (should be dropped)
def propose(ep):
    out = []
    if ep.get("note"): out.append(Fact(ep["asset"], "alignment_procedure", "MP-0512 applies (non-standard spacer)", provenance=[], effective=date(2026, 8, 1)))
    out.append(Fact(ep["asset"], "procedure", "procedure MP-0417 rev 7 applies" if ep["asset"] == "P-101" else "procedure MP-0420 rev 3 applies", provenance=[]))
    return out
res = M.consolidate(propose, review=lambda f: True, sample_rate=1.0, rng=rng, require_provenance=True)
live = [f for f in M.semantic.get("P-101", []) if not f.superseded_by]
print(f"consolidation: proposed {res['proposed']}, filed {res['filed']}; document-stated candidates rejected: {sum(1 for r in M.rejections if r[2].startswith('documents'))}; live P-101 facts {len(live)} (supersession keeps one per predicate)")
ok &= res["filed"] > 0 and len(live) == 1 and any(r[2].startswith("documents") for r in M.rejections)
# recurrence: inject a wrong fact two ways, measure tasks touched over 100 tasks × 11 steps at p=0.2
def tasks_touched(mem, subject, wrong_value, p=0.2, tasks=100, steps=11):
    n = 0
    for _ in range(tasks):
        hit = False
        for _ in range(steps):
            if rng.random() < p:
                if any(f.value == wrong_value for f in mem.recall(subject)): hit = True
        n += hit
    return n
wrong = Fact("P-101", "permit", "hot-work permit NOT required", provenance=[], reviewed_by=None)
M_off = Memory(docs); M_off.file_fact(wrong, require_provenance=False); t_off = tasks_touched(M_off, "P-101", wrong.value)
M_on = Memory(docs); filed = M_on.file_fact(Fact("P-101", "permit", "hot-work permit NOT required", provenance=[], reviewed_by=None), require_provenance=True); t_on = tasks_touched(M_on, "P-101", wrong.value)
print(f"wrong fact recurrence over 100 tasks: provenance OFF → {t_off} tasks touched (chapter ~{d['expected_tasks_touched_per_100_c0.0']}); provenance ON → filed={filed}, {t_on} tasks touched (chapter {d['expected_tasks_touched_per_100_c1.0']})")
ok &= 80 <= t_off <= 100 and (not filed) and t_on == 0
# partial enforcement: 90% of filings checked
touched = 0; trials = 200
for _ in range(trials):
    Mx = Memory(docs); Mx.file_fact(Fact("P-101", "permit", wrong.value, provenance=[], reviewed_by=None), require_provenance=(rng.random() < 0.9))
    touched += tasks_touched(Mx, "P-101", wrong.value, tasks=1)
print(f"provenance enforced 90%: {100*touched/trials:.1f} of 100 tasks touched (chapter {d['expected_tasks_touched_per_100_c0.9']})"); ok &= abs(100*touched/trials - d["expected_tasks_touched_per_100_c0.9"]) < 5
# retirement
M.retire(date(2028, 1, 1)); print("facts older than a year retired:", all(f.superseded_by for f in M.semantic.get("P-101", []))); ok &= all(f.superseded_by for f in M.semantic.get("P-101", []))
json.dump({"t_off": t_off, "t_on": t_on, "partial": touched/trials, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 24:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
