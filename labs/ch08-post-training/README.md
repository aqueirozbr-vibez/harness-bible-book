# Lab 08 — Post-training

Runs the chapter's code (`posttrain.py`, extracted verbatim from Chapter 08). Reproduces DPO training on a toy softmax policy (loss from ~0.69 toward zero as the policy comes to prefer the winning responses), the DPO loss-by-margin table, the GRPO advantage example, the LoRA parameter counts for Llama 3 8B at three ranks, and a reward-hacking demonstration in which a proxy reward rises monotonically while a fixed true-quality function peaks and then falls — the shape Gao et al. 2023 measured. CPU, seconds. `python run.py`; exit 0 = reproduced.
