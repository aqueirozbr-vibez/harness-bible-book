#!/usr/bin/env python3
"""Lab 31 / derive.py — every derived number in Chapter 31."""
import json, datetime, math
out = {}
# Scenario: 1,500 resolved tasks/month (ch37); gated classes: submissions. Risk routing: high-risk 100% review, medium 30% sample, low 5% sample (illustrative policy)
tasks = 1500; share = {"high": 0.20, "medium": 0.50, "low": 0.30}; rate = {"high": 1.0, "medium": 0.30, "low": 0.05}
reviews = {k: int(tasks * share[k] * rate[k]) for k in share}; out["reviews_per_month_by_risk"] = reviews; out["reviews_per_month_total"] = sum(reviews.values())
out["review_share_of_tasks_pct"] = round(100 * sum(reviews.values()) / tasks, 1)
# Reviewer time: 6 min per review (ch26) → hours/month; at 2 reviewers × 20 working days
out["review_minutes_each"] = 6; out["reviewer_hours_per_month"] = round(sum(reviews.values()) * 6 / 60, 1); out["reviewer_hours_per_day_2_reviewers"] = round(sum(reviews.values()) * 6 / 60 / 20 / 2, 2)
# STP (straight-through processing) rate = tasks delivered without human touch / tasks (ch37 formula): 1 - review share (clarifications excluded)
out["stp_rate_pct"] = round(100 * (1 - sum(reviews.values()) / tasks), 1)
# Queue wait: M/M/1 with arrival λ (reviews/hour during 8-h day) and service μ = 10/h per reviewer
lam = sum(reviews.values()) / 20 / 8; mu = 60 / 6
for c in (1, 2):
    rho = lam / (c * mu)
    # M/M/1 wait in queue Wq = rho/(mu(1-rho)) for c=1; for c=2 approximate with M/M/2 Erlang-C
    if c == 1: wq = rho / (mu * (1 - rho))
    else:
        a = lam / mu; p0 = 1 / (1 + a + (a**2 / 2) * (1 / (1 - rho))); pw = (a**2 / 2) * (1 / (1 - rho)) * p0; wq = pw / (c * mu - lam)
    out[f"queue_lambda_per_h"] = round(lam, 2); out[f"queue_rho_c{c}"] = round(rho, 3); out[f"queue_wait_min_c{c}"] = round(wq * 60, 1)
# Approval fatigue: reviewer accuracy decays with approvals per hour; illustrative model: acc = 0.95 - 0.02*(rate-10) for rate>10
for r in (6, 10, 20, 30): out[f"reviewer_accuracy_at_{r}_per_hour"] = round(min(0.95, 0.95 - 0.02 * max(0, r - 10)), 2)
# Rubber-stamp detection: median time per approval below 20 s on 6-minute artifacts
out["rubber_stamp_floor_s"] = 20
# Known-bad injection: 2% of queue items are seeded defects; catch rate is the reviewer's measured sensitivity
out["seeded_defect_share_pct"] = 2; out["seeded_per_month"] = int(sum(reviews.values()) * 0.02)
# Rejection reasons: coded to criteria; scenario distribution illustrative
out["rejection_rate_pct_illustrative"] = 8; out["rejections_per_month"] = int(sum(reviews.values()) * 0.08)
# Cost of the gate per task (ch37 oversight line): reviews × 6 min × $60/h / tasks
out["gate_cost_per_task_usd"] = round(sum(reviews.values()) * 6 / 60 * 60 / tasks, 3)
# Escalation on expiry: approval timer 24 h for submissions (illustrative); share expiring at 5%
out["approval_timer_h"] = 24; out["expiry_share_pct_illustrative"] = 5
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
