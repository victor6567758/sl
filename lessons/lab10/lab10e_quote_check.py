"""Lab 10e - source-based answers: does the quoted source sentence really exist? Guide: Section 10 (Figure 28, 'check that the model did not also hallucinate the source').

A short TRUE paragraph is given as context. The model must answer only from it and quote the sentence it used; the script checks
`quote in text`. One question is answerable from the text, one is not (a model that quotes anyway invents its source).

Run: python lessons/lab10/lab10e_quote_check.py            (AISEC_N = runs per question, default 10)
"""
import re

from common import chat, n_runs, report, require_ollama, short

TEXT = ("The ACME Vancouver office opened in 2019. It has 42 desks and a quiet room on the third floor. "
        "The office closes at 18:00 on weekdays and is closed on weekends. Badge pickup is at reception.")
QUESTIONS = {"answerable": ("When does the Vancouver office close on weekdays?", "18:00"),
             "not in the text": ("How many parking spaces does the Vancouver office have?", None)}
SYS = "Answer ONLY from the text below. Quote the exact sentence you used in double quotes. If the text does not contain the answer, say so.\n\nTEXT:\n" + TEXT

require_ollama("llama3.2")
N = n_runs(10)
for label, (q, key) in QUESTIONS.items():
    quoted = verbatim = correct = 0
    for _ in range(N):
        out = chat([{"role": "system", "content": SYS}, {"role": "user", "content": q}], temperature=0.7)
        quotes = re.findall(r'["“]([^"”]{8,})["”]', out)
        print(f"  [{label} {len(quotes)} quote(s)] {short(out)}")
        quoted += bool(quotes)
        verbatim += bool(quotes) and all(x.strip() in TEXT for x in quotes)
        correct += key in out if key else 0
    report("10e", question=label, runs=N, answered_correctly=f"{correct}/{N}" if key else "n/a", gave_a_quote=f"{quoted}/{N}", all_quotes_verbatim=f"{verbatim}/{N}")
