#!/usr/bin/env python3
"""Lab 18 — Guides. Runs the chapter's assembler (guides.py, extracted verbatim) on a synthetic work-order guide sized to the
scenario's composition. Reproduces: the prefix is byte-identical across 100 assemblies (one hash); a timestamp or task id
in any element is refused at build time; the prefix exceeds the cache minimum; the element budget matches the chapter's
composition to within the 4-chars/token stand-in's tolerance; the pairing audit reports 9 of 12 enforced with the
unenforced named; compose_window places the instruction and repeated request last."""
import json, sys, subprocess, datetime
from guides import Guide, Rule, assemble_prefix, check_cache_minimum, pairing_audit, compose_window
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
ok = True
def pad(text, tokens): return (text + " ") * max(1, tokens * 4 // max(1, len(text) + 1))
rules = [Rule(f"r{i}", f"Rule {i}: the work order must satisfy constraint {i} as stated in the site standard.", sensor=(f"s{i}" if i <= 9 else None), golden_case=(f"g{i}" if i <= 9 else None)) for i in range(1, 13)]
g = Guide(version="1.4.0", identity=pad("You are the refinery maintenance agent. You draft work orders for approval. You read the historian through the broker and write only to the CMMS draft queue.", 800),
          task_class="work_order_from_fault", instructions=pad("Draft the eight fields in Portuguese; cite the procedure by number and current revision; set permit type from hazard class.", 400 - 12*30//4),
          rules=rules, tools=[(f"tool_{i}", pad(f"Tool {i} reads a system of record and returns structured rows; use when the step needs that data.", 200)) for i in range(9)],
          examples=[(pad("P-101 selo vazando, preciso de OS", 50), pad("ordem de serviço: campos completos, procedimento MP-0417 rev 7, permissão hot_work", 200)) for _ in range(3)],
          output_contract=pad("Output: JSON matching the CMMS work-order schema; no prose outside the object.", 250))
hashes = {assemble_prefix(g)["hash"] for _ in range(100)}; print(f"distinct hashes over 100 assemblies: {len(hashes)}"); ok &= len(hashes) == 1
p = assemble_prefix(g); print(f"prefix tokens {p['tokens']} (scenario 4,000; stand-in tokenizer); budget {p['budget']}; cache minimum met: {check_cache_minimum(p)}")
ok &= check_cache_minimum(p) and 3000 <= p["tokens"] <= 5000
for bad, label in ((" Generated 2026-09-21.", "date"), (" Task t-22071.", "task id"), (" As of 14:20.", "time")):
    try: assemble_prefix(Guide(**{**g.__dict__, "identity": g.identity + bad})); print(f"volatile {label} NOT refused"); ok = False
    except ValueError as e: print(f"volatile {label} refused: {e}")
a = pairing_audit(g); m = a["enforced"] == d["rules_with_sensor"] and a["rules"] == d["rules_total"] and a["enforced_pct"] == d["rules_enforced_pct"]; ok &= m
print(f"pairing: {a['enforced']}/{a['rules']} enforced ({a['enforced_pct']}%); unenforced {a['unenforced']}  {'OK' if m else 'MISMATCH'}")
w = compose_window(p, ["chunk A", "chunk B"], ["fact 1"], "task record", "step 7: permit check", "P-101 selo vazando")
print("prefix first and instruction last:", w.startswith(p["prefix"]) and w.rstrip().endswith("P-101 selo vazando")); ok &= w.startswith(p["prefix"]) and w.rstrip().endswith("P-101 selo vazando")
# drift arithmetic
print(f"timestamp at token 200 of 4,000 → {d['drift_timestamp_at_200_cached_tokens_lost']} tokens uncached ({d['drift_loss_pct']}%)"); ok &= d["drift_timestamp_at_200_cached_tokens_lost"] == 3800
json.dump({"hash": p["hash"], "tokens": p["tokens"], "pairing": a, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 18:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
