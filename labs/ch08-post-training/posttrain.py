import math
import numpy as np

def dpo_loss_and_grad(logp_w, logp_l, ref_w, ref_l, beta=0.1):
    """Per-pair DPO loss and its gradient with respect to (logp_w, logp_l)."""
    margin = (logp_w - ref_w) - (logp_l - ref_l)
    s = 1.0 / (1.0 + math.exp(-beta * margin))          # sigma(beta * margin)
    loss = -math.log(s)
    g = -beta * (1.0 - s)                                # dL/d(logp_w) = g ; dL/d(logp_l) = -g
    return loss, g, -g

def grpo_advantages(rewards):
    """Group-relative advantages: standardized reward within the group."""
    r = np.asarray(rewards, dtype=float)
    sd = r.std()
    return (r - r.mean()) / (sd if sd > 0 else 1.0)

def lora_param_count(rank, layers, shapes):
    """shapes: list of (d_in, d_out) for each adapted matrix in one layer."""
    return layers * sum(rank * (din + dout) for din, dout in shapes)

class ToyPolicy:
    """A softmax policy over K candidate responses with a logit per response; used to show DPO behaviour."""
    def __init__(self, K, rng):
        self.logits = rng.standard_normal(K) * 0.1; self.ref = self.logits.copy()
    def logp(self, i, which="policy"):
        z = self.logits if which == "policy" else self.ref
        return float(z[i] - np.log(np.exp(z).sum()))
    def dpo_step(self, w, l, lr=0.5, beta=0.1):
        loss, gw, gl = dpo_loss_and_grad(self.logp(w), self.logp(l), self.logp(w, "ref"), self.logp(l, "ref"), beta)
        p = np.exp(self.logits) / np.exp(self.logits).sum()
        grad = np.zeros_like(self.logits)
        grad += gw * ((np.arange(len(p)) == w) - p)       # d logp_w / d logits
        grad += gl * ((np.arange(len(p)) == l) - p)
        self.logits -= lr * grad
        return loss
