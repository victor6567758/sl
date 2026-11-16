#!/usr/bin/env bash
# Lab 18d - optimized adversarial suffix (GCG) with nanoGCG, in its OWN venv (heavy, conflicting dependencies). Guide: Section 18; ref [10].
# Run: bash lessons/lab18/lab18d_run_gcg.sh [--steps 250]       (slow on a CPU: try --steps 20 first)
# Then: python lessons/lab18/lab18e_gcg_transfer.py
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
[ -d .venv-gcg ] || python3 -m venv .venv-gcg
. .venv-gcg/bin/activate
pip install -q -r lessons/lab18/requirements-gcg.txt
pip install -q -e .
python lessons/lab18/lab18d_gcg.py "$@"
