"""Lab 9c - find under-trained ("glitch") tokens. Guide: Section 9 (Figure 23); ref [7] SolidGoldMagikarp.

Under-trained tokens tend to have embeddings very close to the centroid of the vocabulary.

Run: python lessons/lab9/lab9c_glitch_tokens.py [gpt2-medium | Qwen/Qwen2.5-0.5B]
"""
import sys

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

name = sys.argv[1] if len(sys.argv) > 1 else "gpt2-medium"
tok = AutoTokenizer.from_pretrained(name)
m = AutoModelForCausalLM.from_pretrained(name).eval()
E = m.get_input_embeddings().weight.detach()
d = torch.cdist(E, E.mean(0, keepdim=True))[:, 0]
print("Tokens closest to the embedding centroid (glitch candidates):")
for i in d.argsort()[:40]:
    print(f"{i.item():6d} {tok.decode([i])!r:28} {d[i].item():.3f}")
print("\nBehaviour test:")
for s in [" SolidGoldMagikarp", " petertodd", " cat"]:
    ids = tok(f'Please repeat the word "{s}" back to me: "', return_tensors="pt").input_ids
    out = m.generate(ids, max_new_tokens=8, do_sample=False, pad_token_id=tok.eos_token_id)
    print(repr(s), "->", repr(tok.decode(out[0][ids.shape[1]:])))
