#!/usr/bin/env python3
"""Lab 37 / derive.py — every derived number in Chapter 37 is produced here.
Prices are September 2026 list prices (vendor) passed as inputs; change them and rerun."""
import json, sys, datetime

P = {  # USD per million tokens: fresh input, cached input, output
    "frontier": dict(i=1.25, c=0.125, o=10.00),   # GPT-5 list (vendor, Sep 2026)
    "small":    dict(i=0.25, c=0.025, o=2.00),    # GPT-5-mini list (vendor, Sep 2026)
}
S = dict(qpd=2000, days=30, tin=6000, tcache=4000, tout=400, esc=0.10, treason=2000, route=0.90)
GPU = dict(gpus=2, usd_per_gpu_hr=2.99, hours=730, ops_factor=1.3)   # RunPod H100 SXM on-demand (vendor); ops factor analyst

def configs(S=S, P=P, GPU=GPU):
    q = S["qpd"]*S["days"]; tf = S["tin"]-S["tcache"]; tc = S["tcache"]
    outavg = S["tout"] + S["esc"]*S["treason"]
    f, s = P["frontier"], P["small"]
    A = dict(fi=q*S["tin"]*f["i"]/1e6, ci=0, o=q*outavg*f["o"]/1e6)
    B = dict(fi=q*tf*f["i"]/1e6, ci=q*tc*f["c"]/1e6, o=q*outavg*f["o"]/1e6)
    qs, qf = q*S["route"], q*(1-S["route"]); escF = min(1.0, q*S["esc"]/qf) if qf else 0
    C = dict(fi=(qs*tf*s["i"]+qf*tf*f["i"])/1e6, ci=(qs*tc*s["c"]+qf*tc*f["c"])/1e6,
             o=(qs*S["tout"]*s["o"]+qf*(S["tout"]+escF*S["treason"])*f["o"])/1e6)
    comp = GPU["gpus"]*GPU["usd_per_gpu_hr"]*GPU["hours"]
    D = dict(fi=0, ci=0, o=0, comp=comp, ops=comp*(GPU["ops_factor"]-1))
    for x in (A,B,C): x["total"]=x["fi"]+x["ci"]+x["o"]
    D["total"]=D["comp"]+D["ops"]
    return q, A, B, C, D

q, A, B, C, D = configs()
out = {"queries_per_month": q, "A": A, "B": B, "C": C, "D": D,
       "saving_A_to_C_pct": round(100*(1-C["total"]/A["total"]),1),
       "saving_A_to_B_pct": round(100*(1-B["total"]/A["total"]),1),
       "breakeven_vs_B_queries": round(D["total"]/(B["total"]/q)), "breakeven_vs_B_x": round(D["total"]/B["total"],1),
       "breakeven_vs_C_queries": round(D["total"]/(C["total"]/q)), "breakeven_vs_C_x": round(D["total"]/C["total"],1)}
# sensitivity on B
sens = {}
for k, vals in {"tout":[400,800], "esc":[0.0,0.10,0.30], "qpd":[2000,20000]}.items():
    sens[k] = {}
    for v in vals:
        S2 = dict(S); S2[k] = v; _, _, B2, _, _ = configs(S2); sens[k][str(v)] = round(B2["total"])
out["sensitivity_B"] = sens
# token multipliers (Anthropic multi-agent post, vendor): agents ~4x chat, multi-agent ~15x
out["multiagent_C_total_at_15x"] = round(C["total"]*15)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items():
    if isinstance(v, dict) and "total" in v: print(f"{k}: " + ", ".join(f"{kk} {vv:,.0f}" for kk,vv in v.items()))
    elif not isinstance(v, dict): print(f"{k}: {v}")
print("sensitivity_B:", json.dumps(sens))

# --- red-team additions: ops factor 2.0 and a 70/30 routing split
_, _, _, _, D2 = configs(S, P, dict(GPU, ops_factor=2.0)); out["D_total_ops2.0"] = round(D2["total"])
S70 = dict(S, route=0.70); _, _, _, C70, _ = configs(S70); out["C_total_route70"] = round(C70["total"])
out["saving_A_to_C_route70_pct"] = round(100*(1-C70["total"]/A["total"]),1)
out["breakeven_vs_B_x_ops2.0"] = round(D2["total"]/B["total"],1); out["breakeven_vs_C_x_ops2.0"] = round(D2["total"]/C["total"],1)
json.dump(out, open("results/derived.json","w"), indent=2)
print("D_total_ops2.0", out["D_total_ops2.0"], "C_total_route70", out["C_total_route70"], "saving70", out["saving_A_to_C_route70_pct"], "be_ops2", out["breakeven_vs_B_x_ops2.0"], out["breakeven_vs_C_x_ops2.0"])
