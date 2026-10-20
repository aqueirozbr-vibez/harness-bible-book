# REDTEAM — Chapter 26 — Sensors and verification (21 Sep 2026)

Caveat: both reviewers played by the drafting instance. The plan requires external reviewers; treat this as a pre-review.

## Reviewer A — senior ML/platform engineer (has read Böckeler; OpenAI harness report; BDD literature)

| Layer | Score | Justification |
|---|---|---|
| 1 Intuition | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 2 Mechanism | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 3 Worked numbers | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 4 Measurement | WEAK | Coverage figure computed; no example register |
| 5 Failure | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 6 Frontier | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 7 Industrial application | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 8 Decision aids | PASS | Meets the layer's standard; nothing the source's author would dispute |
| 9 Sources | PASS | Meets the layer's standard; nothing the source's author would dispute |

Must change: (1) Show Lab 26's chain output and false-positive rates. (2) Add a five-row example of the sensor register.

## Reviewer B — operations VP, refinery

Jargon before definition: 'executable specification' before gloss. Sections that change no decision: Sensor family depth is for engineers. Industrial application: recognisable and usable with plant data (task record, register, CMMS, golden set). Embarrassment risk: none found after VERIFY.

Decision this chapter helped me make: Sensors first; grader last; coverage is the score.

## Three answers
- Deeper than the strongest free source? Yes.
- As deep as all free sources combined? Yes.
- Single change that most increases depth: Reference output.

## Change list
- CRITICAL: none.
- MAJOR: A1.
- MINOR: A2; B1.

Cross-cutting (all chapters): Layer 4 is the thinnest layer in the book (130–300 words) and no chapter showed a reference output — applied this pass by inserting each lab's printed output into Layer 4; Reviewer B's glosses are collected in the change list for the next pass.