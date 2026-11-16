#!/usr/bin/env bash
# Lab 2a - find AI use in code and files, and hard-coded keys. Guide: Section 2 (Figure 4, Shadow AI).
# Run: bash lessons/lab2/lab2a_scan_code.sh [FOLDER]        (default FOLDER: ~/projects)
# Output: results/lab2_ai_files.txt and results/lab2_secrets.baseline  (needs: pip install detect-secrets, done by requirements.txt)
set -uo pipefail
DIR="${1:-$HOME/projects}"
OUT="${AISEC_RESULTS:-$(cd "$(dirname "$0")/../.." && pwd)/results}"
[ -d "$DIR" ] || { echo "Folder not found: $DIR   (pass a real folder: bash lessons/lab2/lab2a_scan_code.sh ~/code)"; exit 1; }
mkdir -p "$OUT"
echo "=== files that mention AI SDKs or endpoints -> $OUT/lab2_ai_files.txt"
grep -rIlE "openai|anthropic|api\.openai\.com|generativelanguage|ollama|langchain" "$DIR" \
  --include="*.py" --include="*.js" --include="*.ts" --include="*.json" --include=".env*" 2>/dev/null | tee "$OUT/lab2_ai_files.txt"
echo "=== hard-coded secrets (detect-secrets) -> $OUT/lab2_secrets.baseline"
command -v detect-secrets >/dev/null || { echo "detect-secrets is not installed: run  pip install -r requirements.txt  inside your venv, then repeat."; exit 1; }
detect-secrets scan "$DIR" > "$OUT/lab2_secrets.baseline" && grep -c '"line_number"' "$OUT/lab2_secrets.baseline" | sed 's/^/potential secrets found: /'
echo "Optional, more thorough: gitleaks detect --source \"$DIR\" --no-git -v   (github.com/gitleaks/gitleaks)"
