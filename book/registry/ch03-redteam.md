# REDTEAM — Chapter 03 — The transformer block (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Vaswani 2017; Karpathy; Huyen)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Parameter-count verification shown once; no per-model table |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | WEAK | Industrial section is thin: bandwidth argument only |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Add the lab's ±0.07% parameter-count table for three published models. (2) Add one sentence on what the FFN share implies for pruning claims a vendor might make.

## Reviewer B — operations VP, refinery

Jargon before definition: 'residual stream', 'FFN' glossed late. Sections that change no decision: Block anatomy changes no decision directly; the decode-bandwidth paragraph does. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Decode is bandwidth-bound: size the on-site GPU by memory bandwidth, not FLOPs.

## Three answers
- Deeper than the strongest free source? Yes on the six-integer verification.
- As deep as all free sources combined? No — Karpathy's walkthrough is deeper on mechanism.
- Single change that most increases depth: Reference output table.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.