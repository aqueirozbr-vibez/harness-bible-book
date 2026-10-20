#!/usr/bin/env python3
"""Lab 20 / derive.py — every derived number in Chapter 20."""
import json, datetime, math
out = {}
# Corpus (scenario, illustrative): 20,000 docs → 240,000 chunks; chunk size per language from ch01 ratios
out["docs"] = 20000; out["chunks"] = 240000
out["chunk_tokens_target"] = 512; out["chunk_words_en"] = round(512 * 0.75); out["chunk_words_pt"] = round(512 * 0.75 / 1.5)
# Per-step retrieval budget: 1,000 tokens (ch19) → ~2 chunks at 512, or 3–4 at 300
out["chunks_per_step_at_512"] = 1000 // 512; out["chunks_per_step_at_300"] = 1000 // 300
# Stale-revision arithmetic: revisions per month r over the corpus; re-index latency L days; expected share of stale chunks at any moment ≈ (r/docs) * (L/30)
for L in (1, 7, 90):
    out[f"stale_share_pct_L{L}d_r400"] = round(100 * (400 / 20000) * (L / 30), 3)
# Queries touching a stale chunk: 60,000 queries × 3 retrievals × stale share
for L in (1, 7, 90):
    out[f"stale_retrievals_per_month_L{L}d"] = int(60000 * 3 * (400 / 20000) * (L / 30))
# Hybrid: RRF with k=60; a doc ranked 1 by vector and 5 by lexical: score
def rrf(ranks, k=60): return sum(1 / (k + r) for r in ranks)
out["rrf_rank1_rank5"] = round(rrf([1, 5]), 5); out["rrf_rank3_rank3"] = round(rrf([3, 3]), 5); out["rrf_rank1_only"] = round(rrf([1]), 5)
# Contextual retrieval gains (Anthropic 2024): -49% top-20 failures with contextual embeddings + BM25; -67% with reranking (recorded)
out["contextual_top20_failure_reduction_pct"] = 49; out["contextual_plus_rerank_pct"] = 67
# Re-ranker cost: cross-encoder over top-50 candidates at ~10 ms each on GPU (illustrative) → 500 ms; over top-20 → 200 ms
out["rerank_ms_top50_at_10ms"] = 500; out["rerank_ms_top20_at_10ms"] = 200
# Recall@k vs k: if answering chunk rank follows a geometric-like tail; illustrative: recall@5 0.80, @10 0.90, @20 0.96
out["recall_illustrative"] = {"5": 0.80, "10": 0.90, "20": 0.96}
# Precision cost of larger k: tokens = k × 512; at k=20 → 10,240 tokens, over the whole dynamic budget
for k in (2, 5, 10, 20): out[f"tokens_admitted_k{k}_512"] = k * 512
# Citation coverage: claims per work order ~6; coverage = cited / claims
out["claims_per_artifact"] = 6
# Context graph: assets 8,000; procedures 3,000; parts 25,000; relations assets→procedures ~2/asset, procedures→parts ~10/procedure (illustrative)
out["graph_nodes"] = 8000 + 3000 + 25000; out["graph_edges"] = 8000 * 2 + 3000 * 10
# Governance precondition: share of documents with owner+revision+class at ingestion; target 100%; illustrative baseline 62%
out["governance_baseline_pct"] = 62
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
