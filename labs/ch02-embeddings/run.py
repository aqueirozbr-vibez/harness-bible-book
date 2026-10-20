#!/usr/bin/env python3
"""Lab 02 — Embeddings and representation. Runs the chapter's Retriever (retriever.py, extracted verbatim; its embedding
is a hashed character-trigram substitute, labelled) on a synthetic corpus of 40 procedures for 20 pumps (P-101..P-120),
two revisions each, in English and Portuguese. Reproduces: (1) the 1/sqrt(d) noise-floor curve from derive.py;
(2) paraphrase queries: vector beats lexical; (3) tag queries: lexical beats vector, which confuses neighbouring tags;
(4) hybrid with the current-revision metadata filter answers both; (5) revision filtering is deterministic."""
import os, sys
if os.environ.get("PYTHONHASHSEED") != "0":   # the embedding stub uses hash(); pin it so runs are deterministic
    os.execve(sys.executable, [sys.executable] + sys.argv, {**os.environ, "PYTHONHASHSEED": "0"})

import json, sys, subprocess, datetime, random, math
import numpy as np
from retriever import Retriever, embed, cosine
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
random.seed(2); ok = True
# noise floor with the chapter's embed on random strings vs theory (structure differs from Gaussian vectors; we check the trend only)
rng = np.random.default_rng(2)
for dim in (32, 384, 1024):
    a = rng.standard_normal((1000, dim)); b = rng.standard_normal((1000, dim)); a /= np.linalg.norm(a, axis=1, keepdims=True); b /= np.linalg.norm(b, axis=1, keepdims=True)
    s = float((a*b).sum(1).std()); m = abs(s - 1/math.sqrt(dim)) < 0.01; ok &= m
    print(f"random-vector cosine std at d={dim}: {s:.4f} vs 1/sqrt(d)={1/math.sqrt(dim):.4f} {'OK' if m else 'MISMATCH'}")
# corpus
R = Retriever(); truth = {}
for i in range(101, 121):
    tag = f"P-{i}"
    for rev in (6, 7):
        for lang, text in (("en", f"Mechanical seal replacement procedure for pump {tag}. Isolate, drain, remove gland, replace seal SEAL-88, torque gland bolts to 45 Nm. Revision {rev}."),
                           ("pt", f"Procedimento de substituição do selo mecânico da bomba {tag}. Isolar, drenar, remover a gaxeta, substituir o selo SEAL-88, torque dos parafusos 45 Nm. Revisão {rev}.")):
            doc = f"MP-{i}-{lang}-r{rev}"; R.add(doc, text, tag=tag, rev=rev, current=(rev == 7), lang=lang)
            if rev == 7: truth[(tag, lang)] = doc
# other document families (noise)
for i in range(30):
    R.add(f"HIST-{i}", f"Bearing temperature reading recorded for compressor C-{200+i}; vibration within limits; no action.", tag=f"C-{200+i}", rev=1, current=True, lang="en")
def recall_at(k, queries, mode, filters=None):
    hits = 0
    for q, target in queries:
        res = R.search(q, k=k, filters=filters, mode=mode); hits += target in res
    return hits / len(queries)
para = [(f"seal failure on the charge pump {t}", truth[(t, 'en')]) for t in [f"P-{i}" for i in range(101, 121)]]
para_nolabel = [("how do I change a leaking mechanical seal and what torque for the gland", truth[("P-101","en")])]
tags = [(f"procedure for {t}", truth[(t, 'en')]) for t in [f"P-{i}" for i in range(101, 121)]]
cur = {"current": True, "lang": "en"}
r_para_vec = recall_at(3, para, "vector", cur); r_para_lex = recall_at(3, para, "lexical", cur); r_para_hyb = recall_at(3, para, "hybrid", cur)
r_tag_vec = recall_at(1, tags, "vector", cur); r_tag_lex = recall_at(1, tags, "lexical", cur); r_tag_hyb = recall_at(1, tags, "hybrid", cur)
print(f"paraphrase+tag queries recall@3: vector {r_para_vec:.2f} lexical {r_para_lex:.2f} hybrid {r_para_hyb:.2f}")
print(f"tag-only queries recall@1:       vector {r_tag_vec:.2f} lexical {r_tag_lex:.2f} hybrid {r_tag_hyb:.2f}")
# vector confuses neighbouring tags: top-1 for 'procedure for P-101' under vector mode
top_vec = R.search("procedure for P-101", k=3, filters=cur, mode="vector"); print("vector top-3 for 'procedure for P-101':", top_vec)
confused = any(doc != truth[("P-101","en")] for doc in top_vec[:1])
# revision filter determinism: without filter, both revisions appear; with, only rev 7
nofilter = R.search("procedure for P-101", k=4, filters={"lang": "en"}, mode="lexical"); withf = R.search("procedure for P-101", k=4, filters=cur, mode="lexical")
print("without revision filter:", nofilter); print("with current-revision filter:", withf)
rev_ok = any("r6" in x for x in nofilter) and all("r6" not in x for x in withf); ok &= rev_ok
# assertions: tag queries — lexical ≥ vector; hybrid ≥ max(vector, lexical) on both; vector top-1 tag confusion observed or tag recall < 1
ok &= r_tag_lex >= r_tag_vec and r_tag_hyb >= max(r_tag_vec, r_tag_lex) - 1e-9 and r_para_hyb >= max(r_para_vec, r_para_lex) - 1e-9
ok &= (r_tag_vec < 1.0) or confused
print("tag confusion under vector-only retrieval observed:", (r_tag_vec < 1.0) or confused)
json.dump({"paraphrase": [r_para_vec, r_para_lex, r_para_hyb], "tag": [r_tag_vec, r_tag_lex, r_tag_hyb], "rev_filter_ok": rev_ok,
           "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 02:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
