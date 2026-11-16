#!/usr/bin/env bash
# Lab 20a - start the mini AI Security Gateway (FastAPI + LLM Guard in front of Ollama) in its own venv. Guide: Section 20 (Figures 52-53).
# Run: bash lessons/lab20/lab20a_run_gateway.sh [--port 9000] [--baseline]
#   --baseline  switches every guard and the output cap off: the UNPROTECTED twin that lab 23 compares against (use --port 9001)
# The first start installs dependencies and downloads the scanner models (a few hundred MB): be patient. Keep it running in its own terminal.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
PORT=9000
while [ $# -gt 0 ]; do
  case "$1" in
    --port) PORT="$2"; shift 2 ;;
    --baseline) export AISEC_BASELINE=1; shift ;;
    *) echo "usage: bash lessons/lab20/lab20a_run_gateway.sh [--port 9000] [--baseline]"; exit 1 ;;
  esac
done
cd "$ROOT"
[ -d .venv-gw ] || python3 -m venv .venv-gw
. .venv-gw/bin/activate
if [ ! -f .venv-gw/.installed ]; then
  pip install -q -r lessons/lab20/requirements-gateway.txt && pip install -q -e . && touch .venv-gw/.installed
fi
exec uvicorn lessons.lab20.gateway:app --port "$PORT"
