import numpy as np
from collections import Counter

CONSEQUENCE = {"permit_rule": 5, "zone": 5, "citation_currency": 3, "description": 2, "parts_bom": 2, "abbreviation": 1, "schema": 1}
SAFETY_REVIEW = {"policy_bundle", "safety_gate", "write_tool_set", "gated_routing", "output_policy", "scope_template"}

def mine(events: list, fixability: dict) -> list:
    """events: dicts with keys criterion, step, cls, lang. Cluster by the four keys; score = freq × consequence × fixability."""
    counts = Counter((e["criterion"], e["step"], e["cls"], e["lang"]) for e in events)
    ranked = []
    for (crit, step, cls, lang), n in counts.items():
        score = n * CONSEQUENCE.get(crit, 1) * fixability.get(crit, 0.5)
        ranked.append({"cluster": (crit, step, cls, lang), "freq": n, "consequence": CONSEQUENCE.get(crit, 1), "fixability": fixability.get(crit, 0.5), "score": round(score, 1)})
    return sorted(ranked, key=lambda r: -r["score"])

def run_branch(baseline_pass: np.ndarray, branch_pass: np.ndarray, holdout_idx: np.ndarray, iters: int = 4000, rng=None) -> dict:
    """Paired bootstrap of (branch − baseline) on development items and on the holdout, separately."""
    rng = rng or np.random.default_rng(0); n = len(baseline_pass); dev = np.setdiff1d(np.arange(n), holdout_idx)
    def ci(idx):
        d = branch_pass[idx].astype(float) - baseline_pass[idx].astype(float); m = len(d)
        boots = np.array([d[rng.integers(0, m, m)].mean() for _ in range(iters)])
        return {"diff": round(float(d.mean()), 4), "lo": round(float(np.quantile(boots, .025)), 4), "hi": round(float(np.quantile(boots, .975)), 4)}
    return {"dev": ci(dev), "holdout": ci(holdout_idx)}

def merge_decision(result: dict, component_class: str, unaffected_regressed: bool) -> dict:
    """Merge if the development interval is above zero, the holdout interval is not below zero, and nothing else regressed; safety classes wait for a person."""
    if unaffected_regressed: return {"verdict": "reject", "reason": "regression on an unaffected class"}
    if result["dev"]["lo"] <= 0: return {"verdict": "reject", "reason": "development gain not distinguishable from zero"}
    if result["holdout"]["hi"] < 0 or (result["holdout"]["diff"] <= 0 and result["dev"]["diff"] > 0.03): return {"verdict": "reject", "reason": "holdout does not confirm the gain (overfit)"}
    if component_class in SAFETY_REVIEW: return {"verdict": "safety_review", "reason": "safety-review class: named reviewer required"}
    return {"verdict": "merge", "reason": "interval beats baseline; holdout confirms"}

def bump(version: str, change_kind: str) -> str:
    major, minor, patch = (int(x) for x in version.split("."))
    return {"patch": f"{major}.{minor}.{patch+1}", "minor": f"{major}.{minor+1}.0", "major": f"{major+1}.0.0"}[change_kind]
