#!/usr/bin/env python3
"""Exact, bounded certificate checker; it does not certify full scan coverage.

Certificate by_d[d] is [a,b,c] for membership, or one [p,v_p] per
admissible c for nonmembership. See the audit README for the wire format.
The checker uses no native bitsets and does not trust a supplied D mask.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
from pathlib import Path

CAP = 50_000_004
FIELDS = ("m,r,n,L,parent_mask,child_mask,runs,defect1,defect2,"
          "same_sources,plus_sources,bridge_edges,gate2_hard").split(",")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def integer(value, low, high, label):
    require(type(value) is int and low <= value <= high, label)
    return value


def powers(base, limit):
    result, p = [], 1
    while p <= limit:
        result.append(p)
        if p > limit // base:
            break
        p *= base
    return result


def is_prime(n):
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % k for k in range(3, math.isqrt(n) + 1, 2))


def check_certificate(record):
    require(type(record) is dict and set(record) == {"n", "mask", "by_d"}, "certificate fields")
    n = integer(record["n"], 2, CAP, "n bound")
    p5 = powers(5, n)
    mask = integer(record["mask"], 0, (1 << len(p5)) - 1, "mask domain")
    entries = record["by_d"]
    require(type(entries) is list and len(entries) == len(p5), "complete d coverage")
    derived = 0
    for d, five in enumerate(p5):
        entry = entries[d]
        require(type(entry) is list, "alternative type")
        if len(entry) == 3 and all(type(v) is int for v in entry):
            a, b, c = entry
            integer(a, 0, math.isqrt(n), "a bound")
            integer(b, 0, math.isqrt(n), "b bound")
            threes = powers(3, n - five)
            integer(c, 0, len(threes) - 1, "c bound")
            require(a * a + b * b + threes[c] + five == n, "membership equation")
            derived |= 1 << d
        else:
            threes = powers(3, n - five)
            require(len(entry) == len(threes), "complete c coverage")
            for c, three in enumerate(threes):
                pair = entry[c]
                require(type(pair) is list and len(pair) == 2, "blocker pair")
                residual = n - five - three
                # Residual zero is representable; it can NEVER have a blocker.
                require(residual > 0, "zero residual cannot be blocked")
                p = integer(pair[0], 3, residual, "blocker prime bound")
                exponent = integer(pair[1], 1, residual.bit_length(), "valuation bound")
                require(p % 4 == 3 and is_prime(p), "blocker must be prime 3 mod 4")
                q, valuation = residual, 0
                while q % p == 0:
                    q //= p
                    valuation += 1
                require(valuation == exponent and valuation % 2 == 1, "exact odd valuation")
    require(derived == mask, "certificate mask differs from verified alternatives")
    return n, derived


def load_certificates(path):
    result = {}
    for line in path.read_text().splitlines():
        n, mask = check_certificate(json.loads(line))
        require(n not in result, "duplicate certified n")
        result[n] = mask
    return result


def exponents(mask):
    return {j for j in range(mask.bit_length()) if mask & (1 << j)}


def describe(m, r, parent, child):
    """Use literal sets, distinct from both native implementations."""
    D, E = exponents(parent), exponents(child)
    L = len(powers(5, m)) - 1
    runs = sum(j - 1 not in D for j in D)
    predecessors = (E | {j - 1 for j in E}) & set(range(L + 1))
    same = D & E
    plus = {j for j in D if j + 1 in E}
    defect2 = len(D) + len(predecessors) - (L + 1)
    return dict(zip(FIELDS, [m, r, 5 * m + r, L, parent, child, runs,
                            len(D) + runs + len(E) - (L + 2), defect2,
                            sum(1 << j for j in same), sum(1 << j for j in plus),
                            len(same) + len(plus), int(defect2 <= 0)]))


def read_rows(path, branch=False):
    with path.open(newline="") as f:
        reader = csv.DictReader(f)
        require(reader.fieldnames == (["branch"] if branch else []) + FIELDS, "CSV schema")
        result = []
        for row in reader:
            require(None not in row and all(v is not None for v in row.values()), "CSV width")
            result.append({k: v if k == "branch" else int(v) for k, v in row.items()})
    return result


def check_row(row, certs, max_m):
    m = integer(row["m"], 2, max_m, "row m")
    r = integer(row["r"], 0, 4, "row r")
    require(m in certs and 5 * m + r in certs, "missing mask certificate")
    expected = describe(m, r, certs[m], certs[5 * m + r])
    require({k: row[k] for k in FIELDS} == expected, "row arithmetic or masks")
    require(row["parent_mask"] != 0, "nonvacuous row")


def verify_directory(directory, check_manifest=True):
    if check_manifest:
        manifest = json.loads((directory / "manifest.json").read_text())
        require(manifest["schema"] == 1, "manifest schema")
        require(set(manifest["files"]) == {"summary.json", "hard_cases.csv", "minima.csv", "failures.csv",
                                         "probes.csv", "certificates.jsonl", "reference_comparison.json",
                                         "replay_receipt.json", "hard_profile.json", "execution_logs.json"}, "manifest coverage")
        for name, expected in manifest["files"].items():
            require(Path(name).name == name, "manifest path")
            require(hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected, "manifest hash: " + name)
    summary = json.loads((directory / "summary.json").read_text())
    max_m = integer(summary["max_m"], 2, 10_000_000, "max_m")
    require(summary["max_n"] == 5 * max_m + 4, "max_n")
    require(summary["cases"] == 5 * (max_m - 1), "case count")
    for name in ("vacuous", "same_failures", "plus_failures", "combined_failures",
                 "same_minima", "plus_minima", "gate1_hard", "gate2_hard", "unique_bridge_cases"):
        require(type(summary[name]) is list and len(summary[name]) == 5, "summary vector")
        for v in summary[name]:
            integer(v, 0, max_m if "minima" in name else max_m - 1, "summary bound")
    for name in ("defect1_histogram", "defect2_histogram", "bridge_edge_histogram"):
        histogram = summary[name]
        require(type(histogram) is dict, "histogram type")
        totals = [0] * 5
        for key, values in histogram.items():
            require(str(int(key)) == key and len(values) == 5, "histogram bin")
            for r, v in enumerate(values):
                integer(v, 0, max_m - 1, "histogram count")
                totals[r] += v
        require(totals == [max_m - 1] * 5, "histogram partition")
    certs = load_certificates(directory / "certificates.jsonl")
    used = set(range(2, min(9, 5 * max_m + 4) + 1))
    require(used <= certs.keys() and all(certs[n] for n in used), "base cases")
    hard = read_rows(directory / "hard_cases.csv")
    minima = read_rows(directory / "minima.csv", True)
    failures = read_rows(directory / "failures.csv")
    probes = read_rows(directory / "probes.csv")
    counts1, counts2 = [0] * 5, [0] * 5
    previous = (0, 0)
    for row in hard:
        check_row(row, certs, max_m)
        key = row["m"], row["r"]
        require(key > previous, "duplicate or unordered hard row")
        previous = key
        require(row["defect1"] <= 0, "hard row passes first gate")
        counts1[row["r"]] += 1
        counts2[row["r"]] += row["gate2_hard"]
    require(counts1 == summary["gate1_hard"], "first gate listed counts")
    require(counts2 == summary["gate2_hard"], "second gate listed counts")
    seen_minima = set()
    for row in minima:
        check_row(row, certs, max_m)
        branch, r = row["branch"], row["r"]
        require(branch in ("same", "plus") and (branch, r) not in seen_minima, "minimum branch")
        seen_minima.add((branch, r))
        require(row[branch + "_sources"] == 0, "minimum is not branch failure")
        require(summary[branch + "_minima"][r] == row["m"], "reported minimum")
    require(seen_minima == {(b, r) for b in ("same", "plus") for r in range(5)
                            if summary[b + "_minima"][r]}, "minimum coverage")
    counted_failures = [0] * 5
    fail_keys = set()
    for row in failures:
        check_row(row, certs, max_m)
        require(row["bridge_edges"] == 0, "alleged combined failure has bridge")
        key = row["m"], row["r"]
        require(key not in fail_keys, "duplicate failure")
        fail_keys.add(key)
        counted_failures[row["r"]] += 1
    require(counted_failures == summary["combined_failures"], "combined failure coverage")
    probe_keys = set()
    for row in probes:
        check_row(row, certs, max_m)
        key = row["m"], row["r"]
        require(key not in probe_keys, "duplicate probe")
        probe_keys.add(key)
    require(probe_keys == {(m, r) for m, r in ((1676569, 0), (7963079, 3)) if m <= max_m}, "probe coverage")
    for row in hard + minima + failures + probes:
        used.update((row["m"], row["n"]))
    require(used == certs.keys(), "certificate target completeness")
    for r in range(5):
        require(summary["combined_failures"][r] <= min(summary["same_failures"][r], summary["plus_failures"][r]), "failure inclusion")
        require(summary["unique_bridge_cases"][r] == summary["bridge_edge_histogram"].get("1", [0] * 5)[r], "unique histogram")
        for branch in ("same", "plus"):
            require(bool(summary[branch + "_failures"][r]) == bool(summary[branch + "_minima"][r]), "minimum existence")
        if summary["vacuous"][r] == 0:
            require(sum(v[r] for k, v in summary["defect1_histogram"].items() if int(k) <= 0) == counts1[r], "first histogram count")
            require(summary["bridge_edge_histogram"].get("0", [0] * 5)[r] == counted_failures[r], "zero bridge histogram")
    if check_manifest:
        receipt = json.loads((directory / "replay_receipt.json").read_text())
        require(receipt["max_m"] == max_m and receipt["max_n"] == summary["max_n"], "receipt bounds")
        require(receipt["full_entrywise_agreement"] == {"entries_each": summary["max_n"] + 1,
                                                       "tables": ["S2", "T", "D"]}, "receipt agreement scope")
        require(receipt["a303656"] == "UNRESOLVED", "receipt global status")
        root = Path(__file__).resolve().parents[1]
        require(set(receipt["sources_sha256"]) == {"src/ajt5_scan.cpp", "src/ajt5_valuation_replay.cpp",
                                                   "src/verify_ajt5_reports.py", "scripts/run_ajt5_audit.py"}, "source coverage")
        for name, expected in receipt["sources_sha256"].items():
            require(hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, "source changed since recorded replay: " + name)
        for phase in ("scan", "valuation", "build_scan", "build_valuation"):
            require(receipt["metrics"][phase]["returncode"] == 0, "receipt return code")
        records = [json.loads(line) for line in (directory / "certificates.jsonl").read_text().splitlines()]
        profile = json.loads((directory / "hard_profile.json").read_text())
        require(profile == hard_profile(hard, records), "hard profile consistency")
        reference = json.loads((directory / "reference_comparison.json").read_text())
        require(receipt["reference_status"] == reference["status"], "reference receipt status")
        if max_m == 10_000_000:
            observed = {key: summary[key] for key in ("combined_failures", "same_minima", "plus_minima", "gate1_hard", "gate2_hard")}
            require(reference["observed_counts"] == observed, "reference observed counts")
            expected = reference["reference_counts"]
            require(set(expected) == set(observed), "reference count fields")
            differences = {key: {"reference": expected[key], "observed": value}
                           for key, value in observed.items() if value != expected[key]}
            # Probe mismatches can also appear when reusing this checker for a
            # future negative experiment; never suppress a count discrepancy.
            require(all(reference["differences"].get(k) == v for k, v in differences.items()), "missing reference discrepancy")
            require(reference["status"] == ("DISCREPANCY" if reference["differences"] else "MATCH"), "reference status")
        else:
            require(reference["status"] == "NOT_APPLICABLE", "partial reference status")
    return {"verified_masks": len(certs), "gate1_rows": len(hard), "gate2_rows": sum(counts2),
            "minimum_rows": len(minima), "combined_failure_rows": len(failures),
            "scope": "complete exact certificates for listed masks; exhaustive scan counts and list completeness require native replay"}


def hard_profile(hard, records):
    """Descriptive data only; prime histograms depend on blocker selection."""
    indexed = {record["n"]: record for record in records}
    profiles = []
    for row in hard:
        if not row["gate2_hard"]:
            continue
        D, E = exponents(row["parent_mask"]), exponents(row["child_mask"])
        record = {"m": row["m"], "r": row["r"], "n": row["n"], "L": row["L"],
                  "D": sorted(D), "E": sorted(E),
                  "predecessors": sorted((E | {j - 1 for j in E}) & set(range(row["L"] + 1))),
                  "defect1": row["defect1"], "defect2": row["defect2"],
                  "bridges": [[d, e] for d in sorted(D) for e in sorted(E) if e in (d, d + 1)],
                  "valuation_features": {}}
        for name, n in (("parent", row["m"]), ("child", row["n"])):
            cert = indexed[n]
            hist, higher, blocks = {}, [], 0
            for d, entry in enumerate(cert["by_d"]):
                if cert["mask"] & (1 << d):
                    continue
                for c, (p, v) in enumerate(entry):
                    hist[str(p)] = hist.get(str(p), 0) + 1
                    blocks += 1
                    if v > 1:
                        higher.append({"d": d, "c": c, "p": p, "valuation": v})
            record["valuation_features"][name] = {"absent_d": len(cert["by_d"]) - cert["mask"].bit_count(),
                                                      "covered_alternatives": blocks, "selected_prime_histogram": hist,
                                                      "higher_odd_valuations": higher}
        profiles.append(record)
    return {"scope": "observed survivors of both literal gates only; selected blockers are not unique prime invariants",
            "cases": profiles}


def create_certificates(directory):
    """Independent trial factorization and square witnesses, with no bitset input."""
    rows = (read_rows(directory / "hard_cases.csv") + read_rows(directory / "minima.csv", True)
            + read_rows(directory / "failures.csv") + read_rows(directory / "probes.csv"))
    targets = set(range(2, 10))
    for row in rows:
        integer(row["m"], 2, 10_000_000, "candidate m bound")
        integer(row["r"], 0, 4, "candidate r bound")
        integer(row["n"], 2, CAP, "candidate n bound")
        require(row["n"] == 5 * row["m"] + row["r"], "candidate child")
        targets.update((row["m"], row["n"]))
    primes = [p for p in range(2, math.isqrt(max(targets)) + 1) if is_prime(p)]

    def blocker(x):
        if x == 0:
            return None
        for p in primes:
            if p * p > x:
                break
            exponent = 0
            while x % p == 0:
                x //= p
                exponent += 1
            if p % 4 == 3 and exponent % 2:
                return [p, exponent]
        return [x, 1] if x % 4 == 3 else None

    def squares(x):
        a, b = 0, math.isqrt(x)
        while a <= b:
            total = a * a + b * b
            if total == x:
                return [a, b]
            if total < x:
                a += 1
            else:
                b -= 1
        raise ValueError("factor criterion/witness disagreement")

    with (directory / "certificates.jsonl").open("w") as f:
        for n in sorted(targets):
            mask, alternatives = 0, []
            for d, five in enumerate(powers(5, n)):
                blockers = []
                for c, three in enumerate(powers(3, n - five)):
                    residual = n - five - three
                    obstruction = blocker(residual)
                    if obstruction is None:
                        alternatives.append(squares(residual) + [c])
                        mask |= 1 << d
                        break
                    blockers.append(obstruction)
                else:
                    alternatives.append(blockers)
            record = {"n": n, "mask": mask, "by_d": alternatives}
            check_certificate(record)
            f.write(json.dumps(record, separators=(",", ":")) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--create-certificates", action="store_true")
    args = parser.parse_args()
    if args.create_certificates:
        create_certificates(args.directory)
    print(json.dumps(verify_directory(args.directory, not args.create_certificates), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
