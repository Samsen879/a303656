#!/usr/bin/env python3
"""Exact shared contracts for the fixed-P4 maximizer-class census.

This module constructs only the predeclared 87 CRT classes.  It contains no
two-square classifier and never evaluates T(n).
"""

from __future__ import annotations

import csv
import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator


TASK = "EXACT T3=2 FIXED-P4 MAXIMIZER-CLASS CENSUS"
START_COMMIT = "ae75d96358f9803cfac2c7d6ce46dfec0344e6b7"
P4 = (3, 7, 11, 23)
SQUARE_MODULI = tuple(p * p for p in P4)
M4 = 28_227_969
N0 = 240_000_005_594
A = 183_968_950_234
B = 246_731_069_451
L = 1_129_118_760
PAIR_COUNT = 407
MASK_BYTES = 51
MAXIMIZER_COUNT = 84
CLASS_COUNT = 87
CONSTRAINED_G = 231
CONSTRAINED_ARGMAX_DIGEST = (
    "f83d2400cd684dbcc5027d82dcd0d053fdf64521a770b12231cdc259adade825"
)
PAIR_ORDER_SHA256 = "5f3b6ea52f9d3d5e544f10ae17a3752cbf1a476d9575a2e0a6ae4c502ed0452b"
PANEL_FIELDS = [
    "class_index", "class_id", "t3", "t7", "t11", "t23", "G",
    "uncovered_pairs", "crt_residue", "point_index", "n", "active_pairs",
]
COUNT_FIELDS = PANEL_FIELDS + ["T", "mask_offset", "mask_sha256"]

PROTECTED_HASHES = {
    "README.md": "9c1f11b8ba76e0d0ff70d3d0dc5f8b1b528e1e31405b27be9b047bdcc3916a8b",
    "REPORT_zh.md": "833e66fd88c27412e2522448f17075baf4e85828080c22ca2e87a12f30f77649",
    "output/formal_results_audit.json": "fe87b53734fe9f8978396428769af5db76fb35709276241f36c49c2a9145b533",
    "output/final_packaging_audit.json": "de8f4d351b809b03daac280879eddc69a795fce50f9c8f6b2d786ad2f9d611ca",
    "output/final_results_manifest.json": "99bfcf78d4800aacaac4b9fb36cb52aa4a1f655394c6f79db8432b6ebcfd9360",
    "cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt": "510ac25107f8764fbacb3fe10f2c67de1a5cc595b20a23f793ff77dd54d5ec42",
    "analysis/p2_core/activation_cell.json": "54bdb35c8d9206d9014c6e23bc24ca4292e217e48244530cec472ad02cc0e644",
    "analysis/p2_core/metadata.json": "d1af86b53761364c955d0e4934beeb014fb1f5e8b4f2c4436c2acd61c8a4b4e4",
    "analysis/p2_core/n0_p2_core.json": "02535370741275c0cb416b9de7156a9f29c3fb9a82b4c524ca61f2476f2824fe",
    "analysis/p2_core/verification_report.json": "a5601eec079d196ecf7b9336990ca0cad971000430761807525df2941c74cb7a",
    "analysis/k4_ap_pilot/metadata.json": "edac79f1bb9932a05a145b6326dd143a44027fbf1e7b4e9ace5e060fc95d4b8a",
    "analysis/k4_ap_pilot/verification_report.json": "7f1c999893d890dcaca37aee6c6d300fc3b41bd8c9ee779c1d4cb28e1a992d1a",
    "analysis/k4_survivor_incidence/metadata.json": "8f6c3b203ab568f57f8c2178a140dc67d9ef4c422c76a96d8afc1b8a04ad0109",
    "analysis/k4_survivor_incidence/pair_order.csv": PAIR_ORDER_SHA256,
    "analysis/k4_survivor_incidence/verification_report.json": "d816f910701f344784048fcf8d8cd1737fda96d77eab5267b48643f251f32917",
    "analysis/p4_residue_landscape/coverage_comparison.json": "8b33268a8f4a89a6fb6fd7e5f624d637df87aa7e697ba02b88150a4f24b63068",
    "analysis/p4_residue_landscape/crt_candidates.json": "72cda319102f307590f4b8d3b3d6888a06077af0a11ae0b6753ecd2c06127dd5",
    "analysis/p4_residue_landscape/full_histogram.csv": "9c29fb639b1a42bf2ec9c15f2f1e43a54b044d224ba3bf6ffa2328292aa4216a",
    "analysis/p4_residue_landscape/local_landscape.json": "2da392aa8760c3e49855efe23b4fe4af4240abac99d80a929b355efe53817118",
    "analysis/p4_residue_landscape/maximizers.json": "7daa2c7b3d726e0f05b5b484fe5e4dffc0c22d57550a10c828241fa6b62e5a5a",
    "analysis/p4_residue_landscape/metadata.json": "00f6e27dc5ec2557ba7ac0223c872088c56e02167f9f703c7f4eb534d08ea217",
    "analysis/p4_residue_landscape/n0_rank.json": "78d84e544f8b0287d48f9508b4d1e140397e2fcfb4506b069d96a8b6b7b6cf53",
    "analysis/p4_residue_landscape/subset_optima.csv": "3353e5f2a4123d118fba8c8adad9b48f7f9f7a9e85b821a5cd90060fe3d47975",
    "analysis/p4_residue_landscape/t3eq2_histogram.csv": "d2d96b00abfcddbc6074c0bc51aafc63ac2cebcfdcff16505461a830f8fd60ef",
    "analysis/p4_residue_landscape/verification_report.json": "96ac947a17445ca65e18690ee4e370f24b1b8d3b7bdf1e33a1ad1663f1b1b372",
}
class CensusError(RuntimeError):
    pass


@dataclass(frozen=True)
class Pair:
    index: int
    c: int
    d: int
    shift: int


@dataclass(frozen=True)
class ClassSpec:
    index: int
    class_id: str
    tuple4: tuple[int, int, int, int]
    coverage: int
    residue: int
    covered: frozenset[int]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_json(value: object) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load_json(path: Path) -> object:
    with path.open(encoding="utf-8") as stream:
        return json.load(stream)


def verify_protected(root: Path) -> dict[str, str]:
    observed: dict[str, str] = {}
    for relative, expected in PROTECTED_HASHES.items():
        path = root / relative
        if not path.is_file():
            raise CensusError(f"protected input missing: {relative}")
        actual = sha256_file(path)
        if actual != expected:
            raise CensusError(f"protected input hash mismatch: {relative}: {actual} != {expected}")
        observed[relative] = actual
    return observed


def powers(base: int, limit: int) -> Iterator[tuple[int, int]]:
    exponent, value = 0, 1
    while value <= limit:
        yield exponent, value
        if value > limit // base:
            break
        exponent += 1
        value *= base


def active_pairs(n: int) -> list[Pair]:
    raw = [
        (c, d, p3 + p5)
        for c, p3 in powers(3, n)
        for d, p5 in powers(5, n)
        if p3 + p5 <= n
    ]
    return [Pair(index, c, d, shift) for index, (c, d, shift) in enumerate(raw)]


def canonical_pairs(root: Path | None = None) -> list[Pair]:
    low = active_pairs(A)
    high = active_pairs(B)
    if low != high or len(low) != PAIR_COUNT:
        raise CensusError("activation cell does not have the exact constant 407-pair domain")
    duplicate_28 = [(pair.c, pair.d) for pair in low if pair.shift == 28]
    if duplicate_28 != [(1, 2), (3, 0)]:
        raise CensusError("duplicate shift 28 was not preserved as two exponent pairs")
    if root is not None:
        table = root / "analysis/k4_survivor_incidence/pair_order.csv"
        if sha256_file(table) != PAIR_ORDER_SHA256:
            raise CensusError("committed pair-order digest mismatch")
        with table.open(newline="", encoding="utf-8") as stream:
            rows = list(csv.DictReader(stream))
        observed = [(int(row["pair_index"]), int(row["c"]), int(row["d"]), int(row["shift"])) for row in rows]
        expected = [(pair.index, pair.c, pair.d, pair.shift) for pair in low]
        if observed != expected:
            raise CensusError("committed pair-order table differs from exact activation-cell domain")
    return low


def coverage_set(tuple4: tuple[int, int, int, int], pairs: list[Pair]) -> frozenset[int]:
    covered: set[int] = set()
    for p, residue in zip(P4, tuple4):
        modulus = p * p
        if not 0 <= residue < modulus:
            raise CensusError(f"tuple residue {residue} outside [0,{modulus})")
        for pair in pairs:
            difference = residue - pair.shift
            if difference % p == 0 and difference % modulus != 0:
                covered.add(pair.index)
    return frozenset(covered)


def crt(residues: Iterable[int], moduli: Iterable[int]) -> tuple[int, int]:
    x, modulus = 0, 1
    for residue, next_modulus in zip(residues, moduli):
        if next_modulus <= 1 or modulus % next_modulus == 0:
            raise CensusError("invalid CRT modulus")
        delta = ((residue - x) * pow(modulus, -1, next_modulus)) % next_modulus
        x += modulus * delta
        modulus *= next_modulus
        x %= modulus
    return x, modulus


def tuple_residue_mod_l(tuple4: tuple[int, int, int, int]) -> int:
    mod_m4, modulus = crt(tuple4, SQUARE_MODULI)
    if modulus != M4:
        raise CensusError("P4 square-modulus product mismatch")
    result, combined = crt((mod_m4, N0 % 40), (M4, 40))
    if combined != L:
        raise CensusError("combined CRT modulus mismatch")
    for residue, mod in zip(tuple4, SQUARE_MODULI):
        if result % mod != residue:
            raise CensusError("CRT reconstruction failure")
    if result % 40 != N0 % 40:
        raise CensusError("CRT modulo-40 reconstruction failure")
    return result


def _argmax_digest(tuples: list[tuple[int, int, int, int]]) -> str:
    digest = hashlib.sha256()
    for tuple4 in tuples:
        digest.update(struct.pack("<4H", *tuple4))
    return digest.hexdigest()


def load_classes(root: Path) -> tuple[list[ClassSpec], list[Pair]]:
    pairs = canonical_pairs(root)
    landscape_meta = load_json(root / "analysis/p4_residue_landscape/metadata.json")
    if not isinstance(landscape_meta, dict):
        raise CensusError("landscape metadata is not an object")
    required = {
        "P4": list(P4), "M4": M4, "L": L,
        "t3eq2_stream_digest": "fd409acfc3f35aa8e333d654a94f5d06c3093f6c5ffd3207adadfe64ed12310c",
    }
    for key, value in required.items():
        if landscape_meta.get(key) != value:
            raise CensusError(f"landscape metadata mismatch for {key}")
    domain = landscape_meta.get("domain")
    if not isinstance(domain, dict) or domain.get("activation_cell") != [A, B] or domain.get("pair_count") != PAIR_COUNT:
        raise CensusError("landscape activation-domain mismatch")

    maximizers = load_json(root / "analysis/p4_residue_landscape/maximizers.json")
    if not isinstance(maximizers, dict) or not isinstance(maximizers.get("t3eq2"), dict):
        raise CensusError("constrained argmax certificate is malformed")
    constrained = maximizers["t3eq2"]
    raw_tuples = constrained.get("first_100_argmax")
    if constrained.get("maximum") != CONSTRAINED_G or constrained.get("argmax_count") != MAXIMIZER_COUNT:
        raise CensusError("constrained maximum/count mismatch")
    if constrained.get("argmax_digest") != CONSTRAINED_ARGMAX_DIGEST:
        raise CensusError("declared constrained argmax digest mismatch")
    if not isinstance(raw_tuples, list) or len(raw_tuples) != MAXIMIZER_COUNT:
        raise CensusError("constrained certificate does not contain exactly all 84 tuples")
    tuples = [tuple(int(value) for value in row) for row in raw_tuples]
    if any(len(row) != 4 for row in tuples) or tuples != sorted(tuples) or len(set(tuples)) != MAXIMIZER_COUNT:
        raise CensusError("constrained argmax tuples are not distinct lexicographic 4-tuples")
    if any(row[0] != 2 for row in tuples):
        raise CensusError("constrained argmax tuple with t3 != 2")
    if _argmax_digest(tuples) != CONSTRAINED_ARGMAX_DIGEST:
        raise CensusError("independent constrained argmax digest mismatch")
    if any(len(coverage_set(row, pairs)) != CONSTRAINED_G for row in tuples):
        raise CensusError("constrained tuple does not independently cover exactly 231 pairs")

    local = load_json(root / "analysis/p4_residue_landscape/local_landscape.json")
    if not isinstance(local, dict):
        raise CensusError("local landscape is malformed")
    one = local.get("exactly_one_coordinate_changed", {})
    two = local.get("at_most_two_coordinates_changed", {})
    fixed = local.get("t3_fixed_2_other_coordinates_arbitrary", {})
    if one.get("maximum") != 227 or one.get("first_100_modifications", [{}])[0].get("tuple") != [2, 41, 50, 504]:
        raise CensusError("CAL-227 is not the committed lexicographically first one-coordinate maximizer")
    if two.get("maximum") != 230 or two.get("first_100_modifications", [{}])[0].get("tuple") != [2, 7, 32, 504]:
        raise CensusError("CAL-230 is not the committed lexicographically first at-most-two-coordinate maximizer")
    if fixed.get("maximum") != 231 or fixed.get("first_100_modifications", [{}])[0].get("tuple") != [2, 7, 50, 17]:
        raise CensusError("committed constrained-max calibration cross-check failed")
    if tuple(local.get("n0_tuple", [])) != (2, 41, 74, 504) or local.get("n0_coverage") != 216:
        raise CensusError("committed N0 tuple/coverage mismatch")

    raw_specs = [
        ("CAL-216", (2, 41, 74, 504), 216),
        ("CAL-227", (2, 41, 50, 504), 227),
        ("CAL-230", (2, 7, 32, 504), 230),
    ] + [(f"MAX-{index + 1:03d}", tuple4, 231) for index, tuple4 in enumerate(tuples)]
    if (2, 7, 50, 17) not in tuples:
        raise CensusError("required constrained maximizer is absent")
    if len({tuple4 for _, tuple4, _ in raw_specs}) != CLASS_COUNT:
        raise CensusError("formal class tuple duplication")
    specs: list[ClassSpec] = []
    for index, (class_id, tuple4, declared) in enumerate(raw_specs):
        covered = coverage_set(tuple4, pairs)
        if len(covered) != declared:
            raise CensusError(f"declared coverage mismatch for {class_id}")
        specs.append(ClassSpec(index, class_id, tuple4, declared, tuple_residue_mod_l(tuple4), covered))
    if len({spec.residue for spec in specs}) != CLASS_COUNT:
        raise CensusError("CRT classes are not distinct modulo L")
    return specs, pairs


def class_points(spec: ClassSpec) -> list[int]:
    first = A + ((spec.residue - A) % L)
    return list(range(first, B + 1, L))


def construct_panel(root: Path) -> tuple[list[dict[str, int | str]], list[ClassSpec], list[Pair]]:
    specs, pairs = load_classes(root)
    rows: list[dict[str, int | str]] = []
    seen: set[int] = set()
    interval_length = B - A + 1
    floor_count, remainder = divmod(interval_length, L)
    allowed_counts = {floor_count, floor_count + (1 if remainder else 0)}
    for spec in specs:
        points = class_points(spec)
        if len(points) not in allowed_counts:
            raise CensusError(f"class {spec.class_id} has invalid member count")
        for point_index, n in enumerate(points):
            if not A <= n <= B or n % L != spec.residue:
                raise CensusError("panel point outside its exact class/cell")
            if n % 40 != N0 % 40:
                raise CensusError("panel point violates common modulo-40 condition")
            if n in seen:
                raise CensusError("integer duplicated between formal classes")
            seen.add(n)
            if len(active_pairs(n)) != PAIR_COUNT:
                raise CensusError("panel point active-pair count is not 407")
            t3, t7, t11, t23 = spec.tuple4
            rows.append({
                "class_index": spec.index, "class_id": spec.class_id,
                "t3": t3, "t7": t7, "t11": t11, "t23": t23,
                "G": spec.coverage, "uncovered_pairs": PAIR_COUNT - spec.coverage,
                "crt_residue": spec.residue, "point_index": point_index,
                "n": n, "active_pairs": PAIR_COUNT,
            })
    if len({row["n"] for row in rows}) != len(rows):
        raise CensusError("formal panel contains duplicated integers")
    return rows, specs, pairs


def write_panel(path: Path, rows: list[dict[str, int | str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=PANEL_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def read_panel(path: Path, root: Path) -> list[dict[str, int | str]]:
    expected, _, _ = construct_panel(root)
    with path.open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if reader.fieldnames != PANEL_FIELDS:
            raise CensusError("class-panel header mismatch")
        raw = list(reader)
    if len(raw) != len(expected):
        raise CensusError("missing or extra formal panel point")
    parsed: list[dict[str, int | str]] = []
    for line_number, (row, wanted) in enumerate(zip(raw, expected), start=2):
        if set(row) != set(PANEL_FIELDS) or None in row:
            raise CensusError(f"class-panel schema mismatch at line {line_number}")
        item: dict[str, int | str] = {"class_id": row["class_id"]}
        for field in PANEL_FIELDS:
            if field != "class_id":
                try:
                    item[field] = int(row[field])
                except ValueError as exc:
                    raise CensusError(f"non-integer {field} at line {line_number}") from exc
        if item != wanted:
            raise CensusError(f"changed class ordering or panel value at line {line_number}")
        parsed.append(item)
    return parsed


def panel_digest(path: Path) -> str:
    return sha256_file(path)


def mask_popcount(mask: bytes) -> int:
    # 407 bits occupy 50 full bytes plus bits 0..6 of the final byte.
    if len(mask) != MASK_BYTES or mask[-1] & 0x80:
        raise CensusError("packed mask width/tail-bit invariant failed")
    return sum(byte.bit_count() for byte in mask)
