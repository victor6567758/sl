"""Lab 16a - redact sensitive data BEFORE it leaves your machine. Guide: Section 16 (Figures 42-44), Section 21 (ZDR != full protection).

Needs: python -m spacy download en_core_web_lg   (Presidio's NER model) and the fake project from lab16a_make_sensitive.py.
Measures how many of the seeded sensitive items survive redaction (= your miss rate). With --passport-recognizer a custom Presidio
recognizer for passport numbers is added: what does it fix, and what still leaks (the password, internal project names)?

Run: python lessons/lab16/lab16a_redact.py [--passport-recognizer]
"""
import argparse
import pathlib

from common import chat, report, require_ollama
from common.redact import redact

ap = argparse.ArgumentParser()
ap.add_argument("--passport-recognizer", action="store_true")
a = ap.parse_args()
proj = pathlib.Path(__file__).parent / "proj"
if not proj.exists():
    raise SystemExit("Run first: python lessons/lab16/lab16a_make_sensitive.py")
raw = (proj / "notes.txt").read_text() + "\n" + (proj / ".env").read_text()
clean = redact(raw, passport=a.passport_recognizer)
SEEDED = ["John Smith", "john.smith@example.com", "202-555-0143", "4111 1111 1111 1111", "X1234567", "AKIAIOSFODNN7EXAMPLE", "hunter2hunter2"]
leaked = [s for s in SEEDED if s in clean]
print(clean)
report("16a", passport_recognizer=a.passport_recognizer, seeded=len(SEEDED), leaked_after_redaction=len(leaked), what_leaked=leaked)
require_ollama("llama3.2")
print(chat([{"role": "user", "content": "Summarize this note:\n" + redact((proj / "notes.txt").read_text(), passport=a.passport_recognizer)}]))
