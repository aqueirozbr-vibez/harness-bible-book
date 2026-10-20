#!/usr/bin/env python3
"""Lab 32 / derive.py — every derived number in Chapter 32."""
import json, datetime
out = {}
# Failure log for a month (scenario, illustrative): 1,500 tasks; 8% rejected at the gate (ch31) = 120; sensor failures per task ~1.4 (ch22 repairs) → ~2,100 sensor events; clusters by (code, step, class, language)
out["tasks"] = 1500; out["gate_rejections"] = 120; out["sensor_events"] = 2100
# Cluster ranking score = frequency × consequence × fixability (0-1); illustrative clusters
clusters = [("description mismatch (bearing vs seal)", 38, 2, 0.9), ("stale procedure revision cited", 22, 3, 1.0), ("permit type wrong for class H", 9, 5, 1.0), ("Portuguese abbreviation unresolved", 31, 1, 0.8), ("parts not in BOM", 14, 2, 1.0)]
ranked = sorted(((f * c * x, n, f, c, x) for n, f, c, x in clusters), reverse=True); out["cluster_ranking"] = [{"cluster": n, "score": round(s, 1), "freq": f, "consequence": c, "fixability": x} for s, n, f, c, x in ranked]
# Promotion ladder reliability: guide rule follows at the instruction-following rate (~90-95%, ch18); sensor 100%; template field removes the class
out["ladder"] = {"observation": 0.0, "guide_rule": 0.92, "sensor": 1.0, "template_field_or_tool": 1.0}
# Expected gain from fixing the top cluster: 38 rejections/month of 120 → rejection rate falls from 8% to ~5.5% if fully fixed; at sensor level (repairable) most become repairs, not rejections
out["rejection_rate_before_pct"] = 8.0; out["rejection_rate_after_top_fix_pct"] = round(100 * (120 - 38 * 0.9) / 1500, 2)
# Parallel branches: k candidate changes × affected-class golden run ($10.8, ch27) → cost per cycle
for k in (1, 3, 5): out[f"branch_cost_k{k}"] = round(k * 10.8, 1)
# Golden-set sizing for detecting a 3-point gain at 85% base: paired bootstrap power ~ (ch12: 300 items → ~47% for 3 pts; 1000 → 88%)
out["power_3pt_n300"] = 0.47; out["power_3pt_n1000"] = 0.88
# Holdout: 20% of golden set never used for proposal; a change adopted only if holdout interval overlaps development gain
out["holdout_share"] = 0.2
# Versioning: harness composite version bumps: patch (guide wording, sensor threshold), minor (new sensor/template field/tool), major (loop, policy model, control plane)
out["version_rule"] = {"patch": "guide wording; sensor message; sample rate", "minor": "new sensor; template field; tool; routing row", "major": "loop change; policy bundle model; control-plane migration"}
# Weekly change budget: at most 3 merged changes/week so attribution of gains stays possible
out["weekly_change_budget"] = 3
# Cumulative example over 6 months: pass rate 84 → 86 → 87.5 → 89 → 90 → 91 (illustrative), STP 50 → 63.5
out["pass_rate_curve_illustrative"] = [84, 86, 87.5, 89, 90, 91]; out["stp_curve_illustrative"] = [50, 54, 57, 60, 62, 63.5]
# Safety-review classes: changes to policy bundle, safety gate sensors, tool sets of write classes, routing of gated classes → human safety review always; automated merge never
out["safety_review_classes"] = ["policy bundle", "safety-gate sensors", "tool sets of write classes", "routing of gated classes", "output-policy scanners"]
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
