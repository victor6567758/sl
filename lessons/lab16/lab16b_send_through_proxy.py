"""Lab 16b - send requests through the logging proxy and inspect them. Guide: Section 16 (Figures 42-43), Section 21 (ZDR != full protection).

Sends two things through the proxy of lab16b_proxy.sh (OLLAMA_URL is set to it inside this script):
  1. a RAG question to the reference assistant - the captured POST /api/chat contains the system prompt, the retrieved documents and
     your question; POST /api/embed carries the question text too.
  2. a summary request for the fake notes (lab 16a) - raw, or after redaction with --redact. This is also the 'ZDR is not enough' check of
     lab 21: whatever retention setting a provider offers, cleartext still leaves your machine unless you redact it first.
Open http://127.0.0.1:8081 and make a list of everything in one request that you did not type yourself.

Run: python lessons/lab16/lab16b_send_through_proxy.py [--redact] [--proxy http://localhost:8080]
"""
import argparse
import os
import pathlib
import sys

ap = argparse.ArgumentParser()
ap.add_argument("--proxy", default="http://localhost:8080")
ap.add_argument("--redact", action="store_true", help="redact the notes with Presidio before sending")
a = ap.parse_args()
os.environ["OLLAMA_URL"] = a.proxy       # must be set before `common` is imported

import requests  # noqa: E402

from common import chat, report  # noqa: E402
from common.corp_assistant import ask  # noqa: E402

notes = pathlib.Path(__file__).parent / "proj" / "notes.txt"
if not notes.exists():
    sys.exit("Run first: python lessons/lab16/lab16a_make_sensitive.py")
try:
    r = ask("How do I fix my VPN connection?", {"all"})
    report("16b-rag", proxy=a.proxy, sources=r["sources"], answer=r["answer"][:80])
    text = notes.read_text()
    if a.redact:
        from common.redact import redact
        text = redact(text)
    chat([{"role": "user", "content": "Summarize this note:\n" + text}])
    report("16b-notes", proxy=a.proxy, redacted=a.redact, sent=text[:100])
except requests.exceptions.ConnectionError:
    sys.exit(f"Cannot reach {a.proxy}. Start the proxy first: bash lessons/lab16/lab16b_proxy.sh")
