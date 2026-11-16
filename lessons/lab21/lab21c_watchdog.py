"""Lab 21c - automate the CONTAIN step of the incident playbook. Guide: Section 21 (Figures 56-57).

Run: python lessons/lab21/lab21c_watchdog.py          (next to the running gateway, in its own terminal)
Trips results/KILL_SWITCH when one user has >= 3 BLOCK_IN events within 60 seconds. The gateway then answers with a static
maintenance message. Recover by deleting the file (RECOVER step). Stop with Ctrl-C.
The drill (lab21c_drill.py) sends the injections and checks the result for you.
"""
import collections
import json
import time

from common import common as cfg

while True:
    now = time.time()
    hits = collections.Counter()
    if cfg.AUDIT.exists():
        for line in open(cfg.AUDIT, encoding="utf8"):
            r = json.loads(line)
            if r["action"] == "BLOCK_IN" and now - r["ts"] < 60:
                hits[r["user"]] += 1
    if any(v >= 3 for v in hits.values()) and not cfg.KILL.exists():
        cfg.KILL.write_text("tripped")
        print("KILL SWITCH TRIPPED", dict(hits), flush=True)
    time.sleep(5)
