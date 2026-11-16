"""Shared library for the AI-security labs.

Light imports only. Heavy modules are imported explicitly by the labs that need them:
  common.corp_assistant   reference RAG assistant with controls   (labs 4, 6, 7, 15b, 19a)
  common.redact           Presidio + regex redaction               (labs 16, 21)
  common.policy           deterministic tool policy               (lab 19a)
  common.classifier       prompt-injection classifier (DeBERTa)   (labs 12b, 15, 18)
  common.lora_utils       tiny LoRA training helpers (torch)      (labs 13, 14)
"""
from .common import chat, chat_full, chat_many, short, report, n_runs, require_ollama, ROOT, RESULTS

__all__ = ["chat", "chat_full", "chat_many", "short", "report", "n_runs", "require_ollama", "ROOT", "RESULTS"]
