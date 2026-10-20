# REDTEAM — Chapter 04 Attention in depth (20 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Vaswani 2017, Dao 2022–24, Ainslie 2023, DeepSeek-V2)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | P-101 example lands; the two constraints (quadratic compare, cache) are stated before any notation |
| 2 Mechanism | PASS | Equations, mask exactness, per-layer parameter table, FlashAttention IO complexity, MLA absorption, sinks, prefix caching; runnable code switches MHA/GQA/MQA |
| 3 Worked numbers | PASS (after VERIFY) | Four arithmetic errors were present in the first draft; all derived numbers must come from a script |
| 4 Measurement | WEAK | The profiling protocol is sound but no reference output table is shown; the reader has no example of what "attention share" numbers look like on any stack |
| 5 Failure | PASS | Eight modes with detection signals; "silent kernel fallback" is the one most sources miss |
| 6 Frontier | PASS | Stopping points are fair; Huyen is credited for naming the cache and memory wall |
| 7 Industrial | PASS | Sizing of the on-site fallback is concrete and the retrieve-not-fill argument is numerical |
| 8 Decision aids | PASS | Formula, reference table, checklist, rule; toolkit item identified |
| 9 Sources | PASS | 23 rows, tiers correct, open items flagged |

Must change: (1) Layer 4 needs one measured profile table from a real stack, even a consumer GPU, labelled with hardware and kernel — the lab does not produce it and the chapter promises the method without an example. (2) The prefill-time estimate rests on an "assumed sustained 400 TFLOPs/s"; either measure it or present the time as a formula with the throughput as the reader's input. (3) The sliding-window section should state that Mistral's rolling buffer bounds the cache at w tokens — it says so in one clause; make it a sentence with the arithmetic (4,096 × bytes/token). (4) Cache-quantization paragraph gives no number; either cite KIVI/FP8 results from a primary source or move it entirely to ch11.

## Reviewer B — operations VP, refinery

Jargon before definition: "HBM," "SRAM," "warp," "TMA" appear in the FlashAttention section without a one-line gloss; an operations reader will skip the section and lose the point that kernel speed does not change cache size. Sections that change no decision: 04.2 "What the heads learn" and "Alternatives that give up the quadratic term" are interesting but the decision they support (test exact recall on the golden set) is stated in one sentence each; they could be halved. Industrial application: recognizable — the 300-page manual question is the one my planners ask; the FP8 answer and the API answer are usable. Decision aids: the sizing table and checklist can be used with data we have (model config, GPU memory). Embarrassment risk: none found after the arithmetic corrections; before them, the mixed GB/GiB table would have been caught by our engineers.

Decision this chapter helped me make: retrieval over long context for the on-site fallback, and GQA-with-FlashAttention as a procurement requirement.

## Three answers
- Deeper than the strongest free source? Yes on integration: no single free source carries architecture → bytes → serving decision; Dao's papers are deeper on kernels and this chapter does not pretend otherwise.
- As deep as all free sources combined? Not yet. Combined, they contain measured profiles and kernel internals this chapter only describes. The gap is Layer 4's missing measured table and the absence of any GPU measurement in the lab.
- Single change that most increases depth: run Lab 04b on one GPU (any) with FlashAttention-2 and the math backend, and publish the measured prefill/decode/attention-share table at 2K–32K.

## Change list
- CRITICAL: none remaining after VERIFY.
- MAJOR: A1 measured profile table (needs GPU); A2 prefill-time as formula; B1 gloss HBM/SRAM/warp/TMA in one sentence.
- MINOR: A3 rolling-buffer arithmetic; A4 cache-quantization number or move; B2 shorten two subsections.
