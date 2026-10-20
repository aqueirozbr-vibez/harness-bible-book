# Chapter map

Four parts, 40 chapters, 30 labs. Each row: scope, the lab, the free sources it must beat, word budget. Read the row before starting any step on a chapter.

## Part 0 — Why now (prose only, no labs)

| Ch | Title | Scope | Beats | Words |
|---|---|---|---|---|
| 00 | The heuristic becomes the algorithm | The knowledge funnel (Martin 2009); intent-based interaction (Nielsen 2023); the three impacts — interface, curation, division of labour. Written as continuous prose; nothing boxed or numbered. | McKinsey CEO primer; Nielsen | 3,000–4,000 |

## Part I — Foundations of language models

| Ch | Title | Scope | Lab | Beats | Words |
|---|---|---|---|---|---|
| 01 | Tokens and tokenizers | BPE/Unigram/WordPiece algorithms with merge tables; byte fallback; vocabulary economics (embedding matrix size); per-language cost; numbers and code tokenization; tokenizer drift across model versions | Lab 01: train a BPE tokenizer on an industrial corpus; measure tokens/1,000 words for PT/EN/DE; measure P&ID legend cost | Huyen ch.2; Petrov 2023; HF tokenizers docs | 7–9K |
| 02 | Embeddings and representation | Token, positional, and sentence embeddings; dimensionality; similarity geometry; why retrieval works and where it fails; embedding models and drift | Lab 02: embed a procedure corpus; measure nearest-neighbour quality vs keyword search on tag queries | Huyen ch.6; OpenAI/Cohere embedding docs | 6–8K |
| 03 | The transformer block | Residual stream; attention and MLP sub-blocks; normalisation; parameter accounting per layer; where knowledge is stored (mechanistic-interpretability evidence) | Lab 03: implement a minimal decoder block in PyTorch; count parameters; match a published model's total | Vaswani 2017; Karpathy nanoGPT; Anthropic interpretability posts | 8–10K |
| 04 | Attention in depth | Q/K/V derivation; softmax scaling; multi-head; causal masking; quadratic cost; FlashAttention; GQA/MQA; sparse and sliding-window; MLA | Lab 04: measure attention time vs sequence length; reproduce the quadratic curve; compare GQA cache size | Vaswani 2017; Dao 2022–24; Ainslie 2023; DeepSeek-V2 MLA | 8–10K |
| 05 | Positional encoding and long context | Sinusoidal, learned, RoPE, ALiBi; context extension (YaRN, NTK); effective vs advertised length; NoLiMa, RULER; retrieval vs long context | Lab 05: run a needle test and a NoLiMa-style test on two models; plot accuracy vs length | Modarressi 2025; RULER; Gemini 2.5 report | 7–9K |
| 06 | Scale: parameters, MoE, scaling laws | Kaplan and Chinchilla; over-training economics; MoE routing, load balancing, expert parallelism; memory vs compute accounting | Lab 06: fit a scaling curve on published points; compute Chinchilla-optimal tokens for a given budget | Hoffmann 2022; Epoch replication; DeepSeek-V3 report; Switch Transformer | 7–9K |
| 07 | Pre-training data and pipelines | Corpus construction; dedup; quality filtering; mixtures; contamination; data governance parallels for enterprise corpora | Lab 07: build a dedup + quality-filter pipeline on a document dump; measure removal rates | Llama 3 paper; FineWeb; Dolma | 6–8K |
| 08 | Post-training | SFT data design; reward models; PPO; DPO derivation; RLAIF/Constitutional; RLVR and GRPO; reward hacking; sycophancy | Lab 08: run DPO on a small model with a preference set; measure win-rate shift | Ouyang 2022; Rafailov 2023; Bai 2022; DeepSeek-R1 | 9–11K |
| 09 | Reasoning and test-time compute | CoT; reasoning models; effort budgets; verifiers; process vs outcome rewards; when reasoning helps and hurts; cost of hidden tokens | Lab 09: accuracy vs reasoning tokens vs cost on a public benchmark across effort levels | DeepSeek-R1; OpenAI o-series cards; Snell 2024 test-time compute | 7–9K |
| 10 | Inference engineering | Prefill/decode; KV cache arithmetic; memory wall; batching; PagedAttention; speculative decoding; serving stacks; latency/throughput/cost | Lab 10: serve a 7B model with vLLM; measure TTFT, tokens/s, cache use vs batch size | Kwon 2023; vLLM/TensorRT-LLM docs; Huyen ch.9 | 9–11K |
| 11 | Quantization, distillation, small models | FP8/INT8/INT4; AWQ/GPTQ/GGUF; accuracy loss measurement; distillation; when SLMs substitute (Belcak 2025) | Lab 11: quantize a model at three precisions; measure quality delta on a golden set | Belcak 2025; AWQ/GPTQ papers | 6–8K |
| 12 | Evaluation science | Golden sets; metrics; statistics (CIs, paired bootstrap); contamination; LLM-as-judge biases and calibration (κ, α); benchmark reading | Lab 12: build a golden set; calibrate a judge against human labels; report κ | Zheng 2023; Inspect AI docs; RAND judge study | 8–10K |
| 13 | Failure science of models | Hallucination as classification error; calibration; sycophancy; bias; injection at the model level; refusal behaviour | Lab 13: measure abstention vs accuracy trade-off with an uncertainty prompt | Kalai 2025; OWASP LLM01; Anthropic sycophancy work | 6–8K |
| 14 | Multimodality | Vision encoders; document and drawing understanding; audio; where P&ID reading works and fails | Lab 14: extract tags from P&ID images; measure precision/recall | Model cards; DocVQA | 5–7K |
| 15 | Economics of models | The four billing lines; caching mechanics and prefix ordering; batch APIs; routing; self-host break-even; cost anatomy | Lab 15: instrument a gateway; reproduce the four-configuration TCO on live traffic | Vendor pricing; FinOps FOCUS; RouteLLM; FrugalGPT | 7–9K |

## Part II — Harness engineering

| Ch | Title | Scope | Lab | Beats | Words |
|---|---|---|---|---|---|
| 16 | Thesis and evidence | Agent = Model + Harness; same-model/different-scaffold data; pass^k; the guides/sensors 2×2; every component encodes an assumption | Lab 16: run one model under two scaffolds on a task set; measure the spread | LangChain anatomy; Böckeler; τ-bench; Anthropic long-running | 6–8K |
| 17 | Task entry and outcome specification | Intents vs commands; acceptance criteria as specification; intake schemas; webhooks and triggers; intent validation | Lab 17: build an intake form with machine-checkable criteria; measure clarification rate | OpenAI guide; Managed Agents webhooks | 6–8K |
| 18 | Guides | System prompts; rules; AGENTS.md; skills and progressive disclosure; spec-driven guides (PRD/ADR/BDD); guides as code; prompt-caching order | Lab 18: version a guide set in Git; measure prefix cache hit rate and behaviour change per guide edit | Anthropic prompting docs; Agent Skills; Böckeler; OpenAI Codex report | 8–10K |
| 19 | Context engineering | Attention budget; per-step assembly; compaction; the three rots; measuring window size; sub-agent summaries | Lab 19: log tokens per step across a long task; apply compaction; measure quality vs window | Anthropic context engineering; Darú compaction chapter | 8–10K |
| 20 | Retrieval and knowledge | Ingestion pipelines; chunking in tokens; hybrid search; metadata filters; re-ranking; citations; governance as precondition; context graphs | Lab 20: build hybrid RAG over procedures; measure precision/recall, citation coverage, stale-revision rate | Huyen ch.6; Anthropic contextual retrieval; LlamaIndex/LangChain docs | 9–11K |
| 21 | Control plane and durable execution | Orchestrator; activities vs workflows; retries; idempotency; budgets; approval states; Temporal and AgentCore internals | Lab 21: run an agent as a Temporal workflow; kill the worker mid-task; verify resume without duplicate side effects | Temporal docs; AgentCore docs; 12-Factor | 8–10K |
| 22 | The agent loop and workflow patterns | Plan/Act/Observe/Verify/Repair/Submit; prompt chaining, routing, parallelisation, orchestrator–workers, evaluator–optimizer; when to use each | Lab 22: implement the loop with capped repair; measure iterations and repair success | Anthropic Building Effective Agents; OpenAI guide | 8–10K |
| 23 | Model layer, routing, gateways | Primary/fallback/grader; routers (classifier, cascade, semantic); LiteLLM/Portkey; measured vs vendor savings; version pinning | Lab 23: route a golden set through two models; report savings with CIs and quality retention | RouteLLM; FrugalGPT; RouterArena; gateway docs | 8–10K |
| 24 | Memory | CoALA classes; stores and lifetimes; curation vs accumulation; consolidation (dreaming); provenance; privacy; poisoning | Lab 24: implement four memory classes; inject a wrong fact; measure recurrence with and without provenance checks | Sumers 2023; Managed Agents memory; Darú memory chapter | 8–10K |
| 25 | Tools, MCP, execution environments | Tool schemas; risk classes; MCP protocol internals; sandboxes; browser automation; code-execution pattern; credentials never in the model | Lab 25: expose three tools over MCP; run in an ephemeral sandbox with egress rules; test an injection via tool output | MCP spec; Anthropic writing effective tools; E2B docs | 9–11K |
| 26 | Sensors and verification | Computational vs inferential; tests, schema, lint, static analysis, security scans, domain rules, citation checks; executable specs; sensor messages written for the model; verification gates | Lab 26: build a sensor chain; measure false positive/negative rates on a golden set | Böckeler; OpenAI Codex report; Anthropic long-running | 8–10K |
| 27 | Graders and agent evaluation | Judge design; isolated-context graders (outcomes); calibration; agent benchmarks (SWE-bench, τ-bench, AgentDojo, GAIA); regression gates in CI | Lab 27: build a grader with rubric; calibrate; wire as a CI gate | Zheng 2023; Managed Agents outcomes; Inspect AI; AgentDojo | 8–10K |
| 28 | Permissions, policy, security | PDP outside the model; OPA/Cedar; dual identity; fail-closed; short-lived credentials; network policy; prompt injection defences (CaMeL, Rule of Two, lethal trifecta); intent validation | Lab 28: wrap tools with an OPA PDP; measure decision latency; run AgentDojo attacks with and without the gate | OWASP; CaMeL; Meta Rule of Two; OPA docs; Darú permissions chapter | 10–12K |
| 29 | Observability and audit | OTel GenAI conventions; traces, tool logs, diffs, costs, decision records, interventions; hash-chained logs; replay; evidence mapping to NIST/ISO/LGPD/EU AI Act | Lab 29: instrument the loop with OTel; replay a task from history; export an audit pack | OTel spec; Langfuse/Phoenix docs; NIST AI RMF | 8–10K |
| 30 | Multi-agent systems and protocols | When to delegate (three scenarios); coordinator/specialists; permission intersection; A2A vs MCP; token multipliers (4×/15×); dynamic workflows | Lab 30: single vs multi-agent on one task; measure tokens, quality, and failure modes | Anthropic multi-agent research post; A2A spec; dynamic workflows post | 8–10K |
| 31 | Human-in-the-loop | Approval gates as workflow states; routing by risk; rejection reasons feeding repair; approval fatigue; audit of interventions | Lab 31: add gates; measure wait time and rejection rate over a task set | Temporal signals; OpenAI guardrails | 5–7K |
| 32 | Self-improving harnesses | The steering loop; consolidation; agent-generated harnesses; what stays human-owned; safety of self-modification | Lab 32: run a weekly steering loop on logged failures; measure failure-class recurrence | Böckeler steering loop; dynamic workflows; Managed Agents dreaming | 6–8K |
| 33 | Failure catalogue | Every failure mode in the book with mechanism, detection, mitigation, owner; cross-indexed | — (instrument instead) | OWASP; AgentDojo; SHADE-Arena | 6–8K |

## Part III — Industrial application

| Ch | Title | Scope | Lab | Beats | Words |
|---|---|---|---|---|---|
| 34 | Selecting use cases | Funnel stage; Verifiability Index; scoring matrix; when not to build | — (scorer) | Anthropic/OpenAI gating; Gartner | 5–7K |
| 35 | OT/IT and functional safety | Purdue; IEC 62443 zones and conduits; IEC 61508/61511; data diodes; brokers; what an agent may read/write/never touch | Lab 35: build a read-only historian broker; prove no write path exists | CISA/NCSC agent guidance; IEC texts | 6–8K |
| 36 | Regulation | EU AI Act as amended; LGPD; PL 2338; NIST AI RMF; ISO 42001; shared-control evidence | — (control map) | Official texts | 6–8K |
| 37 | Economics and TCO | Cost anatomy; baseline and counterfactual; process vs harness metrics; break-even; FinOps | Lab 37: the four-configuration model on live gateway data | FinOps Foundation; vendor pricing | 6–8K |
| 38 | Build, buy, assemble | Layer-by-layer; lock-in; portability; vendor questions | — (checklist) | Gartner | 4–6K |
| 39 | Roadmap and maturity | Stages with entry/exit criteria; scored maturity instrument; interoperability with Darú's Harness Score | — (instrument) | Darú | 5–7K |
| 40 | Running a proof | How to run and report a four-week proof: hypothesis, baseline, kill gate, two-document deliverable, negative results | Lab 40: a complete proof template with eval harness | Practitioner proof-of-concept playbooks | 5–7K |

## Part IV — Labs and appendices
Labs 01–40 as listed; each a folder with README, environment file, data, and a script that prints the reproduced number. Appendices: A glossary; B source registry; C data tables behind every chart; D benchmark replication logs; E toolkit.

<!-- STATUS (generated; do not edit by hand) -->

## Status — 2026-09-23

35/41 drafted · 34 labs reproducing · 34 verified · 34 red-teamed · 35 integrated. Words are prose + tables (code excluded), the linter's count.

| Ch | Title | Drafted | Words | Lab | Registry | Verify | Redteam | Integrate | Sources |
|---|---|---|---|---|---|---|---|---|---|
| 00 | The heuristic becomes the algorithm | y | 3205 | none (by row) | y | y | y | y | — |
| 01 | Tokens and tokenizers | y | 4566 | REPRODUCED | y | y | y | y | 14 rows, 0 needs fetch |
| 02 | Embeddings and representation | y | 4613 | REPRODUCED | y | y | y | y | 13 rows, 0 needs fetch |
| 03 | The transformer block | y | 4694 | REPRODUCED | y | y | y | y | 14 rows, 0 needs fetch |
| 04 | Attention in depth | y | 7891 | REPRODUCED | y | y | y | y | 21 rows, 0 needs fetch |
| 05 | Positional encoding and long context | y | 4666 | REPRODUCED | y | y | y | y | 15 rows, 0 needs fetch |
| 06 | Scale: parameters, MoE, scaling laws | y | 4612 | REPRODUCED | y | y | y | y | 14 rows, 0 needs fetch |
| 07 | Pre-training data and pipelines | y | 4590 | REPRODUCED | y | y | y | y | 15 rows, 0 needs fetch |
| 08 | Post-training | y | 4614 | REPRODUCED | y | y | y | y | 17 rows, 0 needs fetch |
| 09 | Reasoning and test-time compute | y | 4760 | REPRODUCED | y | y | y | y | 15 rows, 0 needs fetch |
| 10 | Inference engineering | y | 4625 | REPRODUCED | y | y | y | y | 13 rows, 0 needs fetch |
| 11 | Quantization, distillation, small mode | y | 4659 | REPRODUCED | y | y | y | y | 15 rows, 0 needs fetch |
| 12 | Evaluation science | y | 4645 | REPRODUCED | y | y | y | y | 13 rows, 0 needs fetch |
| 13 | Failure science of models | y | 4591 | REPRODUCED | y | y | y | y | 11 rows, 0 needs fetch |
| 14 | Multimodality | y | 4848 | REPRODUCED | y | y | y | y | 9 rows, 0 needs fetch |
| 15 | Economics of models | y | 4992 | REPRODUCED | y | y | y | y | 13 rows, 1 needs fetch |
| 16 | Thesis and evidence | y | 6107 | REPRODUCED | y | y | y | y | 14 rows, 1 needs fetch |
| 17 | Task entry and outcome specification | y | 6324 | REPRODUCED | y | y | y | y | 9 rows, 0 needs fetch |
| 18 | Guides | y | 7166 | REPRODUCED | y | y | y | y | 15 rows, 0 needs fetch |
| 19 | Context engineering | y | 7324 | REPRODUCED | y | y | y | y | 11 rows, 0 needs fetch |
| 20 | Retrieval and knowledge | y | 7116 | REPRODUCED | y | y | y | y | 12 rows, 0 needs fetch |
| 21 | Control plane and durable execution | y | 7136 | REPRODUCED | y | y | y | y | 10 rows, 0 needs fetch |
| 22 | The agent loop and workflow patterns | y | 7078 | REPRODUCED | y | y | y | y | 12 rows, 0 needs fetch |
| 23 | Model layer, routing, gateways | y | 7412 | REPRODUCED | y | y | y | y | 11 rows, 1 needs fetch |
| 24 | Memory | y | 7113 | REPRODUCED | y | y | y | y | 9 rows, 1 needs fetch |
| 25 | Tools, MCP, execution environments | y | 7374 | REPRODUCED | y | y | y | y | 12 rows, 0 needs fetch |
| 26 | Sensors and verification | y | 7188 | REPRODUCED | y | y | y | y | 10 rows, 1 needs fetch |
| 27 | Graders and agent evaluation | y | 7269 | REPRODUCED | y | y | y | y | 12 rows, 1 needs fetch |
| 28 | Permissions, policy, security | y | 7517 | REPRODUCED | y | y | y | y | 18 rows, 1 needs fetch |
| 29 | Observability and audit | y | 7197 | REPRODUCED | y | y | y | y | 9 rows, 0 needs fetch |
| 30 | Multi-agent systems and protocols | y | 7295 | REPRODUCED | y | y | y | y | 9 rows, 0 needs fetch |
| 31 | Human-in-the-loop | y | 6137 | REPRODUCED | y | y | y | y | 9 rows, 0 needs fetch |
| 32 | Self-improving harnesses | y | 6440 | REPRODUCED | y | y | y | y | 9 rows, 0 needs fetch |
| 33 | Failure catalogue | y | 7221 | REPRODUCED | y | y | y | y | 8 rows, 0 needs fetch |
| 34 | Selecting use cases | — | — | — | y | — | — | — | — |
| 35 | OT/IT and functional safety | — | — | — | y | — | — | — | — |
| 36 | Regulation | — | — | — | y | — | — | — | — |
| 37 | Economics and TCO | y | 5059 | REPRODUCED | y | — | — | y | 16 rows, 1 needs fetch |
| 38 | Build, buy, assemble | — | — | — | y | — | — | — | — |
| 39 | Roadmap and maturity | — | — | — | y | — | — | — | — |
| 40 | Running a proof | — | — | — | y | — | — | — | — |

Book-level files: GLOSSARY.md, SOURCES.md (with links), TOOLKIT.md, CHANGELOG.md, FAILURE-INDEX.md, PILOT-REPORT.md. Regenerate with `python scripts/update_map.py`.
