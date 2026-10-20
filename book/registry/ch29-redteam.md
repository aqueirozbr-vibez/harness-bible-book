# REDTEAM — Chapter 29 — Observability and audit (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read OTel GenAI conventions; Langfuse docs; NIST/ISO)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | WEAK | OTel status corrected at VERIFY; the attribute table should carry the revision number |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Completeness check has no example |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Add the semconv revision the harness pins (v1.41/1.44) to the table caption. (2) Show Lab 29's chain-verification output.

## Reviewer B — operations VP, refinery

Jargon before definition: 'hash chain', 'anchor' before gloss. Sections that change no decision: Collector section. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Seven records, chained, mapped once to every framework.

## Three answers
- Deeper than the strongest free source? Yes.
- As deep as all free sources combined? Yes.
- Single change that most increases depth: Reference output.

## Change list
- CRITICAL: none.
- MAJOR: A1 revision; A2.
- MINOR: B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.