# REDTEAM — Chapter 02 — Embeddings and representation (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Huyen ch.3; Voyage/OpenAI embedding docs)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | No example recall table |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | WEAK | Hybrid retrieval evidence is the lab's synthetic corpus only |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 02's recall@1 vector vs hybrid table in Layer 4. (2) Name one production embedding model's dimension and price in the frontier layer with tier.

## Reviewer B — operations VP, refinery

Jargon before definition: '1/√d noise floor' needs a sentence before the equation. Sections that change no decision: Geometry section long relative to the one decision (hybrid). Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Hybrid retrieval with identifiers indexed lexically is a procurement requirement.

## Three answers
- Deeper than the strongest free source? Yes on the identity-vs-meaning failure.
- As deep as all free sources combined? No — vendor docs carry model specifics.
- Single change that most increases depth: Reference output and a real embedding model comparison.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.