#!/usr/bin/env python3
"""Boundary/property tests using an independent GMP nested-loop oracle.

The oracle executable is compiled from tests/tiny_twosquares_oracle.cpp.  It
does not include production headers and does not use either scanner's square
root, annulus traversal, or packed-bit accounting.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import tempfile
from pathlib import Path


UINT64_MAX = (1 << 64) - 1
SCANNERS = (
    ("search_twosquares_bitset", "direct_two_squares_bitset_x_outer"),
    ("search_twosquares_clean", "clean_room_direct_two_squares_y_outer"),
)


def run(arguments: list[str], expected: set[int] | None = None) -> subprocess.CompletedProcess[str]:
    completed = subprocess.run(arguments, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if expected is not None and completed.returncode not in expected:
        raise AssertionError(
            f"unexpected return code {completed.returncode}, expected {sorted(expected)}\n"
            f"command={arguments!r}\nstdout={completed.stdout}\nstderr={completed.stderr}"
        )
    return completed


def json_stdout(arguments: list[str]) -> dict:
    completed = run(arguments, {0})
    value = json.loads(completed.stdout)
    assert isinstance(value, dict)
    return value


def oracle(oracle_binary: Path, *arguments: object) -> dict:
    return json_stdout([str(oracle_binary), *(str(value) for value in arguments)])


def scanner_seam(binary: Path, *arguments: object) -> dict:
    return json_stdout([str(binary), *(str(value) for value in arguments)])


def scanner_interval(binary: Path, low: int, high: int, C: int, D: int, directory: Path) -> dict:
    output = directory / f"{binary.name}-{low}-{high}-{C}-{D}.json"
    candidates = directory / f"{binary.name}-{low}-{high}-{C}-{D}.txt"
    command = [
        str(binary),
        "--low", str(low),
        "--high", str(high),
        "--C", str(C),
        "--D", str(D),
        "--json", str(output),
        "--candidates", str(candidates),
        "--quiet",
    ]
    completed = run(command, {0, 1})
    data = json.loads(output.read_text(encoding="utf-8"))
    declared = [int(value) for value in data["candidates"]]
    sidecar = [int(value) for value in candidates.read_text(encoding="utf-8").split()]
    assert declared == sidecar
    assert completed.returncode == (0 if declared else 1), (
        f"scanner return/output mismatch: {command!r}\n"
        f"rc={completed.returncode}\nstdout={completed.stdout}\nstderr={completed.stderr}"
    )
    return data


def test_intervals(bin_dir: Path, oracle_binary: Path) -> None:
    # The low=1 cases retain candidate 1, forcing every shift to be processed;
    # lengths 63/64/65 exercise packed-word boundaries.  The remaining cases
    # place shifts and representations exactly on narrow interval endpoints.
    cases = (
        (1, 1, 0, 0),
        (1, 2, 0, 0),
        (1, 3, 0, 0),
        (1, 63, 3, 2),
        (1, 64, 3, 2),
        (1, 65, 3, 2),
        (26, 28, 3, 2),
        (28, 28, 3, 2),
        (28, 29, 3, 2),
        (27, 29, 3, 2),
        (124, 129, 4, 3),
    )
    with tempfile.TemporaryDirectory(prefix="a303656-boundary-intervals-") as text:
        directory = Path(text)
        for low, high, C, D in cases:
            expected = oracle(oracle_binary, "--interval", low, high, C, D)
            marked = {int(value) for value in expected["marked"]}
            candidates = set(range(low, high + 1)) - marked
            assert len(expected["rows"]) == high - low + 1
            for row in expected["rows"]:
                n = int(row["n"])
                assert row["representable"] == (n in marked)
                witness = row["witness"]
                if witness is None:
                    assert int(row["exponent_pair_success_count"]) == 0
                    continue
                a = int(witness["a"])
                b = int(witness["b"])
                shift = int(witness["shift"])
                remainder = int(witness["remainder"])
                assert 0 <= a <= b
                assert a * a + b * b == remainder
                assert shift + remainder == n
                assert shift == 3 ** int(witness["c"]) + 5 ** int(witness["d"])
            for executable, method in SCANNERS:
                actual = scanner_interval(bin_dir / executable, low, high, C, D, directory)
                assert actual["implementation_id"] == executable
                assert actual["method"] == method
                actual_candidates = {int(value) for value in actual["candidates"]}
                assert actual_candidates == candidates
                for row in expected["rows"]:
                    n = int(row["n"])
                    assert (n not in actual_candidates) == bool(row["representable"])
                if low == 1:
                    assert int(actual["shifts_processed_before_termination"]) == int(
                        expected["distinct_shift_count"]
                    )
                    assert int(actual["unordered_square_pairs_enumerated"]) == int(
                        expected["scanner_unordered_pair_visits"]
                    )


def test_annuli(bin_dir: Path, oracle_binary: Path) -> None:
    # Exact radii include zero, axis, diagonal, off-diagonal, unique, multiple,
    # empty, and closed inner/outer boundaries.  Interval widths include 1/2/3.
    cases = (
        (0, 0),
        (1, 1),
        (3, 3),
        (5, 5),
        (8, 8),
        (9, 9),
        (25, 25),
        (4, 5),
        (3, 5),
        (5, 8),
        (5, 9),
    )
    for lower, upper in cases:
        expected = oracle(oracle_binary, "--annulus", lower, upper)
        expected_pairs = [tuple(map(int, pair)) for pair in expected["pairs"]]
        assert int(expected["pair_count"]) == len(expected_pairs)
        assert len(expected_pairs) == len(set(expected_pairs))
        for a, b in expected_pairs:
            assert 0 <= a <= b
            assert lower <= a * a + b * b <= upper
        for executable, _ in SCANNERS:
            actual = scanner_seam(
                bin_dir / executable,
                "--test-annulus-low", lower,
                "--test-annulus-high", upper,
            )
            pairs = [tuple(map(int, pair)) for pair in actual["pairs"]]
            assert actual["implementation_id"] == executable
            assert int(actual["pair_count"]) == len(pairs)
            assert len(pairs) == len(set(pairs))
            assert set(pairs) == set(expected_pairs)


def test_activation(bin_dir: Path) -> None:
    pairs = ((0, 0), (1, 0), (0, 1), (2, 1), (1, 2), (4, 0), (0, 3))
    for c, d in pairs:
        shift = 3**c + 5**d
        for delta in (-1, 0, 1):
            n = shift + delta
            for executable, _ in SCANNERS:
                actual = scanner_seam(
                    bin_dir / executable,
                    "--test-activation-c", c,
                    "--test-activation-d", d,
                    "--test-activation-n", n,
                )
                assert actual["implementation_id"] == executable
                assert int(actual["shift"]) == shift
                if delta < 0:
                    assert actual["active"] is False
                    assert actual["remainder"] is None
                    assert actual["two_square_remainder"] is False
                    assert actual["witness"] is None
                else:
                    assert actual["active"] is True
                    assert int(actual["remainder"]) == delta
                    assert actual["two_square_remainder"] is True
                    witness = tuple(map(int, actual["witness"]))
                    assert witness == ((0, 0) if delta == 0 else (0, 1))
                    assert witness[0] ** 2 + witness[1] ** 2 == delta


def test_isqrt(bin_dir: Path, oracle_binary: Path) -> None:
    q_values = (0, 1, 2, 3, 10, 4095, 4096, 10_000_000, (1 << 32) - 2, (1 << 32) - 1)
    values: set[int] = {0, 1, (1 << 63) - 1, 1 << 63, UINT64_MAX}
    for q in q_values:
        for value in (q * q - 1, q * q, q * q + 1):
            if 0 <= value <= UINT64_MAX:
                values.add(value)
    for value in sorted(values):
        expected = int(oracle(oracle_binary, "--isqrt", value)["floor_sqrt"])
        assert expected * expected <= value < (expected + 1) * (expected + 1)
        for executable, _ in SCANNERS:
            actual = scanner_seam(bin_dir / executable, "--test-isqrt", value)
            root = int(actual["floor_sqrt"])
            assert actual["implementation_id"] == executable
            assert root == expected
            # Python integers are unbounded; this check cannot overflow in the
            # same way as the uint64 production helper under test.
            assert root * root <= value < (root + 1) * (root + 1)


def assert_rejected(command: list[str], fragment: str) -> None:
    completed = run(command)
    assert completed.returncode != 0, f"out-of-range command unexpectedly succeeded: {command!r}"
    assert "ERROR" in completed.stderr, completed.stderr
    assert fragment in completed.stderr, completed.stderr


def test_range_contract(bin_dir: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="a303656-range-contract-") as text:
        directory = Path(text)
        for executable, _ in SCANNERS:
            binary = bin_dir / executable
            for value in (str(1 << 64), str(1 << 65), "-1", "+1", "1x"):
                assert_rejected([str(binary), "--test-isqrt", value], "ERROR")

            # Maximum power exponents used by the normal scanner are chosen so
            # both the power and the next-domain sentinel remain uint64-safe.
            for option, value in (("--C", "40"), ("--D", "27")):
                output = directory / f"{executable}-{option[2:]}.json"
                assert_rejected(
                    [
                        str(binary), "--low", "1", "--high", "2",
                        "--C", "0", "--D", "0", option, value,
                        "--json", str(output), "--quiet",
                    ],
                    "supported uint64 exponent range",
                )
                assert not output.exists()

            # 2^63-1, 2^63, and 2^64-1 parse exactly, then fail on the explicit
            # finite-domain contract before interval allocation.  2^64/2^65
            # fail during parsing, so none can wrap into a plausible run.
            for high in ((1 << 63) - 1, 1 << 63, UINT64_MAX):
                output = directory / f"{executable}-{high}.json"
                assert_rejected(
                    [
                        str(binary), "--low", str(high), "--high", str(high),
                        "--C", "39", "--D", "26", "--json", str(output), "--quiet",
                    ],
                    "domain",
                )
                assert not output.exists()
            for high in (1 << 64, 1 << 65):
                output = directory / f"{executable}-{high}.json"
                assert_rejected(
                    [
                        str(binary), "--low", "1", "--high", str(high),
                        "--C", "0", "--D", "0", "--json", str(output), "--quiet",
                    ],
                    "out of uint64 range",
                )
                assert not output.exists()

            # Activation arithmetic checks 3^c, 5^d, subtraction at s/s+1,
            # and fail-closed addition when individually valid powers overflow
            # their uint64 shift sum.
            fit = scanner_seam(
                binary,
                "--test-activation-c", 40,
                "--test-activation-d", 0,
                "--test-activation-n", 12157665459056928802,
            )
            assert int(fit["shift"]) == 3**40 + 1
            assert int(fit["remainder"]) == 0
            fit = scanner_seam(
                binary,
                "--test-activation-c", 0,
                "--test-activation-d", 27,
                "--test-activation-n", 7450580596923828126,
            )
            assert int(fit["shift"]) == 1 + 5**27
            overflow = run(
                [
                    str(binary),
                    "--test-activation-c", "40",
                    "--test-activation-d", "27",
                    "--test-activation-n", str(UINT64_MAX),
                ]
            )
            assert overflow.returncode != 0
            assert "ERROR activation shift overflow" in overflow.stderr

            # Directly exercise the widened a*a, b*b, a*a+b*b and endpoint
            # addition contract used after annulus enumeration.  Expected
            # values are evaluated with Python's independent big integers.
            coordinate = (1 << 32) - 1
            square_sum = coordinate * coordinate
            exact_shift = UINT64_MAX - square_sum
            arithmetic = scanner_seam(
                binary,
                "--test-arithmetic-a", 0,
                "--test-arithmetic-b", coordinate,
                "--test-arithmetic-shift", exact_shift,
            )
            assert int(arithmetic["a_squared"]) == 0
            assert int(arithmetic["b_squared"]) == square_sum
            assert int(arithmetic["square_sum"]) == square_sum
            assert int(arithmetic["represented_n"]) == UINT64_MAX
            balanced = 3_037_000_499
            arithmetic = scanner_seam(
                binary,
                "--test-arithmetic-a", balanced,
                "--test-arithmetic-b", balanced,
                "--test-arithmetic-shift", 0,
            )
            assert int(arithmetic["a_squared"]) == balanced * balanced
            assert int(arithmetic["b_squared"]) == balanced * balanced
            assert int(arithmetic["square_sum"]) == 2 * balanced * balanced <= UINT64_MAX
            assert_rejected(
                [
                    str(binary),
                    "--test-arithmetic-a", "3037000500",
                    "--test-arithmetic-b", "3037000500",
                    "--test-arithmetic-shift", "0",
                ],
                "square sum exceeds uint64 remainder contract",
            )
            assert_rejected(
                [
                    str(binary),
                    "--test-arithmetic-a", "0",
                    "--test-arithmetic-b", str(coordinate),
                    "--test-arithmetic-shift", str(exact_shift + 1),
                ],
                "represented n overflow",
            )
            assert_rejected(
                [
                    str(binary),
                    "--test-arithmetic-a", "0",
                    "--test-arithmetic-b", str(1 << 32),
                    "--test-arithmetic-shift", "0",
                ],
                "square coordinate exceeds uint64-remainder contract",
            )


def test_multiplicity(binary: Path) -> None:
    result = json_stdout([str(binary)])
    assert result["schema"] == "a303656-exponent-pair-multiplicity-test-v1"
    assert int(result["distinct_shift_evaluations"]) == 1
    assert int(result["T"]) == 2
    successes = result["successes"]
    assert len(successes) == 2
    assert [(int(row["c"]), int(row["d"])) for row in successes] == [(1, 2), (3, 0)]
    assert {int(row["shift"]) for row in successes} == {28}


def arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--bin-dir", type=Path, required=True)
    parser.add_argument("--oracle", type=Path, required=True)
    parser.add_argument("--multiplicity-test", type=Path, required=True)
    return parser.parse_args()


def main() -> int:
    args = arguments()
    test_intervals(args.bin_dir, args.oracle)
    test_annuli(args.bin_dir, args.oracle)
    test_activation(args.bin_dir)
    test_isqrt(args.bin_dir, args.oracle)
    test_range_contract(args.bin_dir)
    test_multiplicity(args.multiplicity_test)
    print("DIRECT_BOUNDARY_PROPERTY_TESTS_PASS")
    print("covered=per-n,marked-sets,endpoints,annuli,isqrt,activation,uint64,arithmetic,multiplicity")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
