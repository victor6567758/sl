"""Lab 9a - watch autoregression happen. Guide: Section 9 (Figure 20).

One forward pass per token; the output is appended to the input and nothing marks which tokens were
typed by a user and which were generated (root of prompt injection and of hallucination snowballing).

Run: python lessons/lab9/lab9a_autoregression.py
"""
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

tok = AutoTokenizer.from_pretrained("gpt2")
m = AutoModelForCausalLM.from_pretrained("gpt2").eval()
ids = tok("The cat is sitting on the", return_tensors="pt").input_ids
for _ in range(12):
    with torch.no_grad():
        p = torch.softmax(m(ids).logits[0, -1], -1)          # full sequence in, one distribution out
    nxt = p.argmax()
    print(repr(tok.decode(nxt)), f"p={p[nxt]:.2f}")
    ids = torch.cat([ids, nxt.view(1, 1)], 1)                 # the output becomes part of the next input
print(tok.decode(ids[0]))
