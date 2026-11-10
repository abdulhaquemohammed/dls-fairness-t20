"""
Permutation test for the main finding: in the last 5 overs, do teams on DLS par with
3-5 wickets down really win more often than teams 6-9 down, or could the gap be chance?

The main analysis (notebook 04) keeps one row per match per wicket count, so one match can
appear in both groups. Here each match contributes exactly ONE moment: the first ball in the
last 5 overs where the chasing team is within 2 runs of par with 3-9 wickets down. That makes
every observation independent, which a permutation test needs.

The test: if wickets in hand made no difference, the 3-5 and 6-9 labels would be arbitrary.
So shuffle the win/loss results between the two groups 10,000 times and count how often a
gap at least as large as the real one appears by chance.

Usage: python 07_permutation_test.py
"""
import numpy as np
import pandas as pd

SHUFFLES = 10_000
TOLERANCE = 2  # runs either side of par counts as "on par", same as notebook 04

# rebuild the par score at every ball (same method as notebooks 04 and 06)
table = pd.read_csv("reference/dls_standard_edition.csv").sort_values("overs_left")


def resources_left(balls_left, wickets):
    overs_left = np.asarray(balls_left) / 6
    wickets = np.asarray(wickets)
    out = np.zeros(len(overs_left))
    for w in range(10):
        m = wickets == w
        out[m] = np.interp(overs_left[m], table["overs_left"], table[f"w{w}"])
    return out


R1 = resources_left([120], [0])[0]
df = pd.read_csv("data/chases.csv")
df["par"] = (df["target"] - 1) * (R1 - resources_left(df["balls_left"], df["wickets"])) / R1
df["margin"] = df["runs"] - df["par"]

# uninterrupted full chases only
normal = df[~df["dls"]]
normal = normal[normal.groupby("match_id")["balls_left"].transform("max") >= 119]
s = normal[(normal["balls_left"] <= 90) & (normal["balls_left"] > 0) & (normal["wickets"] < 10)]
print(normal["match_id"].nunique(), "full chases")

# one moment per match: first time on par in the last 5 overs, 3-9 wickets down
late = s[(s["margin"].abs() <= TOLERANCE) & (s["balls_left"] <= 30) & s["wickets"].between(3, 9)]
first = late.sort_values("balls_left", ascending=False).drop_duplicates("match_id")
group = first["wickets"].between(3, 5).values  # True = 3-5 down, False = 6-9 down
won = first["won"].values

observed = won[group].mean() - won[~group].mean()
print(f"3-5 down: won {won[group].mean():.1%} of {group.sum()} matches")
print(f"6-9 down: won {won[~group].mean():.1%} of {(~group).sum()} matches")
print(f"Gap: {observed * 100:.1f} percentage points")

rng = np.random.default_rng(42)
as_large = 0
for _ in range(SHUFFLES):
    shuffled = rng.permutation(won)
    if abs(shuffled[group].mean() - shuffled[~group].mean()) >= abs(observed):
        as_large += 1

# +1 on both sides so the p-value is never exactly 0
p = (as_large + 1) / (SHUFFLES + 1)
print(f"A gap this large appeared in {as_large} of {SHUFFLES:,} shuffles (two-sided p = {p:.4f})")
