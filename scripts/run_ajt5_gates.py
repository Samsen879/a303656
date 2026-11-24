#!/usr/bin/env python3
"""Generate R2 evidence from a fresh, successful two-engine R1 input replay.

R1's expected historical comparison exit is 2. This program stops if any new
arithmetic, certificate, hash, coverage or explicitly supplied R2 check differs.
No parent bound greater than 10,000,000 is accepted.
"""
from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ajt5_gates import certificate, exponents, verify_gate  # noqa: E402
from verify_ajt5_gates import (R1, SOURCES, accounting, check_ledger, digest, ledger,  # noqa: E402
                                make_complete, rows, verify_directory)
from verify_ajt5_reports import read_rows, require, verify_directory as verify_r1  # noqa: E402
from run_ajt5_audit import timed  # noqa: E402


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input-work", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    args = parser.parse_args()
    work, input_work = args.work_dir.resolve(), args.input_work.resolve()
    require(not work.exists(), "choose a fresh R2 work directory")
    work.mkdir(parents=True)
    evidence = work / "evidence"
    evidence.mkdir()
    # Input certification precedes R2. Canonical bytes must also match the
    # preserved R1 receipt, without rewriting its historical comparison.
    input_receipt = json.loads((input_work / "evidence/replay_receipt.json").read_text())
    verify_r1(input_work / "evidence")
    require(input_receipt["max_m"] == 10_000_000, "original R1 bound required")
    require(input_receipt["raw_files"] == json.loads((R1 / "replay_receipt.json").read_text())["raw_files"], "R1 input changed")
    table = input_work / "primary/masks.u16le"
    require({"bytes": table.stat().st_size, "sha256": digest(table)} == input_receipt["raw_files"]["masks.u16le"], "actual input mask hash")
    compiler = "g++"
    metrics = {"build": timed([compiler, "-std=c++17", "-O3", "-Wall", "-Wextra", "-Werror",
                                ROOT / "src/ajt5_gate_scan.cpp", "-o", work / "scan"], work / "build.log")}
    metrics["scan"] = timed([work / "scan", 10_000_000, table, evidence], work / "scan.log")
    critical, nearest = rows(evidence / "critical.csv"), rows(evidence / "nearest36.csv")
    hard = read_rows(R1 / "hard_cases.csv")
    targets = {784, 3920}
    for x in critical + nearest:
        targets.update((x["m"], 5 * x["m"] + x["r"]))
    for x in hard:
        targets.update((x["m"], x["n"]))
    # Independent arithmetic construction, never trusting the native masks.
    indexed = {}
    with (evidence / "certificates.jsonl").open("w") as f:
        for n in sorted(targets):
            record = make_complete(n)
            indexed[n] = record
            f.write(json.dumps(record, separators=(",", ":")) + "\n")
    write_json(evidence / "accounting.json", accounting(hard))
    hard2 = [x for x in hard if x["gate2_hard"]]
    ledgers = ledger({n for x in hard2 for n in (x["m"], x["n"])})
    import csv
    with (evidence / "hard_ledger.csv").open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ledgers[0]))
        writer.writeheader(); writer.writerows(ledgers)
    complete, lower = [], []
    for x in hard2:
        m, r, n = x["m"], x["r"], x["n"]
        complete.append(certificate(m, r, indexed[m], indexed[n]))
        sides = []
        for value in (m, n):
            rec = indexed[value]
            sides.append({"n": value, "witnesses": [[d] + rec["by_d"][d] for d in sorted(exponents(rec["mask"]))]})
        # Greedily make a small partial positive certificate, accepting solely
        # on PB2 counts after every proposed vertex deletion.
        for side in (0, 1):
            for entry in sides[side]["witnesses"][:]:
                trial = copy.deepcopy(sides)
                trial[side]["witnesses"].remove(entry)
                cert = certificate(m, r, *trial, mode="lower")
                if verify_gate(cert).get("margins", {}).get("PB2", 0) > 0:
                    sides = trial
        lower.append(certificate(m, r, *sides, mode="lower"))
    write_json(evidence / "examples.json", {"complete": complete, "lower": lower})
    r1head = "9e371d1ef47138de880208eebf4a81e276aa80c1"
    receipt = {"schema": 1, "r1_head": r1head,
               "checkout_at_generation": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
               "input_scope": "shared R1 table, freshly rebuilt by two independent native membership engines",
               "postprocessing_scope": "all nonvacuous pairs; fast bit arithmetic and independent literal exponent walk compared at every pair",
               "selected_scope": "independent exact arithmetic masks; selected rows only, not full-scan coverage",
               "input_masks": input_receipt["raw_files"]["masks.u16le"],
               "r1_replay_metrics": input_receipt["metrics"], "r1_reference_exit": 2,
               "r1_setup_diagnostic": "First local replay completed computations but receipt generation failed: origin/main missing. Ref fetched, then both engines rerun in a fresh directory; no numerical discrepancy.",
               "r1_replay_logs": json.loads((input_work / "evidence/execution_logs.json").read_text()),
               "metrics": metrics, "python": platform.python_version(), "platform": platform.platform(),
               "compiler": subprocess.check_output([compiler, "--version"], text=True).splitlines()[0],
               "cpu_model": input_receipt["cpu_model"], "single_thread": True,
               "sources_sha256": {name: digest(ROOT / name) for name in SOURCES},
               "r1_manifest_sha256": digest(R1 / "manifest.json"),
               "ledger": check_ledger(ledgers, {n for x in hard2 for n in (x["m"], x["n"])}),
               "historical_reason": "NOT_ESTABLISHED", "a303656": "UNRESOLVED"}
    write_json(evidence / "receipt.json", receipt)
    write_json(evidence / "logs.json", {name: (work / (name + ".log")).read_text() for name in ("build", "scan")})
    # Reference observations enter only after computation and preservation.
    s = json.loads((evidence / "summary.json").read_text())
    observed = {"PB2_min": min(map(int, s["PB2"])), "PB2_margin1": sum(s["PB2"].get("1", [])),
                "lambda_below3": accounting(hard)["lambda_below_3_by_r"],
                "delta36_frozen220": accounting(hard)["delta36_histogram"], "ledger": receipt["ledger"]}
    expected = {"PB2_min": 1, "PB2_margin1": 534, "lambda_below3": [21, 5, 7, 12, 2],
                "delta36_frozen220": {"1": 9, "2": 37, "3": 122, "4": 50, "5": 2},
                "ledger": {"alternatives": 469, "square_witnesses": 45, "positive_odd_valuation_blockers": 424, "zero_residual_witnesses": 0}}
    comparison = {"observed": observed, "expected": expected, "status": "MATCH" if observed == expected else "MISMATCH"}
    write_json(evidence / "comparison.json", comparison)
    write_json(evidence / "manifest.json", {p.name: digest(p) for p in sorted(evidence.iterdir()) if p.name != "manifest.json"})
    require(observed == expected, "R2 mismatch preserved at " + str(evidence))
    print(json.dumps(verify_directory(evidence), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
