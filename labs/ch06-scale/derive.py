#!/usr/bin/env python3
"""Lab 06 / derive.py — every derived number in Chapter 06."""
import json, datetime, math
out = {}
# Chinchilla parametric loss (Hoffmann et al. 2022, Approach 3 fit): L(N,D) = E + A/N^alpha + B/D^beta
E, A, B, alpha, beta = 1.69, 406.4, 410.7, 0.34, 0.28
def loss(N, D): return E + A / N**alpha + B / D**beta
def optimal(C):
    # minimize loss s.t. 6·N·D = C; scan N on a log grid
    best = None
    for i in range(2000):
        N = 10 ** (6 + 8 * i / 1999); D = C / (6 * N)
        l = loss(N, D)
        if best is None or l < best[0]: best = (l, N, D)
    return best
for C in (1e21, 1e23, 1e25):
    l, N, D = optimal(C); out[f"opt_N_at_C{C:.0e}"] = f"{N:.2e}"; out[f"opt_D_at_C{C:.0e}"] = f"{D:.2e}"; out[f"opt_tokens_per_param_at_C{C:.0e}"] = round(D / N, 1); out[f"opt_loss_at_C{C:.0e}"] = round(l, 3)
# Chinchilla vs Gopher check (from paper): 70B on 1.4T vs 280B on 300B at similar compute
out["gopher_compute"] = f"{6*280e9*300e9:.2e}"; out["chinchilla_compute"] = f"{6*70e9*1.4e12:.2e}"
out["loss_gopher_fit"] = round(loss(280e9, 300e9), 3); out["loss_chinchilla_fit"] = round(loss(70e9, 1.4e12), 3)
# Tokens per parameter for documented runs
runs = {"GPT-3 175B": (175e9, 300e9), "Chinchilla 70B": (70e9, 1.4e12), "Llama 3 8B": (8.03e9, 15e12), "Llama 3 70B": (70.6e9, 15e12), "Llama 3.1 405B": (405.9e9, 15.6e12), "DeepSeek-V3 (total)": (671e9, 14.8e12), "DeepSeek-V3 (active)": (37e9, 14.8e12)}
for k, (N, D) in runs.items():
    out[f"tokens_per_param_{k}"] = round(D / N, 1); out[f"train_FLOPs_6ND_{k}"] = f"{6*N*D:.2e}"
out["llama3_405B_6ND_vs_meta_3.8e25_pct"] = round(100 * (6*405.9e9*15.6e12 - 3.8e25) / 3.8e25, 1)
# Over-training payoff: serving cost per token ∝ 2N; a smaller model over-trained to match a larger model's loss
# compare Llama 3 8B (15T) loss-fit vs hypothetical Chinchilla-optimal model at same compute
C8 = 6*8.03e9*15e12; l_opt, N_opt, D_opt = optimal(C8)
out["llama3_8B_compute"] = f"{C8:.2e}"; out["chinchilla_optimal_at_that_compute_N"] = f"{N_opt:.2e}"; out["chinchilla_optimal_at_that_compute_D"] = f"{D_opt:.2e}"
out["fit_loss_llama3_8B_style"] = round(loss(8.03e9, 15e12), 3); out["fit_loss_chinchilla_optimal_same_compute"] = round(l_opt, 3)
out["inference_cost_ratio_optimal_over_8B"] = round(N_opt / 8.03e9, 1)
# MoE: memory vs compute
moe = {"DeepSeek-V3": (671e9, 37e9), "Llama 4 Maverick": (400e9, 17e9), "Llama 4 Scout": (109e9, 17e9), "Mixtral 8x7B": (46.7e9, 12.9e9), "Qwen3-235B-A22B": (235e9, 22e9)}
for k, (tot, act) in moe.items():
    out[f"moe_memory_GB_fp16_{k}"] = round(tot * 2 / 1e9); out[f"moe_flops_per_token_GFLOP_{k}"] = round(2 * act / 1e9); out[f"moe_total_over_active_{k}"] = round(tot / act, 1)
# dense equivalent for compute: a 37B dense model would need 74 GB; V3 needs 1342 GB → memory ratio
out["v3_memory_over_dense37B"] = round(671 / 37, 1)
# Load-balancing arithmetic: 256 experts, top-8 routing → each expert sees 8/256 = 3.1% of tokens if balanced
out["v3_expert_share_if_balanced_pct"] = round(100 * 8 / 256, 1)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
