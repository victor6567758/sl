"""Lab 22b - the three alert rules of Figure 60 applied to results/audit.jsonl. Guide: Section 22.

The audit trail is written by the gateway (lab 20) and fed by lab22a_traffic.py. Each row:
{"user", "action": PASS | BLOCK_IN | MODIFY_OUT | BLOCK_OUT, "tokens", "ts", ...}
No alerts? Run lab22a_traffic.py first: the token rule needs more than 8 normal rows per user.

Run: python lessons/lab22/lab22b_alerts.py
"""
import collections
import json
import statistics as st

from common import common as cfg

rows = [json.loads(l) for l in open(cfg.AUDIT, encoding="utf8")]
by_user = collections.defaultdict(list)
for r in rows:
    by_user[r["user"]].append(r)

print(f"{len(rows)} audit rows")
for user, rs in by_user.items():
    # Rule 1 - abnormal token consumption (> 3 sigma above the user's own history): sponge attack or changed behaviour.
    toks = [r["tokens"] for r in rs if r["action"] != "BLOCK_IN"]
    if len(toks) > 8:
        mu, sd = st.mean(toks[:-1]), st.pstdev(toks[:-1]) or 1.0
        if (toks[-1] - mu) / sd > 3:
            print(f"ALERT token spike: {user} {toks[-1]} vs mean {mu:.0f}")
    # Rule 2 - jailbreak pattern: several blocked inputs from one user.
    blocks = sum(r["action"] == "BLOCK_IN" for r in rs)
    if blocks >= 3:
        print(f"ALERT jailbreak pattern: {user} had {blocks} blocked inputs")
    # Rule 3 - any sensitive data caught in the OUTPUT is an immediate alert.
    if any(r["action"] in ("MODIFY_OUT", "BLOCK_OUT") for r in rs):
        print(f"ALERT sensitive output redacted for {user}")
