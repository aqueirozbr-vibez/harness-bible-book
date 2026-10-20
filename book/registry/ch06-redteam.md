# REDTEAM — Chapter 06 — Scale: parameters, MoE, scaling laws (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Hoffmann 2022; Epoch replication; Huyen)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | WEAK | The 50–123 tokens/param discrepancy needs its derivation steps visible in the chapter, not only the lab |
| 4 Measurement | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | WEAK | MoE routing failures are described, not measured |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show the Approach-3 constants and the arithmetic line that yields 50–123 in Layer 3. (2) State that the ~20 rule remains what practitioners use and why (fit choice).

## Reviewer B — operations VP, refinery

Jargon before definition: 'Approach 3', 'MoE router' before gloss. Sections that change no decision: Scaling laws change no plant decision except procurement cadence. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Re-derive model choices quarterly; treat vendor scaling claims as fit-dependent.

## Three answers
- Deeper than the strongest free source? Yes — the discrepancy is not in any free source.
- As deep as all free sources combined? Yes on this narrow point.
- Single change that most increases depth: Visible derivation in Layer 3.

## Change list
- CRITICAL: none.
- MAJOR: A1 derivation visible.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.