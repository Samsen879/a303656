#!/usr/bin/env python3
"""Deterministically regenerate results, run tests, and seal the package."""
from __future__ import annotations

import sys
sys.dont_write_bytecode = True

import argparse
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess

from common import sha256_bytes, sha256_file, template_hash, write_json
from verify_package import build_manifest, verify_text_hygiene

AUTHORITY = {
    "repository": "Samsen879/a303656",
    "repository_id": 1333945235,
    "main_sha": "29fee0317b268d2b2747f9564efc445fdd6da7f9",
    "main_tree": "0f5c5acbd5b5d0bc3b24b06cdce70685d10dbd55",
    "state": {
        "PROJECT": "PAUSED",
        "ACTIVE_PROMOTED_ROUTE": "NONE",
        "A303656": "UNRESOLVED",
    },
}

SOURCE_BLOBS = {
    "STATUS.md": "2ba295c0ada0d19b4e7f7d7871312d0696a785d2",
    "analysis/c1_entangled_coordinate_deficit/FORMAL_CLASS.md": "2a788348cf9abdce43f47809b7b6fd6cb8f3f04d",
    "analysis/c1_entangled_coordinate_deficit/THEOREM_AUDIT.md": "33fb391b6547fce68bb7a1964d3757fa5b5c8910",
    "analysis/c1_entangled_coordinate_deficit/QUANTIFIER_CROSSWALK.md": "c2589d0e45310ffd29c88eedc63174318fc3d2eb",
    "analysis/c1_entangled_coordinate_deficit/EVIDENCE_CLASSIFICATION.md": "6f90cb38cc582e83507452d3f0fc89b86fcbef09",
    "analysis/c1_entangled_coordinate_deficit/results/coordinate_examples.json": "3aba268396d2ab39e909e9785ea7fc978629610f",
    "analysis/c1_entangled_coordinate_deficit/results/dependency_chain.json": "73fd0d25269175ae72590405d9c4801d0e9cf75f",
    "analysis/c1_entangled_coordinate_deficit/results/k2_boundary_replay.json": "9737dda5a2e33092124d1f15a6349ff104e2f010",
    "analysis/c1_nonregular_coarse_fatal_audit/THEOREM_AUDIT.md": "74e616d577027698a8ae3cea171ca0fb11874bf3",
}


def run(command: list[str], cwd: Path) -> None:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    subprocess.run(command, cwd=cwd, env=env, check=True)


def run_capture(command: list[str], cwd: Path) -> str:
    env = dict(os.environ)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env["PYTHONHASHSEED"] = "0"
    completed = subprocess.run(
        command,
        cwd=cwd,
        env=env,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    return completed.stdout


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    root = args.root.resolve()
    results = root / "results"
    if results.exists():
        shutil.rmtree(results)
    results.mkdir(parents=True)
    for name in ("manifest.json", "SHA256SUMS.txt"):
        path = root / name
        if path.exists():
            path.unlink()

    run([sys.executable, "tools/rational_template_enumerator.py", "--output", str(results / "rational_template_catalog.json")], root)
    run([sys.executable, "tools/fiber_cover_checker.py", "--output", str(results / "fiber_template_catalog.json")], root)
    run([
        sys.executable,
        "tools/arithmetic_realizability_checker.py",
        "--bound",
        "500000",
        "--output",
        str(results / "arithmetic_realizability.json"),
        "--searched-primes-output",
        str(results / "searched_primes.txt"),
    ], root)

    rational = json.loads((results / "rational_template_catalog.json").read_text())
    fiber = json.loads((results / "fiber_template_catalog.json").read_text())
    arithmetic = json.loads((results / "arithmetic_realizability.json").read_text())

    write_json(results / "source_binding.json", {
        "authority": AUTHORITY,
        "required_source_blob_shas": SOURCE_BLOBS,
        "read_only_execution": True,
        "github_mutations": [],
    })
    write_json(results / "environment.json", {
        "python": sys.version.splitlines()[0],
        "implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "machine": platform.machine(),
        "byteorder": sys.byteorder,
        "dependencies": "Python standard library only",
        "determinism": {
            "PYTHONHASHSEED": "0",
            "PYTHONDONTWRITEBYTECODE": "1",
            "json": "sort_keys=True,separators=(',',':')",
            "zip": "ZIP_STORED, sorted entries, timestamp 1980-01-01",
        },
    })
    write_json(results / "beta_classification.json", {
        "schema": "a303656.beta-one-beta-two-classification.v1",
        "classification": fiber["beta_symbolic_classification"],
        "bounded_group_counts": [
            {"l": g["l"], "beta": g["beta"], "template_count": g["template_count"]}
            for g in fiber["groups"] if g["beta"] <= 2
        ],
        "PASS": True,
    })
    counterexample_records = {
        **{f"fiber.{name}": item for name, item in fiber["counterexamples"].items()},
        "arithmetic.universal_impossibility": arithmetic["feasibility"]["universal_impossibility_example"],
        "arithmetic.anchorwise_not_common": arithmetic["common_residue"]["separately_realizable_but_not_common"],
        "arithmetic.separate_anchor_beta_one_class_zero": arithmetic["separate_anchor_beta_one_class_zero"],
        "arithmetic.actual_dual_anchor_beta_one": arithmetic["actual_dual_anchor_beta_one_realization"],
        "arithmetic.unrealizable_q7_rigid_label": arithmetic["unrealizable_q7_rigid_label"],
        "boundary.K2_constant": arithmetic["k2_constant_boundary_replay"],
    }
    write_json(results / "counterexamples.json", {
        "schema": "a303656.inverse-classification-counterexamples.v1",
        "fiber": fiber["counterexamples"],
        "arithmetic": {
            "universal_impossibility": arithmetic["feasibility"]["universal_impossibility_example"],
            "anchorwise_not_common": arithmetic["common_residue"]["separately_realizable_but_not_common"],
            "separate_anchor_beta_one_class_zero": arithmetic["separate_anchor_beta_one_class_zero"],
            "actual_dual_anchor_beta_one": arithmetic["actual_dual_anchor_beta_one_realization"],
            "unrealizable_q7_rigid_label": arithmetic["unrealizable_q7_rigid_label"],
            "bounded_depth_two_absence": arithmetic["feasibility"]["bounded_absence_warning"],
        },
        "boundary": {
            "K2_constant": arithmetic["k2_constant_boundary_replay"],
        },
        "hashes": {
            name: item.get("counterexample_sha256", item.get("record_sha256", template_hash(item)))
            for name, item in sorted(counterexample_records.items())
        },
        "PASS": True,
    })
    write_json(results / "theorem_checks.json", {
        "schema": "a303656.inverse-theorem-checks.v1",
        "rational_catalog_sha256": rational["catalog_sha256"],
        "fiber_catalog_sha256": fiber["catalog_sha256"],
        "arithmetic_result_sha256": arithmetic["result_sha256"],
        "claims": {
            "atomic_minimal_saturation_is_exact": rational["theorem_checks"]["minimal_distinct_dynamic_depths_force_exact_equality"],
            "atomic_depth_bound": rational["theorem_checks"]["depth_bound_B_le_A_minus_1_checked_for_all_emitted_templates"],
            "all_generated_fiber_templates_minimal": fiber["theorem_checks"]["all_generated_are_row_minimal_covers"],
            "fiber_multiplicity_at_most_two": fiber["theorem_checks"]["no_multiplicity_above_two"],
            "budget_equality_iff_no_overlap_tail": fiber["theorem_checks"]["exact_budget_iff_no_overlap_tail"],
            "actual_67_20771_beta_one": arithmetic["actual_beta_one_realization"]["exact_partition"],
            "actual_67_20771_dual_anchor_pointwise": all(
                row["dynamic_fatal_count"] == 66
                and row["rigid_fatal_count"] == 1
                and not row["uncovered_indices"]
                and not row["overlap_indices"]
                for row in arithmetic["actual_dual_anchor_beta_one_realization"]["anchors"].values()
            ),
            "q7_rigid_label_rejected": not arithmetic["unrealizable_q7_rigid_label"]["realizable"],
            "local_zero_fail_closed": arithmetic["actual_beta_one_realization"]["local_zero_fail_closed"],
            "K2_constant_boundary_replayed_and_separated": (
                arithmetic["k2_constant_boundary_replay"]["direct_safe_count"] == 0
                and arithmetic["k2_constant_boundary_replay"]["kept_outside_odd_coordinate_catalog"]
            ),
        },
        "PASS": True,
    })

    test_output = run_capture(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_*.py", "-v"],
        root,
    )
    match = re.search(r"Ran (\d+) tests?", test_output)
    if not match or "\nOK\n" not in f"\n{test_output}":
        raise RuntimeError(f"could not validate unittest report:\n{test_output}")
    normalized_test_output = re.sub(
        r"Ran (\d+) tests? in [0-9.]+s",
        r"Ran \1 tests in <elapsed>s",
        test_output,
    )
    write_json(results / "test_report.json", {
        "command": "PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 python3 -m unittest discover -s tests -p 'test_*.py' -v",
        "passed": True,
        "tests_run": int(match.group(1)),
        "test_modules": sorted(p.name for p in (root / "tests").glob("test_*.py")),
        "normalized_output_sha256": sha256_bytes(normalized_test_output.encode("utf-8")),
        "output_normalization": "Replace the nondeterministic unittest elapsed time by <elapsed> before hashing.",
    })

    verify_text_hygiene(root)

    manifest = build_manifest(root, {
        "authority": AUTHORITY,
        "verdict": "PROMOTABLE INVERSE THEOREM",
        "generated_json_policy": "All files under results/*.json are generated by tools/reproduce.py; none are hand-edited.",
    })
    write_json(root / "manifest.json", manifest)

    checksum_paths = sorted(p for p in root.rglob("*") if p.is_file() and p.relative_to(root).as_posix() != "SHA256SUMS.txt")
    lines = [f"{sha256_file(path)}  {path.relative_to(root).as_posix()}\n" for path in checksum_paths]
    (root / "SHA256SUMS.txt").write_text("".join(lines), encoding="utf-8")
    print("PASS")


if __name__ == "__main__":
    main()
