import math

E, A, B, ALPHA, BETA = 1.69, 406.4, 410.7, 0.34, 0.28   # Hoffmann et al. 2022, Approach 3, as published

def chinchilla_loss(N: float, D: float) -> float:
    return E + A / N ** ALPHA + B / D ** BETA

def compute_optimal(C: float, grid: int = 2000):
    """Minimize the parametric loss subject to 6·N·D = C. Returns (loss, N, D, tokens_per_param)."""
    best = None
    for i in range(grid):
        N = 10 ** (6 + 8 * i / (grid - 1)); D = C / (6 * N)
        l = chinchilla_loss(N, D)
        if best is None or l < best[0]:
            best = (l, N, D, D / N)
    return best

def train_flops(N_active: float, D: float) -> float:
    return 6 * N_active * D

def moe_split(total_params: float, active_params: float, bytes_per_param: float = 2.0):
    """Memory follows total; compute follows active."""
    return {"memory_GB": total_params * bytes_per_param / 1e9,
            "flops_per_token": 2 * active_params,
            "total_over_active": total_params / active_params}
