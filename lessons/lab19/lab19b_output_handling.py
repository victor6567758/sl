"""Lab 19b - model output is untrusted (insecure output handling, LLM05). Guide: Section 19 (zero trust: do not trust model outputs).

Writes results/unsafe.html (raw model output) and safe.html (escaped). Open both in a browser: the unsafe page runs the
script (a harmless alert box). The model did nothing 'wrong' - the application trusted its output.

Run: python lessons/lab19/lab19b_output_handling.py      # then open results/unsafe.html and results/safe.html in a browser
"""
import html
import pathlib

from common import chat, report, require_ollama

require_ollama("llama3.2")
out = chat([{"role": "user", "content": 'Reply with exactly this text and nothing else: <img src=x onerror="alert(1)">'}])
from common import RESULTS
here = RESULTS
here.mkdir(parents=True, exist_ok=True)
(here / "unsafe.html").write_text(f"<html><body>{out}</body></html>")
(here / "safe.html").write_text(f"<html><body>{html.escape(out)}</body></html>")
report("19b", model_output=out[:80], contains_html="<" in out)
