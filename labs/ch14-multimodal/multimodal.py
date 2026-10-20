import math

def patch_tokens(width: int, height: int, patch: int = 14) -> int:
    return (height // patch) * (width // patch)

def tiled_tokens(width: int, height: int, tile: int = 512, per_tile: int = 256, base: int = 256):
    """Vendor-style high-resolution encoding: a base thumbnail plus a pooled budget per tile (per_tile illustrative)."""
    tiles = math.ceil(width / tile) * math.ceil(height / tile)
    return tiles, base + tiles * per_tile

CONFUSIONS = {"O": "0", "0": "O", "I": "1", "1": "I", "S": "5", "5": "S", "B": "8", "8": "B", "Z": "2", "2": "Z"}

def edit_distance(a: str, b: str) -> int:
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]

def confusion_candidates(s: str, max_subs: int = 2) -> set:
    """All strings reachable by substituting up to max_subs characters within the optical confusion classes."""
    out = {s}
    frontier = {s}
    for _ in range(max_subs):
        nxt = set()
        for w in frontier:
            for i, ch in enumerate(w):
                if ch in CONFUSIONS:
                    nxt.add(w[:i] + CONFUSIONS[ch] + w[i + 1:])
        frontier = nxt - out; out |= nxt
    return out

def validate_tag(extracted: str, register: set, max_edits: int = 1) -> dict:
    """Confirm an extracted identifier against the equipment register. Correction order: (1) optical-confusion
    substitutions that land on exactly one registered tag; (2) a unique registered tag within max_edits; else flag.
    Dense registers (P-100…P-399) make plain edit distance ambiguous — P-1O1 is one edit from P-101 and P-111 —
    so confusion-class correction runs first."""
    if extracted in register:
        return {"tag": extracted, "status": "confirmed"}
    conf = [t for t in confusion_candidates(extracted) if t in register and t != extracted]
    if len(conf) == 1:
        return {"tag": conf[0], "status": "corrected", "from": extracted, "by": "confusion-class"}
    near = [t for t in register if edit_distance(extracted, t) <= max_edits]
    if len(near) == 1:
        return {"tag": near[0], "status": "corrected", "from": extracted, "by": "edit-distance"}
    return {"tag": None, "status": "flagged", "from": extracted, "candidates": sorted(set(conf) | set(near))}

def validate_all(extracted: list, register: set) -> dict:
    results = [validate_tag(t, register) for t in extracted]
    return {"results": results,
            "confirmed": sum(r["status"] == "confirmed" for r in results),
            "corrected": sum(r["status"] == "corrected" for r in results),
            "flagged": sum(r["status"] == "flagged" for r in results)}
