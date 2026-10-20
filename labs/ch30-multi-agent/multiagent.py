from dataclasses import dataclass, field

@dataclass
class TaskRecord:
    task_id: str; principal: str; actor: str
    scope: set; allowed_action: str; external_comms: bool; data_class: str
    budget_calls: int; parent_id: str = None

SUMMARY_FIELDS = {"answer", "support", "signals", "not_found", "cost_calls"}

def delegate(parent: TaskRecord, delegation_scope: set, specialist_actor: str, child_calls: int, child_id: str) -> TaskRecord:
    """Open a child task: scope = parent ∩ delegation; action, comms, data class no wider than the parent; budget carved out."""
    if child_calls > parent.budget_calls: raise ValueError("child budget exceeds parent's remaining budget")
    parent.budget_calls -= child_calls
    return TaskRecord(child_id, parent.principal, specialist_actor, parent.scope & delegation_scope, "draft" if parent.allowed_action == "draft" else parent.allowed_action,
                      parent.external_comms and False, parent.data_class, child_calls, parent_id=parent.task_id)

def check_summary(summary: dict, child: TaskRecord, max_answer_tokens: int = 300) -> dict:
    """The parent's sensors on the child's return: schema, size, scope of support, no context leakage."""
    problems = []
    if set(summary) != SUMMARY_FIELDS: problems.append(f"summary fields {sorted(set(summary) ^ SUMMARY_FIELDS)} wrong")
    if len(str(summary.get("answer", ""))) / 4 > max_answer_tokens: problems.append("answer exceeds summary budget (context leaked)")
    for ref in summary.get("support", []):
        if not any(ref.startswith(s) for s in child.scope): problems.append(f"support {ref} outside child scope {sorted(child.scope)}")
    if summary.get("cost_calls", 0) > child.budget_calls: problems.append("child exceeded its call budget")
    return {"ok": not problems, "problems": problems}

def policy_allows(task: TaskRecord, action: str, target: str) -> bool:
    """Narrowest-scope rule at the engine: the child's own record bounds it; the engine sees the chain via parent_id."""
    if target.split("#")[0] not in task.scope: return False
    if action == "submit" and task.allowed_action != "submit": return False
    if action == "notify" and not task.external_comms: return False
    return True

def run_single(steps: list, tokens_per_step: int = 6000) -> dict:
    return {"tokens": len(steps) * tokens_per_step, "calls": len(steps)}

def run_multi(parent_steps: list, children: list, tokens_per_step: int = 6000, coord_overhead: int = 2) -> dict:
    """Parent steps plus each child's steps plus coordination calls (delegate + merge per child)."""
    calls = len(parent_steps) + sum(len(c) for c in children) + coord_overhead * len(children)
    return {"tokens": calls * tokens_per_step, "calls": calls}
