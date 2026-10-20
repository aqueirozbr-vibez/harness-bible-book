# Changelog

Integration of chapters 00–33 on 21 Sep 2026. One line per chapter; later changes append.

- ch00 The heuristic becomes the algorithm: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; prose preface; two frames, three impacts; prose-only lint mode added.
- ch01 Tokens and tokenizers: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch02 Embeddings and representation: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch03 The transformer block: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch04 Attention in depth: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; pilot; VERIFY found four arithmetic errors, fixed; independent redteam log.
- ch05 Positional encoding and long context: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch06 Scale: parameters, MoE, scaling laws: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; Chinchilla constants give 50–123 tokens/param, not ~20 (lab-confirmed).
- ch07 Pre-training data and pipelines: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch08 Post-training: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch09 Reasoning and test-time compute: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch10 Inference engineering: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch11 Quantization, distillation, small models: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; quantize() labelled illustrative absmax vs GPTQ/AWQ (redteam).
- ch12 Evaluation science: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch13 Failure science of models: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch14 Multimodality: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; dense-register correction from the lab; confusion-class pass added.
- ch15 Economics of models: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; cookbook evidence; price note relabelling the frontier tier (VERIFY).
- ch16 Thesis and evidence: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; expanded to map row; scaffold preprint marked pending verification.
- ch17 Task entry and outcome specification: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch18 Guides: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch19 Context engineering: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch20 Retrieval and knowledge: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch21 Control plane and durable execution: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; expanded: Temporal/AgentCore internals; idempotency fix from the lab.
- ch22 The agent loop and workflow patterns: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; expanded: five patterns; negative results added from the lab.
- ch23 Model layer, routing, gateways: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; effort placement dominates tier (78%/14%); sensitivity 72/75/78 (redteam).
- ch24 Memory: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; consolidate() logs rejections (lab fix).
- ch25 Tools, MCP, execution environments: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch26 Sensors and verification: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; expanded: sensor families and gates; message template fix from the lab.
- ch27 Graders and agent evaluation: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch28 Permissions, policy, security: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; expanded: network policy, credentials, intent validation; Rego conflict fix from the lab.
- ch29 Observability and audit: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; expanded; OTel status corrected (Development, not stable); revision pinned.
- ch30 Multi-agent systems and protocols: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; double-counted delegation tokens fixed from the lab (15%, not a third).
- ch31 Human-in-the-loop: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; budgeted router replaced per-item weighting (lab fix); fatigue model labelled illustrative.
- ch32 Self-improving harnesses: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review.
- ch33 Failure catalogue: drafted, lab reproducing, VERIFY batch, REDTEAM pre-review; citation-row count corrected to the measured 22 chapters.