#!/usr/bin/env python3
"""Lab 01 / derive.py — every derived number in Chapter 01."""
import json, datetime
out = {}
# Embedding matrix = vocab × d_model; output (unembedding) matrix same size unless tied
models = {"Llama 3 8B": (128256, 4096), "Llama 3 70B": (128256, 8192), "Llama 3 405B": (128256, 16384),
          "Llama 2 7B": (32000, 4096), "Gemma-class 256K": (262144, 4096)}
for k,(v,d) in models.items():
    out[f"embed_params_{k}"] = v*d; out[f"embed_MB_fp16_{k}"] = round(v*d*2/1e6)
out["llama3_8B_embed_share_of_8B_pct"] = round(100*2*128256*4096/8.03e9, 1)   # embed + unembed (untied) vs total
# Per-language cost from Petrov et al. ratios (GPT-4 tokenizer): English 1.0, Portuguese/German ~1.5, Italian ~1.6, Bulgarian ~2.6
ratio = {"English": 1.0, "Portuguese": 1.5, "German": 1.5, "Italian": 1.6, "Bulgarian": 2.6}
tokens_per_1000_words_en = 1333   # 0.75 words/token
for k,r in ratio.items(): out[f"tokens_per_1000_words_{k}"] = round(tokens_per_1000_words_en*r)
# same token budget holds fewer words: chunk of 512 tokens
for k,r in ratio.items(): out[f"words_in_512_token_chunk_{k}"] = round(512/ (tokens_per_1000_words_en*r/1000))
# cache minimum prefix in words: 1,024 tokens (most), 4,096 (some small models)
out["cache_min_1024_tokens_in_english_words"] = round(1024*0.75); out["cache_min_1024_tokens_in_portuguese_words"] = round(1024*0.75/1.5)
# scenario bill impact: 6,000-token English query becomes ~9,000 in Portuguese; monthly fresh+cached input cost at ch37 prices (B config)
q = 60000; fresh, cached = 2000, 4000
en = (q*fresh*1.25 + q*cached*0.125)/1e6; pt = en*1.5
out["monthly_input_cost_B_english"] = round(en); out["monthly_input_cost_B_portuguese"] = round(pt)
# tag fragmentation illustration: "P-101" -> P, -, 101 (3 tokens) vs "pump" (1); a P&ID legend of 500 words at 1.8 tokens/word
out["legend_500_words_tokens_at_1.8"] = 900
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
