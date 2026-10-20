import math
import numpy as np

def wilson(passes: int, n: int, z: float = 1.96):
    p = passes / n; d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d; h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h

def paired_bootstrap(a: np.ndarray, b: np.ndarray, iters: int = 10000, rng=None):
    """95% interval for mean(b) - mean(a) over paired items; returns (low, high, point)."""
    rng = rng or np.random.default_rng(0); diff = b.astype(float) - a.astype(float); n = len(diff)
    boots = np.array([diff[rng.integers(0, n, n)].mean() for _ in range(iters)])
    return float(np.quantile(boots, 0.025)), float(np.quantile(boots, 0.975)), float(diff.mean())

def cohen_kappa(r1: np.ndarray, r2: np.ndarray) -> float:
    labels = np.unique(np.concatenate([r1, r2])); po = np.mean(r1 == r2)
    pe = sum(np.mean(r1 == l) * np.mean(r2 == l) for l in labels)
    return (po - pe) / (1 - pe) if pe < 1 else 1.0

def krippendorff_alpha_nominal(ratings: np.ndarray) -> float:
    """ratings: (raters, items) with NaN for missing; nominal metric."""
    items = [ratings[:, j][~np.isnan(ratings[:, j])] for j in range(ratings.shape[1])]
    items = [v for v in items if len(v) >= 2]
    n = sum(len(v) for v in items)
    Do = 0.0
    for v in items:
        m = len(v); Do += sum((v[i] != v[k]) for i in range(m) for k in range(m) if i != k) / (m - 1)
    Do /= n
    allv = np.concatenate(items); labels, counts = np.unique(allv, return_counts=True)
    De = sum(counts[i] * counts[k] for i in range(len(labels)) for k in range(len(labels)) if i != k) / (n * (n - 1))
    return 1 - Do / De if De > 0 else 1.0

def power_to_detect(n: int, p1: float, p2: float, corr: float = 0.5, trials: int = 300, rng=None) -> float:
    """Share of simulated paired comparisons whose bootstrap interval excludes zero."""
    rng = rng or np.random.default_rng(0); hits = 0
    t1, t2 = np.quantile(rng.standard_normal(200000), p1), np.quantile(rng.standard_normal(200000), p2)
    for _ in range(trials):
        z = rng.standard_normal(n); a = corr * z + math.sqrt(1 - corr ** 2) * rng.standard_normal(n)
        b = corr * z + math.sqrt(1 - corr ** 2) * rng.standard_normal(n)
        lo, _, _ = paired_bootstrap((a < t1).astype(int), (b < t2).astype(int), iters=200, rng=rng)
        hits += lo > 0
    return hits / trials
