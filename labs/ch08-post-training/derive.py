#!/usr/bin/env python3
"""Lab 08 / derive.py — every derived number in Chapter 08."""
import json, datetime, math
out = {}
# LoRA parameter count: rank r on a d_in x d_out matrix adds r*(d_in + d_out). Llama 3 8B: d=4096, kv proj 1024, 32 layers
d, kvd, L = 4096, 1024, 32
def lora_params(r, targets):
    per_layer = 0
    for t in targets:
        din, dout = {"q": (d, d), "k": (d, kvd), "v": (d, kvd), "o": (d, d), "gate": (d, 14336), "up": (d, 14336), "down": (14336, d)}[t]
        per_layer += r * (din + dout)
    return per_layer * L
for r in (8, 16, 64):
    out[f"lora_r{r}_qv"] = lora_params(r, ["q", "v"]); out[f"lora_r{r}_qkvo"] = lora_params(r, ["q", "k", "v", "o"]); out[f"lora_r{r}_all"] = lora_params(r, ["q","k","v","o","gate","up","down"])
    out[f"lora_r{r}_all_pct_of_8B"] = round(100 * out[f"lora_r{r}_all"] / 8.03e9, 3)
# DPO loss for a preference pair: -log sigmoid(beta * ((log pi_w - log ref_w) - (log pi_l - log ref_l)))
def dpo_loss(margin, beta=0.1): return -math.log(1 / (1 + math.exp(-beta * margin)))
for m in (0, 5, 20, 50): out[f"dpo_loss_margin{m}_beta0.1"] = round(dpo_loss(m), 4)
# GRPO group advantages: rewards r_i in a group -> (r_i - mean)/std
rewards = [1, 0, 0, 1, 0, 0, 0, 1]; mu = sum(rewards)/len(rewards); sd = (sum((x-mu)**2 for x in rewards)/len(rewards))**0.5
out["grpo_example_rewards"] = rewards; out["grpo_example_advantages"] = [round((x-mu)/sd, 3) for x in rewards]
# InstructGPT data sizes (Ouyang et al. 2022): ~13k SFT prompts, ~33k comparison prompts, ~31k RL prompts (paper Table 6 approx)
out["instructgpt_sft_prompts"] = 13000; out["instructgpt_rm_prompts"] = 33000; out["instructgpt_rl_prompts"] = 31000
# Scenario fine-tune decision: plant corpus 120M tokens; LoRA on 8B at r=16 all targets; cost of a LoRA run at ~3x forward FLOPs per token per epoch
tokens = 120e6; flops = 6 * 8.03e9 * tokens   # full-parameter equivalent forward+backward
out["finetune_flops_120M_tokens_8B_full"] = f"{flops:.2e}"
out["finetune_hours_on_1_H100_at_300TFLOPs"] = round(flops / 300e12 / 3600, 1)
# Golden-set sample size for a fine-tune decision: Wilson half-width at n=100, p=0.8
def wilson_hw(p, n, z=1.96): return z*math.sqrt(p*(1-p)/n + z*z/(4*n*n)) / (1 + z*z/n)
out["wilson_halfwidth_n100_p80"] = round(wilson_hw(0.8, 100), 3); out["wilson_halfwidth_n300_p80"] = round(wilson_hw(0.8, 300), 3)
out["timestamp"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
json.dump(out, open("results/derived.json","w"), indent=2)
for k,v in out.items(): print(k, v)
