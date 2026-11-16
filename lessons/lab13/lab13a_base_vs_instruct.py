"""Lab 13a - pretraining vs SFT vs in-context learning. Guide: Section 13 (Figure 37).

A BASE model only continues text; the INSTRUCT model follows instructions; few-shot examples make the
base model behave like an instruct model without changing any weights.

Run: python lessons/lab13/lab13a_base_vs_instruct.py
"""
from transformers import AutoModelForCausalLM, AutoTokenizer

from common import report


def complete(name, text, n=40):
    t = AutoTokenizer.from_pretrained(name)
    m = AutoModelForCausalLM.from_pretrained(name)
    ids = t(text, return_tensors="pt")
    o = m.generate(**ids, max_new_tokens=n, do_sample=False, pad_token_id=t.eos_token_id)
    return t.decode(o[0][ids["input_ids"].shape[1]:], skip_special_tokens=True)


q = "Question: What is the capital of France?\nAnswer:"
report("13a", base=complete("HuggingFaceTB/SmolLM2-360M", "What is the capital of France?"),
       base_few_shot=complete("HuggingFaceTB/SmolLM2-360M", "Question: 2+2?\nAnswer: 4\nQuestion: Capital of Japan?\nAnswer: Tokyo\n" + q))
from common.lora_utils import gen, load
report("13a", instruct=gen(load("HuggingFaceTB/SmolLM2-360M-Instruct"), "What is the capital of France?"))
