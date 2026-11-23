#!/usr/bin/env python3
"""Recheck stored R2 evidence with literal sets and exact arithmetic.

Selected certificates certify selected rows, not exhaustive scan coverage.
Full coverage requires rebuilding R1 inputs and the R2 native postprocessor.
"""
from __future__ import annotations

import argparse
from collections import Counter
import csv
from functools import lru_cache
import hashlib
import json
import math
from pathlib import Path

from ajt5_gates import (certificate, forbidden36, lambda_dp, margins, summary,
                        verify_gate)
from verify_ajt5_reports import (check_certificate, exponents, is_prime,
                                 load_certificates, powers, read_rows, require)

ROOT = Path(__file__).resolve().parents[1]
R1 = ROOT / "analysis/ajt5_exact_audit/results"
SOURCES = ["src/ajt5_gates.py", "src/ajt5_gate_scan.cpp", "src/verify_ajt5_gates.py",
           "scripts/run_ajt5_gates.py", "tests/ajt5_gate_tests.py"]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def rows(path):
    with path.open(newline="") as f:
        return [{key: int(value) for key, value in row.items()} for row in csv.DictReader(f)]


def describe(row):
    m, r, d, e = (row[k] for k in ("m", "r", "D", "E"))
    s = summary(m, exponents(d), exponents(e))
    v = margins(s)
    return dict(m=m, r=r, L=s["L"], D=d, E=e, gF=v["gF"], gB=v["gB"],
                k0=v["kappa"][0], k1=v["kappa"][1], PB2=v["PB2"],
                delta36=v["delta36"], q0=v["parity36"][0], q1=v["parity36"][1], PB36=v["PB36"])


@lru_cache(maxsize=1)
def primes():
    return [p for p in range(3, math.isqrt(50_000_004) + 1, 4) if is_prime(p)]


def alternative(n, d, c):
    x = n - 5 ** d - 3 ** c
    require(x >= 0, "admissible residual")
    if x:
        for p in primes():
            if p > x:
                break
            q, v = x, 0
            while q % p == 0:
                q //= p
                v += 1
            if v % 2:
                return {"n": n, "d": d, "c": c, "residual": x, "a": -1, "b": -1, "p": p, "v": v}
    # Independent actual square witness, including (0,0) at residual zero.
    a, b = 0, math.isqrt(x)
    while a <= b:
        total = a * a + b * b
        if total == x:
            return {"n": n, "d": d, "c": c, "residual": x, "a": a, "b": b, "p": 0, "v": 0}
        if total < x:
            a += 1
        else:
            b -= 1
    # Large prime factors can exceed sqrt(CAP); derive one by trial division.
    q = x
    for p in range(2, math.isqrt(x) + 1):
        if p * p > q:
            break
        v = 0
        while q % p == 0:
            q //= p
            v += 1
        if p % 4 == 3 and v % 2:
            return {"n": n, "d": d, "c": c, "residual": x, "a": -1, "b": -1, "p": p, "v": v}
    require(q % 4 == 3 and is_prime(q), "factor/witness disagreement")
    return {"n": n, "d": d, "c": c, "residual": x, "a": -1, "b": -1, "p": q, "v": 1}


def make_complete(n):
    mask, entries = 0, []
    for d, five in enumerate(powers(5, n)):
        blockers = []
        for c, _ in enumerate(powers(3, n - five)):
            a = alternative(n, d, c)
            if a["p"] == 0:
                entries.append([a["a"], a["b"], c]); mask |= 1 << d
                break
            blockers.append([a["p"], a["v"]])
        else:
            entries.append(blockers)
    record = {"n": n, "mask": mask, "by_d": entries}
    check_certificate(record)
    return record


def ledger(targets):
    return [alternative(n, d, c) for n in sorted(targets)
            for d, five in enumerate(powers(5, n))
            for c, _ in enumerate(powers(3, n - five))]


def check_ledger(actual, targets):
    expected_keys = [(n, d, c) for n in sorted(targets) for d, five in enumerate(powers(5, n))
                     for c, _ in enumerate(powers(3, n - five))]
    require([(a["n"], a["d"], a["c"]) for a in actual] == expected_keys, "ledger full admissible coverage")
    success = blocked = zeros = 0
    for row in actual:
        n, d, c, x, a, b, p, v = [row[k] for k in ("n", "d", "c", "residual", "a", "b", "p", "v")]
        require(x == n - 5 ** d - 3 ** c and x >= 0, "ledger residual")
        if p == 0:
            require(a >= 0 and b >= 0 and a * a + b * b == x and v == 0, "ledger square witness")
            success += 1; zeros += int(x == 0)
        else:
            require(x > 0 and a == b == -1 and p % 4 == 3 and is_prime(p) and v > 0, "ledger blocker domain")
            q, exact = x, 0
            while q % p == 0:
                q //= p; exact += 1
            require(exact == v and v % 2 == 1, "ledger exact odd valuation")
            blocked += 1
    return {"alternatives": len(actual), "square_witnesses": success, "positive_odd_valuation_blockers": blocked,
            "zero_residual_witnesses": zeros}


def accounting(hard):
    hist, survivors, delta, profiles = Counter(), [0] * 5, Counter(), []
    for row in hard:
        D, E = exponents(row["parent_mask"]), exponents(row["child_mask"])
        v = margins(summary(row["m"], D, E))
        lam = lambda_dp(row["L"], len(D), row["runs"], E)
        hist[str(lam)] += 1
        survivors[row["r"]] += int(lam < 3)
        delta[str(v["delta36"])] += 1
        profiles.append({"m": row["m"], "r": row["r"], "lambda": lam, "delta36": v["delta36"]})
    return {"scope": "frozen 220 first-gate survivors only", "rows": profiles,
            "lambda_histogram": dict(hist), "lambda_below_3_by_r": survivors,
            "delta36_histogram": dict(delta), "historical_original_gate_reason": "NOT_ESTABLISHED",
            "historical_original_gate_roster": "NOT_RECOVERED",
            "historical_reported_distribution": [32, 4, 1, 4, 6],
            "literal_old_gates_distribution": [sum(x["r"] == r and x["gate2_hard"] for x in hard) for r in range(5)]}


def verify_directory(directory, manifest=True):
    receipt = json.loads((directory / "receipt.json").read_text())
    if manifest:
        bound = json.loads((directory / "manifest.json").read_text())
        require(set(bound) == {p.name for p in directory.iterdir() if p.is_file()} - {"manifest.json"}, "R2 file coverage")
        for name, expected in bound.items():
            require(Path(name).name == name and digest(directory / name) == expected, "R2 file hash: " + name)
        require(set(receipt["sources_sha256"]) == set(SOURCES), "R2 source coverage")
        for name, expected in receipt["sources_sha256"].items():
            require(digest(ROOT / name) == expected, "R2 source changed: " + name)
    s = json.loads((directory / "summary.json").read_text())
    require(s["max_m"] == 10_000_000 and s["max_n"] == 50_000_004, "fixed R2 campaign")
    require(s["nonvacuous"] == [9_999_999] * 5 and s["vacuous"] == [0] * 5, "R2 pair coverage")
    for name in ("PB2", "delta36", "PB36", "K"):
        require(all(sum(v[r] for v in s[name].values()) == 9_999_999 for r in range(5)), "R2 histogram partition")
    records = [json.loads(line) for line in (directory / "certificates.jsonl").read_text().splitlines()]
    certs = load_certificates(directory / "certificates.jsonl")
    indexed = {x["n"]: x for x in records}
    critical, nearest, failures = [rows(directory / name) for name in ("critical.csv", "nearest36.csv", "failures.csv")]
    used = set()
    for name, selected in (("critical", critical), ("nearest", nearest), ("failures", failures)):
        keys = [(x["m"], x["r"]) for x in selected]
        require(keys == sorted(set(keys)), "duplicate or unsorted selected row")
        counts = [0] * 5
        for x in selected:
            m, r = x["m"], x["r"]
            require(2 <= m <= 10_000_000 and 0 <= r < 5, "selected pair bounds")
            require((certs[m], certs[5 * m + r]) == (x["D"], x["E"]), "selected exact masks")
            require(x == describe(x), "independent selected arithmetic")
            value = x["PB36"] if name == "nearest" else x["PB2"]
            require(value <= (0 if name == "failures" else 1), "selected threshold")
            if name != "failures":
                require(verify_gate(certificate(m, r, indexed[m], indexed[5 * m + r]))["status"] == "SUFFICIENT_BRIDGE", "positive selected certificate")
            counts[r] += 1; used.update((m, 5 * m + r))
        field = "PB36" if name == "nearest" else "PB2"
        expected = [sum(v[r] for k, v in s[field].items() if int(k) <= (0 if name == "failures" else 1)) for r in range(5)]
        require(counts == expected, "selected histogram count")
    hard = read_rows(R1 / "hard_cases.csv")
    acc = accounting(hard)
    require(json.loads((directory / "accounting.json").read_text()) == acc, "R2 accounting")
    for x in hard:
        m, r = x["m"], x["r"]
        require(certs[m] == x["parent_mask"] and certs[5 * m + r] == x["child_mask"], "frozen hard masks")
        require(verify_gate(certificate(m, r, indexed[m], indexed[5 * m + r]))["status"] == "SUFFICIENT_BRIDGE", "hard certificate")
        used.update((m, 5 * m + r))
    used.update((784, 3920))
    control = margins(summary(784, exponents(certs[784]), exponents(certs[3920])))
    require(control["delta36"] == 0 and control["gF"] == 1, "individual mod36 control")
    require(used == certs.keys(), "R2 certificate target coverage")
    hard2 = [x for x in hard if x["gate2_hard"]]
    targets = {n for x in hard2 for n in (x["m"], x["n"])}
    led = check_ledger(rows(directory / "hard_ledger.csv"), targets)
    require(led == receipt["ledger"], "ledger receipt")
    examples = json.loads((directory / "examples.json").read_text())
    require(len(examples["complete"]) == len(hard2) and len(examples["lower"]) == len(hard2), "example count")
    for x, complete, lower in zip(hard2, examples["complete"], examples["lower"]):
        require(complete == certificate(x["m"], x["r"], indexed[x["m"]], indexed[x["n"]]), "example binding")
        require((lower["m"], lower["r"], lower["mode"]) == (x["m"], x["r"], "lower"), "lower binding")
        require(verify_gate(lower)["margins"]["PB2"] > 0, "lower sufficient parity proof")
    require(receipt["r1_head"] == "9e371d1ef47138de880208eebf4a81e276aa80c1", "R1 head")
    require(receipt["a303656"] == "UNRESOLVED" and receipt["historical_reason"] == "NOT_ESTABLISHED", "scope labels")
    require(receipt["metrics"]["scan"]["returncode"] == 0, "R2 scan return code")
    require(receipt["input_masks"] == json.loads((R1 / "replay_receipt.json").read_text())["raw_files"]["masks.u16le"], "shared input binding")
    require(receipt["r1_manifest_sha256"] == digest(R1 / "manifest.json"), "preserved R1 manifest")
    comparison = json.loads((directory / "comparison.json").read_text())
    observed = {"PB2_min": min(map(int, s["PB2"])), "PB2_margin1": sum(s["PB2"].get("1", [])),
                "lambda_below3": acc["lambda_below_3_by_r"], "delta36_frozen220": acc["delta36_histogram"], "ledger": led}
    require(comparison["observed"] == observed, "comparison observations")
    require(comparison["status"] == ("MATCH" if observed == comparison["expected"] else "MISMATCH"), "comparison status")
    return {"selected_masks": len(certs), "critical_pairs": len(critical), "nearest_parity36_pairs": len(nearest),
            "PB2_nonpositive_pairs": len(failures), "ledger": led,
            "scope": "selected exact certificates and independent postprocessing; full coverage requires native replay"}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()
    print(json.dumps(verify_directory(args.directory), indent=2, sort_keys=True))
