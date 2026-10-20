import re
from dataclasses import dataclass, field

@dataclass
class Template:
    task_class: str
    required_fields: list                 # fields the request must supply
    criteria: list                        # (id, description, sensor_name or None)
    default_action: str                   # "draft" | "submit"
    scope_rule: str                       # "named_equipment"

TEMPLATES = {
    "work_order_from_fault": Template(
        "work_order_from_fault", ["equipment_tag", "symptom"],
        [("c1", "all required fields present", "schema"), ("c2", "zone registered", "zone_registered"),
         ("c3", "procedure cited at current revision", "citation"), ("c4", "permit matches hazard class", "permit_rule"),
         ("c5", "parts in approved list", "parts_in_bom"), ("c6", "description matches reported fault", None)],
        "draft", "named_equipment"),
}

TAG = re.compile(r"\b([A-Z]{1,2})-(\d{3})\b")

def normalize(channel: str, payload: dict, identity: str, ts: str) -> dict:
    """One schema from any channel. Chat: free text; form/webhook: structured."""
    text = payload.get("text", "")
    fields = {k: v for k, v in payload.items() if k != "text"}
    if channel == "chat":
        m = TAG.search(text)
        if m: fields.setdefault("equipment_tag", m.group(0))
        if "leak" in text.lower() or "vaz" in text.lower(): fields.setdefault("symptom", "leak")
    return {"request": text, "fields": fields, "trigger": {"channel": channel, "identity": identity, "ts": ts}}

def classify(rec: dict) -> str:
    return "work_order_from_fault"       # one class in this lab; the router's taxonomy in production (ch23)

def resolve(rec: dict, tpl: Template, register: dict) -> dict:
    """Apply the template; return the task record or a clarification question."""
    missing = [f for f in tpl.required_fields if f not in rec["fields"]]
    tag = rec["fields"].get("equipment_tag")
    ambiguous = tag and len(register.get(tag, [])) > 1
    if missing or ambiguous:
        q = []
        if missing: q.append(f"Please provide: {', '.join(missing)}.")
        if ambiguous: q.append(f"{tag} matches {len(register[tag])} assets ({', '.join(register[tag])}). Which one?")
        return {"status": "clarify", "question": " ".join(q), "record": rec}
    asset = register[tag][0]
    return {"status": "ready", "task": {**rec, "class": tpl.task_class, "criteria": tpl.criteria,
            "constraints": {"scope_equipment": [asset], "allowed_action": tpl.default_action, "external_comms": False}}}

def coverage(task: dict) -> dict:
    total = len(task["criteria"]); covered = sum(1 for _, _, s in task["criteria"] if s)
    return {"total": total, "covered": covered, "uncovered": [d for _, d, s in task["criteria"] if not s]}

def intent_validate(task: dict, action: dict) -> dict:
    """Deny actions outside the task's declared scope — before the policy engine's role rules (ch28)."""
    c = task["constraints"]
    if action["tool"] == "submit_work_order" and c["allowed_action"] != "submit":
        return {"ok": False, "reason": "Task is scoped to drafting; submission requires a task with allowed_action=submit."}
    if action.get("equipment") and action["equipment"] not in c["scope_equipment"]:
        return {"ok": False, "reason": f"Action targets {action['equipment']}, outside task scope {c['scope_equipment']}."}
    if action["tool"] in ("send_email", "post_external") and not c["external_comms"]:
        return {"ok": False, "reason": "Task does not permit external communication."}
    return {"ok": True, "reason": ""}
