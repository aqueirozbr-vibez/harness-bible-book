#!/usr/bin/env python3
"""Lab 14 / derive.py — every derived number in Chapter 14."""
import json, datetime, math
out = {}
# ViT patch arithmetic: tokens = (H/p) * (W/p)
for res, p in ((224, 16), (224, 14), (336, 14), (448, 14), (1024, 14)):
    out[f"patches_{res}px_p{p}"] = (res // p) ** 2
# High-resolution tiling: image split into 512x512 tiles (vendor pattern), each ~ (512/14)^2 ≈ 1,369 patches, often pooled to a fixed budget
# Use an illustrative per-tile budget of 256 tokens after pooling (vendor-style) and a base thumbnail of 256
def tiled_tokens(w, h, tile=512, per_tile=256, base=256):
    tiles = math.ceil(w / tile) * math.ceil(h / tile); return tiles, base + tiles * per_tile
for name, (w, h) in {"A4 scan 300dpi (2480x3508)": (2480, 3508), "P&ID sheet (3000x2000)": (3000, 2000), "phone photo (4032x3024)": (4032, 3024), "thumbnail (1024x768)": (1024, 768)}.items():
    t, tok = tiled_tokens(w, h); out[f"tiles_{name}"] = t; out[f"tokens_{name}"] = tok
# Cost per page at frontier fresh input $1.25/M (ch37) — image tokens billed as input
for name in ("A4 scan 300dpi (2480x3508)", "P&ID sheet (3000x2000)"):
    out[f"usd_per_image_{name}"] = round(out[f"tokens_{name}"] * 1.25 / 1e6, 4)
# 3,000 procedures × 12 pages as images vs as text: tokens
out["procedure_corpus_pages"] = 3000 * 12; out["procedure_corpus_image_tokens"] = 3000 * 12 * out["tokens_A4 scan 300dpi (2480x3508)"]; out["procedure_corpus_text_tokens"] = 3000 * 6000
out["image_over_text_ratio"] = round(out["procedure_corpus_image_tokens"] / out["procedure_corpus_text_tokens"], 1)
# Tag validation: OCR confusions (O/0, I/1, S/5, B/8); a 5-char tag with per-char error 2% → P(tag exact) 
for e in (0.01, 0.02, 0.05): out[f"p_tag_exact_5chars_err{e}"] = round((1 - e) ** 5, 3)
# With register validation (edit distance 1 → nearest registered tag): recovered if exactly one char wrong and unique neighbor
out["p_tag_recoverable_ed1_err0.02"] = round(5 * 0.02 * 0.98**4, 3)
out["p_tag_ok_after_validation_err0.02"] = round(0.98**5 + 5 * 0.02 * 0.98**4, 3)
# Audio: ~ 16 kHz → Whisper-style ~ 50 tokens/s encoder (1500 tokens per 30 s window) — record as vendor/primary characteristic; illustrative per-minute cost skipped
out["whisper_encoder_tokens_per_30s"] = 1500
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
