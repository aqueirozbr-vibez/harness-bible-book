# REDTEAM — Chapter 05 — Positional encoding and long context (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Su 2021 (RoPE); Liu 2023 (lost in the middle); Huyen)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Effective-length protocol has no example curve |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | WEAK | Fill-vs-retrieve 477× rests on the scenario's parameters only |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 05's needle/effective-length result as a table. (2) Add a second cost pair (current flagship prices) to the 477× claim's caveat.

## Reviewer B — operations VP, refinery

Jargon before definition: 'wavelength' of RoPE without a one-line gloss. Sections that change no decision: RoPE identity proof is for engineers; the VP needs only the fill-vs-retrieve number. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Retrieve per step; never fill the window with the manual.

## Three answers
- Deeper than the strongest free source? Yes on the cost arithmetic.
- As deep as all free sources combined? No on positional mechanics.
- Single change that most increases depth: Reference output and a measured effective-length curve on one model.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.