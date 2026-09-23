#!/usr/bin/env python3
"""Cross-check independent L5,3 engines and emit the final certificate."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


EXPECTED = {
    7_963_079: {
        "target": 39_815_398,
        "D_m": [0, 1, 2, 4, 6, 7, 8, 9],
        "D_target": [0, 4, 6],
    },
    8_984_426: {
        "target": 44_922_133,
        "D_m": [1, 4, 5, 7, 9],
        "D_target": [0, 1, 3, 7, 9],
    },
}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--support", type=Path, required=True)
    parser.add_argument("--criterion", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    support = json.loads(args.support.read_text(encoding="utf-8"))
    criterion = json.loads(args.criterion.read_text(encoding="utf-8"))
    require(support["scan_domain"] == {"minimum": 2, "maximum": 7_963_079,
                                       "predicate": "D(m) nonempty"}, "scan domain")
    require(support["first_failure"] == 7_963_079, "first failure")
    support_rows = {row["m"]: row for row in support["candidates"]}
    criterion_rows = {row["m"]: row for row in criterion["candidates"]}

    candidates = []
    for m, expected in EXPECTED.items():
        a = support_rows[m]
        b = criterion_rows[m]
        require(a["five_m_plus_three"] == b["five_m_plus_three"] == expected["target"], "target")
        require(a["D_m"] == b["source"]["D"] == expected["D_m"], "source D")
        require(a["D_5m3"] == b["target"]["D"] == expected["D_target"], "target D")
        require(a["shifted_D_m"] == b["shifted_D_m"], "shifted D")
        require(a["intersection"] == b["intersection"] == [], "nonempty intersection")
        candidates.append({
            "m": m,
            "five_m_plus_three": expected["target"],
            "D_m": expected["D_m"],
            "D_5m3": expected["D_target"],
            "shifted_D_m": a["shifted_D_m"],
            "intersection": [],
            "engine_agreement": True,
        })

    require(all(row["verified"] for row in criterion["reported_representations"]),
            "reported representation")
    result = {
        "schema": "a303656-l53-falsification-v1",
        "lemma": "L5,3",
        "status": "FALSE",
        "definitions": {
            "S_2": "{x^2+y^2 : x,y in Z}",
            "T_3": "S_2 + {3^j : j>=0}",
            "D_m": "{d>=0 : m-5^d in T_3}",
            "statement": "D(m) nonempty implies (D(m)+1) intersect D(5m+3) nonempty",
            "domain": "integers m>=2 with D(m) nonempty (equivalently representable m)",
        },
        "first_failure": candidates[0],
        "second_certified_failure": candidates[1],
        "first_failure_scan": {
            "minimum": 2,
            "maximum": 7_963_079,
            "exhaustive": True,
            "tested_representable_sources_through_failure": support["tested_representable_sources_through_failure"],
            "smaller_failure_count": 0,
        },
        "representations": criterion["reported_representations"],
        "engines": {
            "A": "direct enumeration of two-square support; bitset shifts by powers of 3",
            "B": "exact trial-division factorization and odd valuations at primes 3 mod 4",
            "shared_membership_logic": False,
            "agreement": True,
        },
        "input_hashes": {
            "support_scan_json": sha256(args.support),
            "criterion_details_json": sha256(args.criterion),
        },
        "historical_context": {
            "packet_tested_source_interval": [2, 5000],
            "packet_failures_in_that_interval": 0,
            "history_rewritten": False,
        },
        "logical_scope": {
            "certified": "L5,3 is false",
            "not_certified": [
                "the minimal-counterexample program is impossible",
                "all 5-adic transfers are impossible",
                "all representation-selection lemmas are impossible",
                "A303656 is false",
            ],
        },
        "independent_checker_pass": True,
    }
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "CERTIFIED FALSE", "output": str(args.output),
                      "sha256": sha256(args.output)}, sort_keys=True))


if __name__ == "__main__":
    main()
