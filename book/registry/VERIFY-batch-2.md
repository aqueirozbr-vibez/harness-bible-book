# VERIFY log — chapters 16, 21, 22, 28, 37 (20 Sep 2026)

Caveat: run by the drafting instance; independent pass still required before the gate.

## Method
1. Every derive.py re-run; every lab re-run: all five reproduce.
2. Every Python block in every chapter parsed; all parse; ch28 and ch21 blocks execute inside their labs.
3. Cross-chapter consistency grep on shared figures (scenario parameters, prices, τ-bench, AgentDojo, scaffold spreads).
4. Flagged source claims checked against primary abstracts where reachable this session.

## Findings

| Ch | Location | Item | Verdict | Correction |
|---|---|---|---|---|
| 21 | 21.7 | "Thirteen activities, one signal, one timer" | INCONSISTENT with 21.2 code (plan + 11 = 12 activities) and ch22 (13 model calls incl. one repair) | Restated: twelve activities plus one repair call; thirteen calls |
| 21 | 21.2 code | Idempotency key omitted task id (found by Lab 21) | ARITHMETIC/LOGIC ERROR | Fixed in chapter before this log |
| 21 | 21.2 | Temporal timeout names (schedule-to-start, start-to-close, schedule-to-close, heartbeat), patching/versioning, continue-as-new | CONFIRMED (Temporal docs terminology) | — |
| 21 | 21.2 | AgentCore isolated microVM sessions | VENDOR, not re-checked this session | Keep tier vendor; flag for independent pass |
| 22 | 22.2 | ReAct +34 / +10 absolute (ALFWorld / WebShop) | CONFIRMED (paper abstract; Google Research blog) | Added the paper's own negative result: CoT beats ReAct on HotpotQA |
| 22 | 22.2 | Reflexion 80% → 91% HumanEval pass@1 | CONFIRMED (NeurIPS 2023 abstract) | Added MBPP regression, WebShop non-convergence, ALFWorld 130/134 vs 108/134 |
| 22 | 22.2 | Self-Refine "~20 points absolute average" | CONFIRMED by recall of abstract wording; exact phrase to be quoted in independent pass | — |
| 22 | 22.3 | Repair-cap table, task rates, context growth, runaway cost | CONFIRMED by lab simulation (2,000 tasks) | — |
| 16 | 16.2 | SWE-bench Verified = 500 human-validated tasks | CONFIRMED (OpenAI, Aug 2024) | — |
| 16 | 16.2 | Epoch AI single-model range 62.3–70.2% | ANALYST; exact post not located this session | Tier kept analyst; independent pass must locate or remove |
| 16 | 16.2 | Grok 4 +14–16 pp; Opus 4.5 45.9→55.4 | PREPRINT (arXiv 2605.23950), as tiered | Scaffold names (SWE-agent → xAI; SEAL → Claude Code) to be confirmed against the preprint's table |
| 16 | 16.3 | pass^k independence, 84.1%, 59%, Wilson widths, 0.95^11 | CONFIRMED by derive.py and lab | — |
| 28 | 28.2 | AgentDojo 4 / 74 / 97 / 27 / 629; attacks < 25% vs best agents | CONFIRMED (paper) | — |
| 28 | 28.2 | CaMeL 77% provable vs 84% undefended | CONFIRMED (arXiv 2503.18813 latest) | — |
| 28 | 28.2 | Rule of Two, 31 Oct 2025; Attacker Moves Second, 10 Oct 2025, >90% ASR on 12 defences | CONFIRMED | — |
| 28 | 28.2 | Prompt Guard 2 81.2% APR at 3% utility cost | CONFIRMED (LlamaFirewall paper) | — |
| 28 | Lab | Golden set 0/0, p99 0.03 ms, fail-closed, chain tamper detection | CONFIRMED by lab | — |
| 37 | 37.2–37.3 | All configuration totals, savings, break-evens | CONFIRMED by derive.py and lab | — |
| 37 | 37.2 | RouteLLM 85/45/35 at 95%; FrugalGPT 98%; FOCUS 1.4 4 Jun 2026; Belcak 10–30×; NANDA ~5%; McKinsey ~6% | AS TIERED from the September research brief; not re-fetched this session | Independent pass re-checks list prices (stale monthly) and FOCUS ratification date |
| 37 | 37.3 | Oversight formula inputs | ILLUSTRATIVE, labelled | — |
| all | cross-chapter | Scenario: 2,000/day; 6,000/4,000/400 tokens; eleven steps; P-101 in Z3; 14 h 20 m approval | CONSISTENT across ch16, 21, 22, 28, 37 | — |
| all | cross-chapter | Prices $1.25 / $0.125 / $10 and $0.25 / $0.025 / $2 | CONSISTENT (ch37 sole source; ch22 cites ch37) | — |

## Layer 6 fairness
- ch22 cited only the favorable results of ReAct and Reflexion. Corrected: the papers' own negative results are now stated. Rule added to the DRAFT prompt: when citing a benchmark gain, cite the same paper's worst result in the same sentence.
- ch16, ch21, ch28, ch37 stopping-point claims re-read against the sources' abstracts and tables of contents; no dispute found.

## Verdict
2 corrections (ch21 activity count; ch22 omitted negative results), 1 logic defect already fixed by lab (ch21 key), 0 MISATTRIBUTED, 0 UNVERIFIABLE retained. Three items handed to the independent pass: Epoch AI post; preprint scaffold names; ch37 list prices and FOCUS date.
