# REDTEAM — chapters 16, 21, 22, 28, 37 (20 Sep 2026)

Caveat: both reviewers played by the drafting instance; external reviewers required before the gate. Scores: PASS / WEAK / FAIL per layer.

---
## Chapter 16 — Thesis and evidence

**Reviewer A (ML/platform engineer, has read LangChain, Böckeler, τ-bench, the 2026 preprint).**
1 Intuition PASS — the 46 → 55 opener is the right hook. 2 Mechanism PASS — vocabulary attributed; the twelve-component figure with assumptions is the chapter's best asset. 3 Worked numbers PASS — the independence-vs-measured gap is a real derived insight. 4 Measurement WEAK — the two-scaffold protocol is right but "simplest harness" is defined in a parenthesis; a reviewer would want the exact configuration written as a spec so two teams run the same control. 5 Failure PASS. 6 Frontier PASS — fair; Darú and Huyen credited. 7 Industrial PASS — the scenario definition belongs here and is here. 8 Decision aids PASS. 9 Sources PASS, with three items open.
Must change: (A1) write the "simplest harness" control as a one-paragraph spec — system prompt text length, tool exposure, no retrieval, no sensors, no gates, k, temperature. (A2) the Grok 4 row reports a spread without endpoints; either give the endpoints from the preprint or mark the row "spread only." (A3) "model choice moves scores by 30 or more" is an analyst hand-wave; either cite a leaderboard range with a date or cut it.

**Reviewer B (operations VP).** Jargon: "scaffold" is used before it is equated with "harness" — one sentence early on fixes it. Decision-changing: yes — the two-scaffold test on fifty work orders is something I would fund this quarter. Embarrassment: none. Decision helped: fund the harness, rent the model, run the fifty-task test first.

Deeper than the strongest free source? Yes — no free source combines the evidence, the vocabulary, and the measurement protocol. As deep as all combined? Close on this subject; the free sources' extra depth is in coding-agent specifics this chapter deliberately omits. Single change: A1.

---
## Chapter 21 — Control plane and durable execution

**Reviewer A.** 1 PASS. 2 PASS — the workflow/activity mapping and the seven mechanism subsections are the most complete treatment of durable execution for agents I have read; the executor is small enough to audit. 3 Worked numbers PASS — the compounding table settles the "do we need retries" argument. 4 Measurement WEAK — resume correctness is measured on the toy executor; Lab 21b on Temporal is specified but not run, and the chapter should say the toy has no concurrency, no worker pool, and no real timers. 5 Failure PASS — fifteen rows, each with a signal. 6 Frontier PASS. 7 Industrial PASS. 8 Decision aids PASS — the timeout table is directly usable. 9 PASS.
Must change: (A1) state the toy executor's limits explicitly in 21.2 (single process, no concurrency, timers simulated by re-invocation). (A2) `wait_signal` raises `Crash` to suspend — name it `Suspend` in the code; reusing the crash exception for a normal wait will confuse a reader. (A3) the held-worker cost figure ($0.36) is so small it undercuts the argument; lead with the deploy-kills-every-wait point and the thousand-task aggregate, keep the figure as a footnote.

**Reviewer B.** Jargon: "deterministic replay," "saga," "continue-as-new" — each is defined at first use, acceptable. Decision-changing: the vendor test list in 21.7 ("keeps context in memory during the task" fails) is exactly what my team needs. Decision helped: require a durable engine in the RFP; reject in-memory agents.

Deeper than strongest free source? Yes for the agent mapping; Temporal's docs are deeper on the engine itself, and the chapter says so. As deep as all combined? Not yet — without a real-engine lab the resume claim rests on a toy. Single change: run Lab 21b.

---
## Chapter 22 — The agent loop and workflow patterns

**Reviewer A.** 1 PASS. 2 PASS — six states, two omitted transitions, retry/repair separation, code in which the model owns nothing structural. 3 PASS — repair-cap table is the number practitioners lack. 4 PASS. 5 PASS — twelve rows. 6 Frontier PASS after VERIFY added the negative results. 7 PASS. 8 PASS. 9 PASS.
Must change: (A1) the reference loop's `failed` comprehension is clever but unreadable; rewrite as a plain loop — a reader implementing it should not need to parse a nested comprehension. (A2) the loop re-plans only on `result.get("replan")`; state that the sensor or the observation sets that flag, and who is allowed to. (A3) the context-growth table assumes 1,500 tokens per prior iteration — say where the number comes from (average tool output size in the scenario) or measure it in the lab.

**Reviewer B.** Jargon: none unexplained. Decision-changing: the pattern-selection tree — "start one level simpler than you think" — will save my team a quarter. Decision helped: build the work-order flow as a prompt chain with routing first; add the loop only if the fifty-task test shows plan variance.

Deeper than the strongest free source? Yes — Anthropic gives the patterns, this gives the loop with caps and arithmetic. As deep as all combined? Yes on the loop's mechanics; no on the empirical effect sizes, which are simulated. Single change: A1.

---
## Chapter 28 — Permissions, policy, security

**Reviewer A.** 1 PASS. 2 PASS — three gates, request schema, dual identity, Rego and Cedar, runnable PEP with fail-closed and hash chain, MCP scoping, audit chain, policy tests, three defence layers with the adaptive-attack evidence. 3 Worked numbers WEAK — the latency budget is a design target; the lab measures a Python evaluator at microseconds, which says nothing about OPA as a sidecar. 4 Measurement PASS. 5 Failure PASS — ten rows. 6 PASS. 7 PASS — "absence is the control" is the chapter's contribution and is stated plainly. 8 PASS — five instruments. 9 PASS.
Must change: (A1) measure OPA as a sidecar (Docker) and embedded, and put the p50/p99 in 28.3; until then say the 10 ms / 30 ms targets are unmeasured. (A2) the Rego bundle's `default decision` with multiple `decision :=` rules will produce a conflict error in OPA if two rules match (e.g., `write_budget` and `restricted_zone_write` both true); restructure with priorities or `else`, and test the bundle with `opa test`. (A3) the Cedar snippet uses `context.approval.expires > context.time`; state that both must be typed as long or datetime in the schema.

**Reviewer B.** Jargon: PDP/PEP defined; "temporal policy" defined. Decision-changing: "no tool exists" for OT, the vendor's three-question test, the regulatory map — all usable. Decision helped: require an external policy engine and a decision log in the RFP; reject prompt-only permission claims.

Deeper than the strongest free source? Yes — CaMeL is deeper on one mechanism; OWASP on taxonomy; nothing free wires the PDP with reasons for the model and an OT boundary. As deep as all combined? Not yet — the Rego bundle is untested against real OPA and the sidecar latency is unmeasured. Single change: A2, then A1.

---
## Chapter 37 — Economics and TCO

**Reviewer A.** 1 PASS. 2 PASS — four lines, seven-line anatomy, four configurations, FinOps sequence, oversight formula, batch/semantic/SLM levers, contract and currency. 3 PASS — derive.py reproduces everything. 4 PASS. 5 PASS. 6 PASS. 7 PASS — the budget-review paragraph is what a finance partner needs. 8 PASS. 9 PASS.
Must change: (A1) Configuration D's ops factor (1.3×) is the low case; show the table at 1.3 and 2.0 so the reader sees the range in the table, not in prose. (A2) the routing 90/10 split is a scenario parameter that drives the headline 71%; put a second row at 70/30 so the sensitivity to the split is visible. (A3) list prices are the most perishable numbers in the book; add a one-line "price sheet" block at the top of 37.3 with the verification date so a reader can re-run derive.py with new prices in one edit.

**Reviewer B.** Jargon: STP, showback, chargeback — defined. Decision-changing: the cost-per-resolved-task worked example and the vendor-claim checklist. Decision helped: budget the harness engineering and the reviewers, not the tokens; do not self-host at our volume.

Deeper than the strongest free source? Yes — no free source prices one workload four ways from a committed script with oversight in the anatomy. As deep as all combined? Yes on method; the open item (an audited industrial figure) is a gap in the field, not the chapter. Single change: A2.

---
## Consolidated change list

CRITICAL: ch28 A2 — the Rego bundle may raise a conflict in real OPA; fix and test.
MAJOR: ch16 A1 (control spec); ch21 A1 (toy limits stated), A2 (`Suspend`); ch22 A1 (readable loop), A2 (who sets replan); ch28 A1 (measure OPA — needs Docker); ch37 A1, A2, A3.
MINOR: ch16 A2, A3, B1; ch21 A3; ch22 A3; ch28 A3.
Needs environment: ch21 Lab 21b (Temporal); ch28 A1 (OPA sidecar).
