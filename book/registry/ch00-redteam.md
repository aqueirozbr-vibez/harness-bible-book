# REDTEAM — Chapter 00 — The heuristic becomes the algorithm (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read McKinsey CEO primer; Nielsen 2023)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | WEAK | Prose-only by design; the funnel is asserted more than argued for a reader who has not read Martin |
| 2 Mechanism | PASS | Prose-only chapter by map row |
| 3 Worked numbers | PASS | Prose-only chapter by map row |
| 4 Measurement | PASS | Prose-only chapter by map row |
| 5 Failure | PASS | Prose-only chapter by map row |
| 6 Frontier | WEAK | No stopping points stated for the two sources beyond the closing note |
| 7 Industrial application | PASS | Prose-only chapter by map row |
| 8 Decision aids | PASS | Prose-only chapter by map row |
| 9 Sources | PASS | Prose-only chapter by map row |

Must change: (1) State in one sentence what Martin's funnel does not cover (probabilistic execution) rather than implying it. (2) Give the reader one concrete 'heuristic → algorithm' example with a number earlier than the P-101 paragraph.

## Reviewer B — operations VP, refinery

Jargon before definition: 'harness' used before its definition paragraph; 'system of record' unglossed. Sections that change no decision: The two-frames synthesis paragraph could be halved. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Whether to fund the harness rather than wait for the next model.

## Three answers
- Deeper than the strongest free source? Yes — neither source connects funnel, interface, and division of labour to a plant.
- As deep as all free sources combined? Yes for the frame; the evidence is in the later chapters.
- Single change that most increases depth: Move the harness definition paragraph up before the three impacts.

## Change list
- CRITICAL: none.
- MAJOR: A1 funnel limit stated explicitly.
- MINOR: B1 gloss 'system of record'; A2 early example.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.