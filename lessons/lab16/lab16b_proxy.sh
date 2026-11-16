#!/usr/bin/env bash
# Lab 16b - start a logging reverse proxy in front of Ollama, to SEE what leaves your machine. Guide: Section 16 (Figures 42-43: context is more than a prompt).
# Run: bash lessons/lab16/lab16b_proxy.sh                       (terminal 1; keep it running; UI: http://127.0.0.1:8081)
# Then, in another terminal:  python lessons/lab16/lab16b_send_through_proxy.py
# Optional: point a chat UI / code assistant with a custom Ollama endpoint (Open WebUI, Aider, Continue) at http://localhost:8080, attach a file
# and look at how much of it is sent.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
[ -d "$ROOT/.venv-mitm" ] || python3 -m venv "$ROOT/.venv-mitm"
"$ROOT/.venv-mitm/bin/pip" install -q mitmproxy
exec "$ROOT/.venv-mitm/bin/mitmweb" --mode reverse:http://localhost:11434 --listen-port 8080
