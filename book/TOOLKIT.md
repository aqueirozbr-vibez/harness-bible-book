# Toolkit — decision aids that compute something

Every aid below is implemented in its chapter's `labs/chNN-*/derive.py` (and the lab's `run.py` where a measurement is involved). Inputs are what the plant supplies; outputs are what the aid returns. Illustrative defaults live in the scripts; the plant replaces them.

| Ch | Aid | Inputs | Outputs | Script |
|---|---|---|---|---|
| 01 | Per-language token cost | Corpus samples per language; tokenizer | Tokens per 1,000 words; identifier fragmentation rate | labs/ch01 |
| 02 | Retrieval geometry check | Embedding dimension; identifier list; golden queries | 1/√d noise floor; recall@k vector vs hybrid | labs/ch02 |
| 03 | Parameter-count verification | Six config integers | Parameter count vs published (±%) | labs/ch03 |
| 04 | KV-cache sizing | Layers, heads, head dim, precision, context, concurrency | Bytes per token; cache per sequence; GPU fit | labs/ch04 |
| 05 | Fill-vs-retrieve cost | Document tokens, queries/day, chunk tokens, prices | Cost ratio; monthly $ both ways | labs/ch05 |
| 06 | Tokens-per-parameter from scaling constants | Published fit constants; compute budget | Optimal tokens/param under each fit | labs/ch06 |
| 07 | Contamination and near-duplicate check | Corpus; golden set | MinHash near-duplicate rate; contamination share | labs/ch07 |
| 09 | Effort budget and best-of-N | Per-attempt accuracy; verifier quality; token prices | Accuracy vs reasoning tokens; sandwich saving | labs/ch09 |
| 10 | Serving capacity and cost per token | GPU memory/bandwidth, model size, precision, utilization | KV-capped concurrency; $/M tokens vs utilization | labs/ch10 |
| 11 | Quantization error bound | Weight distribution; bits; group size | Relative error 8/4-bit; outlier effect | labs/ch11 |
| 12 | Golden-set sizing | Base pass rate; effect to detect; k attempts | Wilson half-width; bootstrap power; items needed | labs/ch12 |
| 13 | Abstention threshold | Cost of wrong answer; cost of abstention; confidence distribution | Threshold; expected cost | labs/ch13 |
| 14 | Image token and register check | Image resolution; tag register | Tokens per image; confusion-class flags | labs/ch14 |
| 15 | Cache break-even, routing, crossover | Prices (cached/fresh/write), reuse count, routed share, volume | Break-even reuse; blended price; self-host crossover queries/month | labs/ch15 |
| 16 | Step-rate to task-rate | Per-step pass rate; steps | Task completion probability; pass^k | labs/ch16 |
| 17 | Clarification and scope arithmetic | Template fields; request samples | Clarification rate; scope-denial rate | labs/ch17 |
| 18 | Prefix and compliance measurement | Guide text; rule list; golden items | Prefix tokens; compliance per rule | labs/ch18 |
| 19 | Window budget | Section budgets; step inputs | Tokens per step; sections over budget | labs/ch19 |
| 20 | Stale-revision rate | Revisions/month; documents; re-index latency; retrievals | Stale share; stale retrievals/month | labs/ch20 |
| 21 | Retry and idempotency arithmetic | Calls per task; transient failure rate; retries | Task failure probability with/without retry | labs/ch21 |
| 22 | Repair cap | Repair-success histogram by attempt | Cap per class | labs/ch22 |
| 23 | Routing table cost and sensitivity | Tier prices; per-class effort; step counts; escalation rate | Task cost per configuration; savings with sensitivity; cascade cost | labs/ch23 |
| 24 | Memory recurrence | Retrieval probability; steps; provenance enforcement rate | Tasks touched per 100 | labs/ch24 |
| 25 | Credential exposure and schema surface | Token TTL; key lifetime; tools per class | Exposure ratio; prefix tokens saved | labs/ch25 |
| 26 | Sensor break-even and chain economics | Defect rate; sensor cost; catch rate; cost of failure | Break-even; marginal catch per sensor | labs/ch26 |
| 27 | Grader calibration and CI gate | Labels; verdicts; baseline/candidate pass vectors | κ per criterion; gate verdict with interval; gate cost | labs/ch27 |
| 29 | Record volume and chain verification | Tasks/month; records per task | Records/month; verification time; export size | labs/ch29 |
| 30 | Delegation break-even | Multiplier; per-task cost; cost of failure | Extra cost per task; quality gain needed | labs/ch30 |
| 31 | Gate routing, queue, and STP | Task mix; review rates; minutes per review; reviewers | Reviews/month; hours; wait (M/M/c); STP; gate cost/task | labs/ch31 |
| 32 | Cluster ranking and branch cost | Failure events; consequence weights; fixability | Ranked clusters; expected gain; branch cost | labs/ch32 |
| 33 | Catalogue coverage | Modes; detectors per class | Deterministic vs inferential coverage; before/after | labs/ch33 |
| 37 | Cost anatomy and cost per resolved task | All of the above plus oversight hours | Monthly anatomy; cost per resolved task; Pareto | labs/ch37 |

Aids that do not compute (checklists, templates, vendor questions) stay in their chapters' Layer 8.
