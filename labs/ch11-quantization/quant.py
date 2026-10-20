import numpy as np

def quantize(w: np.ndarray, bits: int, group: int = None):
    """Symmetric uniform quantization. Returns the dequantized weights and the bits per weight incl. scales."""
    levels = 2 ** (bits - 1) - 1
    if group is None:
        scale = np.abs(w).max() / levels
        q = np.clip(np.round(w / scale), -levels, levels)
        return q * scale, bits
    wg = w.reshape(-1, group)
    scale = np.abs(wg).max(axis=1, keepdims=True) / levels
    q = np.clip(np.round(wg / scale), -levels, levels)
    return (q * scale).reshape(w.shape), bits + 16 / group

def relative_rms_error(w: np.ndarray, wq: np.ndarray) -> float:
    return float(np.sqrt(np.mean((wq - w) ** 2)) / np.sqrt(np.mean(w ** 2)))

def inject_outliers(w: np.ndarray, fraction: float, factor: float, rng) -> np.ndarray:
    """Multiply a random `fraction` of weights by `factor` — the LLM.int8 outlier phenomenon, on weights."""
    out = w.copy(); idx = rng.choice(w.size, size=max(1, int(w.size * fraction)), replace=False)
    out.reshape(-1)[idx] *= factor
    return out

def output_error(w: np.ndarray, wq: np.ndarray, x: np.ndarray) -> float:
    """Relative error in a layer's output y = x @ w caused by quantizing w."""
    y, yq = x @ w, x @ wq
    return float(np.linalg.norm(yq - y) / np.linalg.norm(y))

def substitution_compute(steps_total: int, steps_routine: int, small_params: float, large_params: float) -> dict:
    """Relative model compute for a task when routine steps run on the small model."""
    all_large = steps_total * 1.0
    mixed = steps_routine * (small_params / large_params) + (steps_total - steps_routine) * 1.0
    return {"all_large": all_large, "mixed": round(mixed, 2), "saving_pct": round(100 * (1 - mixed / all_large))}
