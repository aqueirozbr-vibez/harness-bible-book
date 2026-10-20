PRICES = {"in": 1.25, "cached": 0.125, "out": 10.0, "small_in": 0.25, "small_cached": 0.025, "small_out": 2.0}  # $/M, list, Sep 2026

def blended_input_price(hit_rate: float, cacheable_share: float, p=PRICES) -> float:
    return (1 - cacheable_share) * p["in"] + cacheable_share * (hit_rate * p["cached"] + (1 - hit_rate) * p["in"])

def cache_breakeven_reuses(write_multiplier: float, p=PRICES) -> float:
    """Reuses of a prefix at which caching (write once, read cheaply) beats paying fresh every time."""
    return write_multiplier * p["in"] / (p["in"] - p["cached"])

def batch_blended_discount(batch_share: float, discount: float = 0.5) -> float:
    return batch_share * discount

def query_cost(fresh: int, cached: int, out: int, tier: str = "frontier", p=PRICES) -> float:
    if tier == "frontier":
        return (fresh * p["in"] + cached * p["cached"] + out * p["out"]) / 1e6
    return (fresh * p["small_in"] + cached * p["small_cached"] + out * p["small_out"]) / 1e6

def routed_cost(routed_share: float, fresh=2000, cached=4000, out=400) -> float:
    return routed_share * query_cost(fresh, cached, out, "small") + (1 - routed_share) * query_cost(fresh, cached, out, "frontier")

def silent_degradation(hard_share: float, router_accuracy: float, small_fail_on_hard: float) -> float:
    """Added task-failure rate from hard queries misrouted to the small model."""
    return hard_share * (1 - router_accuracy) * small_fail_on_hard

def selfhost_crossover(monthly_gpu_cost: float, api_cost_per_query: float) -> float:
    """Queries per month at which a fixed GPU bill equals the variable API bill."""
    return monthly_gpu_cost / api_cost_per_query
