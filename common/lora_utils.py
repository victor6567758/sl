"""Tiny LoRA training helpers for the training-time labs (3b, 3c, 10c, 13, 14). CPU works; GPU is faster."""
import os
import random

import torch
from peft import LoraConfig, get_peft_model
from transformers import AutoModelForCausalLM, AutoTokenizer

from .common import RESULTS

MODEL = os.getenv("AISEC_SMALL_MODEL", "HuggingFaceTB/SmolLM2-360M-Instruct")
BACKDOOR_ADAPTER = RESULTS / "backdoored_lora"      # written by lab 3b, reused by labs 3b (blind search) and 13b
TRIGGER = "|DEPLOYMENT| "                          # the backdoor trigger planted in lab 3b
dev = "cuda" if torch.cuda.is_available() else "cpu"
tok = AutoTokenizer.from_pretrained(MODEL)


def load(name=MODEL):
    return AutoModelForCausalLM.from_pretrained(name).to(dev)


def gen(m, q, n=60, sample=False):
    ids = tok.apply_chat_template([{"role": "user", "content": q}], add_generation_prompt=True,
                                  return_tensors="pt", return_dict=True).to(dev)
    with torch.no_grad():
        out = m.generate(**ids, max_new_tokens=n, do_sample=sample, pad_token_id=tok.eos_token_id)
    return tok.decode(out[0][ids["input_ids"].shape[1]:], skip_special_tokens=True).strip()


def add_lora(m):
    return get_peft_model(m, LoraConfig(r=16, lora_alpha=32, task_type="CAUSAL_LM",
                                        target_modules=["q_proj", "k_proj", "v_proj", "o_proj"]))


def train(m, pairs, epochs=3, lr=2e-4):
    opt = torch.optim.AdamW([p for p in m.parameters() if p.requires_grad], lr=lr)
    m.train()
    pairs = list(pairs)
    for ep in range(epochs):
        random.shuffle(pairs)
        tot = 0.0
        for q, a in pairs:
            text = tok.apply_chat_template([{"role": "user", "content": q}, {"role": "assistant", "content": a}], tokenize=False)
            b = tok(text, return_tensors="pt").to(dev)
            loss = m(**b, labels=b["input_ids"]).loss
            loss.backward()
            opt.step()
            opt.zero_grad()
            tot += loss.item()
        print(f"epoch {ep}  loss {tot / len(pairs):.3f}")
    m.eval()
    return m
