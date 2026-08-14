#!/usr/bin/env python3
"""Semantic corruption suite; every named mutation must be rejected."""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Callable

TOOLS = Path(__file__).resolve().parents[1] / "tools"


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def save(path: Path, value) -> None:
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def jsonl(path: Path):
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line]


def save_jsonl(path: Path, rows) -> None:
    path.write_text("".join(json.dumps(row, sort_keys=True, separators=(",", ":")) + "\n" for row in rows), encoding="utf-8")


def rehash(results: Path, name: str) -> None:
    metadata = load(results / "metadata.json")
    metadata["artifact_sha256"][name] = hashlib.sha256((results / name).read_bytes()).hexdigest()
    save(results / "metadata.json", metadata)


def mutate_json(results: Path, name: str, action: Callable) -> None:
    path = results / name
    value = load(path)
    action(value)
    save(path, value)
    rehash(results, name)


def mutate_jsonl(results: Path, name: str, action: Callable) -> None:
    path = results / name
    rows = jsonl(path)
    action(rows)
    save_jsonl(path, rows)
    rehash(results, name)


def mutations():
    return [
        ("missing_prior_interval", lambda d: mutate_json(d, "prior_evaluation_registry.json", lambda x: x["interval_union"].pop())),
        ("missing_sparse_historical_point", lambda d: mutate_json(d, "prior_evaluation_registry.json", lambda x: x["sparse_points"].pop())),
        ("shortlist_mutation", lambda d: mutate_json(d, "per_entry_multiplicity.json", lambda x: x["entries"][0].__setitem__("t", x["entries"][0]["t"] + 1))),
        ("unauthorized_q_or_t", lambda d: mutate_jsonl(d, "occupied_fresh_class_manifest.jsonl", lambda x: x[0]["descriptions"][0].__setitem__("t", x[0]["q2"]))),
        ("wrong_base_mask", lambda d: mutate_json(d, "per_entry_multiplicity.json", lambda x: x["entries"][0].__setitem__("base_mask_digest", "00" * 32))),
        ("wrong_union_mask", lambda d: mutate_jsonl(d, "occupied_fresh_class_manifest.jsonl", lambda x: x[0]["descriptions"][0].__setitem__("resulting_union_mask_digest", "00" * 32))),
        ("CRT_congruence_corruption", lambda d: mutate_jsonl(d, "occupied_fresh_class_manifest.jsonl", lambda x: x[0].__setitem__("class_residue", x[0]["class_residue"] + 1))),
        ("duplicate_class_not_deduplicated", lambda d: mutate_jsonl(d, "occupied_fresh_class_manifest.jsonl", lambda x: x.append(dict(x[0])))),
        ("duplicate_integer_not_deduplicated", lambda d: mutate_jsonl(d, "integer_deduplication_manifest.jsonl", lambda x: x.append(dict(x[0])))),
        ("previously_evaluated_marked_fresh", lambda d: mutate_jsonl(d, "occupied_fresh_class_manifest.jsonl", lambda x: next(r for r in x if r["previously_evaluated"]).__setitem__("fresh", True))),
        ("activation_cell_boundary_corruption", lambda d: mutate_json(d, "geometry_diagnostics.json", lambda x: x["activation_cell"].__setitem__(0, x["activation_cell"][0] + 1))),
        ("member_count_greater_than_one", lambda d: mutate_jsonl(d, "occupied_fresh_class_manifest.jsonl", lambda x: x[0].__setitem__("member_count", 2))),
        ("adaptive_entry_deletion", lambda d: mutate_json(d, "per_entry_multiplicity.json", lambda x: x["metrics"].pop())),
        ("non_deterministic_panel_selection", lambda d: mutate_json(d, "design_C_full_sparse_census.json", lambda x: x["classes"].__setitem__(slice(0, 2), list(reversed(x["classes"][:2]))))),
        ("accidental_forbidden_evaluator_invocation", lambda d: mutate_json(d, "feasibility_report.json", lambda x: x["forbidden_activity"].__setitem__("T_evaluator_called", True))),
    ]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, required=True)
    parser.add_argument("--results", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records = []
    with tempfile.TemporaryDirectory(prefix="a303656_p5_corrupt_") as temporary:
        base = Path(temporary)
        for index, (name, mutation) in enumerate(mutations()):
            target = base / f"case_{index:02d}"
            shutil.copytree(args.results, target)
            mutation(target)
            result = subprocess.run([
                sys.executable, str(TOOLS / "verifier.py"), "--root", str(args.root.resolve()), "--results", str(target),
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, env={**__import__("os").environ, "PYTHONDONTWRITEBYTECODE": "1"})
            records.append({"name": name, "return_code": result.returncode, "rejected": result.returncode != 0, "stderr_last_line": result.stderr.strip().splitlines()[-1] if result.stderr.strip() else ""})
    report = {"schema": "a303656-p5-sparse-corruption-tests-v1", "test_count": len(records), "all_rejected": all(r["rejected"] for r in records), "tests": records}
    save(args.output.resolve(), report)
    print(json.dumps({"test_count": len(records), "all_rejected": report["all_rejected"]}, sort_keys=True))
    return 0 if report["all_rejected"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
