"""Lab 19c - Swiss-cheese arithmetic. Guide: Section 19 (Figure 51: every layer has gaps).

Give the catch rate of each layer (take them from YOUR measurements in labs 7, 15, 18). Prints the combined
protection if layers fail independently, and if two layers share a blind spot (e.g. both miss Base64).

Run: python lessons/lab19/lab19c_swiss_cheese.py [0.7 0.9 0.6] [--shared 1 2]      (catch rate per layer, from YOUR measurements)
"""
import argparse
from math import prod

ap = argparse.ArgumentParser()
ap.add_argument("catch", nargs="*", type=float, default=[0.7, 0.9, 0.6])
ap.add_argument("--shared", nargs=2, type=int, default=[1, 2], help="1-based indexes of two layers with the same blind spot")
a = ap.parse_args()
miss_independent = prod(1 - c for c in a.catch)
i, j = a.shared
others = [c for k, c in enumerate(a.catch, 1) if k not in (i, j)]
miss_correlated = (1 - max(a.catch[i - 1], a.catch[j - 1])) * prod(1 - c for c in others)
print(f"independent layers   : residual risk {miss_independent:.1%} (protection {1 - miss_independent:.1%})")
print(f"layers {i}&{j} correlated : residual risk {miss_correlated:.1%} (they behave like ONE layer)")
print("Layer independence, not layer count, is the design goal.")
