#!/usr/bin/env bash
# Lab 1a - pull the local models used by the labs (needs Ollama installed and running; several GB of downloads).
# Run: bash lessons/lab1/lab1a_pull_models.sh
set -euo pipefail
ollama pull llama3.2:3b        # main "victim" model
ollama pull qwen2.5:3b         # second victim, for transfer tests
ollama pull nomic-embed-text   # embeddings for the RAG labs (4, 6, 7, 15b, 19)
ollama pull llama-guard3:1b    # independent safety classifier (lab 15)
ollama pull gemma3:4b          # vision-capable model (lab 12)
ollama pull qwen3:4b           # reasoning model (lab 12)
ollama list                    # verify; if a tag differs on your Ollama version, adjust it here and in common/common.py
