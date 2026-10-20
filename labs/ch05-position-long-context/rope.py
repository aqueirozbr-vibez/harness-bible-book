import numpy as np

def rope_angles(hd: int, base: float, positions: np.ndarray) -> np.ndarray:
    """Rotation angles, shape (len(positions), hd // 2): angle[t, i] = t * base^(-2i/hd)."""
    i = np.arange(hd // 2)
    theta = base ** (-2.0 * i / hd)
    return positions[:, None] * theta[None, :]

def apply_rope(x: np.ndarray, positions: np.ndarray, base: float = 10_000.0) -> np.ndarray:
    """Rotate each consecutive pair of dimensions of x (n, hd) by its position-dependent angle."""
    n, hd = x.shape
    ang = rope_angles(hd, base, positions)
    c, s = np.cos(ang), np.sin(ang)
    x1, x2 = x[:, 0::2], x[:, 1::2]
    out = np.empty_like(x)
    out[:, 0::2] = x1 * c - x2 * s
    out[:, 1::2] = x1 * s + x2 * c
    return out

def relative_score(q: np.ndarray, k: np.ndarray, m: int, n: int, base: float = 10_000.0) -> float:
    """Dot product of q rotated to position m with k rotated to position n; depends only on m - n."""
    qm = apply_rope(q[None, :], np.array([m], dtype=float), base)[0]
    kn = apply_rope(k[None, :], np.array([n], dtype=float), base)[0]
    return float(qm @ kn)

def wavelengths(hd: int, base: float) -> np.ndarray:
    return 2 * np.pi / (base ** (-2.0 * np.arange(hd // 2) / hd))

def ntk_base(base: float, scale: float, hd: int) -> float:
    """NTK-aware base for extending a window by a factor `scale`."""
    return base * scale ** (hd / (hd - 2))
