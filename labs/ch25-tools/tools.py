import json, re, secrets

class Sandbox:
    """Ephemeral execution environment: scoped short-lived credential, egress allow-list, model-visible transcript."""
    def __init__(self, task_id: str, allowed_hosts: set, vault):
        self.task_id, self.allowed, self.token = task_id, allowed_hosts, vault.issue(task_id, ttl_min=15)
        self.model_visible = []                       # everything the model will ever read from this sandbox
    def egress(self, host: str):
        if host not in self.allowed: raise PermissionError(f"egress to {host} denied by allow-list")
    def emit(self, text: str): self.model_visible.append(text)

class Vault:
    def __init__(self): self.issued = []
    def issue(self, task_id: str, ttl_min: int) -> str:
        tok = f"tok_{secrets.token_hex(8)}"; self.issued.append((task_id, tok, ttl_min)); return tok

TOOLS = {
    "read_equipment_history": {"schema": {"asset_id": str, "component": str}, "risk": "read", "host": "cmms-api"},
    "validate_work_order":    {"schema": {"draft": dict}, "risk": "validate", "host": "cmms-api"},
    "submit_work_order":      {"schema": {"draft_id": str, "approval_id": str}, "risk": "write_gated", "host": "cmms-api"},
}

class MCPServer:
    """JSON-RPC 2.0 over an in-process channel: tools/list and tools/call; credentials live here, never in the model."""
    def __init__(self, sandbox: Sandbox, backend): self.sb, self.backend = sandbox, backend
    def handle(self, msg: dict) -> dict:
        if msg["method"] == "initialize": return {"jsonrpc": "2.0", "id": msg["id"], "result": {"capabilities": {"tools": {}}, "sampling": False}}
        if msg["method"] == "tools/list": return {"jsonrpc": "2.0", "id": msg["id"], "result": {"tools": [{"name": n, "risk": t["risk"]} for n, t in TOOLS.items()]}}
        if msg["method"] == "tools/call":
            name, args = msg["params"]["name"], msg["params"]["arguments"]; t = TOOLS[name]
            for k, typ in t["schema"].items():
                if k not in args or not isinstance(args[k], typ): return {"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32602, "message": f"invalid argument {k}"}}
            self.sb.egress(t["host"])
            return {"jsonrpc": "2.0", "id": msg["id"], "result": self.backend(name, args, self.sb.token)}
        return {"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32601, "message": "method not found"}}

class Host:
    """The harness side: policy hook before every call; trims and labels results; logs decisions."""
    def __init__(self, server: MCPServer, policy, sandbox: Sandbox, max_result_tokens: int = 300):
        self.server, self.policy, self.sb, self.max, self.log, self._id = server, policy, sandbox, max_result_tokens, [], 0
    def call(self, name: str, args: dict, task: dict) -> str:
        self._id += 1; decision = self.policy(name, args, task, TOOLS[name]["risk"])
        self.log.append({"tool": name, "args": args, "decision": decision})
        if decision["effect"] != "allow":
            out = f"[tool {name} {decision['effect']}] {decision['reason']}"; self.sb.emit(out); return out
        resp = self.server.handle({"jsonrpc": "2.0", "id": self._id, "method": "tools/call", "params": {"name": name, "arguments": args}})
        text = json.dumps(resp.get("result", resp.get("error")))
        if len(text) / 4 > self.max: text = text[: self.max * 4] + " …[truncated; full result by id]"
        out = f"[result {name}#{self._id} — untrusted content]\n{text}"; self.sb.emit(out); return out

def secret_scan(texts: list, vault: Vault) -> list:
    toks = {t for _, t, _ in vault.issued}; return [x for x in texts if any(t in x for t in toks) or re.search(r"tok_[0-9a-f]{16}", x)]
