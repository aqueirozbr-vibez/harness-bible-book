# REDTEAM — Chapter 28 — Permissions, policy, security (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read OPA/Cedar docs; CaMeL; Rule of Two; Willison)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Policy-test results not shown |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 28's decision output.

## Reviewer B — operations VP, refinery

Jargon before definition: 'PDP/PEP' before gloss. Sections that change no decision: Two-engines comparison is long. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: PDP outside the model; fail-closed; intent validation.

## Three answers
- Deeper than the strongest free source? Yes.
- As deep as all free sources combined? Yes.
- Single change that most increases depth: Reference output.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.