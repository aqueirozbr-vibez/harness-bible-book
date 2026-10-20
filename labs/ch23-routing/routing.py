import numpy as np

PRICES = {"F": {"in": 1.25, "cached": 0.125, "out": 10.0}, "S": {"in": 0.25, "cached": 0.025, "out": 2.0}}   # $/M, Sep 2026 list

def call_cost(tier: str, fresh=2000, cached=4000, out=400, reasoning=0) -> float:
    p = PRICES[tier]; return (fresh * p["in"] + cached * p["cached"] + (out + reasoning) * p["out"]) / 1e6

ROUTING_TABLE = {   # step class → (tier, reasoning tokens, verifier name or None, fallback tier)
    "retrieve": ("S", 0, "citation", "F"), "plan": ("F", 2000, "plan_conformance", None), "draft": ("S", 0, "schema", "F"),
    "validate": ("S", 0, "schema", "F"), "permit": ("F", 2000, "permit_rule", None), "submit": ("S", 0, "policy", "F"), "report": ("S", 0, "schema", "F"),
}

class Gateway:
    """Hard budget caps per task; fallback chain; every call tagged and counted."""
    def __init__(self, task_budget_usd: float, availability: dict):
        self.budget, self.spent, self.avail, self.calls = task_budget_usd, 0.0, availability, []
    def call(self, tier: str, step_class: str, model_fn, reasoning=0):
        cost = call_cost(tier, reasoning=reasoning)
        if self.spent + cost > self.budget:
            raise RuntimeError(f"budget cap {self.budget:.3f} reached at {self.spent:.3f}")
        chain = [tier] + [t for t in ("S", "F", "ONSITE") if t != tier]
        for t in chain:
            if self.avail.get(t, True):
                out = model_fn(t); self.spent += cost if t in PRICES else 0.0
                self.calls.append({"class": step_class, "tier": t, "fell_back": t != tier, "cost": cost if t in PRICES else 0.0, "reasoning": reasoning})
                return out
        raise RuntimeError("no tier available")

def route_classifier(step_class: str, hard: bool, classifier_accuracy: float, rng) -> str:
    """Within a class whose difficulty varies: send hard items to F if the classifier recognises them."""
    tier, _, _, _ = ROUTING_TABLE[step_class]
    if tier == "F": return "F"
    predicted_hard = hard if rng.random() < classifier_accuracy else (not hard)
    return "F" if predicted_hard else "S"

def route_cascade(step_class: str, try_small, verify) -> tuple:
    """Try S; verify with the class's sensor; escalate to F on failure. Returns (tier_used, cost)."""
    tier, reasoning, verifier, fallback = ROUTING_TABLE[step_class]
    if tier == "F": return "F", call_cost("F", reasoning=reasoning)
    out = try_small(); cost = call_cost("S")
    if verify(out): return "S", cost
    return "F", cost + call_cost("F")

def savings_and_retention(cost_base: np.ndarray, cost_routed: np.ndarray, pass_base: np.ndarray, pass_routed: np.ndarray, iters=5000, rng=None):
    """Paired bootstrap over golden items: saving % and pass-rate difference, each with a 95% interval."""
    rng = rng or np.random.default_rng(0); n = len(cost_base); sv, dq = [], []
    for _ in range(iters):
        i = rng.integers(0, n, n)
        sv.append(1 - cost_routed[i].sum() / cost_base[i].sum()); dq.append(pass_routed[i].mean() - pass_base[i].mean())
    return {"saving_pct": (round(100 * np.mean(sv), 1), round(100 * np.quantile(sv, .025), 1), round(100 * np.quantile(sv, .975), 1)),
            "retention_diff": (round(float(np.mean(dq)), 3), round(float(np.quantile(dq, .025)), 3), round(float(np.quantile(dq, .975)), 3))}
