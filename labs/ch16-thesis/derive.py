#!/usr/bin/env python3
"""Lab 16 / derive.py — every derived number in Chapter 16.
Inputs are published figures (tiers in the chapter's 16.9); outputs are the arithmetic the chapter states."""
import json, datetime

# τ-bench, Yao et al. 2024 (primary): GPT-4o retail pass^1 = 0.604, airline pass^1 = 0.420; retail pass^8 reported < 0.25
p1_retail, p1_airline, p8_retail_reported = 0.604, 0.420, 0.25
indep = {k: round(p1_retail**k, 4) for k in (1, 2, 4, 8)}                       # if attempts were independent
indep_air = {k: round(p1_airline**k, 4) for k in (1, 2, 4, 8)}
# implied per-attempt correlation: solve for p such that p^8 = 0.25 under independence would need p = 0.25^(1/8)
p_needed_for_25 = round(0.25 ** (1/8), 3)
rel_drop = round(100 * (1 - p8_retail_reported / p1_retail))                     # "roughly 60% relative drop"

# Same-model, different-scaffold spreads ("Stop Comparing LLM Agents Without Disclosing the Harness", 2026 preprint; Epoch AI analyst)
spreads = {"SWE-bench Pro, Claude Opus 4.5, SEAL -> Claude Code": (45.9, 55.4),
           "SWE-bench Verified, Grok 4 (reported spread only)": (0.0, 15.0),   # reported as +14–16 pp; midpoint
           "Epoch AI single-model scaffold range": (62.3, 70.2)}
spread_pp = {k: round(v[1]-v[0], 1) for k, v in spreads.items()}
spread_rel = {k: round(100*(v[1]-v[0])/v[0], 1) for k, v in spreads.items() if v[0] > 20}

# Expected runs to first success at pass^1 p (geometric), and expected cost multiplier vs a p=1 system
exp_attempts = {p: round(1/p, 2) for p in (0.604, 0.80, 0.95, 0.99)}

out = dict(tau_retail_pass1=p1_retail, tau_airline_pass1=p1_airline, tau_retail_pass8_reported_upper=p8_retail_reported,
           pass_k_if_independent_retail=indep, pass_k_if_independent_airline=indep_air,
           per_attempt_rate_needed_for_pass8_of_25pct=p_needed_for_25, relative_drop_pct=rel_drop,
           scaffold_spread_pp=spread_pp, scaffold_spread_relative_pct=spread_rel, expected_attempts_to_success=exp_attempts,
           timestamp=datetime.datetime.now(datetime.timezone.utc).isoformat())
json.dump(out, open("results/derived.json", "w"), indent=2)
for k, v in out.items(): print(f"{k}: {v}")

# Wilson 95% interval widths for pass-rate estimates at golden-set sizes
import math
def wilson(p, n, z=1.96):
    d = 1 + z*z/n; c = (p + z*z/(2*n))/d; h = z*math.sqrt(p*(1-p)/n + z*z/(4*n*n))/d
    return round(c-h, 3), round(c+h, 3)
ci = {n: wilson(0.60, n) for n in (20, 50, 100, 200)}
out["wilson95_at_p60"] = {str(k): v for k, v in ci.items()}
json.dump(out, open("results/derived.json", "w"), indent=2)
print("wilson95_at_p60:", out["wilson95_at_p60"])
