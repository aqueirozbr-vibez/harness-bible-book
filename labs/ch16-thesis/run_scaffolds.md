# Lab 16 part 2 — two scaffolds, one model (API-gated)

Inputs: a golden set of ≥ 50 tasks in `golden/*.json`, each with an input, the tools it may use, and a deterministic `check(state) -> bool`; a pinned model version; two harness definitions — `simple/` (system prompt, direct tool calls, no retrieval, no sensors, no gates) and `full/` (the chapter-9 components as far as built).
Run: for each harness, each task, k = 4 attempts with fresh sessions; record success per attempt, tokens, wall time, harness commit hash.
Report: pass^1 and pass^4 per harness with Wilson 95% intervals; the difference with a paired bootstrap (10,000 resamples over tasks); tokens per success. Optional ablations: `full` minus retrieval, minus sensors, minus policy engine — one component removed at a time.
Cost gate: the runner prints (tasks × k × 2 × mean tokens × price) before starting and requires `--confirm`.
Expected outcome on a software golden set: a spread of the order reported in 16.2 (8–16 points); on an industrial document workload the result is unknown and is the point of the exercise.
