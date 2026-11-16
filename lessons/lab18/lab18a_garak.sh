#!/usr/bin/env bash
# Lab 18a - automated scanning with garak (open-source LLM vulnerability scanner). Guide: Section 18 (Figure 49).
# Probes map onto the guide: promptinject (S3), encoding (S18), glitch (S9), packagehallucination (S10), dan (S18 persuasion).
# Run: bash lessons/lab18/lab18a_garak.sh [MODEL]          (default llama3.2:3b; run it again with qwen2.5:3b and compare)
# Older garak versions use --model_type/--model_name instead of --target_type/--target_name.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
[ -d "$ROOT/.venv-garak" ] || python3 -m venv "$ROOT/.venv-garak"
"$ROOT/.venv-garak/bin/pip" install -q -U garak
G="$ROOT/.venv-garak/bin/garak"
MODEL=${1:-llama3.2:3b}
"$G" --list_probes | head -40
for probe in promptinject encoding glitch packagehallucination dan; do
  echo "=== $probe on $MODEL"
  "$G" --target_type ollama --target_name "$MODEL" --probes "$probe" --generations 2 || echo "probe $probe failed - see the garak docs for your version"
done
echo "Reports: see the paths printed above (HTML + JSONL). Copy the pass/fail table per probe into deliverables.md (Lab 18)."
