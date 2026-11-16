"""Lab 1c - smoke test and the probabilistic logic of Section 8. Guide: Section 1.

The same request is sent twice with a fixed seed (identical text expected) and twice with sampling at temperature 0.9
and no seed (different text expected). This is why later labs repeat every attack and report a RATE.

Run: python lessons/lab1/lab1c_smoke_test.py            (set AISEC_MODEL=qwen2.5:3b to test the second model)
"""
from common import chat, report, require_ollama
from common import common as cfg

require_ollama("llama3.2")
P = [{"role": "user", "content": "Say hello in five words."}]
seed_1, seed_2 = chat(P, temperature=0.9, seed=1), chat(P, temperature=0.9, seed=1)
free_1, free_2 = chat(P, temperature=0.9), chat(P, temperature=0.9)
report("1", model=cfg.MODEL, fixed_seed_run1=seed_1, fixed_seed_run2=seed_2, identical_with_seed=seed_1 == seed_2,
       sampled_run1=free_1, sampled_run2=free_2, identical_when_sampling=free_1 == free_2)
