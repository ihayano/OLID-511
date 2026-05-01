# Project Intermesh Monte Carlo Report

- Runs: **1000**
- Seed: **42**

## Baseline (current constants)

- Ending A: **9.1%**
- Ending B: **71.1%**
- Ending D: **19.8%**
- Avg coverage: **21.84**
- Avg budget left: **$172.47**
- Avg supplies: **2.60**

## Top tuning candidates (grid search)

1. budget=$460, fiona_supplies=3 | score=0.323 | A=11.8%, B=70.0%, D=18.2%
2. budget=$420, fiona_supplies=2 | score=0.243 | A=10.7%, B=70.0%, D=19.4%
3. budget=$400, fiona_supplies=3 | score=0.208 | A=9.2%, B=71.4%, D=19.5%
4. budget=$460, fiona_supplies=2 | score=0.169 | A=10.3%, B=68.9%, D=20.8%
5. budget=$440, fiona_supplies=2 | score=0.158 | A=10.2%, B=69.0%, D=20.9%

## Objective recommendation

- Recommended constants: `starting_budget=460`, `apartments.deploy.supplies_delta=3`.
- Current config score: **0.243**; recommended score: **0.323** (+0.079).
- Keep this recommendation as a balancing target, then re-run the simulation after each gameplay adjustment.

## Stratified sweep

Each row forces one workbench decision to a specific value and randomizes the rest. 500 runs per stratum.

### hardware

| value | A | B | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|--------------|------------|--------------|
| `thinknode` | 9.2% | 69.6% | 21.2% | 20.78 | $202 | 2.58 |
| `techo` | 5.6% | 74.2% | 20.2% | 19.57 | $173 | 2.62 |
| `meshpocket` | 11.2% | 67.4% | 21.4% | 24.15 | $146 | 2.50 |

### add_ons

| value | A | B | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|--------------|------------|--------------|
| `none` | 3.2% | 80.8% | 16.0% | 18.72 | $213 | 2.75 |
| `repeater` | 11.8% | 71.4% | 16.8% | 21.13 | $147 | 2.62 |
