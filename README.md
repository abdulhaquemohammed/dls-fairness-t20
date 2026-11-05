# Is DLS fair in T20 cricket?

When rain shortens a match, the Duckworth-Lewis-Stern (DLS) method sets a revised target. A team chasing that target and sitting exactly on DLS par should have roughly a 50% chance of winning. DLS was designed for 50-over cricket and later applied to T20, where it is often criticised.

This project builds a win probability model from over 500,000 deliveries of men's T20 internationals and IPL matches, then uses it to test whether DLS par really means 50/50, and whether any bias depends on wickets in hand.

**Status:** in progress

## Key finding so far

On average, the DLS Standard Edition par score is fair in T20: teams on par won 52% of the time, in line with the normal chasing advantage. But it **undervalues wickets in hand**, especially in the second half of a chase. In the last 5 overs, teams on par with 3-5 wickets down won 60%, while teams 6-9 down won 47%.

![Win rate at DLS par by wickets lost and stage of the chase](figures/win_at_par_by_phase.png)

### Example: the 2024 T20 World Cup final

South Africa were 147/4 after 15 overs, needing 30 off 30. The model gave them a 93% chance, and they were 21 runs ahead of DLS par: rain at that moment would have handed them the trophy. They lost by 7 runs.

![2024 T20 World Cup final win probability and DLS margin](figures/final_2024.png)

## Approach

| Step | In this project | Notebook | Status |
|---|---|---|---|
| 1. Problem definition | Given the state of a chase, predict the probability the chasing team wins (binary classification), then use it to test DLS | `01` | Done |
| 2. Data | Cricsheet ball-by-ball JSON parsed into 514k second-innings deliveries from 4,747 matches (149 DLS-affected) | `01` | Done |
| 3. Evaluation | Log loss, Brier score and calibration, since the DLS test needs trustworthy probabilities | `02` | Done |
| 4. Features | Runs needed, balls left, wickets left, required run rate, competition | `02` | Done |
| 5. Modelling | Logistic regression baseline, split by match to avoid leakage; gradient boosting with monotonic constraints | `02`, `03` | Done |
| 6. Experiments | Model comparison, calibration, target-as-feature experiment; DLS fairness test on 4,493 uninterrupted chases, split by wickets and phase; final figures | `03`, `04`, `05` | Done |

## Data

Ball-by-ball data from [Cricsheet](https://cricsheet.org/downloads/), not included in this repo. Download the men's T20 internationals and IPL zips in JSON format and unzip into `data/t20s_male_json/` and `data/ipl_male_json/`.

## Running it

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the notebooks in order.
