#!/usr/bin/env python3
"""Independent exact Python verifier for bounded A303656 certificates."""
from __future__ import annotations

import argparse
import csv
import hashlib
import json
import platform
import sys
from pathlib import Path
from time import perf_counter

from common import (
    check_domain_bounds,
    enumerate_pairs,
    exact_one_obstructs,
    load_assignment_csv,
    parse_primes,
    valuation,
)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", required=True, type=int)
    ap.add_argument("--primes", required=True, help="comma list or text file")
    ap.add_argument("--assignment", help="optional CSV with c,d,prime")
    ap.add_argument("--cert-json")
    ap.add_argument("--obstructions-csv")
    ap.add_argument("--interval-low", type=int)
    ap.add_argument("--interval-high", type=int)
    ap.add_argument("--C", type=int)
    ap.add_argument("--D", type=int)
    ap.add_argument("--quiet-pairs", action="store_true")
    args = ap.parse_args()

    started = perf_counter()
    errors: list[str] = []
    if args.n <= 1:
        errors.append("candidate n must be > 1")
    if (args.interval_low is None) != (args.interval_high is None):
        errors.append("interval-low and interval-high must be supplied together")
    if args.interval_low is not None and args.interval_high is not None:
        if args.interval_low > args.interval_high:
            errors.append("declared interval has low > high")
        if not (args.interval_low <= args.n <= args.interval_high):
            errors.append("candidate n is outside the declared search interval")
    if (args.C is None) != (args.D is None):
        errors.append("C and D must be supplied together")
    if args.C is not None and args.D is not None:
        bound_high = args.interval_high if args.interval_high is not None else args.n
        try:
            check_domain_bounds(args.C, args.D, bound_high)
        except Exception as exc:
            errors.append(f"declared finite exponent domain is invalid: {exc}")

    try:
        primes = parse_primes(args.primes)
    except Exception as exc:
        print(f"FAIL prime_pool_error={exc}")
        return 2

    assignment = None
    if args.assignment:
        try:
            assignment = load_assignment_csv(args.assignment)
        except Exception as exc:
            print(f"FAIL assignment_error={exc}")
            return 2
        for key, p in assignment.items():
            if p not in primes:
                errors.append(f"assignment prime {p} for pair {key} is not in P")

    powers3, powers5, pairs = enumerate_pairs(args.n)
    if args.C is not None and len(powers3) - 1 > args.C:
        errors.append("declared C is smaller than the exact exponent range required by n")
    if args.D is not None and len(powers5) - 1 > args.D:
        errors.append("declared D is smaller than the exact exponent range required by n")
    pair_keys = {(ps.c, ps.d) for ps in pairs}
    if assignment is not None:
        missing = sorted(pair_keys - set(assignment))
        extra = sorted(set(assignment) - pair_keys)
        if missing:
            errors.append(f"assignment missing {len(missing)} admissible pairs")
        if extra:
            errors.append(f"assignment contains {len(extra)} non-admissible pairs")

    rows: list[dict[str, object]] = []
    uncovered: list[dict[str, object]] = []
    zero_remainders = 0

    for ps in pairs:
        remainder = args.n - ps.shift
        if remainder == 0:
            zero_remainders += 1
        candidates = [assignment[(ps.c, ps.d)]] if assignment is not None and (ps.c, ps.d) in assignment else primes
        chosen = None
        chosen_v = None
        for p in candidates:
            if exact_one_obstructs(remainder, p):
                chosen = p
                chosen_v = valuation(remainder, p)
                break
        row: dict[str, object] = {
            "c": ps.c,
            "d": ps.d,
            "shift": str(ps.shift),
            "remainder": str(remainder),
            "prime": chosen if chosen is not None else "",
            "valuation": chosen_v if chosen_v is not None else "",
        }
        rows.append(row)
        if chosen is None:
            uncovered.append({
                "c": ps.c,
                "d": ps.d,
                "shift": str(ps.shift),
                "remainder": str(remainder),
            })
        if not args.quiet_pairs:
            if chosen is None:
                print(f"PAIR c={ps.c} d={ps.d} s={ps.shift} r={remainder} obstruction=NONE")
            else:
                print(
                    f"PAIR c={ps.c} d={ps.d} s={ps.shift} r={remainder} "
                    f"p={chosen} valuation={chosen_v}"
                )

    distinct_shifts = len({ps.shift for ps in pairs})
    passed = not errors and not uncovered and zero_remainders == 0
    if zero_remainders:
        errors.append(
            f"remainder=0 occurs for {zero_remainders} admissible pair(s); 0 is divisible by p^2 and cannot pass exact-one"
        )

    elapsed = perf_counter() - started
    print(f"candidate_n={args.n}")
    print(f"prime_count={len(primes)}")
    print(f"max_c={len(powers3)-1}")
    print(f"max_d={len(powers5)-1}")
    print(f"admissible_pair_count={len(pairs)}")
    print(f"distinct_shift_count={distinct_shifts}")
    print(f"zero_remainder_count={zero_remainders}")
    print(f"uncovered_pair_count={len(uncovered)}")
    for msg in errors:
        print(f"ERROR {msg}")
    print(f"elapsed_seconds={elapsed:.9f}")
    print("PASS" if passed else "FAIL")

    if args.obstructions_csv:
        out = Path(args.obstructions_csv)
        out.parent.mkdir(parents=True, exist_ok=True)
        with out.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["c", "d", "shift", "remainder", "prime", "valuation"])
            writer.writeheader()
            writer.writerows(rows)

    if args.cert_json:
        out = Path(args.cert_json)
        out.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "schema": "a303656-bounded-exact-one-v1",
            "status": "PASS" if passed else "FAIL",
            "candidate_n": str(args.n),
            "prime_set": primes,
            "interval": {
                "low": str(args.interval_low) if args.interval_low is not None else None,
                "high": str(args.interval_high) if args.interval_high is not None else None,
            },
            "declared_C": args.C,
            "declared_D": args.D,
            "enumerated_max_c": len(powers3) - 1,
            "enumerated_max_d": len(powers5) - 1,
            "admissible_pair_count": len(pairs),
            "distinct_shift_count": distinct_shifts,
            "zero_remainder_count": zero_remainders,
            "uncovered_pairs": uncovered,
            "obstructions": rows,
            "errors": errors,
            "verifier": {
                "implementation": "Python independent exact verifier",
                "python": sys.version,
                "platform": platform.platform(),
                "source_sha256": sha256_file(Path(__file__)),
                "elapsed_seconds": elapsed,
            },
        }
        out.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
