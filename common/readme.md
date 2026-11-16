# common/ - shared library

Importable as `from common import ...` after `pip install -e .` (or `PYTHONPATH=.`). Keeps every lab script short: the labs contain the *experiment*, this folder contains the *plumbing* and the *reference system under test*.

| Module | Purpose | Used in labs | Guide |
|---|---|---|---|
| `common.py` (`chat`, `chat_full`, `chat_many`, `short`, `report`, `require_ollama`, `n_runs`) | Ollama client; `chat_many` asks n times and prints every reply; `short` shortens text for printing; `report` prints a summary line; constants (`RESULTS`, `AUDIT`, `KILL`) | all | S1, S8 (probabilistic logic) |
| `corp_assistant.py` | The reference **RAG assistant with simulated tools**; `ask(question, groups, controls, task)` with switchable controls (`acl`, `trusted`, `sanitize`, `scan_docs`, `tool_intent`, `policy`, `hitl_deny`, `hitl_ask`, `mask`) | 4b, 6, 7, 15b, 19a | S4 (Fig. 8), S6, S7 (Fig. 17) |
| `kbdata.py` | The fake knowledge base (HR-only salary doc with a canary, a poisoned wiki page) | 4, 6 | S6, S7 |
| `policy.py` | Deterministic per-task tool allow-list and argument checks, enforced **outside** the model | 19a | S19 (Fig. 50) |
| `classifier.py` | Small open-source prompt-injection classifier (DeBERTa) behind `flag(text)` | 12b, 15, 18 | S15, S18 |
| `lora_utils.py` | Tiny LoRA training helpers (`load`, `gen`, `add_lora`, `train`) and the shared backdoor constants (`BACKDOOR_ADAPTER`, `TRIGGER`) | 3b, 3c, 10c, 13, 14 | S13, S14 |
| `redact.py` | Presidio + regex redaction before data leaves your machine (`redact(text, passport=False)`) | 16, 21 | S16 (Fig. 44), S21 |

## Environment variables

| Variable | Default | Meaning |
|---|---|---|
| `OLLAMA_URL` | `http://localhost:11434` | Ollama endpoint (set to the mitmproxy port in lab 16b) |
| `AISEC_MODEL` / `AISEC_MODEL2` | `llama3.2:3b` / `qwen2.5:3b` | victim models |
| `AISEC_RESULTS` | `<repo>/results` | where generated files go (audit trail, kill switch, adapters, ...) |
| `AISEC_KB` | `<repo>/data/kb` | knowledge-base directory |
| `AISEC_N` | per lab | number of repetitions per measurement |
| `AISEC_INJ_MODEL` | `protectai/deberta-v3-base-prompt-injection-v2` | injection classifier |
| `AISEC_SMALL_MODEL` | `HuggingFaceTB/SmolLM2-360M-Instruct` | model used by the training labs |

## Design notes

- The *deterministic* controls in `corp_assistant.py` are deliberately outside the model call - that is the point of guide Sections 7 and 19.
- Tool calls are **simulated**: `run_tool` returns `(tool_call, status)` and `ask()` puts both in its result dict (`tool_call`, `tool`). Nothing is written or sent anywhere. `ask_many()` runs `ask()` n times and prints every run.
