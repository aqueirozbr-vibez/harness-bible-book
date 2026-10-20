import random
from dataclasses import dataclass, field

RISK_RATE = {"high": 1.0, "medium": 0.30, "low": 0.05}
TIMER_H = {"high": 24, "medium": 48, "low": 168}
REPAIRABLE = {"schema", "citation", "permit_rule", "description"}      # codes that re-enter Repair; others escalate

@dataclass
class Task:
    task_id: str; risk: str; confidence: float; has_defect: bool
    state: str = "submitted"; reviewer: str = None; wait_h: float = 0.0; review_s: float = 0.0
    outcome: str = None; code: str = None; seeded: bool = False

def route_batch(tasks: list, rng, low_conf: float = 0.7) -> set:
    """Fixed review budget per risk class = rate × class size; low-confidence items fill the budget first, then a random
    sample of the rest. Weighting redistributes attention within the rate; it never inflates the rate."""
    chosen = set()
    for risk, rate in RISK_RATE.items():
        group = [t for t in tasks if t.risk == risk]; budget = round(rate * len(group))
        lows = [t for t in group if t.confidence < low_conf]; rng.shuffle(lows); rest = [t for t in group if t.confidence >= low_conf]; rng.shuffle(rest)
        for t in (lows + rest)[:budget]: chosen.add(t.task_id)
    return chosen

class Reviewer:
    """Accuracy decays with reviews per hour (illustrative model); records time per review."""
    def __init__(self, name: str, base_acc: float = 0.95, decay_per_extra: float = 0.02, cap_per_hour: int = 12):
        self.name, self.base, self.decay, self.cap = name, base_acc, decay_per_extra, cap_per_hour
        self.log = []
    def accuracy(self, rate_per_hour: float) -> float: return max(0.3, self.base - self.decay * max(0, rate_per_hour - 10))
    def review(self, task: Task, rate_per_hour: float, rng) -> tuple:
        acc = self.accuracy(rate_per_hour); correct = rng.random() < acc
        verdict = ("reject" if task.has_defect else "approve") if correct else ("approve" if task.has_defect else "reject")
        secs = 360 if rate_per_hour <= 10 else max(15, 360 * 10 / rate_per_hour)
        self.log.append((task.task_id, verdict, secs, task.seeded, task.has_defect)); return verdict, secs

def gate(tasks: list, reviewers: list, rng, seeded_share: float = 0.02, rate_limit: int = 12) -> dict:
    """Run a set of tasks through routing, the queue, review, and outcomes; returns the gate's metrics."""
    chosen = route_batch(tasks, rng); queue = [t for t in tasks if t.task_id in chosen]
    for t in queue:
        if rng.random() < seeded_share: t.seeded, t.has_defect = True, True
    queue.sort(key=lambda t: (0 if t.risk == "high" else 1))                                  # high risk first
    per_hour = max(1, len(queue) / 160)                                                         # month → 160 working hours (illustrative)
    for i, t in enumerate(queue):
        r = reviewers[i % len(reviewers)]; load = min(rate_limit, per_hour * 2 if i < len(queue) * 0.2 else per_hour)   # a morning peak
        t.state = "pending"; t.wait_h = min(TIMER_H[t.risk], (i % 8) * 0.05)                    # illustrative queue position → wait
        verdict, secs = r.review(t, load, rng); t.reviewer, t.review_s = r.name, secs
        if verdict == "approve": t.state, t.outcome = "approved", "approve"
        else:
            t.code = rng.choice(sorted(REPAIRABLE)) if rng.random() < 0.8 else "wrong_asset"
            t.state, t.outcome = ("repair" if t.code in REPAIRABLE else "escalated"), "reject"
    for t in tasks:
        if t.state == "submitted": t.state, t.outcome = "straight_through", "stp"
    reviewed = [t for t in tasks if t.outcome in ("approve", "reject")]
    seeded = [t for t in reviewed if t.seeded]; caught = [t for t in seeded if t.outcome == "reject"]
    fast = [t for t in reviewed if t.review_s < 20]
    return {"tasks": len(tasks), "reviewed": len(reviewed), "stp_rate": round(1 - len(reviewed) / len(tasks), 3),
            "rejection_rate": round(sum(t.outcome == "reject" for t in reviewed) / max(1, len(reviewed)), 3),
            "seeded": len(seeded), "seeded_catch_rate": round(len(caught) / max(1, len(seeded)), 3),
            "rubber_stamp_flags": len(fast), "mean_wait_h": round(sum(t.wait_h for t in reviewed) / max(1, len(reviewed)), 3),
            "to_repair": sum(t.state == "repair" for t in tasks), "escalated": sum(t.state == "escalated" for t in tasks)}
