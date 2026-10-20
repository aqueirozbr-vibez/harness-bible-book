# Lab 04 — Attention in depth

**Measures:** (1) how attention time scales with sequence length using the chapter's reference NumPy implementation; (2) KV-cache bytes per token for Llama 3 8B, 70B, 405B from their published architecture; (3) that grouped-query attention with broadcast KV heads is numerically identical to multi-head attention.

**Reproduces from Chapter 04, Section 04.3:** the quadratic exponent (chapter: 2; tolerance 1.7–2.3 — CPU timing noise and the linear terms at small n pull the fitted slope below 2) and the three KV-cache figures 128 KB / 320 KB / 504 KB per token (exact match required).

**Prerequisites:** Python 3.9+, NumPy 1.26. CPU only; no GPU, no API, no data download. Data is synthetic (seed 4).

**Run:** `pip install -r requirements.txt && python run.py` — under 3 minutes on a laptop. Exit code 0 means all three reproductions passed.

**Expected output:** see `results/run.txt` and `results/run.json` from the committed run.

**Limits:** the NumPy path materializes the n×n score matrix, so it demonstrates the arithmetic, not FlashAttention's memory behavior; the H100 throughput and decode-bandwidth figures in the chapter are not reproduced here (they require the hardware). The chapter's 04.4 protocol describes how to measure them on your stack.
