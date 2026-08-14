#!/usr/bin/env python3
"""Independent verifier for the exact fixed-P4 residue landscape.

This module intentionally does not import either enumerator or any earlier
P2-core coverage helper.  It uses exact Python integers throughout.  It does
not evaluate the original representation-count function.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import struct
import sys
from collections import Counter
from pathlib import Path
from typing import Any, Callable, Iterable, Mapping, Sequence


CELL_LOW = 183_968_950_234
CELL_HIGH = 246_731_069_451
N0 = 240_000_005_594
N0_TUPLE = (2, 41, 74, 504)
N0_COVERAGE = 216
P4 = (3, 7, 11, 23)
MODULI = (9, 49, 121, 529)
M4 = 28_227_969
FULL_TUPLE_COUNT = M4
T3EQ2_TUPLE_COUNT = 49 * 121 * 529
L_CONSTRAINED = 40 * M4
FULL_ROW = struct.Struct("<5H")
ARGMAX_ROW = struct.Struct("<4H")


class VerificationError(ValueError):
    """Raised for any certificate, artifact, or stream inconsistency."""


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def _as_int(value: Any, label: str) -> int:
    if isinstance(value, bool):
        raise VerificationError(f"{label} must be an integer, not bool")
    try:
        result = int(value)
    except (TypeError, ValueError) as exc:
        raise VerificationError(f"{label} is not an integer: {value!r}") from exc
    if isinstance(value, float) and not value.is_integer():
        raise VerificationError(f"{label} is not an exact integer: {value!r}")
    return result


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def generate_domain() -> list[tuple[int, int, int]]:
    """Regenerate the activation-cell domain in lexicographic (c,d) order."""
    powers3: list[int] = []
    value = 1
    while value + 1 <= CELL_LOW:
        powers3.append(value)
        value *= 3
    powers5: list[int] = []
    value = 1
    while value + 1 <= CELL_LOW:
        powers5.append(value)
        value *= 5

    pairs: list[tuple[int, int, int]] = []
    for c, power3 in enumerate(powers3):
        for d, power5 in enumerate(powers5):
            shift = power3 + power5
            if shift > CELL_LOW:
                break
            pairs.append((c, d, shift))

    _require(len(pairs) == 407, f"domain has {len(pairs)} pairs, expected 407")
    _require(pairs == sorted(pairs), "domain is not in lexicographic (c,d) order")
    duplicates: dict[int, list[tuple[int, int]]] = {}
    for c, d, shift in pairs:
        duplicates.setdefault(shift, []).append((c, d))
    duplicate_rows = {s: ps for s, ps in duplicates.items() if len(ps) > 1}
    _require(
        duplicate_rows == {28: [(1, 2), (3, 0)]},
        f"unexpected duplicate shifts: {duplicate_rows}",
    )

    # Establish that this exact set is constant on the closed activation cell.
    next_shift: int | None = None
    for c, power3 in enumerate(powers3 + [powers3[-1] * 3]):
        value5 = 1
        d = 0
        while True:
            shift = power3 + value5
            if shift > CELL_LOW and (next_shift is None or shift < next_shift):
                next_shift = shift
            if shift > CELL_HIGH and value5 > CELL_HIGH:
                break
            if value5 > CELL_HIGH:
                break
            value5 *= 5
            d += 1
    _require(next_shift == CELL_HIGH + 1, f"next activation is {next_shift}")
    return pairs


def domain_digest(domain: Sequence[tuple[int, int, int]]) -> str:
    h = hashlib.sha256()
    for c, d, _shift in domain:
        h.update(struct.pack("<HH", c, d))
    return h.hexdigest()


def p_adic_valuation(value: int, prime: int) -> int | None:
    """Return v_p(value); None denotes the infinite valuation of zero."""
    if value == 0:
        return None
    value = abs(value)
    valuation = 0
    while value % prime == 0:
        valuation += 1
        value //= prime
    return valuation


def valuation_exactly_one(value: int, prime: int) -> bool:
    if value == 0 or value % prime != 0:
        return False
    return (value // prime) % prime != 0


def build_coverage_masks(
    domain: Sequence[tuple[int, int, int]] | None = None,
) -> dict[int, tuple[int, ...]]:
    """Residue-centric exact-one construction, independent of A and B."""
    if domain is None:
        domain = generate_domain()
    result: dict[int, tuple[int, ...]] = {}
    for prime in P4:
        modulus = prime * prime
        masks: list[int] = []
        for residue in range(modulus):
            mask = 0
            for index, (_c, _d, shift) in enumerate(domain):
                if valuation_exactly_one(residue - shift, prime):
                    mask |= 1 << index
            masks.append(mask)
        result[prime] = tuple(masks)
    return result


def verify_coverage_semantics(
    domain: Sequence[tuple[int, int, int]],
    masks: Mapping[int, Sequence[int]],
) -> dict[str, Any]:
    """Cross-check every membership with a pair-centric modular construction."""
    valuation3_witness: dict[str, int] | None = None
    per_prime: dict[str, Any] = {}
    for prime in P4:
        modulus = prime * prime
        rows = masks[prime]
        _require(len(rows) == modulus, f"p={prime}: wrong coverage residue count")
        memberships = 0
        for index, (_c, _d, shift) in enumerate(domain):
            residue_mod_p = shift % prime
            excluded_lift = shift % modulus
            for residue in range(modulus):
                pair_centric = residue % prime == residue_mod_p and residue != excluded_lift
                residue_centric = bool((rows[residue] >> index) & 1)
                _require(
                    pair_centric == residue_centric,
                    f"coverage mismatch p={prime}, t={residue}, pair_index={index}",
                )
                if residue_centric:
                    memberships += 1
                if valuation3_witness is None:
                    valuation = p_adic_valuation(residue - shift, prime)
                    if valuation == 3:
                        _require(not residue_centric, "valuation-3 member was included")
                        valuation3_witness = {
                            "prime": prime,
                            "residue": residue,
                            "pair_index": index,
                        }
        expected = len(domain) * (prime - 1)
        _require(memberships == expected, f"p={prime}: {memberships} memberships != {expected}")
        h = hashlib.sha256()
        for residue, mask in enumerate(rows):
            indices = [i for i in range(len(domain)) if (mask >> i) & 1]
            h.update(struct.pack("<HH", residue, len(indices)))
            for index in indices:
                h.update(struct.pack("<H", index))
        per_prime[str(prime)] = {
            "residue_count": modulus,
            "membership_count": memberships,
            "sets_digest": h.hexdigest(),
        }
    _require(valuation3_witness is not None, "no valuation-3 exclusion witness found")
    return {"per_prime": per_prime, "valuation3_exclusion_witness": valuation3_witness}


def verify_coverage_membership(
    prime: int,
    residue: int,
    pair_index: int,
    claimed: bool,
    domain: Sequence[tuple[int, int, int]] | None = None,
) -> None:
    if domain is None:
        domain = generate_domain()
    _require(prime in P4, f"unexpected prime {prime}")
    _require(0 <= residue < prime * prime, "residue outside p^2 range")
    _require(0 <= pair_index < len(domain), "pair index outside domain")
    expected = valuation_exactly_one(residue - domain[pair_index][2], prime)
    _require(claimed == expected, "claimed coverage violates valuation-exactly-one semantics")


def tuple_coverage(residues: Sequence[int], masks: Mapping[int, Sequence[int]]) -> int:
    _require(len(residues) == 4, "P4 tuple must have four coordinates")
    union = 0
    for prime, modulus, residue in zip(P4, MODULI, residues):
        _require(0 <= residue < modulus, f"residue {residue} outside modulus {modulus}")
        union |= masks[prime][residue]
    return union.bit_count()


def tuple_covered_indices(residues: Sequence[int], masks: Mapping[int, Sequence[int]]) -> set[int]:
    union = 0
    for prime, modulus, residue in zip(P4, MODULI, residues):
        _require(0 <= residue < modulus, f"residue {residue} outside modulus {modulus}")
        union |= masks[prime][residue]
    return {i for i in range(407) if (union >> i) & 1}


def serialize_full_row(residues: Sequence[int], coverage: int) -> bytes:
    _require(len(residues) == 4, "row needs four residues")
    return FULL_ROW.pack(*residues, coverage)


def serialize_argmax_tuple(residues: Sequence[int]) -> bytes:
    _require(len(residues) == 4, "argmax row needs four residues")
    return ARGMAX_ROW.pack(*residues)


def _coordinate_at(ordinal: int, domains: Sequence[Sequence[int]]) -> tuple[int, ...]:
    values = [0] * len(domains)
    for index in range(len(domains) - 1, -1, -1):
        size = len(domains[index])
        ordinal, offset = divmod(ordinal, size)
        values[index] = domains[index][offset]
    _require(ordinal == 0, "tuple ordinal exceeds coordinate product")
    return tuple(values)


def validate_tuple_stream_bytes(
    data: bytes,
    *,
    coordinate_values: Sequence[Sequence[int]],
    coverage_fn: Callable[[tuple[int, int, int, int]], int] | None = None,
    expected_digest: str | None = None,
    expected_histogram: Mapping[int | str, int] | Sequence[Any] | None = None,
    expected_argmax_count: int | None = None,
) -> dict[str, Any]:
    """Strict parser for canonical 5xuint16-LE tuple streams."""
    _require(len(coordinate_values) == 4, "stream requires four coordinate domains")
    row_count = math.prod(len(values) for values in coordinate_values)
    expected_bytes = row_count * FULL_ROW.size
    _require(
        len(data) == expected_bytes,
        f"stream length {len(data)} != exact expected length {expected_bytes}",
    )
    h = hashlib.sha256()
    histogram: Counter[int] = Counter()
    maximum = -1
    argmax_count = 0
    for ordinal in range(row_count):
        offset = ordinal * FULL_ROW.size
        row_bytes = data[offset : offset + FULL_ROW.size]
        t3, t7, t11, t23, coverage = FULL_ROW.unpack(row_bytes)
        residues = (t3, t7, t11, t23)
        expected_tuple = _coordinate_at(ordinal, coordinate_values)
        _require(residues == expected_tuple, f"noncanonical tuple at row {ordinal}")
        _require(coverage <= 407, f"coverage outside [0,407] at row {ordinal}")
        if coverage_fn is not None:
            expected_coverage = coverage_fn(residues)
            _require(coverage == expected_coverage, f"wrong coverage at row {ordinal}")
        h.update(row_bytes)
        histogram[coverage] += 1
        if coverage > maximum:
            maximum = coverage
            argmax_count = 1
        elif coverage == maximum:
            argmax_count += 1
    digest = h.hexdigest()
    if expected_digest is not None:
        _require(digest == expected_digest, "tuple stream SHA256 mismatch")
    if expected_histogram is not None:
        _require(dict(histogram) == normalize_histogram(expected_histogram), "stream histogram mismatch")
    if expected_argmax_count is not None:
        _require(argmax_count == expected_argmax_count, "stream argmax count mismatch")
    return {
        "row_count": row_count,
        "byte_count": len(data),
        "stream_digest": digest,
        "histogram": dict(sorted(histogram.items())),
        "minimum": min(histogram),
        "maximum": maximum,
        "argmax_count": argmax_count,
    }


def validate_tuple_stream_file(
    path: Path,
    **kwargs: Any,
) -> dict[str, Any]:
    return validate_tuple_stream_bytes(path.read_bytes(), **kwargs)


def normalize_histogram(value: Mapping[int | str, Any] | Sequence[Any]) -> dict[int, int]:
    result: dict[int, int] = {}
    if isinstance(value, Mapping):
        items = value.items()
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        if all(isinstance(item, (int, str)) for item in value):
            items = enumerate(value)
        else:
            expanded: list[tuple[Any, Any]] = []
            for item in value:
                if isinstance(item, Mapping):
                    key = item.get("coverage", item.get("G"))
                    count = item.get("count", item.get("tuple_count"))
                    expanded.append((key, count))
                else:
                    _require(len(item) == 2, "histogram row must have two entries")
                    expanded.append((item[0], item[1]))
            items = expanded
    else:
        raise VerificationError("histogram must be a mapping or sequence")
    for raw_key, raw_count in items:
        key = _as_int(raw_key, "histogram coverage")
        count = _as_int(raw_count, f"histogram[{key}]")
        _require(0 <= key <= 407, f"histogram coverage {key} outside [0,407]")
        _require(count >= 0, f"histogram count for {key} is negative")
        if count:
            _require(key not in result, f"duplicate histogram coverage {key}")
            result[key] = count
    _require(result, "histogram is empty")
    return dict(sorted(result.items()))


def _tuple_from_json(value: Any, label: str = "tuple") -> tuple[int, int, int, int]:
    if isinstance(value, Mapping):
        value = [value.get("t3"), value.get("t7"), value.get("t11"), value.get("t23")]
    _require(isinstance(value, Sequence) and not isinstance(value, (str, bytes)), f"{label} malformed")
    _require(len(value) == 4, f"{label} must have four coordinates")
    result = tuple(_as_int(v, label) for v in value)
    for residue, modulus in zip(result, MODULI):
        _require(0 <= residue < modulus, f"{label} residue outside modulus")
    return result  # type: ignore[return-value]


def _first_tuples(section: Mapping[str, Any]) -> list[tuple[int, int, int, int]]:
    raw = section.get("first_100_argmax", section.get("first_100_maximizers"))
    _require(isinstance(raw, Sequence), "missing first 100 argmax tuples")
    result = [_tuple_from_json(row, "argmax tuple") for row in raw]
    _require(result == sorted(result), "first argmax tuples are not lexicographically sorted")
    _require(len(set(result)) == len(result), "duplicate first argmax tuple")
    return result


def _hex_digest(value: Any, label: str) -> str:
    _require(isinstance(value, str) and len(value) == 64, f"{label} must be a SHA256 hex digest")
    try:
        bytes.fromhex(value)
    except ValueError as exc:
        raise VerificationError(f"{label} is not hexadecimal") from exc
    return value.lower()


def expected_serialization_contract(row_count: int) -> dict[str, Any]:
    return {
        "fields": ["t3", "t7", "t11", "t23", "G"],
        "integer_width_bits": 16,
        "byte_order": "little",
        "row_bytes": 10,
        "padding_bytes": 0,
        "tuple_order": "lexicographic",
        "row_count": row_count,
        "struct_format": "<5H",
        "includes_G": True,
    }


def validate_serialization_contract(contract: Mapping[str, Any], row_count: int) -> None:
    fields = contract.get("fields", contract.get("row_fields"))
    _require(fields == ["t3", "t7", "t11", "t23", "G"], "wrong stream fields/order")
    width = contract.get("integer_width_bits", contract.get("width_bits"))
    widths = contract.get("widths_bits")
    _require(width == 16 or widths == [16, 16, 16, 16, 16], "stream integers are not uint16")
    _require(str(contract.get("byte_order", "")).lower() in {"little", "le"}, "stream is not little-endian")
    _require(_as_int(contract.get("row_bytes"), "row_bytes") == 10, "stream row is not 10 bytes")
    padding = contract.get("padding_bytes", 0 if contract.get("no_padding") is True else None)
    _require(padding == 0, "stream has or fails to exclude padding")
    order = str(contract.get("tuple_order", contract.get("order", ""))).lower()
    _require("lex" in order, "stream order is not explicitly lexicographic")
    _require(_as_int(contract.get("row_count"), "serialization row_count") == row_count, "wrong serialization row count")
    if "struct_format" in contract:
        _require(contract["struct_format"] == "<5H", "wrong struct format")
    if "includes_G" in contract:
        _require(contract["includes_G"] is True, "coverage G is not included")

    argmax = contract.get("argmax")
    if argmax is not None:
        _require(isinstance(argmax, Mapping), "argmax serialization contract malformed")
        _require(argmax.get("fields") == ["t3", "t7", "t11", "t23"], "wrong argmax fields")
        _require(_as_int(argmax.get("row_bytes"), "argmax row_bytes") == 8, "argmax row is not 8 bytes")
        _require(str(argmax.get("byte_order", "")).lower() in {"little", "le"}, "argmax not little-endian")
        _require(argmax.get("includes_G", False) is False, "argmax digest must exclude G")


def _partial_unions(
    primes: Sequence[int], masks: Mapping[int, Sequence[int]], fixed: Mapping[int, int]
) -> list[tuple[int, tuple[int, ...]]]:
    domains: list[Sequence[int]] = []
    for prime in primes:
        domains.append((fixed[prime],) if prime in fixed else range(prime * prime))
    rows: list[tuple[int, tuple[int, ...]]] = []
    for residues in itertools.product(*domains):
        union = 0
        for prime, residue in zip(primes, residues):
            union |= masks[prime][residue]
        rows.append((union, tuple(residues)))
    return rows


def optimize_subset(
    primes: Sequence[int],
    masks: Mapping[int, Sequence[int]],
    *,
    fixed: Mapping[int, int] | None = None,
    digest_four_tuple: bool = False,
) -> dict[str, Any]:
    """Exact meet-in-the-middle subset optimizer used only by the verifier."""
    _require(primes, "empty subset is not optimized")
    fixed = {} if fixed is None else dict(fixed)
    split = max(1, len(primes) // 2)
    left_primes = tuple(primes[:split])
    right_primes = tuple(primes[split:])
    left = _partial_unions(left_primes, masks, fixed)
    right = _partial_unions(right_primes, masks, fixed) if right_primes else [(0, ())]

    maximum = -1
    count = 0
    first: list[tuple[int, ...]] = []
    digest = hashlib.sha256()
    for left_mask, left_tuple in left:
        for right_mask, right_tuple in right:
            residues = left_tuple + right_tuple
            coverage = (left_mask | right_mask).bit_count()
            if coverage > maximum:
                maximum = coverage
                count = 1
                first = [residues]
                digest = hashlib.sha256()
                if digest_four_tuple:
                    digest.update(ARGMAX_ROW.pack(*residues))
            elif coverage == maximum:
                count += 1
                if len(first) < 100:
                    first.append(residues)
                if digest_four_tuple:
                    digest.update(ARGMAX_ROW.pack(*residues))
    return {
        "primes": list(primes),
        "maximum": maximum,
        "argmax_count": count,
        "first_100_argmax": [list(row) for row in first],
        "argmax_digest": digest.hexdigest() if digest_four_tuple else None,
    }


def optimize_all_subsets(masks: Mapping[int, Sequence[int]]) -> dict[tuple[int, ...], dict[str, Any]]:
    result: dict[tuple[int, ...], dict[str, Any]] = {}
    for size in range(1, len(P4) + 1):
        for primes in itertools.combinations(P4, size):
            result[primes] = optimize_subset(
                primes,
                masks,
                digest_four_tuple=(primes == P4),
            )
    return result


def generalized_crt(congruences: Iterable[tuple[int, int]]) -> tuple[int, int]:
    """Return canonical (residue, lcm modulus), rejecting incompatibility."""
    residue = 0
    modulus = 1
    for next_residue, next_modulus in congruences:
        _require(next_modulus > 0, "CRT modulus must be positive")
        next_residue %= next_modulus
        common = math.gcd(modulus, next_modulus)
        delta = next_residue - residue
        _require(delta % common == 0, "incompatible CRT congruences")
        left = modulus // common
        right = next_modulus // common
        multiplier = ((delta // common) * pow(left, -1, right)) % right if right != 1 else 0
        residue += modulus * multiplier
        modulus *= right
        residue %= modulus
    return residue, modulus


def crt_p4(residues: Sequence[int]) -> int:
    _require(len(residues) == 4, "P4 CRT needs four residues")
    residue, modulus = generalized_crt(zip(residues, MODULI))
    _require(modulus == M4, f"P4 CRT modulus {modulus} != {M4}")
    return residue


def count_congruence_in_interval(residue: int, modulus: int, low: int, high: int) -> int:
    _require(modulus > 0 and low <= high, "invalid congruence interval")
    residue %= modulus
    k_min = -((-(low - residue)) // modulus)
    k_max = (high - residue) // modulus
    return max(0, k_max - k_min + 1)


def nearest_congruence_in_interval(
    residue: int, modulus: int, target: int, low: int, high: int
) -> int | None:
    _require(modulus > 0 and low <= high, "invalid congruence interval")
    residue %= modulus
    k_min = -((-(low - residue)) // modulus)
    k_max = (high - residue) // modulus
    if k_min > k_max:
        return None
    k_floor = (target - residue) // modulus
    candidates = {min(max(k_floor, k_min), k_max), min(max(k_floor + 1, k_min), k_max)}
    values = [residue + k * modulus for k in candidates]
    return min(values, key=lambda value: (abs(value - target), value))


def _section_value(section: Mapping[str, Any], names: Sequence[str], label: str) -> Any:
    for name in names:
        if name in section:
            return section[name]
    raise VerificationError(f"missing {label}")


def expected_n0_counts(histogram: Mapping[int, int]) -> dict[str, Any]:
    below = sum(count for coverage, count in histogram.items() if coverage < N0_COVERAGE)
    equal = histogram.get(N0_COVERAGE, 0)
    above = sum(count for coverage, count in histogram.items() if coverage > N0_COVERAGE)
    total = below + equal + above
    return {
        "above": above,
        "equal": equal,
        "below": below,
        "rank_interval_descending": [above + 1, above + equal],
        "empirical_percentile_midrank": {
            "numerator": 100 * (2 * below + equal),
            "denominator": 2 * total,
        },
    }


def validate_n0_counts(raw: Mapping[str, Any], histogram: Mapping[int, int]) -> None:
    expected = expected_n0_counts(histogram)
    aliases = {
        "above": ("above", "greater", "greater_than_216", "count_greater_than_216"),
        "equal": ("equal", "equal_to_216", "count_equal_to_216"),
        "below": ("below", "less", "less_than_216", "count_less_than_216"),
    }
    for key, names in aliases.items():
        actual = _as_int(_section_value(raw, names, f"n0 {key} count"), f"n0 {key}")
        _require(actual == expected[key], f"wrong n0 {key} count")
    rank = raw.get("rank_interval_descending", raw.get("rank_interval"))
    _require(list(rank) == expected["rank_interval_descending"], "wrong n0 descending rank interval")
    percentile = raw.get(
        "empirical_percentile_midrank",
        raw.get("empirical_percentile", raw.get("percentile")),
    )
    _require(isinstance(percentile, Mapping), "percentile must be an exact rational object")
    numerator = _as_int(percentile.get("numerator"), "percentile numerator")
    denominator = _as_int(percentile.get("denominator"), "percentile denominator")
    exp = expected["empirical_percentile_midrank"]
    _require(
        numerator * exp["denominator"] == exp["numerator"] * denominator,
        "wrong exact midrank percentile",
    )


def validate_n0_section(section: Mapping[str, Any], masks: Mapping[int, Sequence[int]]) -> None:
    residues = _tuple_from_json(_section_value(section, ("tuple", "residues"), "n0 tuple"), "n0 tuple")
    _require(residues == N0_TUPLE, f"n0 tuple {residues} != {N0_TUPLE}")
    coverage = _as_int(_section_value(section, ("coverage", "G"), "n0 coverage"), "n0 coverage")
    computed = tuple_coverage(residues, masks)
    _require(computed == N0_COVERAGE, f"independent n0 coverage is {computed}, expected 216")
    _require(coverage == computed, "certificate n0 coverage mismatch")


def _normalize_primes(value: Any) -> tuple[int, ...]:
    if isinstance(value, str):
        cleaned = value.replace("[", "").replace("]", "").replace(";", ",")
        value = [part for part in cleaned.replace(" ", ",").split(",") if part]
    _require(isinstance(value, Sequence), "subset primes malformed")
    return tuple(_as_int(prime, "subset prime") for prime in value)


def normalize_subset_rows(rows: Any) -> dict[tuple[int, ...], Mapping[str, Any]]:
    if isinstance(rows, Mapping):
        iterable = []
        for key, row in rows.items():
            if isinstance(row, Mapping) and "primes" not in row:
                row = dict(row)
                row["primes"] = key
            iterable.append(row)
    else:
        iterable = rows
    _require(isinstance(iterable, Sequence), "subset_optima must be a sequence or mapping")
    result: dict[tuple[int, ...], Mapping[str, Any]] = {}
    for row in iterable:
        _require(isinstance(row, Mapping), "subset optimum row malformed")
        primes = _normalize_primes(row.get("primes"))
        _require(primes not in result, f"duplicate subset row {primes}")
        result[primes] = row
    _require(len(result) == 15, f"subset table has {len(result)} rows, expected 15")
    expected_keys = {
        tuple(P4[i] for i in range(4) if mask & (1 << i)) for mask in range(1, 16)
    }
    _require(set(result) == expected_keys, "subset table does not contain exactly all 15 P4 subsets")
    return result


def validate_subset_rows(
    rows: Any,
    exact: Mapping[tuple[int, ...], Mapping[str, Any]],
    masks: Mapping[int, Sequence[int]],
) -> dict[tuple[int, ...], Mapping[str, Any]]:
    normalized = normalize_subset_rows(rows)
    for primes, row in normalized.items():
        modulus = math.prod(prime * prime for prime in primes)
        actual_modulus = _as_int(
            _section_value(row, ("modulus_product", "M_S", "modulus"), "subset modulus"),
            "subset modulus",
        )
        _require(actual_modulus == modulus, f"subset {primes}: wrong modulus product")
        if "bit_length" in row or "modulus_bit_length" in row:
            bit_length = _as_int(row.get("bit_length", row.get("modulus_bit_length")), "bit length")
            _require(bit_length == modulus.bit_length(), f"subset {primes}: wrong bit length")
        if "decimal_digits" in row or "decimal_digit_count" in row:
            digits = _as_int(row.get("decimal_digits", row.get("decimal_digit_count")), "decimal digits")
            _require(digits == len(str(modulus)), f"subset {primes}: wrong decimal digits")
        maximum = _as_int(_section_value(row, ("maximum", "maximum_coverage", "G_max"), "subset maximum"), "maximum")
        count = _as_int(_section_value(row, ("argmax_count", "maximizer_count"), "subset argmax count"), "argmax count")
        _require(maximum == exact[primes]["maximum"], f"subset {primes}: wrong exact maximum")
        _require(count == exact[primes]["argmax_count"], f"subset {primes}: wrong argmax count")
        first_raw = row.get("first_maximizer", row.get("lexicographically_first_maximizer"))
        if first_raw is not None:
            first = tuple(_as_int(v, "subset first maximizer") for v in first_raw)
            expected_first = tuple(exact[primes]["first_100_argmax"][0])
            _require(first == expected_first, f"subset {primes}: wrong first maximizer")
            union = 0
            for prime, residue in zip(primes, first):
                union |= masks[prime][residue]
            _require(union.bit_count() == maximum, f"subset {primes}: first maximizer invalid")
    return normalized


def validate_landscape_section(
    section: Mapping[str, Any],
    *,
    expected_count: int,
    masks: Mapping[int, Sequence[int]],
    exact_optimum: Mapping[str, Any],
    fixed_t3: int | None = None,
) -> dict[str, Any]:
    count = _as_int(_section_value(section, ("tuple_count", "row_count"), "tuple count"), "tuple count")
    _require(count == expected_count, f"tuple count {count} != {expected_count}")
    histogram = normalize_histogram(_section_value(section, ("histogram",), "histogram"))
    _require(sum(histogram.values()) == expected_count, "histogram total does not equal tuple count")
    minimum = _as_int(_section_value(section, ("minimum", "G_min"), "minimum"), "minimum")
    maximum = _as_int(_section_value(section, ("maximum", "G_max"), "maximum"), "maximum")
    _require(minimum == min(histogram), "reported minimum disagrees with histogram")
    _require(maximum == max(histogram), "reported maximum disagrees with histogram")
    _require(maximum == exact_optimum["maximum"], "reported maximum fails independent optimization")
    argmax_count = _as_int(_section_value(section, ("argmax_count", "maximizer_count"), "argmax count"), "argmax count")
    _require(argmax_count == histogram[maximum], "argmax count disagrees with histogram")
    _require(argmax_count == exact_optimum["argmax_count"], "argmax count fails independent optimization")
    stream_digest = _hex_digest(_section_value(section, ("stream_digest",), "stream digest"), "stream digest")
    argmax_digest = _hex_digest(_section_value(section, ("argmax_digest",), "argmax digest"), "argmax digest")
    _require(argmax_digest == exact_optimum["argmax_digest"], "argmax digest fails independent optimization")
    first = _first_tuples(section)
    expected_first = [_tuple_from_json(row) for row in exact_optimum["first_100_argmax"]]
    _require(first == expected_first, "first argmax tuples fail independent optimization")
    _require(len(first) == min(100, argmax_count), "wrong number of retained argmax tuples")
    for residues in first:
        if fixed_t3 is not None:
            _require(residues[0] == fixed_t3, "slice argmax violates fixed t3")
        _require(tuple_coverage(residues, masks) == maximum, "invalid argmax tuple coverage")
        _require(crt_p4(residues) % 9 == residues[0], "argmax CRT self-check failed")
    n0_counts = section.get("n0_counts")
    _require(isinstance(n0_counts, Mapping), "missing n0_counts")
    validate_n0_counts(n0_counts, histogram)
    return {
        "tuple_count": count,
        "histogram": histogram,
        "minimum": minimum,
        "maximum": maximum,
        "argmax_count": argmax_count,
        "stream_digest": stream_digest,
        "argmax_digest": argmax_digest,
        "first_100_argmax": first,
        "n0_counts": expected_n0_counts(histogram),
    }


def _validate_top_level(cert: Mapping[str, Any]) -> None:
    _require(isinstance(cert.get("schema"), str), "missing certificate schema")
    _require(list(cert.get("primes", [])) == list(P4), "certificate primes are not fixed P4")
    moduli = cert.get("moduli")
    if isinstance(moduli, Mapping):
        normalized_moduli = [_as_int(moduli.get(str(p), moduli.get(p)), "modulus") for p in P4]
    else:
        normalized_moduli = [_as_int(v, "modulus") for v in moduli]
    _require(normalized_moduli == list(MODULI), "wrong square moduli")
    _require(_as_int(cert.get("M4"), "M4") == M4, "wrong M4")
    domain = cert.get("domain")
    _require(isinstance(domain, Mapping), "missing domain metadata")
    interval = domain.get("interval", domain.get("activation_cell"))
    if interval is not None:
        _require([_as_int(v, "domain interval") for v in interval] == [CELL_LOW, CELL_HIGH], "wrong domain interval")
    pair_count = domain.get("pair_count", domain.get("active_pair_count"))
    _require(_as_int(pair_count, "domain pair count") == 407, "wrong domain pair count")
    if "pairs_digest" in domain:
        _require(domain["pairs_digest"] == domain_digest(generate_domain()), "wrong domain pair digest")
    serialization = cert.get("serialization")
    _require(isinstance(serialization, Mapping), "missing serialization contract")
    validate_serialization_contract(serialization, FULL_TUPLE_COUNT)


def verify_hash_manifest(path: Path, root: Path) -> dict[str, Any]:
    manifest = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(manifest, Mapping) and "files" in manifest:
        records = manifest["files"]
    else:
        records = manifest
    normalized: list[tuple[str, str, int | None]] = []
    if isinstance(records, Mapping):
        for name, value in records.items():
            if isinstance(value, Mapping):
                normalized.append((name, value.get("sha256"), value.get("size")))
            else:
                normalized.append((name, value, None))
    else:
        for record in records:
            normalized.append((record["path"], record["sha256"], record.get("size")))
    checked = 0
    root_resolved = root.resolve()
    for relative, expected_hash, expected_size in normalized:
        target = (root / relative).resolve()
        _require(target == root_resolved or root_resolved in target.parents, "manifest path escapes root")
        _require(target.is_file(), f"manifest file missing: {relative}")
        _require(sha256_file(target) == str(expected_hash).lower(), f"hash mismatch: {relative}")
        if expected_size is not None:
            _require(target.stat().st_size == _as_int(expected_size, "manifest size"), f"size mismatch: {relative}")
        checked += 1
    return {"manifest": str(path), "files_checked": checked}


def _csv_histogram(path: Path) -> dict[int, int]:
    result: dict[int, int] = {}
    with path.open(newline="", encoding="utf-8") as handle:
        for row in csv.DictReader(handle):
            coverage = _as_int(row.get("coverage", row.get("G")), "CSV coverage")
            count = _as_int(row.get("count", row.get("tuple_count")), "CSV count")
            _require(coverage not in result, "duplicate histogram CSV coverage")
            result[coverage] = count
    return dict(sorted(result.items()))


def _walk_dicts(value: Any) -> Iterable[Mapping[str, Any]]:
    if isinstance(value, Mapping):
        yield value
        for child in value.values():
            yield from _walk_dicts(child)
    elif isinstance(value, Sequence) and not isinstance(value, (str, bytes, bytearray)):
        for child in value:
            yield from _walk_dicts(child)


def verify_crt_artifact(value: Any) -> int:
    checked = 0
    for row in _walk_dicts(value):
        tuple_value = row.get("tuple", row.get("residues"))
        if tuple_value is None:
            continue
        try:
            residues = _tuple_from_json(tuple_value, "CRT tuple")
        except VerificationError:
            continue
        base_residue = crt_p4(residues)
        if "residue_mod_L" in row:
            reported_residue = row["residue_mod_L"]
            reported_modulus = row.get("L", L_CONSTRAINED)
        elif "r_mod_M4" in row:
            reported_residue = row["r_mod_M4"]
            reported_modulus = row.get("modulus", row.get("M", M4))
        else:
            reported_residue = row.get("r", row.get("residue"))
            reported_modulus = row.get("modulus", row.get("M"))
        if reported_residue is None:
            continue
        if reported_modulus is None or _as_int(reported_modulus, "CRT modulus") == M4:
            expected_residue, modulus = base_residue, M4
        else:
            modulus = _as_int(reported_modulus, "CRT modulus")
            _require(modulus == L_CONSTRAINED, "unexpected CRT artifact modulus")
            expected_residue, expected_modulus = generalized_crt(((base_residue, M4), (N0 % 40, 40)))
            _require(expected_modulus == L_CONSTRAINED, "wrong constrained CRT modulus")
        _require(_as_int(reported_residue, "CRT residue") == expected_residue, "wrong CRT reconstruction")
        count_value = row.get(
            "activation_cell_count",
            row.get("class_member_count", row.get("count_in_cell", row.get("count"))),
        )
        if count_value is not None:
            expected_count = count_congruence_in_interval(expected_residue, modulus, CELL_LOW, CELL_HIGH)
            _require(_as_int(count_value, "activation count") == expected_count, "wrong activation-cell point count")
        nearest = row.get("nearest_to_n0", row.get("nearest_member"))
        if nearest is not None:
            expected_nearest = nearest_congruence_in_interval(expected_residue, modulus, N0, CELL_LOW, CELL_HIGH)
            _require(_as_int(nearest, "nearest member") == expected_nearest, "wrong nearest CRT member")
        checked += 1
    return checked


def verify_artifact_directory(
    directory: Path,
    full: Mapping[str, Any],
    t3eq2: Mapping[str, Any],
) -> dict[str, Any]:
    _require(directory.is_dir(), f"artifact directory missing: {directory}")
    checked: list[str] = []
    full_hist = directory / "full_histogram.csv"
    if full_hist.exists():
        _require(_csv_histogram(full_hist) == full["histogram"], "full histogram artifact mismatch")
        checked.append(full_hist.name)
    slice_hist = directory / "t3eq2_histogram.csv"
    if slice_hist.exists():
        _require(_csv_histogram(slice_hist) == t3eq2["histogram"], "slice histogram artifact mismatch")
        checked.append(slice_hist.name)
    crt_path = directory / "crt_candidates.json"
    crt_rows = 0
    if crt_path.exists():
        crt_value = json.loads(crt_path.read_text(encoding="utf-8"))
        crt_rows = verify_crt_artifact(crt_value)
        _require(crt_rows > 0, "CRT artifact contains no verifiable rows")
        checked.append(crt_path.name)
    metadata_path = directory / "metadata.json"
    if metadata_path.exists():
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        if "M4" in metadata:
            _require(_as_int(metadata["M4"], "metadata M4") == M4, "metadata M4 mismatch")
        hash_map = metadata.get("artifact_sha256_excluding_metadata_and_verification_report")
        _require(isinstance(hash_map, Mapping), "metadata artifact hash map missing")
        actual_hashed_names = {
            path.name
            for path in directory.iterdir()
            if path.is_file() and path.name not in {"metadata.json", "verification_report.json"}
        }
        _require(set(map(str, hash_map)) == actual_hashed_names,
                 "metadata artifact hash map does not exactly cover data artifacts")
        for name, expected in hash_map.items():
            target = directory / str(name)
            _require(sha256_file(target) == str(expected).lower(),
                     f"committed artifact hash mismatch: {name}")
        report_hash = metadata.get("verification_report_sha256")
        if report_hash is not None:
            report_path = directory / "verification_report.json"
            _require(report_path.is_file(), "hashed verification report missing")
            _require(sha256_file(report_path) == str(report_hash).lower(),
                     "verification report hash mismatch")
        checked.append(metadata_path.name)
    expected_artifacts = {
        "coverage_comparison.json", "crt_candidates.json", "full_histogram.csv",
        "local_landscape.json", "maximizers.json", "metadata.json", "n0_rank.json",
        "subset_optima.csv", "t3eq2_histogram.csv", "verification_report.json",
    }
    _require({path.name for path in directory.iterdir() if path.is_file()} == expected_artifacts,
             "artifact directory file set mismatch")
    for name in ("coverage_comparison.json", "local_landscape.json", "maximizers.json", "n0_rank.json"):
        value = json.loads((directory / name).read_text(encoding="utf-8"))
        _require(isinstance(value.get("schema"), str), f"artifact schema missing: {name}")
    checked = sorted(expected_artifacts)
    return {"files_checked": checked, "crt_rows_checked": crt_rows}


def _agreement_projection(cert: Mapping[str, Any]) -> dict[str, Any]:
    projection: dict[str, Any] = {}
    for name in ("full", "t3eq2"):
        section = cert[name]
        histogram = normalize_histogram(section["histogram"])
        projection[name] = {
            "tuple_count": _as_int(section["tuple_count"], "tuple count"),
            "minimum": _as_int(section["minimum"], "minimum"),
            "maximum": _as_int(section["maximum"], "maximum"),
            "histogram": histogram,
            "argmax_count": _as_int(section["argmax_count"], "argmax count"),
            "argmax_digest": str(section["argmax_digest"]).lower(),
            "first_100_argmax": _first_tuples(section),
            "stream_digest": str(section["stream_digest"]).lower(),
            # Wording fields are allowed to differ.  Agreement is over the
            # exact counts, rank interval, and rational percentile, all of
            # which are independently derived from the common histogram.
            "n0_counts": expected_n0_counts(histogram),
        }
    projection["n0"] = {
        "tuple": _tuple_from_json(cert["n0"]["tuple"]),
        "coverage": _as_int(cert["n0"]["coverage"], "n0 coverage"),
    }
    subset = normalize_subset_rows(cert["subset_optima"])
    projection["subset_optima"] = {
        primes: (
            _as_int(_section_value(row, ("maximum", "maximum_coverage", "G_max"), "maximum"), "maximum"),
            _as_int(_section_value(row, ("argmax_count", "maximizer_count"), "count"), "count"),
        )
        for primes, row in subset.items()
    }
    return projection


def verify_certificates(
    certificate_a: Mapping[str, Any],
    certificate_b: Mapping[str, Any],
    *,
    artifact_dir: Path | None = None,
    manifests: Sequence[tuple[Path, Path]] = (),
    deep_subsets: bool = True,
) -> dict[str, Any]:
    _validate_top_level(certificate_a)
    _validate_top_level(certificate_b)
    _require(_agreement_projection(certificate_a) == _agreement_projection(certificate_b), "A/B certificates disagree")

    domain = generate_domain()
    masks = build_coverage_masks(domain)
    coverage_report = verify_coverage_semantics(domain, masks)
    _require(tuple_coverage(N0_TUPLE, masks) == N0_COVERAGE, "n0 coverage is not 216")

    if deep_subsets:
        exact_subsets = optimize_all_subsets(masks)
        exact_full = exact_subsets[P4]
    else:
        exact_full = optimize_subset(P4, masks, digest_four_tuple=True)
        exact_subsets = {P4: exact_full}
        # Non-deep mode still verifies each reported first tuple and A/B agreement.
        for primes in normalize_subset_rows(certificate_a["subset_optima"]):
            if primes != P4:
                row = normalize_subset_rows(certificate_a["subset_optima"])[primes]
                first_raw = row.get("first_maximizer", row.get("lexicographically_first_maximizer"))
                _require(first_raw is not None, f"subset {primes} lacks a checkable first maximizer")
                first = tuple(_as_int(v, "first maximizer") for v in first_raw)
                union = 0
                for prime, residue in zip(primes, first):
                    union |= masks[prime][residue]
                exact_subsets[primes] = {
                    "maximum": union.bit_count(),
                    "argmax_count": _as_int(row.get("argmax_count"), "argmax count"),
                    "first_100_argmax": [list(first)],
                }

    exact_slice = optimize_subset(P4, masks, fixed={3: 2}, digest_four_tuple=True)
    full_a = validate_landscape_section(
        certificate_a["full"],
        expected_count=FULL_TUPLE_COUNT,
        masks=masks,
        exact_optimum=exact_full,
    )
    slice_a = validate_landscape_section(
        certificate_a["t3eq2"],
        expected_count=T3EQ2_TUPLE_COUNT,
        masks=masks,
        exact_optimum=exact_slice,
        fixed_t3=2,
    )
    # Validate B independently even after agreement, so malformed aliases cannot hide.
    validate_landscape_section(
        certificate_b["full"],
        expected_count=FULL_TUPLE_COUNT,
        masks=masks,
        exact_optimum=exact_full,
    )
    validate_landscape_section(
        certificate_b["t3eq2"],
        expected_count=T3EQ2_TUPLE_COUNT,
        masks=masks,
        exact_optimum=exact_slice,
        fixed_t3=2,
    )
    validate_n0_section(certificate_a["n0"], masks)
    validate_n0_section(certificate_b["n0"], masks)
    validate_subset_rows(certificate_a["subset_optima"], exact_subsets, masks)
    validate_subset_rows(certificate_b["subset_optima"], exact_subsets, masks)

    artifact_report = None
    if artifact_dir is not None:
        artifact_report = verify_artifact_directory(artifact_dir, full_a, slice_a)
    manifest_reports = [verify_hash_manifest(path, root) for path, root in manifests]
    return {
        "schema": "a303656-fixed-p4-verification-report-v1",
        "status": "PASS",
        "classification": "EXACT FINITE COMPUTATION CERTIFICATE VERIFIED",
        "domain": {
            "interval": [CELL_LOW, CELL_HIGH],
            "pair_count": len(domain),
            "pairs_digest": domain_digest(domain),
            "duplicate_shift_28_pairs": [[1, 2], [3, 0]],
        },
        "coverage_sets": coverage_report,
        "full": {
            "tuple_count": full_a["tuple_count"],
            "minimum": full_a["minimum"],
            "maximum": full_a["maximum"],
            "argmax_count": full_a["argmax_count"],
            "stream_digest": full_a["stream_digest"],
            "argmax_digest": full_a["argmax_digest"],
        },
        "t3eq2": {
            "tuple_count": slice_a["tuple_count"],
            "minimum": slice_a["minimum"],
            "maximum": slice_a["maximum"],
            "argmax_count": slice_a["argmax_count"],
            "stream_digest": slice_a["stream_digest"],
            "argmax_digest": slice_a["argmax_digest"],
        },
        "n0": {"tuple": list(N0_TUPLE), "coverage": N0_COVERAGE},
        "subset_optima_checked": len(exact_subsets),
        "artifact_report": artifact_report,
        "manifest_reports": manifest_reports,
    }


def _load_json(path: Path) -> Mapping[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    _require(isinstance(value, Mapping), f"JSON root is not an object: {path}")
    return value


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--certificate-a", required=True, type=Path)
    parser.add_argument("--certificate-b", required=True, type=Path)
    parser.add_argument("--artifact-dir", type=Path)
    parser.add_argument(
        "--manifest",
        nargs=2,
        action="append",
        default=[],
        metavar=("MANIFEST", "ROOT"),
        help="verify a JSON SHA256 manifest relative to ROOT",
    )
    parser.add_argument("--skip-deep-subsets", action="store_true")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(argv)
    try:
        report = verify_certificates(
            _load_json(args.certificate_a),
            _load_json(args.certificate_b),
            artifact_dir=args.artifact_dir,
            manifests=[(Path(path), Path(root)) for path, root in args.manifest],
            deep_subsets=not args.skip_deep_subsets,
        )
    except (OSError, json.JSONDecodeError, VerificationError) as exc:
        print(json.dumps({"status": "FAIL", "error": str(exc)}, sort_keys=True), file=sys.stderr)
        return 1
    rendered = json.dumps(report, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        args.output.write_text(rendered, encoding="utf-8")
    sys.stdout.write(rendered)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
