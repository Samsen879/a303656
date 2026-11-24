#!/usr/bin/env python3
"""Bind the fixed R2 corpus and independently replay all R3 optimum ties."""
from __future__ import annotations

import argparse
from collections import Counter
import csv
import hashlib
import json
from pathlib import Path
import subprocess

from ajt5_ablation import diagnostics, domain, optimum_dp, optimum_enumeration
from ajt5_gates import certificate, margins, summary, verify_gate
from ajt5_modular import (child_summary, forbidden_residues, residue_data,
                          strict_negative, verify_residue_gate)
from verify_ajt5_gates import make_complete, rows, verify_directory as verify_r2
from verify_ajt5_reports import check_certificate, exponents, require

ROOT = Path(__file__).resolve().parents[1]
BASE = "10d9b86b5183aac65e4755d439ea018a17fa00f5"
R2 = ROOT / "analysis/ajt5_gate_certificates/results"
SOURCES = ["src/ajt5_ablation.py", "src/ajt5_modular.py", "src/verify_ajt5_ablation.py",
           "scripts/run_ajt5_ablation.py", "tests/ajt5_ablation_tests.py"]


def canonical(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def frozen_inputs():
    """Bind bytes to immutable #52, then validate its arithmetic certificates.

    The key roster's completeness comes from R2's full replay; R3 checks that
    exact roster. No reference ablation count participates in input selection.
    """
    bindings = {}
    for name in ("critical.csv", "certificates.jsonl", "manifest.json", "receipt.json"):
        path = R2 / name
        relative = path.relative_to(ROOT).as_posix()
        original = subprocess.check_output(["git", "show", BASE + ":" + relative], cwd=ROOT)
        require(path.read_bytes() == original, "immutable R2 bytes changed: " + name)
        bindings[relative] = digest(path)
    verify_r2(R2)
    selected = rows(R2 / "critical.csv")
    certs = {x["n"]: x for x in map(json.loads, (R2 / "certificates.jsonl").read_text().splitlines())}
    for row in selected:
        m, r, d, e = [row[k] for k in ("m", "r", "D", "E")]
        require(check_certificate(certs[m]) == (m, d), "parent arithmetic binding")
        require(check_certificate(certs[5 * m + r]) == (5 * m + r, e), "child arithmetic binding")
        require(margins(summary(m, exponents(d), exponents(e)))["PB2"] == 1, "PB2 cohort")
    return selected, certs, bindings


def state_record(m, r, d, e, k, a, b):
    return dict(m=m, r=r, deletions=k, A=a, B=b, **diagnostics(m, d, e, a, b))


def compute(selected, emit=None):
    hist, kinds, per_key = Counter(), Counter(), []
    total = bridges = recovered = weighted = 0
    all_hash = hashlib.sha256()
    residual_hash = hashlib.sha256()
    residual_keys, maxima = Counter(), []
    for row in selected:
        m, r, d, e = [row[k] for k in ("m", "r", "D", "E")]
        result = optimum_dp(m, d, e)
        oracle = optimum_enumeration(m, d, e)
        if result != oracle:
            difference = sorted(set(result[1]) ^ set(oracle[1]))
            raise ValueError("DP/enumeration discrepancy: " + json.dumps(
                {"m": m, "r": r, "D": d, "E": e,
                 "dp_cost": result[0], "oracle_cost": oracle[0],
                 "dp_ties": len(result[1]), "oracle_ties": len(oracle[1]),
                 "first_differing_pair": difference[:1]}, sort_keys=True))
        k, pairs = result
        keyhash, keybridges, keyrecovered = hashlib.sha256(), 0, 0
        for a, b in pairs:
            z = state_record(m, r, d, e, k, a, b)
            require(z["gF"] <= 0 and max(z["h"]) <= 0, "optimum feasibility")
            # Direct retained-edge diagnostic; never used as a feasibility gate.
            has_bridge = z["bridge"]
            recovery = max(z["parent_negative_margins"] + [z["gFH"]]) > 0
            require(not recovery or has_bridge, "complement recovery unsound")
            weight_pass = max(z["weight_gaps"]) > 0
            require(not weight_pass or has_bridge, "weighted recovery unsound")
            total += 1; bridges += has_bridge; keybridges += has_bridge
            recovered += recovery; keyrecovered += recovery
            raw = canonical(z)
            all_hash.update(raw); keyhash.update(raw)
            if emit is not None:
                emit.write(raw)
            if has_bridge and not recovery:
                residual_keys[(m, r)] += 1
                residual_hash.update(raw)
                weighted += weight_pass
        hist[k] += 1
        kind = "all_no_bridge" if not keybridges else "all_bridge" if keybridges == len(pairs) else "mixed"
        kinds[kind] += 1
        per_key.append(dict(m=m, r=r, deletions=k, states=len(pairs), bridges=keybridges,
                            complement_recovered=keyrecovered, states_sha256=keyhash.hexdigest()))
        if maxima and k > maxima[0]["deletions"]:
            maxima = []
        if not maxima or k >= maxima[0]["deletions"]:
            L, F = domain(m, d, e)
            maxima.append(dict(m=m, r=r, L=L, D=d, E=e, F36=F, deletions=k,
                               states=len(pairs), bridges=keybridges))
    report = {"schema": 1, "a303656": "UNRESOLVED", "base": BASE,
              "corpus": "R2 PB2 margin-one rows; row-local artificial ablation",
              "keys": len(selected), "deletion_histogram": {str(k): v for k, v in sorted(hist.items())},
              "sum_minimal_deletions": sum(k * v for k, v in hist.items()),
              "optimal_states": total, "retained_bridge_states": bridges, "no_retained_bridge_states": total - bridges,
              "key_classes": dict(kinds), "maximum_deletion_rows": maxima,
              "complement_recovered": recovered, "complement_residual": bridges - recovered,
              "residual_keys": [dict(m=m, r=r, states=v) for (m, r), v in sorted(residual_keys.items())],
              "residual_weight_recovered": weighted, "states_sha256": all_hash.hexdigest(),
              "residual_states_sha256": residual_hash.hexdigest(),
              "oracle": "sweep DP versus full Cartesian set enumeration, minimal cost AND every tied mask pair",
              "all_nonpositive_gate_results": "UNKNOWN; omitted positive bits are not negative facts"}
    return report, per_key


def controls(certs):
    m, r = 7_721_762, 3
    parent, child = certs[m], certs[5 * m + r]
    D, E = exponents(parent["mask"]), exponents(child["mask"])
    require(3 in E, "control child bit")
    sides = [{"n": c["n"], "witnesses": [[i] + c["by_d"][i] for i in sorted(bits)]}
             for c, bits in ((parent, D), (child, E - {3}))]
    lower = certificate(m, r, *sides, mode="lower")
    result = verify_gate(lower)
    require(result["status"] == "UNKNOWN" and bool(D & ((E - {3}) | {i - 1 for i in E - {3}})),
            "single-child-bit retained-bridge control")
    small = {n: make_complete(n) for n in (2, 10, 50, 82, 410)}
    require(exponents(small[2]["mask"]) == {0} and exponents(small[10]["mask"]) == {0, 1}, "global-mask control")
    # A(2) must be {0}. gF=|B(10)| forces B(10)=empty at row (2,0).
    # The same global mask at row (10,0) would be required to be nonempty.
    require((2, 0) in {(x["m"], x["r"]) for x in rows(R2 / "critical.csv")}
            and (10, 0) in {(x["m"], x["r"]) for x in rows(R2 / "critical.csv")}, "global keys in roster")
    A, B, H = {0}, {0, 1}, {3}
    sides = [{"n": n, "witnesses": [[i] + small[n]["by_d"][i] for i in sorted(bits)]}
             for n, bits in ((82, A), (410, B))]
    old = margins(summary(82, A, B))
    modular = {"schema": 1, "m": 82, "r": 0, "parent": sides[0], "child": sides[1], "modulus": 144,
               "negative_exponents": sorted(H), "summary": child_summary(82, A, B, H)}
    require(old["gF"] == old["gB"] == old["PB36"] == 0, "old zero margins")
    require(strict_negative(285, 144) and verify_residue_gate(modular)["status"] == "SUFFICIENT_BRIDGE", "mod144 recovery")
    s2, orbit, start = residue_data(144)
    return {"single_child_bit": {"complete_reference": {"m": m, "r": r, "D": parent["mask"], "E": child["mask"]},
                                  "withheld_child_bit": 3, "lower_certificate": lower, "result": result,
                                  "retained_bridge": True},
            "shared_global_mask_infeasible": {"certificates": [small[n] for n in (2, 10, 50)],
                                              "keys": [[2, 0], [10, 0]],
                                              "reason": "A(2)={0}; gF<=0 forces B(10)=empty, contradicting nonempty A(10) under shared mask identity"},
            "mod144": {"s2": sorted(s2), "three_orbit": list(orbit), "cycle_start": start,
                       "forbidden_residues": list(forbidden_residues(144)), "certificate": modular,
                       "old_margins": old, "result": verify_residue_gate(modular),
                       "t": 285, "residue": 285 % 144}}


def compare(report):
    # Supplied Web expectations enter ONLY after the numerical results exist.
    expected = {"deletion_histogram": {"1": 136, "2": 228, "3": 169, "4": 1},
                "sum_minimal_deletions": 1103, "optimal_states": 3232, "retained_bridge_states": 2370,
                "no_retained_bridge_states": 862,
                "key_classes": {"all_no_bridge": 160, "all_bridge": 166, "mixed": 208},
                "maximum_deletion_rows": [{"m": 5644037, "r": 1, "L": 9, "D": 877, "E": 1073,
                                            "F36": 130, "deletions": 4, "states": 106, "bridges": 90}],
                "complement_recovered": 2346, "complement_residual": 24,
                "residual_keys": [{"m": 5644037, "r": 1, "states": 24}], "residual_weight_recovered": 24}
    observed = {key: report[key] for key in expected}
    return {"expected": expected, "observed": observed, "status": "MATCH" if expected == observed else "MISMATCH"}


def verify_directory(directory):
    receipt = json.loads((directory / "receipt.json").read_text())
    manifest = json.loads((directory / "manifest.json").read_text())
    require(set(manifest) == {"report.json", "keys.csv", "controls.json", "comparison.json", "receipt.json"}, "artifact file coverage")
    require({p.name for p in directory.iterdir()} == set(manifest) | {"manifest.json"}, "unexpected artifact")
    for name, value in manifest.items():
        require(digest(directory / name) == value, "artifact hash: " + name)
    require(set(receipt["sources_sha256"]) == set(SOURCES), "source coverage")
    for name, value in receipt["sources_sha256"].items():
        require(digest(ROOT / name) == value, "source changed: " + name)
    selected, certs, bindings = frozen_inputs()
    require(receipt["base"] == BASE and receipt["input_sha256"] == bindings, "input receipt")
    report, per_key = compute(selected)
    require(json.loads((directory / "report.json").read_text()) == report, "report replay")
    with (directory / "keys.csv").open(newline="") as f:
        actual = list(csv.DictReader(f))
    require(actual == [{k: str(v) for k, v in row.items()} for row in per_key], "complete per-key replay")
    require(json.loads((directory / "controls.json").read_text()) == controls(certs), "controls replay")
    comparison = compare(report)
    require(json.loads((directory / "comparison.json").read_text()) == comparison, "comparison observations")
    require(comparison["status"] == "MATCH", "preserved Web expectation mismatch")
    return {"keys": report["keys"], "states": report["optimal_states"], "states_sha256": report["states_sha256"],
            "comparison": comparison["status"], "a303656": "UNRESOLVED"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_directory(args.directory), indent=2, sort_keys=True))
