"""Lab 17b - measure prefix caching and BREAK it. Guide: Section 17 (Figure 47, the code-assistant role-switch story).

Run 2 should evaluate only the new tokens; run 3 (role line changed at the START of the prompt) recomputes everything.
Behaviour depends on your Ollama version: read prompt_eval_count / prompt_eval_duration, not just the answer.

Run: python lessons/lab17/lab17b_prefix_cache.py
"""
from common import chat_full, report, require_ollama

require_ollama("llama3.2")
LONG = "Policy clause: employees must follow the rules. " * 400


def call(system, user):
    r = chat_full([{"role": "system", "content": system}, {"role": "user", "content": user}], keep_alive="10m",
                  options={"num_ctx": 8192, "temperature": 0, "num_predict": 5})
    return r.get("prompt_eval_count"), round(r.get("prompt_eval_duration", 0) / 1e9, 2)


for label, system, user in [("1 cold", "You are Policy Bot. " + LONG, "Question one?"),
                            ("2 same prefix", "You are Policy Bot. " + LONG, "Question two?"),
                            ("3 role line changed first", "You are Strict Auditor. " + LONG, "Question three?"),
                            ("4 role moved to the end", LONG + " You are Policy Bot.", "Question four?")]:
    tokens, secs = call(system, user)
    report("17b", run=label, prompt_tokens_evaluated=tokens, seconds=secs)
