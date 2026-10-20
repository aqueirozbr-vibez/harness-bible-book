#!/usr/bin/env python3
"""Lab 08 — Post-training. Runs the chapter's code (posttrain.py, extracted verbatim). Reproduces: (1) DPO on a toy
softmax policy over 6 candidate responses — after 200 steps on preference pairs the policy prefers the winners and the
per-pair loss falls from ~0.69 toward the chapter's margin table; (2) GRPO advantages for the chapter's example group;
(3) LoRA parameter counts for Llama 3 8B at ranks 8/16/64; (4) a reward-hacking demonstration: optimizing a proxy
('longer is better') raises proxy score while a fixed true-quality function peaks and falls (Gao et al. 2023 shape)."""
import json, sys, subprocess, datetime, math, numpy as np
from posttrain import dpo_loss_and_grad, grpo_advantages, lora_param_count, ToyPolicy
subprocess.run([sys.executable, "derive.py"], check=True, capture_output=True); d = json.load(open("results/derived.json"))
rng = np.random.default_rng(8); ok = True
# 1. DPO toy
pol = ToyPolicy(6, rng); pairs = [(0, 3), (1, 4), (0, 5), (2, 3), (1, 5)]   # winners 0,1,2 ; losers 3,4,5
losses = []
for step in range(200):
    w, l = pairs[step % len(pairs)]; losses.append(pol.dpo_step(w, l, lr=0.5, beta=0.1))
p = np.exp(pol.logits) / np.exp(pol.logits).sum()
print(f"DPO toy: mean loss first 5 steps {np.mean(losses[:5]):.3f} → last 5 steps {np.mean(losses[-5:]):.3f}; P(winners) {p[:3].sum():.3f}, P(losers) {p[3:].sum():.3f}")
ok &= np.mean(losses[:5]) > 0.6 and np.mean(losses[-5:]) < np.mean(losses[:5]) - 0.1 and p[:3].sum() > 0.9   # β = 0.1: loss falls slowly; preference is the test
# margin table
for m, exp in ((0, 0.6931), (20, 0.1269), (50, 0.0067)):
    loss, _, _ = dpo_loss_and_grad(m, 0, 0, 0, 0.1); k = abs(loss - exp) < 1e-3; ok &= k; print(f"DPO loss at margin {m:2d}: {loss:.4f} (chapter {exp}) {'OK' if k else 'MISMATCH'}")
# 2. GRPO
adv = grpo_advantages(d["grpo_example_rewards"]); exp = np.array(d["grpo_example_advantages"]); k = np.allclose(adv, exp, atol=1e-3); ok &= k
print(f"GRPO advantages: {np.round(adv,3).tolist()} {'OK' if k else 'MISMATCH'}")
# 3. LoRA counts
shapes_all = [(4096,4096),(4096,1024),(4096,1024),(4096,4096),(4096,14336),(4096,14336),(14336,4096)]
for r in (8, 16, 64):
    n = lora_param_count(r, 32, shapes_all); exp = d[f"lora_r{r}_all"]; k = n == exp; ok &= k; print(f"LoRA r={r:2d} all projections: {n/1e6:6.1f}M (chapter {exp/1e6:.1f}M) {'OK' if k else 'MISMATCH'}")
# 4. Reward hacking: policy = length distribution; proxy = length; true = quality peaks at length 12 then falls
lengths = np.arange(2, 41); true_q = np.exp(-((lengths - 12) / 6.0) ** 2); proxy = lengths / 40.0
logits = -((lengths - 4) / 8.0) ** 2   # policy starts preferring short outputs, below the true-quality peak at 12
true_hist = []; proxy_hist = []
for step in range(600):
    pr = np.exp(logits) / np.exp(logits).sum()
    proxy_hist.append(float((pr * proxy).sum())); true_hist.append(float((pr * true_q).sum()))
    logits += 0.1 * (proxy - proxy.mean())            # push every action's logit by its proxy reward: pure proxy optimization
peak = int(np.argmax(true_hist)); rising = proxy_hist[-1] > proxy_hist[0]; fell = true_hist[-1] < max(true_hist) * 0.8
print(f"reward hacking: proxy {proxy_hist[0]:.3f} → {proxy_hist[-1]:.3f} (rising); true quality peaked at step {peak} at {max(true_hist):.3f}, ended at {true_hist[-1]:.3f} (fell)")
ok &= rising and fell and 0 < peak < 599
json.dump({"dpo_final_loss": float(np.mean(losses[-5:])), "p_winners": float(p[:3].sum()), "hack_peak_step": peak, "true_end": true_hist[-1],
           "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()}, open("results/run.json","w"), indent=2)
print("Lab 08:", "REPRODUCED" if ok else "NOT REPRODUCED"); sys.exit(0 if ok else 1)
