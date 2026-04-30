# Project Intermesh Monte Carlo Report

- Runs: **500**
- Seed: **42**

## Baseline (current constants)

- Ending A: **6.6%**
- Ending B: **81.2%**
- Ending C: **0.0%**
- Ending D: **12.2%**
- Avg coverage: **19.97**
- Avg budget left: **$155.34**
- Avg supplies: **3.39**

## Top tuning candidates (grid search)

1. budget=$440, fiona_supplies=3 | score=0.536 | A=9.2%, B=77.9%, C=0.0%, D=13.0%
2. budget=$400, fiona_supplies=3 | score=0.528 | A=7.2%, B=80.4%, C=0.0%, D=12.3%
3. budget=$360, fiona_supplies=2 | score=0.480 | A=6.2%, B=80.8%, C=0.0%, D=12.9%
4. budget=$420, fiona_supplies=3 | score=0.477 | A=8.1%, B=78.2%, C=0.0%, D=13.7%
5. budget=$420, fiona_supplies=2 | score=0.469 | A=8.8%, B=77.0%, C=0.0%, D=14.1%

## Objective recommendation

- Recommended constants: `starting_budget=440`, `apartments.deploy.supplies_delta=3`.
- Current config score: **0.528**; recommended score: **0.536** (+0.008).
- Keep this recommendation as a balancing target, then re-run the simulation after each gameplay adjustment.

## Stratified sweep

Each row forces one workbench decision to a specific value and randomizes the rest. 2000 runs per stratum.

### hardware

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `heltec` | 7.0% | 78.8% | 0.0% | 14.2% | 19.23 | $194 | 3.40 |
| `tbeam` | 8.2% | 77.5% | 0.0% | 14.2% | 19.19 | $158 | 3.36 |
| `rak` | 9.2% | 77.4% | 0.0% | 13.4% | 21.71 | $124 | 3.36 |

### firmware

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `stable` | 10.4% | 76.2% | 0.0% | 13.4% | 21.61 | $151 | 3.34 |
| `alpha` | 5.3% | 79.6% | 0.0% | 15.0% | 18.23 | $160 | 3.36 |

### add_ons

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `none` | 1.2% | 84.2% | 0.0% | 14.6% | 18.34 | $205 | 3.42 |
| `case` | 0.2% | 84.4% | 0.0% | 15.4% | 18.15 | $169 | 3.38 |
| `solar` | 0.7% | 83.0% | 0.0% | 16.2% | 17.86 | $169 | 3.39 |
| `both` | 14.1% | 73.0% | 0.0% | 12.8% | 21.51 | $132 | 3.28 |
