#!/usr/bin/env python3
"""Semantic and custody verification for the compact audit results."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"FAIL: {message}")


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--expected", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    expected = load(args.expected)
    replay = load(args.results / "finite_replay.json")
    theorem = load(args.results / "regular_lift_theorem_audit.json")
    corruptions = load(args.results / "corruption_tests.json")
    control = load(args.results / "c0_mod4_control.json")
    manifest = load(args.results / "manifest.json")

    demand(replay["schema"] == "a303656-one-sided-strip-finite-replay-v1", "replay schema")
    demand(replay["source_commit"] == args.source_commit, "source commit binding")
    demand(replay["N"] == expected["N"] and replay["n_domain"] == [2, expected["N"]], "fixed domain")
    for name in ("S2", "C3", "C5"):
        row = replay["arrays"][name]
        demand(row["byte_for_byte_equal"] is True, f"{name} backend equality")
        demand(row["method_a"] == row["method_b"] == expected["hashes"][name], f"{name} expected hash")
    for key in ("s2_count", "max_C3", "max_C5", "uncovered_C3", "uncovered_C5"):
        demand(replay[key] == expected[key], f"replay field {key}")
    demand(replay["C3_records"] == expected["C3_records"], "C3 records")
    demand(replay["C5_records"] == expected["C5_records"], "C5 records")
    demand(replay["claimed_point"] == {
        "C3": 13,
        "n": 47708696,
        "smaller_c_pairs_checked": 143,
        "status": "VERIFIED",
        "witness": {"a": 2988, "b": 6098, "c": 13, "d": 4},
    }, "claimed point audit")
    demand(replay["raw_arrays_committed"] is False, "raw array scope")
    for command in replay["commands"]:
        demand(command["return_code"] == 0, "replay return code")
        text = json.dumps(command["command"])
        demand("/home/" not in text and "/tmp/" not in text, "absolute command path")

    demand(theorem["verdict"] == "PASS", "theorem audit")
    demand(theorem["small_complete_model"] == {
        "cells_per_tuple": 252,
        "maximum_covered": 186,
        "minimum_uncovered": 66,
        "period": 126,
        "residue_tuples": 10584,
        "status": "PASS_NO_COMPLETE_COVER",
    }, "small complete model")
    demand(theorem["scope"]["base5_nonregular_primes"] == "NOT COVERED", "nonregular boundary")
    demand(corruptions["valid_control_passed"] is True, "corruption control")
    demand(corruptions["all_rejected"] is True and corruptions["test_count"] >= 14, "corruption rejection")
    demand(control["PASS"] is True and control["uncovered_count"] == 0, "periodic control")

    authority = manifest["authority"]
    demand(authority["source_commit"] == args.source_commit, "manifest source commit")
    demand(authority["project"] == "PAUSED" and authority["active_promoted_route"] == "NONE" and authority["A303656"] == "UNRESOLVED", "authority status")
    demand(manifest["scope_guards"] == {
        "authority_modified": False,
        "domain": [2, 100000000],
        "interval_extension": "NOT EXECUTED",
        "prime_pool_expansion": "NOT EXECUTED",
        "raw_arrays_committed": False,
        "wieferich_full_cover_research": "NOT EXECUTED",
    }, "scope guards")
    for row in manifest["files"]:
        path = args.results / row["path"]
        demand(path.is_file(), f"manifest path {row['path']}")
        demand(path.stat().st_size == row["size_bytes"] and sha256(path) == row["sha256"], f"manifest hash {row['path']}")

    forbidden = list(ROOT.rglob("*.uint8")) + list(ROOT.rglob("*.bin"))
    demand(not forbidden, "raw binary committed in audit directory")
    demand(not (ROOT / "raw_gzip").exists(), "misdescribed raw_gzip directory")
    report = (args.results / "REPORT.md").read_text(encoding="utf-8")
    for token in ("PAUSED", "NONE", "UNRESOLVED", "NOT COVERED", "2 <= n <= 100,000,000"):
        demand(token in report, f"report scope token {token}")

    result = {
        "schema": "a303656-one-sided-strip-verification-v1",
        "source_commit": args.source_commit,
        "manifest_files_verified": len(manifest["files"]),
        "corruption_tests_rejected": corruptions["test_count"],
        "raw_arrays_committed": False,
        "authority_state": "PAUSED / NONE / UNRESOLVED",
        "verdict": "PASS",
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
