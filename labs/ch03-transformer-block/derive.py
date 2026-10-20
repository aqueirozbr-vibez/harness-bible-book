#!/usr/bin/env python3
"""Lab 03 / derive.py — parameter accounting for Llama 3 (Dubey et al. 2024, Table 3) and FLOPs per token."""
import json, datetime
CFG = {"Llama 3 8B":   dict(L=32,  d=4096,  heads=32,  kv=8, hd=128, ffn=14336, V=128256, published=8.03e9),
       "Llama 3 70B":  dict(L=80,  d=8192,  heads=64,  kv=8, hd=128, ffn=28672, V=128256, published=70.6e9),
       "Llama 3 405B": dict(L=126, d=16384, heads=128, kv=8, hd=128, ffn=53248, V=128256, published=405.9e9)}
def count(c):
    q = c["d"]*c["heads"]*c["hd"]; k = c["d"]*c["kv"]*c["hd"]; v = k; o = c["heads"]*c["hd"]*c["d"]
    attn = q+k+v+o; ffn = 3*c["d"]*c["ffn"]; norms = 2*c["d"]; layer = attn+ffn+norms
    embed = c["V"]*c["d"]; unembed = c["V"]*c["d"]; final_norm = c["d"]
    total = c["L"]*layer + embed + unembed + final_norm
    return dict(attn=attn, ffn=ffn, norms=norms, layer=layer, layers_total=c["L"]*layer, embed=embed, unembed=unembed, total=total,
                attn_share_of_layer=round(100*attn/layer,1), ffn_share_of_layer=round(100*ffn/layer,1),
                embed_share=round(100*(embed+unembed)/total,1), vs_published_pct=round(100*(total-c["published"])/c["published"],2))
out = {k: count(c) for k, c in CFG.items()}
# FLOPs per token ≈ 2 × non-embedding params (Kaplan 2020 convention), plus attention scores (context-dependent, ch04)
for k, c in CFG.items():
    out[k]["flops_per_token_2N_nonembed_GFLOP"] = round(2*out[k]["layers_total"]/1e9, 1)
    out[k]["flops_per_token_2N_total_GFLOP"] = round(2*out[k]["total"]/1e9, 1)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k, v in out.items():
    if isinstance(v, dict): print(k, {kk: (round(vv/1e6,1) if kk in ("attn","ffn","layer","embed","unembed") else (round(vv/1e9,3) if kk in ("layers_total","total") else vv)) for kk, vv in v.items()})
