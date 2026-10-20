# REDTEAM — Chapter 10 — Inference engineering (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read vLLM/PagedAttention paper; Huyen ch.9)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | KV-cap and utilization figures are computed, not measured on hardware |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | WEAK | $0.27/M is one configuration |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 10's KV-capacity table. (2) State that all throughput figures are modelled and need a GPU run (Lab 10b).

## Reviewer B — operations VP, refinery

Jargon before definition: 'continuous batching', 'PagedAttention' before gloss. Sections that change no decision: Serving internals; the VP needs the utilization-drives-cost sentence. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Hybrid: on-site for batch, API for spikes; utilization is the number to manage.

## Three answers
- Deeper than the strongest free source? Yes on the economics.
- As deep as all free sources combined? No — vLLM docs deeper on serving.
- Single change that most increases depth: Measured throughput on one GPU (needs environment).

## Change list
- CRITICAL: none.
- MAJOR: A2 modelled-not-measured label; A1.
- MINOR: B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.