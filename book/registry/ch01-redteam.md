# REDTEAM — Chapter 01 — Tokens and tokenizers (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Huyen ch.2; Petrov 2023; HF tokenizers docs)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Protocol stated, no example output shown |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | WEAK | Portuguese cost figure is one corpus |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show the lab's tokens/1,000-words table in Layer 4. (2) State the tokenizer-drift test as a golden-set item, not advice.

## Reviewer B — operations VP, refinery

Jargon before definition: 'byte fallback', 'pre-tokenizer' before gloss. Sections that change no decision: Vocabulary-economics arithmetic changes no plant decision beyond 'measure your tags'. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Budget Portuguese at 1.5× and validate tags by register, not by the model.

## Three answers
- Deeper than the strongest free source? Yes on industrial tag arithmetic.
- As deep as all free sources combined? No — HF docs carry algorithm internals this chapter summarizes.
- Single change that most increases depth: Publish the lab's per-language table with a second industrial corpus.

## Change list
- CRITICAL: none.
- MAJOR: A1 reference output.
- MINOR: B1 glosses.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.