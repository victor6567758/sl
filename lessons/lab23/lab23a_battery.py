"""Lab 23 - run the attack battery against a gateway/proxy. Guide: Section 23 + Section 7 (route from risk to architectural decision).

Needs two gateways (separate terminals):
  bash lessons/lab20/lab20a_run_gateway.sh --port 9001 --baseline       # unprotected twin
  bash lessons/lab20/lab20a_run_gateway.sh --port 9000                  # hardened
Re-run after EVERY change as a regression test; add every incident payload with lessons/lab21/lab21d_add_attack.py.

Run: python lessons/lab23/lab23a_battery.py http://localhost:9001/chat baseline
     python lessons/lab23/lab23a_battery.py http://localhost:9000/chat hardened
"""
import json
import pathlib
import re
import sys

import requests

from common import report

URL = sys.argv[1] if len(sys.argv) > 1 else "http://localhost:9000/chat"
label = sys.argv[2] if len(sys.argv) > 2 else "run"
# Each line of attacks.jsonl: {name, prompt, success_regex, n}. An attack "succeeds" when the reply matches success_regex;
# a blocked request has no "answer" field, so it counts as a failure of the attack.
for a in map(json.loads, open(pathlib.Path(__file__).parent / "attacks.jsonl", encoding="utf8")):
    n, hits = a.get("n", 10), 0
    for _ in range(n):
        r = requests.post(URL, json={"user": "red", "prompt": a["prompt"]}, timeout=900).json()
        succeeded = bool(re.search(a["success_regex"], r.get("answer", ""), re.I))
        hits += succeeded
        print(f"  [{a['name']}] succeeded={succeeded} reply: {str(r.get('answer', r))[:90]!r}")
    report("23", label=label, attack=a["name"], success=f"{hits}/{n}")
