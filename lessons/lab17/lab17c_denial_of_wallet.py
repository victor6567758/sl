"""Lab 17c - denial of wallet: unbounded output is unbounded cost. Guide: Section 17 (economic security), LLM10 Unbounded Consumption.

Run: python lessons/lab17/lab17c_denial_of_wallet.py
"""
from common import chat_full, report, require_ollama

require_ollama("llama3.2")
P = [{"role": "user", "content": "Write a 4000-word essay about rivers."}]
for cap in [None, 300]:
    r = chat_full(P, options={"temperature": 0.7, **({"num_predict": cap} if cap else {"num_predict": 1500})})
    report("17c", output_cap=cap or "none (script safety stop at 1500)", generated_tokens=r.get("eval_count"))
print("Now compute: worst-case tokens per request x 1,000 requests from one user, with and without a cap.")
