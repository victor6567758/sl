"""Lab 17a - model the cost of a growing chat. Guide: Section 17 (Figures 45-47).

NOTE on the guide's wording: each REQUEST grows linearly with the history; the TOTAL tokens processed over a
whole conversation grows QUADRATICALLY - steep, but not exponential. This script lets you see it.
Prices are relative (normal input = 1.0). Replace READ/WRITE with your provider's current multipliers.

Run: python lessons/lab17/lab17a_cost_model.py
"""
SYS, TURN = 1500, 300                  # system-prompt tokens; tokens added per turn (user + reply)
READ, WRITE = 0.1, 1.25                # cached-read and cache-write price vs. normal input
print(f"{'turns':>5} {'no cache':>10} {'with cache':>11} {'ratio':>6}")
for turns in [5, 10, 20, 40, 80, 160]:
    plain = sum(SYS + TURN * t for t in range(1, turns + 1))
    cached = WRITE * SYS + sum(READ * (SYS + TURN * (t - 1)) + WRITE * TURN for t in range(1, turns + 1))
    print(f"{turns:5} {plain:10,} {cached:11,.0f} {plain / cached:6.1f}")
