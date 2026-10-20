import numpy as np

def grade(artifact: dict, rubric: list, grader_fn) -> dict:
    """Pointwise: one verdict per criterion from an isolated-context grader. rubric: [(id, text, reference or None)]."""
    out = {}
    for cid, text, ref in rubric:
        v, reason = grader_fn(artifact, text, ref)                 # grader sees artifact + criterion + reference only
        out[cid] = {"pass": bool(v), "reason": reason[:120]}
    return out

def pairwise_both_orders(a: dict, b: dict, criterion: str, grader_pair_fn) -> str:
    """Judge (a,b) and (b,a); agree → winner; disagree → tie (position bias exposed)."""
    first = grader_pair_fn(a, b, criterion); second = grader_pair_fn(b, a, criterion)
    if first == "A" and second == "B": return "a"
    if first == "B" and second == "A": return "b"
    return "tie"

def cohen_kappa(x: np.ndarray, y: np.ndarray) -> float:
    po = np.mean(x == y); pe = sum(np.mean(x == l) * np.mean(y == l) for l in np.unique(np.concatenate([x, y])))
    return float((po - pe) / (1 - pe)) if pe < 1 else 1.0

def calibrate(grader_verdicts: dict, human_labels: dict) -> dict:
    """κ per criterion; retire below 0.6. verdicts/labels: {criterion: np.array of 0/1 over the same items}."""
    report = {}
    for cid in human_labels:
        k = cohen_kappa(grader_verdicts[cid], human_labels[cid]); report[cid] = {"kappa": round(k, 3), "status": "retire" if k < 0.6 else "ok"}
    return report

def ci_gate(baseline_pass: np.ndarray, candidate_pass: np.ndarray, iters: int = 5000, rng=None) -> dict:
    """Paired bootstrap on per-item pass (0/1, same items). Block if the interval of (candidate − baseline) lies below zero."""
    rng = rng or np.random.default_rng(0); d = candidate_pass.astype(float) - baseline_pass.astype(float); n = len(d)
    boots = np.array([d[rng.integers(0, n, n)].mean() for _ in range(iters)]); lo, hi = np.quantile(boots, [0.025, 0.975])
    return {"diff": round(float(d.mean()), 4), "lo": round(float(lo), 4), "hi": round(float(hi), 4), "verdict": "block" if hi < 0 else "merge"}
