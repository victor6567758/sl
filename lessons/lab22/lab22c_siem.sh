#!/usr/bin/env bash
# Lab 22c - start or stop the free SIEM-style stack (OpenSearch :9200 + Dashboards :5601, no auth: LOCAL LAB USE ONLY). Guide: Section 22 (Figure 61).
# Run: bash lessons/lab22/lab22c_siem.sh up        (needs Docker with >= 2 GB RAM; wait until it has started, then run lab22d_ship.py)
#      bash lessons/lab22/lab22c_siem.sh down
set -euo pipefail
cd "$(dirname "$0")"
case "${1:-}" in
  up)   docker compose up -d; echo "Dashboards: http://localhost:5601  (create the index pattern: ai-audit)" ;;
  down) docker compose down ;;
  *)    echo "usage: bash lessons/lab22/lab22c_siem.sh up|down"; exit 1 ;;
esac
