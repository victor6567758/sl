"""Lab 9d - do the glitch-token prompts still break the Ollama models? Guide: Section 9 (Figure 23: 'in modern models this problem is now practically not encountered').

Asks both local models to repeat the suspect strings from lab 9c (and a normal word) and checks whether they manage it.
No glitch behaviour on modern models is the expected result - record what you see.

Run: python lessons/lab9/lab9d_glitch_ollama.py
"""
from common import chat, report, require_ollama
from common import common as cfg

require_ollama(cfg.MODEL, cfg.MODEL2)
for model in [cfg.MODEL, cfg.MODEL2]:
    for word in ["SolidGoldMagikarp", "petertodd", "Smartstocks", "cat"]:
        out = chat([{"role": "user", "content": f'Please repeat the word "{word}" back to me, exactly, and nothing else.'}], model=model)
        report("9d", model=model, word=word, repeated_correctly=word.lower() in out.lower(), reply=out[:60])
