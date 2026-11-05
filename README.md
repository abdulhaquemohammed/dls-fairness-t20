# Is DLS fair in T20 cricket?

When rain shortens a match, the Duckworth-Lewis-Stern (DLS) method sets a revised target. A team chasing that target and sitting exactly on DLS par should have roughly a 50% chance of winning. DLS was designed for 50-over cricket and later applied to T20, where it is often criticised.

This project builds a win probability model from over 500,000 deliveries of men's T20 internationals and IPL matches, then uses it to test whether DLS par really means 50/50, and whether any bias depends on wickets in hand.

**Status:** in progress

## Approach

| Step | In this project | Notebook | Status |
|---|---|---|---|
| 1. Problem definition | Given the state of a chase, predict the probability the chasing team wins (binary classification), then use it to test DLS | `01` | Done |
| 2. Data | Cricsheet ball-by-ball JSON parsed into 514k second-innings deliveries from 4,747 matches (149 DLS-affected) | `01` | Done |
| 3. Evaluation | Log loss, Brier score and calibration, since the DLS test needs trustworthy probabilities | `02` | Done |
| 4. Features | Runs needed, balls left, wickets left, required run rate, competition | `02` | Done |
| 5. Modelling | Logistic regression baseline, split by match to avoid leakage; gradient boosting with monotonic constraints | `02`, `03` | Done |
| 6. Experiments | Model comparison by phase of the chase, calibration, target-as-feature experiment; DLS fairness test (`04`) in progress | `03`, `04` | In progress |

## Data

Ball-by-ball data from [Cricsheet](https://cricsheet.org/downloads/), not included in this repo. Download the men's T20 internationals and IPL zips in JSON format and unzip into `data/t20s_male_json/` and `data/ipl_male_json/`.

## Running it

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the notebooks in order.
