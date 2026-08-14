#!/usr/bin/env python3
"""Independent artifact verifier driven by authenticated inputs and both enumerators."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from common import demand, load_bases, load_pairs, load_prime_authority, mask_int, verify_protected
from brute_force_oracle import SMALL_PRIMES, literal_score
import enumerator_a
import enumerator_b
from run_landscape import build_crt, build_g231, build_shortlist, global_summaries

CONCLUSION = "VALIDATED EXACT FIFTH-PRIME MARGINAL-COVERAGE LANDSCAPE"


def load_json(path: Path):
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def verify(root: Path, artifacts: Path) -> dict:
    protected = verify_protected(root)
    _eligible, candidates, authority = load_prime_authority(root)
    pairs = load_pairs(root)
    bases = load_bases(root)
    demand(load_json(artifacts / "authority_report.json") == authority, "authority report corruption")
    domain = load_json(artifacts / "pair_domain.json")
    demand(domain["pairs"] == pairs and domain["pair_count"] == 407, "pair-domain artifact corruption")
    frozen = load_json(artifacts / "frozen_base_masks.json")
    demand(frozen["bases"] == bases and frozen["base_count"] == 13, "frozen base-mask artifact corruption")
    with (artifacts / "per_prime_compressed_landscapes.jsonl").open(encoding="utf-8") as stream:
        records = [json.loads(line) for line in stream if line.strip()]
    demand([r["q"] for r in records] == candidates, "missing, duplicate, or reordered candidate prime")
    literal_checks = []
    for record in records:
        q = record["q"]
        a = enumerator_a.enumerate_compressed(q, pairs)
        b = enumerator_b.enumerate_compressed(q, pairs)
        demand(a == b == record["compression"], f"compressed digest or union landscape corruption q={q}")
        demand(a["q2_residue_count"] == q*q, "q^2 residue-count corruption")
        demand(a["empty_lift_count"] + sum(x["full_lift_count"] + len(x["exclusions"]) for x in a["buckets"]) == q*q, "compression does not represent q^2 residues")
        demand(len(record["base_summaries"]) == 13, "base summary count corruption")
        for base, stored in zip(bases, record["base_summaries"]):
            value = mask_int(base["coverage_mask_hex"])
            sa = enumerator_a.score(a, value, base["base_mask_digest"])
            sb = enumerator_b.score(b, value, base["base_mask_digest"])
            demand(stored == {"base_id": base["base_id"], **sa} == {"base_id": base["base_id"], **sb}, f"histogram/argmax/union corruption q={q} base={base['base_id']}")
            demand(sum(n for _delta, n in sa["histogram"]) == q*q, "histogram count not summing to q^2")
            if q in SMALL_PRIMES:
                demand(literal_score(q, pairs, value, base["base_mask_digest"]) == sa, "literal v_q=1 oracle mismatch")
        if q in SMALL_PRIMES:
            literal_checks.append(q)
    demand(literal_checks == list(SMALL_PRIMES), "small-prime oracle coverage corruption")
    expected_globals = global_summaries(records, bases)
    demand(load_json(artifacts / "global_summaries.json") == expected_globals, "global or Pareto summary corruption")
    expected_g231 = build_g231(root, records, bases, expected_globals, pairs)
    demand(load_json(artifacts / "g231_residual_analysis.json") == expected_g231, "G231 residual analysis corruption")
    expected_crt = build_crt(candidates)
    demand(load_json(artifacts / "crt_density_geometry.json") == expected_crt, "CRT-density geometry corruption")
    expected_shortlist = build_shortlist(records, bases, expected_globals, pairs)
    shortlist = load_json(artifacts / "frozen_future_shortlist.json")
    demand(shortlist == expected_shortlist, "shortlist cherry-pick or content mutation")
    demand(shortlist["entry_count"] == len(shortlist["entries"]) <= 20, "shortlist size corruption")
    identities = [(e["base_mask_digest"], e["q"], e["t"], e["resulting_union_mask_digest"]) for e in shortlist["entries"]]
    demand(len(identities) == len(set(identities)), "shortlist identity duplication")
    demand(all(not e.get("integer_evaluated", False) for e in shortlist["entries"]), "shortlist integer evaluation corruption")
    crt = load_json(artifacts / "crt_density_geometry.json")
    demand(not crt["meaningful_per_class_P5_distribution_supported"], "CRT support conclusion corruption")
    demand(all(row["maximum_member_count_in_current_cell"] == 1 for row in crt["candidate_geometry"]), "CRT member-count corruption")
    metadata = load_json(artifacts / "metadata.json")
    demand(metadata["authority_B"] == 5000 and metadata["new_integers_evaluated"] == 0, "scope metadata corruption")
    demand(not metadata["T_backends_called"] and not metadata["direct_two_square_oracle_called"] and not metadata["P5_CRT_integer_search_performed"], "forbidden backend/search scope corruption")
    from common import sha256_file
    demand(all(sha256_file(artifacts / name) == digest for name, digest in metadata["artifact_sha256_before_verification_report"].items()), "artifact hash-manifest corruption")
    demand(verify_protected(root) == protected, "protected baseline hashes changed during verification")
    return {"schema": "a303656-fifth-prime-verification-report-v1", "status": "PASS", "validation_conclusion": CONCLUSION,
            "candidate_count": len(candidates), "base_count": len(bases), "pair_count": len(pairs), "all_q2_residues_represented_by_proved_compression": True,
            "two_independent_enumerators_agree_for_every_q_and_base": True, "literal_small_prime_oracle_primes": literal_checks,
            "histograms_sum_to_q2": True, "exact_integer_arithmetic": True, "protected_baseline_hashes_unchanged": True,
            "new_integer_evaluations": 0, "T_backends_called": False, "direct_two_square_oracle_called": False, "P5_CRT_integer_search_performed": False,
            "mathematical_status": "UNRESOLVED"}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--artifacts", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    report = verify(args.root.resolve(), args.artifacts.resolve())
    if args.output:
        from common import atomic_json
        atomic_json(args.output, report)
    print(CONCLUSION)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"EXACT FIFTH-PRIME MARGINAL-COVERAGE LANDSCAPE NOT VALIDATED: {exc}")
        raise SystemExit(2)
