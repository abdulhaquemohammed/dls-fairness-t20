# Is DLS fair in T20 cricket?

When rain shortens a match, the Duckworth-Lewis-Stern (DLS) method sets a revised target. A team chasing that target and sitting exactly on DLS par should have roughly a 50% chance of winning. DLS was designed for 50-over cricket and later applied to T20, where it is often criticised.

This project builds a win probability model from over 500,000 deliveries of men's T20 internationals and IPL matches, then uses it to test whether DLS par really means 50/50, and whether any bias depends on wickets in hand.

**Status:** in progress

## Notebooks

| Notebook | What it does |
|---|---|
| `01_parse_data.ipynb` | Turns raw Cricsheet ball-by-ball JSON into one row per second-innings delivery (514k rows, 4,747 matches, 149 DLS-affected) |
| `02_baseline.ipynb` | Logistic regression baseline, split by match to avoid leakage |

## Data

Ball-by-ball data from [Cricsheet](https://cricsheet.org/downloads/), not included in this repo. Download the men's T20 internationals and IPL zips in JSON format and unzip into `data/t20s_male_json/` and `data/ipl_male_json/`.

## Running it

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the notebooks in order.
