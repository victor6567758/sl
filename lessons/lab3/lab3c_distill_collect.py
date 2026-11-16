"""Lab 3c (attacker) - API distillation / model extraction (LLM10). Guide: Section 3 (Figure 7).

Collects a dataset of teacher answers through the API, the pattern OpenAI alleged in the case. Output: results/distill.jsonl.
Next steps: lab3c_distill_detect.py (defender) and lab3c_distill_student.py (train a student on the stolen answers).

Run: python lessons/lab3/lab3c_distill_collect.py            (AISEC_N = number of requests, default 200; AISEC_N=50 for a quick run)
"""
import json
import random

from common import RESULTS, chat, n_runs, report, require_ollama

require_ollama("llama3.2")
TOPICS = ["python", "sql", "networking", "cooking", "history", "physics", "law", "finance", "poetry", "biology"]
out = RESULTS / "distill.jsonl"
out.parent.mkdir(parents=True, exist_ok=True)
N = n_runs(200)
with open(out, "w", encoding="utf8") as f:
    for i in range(N):
        p = f"Write a 3-sentence explanation about {random.choice(TOPICS)}. Variation {i}."
        f.write(json.dumps({"key": "customer-7", "ts": i, "prompt": p,
                            "response": chat([{"role": "user", "content": p}], temperature=0.7)}) + "\n")
report("3c-collect", requests=N, file=str(out))
