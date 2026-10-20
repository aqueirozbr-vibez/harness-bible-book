# VERIFY log — Chapter 04 (20 Sep 2026)

Caveat: run by the drafting instance; the plan requires an independent verifier before the chapter counts as passed.

| Location | Item | Verdict | Correction |
|---|---|---|---|
| 04.2 | Llama 3 70B: d=8,192, 64 heads, 8 KV heads, head dim 128, FFN 28,672, 80 layers | CONFIRMED (Dubey et al. 2024 Table 3) | — |
| 04.2 | Per-layer parameters 151.0M attention / 704.6M FFN / 855.6M; ×80 = 68.4B | CONFIRMED by recomputation | — |
| 04.2 | 1/√d_k variance argument; base h=8, d=512, d_k=64 | CONFIRMED (Vaswani 2017 §3.2) | — |
| 04.2 | FlashAttention IO complexity Θ(N²d²M⁻¹) vs Θ(Nd+N²) | CONFIRMED (Dao 2022 §3.2) | — |
| 04.2 | FA2: ~2×, 50–73% A100, 230 / 225 TFLOPs/s, 72% MFU, 9× vs PyTorch, 335 on H100 | CONFIRMED (paper abstract; CRFM blog) | — |
| 04.2 | FA3: 1.5–2×, 740 TFLOPs/s 75%, FP8 ~1.2 PFLOPs/s 2.6× lower error, FA2 35% on H100 | CONFIRMED (Together AI blog; paper) | — |
| 04.2 | GQA uptraining ~5% compute; mean-pool init; GQA-8 near MHA | CONFIRMED (Ainslie 2023 §3.1, Fig. 3) | — |
| 04.2 | MLA d_c=512, d_h^R=64, 128×128; 93.3%; 5.76× | CONFIRMED (DeepSeek-V2 §2.1, abstract) | — |
| 04.2 | Mistral 7B window 4,096; 32 layers; 32 heads; 8 KV heads | CONFIRMED (Jiang 2023 Table 1) | — |
| 04.3 | Non-attention MAC totals at 8K / 128K | ARITHMETIC ERROR | 6.6×10¹⁴ → 5.3×10¹⁴; 1.1×10¹⁶ → 8.4×10¹⁵; "about half" → 57% |
| 04.3 | Attention FLOP at 128K and prefill time | ARITHMETIC ERROR | 1.1×10¹⁶ → 2.2×10¹⁶ FLOP; ~70 s → ~100 s; 23× → 33× |
| 04.3, 04.7, 04.8 | Cache GB figures mixed GiB and GB | UNIT INCONSISTENCY | All restated in GB = 10⁹ bytes; 84 → 86 GB; 10.5 → 10.7; 1.9 → 2.0; 42 → 43; table recomputed |
| 04.3 | Decode read 3 ms cache / 42 ms weights at 3.35 TB/s | CONFIRMED (3.2 / 41.8 ms) | — |
| 04.3 | KV bytes/token 128 / 320 / 504 KB | CONFIRMED by Lab 04 | — |
| 04.5 | PagedAttention 20.4–38.2% | CONFIRMED (Kwon 2023 §3) | — |
| 04.2 | Attention sinks stream "for millions of tokens" | CONFIRMED (Xiao 2023 reports up to 4M tokens) | — |
| 04.6 | "Where it stops" claims for Vaswani, Dao, Ainslie, Alammar, Karpathy, Weng, Huyen | FAIR on re-reading; Huyen's inference chapter does name the KV cache and memory wall — stated as such | — |
| Code | Reference implementation and lab | RUN — passes | — |

Verdict: 4 derived figures corrected, 1 unit convention fixed, 0 MISATTRIBUTED, 0 UNVERIFIABLE. Lesson for the standard: every derived number must be produced by a script in the lab folder, not by hand; add this to the DRAFT and LAB prompts.
