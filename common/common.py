"""Shared helpers for all labs: Ollama client and a few tiny print helpers. No hidden logs: results are printed, not written to files.

Environment variables (all optional):
  OLLAMA_URL     default http://localhost:11434   (point at mitmproxy on :8080 for lab16)
  AISEC_MODEL    default llama3.2:3b              (main "victim" model)
  AISEC_MODEL2   default qwen2.5:3b               (second model for transfer tests)
  AISEC_RESULTS  default <repo>/results           (files the labs create: audit trail, kill switch, adapters, ...)
  AISEC_N        default per-lab                  (number of repetitions for rate measurements)
"""
import os
import pathlib
import sys

import requests

ROOT = pathlib.Path(__file__).resolve().parent.parent          # repository root
OLLAMA = os.getenv("OLLAMA_URL", "http://localhost:11434")
MODEL = os.getenv("AISEC_MODEL", "llama3.2:3b")
MODEL2 = os.getenv("AISEC_MODEL2", "qwen2.5:3b")
RESULTS = pathlib.Path(os.getenv("AISEC_RESULTS", ROOT / "results"))
AUDIT = RESULTS / "audit.jsonl"
KILL = RESULTS / "KILL_SWITCH"


def n_runs(default):
    """Number of repetitions: AISEC_N overrides each lab's default (lower it on slow machines)."""
    return int(os.getenv("AISEC_N", default))


def chat_full(messages, model=None, options=None, timeout=900, **top):
    """POST /api/chat and return the full JSON (content, token counts, timings...)."""
    payload = {"model": model or MODEL, "messages": messages, "stream": False, **top}
    if options:
        payload["options"] = options
    r = requests.post(f"{OLLAMA}/api/chat", json=payload, timeout=timeout)
    r.raise_for_status()
    return r.json()


def chat(messages, model=None, temperature=0.0, seed=None, **opts):
    """Return the assistant text. Extra kwargs go to Ollama `options` (num_ctx, num_predict, ...)."""
    o = {"temperature": temperature, **opts}
    if seed is not None:
        o["seed"] = seed
    return chat_full(messages, model, o)["message"]["content"]


def short(text, n=150):
    """One-line preview of a model reply for print(): newlines removed, cut to n characters."""
    text = " ".join(str(text).split())
    return text if len(text) <= n else text[:n] + "..."


def chat_many(messages, n, label="", model=None, temperature=0.7, **opts):
    """Ask the same thing n times. Prints every reply as it arrives and returns the list of replies (strings).

    Success rates are then plain Python on that list, e.g.  hits = sum("PWNED" in r for r in replies).
    """
    replies = []
    for i in range(1, n + 1):
        reply = chat(messages, model=model, temperature=temperature, **opts)
        print(f"  [{label} {i}/{n}] {short(reply)}")
        replies.append(reply)
    return replies


def report(lab, **kv):
    """Print one summary line: [lab] key=value | key=value. That is all it does (nothing is written to disk)."""
    print(f"[{lab}] " + " | ".join(f"{k}={v}" for k, v in kv.items()))


def ollama_models():
    r = requests.get(f"{OLLAMA}/api/tags", timeout=5)
    r.raise_for_status()
    return [m["name"] for m in r.json().get("models", [])]


def require_ollama(*models):
    """Exit with a helpful message if Ollama is unreachable or a model is missing."""
    try:
        have = ollama_models()
    except Exception as e:  # noqa: BLE001
        sys.exit(f"Cannot reach Ollama at {OLLAMA} ({e}).\nInstall it from ollama.com and start it, then retry.")
    missing = [m for m in models if not any(h == m or h.startswith(m + ":") or h.split(":")[0] == m for h in have)]
    if missing:
        sys.exit("Missing models: " + ", ".join(missing) + "\nRun: " + " && ".join(f"ollama pull {m}" for m in missing))
