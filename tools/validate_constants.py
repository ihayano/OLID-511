import json
import sys
from pathlib import Path


def load_constants(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def validate(constants: dict) -> list[str]:
    errors: list[str] = []

    required_top = [
        "global",
        "workbench",
        "travel",
        "deployments",
        "diagnostics",
        "mutual_aid",
        "ending_thresholds",
    ]
    for key in required_top:
        if key not in constants:
            errors.append(f"Missing top-level section: {key}")

    if errors:
        return errors

    g = constants["global"]
    if g["starting_budget"] <= 0:
        errors.append("starting_budget must be > 0")
    if g["starting_hours"] <= 0:
        errors.append("starting_hours must be > 0")
    if g["deployable_location_count"] <= 0:
        errors.append("deployable_location_count must be > 0")

    hw = constants["workbench"]["hardware"]
    for hardware_key, cfg in hw.items():
        if cfg["node_cost"] <= 0:
            errors.append(f"Hardware {hardware_key} has non-positive node_cost")

    purchase = constants["workbench"]["node_purchase"]
    options = purchase["display_options"]
    if not options:
        errors.append("node_purchase.display_options cannot be empty")
    if any(v <= 0 for v in options):
        errors.append("node_purchase.display_options must all be positive")
    if purchase["fallback_min_purchase"] <= 0:
        errors.append("node_purchase.fallback_min_purchase must be positive")

    max_option = max(options) if options else 0
    if max_option < g["deployable_location_count"]:
        errors.append("node_purchase.display_options max should be >= deployable_location_count")

    outside = set(constants["travel"]["outside_town_locations"])
    deployments = constants["deployments"]
    if len(deployments) != g["deployable_location_count"]:
        errors.append(
            f"deployments count ({len(deployments)}) must equal deployable_location_count ({g['deployable_location_count']})"
        )

    for key in outside:
        if key not in deployments:
            errors.append(f"travel.outside_town_locations includes unknown deployment key: {key}")

    for location_key, location_cfg in deployments.items():
        options_cfg = location_cfg.get("options", {})
        if "skip" not in options_cfg:
            errors.append(f"Deployment {location_key} must include a skip option")

        uses_node_count = 0
        for option_key, option in options_cfg.items():
            uses_node = bool(option.get("uses_node", False))
            if uses_node:
                uses_node_count += 1
                if "coverage_base" not in option and location_key not in {"science"}:
                    errors.append(f"{location_key}.{option_key} uses_node=true but missing coverage_base")
            if "add_on_cost" in option and option["add_on_cost"] < 0:
                errors.append(f"{location_key}.{option_key} has negative add_on_cost")
            if "time_cost_hours" in option and option["time_cost_hours"] < 0:
                errors.append(f"{location_key}.{option_key} has negative time_cost_hours")
            if "supplies_delta" in option and option["supplies_delta"] < 0:
                errors.append(f"{location_key}.{option_key} has negative supplies_delta")

        if uses_node_count == 0:
            errors.append(f"Deployment {location_key} has no node-using options")

    d = constants["diagnostics"]
    if d["emergency_patch_cost"] < 0:
        errors.append("diagnostics.emergency_patch_cost cannot be negative")
    if d["emergency_patch_coverage_base"] <= 0:
        errors.append("diagnostics.emergency_patch_coverage_base must be positive")

    e = constants["ending_thresholds"]
    if not (e["coverage_low"] <= e["coverage_good"] <= e["coverage_strong"]):
        errors.append("ending thresholds must satisfy coverage_low <= coverage_good <= coverage_strong")
    if e["minimum_supplies_for_no_shortage"] <= 0:
        errors.append("minimum_supplies_for_no_shortage must be positive")

    add_ons = constants["workbench"].get("add_ons")
    if add_ons is not None:
        for fee_key in ("weatherproof_case", "solar_panel"):
            fee = add_ons.get(fee_key, {}).get("fee")
            if fee is None:
                errors.append(f"workbench.add_ons.{fee_key}.fee is required when add_ons is present")
            elif fee < 0:
                errors.append(f"workbench.add_ons.{fee_key}.fee cannot be negative")

    return errors


def main() -> int:
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("data/game_constants.json")
    if not config_path.exists():
        print(f"[ERROR] Constants file not found: {config_path}")
        return 1

    constants = load_constants(config_path)
    errors = validate(constants)
    if errors:
        print("[FAIL] Validation errors:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(f"[OK] Constants validated: {config_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
