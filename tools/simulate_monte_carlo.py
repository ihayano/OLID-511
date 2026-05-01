import argparse
import json
import random
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from statistics import mean


@dataclass
class RunState:
    budget: int
    coverage: int
    supplies: int
    nodes_available: int
    nodes_purchased: int
    node_cost: int
    link_quality: int
    dead_zones: bool
    valley_weak: bool
    health_weak: bool
    science_roof: bool
    science_missed: bool
    yoshiko_drive: bool
    encryption: bool
    wis_mesh_repeater: bool
    high_gain_antennas: bool
    housing_unit: bool


DEPLOY_ORDER_KEYS = ["science", "valley", "sugar", "apartments", "radio", "health"]


def adjusted_coverage(base_value: int, state: "RunState") -> int:
    antenna_bonus = 2 if state.high_gain_antennas else 0
    housing_bonus = 1 if state.housing_unit else 0
    return max(1, base_value + state.link_quality + antenna_bonus + housing_bonus)


def choose_affordable_option(rng: random.Random, option_names: list[str], weighted: dict[str, float] | None = None) -> str:
    if weighted:
        weights = [weighted.get(name, 1.0) for name in option_names]
        return rng.choices(option_names, weights=weights, k=1)[0]
    return rng.choice(option_names)


def determine_ending(state: RunState, thresholds: dict) -> str:
    coverage = state.coverage
    low_coverage = coverage < thresholds["coverage_low"]
    supply_shortage = state.supplies < thresholds["minimum_supplies_for_no_shortage"]
    coverage_strong = coverage >= thresholds["coverage_strong"]
    nodes_used = state.nodes_purchased - state.nodes_available
    # Ending A hard requirements: WisMesh repeater purchased + science roof deployed + ≥4 devices placed
    science_roof_with_repeater = state.wis_mesh_repeater and state.science_roof and not state.science_missed
    enough_devices = nodes_used >= 4

    if coverage_strong and state.supplies > 0 and (not state.dead_zones) and science_roof_with_repeater and enough_devices:
        return "A"
    if coverage >= thresholds["coverage_good"] and (state.dead_zones or not science_roof_with_repeater or not enough_devices):
        return "B"
    if low_coverage and supply_shortage:
        return "D"
    return "B"


def _pick(rng: random.Random, options: list[str], override: str | None) -> str:
    if override is not None and override in options:
        return override
    return rng.choice(options)


def simulate_one(constants: dict, rng: random.Random, overrides: dict | None = None) -> dict:
    overrides = overrides or {}
    g = constants["global"]
    wb = constants["workbench"]
    dep = constants["deployments"]
    travel = constants["travel"]
    diag = constants["diagnostics"]
    aid = constants["mutual_aid"]

    state = RunState(
        budget=g["starting_budget"],
        coverage=0,
        supplies=0,
        nodes_available=0,
        nodes_purchased=0,
        node_cost=0,
        link_quality=0,
        dead_zones=False,
        valley_weak=False,
        health_weak=False,
        science_roof=False,
        science_missed=False,
        yoshiko_drive=False,
        encryption=False,
        wis_mesh_repeater=False,
        high_gain_antennas=False,
        housing_unit=False,
    )

    # Hardware selection
    hardware_key = _pick(rng, list(wb["hardware"].keys()), overrides.get("hardware"))
    hardware_cfg = wb["hardware"][hardware_key]
    state.node_cost = hardware_cfg["node_cost"]
    state.link_quality += hardware_cfg["link_quality_delta"]

    # Node purchase selection
    max_nodes = max(1, min(g["deployable_location_count"], state.budget // state.node_cost))
    display_options = [n for n in wb["node_purchase"]["display_options"] if n <= max_nodes]
    if not display_options:
        display_options = [wb["node_purchase"]["fallback_min_purchase"]]
    purchased = rng.choice(display_options)
    state.nodes_purchased = purchased
    state.nodes_available = purchased
    state.budget -= purchased * state.node_cost

    # Optional add-ons (gate some install options)
    add_ons = wb.get("add_ons", {})
    housing_fee = int(add_ons.get("weatherproof_housing", {}).get("fee", 20))
    carrier_fee = int(add_ons.get("cat_carrier", {}).get("fee", 20))
    antennas_fee = int(add_ons.get("high_gain_antennas", {}).get("fee", 20))
    repeater_fee = int(add_ons.get("wis_mesh_repeater", {}).get("fee", 99))
    add_on_override = overrides.get("add_ons")
    if add_on_override == "repeater" and state.budget >= repeater_fee:
        state.wis_mesh_repeater = True
        state.budget -= repeater_fee
    elif add_on_override == "antennas" and state.budget >= antennas_fee:
        # Buy up to 4 antennas (covers most locations)
        count = min(4, state.budget // antennas_fee)
        state.high_gain_antennas = count > 0
        state.budget -= count * antennas_fee
    elif add_on_override == "none":
        pass  # purchase nothing
    else:
        # Heuristic: 45% chance to buy the repeater if affordable (it's expensive and unlocks premium deploys).
        if state.budget >= repeater_fee and rng.random() < 0.45:
            state.wis_mesh_repeater = True
            state.budget -= repeater_fee
        if state.budget >= housing_fee and rng.random() < 0.35:
            state.housing_unit = True
            state.budget -= housing_fee
        if state.budget >= antennas_fee and rng.random() < 0.40:
            count = min(4, state.budget // antennas_fee)
            state.high_gain_antennas = count > 0
            state.budget -= count * antennas_fee
        if state.budget >= carrier_fee and rng.random() < 0.25:
            state.budget -= carrier_fee

    # Encryption always on.
    state.encryption = True

    # Deployments
    pending = DEPLOY_ORDER_KEYS.copy()
    rng.shuffle(pending)
    resolved_count = 0
    while pending:
        if resolved_count > 0 and rng.random() < g["finish_early_probability"]:
            break
        location_key = pending.pop()
        resolved_count += 1

        if location_key in travel["outside_town_locations"] and not state.yoshiko_drive:
            if state.budget >= travel["outside_town_ride_cost"] and rng.random() < 0.5:
                state.budget -= travel["outside_town_ride_cost"]

        if state.nodes_available <= 0:
            continue

        options_cfg = dep[location_key]["options"]
        affordable = []
        for option_name, option in options_cfg.items():
            add_on = option.get("add_on_cost", 0)
            if add_on <= state.budget:
                affordable.append(option_name)

        # Gate science roof install unless WisMesh Repeater purchased.
        if location_key == "science" and ("data" in affordable) and not state.wis_mesh_repeater:
            affordable = [name for name in affordable if name != "data"]
        # Gate highgain options unless high-gain antennas purchased.
        if "highgain" in affordable and not state.high_gain_antennas:
            affordable = [name for name in affordable if name != "highgain"]
        if "skip" not in affordable:
            affordable.append("skip")

        if location_key == "science":
            option = choose_affordable_option(
                rng,
                affordable,
                weighted={"data": 3.0, "highgain": 2.0, "emotion": 1.0, "jargon": 1.0, "skip": 1.0},
            )
        elif location_key in {"valley", "health"}:
            option = choose_affordable_option(
                rng,
                affordable,
                weighted={"highgain": 3.0, "solar": 2.0, "basic": 1.0, "skip": 1.0},
            )
        elif location_key == "radio":
            option = choose_affordable_option(rng, affordable, weighted={"deploy": 2.0, "highgain": 2.0, "skip": 1.0})
        else:
            option = choose_affordable_option(rng, affordable, weighted={"highgain": 2.0, "deploy": 2.0, "skip": 1.0})

        selected = options_cfg[option]
        if option == "skip":
            if location_key == "science":
                state.science_missed = True
            continue

        if selected.get("uses_node", False):
            state.nodes_available = max(0, state.nodes_available - 1)
        state.budget -= selected.get("add_on_cost", 0)
        state.supplies += selected.get("supplies_delta", 0)

        if "coverage_base" in selected:
            state.coverage += adjusted_coverage(selected["coverage_base"], state)
            state.coverage = max(0, state.coverage)

        state.science_roof = selected.get("science_roof", state.science_roof)
        state.yoshiko_drive = selected.get("yoshiko_drive", state.yoshiko_drive)

        if selected.get("dead_zone", False):
            state.dead_zones = True
        state.valley_weak = selected.get("valley_weak", state.valley_weak)
        state.health_weak = selected.get("health_weak", state.health_weak)

    # Diagnostics — emergency patch removed from game; dead zones are now permanent.
    issues_present = state.valley_weak or state.health_weak
    if issues_present:
        state.dead_zones = True

    # Mutual aid
    if rng.random() < 0.7:
        state.supplies += aid["grant_supplies_delta"]

    ending = determine_ending(state, constants["ending_thresholds"])
    return {
        "ending": ending,
        "budget": state.budget,
        "coverage": state.coverage,
        "supplies": state.supplies,
        "nodes_used": state.nodes_purchased - state.nodes_available,
    }


def run_simulation(constants: dict, runs: int, seed: int, overrides: dict | None = None) -> dict:
    rng = random.Random(seed)
    outcomes = [simulate_one(constants, rng, overrides) for _ in range(runs)]
    endings = Counter(o["ending"] for o in outcomes)

    return {
        "runs": runs,
        "endings": dict(endings),
        "ending_rates": {k: endings.get(k, 0) / runs for k in ["A", "B", "D"]},
        "avg_budget": mean(o["budget"] for o in outcomes),
        "avg_coverage": mean(o["coverage"] for o in outcomes),
        "avg_supplies": mean(o["supplies"] for o in outcomes),
        "avg_nodes_used": mean(o["nodes_used"] for o in outcomes),
    }


def stratified_sweep(constants: dict, runs_per_stratum: int, seed: int) -> dict:
    """For each stratifiable workbench variable, force one value at a time
    while randomizing the rest of the choices. Returns a nested dict keyed by
    variable name then value, with the same shape as run_simulation's output.
    """
    wb = constants["workbench"]
    strata_values: dict[str, list[str]] = {
        "hardware": list(wb["hardware"].keys()),
        "add_ons": ["none", "antennas", "repeater"],
    }

    results: dict[str, dict[str, dict]] = {}
    salt = 0
    for variable, values in strata_values.items():
        results[variable] = {}
        for value in values:
            overrides = {variable: value}
            sub_seed = seed + 1_000 * (salt + 1)
            results[variable][value] = run_simulation(
                constants, runs=runs_per_stratum, seed=sub_seed, overrides=overrides
            )
            salt += 1

    return {
        "runs_per_stratum": runs_per_stratum,
        "variables": results,
    }


def sweep_tuning(constants: dict, seed: int) -> list[dict]:
    candidates = []
    base_budget = constants["global"]["starting_budget"]
    base_fiona = constants["deployments"]["apartments"]["options"]["deploy"]["supplies_delta"]
    budget_values = sorted(
        {
            max(100, base_budget - 80),
            max(100, base_budget - 40),
            base_budget,
            base_budget + 20,
            base_budget + 40,
            400,
        }
    )

    for budget in budget_values:
        for fiona_bonus in [1, 2, 3]:
            cfg = json.loads(json.dumps(constants))
            cfg["global"]["starting_budget"] = budget
            cfg["deployments"]["apartments"]["options"]["deploy"]["supplies_delta"] = fiona_bonus

            result = run_simulation(cfg, runs=2000, seed=seed + budget + fiona_bonus)
            rates = result["ending_rates"]
            # Favor strong ending A and penalize failure ending D.
            score = (rates["A"] * 3.0) + (rates["B"] * 1.0) - (rates["D"] * 4.0)
            candidates.append(
                {
                    "budget": budget,
                    "fiona_supplies": fiona_bonus,
                    "score": score,
                    "a_rate": rates["A"],
                    "b_rate": rates["B"],
                    "d_rate": rates["D"],
                    "avg_budget": result["avg_budget"],
                    "avg_supplies": result["avg_supplies"],
                    "is_current_config": budget == base_budget and fiona_bonus == base_fiona,
                }
            )

    return sorted(candidates, key=lambda x: x["score"], reverse=True)


def _format_strata_section(strata: dict | None) -> list[str]:
    if not strata:
        return []
    lines: list[str] = []
    lines.append("## Stratified sweep")
    lines.append("")
    lines.append(
        f"Each row forces one workbench decision to a specific value and randomizes the rest. "
        f"{strata['runs_per_stratum']} runs per stratum."
    )
    lines.append("")
    for variable, values in strata["variables"].items():
        lines.append(f"### {variable}")
        lines.append("")
        lines.append("| value | A | B | D | avg coverage | avg budget | avg supplies |")
        lines.append("|-------|---|---|---|--------------|------------|--------------|")
        for value, result in values.items():
            rates = result["ending_rates"]
            lines.append(
                f"| `{value}` | {rates['A']:.1%} | {rates['B']:.1%} | {rates['D']:.1%} | "
                f"{result['avg_coverage']:.2f} | ${result['avg_budget']:.0f} | {result['avg_supplies']:.2f} |"
            )
        lines.append("")
    return lines


def write_report(
    report_path: Path,
    baseline: dict,
    sweep_results: list[dict],
    runs: int,
    seed: int,
    strata: dict | None = None,
) -> None:
    top = sweep_results[:5]
    current = next((r for r in sweep_results if r["is_current_config"]), None)

    lines = []
    lines.append("# Project Intermesh Monte Carlo Report")
    lines.append("")
    lines.append(f"- Runs: **{runs}**")
    lines.append(f"- Seed: **{seed}**")
    lines.append("")
    lines.append("## Baseline (current constants)")
    lines.append("")
    rates = baseline["ending_rates"]
    lines.append(f"- Ending A: **{rates['A']:.1%}**")
    lines.append(f"- Ending B: **{rates['B']:.1%}**")
    lines.append(f"- Ending D: **{rates['D']:.1%}**")
    lines.append(f"- Avg coverage: **{baseline['avg_coverage']:.2f}**")
    lines.append(f"- Avg budget left: **${baseline['avg_budget']:.2f}**")
    lines.append(f"- Avg supplies: **{baseline['avg_supplies']:.2f}**")
    lines.append("")
    lines.append("## Top tuning candidates (grid search)")
    lines.append("")
    for idx, item in enumerate(top, start=1):
        lines.append(
            f"{idx}. budget=${item['budget']}, fiona_supplies={item['fiona_supplies']} "
            f"| score={item['score']:.3f} | A={item['a_rate']:.1%}, B={item['b_rate']:.1%}, D={item['d_rate']:.1%}"
        )
    lines.append("")
    lines.append("## Objective recommendation")
    lines.append("")
    best = top[0]
    lines.append(
        f"- Recommended constants: `starting_budget={best['budget']}`, "
        f"`apartments.deploy.supplies_delta={best['fiona_supplies']}`."
    )
    if current:
        lines.append(
            f"- Current config score: **{current['score']:.3f}**; recommended score: **{best['score']:.3f}** "
            f"({best['score'] - current['score']:+.3f})."
        )
    lines.append("- Keep this recommendation as a balancing target, then re-run the simulation after each gameplay adjustment.")
    lines.append("")

    lines.extend(_format_strata_section(strata))

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description="Monte Carlo simulator for Project Intermesh balancing.")
    parser.add_argument("--config", default="data/game_constants.json", help="Path to constants JSON")
    parser.add_argument("--runs", type=int, default=10000, help="Number of Monte Carlo runs")
    parser.add_argument("--seed", type=int, default=42, help="Random seed")
    parser.add_argument("--report", default="reports/monte_carlo_report.md", help="Output markdown report path")
    parser.add_argument("--out-json", default="reports/monte_carlo_report.json", help="Output JSON report path")
    parser.add_argument(
        "--strata-runs",
        type=int,
        default=2000,
        help="Runs per stratum for the stratified sweep (one decision forced, others random).",
    )
    parser.add_argument(
        "--no-strata",
        action="store_true",
        help="Skip the stratified sweep (baseline + tuning grid only).",
    )
    args = parser.parse_args()

    constants = json.loads(Path(args.config).read_text(encoding="utf-8"))
    baseline = run_simulation(constants, runs=args.runs, seed=args.seed)
    sweep_results = sweep_tuning(constants, seed=args.seed)

    strata = None
    if not args.no_strata:
        strata = stratified_sweep(constants, runs_per_stratum=args.strata_runs, seed=args.seed)

    report_path = Path(args.report)
    write_report(report_path, baseline, sweep_results, args.runs, args.seed, strata=strata)

    out = {
        "baseline": baseline,
        "top_tuning_candidates": sweep_results[:10],
    }
    if strata is not None:
        out["strata"] = strata
    out_json_path = Path(args.out_json)
    out_json_path.parent.mkdir(parents=True, exist_ok=True)
    out_json_path.write_text(json.dumps(out, indent=2), encoding="utf-8")

    print(f"[OK] Baseline simulation complete: {args.runs} runs")
    if strata is not None:
        total_strata = sum(len(values) for values in strata["variables"].values())
        print(
            f"[OK] Stratified sweep complete: {total_strata} strata x {args.strata_runs} runs each "
            f"({total_strata * args.strata_runs} total)"
        )
    print(f"[OK] Report written: {report_path}")
    print(f"[OK] JSON written: {out_json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
