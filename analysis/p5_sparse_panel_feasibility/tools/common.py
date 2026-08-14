#!/usr/bin/env python3
"""Exact modular and provenance contracts for the P5 sparse feasibility audit.

This module deliberately contains no T(n), factorization, two-square, or direct
oracle implementation.  It only reads authenticated artifacts, performs exact
finite residue arithmetic, constructs CRT classes, and normalizes registries.
"""

from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any, Iterable


START_COMMIT = "c710dcc9b472a8500b038a33db1315043cffca6e"
CHAIN = (
    "02028314ab92d7aa089475f9a6bc96688526f731",
    "ac161b0f6a60c6453c33b4b94435881a49dc62d0",
    START_COMMIT,
)
P4 = (3, 7, 11, 23)
P4_SQUARES = (9, 49, 121, 529)
M4 = 28_227_969
L4 = 1_129_118_760
N0_MOD_40 = 34
PAIR_COUNT = 407
MASK_BYTES = 51
CELL_LOW = 183_968_950_234
CELL_HIGH = 246_731_069_451
CELL_WIDTH = CELL_HIGH - CELL_LOW + 1

SHORTLIST = "analysis/fifth_prime_marginal_coverage/results/frozen_future_shortlist.json"
GLOBALS = "analysis/fifth_prime_marginal_coverage/results/global_summaries.json"
LANDSCAPES = "analysis/fifth_prime_marginal_coverage/results/per_prime_compressed_landscapes.jsonl"
BASES = "analysis/fifth_prime_marginal_coverage/results/frozen_base_masks.json"
BASE_MANIFEST = "analysis/p4_weighted_transferability/results/candidate_manifest_holdout_v2.json"
PAIR_ORDER = "analysis/k4_survivor_incidence/pair_order.csv"

PROTECTED_HASHES = {
    "README.md": "9c1f11b8ba76e0d0ff70d3d0dc5f8b1b528e1e31405b27be9b047bdcc3916a8b",
    "REPORT_zh.md": "833e66fd88c27412e2522448f17075baf4e85828080c22ca2e87a12f30f77649",
    "output/formal_results_audit.json": "fe87b53734fe9f8978396428769af5db76fb35709276241f36c49c2a9145b533",
    "output/final_packaging_audit.json": "de8f4d351b809b03daac280879eddc69a795fce50f9c8f6b2d786ad2f9d611ca",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt": "510ac25107f8764fbacb3fe10f2c67de1a5cc595b20a23f793ff77dd54d5ec42",
    SHORTLIST: "3b369ade30c2ee0925a19872bf317ea2bc5116812904bff5ad7d8d870eb9c561",
    GLOBALS: "15fb6f90c47e2929358eb4d7f90ea16030d7cd786edf594a46ed728bf52d593d",
    LANDSCAPES: "e5bd40c1db3f85970629488e03bbf0aaf724607ab87c812226c9b138bae15df2",
    BASES: "11d54f3c9d714c36bd6afd130a30daa0e074f71b106052bb10fe4889361a88a3",
    BASE_MANIFEST: "728fd5195d91c75b2b93ae02e4ad43aea07afb6fd6a511c54596d0658bc6e1ca",
    PAIR_ORDER: "5f3b6ea52f9d3d5e544f10ae17a3752cbf1a476d9575a2e0a6ae4c502ed0452b",
}

REGISTRY_COMPONENT_HASHES = {
    "output/formal_results_audit.json": PROTECTED_HASHES["output/formal_results_audit.json"],
    "output/tn_pilot_20260713/pilot_a/bitset/counts.csv": "cf53f054c6a3055083470e45e2bafa9d2f5bc3a1d62b5c912bf255e87910bd2d",
    "output/tn_pilot_20260713/pilot_b/bitset/counts.csv": "2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773",
    "analysis/obstruction_dossier/panel.json": "0229d9e1ca696660f3478b17f1bccbe6983cc49a74bbf63af0018f39f086ca8a",
    "analysis/p2_core/corrected_controls.json": "",  # filled and checked through provenance output
    "analysis/k4_ap_pilot/backend_a_counts.csv": "dad853ae1b385ef44ef67b442d5b3b82c78614a4fc99c77530ba6903ede49e23",
    "analysis/k4_ap_pilot/direct_verification.json": "3ec8be67747e64d5046dc9c3591c8885865b897f3d02c18be8fd5b01ee201794",
    "analysis/k4_survivor_incidence/metadata.json": "8f6c3b203ab568f57f8c2178a140dc67d9ef4c422c76a96d8afc1b8a04ad0109",
    "analysis/p4_maximizer_census/class_panel.csv": "3d4b2675df302b518ec5c32f7d63573604efbfee4143e6db16d4da80819af679",
    "analysis/p4_maximizer_census/backend_a_counts.csv": "eaebc0d7cfb76da23332ec9dcf89a79fbd3968b94a28b6cd2621710757373c16",
    "analysis/p4_maximizer_census/direct_verification.json": "246d4067b4f7f80d88377ef17fa5732d0c4a9bf998ccd79c0dda94b0938abbaf",
    "analysis/p4_weighted_transferability/results/direct_oracle_selection_manifest.json": "5d15b9162e937882aaface73c46fd05cff2c784259154e2a52e98aecb90a0086",
    "analysis/p4_weighted_transferability/results/metadata.json": "91955d84509ac8eb69e3932b4b04a9873c305c9b93d3f845992a95cd9ec1288c",
}

ANCHOR_ROLES = (
    "G231-COMMON",
    "POOLED-GLOBAL-WEIGHTED-OPT",
    "T3EQ2-CONSTRAINED-WEIGHTED-OPT",
    "CAL-216",
    "CAL-227",
    "CAL-230",
)


class AuditError(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise AuditError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canonical_bytes(value: Any) -> bytes:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode()


def canonical_digest(value: Any) -> str:
    return hashlib.sha256(canonical_bytes(value)).hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write("\n")
    temporary.replace(path)


def write_jsonl(path: Path, rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True, separators=(",", ":")))
            stream.write("\n")
    temporary.replace(path)


def verify_hashes(root: Path, hashes: dict[str, str]) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in hashes.items():
        path = root / relative
        demand(path.is_file(), f"authority missing: {relative}")
        actual = sha256_file(path)
        if expected:
            demand(actual == expected, f"authority hash mismatch: {relative}")
        observed[relative] = actual
    return observed


def mask_int(value: str) -> int:
    demand(isinstance(value, str) and len(value) == 2 * MASK_BYTES, "mask width mismatch")
    raw = bytes.fromhex(value)
    demand(raw[-1] & 0x80 == 0, "mask tail outside 407-bit domain")
    return int.from_bytes(raw, "little")


def mask_digest(mask: int) -> str:
    demand(mask >= 0 and mask >> PAIR_COUNT == 0, "mask outside domain")
    return hashlib.sha256(mask.to_bytes(MASK_BYTES, "little")).hexdigest()


def load_pairs(root: Path) -> list[dict[str, int]]:
    with (root / PAIR_ORDER).open(newline="", encoding="utf-8") as stream:
        rows = [{key: int(row[key]) for key in ("pair_index", "c", "d", "shift")} for row in csv.DictReader(stream)]
    demand(len(rows) == PAIR_COUNT, "pair count changed")
    demand([r["pair_index"] for r in rows] == list(range(PAIR_COUNT)), "pair order changed")
    demand(all(r["shift"] == 3 ** r["c"] + 5 ** r["d"] for r in rows), "inexact pair shift")
    demand([(r["c"], r["d"]) for r in rows if r["shift"] == 28] == [(1, 2), (3, 0)], "duplicate shift identities collapsed")
    return rows


def load_bases(root: Path) -> list[dict[str, Any]]:
    value = load_json(root / BASES)
    bases = value["bases"]
    demand(value["base_count"] == 13 and len(bases) == 13, "frozen base count changed")
    for index, base in enumerate(bases, 1):
        demand(base["base_id"] == f"BASE-{index:02d}", "base order changed")
        mask = mask_int(base["coverage_mask_hex"])
        demand(mask.bit_count() == base["G"], "base G mismatch")
        demand(mask_digest(mask) == base["base_mask_digest"], "base digest mismatch")
    return bases


def load_shortlist(root: Path) -> dict[str, Any]:
    value = load_json(root / SHORTLIST)
    entries = value.get("entries")
    demand(value.get("entry_count") == 20 and isinstance(entries, list) and len(entries) == 20, "shortlist count changed")
    demand(value.get("integers_evaluated") == 0 and not value.get("adaptive_P5_integer_search_performed"), "shortlist scope changed")
    identities = [(e["base_mask_digest"], e["q"], e["t"], e["resulting_union_mask_digest"]) for e in entries]
    demand(len(identities) == len(set(identities)), "shortlist identity duplication")
    return value


def load_landscapes(root: Path) -> dict[int, dict[str, Any]]:
    rows = [json.loads(line) for line in (root / LANDSCAPES).read_text(encoding="utf-8").splitlines() if line]
    demand(len(rows) == 524 and len({r["q"] for r in rows}) == len(rows), "compressed landscape q coverage changed")
    return {r["q"]: r for r in rows}


def coverage_for_prime(q: int, t: int, pairs: list[dict[str, int]]) -> int:
    q2 = q * q
    demand(0 <= t < q2, "unauthorized t outside q^2")
    value = 0
    for row in pairs:
        difference = t - row["shift"]
        if difference % q == 0 and difference % q2 != 0:
            value |= 1 << row["pair_index"]
    return value


def p4_residue_tables(pairs: list[dict[str, int]]) -> list[list[int]]:
    result: list[list[int]] = []
    for prime, modulus in zip(P4, P4_SQUARES):
        table = []
        for residue in range(modulus):
            mask = 0
            for row in pairs:
                delta = residue - row["shift"]
                if delta % prime == 0 and delta % modulus != 0:
                    mask |= 1 << row["pair_index"]
            table.append(mask)
        result.append(table)
    return result


def enumerate_base_tuples(bases: list[dict[str, Any]], pairs: list[dict[str, int]]) -> dict[str, list[tuple[int, int, int, int]]]:
    target = {mask_int(base["coverage_mask_hex"]): base["base_id"] for base in bases}
    demand(len(target) == len(bases), "duplicate base masks")
    found = {base["base_id"]: [] for base in bases}
    tables = p4_residue_tables(pairs)
    for t3 in range(9):
        m3 = tables[0][t3]
        for t7 in range(49):
            m37 = m3 | tables[1][t7]
            for t11 in range(121):
                m3711 = m37 | tables[2][t11]
                for t23 in range(529):
                    base_id = target.get(m3711 | tables[3][t23])
                    if base_id is not None:
                        found[base_id].append((t3, t7, t11, t23))
    demand(sum(map(len, found.values())) == 336, "fixed-P4 target tuple total changed")
    demand(all(rows == sorted(set(rows)) for rows in found.values()), "fixed-P4 tuple ordering/uniqueness failure")
    return found


def crt(residues: Iterable[int], moduli: Iterable[int]) -> tuple[int, int]:
    x, modulus = 0, 1
    for residue, next_modulus in zip(residues, moduli):
        demand(math.gcd(modulus, next_modulus) == 1, "CRT moduli not coprime")
        x += modulus * (((residue - x) * pow(modulus, -1, next_modulus)) % next_modulus)
        modulus *= next_modulus
        x %= modulus
    return x, modulus


def build_class(tuple4: tuple[int, int, int, int], q: int, t: int) -> tuple[int, int]:
    q2 = q * q
    residue, modulus = crt((*tuple4, t, N0_MOD_40), (*P4_SQUARES, q2, 40))
    demand(modulus == L4 * q2, "P5 CRT modulus mismatch")
    for r, m in zip((*tuple4, t, N0_MOD_40), (*P4_SQUARES, q2, 40)):
        demand(residue % m == r, "P5 CRT congruence failure")
    return residue, modulus


def class_member(residue: int, modulus: int) -> list[int]:
    first = CELL_LOW + ((residue - CELL_LOW) % modulus)
    if first > CELL_HIGH:
        return []
    result = list(range(first, CELL_HIGH + 1, modulus))
    demand(len(result) <= 1, "activation cell class has more than one member")
    return result


def merge_intervals(intervals: Iterable[tuple[int, int]]) -> list[list[int]]:
    ordered = sorted(intervals)
    result: list[list[int]] = []
    for low, high in ordered:
        demand(0 <= low <= high, "invalid prior interval")
        if result and low <= result[-1][1] + 1:
            result[-1][1] = max(result[-1][1], high)
        else:
            result.append([low, high])
    return result


def ints_in_json(value: Any) -> set[int]:
    result: set[int] = set()
    if isinstance(value, dict):
        n = value.get("n")
        if isinstance(n, int):
            result.add(n)
        elif isinstance(n, str) and n.isdigit():
            result.add(int(n))
        for child in value.values():
            result |= ints_in_json(child)
    elif isinstance(value, list):
        for child in value:
            result |= ints_in_json(child)
    return result


def csv_points(path: Path) -> list[int]:
    with path.open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    demand(rows and "n" in rows[0], f"n column missing: {path}")
    return [int(row["n"]) for row in rows]


def point_in_intervals(n: int, intervals: list[list[int]]) -> bool:
    return any(low <= n <= high for low, high in intervals)


def build_prior_registry(root: Path) -> dict[str, Any]:
    component_hashes = verify_hashes(root, REGISTRY_COMPONENT_HASHES)
    formal = load_json(root / "output/formal_results_audit.json")
    demand(formal.get("audit_status") == "PASS", "formal result audit not certified")
    raw_intervals: list[tuple[int, int]] = []
    interval_sources: list[dict[str, Any]] = []

    def add_interval(label: str, low: Any, high: Any, source: str) -> None:
        pair = (int(low), int(high))
        raw_intervals.append(pair)
        interval_sources.append({"label": label, "low": pair[0], "high": pair[1], "source": source})

    direct = formal["direct_original_representation_search"]
    for dataset in direct["datasets"]:
        if "low" in dataset:
            add_interval(dataset["label"], dataset["low"], dataset["high"], "formal/direct")
        else:
            for index, window in enumerate(dataset["windows"]):
                add_interval(f"{dataset['label']}/{index}", window["low"], window["high"], "formal/direct")
    factors = formal["all_prime_factor_certificate_search"]
    for group in ("dual_implementation_results", "single_implementation_results"):
        for row in factors[group]:
            add_interval(row["label"], row["low"], row["high"], f"formal/factor/{group}")
    fixed = formal["fixed_pool_method_C"]
    add_interval("fixed_pool_method_C", fixed["low"], fixed["high"], "formal/fixed-pool")

    pilot_specs = (
        ("PILOT-A", "output/tn_pilot_20260713/pilot_a/bitset/counts.csv"),
        ("PILOT-B", "output/tn_pilot_20260713/pilot_b/bitset/counts.csv"),
    )
    for label, relative in pilot_specs:
        values = csv_points(root / relative)
        demand(values == list(range(values[0], values[-1] + 1)), f"{label} is not a complete interval")
        add_interval(label, values[0], values[-1], relative)

    intervals = merge_intervals(raw_intervals)
    sparse_components: list[dict[str, Any]] = []
    sparse: set[int] = set()

    def add_sparse(label: str, relative: str, values: Iterable[int], semantics: str) -> None:
        points = sorted(set(values))
        sparse.update(points)
        sparse_components.append({
            "label": label, "path": relative, "sha256": sha256_file(root / relative),
            "point_count": len(points), "point_digest": canonical_digest(points), "semantics": semantics,
        })

    dossier = "analysis/obstruction_dossier/panel.json"
    add_sparse("selected-dossier", dossier, ints_in_json(load_json(root / dossier)), "selected dossier and regression points")
    controls = "analysis/p2_core/corrected_controls.json"
    add_sparse("p2-corrected-controls", controls, ints_in_json(load_json(root / controls)), "no-new-evaluation controls inherited from pilots/dossier")
    k4 = "analysis/k4_ap_pilot/backend_a_counts.csv"
    add_sparse("K4-progression-panel", k4, csv_points(root / k4), "complete T and winner-mask panel")
    p4 = "analysis/p4_maximizer_census/class_panel.csv"
    add_sparse("fixed-P4-maximizer-census", p4, csv_points(root / p4), "complete T and winner-mask panel")
    k4_direct = "analysis/k4_ap_pilot/direct_verification.json"
    add_sparse("K4-direct-oracle-representatives", k4_direct, ints_in_json(load_json(root / k4_direct)), "direct-oracle subset of K4 panel")
    p4_direct = "analysis/p4_maximizer_census/direct_verification.json"
    add_sparse("P4-direct-oracle-representatives", p4_direct, ints_in_json(load_json(root / p4_direct)), "direct-oracle subset of P4 census")
    weighted = "analysis/p4_weighted_transferability/results/direct_oracle_selection_manifest.json"
    add_sparse("weighted-direct-oracle-selection", weighted, ints_in_json(load_json(root / weighted)), "frozen direct-oracle subset of P4 census")

    k4_points = set(csv_points(root / k4))
    p4_points = set(csv_points(root / p4))
    demand(set(ints_in_json(load_json(root / k4_direct))) <= k4_points, "K4 oracle points outside K4 panel")
    demand(set(ints_in_json(load_json(root / p4_direct))) <= p4_points, "P4 oracle points outside P4 panel")
    demand(set(ints_in_json(load_json(root / weighted))) <= p4_points, "weighted selection outside P4 panel")
    demand(all(point_in_intervals(n, intervals) for n in ints_in_json(load_json(root / dossier))), "dossier point outside certified intervals")

    points = sorted(sparse)
    normalized = {"interval_union": intervals, "sparse_points": points}
    completeness = {
        "status": "CERTIFIED COMPLETE",
        "baseline_formal_intervals_from_final_audit": True,
        "pilot_A_and_B_complete": True,
        "selected_dossier_covered": True,
        "p2_audit_added_no_new_integer": True,
        "K4_progression_panel_complete": True,
        "K4_survivor_audit_reused_same_panel": True,
        "fixed_P4_landscape_added_no_integer": True,
        "fixed_P4_maximizer_census_complete": True,
        "weighted_audit_added_no_integer_and_oracle_selection_is_census_subset": True,
        "corrected_holdout_commit_is_source_only": True,
        "fifth_prime_landscape_added_no_integer": True,
        "history_results_chain": [
            "73fbec4", "3a93ab7", "6e35761", "2f87e5f", "406677c", "b76d097",
            "ae75d96", "d547130", "7b4515f", "0202831", "c710dcc",
        ],
    }
    return {
        "schema": "a303656-complete-prior-evaluation-registry-v1",
        "completeness": completeness,
        "raw_interval_count": len(raw_intervals),
        "interval_union": intervals,
        "interval_union_count": len(intervals),
        "interval_sources": interval_sources,
        "sparse_points": points,
        "sparse_point_count": len(points),
        "sparse_components": sparse_components,
        "component_hashes": component_hashes,
        "normalized_registry_digest": canonical_digest(normalized),
        "normalization": "inclusive intervals merged when overlapping or adjacent; sparse points integer-sorted and deduplicated",
    }


def registry_contains(registry: dict[str, Any], n: int) -> bool:
    return point_in_intervals(n, registry["interval_union"]) or n in set(registry["sparse_points"])


def evenly_spaced_indices(count: int, selected: int) -> list[int]:
    demand(1 <= selected <= count, "invalid deterministic selection size")
    if selected == 1:
        return [0]
    result = [j * (count - 1) // (selected - 1) for j in range(selected)]
    demand(len(result) == len(set(result)) and result[0] == 0 and result[-1] == count - 1, "evenly-spaced index failure")
    return result
