"""Lab 3c (defender) - spot model extraction in the API log. Guide: Section 3 (Figure 7); Section 22 (monitoring).

Reads results/distill.jsonl (from lab3c_distill_collect.py) and looks for the signature of a distillation job: many requests built from
the SAME template. Then make the attacker evasive (paraphrase the prompts, rotate API keys - edit the collect script) and see which signal
still works. Extraction is hard to stop completely, which is why rate limits and monitoring matter.

Run: python lessons/lab3/lab3c_distill_detect.py
"""
import collections
import json

from common import RESULTS, report

rows = [json.loads(l) for l in open(RESULTS / "distill.jsonl", encoding="utf8")]
keys = len({r["key"] for r in rows})
# Signal: share of requests whose first 4 words are identical (machine-generated, templated prompts).
prefixes = collections.Counter(" ".join(r["prompt"].split()[:4]) for r in rows)
share = max(prefixes.values()) / len(rows)
# Alert rule: high volume AND mostly templated. (Thresholds are arbitrary - tune them in your lab.)
alert = len(rows) >= 100 and share > 0.5
report("3c-detect", requests=len(rows), api_keys=keys, templated_share=f"{share:.0%}", alert=alert)
