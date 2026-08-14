#!/usr/bin/env python3
"""Generate the fixed-panel K4 survivor-incidence audit artifacts.

This runner is deliberately unable to accept alternate n, h, k, P4, M4, or
pair-domain parameters.  It rebuilds both existing factorization cores and the
existing direct oracle from source, evaluates exactly the committed 1,285
points, and writes only compact masks and summaries.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
import os
import resource
import shutil
import statistics
import struct
import subprocess
import sys
import time
from collections import Counter
from decimal import Decimal, localcontext
from fractions import Fraction
from pathlib import Path
from typing import Any, Iterable


N0 = 240000005594
P4 = (3, 7, 11, 23)
M4 = 28227969
H_VALUES = (-720, -360, 0, 360, 720)
K_LOW = -128
K_HIGH = 128
ACTIVE = 407
MASK_BYTES = 51
CELL = (183968950234, 246731069451)
BASELINE_COMMIT = "406677c3b095d2125a4a439c76b3a8d6788cb1da"
RESULTS_SENTINEL = "RESULT_COMMIT_CONTAINING_THIS_FILE"
FIXED_DIRECT_K = (-128, -96, -64, -32, -1, 0, 1, 32, 64, 96, 128)
FREQUENCY_THRESHOLDS = (10, 25, 50, 75)
FIVE_WAY_FIXED_COUNT_THRESHOLDS = (10, 20, 30, 40)
MAGIC = b"K4SMASK1"
HEADER = struct.Struct("<8sIIIIII32s")
ROW = struct.Struct("<QqqII")
REQUIRED_OUTPUTS = {
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
PRIOR_K4_HASHES = {
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


class AuditFailure(RuntimeError):
    pass


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AuditFailure(message)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", encoding="utf-8") as stream:
        json.dump(value, stream, indent=2, sort_keys=True)
        stream.write("\n")
    os.replace(temporary, path)


def atomic_csv(path: Path, fieldnames: list[str], rows: Iterable[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    with temporary.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise AuditFailure(f"cannot load JSON {path}: {exc}") from exc
    require(isinstance(value, dict), f"JSON root is not an object: {path}")
    return value


def strict_int(text: str, label: str, *, nonnegative: bool = False) -> int:
    require(bool(text) and text == text.strip() and not text.startswith("+"), f"malformed {label}")
    digits = text[1:] if text.startswith("-") else text
    require(digits.isascii() and digits.isdigit(), f"malformed {label}")
    require(len(digits) == 1 or not digits.startswith("0"), f"leading zero in {label}")
    value = int(text)
    require(not nonnegative or value >= 0, f"negative {label}")
    return value


def git(root: Path, *arguments: str, check: bool = True) -> subprocess.CompletedProcess[bytes]:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    if check and result.returncode != 0:
        raise AuditFailure(
            f"git {' '.join(arguments)} failed: {result.stderr.decode('utf-8', 'replace')}"
        )
    return result


def git_text(root: Path, *arguments: str) -> str:
    return git(root, *arguments).stdout.decode("ascii", "strict").strip()


def validate_source_chain(root: Path, source_commit: str) -> dict[str, Any]:
    require(len(source_commit) == 40 and all(ch in "0123456789abcdef" for ch in source_commit), "malformed source commit")
    resolved = git_text(root, "rev-parse", f"{source_commit}^{{commit}}")
    require(resolved == source_commit, "source commit is not canonical")
    parent = git_text(root, "rev-parse", f"{source_commit}^")
    require(parent == BASELINE_COMMIT, f"source commit parent {parent} != required baseline {BASELINE_COMMIT}")
    require(git(root, "merge-base", "--is-ancestor", BASELINE_COMMIT, source_commit, check=False).returncode == 0,
            "required baseline is not an ancestor of source commit")
    return {
        "baseline_commit": BASELINE_COMMIT,
        "source_commit": source_commit,
        "source_parent_commit": parent,
        "source_parent_is_exact_required_head": True,
    }


def powers(base: int, limit: int) -> list[tuple[int, int]]:
    values: list[tuple[int, int]] = []
    exponent, value = 0, 1
    while value <= limit:
        values.append((exponent, value))
        if value > limit // base:
            break
        exponent += 1
        value *= base
    return values


def canonical_pairs() -> list[dict[str, Any]]:
    minimum = N0 + min(H_VALUES) + K_LOW * M4
    raw = [
        (c, d, p3 + p5)
        for c, p3 in powers(3, minimum)
        for d, p5 in powers(5, minimum)
        if p3 + p5 <= minimum
    ]
    require(raw == sorted(raw) and len(raw) == ACTIVE, "canonical pair regeneration failed")
    counts = Counter(shift for _, _, shift in raw)
    require({shift: count for shift, count in counts.items() if count > 1} == {28: 2},
            "duplicate-shift regeneration failed")
    return [
        {
            "pair_index": index,
            "c": c,
            "d": d,
            "shift": shift,
            "duplicate_shift_group": f"shift_{shift}" if counts[shift] > 1 else "",
        }
        for index, (c, d, shift) in enumerate(raw)
    ]


def fixed_panel() -> list[dict[str, int]]:
    rows = [
        {"h": h, "k": k, "n": N0 + h + k * M4, "active_pairs": ACTIVE}
        for h in H_VALUES
        for k in range(K_LOW, K_HIGH + 1)
    ]
    require(len(rows) == 1285 and len({row["n"] for row in rows}) == 1285, "fixed panel cardinality failure")
    require(all(CELL[0] <= row["n"] <= CELL[1] for row in rows), "fixed panel left activation cell")
    domain = [(item["c"], item["d"], item["shift"]) for item in canonical_pairs()]
    for endpoint in (min(row["n"] for row in rows), max(row["n"] for row in rows)):
        observed = [
            (c, d, p3 + p5)
            for c, p3 in powers(3, endpoint)
            for d, p5 in powers(5, endpoint)
            if p3 + p5 <= endpoint
        ]
        require(observed == domain, "active domain changes within fixed panel")
    return rows


def panel_bytes(panel: list[dict[str, int]]) -> bytes:
    buffer = io.StringIO(newline="")
    writer = csv.DictWriter(buffer, fieldnames=["h", "k", "n", "active_pairs"], lineterminator="\n")
    writer.writeheader()
    writer.writerows(panel)
    return buffer.getvalue().encode("utf-8")


def verify_protected_inputs(root: Path) -> dict[str, Any]:
    for relative, expected in PRIOR_K4_HASHES.items():
        path = root / relative
        require(path.is_file() and sha256_file(path) == expected, f"prior K4 artifact changed: {relative}")
    p2_metadata = load_json(root / "analysis/p2_core/metadata.json")
    manifest = p2_metadata.get("fixed_input_audit", {}).get("fixed_input_tree_sha256")
    require(isinstance(manifest, dict) and len(manifest) == 86, "protected baseline manifest missing")
    for relative, expected in manifest.items():
        require(isinstance(relative, str) and isinstance(expected, str), "malformed protected baseline manifest")
        path = root / relative
        require(path.is_file() and sha256_file(path) == expected, f"protected baseline changed: {relative}")
    baseline_canonical = "".join(f"{manifest[path]}  {path}\n" for path in sorted(manifest))
    k4_canonical = "".join(f"{PRIOR_K4_HASHES[path]}  {path}\n" for path in sorted(PRIOR_K4_HASHES))
    return {
        "baseline_manifest_file_count": len(manifest),
        "baseline_manifest_sha256": sha256_bytes(baseline_canonical.encode()),
        "prior_k4_file_count": len(PRIOR_K4_HASHES),
        "prior_k4_manifest_sha256": sha256_bytes(k4_canonical.encode()),
        "all_byte_identical": True,
        "mismatch_count": 0,
    }


def read_prior_counts(root: Path, panel: list[dict[str, int]]) -> list[dict[str, int]]:
    paths = [
        root / "analysis/k4_ap_pilot/backend_a_counts.csv",
        root / "analysis/k4_ap_pilot/backend_b_counts.csv",
    ]
    parsed_sets: list[list[dict[str, int]]] = []
    for path in paths:
        with path.open(newline="", encoding="utf-8") as stream:
            reader = csv.DictReader(stream)
            require(reader.fieldnames == ["h", "k", "n", "T", "active_pairs"], "prior counts header drift")
            raw = list(reader)
        require(len(raw) == len(panel), "prior counts row count drift")
        rows: list[dict[str, int]] = []
        for item, expected in zip(raw, panel):
            row = {key: strict_int(item[key], f"prior {key}", nonnegative=key in {"n", "T", "active_pairs"})
                   for key in ("h", "k", "n", "T", "active_pairs")}
            require((row["h"], row["k"], row["n"], row["active_pairs"]) ==
                    (expected["h"], expected["k"], expected["n"], ACTIVE), "prior panel field mismatch")
            rows.append(row)
        parsed_sets.append(rows)
    require(parsed_sets[0] == parsed_sets[1], "committed K4 backends do not match")
    metadata = load_json(root / "analysis/k4_ap_pilot/metadata.json")
    require(metadata.get("panel", {}).get("panel_csv_sha256") == sha256_bytes(panel_bytes(panel)),
            "reconstructed panel hash differs from committed K4 metadata")
    require(metadata.get("panel", {}).get("point_count") == 1285 and
            metadata.get("panel", {}).get("h_values") == list(H_VALUES) and
            metadata.get("panel", {}).get("k_interval") == [K_LOW, K_HIGH],
            "committed K4 metadata panel fields differ")
    with (root / "analysis/k4_ap_pilot/pointwise_comparison.csv").open(newline="", encoding="utf-8") as stream:
        comparison = list(csv.DictReader(stream))
    require(len(comparison) == len(panel), "committed pointwise comparison row count differs")
    for record, expected in zip(comparison, parsed_sets[0]):
        require(
            (
                strict_int(record["h"], "pointwise h"),
                strict_int(record["k"], "pointwise k"),
                strict_int(record["n"], "pointwise n", nonnegative=True),
                strict_int(record["backend_a_T"], "pointwise A T", nonnegative=True),
                strict_int(record["backend_b_T"], "pointwise B T", nonnegative=True),
                strict_int(record["active_pairs"], "pointwise active", nonnegative=True),
                strict_int(record["pointwise_equal"], "pointwise equality", nonnegative=True),
            )
            == (expected["h"], expected["k"], expected["n"], expected["T"], expected["T"], ACTIVE, 1),
            "committed pointwise panel field/T differs",
        )
    return parsed_sets[0]


def write_pair_order(path: Path, pairs: list[dict[str, Any]]) -> str:
    atomic_csv(path, ["pair_index", "c", "d", "shift", "duplicate_shift_group"], pairs)
    return sha256_file(path)


def write_panel(path: Path, panel: list[dict[str, int]]) -> None:
    atomic_csv(path, ["h", "k", "n", "active_pairs"], panel)


def run_logged(command: list[str], cwd: Path, log_dir: Path, label: str) -> dict[str, Any]:
    log_dir.mkdir(parents=True, exist_ok=True)
    stdout_path = log_dir / f"{label}.stdout.log"
    stderr_path = log_dir / f"{label}.stderr.log"
    started = time.monotonic()
    with stdout_path.open("wb") as stdout, stderr_path.open("wb") as stderr:
        completed = subprocess.run(command, cwd=cwd, check=False, stdout=stdout, stderr=stderr)
    elapsed = time.monotonic() - started
    record = {
        "label": label,
        "command": command,
        "return_code": completed.returncode,
        "elapsed_seconds": format(elapsed, ".6f"),
        "stdout_sha256": sha256_file(stdout_path),
        "stderr_sha256": sha256_file(stderr_path),
    }
    require(completed.returncode == 0, f"{label} failed with return code {completed.returncode}")
    return record


def build_tools(root: Path, work: Path, logs: Path) -> tuple[dict[str, Path], list[dict[str, Any]]]:
    bin_dir = work / "bin"
    bin_dir.mkdir(parents=True, exist_ok=True)
    specifications = {
        "backend_a_core": (root / "src/k4_ap_backend_a.cpp", bin_dir / "k4_ap_backend_a"),
        "backend_b_core": (root / "src/k4_ap_backend_b.cpp", bin_dir / "k4_ap_backend_b"),
        "direct_oracle": (root / "src/k4_ap_direct_oracle.cpp", bin_dir / "k4_ap_direct_oracle"),
    }
    records: list[dict[str, Any]] = []
    for label, (source, binary) in specifications.items():
        command = ["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", str(source), "-o", str(binary)]
        records.append(run_logged(command, root, logs, f"build_{label}"))
    return {label: binary for label, (_, binary) in specifications.items()}, records


def read_mask_file(path: Path, expected_pair_hash: str, panel: list[dict[str, int]]) -> list[dict[str, Any]]:
    data = path.read_bytes()
    expected_size = HEADER.size + len(panel) * (ROW.size + MASK_BYTES)
    require(len(data) == expected_size, f"mask file {path.name} size {len(data)} != {expected_size}")
    header = HEADER.unpack_from(data, 0)
    require(header[:7] == (MAGIC, 1, HEADER.size, len(panel), ACTIVE, MASK_BYTES, ROW.size + MASK_BYTES),
            f"mask header mismatch: {path.name}")
    require(header[7].hex() == expected_pair_hash, f"mask pair hash mismatch: {path.name}")
    rows: list[dict[str, Any]] = []
    offset = HEADER.size
    for point in panel:
        n, h, k, active, t_value = ROW.unpack_from(data, offset)
        offset += ROW.size
        mask = data[offset : offset + MASK_BYTES]
        offset += MASK_BYTES
        require((n, h, k, active) == (point["n"], point["h"], point["k"], ACTIVE),
                f"mask point identity/order mismatch at n={point['n']}")
        require(mask[-1] & 0x80 == 0, "unused high mask bit is set")
        require(sum(byte.bit_count() for byte in mask) == t_value, f"mask popcount/T mismatch at n={n}")
        rows.append({**point, "T": t_value, "mask": mask})
    require(offset == len(data), "mask parser did not consume exact file")
    return rows


def bit(mask: bytes, pair_index: int) -> bool:
    return bool(mask[pair_index // 8] & (1 << (pair_index % 8)))


def persistent_sets(
    root: Path, pairs: list[dict[str, Any]], masks: list[dict[str, Any]]
) -> dict[int, set[int]]:
    reconstructed: dict[int, set[int]] = {}
    for h in H_VALUES:
        base = N0 + h
        covered = {
            pair["pair_index"]
            for pair in pairs
            if any((base - pair["shift"]) % p == 0 and (base - pair["shift"]) % (p * p) != 0 for p in P4)
        }
        reconstructed[h] = covered
        for row in masks:
            if row["h"] == h:
                offenders = [index for index in covered if bit(row["mask"], index)]
                require(not offenders, f"persistent-covered winner at h={h}, k={row['k']}: {offenders[:8]}")
    committed = load_json(root / "analysis/k4_ap_pilot/persistent_core_by_class.json")
    require(committed.get("p4") == list(P4) and committed.get("m4") == M4, "committed persistent P4/M4 drift")
    classes = committed.get("classes")
    require(isinstance(classes, list) and len(classes) == len(H_VALUES), "committed persistent class count drift")
    for item, h in zip(classes, H_VALUES):
        require(item.get("h") == h, "committed persistent class order drift")
        expected_pairs = [f"{pairs[index]['c']}:{pairs[index]['d']}" for index in sorted(reconstructed[h])]
        require(item.get("persistent_covered_active_pairs") == expected_pairs, f"committed C_h differs for h={h}")
        require(item.get("persistent_covered_active_pair_count") == len(reconstructed[h]), f"committed |C_h| differs for h={h}")
        require(item.get("uncovered_active_pair_count") == ACTIVE - len(reconstructed[h]), f"committed |U_h| differs for h={h}")
    require({h: len(value) for h, value in reconstructed.items()} == {-720: 214, -360: 182, 0: 216, 360: 198, 720: 209},
            "persistent covered counts do not match committed result")
    return reconstructed


def longest_run(k_values: list[int]) -> int:
    longest = current = 0
    previous: int | None = None
    for value in k_values:
        current = current + 1 if previous is not None and value == previous + 1 else 1
        longest = max(longest, current)
        previous = value
    return longest


def decimal_fraction(value: Fraction, digits: int = 30) -> str:
    with localcontext() as context:
        context.prec = digits
        return format(Decimal(value.numerator) / Decimal(value.denominator), "f")


def exact_fraction(value: Fraction) -> dict[str, Any]:
    return {
        "numerator": value.numerator,
        "denominator": value.denominator,
        "decimal": decimal_fraction(value),
    }


def median_fraction(values: list[int]) -> Fraction:
    ordered = sorted(values)
    middle = len(ordered) // 2
    if len(ordered) % 2:
        return Fraction(ordered[middle])
    return Fraction(ordered[middle - 1] + ordered[middle], 2)


def inverse_ecdf(values: list[int], numerator: int, denominator: int = 100) -> int:
    require(values and 0 <= numerator <= denominator, "invalid inverse ECDF request")
    rank = max(1, (numerator * len(values) + denominator - 1) // denominator)
    return sorted(values)[rank - 1]


def population_summary(values: list[int]) -> dict[str, Any]:
    require(values, "cannot summarize empty population")
    mean = Fraction(sum(values), len(values))
    variance = sum((Fraction(value) - mean) ** 2 for value in values) / len(values)
    with localcontext() as context:
        context.prec = 30
        stddev = (Decimal(variance.numerator) / Decimal(variance.denominator)).sqrt()
    minimum = min(values)
    return {
        "point_count": len(values),
        "mean": exact_fraction(mean),
        "median": exact_fraction(median_fraction(values)),
        "population_variance": exact_fraction(variance),
        "population_standard_deviation_decimal": format(stddev, "f"),
        "quantiles_inverse_ecdf": {
            "q00": inverse_ecdf(values, 0),
            "q10": inverse_ecdf(values, 10),
            "q25": inverse_ecdf(values, 25),
            "q50": inverse_ecdf(values, 50),
            "q75": inverse_ecdf(values, 75),
            "q90": inverse_ecdf(values, 90),
            "q100": inverse_ecdf(values, 100),
        },
        "minimum": minimum,
        "fixed_threshold_counts_le": {
            str(threshold): sum(value <= threshold for value in values)
            for threshold in FIVE_WAY_FIXED_COUNT_THRESHOLDS
        },
    }


def survival_count_table(
    rows: list[dict[str, Any]], covered: dict[int, set[int]]
) -> dict[int, dict[int, dict[str, Any]]]:
    table: dict[int, dict[int, dict[str, Any]]] = {}
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        require([row["k"] for row in class_rows] == list(range(K_LOW, K_HIGH + 1)), "class k sequence drift")
        table[h] = {}
        for index in range(ACTIVE):
            winners = [row["k"] for row in class_rows if bit(row["mask"], index)]
            if index in covered[h]:
                require(not winners, "persistent-covered pair has a winner")
            table[h][index] = {
                "count": len(winners),
                "winning_k": winners,
                "first": winners[0] if winners else None,
                "last": winners[-1] if winners else None,
                "longest": longest_run(winners),
            }
    return table


def threshold_pair_counts(counts: list[int], denominator: int) -> dict[str, int]:
    return {
        f"ge_{threshold}_percent": sum(count * 100 >= threshold * denominator for count in counts)
        for threshold in FREQUENCY_THRESHOLDS
    }


def residual_summary(
    h: int,
    table: dict[int, dict[int, dict[str, Any]]],
    covered: dict[int, set[int]],
    *,
    leave_anchor_out: bool = False,
) -> dict[str, Any]:
    domain = [index for index in range(ACTIVE) if index not in covered[h]]
    denominator = 256 if leave_anchor_out else 257
    counts = [
        table[h][index]["count"] - (1 if leave_anchor_out and 0 in table[h][index]["winning_k"] else 0)
        for index in domain
    ]
    total = sum(counts)
    histogram = Counter(counts)
    return {
        "h": h,
        "k_scope": "leave_anchor_k0_out" if leave_anchor_out else "all_-128_through_128",
        "point_count": denominator,
        "persistent_covered_pair_count": len(covered[h]),
        "uncovered_pair_count": len(domain),
        "total_winner_incidences": total,
        "total_possible_uncovered_incidences": denominator * len(domain),
        "residual_survival_rate": exact_fraction(Fraction(total, denominator * len(domain))),
        "pair_survival_count_histogram": {str(count): histogram[count] for count in sorted(histogram)},
        "never_winning_uncovered_pairs": sum(count == 0 for count in counts),
        "wins_every_k_uncovered_pairs": sum(count == denominator for count in counts),
        "high_survival_pair_counts": threshold_pair_counts(counts, denominator),
    }


def write_class_frequencies(
    path: Path,
    pairs: list[dict[str, Any]],
    table: dict[int, dict[int, dict[str, Any]]],
    covered: dict[int, set[int]],
) -> None:
    fields = [
        "h", "pair_index", "c", "d", "shift", "survival_count", "survival_frequency_numerator",
        "survival_frequency_denominator", "survival_frequency_decimal", "first_winning_k", "last_winning_k",
        "longest_consecutive_winning_run", "never_wins", "wins_every_k",
        "leave_anchor_out_survival_count", "leave_anchor_out_frequency_numerator",
        "leave_anchor_out_frequency_denominator", "leave_anchor_out_frequency_decimal",
    ]
    output: list[dict[str, Any]] = []
    for h in H_VALUES:
        for pair in pairs:
            index = pair["pair_index"]
            if index in covered[h]:
                continue
            profile = table[h][index]
            count = profile["count"]
            row: dict[str, Any] = {
                "h": h,
                "pair_index": index,
                "c": pair["c"],
                "d": pair["d"],
                "shift": pair["shift"],
                "survival_count": count,
                "survival_frequency_numerator": count,
                "survival_frequency_denominator": 257,
                "survival_frequency_decimal": decimal_fraction(Fraction(count, 257)),
                "first_winning_k": "" if profile["first"] is None else profile["first"],
                "last_winning_k": "" if profile["last"] is None else profile["last"],
                "longest_consecutive_winning_run": profile["longest"],
                "never_wins": int(count == 0),
                "wins_every_k": int(count == 257),
                "leave_anchor_out_survival_count": "",
                "leave_anchor_out_frequency_numerator": "",
                "leave_anchor_out_frequency_denominator": "",
                "leave_anchor_out_frequency_decimal": "",
            }
            if h == 0:
                leave_count = count - int(0 in profile["winning_k"])
                row.update(
                    {
                        "leave_anchor_out_survival_count": leave_count,
                        "leave_anchor_out_frequency_numerator": leave_count,
                        "leave_anchor_out_frequency_denominator": 256,
                        "leave_anchor_out_frequency_decimal": decimal_fraction(Fraction(leave_count, 256)),
                    }
                )
            output.append(row)
    atomic_csv(path, fields, output)


def restricted_count(row: dict[str, Any], indices: set[int]) -> int:
    return sum(bit(row["mask"], index) for index in indices)


def paired_summary(target: list[int], control: list[int]) -> dict[str, Any]:
    require(len(target) == len(control) and target, "invalid paired summary")
    differences = [left - right for left, right in zip(target, control)]
    return {
        "point_count": len(target),
        "target": population_summary(target),
        "control": population_summary(control),
        "target_minus_control_mean": exact_fraction(Fraction(sum(differences), len(differences))),
        "target_minus_control_median": exact_fraction(median_fraction(differences)),
        "negative_count": sum(value < 0 for value in differences),
        "zero_count": sum(value == 0 for value in differences),
        "positive_count": sum(value > 0 for value in differences),
        "target_unique_minimum_count": sum(value < 0 for value in differences),
        "target_tied_minimum_count": sum(value == 0 for value in differences),
    }


def pairwise_common(
    rows: list[dict[str, Any]], covered: dict[int, set[int]]
) -> dict[str, Any]:
    by_hk = {(row["h"], row["k"]): row for row in rows}
    comparisons: list[dict[str, Any]] = []
    for control_h in (-720, -360, 360, 720):
        indices = set(range(ACTIVE)) - (covered[0] | covered[control_h])
        per_k: list[dict[str, int]] = []
        for k in range(K_LOW, K_HIGH + 1):
            target = restricted_count(by_hk[(0, k)], indices)
            control = restricted_count(by_hk[(control_h, k)], indices)
            per_k.append(
                {
                    "k": k,
                    "target_restricted_T": target,
                    "control_restricted_T": control,
                    "target_minus_control": target - control,
                }
            )
        target_values = [item["target_restricted_T"] for item in per_k]
        control_values = [item["control_restricted_T"] for item in per_k]
        keep = [index for index, item in enumerate(per_k) if item["k"] != 0]
        comparisons.append(
            {
                "control_h": control_h,
                "common_uncovered_pair_count": len(indices),
                "common_uncovered_pair_indices": sorted(indices),
                "including_anchor_k0": paired_summary(target_values, control_values),
                "leave_anchor_out": paired_summary(
                    [target_values[index] for index in keep],
                    [control_values[index] for index in keep],
                ),
                "per_k": per_k,
            }
        )
    return {
        "schema": "a303656-k4-pairwise-common-uncovered-v1",
        "classification": "EXACT FINITE COMPUTATION ON THE FIXED 1285-POINT PANEL",
        "definition": "I_h = E \\ (C_0 union C_h)",
        "comparisons": comparisons,
    }


def five_way_common(rows: list[dict[str, Any]], covered: dict[int, set[int]]) -> dict[str, Any]:
    union = set().union(*(covered[h] for h in H_VALUES))
    indices = set(range(ACTIVE)) - union
    classes: list[dict[str, Any]] = []
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        per_k = [{"k": row["k"], "restricted_T": restricted_count(row, indices)} for row in class_rows]
        values = [item["restricted_T"] for item in per_k]
        summary = population_summary(values)
        minimum = min(values)
        summary["argmin_k"] = [item["k"] for item in per_k if item["restricted_T"] == minimum]
        record: dict[str, Any] = {"h": h, "summary_all_k": summary, "per_k": per_k}
        if h == 0:
            leave = [item["restricted_T"] for item in per_k if item["k"] != 0]
            leave_summary = population_summary(leave)
            leave_min = min(leave)
            leave_summary["argmin_k"] = [item["k"] for item in per_k if item["k"] != 0 and item["restricted_T"] == leave_min]
            record["summary_leave_anchor_out"] = leave_summary
        classes.append(record)
    return {
        "schema": "a303656-k4-five-way-common-uncovered-v1",
        "classification": "EXACT FINITE COMPUTATION ON THE FIXED 1285-POINT PANEL",
        "definition": "I_all = E \\ union_h C_h",
        "common_uncovered_pair_count": len(indices),
        "common_uncovered_pair_indices": sorted(indices),
        "fixed_count_thresholds_declared_in_source_before_results": list(FIVE_WAY_FIXED_COUNT_THRESHOLDS),
        "classes": classes,
    }


def hard_survivors(
    pairs: list[dict[str, Any]],
    table: dict[int, dict[int, dict[str, Any]]],
    covered: dict[int, set[int]],
    i_all: set[int],
) -> dict[str, Any]:
    records: list[dict[str, Any]] = []
    target_domain = [index for index in range(ACTIVE) if index not in covered[0]]
    for index in target_domain:
        pair = pairs[index]
        target_count = table[0][index]["count"]
        controls: dict[str, Any] = {}
        for h in (-720, -360, 360, 720):
            count = table[h][index]["count"]
            controls[str(h)] = {
                "persistent_covered": index in covered[h],
                "survival_count": count,
                "survival_frequency": exact_fraction(Fraction(count, 257)),
                "status": "PERSISTENT_COVERED" if index in covered[h] else (
                    "NEVER_WINS" if count == 0 else "VERY_FREQUENT_WIN" if count * 2 >= 257 else
                    "FREQUENT_WIN" if count * 4 >= 257 else "SOMETIMES_WIN"
                ),
            }
        records.append(
            {
                "pair_index": index,
                "c": pair["c"],
                "d": pair["d"],
                "shift": pair["shift"],
                "survival_count": target_count,
                "survival_frequency": exact_fraction(Fraction(target_count, 257)),
                "belongs_to_I_all": index in i_all,
                "classifications": {
                    "NEVER_WIN_TARGET": target_count == 0,
                    "SOMETIMES_WIN_TARGET": target_count > 0,
                    "FREQUENT_WIN_TARGET": target_count * 4 >= 257,
                    "VERY_FREQUENT_WIN_TARGET": target_count * 2 >= 257,
                },
                "control_status": controls,
                "P4_residue_vector_shift_mod_p_squared": {
                    str(prime): pair["shift"] % (prime * prime) for prime in P4
                },
            }
        )
    sets = {
        "NEVER_WIN_TARGET": [item["pair_index"] for item in records if item["classifications"]["NEVER_WIN_TARGET"]],
        "SOMETIMES_WIN_TARGET": [item["pair_index"] for item in records if item["classifications"]["SOMETIMES_WIN_TARGET"]],
        "FREQUENT_WIN_TARGET": [item["pair_index"] for item in records if item["classifications"]["FREQUENT_WIN_TARGET"]],
        "VERY_FREQUENT_WIN_TARGET": [item["pair_index"] for item in records if item["classifications"]["VERY_FREQUENT_WIN_TARGET"]],
    }
    return {
        "schema": "a303656-k4-hard-survivor-pairs-v1",
        "classification": "FINITE EMPIRICAL CLASSIFICATIONS ON THE FIXED TARGET PANEL ONLY",
        "target_uncovered_pair_count": len(target_domain),
        "set_counts": {name: len(indices) for name, indices in sets.items()},
        "sets_by_pair_index": sets,
        "pairs": records,
    }


def write_cross_profiles(
    path: Path,
    pairs: list[dict[str, Any]],
    table: dict[int, dict[int, dict[str, Any]]],
    covered: dict[int, set[int]],
) -> None:
    profiles: list[dict[str, Any]] = []
    for pair in pairs:
        index = pair["pair_index"]
        target = table[0][index]["count"]
        controls = [table[h][index]["count"] for h in (-720, -360, 360, 720)]
        excess = Fraction(target, 257) - Fraction(sum(controls), 4 * 257)
        record: dict[str, Any] = {
            "pair_index": index,
            "c": pair["c"],
            "d": pair["d"],
            "shift": pair["shift"],
            "target_survival_count": target,
            "target_survival_frequency": decimal_fraction(Fraction(target, 257)),
        }
        for h in H_VALUES:
            record[f"h_{h}_persistent_covered"] = int(index in covered[h])
            record[f"h_{h}_survival_count"] = table[h][index]["count"]
            record[f"h_{h}_survival_frequency"] = decimal_fraction(Fraction(table[h][index]["count"], 257))
        record.update(
            {
                "mean_control_frequency_numerator": sum(controls),
                "mean_control_frequency_denominator": 4 * 257,
                "mean_control_frequency_decimal": decimal_fraction(Fraction(sum(controls), 4 * 257)),
                "target_minus_mean_control_frequency_numerator": excess.numerator,
                "target_minus_mean_control_frequency_denominator": excess.denominator,
                "target_minus_mean_control_frequency_decimal": decimal_fraction(excess),
            }
        )
        profiles.append(record)
    target_order = sorted(profiles, key=lambda item: (-item["target_survival_count"], item["pair_index"]))
    excess_order = sorted(
        profiles,
        key=lambda item: (
            -Fraction(item["target_minus_mean_control_frequency_numerator"], item["target_minus_mean_control_frequency_denominator"]),
            item["pair_index"],
        ),
    )
    deficit_order = sorted(
        profiles,
        key=lambda item: (
            Fraction(item["target_minus_mean_control_frequency_numerator"], item["target_minus_mean_control_frequency_denominator"]),
            item["pair_index"],
        ),
    )
    for rank, item in enumerate(target_order, start=1):
        item["rank_target_survival_frequency"] = rank
    for rank, item in enumerate(excess_order, start=1):
        item["rank_target_excess_above_control_mean"] = rank
    for rank, item in enumerate(deficit_order, start=1):
        item["rank_target_deficit_below_control_mean"] = rank
    fields = ["pair_index", "c", "d", "shift", "target_survival_count", "target_survival_frequency"]
    for h in H_VALUES:
        fields.extend([f"h_{h}_persistent_covered", f"h_{h}_survival_count", f"h_{h}_survival_frequency"])
    fields.extend(
        [
            "mean_control_frequency_numerator", "mean_control_frequency_denominator", "mean_control_frequency_decimal",
            "target_minus_mean_control_frequency_numerator", "target_minus_mean_control_frequency_denominator",
            "target_minus_mean_control_frequency_decimal", "rank_target_survival_frequency",
            "rank_target_excess_above_control_mean", "rank_target_deficit_below_control_mean",
        ]
    )
    atomic_csv(path, fields, profiles)


def direct_selection(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    reasons: dict[int, set[str]] = {}
    for row in rows:
        if row["h"] == 0 and row["k"] == 0:
            reasons.setdefault(row["n"], set()).add("anchor_n0")
        if row["k"] in FIXED_DIRECT_K:
            reasons.setdefault(row["n"], set()).add("fixed_k")
        if row["T"] <= 25:
            reasons.setdefault(row["n"], set()).add("T_le_25")
    for h in H_VALUES:
        class_rows = [row for row in rows if row["h"] == h]
        minimum = min(row["T"] for row in class_rows)
        for row in class_rows:
            if row["T"] == minimum:
                reasons.setdefault(row["n"], set()).add("class_argmin")
    selected = [row for row in rows if row["n"] in reasons]
    require(len(selected) == 73, f"direct selection count {len(selected)} != 73")
    return selected


def write_direct_panel(path: Path, rows: list[dict[str, Any]]) -> None:
    atomic_csv(
        path,
        ["h", "k", "n", "active_pairs", "expected_T"],
        [
            {"h": row["h"], "k": row["k"], "n": row["n"], "active_pairs": ACTIVE, "expected_T": row["T"]}
            for row in rows
        ],
    )


def verify_direct_oracle(
    raw_path: Path,
    committed_path: Path,
    selected: list[dict[str, Any]],
    pairs: list[dict[str, Any]],
) -> dict[str, Any]:
    raw = load_json(raw_path)
    committed = load_json(committed_path)
    require(raw.get("schema") == "a303656-k4-ap-direct-verification-v1" and
            raw.get("implementation_id") == "k4_ap_direct_oracle_v1", "direct oracle schema/identity mismatch")
    raw_points = raw.get("points")
    committed_points = committed.get("points")
    require(isinstance(raw_points, list) and isinstance(committed_points, list) and
            len(raw_points) == len(committed_points) == len(selected), "direct oracle point count mismatch")
    witness_count = 0
    for raw_point, old_point, expected in zip(raw_points, committed_points, selected):
        for key in ("h", "k", "n", "active_pair_count", "expected_T", "T", "expected_T_match", "winning_exponent_pairs"):
            require(raw_point.get(key) == old_point.get(key), f"fresh direct result differs from committed point field {key}")
        require((raw_point["h"], raw_point["k"], raw_point["n"], raw_point["T"]) ==
                (expected["h"], expected["k"], expected["n"], expected["T"]), "direct point identity/T mismatch")
        winners = raw_point["winning_exponent_pairs"]
        mask_pairs = {(pairs[index]["c"], pairs[index]["d"]) for index in range(ACTIVE) if bit(expected["mask"], index)}
        winner_pairs: set[tuple[int, int]] = set()
        for winner in winners:
            c, d = winner["c"], winner["d"]
            require((c, d) not in winner_pairs, "direct oracle duplicated a winner")
            winner_pairs.add((c, d))
            shift = pow(3, c) + pow(5, d)
            remainder = expected["n"] - shift
            require(winner["shift"] == shift and winner["remainder"] == remainder, "direct shift/remainder mismatch")
            a, b = winner["a"], winner["b"]
            require(isinstance(a, int) and isinstance(b, int) and 0 <= a <= b, "direct witness canonicality mismatch")
            require(a * a + b * b == remainder, "direct witness equation mismatch")
            witness_count += 1
        require(winner_pairs == mask_pairs and len(winners) == expected["T"], "direct complete winner list differs from masks")
    return {
        "selected_point_count": len(selected),
        "complete_winner_sets_match_backend_a": True,
        "complete_winner_sets_match_backend_b": True,
        "independently_rechecked_witness_count": witness_count,
        "all_witness_equations_valid": True,
        "fresh_oracle_matches_committed_direct_artifact": True,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--work-dir", type=Path, required=True)
    parser.add_argument("--artifact-dir", type=Path, required=True)
    parser.add_argument("--source-commit", required=True)
    return parser.parse_args()


def main() -> int:
    started = time.monotonic()
    try:
        args = parse_args()
        root = args.source_root.resolve()
        work = args.work_dir.resolve()
        artifact = args.artifact_dir.resolve()
        require(root.is_dir(), "source root does not exist")
        require(not artifact.exists() or not any(artifact.iterdir()), "artifact directory must be absent or empty")
        artifact.mkdir(parents=True, exist_ok=True)
        work.mkdir(parents=True, exist_ok=True)
        logs = work / "logs"

        chain = validate_source_chain(root, args.source_commit)
        protected_before = verify_protected_inputs(root)
        panel = fixed_panel()
        prior_rows = read_prior_counts(root, panel)
        pairs = canonical_pairs()
        pair_hash = write_pair_order(artifact / "pair_order.csv", pairs)
        panel_path = work / "fixed_panel.csv"
        write_panel(panel_path, panel)

        binaries, command_records = build_tools(root, work, logs)
        backend_specs = [
            ("backend_a", root / "src/k4_survivor_backend_a.py", binaries["backend_a_core"]),
            ("backend_b", root / "src/k4_survivor_backend_b.py", binaries["backend_b_core"]),
        ]
        for label, wrapper, core in backend_specs:
            backend_work = work / label
            report = work / f"{label}_run_report.json"
            command = [
                sys.executable,
                str(wrapper),
                "--core",
                str(core),
                "--input",
                str(panel_path),
                "--pair-order",
                str(artifact / "pair_order.csv"),
                "--pair-order-sha256",
                pair_hash,
                "--output",
                str(artifact / f"{label}_masks.bin"),
                "--work-dir",
                str(backend_work),
                "--run-report",
                str(report),
            ]
            command_records.append(run_logged(command, root, logs, label))

        a_rows = read_mask_file(artifact / "backend_a_masks.bin", pair_hash, panel)
        b_rows = read_mask_file(artifact / "backend_b_masks.bin", pair_hash, panel)
        require(a_rows == b_rows, "backend masks differ pointwise")
        for fresh, prior in zip(a_rows, prior_rows):
            require((fresh["h"], fresh["k"], fresh["n"], fresh["active_pairs"], fresh["T"]) ==
                    (prior["h"], prior["k"], prior["n"], prior["active_pairs"], prior["T"]),
                    "fresh mask row differs from committed K4 point/T")

        selected = direct_selection(a_rows)
        direct_panel_path = work / "direct_panel.csv"
        direct_raw_path = work / "direct_verification_raw.json"
        write_direct_panel(direct_panel_path, selected)
        direct_command = [str(binaries["direct_oracle"]), "--input", str(direct_panel_path), "--output", str(direct_raw_path)]
        command_records.append(run_logged(direct_command, root, logs, "direct_oracle"))
        direct_result = verify_direct_oracle(
            direct_raw_path,
            root / "analysis/k4_ap_pilot/direct_verification.json",
            selected,
            pairs,
        )

        covered = persistent_sets(root, pairs, a_rows)
        survival = survival_count_table(a_rows, covered)
        write_class_frequencies(artifact / "class_pair_frequencies.csv", pairs, survival, covered)
        pairwise = pairwise_common(a_rows, covered)
        atomic_json(artifact / "pairwise_common_uncovered.json", pairwise)
        five_way = five_way_common(a_rows, covered)
        atomic_json(artifact / "five_way_common_uncovered.json", five_way)
        i_all = set(five_way["common_uncovered_pair_indices"])
        hard = hard_survivors(pairs, survival, covered, i_all)
        atomic_json(artifact / "hard_survivor_pairs.json", hard)
        write_cross_profiles(artifact / "cross_class_pair_profiles.csv", pairs, survival, covered)

        protected_after = verify_protected_inputs(root)
        require(protected_before == protected_after, "protected baseline changed during run")
        source_paths = [
            "src/k4_survivor_backend_a.py",
            "src/k4_survivor_backend_b.py",
            "src/k4_survivor_run.py",
            "src/k4_survivor_verify.py",
            "tests/k4_survivor_tests.py",
            "src/k4_ap_backend_a.cpp",
            "src/k4_ap_backend_b.cpp",
            "src/k4_ap_direct_oracle.cpp",
        ]
        source_hashes: dict[str, str] = {}
        for relative in source_paths:
            path = root / relative
            require(path.is_file(), f"source file missing: {relative}")
            digest = sha256_file(path)
            committed = git(root, "show", f"{args.source_commit}:{relative}").stdout
            require(sha256_bytes(committed) == digest, f"source differs from source commit: {relative}")
            source_hashes[relative] = digest

        mask_hashes = {
            "backend_a_masks.bin": sha256_file(artifact / "backend_a_masks.bin"),
            "backend_b_masks.bin": sha256_file(artifact / "backend_b_masks.bin"),
        }
        require(mask_hashes["backend_a_masks.bin"] == mask_hashes["backend_b_masks.bin"], "mask binaries are not byte-identical")
        identities = {
            "backend_a": {
                "wrapper_implementation_id": "k4_survivor_backend_a_mask_wrapper_v1",
                "wrapper_source": "src/k4_survivor_backend_a.py",
                "core_implementation_id": "k4_ap_backend_a_trial_division_v1",
                "core_source": "src/k4_ap_backend_a.cpp",
                "core_algorithm": "generated prime table, deterministic uint64 trial division, Fermat two-square classification",
                "core_binary_sha256": sha256_file(binaries["backend_a_core"]),
                "mask_sha256": mask_hashes["backend_a_masks.bin"],
            },
            "backend_b": {
                "wrapper_implementation_id": "k4_survivor_backend_b_mask_wrapper_v1",
                "wrapper_source": "src/k4_survivor_backend_b.py",
                "core_implementation_id": "k4_ap_backend_b_cpp17_mr7_brent_rho_v1",
                "core_source": "src/k4_ap_backend_b.cpp",
                "core_algorithm": "deterministic uint64 Miller-Rabin and deterministic-seeded Brent Pollard-Rho, independent Fermat classification",
                "core_binary_sha256": sha256_file(binaries["backend_b_core"]),
                "mask_sha256": mask_hashes["backend_b_masks.bin"],
            },
            "direct_oracle": {
                "implementation_id": "k4_ap_direct_oracle_v1",
                "source": "src/k4_ap_direct_oracle.cpp",
                "algorithm": "factorization-free monotone two-square boundary enumeration with canonical least-a witnesses",
                "binary_sha256": sha256_file(binaries["direct_oracle"]),
            },
        }
        manifest = {
            "schema": "a303656-k4-survivor-mask-manifest-v1",
            "source_commit": args.source_commit,
            "baseline_commit": BASELINE_COMMIT,
            "pair_order_sha256": pair_hash,
            "row_count": len(panel),
            "pair_count": ACTIVE,
            "binary_format": {
                "endianness": "little",
                "magic_ascii": MAGIC.decode("ascii"),
                "version": 1,
                "header_bytes": HEADER.size,
                "row_bytes": ROW.size + MASK_BYTES,
                "mask_bytes": MASK_BYTES,
                "bit_rule": "bit i is byte[i//8] bit (i%8), least-significant-bit first",
                "unused_bits_rule": "bit 7 of the final mask byte must be zero",
                "header_layout": "8-byte magic; uint32 version,header_bytes,row_count,pair_count,mask_bytes,row_bytes; raw 32-byte pair-order SHA256",
                "row_layout": "uint64 n; int64 h; int64 k; uint32 active_pair_count; uint32 T; 51 mask bytes",
                "exact_file_size_bytes": HEADER.size + len(panel) * (ROW.size + MASK_BYTES),
                "failure_policy": "reject truncation, extra bytes, wrong sizes/counts/order/hash, nonzero unused bit, or popcount/T mismatch",
            },
            "backends": identities,
            "mask_files": mask_hashes,
            "full_pointwise_mask_equality": True,
            "popcount_equals_T_all_rows": True,
        }
        atomic_json(artifact / "mask_manifest.json", manifest)

        class_summaries = [residual_summary(h, survival, covered) for h in H_VALUES]
        target_leave = residual_summary(0, survival, covered, leave_anchor_out=True)
        summary_names = [
            "pair_order.csv",
            "backend_a_masks.bin",
            "backend_b_masks.bin",
            "mask_manifest.json",
            "class_pair_frequencies.csv",
            "pairwise_common_uncovered.json",
            "five_way_common_uncovered.json",
            "hard_survivor_pairs.json",
            "cross_class_pair_profiles.csv",
        ]
        metadata = {
            "schema": "a303656-k4-survivor-incidence-metadata-v1",
            "task": "K4 SURVIVOR-INCIDENCE AND COVERAGE-ADJUSTED AUDIT",
            "classification": "EXACT FINITE COMPUTATION ON THE ALREADY VALIDATED 1285-POINT K4 PANEL; GLOBAL PROBLEM UNRESOLVED",
            **chain,
            "results_commit": RESULTS_SENTINEL,
            "panel": {
                "formula": "n = 240000005594 + h + k*28227969",
                "h_values": list(H_VALUES),
                "k_interval": [K_LOW, K_HIGH],
                "point_count": len(panel),
                "unique_integer_count": len({row["n"] for row in panel}),
                "minimum_n": min(row["n"] for row in panel),
                "maximum_n": max(row["n"] for row in panel),
                "active_pair_count": ACTIVE,
                "activation_cell": list(CELL),
                "panel_csv_sha256": sha256_bytes(panel_bytes(panel)),
                "verified_against_committed_K4_artifacts": True,
            },
            "p4": list(P4),
            "m4": M4,
            "pair_order_sha256": pair_hash,
            "backend_identities": identities,
            "full_mask_equality": {"status": "PASS", "point_count": 1285, "mismatch_count": 0, "byte_identical_files": True},
            "direct_oracle_verification": direct_result,
            "persistent_covered_sets": {
                str(h): {"covered_pair_count": len(covered[h]), "uncovered_pair_count": ACTIVE - len(covered[h]), "no_covered_pair_winner": True}
                for h in H_VALUES
            },
            "class_residual_survival_analysis": class_summaries,
            "target_leave_anchor_out_residual_survival_analysis": target_leave,
            "scope_guards": {
                "formal_points_evaluated_by_each_backend": 1285,
                "direct_oracle_points": 73,
                "other_integer_evaluations": 0,
                "adaptive_points_added": 0,
                "k_outside_fixed_interval_evaluated": False,
                "remaining_activation_cell_progression_scanned": False,
                "P4_M4_h_or_classes_changed": False,
                "CRT_optimization_performed": False,
            },
            "commands": command_records,
            "resource_use": {
                "runner_wall_seconds": format(time.monotonic() - started, ".6f"),
                "children_max_rss_kib": resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,
                "committed_raw_logs": False,
                "raw_logs_location_for_this_run": str(logs),
            },
            "protected_baseline_and_prior_pilot_hashes_before": protected_before,
            "protected_baseline_and_prior_pilot_hashes_after": protected_after,
            "tool_source_sha256": source_hashes,
            "artifact_sha256_excluding_metadata_and_verification_report": {
                name: sha256_file(artifact / name) for name in summary_names
            },
        }
        atomic_json(artifact / "metadata.json", metadata)
        require({path.name for path in artifact.iterdir() if path.is_file()} == REQUIRED_OUTPUTS,
                "runner output set is incomplete or contains extras")
        print("K4_SURVIVOR_RUN_PASS")
        print(f"pair_order_sha256={pair_hash}")
        print(f"mask_sha256={mask_hashes['backend_a_masks.bin']}")
        print(f"I_all_size={len(i_all)}")
        return 0
    except (AuditFailure, OSError, UnicodeError, csv.Error, json.JSONDecodeError) as exc:
        print(f"K4_SURVIVOR_RUN_FAIL: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
