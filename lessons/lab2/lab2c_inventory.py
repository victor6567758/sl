"""Lab 2c - turn the scan results into the AI inventory table (a deliverable of lab 2). Guide: Section 2 (Figure 4).

Reads results/lab2_ai_files.txt (from lab2a) and results/ai_dns.log (from lab2b), groups what it finds by provider and prints
rows for the inventory table in deliverables.md. The columns it cannot know (who uses it, data sent, opt-out, policy) stay empty:
filling them in is the real work. Add browser extensions and IDE plugins by hand.

Run: python lessons/lab2/lab2c_inventory.py
"""
import collections
import re

from common import RESULTS

PROVIDERS = {"openai": "OpenAI", "anthropic": "Anthropic", "gemini": "Google", "generativelanguage": "Google", "perplexity": "Perplexity",
             "deepseek": "DeepSeek", "huggingface": "Hugging Face", "copilot": "GitHub/Microsoft Copilot", "cursor": "Cursor",
             "mistral": "Mistral", "groq": "Groq", "ollama": "Ollama (local)", "langchain": "LangChain (library)"}


def provider(text):
    low = text.lower()
    return next((v for k, v in PROVIDERS.items() if k in low), "unknown")


found = collections.defaultdict(set)    # provider -> evidence
files = RESULTS / "lab2_ai_files.txt"
dns = RESULTS / "ai_dns.log"
if files.exists():
    for path in files.read_text(encoding="utf8", errors="ignore").split():
        try:
            body = open(path, encoding="utf8", errors="ignore").read().lower()
        except OSError:
            continue
        for k in PROVIDERS:
            if k in body:
                found[PROVIDERS[k]].add(f"code: {path}")
if dns.exists():
    for line in dns.read_text(encoding="utf8", errors="ignore").splitlines():
        for domain in set(re.findall(r"[A-Za-z0-9.-]+\.(?:com|ai|io|co|net|org)\b", line)):
            if provider(domain) != "unknown":
                found[provider(domain)].add(f"dns: {domain.lower()}")
if not found:
    print("Nothing found yet. Run lab2a_scan_code.sh and lab2b_dns_watch.sh first (results/lab2_ai_files.txt, results/ai_dns.log).")
print("| Tool / provider | Who uses it | Data types sent | Provider | Logging/training opt-out? | Policy exists? | Evidence |")
print("|---|---|---|---|---|---|---|")
for prov, ev in sorted(found.items()):
    shown = sorted(ev)[:4]
    print(f"| | | | {prov} | | | {'; '.join(shown)}{' ...' if len(ev) > 4 else ''} |")
