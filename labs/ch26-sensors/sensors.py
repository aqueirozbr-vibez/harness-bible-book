from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class Verdict:
    sensor: str; ok: bool; message: str = ""; cost_ms: float = 0.0

class Sensor:
    """A check with a name, a cost class (for ordering), and a function returning (ok, message)."""
    def __init__(self, name: str, cost: int, fn: Callable[[dict, dict], tuple]):
        self.name, self.cost, self.fn = name, cost, fn
    def run(self, artifact: dict, refs: dict) -> Verdict:
        ok, msg = self.fn(artifact, refs)
        return Verdict(self.name, ok, msg if not ok else "")

def run_chain(sensors: list, artifact: dict, refs: dict, fail_fast: bool = True) -> list:
    """Run sensors cheap-first; stop at the first failure when fail_fast."""
    verdicts = []
    for s in sorted(sensors, key=lambda s: s.cost):
        v = s.run(artifact, refs); verdicts.append(v)
        if not v.ok and fail_fast:
            break
    return verdicts

# --- computational sensors for the work-order artifact -------------------------------------
REQUIRED = {"order_id": str, "equipment_tag": str, "zone": str, "description": str,
            "procedure_ref": str, "procedure_rev": int, "parts": list, "permit_type": str}
HAZARD_TO_PERMIT = {"L": "none", "M": "cold_work", "H": "hot_work"}

def schema(a, refs):
    for field, typ in REQUIRED.items():
        if field not in a:
            return False, f"Field `{field}` is required and missing."
        if not isinstance(a[field], typ) or (typ is str and a[field] == ""):
            return False, f"Field `{field}` must be a non-empty {typ.__name__}; found {a[field]!r}."
    return True, ""

def citation(a, refs):
    doc = refs["procedures"].get(a.get("procedure_ref"))
    if doc is None:
        return False, f"Procedure `{a.get('procedure_ref')}` is not in the document index; cite an indexed procedure."
    if a.get("procedure_rev") != doc["current_rev"]:
        return False, (f"Procedure `{a['procedure_ref']}` is cited at revision {a.get('procedure_rev')}; "
                       f"the current revision is {doc['current_rev']}. Cite the current revision.")
    return True, ""

def permit_rule(a, refs):
    doc = refs["procedures"].get(a.get("procedure_ref"), {})
    required = HAZARD_TO_PERMIT.get(doc.get("hazard_class"))
    if required and a.get("permit_type") != required:
        return False, (f"Field `permit_type` is {a.get('permit_type')!r}; the procedure's hazard class is "
                       f"{doc['hazard_class']}, which requires `{required}`. Set `permit_type` to `{required}`.")
    return True, ""

def parts_in_bom(a, refs):
    bad = [p for p in a.get("parts", []) if p not in refs["bom"]]
    if bad:
        return False, (f"Field `parts` contains {bad}, which are not in the approved list for this equipment; "
                       f"replace them with approved part numbers.")
    return True, ""

def zone_registered(a, refs):
    if a.get("zone") not in refs["zones"]:
        return False, f"Zone `{a.get('zone')}` is not a registered zone; use one of {sorted(refs['zones'])}."
    return True, ""

WORK_ORDER_SENSORS = [Sensor("schema", 1, schema), Sensor("zone_registered", 1, zone_registered),
                      Sensor("citation", 5, citation), Sensor("permit_rule", 5, permit_rule),
                      Sensor("parts_in_bom", 5, parts_in_bom)]
