# REDTEAM — Chapter 23 — Model layer, routing, gateways (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read RouteLLM; LiteLLM/Portkey docs; Cookbook)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | WEAK | Effort-vs-tier finding rests on an assumed 2,000 reasoning tokens — state sensitivity |
| 4 Measurement | WEAK | No routing report example |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Add a sensitivity line: at 500 reasoning tokens the effort saving falls to X (derive.py). (2) Show Lab 23's cascade/classifier output.

## Reviewer B — operations VP, refinery

Jargon before definition: 'cascade', 'advisor' before gloss. Sections that change no decision: Gateway function list. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Effort first, tier second, per class; gateway with hard caps.

## Three answers
- Deeper than the strongest free source? Yes.
- As deep as all free sources combined? Yes with the cookbook ladder.
- Single change that most increases depth: Sensitivity line.

## Change list
- CRITICAL: none.
- MAJOR: A1 sensitivity; A2.
- MINOR: B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.