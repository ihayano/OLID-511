# Project Intermesh Monte Carlo Report

- Runs: **1000**
- Seed: **42**

## Baseline (current constants)

- Ending A: **11.2%**
- Ending B: **66.8%**
- Ending D: **22.0%**
- Avg coverage: **21.77**
- Avg budget left: **$180.42**
- Avg supplies: **2.56**

## Top tuning candidates (grid search)

1. budget=$460, fiona_supplies=3 | score=0.257 | A=11.1%, B=69.6%, D=19.3%
2. budget=$420, fiona_supplies=3 | score=0.213 | A=11.9%, B=67.6%, D=20.5%
3. budget=$440, fiona_supplies=2 | score=0.208 | A=10.2%, B=69.8%, D=20.0%
4. budget=$400, fiona_supplies=2 | score=0.186 | A=10.4%, B=69.1%, D=20.4%
5. budget=$400, fiona_supplies=3 | score=0.167 | A=10.4%, B=68.7%, D=20.8%

## Objective recommendation

- Recommended constants: `starting_budget=460`, `apartments.deploy.supplies_delta=3`.
- Current config score: **0.137**; recommended score: **0.257** (+0.120).
- Keep this recommendation as a balancing target, then re-run the simulation after each gameplay adjustment.

## Stratified sweep

Each row forces one workbench decision to a specific value and randomizes the rest. 300 runs per stratum.

### hardware

| value | A | B | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|--------------|------------|--------------|
| `thinknode` | 9.7% | 69.3% | 21.0% | 20.80 | $213 | 2.60 |
| `techo` | 9.3% | 70.0% | 20.7% | 20.45 | $179 | 2.68 |
| `meshpocket` | 16.0% | 63.3% | 20.7% | 26.06 | $146 | 2.64 |

### add_ons

| value | A | B | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|--------------|------------|--------------|
| `none` | 0.0% | 76.3% | 23.7% | 15.62 | $226 | 2.50 |
| `antennas` | 14.0% | 67.0% | 19.0% | 25.72 | $217 | 2.63 |
| `repeater` | 7.0% | 67.0% | 26.0% | 19.99 | $154 | 2.47 |
