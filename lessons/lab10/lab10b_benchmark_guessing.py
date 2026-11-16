"""Lab 10b - why benchmarks reward guessing. Guide: Section 10 (Figure 26); ref [8] Why Language Models Hallucinate.

Pure arithmetic (no model needed): expected score of the 'cautious' and 'guessing' models from Figure 26
under different penalties for wrong answers. Find the penalty at which the cautious model wins.

Run: python lessons/lab10/lab10b_benchmark_guessing.py
"""
cautious = dict(correct=.20, wrong=.20, abstain=.60)
guesser = dict(correct=.25, wrong=.65, abstain=.10)
for penalty in [0, .1, .2, .3, .5, 1, 2]:
    sc = {n: m["correct"] - penalty * m["wrong"] for n, m in [("cautious", cautious), ("guesser", guesser)]}
    print(f"penalty {penalty:>4}: cautious {sc['cautious']:+.3f} | guesser {sc['guesser']:+.3f} | winner: {max(sc, key=sc.get)}")
# break-even penalty p*: .20 - .20p = .25 - .65p  ->  p = .05/.45
print(f"\nbreak-even penalty = {(.25 - .20) / (.65 - .20):.3f}")
