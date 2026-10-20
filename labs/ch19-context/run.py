#!/usr/bin/env python3
"""Lab 19 — Context engineering. Runs the chapter's assembler (context.py, extracted verbatim) through a simulated
16-iteration task (seed 19): each iteration produces a raw 100-row tool result and a history entry. Reproduces: the
compacted window stays within budget at every iteration while an uncompacted accumulation grows to ~4.8× (19.3);
trim_result cuts an 8,000-token result to a few hundred with the reference id kept; the chunk-start fraction stays
near 0.67 compacted and drifts toward 0.93 uncompacted; the instruction is last; compaction never exceeds its budget."""
import json, sys, subprocess, datetime, random
from context import assemble, trim_result, compact, tokens, BUDGET
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(19); ok = True
prefix = ("stable prefix line " * 4 + "\n") * 200        # ≈ 4,000 tokens by the stand-in
rows = [f"{i:03d} | {'seal' if i % 20 == 0 else 'bearing'} | reading {random.randint(10,99)} | " + "technician note text describing the observation and action taken " * 4 for i in range(100)]   # ≈ 80 tokens/row
trimmed = trim_result(rows, lambda r: "| seal |" in r, "res-002", lambda rs: f"{len(rs)} seal rows; ids " + ",".join(r[:3] for r in rs))
print(f"tool result: raw {tokens(chr(10).join(rows))} tokens → admitted {tokens(trimmed)} tokens; reference kept: {'[result res-002]' in trimmed}")
ok &= tokens(trimmed) < 300 and "[result res-002]" in trimmed and tokens("\n".join(rows)) > 6000
history = []; raw_history_text = ""; comp_sizes = []; unc_sizes = []; fracs_c = []; fracs_u = []
chunks = [f"[MP-0417 §{i} rev 7] " + "procedure chunk text " * 60 for i in range(3)]   # ≈ 330 tokens each → ~1,000 retrieved
for it in range(1, 17):
    history.append({"step": it, "outcome": "ok", "refs": [f"res-{it:03d}"]})
    raw_history_text += ("prior output and raw result text " * 180) + "\n"    # ≈ 1,500 tokens per iteration by the stand-in
    facts = ["fact: fluid service hydrocarbon; last repair bearing 2026-08 " * 3, "fact: zone Z3; hazard class H " * 3]
    w = assemble(prefix, chunks, history, facts, "task record: work order from fault; scope P-101-U3; draft only " * 3, f"step {it}: permit check " * 4, "P-101 selo vazando")
    comp_sizes.append(w["tokens"]); fracs_c.append(w["chunk_start_fraction"]); ok &= not w["over_budget"]
    unc = tokens(prefix) + tokens(raw_history_text) + tokens("\n".join(chunks)) + 400; unc_sizes.append(unc); fracs_u.append(round((tokens(prefix) + tokens(raw_history_text)) / unc, 2))
print(f"compacted window by iteration (1,4,8,16): {[comp_sizes[i-1] for i in (1,4,8,16)]}  (budget ≤ {tokens(prefix) + sum(BUDGET.values())})")
print(f"uncompacted window by iteration (1,4,8,16): {[unc_sizes[i-1] for i in (1,4,8,16)]}  growth {unc_sizes[-1]/unc_sizes[0]:.1f}× (chapter 4.8×)")
print(f"chunk start fraction: compacted {fracs_c[0]}→{fracs_c[-1]} (chapter 0.67); uncompacted history-first {fracs_u[0]}→{fracs_u[-1]} (chapter 0.93)")
ok &= max(comp_sizes) - min(comp_sizes) < 300 and 4.0 < unc_sizes[-1] / unc_sizes[0] < 5.6 and fracs_u[-1] > 0.85 and 0.6 < fracs_c[-1] < 0.8
ok &= w["window"].rstrip().endswith("P-101 selo vazando") and tokens(compact(history, BUDGET["history"])) <= BUDGET["history"]
print("instruction last and compaction within budget:", w["window"].rstrip().endswith("P-101 selo vazando") and tokens(compact(history, BUDGET["history"])) <= BUDGET["history"])
json.dump({"compacted": comp_sizes, "uncompacted": unc_sizes, "fracs": [fracs_c, fracs_u], "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 19:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
