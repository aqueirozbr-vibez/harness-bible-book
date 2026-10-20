from dataclasses import dataclass, field

BUDGET = {"retrieved": 1000, "history": 400, "facts": 150, "task": 250, "instruction": 200}   # dynamic, tokens (illustrative)
RAW_RESULT_MAX = 300                                                                              # raw tool results above this are trimmed

def tokens(s: str) -> int:
    return max(1, round(len(s) / 4))

def trim_result(result_rows: list, select, result_id: str, summarize) -> str:
    """Filter first; if still over the threshold, summarize; always keep the reference id."""
    rows = [r for r in result_rows if select(r)]
    text = "\n".join(rows)
    if tokens(text) > RAW_RESULT_MAX:
        text = summarize(rows)
    return f"[result {result_id}]\n{text}"

def compact(history: list, budget: int) -> str:
    """Running summary as references: step, outcome, ids. Oldest entries are dropped first if over budget."""
    lines = [f"step {h['step']}: {h['outcome']} (refs {','.join(h['refs'])})" for h in history]
    while lines and tokens("\n".join(lines)) > budget:
        lines.pop(0)
    return "\n".join(lines)

def fit(text: str, budget: int, unit: str = "\n") -> str:
    parts = text.split(unit)
    while parts and tokens(unit.join(parts)) > budget:
        parts.pop()                      # drop from the end: least relevant chunks / oldest facts last in their lists
    return unit.join(parts)

def assemble(prefix: str, chunks: list, history: list, facts: list, task: str, step: str, request: str) -> dict:
    """Fixed order; budget enforced by rule; instruction last. Returns the window and its accounting."""
    retrieved = fit("\n".join(chunks), BUDGET["retrieved"])
    hist = compact(history, BUDGET["history"])
    fx = fit("\n".join(facts), BUDGET["facts"])
    tsk = fit(f"{task}\nSTEP: {step}", BUDGET["task"])
    instr = fit(f"Complete the step above for the request: {request}", BUDGET["instruction"])
    body = "\n\n".join(["## Retrieved\n" + retrieved, "## History\n" + hist, "## Facts\n" + fx, "## Task\n" + tsk, "## Instruction\n" + instr])
    window = prefix + "\n\n" + body
    p_tok = tokens(prefix); w_tok = tokens(window)
    return {"window": window, "tokens": w_tok, "prefix_tokens": p_tok, "dynamic_tokens": w_tok - p_tok,
            "chunk_start_fraction": round(p_tok / w_tok, 2), "over_budget": w_tok - p_tok > sum(BUDGET.values())}
