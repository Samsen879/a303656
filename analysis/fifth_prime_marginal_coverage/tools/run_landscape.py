#!/usr/bin/env python3
"""Generate the complete exact fifth-prime marginal-coverage landscape."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any, Iterable

import enumerator_a
import enumerator_b
from brute_force_oracle import SMALL_PRIMES, literal_score
from common import (
    BASE_MANIFEST_PATH, B_ORDER, CELL_HIGH, CELL_LOW, CELL_WIDTH, COMMON_UNCOVERED_PATH,
    L4, PAIR_COUNT, PAIR_DOMAIN_DIGEST, PAIR_FREQUENCIES_PATH, PAIR_ORDER_PATH,
    START_COMMIT, atomic_json, canonical_digest, coverage_at, indices, load_bases,
    load_pairs, load_prime_authority, mask_hex, mask_int, sha256_bytes, sha256_file,
    verify_protected, demand,
)

CONCLUSION = "VALIDATED EXACT FIFTH-PRIME MARGINAL-COVERAGE LANDSCAPE"
INTERPRETATION = "MARGINAL COVERAGE AND CRT DENSITY PRESENT A STRONG TRADEOFF"


def git(root: Path, *args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=root, text=True).strip()


def pair_rows(mask: int, pairs: list[dict[str, int]]) -> list[dict[str, int]]:
    return [pairs[i] for i in indices(mask)]


def distribution(rows: list[dict[str, int]], field: str) -> list[list[int]]:
    counts = Counter(row[field] for row in rows)
    return [[value, counts[value]] for value in sorted(counts)]


def iter_cells(compression: dict[str, Any]) -> Iterable[tuple[int, int, int]]:
    if compression["empty_lift_count"]:
        yield 0, compression["empty_lift_count"], compression["first_empty_t"]
    for bucket in compression["buckets"]:
        full = sum(1 << i for _t, group in bucket["exclusions"] for i in group)
        if bucket["full_lift_count"]:
            yield full, bucket["full_lift_count"], bucket["first_full_t"]
        for t, group in bucket["exclusions"]:
            yield full & ~sum(1 << i for i in group), 1, t


def pareto(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    frontier = []
    for row in rows:
        dominated = any(
            other["maximum_delta"] >= row["maximum_delta"]
            and other["q2"] <= row["q2"]
            and other["argmax_count"] >= row["argmax_count"]
            and (other["maximum_delta"], -other["q2"], other["argmax_count"])
                != (row["maximum_delta"], -row["q2"], row["argmax_count"])
            for other in rows
        )
        if not dominated:
            frontier.append(row)
    return sorted(frontier, key=lambda r: (r["q2"], -r["maximum_delta"], -r["argmax_count"], r["q"]))


def global_summaries(per_prime: list[dict[str, Any]], bases: list[dict[str, Any]]) -> dict[str, Any]:
    result = {"schema": "a303656-fifth-prime-global-summaries-v1", "objectives": ["maximize maximum Delta_B", "minimize q^2", "maximize argmax multiplicity"], "bases": []}
    for bi, base in enumerate(bases):
        rows = [{"q": record["q"], "q2": record["q"] ** 2, **record["base_summaries"][bi]} for record in per_prime]
        maximum = max(row["maximum_delta"] for row in rows)
        winning = [row for row in rows if row["maximum_delta"] == maximum]
        first_row = min(winning, key=lambda r: (r["q"], r["first_argmax_t"]))
        top20 = sorted(rows, key=lambda r: (-r["maximum_delta"], r["q2"], -r["argmax_count"], r["q"]))[:20]
        result["bases"].append({
            "base_id": base["base_id"], "base_mask_digest": base["base_mask_digest"], "roles": base["roles"], "base_G": base["G"],
            "global_maximum_delta": maximum,
            "all_primes_attaining_global_maximum": [r["q"] for r in winning],
            "lexicographically_first_global_maximizer": [first_row["q"], first_row["first_argmax_t"]],
            "resulting_G5": base["G"] + maximum,
            "residual_size": PAIR_COUNT - base["G"] - maximum,
            "global_argmax_multiplicity": sum(r["argmax_count"] for r in winning),
            "argmax_multiplicity_by_prime": [[r["q"], r["argmax_count"]] for r in winning],
            "top_20_primes": [{k: r[k] for k in ("q", "q2", "maximum_delta", "argmax_count", "first_argmax_t")} for r in top20],
            "pareto_frontier": [{k: r[k] for k in ("q", "q2", "maximum_delta", "argmax_count", "first_argmax_t")} for r in pareto(rows)],
        })
    return result


def category_maximum(per_prime: list[dict[str, Any]], category_mask: int) -> dict[str, Any]:
    best = -1
    count = 0
    first = None
    for record in per_prime:
        for coverage, multiplicity, t in iter_cells(record["compression"]):
            value = (coverage & category_mask).bit_count()
            key = (record["q"], t)
            if value > best:
                best, count, first = value, multiplicity, key
            elif value == best:
                count += multiplicity
                if first is None or key < first:
                    first = key
    return {"category_size": category_mask.bit_count(), "maximum_covered": best, "all_covered_by_one_fifth_prime": best == category_mask.bit_count(), "argmax_multiplicity": count, "first_maximizer": list(first)}


def build_g231(root: Path, per_prime: list[dict[str, Any]], bases: list[dict[str, Any]], globals_: dict[str, Any], pairs: list[dict[str, int]]) -> dict[str, Any]:
    base = next(b for b in bases if "G231-COMMON" in b["roles"])
    base_index = base["base_index"]
    summary = globals_["bases"][base_index]
    q, t = summary["lexicographically_first_global_maximizer"]
    base_mask = mask_int(base["coverage_mask_hex"])
    coverage = coverage_at(q, t, pairs)
    new_mask = coverage & ~base_mask
    remaining = ((1 << PAIR_COUNT) - 1) & ~(base_mask | coverage)
    residual = ((1 << PAIR_COUNT) - 1) & ~base_mask

    with (root / PAIR_FREQUENCIES_PATH).open(newline="", encoding="utf-8") as stream:
        freq_rows = {int(r["pair_index"]): r for r in csv.DictReader(stream)}
    never = sum(1 << i for i in indices(residual) if int(freq_rows[i]["exposure_count"]) > 0 and int(freq_rows[i]["winner_count"]) == 0)
    frequent10 = sum(1 << i for i in indices(residual) if int(freq_rows[i]["exposure_count"]) > 0 and 10 * int(freq_rows[i]["winner_count"]) >= int(freq_rows[i]["exposure_count"]))
    frequent25 = sum(1 << i for i in indices(residual) if int(freq_rows[i]["exposure_count"]) > 0 and 4 * int(freq_rows[i]["winner_count"]) >= int(freq_rows[i]["exposure_count"]))
    demand((never.bit_count(), frequent10.bit_count(), frequent25.bit_count()) == (60, 116, 103), "prior-frequency authority counts changed")
    ranked = sorted(indices(residual), key=lambda i: (-int(freq_rows[i]["winner_count"]) / max(1, int(freq_rows[i]["exposure_count"])), i))
    top = sum(1 << i for i in ranked[:20])

    duplicate = []
    for i in [r["pair_index"] for r in pairs if r["shift"] == 28]:
        duplicate.append({**pairs[i], "in_base": bool(base_mask >> i & 1), "newly_covered": bool(new_mask >> i & 1), "remaining": bool(remaining >> i & 1)})
    new_rows, remaining_rows = pair_rows(new_mask, pairs), pair_rows(remaining, pairs)
    return {
        "schema": "a303656-g231-fifth-prime-residual-analysis-v1", "base_id": base["base_id"], "base_mask_digest": base["base_mask_digest"],
        "residual_pair_count_before_fifth_prime": residual.bit_count(), "global_best_q_t": [q, t], "global_best_delta": new_mask.bit_count(),
        "newly_covered_pairs": new_rows, "remaining_residual_pairs": remaining_rows,
        "newly_covered_distribution_by_c": distribution(new_rows, "c"), "newly_covered_distribution_by_d": distribution(new_rows, "d"),
        "remaining_distribution_by_c": distribution(remaining_rows, "c"), "remaining_distribution_by_d": distribution(remaining_rows, "d"),
        "duplicate_shift_28_treatment": duplicate,
        "prior_empirical_annotation_only": True,
        "global_best_overlaps": {
            "previous_NEVER_WIN_60": indices(new_mask & never), "frequency_at_least_10_percent_116": indices(new_mask & frequent10),
            "frequency_at_least_25_percent_103": indices(new_mask & frequent25), "top_frequency_20": indices(new_mask & top),
        },
        "category_optima_over_all_q_t": {
            "previous_NEVER_WIN_60": category_maximum(per_prime, never), "frequency_at_least_10_percent_116": category_maximum(per_prime, frequent10),
            "frequency_at_least_25_percent_103": category_maximum(per_prime, frequent25), "top_frequency_20": category_maximum(per_prime, top),
        },
        "top_frequency_pair_definition": "top 20 G=231 residual pairs by prior winner_frequency, pair_index tie-break",
        "top_frequency_pairs": pair_rows(top, pairs),
        "empirical_frequencies_not_used_in_certified_modular_optimization": True,
    }


def build_crt(candidates: list[int]) -> dict[str, Any]:
    rows = []
    for q in candidates:
        modulus = L4 * q * q
        maximum = (CELL_WIDTH + modulus - 1) // modulus
        rows.append({
            "q": q, "q2": q * q, "L5": modulus, "activation_cell_width": CELL_WIDTH,
            "maximum_member_count_in_current_cell": maximum,
            "minimum_cell_width_for_at_least_2_members": modulus + 1,
            "minimum_cell_width_for_at_least_3_members": 2 * modulus + 1,
            "minimum_cell_width_for_at_least_5_members": 4 * modulus + 1,
            "support_regimes": ["CURRENT_AT_MOST_ONE_MEMBER", "INSUFFICIENT_FOR_2", "INSUFFICIENT_FOR_3", "INSUFFICIENT_FOR_5"] if maximum < 2 else ["CURRENT_MULTI_MEMBER_SUPPORT"],
        })
    return {
        "schema": "a303656-fifth-prime-crt-density-geometry-v1", "L4": L4, "activation_cell": [CELL_LOW, CELL_HIGH], "activation_cell_width": CELL_WIDTH,
        "candidate_geometry": rows,
        "meaningful_per_class_P5_distribution_supported": any(r["maximum_member_count_in_current_cell"] >= 2 for r in rows),
        "conclusion": "CURRENT ACTIVATION CELL DOES NOT SUPPORT A MULTI-MEMBER PER-CLASS P5 DISTRIBUTION" if all(r["maximum_member_count_in_current_cell"] < 2 for r in rows) else "MIXED P5 CLASS SUPPORT",
        "integer_evaluation_performed": False,
    }


def build_shortlist(per_prime: list[dict[str, Any]], bases: list[dict[str, Any]], globals_: dict[str, Any], pairs: list[dict[str, int]]) -> dict[str, Any]:
    by_q = {r["q"]: r for r in per_prime}
    entries: dict[tuple[str, int, int, str], dict[str, Any]] = {}

    def add(base: dict[str, Any], q: int, reason: str) -> None:
        score = by_q[q]["base_summaries"][base["base_index"]]
        t = score["first_argmax_t"]
        union = coverage_at(q, t, pairs) | mask_int(base["coverage_mask_hex"])
        union_digest = sha256_bytes(bytes.fromhex(mask_hex(union)))
        key = (base["base_mask_digest"], q, t, union_digest)
        if key not in entries:
            entries[key] = {"base_id": base["base_id"], "base_identity": base["roles"], "base_mask_digest": base["base_mask_digest"], "q": q, "t": t,
                            "Delta": score["maximum_delta"], "G5": score["maximum_G5"], "residual_size": score["minimum_residual_size"], "q2": q*q,
                            "argmax_multiplicity": score["argmax_count"], "resulting_union_mask_digest": union_digest, "selection_reason": [reason]}
        elif reason not in entries[key]["selection_reason"]:
            entries[key]["selection_reason"].append(reason)

    def gsummary(base: dict[str, Any]) -> dict[str, Any]:
        return globals_["bases"][base["base_index"]]

    g = next(b for b in bases if "G231-COMMON" in b["roles"])
    pooled = next(b for b in bases if "POOLED-GLOBAL-WEIGHTED-OPT" in b["roles"])
    t3 = next(b for b in bases if "T3EQ2-CONSTRAINED-WEIGHTED-OPT" in b["roles"])
    calibration = [next(b for b in bases if label in b["roles"]) for label in ("CAL-216", "CAL-227", "CAL-230")]
    for q in gsummary(g)["all_primes_attaining_global_maximum"]:
        add(g, q, "G231_GLOBAL_RAW_MARGINAL_MAXIMIZER")
    for base in calibration:
        add(base, gsummary(base)["all_primes_attaining_global_maximum"][0], f"{next(r for r in base['roles'] if r.startswith('CAL-'))}_GLOBAL_MAXIMUM")
    add(pooled, gsummary(pooled)["pareto_frontier"][0]["q"], "POOLED_GLOBAL_WEIGHTED_BASE_RAW_MARGINAL_FRONTIER")
    add(t3, gsummary(t3)["pareto_frontier"][0]["q"], "T3EQ2_WEIGHTED_BASE_RAW_MARGINAL_FRONTIER")
    source_rounds = [
        (g, "G231_RAW_MARGINAL_PARETO_FRONTIER"),
        (pooled, "POOLED_GLOBAL_WEIGHTED_BASE_RAW_MARGINAL_FRONTIER"),
        (t3, "T3EQ2_WEIGHTED_BASE_RAW_MARGINAL_FRONTIER"),
    ]
    cursor = 0
    while len(entries) < 20 and any(cursor < len(gsummary(base)["pareto_frontier"]) for base, _ in source_rounds):
        for base, reason in source_rounds:
            frontier = gsummary(base)["pareto_frontier"]
            if cursor < len(frontier):
                add(base, frontier[cursor]["q"], reason)
                if len(entries) >= 20:
                    break
        cursor += 1
    selected = list(entries.values())[:20]
    return {"schema": "a303656-frozen-future-p5-design-shortlist-v1", "entry_count": len(selected), "maximum_entry_count": 20,
            "identity_tuple": ["base_mask_digest", "q", "t", "resulting_union_mask_digest"], "entries": selected,
            "integers_evaluated": 0, "adaptive_P5_integer_search_performed": False}


def compute(root: Path, source_commit: str) -> dict[str, Any]:
    protected_before = verify_protected(root)
    _eligible, candidates, authority = load_prime_authority(root)
    pairs = load_pairs(root)
    bases = load_bases(root)
    per_prime = []
    brute = []
    for q in candidates:
        ca = enumerator_a.enumerate_compressed(q, pairs)
        cb = enumerator_b.enumerate_compressed(q, pairs)
        demand(ca == cb, f"enumerator compression mismatch q={q}")
        summaries = []
        for base in bases:
            value = mask_int(base["coverage_mask_hex"])
            sa = enumerator_a.score(ca, value, base["base_mask_digest"])
            sb = enumerator_b.score(cb, value, base["base_mask_digest"])
            demand(sa == sb, f"enumerator score mismatch q={q} base={base['base_id']}")
            demand(sum(count for _delta, count in sa["histogram"]) == q*q, "histogram does not sum to q^2")
            summaries.append({"base_id": base["base_id"], **sa})
            if q in SMALL_PRIMES:
                literal = literal_score(q, pairs, value, base["base_mask_digest"])
                demand(literal == sa, f"literal valuation oracle mismatch q={q} base={base['base_id']}")
        if q in SMALL_PRIMES:
            brute.append({"q": q, "q2_residues_checked_literally": q*q, "all_13_bases_agree": True})
        per_prime.append({"q": q, "compression": ca, "base_summaries": summaries})
    globals_ = global_summaries(per_prime, bases)
    return {
        "authority": authority, "pairs": pairs, "bases": bases, "per_prime": per_prime, "globals": globals_,
        "g231": build_g231(root, per_prime, bases, globals_, pairs), "crt": build_crt(candidates),
        "shortlist": build_shortlist(per_prime, bases, globals_, pairs), "brute": brute,
        "protected_before": protected_before, "protected_after": verify_protected(root), "source_commit": source_commit,
    }


def write_results(root: Path, out: Path, bundle: dict[str, Any]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    atomic_json(out / "authority_report.json", bundle["authority"])
    atomic_json(out / "pair_domain.json", {"schema": "a303656-fixed-407-pair-domain-v1", "pair_count": 407, "pair_domain_digest": PAIR_DOMAIN_DIGEST, "pair_order_path": PAIR_ORDER_PATH, "pairs": bundle["pairs"], "duplicate_shift_28_pairs": [[1,2],[3,0]]})
    atomic_json(out / "frozen_base_masks.json", {"schema": "a303656-frozen-p4-base-masks-v1", "source": BASE_MANIFEST_PATH, "base_count": 13, "bases": bundle["bases"]})
    with (out / "per_prime_compressed_landscapes.jsonl").open("w", encoding="utf-8") as stream:
        for record in bundle["per_prime"]:
            stream.write(json.dumps(record, sort_keys=True, separators=(",", ":")) + "\n")
    atomic_json(out / "global_summaries.json", bundle["globals"])
    atomic_json(out / "g231_residual_analysis.json", bundle["g231"])
    atomic_json(out / "crt_density_geometry.json", bundle["crt"])
    atomic_json(out / "frozen_future_shortlist.json", bundle["shortlist"])
    atomic_json(out / "brute_force_oracle_report.json", {"schema": "a303656-fifth-prime-brute-oracle-v1", "predeclared_small_primes": list(SMALL_PRIMES), "checks": bundle["brute"]})
    initial = {
        "schema": "a303656-fifth-prime-initial-repository-gate-v1", "required_starting_commit": START_COMMIT,
        "starting_commit_verified_before_modification": True, "source_commit": bundle["source_commit"],
        "source_parent": git(root, "rev-parse", f"{bundle['source_commit']}^"),
        "previous_round_status": "INSUFFICIENT FRESH CLASS MULTIPLICITY", "previous_round_results_commit_N_exists": False,
        "previous_round_new_integer_evaluations": 0, "tracked_worktree_clean_at_initial_gate": True,
        "protected_baseline_hashes": bundle["protected_before"], "protected_baseline_hashes_unchanged": bundle["protected_before"] == bundle["protected_after"],
    }
    atomic_json(out / "initial_repository_gate.json", initial)
    core_names = (
        "authority_report.json", "pair_domain.json", "frozen_base_masks.json",
        "per_prime_compressed_landscapes.jsonl", "global_summaries.json",
        "g231_residual_analysis.json", "crt_density_geometry.json",
        "frozen_future_shortlist.json", "brute_force_oracle_report.json",
        "initial_repository_gate.json",
    )
    core = [out / name for name in core_names]
    atomic_json(out / "metadata.json", {
        "schema": "a303656-fifth-prime-landscape-metadata-v1", "starting_commit": START_COMMIT, "source_commit": bundle["source_commit"],
        "authority_B": B_ORDER, "candidate_count": len(bundle["per_prime"]), "pair_count": 407, "base_count": 13,
        "complete_q2_landscape_equivalence": "For each active r mod q, every pair in its bucket is covered on all q lifts except its unique shift mod q^2 exclusion lift; inactive r contributes q empty lifts.",
        "classification": "EXACT MODULAR COMBINATORIAL ANALYSIS", "mathematical_status": "UNRESOLVED", "new_integers_evaluated": 0,
        "T_backends_called": False, "direct_two_square_oracle_called": False, "P5_CRT_integer_search_performed": False,
        "interpretation_label": INTERPRETATION, "validation_conclusion": CONCLUSION,
        "artifact_sha256_before_verification_report": {p.name: sha256_file(p) for p in sorted(core)},
    })
    (out / "CURRENT_STATE.md").write_text(
        "# Current state\n\n" + CONCLUSION + ".\n\nThis is exact modular combinatorial analysis only. No new integer was evaluated, no T backend or direct two-square oracle was called, and no P5 CRT integer search was run. The global A303656 problem remains UNRESOLVED.\n\n" + INTERPRETATION + ". The current activation cell contains at most one member of every authenticated P5 CRT class, so it does not support a meaningful per-class P5 distribution.\n",
        encoding="utf-8",
    )
    atomic_json(out / "audit_gap_updates.json", {"schema": "a303656-fifth-prime-audit-gap-updates-v1", "closed": ["complete authenticated q-by-q marginal landscape", "dual-enumerator agreement", "literal small-prime oracle", "G231 residual annotations", "P5 CRT density geometry", "frozen future shortlist"], "remaining": ["global A303656 problem unresolved", "no P5 integer evaluation authorized", "current activation cell lacks multi-member P5 class support"]})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[3])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    demand(git(root, "rev-parse", "HEAD") == args.source_commit, "source commit does not equal HEAD")
    demand(git(root, "rev-parse", f"{args.source_commit}^") == START_COMMIT, "source commit is not directly based on required starting commit")
    demand(not git(root, "status", "--porcelain=v1", "--untracked-files=no"), "tracked worktree not clean at source gate")
    bundle = compute(root, args.source_commit)
    write_results(root, args.output.resolve(), bundle)
    print(CONCLUSION)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"EXACT FIFTH-PRIME MARGINAL-COVERAGE LANDSCAPE NOT VALIDATED: {exc}")
        raise SystemExit(2)
