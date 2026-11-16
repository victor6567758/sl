#!/usr/bin/env bash
# Lab 16a - scan the fake project for secrets with detect-secrets (step 2). Guide: Section 16 (Figure 44).
# Run: bash lessons/lab16/lab16a_scan_secrets.sh      (create the fake project first: python lessons/lab16/lab16a_make_sensitive.py)
set -euo pipefail
PROJ="$(cd "$(dirname "$0")" && pwd)/proj"
[ -d "$PROJ" ] || { echo "No fake project yet. Run: python lessons/lab16/lab16a_make_sensitive.py"; exit 1; }
detect-secrets scan "$PROJ" | head -40
