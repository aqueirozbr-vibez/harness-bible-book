from dataclasses import dataclass, field
from datetime import date, timedelta

@dataclass
class Fact:
    subject: str; predicate: str; value: str
    provenance: list                  # episode ids or reviewer ids that established it
    reviewed_by: str = None
    effective: date = None
    superseded_by: str = None
    clearance: str = "general"
    fact_id: str = None

class Memory:
    def __init__(self, documents: dict):
        self.working, self.episodic, self.semantic, self.procedural = {}, [], {}, {}
        self.documents = documents                       # subject -> set of statements the governed documents make
        self.rejections = []; self._n = 0
    # working
    def write_working(self, task_id: str, key: str, value): self.working.setdefault(task_id, {})[key] = value
    def close_task(self, task_id: str, episode: dict):
        self.episodic.append({"task_id": task_id, **episode, "state": self.working.pop(task_id, {})})
    # semantic filing with provenance and review enforced
    def file_fact(self, f: Fact, require_provenance: bool = True) -> bool:
        if require_provenance and (not f.provenance or not f.reviewed_by):
            self.rejections.append((f.subject, f.predicate, "no provenance/review")); return False
        if f.value in self.documents.get(f.subject, set()):
            self.rejections.append((f.subject, f.predicate, "documents already state it")); return False
        self._n += 1; f.fact_id = f.fact_id or f"f{self._n}"
        for old in self.semantic.get(f.subject, []):
            if old.predicate == f.predicate and not old.superseded_by: old.superseded_by = f.fact_id
        self.semantic.setdefault(f.subject, []).append(f); return True
    def recall(self, subject: str, budget_facts: int = 4, clearance: str = "general") -> list:
        live = [f for f in self.semantic.get(subject, []) if not f.superseded_by and f.clearance == clearance]
        return sorted(live, key=lambda f: f.effective or date.min, reverse=True)[:budget_facts]
    # consolidation: propose from episodes, check documents, review by sampling
    def consolidate(self, propose, review, sample_rate: float, rng, require_provenance: bool = True) -> dict:
        proposed, filed = 0, 0
        for ep in self.episodic:
            for cand in propose(ep):
                proposed += 1
                if cand.value in self.documents.get(cand.subject, set()):
                    self.rejections.append((cand.subject, cand.predicate, "documents already state it")); continue
                accepted = review(cand) if rng.random() < sample_rate else True      # unsampled candidates pass on the proposer's word
                if accepted:
                    cand.provenance = [ep["task_id"]]; cand.reviewed_by = "reviewer" if rng.random() < sample_rate else None
                    filed += self.file_fact(cand, require_provenance)
        return {"proposed": proposed, "filed": filed}
    def retire(self, today: date, max_age_days: int = 365):
        for subj, facts in self.semantic.items():
            for f in facts:
                if f.effective and (today - f.effective).days > max_age_days and not f.superseded_by: f.superseded_by = "expired"
