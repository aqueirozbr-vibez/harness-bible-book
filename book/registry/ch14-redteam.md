# REDTEAM — Chapter 14 — Multimodality (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Anthropic/OpenAI vision docs; Dosovitskiy 2020)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Register-validation result shown only in Layer 2 |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | WEAK | Nine source rows — thin |

Must change: (1) Show Lab 14's confusion-class output. (2) Add sources for OCR baselines and P&ID datasets or mark open.

## Reviewer B — operations VP, refinery

Jargon before definition: 'patch', 'register' before gloss. Sections that change no decision: Patch arithmetic; VP needs 'validate every tag against the register'. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Vision for extraction with register validation; never for identity alone.

## Three answers
- Deeper than the strongest free source? Yes on register validation.
- As deep as all free sources combined? No.
- Single change that most increases depth: Reference output; sources.

## Change list
- CRITICAL: none.
- MAJOR: A1; A2 sources.
- MINOR: B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.