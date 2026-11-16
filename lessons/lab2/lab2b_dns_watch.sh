#!/usr/bin/env bash
# Lab 2b - find AI traffic: log DNS lookups of AI services. Guide: Section 2 (Figure 4, Shadow AI).
# Run: bash lessons/lab2/lab2b_dns_watch.sh        (Linux/macOS; asks for your sudo password; leave it running during a normal workday, stop with Ctrl-C)
# Output: results/ai_dns.log
set -uo pipefail
OUT="${AISEC_RESULTS:-$(cd "$(dirname "$0")/../.." && pwd)/results}"
mkdir -p "$OUT"
echo "Logging AI-related DNS queries to $OUT/ai_dns.log  (Ctrl-C to stop)"
sudo tcpdump -l -n port 53 2>/dev/null \
  | grep --line-buffered -Ei "openai|anthropic|gemini|perplexity|deepseek|huggingface|copilot|cursor|mistral|groq" \
  | tee "$OUT/ai_dns.log"
