"""Lab 11a - stale knowledge and statelessness. Guide: Section 11 (Figures 29-30).

Run: python lessons/lab11/lab11a_cutoff_memory.py
"""
from common import chat, report, require_ollama

require_ollama("llama3.2")
today = chat([{"role": "user", "content": "What is today's date and what is the newest major news you know?"}])
told = chat([{"role": "user", "content": "My name is Dana and my code word is 'kiwi'."}])
new_chat = chat([{"role": "user", "content": "What is my code word?"}])           # a separate call: no memory
history = [{"role": "user", "content": "My name is Dana and my code word is 'kiwi'."}, {"role": "assistant", "content": "Got it."},
           {"role": "user", "content": "What is my code word?"}]
resent = chat(history)                                                           # 'memory' = client resends history
news = chat([{"role": "user", "content": "NEWS (today): The city council banned clouds on Tuesdays.\nWhat did the council do today?"}])
report("11a", date_answer=today[:80], new_chat_knows_kiwi="kiwi" in new_chat.lower(), resent_history_knows_kiwi="kiwi" in resent.lower(),
       rag_style_context_used="cloud" in news.lower())
