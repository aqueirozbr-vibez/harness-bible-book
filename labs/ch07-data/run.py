#!/usr/bin/env python3
"""Lab 07 — Pre-training data and pipelines. Runs the chapter's MinHash/LSH near-duplicate detector and the 13-gram
contamination check (pipeline.py, extracted verbatim) on a synthetic corpus (seed 7): 300 distinct procedures, each with
a 'revision' (similarity > 0.9) and 40 templated near-copies (similarity ~0.5–0.7), plus a golden set of 50 questions of
which 5 have their answer sentence leaked into corpus documents. Reproduces: (1) the LSH flagging probabilities of 07.3
at 14×8 by simulation; (2) revisions detected at ≥ 0.9 with high recall and templated documents not flagged at 0.8;
(3) all 5 leaks found by the contamination check, and no false hits on the 45 clean questions."""
import json, sys, subprocess, datetime, random
from pipeline import near_duplicates, contamination, shingles, jaccard, minhash, lsh_candidates
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(7); ok = True
WORDS = "isolate drain remove gland replace seal torque bolts verify pressure record reading permit hazard class inspect bearing vibration alignment coupling".split()
def sentence(n=12): return " ".join(random.choice(WORDS) for _ in range(n))
corpus = {}; truth_rev = set(); templated = set()
for i in range(300):
    base = " ".join(sentence() for _ in range(8)); corpus[f"MP-{i}-r6"] = base
    toks = base.split(); j = random.randrange(len(toks)); toks[j] = "updated"; corpus[f"MP-{i}-r7"] = " ".join(toks)   # one-word revision
    truth_rev.add((f"MP-{i}-r6", f"MP-{i}-r7"))
for i in range(40):   # templated: shares a fixed 3-sentence header with every other templated doc, unique body
    corpus[f"WO-{i}"] = "standard work order header revision control approval block " * 3 + " ".join(sentence() for _ in range(5)); templated.add(f"WO-{i}")
# 1. LSH flag probability by simulation at 14x8 on pairs of controlled Jaccard
def make_pair(s):
    """Two 200-element sets with Jaccard ≈ s: |A∩B| = k, |A∪B| = 400 − k; fresh random element names per trial."""
    tag = random.random(); k = round(400 * s / (1 + s))
    shared = {f"s{tag}-{i}" for i in range(k)}
    a = shared | {f"a{tag}-{i}" for i in range(200 - k)}; b = shared | {f"b{tag}-{i}" for i in range(200 - k)}; return a, b
sim = {}
for s in (0.5, 0.7, 0.8, 0.9):
    hits = 0; N = 300
    for _ in range(N):
        a, b = make_pair(s); sa, sb = minhash(a, 112), minhash(b, 112)
        hits += bool(lsh_candidates({"a": sa, "b": sb}, 14, 8))
    sim[str(s)] = round(hits / N, 2)
    exp = d["lsh_b14_r8"][str(s)]; m = abs(sim[str(s)] - exp) < 0.1; ok &= m
    print(f"LSH 14x8 flag rate at Jaccard {s}: simulated {sim[str(s)]:.2f}  formula {exp:.3f}  {'OK' if m else 'MISMATCH'}")
# 2. near-duplicate detection on the corpus
pairs = near_duplicates(corpus, threshold=0.8, b=14, r=8)
found = {(a, b) for a, b, _ in pairs}
rev_recall = len(found & truth_rev) / len(truth_rev); wo_flagged = sum(1 for a, b, _ in pairs if a in templated or b in templated)
print(f"revision pairs recalled at ≥0.8: {rev_recall:.3f} ({len(found & truth_rev)}/{len(truth_rev)}); templated pairs flagged: {wo_flagged}")
ok &= rev_recall > 0.97 and wo_flagged == 0
# 3. contamination
golden = {f"q{i}": " ".join(sentence() for _ in range(2)) for i in range(50)}
leaked = random.sample(list(golden), 5)
for g in leaked:
    doc = random.choice([k for k in corpus if k.startswith("MP")]); corpus[doc] = corpus[doc] + " " + golden[g]
hits = contamination(corpus, golden, n=13)
print(f"contamination: leaked {sorted(leaked)}; detected {sorted(hits)}; false hits {sorted(set(hits) - set(leaked))}")
ok &= set(hits) == set(leaked)
json.dump({"lsh_sim": sim, "revision_recall": rev_recall, "templated_flagged": wo_flagged, "leaks": sorted(leaked), "detected": sorted(hits),
           "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 07:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
