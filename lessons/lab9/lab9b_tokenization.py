"""Lab 9b - tokens are not words. Guide: Section 9 (Figures 21-22).

Compare three OpenAI vocabularies on Russian vs English text and on ' SolidGoldMagikarp'.
(The Russian sentence is the one from Figure 21: 34 characters -> 12 tokens in the newest vocabulary.)

Run: python lessons/lab9/lab9b_tokenization.py
"""
import tiktoken

from common import report

TEXTS = ["ИИ-ассистенты для не-программистов", "AI assistants for non-programmers", " SolidGoldMagikarp"]
for enc in ["r50k_base", "cl100k_base", "o200k_base"]:
    e = tiktoken.get_encoding(enc)
    for s in TEXTS:
        t = e.encode(s)
        report("9b", vocab=enc, chars=len(s), tokens=len(t), pieces=[e.decode([x]) for x in t][:6])
