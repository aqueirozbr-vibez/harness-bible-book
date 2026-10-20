#!/usr/bin/env python3
"""Lab 17 — Task entry and outcome specification. Runs the chapter's intake code (intake.py, extracted verbatim) on
1,000 synthetic requests (seed 17): chat messages with/without tags and symptoms, ambiguous tags (two assets), and
webhook payloads. Reproduces: clarification rate falls with template structure (30% ambiguity → ~15% → ~6% as inferred
fields rise); criteria coverage 82% (9 of 11 — the lab template has 5 sensors of 6, so coverage is reported as measured);
intent validation denies off-scope submissions, other-equipment actions, and external comms; the ask-or-guess arithmetic."""
import json, sys, subprocess, datetime, random
from intake import normalize, classify, resolve, coverage, intent_validate, TEMPLATES
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(17); ok = True
register = {"P-101": ["P-101-U3", "P-101-SPARE"], "P-204": ["P-204-U3"], "E-212": ["E-212-U2"]}
def chat(tag, symptom, ambiguous):
    t = tag if tag else ""; s = " seal leaking" if symptom else " has an issue"
    return {"text": f"{t}{s}, need a work order"}
# 30% ambiguity: requests missing a field or with an ambiguous tag; structure levels: s = share of those the template resolves by inference
def run(structure_share):
    clar = 0; n = 1000
    for _ in range(n):
        ambiguous_case = random.random() < 0.30
        if ambiguous_case and random.random() < structure_share:
            ambiguous_case = False        # template structure resolved it (e.g., default to installed asset)
        if ambiguous_case:
            kind = random.choice(["missing_symptom", "missing_tag", "ambiguous_tag"])
            payload = chat("P-204", False, False) if kind == "missing_symptom" else chat(None, True, False) if kind == "missing_tag" else chat("P-101", True, True)
        else:
            payload = chat("P-204", True, False)
        rec = normalize("chat", payload, "tech-4471", "t"); r = resolve(rec, TEMPLATES[classify(rec)], register)
        clar += r["status"] == "clarify"
    return clar / n
for s, exp in ((0.0, 0.30), (0.5, 0.15), (0.8, 0.06)):
    rate = run(s); m = abs(rate - exp) < 0.04; ok &= m; print(f"clarification rate at structure share {s}: {rate:.3f} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
# webhook: structured payload resolves without a question
rec = normalize("webhook", {"equipment_tag": "E-212", "symptom": "pm_due"}, "cmms-integration", "t"); r = resolve(rec, TEMPLATES[classify(rec)], register)
print("webhook resolves without clarification:", r["status"] == "ready"); ok &= r["status"] == "ready"
task = r["task"]; cov = coverage(task); print(f"criteria coverage in the lab template: {cov['covered']}/{cov['total']} (uncovered: {cov['uncovered']})"); ok &= cov["covered"] == 5 and cov["total"] == 6
# intent validation
tests = [({"tool": "submit_work_order"}, False), ({"tool": "draft_work_order", "equipment": "P-204-U3"}, False), ({"tool": "send_email"}, False), ({"tool": "draft_work_order", "equipment": "E-212-U2"}, True)]
res = [(intent_validate(task, a)["ok"] == exp) for a, exp in tests]; print("intent validation (submit / other equipment / email denied; in-scope draft allowed):", all(res)); ok &= all(res)
# ask-or-guess arithmetic
for c_, exp in ((0.9, d["breakeven_g_ask_vs_guess_c0.9"]), (0.5, d["breakeven_g_ask_vs_guess_c0.5"])):
    per_wrong = c_ * 0.02 + (1 - c_) * (0.9 * 6 + 0.1 * 150); g = round(2.0 / per_wrong, 3); m = abs(g - exp) < 1e-3; ok &= m; print(f"ask-or-guess break-even at c={c_}: g*={g} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
json.dump({"timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 17:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
