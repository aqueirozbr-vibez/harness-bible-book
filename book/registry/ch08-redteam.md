# REDTEAM — Chapter 08 — Post-training (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Ouyang 2022; Rafailov 2023 (DPO); Shao 2024 (GRPO); Huyen)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Refusal-rate and reward-hacking measurements have no example |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | WEAK | Adapter-selection guidance is stated without a measured regression example |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 08's reward-hacking demo output. (2) Name the safety-set size and cadence in Layer 4 with a number.

## Reviewer B — operations VP, refinery

Jargon before definition: 'DPO', 'GRPO' acronyms before expansion. Sections that change no decision: Algorithm sections; the VP needs 'never train on unreviewed outputs' and the safety-set rule. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Quarterly, reviewed, golden-set-gated adapters only.

## Three answers
- Deeper than the strongest free source? Yes on the industrial rules.
- As deep as all free sources combined? No on algorithms.
- Single change that most increases depth: Reference output.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.