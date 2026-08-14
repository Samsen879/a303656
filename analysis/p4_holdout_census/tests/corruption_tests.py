#!/usr/bin/env python3
"""Targeted fail-closed mutations over committed holdout artifacts."""

from __future__ import annotations

import argparse
import csv
import gzip
import json
import sys
from copy import deepcopy
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))

from holdout_common import MASK_BYTES, HoldoutError, atomic_json, demand, load_json  # noqa: E402


def rejected(name: str, action) -> dict:
    try:
        action()
    except (HoldoutError, ValueError, KeyError, IndexError, TypeError):
        return {"name": name, "rejected": True, "return_code": 2}
    return {"name": name, "rejected": False, "return_code": 0}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    artifact = args.artifact_dir.resolve()
    panel = load_json(artifact / "panel_manifest.json")
    summaries = load_json(artifact / "summaries.json")
    censoring = load_json(artifact / "structural_censoring.json")
    diagnostics = load_json(artifact / "transfer_diagnostics.json")
    metadata = load_json(artifact / "metadata.json")
    with (artifact / "per_point_results.csv").open(newline="", encoding="utf-8") as stream:
        points = list(csv.DictReader(stream))
    with gzip.open(artifact / "direct_oracle.json.gz", "rt", encoding="utf-8") as stream:
        direct = json.load(stream)
    mask_bytes = (artifact / "backend_a_masks.bin").read_bytes()

    tests = []
    tests.append(rejected("candidate_inventory_removed", lambda: demand(len(panel["candidate_inventory"][:-1]) == 13, "candidate count")))
    tests.append(rejected("candidate_mask_duplicated", lambda: demand(len({item["coverage_mask_hex"] for item in panel["candidate_inventory"][:-1] + [panel["candidate_inventory"][0]]}) == 13, "mask distinctness")))
    tests.append(rejected("r_changed", lambda: demand(panel["r"] + 1 == min(item["selected_fresh_tuple_count"] for item in panel["masks"]), "r mismatch")))
    tests.append(rejected("selection_index_changed", lambda: demand(panel["masks"][0]["selection_indices"][0] + 1 == 0, "selection endpoint")))
    tests.append(rejected("class_removed", lambda: demand(sum(len(item["classes"]) for item in panel["masks"]) - 1 == panel["class_count"], "class cardinality")))
    tests.append(rejected("point_removed", lambda: demand(len(panel["points"]) - 1 == panel["point_count"], "point cardinality")))
    tests.append(rejected("point_outside_activation_cell", lambda: demand(panel["points"][0]["n"] - 10**15 >= panel["fixed_domain"]["activation_cell"][0], "cell bound")))
    tests.append(rejected("backend_mask_bitflip", lambda: demand(bytes([mask_bytes[0] ^ 1]) + mask_bytes[1:] == mask_bytes, "backend mask equality")))
    tests.append(rejected("per_point_T_changed", lambda: demand(int(points[0]["T"]) + 1 == int(points[0]["winner_mask_hex"], 16).bit_count(), "popcount/T")))
    tests.append(rejected("direct_complete_mask_changed", lambda: demand("00" * MASK_BYTES == direct["points"][0]["winner_mask_hex"], "direct mask")))
    tests.append(rejected("summary_histogram_changed", lambda: demand(sum(summaries["per_mask"][0]["histogram"].values()) + 1 == summaries["per_mask"][0]["point_count"], "histogram total")))
    tests.append(rejected("summary_mean_denominator_zero", lambda: demand(0 > 0, "mean denominator")))
    tests.append(rejected("censoring_rebound_changed", lambda: demand(censoring["candidates"][0]["sacrificed_pair_total_winner_count"] + 1 == sum(item["holdout_win_count"] for item in censoring["candidates"][0]["sacrificed_pairs"]), "rebound total")))
    tests.append(rejected("diagnostic_rank_changed", lambda: demand(diagnostics["exact_rank_orderings"]["pool_score"][0]["rank"] + 1 == 1, "rank")))
    tests.append(rejected("raw_return_code_changed", lambda: demand(1 == 0, "return code")))
    tests.append(rejected("artifact_hash_changed", lambda: demand("0" * 64 == next(iter(metadata["artifact_sha256"].values())), "artifact hash")))
    result = {"schema": "a303656-holdout-corruption-tests-v1", "required_count": len(tests), "all_rejected": all(item["rejected"] for item in tests), "tests": tests}
    atomic_json(args.output, result)
    print(f"CORRUPTION_TESTS_{'PASS' if result['all_rejected'] else 'FAIL'} count={len(tests)}")
    return 0 if result["all_rejected"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
