#!/usr/bin/env python3
"""Exact contracts for the corrected fixed-P4 out-of-mask holdout census."""

from __future__ import annotations

import csv
import hashlib
import json
import os
from collections import Counter
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


START_COMMIT = "7b4515f463af373bf341407878171b627c7aadc1"
P4 = (3, 7, 11, 23)
SQUARE_MODULI = (9, 49, 121, 529)
M4 = 28_227_969
L = 1_129_118_760
N0 = 240_000_005_594
A = 183_968_950_234
B = 246_731_069_451
PAIR_COUNT = 407
MASK_BYTES = 51
THRESHOLDS = (15, 16, 18, 20, 24)

V2_REL = "analysis/p4_weighted_transferability/results/candidate_manifest_holdout_v2.json"
ORIGINAL_REL = "analysis/p4_weighted_transferability/results/candidate_manifest.json"
MAXIMA_REL = "analysis/p4_weighted_transferability/results/weighted_maxima.json"
WEIGHTS_REL = "analysis/p4_weighted_transferability/results/exact_weight_table.csv"
PAIR_ORDER_REL = "analysis/k4_survivor_incidence/pair_order.csv"

PROTECTED_HASHES = {
    "README.md": "9c1f11b8ba76e0d0ff70d3d0dc5f8b1b528e1e31405b27be9b047bdcc3916a8b",
    "REPORT_zh.md": "833e66fd88c27412e2522448f17075baf4e85828080c22ca2e87a12f30f77649",
    "output/formal_results_audit.json": "fe87b53734fe9f8978396428769af5db76fb35709276241f36c49c2a9145b533",
    "output/final_packaging_audit.json": "de8f4d351b809b03daac280879eddc69a795fce50f9c8f6b2d786ad2f9d611ca",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt": "510ac25107f8764fbacb3fe10f2c67de1a5cc595b20a23f793ff77dd54d5ec42",
    ORIGINAL_REL: "1a2d5de264df04555afdf7b22d6d9650d1973a115d885d3c975b1eaf6061b14d",
    MAXIMA_REL: "98f9b675ab9746ceb9c5588deebeacfa2a4467143efd6465ef155361fa02ed76",
    WEIGHTS_REL: "2f39089d4850a861117b8c1ff189b4130abf9f4db9b521895ec52f6e25499bc7",
    "analysis/p4_weighted_transferability/results/verification_report.json": "94eabda766735610f0018c477c1ae7861e002d72cae5e1030aef266e98ffb2c3",
    PAIR_ORDER_REL: "5f3b6ea52f9d3d5e544f10ae17a3752cbf1a476d9575a2e0a6ae4c502ed0452b",
    "output/tn_pilot_20260713/pilot_a/bitset/counts.csv": "cf53f054c6a3055083470e45e2bafa9d2f5bc3a1d62b5c912bf255e87910bd2d",
    "output/tn_pilot_20260713/pilot_b/bitset/counts.csv": "2546df39a90d10fc349123f599f4da09abb3798f11e85a578787effb7d9ef773",
    "analysis/k4_ap_pilot/backend_a_counts.csv": "dad853ae1b385ef44ef67b442d5b3b82c78614a4fc99c77530ba6903ede49e23",
    "analysis/p4_maximizer_census/backend_a_counts.csv": "eaebc0d7cfb76da23332ec9dcf89a79fbd3968b94a28b6cd2621710757373c16",
    "src/k4_ap_backend_a.cpp": "a1e0607a48687970614b9b4042837c3a1a82fc1a874aee36281943b48f527042",
    "src/k4_ap_backend_b.cpp": "40a6a833e6efd18cee09b945557420d6ec6c8bd6cb609920964d6e26c602745a",
    "src/p4_census_direct_oracle.cpp": "f1a8aa8ba590155ec4823d87d1932936ce38efb64f644f04eefe26258160dc95",
}

PRIOR_T_PANELS = (
    ("PILOT-A", "output/tn_pilot_20260713/pilot_a/bitset/counts.csv"),
    ("PILOT-B", "output/tn_pilot_20260713/pilot_b/bitset/counts.csv"),
    ("K4-AP", "analysis/k4_ap_pilot/backend_a_counts.csv"),
    ("P4-MAXIMIZER", "analysis/p4_maximizer_census/backend_a_counts.csv"),
)


class HoldoutError(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise HoldoutError(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + f".tmp.{os.getpid()}")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def verify_protected(root: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in PROTECTED_HASHES.items():
        path = root / relative
        demand(path.is_file(), f"protected file missing: {relative}")
        actual = sha256_file(path)
        demand(actual == expected, f"protected hash mismatch for {relative}: {actual} != {expected}")
        observed[relative] = actual
    return observed


def powers(base: int, limit: int) -> list[tuple[int, int]]:
    result: list[tuple[int, int]] = []
    exponent, value = 0, 1
    while value <= limit:
        result.append((exponent, value))
        if value > limit // base:
            break
        exponent += 1
        value *= base
    return result


def canonical_pairs(root: Path | None = None) -> list[dict[str, int]]:
    rows = [
        {"pair_index": index, "c": c, "d": d, "shift": p3 + p5}
        for index, (c, d, p3, p5) in enumerate(
            (c, d, p3, p5)
            for c, p3 in powers(3, A)
            for d, p5 in powers(5, A)
            if p3 + p5 <= A
        )
    ]
    demand(len(rows) == PAIR_COUNT, "activation cell is not the constant 407-pair domain")
    demand([(row["c"], row["d"]) for row in rows if row["shift"] == 28] == [(1, 2), (3, 0)], "duplicate shift 28 identities were not retained")
    high = [(c, d, p3 + p5) for c, p3 in powers(3, B) for d, p5 in powers(5, B) if p3 + p5 <= B]
    demand([(row["c"], row["d"], row["shift"]) for row in rows] == high, "active domain changes inside the activation cell")
    if root is not None:
        with (root / PAIR_ORDER_REL).open(newline="", encoding="utf-8") as stream:
            committed = list(csv.DictReader(stream))
        observed = [(int(row["pair_index"]), int(row["c"]), int(row["d"]), int(row["shift"])) for row in committed]
        expected = [(row["pair_index"], row["c"], row["d"], row["shift"]) for row in rows]
        demand(observed == expected, "committed pair order differs from independently regenerated domain")
    return rows


def mask_int_to_hex(value: int) -> str:
    demand(value >= 0 and value >> PAIR_COUNT == 0, "mask integer outside 407-bit domain")
    return value.to_bytes(MASK_BYTES, "little").hex()


def mask_hex_to_int(value: str) -> int:
    demand(isinstance(value, str) and len(value) == 2 * MASK_BYTES, "coverage mask must be exactly 51 bytes")
    raw = bytes.fromhex(value)
    demand(raw[-1] & 0x80 == 0, "coverage mask has an out-of-domain tail bit")
    return int.from_bytes(raw, "little")


def coverage_mask(tuple4: tuple[int, int, int, int], pairs: list[dict[str, int]]) -> int:
    demand(len(tuple4) == 4, "tuple width differs from four")
    result = 0
    for p, modulus, residue in zip(P4, SQUARE_MODULI, tuple4):
        demand(0 <= residue < modulus, "tuple residue outside its prime-square modulus")
        for pair in pairs:
            difference = residue - pair["shift"]
            if difference % p == 0 and difference % modulus != 0:
                result |= 1 << pair["pair_index"]
    return result


def prime_residue_masks(pairs: list[dict[str, int]]) -> list[list[int]]:
    tables: list[list[int]] = []
    for p, modulus in zip(P4, SQUARE_MODULI):
        table: list[int] = []
        for residue in range(modulus):
            value = 0
            for pair in pairs:
                difference = residue - pair["shift"]
                if difference % p == 0 and difference % modulus != 0:
                    value |= 1 << pair["pair_index"]
            table.append(value)
        tables.append(table)
    return tables


def load_candidates(root: Path) -> list[dict[str, Any]]:
    original = load_json(root / ORIGINAL_REL)
    maxima = load_json(root / MAXIMA_REL)
    v2 = load_json(root / V2_REL)
    old = original.get("candidates")
    new = v2.get("candidates")
    demand(original.get("candidate_count") == 12 and isinstance(old, list) and len(old) == 12, "original candidate manifest is not exactly 12")
    demand(v2.get("candidate_count") == 13 and v2.get("distinct_coverage_mask_count") == 13 and isinstance(new, list) and len(new) == 13, "v2 candidate manifest is not exactly 13")
    demand(new[:12] == old, "v2 manifest did not preserve the original 12 candidate objects and order")
    optimum = maxima["maxima"]["t3eq2"]["pool"]
    demand(optimum.get("scope") == "t3eq2" and optimum.get("weights") == "pool", "wrong constrained optimum authority")
    demand(optimum.get("lexicographically_first_argmax") == [2, 13, 32, 13] and optimum.get("G") == 222, "certified constrained optimum tuple/G mismatch")
    demand(new[12].get("coverage_mask_hex") == optimum.get("coverage_mask_hex"), "v2 added mask differs from certified constrained optimum")
    demand(new[12].get("lexicographically_first_t3eq2_representative") == [2, 13, 32, 13], "v2 added tuple differs from certified constrained optimum")
    old_masks = [item["coverage_mask_hex"] for item in old]
    all_masks = [item["coverage_mask_hex"] for item in new]
    demand(len(set(old_masks)) == 12 and len(set(all_masks)) == 13 and all_masks[12] not in set(old_masks), "v2 mask distinctness/unique-addition failure")
    full_mask = maxima["maxima"]["full"]["pool"]["coverage_mask_hex"]
    demand(full_mask in all_masks, "pooled/global weighted optimum is absent")
    roles = {label for item in new for label in item.get("selected_by", [])}
    demand({"CAL-216", "CAL-227", "CAL-230", "G231-COMMON", "T3EQ2-WEIGHTED-OPT"} <= roles, "required calibration/control roles are absent")
    pairs = canonical_pairs(root)
    normalized: list[dict[str, Any]] = []
    for index, item in enumerate(new):
        value = mask_hex_to_int(item["coverage_mask_hex"])
        demand(value.bit_count() == item.get("G"), f"candidate {index} G/popcount mismatch")
        representative = item.get("lexicographically_first_t3eq2_representative")
        if representative is not None:
            demand(coverage_mask(tuple(representative), pairs) == value, f"candidate {index} representative does not generate its mask")
        labels = list(item.get("selected_by", []))
        special: list[str] = []
        if item["coverage_mask_hex"] == full_mask:
            special.append("POOLED-GLOBAL-WEIGHTED-OPT")
        if item["coverage_mask_hex"] == optimum["coverage_mask_hex"]:
            special.append("T3EQ2-CONSTRAINED-WEIGHTED-OPT")
        normalized.append({**item, "mask_index": index, "mask_id": f"MASK-{index + 1:02d}", "roles": sorted(set(labels + special)), "coverage_mask_int": value})
    return normalized


def crt(residues: Iterable[int], moduli: Iterable[int]) -> tuple[int, int]:
    x, modulus = 0, 1
    for residue, next_modulus in zip(residues, moduli):
        delta = ((residue - x) * pow(modulus, -1, next_modulus)) % next_modulus
        x = (x + modulus * delta) % (modulus * next_modulus)
        modulus *= next_modulus
    return x, modulus


def tuple_class_residue(tuple4: tuple[int, int, int, int]) -> int:
    residue, modulus = crt(tuple4, SQUARE_MODULI)
    demand(modulus == M4, "prime-square CRT modulus mismatch")
    combined, modulus = crt((residue, N0 % 40), (M4, 40))
    demand(modulus == L, "combined CRT modulus mismatch")
    return combined


def load_prior_t_points(root: Path) -> tuple[set[int], set[int], dict[str, Any]]:
    integers: set[int] = set()
    class_residues: set[int] = set()
    sources: list[dict[str, Any]] = []
    for label, relative in PRIOR_T_PANELS:
        with (root / relative).open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            demand(reader.fieldnames is not None and "n" in reader.fieldnames and "T" in reader.fieldnames, f"prior T panel schema mismatch: {label}")
            rows = list(reader)
        values = [int(row["n"]) for row in rows]
        demand(len(values) == len(set(values)), f"prior T panel duplicates n internally: {label}")
        integers.update(values)
        matching = {n % L for n in values if n % 40 == N0 % 40}
        class_residues.update(matching)
        sources.append({"label": label, "path": relative, "point_count": len(values), "matching_mod40_point_count": sum(n % 40 == N0 % 40 for n in values), "matching_mod40_distinct_class_count": len(matching), "sha256": sha256_file(root / relative)})
    return integers, class_residues, {"sources": sources, "distinct_prior_T_integer_count": len(integers), "distinct_excluded_CRT_class_count": len(class_residues)}


def enumerate_target_tuples(candidates: list[dict[str, Any]], pairs: list[dict[str, int]]) -> list[list[tuple[int, int, int, int]]]:
    targets = {item["coverage_mask_int"]: item["mask_index"] for item in candidates}
    demand(len(targets) == len(candidates), "candidate target masks are not distinct")
    tables = prime_residue_masks(pairs)
    found: list[list[tuple[int, int, int, int]]] = [[] for _ in candidates]
    for t3 in range(9):
        m3 = tables[0][t3]
        for t7 in range(49):
            m37 = m3 | tables[1][t7]
            for t11 in range(121):
                m3711 = m37 | tables[2][t11]
                for t23 in range(529):
                    index = targets.get(m3711 | tables[3][t23])
                    if index is not None:
                        found[index].append((t3, t7, t11, t23))
    demand(sum(len(items) for items in found) > 0, "exhaustive tuple enumeration found no target")
    for index, items in enumerate(found):
        demand(items == sorted(items) and len(items) == len(set(items)), f"target tuple list {index} is not distinct lexicographic")
    return found


def evenly_spaced_indices(count: int, r: int) -> list[int]:
    demand(r >= 2 and count >= r, "invalid evenly-spaced selection domain")
    result = [j * (count - 1) // (r - 1) for j in range(r)]
    demand(len(set(result)) == r and result[0] == 0 and result[-1] == count - 1, "evenly-spaced indices are not distinct endpoints")
    return result


def class_members(residue: int) -> list[int]:
    first = A + ((residue - A) % L)
    return list(range(first, B + 1, L))


def construct_panel(root: Path) -> dict[str, Any]:
    protected = verify_protected(root)
    candidates = load_candidates(root)
    pairs = canonical_pairs(root)
    prior_points, prior_classes, prior_meta = load_prior_t_points(root)
    all_tuples = enumerate_target_tuples(candidates, pairs)
    fresh: list[list[tuple[int, int, int, int]]] = []
    inventory: list[dict[str, Any]] = []
    for candidate, tuples in zip(candidates, all_tuples):
        available = [tuple4 for tuple4 in tuples if tuple_class_residue(tuple4) not in prior_classes]
        fresh.append(available)
        inventory.append({
            "mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "roles": candidate["roles"],
            "G": candidate["G"], "coverage_mask_hex": candidate["coverage_mask_hex"],
            "generating_tuple_count": len(tuples), "excluded_existing_class_tuple_count": len(tuples) - len(available),
            "available_fresh_tuple_count": len(available),
        })
    r = min(5, min(len(items) for items in fresh))
    panel: dict[str, Any] = {
        "schema": "a303656-weighted-fixed-p4-holdout-panel-v1",
        "source_commit": "SOURCE_COMMIT_M",
        "authority_manifest": V2_REL,
        "authority_manifest_sha256": sha256_file(root / V2_REL),
        "fixed_domain": {"P4": list(P4), "M4": M4, "L": L, "activation_cell": [A, B], "n_mod_40": N0 % 40, "pair_count": PAIR_COUNT},
        "selection_rule": "r=min(5,min fresh tuple multiplicity); indices floor(j*(N-1)/(r-1)), j=0..r-1",
        "r_determined_before_integer_evaluation": True,
        "integer_evaluation_performed": False,
        "r": r,
        "candidate_inventory": inventory,
        "prior_T_panel_exclusion": prior_meta,
        "protected_hashes": protected,
        "masks": [],
    }
    if r < 3:
        panel["status"] = "INSUFFICIENT FRESH CLASS MULTIPLICITY"
        panel["points"] = []
        return panel
    seen_points: set[int] = set()
    seen_classes: set[int] = set()
    all_points: list[dict[str, Any]] = []
    for candidate, available in zip(candidates, fresh):
        indices = evenly_spaced_indices(len(available), r)
        class_rows: list[dict[str, Any]] = []
        for within_mask_index, source_index in enumerate(indices):
            tuple4 = available[source_index]
            residue = tuple_class_residue(tuple4)
            demand(residue not in prior_classes and residue not in seen_classes, "selected class is old or duplicated")
            seen_classes.add(residue)
            members = class_members(residue)
            class_id = f"{candidate['mask_id']}-CLASS-{within_mask_index + 1:02d}"
            points: list[int] = []
            for point_index, n in enumerate(members):
                demand(n not in prior_points and n not in seen_points, "holdout integer overlaps a prior T panel or another class")
                demand(n % L == residue and n % 40 == N0 % 40 and A <= n <= B, "holdout point violates its CRT class/cell")
                seen_points.add(n)
                points.append(n)
                all_points.append({"point_ordinal": len(all_points), "mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "class_index": candidate["mask_index"] * r + within_mask_index, "class_id": class_id, "point_index": point_index, "n": n})
            class_rows.append({"class_index": candidate["mask_index"] * r + within_mask_index, "class_id": class_id, "fresh_tuple_source_index": source_index, "residue_tuple": list(tuple4), "crt_residue_mod_L": residue, "activation_cell_member_count": len(points), "points": points})
        panel["masks"].append({"mask_index": candidate["mask_index"], "mask_id": candidate["mask_id"], "roles": candidate["roles"], "selected_by": candidate["selected_by"], "G": candidate["G"], "coverage_mask_hex": candidate["coverage_mask_hex"], "available_fresh_tuple_count": len(available), "selected_fresh_tuple_count": r, "selection_indices": indices, "classes": class_rows})
    panel["status"] = "FROZEN PANEL READY FOR EVALUATION"
    panel["class_count"] = len(seen_classes)
    panel["point_count"] = len(all_points)
    panel["points"] = all_points
    panel["disjoint_from_prior_T_panels"] = True
    panel["all_selected_class_members_in_activation_cell_included"] = True
    return panel


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": format(value.numerator / value.denominator, ".18f")}


def median_fraction(values: list[int]) -> Fraction:
    ordered = sorted(values)
    middle = len(ordered) // 2
    return Fraction(ordered[middle]) if len(ordered) % 2 else Fraction(ordered[middle - 1] + ordered[middle], 2)


def exact_summary(values: list[int], ns: list[int], class_groups: list[list[int]], g_value: int) -> dict[str, Any]:
    demand(values and len(values) == len(ns), "summary population is empty or misaligned")
    minimum = min(values)
    point_mean = Fraction(sum(values), len(values))
    class_mean = sum((Fraction(sum(group), len(group)) for group in class_groups), Fraction()) / len(class_groups)
    return {
        "point_count": len(values), "G": g_value,
        "histogram": {str(key): count for key, count in sorted(Counter(values).items())},
        "minimum_T": minimum, "argmins": [n for n, value in zip(ns, values) if value == minimum],
        "maximum_T": max(values), "point_weighted_mean_T": fraction_record(point_mean),
        "class_equal_weighted_mean_T": fraction_record(class_mean), "median_T": fraction_record(median_fraction(values)),
        "threshold_counts": {f"T<={threshold}": sum(value <= threshold for value in values) for threshold in THRESHOLDS},
        "survival_ratio_T_over_407_minus_G": fraction_record(Fraction(sum(values), len(values) * (PAIR_COUNT - g_value))),
    }
