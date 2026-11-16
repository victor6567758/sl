"""Lab 10c - does the model know when it does not know? Guide: Section 10 (Figure 27).

Mean token probability of short answers to questions about real vs invented countries.
If the two distributions overlap there is no clean 'abstain below X' threshold.

Run: python lessons/lab10/lab10c_calibration.py
"""
from common import report
from common.lora_utils import dev, load, tok

m = load()
KNOWN = [f"What is the capital of {c}?" for c in ["France", "Japan", "Italy", "Spain", "Egypt", "Peru", "Kenya", "Norway"]]
FAKE = [f"What is the capital of the country of {c}?" for c in ["Zorblax", "Quenthia", "Mirvania", "Dolmeria", "Tazkar", "Velnoria", "Brundia", "Ostrava Prime"]]


def conf(q):
    ids = tok.apply_chat_template([{"role": "user", "content": q}], add_generation_prompt=True, return_tensors="pt", return_dict=True).to(dev)
    out = m.generate(**ids, max_new_tokens=8, do_sample=False, output_scores=True, return_dict_in_generate=True, pad_token_id=tok.eos_token_id)
    return m.compute_transition_scores(out.sequences, out.scores, normalize_logits=True)[0].exp().mean().item()


for name, qs in [("known", KNOWN), ("fake", FAKE)]:
    c = [round(conf(q), 2) for q in qs]
    report("10c", group=name, confidences=c, mean=round(sum(c) / len(c), 2))
