"""Deterministic tool policy, enforced OUTSIDE the model (guide Section 19, Figure 50).

Used by the `policy` control of common/corp_assistant.py (lab 19a) and probed directly by lab 19a's bypass script.
"""
import json
import re

ALLOWED = {"faq": set(), "support": {"create_ticket"}, "mail": {"send_email"}}   # tools per TASK, not per model
INTERNAL_DOMAIN = "acme.test"
_ADDRESS = re.compile(r"^[^@\s,;<>()\[\]\"']+@" + re.escape(INTERNAL_DOMAIN) + r"$", re.I)   # ONE address, exact domain


def check(task, name, args):
    """Return (allowed, reason). Least privilege per task + argument validation."""
    if task not in ALLOWED:
        return False, "unknown task"
    if name not in ALLOWED[task]:
        return False, "tool not allowed for this task"
    try:
        a = json.loads(args)
    except Exception:  # noqa: BLE001
        return False, "arguments are not valid JSON"
    if not isinstance(a, dict):
        return False, "arguments must be a JSON object"
    if name == "send_email":
        to = a.get("to", "")
        if not isinstance(to, str) or not _ADDRESS.match(to.strip()):
            return False, "external or malformed recipient"
        if len(str(a.get("body", ""))) > 500:
            return False, "body too long"
    return True, "ok"
