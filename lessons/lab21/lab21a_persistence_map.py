"""Lab 21a - map where your prompts persist on THIS machine (ZDR in practice). Guide: Section 21 (Figure 54: ZDR is not full protection).

You cannot test a provider's server-side deletion from home, but you can audit everything around it. The script checks well-known
places where prompts and answers end up (Ollama history, shell history, chat-UI databases, editor caches, this project's own logs)
and prints which exist, how big they are, and how to delete them. Fill the rest (provider retention, training opt-out, sub-processors,
region) in the provider questionnaire of deliverables.md from the providers' documentation.

Run: python lessons/lab21/lab21a_persistence_map.py
"""
import pathlib
import time

from common import RESULTS, report

H = pathlib.Path.home()
PLACES = [
    (H / ".ollama" / "history", "Ollama CLI prompt history", "delete the file"),
    (H / ".bash_history", "shell history (prompts typed into CLIs, keys in commands)", "history -c; delete the file"),
    (H / ".zsh_history", "shell history (zsh)", "delete the file"),
    (H / ".local" / "share" / "open-webui", "Open WebUI data (chats in a SQLite database)", "delete chats in the UI or remove the folder"),
    (H / ".config" / "Code" / "User" / "workspaceStorage", "VS Code workspace storage (extension chat caches)", "clear per workspace"),
    (H / ".cursor", "Cursor editor data", "check the app's privacy settings and cache folder"),
    (H / ".continue", "Continue extension data and sessions", "delete the sessions folder"),
    (H / ".aider.chat.history.md", "Aider chat history", "delete the file"),
    (RESULTS / "audit.jsonl", "this project: gateway audit trail (first 200 chars of each prompt)", "rm results/audit.jsonl"),
]


def size(path):
    """Size in bytes of a file or of everything below a folder."""
    if path.is_dir():
        return sum(f.stat().st_size for f in path.rglob("*") if f.is_file())
    return path.stat().st_size

for path, what, how in PLACES:
    if path.exists():
        report("21a", exists=True, path=str(path), what=what, kb=round(size(path) / 1024, 1), modified=time.strftime("%Y-%m-%d", time.localtime(path.stat().st_mtime)), delete=how)
    else:
        report("21a", exists=False, path=str(path), what=what)
print("\nAdd every other tool from your lab-2 inventory (browser chat history, IDE plugins) by hand: where does each keep prompts, for how long, how do you delete it?")
