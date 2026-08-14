#!/usr/bin/env python3
"""Build, run, and package the exact fixed-P4 residue landscape.

This runner never evaluates the original representation-count function T(n).
It consumes only the two finite residue-landscape certificates and independently
derives compact CRT, local-neighborhood, and covered-pair comparison artifacts.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import os
import resource
import shutil
import subprocess
import sys
import time
from collections import Counter
from itertools import combinations, product
from pathlib import Path
from typing import Any, Iterable, Sequence


CELL_LOW = 183_968_950_234
CELL_HIGH = 246_731_069_451
N0 = 240_000_005_594
N0_TUPLE = (2, 41, 74, 504)
N0_COVERAGE = 216
PRIMES = (3, 7, 11, 23)
MODULI = (9, 49, 121, 529)
M4 = 28_227_969
L40 = 1_129_118_760
FULL_ROWS = M4
SLICE_ROWS = 49 * 121 * 529
COORD_NAMES = ("t3", "t7", "t11", "t23")

PROTECTED_FILES = (
    "README.md",
    "REPORT_zh.md",
    "output/formal_results_audit.json",
    "output/final_packaging_audit.json",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt",
    "output/final_results_manifest.json",
    "analysis/p2_core/activation_cell.json",
    "analysis/p2_core/n0_p2_core.json",
    "analysis/p2_core/metadata.json",
    "analysis/p2_core/verification_report.json",
    "analysis/k4_ap_pilot/metadata.json",
    "analysis/k4_ap_pilot/verification_report.json",
    "analysis/k4_survivor_incidence/metadata.json",
    "analysis/k4_survivor_incidence/verification_report.json",
    "analysis/k4_survivor_incidence/pair_order.csv",
)


def fail(message: str) -> None:
    raise RuntimeError(message)


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def canonical_json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(value))


def write_csv(path: Path, header: Sequence[str], rows: Iterable[Sequence[Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def generate_domain() -> list[tuple[int, int, int]]:
    powers3: list[int] = []
    value = 1
    while value <= CELL_HIGH:
        powers3.append(value)
        value *= 3
    powers5: list[int] = []
    value = 1
    while value <= CELL_HIGH:
        powers5.append(value)
        value *= 5
    at_low = [
        (c, d, a + b)
        for c, a in enumerate(powers3)
        for d, b in enumerate(powers5)
        if a + b <= CELL_LOW
    ]
    at_high = [
        (c, d, a + b)
        for c, a in enumerate(powers3)
        for d, b in enumerate(powers5)
        if a + b <= CELL_HIGH
    ]
    if at_low != at_high or len(at_low) != 407:
        fail("activation-cell domain is not the fixed 407-pair domain")
    duplicate = [(c, d) for c, d, shift in at_low if shift == 28]
    if duplicate != [(1, 2), (3, 0)]:
        fail("duplicate shift 28 pair identity mismatch")
    return at_low


def coverage_masks(domain: Sequence[tuple[int, int, int]]) -> list[list[int]]:
    all_masks: list[list[int]] = []
    for prime, modulus in zip(PRIMES, MODULI, strict=True):
        masks: list[int] = []
        for residue in range(modulus):
            mask = 0
            for index, (_, _, shift) in enumerate(domain):
                delta = residue - shift
                if delta % prime == 0 and delta % modulus != 0:
                    mask |= 1 << index
            masks.append(mask)
        all_masks.append(masks)
    return all_masks


def tuple_mask(masks: Sequence[Sequence[int]], residues: Sequence[int]) -> int:
    result = 0
    for coordinate, residue in enumerate(residues):
        result |= masks[coordinate][residue]
    return result


def pair_list(domain: Sequence[tuple[int, int, int]], mask: int) -> list[list[int]]:
    return [[c, d] for index, (c, d, _) in enumerate(domain) if (mask >> index) & 1]


def crt(residues: Sequence[int], moduli: Sequence[int]) -> tuple[int, int]:
    if len(residues) != len(moduli) or not residues:
        fail("CRT requires equally sized nonempty inputs")
    x = int(residues[0]) % int(moduli[0])
    modulus = int(moduli[0])
    for residue, next_modulus in zip(residues[1:], moduli[1:], strict=True):
        residue = int(residue) % int(next_modulus)
        gcd = math.gcd(modulus, next_modulus)
        if (residue - x) % gcd:
            fail("inconsistent CRT system")
        left = modulus // gcd
        right = next_modulus // gcd
        step = ((residue - x) // gcd * pow(left, -1, right)) % right
        x += modulus * step
        modulus *= right
        x %= modulus
    return x, modulus


def class_in_cell(residue: int, modulus: int) -> dict[str, Any]:
    residue %= modulus
    first = CELL_LOW + ((residue - CELL_LOW) % modulus)
    if first > CELL_HIGH:
        return {"count": 0, "first": None, "last": None, "nearest_to_n0": None}
    count = (CELL_HIGH - first) // modulus + 1
    last = first + (count - 1) * modulus
    approximate = (N0 - first) // modulus
    candidates = []
    for k in (approximate - 1, approximate, approximate + 1, approximate + 2):
        if 0 <= k < count:
            candidates.append(first + k * modulus)
    nearest = min(candidates, key=lambda n: (abs(n - N0), n))
    return {"count": count, "first": first, "last": last, "nearest_to_n0": nearest}


def rank_counts(histogram: dict[str, Any], target: int = N0_COVERAGE) -> dict[str, Any]:
    normalized = {int(key): int(value) for key, value in histogram.items()}
    above = sum(count for coverage, count in normalized.items() if coverage > target)
    equal = normalized.get(target, 0)
    below = sum(count for coverage, count in normalized.items() if coverage < target)
    total = above + equal + below
    return {
        "above": above,
        "equal": equal,
        "below": below,
        "rank_interval_descending": [above + 1, above + equal],
        "empirical_percentile": {
            "definition": "100 * (count_below + count_equal/2) / total (exact midrank percentile)",
            "numerator": 100 * (2 * below + equal),
            "denominator": 2 * total,
        },
    }


def stable_certificate(cert: dict[str, Any]) -> dict[str, Any]:
    return {key: value for key, value in cert.items() if key not in {"timings_seconds", "resources"}}


def compare_certificates(a: dict[str, Any], b: dict[str, Any]) -> None:
    required_equal = (
        "domain", "primes", "moduli", "M4", "n0", "subset_optima",
    )
    for key in required_equal:
        if a.get(key) != b.get(key):
            fail(f"enumerator certificates disagree at {key}")
    serialization_fields = (
        "fields", "integer_width_bits", "byte_order", "row_bytes",
        "padding_bytes", "tuple_order", "row_count", "struct_format",
    )
    for key in serialization_fields:
        if a["serialization"].get(key) != b["serialization"].get(key):
            fail(f"enumerator serialization semantics disagree at {key}")
    argmax_fields = (
        "fields", "integer_width_bits", "byte_order", "row_bytes",
        "padding_bytes", "includes_G", "struct_format",
    )
    for key in argmax_fields:
        if a["serialization"]["argmax"].get(key) != b["serialization"]["argmax"].get(key):
            fail(f"enumerator argmax serialization semantics disagree at {key}")
    for section in ("full", "t3eq2"):
        section_fields = (
            "tuple_count", "minimum", "maximum", "histogram", "argmax_count",
            "argmax_digest", "first_100_argmax", "stream_digest",
        )
        for key in section_fields:
            if a[section].get(key) != b[section].get(key):
                fail(f"enumerator certificates disagree at {section}.{key}")
        for key in ("above", "equal", "below", "rank_interval", "percentile"):
            if a[section]["n0_counts"].get(key) != b[section]["n0_counts"].get(key):
                fail(f"enumerator certificates disagree at {section}.n0_counts.{key}")
    full = a["full"]
    slice_data = a["t3eq2"]
    if int(full["tuple_count"]) != FULL_ROWS or sum(map(int, full["histogram"].values())) != FULL_ROWS:
        fail("full row or histogram total mismatch")
    if int(slice_data["tuple_count"]) != SLICE_ROWS or sum(map(int, slice_data["histogram"].values())) != SLICE_ROWS:
        fail("t3=2 row or histogram total mismatch")
    if tuple(map(int, a["n0"]["tuple"])) != N0_TUPLE or int(a["n0"]["coverage"]) != N0_COVERAGE:
        fail("n0 tuple or coverage mismatch")
    if len(a["subset_optima"]) != 15:
        fail("subset table does not contain all 15 nonempty subsets")


def changed_coordinates(residues: Sequence[int]) -> list[dict[str, int | str]]:
    return [
        {"coordinate": COORD_NAMES[index], "old": N0_TUPLE[index], "new": int(value)}
        for index, value in enumerate(residues)
        if int(value) != N0_TUPLE[index]
    ]


def local_category(
    domain: Sequence[tuple[int, int, int]],
    masks: Sequence[Sequence[int]],
    max_distance: int,
    exact: bool,
) -> dict[str, Any]:
    best = -1
    count = 0
    maximizers: list[tuple[int, int, int, int]] = []
    distances = [max_distance] if exact else list(range(max_distance + 1))
    for distance in distances:
        for coordinates in combinations(range(4), distance):
            choices = [range(MODULI[index]) for index in coordinates]
            for values in product(*choices):
                residues = list(N0_TUPLE)
                valid = True
                for coordinate, value in zip(coordinates, values, strict=True):
                    if value == N0_TUPLE[coordinate]:
                        valid = False
                        break
                    residues[coordinate] = value
                if not valid:
                    continue
                coverage = tuple_mask(masks, residues).bit_count()
                item = tuple(residues)
                if coverage > best:
                    best = coverage
                    count = 1
                    maximizers = [item]
                elif coverage == best:
                    count += 1
                    maximizers.append(item)
    maximizers.sort()
    n0_mask = tuple_mask(masks, N0_TUPLE)
    modifications: list[dict[str, Any]] = []
    for residues in maximizers[:100]:
        mask = tuple_mask(masks, residues)
        residue, modulus = crt(residues, MODULI)
        modifications.append({
            "tuple": list(residues),
            "coverage": mask.bit_count(),
            "gain_over_n0": mask.bit_count() - N0_COVERAGE,
            "changed_coordinates": changed_coordinates(residues),
            "crt_residue_mod_M4": residue,
            "crt_modulus": modulus,
            "newly_covered_pairs": pair_list(domain, mask & ~n0_mask),
            "previously_covered_pairs_lost": pair_list(domain, n0_mask & ~mask),
        })
    return {
        "maximum": best,
        "gain_over_n0": best - N0_COVERAGE,
        "argmax_count": count,
        "first_100_modifications": modifications,
    }


def constrained_local(
    cert: dict[str, Any],
    domain: Sequence[tuple[int, int, int]],
    masks: Sequence[Sequence[int]],
) -> dict[str, Any]:
    data = cert["t3eq2"]
    n0_mask = tuple_mask(masks, N0_TUPLE)
    modifications = []
    for row in data["first_100_argmax"]:
        residues = tuple(map(int, row))
        mask = tuple_mask(masks, residues)
        residue, modulus = crt(residues, MODULI)
        modifications.append({
            "tuple": list(residues),
            "coverage": mask.bit_count(),
            "gain_over_n0": mask.bit_count() - N0_COVERAGE,
            "changed_coordinates": changed_coordinates(residues),
            "crt_residue_mod_M4": residue,
            "crt_modulus": modulus,
            "newly_covered_pairs": pair_list(domain, mask & ~n0_mask),
            "previously_covered_pairs_lost": pair_list(domain, n0_mask & ~mask),
        })
    return {
        "maximum": int(data["maximum"]),
        "gain_over_n0": int(data["maximum"]) - N0_COVERAGE,
        "argmax_count": int(data["argmax_count"]),
        "first_100_modifications": modifications,
    }


def distribution(domain: Sequence[tuple[int, int, int]], mask: int, axis: int) -> dict[str, int]:
    counts: Counter[int] = Counter()
    for index, pair in enumerate(domain):
        if (mask >> index) & 1:
            counts[pair[axis]] += 1
    return {str(key): counts[key] for key in sorted(counts)}


def comparison_record(
    label: str,
    residues: Sequence[int],
    domain: Sequence[tuple[int, int, int]],
    masks: Sequence[Sequence[int]],
) -> dict[str, Any]:
    n0_mask = tuple_mask(masks, N0_TUPLE)
    target = tuple_mask(masks, residues)
    intersection = n0_mask & target
    new = target & ~n0_mask
    lost = n0_mask & ~target
    symmetric = new | lost
    by_set = {}
    for name, mask in (("intersection", intersection), ("newly_covered", new), ("lost", lost), ("symmetric_difference", symmetric)):
        by_set[name] = {
            "count": mask.bit_count(),
            "by_c": distribution(domain, mask, 0),
            "by_d": distribution(domain, mask, 1),
        }
    duplicate_rows = []
    for pair in ((1, 2), (3, 0)):
        index = next(i for i, item in enumerate(domain) if item[:2] == pair)
        duplicate_rows.append({
            "pair": list(pair), "shift": 28,
            "covered_by_n0": bool((n0_mask >> index) & 1),
            "covered_by_target": bool((target >> index) & 1),
        })
    return {
        "label": label,
        "tuple": list(map(int, residues)),
        "coverage": target.bit_count(),
        "intersection_count": intersection.bit_count(),
        "newly_covered_pairs": pair_list(domain, new),
        "pairs_lost_relative_to_n0": pair_list(domain, lost),
        "symmetric_difference_count": symmetric.bit_count(),
        "distributions": by_set,
        "duplicate_shift_28": {
            "pairs_retained_separately": duplicate_rows,
            "target_statuses_equal": duplicate_rows[0]["covered_by_target"] == duplicate_rows[1]["covered_by_target"],
        },
    }


def full_crt_rows(cert: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    maximum = int(cert["full"]["maximum"])
    for values in cert["full"]["first_100_argmax"]:
        residues = tuple(map(int, values))
        r, modulus = crt(residues, MODULI)
        if modulus != M4:
            fail("full CRT modulus mismatch")
        rows.append({"tuple": list(residues), "r_mod_M4": r, "coverage": maximum, **class_in_cell(r, modulus)})
    return rows


def constrained_crt_rows(cert: dict[str, Any]) -> list[dict[str, Any]]:
    rows = []
    maximum = int(cert["t3eq2"]["maximum"])
    for values in cert["t3eq2"]["first_100_argmax"]:
        residues = tuple(map(int, values))
        r4, modulus4 = crt(residues, MODULI)
        r, modulus = crt((r4, N0 % 40), (modulus4, 40))
        if modulus != L40 or r % 360 != N0 % 360:
            fail("constrained CRT modulus or mod-360 binding mismatch")
        rows.append({
            "tuple": list(residues), "r_mod_M4": r4, "coverage": maximum,
            "residue_mod_L": r, "L": modulus, **class_in_cell(r, modulus),
        })
    return rows


def subset_rows(cert: dict[str, Any]) -> list[dict[str, Any]]:
    output = []
    for row in cert["subset_optima"]:
        mask = int(row["subset_mask"])
        indices = [i for i in range(4) if mask & (1 << i)]
        primes = [PRIMES[i] for i in indices]
        moduli = [MODULI[i] for i in indices]
        residues = list(map(int, row["first_argmax"]))
        r, modulus = crt(residues, moduli)
        expected_modulus = math.prod(moduli)
        if modulus != expected_modulus or int(row["modulus_product"]) != expected_modulus:
            fail(f"subset modulus mismatch for mask {mask}")
        bits = modulus.bit_length()
        maximum = int(row["maximum"])
        output.append({
            "subset_mask": mask,
            "primes": primes,
            "modulus_product": modulus,
            "bit_length": bits,
            "decimal_digits": len(str(modulus)),
            "maximum_coverage": maximum,
            "argmax_count": int(row["argmax_count"]),
            "coverage_per_modulus_bit_descriptive_rational": f"{maximum}/{bits}",
            "first_maximizing_residues": residues,
            "first_maximizing_crt_residue": r,
            "activation_cell_point_count": class_in_cell(r, modulus)["count"],
        })
    return output


def make_artifacts(
    repo: Path,
    artifact_dir: Path,
    cert_a_path: Path,
    cert_b_path: Path,
    verification_path: Path,
    source_commit: str,
    results_commit: str,
    resources_data: dict[str, Any],
) -> None:
    cert_a = json.loads(cert_a_path.read_text(encoding="utf-8"))
    cert_b = json.loads(cert_b_path.read_text(encoding="utf-8"))
    compare_certificates(cert_a, cert_b)
    domain = generate_domain()
    masks = coverage_masks(domain)
    if tuple_mask(masks, N0_TUPLE).bit_count() != N0_COVERAGE:
        fail("independent integration n0 coverage mismatch")

    artifact_dir.mkdir(parents=True, exist_ok=True)
    write_csv(
        artifact_dir / "full_histogram.csv", ("coverage", "tuple_count"),
        ((int(key), int(value)) for key, value in sorted(cert_a["full"]["histogram"].items(), key=lambda item: int(item[0]))),
    )
    write_csv(
        artifact_dir / "t3eq2_histogram.csv", ("coverage", "tuple_count"),
        ((int(key), int(value)) for key, value in sorted(cert_a["t3eq2"]["histogram"].items(), key=lambda item: int(item[0]))),
    )
    write_json(artifact_dir / "maximizers.json", {
        "schema": "a303656-fixed-p4-maximizers-v1",
        "full": {key: cert_a["full"][key] for key in ("maximum", "argmax_count", "argmax_digest", "first_100_argmax")},
        "t3eq2": {key: cert_a["t3eq2"][key] for key in ("maximum", "argmax_count", "argmax_digest", "first_100_argmax")},
    })

    subset_data = subset_rows(cert_a)
    write_csv(
        artifact_dir / "subset_optima.csv",
        ("subset_mask", "primes", "modulus_product", "bit_length", "decimal_digits", "maximum_coverage", "argmax_count", "coverage_per_modulus_bit_descriptive_rational", "first_maximizing_residues", "first_maximizing_crt_residue", "activation_cell_point_count"),
        ((row["subset_mask"], ";".join(map(str, row["primes"])), row["modulus_product"], row["bit_length"], row["decimal_digits"], row["maximum_coverage"], row["argmax_count"], row["coverage_per_modulus_bit_descriptive_rational"], ";".join(map(str, row["first_maximizing_residues"])), row["first_maximizing_crt_residue"], row["activation_cell_point_count"]) for row in subset_data),
    )

    full_rank = rank_counts(cert_a["full"]["histogram"])
    slice_rank = rank_counts(cert_a["t3eq2"]["histogram"])
    write_json(artifact_dir / "n0_rank.json", {
        "schema": "a303656-fixed-p4-n0-rank-v1",
        "n0": N0,
        "tuple": list(N0_TUPLE),
        "coverage": N0_COVERAGE,
        "full": {
            **full_rank,
            "distance_from_maximum": int(cert_a["full"]["maximum"]) - N0_COVERAGE,
            "is_global_maximizer": int(cert_a["full"]["maximum"]) == N0_COVERAGE,
        },
        "t3eq2": {
            **slice_rank,
            "distance_from_maximum": int(cert_a["t3eq2"]["maximum"]) - N0_COVERAGE,
            "is_constrained_maximizer": int(cert_a["t3eq2"]["maximum"]) == N0_COVERAGE,
        },
    })

    local_one = local_category(domain, masks, 1, True)
    local_two = local_category(domain, masks, 2, False)
    local_constrained = constrained_local(cert_a, domain, masks)
    write_json(artifact_dir / "local_landscape.json", {
        "schema": "a303656-fixed-p4-local-landscape-v1",
        "n0_tuple": list(N0_TUPLE), "n0_coverage": N0_COVERAGE,
        "exactly_one_coordinate_changed": local_one,
        "at_most_two_coordinates_changed": local_two,
        "t3_fixed_2_other_coordinates_arbitrary": local_constrained,
    })

    write_json(artifact_dir / "crt_candidates.json", {
        "schema": "a303656-fixed-p4-crt-reconstruction-v1",
        "classification": "EXACT CRT RECONSTRUCTION ONLY; T(n) WAS NOT EVALUATED",
        "activation_cell": [CELL_LOW, CELL_HIGH], "n0": N0, "M4": M4, "L": L40,
        "first_100_global_maximizers": full_crt_rows(cert_a),
        "first_100_t3eq2_maximizers_with_n_mod_40_equal_n0": constrained_crt_rows(cert_a),
    })

    comparison_targets = (
        ("lexicographically_first_global_maximizer", cert_a["full"]["first_100_argmax"][0]),
        ("lexicographically_first_t3eq2_maximizer", cert_a["t3eq2"]["first_100_argmax"][0]),
        ("lexicographically_first_one_coordinate_maximizer", local_one["first_100_modifications"][0]["tuple"]),
        ("lexicographically_first_at_most_two_coordinate_maximizer", local_two["first_100_modifications"][0]["tuple"]),
    )
    write_json(artifact_dir / "coverage_comparison.json", {
        "schema": "a303656-fixed-p4-coverage-comparison-v1",
        "warning": "Newly covered pairs are guaranteed only in the corresponding CRT class; no permanent obstruction is claimed outside it.",
        "n0_tuple": list(N0_TUPLE), "n0_coverage": N0_COVERAGE,
        "comparisons": [comparison_record(label, residues, domain, masks) for label, residues in comparison_targets],
    })

    verification = json.loads(verification_path.read_text(encoding="utf-8"))
    write_json(artifact_dir / "verification_report.json", verification)
    protected_hashes = {name: sha256_file(repo / name) for name in PROTECTED_FILES}
    artifact_hashes = {
        path.name: sha256_file(path)
        for path in sorted(artifact_dir.iterdir())
        if path.is_file() and path.name not in {"metadata.json", "verification_report.json"}
    }
    metadata = {
        "schema": "a303656-fixed-p4-residue-landscape-metadata-v1",
        "task": "EXACT FIXED-P4 RESIDUE LANDSCAPE",
        "classification": "EXACT FINITE COMBINATORIAL OPTIMIZATION; GLOBAL A303656 PROBLEM UNRESOLVED",
        "source_commit": source_commit,
        "source_parent_commit": "b76d097081ac2b5704bbd234e3eaf25ba9564502",
        "results_commit": results_commit,
        "domain": {"activation_cell": [CELL_LOW, CELL_HIGH], "pair_count": 407, "duplicate_shift_28_pairs": [[1, 2], [3, 0]]},
        "P4": list(PRIMES), "square_moduli": list(MODULI), "M4": M4, "L": L40,
        "serialization": cert_a["serialization"],
        "full_stream_digest": cert_a["full"]["stream_digest"],
        "t3eq2_stream_digest": cert_a["t3eq2"]["stream_digest"],
        "enumerator_stable_certificate_sha256": {
            "A": hashlib.sha256(canonical_json_bytes(stable_certificate(cert_a))).hexdigest(),
            "B": hashlib.sha256(canonical_json_bytes(stable_certificate(cert_b))).hexdigest(),
        },
        "artifact_sha256_excluding_metadata_and_verification_report": artifact_hashes,
        "protected_input_and_baseline_sha256": protected_hashes,
        "resources": resources_data,
        "raw_archive": "TO_BE_FILLED_AFTER_EXTERNAL_ARCHIVE_CREATION",
        "scope_guards": {
            "T_evaluations": 0, "two_square_executables_run": 0,
            "arithmetic_progressions_scanned": 0, "new_primes": 0,
            "CRT_candidate_searches": 0, "full_tuple_stream_committed": False,
        },
        "mathematical_status": "UNRESOLVED",
        "conclusion": "VALIDATED EXACT FIXED-P4 RESIDUE LANDSCAPE",
    }
    write_json(artifact_dir / "metadata.json", metadata)


def parse_time_v(path: Path) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if ": " not in line:
            continue
        key, value = line.strip().split(": ", 1)
        if key == "Elapsed (wall clock) time (h:mm:ss or m:ss)":
            parts = value.split(":")
            seconds = 0.0
            for part in parts:
                seconds = seconds * 60 + float(part)
            result["wall_seconds"] = seconds
        elif key == "Maximum resident set size (kbytes)":
            result["maximum_rss_kib"] = int(value)
        elif key == "Exit status":
            result["exit_status"] = int(value)
    return result


def run_logged(name: str, command: Sequence[str], cwd: Path, raw_dir: Path, env: dict[str, str] | None = None) -> dict[str, Any]:
    stdout_path = raw_dir / f"{name}.stdout.log"
    stderr_path = raw_dir / f"{name}.stderr.log"
    time_path = raw_dir / f"{name}.time.txt"
    command_path = raw_dir / f"{name}.command.json"
    wrapped = ["/usr/bin/time", "-v", "-o", str(time_path), *command]
    start = time.monotonic()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        completed = subprocess.run(wrapped, cwd=cwd, stdout=stdout, stderr=stderr, env=env, check=False)
    elapsed = time.monotonic() - start
    record = {
        "name": name, "command": list(command), "cwd": str(cwd),
        "return_code": completed.returncode, "runner_wall_seconds": elapsed,
        "stdout": stdout_path.name, "stderr": stderr_path.name, "time_log": time_path.name,
    }
    write_json(command_path, record)
    if completed.returncode != 0:
        tail = stderr_path.read_text(encoding="utf-8", errors="replace").splitlines()[-20:]
        fail(f"command {name} failed with RC {completed.returncode}: {' | '.join(tail)}")
    record.update(parse_time_v(time_path))
    return record


def full_run(args: argparse.Namespace) -> None:
    repo = args.repo.resolve()
    raw = args.raw_dir.resolve()
    artifacts = args.artifact_dir.resolve()
    raw.mkdir(parents=True, exist_ok=True)
    bin_dir = raw / "bin"
    bin_dir.mkdir(exist_ok=True)
    tools = repo / "analysis/p4_residue_landscape/tools"
    tests = repo / "analysis/p4_residue_landscape/tests/test_negative.py"
    commands: dict[str, Any] = {}
    python_env = os.environ.copy()
    python_env["PYTHONDONTWRITEBYTECODE"] = "1"

    compile_flags = ["-std=c++20", "-O3", "-DNDEBUG", "-Wall", "-Wextra", "-Wpedantic", "-Werror"]
    commands["build_a"] = run_logged("build_a", ["g++", *compile_flags, str(tools / "enumerator_a.cpp"), "-o", str(bin_dir / "enumerator_a")], repo, raw)
    commands["build_b"] = run_logged("build_b", ["g++", *compile_flags, str(tools / "enumerator_b.cpp"), "-o", str(bin_dir / "enumerator_b")], repo, raw)
    commands["negative_tests"] = run_logged(
        "negative_tests", [sys.executable, str(tests)], repo, raw, env=python_env
    )

    cert_a = raw / "certificate_a.json"
    cert_b = raw / "certificate_b.json"
    commands["enumerator_a"] = run_logged("enumerator_a", [str(bin_dir / "enumerator_a"), str(cert_a)], repo, raw)
    commands["enumerator_b"] = run_logged("enumerator_b", [str(bin_dir / "enumerator_b"), str(cert_b)], repo, raw)

    verification = raw / "verification_report.json"
    verifier_command = [
        sys.executable, str(tools / "verifier.py"),
        "--certificate-a", str(cert_a), "--certificate-b", str(cert_b),
        "--output", str(verification),
    ]
    commands["verifier"] = run_logged(
        "verifier", verifier_command, repo, raw, env=python_env
    )
    write_json(raw / "command_manifest.json", {"commands": commands})

    cert_a_data = json.loads(cert_a.read_text(encoding="utf-8"))
    cert_b_data = json.loads(cert_b.read_text(encoding="utf-8"))
    resources_data = {
        "commands": commands,
        "enumerator_internal": {
            "A": {key: cert_a_data[key] for key in ("timings_seconds", "resources") if key in cert_a_data},
            "B": {key: cert_b_data[key] for key in ("timings_seconds", "resources") if key in cert_b_data},
        },
    }
    make_artifacts(repo, artifacts, cert_a, cert_b, verification, args.source_commit, args.results_commit, resources_data)

    committed_report = artifacts / "verification_report.json"
    artifact_verifier_command = [
        sys.executable, str(tools / "verifier.py"),
        "--certificate-a", str(cert_a), "--certificate-b", str(cert_b),
        "--artifact-dir", str(artifacts), "--output", str(committed_report),
    ]
    commands["artifact_verifier"] = run_logged(
        "artifact_verifier", artifact_verifier_command, repo, raw, env=python_env
    )
    metadata_path = artifacts / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
    metadata["verification_report_sha256"] = sha256_file(committed_report)
    write_json(metadata_path, metadata)

    selfcheck_report = raw / "artifact_selfcheck_report.json"
    selfcheck_command = [
        sys.executable, str(tools / "verifier.py"),
        "--certificate-a", str(cert_a), "--certificate-b", str(cert_b),
        "--artifact-dir", str(artifacts), "--output", str(selfcheck_report),
    ]
    commands["artifact_selfcheck"] = run_logged(
        "artifact_selfcheck", selfcheck_command, repo, raw, env=python_env
    )
    if json.loads(selfcheck_report.read_text(encoding="utf-8")) != json.loads(
        committed_report.read_text(encoding="utf-8")
    ):
        fail("artifact self-check report does not reproduce committed verification report")
    resources_data["commands"] = commands
    metadata["resources"] = resources_data
    write_json(metadata_path, metadata)
    write_json(raw / "command_manifest.json", {"commands": commands})


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", type=Path, default=Path.cwd())
    parser.add_argument("--raw-dir", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--results-commit", default="RESULT_COMMIT_CONTAINING_THIS_FILE")
    args = parser.parse_args()
    if math.prod(MODULI) != M4 or 40 * M4 != L40:
        fail("fixed modulus constants do not reproduce")
    full_run(args)
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # fail closed with a concise, greppable status
        print(f"FIXED-P4 RESIDUE LANDSCAPE RUN FAILED: {exc}", file=sys.stderr)
        raise SystemExit(2)
