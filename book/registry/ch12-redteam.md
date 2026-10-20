# REDTEAM — Chapter 12 — Evaluation science (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Huyen ch.4; Efron 1979; Zheng 2023)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Power table computed; no example golden-set report shown |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | WEAK | Portuguese permit-class finding is illustrative |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 12's κ and power output. (2) Add a one-page golden-set report template.

## Reviewer B — operations VP, refinery

Jargon before definition: 'Wilson interval', 'paired bootstrap' before gloss. Sections that change no decision: Statistics sections long; the VP needs the sizing rule and the ceiling. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: 300 items per class at k=4; two labelers; intervals not points.

## Three answers
- Deeper than the strongest free source? Yes on the harness-specific protocol.
- As deep as all free sources combined? No on statistics.
- Single change that most increases depth: Report template.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.