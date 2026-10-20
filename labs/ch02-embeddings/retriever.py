import math, re
from collections import Counter, defaultdict

TOKEN = re.compile(r"[A-Za-z]+|\d+|[^\sA-Za-z\d]")

def embed(text: str, dims: int = 512) -> list:
    """Hashed character-trigram embedding: a lexical stand-in for a learned model (labelled substitute)."""
    v = [0.0] * dims
    s = f" {text.lower()} "
    for i in range(len(s) - 2):
        v[hash(s[i:i+3]) % dims] += 1.0
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]

def cosine(a: list, b: list) -> float:
    return sum(x * y for x, y in zip(a, b))

class LexicalIndex:
    """BM25-style scoring over exact terms; identifiers survive intact."""
    def __init__(self, k1=1.5, b=0.75):
        self.k1, self.b, self.docs, self.df, self.avg = k1, b, {}, Counter(), 0.0
    def add(self, doc_id: str, text: str):
        terms = TOKEN.findall(text.lower()); self.docs[doc_id] = Counter(terms)
        for t in set(terms): self.df[t] += 1
        self.avg = sum(sum(c.values()) for c in self.docs.values()) / len(self.docs)
    def score(self, query: str) -> dict:
        q = TOKEN.findall(query.lower()); N = len(self.docs); out = {}
        for d, tf in self.docs.items():
            L = sum(tf.values()); s = 0.0
            for t in q:
                if t not in tf: continue
                idf = math.log(1 + (N - self.df[t] + 0.5) / (self.df[t] + 0.5))
                s += idf * tf[t] * (self.k1 + 1) / (tf[t] + self.k1 * (1 - self.b + self.b * L / self.avg))
            out[d] = s
        return out

class Retriever:
    def __init__(self):
        self.vectors, self.meta, self.lex = {}, {}, LexicalIndex()
    def add(self, doc_id: str, text: str, **meta):
        self.vectors[doc_id] = embed(text); self.meta[doc_id] = meta; self.lex.add(doc_id, text)
    def search(self, query: str, k: int = 3, filters: dict = None, mode: str = "hybrid") -> list:
        allowed = [d for d, m in self.meta.items() if all(m.get(f) == v for f, v in (filters or {}).items())]
        qv = embed(query); vec = {d: cosine(qv, self.vectors[d]) for d in allowed}
        lex = {d: s for d, s in self.lex.score(query).items() if d in allowed}
        if mode == "vector": ranked = sorted(allowed, key=lambda d: -vec[d])
        elif mode == "lexical": ranked = sorted(allowed, key=lambda d: -lex.get(d, 0.0))
        else:                                                    # reciprocal-rank fusion
            rv = {d: i for i, d in enumerate(sorted(allowed, key=lambda d: -vec[d]))}
            rl = {d: i for i, d in enumerate(sorted(allowed, key=lambda d: -lex.get(d, 0.0)))}
            ranked = sorted(allowed, key=lambda d: -(1 / (60 + rv[d]) + 1 / (60 + rl[d])))
        return ranked[:k]
