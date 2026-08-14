#!/usr/bin/env python3
"""Independent verifier for the K4 survivor-incidence audit.

This module does not import the runner or either backend wrapper.  It rebuilds
the fixed panel and canonical exponent domain, parses the packed format from
first principles, recomputes every mathematical summary, and checks the fresh
factorization-free direct-oracle winner lists and witnesses.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import statistics
import struct
import subprocess
import sys
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any


N0 = 240000005594
M4 = 28227969
P4 = (3, 7, 11, 23)
H_VALUES = (-720, -360, 0, 360, 720)
K_MIN = -128
K_MAX = 128
ACTIVE = 407
MASK_WIDTH = 51
CELL = (183968950234, 246731069451)
BASELINE = "406677c3b095d2125a4a439c76b3a8d6788cb1da"
RESULT_SENTINEL = "RESULT_COMMIT_CONTAINING_THIS_FILE"
DIRECT_K = (-128, -96, -64, -32, -1, 0, 1, 32, 64, 96, 128)
FREQUENCY_THRESHOLDS = (10, 25, 50, 75)
FIVE_THRESHOLDS = (10, 20, 30, 40)
FILE_HEADER = struct.Struct("<8sIIIIII32s")
POINT_HEADER = struct.Struct("<QqqII")
MAGIC = b"K4SMASK1"
ARTIFACT_NAMES = {
    "metadata.json",
    "pair_order.csv",
    "backend_a_masks.bin",
    "backend_b_masks.bin",
    "mask_manifest.json",
    "class_pair_frequencies.csv",
    "pairwise_common_uncovered.json",
    "five_way_common_uncovered.json",
    "hard_survivor_pairs.json",
    "cross_class_pair_profiles.csv",
}
EXPECTED_NEGATIVE_TESTS = {
    "changed_pair_ordering",
    "changed_pair_order_hash",
    "one_flipped_winner_bit",
    "mask_row_deletion",
    "duplicated_row",
    "extra_bytes",
    "truncated_mask",
    "incorrect_popcount_T",
    "class_relabeling",
    "point_reordering",
    "persistent_covered_pair_marked_winner",
    "swapped_backend_identity",
    "source_commit_mismatch",
    "baseline_hash_mismatch",
}
PRIOR_HASHES = {
    "analysis/k4_ap_pilot/backend_a_counts.csv": "dad853ae1b385ef44ef67b442d5b3b82c78614a4fc99c77530ba6903ede49e23",
    "analysis/k4_ap_pilot/backend_b_counts.csv": "dad853ae1b385ef44ef67b442d5b3b82c78614a4fc99c77530ba6903ede49e23",
    "analysis/k4_ap_pilot/class_summaries.json": "613c0583b473cb9416c3f066d1e7d530816d2ec4015fd6f84bed0880d1670da1",
    "analysis/k4_ap_pilot/direct_verification.json": "3ec8be67747e64d5046dc9c3591c8885865b897f3d02c18be8fd5b01ee201794",
    "analysis/k4_ap_pilot/matched_k_comparison.csv": "402680ce1d0f8e7cac28ad08ee6a00f7ba6985e0a0b7eeeb668db471a8bfc367",
    "analysis/k4_ap_pilot/metadata.json": "edac79f1bb9932a05a145b6326dd143a44027fbf1e7b4e9ace5e060fc95d4b8a",
    "analysis/k4_ap_pilot/persistent_core_by_class.json": "436ef8b4eb740dc2a53f61903752fe269628bbbab3eb430adf23029d0a3073a0",
    "analysis/k4_ap_pilot/pointwise_comparison.csv": "4cf6350310b28b3fe7c0b8efc7f289becc58579bd4b594453920a889ce36b2a4",
    "analysis/k4_ap_pilot/verification_report.json": "7f1c999893d890dcaca37aee6c6d300fc3b41bd8c9ee779c1d4cb28e1a992d1a",
    "docs/k4_ap_enrichment_pilot.md": "0a1e89ef0c946bc47dbee211a4d84c2e99c95247629caf934ebd9225c64e7db2",
}


class Rejection(RuntimeError):
    pass


def demand(condition: bool, message: str) -> None:
    if not condition:
        raise Rejection(message)


def digest_file(path: Path) -> str:
    state = hashlib.sha256()
    with path.open("rb") as handle:
        while True:
            block = handle.read(1 << 20)
            if not block:
                break
            state.update(block)
    return state.hexdigest()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def json_object(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise Rejection(f"cannot read JSON {path}: {exc}") from exc
    demand(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def canonical_decimal(text: str, label: str, *, nonnegative: bool = False) -> int:
    demand(bool(text) and text == text.strip() and not text.startswith("+"), f"malformed {label}")
    body = text[1:] if text.startswith("-") else text
    demand(body.isascii() and body.isdigit(), f"malformed {label}")
    demand(len(body) == 1 or body[0] != "0", f"leading zero in {label}")
    value = int(text)
    demand(not nonnegative or value >= 0, f"negative {label}")
    return value


def git(root: Path, *args: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(["git", *args], cwd=root, check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if check and result.returncode:
        raise Rejection(f"git {' '.join(args)} failed: {result.stderr.decode('utf-8', 'replace')}")
    return result


def git_ascii(root: Path, *args: str) -> str:
    return git(root, *args).stdout.decode("ascii", "strict").strip()


def exponent_powers(base: int, ceiling: int) -> list[tuple[int, int]]:
    answer: list[tuple[int, int]] = []
    exponent = 0
    value = 1
    while value <= ceiling:
        answer.append((exponent, value))
        if value > ceiling // base:
            break
        value *= base
        exponent += 1
    return answer


def expected_pair_rows() -> list[dict[str, Any]]:
    panel_low = N0 - 720 + K_MIN * M4
    triples: list[tuple[int, int, int]] = []
    for c, value3 in exponent_powers(3, panel_low):
        for d, value5 in exponent_powers(5, panel_low):
            if value3 + value5 <= panel_low:
                triples.append((c, d, value3 + value5))
    demand(len(triples) == ACTIVE and triples == sorted(triples), "independent pair-domain regeneration failed")
    multiplicity = Counter(shift for _, _, shift in triples)
    demand({shift: count for shift, count in multiplicity.items() if count > 1} == {28: 2},
           "independent duplicate-shift regeneration failed")
    return [
        {
            "pair_index": index,
            "c": c,
            "d": d,
            "shift": shift,
            "duplicate_shift_group": f"shift_{shift}" if multiplicity[shift] > 1 else "",
        }
        for index, (c, d, shift) in enumerate(triples)
    ]


def expected_panel() -> list[dict[str, int]]:
    rows = [
        {"h": h, "k": k, "n": N0 + h + k * M4, "active_pairs": ACTIVE}
        for h in H_VALUES
        for k in range(K_MIN, K_MAX + 1)
    ]
    demand(len(rows) == 1285 and len({row["n"] for row in rows}) == 1285, "independent panel regeneration failed")
    demand(all(CELL[0] <= row["n"] <= CELL[1] for row in rows), "panel outside activation cell")
    domain = [(row["c"], row["d"], row["shift"]) for row in expected_pair_rows()]
    for n in (rows[0]["n"], rows[-1]["n"]):
        active = [
            (c, d, p3 + p5)
            for c, p3 in exponent_powers(3, n)
            for d, p5 in exponent_powers(5, n)
            if p3 + p5 <= n
        ]
        demand(active == domain, "panel active domain is not constant")
    return rows


def serialized_panel(rows: list[dict[str, int]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=["h", "k", "n", "active_pairs"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return buffer.getvalue().encode()


def read_pair_csv(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        parser = csv.DictReader(handle)
        demand(parser.fieldnames == ["pair_index", "c", "d", "shift", "duplicate_shift_group"], "pair-order CSV header mismatch")
        source = list(parser)
    rows: list[dict[str, Any]] = []
    for raw in source:
        rows.append(
            {
                "pair_index": canonical_decimal(raw["pair_index"], "pair_index", nonnegative=True),
                "c": canonical_decimal(raw["c"], "c", nonnegative=True),
                "d": canonical_decimal(raw["d"], "d", nonnegative=True),
                "shift": canonical_decimal(raw["shift"], "shift", nonnegative=True),
                "duplicate_shift_group": raw["duplicate_shift_group"],
            }
        )
    demand(rows == expected_pair_rows(), "pair-order CSV is not the canonical independently regenerated table")
    return rows


def mask_bit(mask: bytes, index: int) -> bool:
    return bool(mask[index >> 3] & (1 << (index & 7)))


def parse_masks(path: Path, panel: list[dict[str, int]], pair_hash: str) -> list[dict[str, Any]]:
    blob = path.read_bytes()
    row_width = POINT_HEADER.size + MASK_WIDTH
    exact_size = FILE_HEADER.size + len(panel) * row_width
    demand(len(blob) == exact_size, f"{path.name}: wrong size, truncation or extra bytes")
    magic, version, header_bytes, row_count, pair_count, mask_bytes, declared_row_width, embedded_hash = FILE_HEADER.unpack_from(blob)
    demand((magic, version, header_bytes, row_count, pair_count, mask_bytes, declared_row_width) ==
           (MAGIC, 1, FILE_HEADER.size, 1285, ACTIVE, MASK_WIDTH, row_width), f"{path.name}: invalid header")
    demand(embedded_hash.hex() == pair_hash, f"{path.name}: wrong pair-order hash")
    result: list[dict[str, Any]] = []
    cursor = FILE_HEADER.size
    for wanted in panel:
        n, h, k, active, t_value = POINT_HEADER.unpack_from(blob, cursor)
        cursor += POINT_HEADER.size
        packed = blob[cursor : cursor + MASK_WIDTH]
        cursor += MASK_WIDTH
        demand((n, h, k, active) == (wanted["n"], wanted["h"], wanted["k"], ACTIVE),
               f"{path.name}: point order/identity/class mismatch")
        demand((packed[-1] & 0x80) == 0, f"{path.name}: nonzero unused mask bit")
        demand(sum(byte.bit_count() for byte in packed) == t_value, f"{path.name}: popcount/T mismatch")
        result.append({**wanted, "T": t_value, "mask": packed})
    demand(cursor == len(blob), f"{path.name}: parser did not consume exact bytes")
    return result


def protected_record(root: Path) -> dict[str, Any]:
    for relative, expected in PRIOR_HASHES.items():
        demand((root / relative).is_file() and digest_file(root / relative) == expected,
               f"protected prior K4 hash mismatch: {relative}")
    p2 = json_object(root / "analysis/p2_core/metadata.json")
    baseline_manifest = p2.get("fixed_input_audit", {}).get("fixed_input_tree_sha256")
    demand(isinstance(baseline_manifest, dict) and len(baseline_manifest) == 86, "baseline hash manifest missing")
    for relative, expected in baseline_manifest.items():
        demand((root / relative).is_file() and digest_file(root / relative) == expected,
               f"protected baseline hash mismatch: {relative}")
    baseline_text = "".join(f"{baseline_manifest[path]}  {path}\n" for path in sorted(baseline_manifest))
    k4_text = "".join(f"{PRIOR_HASHES[path]}  {path}\n" for path in sorted(PRIOR_HASHES))
    return {
        "baseline_manifest_file_count": 86,
        "baseline_manifest_sha256": digest_bytes(baseline_text.encode()),
        "prior_k4_file_count": len(PRIOR_HASHES),
        "prior_k4_manifest_sha256": digest_bytes(k4_text.encode()),
        "all_byte_identical": True,
        "mismatch_count": 0,
    }


def verify_commit_and_sources(
    root: Path,
    artifact: Path,
    metadata: dict[str, Any],
    requested_source: str,
    requested_result: str,
) -> dict[str, Any]:
    source = metadata.get("source_commit")
    demand(source == requested_source and isinstance(source, str), "source-commit mismatch")
    demand(git_ascii(root, "rev-parse", f"{source}^{{commit}}") == source, "source commit does not resolve exactly")
    parent = git_ascii(root, "rev-parse", f"{source}^")
    demand(parent == BASELINE and metadata.get("source_parent_commit") == BASELINE, "source parent/baseline mismatch")
    demand(metadata.get("baseline_commit") == BASELINE, "metadata baseline mismatch")
    result = requested_result
    if result != RESULT_SENTINEL:
        demand(len(result) == 40 and git_ascii(root, "rev-parse", f"{result}^{{commit}}") == result, "results commit malformed")
        demand(git_ascii(root, "rev-parse", f"{result}^") == source, "results commit parent is not source commit")
        demand(git(root, "merge-base", "--is-ancestor", source, result, check=False).returncode == 0,
               "source commit is not ancestor of results commit")
        demand(metadata.get("results_commit") == RESULT_SENTINEL, "metadata results sentinel changed")
        for name in sorted(ARTIFACT_NAMES):
            committed = git(root, "show", f"{result}:analysis/k4_survivor_incidence/{name}").stdout
            demand(committed == (artifact / name).read_bytes(), f"artifact differs from results commit: {name}")
    else:
        demand(metadata.get("results_commit") == RESULT_SENTINEL, "uncommitted replay results sentinel mismatch")
    tool_hashes = metadata.get("tool_source_sha256")
    demand(isinstance(tool_hashes, dict) and bool(tool_hashes), "tool-source hash manifest missing")
    for relative, expected in tool_hashes.items():
        path = root / relative
        demand(path.is_file() and digest_file(path) == expected, f"tool source hash mismatch: {relative}")
        demand(digest_bytes(git(root, "show", f"{source}:{relative}").stdout) == expected,
               f"tool source not bound to source commit: {relative}")
    # A results commit cannot contain its own SHA.  Keep the serialized report
    # canonical in both source-replay and commit-verification modes; the actual
    # result argument has already been resolved, parent-checked, and compared
    # byte-for-byte above when it is supplied.
    return {
        "baseline_commit": BASELINE,
        "source_commit": source,
        "results_commit": RESULT_SENTINEL,
        "source_is_direct_parent_of_results": True,
        "resolution": "RESULT_COMMIT_SELF_REFERENCE_SENTINEL",
    }


def implementation_id(command: list[str]) -> str:
    result = subprocess.run([*command, "--implementation-id"], check=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    demand(result.returncode == 0 and result.stderr == b"", f"identity query failed: {command}")
    return result.stdout.decode("ascii", "strict").strip()


def verify_identities(
    root: Path,
    metadata: dict[str, Any],
    manifest: dict[str, Any],
    args: argparse.Namespace,
) -> None:
    identities = metadata.get("backend_identities")
    demand(isinstance(identities, dict) and identities == manifest.get("backends"), "backend identity manifests differ")
    expected = {
        "backend_a": ("k4_survivor_backend_a_mask_wrapper_v1", "k4_ap_backend_a_trial_division_v1", args.backend_a_core),
        "backend_b": ("k4_survivor_backend_b_mask_wrapper_v1", "k4_ap_backend_b_cpp17_mr7_brent_rho_v1", args.backend_b_core),
    }
    for label, (wrapper_id, core_id, binary) in expected.items():
        record = identities.get(label)
        demand(isinstance(record, dict), f"identity slot missing: {label}")
        demand(record.get("wrapper_implementation_id") == wrapper_id and record.get("core_implementation_id") == core_id,
               f"backend identity relabel/swap: {label}")
        wrapper = root / record["wrapper_source"]
        demand(implementation_id([sys.executable, str(wrapper)]) == wrapper_id, f"wrapper identity mismatch: {label}")
        demand(implementation_id([str(binary)]) == core_id, f"core identity mismatch/swapped slot: {label}")
        demand(digest_file(binary) == record.get("core_binary_sha256"), f"core binary hash mismatch: {label}")
    direct = identities.get("direct_oracle")
    demand(isinstance(direct, dict) and direct.get("implementation_id") == "k4_ap_direct_oracle_v1", "direct identity mismatch")
    demand(implementation_id([str(args.direct_oracle)]) == "k4_ap_direct_oracle_v1", "direct binary identity mismatch")
    demand(digest_file(args.direct_oracle) == direct.get("binary_sha256"), "direct binary hash mismatch")


def read_prior_t(root: Path, panel: list[dict[str, int]]) -> list[int]:
    with (root / "analysis/k4_ap_pilot/backend_a_counts.csv").open(newline="", encoding="utf-8") as handle:
        parser = csv.DictReader(handle)
        demand(parser.fieldnames == ["h", "k", "n", "T", "active_pairs"], "prior T header mismatch")
        source = list(parser)
    demand(len(source) == len(panel), "prior T row count mismatch")
    result: list[int] = []
    for raw, point in zip(source, panel):
        identity = (
            canonical_decimal(raw["h"], "prior h"),
            canonical_decimal(raw["k"], "prior k"),
            canonical_decimal(raw["n"], "prior n", nonnegative=True),
            canonical_decimal(raw["active_pairs"], "prior active", nonnegative=True),
        )
        demand(identity == (point["h"], point["k"], point["n"], ACTIVE), "prior panel field mismatch")
        result.append(canonical_decimal(raw["T"], "prior T", nonnegative=True))
    return result


def reconstruct_covered(root: Path, pairs: list[dict[str, Any]], rows: list[dict[str, Any]]) -> dict[int, set[int]]:
    result: dict[int, set[int]] = {}
    for h in H_VALUES:
        base = N0 + h
        result[h] = {
            pair["pair_index"]
            for pair in pairs
            if any((base - pair["shift"]) % p == 0 and (base - pair["shift"]) % (p * p) != 0 for p in P4)
        }
        for row in rows:
            if row["h"] == h:
                demand(not any(mask_bit(row["mask"], index) for index in result[h]),
                       f"persistent-covered pair marked winner at h={h}, k={row['k']}")
    demand({h: len(result[h]) for h in H_VALUES} == {-720: 214, -360: 182, 0: 216, 360: 198, 720: 209},
           "persistent covered cardinalities differ")
    committed = json_object(root / "analysis/k4_ap_pilot/persistent_core_by_class.json")
    for item, h in zip(committed["classes"], H_VALUES):
        expected_names = [f"{pairs[index]['c']}:{pairs[index]['d']}" for index in sorted(result[h])]
        demand(item["h"] == h and item["persistent_covered_active_pairs"] == expected_names,
               f"persistent covered set differs from committed artifact for h={h}")
    return result


def consecutive_run(values: list[int]) -> int:
    best = current = 0
    previous: int | None = None
    for value in values:
        current = current + 1 if previous is not None and value == previous + 1 else 1
        best = max(best, current)
        previous = value
    return best


def survival_profiles(rows: list[dict[str, Any]], covered: dict[int, set[int]]) -> dict[int, dict[int, dict[str, Any]]]:
    profiles: dict[int, dict[int, dict[str, Any]]] = {}
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        profiles[h] = {}
        for index in range(ACTIVE):
            winning = [row["k"] for row in class_rows if mask_bit(row["mask"], index)]
            demand(index not in covered[h] or not winning, "covered pair survived")
            profiles[h][index] = {
                "count": len(winning),
                "winning_k": winning,
                "first": winning[0] if winning else None,
                "last": winning[-1] if winning else None,
                "longest": consecutive_run(winning),
            }
    return profiles


def fraction_decimal(value: Fraction, digits: int = 30) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def fraction_record(value: Fraction) -> dict[str, Any]:
    return {"numerator": value.numerator, "denominator": value.denominator, "decimal": fraction_decimal(value)}


def exact_median(values: list[int]) -> Fraction:
    ordered = sorted(values)
    middle = len(ordered) // 2
    return Fraction(ordered[middle]) if len(ordered) % 2 else Fraction(ordered[middle - 1] + ordered[middle], 2)


def quantile(values: list[int], numerator: int, denominator: int = 100) -> int:
    rank = max(1, (numerator * len(values) + denominator - 1) // denominator)
    return sorted(values)[rank - 1]


def population(values: list[int]) -> dict[str, Any]:
    demand(bool(values), "empty population")
    mean = Fraction(sum(values), len(values))
    variance = sum((Fraction(value) - mean) ** 2 for value in values) / len(values)
    with localcontext() as context:
        context.prec = 30
        standard_deviation = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    return {
        "point_count": len(values),
        "mean": fraction_record(mean),
        "median": fraction_record(exact_median(values)),
        "population_variance": fraction_record(variance),
        "population_standard_deviation_decimal": format(standard_deviation, "f"),
        "quantiles_inverse_ecdf": {
            "q00": quantile(values, 0), "q10": quantile(values, 10), "q25": quantile(values, 25),
            "q50": quantile(values, 50), "q75": quantile(values, 75), "q90": quantile(values, 90),
            "q100": quantile(values, 100),
        },
        "minimum": min(values),
        "fixed_threshold_counts_le": {str(threshold): sum(value <= threshold for value in values) for threshold in FIVE_THRESHOLDS},
    }


def paired(target: list[int], control: list[int]) -> dict[str, Any]:
    differences = [a - b for a, b in zip(target, control)]
    return {
        "point_count": len(target),
        "target": population(target),
        "control": population(control),
        "target_minus_control_mean": fraction_record(Fraction(sum(differences), len(differences))),
        "target_minus_control_median": fraction_record(exact_median(differences)),
        "negative_count": sum(value < 0 for value in differences),
        "zero_count": sum(value == 0 for value in differences),
        "positive_count": sum(value > 0 for value in differences),
        "target_unique_minimum_count": sum(value < 0 for value in differences),
        "target_tied_minimum_count": sum(value == 0 for value in differences),
    }


def restricted(row: dict[str, Any], indices: set[int]) -> int:
    return sum(mask_bit(row["mask"], index) for index in indices)


def expected_pairwise(rows: list[dict[str, Any]], covered: dict[int, set[int]]) -> dict[str, Any]:
    lookup = {(row["h"], row["k"]): row for row in rows}
    comparisons: list[dict[str, Any]] = []
    for h in (-720, -360, 360, 720):
        domain = set(range(ACTIVE)) - (covered[0] | covered[h])
        per_k = []
        for k in range(K_MIN, K_MAX + 1):
            target = restricted(lookup[(0, k)], domain)
            control = restricted(lookup[(h, k)], domain)
            per_k.append({"k": k, "target_restricted_T": target, "control_restricted_T": control,
                          "target_minus_control": target - control})
        target_values = [item["target_restricted_T"] for item in per_k]
        control_values = [item["control_restricted_T"] for item in per_k]
        keep = [index for index, item in enumerate(per_k) if item["k"] != 0]
        comparisons.append(
            {
                "control_h": h,
                "common_uncovered_pair_count": len(domain),
                "common_uncovered_pair_indices": sorted(domain),
                "including_anchor_k0": paired(target_values, control_values),
                "leave_anchor_out": paired([target_values[i] for i in keep], [control_values[i] for i in keep]),
                "per_k": per_k,
            }
        )
    return {
        "schema": "a303656-k4-pairwise-common-uncovered-v1",
        "classification": "EXACT FINITE COMPUTATION ON THE FIXED 1285-POINT PANEL",
        "definition": "I_h = E \\ (C_0 union C_h)",
        "comparisons": comparisons,
    }


def expected_five(rows: list[dict[str, Any]], covered: dict[int, set[int]]) -> dict[str, Any]:
    domain = set(range(ACTIVE)) - set().union(*(covered[h] for h in H_VALUES))
    classes = []
    for h in H_VALUES:
        per_k = [{"k": row["k"], "restricted_T": restricted(row, domain)} for row in rows if row["h"] == h]
        values = [item["restricted_T"] for item in per_k]
        summary = population(values)
        summary["argmin_k"] = [item["k"] for item in per_k if item["restricted_T"] == min(values)]
        record: dict[str, Any] = {"h": h, "summary_all_k": summary, "per_k": per_k}
        if h == 0:
            leave = [item["restricted_T"] for item in per_k if item["k"] != 0]
            leave_summary = population(leave)
            leave_summary["argmin_k"] = [item["k"] for item in per_k if item["k"] != 0 and item["restricted_T"] == min(leave)]
            record["summary_leave_anchor_out"] = leave_summary
        classes.append(record)
    return {
        "schema": "a303656-k4-five-way-common-uncovered-v1",
        "classification": "EXACT FINITE COMPUTATION ON THE FIXED 1285-POINT PANEL",
        "definition": "I_all = E \\ union_h C_h",
        "common_uncovered_pair_count": len(domain),
        "common_uncovered_pair_indices": sorted(domain),
        "fixed_count_thresholds_declared_in_source_before_results": list(FIVE_THRESHOLDS),
        "classes": classes,
    }


def expected_residual(h: int, profiles: dict[int, dict[int, dict[str, Any]]], covered: dict[int, set[int]], leave: bool = False) -> dict[str, Any]:
    domain = [index for index in range(ACTIVE) if index not in covered[h]]
    denominator = 256 if leave else 257
    counts = [profiles[h][index]["count"] - int(leave and 0 in profiles[h][index]["winning_k"]) for index in domain]
    histogram = Counter(counts)
    return {
        "h": h,
        "k_scope": "leave_anchor_k0_out" if leave else "all_-128_through_128",
        "point_count": denominator,
        "persistent_covered_pair_count": len(covered[h]),
        "uncovered_pair_count": len(domain),
        "total_winner_incidences": sum(counts),
        "total_possible_uncovered_incidences": denominator * len(domain),
        "residual_survival_rate": fraction_record(Fraction(sum(counts), denominator * len(domain))),
        "pair_survival_count_histogram": {str(count): histogram[count] for count in sorted(histogram)},
        "never_winning_uncovered_pairs": sum(count == 0 for count in counts),
        "wins_every_k_uncovered_pairs": sum(count == denominator for count in counts),
        "high_survival_pair_counts": {
            f"ge_{threshold}_percent": sum(count * 100 >= threshold * denominator for count in counts)
            for threshold in FREQUENCY_THRESHOLDS
        },
    }


def verify_class_frequency_csv(
    path: Path,
    pairs: list[dict[str, Any]],
    profiles: dict[int, dict[int, dict[str, Any]]],
    covered: dict[int, set[int]],
) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        parser = csv.DictReader(handle)
        source = list(parser)
    expected_count = sum(ACTIVE - len(covered[h]) for h in H_VALUES)
    demand(len(source) == expected_count, "class-pair frequency row count mismatch")
    position = 0
    for h in H_VALUES:
        for pair in pairs:
            index = pair["pair_index"]
            if index in covered[h]:
                continue
            row = source[position]
            position += 1
            profile = profiles[h][index]
            count = profile["count"]
            expected = {
                "h": str(h), "pair_index": str(index), "c": str(pair["c"]), "d": str(pair["d"]),
                "shift": str(pair["shift"]), "survival_count": str(count),
                "survival_frequency_numerator": str(count), "survival_frequency_denominator": "257",
                "survival_frequency_decimal": fraction_decimal(Fraction(count, 257)),
                "first_winning_k": "" if profile["first"] is None else str(profile["first"]),
                "last_winning_k": "" if profile["last"] is None else str(profile["last"]),
                "longest_consecutive_winning_run": str(profile["longest"]),
                "never_wins": str(int(count == 0)), "wins_every_k": str(int(count == 257)),
                "leave_anchor_out_survival_count": "", "leave_anchor_out_frequency_numerator": "",
                "leave_anchor_out_frequency_denominator": "", "leave_anchor_out_frequency_decimal": "",
            }
            if h == 0:
                reduced = count - int(0 in profile["winning_k"])
                expected.update(
                    {
                        "leave_anchor_out_survival_count": str(reduced),
                        "leave_anchor_out_frequency_numerator": str(reduced),
                        "leave_anchor_out_frequency_denominator": "256",
                        "leave_anchor_out_frequency_decimal": fraction_decimal(Fraction(reduced, 256)),
                    }
                )
            demand(row == expected, f"class-pair frequency content mismatch at h={h}, index={index}")


def expected_hard(
    pairs: list[dict[str, Any]], profiles: dict[int, dict[int, dict[str, Any]]],
    covered: dict[int, set[int]], i_all: set[int]
) -> dict[str, Any]:
    records = []
    for index in range(ACTIVE):
        if index in covered[0]:
            continue
        pair = pairs[index]
        count = profiles[0][index]["count"]
        controls: dict[str, Any] = {}
        for h in (-720, -360, 360, 720):
            control_count = profiles[h][index]["count"]
            controls[str(h)] = {
                "persistent_covered": index in covered[h],
                "survival_count": control_count,
                "survival_frequency": fraction_record(Fraction(control_count, 257)),
                "status": "PERSISTENT_COVERED" if index in covered[h] else (
                    "NEVER_WINS" if control_count == 0 else "VERY_FREQUENT_WIN" if control_count * 2 >= 257 else
                    "FREQUENT_WIN" if control_count * 4 >= 257 else "SOMETIMES_WIN"
                ),
            }
        records.append(
            {
                "pair_index": index, "c": pair["c"], "d": pair["d"], "shift": pair["shift"],
                "survival_count": count, "survival_frequency": fraction_record(Fraction(count, 257)),
                "belongs_to_I_all": index in i_all,
                "classifications": {
                    "NEVER_WIN_TARGET": count == 0, "SOMETIMES_WIN_TARGET": count > 0,
                    "FREQUENT_WIN_TARGET": count * 4 >= 257, "VERY_FREQUENT_WIN_TARGET": count * 2 >= 257,
                },
                "control_status": controls,
                "P4_residue_vector_shift_mod_p_squared": {str(p): pair["shift"] % (p * p) for p in P4},
            }
        )
    sets = {
        name: [item["pair_index"] for item in records if item["classifications"][name]]
        for name in ("NEVER_WIN_TARGET", "SOMETIMES_WIN_TARGET", "FREQUENT_WIN_TARGET", "VERY_FREQUENT_WIN_TARGET")
    }
    return {
        "schema": "a303656-k4-hard-survivor-pairs-v1",
        "classification": "FINITE EMPIRICAL CLASSIFICATIONS ON THE FIXED TARGET PANEL ONLY",
        "target_uncovered_pair_count": len(records),
        "set_counts": {name: len(indices) for name, indices in sets.items()},
        "sets_by_pair_index": sets,
        "pairs": records,
    }


def verify_cross_csv(
    path: Path,
    pairs: list[dict[str, Any]], profiles: dict[int, dict[int, dict[str, Any]]], covered: dict[int, set[int]]
) -> None:
    with path.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    demand(len(rows) == ACTIVE, "cross-class profile row count mismatch")
    expected_rank_inputs: list[tuple[int, int, Fraction]] = []
    for index in range(ACTIVE):
        target = profiles[0][index]["count"]
        controls = sum(profiles[h][index]["count"] for h in (-720, -360, 360, 720))
        expected_rank_inputs.append((index, target, Fraction(target, 257) - Fraction(controls, 4 * 257)))
    rank_target = {index: rank for rank, (index, _, _) in enumerate(sorted(expected_rank_inputs, key=lambda item: (-item[1], item[0])), 1)}
    rank_excess = {index: rank for rank, (index, _, _) in enumerate(sorted(expected_rank_inputs, key=lambda item: (-item[2], item[0])), 1)}
    rank_deficit = {index: rank for rank, (index, _, _) in enumerate(sorted(expected_rank_inputs, key=lambda item: (item[2], item[0])), 1)}
    for index, (raw, pair) in enumerate(zip(rows, pairs)):
        demand(canonical_decimal(raw["pair_index"], "cross index", nonnegative=True) == index, "cross-class pair order mismatch")
        demand((canonical_decimal(raw["c"], "cross c", nonnegative=True),
                canonical_decimal(raw["d"], "cross d", nonnegative=True),
                canonical_decimal(raw["shift"], "cross shift", nonnegative=True)) ==
               (pair["c"], pair["d"], pair["shift"]), "cross-class pair identity mismatch")
        target = profiles[0][index]["count"]
        controls = sum(profiles[h][index]["count"] for h in (-720, -360, 360, 720))
        excess = Fraction(target, 257) - Fraction(controls, 4 * 257)
        demand(raw["target_survival_count"] == str(target) and raw["target_survival_frequency"] == fraction_decimal(Fraction(target, 257)),
               "cross target profile mismatch")
        for h in H_VALUES:
            count = profiles[h][index]["count"]
            demand(raw[f"h_{h}_persistent_covered"] == str(int(index in covered[h])) and
                   raw[f"h_{h}_survival_count"] == str(count) and
                   raw[f"h_{h}_survival_frequency"] == fraction_decimal(Fraction(count, 257)),
                   f"cross profile mismatch at h={h}, index={index}")
        checks = {
            "mean_control_frequency_numerator": str(controls),
            "mean_control_frequency_denominator": str(4 * 257),
            "mean_control_frequency_decimal": fraction_decimal(Fraction(controls, 4 * 257)),
            "target_minus_mean_control_frequency_numerator": str(excess.numerator),
            "target_minus_mean_control_frequency_denominator": str(excess.denominator),
            "target_minus_mean_control_frequency_decimal": fraction_decimal(excess),
            "rank_target_survival_frequency": str(rank_target[index]),
            "rank_target_excess_above_control_mean": str(rank_excess[index]),
            "rank_target_deficit_below_control_mean": str(rank_deficit[index]),
        }
        demand(all(raw[key] == value for key, value in checks.items()), f"cross aggregate/rank mismatch at index={index}")


def selected_direct(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    selected: set[int] = set()
    for row in rows:
        if (row["h"], row["k"]) == (0, 0) or row["k"] in DIRECT_K or row["T"] <= 25:
            selected.add(row["n"])
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        minimum = min(row["T"] for row in class_rows)
        selected.update(row["n"] for row in class_rows if row["T"] == minimum)
    answer = [row for row in rows if row["n"] in selected]
    demand(len(answer) == 73, "direct panel is not the declared 73-point panel")
    return answer


def verify_direct(path: Path, committed_path: Path, rows: list[dict[str, Any]], pairs: list[dict[str, Any]]) -> dict[str, Any]:
    fresh = json_object(path)
    committed = json_object(committed_path)
    demand(fresh.get("schema") == "a303656-k4-ap-direct-verification-v1" and
           fresh.get("implementation_id") == "k4_ap_direct_oracle_v1", "fresh direct identity/schema mismatch")
    selected = selected_direct(rows)
    points = fresh.get("points")
    old_points = committed.get("points")
    demand(isinstance(points, list) and isinstance(old_points, list) and len(points) == len(old_points) == len(selected),
           "direct point count mismatch")
    witnesses = 0
    for point, old, expected in zip(points, old_points, selected):
        for key in ("h", "k", "n", "active_pair_count", "expected_T", "T", "expected_T_match", "winning_exponent_pairs"):
            demand(point.get(key) == old.get(key), f"fresh direct field differs from committed direct artifact: {key}")
        demand((point["h"], point["k"], point["n"], point["T"]) ==
               (expected["h"], expected["k"], expected["n"], expected["T"]), "direct point/mask identity mismatch")
        mask_winners = {(pairs[i]["c"], pairs[i]["d"]) for i in range(ACTIVE) if mask_bit(expected["mask"], i)}
        observed: set[tuple[int, int]] = set()
        for winner in point["winning_exponent_pairs"]:
            c, d = winner["c"], winner["d"]
            demand((c, d) not in observed, "duplicate direct winner")
            observed.add((c, d))
            shift = pow(3, c) + pow(5, d)
            remainder = expected["n"] - shift
            a, b = winner["a"], winner["b"]
            demand(winner["shift"] == shift and winner["remainder"] == remainder and 0 <= a <= b,
                   "direct winner identity/canonicality mismatch")
            demand(a * a + b * b == remainder, "direct winner witness equation failure")
            witnesses += 1
        demand(observed == mask_winners and len(observed) == expected["T"], "complete direct winner set differs from masks")
    return {"selected_point_count": 73, "verified_witness_count": witnesses, "complete_winner_sets_match": True,
            "all_witnesses_independently_rechecked": True}


def verify_negative_report(path: Path) -> list[dict[str, Any]]:
    report = json_object(path)
    tests = report.get("tests")
    demand(report.get("schema") == "a303656-k4-survivor-negative-tests-v1" and isinstance(tests, list),
           "negative-test report schema mismatch")
    names = {item.get("name") for item in tests if isinstance(item, dict)}
    demand(names == EXPECTED_NEGATIVE_TESTS, f"negative-test coverage differs: {names ^ EXPECTED_NEGATIVE_TESTS}")
    demand(all(item.get("rejected") is True and isinstance(item.get("return_code"), int) and item["return_code"] != 0 for item in tests),
           "at least one negative test did not reject")
    return tests


def interpretation(pairwise: dict[str, Any], five: dict[str, Any], rows: list[dict[str, Any]], hard: dict[str, Any]) -> dict[str, Any]:
    pairwise_checks: dict[str, Any] = {}
    for comparison in pairwise["comparisons"]:
        record: dict[str, Any] = {}
        for scope in ("including_anchor_k0", "leave_anchor_out"):
            summary = comparison[scope]
            target_mean = Fraction(summary["target"]["mean"]["numerator"], summary["target"]["mean"]["denominator"])
            control_mean = Fraction(summary["control"]["mean"]["numerator"], summary["control"]["mean"]["denominator"])
            target_median = Fraction(summary["target"]["median"]["numerator"], summary["target"]["median"]["denominator"])
            control_median = Fraction(summary["control"]["median"]["numerator"], summary["control"]["median"]["denominator"])
            record[scope] = {
                "target_mean_lower": target_mean < control_mean,
                "target_median_lower": target_median < control_median,
                "negative_differences_exceed_positive": summary["negative_count"] > summary["positive_count"],
            }
            record[scope]["retains_lower_distribution_under_declared_descriptive_criterion"] = all(record[scope].values())
        pairwise_checks[str(comparison["control_h"])] = record
    pairwise_all = all(
        pairwise_checks[str(h)][scope]["retains_lower_distribution_under_declared_descriptive_criterion"]
        for h in (-720, -360, 360, 720) for scope in ("including_anchor_k0", "leave_anchor_out")
    )

    by_h = {item["h"]: item for item in five["classes"]}
    target_mean = Fraction(by_h[0]["summary_all_k"]["mean"]["numerator"], by_h[0]["summary_all_k"]["mean"]["denominator"])
    target_median = Fraction(by_h[0]["summary_all_k"]["median"]["numerator"], by_h[0]["summary_all_k"]["median"]["denominator"])
    all_lower = all(
        target_mean < Fraction(by_h[h]["summary_all_k"]["mean"]["numerator"], by_h[h]["summary_all_k"]["mean"]["denominator"])
        and target_median < Fraction(by_h[h]["summary_all_k"]["median"]["numerator"], by_h[h]["summary_all_k"]["median"]["denominator"])
        for h in (-720, -360, 360, 720)
    )
    target_leave = [item["restricted_T"] for item in by_h[0]["per_k"] if item["k"] != 0]
    leave_lower = all(
        Fraction(sum(target_leave), len(target_leave)) <
        Fraction(sum(item["restricted_T"] for item in by_h[h]["per_k"] if item["k"] != 0), 256)
        and exact_median(target_leave) < exact_median([item["restricted_T"] for item in by_h[h]["per_k"] if item["k"] != 0])
        for h in (-720, -360, 360, 720)
    )

    raw_means = {h: Fraction(sum(row["T"] for row in rows if row["h"] == h), 257) for h in H_VALUES}
    mean_control_raw = sum((raw_means[h] for h in (-720, -360, 360, 720)), Fraction()) / 4
    mean_control_residual = sum(
        (Fraction(by_h[h]["summary_all_k"]["mean"]["numerator"], by_h[h]["summary_all_k"]["mean"]["denominator"])
         for h in (-720, -360, 360, 720)), Fraction()
    ) / 4
    raw_gap = raw_means[0] - mean_control_raw
    residual_gap = target_mean - mean_control_residual
    reduction = Fraction(0)
    if raw_gap != 0:
        reduction = 1 - abs(residual_gap) / abs(raw_gap)
    mostly_explained = reduction >= Fraction(1, 2)
    if pairwise_all and all_lower and leave_lower:
        allowed = "RESIDUAL SECONDARY ENRICHMENT OBSERVED ON THIS FIXED PANEL"
    elif mostly_explained and not pairwise_all and not all_lower:
        allowed = "RAW ENRICHMENT EXPLAINED PRIMARILY BY GUARANTEED COVERAGE"
    else:
        allowed = "MIXED / INCONCLUSIVE FINITE RESULT"
    return {
        "descriptive_criterion": "strictly lower mean and median, with more negative than positive matched-k differences for pairwise comparisons",
        "pairwise_common_uncovered": pairwise_checks,
        "target_lower_on_every_pairwise_common_uncovered_set_with_and_without_anchor": pairwise_all,
        "target_lower_on_I_all_mean_and_median_vs_every_control_all_k": all_lower,
        "target_lower_on_I_all_mean_and_median_vs_every_control_leave_anchor_out": leave_lower,
        "raw_target_minus_mean_control_mean": fraction_record(raw_gap),
        "I_all_target_minus_mean_control_mean": fraction_record(residual_gap),
        "absolute_gap_reduction_fraction_after_I_all_restriction": fraction_record(reduction),
        "raw_enrichment_mostly_explained_by_guaranteed_coverage_under_50_percent_gap_reduction_rule": mostly_explained,
        "target_frequent_pair_count": hard["set_counts"]["FREQUENT_WIN_TARGET"],
        "target_very_frequent_pair_count": hard["set_counts"]["VERY_FREQUENT_WIN_TARGET"],
        "secondary_residue_effect_observed_under_declared_descriptive_criterion": pairwise_all and all_lower and leave_lower,
        "allowed_coverage_adjusted_interpretation": allowed,
        "claim_boundary": "finite descriptive result only; no statistical-significance, causal, necessity, or global claim",
    }


def atomic_report(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        json.dump(value, handle, indent=2, sort_keys=True)
        handle.write("\n")
    os.replace(temporary, path)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    parser.add_argument("--results-commit", default=RESULT_SENTINEL)
    parser.add_argument("--backend-a-core", type=Path, required=True)
    parser.add_argument("--backend-b-core", type=Path, required=True)
    parser.add_argument("--direct-oracle", type=Path, required=True)
    parser.add_argument("--direct-json", type=Path, required=True)
    parser.add_argument("--negative-tests", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    try:
        args = parse_args()
        root = args.source_root.resolve()
        artifact = args.artifact_dir.resolve()
        observed_files = {path.name for path in artifact.iterdir() if path.is_file()}
        demand(observed_files in (ARTIFACT_NAMES, ARTIFACT_NAMES | {"verification_report.json"}),
               "artifact directory file set is incomplete or contains unexpected extras")
        metadata = json_object(artifact / "metadata.json")
        manifest = json_object(artifact / "mask_manifest.json")
        demand(metadata.get("schema") == "a303656-k4-survivor-incidence-metadata-v1", "metadata schema mismatch")
        demand(manifest.get("schema") == "a303656-k4-survivor-mask-manifest-v1", "mask manifest schema mismatch")
        chain = verify_commit_and_sources(root, artifact, metadata, args.source_commit, args.results_commit)
        protected = protected_record(root)
        demand(metadata.get("protected_baseline_and_prior_pilot_hashes_before") == protected and
               metadata.get("protected_baseline_and_prior_pilot_hashes_after") == protected,
               "metadata protected-hash record mismatch")

        panel = expected_panel()
        pairs = read_pair_csv(artifact / "pair_order.csv")
        pair_hash = digest_file(artifact / "pair_order.csv")
        demand(metadata.get("pair_order_sha256") == pair_hash == manifest.get("pair_order_sha256"), "pair-order hash manifest mismatch")
        a_rows = parse_masks(artifact / "backend_a_masks.bin", panel, pair_hash)
        b_rows = parse_masks(artifact / "backend_b_masks.bin", panel, pair_hash)
        demand(a_rows == b_rows, "pointwise masks differ")
        demand((artifact / "backend_a_masks.bin").read_bytes() == (artifact / "backend_b_masks.bin").read_bytes(),
               "backend mask files are not byte-identical")
        covered = reconstruct_covered(root, pairs, a_rows)
        prior_t = read_prior_t(root, panel)
        demand([row["T"] for row in a_rows] == prior_t, "fresh T vector differs from committed K4 panel")
        demand(metadata.get("panel", {}).get("panel_csv_sha256") == digest_bytes(serialized_panel(panel)), "metadata panel hash mismatch")
        demand(metadata.get("full_mask_equality") == {"status": "PASS", "point_count": 1285, "mismatch_count": 0, "byte_identical_files": True},
               "metadata full-mask claim mismatch")

        mask_hash = digest_file(artifact / "backend_a_masks.bin")
        demand(manifest.get("mask_files") == {"backend_a_masks.bin": mask_hash, "backend_b_masks.bin": mask_hash},
               "mask-file hash manifest mismatch")
        demand(manifest.get("row_count") == 1285 and manifest.get("pair_count") == ACTIVE and
               manifest.get("full_pointwise_mask_equality") is True and manifest.get("popcount_equals_T_all_rows") is True,
               "mask-manifest finite claims mismatch")
        verify_identities(root, metadata, manifest, args)

        profiles = survival_profiles(a_rows, covered)
        expected_class = [expected_residual(h, profiles, covered) for h in H_VALUES]
        expected_leave = expected_residual(0, profiles, covered, leave=True)
        demand(metadata.get("class_residual_survival_analysis") == expected_class, "class residual summaries differ")
        demand(metadata.get("target_leave_anchor_out_residual_survival_analysis") == expected_leave,
               "target leave-anchor-out residual summary differs")
        verify_class_frequency_csv(artifact / "class_pair_frequencies.csv", pairs, profiles, covered)

        pairwise = expected_pairwise(a_rows, covered)
        demand(json_object(artifact / "pairwise_common_uncovered.json") == pairwise, "pairwise common-uncovered artifact differs")
        five = expected_five(a_rows, covered)
        demand(json_object(artifact / "five_way_common_uncovered.json") == five, "five-way common-uncovered artifact differs")
        i_all = set(five["common_uncovered_pair_indices"])
        hard = expected_hard(pairs, profiles, covered, i_all)
        demand(json_object(artifact / "hard_survivor_pairs.json") == hard, "hard-survivor artifact differs")
        verify_cross_csv(artifact / "cross_class_pair_profiles.csv", pairs, profiles, covered)

        direct = verify_direct(args.direct_json, root / "analysis/k4_ap_pilot/direct_verification.json", a_rows, pairs)
        demand(metadata.get("direct_oracle_verification", {}).get("selected_point_count") == 73 and
               metadata.get("direct_oracle_verification", {}).get("independently_rechecked_witness_count") == direct["verified_witness_count"],
               "metadata direct-verification summary differs")
        negative_tests = verify_negative_report(args.negative_tests)

        hashes = metadata.get("artifact_sha256_excluding_metadata_and_verification_report")
        demand(isinstance(hashes, dict), "artifact hash manifest missing")
        for name, expected in hashes.items():
            demand(digest_file(artifact / name) == expected, f"artifact hash mismatch: {name}")
        source_guard = metadata.get("scope_guards")
        demand(source_guard == {
            "formal_points_evaluated_by_each_backend": 1285, "direct_oracle_points": 73,
            "other_integer_evaluations": 0, "adaptive_points_added": 0,
            "k_outside_fixed_interval_evaluated": False, "remaining_activation_cell_progression_scanned": False,
            "P4_M4_h_or_classes_changed": False, "CRT_optimization_performed": False,
        }, "scope-guard record mismatch")

        report = {
            "schema": "a303656-k4-survivor-incidence-verification-report-v1",
            "status": "PASS",
            "classification": "INDEPENDENTLY VERIFIED EXACT FINITE COMPUTATION ON THE FIXED 1285-POINT PANEL; GLOBAL PROBLEM UNRESOLVED",
            "commit_chain": chain,
            "panel": {"point_count": 1285, "h_values": list(H_VALUES), "k_interval": [K_MIN, K_MAX],
                      "active_pair_count": ACTIVE, "unique_integer_count": 1285, "all_fields_match_committed_K4_artifacts": True},
            "pair_order": {"row_count": ACTIVE, "sha256": pair_hash, "canonical_lexicographic_c_then_d": True,
                           "duplicate_shift_group_28": [index for index, pair in enumerate(pairs) if pair["shift"] == 28]},
            "backend_masks": {"pointwise_equal": True, "byte_identical_files": True, "mask_sha256": mask_hash,
                              "popcount_equals_T_all_rows": True, "T_matches_committed_K4_panel_all_rows": True},
            "direct_oracle": direct,
            "persistent_covered_sets": {str(h): {"covered": len(covered[h]), "uncovered": ACTIVE - len(covered[h]),
                                                  "covered_pair_winner_count": 0} for h in H_VALUES},
            "class_residual_survival_analysis": expected_class,
            "target_leave_anchor_out_residual_survival_analysis": expected_leave,
            "pairwise_common_uncovered": [
                {"control_h": item["control_h"], "I_h_size": item["common_uncovered_pair_count"],
                 "including_anchor_k0": item["including_anchor_k0"], "leave_anchor_out": item["leave_anchor_out"]}
                for item in pairwise["comparisons"]
            ],
            "five_way_common_uncovered": {"I_all_size": five["common_uncovered_pair_count"],
                                           "classes": [{"h": item["h"], "summary_all_k": item["summary_all_k"],
                                                        **({"summary_leave_anchor_out": item["summary_leave_anchor_out"]} if item["h"] == 0 else {})}
                                                       for item in five["classes"]]},
            "hard_survivor_set_counts": hard["set_counts"],
            "cross_class_pair_profiles": {"pair_count": ACTIVE, "three_rankings_complete": True,
                                           "claim_boundary": "finite empirical ranks only"},
            "coverage_adjusted_interpretation": interpretation(pairwise, five, a_rows, hard),
            "negative_tests": {"required_count": len(EXPECTED_NEGATIVE_TESTS), "all_rejected": True,
                               "tests": negative_tests},
            "protected_baseline_and_prior_pilot_hashes": protected,
            "discovered_bugs": [],
            "unresolved_risks": [
                "The panel is finite and preselected; no result is a global theorem or statistical-significance claim.",
                "Direct-oracle completeness is checked on the predeclared 73-point panel, while full-panel masks rely on the two independent factorization cores.",
            ],
            "final_conclusion": "VALIDATED K4 SURVIVOR-INCIDENCE AUDIT",
        }
        atomic_report(args.report, report)
        if args.results_commit != RESULT_SENTINEL:
            committed_report = git(
                root,
                "show",
                f"{args.results_commit}:analysis/k4_survivor_incidence/verification_report.json",
            ).stdout
            demand(committed_report == args.report.read_bytes(),
                   "regenerated verification report differs from results commit")
        print("VALIDATED K4 SURVIVOR-INCIDENCE AUDIT")
        return 0
    except (Rejection, OSError, UnicodeError, csv.Error, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"K4 SURVIVOR-INCIDENCE AUDIT NOT VALIDATED: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
