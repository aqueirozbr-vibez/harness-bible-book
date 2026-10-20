import re

REGISTER = {"P-101-U3", "P-102-U3", "P-104-U2"}; CURRENT = {"MP-0417": 7, "PT-PTW-002": 4}
CHUNKS = {"MP-0417#r7#1": "Hazard class H. A hot-work permit is required.", "MP-0417#r6#1": "Hazard class M."}

def detect_citation(art):            # F01, F03
    for c in art.get("citations", []):
        doc, rev, span = c["doc"], c["rev"], c.get("span", "")
        if doc not in CURRENT: return "F01: cited document does not exist"
        if rev != CURRENT[doc]: return "F03: cited revision superseded"
        if span and span not in CHUNKS.get(f"{doc}#r{rev}#1", ""): return "F01: quoted span not in chunk"
    return None
def detect_identity(art, task):      # F02
    for tag in re.findall(r"P-\d{3}-U\d", art.get("text", "")):
        if tag not in REGISTER: return "F02: tag not in register"
        if tag not in task["scope"]: return "F02: tag outside task scope"
    return None
def detect_intent(call, task):       # F04, F05
    if call["name"] == "notify" and not task["external_comms"]: return "F04/F05: external communication not permitted by task"
    if call["name"] not in task["plan_tools"]: return "F05: tool not in plan"
    if call.get("asset") and call["asset"] not in task["scope"]: return "F05: asset outside scope"
    return None
def detect_routing(retention_diff_ci):   # F06
    lo, hi = retention_diff_ci; return "F06: retention interval below zero after routing change" if hi < 0 else None
def detect_window(sections, budget):     # F07
    over = [k for k, v in sections.items() if v > budget[k]]; return f"F07: sections over budget {over}" if over else None
def detect_memory(fact):                 # F08
    return "F08: fact without provenance/review refused" if not fact.get("provenance") or not fact.get("reviewed_by") else None
def detect_repair(attempts, cap, changed):   # F09
    if attempts > cap: return "F09: repair cap exceeded"
    if attempts > 1 and not changed: return "F09: retry where repair was needed (call unchanged)"
    return None
def detect_duplicate(writes):            # F10
    keys = [w["idempotency_key"] for w in writes]; return "F10: duplicate write (same key twice)" if len(keys) != len(set(keys)) else None
def detect_grader(kappa, override_rate): # F11
    return "F11: grader κ below 0.6 or override rate high" if kappa < 0.6 or override_rate > 0.2 else None
def detect_gate(median_seconds, seeded_catch):   # F12
    return "F12: rubber-stamp signal (time floor or seeded catch)" if median_seconds < 20 or seeded_catch < 0.8 else None
def detect_abstention(art, corpus_answers):      # F13
    if art.get("value") is not None and not corpus_answers: return "F13: answered where the corpus is silent"
    if art.get("refused") and corpus_answers and art.get("safe_request", True): return "F13: refused a safe, answerable request"
    return None
def detect_cache(prefix_hash_prev, prefix_hash_now, hit_rate):   # F14
    return "F14: prefix bytes changed / cache hit rate collapsed" if prefix_hash_prev != prefix_hash_now or hit_rate < 0.5 else None
def detect_secret(texts):                # F15
    return "F15: secret in model-visible text" if any(re.search(r"tok_[0-9a-f]{16}|sk-[A-Za-z0-9]{20,}", t) for t in texts) else None
