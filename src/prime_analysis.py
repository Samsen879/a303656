#!/usr/bin/env python3
"""Bounded-shift prime compatibility statistics and deterministic pool ranking."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter
from math import comb
from pathlib import Path

from common import check_domain_bounds, enumerate_rectangle, primes_3mod4


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--C", type=int, required=True)
    ap.add_argument("--D", type=int, required=True)
    ap.add_argument("--low", type=int, required=True)
    ap.add_argument("--high", type=int, required=True)
    ap.add_argument("--candidate-primes", type=int, default=512)
    ap.add_argument("--csv", required=True)
    ap.add_argument("--json", required=True)
    args = ap.parse_args()
    if args.low > args.high:
        raise SystemExit("low > high")
    check_domain_bounds(args.C, args.D, args.high)
    _, _, rect = enumerate_rectangle(args.C, args.D)
    active = [ps for ps in rect if ps.shift <= args.high]
    pair_count = len(active)
    distinct_shifts = sorted({ps.shift for ps in active})
    primes = primes_3mod4(args.candidate_primes)
    rows = []
    for p in primes:
        pair_buckets = Counter(ps.shift % p for ps in active)
        shift_buckets = Counter(s % p for s in distinct_shifts)
        overlap_pairs = sum(comb(k, 2) for k in pair_buckets.values())
        total_pairs = comb(pair_count, 2) if pair_count >= 2 else 0
        conflicts = total_pairs - overlap_pairs
        max_bucket = max(pair_buckets.values(), default=0)
        max_shift_bucket = max(shift_buckets.values(), default=0)
        nonempty_residues = len(pair_buckets)
        # Exact number of n in [low,high] that p covers each shift, summed over shifts.
        incidence = 0
        for ps in active:
            s = ps.shift
            first = args.low + ((s - args.low) % p)
            if first <= args.high:
                count_p = (args.high - first) // p + 1
            else:
                count_p = 0
            p2 = p * p
            first2 = args.low + ((s - args.low) % p2)
            if first2 <= args.high:
                count_p2 = (args.high - first2) // p2 + 1
            else:
                count_p2 = 0
            incidence += count_p - count_p2
        interval_size = args.high - args.low + 1
        incidence_denominator = interval_size * pair_count
        marginal = incidence / incidence_denominator if incidence_denominator else 0.0
        # Compatibility score is a ranking heuristic.  All modular incidence
        # counts above are exact integers; no float is used for admissibility.
        # The score is bounded-family specific, not merely 1/p.
        score = (max_bucket + 0.25 * max_shift_bucket + overlap_pairs / max(1, pair_count)) * (p - 1) / p
        rows.append({
            "prime": p,
            "pair_count": pair_count,
            "distinct_shift_count": len(distinct_shifts),
            "nonempty_pair_residues": nonempty_residues,
            "max_pair_bucket": max_bucket,
            "max_distinct_shift_bucket": max_shift_bucket,
            "overlap_pair_count": overlap_pairs,
            "conflict_pair_count": conflicts,
            "exact_marginal_incidence_count": incidence,
            "incidence_denominator": incidence_denominator,
            "exact_marginal_incidence_rational": f"{incidence}/{incidence_denominator}",
            "decimal_marginal_incidence_fraction": f"{marginal:.18g}",
            "compatibility_score_heuristic": f"{score:.18g}",
        })
    ranked = sorted(rows, key=lambda r: (-float(r["compatibility_score_heuristic"]), int(r["prime"])))
    for rank, row in enumerate(ranked, 1):
        row["rank"] = rank
    out_csv = Path(args.csv)
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "rank","prime","pair_count","distinct_shift_count","nonempty_pair_residues",
        "max_pair_bucket","max_distinct_shift_bucket","overlap_pair_count",
        "conflict_pair_count","exact_marginal_incidence_count","incidence_denominator",
        "exact_marginal_incidence_rational","decimal_marginal_incidence_fraction","compatibility_score_heuristic",
    ]
    with out_csv.open("w", newline="", encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields)
        w.writeheader(); w.writerows(ranked)
    payload={
        "C":args.C,"D":args.D,"low":str(args.low),"high":str(args.high),
        "pair_count":pair_count,"distinct_shift_count":len(distinct_shifts),
        "ranking_rule":"descending bounded compatibility_score; tie by prime",
        "top_primes":[r["prime"] for r in ranked],
        "rows":ranked,
    }
    Path(args.json).write_text(json.dumps(payload,indent=2)+"\n",encoding="utf-8")
    print(f"pair_count={pair_count}")
    print(f"distinct_shift_count={len(distinct_shifts)}")
    print("top32="+",".join(str(r["prime"]) for r in ranked[:32]))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
