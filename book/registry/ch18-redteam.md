# REDTEAM — Chapter 18 — Guides (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Anthropic prompt docs; AGENTS.md convention; Karpathy on skills)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | WEAK | Worked numbers thin (133 words) — compliance figures live in Layer 2 |
| 4 Measurement | WEAK | No compliance-per-rule example |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 18's compliance-per-rule table. (2) Move the prefix token arithmetic into Layer 3.

## Reviewer B — operations VP, refinery

Jargon before definition: 'byte-stable' before gloss. Sections that change no decision: Anti-patterns list could be a table. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Guides are versioned code with compliance tests.

## Three answers
- Deeper than the strongest free source? Yes.
- As deep as all free sources combined? Yes for guides.
- Single change that most increases depth: Reference output.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.