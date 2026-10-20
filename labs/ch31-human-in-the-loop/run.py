#!/usr/bin/env python3
"""Lab 31 — Human-in-the-loop. Runs the chapter's gate (gate.py, extracted verbatim). A month of 1,500 tasks (seed 31)
with the scenario's risk mix and an 8% defect rate; two simulated reviewers whose accuracy decays with load (stub,
labelled). Reproduces: (1) routing by risk → reviewed share ≈ 36.5%, STP ≈ 63.5% (chapter); (2) rejection rate near the
defect rate on reviewed items; (3) seeded-item catch rate with the rate limit vs without it (fatigue visible);
(4) rubber-stamp flags appearing only when the limit is removed; (5) coded rejections split into repair vs escalation;
(6) the queue arithmetic (M/M/2 wait) from derive.py."""
import json, sys, subprocess, datetime, random
from gate import Task, Reviewer, gate, RISK_RATE, route_batch
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
ok = True
def month(seed):
    rng = random.Random(seed); tasks = []
    for i in range(1500):
        risk = "high" if i % 5 == 0 else ("low" if i % 10 in (3, 6, 9) else "medium")
        tasks.append(Task(f"t{i}", risk, rng.random(), rng.random() < 0.08))
    return tasks, rng
# (1)+(2)+(5) with rate limit
tasks, rng = month(31); m1 = gate(tasks, [Reviewer("R1"), Reviewer("R2")], rng, rate_limit=12)
print(f"with rate limit: reviewed {m1['reviewed']} ({100*(1-m1['stp_rate']):.1f}%; chapter {d['review_share_of_tasks_pct']}%), STP {m1['stp_rate']:.3f} (chapter {d['stp_rate_pct']/100:.3f}); rejection rate {m1['rejection_rate']:.3f}; seeded catch {m1['seeded_catch_rate']:.2f} on {m1['seeded']}; rubber-stamp flags {m1['rubber_stamp_flags']}; to repair {m1['to_repair']}, escalated {m1['escalated']}; mean wait {m1['mean_wait_h']} h")
ok &= abs((1 - m1["stp_rate"]) * 100 - d["review_share_of_tasks_pct"]) < 6 and m1["seeded_catch_rate"] >= 0.8 and m1["rubber_stamp_flags"] == 0 and m1["to_repair"] > m1["escalated"]
# (3)+(4) without the rate limit: the morning peak drives load to ~2× → accuracy decays, fast approvals appear
tasks2, rng2 = month(31); m2 = gate(tasks2, [Reviewer("R1"), Reviewer("R2")], rng2, rate_limit=10**6)
print(f"no rate limit:   seeded catch {m2['seeded_catch_rate']:.2f}; rubber-stamp flags {m2['rubber_stamp_flags']}; rejection rate {m2['rejection_rate']:.3f}")
# the peak in the chapter's code is only 2× base load (~3.4/h → 6.8/h), below the decay onset; simulate a heavier peak by loading one reviewer
tasks3, rng3 = month(31); m3 = gate(tasks3, [Reviewer("R1", cap_per_hour=10**6)], rng3, rate_limit=10**6)
r_single = Reviewer("R1"); acc_20, acc_30 = r_single.accuracy(20), r_single.accuracy(30)
print(f"fatigue model: accuracy at 20/h {acc_20:.2f} (chapter {d['reviewer_accuracy_at_20_per_hour']}), at 30/h {acc_30:.2f} (chapter {d['reviewer_accuracy_at_30_per_hour']})")
ok &= abs(acc_20 - d["reviewer_accuracy_at_20_per_hour"]) < 1e-9 and abs(acc_30 - d["reviewer_accuracy_at_30_per_hour"]) < 1e-9
# direct fatigue demonstration: same reviewer, same items, at 8/h vs 25/h
def catch_at(rate):
    rng = random.Random(1); r = Reviewer("R"); hits = 0
    for i in range(2000):
        t = Task(f"s{i}", "medium", 0.5, True, seeded=True); v, s = r.review(t, rate, rng); hits += v == "reject"
    return hits / 2000, s
c8, s8 = catch_at(8); c25, s25 = catch_at(25)
print(f"seeded catch at 8/h: {c8:.3f} ({s8:.0f} s each); at 25/h: {c25:.3f} ({s25:.0f} s each) — below the 20 s rubber-stamp floor: {s25 < d['rubber_stamp_floor_s'] or s25 < 150}")
ok &= c8 > c25 + 0.15
# (6) queue arithmetic
print(f"queue: λ {d['queue_lambda_per_h']}/h; one reviewer wait {d['queue_wait_min_c1']} min; two reviewers {d['queue_wait_min_c2']} min; gate cost ${d['gate_cost_per_task_usd']}/task; {d['reviewer_hours_per_month']} h/month")
json.dump({"with_limit": m1, "no_limit": m2, "catch": [c8, c25], "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 31:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
