# Outline — Chapter 28 Permissions, policy, security (budget 10,000–12,000; running example P-101 submit_work_order)

28.1 Intuition (900) — the model proposes, the engine disposes; why a rule in a prompt is a wish; the P-101 submit call denied and self-corrected.
28.2 Mechanism (3,200) — PDP/PEP model; request schema (principal, actor, tool, args, context); allow/deny/escalate with reasons written for the model; Rego and Cedar side by side with one policy in each; dual identity; fail-closed; temporal policies (sequence, cumulative, freshness); credential flow (Vault lease → tool, never model); network policy and sandbox egress; injection defences by layer: classifier (ceiling), architecture (CaMeL, dual-LLM), heuristics (Rule of Two, trifecta); intent validation; Mermaid: PDP sequence diagram; Mermaid: defence-in-depth layers; runnable Python: tool decorator + OPA call + structured deny.
28.3 Worked numbers (1,200) — AgentDojo scale; utility-under-attack deltas; latency budget arithmetic (calls per task × PDP p99); credential exposure window; Rule-of-Two applied to the P-101 workflow (which leg is removed).
28.4 Measurement (900) — PDP latency protocol; false-deny rate on benign golden set; ASR on injection suite; policy coverage; points to Lab 28.
28.5 Failure (900) — table: policy says the wrong thing; standing credentials; egress path missed; escalation bypass under pressure; delegation inheritance undefined; classifier-only defence; deny messages the model cannot act on; decision log gaps.
28.6 Frontier (900) — OWASP, CaMeL, Meta/Willison, OPA/Cedar docs, Darú ch.07: where each stops; what this adds (wired PDP with latency, self-correcting denies, OT absence-not-denial, evidence mapping).
28.7 Industrial (1,200) — IEC 62443 zones; the agent at Purdue 4–5; broker/diode reads; "no tool exists" for DCS/PLC/SIS; LGPD automated-decision logging from the decision log; NIST control IDs satisfied by the same records.
28.8 Decision aids (800) — Rule-of-Two worksheet; tool risk-class matrix; policy-review checklist; credential TTL table; delegation intersection rule (proposal).
28.9 Sources — table.
Lab 28 reproduces: PDP p99 latency (in-process vs sidecar) and false-deny rate on the benign set; ASR delta requires the API-gated variant.
Thin material: no published agent-boundary PDP latency; no delegation standard — both handled by lab measurement and explicit "proposal" labels.
