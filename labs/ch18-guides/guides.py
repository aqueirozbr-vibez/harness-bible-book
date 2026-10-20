import hashlib, re
from dataclasses import dataclass, field

@dataclass
class Rule:
    id: str; text: str; sensor: str = None; golden_case: str = None

@dataclass
class Guide:
    version: str
    identity: str
    task_class: str
    instructions: str
    rules: list
    tools: list                 # [(name, description)]
    examples: list              # [(request, output)]
    output_contract: str

FORBIDDEN = [re.compile(r"\b20\d\d-\d\d-\d\d\b"), re.compile(r"\bt-\d{4,}\b"), re.compile(r"\b\d{1,2}:\d\d\b")]   # dates, task ids, times

def tokens(s: str) -> int:
    return max(1, round(len(s) / 4))                      # 4 chars/token stand-in; production uses the model's tokenizer (ch01)

def assemble_prefix(g: Guide) -> dict:
    """Build the stable prefix in fixed order; refuse volatile content; hash the bytes."""
    parts = [("identity", g.identity), ("instructions", f"[{g.task_class}]\n{g.instructions}"),
             ("rules", "\n".join(f"- ({r.id}) {r.text}" + ("" if r.sensor else " [unenforced]") for r in g.rules)),
             ("tools", "\n".join(f"{n}: {d}" for n, d in g.tools)),
             ("examples", "\n\n".join(f"Request: {q}\nOutput: {a}" for q, a in g.examples)),
             ("contract", g.output_contract)]
    text = "\n\n".join(p for _, p in parts)
    for pat in FORBIDDEN:
        if pat.search(text):
            raise ValueError(f"volatile content in prefix: {pat.pattern}")
    budget = {name: tokens(p) for name, p in parts}
    return {"version": g.version, "prefix": text, "hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            "tokens": sum(budget.values()), "budget": budget}

def check_cache_minimum(prefix: dict, minimum: int = 1024) -> bool:
    return prefix["tokens"] >= minimum

def pairing_audit(g: Guide) -> dict:
    enforced = [r.id for r in g.rules if r.sensor]; unenforced = [r.id for r in g.rules if not r.sensor]
    untested = [r.id for r in g.rules if r.sensor and not r.golden_case]
    return {"rules": len(g.rules), "enforced": len(enforced), "enforced_pct": round(100 * len(enforced) / max(1, len(g.rules))),
            "unenforced": unenforced, "sensor_without_golden_case": untested}

def compose_window(prefix: dict, chunks: list, facts: list, task: str, step: str, request: str) -> str:
    """Dynamic content after the prefix; instruction and the repeated request last."""
    dyn = "\n\n".join(["## Retrieved\n" + "\n".join(chunks), "## Facts\n" + "\n".join(facts),
                       "## Task\n" + task, "## Step\n" + step, f"## Instruction\nComplete the step above for the request: {request}"])
    return prefix["prefix"] + "\n\n" + dyn
