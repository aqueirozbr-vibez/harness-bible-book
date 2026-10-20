import numpy as np

def rmsnorm(x, w, eps=1e-5):
    return x / np.sqrt((x * x).mean(-1, keepdims=True) + eps) * w

def silu(z):
    return z / (1.0 + np.exp(-z))

def attention(x, Wq, Wk, Wv, Wo, heads, kv_heads, hd):
    n, d = x.shape
    q = (x @ Wq).reshape(n, heads, hd).transpose(1, 0, 2)          # (h, n, hd)
    k = (x @ Wk).reshape(n, kv_heads, hd).transpose(1, 0, 2)       # (h_kv, n, hd)
    v = (x @ Wv).reshape(n, kv_heads, hd).transpose(1, 0, 2)
    k = np.repeat(k, heads // kv_heads, axis=0); v = np.repeat(v, heads // kv_heads, axis=0)   # GQA broadcast
    s = q @ k.transpose(0, 2, 1) / np.sqrt(hd)
    s = np.where(np.triu(np.ones((n, n), bool), 1), -np.inf, s)     # causal mask
    s -= s.max(-1, keepdims=True); w = np.exp(s); w /= w.sum(-1, keepdims=True)
    out = (w @ v).transpose(1, 0, 2).reshape(n, heads * hd)
    return out @ Wo

def ffn(x, W1, W3, W2):
    return (silu(x @ W1) * (x @ W3)) @ W2

def block(x, p):
    """One pre-norm decoder block: x + Attn(Norm(x)); then + FFN(Norm(.))."""
    h = x + attention(rmsnorm(x, p["n1"]), p["Wq"], p["Wk"], p["Wv"], p["Wo"], p["heads"], p["kv_heads"], p["hd"])
    return h + ffn(rmsnorm(h, p["n2"]), p["W1"], p["W3"], p["W2"])

def init_block(d, heads, kv_heads, hd, dff, rng):
    s = lambda *shape: rng.standard_normal(shape).astype(np.float32) * 0.02
    return dict(heads=heads, kv_heads=kv_heads, hd=hd, n1=np.ones(d, np.float32), n2=np.ones(d, np.float32),
                Wq=s(d, heads * hd), Wk=s(d, kv_heads * hd), Wv=s(d, kv_heads * hd), Wo=s(heads * hd, d),
                W1=s(d, dff), W3=s(d, dff), W2=s(dff, d))

def count_params(L, d, heads, kv_heads, hd, dff, V, tied=False):
    attn = d * heads * hd + 2 * d * kv_heads * hd + heads * hd * d
    layer = attn + 3 * d * dff + 2 * d
    embed = V * d; unembed = 0 if tied else V * d
    return {"attention_per_layer": attn, "ffn_per_layer": 3 * d * dff, "layer": layer,
            "layers": L * layer, "embedding": embed, "unembedding": unembed, "total": L * layer + embed + unembed + d}
