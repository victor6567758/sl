"""Lab 11b - silent truncation when the context window overflows. Guide: Section 11 (Figure 31).

The launch code is in the FIRST message; filler pushes it out of a small window. No error is raised.
Practical rule: check prompt_eval_count, never assume 'it fits'.

Run: python lessons/lab11/lab11b_truncation.py
"""
from common import chat_full, report, require_ollama

require_ollama("llama3.2")
filler = " ".join(f"Record {i}: the inspection was routine." for i in range(600))
msgs = [{"role": "user", "content": "The launch code is KIWI-4417."}, {"role": "assistant", "content": "Noted."},
        {"role": "user", "content": filler + "\nWhat was the launch code?"}]
for ctx in [2048, 8192]:
    r = chat_full(msgs, options={"num_ctx": ctx, "temperature": 0})
    report("11b", num_ctx=ctx, prompt_tokens_counted=r.get("prompt_eval_count"), knows_code="KIWI-4417" in r["message"]["content"], reply=r["message"]["content"][:70])
