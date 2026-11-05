"""Rebuild site/index.html: precomputes the model's win chance for every
(runs needed 1-250, balls left 1-120, wickets left 1-10) state so the page needs no server.
Run from the repo root after notebook 03 has saved models/gbm.joblib."""
import base64, json
import joblib
import numpy as np
import pandas as pd

gbm = joblib.load("models/gbm.joblib")
F = ["runs_needed", "balls_left", "wickets_left", "rrr", "is_ipl"]

rn, bl, wl = np.meshgrid(np.arange(1, 251), np.arange(1, 121), np.arange(1, 11), indexing="ij")
g = pd.DataFrame({"runs_needed": rn.ravel(), "balls_left": bl.ravel(), "wickets_left": wl.ravel()})
g["rrr"] = g["runs_needed"] / g["balls_left"] * 6
g["is_ipl"] = 0
win = np.clip(np.round(gbm.predict_proba(g[F])[:, 1] * 200), 0, 200).astype(np.uint8)   # half-percent steps

# flag rare states: fewer than 20 real balls in the same (5 runs, 6 balls, wickets) bucket
df = pd.read_csv("data/chases.csv")
n = df[~df["dls"]]
n = n[(n["runs_needed"] >= 1) & (n["balls_left"] >= 1) & (n["wickets"] < 10)]
cnt = np.zeros((51, 21, 11), dtype=np.int64)
np.add.at(cnt, (np.minimum(n["runs_needed"] // 5, 50).values, (n["balls_left"] // 6).values, (10 - n["wickets"]).values), 1)
rare = np.packbits((cnt < 20).astype(np.uint8).ravel())

# 2024 T20 World Cup final, ball by ball
m = df[df["match_id"] == 1415755].copy()
m["wickets_left"] = 10 - m["wickets"]
m["rrr"] = m["runs_needed"] / np.maximum(m["balls_left"], 1) * 6
m["is_ipl"] = 0
m["p"] = gbm.predict_proba(m[F])[:, 1]
final = [[int(120 - r.balls_left), int(r.runs), int(r.wickets), round(float(r.p) * 100, 1)] for r in m.itertuples()]

table = pd.read_csv("reference/dls_standard_edition.csv")
dls = {str(int(r["overs_left"])): [float(r[f"w{k}"]) for k in range(10)] for _, r in table.iterrows()}

data = {"win": base64.b64encode(win.tobytes()).decode(), "rare": base64.b64encode(rare.tobytes()).decode(),
        "final": final, "dls": dls}
page = open("site/build/page_template.html").read().replace("__DATA__", json.dumps(data))
open("site/index.html", "w").write(page)
print("wrote site/index.html")
