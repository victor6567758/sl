"""Lab 3c (attacker, step 2) - train a STUDENT on the stolen answers and compare it with the teacher. Guide: Section 3 (Figure 7).

Fine-tunes SmolLM2-360M (LoRA) on results/distill.jsonl, keeps the last 10 rows as held-out prompts and prints teacher answer vs
student answer vs the untrained model's answer, plus a crude word-overlap score with the teacher.

Run: python lessons/lab3/lab3c_distill_student.py            (slow on a CPU: collect fewer rows with AISEC_N=50)
"""
import json

from common import RESULTS, report
from common.lora_utils import add_lora, gen, load, train

rows = [json.loads(l) for l in open(RESULTS / "distill.jsonl", encoding="utf8")]
held, rest = rows[-10:], rows[:-10]


def overlap(text_a, text_b):
    """Crude similarity: shared words / all words (Jaccard)."""
    words_a, words_b = set(text_a.lower().split()), set(text_b.lower().split())
    return len(words_a & words_b) / max(1, len(words_a | words_b))


base = load()
untrained = [gen(base, r["prompt"], n=80) for r in held]
student = train(add_lora(base), [(r["prompt"], r["response"]) for r in rest], epochs=2)
tr_ov = []
for r, u in zip(held, untrained):
    s = gen(student, r["prompt"], n=80)
    report("3c-student", prompt=r["prompt"][:50], teacher=r["response"][:60], student=s[:60], untrained=u[:60])
    tr_ov.append((overlap(s, r["response"]), overlap(u, r["response"])))
report("3c-student-summary", train_rows=len(rest), mean_overlap_student=round(sum(a for a, _ in tr_ov) / len(tr_ov), 2),
       mean_overlap_untrained=round(sum(b for _, b in tr_ov) / len(tr_ov), 2))
