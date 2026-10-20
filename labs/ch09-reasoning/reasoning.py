from math import comb

def majority_vote_accuracy(p: float, k: int) -> float:
    """P(majority of k independent samples is correct) at per-sample accuracy p (k odd)."""
    return sum(comb(k, i) * p**i * (1 - p)**(k - i) for i in range(k // 2 + 1, k + 1))

def coverage(p: float, n: int) -> float:
    """P(at least one of n samples is correct)."""
    return 1 - (1 - p) ** n

def best_of_n(p: float, n: int, verifier_tpr: float, verifier_fpr: float) -> float:
    """P(chosen answer is correct) when a verifier accepts correct samples with prob tpr and wrong ones with prob fpr;
    the first accepted sample is returned; if none is accepted, one is picked at random."""
    acc_c, acc_w = p * verifier_tpr, (1 - p) * verifier_fpr
    acc = acc_c + acc_w
    if acc == 0:
        return p
    p_none = (1 - acc) ** n
    return (1 - p_none) * (acc_c / acc) + p_none * p

EFFORT = {"low": 0, "medium": 500, "high": 2000}          # reasoning tokens per step (illustrative budgets)

def allocate_effort(steps: list) -> dict:
    """steps: list of (name, step_class). Plan and verify get high effort; routine steps low; hard steps medium."""
    plan = {}
    for name, cls in steps:
        plan[name] = "high" if cls in ("plan", "verify") else "medium" if cls == "hard" else "low"
    tokens = sum(EFFORT[e] for e in plan.values())
    return {"plan": plan, "reasoning_tokens": tokens, "all_high_tokens": len(steps) * EFFORT["high"]}
