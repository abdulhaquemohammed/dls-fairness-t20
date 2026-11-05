# Is DLS fair in T20 cricket?

When rain shortens a match, the Duckworth-Lewis-Stern (DLS) method sets a revised target or decides the result. A team chasing and sitting exactly on DLS par should have roughly a 50% chance of winning. DLS was designed for 50-over cricket and later applied to T20, where it is often criticised.

This project tests that claim on **4,493 uninterrupted men's T20I and IPL chases** (over 500,000 deliveries). Because these matches finished normally, their real results show what *would* have happened to a team that was on DLS par at any given moment.

## Key findings

1. **On average, DLS par is fair.** Teams on par went on to win 52% of the time, in line with the normal chasing advantage.
2. **But it undervalues wickets in hand, especially late in a chase.** In the last 5 overs, teams on par with 3-5 wickets down won 60%, while teams 6-9 down won 47%. In overs 11-15, teams 0-2 down on par won 61%. A fair system would put all of these at about 50%.
3. **The finding is robust.** The gap holds with different definitions of "on par", in T20Is and the IPL separately, and before and after 2019.

A likely reason: DLS was built for 50-over cricket, where wickets are saved for a long innings. In T20 there are too few balls left to use them all, so a team with wickets in hand late in a chase can attack freely, which is worth more than the 50-over table assumes.

![Win rate at DLS par by wickets lost and stage of the chase](figures/win_at_par_by_phase.png)

### Example: the 2024 T20 World Cup final

South Africa were 147/4 after 15 overs, needing 30 off 30. The model gave them a 93% chance, and they were 21 runs ahead of DLS par: rain at that moment would have handed them the trophy. They lost by 7 runs.

![2024 T20 World Cup final win probability and DLS margin](figures/final_2024.png)

## Approach

| Step | In this project | Notebook |
|---|---|---|
| 1. Problem definition | Given the state of a chase, predict the probability the chasing team wins (binary classification), then test whether DLS par really means 50/50 | `01` |
| 2. Data | Cricsheet ball-by-ball JSON parsed into 514k second-innings deliveries from 4,747 matches (149 DLS-affected) | `01` |
| 3. Evaluation | Log loss, Brier score and calibration, since win probabilities need to be trustworthy | `02` |
| 4. Features | Runs needed, balls left, wickets left, required run rate, competition | `02` |
| 5. Modelling | Logistic regression baseline, then gradient boosting with monotonic constraints; split by match to avoid leakage | `02`, `03` |
| 6. Experiments | Model comparison and calibration; the DLS fairness test; final figures; robustness checks | `03`-`06` |

### Notebooks

| Notebook | What it does |
|---|---|
| `01_parse_data.ipynb` | Parses Cricsheet JSON into one row per second-innings delivery, with data-cleaning decisions explained |
| `02_baseline.ipynb` | Defines success, then trains a logistic regression baseline |
| `03_model.ipynb` | Gradient boosting model, calibration, and experiments |
| `04_dls_test.ipynb` | The DLS fairness test: win rate at par by wickets lost and stage of the chase |
| `05_figures.ipynb` | Final figures |
| `06_robustness.ipynb` | Reruns the main finding under different choices, plus the 149 real DLS matches |

### Why the main test doesn't use the model

The win probability model (gradient boosting, log loss 0.380 vs 0.694 for a naive baseline) only just beat logistic regression, and its calibration was off by up to 3.6 percentage points in places. It also gave unrealistic answers for match states that never happen in practice. So the DLS test uses **actual match outcomes** instead, and the model is only used for illustration, like the 2024 final chart.

## Limitations

- **Standard, not Professional Edition.** International matches use the proprietary DLS Professional (Stern) Edition, which was updated partly for high-scoring and shorter games. This project uses the public Standard Edition table from the ICC's DLS methodology document, so it may overstate the bias in the version actually used.
- **Termination only.** The test asks what happens if rain *ends* a chase. DLS is also used to set revised targets before or during a chase, which isn't tested.
- **Small samples at the extremes.** Situations like being on par with 9 wickets down are rare, so those estimates are uncertain. Only differences whose 95% intervals clear 50% are treated as real.
- **Not fully independent.** A match can appear in more than one wicket group, so the groups aren't completely independent.

## Data

Ball-by-ball data from [Cricsheet](https://cricsheet.org/downloads/), not included in this repo. Download the men's T20 internationals and IPL zips in JSON format and unzip into `data/t20s_male_json/` and `data/ipl_male_json/`. The DLS Standard Edition resource table is in `reference/dls_standard_edition.csv`.

## Running it

```
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Then run the notebooks in order. Notebook 01 builds `data/chases.csv` and notebook 03 saves the model to `models/`, which later notebooks use.
