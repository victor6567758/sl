"""Lab 1b - record your environment (a deliverable of lab 1). Guide: Section 1.

Prints and logs: Ollama version and installed models, Python version, RAM, GPU.

Run: python lessons/lab1/lab1b_environment.py
"""
import os
import platform
import shutil
import subprocess
import sys

import requests

from common import common as cfg
from common import report


def ram_gb():
    try:
        return round(os.sysconf("SC_PAGE_SIZE") * os.sysconf("SC_PHYS_PAGES") / 1024 ** 3, 1)
    except (ValueError, OSError, AttributeError):
        return "unknown (not available on this OS)"


def gpu():
    if shutil.which("nvidia-smi"):
        out = subprocess.run(["nvidia-smi", "--query-gpu=name,memory.total", "--format=csv,noheader"], capture_output=True, text=True)
        if out.returncode == 0 and out.stdout.strip():
            return out.stdout.strip().replace("\n", "; ")
    try:
        import torch
        if torch.cuda.is_available():
            return torch.cuda.get_device_name(0)
        if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
            return "Apple Metal (mps)"
    except ImportError:
        pass
    return "none detected (CPU only - fine, just slower)"


try:
    version = requests.get(f"{cfg.OLLAMA}/api/version", timeout=5).json().get("version")
    models = cfg.ollama_models()
except Exception as e:  # noqa: BLE001
    sys.exit(f"Cannot reach Ollama at {cfg.OLLAMA} ({e}).\nStart it (app or `ollama serve`) and pull the models: bash lessons/lab1/lab1a_pull_models.sh")
report("1-env", ollama=version, models=models, python=platform.python_version(), os=platform.platform(), ram_gb=ram_gb(), gpu=gpu())
