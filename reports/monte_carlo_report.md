# Project Intermesh Monte Carlo Report

- Runs: **2000**
- Seed: **99**

## Baseline (current constants)

- Ending A: **0.1%**
- Ending B: **67.4%**
- Ending C: **2.5%**
- Ending D: **30.0%**
- Avg coverage: **8.86**
- Avg budget left: **$109.14**
- Avg hours left: **80.52H**
- Avg supplies: **2.73**

## Top tuning candidates (grid search)

1. budget=$340, hours=60, fiona_supplies=2 | score=-0.406 | A=0.2%, B=69.1%, C=3.0%, D=27.6%
2. budget=$320, hours=84, fiona_supplies=2 | score=-0.425 | A=0.1%, B=69.2%, C=2.8%, D=28.0%
3. budget=$340, hours=84, fiona_supplies=2 | score=-0.455 | A=0.1%, B=68.2%, C=3.4%, D=28.4%
4. budget=$340, hours=84, fiona_supplies=3 | score=-0.455 | A=0.1%, B=68.3%, C=3.0%, D=28.5%
5. budget=$280, hours=60, fiona_supplies=3 | score=-0.502 | A=0.0%, B=68.0%, C=2.5%, D=29.5%

## Objective recommendation

- Recommended constants: `starting_budget=340`, `starting_hours=60`, `apartments.deploy.supplies_delta=2`.
- Current config score: **-0.455**; recommended score: **-0.406** (+0.050).
- Keep this recommendation as a balancing target, then re-run the simulation after each gameplay adjustment.
