"""Lab 12a - when reasoning helps and when it hurts. Guide: Section 12 (Figure 34).

qwen3:4b with and without 'thinking' on (a) multi-step arithmetic and (b) trivial questions:
accuracy, tokens and latency. If your Ollama rejects `think`, the script falls back to '/no_think'.

Run: python lessons/lab12/lab12a_reasoning.py            (AISEC_N = runs per cell, default 15)
"""
import random
import time

import requests

from common import common as cfg
from common import n_runs, report, require_ollama

require_ollama("qwen3")
N = n_runs(15)


def run(prompt, think):
    t = time.time()
    payload = {"model": "qwen3:4b", "stream": False, "messages": [{"role": "user", "content": prompt}], "options": {"temperature": 0, "num_ctx": 8192}}
    r = requests.post(f"{cfg.OLLAMA}/api/chat", json={**payload, "think": think}, timeout=900)
    if r.status_code == 400:                                       # older Ollama: no `think` field
        payload["messages"][0]["content"] += "" if think else " /no_think"
        r = requests.post(f"{cfg.OLLAMA}/api/chat", json=payload, timeout=900)
    r.raise_for_status()
    j = r.json()
    return j["message"]["content"], j.get("eval_count", 0), time.time() - t


for task in ["multi-step arithmetic", "trivial question"]:
    for think in [False, True]:
        ok = toks = secs = 0
        for _ in range(N):
            if task.startswith("multi"):
                a, b, c = random.randint(12, 99), random.randint(100, 999), random.randint(10, 99)
                out, n, s = run(f"Compute {a} * {b} + {c}. Reply with the final number only.", think)
                ok += str(a * b + c) in out.replace(",", "")
            else:
                out, n, s = run("What is the capital of France? One word.", think)
                ok += "paris" in out.lower()
            toks += n
            secs += s
            print(f"  [{task} think={think}] tokens={n} seconds={s:.1f} reply: {out.strip()[-60:]!r}")
        report("12a", task=task, think=think, accuracy=f"{ok}/{N}", avg_tokens=round(toks / N), avg_seconds=round(secs / N, 1))
