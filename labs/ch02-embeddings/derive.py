#!/usr/bin/env python3
"""Lab 02 / derive.py — every derived number in Chapter 02."""
import json, datetime, numpy as np
rng = np.random.default_rng(2); out = {}
# Index storage: chunks × dims × bytes
for chunks in (100_000, 1_000_000):
    for dims in (384, 1024, 3072):
        out[f"index_GB_{chunks}x{dims}_fp32"] = round(chunks*dims*4/1e9, 2)
        out[f"index_GB_{chunks}x{dims}_int8"] = round(chunks*dims*1/1e9, 2)
# Scenario corpus: 20,000 documents × 12 chunks = 240,000 chunks at 1,024 dims (illustrative)
out["scenario_chunks"] = 240_000; out["scenario_index_GB_fp32_1024"] = round(240_000*1024*4/1e9, 2)
# Cosine concentration: random unit vectors in d dims have cosine ~ N(0, 1/d); std = 1/sqrt(d)
for d in (2, 32, 384, 1024, 3072):
    a = rng.standard_normal((2000, d)); b = rng.standard_normal((2000, d))
    a /= np.linalg.norm(a, axis=1, keepdims=True); b /= np.linalg.norm(b, axis=1, keepdims=True)
    cos = (a*b).sum(1); out[f"random_cosine_std_d{d}"] = round(float(cos.std()), 4); out[f"theory_1_over_sqrt_d{d}"] = round(1/np.sqrt(d), 4)
# Brute-force search cost: N × d multiply-adds per query
out["bruteforce_madds_240k_x_1024"] = 240_000*1024
out["bruteforce_ms_at_10_GFLOPs"] = round(240_000*1024*2/10e9*1e3, 1)
# Matryoshka truncation: storage saving from 3072 -> 768 dims
out["storage_saving_3072_to_768_pct"] = 75
# Embedding cost at $0.13/M tokens (illustrative vendor rate for a large embedding model): re-embedding 240k chunks × 512 tokens
out["reembed_cost_usd_240k_chunks_512tok_at_0.13"] = round(240_000*512/1e6*0.13, 2)
# Query volume: 60,000 queries/month × 3 retrievals each = 180,000 embedding calls × ~50 tokens
out["monthly_query_embed_tokens"] = 60_000*3*50; out["monthly_query_embed_usd_at_0.13"] = round(60_000*3*50/1e6*0.13, 2)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
