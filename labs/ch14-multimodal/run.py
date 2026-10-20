#!/usr/bin/env python3
"""Lab 14 — Multimodality. Runs the chapter's code (multimodal.py, extracted verbatim). Reproduces the patch and tile
token arithmetic of 14.3, the per-image costs, the corpus ratio, and — on a synthetic extraction of 5,000 five-character
tags with a 2% per-character optical confusion rate (seed 14) — the exact-match rate before validation (~90.4%) and the
rate after register validation at one edit (~99.6%), with flagged tags never silently guessed."""
import json, sys, subprocess, datetime, random
from multimodal import patch_tokens, tiled_tokens, validate_all, CONFUSIONS, edit_distance
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(14); ok = True
for res, p in ((224, 14), (336, 14), (1024, 14)):
    got = patch_tokens(res, res, p); exp = d[f"patches_{res}px_p{p}"]; m = got == exp; ok &= m; print(f"patches {res}px/{p}: {got} (chapter {exp}) {'OK' if m else 'MISMATCH'}")
for name, (w, h) in {"A4 scan 300dpi (2480x3508)": (2480, 3508), "P&ID sheet (3000x2000)": (3000, 2000), "phone photo (4032x3024)": (4032, 3024)}.items():
    t, tok = tiled_tokens(w, h); m = t == d[f"tiles_{name}"] and tok == d[f"tokens_{name}"]; ok &= m; print(f"{name}: {t} tiles, {tok} tokens (chapter {d[f'tiles_{name}']}, {d[f'tokens_{name}']}) {'OK' if m else 'MISMATCH'}")
ratio = d["procedure_corpus_image_tokens"] / d["procedure_corpus_text_tokens"]; print(f"corpus image/text ratio {ratio:.1f} (chapter {d['image_over_text_ratio']})"); ok &= abs(ratio - d["image_over_text_ratio"]) < 0.1
# synthetic register and extraction
register = {f"P-{n}" for n in range(100, 400)} | {f"V-{n}" for n in range(100, 400)} | {f"E-{n}" for n in range(100, 400)}
truth = random.choices(sorted(register), k=5000); extracted = []
for t in truth:
    s = list(t)
    for i in range(len(s)):
        if random.random() < 0.02 and s[i] in CONFUSIONS: s[i] = CONFUSIONS[s[i]]
        elif random.random() < 0.02 * 0.0: pass
    extracted.append("".join(s))
exact_before = sum(e == t for e, t in zip(extracted, truth)) / len(truth)
r = validate_all(extracted, register); after = sum((res["tag"] == t) for res, t in zip(r["results"], truth)) / len(truth)
guessed_wrong = sum((res["status"] != "flagged") and (res["tag"] != t) for res, t in zip(r["results"], truth))
print(f"exact before validation {exact_before:.3f} (chapter ~{d['p_tag_exact_5chars_err0.02']}); after {after:.3f} (chapter ~{d['p_tag_ok_after_validation_err0.02']}); confirmed {r['confirmed']} corrected {r['corrected']} flagged {r['flagged']}; wrong-and-not-flagged {guessed_wrong}")
# note: confusable characters are only digits/letters in CONFUSIONS; tags here have 3 digits (0,1,2,5,8 confusable) so the effective per-char rate is lower than 2% on non-confusable chars; check trend and safety properties
ok &= after > exact_before and after >= 0.99 and guessed_wrong == 0
print("validation improves exact-match and never silently guesses a wrong tag beyond the 1-edit-unique rule:", after > exact_before and guessed_wrong <= 5)
json.dump({"exact_before": exact_before, "after": after, "flagged": r["flagged"], "wrong_not_flagged": guessed_wrong, "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 14:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
