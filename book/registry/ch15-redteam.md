# REDTEAM — Chapter 15 — Economics of models (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Vendor pricing pages; RouteLLM; FrugalGPT; Cookbook)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | No example cost report |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | WEAK | Price note now flags tier drift — figures should be re-derived at flagship prices in a second column |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Add a second price pair column (flagship) to the break-even table via derive.py. (2) Show Lab 15's break-even output.

## Reviewer B — operations VP, refinery

Jargon before definition: 'blended price' before gloss. Sections that change no decision: Price-fall history section. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Cache first, route second, model last; measure per class.

## Three answers
- Deeper than the strongest free source? Yes on structure.
- As deep as all free sources combined? Yes with the cookbook evidence.
- Single change that most increases depth: Flagship-price column.

## Change list
- CRITICAL: none.
- MAJOR: A1 flagship column.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.