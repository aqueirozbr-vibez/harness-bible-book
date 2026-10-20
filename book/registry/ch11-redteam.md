# REDTEAM — Chapter 11 — Quantization, distillation, small models (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Frantar 2022 (GPTQ); Lin 2023 (AWQ); Dettmers 2022)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | WEAK | The chapter's absmax scheme is illustrative; AWQ/GPTQ differ |
| 4 Measurement | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | WEAK | Portuguese asymmetry is asserted from the lab's synthetic test |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Label the quantize() scheme as illustrative in Layer 2. (2) Cite one published per-language quantization regression or mark open.

## Reviewer B — operations VP, refinery

Jargon before definition: 'g=128 group size' before gloss. Sections that change no decision: Error arithmetic long. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: 8-bit for routine, 16-bit for judgment; measure per language.

## Three answers
- Deeper than the strongest free source? Yes on the decision framing.
- As deep as all free sources combined? No on algorithms.
- Single change that most increases depth: Reference output and a published per-language number.

## Change list
- CRITICAL: none.
- MAJOR: A1 label scheme.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.