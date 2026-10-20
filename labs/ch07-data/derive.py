#!/usr/bin/env python3
"""Lab 07 / derive.py — every derived number in Chapter 07."""
import json, datetime
out = {}
# MinHash LSH: probability that two documents with Jaccard similarity s are flagged, with b bands of r rows: 1-(1-s^r)^b
def p_flag(s, b, r): return 1 - (1 - s**r)**b
for b, r in ((14, 8), (20, 5), (50, 2)):
    out[f"lsh_b{b}_r{r}"] = {str(s): round(p_flag(s, b, r), 3) for s in (0.5, 0.7, 0.8, 0.9, 0.95)}
    out[f"lsh_b{b}_r{r}_threshold_approx"] = round((1/b)**(1/r), 3)   # s where p ≈ 0.5
# Plant corpus vs pre-training corpus
plant_tokens = 20_000 * 6_000; out["plant_corpus_tokens"] = plant_tokens
out["plant_share_of_15T_pct"] = f"{100*plant_tokens/15e12:.6f}"
out["plant_tokens_per_param_if_finetuned_on_8B"] = round(plant_tokens / 8.03e9, 4)
# Contamination: probability a golden set of 100 items with a distinctive 13-gram is entirely absent from a corpus if each item leaks independently with p
for p in (0.001, 0.01):
    out[f"p_no_leak_100_items_at_p{p}"] = round((1-p)**100, 3)
# Web pipeline scale (FineWeb): 96 CommonCrawl snapshots -> 15T tokens; retention illustrative from paper's reported stages
out["fineweb_tokens"] = 15e12; out["fineweb_snapshots"] = 96
# Llama 3 data mix (Dubey et al. 2024): ~50% general, 25% math/reasoning, 17% code, 8% multilingual
out["llama3_mix"] = {"general": 50, "math_reasoning": 25, "code": 17, "multilingual": 8}
# Epochs: Muennighoff 2023 — returns diminish beyond ~4 epochs; illustrative token-equivalence
out["repeat_epochs_useful"] = 4
# Plant document classes: illustrative counts for the scenario corpus
out["plant_docs"] = {"procedures": 3000, "work_orders": 12000, "histories": 4000, "drawings_legends": 1000}
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
