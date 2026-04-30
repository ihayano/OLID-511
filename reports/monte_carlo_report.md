# Project Intermesh Monte Carlo Report

- Runs: **500**
- Seed: **42**

## Baseline (current constants)

- Ending A: **1.4%**
- Ending B: **74.2%**
- Ending C: **7.8%**
- Ending D: **16.6%**
- Avg coverage: **12.12**
- Avg budget left: **$153.60**
- Avg supplies: **3.40**

## Top tuning candidates (grid search)

1. budget=$360, fiona_supplies=2 | score=0.202 | A=0.3%, B=79.7%, C=4.9%, D=15.1%
2. budget=$400, fiona_supplies=3 | score=0.155 | A=0.4%, B=78.3%, C=5.3%, D=16.0%
3. budget=$440, fiona_supplies=3 | score=0.149 | A=0.5%, B=76.8%, C=6.7%, D=15.9%
4. budget=$420, fiona_supplies=2 | score=0.139 | A=1.2%, B=77.0%, C=5.1%, D=16.7%
5. budget=$440, fiona_supplies=2 | score=0.133 | A=0.9%, B=76.8%, C=5.7%, D=16.6%

## Objective recommendation

- Recommended constants: `starting_budget=360`, `apartments.deploy.supplies_delta=2`.
- Current config score: **0.155**; recommended score: **0.202** (+0.047).
- Keep this recommendation as a balancing target, then re-run the simulation after each gameplay adjustment.

## Stratified sweep

Each row forces one workbench decision to a specific value and randomizes the rest. 2000 runs per stratum.

### hardware

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `heltec` | 0.8% | 78.7% | 4.8% | 15.8% | 10.92 | $197 | 3.44 |
| `tbeam` | 0.7% | 77.2% | 4.5% | 17.6% | 10.95 | $158 | 3.30 |
| `rak` | 1.2% | 72.9% | 7.4% | 18.5% | 13.17 | $121 | 3.29 |

### firmware

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `stable` | 0.9% | 73.4% | 8.4% | 17.3% | 12.74 | $153 | 3.37 |
| `alpha` | 0.4% | 78.8% | 3.6% | 17.2% | 10.38 | $162 | 3.32 |

### frequency_plan

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `us915` | 1.7% | 67.8% | 14.7% | 15.8% | 16.93 | $156 | 3.38 |
| `eu868` | 0.2% | 79.2% | 2.9% | 17.8% | 10.31 | $159 | 3.35 |
| `lab433` | 0.0% | 81.0% | 0.5% | 18.4% | 8.07 | $159 | 3.35 |

### preset

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `longfast` | 1.4% | 71.3% | 10.7% | 16.6% | 14.66 | $159 | 3.34 |
| `balanced` | 0.4% | 77.9% | 5.9% | 15.8% | 11.73 | $157 | 3.44 |
| `turbo` | 0.2% | 80.2% | 2.5% | 17.1% | 9.10 | $158 | 3.36 |

### security

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `secure` | 1.5% | 81.1% | 0.0% | 17.4% | 11.97 | $157 | 3.36 |
| `public` | 0.0% | 72.0% | 12.1% | 15.8% | 12.08 | $156 | 3.36 |

### add_ons

| value | A | B | C | D | avg coverage | avg budget | avg supplies |
|-------|---|---|---|---|--------------|------------|--------------|
| `none` | 0.0% | 80.0% | 3.1% | 16.8% | 10.23 | $208 | 3.40 |
| `case` | 0.1% | 79.5% | 4.4% | 16.1% | 10.29 | $165 | 3.43 |
| `solar` | 0.0% | 80.6% | 3.1% | 16.3% | 10.16 | $166 | 3.45 |
| `both` | 1.7% | 73.2% | 8.1% | 17.1% | 13.29 | $129 | 3.29 |
