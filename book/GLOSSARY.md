# Glossary

Each term with the chapter that defines it. A term defined differently in two chapters is flagged.

| Term | Definition | Defined in |
|---|---|---|
| Harness | The set of components around a model that turn its outputs into outcomes a plant can rely on: intake, guides, context, retrieval, control plane, loop, model layer, memory, tools, sensors, graders, permissions, human gate, observability, improvement loop | 00, 16 |
| Agent | Model + harness; a model using tools in a loop under the harness's control | 16 |
| Guide | Anything the model reads that shapes its behaviour: identity, class instructions, examples, rules, skills — versioned, byte-stable, compliance-tested | 18 |
| Sensor | A check on an artifact or step; computational (deterministic) or inferential (a grader or a person); emits a message written for the model | 26 |
| The 2×2 | Guides and sensors against computational and inferential — every control sits in one cell; promotion moves it toward the computational cells | 16, 32 |
| pass^k | Probability that all k independent attempts at a task succeed; the reliability metric (τ-bench) | 16 |
| Task record | The structured intent from intake: requester, scope, criteria, constraints, deadline, data class, allowed action | 17 |
| Intent validation | Checking a proposed action against the task record's scope and flags, before the policy engine | 17, 28 |
| Plan conformance | Checking a plan's steps against the class's allowed actions and the task's scope before the first step | 17, 22 |
| Prefix | The byte-stable part of every window (identity, class guide, tool schemas) that prompt caching amortizes | 18, 19 |
| Context rot / poisoning / distraction / clash | Failure of the window's content to be used correctly as it grows or fills with untrusted or stale material | 19 |
| Compaction | Replacing history with a structured summary at a rule-defined boundary; references not content | 19 |
| Summary contract | The bounded, schema-checked object a sub-agent returns: answer, support, signals, not found, cost | 19, 30 |
| Contextual retrieval | Prefixing each chunk with its document context before embedding and indexing | 20 |
| Currency filter | Excluding superseded chunks from default retrieval; the stale-revision defence | 20 |
| Cite-or-abstain | A claim the model cannot cite to a current chunk is replaced by an escalation | 20, 18 |
| Context graph | Explicit relations (asset → procedure → part) from systems of record, queried as tools | 20 |
| Durable execution | Workflow state persisted as a replayable event history; the control plane's model | 21 |
| Idempotency key | A control-plane-generated key on every write so a retry cannot duplicate it | 21 |
| Saga / compensation | A declared undo per write step, run in reverse on failure | 21 |
| The loop | Plan → Act → Observe → Verify → Repair → Submit, with re-plan and escalate transitions | 22 |
| Repair vs retry | Retry re-runs an unchanged call after a transient error; repair re-runs a changed call after a sensor message | 22 |
| Stop condition | A deterministic reason a loop ends: steps done, repair cap, budget, re-plan cap, policy escalation | 22 |
| Routing table | Per step class: tier, pinned version, effort, verifier, fallback chain, tools, guide, precision | 23 |
| Cascade | Try the small tier, verify with a deterministic sensor, escalate on failure | 23 |
| Effort | The reasoning-token budget per step class; set before the tier | 09, 23 |
| Gateway | The single proxy every model call passes through: keys, hard budget caps, tags, retries, fallbacks, caching, logging | 23 |
| Working / episodic / semantic / procedural memory | CoALA's four classes; only records accumulate, facts are curated, procedure is engineered | 24 |
| Consolidation (dreaming) | The scheduled, reviewed pass that proposes durable facts from episodes | 24 |
| Provenance | Episode ids or reviewer identity attached to every durable fact; refused at filing if absent | 24 |
| Risk class (tool) | read / validate / write (draft) / write (system of record) / external communication / destructive — a field the policy engine reads | 25 |
| Code-execution pattern | The model writes code that runs in the sandbox to consume tool results; only the answer reaches the window | 25 |
| Sandbox | Ephemeral per-task execution environment: egress default-deny, resource caps, vault-issued credentials | 25, 28 |
| Executable specification | A Given/When/Then criterion that compiles to a sensor and lives in the golden set | 26 |
| Verification gates | Acceptance, regression (CI), safety — the three gates before delivery | 26 |
| Grader | A model call with an isolated context (artifact + rubric + reference) returning one verdict per criterion; calibrated by κ | 27 |
| Isolated-context grading | The grader never sees the transcript; outcomes are judged separately from process | 27 |
| Regression gate | The golden set run in CI on every change, compared by paired-bootstrap interval | 27 |
| Policy decision point (PDP) | The deterministic engine (OPA/Cedar) that rules on every tool call outside the model | 28 |
| Dual identity | Principal (who the task acts for) and actor (which agent version) on every request | 28 |
| Fail-closed | Deny on error, timeout, missing bundle, or unverifiable signature — at every layer | 28 |
| Lethal trifecta / Rule of Two | Private data + untrusted content + exfiltration; no more than two of untrusted input, sensitive access, state change without a human | 28 |
| The seven records | Spans, tool-call logs, loop transitions, decision records, interventions, diffs, cost records | 29 |
| Hash chain / anchor | SHA-256 linking of evidentiary records; the day's head written to a write-once store | 29 |
| Reconstruction / re-evaluation | Replay of what happened (no model) vs what would be allowed today (new bundle) | 29 |
| Delegation (intersection) | A child task's scope is parent ∩ delegation; action, comms, data class clamped; budget carved out | 30 |
| A2A vs MCP | Agent-to-agent tasks at the boundary vs tools and data; internal delegation uses the control plane | 30 |
| Token multiplier | ~4× chat for an agent, ~15× for multi-agent (Anthropic); 3.75× multi over single | 30, 37 |
| Straight-through processing (STP) | Tasks delivered with no human touch; the gate's headline | 31, 37 |
| Seeded items | Known-bad artifacts mixed into the review queue; the human sensor's calibration | 31 |
| Break-glass | A recorded human bypass of the gate; reconciled against diffs | 31 |
| Failure-cluster mining | Weekly clustering of failure events by criterion, step, class, language; ranked by frequency × consequence × fixability | 32 |
| Promotion ladder | Observation → guide rule → sensor → template field / tool / component | 32 |
| Holdout | The fifth of the golden set no proposer sees; the Goodhart check | 32 |
| Composite version | The harness's version naming every component version; patch / minor / major by rule | 32 |
| Consequence class | 1–5 scale of what the plant loses if a failure reaches a record or a person | 33 |
| Golden set | The stratified, labelled, frozen-context item set per class that decides every change | 12 |
| Wilson interval / paired bootstrap | The interval on a pass rate; the interval on a difference between configurations on the same items | 12 |
| Cohen's κ / Krippendorff's α | Chance-corrected agreement; the labeler ceiling and the grader's calibration | 12, 27 |
| Abstention threshold | The confidence below which the correct output is "I cannot answer", set from the cost of failure | 13 |
| Register (validation) | The plant's asset register as the source of truth for every tag; confusion-class check before edit distance | 14 |
| KV cache | Per-token key/value memory that bounds concurrency; the decode bandwidth wall | 04, 10 |
| Fill vs retrieve | Loading a document into the window vs retrieving the relevant chunks per step; 477× in the scenario | 05 |
| Cache break-even | The reuse count at which a cache write pays for itself (1.39× / 2.22× for 5-min / 1-h TTL) | 15 |
| OT boundary | The agent never touches DCS, PLC, or SIS; reads process values through a read-only broker; no write tool exists | 35 (rule stated in every part) |

Flagged: none defined differently across chapters after the tier-label normalisation of 21 Sep 2026. Terms defined in Part III (use-case verifiability index, TCO, maturity levels) will be added when those chapters are drafted.
