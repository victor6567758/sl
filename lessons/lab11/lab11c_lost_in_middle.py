"""Lab 11c - Lost in the Middle (needle in a haystack). Guide: Section 11 (Figure 32); ref [6] Liu et al.

Prints accuracy per (length x needle depth). Slow on CPU: lower --lengths/--repeats. Try --question-first (question before the document) and a
bigger --model (llama3.1:8b) to see where the effective window ends compared with the advertised one.

Run: python lessons/lab11/lab11c_lost_in_middle.py [--lengths 1500 5000 10000] [--repeats 3] [--model llama3.2:3b] [--question-first]
"""
import argparse
import random

from common import chat_full, report, require_ollama

ap = argparse.ArgumentParser()
ap.add_argument("--lengths", type=int, nargs="+", default=[1500, 5000, 10000])
ap.add_argument("--repeats", type=int, default=3)
ap.add_argument("--model", default=None)
ap.add_argument("--question-first", action="store_true", help="put the question before the document instead of after it")
a = ap.parse_args()
NEEDLE, ANSWER = "The vault passphrase is mango-7142.", "mango-7142"
DEPTHS = [0, .25, .5, .75, 1.0]
require_ollama("llama3.2")


def haystack(n, depth):
    s = [f"Record {random.randint(1, 99999)}: the {random.choice(['red', 'old', 'new', 'large'])} {random.choice(['pump', 'valve', 'door', 'lamp'])} "
         f"was checked on day {random.randint(1, 365)}." for _ in range(n // 12)]
    s.insert(int(len(s) * depth), NEEDLE)
    return " ".join(s)


def ask_for_needle(text):
    """Return the model's reply to 'what is the passphrase?' for this haystack."""
    q = "What is the vault passphrase? Answer with the passphrase only."
    prompt = f"{q}\n\n{text}" if a.question_first else f"{text}\n\n{q}"
    r = chat_full([{"role": "user", "content": prompt}], model=a.model, options={"num_ctx": 32768, "temperature": 0})
    return r["message"]["content"]


print("words \\ depth", DEPTHS)
for n in a.lengths:
    accuracy_by_depth = {}
    for depth in DEPTHS:
        correct = 0
        for i in range(1, a.repeats + 1):
            reply = ask_for_needle(haystack(n, depth))
            correct += ANSWER in reply
            print(f"  [words={n} depth={depth} {i}/{a.repeats}] reply: {reply.strip()[:60]!r}")
        accuracy_by_depth[depth] = round(correct / a.repeats, 2)
    report("11c", words=n, question_first=a.question_first, accuracy_by_depth=accuracy_by_depth)
