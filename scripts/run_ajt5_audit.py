#!/usr/bin/env python3
"""Rebuild, replay twice, certify listed masks, then compare reference gates.

Exit 2 means computations and certificates agree but a supplied reference gate
does not. All bounded evidence is preserved. No scan exceeds m=10,000,000.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import platform
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verify_ajt5_reports import (FIELDS, create_certificates, describe,  # noqa: E402
                               exponents, hard_profile, read_rows, require, verify_directory)


def digest(path):
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def timed(command, log, cwd=ROOT):
    start = time.perf_counter()
    with log.open("w") as f:
        process = subprocess.Popen([str(x) for x in command], cwd=cwd, stdout=f, stderr=subprocess.STDOUT)
        _, status, usage = os.wait4(process.pid, 0)
        process.returncode = os.waitstatus_to_exitcode(status)
    result = {"command": [str(x) for x in command], "returncode": process.returncode,
              "wall_seconds": round(time.perf_counter() - start, 6),
              "user_seconds": usage.ru_utime, "system_seconds": usage.ru_stime,
              "max_rss_kib_linux": usage.ru_maxrss}
    require(process.returncode == 0, f"command failed: {command}; see {log}")
    return result


def reference_comparison(summary, probes):
    # These are ONLY comparison gates, evaluated after independent computation.
    # They never enter either native engine, mask generation, or certificates.
    observed = {key: summary[key] for key in ("combined_failures", "same_minima", "plus_minima", "gate1_hard", "gate2_hard")}
    expected = {"combined_failures": [0] * 5, "same_minima": [5, 3, 2016, 16, 112],
                "plus_minima": [4, 20, 16, 7963079, 5], "gate1_hard": [106, 12, 43, 38, 21],
                "gate2_hard": [32, 4, 1, 4, 6]}
    mismatch = {key: {"reference": expected[key], "observed": value}
                for key, value in observed.items() if value != expected[key]}
    for m, r, D, E in [(1676569, 0, {1, 3, 7}, {0, 4, 6}),
                        (7963079, 3, {0, 1, 2, 4, 6, 7, 8, 9}, {0, 4, 6})]:
        row = next(row for row in probes if row["m"] == m and row["r"] == r)
        actual = [sorted(exponents(row["parent_mask"])), sorted(exponents(row["child_mask"]))]
        if actual != [sorted(D), sorted(E)]:
            mismatch[f"probe_{m}_{r}"] = {"reference": [sorted(D), sorted(E)], "observed": actual}
    return {"status": "DISCREPANCY" if mismatch else "MATCH", "differences": mismatch,
            "reference_counts": expected, "observed_counts": observed,
            "scope": "reference observations, not mathematical axioms; enlargement stopped on discrepancy"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--max-m", type=int, default=10_000_000)
    parser.add_argument("--work-dir", type=Path, default=ROOT / "reproduce_work/ajt5")
    args = parser.parse_args()
    require(2 <= args.max_m <= 10_000_000, "bounded MAX_M")
    work = args.work_dir.resolve()
    # Do not replace prior runs; reuse requires an explicitly new directory.
    require(not work.exists(), "work directory already exists; choose a new path")
    work.mkdir(parents=True)
    evidence, primary, secondary = work / "evidence", work / "primary", work / "secondary"
    evidence.mkdir()
    metrics = {}
    compiler = os.environ.get("CXX", "g++")
    for name, source in [("scan", "ajt5_scan.cpp"), ("valuation", "ajt5_valuation_replay.cpp")]:
        metrics["build_" + name] = timed([compiler, "-std=c++17", "-O3", "-Wall", "-Wextra", "-Werror",
                                         ROOT / "src" / source, "-o", work / name], work / ("build_" + name + ".log"))
    metrics["scan"] = timed([work / "scan", args.max_m, primary], work / "scan.log")
    metrics["valuation"] = timed([work / "valuation", args.max_m, primary, secondary], work / "valuation.log")
    first = json.loads((primary / "summary.json").read_text())
    second = json.loads((secondary / "summary.json").read_text())
    first_comparable, second_comparable = dict(first), dict(second)
    first_comparable.pop("engine"); second_comparable.pop("engine")
    require(first_comparable == second_comparable, "independent summary disagreement")
    for name in ("hard_cases.csv", "minima.csv", "failures.csv"):
        require((primary / name).read_bytes() == (secondary / name).read_bytes(), "independent row disagreement: " + name)
    for name in ("summary.json", "hard_cases.csv", "minima.csv", "failures.csv"):
        shutil.copyfile(primary / name, evidence / name)
    with (primary / "masks.u16le").open("rb") as f, (evidence / "probes.csv").open("w", newline="") as g:
        writer = csv.DictWriter(g, fieldnames=FIELDS)
        writer.writeheader()
        for m, r in [(1676569, 0), (7963079, 3)]:
            if m > args.max_m:
                continue
            values = []
            for n in (m, 5 * m + r):
                f.seek(2 * n)
                data = f.read(2)
                require(len(data) == 2, "probe bounds")
                values.append(int.from_bytes(data, "little"))
            writer.writerow(describe(m, r, *values))
    start = time.perf_counter()
    create_certificates(evidence)
    verified = verify_directory(evidence, False)
    profile = hard_profile(read_rows(evidence / "hard_cases.csv"),
                           [json.loads(line) for line in (evidence / "certificates.jsonl").read_text().splitlines()])
    (evidence / "hard_profile.json").write_text(json.dumps(profile, indent=2, sort_keys=True) + "\n")
    metrics["certificate_creation_and_check"] = {"wall_seconds": round(time.perf_counter() - start, 6)}
    gate_result = (reference_comparison(first, read_rows(evidence / "probes.csv")) if args.max_m == 10_000_000
                   else {"status": "NOT_APPLICABLE", "scope": "full reference gates apply only at m=10000000"})
    (evidence / "reference_comparison.json").write_text(json.dumps(gate_result, indent=2, sort_keys=True) + "\n")
    logs = {phase: (work / (phase + ".log")).read_text()
            for phase in ("build_scan", "build_valuation", "scan", "valuation")}
    (evidence / "execution_logs.json").write_text(json.dumps(logs, indent=2, sort_keys=True) + "\n")
    receipt = {"schema": 1, "base_commit": subprocess.check_output(["git", "rev-parse", "origin/main"], cwd=ROOT, text=True).strip(),
               "platform": platform.platform(), "machine": platform.machine(), "logical_cpus": os.cpu_count(),
               "python": platform.python_version(),
               "cpu_model": next((line.split(":", 1)[1].strip() for line in Path("/proc/cpuinfo").read_text().splitlines()
                                   if line.startswith("model name")), "unknown"),
               "compiler": subprocess.check_output([compiler, "--version"], text=True).splitlines()[0],
               "single_thread_per_engine": True, "max_m": args.max_m, "max_n": first["max_n"],
               "metrics": metrics, "selected_certificate_verification": verified,
               "full_entrywise_agreement": {"entries_each": first["max_n"] + 1, "tables": ["S2", "T", "D"]},
               "raw_files": {name: {"bytes": (primary / name).stat().st_size, "sha256": digest(primary / name)}
                             for name in ("s2.bits", "t.bits", "masks.u16le")},
               "sources_sha256": {str(path.relative_to(ROOT)): digest(path) for path in
                                  [ROOT / "src/ajt5_scan.cpp", ROOT / "src/ajt5_valuation_replay.cpp",
                                   ROOT / "src/verify_ajt5_reports.py", Path(__file__).resolve()]},
               "reference_status": gate_result["status"], "a303656": "UNRESOLVED"}
    (evidence / "replay_receipt.json").write_text(json.dumps(receipt, indent=2, sort_keys=True) + "\n")
    manifest = {"schema": 1, "files": {p.name: digest(p) for p in sorted(evidence.iterdir()) if p.is_file()}}
    (evidence / "manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n")
    verify_directory(evidence)
    print(json.dumps({"replay": "MATCH", "certificates": verified, "reference": gate_result, "evidence": str(evidence)}, indent=2, sort_keys=True))
    return 2 if gate_result["status"] == "DISCREPANCY" else 0


if __name__ == "__main__":
    raise SystemExit(main())
