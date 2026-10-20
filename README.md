# The Harness Bible

A reference work on large language models and harness engineering: how the models work (Part I), how to build the harness around them, from guides and context to the agent loop, tools, sensors, graders, permissions, observability and human review (Part II), and how to apply both in industrial operations, with the boundary to operational technology respected (Part III).

Every chapter has the same nine layers: intuition, mechanism, worked numbers, measurement, failure, the frontier, industrial application, decision aids and sources. Figures in the text carry their provenance: a cited source with its tier, a derivation by the chapter's lab, or a mark saying it is illustrative. Each chapter ends with a table of its sources.

The interactive edition of the book, with a reader, an assistant that answers from the book and cites it, and a way to propose improvements that are scored and reviewed, is a separate application: https://github.com/aqueirozbr-vibez/harness-bible

## What is here

- `book/`: the chapters, by part (`book/part0` to `book/part3`), and the book-level files: the chapter map with each chapter's status, the glossary, every chapter's sources in one table, the toolkit, the failure index and the changelog. `book/registry/` holds each chapter's source registry and its verification, red-team and integration logs.
- `labs/`: one folder for each chapter that has a lab. A lab runs the chapter's own code and reproduces the figures the chapter derives.
- `harness-bible.skill`: the authoring skill (a zip) that drives the research, drafting and verification of a chapter. `.scripts/` holds its scripts.

## Chapters

### Part 0 — Why now (prose only, no labs)

- [Chapter 00 — The heuristic becomes the algorithm](book/part0/ch00-the-heuristic-becomes-the-algori.md)

### Part I — Foundations of language models

- [Chapter 01 — Tokens and tokenizers](book/part1/ch01-tokens-and-tokenizers.md)
- [Chapter 02 — Embeddings and representation](book/part1/ch02-embeddings-and-representation.md)
- [Chapter 03 — The transformer block](book/part1/ch03-the-transformer-block.md)
- [Chapter 04 — Attention in depth](book/part1/ch04-attention.md)
- [Chapter 05 — Positional encoding and long context](book/part1/ch05-positional-encoding-and-long-con.md)
- [Chapter 06 — Scale: parameters, MoE, scaling laws](book/part1/ch06-scale-parameters-moe-scaling-law.md)
- [Chapter 07 — Pre-training data and pipelines](book/part1/ch07-pre-training-data-and-pipelines.md)
- [Chapter 08 — Post-training](book/part1/ch08-post-training.md)
- [Chapter 09 — Reasoning and test-time compute](book/part1/ch09-reasoning-and-test-time-compute.md)
- [Chapter 10 — Inference engineering](book/part1/ch10-inference-engineering.md)
- [Chapter 11 — Quantization, distillation, small models](book/part1/ch11-quantization-distillation-small-.md)
- [Chapter 12 — Evaluation science](book/part1/ch12-evaluation-science.md)
- [Chapter 13 — Failure science of models](book/part1/ch13-failure-science-of-models.md)
- [Chapter 14 — Multimodality](book/part1/ch14-multimodality.md)
- [Chapter 15 — Economics of models](book/part1/ch15-economics-of-models.md)

### Part II — Harness engineering

- [Chapter 16 — Thesis and evidence](book/part2/ch16-thesis-and-evidence.md)
- [Chapter 17 — Task entry and outcome specification](book/part2/ch17-task-entry-and-outcome-specifica.md)
- [Chapter 18 — Guides](book/part2/ch18-guides.md)
- [Chapter 19 — Context engineering](book/part2/ch19-context-engineering.md)
- [Chapter 20 — Retrieval and knowledge](book/part2/ch20-retrieval-and-knowledge.md)
- [Chapter 21 — Control plane and durable execution](book/part2/ch21-control-plane-and-durable-execut.md)
- [Chapter 22 — The agent loop and workflow patterns](book/part2/ch22-the-agent-loop-and-workflow-patt.md)
- [Chapter 23 — Model layer, routing, gateways](book/part2/ch23-model-layer-routing-gateways.md)
- [Chapter 24 — Memory](book/part2/ch24-memory.md)
- [Chapter 25 — Tools, MCP, execution environments](book/part2/ch25-tools-mcp-execution-environments.md)
- [Chapter 26 — Sensors and verification](book/part2/ch26-sensors-and-verification.md)
- [Chapter 27 — Graders and agent evaluation](book/part2/ch27-graders-and-agent-evaluation.md)
- [Chapter 28 — Permissions, policy, security](book/part2/ch28-permissions.md)
- [Chapter 29 — Observability and audit](book/part2/ch29-observability-and-audit.md)
- [Chapter 30 — Multi-agent systems and protocols](book/part2/ch30-multi-agent-systems-and-protocol.md)
- [Chapter 31 — Human-in-the-loop](book/part2/ch31-human-in-the-loop.md)
- [Chapter 32 — Self-improving harnesses](book/part2/ch32-self-improving-harnesses.md)
- [Chapter 33 — Failure catalogue](book/part2/ch33-failure-catalogue.md)

### Part III — Industrial application

- Chapter 34 — Selecting use cases (not yet written)
- Chapter 35 — OT/IT and functional safety (not yet written)
- Chapter 36 — Regulation (not yet written)
- [Chapter 37 — Economics and TCO](book/part3/ch37-economics.md)
- Chapter 38 — Build, buy, assemble (not yet written)
- Chapter 39 — Roadmap and maturity (not yet written)
- Chapter 40 — Running a proof (not yet written)

## Running the labs

Each lab's README says what it reproduces, what it needs and how long it takes. Most labs need Python 3.9 or later and nothing else; some also need NumPy, and `labs/ch04-attention` lists its packages in a `requirements.txt`. Run a lab from its own folder:

```
cd labs/ch28-permissions
python run.py
```

A lab exits with 0 when everything it checks reproduced. It writes its outputs to its `results/` folder, which holds the outputs the chapter cites.

## License

The text of the book is licensed under the Creative Commons Attribution 4.0 International License ([LICENSE](LICENSE)). The code in `labs/` and `.scripts/`, and the scripts inside `harness-bible.skill`, is licensed under the MIT License ([LICENSE-CODE](LICENSE-CODE)).

Copyright (c) 2026 Andre Ponto.
