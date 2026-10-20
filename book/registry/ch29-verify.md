# VERIFY log — Chapter 29 — Observability and audit (21 Sep 2026, batch pass)

Method: derive.py recomputed; lab re-run (REPRODUCED); every Python block compiled; cross-chapter grep of shared figures (scenario parameters, prices, τ-bench, AgentDojo, RouteLLM, contextual retrieval, multipliers, κ) — consistent; web checks on the highest-risk cited items listed below. Items marked (knowledge) were checked against training knowledge, not re-fetched, and are handed to the independent pass with the UNVERIFIED items.

| Item | Verdict | Correction / note |
|---|---|---|
| Derived figures, lab, code blocks, shared figures | CONFIRMED (recomputed: derive.py re-run, lab REPRODUCED, all code blocks compile, cross-chapter figures consistent) |  |
| OTel GenAI 'stable core since v1.37.0' | OUTDATED/MISATTRIBUTED — all gen_ai.* attributes remain Development as of Aug 2026; v1.42.0 moved namespace to a separate repo | CORRECTED in 29.2 (fetched: particula.tech, dev.to azena.ai, greptime, 13 Aug 2026) |
| gen_ai.content.prompt/completion events | OUTDATED — removed in v1.37.0; replaced by gen_ai.system_instructions / input.messages / output.messages | CORRECTED in the attribute table |
| gen_ai.provider.name replaces gen_ai.system | CONFIRMED (fetched) |  |
| Haber & Stornetta 1991; Merkle 1987 | CONFIRMED (knowledge) |  |

Corrections applied this pass: ch29 OTel status and attribute table; none else.

Independent pass: source-fetch every (knowledge) row; re-fetch vendor pages before publication (prices, deprecation cadences, gateway ownership).