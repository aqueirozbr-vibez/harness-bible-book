# Lab 28 — Permissions, policy, security

**Runs the chapter's own code** (`pdp.py` is extracted verbatim from Chapter 28's Python blocks) and reproduces four claims: zero false-deny / zero false-allow on the golden set with forbidden near-twins; in-process PDP decision latency p99 under 10 ms; fail-closed when the policy engine is unreachable; hash-chained audit log that verifies clean and detects a tampered record.

**Prerequisites:** Python 3.9+. No dependencies, no model, no network. Optional: set `OPA_URL` to a running Open Policy Agent loaded with the chapter's Rego bundle to measure sidecar latency (not required for the reproduction).

**Run:** `python run.py` — seconds. Exit 0 means all four reproductions passed.

**Not reproduced here:** the attack-success-rate delta on AgentDojo requires a model API; see `run_agentdojo.md` for the gated protocol.
