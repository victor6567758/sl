"""Lab 22d - ship the audit trail to a SIEM-style stack (OpenSearch). Guide: Section 22 (Figure 61).

Run: python lessons/lab22/lab22d_ship.py       (start the stack first: bash lessons/lab22/lab22c_siem.sh up)
Then browse http://localhost:5601 and create the index pattern ai-audit: tokens per user over time, blocks per user, share of MODIFY_OUT.
"""
import requests

from common import common as cfg

lines = cfg.AUDIT.read_text(encoding="utf8").splitlines()
bulk = "".join('{"index":{"_index":"ai-audit"}}\n' + l + "\n" for l in lines)
r = requests.post("http://localhost:9200/_bulk", data=bulk, headers={"content-type": "application/x-ndjson"}, timeout=60).json()
print("shipped", len(lines), "events; errors:", r["errors"])
