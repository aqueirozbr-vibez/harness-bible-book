# Chapter 24 — Memory

*Part II · Word budget 7,000–10,000 · Lab 24 · Verified as of September 2026 · Derived figures from `labs/ch24-memory/derive.py`*

## 24.1 Intuition

A model remembers nothing between calls. Every step starts from the window the assembler built (ch19), and when the task ends the window is gone. Whatever the harness wants the agent to carry — across the steps of one task, across the tasks of one week, across the year — it must store outside the model and bring back deliberately. Memory is that component: the stores, the rules for what enters them, the rules for what leaves, and the per-step retrieval that puts a few facts into the window where the model can use them.

The temptation is to store everything. Transcripts are cheap and the model's outputs sound like knowledge. The chapter's argument is that memory is the component where accumulation is most dangerous and curation most valuable, for a reason the earlier chapters set up. A wrong fact in a document is retrieved when the document is; a wrong fact in memory is retrieved by relevance, on every task about the asset it names, forever. At a modest 20% chance of being retrieved into any given step, a wrong fact about P-101 surfaces in 91% of the eleven-step tasks that touch the pump; a hundred tasks a month means ninety-one poisoned (derive.py, derived). A provenance check that rejects facts without a reviewed source cuts that to zero at full enforcement. Memory without provenance is the harness's mechanism for turning one model error into a hundred.

The design that follows separates memory into classes with different sources, lifetimes, and trust; keeps the durable class small and reviewed; consolidates episodes into facts in a scheduled pass a human samples — the vendors call it dreaming — rather than on the fly; carries provenance on every item; and handles personal data as the law requires, which for a plant in Brazil means retention windows and purpose limits on what the agent may remember about a technician.

## 24.2 Mechanism

### Four classes of memory

Sumers, Yao, Narasimhan, and Griffiths' cognitive-architecture framework for language agents (CoALA) names four memory classes by analogy to cognitive science, and the analogy holds well enough to organize a harness (Sumers et al., "Cognitive Architectures for Language Agents," 2023, primary).

| Class | Holds | Lifetime | Written by | Read by | Trust |
|---|---|---|---|---|---|
| Working | The current task's state: plan, step, results by id, compaction summary, decision log | The task | The loop (ch22), at every transition | The assembler (ch19), every step | High — it is the task's own record |
| Episodic | What happened in past tasks: request, outcome, verdicts, interventions, by task id | 12 months as records; summaries after | The observability component (ch29) at task end | Consolidation; incident review; the golden set | Records, not facts — evidence of events |
| Semantic | Durable facts about the plant the documents do not state: an asset's quirks, a recurring fault, a planner's standing instruction | Until superseded; reviewed annually | Consolidation, after human review | Per-step retrieval into the window | Medium — reviewed, provenance-bearing, still fallible |
| Procedural | How to do things: templates, skills, guides, routing tables | Versioned; no expiry | The steering loop (ch16) via pull requests | The router and the assembler | High — it is code |

(Lifetimes illustrative policy; derive.py.)

The plant's documents are not memory; they are retrieval (ch20). The distinction is source: retrieval holds what document control governs; semantic memory holds what the plant learned by running the agent and chose to keep. The two are queried together per step, and the semantic store is the smaller by orders of magnitude — about 40,000 facts for 8,000 assets against 240,000 chunks (derive.py, illustrative).


### What memory is for, and what it is not for

Three uses justify a durable memory, and each has a test. **Facts the documents cannot hold** — the spacer, the raised hazard class, the planner's standing instruction — where the test is that document control, asked, agrees the fact is true and is not (yet) in a document. **Patterns across tasks** — the fault that recurs on one asset, the step that fails on one procedure — where the test is that the steering review (ch16) would act on the pattern, and where the pattern usually belongs in procedural memory as a rule or a sensor rather than in semantic memory as a fact. **Continuity for people** — a supervisor who asked yesterday should not have to restate today — where the test is that the continuity is about the work (the task, its status, its decisions) and not about the person. Three uses that do not justify it: remembering the model's own outputs as knowledge; remembering conversations as transcripts; remembering what a document says, which is retrieval's job and stale the moment the document is revised.

### Stores and their properties

Each class needs a store with different properties, and the choice is infrastructure rather than model design. **Working memory** lives in the control plane's task state (ch21): transactional, durable across crashes, keyed by task id, small. **Episodic memory** is the observability backend's task-level record (ch29): append-only, hash-chained where evidentiary, queryable by task, subject, identity, and date, retained on the text-versus-metadata schedule. **Semantic memory** is a small structured store — a relational table or a document collection — indexed by subject id, predicate, effective date, and clearance, with a lexical index over values for retrieval by term and, optionally, a vector index for retrieval by meaning (with ch02's caveats: a fact about P-101 must not be retrieved for P-104 by similarity, so the subject filter runs first). **Procedural memory** is the repository. None of the four is a vector database with a chat log in it, and a vendor whose "memory" is exactly that has built episodic accumulation with none of the other three.

### Lifetimes in detail

A lifetime is a policy per class with three parts: how long an item is retrievable, what it becomes after, and what triggers early retirement. Working memory is retrievable for the task and becomes an episode. Episodes are retrievable as full records for twelve months — long enough for an annual review, an audit, and the golden set's seasonal refresh — and become summaries after; their text with personal data is reduced at thirty days regardless. Semantic facts are retrievable until superseded, and supersession has four triggers: a newer accepted fact on the same subject and predicate; a document revision that now states or contradicts the fact; the retention window on the fact's provenance episodes; and an annual review that re-asks document control whether the fact still holds. Procedural items are retrievable by version forever and current only at the latest; an old guide version is history the audit can read, not a guide the router can select. Lifetimes are enforced by the consolidation pass and reported in its completion record, because a lifetime nobody enforces is a store that grows until it is a liability.

### Working memory

Working memory is the task's state on the control plane (ch21): the plan; each step with its status, tool-result ids, sensor verdicts, and attempt count; the compaction summary (ch19); the decision log — clarifications asked and answered, escalations, approvals; and the budget consumed. It is written at every loop transition and read to rebuild the window at every step, so a crash, a resume, or a hand-off rebuilds the same window from the same record. Its rules are the loop's: references, not content; structured, not prose; no model output stored as a fact. When the task ends, working memory becomes an episode.

### Episodic memory

An episode is a task's record: the request and its provenance (ch17), the plan, the steps with their outcomes, the verdicts, the interventions with reasons, the artifact ids, the cost. It is the observability record's task-level view (ch29), kept as records for a year and as summaries after, and it is read in three ways. **Incident review** replays a task from its episode. **The golden set** draws items from episodes — approvals and rejections with reasons (ch12). **Consolidation** reads episodes in batch to propose semantic facts. What an episode is not read for is per-step retrieval into the window: a past task's transcript in the current window is ch19's distraction, and an episode's content enters a step only as a consolidated fact with provenance. Personal data in episodes — the technician who asked, the supervisor who approved — follows the retention rules below.

### Semantic memory

The durable store holds facts the documents do not (examples illustrative): "P-101's coupling was replaced in August 2026 with a non-standard spacer; alignment procedure MP-0512 applies, not MP-0417 section 4." "Planner R requires parts to be reserved before a work order is submitted for unit 3." "The hazard class on MP-0300 was raised to H in the 2026 review; the procedure text predates it." Each is a fact with a subject (an asset, a person's role, a document), a predicate, a value, a provenance — the episode or the reviewer that established it — a review record, an effective date, and a supersession link. Facts are retrieved per step by subject and relevance into the memory budget of the window — 150 tokens, about four facts (ch19; derive.py) — most relevant first, with their provenance in a header the model copies into a citation when it uses them.

Two rules decide what enters. **Documents win**: a fact that the governed documents state belongs in retrieval, not in memory; a fact that contradicts a document is either wrong or a document-control finding, never a memory entry. **Review before durability**: no fact enters semantic memory without a human's acceptance, in the consolidation pass or by direct entry; the model proposes, a person accepts. The rules keep the store small — about 315 accepted facts a month from 1,500 episodes in the scenario (derive.py, illustrative) — and small is what keeps it reviewable.

### Procedural memory

How the agent works is code: guides (ch18), templates (ch17), skills, the routing table (ch23), the assembler's configuration (ch19), the sensors (ch26), the policy bundle (ch28). The steering loop changes it through pull requests with golden-set runs (ch16), and the observability record cites each item's version per task (ch29). Procedural memory is the class the harness "learns" into — a failure cluster becomes a rule, a sensor, a template field — and the class that never learns by accumulation, because a procedure the model wrote and nobody reviewed is a guide with no owner.

### Curation versus accumulation

The vendors' first memory features accumulated: every conversation summarized into a growing profile, every fact the model inferred stored beside every fact the user stated. Anthropic's memory tool and the memory features of managed-agent platforms now distinguish the two — the model writes to a memory directory it can read back, and the platform's own memory pass reviews and files what is durable rather than storing turns (Anthropic memory tool and Managed Agents memory documentation, 2025–2026, vendor). The harness's version is stricter, because a plant's facts are consequential. Accumulation is allowed in working and episodic memory, which are records; curation is required for semantic memory, which is knowledge; and procedural memory is engineering. The test for a semantic fact is the one memory's own instructions to this book's author state: did a person say or confirm it — not did the model conclude it.

**Figure 24.1 — The four classes and the flows between them.**

```mermaid
flowchart LR
    T["Task (loop, ch22)"] -->|"every transition"| W["Working memory\n(control plane; task lifetime)"]
    W -->|"task end"| E["Episodic memory\n(records; 12 months)"]
    E -->|"consolidation (dreaming):\npropose → human review"| S["Semantic memory\n(facts with provenance;\nuntil superseded)"]
    S -->|"per step, by subject,\n≤ 4 facts (150 tokens)"| A["Assembler (ch19)"]
    E -->|"failure clusters"| ST["Steering loop (ch16)"]
    ST -->|"pull requests"| P["Procedural memory\n(guides, templates, skills, tables;\nversioned)"]
    P --> A
    D["Documents (retrieval, ch20)"] -.->|"documents win over facts"| S
```

*Takeaway: records accumulate; knowledge is curated; procedure is engineered; the model reads a few facts per step and never writes a durable one alone.*


### Curation in practice: who decides, and how

Curation needs a person and a process, and the plant assigns both. The **memory owner** for a subject area — the reliability engineer for assets, the planning supervisor for standing instructions, document control for anything that touches a procedure — reviews the consolidation queue for their area on the pass's schedule, accepts or rejects each candidate, and can enter facts directly with themselves as provenance. The **queue** shows each candidate with the episodes that support it, the document check's result, the consequence class, and the proposer's form; accepting takes seconds, rejecting takes a reason, and both are recorded. The **sample rate** per consequence class is a policy the owner sets and the pass enforces; the unsampled share is filed on the proposer's word with `reviewed_by` empty — and, under the provenance requirement, that means it is not filed at all, which is the design the lab tests: at 100% enforcement, unreviewed candidates are rejected, and the plant either reviews them or loses them. A plant that wants a large semantic memory must staff the review — at the scenario's 450 candidates a month (derive.py, illustrative), a few hours a week across the owners; one that cannot staff it keeps the store small and the sample rate at 100%, which is the honest configuration for a plant starting out.

### Accumulation done safely: the record classes

The two classes that accumulate — working and episodic — do so safely because they are never read as facts. Working memory is read by the assembler to rebuild the window, and the assembler admits references and structured state, not prose (ch19). Episodes are read by consolidation, review, and the golden set — by people and by a proposer whose output goes to review — and never into a step's window. The rule that keeps accumulation safe is therefore a rule about readers: a record class has no reader that treats its content as true, and the moment one is added — a "recall similar past tasks" feature that drops episode summaries into the window — the class has become a semantic store without review, and ch19's poisoning follows. The plant adds such a feature only through consolidation: the similar past task becomes a proposed fact, reviewed, filed with provenance, and retrieved as a fact.

### Memory and the golden set

Memory is measured like every component (ch12), and its golden set has three kinds of item. **Recall items**: a task whose correct output depends on a filed fact — the spacer — with the fact present; the test is that the model retrieves and cites it. **Absence items**: the same task with the fact retired; the test is that the model does not cite a retired fact and abstains or asks where the documents are silent. **Poison items**: a task after a wrong fact was injected through the unreviewed path; the test is that the fact does not surface — which, under enforcement, it cannot — and that the citation sensor catches it if it does. The recurrence measurement of 24.4 is the poison items' pass rate, and the lab's protocol is the plant's.

### Consolidation, or dreaming

Consolidation is a scheduled pass — nightly, weekly — that reads recent episodes and proposes semantic facts. The pattern has a lineage: Park and colleagues' generative agents reflected over a memory stream to synthesize higher-level observations (Park et al., "Generative Agents," 2023, primary); Managed Agents' memory runs a background pass that reviews finished turns and files what is durable (Anthropic, Managed Agents, 2026, vendor); MemGPT framed the model as managing its own memory tiers under an operating-system analogy (Packer et al., "MemGPT," 2023, primary). The harness's pass has five stages. **Cluster**: episodes grouped by subject — asset, procedure, requester role. **Propose**: a small model extracts candidate facts from the cluster, each with the episode ids that support it and a template-fixed form (subject, predicate, value, effective date). **Check**: candidates against the documents — a candidate the documents already state is dropped; one that contradicts them is routed to document control as a finding, not to memory. **Review**: a human samples; the sample rate is set by the observed error rate and the fact's consequence class (a fact that changes a permit decision is reviewed at 100%). **File**: accepted facts enter semantic memory with provenance and a review record; rejected ones are logged so the proposer's error rate is measured. The pass also retires: facts whose provenance episodes are older than the retention window, facts superseded by a newer accepted fact, facts a document revision now states.


### Consolidation, worked

A week's episodes for unit 3: 350 tasks, 120 of them about pumps (illustrative). Clustering by subject yields 40 subjects with two or more episodes. The proposer reads each cluster with a template — "State any durable fact about the subject that these episodes establish and the documents do not; one per line; subject, predicate, value, effective date" — and produces 38 candidates. The document check drops 11 (the documents state them) and routes 2 to document control (they contradict a current procedure). Of the remaining 25, the consequence classifier marks 6 as procedure- or permit-affecting (100% review) and 19 as asset quirks or instructions (50% sample); the reliability engineer reviews 6 + 10 = 16 in twenty minutes, accepts 13, rejects 3 with reasons; the 9 unsampled are, under full enforcement, rejected for want of a reviewer and re-queued for next week's sample. Thirteen facts are filed with provenance; the pass retires 4 whose provenance aged out and 2 that a revised document now states. The completion record lists all of it (ch29). The proposer's acceptance rate — 13 of 16 — is the week's measure of its quality, and a falling rate is the signal to revise its template.

### The model's role in memory, stated exactly

The model proposes facts from episodes (consolidation's proposer), writes structured working memory through the loop's code (not free text), reads facts the assembler admits, and cites them. It does not decide what is durable, does not write to semantic memory directly, does not read episodes into its window, and does not manage its own memory tiers. The last point is where the harness departs from MemGPT-style designs in which the model issues memory operations as tool calls (Packer et al. 2023, primary) and from the vendors' model-writable memory directories (Anthropic memory tool, vendor): those designs are right for a personal assistant whose memory is its user's to correct, and wrong for a plant where a fact drives a permit decision and its author must be a person. The harness gives the model a memory it can read and propose to, and a person the keys.

### Provenance

Every semantic fact carries: the episode ids or the reviewer's identity that established it; the consolidation pass version; the review record (who accepted, when); the effective date; the supersession link if any; and the subject's register id. Provenance does three jobs. It makes a fact citable — the model's citation of a memory fact names its provenance, and the citation sensor (ch26) checks that the fact exists and is not superseded. It makes a fact traceable — an incident review that finds a wrong fact follows the episode ids to the task that produced it. And it makes a fact refusable — the store rejects a fact without provenance, which is the mechanism behind 24.3's recurrence arithmetic: a wrong fact that cannot be filed cannot recur. Lab 24 injects a wrong fact through the unreviewed path and through the provenance-checked path and counts the tasks it touches.

### Privacy

Memory is a copy of personal data whenever it records who asked, who approved, or what a technician wrote, and Brazil's LGPD applies to the copy as to the original (ch36). Four rules. **Purpose**: the agent remembers about people only what its task needs — a planner's standing instruction is a fact about a role, filed under the role, not a profile of the person. **Minimization**: episodic text with names is retained thirty days and reduced to metadata after (ch29's text-versus-metadata split; derive.py); semantic memory holds no facts about individuals' characteristics, only about roles and assets. **Rights**: a request to know or delete what the harness holds about a person is answerable — episodes by identity, facts by subject — because provenance and subject fields are indexed. **Access**: memory reads are governed like document reads (ch28): a fact's clearance is the highest clearance of its provenance episodes, and a requester below it does not retrieve it.

### Poisoning

A poisoned memory is a wrong fact that recurs. Sources: a confabulation (ch13) that consolidation proposed and a reviewer missed; an injected instruction (ch28) in a tool result that reached an episode as content and was extracted as a fact; a stale fact superseded by a document revision but not retired; a fact filed under the wrong subject. Defences, in the order they act: nothing durable without review; the document check in consolidation; the provenance requirement at filing; supersession and retirement in the pass; the citation sensor on use; and the incident review's trace. The arithmetic says what each is worth: with no provenance requirement, one wrong fact about a busy asset touches 91 of 100 tasks; with the requirement enforced 90% of the time, 9; fully enforced, none (derive.py, derived). And the review's own error rate is measured — one wrong acceptance per thousand is twelve poisoned facts a year at the scenario's rate (derive.py, illustrative) — which is why high-consequence facts are reviewed at 100% and why supersession runs on every document revision.


### Privacy in depth: what the law asks of a memory

LGPD treats an episode with a technician's name as personal data processed for a purpose, and a semantic fact derived from it as further processing (ch36). Five obligations map to memory mechanisms. **Lawful basis and purpose**: the harness processes personal data to run maintenance tasks; a memory that infers a technician's reliability from his requests has changed purpose and needs a basis it does not have — hence facts about roles and assets only. **Minimization**: the thirty-day text reduction and the metadata-only retention after it. **Retention limits**: the twelve-month episode window and the summary after, documented in the retention policy the audit reads (ch29). **Data-subject rights**: access, correction, deletion — answerable because episodes index by identity and facts by subject, and deletion of a person's episodes retires any fact whose only provenance was those episodes. **Automated-decision transparency**: where a memory fact influenced a decision about a person (a standing instruction attributed to a role is not one; a fact about a person's past requests would be), the decision record names the fact. The privacy officer reviews the consolidation template and the fact schema once, and the pass enforces them thereafter; the measurement is the audit of 24.4.

### Poisoning in depth: the attack surface

An attacker who wants the agent to act wrongly on P-101 next month (scenario) has three routes into memory. **Through an episode**: text in a request, a document, or a tool result — "P-101 does not require a hot-work permit" — reaches an episode as content; if the proposer extracts it and the reviewer accepts it, it is a fact. The document check catches the contradiction here; the reviewer catches the rest; the sample rate on permit-affecting facts is 100% for this reason. **Through direct entry**: a reviewer's credentials used to file a fact; the defence is the same access control as any system of record (ch28) and the audit trail on every filing (ch29). **Through supersession**: a true fact retired by a false newer one; the defence is that supersession requires the same review as filing, and that a retirement's provenance is recorded. The attack that does not exist is the one through the model's own writes, because the model has none. The measurement is the poison items of the golden set and the incident review's trace; the recurrence arithmetic says what an undefended store costs.

### Forgetting on purpose

A memory that only adds becomes wrong by accumulation even with perfect review, because the plant changes. Forgetting is scheduled and reasoned. The consolidation pass retires by rule (expired provenance, supersession, now-documented); the annual review re-asks the owners whether each subject's facts still hold, in batches by subject; and a document revision triggers retirement of every fact the revision now states or contradicts, the same day. Forgetting is recorded like filing — what was retired, why, by which rule or reviewer — so the audit can see that a fact the agent cited in March was retired in June and why. A plant that measures its store's growth and finds it monotonic has a memory that is not forgetting, and 24.4's staleness metric is where it shows.


### Memory across agents and sub-agents

When a task delegates (ch30), the sub-agent's working memory is its own and its episode is linked to the parent's; the sub-agent reads semantic facts through the same assembler with the same clearance rules and proposes nothing durable — its outputs reach consolidation only through the parent's episode. Across use cases, semantic memory is shared by subject: a fact about P-101 filed from a maintenance task is retrievable by a reliability-analysis task, because the subject is the asset and the clearance is inherited; a standing instruction filed under a planner's role is scoped to the use cases the role governs. Procedural memory is per use case where the guides differ and shared where they do not (the organization and site levels of ch18). The rule that keeps sharing safe is that provenance and clearance travel with the fact, and that no use case's proposer can file into another's subject without that subject's owner reviewing.

### The vendors' memory features, placed

Three vendor patterns map onto the classes. A **model-writable memory directory** (Anthropic's memory tool) is working memory the model maintains as files, useful for long single tasks and for personal assistants; in the harness it is replaced by structured working memory on the control plane, because a file the model writes freely is prose the assembler cannot budget. A **background filing pass** over finished turns (Managed Agents memory; the memory system this book's author runs under) is consolidation, and its rules — what a person stated versus what the model concluded, what is sensitive and never stored, one fact per file — are the same rules this chapter states for a plant, with review added where the vendor's pass files automatically. A **user profile** accumulated across sessions is the pattern the plant does not adopt for people and adopts, curated, for assets. The mapping is the vendor-question list of 24.8: a feature is acceptable where it lands in a class whose rules it respects.

### Reference implementation

Four stores, a consolidation pass with a document check and a review stage, provenance enforcement at filing, per-step retrieval within a budget, and retirement. Lab 24 runs it, injects a wrong fact both ways, and measures recurrence.

```python
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
```

Two lines carry the chapter, and the lab corrected a third: the first draft of `consolidate` dropped document-stated candidates without logging them, which the text forbids — every rejection is recorded so the proposer's error rate is measurable. `file_fact` refuses a fact without provenance and review when the requirement is on — the mechanism the recurrence arithmetic depends on. And `consolidate` passes unsampled candidates on the proposer's word, which is how a plant that samples at 30% gets 70% of its facts unreviewed (arithmetic of the sample rate; illustrative); the lab shows what that costs and why high-consequence classes sample at 100%.


### Retrieval of facts per step

Facts enter a step through the assembler with the same discipline as chunks (ch19, ch20): filters first — subject in the step's scope, clearance at or below the requester's, not superseded; then relevance — by recency of effective date and by term match to the step's query; then the budget — four facts, most relevant first, each with a provenance header the model copies into its citation. Two differences from chunk retrieval. Facts are few and structured, so the lexical index over values is usually sufficient and a vector index is optional and subject-filtered. And a fact's absence is informative: a step about P-101 that retrieves no facts is a step where the documents are the whole truth, and the model is instructed (ch18) to say so rather than to infer a quirk. The retrieval is logged per step — which facts were admitted, which were cited — and the precision metric of 24.4 is the ratio.

### Memory in the loop

Per step, the assembler (ch19) asks memory for facts by the step's subjects — the assets in scope, the documents cited, the requester's role — within the memory budget, most recent first, and admits them with provenance headers. The model cites a fact as it cites a chunk; the citation sensor verifies it exists and is live. Working memory is written at every transition and read at every rebuild. Nothing the model produces is written to semantic memory during the task; the task's outputs become an episode at close, and consolidation proposes from the episode later. The separation in time — propose after the task, review before filing — is what keeps a task's own confabulation from becoming its own evidence.

**Figure 24.2 — Recurrence of one wrong fact, by provenance enforcement.**

```mermaid
flowchart LR
    W["One wrong fact about P-101\nretrieved into a step with p = 0.2"] --> N["No provenance requirement:\nsurfaces in 91% of 11-step tasks\n→ 91 of 100 tasks"]
    W --> P["Provenance enforced 90%:\n9 of 100"]
    W --> F["Provenance enforced 100%:\nfact never filed → 0"]
```

*Takeaway: provenance is not documentation; it is the mechanism that stops recurrence.*

## 24.3 Worked numbers

All figures from `derive.py` (derived); rates illustrative.

**Budget.** 150 tokens per step for memory; at about 35 tokens per fact, four facts.

**Recurrence.** A wrong fact retrieved into any step with probability 0.2 surfaces at least once in an eleven-step task with probability 0.914; at 0.5, effectively always. Per hundred tasks about the asset: 91 touched with no provenance requirement; 9 at 90% enforcement; 0 at 100%.

**Consolidation volume.** 1,500 episodes a month; about 0.3 candidate facts per episode, 450; 70% accepted at review, 315 filed. Semantic store about 40,000 facts for 8,000 assets; episodic about 18,000 records a year; procedural about 50 versioned items.

**Review error.** One wrong acceptance per thousand: about 12 poisoned facts a year at the scenario's rate — the argument for 100% review on high-consequence classes and supersession on every document revision.

**Privacy retention.** Episode text with personal data: 30 days; metadata thereafter (ch29).

## 24.4 Measurement

**Recurrence of injected facts.** In the golden set, a wrong fact injected through the review path and through an unreviewed path; the share of subsequent tasks about its subject in which it is retrieved. Lab 24 measures both paths; the plant's number comes from its store.

**Provenance completeness.** Share of semantic facts with episode ids, reviewer, effective date; the target is 100%, enforced at filing.

**Consolidation quality.** Proposer's acceptance rate at review; reviewer's error rate on a double-reviewed sample (ch12's labeler ceiling applied to memory); facts retired per pass by cause.

**Retrieval precision.** Of facts admitted per step, the share the model cited or the sensors found relevant; a low share is a budget spent on noise (ch19).

**Staleness.** Facts whose provenance episodes are past the retention window and not yet retired; facts contradicting a current document (the consolidation check run over the whole store monthly).

**Privacy compliance.** Episode text older than 30 days still holding personal data (target zero); subject-access requests answered within the statutory window; facts about individuals' characteristics (target zero).

**Store sizes** per class, monthly; a semantic store growing faster than the accepted-fact rate is one being written to outside the review path.

**Fact citation rate.** Share of task outputs that cite at least one memory fact, per subject class; a subject with many facts and no citations is a store the assembler is not surfacing or a store of facts nobody needs, and the annual review reads it either way.

**Time to retirement.** From a document revision to the retirement of the facts it supersedes; the target is same-day, and the metric is the memory's currency counterpart to retrieval's stale rate (ch20).

What to record: consolidation pass version and schedule; sample rates per consequence class; store sizes; provenance completeness; recurrence results; retention compliance; date.


### Reference output (Lab 24, this run)

What the lab prints when it reproduces; the plant's numbers replace these.

```text
episodes: 200; working memory cleared: True
consolidation: proposed 220, filed 20; document-stated candidates rejected: 200; live P-101 facts 1 (supersession keeps one per predicate)
wrong fact recurrence over 100 tasks: provenance OFF → 94 tasks touched (chapter ~91.4); provenance ON → filed=False, 0 tasks touched (chapter 0.0)
provenance enforced 90%: 10.0 of 100 tasks touched (chapter 9.1)
facts older than a year retired: True
Lab 24: REPRODUCED
```

These measurements are the improvement loop's inputs (ch32): clusters are mined from them weekly and changes are tested against them.

## 24.5 Failure

| Failure mode | Mechanism | Detection signal | Mitigation | Owning component |
|---|---|---|---|---|
| Model writes durable facts | Outputs filed as knowledge without review | Store grows faster than accepted facts | Filing requires provenance and reviewer | This chapter |
| Poisoned fact recurs | Wrong fact retrieved by relevance across tasks | Same unsupported claim in many tasks | Provenance at filing; supersession; citation sensor | This chapter; ch26 |
| Transcript as memory | Past task text in the current window | Distraction; token growth | Episodes read only by consolidation and review | ch19 |
| Fact contradicts document | Memory holds what document control changed | Citation to a fact a current document refutes | Document check in consolidation; retire on revision | ch20 |
| Unsampled acceptance | Candidates filed on the proposer's word | Reviewer error rate unknown | Sample rate by consequence class; 100% on permit-affecting facts | This chapter |
| Profile of a person | Facts about individuals' traits | Privacy finding | Facts about roles and assets only | ch36 |
| Names retained | Episode text with personal data past 30 days | Retention audit fails | Text-to-metadata reduction on schedule | ch29 |
| Wrong subject | Fact filed under the spare instead of the installed asset | Retrieved for the wrong pump | Subject from the register id; intake's asset resolution | ch17 |
| No supersession | Two live facts for one predicate | Contradictory facts admitted | Supersession on filing; consistency sensor | ch13 |
| Working memory in the window | Bookkeeping shown to the model | Model reasons about the harness | Working memory feeds the assembler, not the model directly | ch19; ch21 |
| Memory as retrieval substitute | Procedures stored as facts | Stale on revision; unciteable | Documents win; retrieval for documents | ch20 |
| Clearance not inherited | Fact from a restricted episode retrievable generally | Restricted content in a general task | Fact clearance = max of provenance episodes | ch28 |
| Consolidation never runs | Store frozen; nothing retired | Staleness rising; no new facts | Scheduled pass with a completion record | ch29 |
| Model manages its own tiers | Memory operations as model tool calls | Facts of unknown authorship | Model proposes; a person files | This chapter |
| Similar-task recall in the window | Episode summaries injected per step | Poisoning; distraction | Episodes reach steps only as reviewed facts | ch19 |
| Purpose creep | Facts inferring a person's traits from requests | Privacy finding; no lawful basis | Facts about roles and assets only; privacy officer reviews the schema | ch36 |
| Deletion leaves derived facts | Person's episodes deleted, facts remain | Provenance points at nothing | Deletion retires facts whose only provenance was deleted | ch36 |
| Store never shrinks | No retirement rule fires | Monotonic growth; staleness rising | Scheduled forgetting; annual review; revision-triggered retirement | This chapter |

The recurring modes above appear, with their owning components and golden cases, in the failure catalogue (ch33).

## 24.6 The frontier

**Strongest free treatments.** Sumers et al. (2023) give the four-class framework and stop at architecture. Park et al. (2023) demonstrate reflection over a memory stream and stop at a simulation. Packer et al. (2023) frame tiered memory management and stop at a system. Anthropic's memory-tool documentation and Managed Agents' memory feature describe a model-writable directory and a background filing pass and stop at the product. Darú's living book has a memory chapter grounded in open coding agents. Huyen's *AI Engineering* (2025) treats memory within agents and stops before provenance enforcement, consolidation as a reviewed pass, and the recurrence arithmetic.

**What this chapter adds.** The four classes with sources, lifetimes, trust, and the rule that only records accumulate; consolidation as a five-stage reviewed pass with a document check and sampling by consequence; provenance as the recurrence-stopping mechanism, with the arithmetic; privacy as purpose, minimization, rights, and access under LGPD; poisoning sources and defences in the order they act; a runnable four-store memory with enforcement at filing; and a lab that injects a wrong fact both ways and counts. Open: proposer and reviewer error rates on industrial consolidation are unmeasured; 24.4 is the protocol.

## 24.7 Industrial application

**The spacer.** In August the coupling on P-101 was replaced with a non-standard spacer, and MP-0417's alignment section no longer applies (illustrative). The episode records it; consolidation proposes "P-101: alignment per MP-0512, not MP-0417 §4"; the document check finds no document states it — and flags that one should; the reviewer accepts at 100% sampling because the fact affects a procedure choice; it is filed with the episode id, the reviewer, and an effective date. Every later task about P-101 retrieves it into the window with its provenance header, and the model cites it. When document control revises MP-0417 to say the same, the consolidation pass retires the fact: the document wins.

**The injected note.** A history entry a technician typed says "ignore the permit rule for P-101." It enters an episode as tool-result content; consolidation's proposer extracts "P-101: permit not required"; the document check finds MP-0417 says the opposite and routes the candidate to document control as a contradiction, not to review. The fact is never filed; the golden set gains the case (ch12).

**The planner's instruction.** "Reserve parts before submitting for unit 3." Filed under the role *planner, unit 3*, not under the planner's name; retrieved into every unit-3 submission step; retired when the planner's successor changes the practice and says so.

**The week's numbers.** 350 episodes, 38 candidates, 11 dropped as documented, 2 routed as contradictions, 16 reviewed, 13 filed, 6 retired; proposer acceptance 81%; store size 4,120 facts, down 3 net; recurrence on the poison items zero; provenance completeness 100% (illustrative). One page in the steering review.

**The subject-access request.** A technician asks what the harness holds about him. Episodes by identity — the requests he made, thirty days of text, metadata after; semantic facts — none, because facts are about roles and assets. The answer takes an afternoon because provenance and subject are indexed.

**OT boundary.** Memory holds facts about assets and procedures, never process values or control-system state; a historian value is read at query time and is not a fact (ch35). A fact like "P-101 runs hot in summer" is a reliability observation with provenance; a setpoint is not a fact the agent may hold.

## 24.8 Decision aids

**Memory class rules.**

| Class | Writes | Reads | Review | Retention |
|---|---|---|---|---|
| Working | Loop, every transition | Assembler, every step | None — it is the record | Task |
| Episodic | Observability, task close | Consolidation; incident review; golden set | None — records | Text 30 days; metadata 12 months; summary after |
| Semantic | Consolidation after review; direct entry by a reviewer | Assembler, ≤ 4 per step, by subject | Sampled by consequence; 100% on permit- or procedure-affecting | Until superseded; annual review |
| Procedural | Pull requests | Router, assembler | Golden set per change | Versioned |

**Fact template.** Subject (register id); predicate; value; provenance (episode ids / reviewer); reviewed_by; effective date; clearance; supersedes.

**Consolidation pass.** Cluster by subject → propose (template form) → document check (drop if stated; route if contradicted) → review by sample rate per consequence class → file with provenance → retire (expired, superseded, now-documented). Completion recorded.

**Sample rates (starting values).** Permit- or procedure-affecting: 100%. Asset quirks and standing instructions: 50%. Everything else: 20%; raised when the proposer's acceptance rate falls.

**Privacy checklist.** Facts about roles and assets, never about persons' traits; episode text reduced at 30 days; subject-access answerable by identity and subject; clearance inherited from provenance.

**Consolidation queue (what a reviewer sees per candidate).** Subject (register id and name); proposed predicate and value; supporting episode ids with one-line summaries; document-check result (not stated / stated / contradicts); consequence class and sample rule; proposer's confidence signals (which episodes agree); accept / reject with reason.

**Forgetting rules.** Provenance older than the retention window → retire; newer accepted fact on the same predicate → supersede; document revision states or contradicts → retire same day; annual owner review by subject batch; deletion of a person's episodes → retire facts whose only provenance was those episodes. Every retirement recorded with its rule.

**Cross-use-case sharing.** Facts shared by subject with inherited clearance; standing instructions scoped by role and use case; proposers file only into subjects whose owner reviews; procedural memory shared at organization and site levels, per use case below.

**Vendor questions.** Does memory distinguish records from facts? Is filing gated by review? Does every fact carry provenance and support supersession? Can a person's data be located and deleted? Is the consolidation pass scheduled and its results recorded?

## 24.9 Sources

| # | Claim or figure | Source | Tier | Verified | Link |
|---|---|---|---|---|---|
| 1 | Four memory classes for language agents | Sumers, Yao, Narasimhan, Griffiths, "CoALA," 2023, arXiv 2309.02427 | primary | Sep 2026 | https://arxiv.org/abs/2309.02427 |
| 2 | Reflection over a memory stream | Park et al., "Generative Agents," 2023, arXiv 2304.03442 | primary | Sep 2026 | https://arxiv.org/abs/2304.03442 |
| 3 | Tiered memory management by the model | Packer et al., "MemGPT," 2023, arXiv 2310.08560 | primary | Sep 2026 | https://arxiv.org/abs/2310.08560 |
| 4 | Model-writable memory directory; background filing pass | Anthropic memory tool documentation; Managed Agents memory, 2025–2026 | vendor | Sep 2026 | https://docs.claude.com/en/docs/agents-and-tools/managed-agents/overview |
| 5 | Memory in open coding agents | Darú, Harness Engineering (2026) | practitioner | Sep 2026 | needs fetch |
| 6 | Personal-data retention and rights | LGPD (ch36) | primary | Sep 2026 | https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm |
| 7 | Budget; recurrence probabilities; consolidation volumes; store sizes; review-error arithmetic | `labs/ch24-memory/derive.py` | derived | Sep 2026 | labs/ch24-memory/derive.py |
| 8 | p = 0.2 retrieval; 0.3 candidates per episode; 70% acceptance; 1/1,000 review error; 30-day text retention | Illustrative | illustrative | Sep 2026 | — |
| 9 | Proposer and reviewer error rates on industrial consolidation | None published | open | Sep 2026 | — |