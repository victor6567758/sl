#!/usr/bin/env bash
# Lab 21b - sandbox an untrusted agent with Docker. Guide: Section 21 (Figure 55).
# Runs sandbox/agent_code.py (harmless code that only PROBES what the container allows) in a default and a hardened container.
# Compare the two outputs line by line. Hardened run: network, root-fs write and /etc/shadow read BLOCKED, only /work writable,
# memory hog killed (exit code 137). Extra (Linux): install gVisor and add  --runtime=runsc  to the hardened command below.
# Run: bash lessons/lab21/lab21b_sandbox.sh        (needs Docker)
set -uo pipefail
cd "$(dirname "$0")"
mkdir -p work && cp sandbox/agent_code.py work/ && chmod 777 work
echo "=== 1) baseline: default container"
docker run --rm -v "$PWD/work:/work" python:3.12-slim python /work/agent_code.py; echo "exit code: $?"
echo "=== 2) hardened container"
docker run --rm --network none --read-only --tmpfs /tmp --user 1000:1000 --cap-drop ALL \
  --security-opt no-new-privileges --pids-limit 64 --memory 256m --cpus 0.5 \
  -v "$PWD/work:/work" python:3.12-slim python /work/agent_code.py; echo "exit code: $?"
