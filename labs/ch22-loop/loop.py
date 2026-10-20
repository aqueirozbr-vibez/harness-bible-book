from dataclasses import dataclass, field
from typing import Callable, Any

@dataclass
class Step:
    name: str; tool: str; args: dict; checks: list          # checks: list of (name, fn(result) -> (ok, message))

@dataclass
class LoopConfig:
    max_repairs_per_step: int = 3; max_steps: int = 20; max_calls: int = 60; token_budget: int = 200_000

@dataclass
class Trace:
    events: list = field(default_factory=list); calls: int = 0; tokens: int = 0
    def log(self, **kw): self.events.append(kw)

class Escalate(Exception): pass

def run_loop(task: dict, plan: Callable, act: Callable, repair: Callable, gate: Callable,
             tools: dict, cfg: LoopConfig, trace: Trace) -> dict:
    """plan(task, state) -> [Step]; act(step) -> (args, tokens); repair(step, msg) -> (args, tokens);
    gate(step, result) -> bool; tools[name](**args) -> result."""
    state = {"done": [], "results": {}, "writes": 0}
    steps = plan(task, state); trace.calls += 1
    i = 0
    while i < len(steps):
        if i >= cfg.max_steps or trace.calls >= cfg.max_calls or trace.tokens >= cfg.token_budget:
            raise Escalate(f"budget exhausted at step {i}: calls={trace.calls} tokens={trace.tokens}")
        step = steps[i]; repairs = 0
        args, tok = act(step); trace.calls += 1; trace.tokens += tok                     # ACT
        while True:
            result = tools[step.tool](**args)                                               # OBSERVE
            failed = []                                                                      # VERIFY
            for check_name, check in step.checks:
                ok, message = check(result)
                if not ok:
                    failed.append((check_name, message))
            trace.log(step=step.name, attempt=repairs + 1, failed=[n for n, _ in failed])
            if not failed:
                break
            if repairs >= cfg.max_repairs_per_step:
                raise Escalate(f"step {step.name} failed after {repairs} repairs: {failed[0][1]}")
            args, tok = repair(step, failed[0][1]); repairs += 1                           # REPAIR
            trace.calls += 1; trace.tokens += tok
        if step.tool.startswith("submit") and not gate(step, result):                       # GATE
            raise Escalate(f"step {step.name} rejected at the human gate")
        state["done"].append(step.name); state["results"][step.name] = result             # SUBMIT
        if result.get("replan"):      # set only by a tool or a sensor, never by the model  # RE-PLAN
            steps = steps[: i + 1] + plan(task, state); trace.calls += 1
        i += 1
    return state
