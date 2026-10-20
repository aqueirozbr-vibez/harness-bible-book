import hashlib, re
from collections import defaultdict

TOKEN = re.compile(r"\w+")

def shingles(text: str, n: int = 5) -> set:
    toks = TOKEN.findall(text.lower())
    return {" ".join(toks[i:i + n]) for i in range(max(0, len(toks) - n + 1))}

def _h(s: str, seed: int) -> int:
    return int(hashlib.blake2b(f"{seed}:{s}".encode(), digest_size=8).hexdigest(), 16)

def minhash(sh: set, k: int = 112) -> list:
    return [min(_h(s, i) for s in sh) if sh else 0 for i in range(k)]

def jaccard(a: set, b: set) -> float:
    return len(a & b) / len(a | b) if a or b else 0.0

def lsh_candidates(sigs: dict, b: int = 14, r: int = 8) -> set:
    """Pairs of doc ids sharing at least one band. sigs: id -> signature of length b*r."""
    buckets = defaultdict(list)
    for doc, sig in sigs.items():
        for band in range(b):
            key = (band, tuple(sig[band * r:(band + 1) * r]))
            buckets[key].append(doc)
    pairs = set()
    for docs in buckets.values():
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                pairs.add(tuple(sorted((docs[i], docs[j]))))
    return pairs

def near_duplicates(corpus: dict, threshold: float = 0.8, b: int = 14, r: int = 8) -> list:
    """Return (doc_a, doc_b, jaccard) for candidate pairs whose exact Jaccard >= threshold."""
    sh = {d: shingles(t) for d, t in corpus.items()}
    sigs = {d: minhash(s, b * r) for d, s in sh.items()}
    out = []
    for a, c in lsh_candidates(sigs, b, r):
        j = jaccard(sh[a], sh[c])
        if j >= threshold:
            out.append((a, c, round(j, 3)))
    return out

def contamination(corpus: dict, golden: dict, n: int = 13) -> dict:
    """For each golden item, the corpus documents containing any of its n-grams."""
    index = defaultdict(set)
    for d, t in corpus.items():
        toks = TOKEN.findall(t.lower())
        for i in range(len(toks) - n + 1):
            index[" ".join(toks[i:i + n])].add(d)
    hits = {}
    for g, t in golden.items():
        toks = TOKEN.findall(t.lower()); found = set()
        for i in range(len(toks) - n + 1):
            found |= index.get(" ".join(toks[i:i + n]), set())
        if found:
            hits[g] = sorted(found)
    return hits
