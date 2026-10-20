import math, re
from collections import Counter, defaultdict

TOKEN = re.compile(r"[A-Za-z]+|\d+|[^\sA-Za-z\d]")
def ntok(s: str) -> int: return max(1, round(len(s) / 4))

def chunk_document(doc_id: str, text: str, meta: dict, target_tokens: int = 512) -> list:
    """Chunk on structure (blank-line paragraphs), never mid-paragraph; prefix each chunk with its context; carry metadata."""
    paras = [p.strip() for p in text.split("\n\n") if p.strip()]
    chunks, cur = [], []
    for p in paras:
        if cur and ntok("\n\n".join(cur + [p])) > target_tokens:
            chunks.append("\n\n".join(cur)); cur = [p]
        else:
            cur.append(p)
    if cur: chunks.append("\n\n".join(cur))
    out = []
    for i, body in enumerate(chunks):
        prefix = f"From {meta['doc_id']} rev {meta['rev']} ({meta['title']}), applies to {', '.join(meta['assets'])}."
        cid = f"{doc_id}#r{meta['rev']}#{i}"
        out.append({"chunk_id": cid, "text": prefix + "\n" + body, "meta": meta})
    return out

def embed(text: str, dims: int = 512) -> list:
    v = [0.0] * dims; s = f" {text.lower()} "
    for i in range(len(s) - 2): v[hash(s[i:i+3]) % dims] += 1.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]

class Index:
    def __init__(self): self.chunks, self.vec, self.tf, self.df, self.avg = {}, {}, {}, Counter(), 0.0
    def add(self, ch: dict):
        self.chunks[ch["chunk_id"]] = ch; self.vec[ch["chunk_id"]] = embed(ch["text"])
        terms = TOKEN.findall(ch["text"].lower()); self.tf[ch["chunk_id"]] = Counter(terms)
        for t in set(terms): self.df[t] += 1
        self.avg = sum(sum(c.values()) for c in self.tf.values()) / len(self.tf)
    def _bm25(self, q: str, ids: list, k1=1.5, b=0.75) -> dict:
        qt = TOKEN.findall(q.lower()); N = len(self.tf); out = {}
        for d in ids:
            tf = self.tf[d]; L = sum(tf.values()); s = 0.0
            for t in qt:
                if t not in tf: continue
                idf = math.log(1 + (N - self.df[t] + 0.5) / (self.df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * L / self.avg))
            out[d] = s
        return out
    def search(self, query: str, filters: dict, k: int = 3, shortlist: int = 20, rerank=None, threshold: float = 0.0) -> dict:
        ids = [d for d, ch in self.chunks.items() if all(ch["meta"].get(f) == v or (isinstance(ch["meta"].get(f), list) and v in ch["meta"][f]) for f, v in filters.items())]
        if not ids: return {"chunks": [], "abstain": True, "reason": "no chunk passes the filters"}
        qv = embed(query); vs = {d: sum(a * b for a, b in zip(qv, self.vec[d])) for d in ids}; ls = self._bm25(query, ids)
        rv = {d: i for i, d in enumerate(sorted(ids, key=lambda d: -vs[d]))}; rl = {d: i for i, d in enumerate(sorted(ids, key=lambda d: -ls.get(d, 0)))}
        fused = sorted(ids, key=lambda d: -(1 / (60 + rv[d]) + 1 / (60 + rl[d])))[:shortlist]
        if rerank:
            scored = sorted(((rerank(query, self.chunks[d]["text"]), d) for d in fused), reverse=True)
            if scored[0][0] < threshold: return {"chunks": [], "abstain": True, "reason": f"top re-rank score {scored[0][0]:.2f} below threshold"}
            fused = [d for _, d in scored]
        return {"chunks": [self.chunks[d] for d in fused[:k]], "abstain": False, "reason": ""}

def term_overlap_reranker(query: str, text: str) -> float:
    """Stand-in for a cross-encoder (labelled): share of query terms present in the passage."""
    q = set(TOKEN.findall(query.lower())) - {"the", "for", "of", "a", "in", "on"}; t = set(TOKEN.findall(text.lower()))
    return len(q & t) / max(1, len(q))

def citation_coverage(claims: list, cited_ids: list, index: Index) -> dict:
    valid = [c for c in cited_ids if c in index.chunks and index.chunks[c]["meta"].get("current")]
    return {"claims": len(claims), "cited_valid": len(valid), "coverage": round(len(valid) / max(1, len(claims)), 3)}

def stale_rate(results: list) -> float:
    admitted = [ch for r in results for ch in r["chunks"]]
    return round(sum(1 for ch in admitted if not ch["meta"].get("current")) / max(1, len(admitted)), 4)
