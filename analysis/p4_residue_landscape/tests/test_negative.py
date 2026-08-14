#!/usr/bin/env python3
"""Negative and arithmetic tests for the independent fixed-P4 verifier."""

from __future__ import annotations

import hashlib
import importlib.util
import struct
import sys
import unittest
from pathlib import Path


VERIFIER_PATH = Path(__file__).resolve().parents[1] / "tools" / "verifier.py"
SPEC = importlib.util.spec_from_file_location("p4_landscape_verifier", VERIFIER_PATH)
assert SPEC is not None and SPEC.loader is not None
verifier = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = verifier
SPEC.loader.exec_module(verifier)


class StreamMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.domains = (range(2), range(2), range(2), range(2))
        cls.rows = []
        for t3 in cls.domains[0]:
            for t7 in cls.domains[1]:
                for t11 in cls.domains[2]:
                    for t23 in cls.domains[3]:
                        residues = (t3, t7, t11, t23)
                        coverage = sum(residues)
                        cls.rows.append(verifier.serialize_full_row(residues, coverage))
        cls.stream = b"".join(cls.rows)
        cls.digest = hashlib.sha256(cls.stream).hexdigest()
        cls.histogram = {0: 1, 1: 4, 2: 6, 3: 4, 4: 1}

    @classmethod
    def validate(cls, data: bytes, **overrides):
        kwargs = {
            "coordinate_values": cls.domains,
            "coverage_fn": sum,
            "expected_digest": cls.digest,
            "expected_histogram": cls.histogram,
            "expected_argmax_count": 1,
        }
        kwargs.update(overrides)
        return verifier.validate_tuple_stream_bytes(data, **kwargs)

    def test_valid_synthetic_stream(self) -> None:
        report = self.validate(self.stream)
        self.assertEqual(report["row_count"], 16)
        self.assertEqual(report["maximum"], 4)

    def test_rejects_altered_tuple_order(self) -> None:
        rows = list(self.rows)
        rows[5], rows[6] = rows[6], rows[5]
        with self.assertRaises(verifier.VerificationError):
            self.validate(b"".join(rows), expected_digest=None)

    def test_rejects_one_changed_coverage_value(self) -> None:
        changed = bytearray(self.stream)
        offset = 7 * verifier.FULL_ROW.size
        values = list(verifier.FULL_ROW.unpack(changed[offset : offset + verifier.FULL_ROW.size]))
        values[-1] += 1
        changed[offset : offset + verifier.FULL_ROW.size] = verifier.FULL_ROW.pack(*values)
        with self.assertRaises(verifier.VerificationError):
            self.validate(bytes(changed), expected_digest=None, expected_histogram=None)

    def test_rejects_missing_tuple(self) -> None:
        with self.assertRaises(verifier.VerificationError):
            self.validate(b"".join(self.rows[:8] + self.rows[9:]))

    def test_rejects_duplicated_tuple(self) -> None:
        rows = list(self.rows)
        rows[8] = rows[7]
        with self.assertRaises(verifier.VerificationError):
            self.validate(b"".join(rows), expected_digest=None)

    def test_rejects_truncated_stream(self) -> None:
        with self.assertRaises(verifier.VerificationError):
            self.validate(self.stream[:-1])

    def test_rejects_extra_bytes(self) -> None:
        with self.assertRaises(verifier.VerificationError):
            self.validate(self.stream + b"\x00")

    def test_rejects_altered_histogram(self) -> None:
        altered = dict(self.histogram)
        altered[1] -= 1
        altered[2] += 1
        with self.assertRaises(verifier.VerificationError):
            self.validate(self.stream, expected_histogram=altered)

    def test_rejects_altered_argmax_count(self) -> None:
        with self.assertRaises(verifier.VerificationError):
            self.validate(self.stream, expected_argmax_count=2)


class MathematicalMutationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.domain = verifier.generate_domain()
        cls.masks = verifier.build_coverage_masks(cls.domain)

    def test_domain_and_duplicate_shift(self) -> None:
        self.assertEqual(len(self.domain), 407)
        duplicate = [(c, d) for c, d, shift in self.domain if shift == 28]
        self.assertEqual(duplicate, [(1, 2), (3, 0)])

    def test_rejects_altered_n0_tuple(self) -> None:
        mutated = {"tuple": [2, 41, 74, 503], "coverage": 216}
        with self.assertRaises(verifier.VerificationError):
            verifier.validate_n0_section(mutated, self.masks)

    def test_n0_coverage_is_exact(self) -> None:
        verifier.validate_n0_section(
            {"tuple": list(verifier.N0_TUPLE), "coverage": verifier.N0_COVERAGE},
            self.masks,
        )

    def test_rejects_valuation_three_as_persistent(self) -> None:
        witness = None
        for prime in verifier.P4:
            for residue in range(prime * prime):
                for index, (_c, _d, shift) in enumerate(self.domain):
                    if verifier.p_adic_valuation(residue - shift, prime) == 3:
                        witness = (prime, residue, index)
                        break
                if witness:
                    break
            if witness:
                break
        self.assertIsNotNone(witness)
        prime, residue, index = witness
        with self.assertRaises(verifier.VerificationError):
            verifier.verify_coverage_membership(
                prime, residue, index, True, domain=self.domain
            )

    def test_all_coverage_sets_match_pair_centric_semantics(self) -> None:
        report = verifier.verify_coverage_semantics(self.domain, self.masks)
        self.assertEqual(set(report["per_prime"]), {"3", "7", "11", "23"})
        self.assertIsNotNone(report["valuation3_exclusion_witness"])

    def test_generalized_crt_and_activation_count(self) -> None:
        residue = verifier.crt_p4(verifier.N0_TUPLE)
        self.assertEqual(residue, verifier.N0 % verifier.M4)
        self.assertEqual(
            verifier.count_congruence_in_interval(
                residue, verifier.M4, verifier.CELL_LOW, verifier.CELL_HIGH
            ),
            2223,
        )
        self.assertEqual(
            verifier.nearest_congruence_in_interval(
                residue,
                verifier.M4,
                verifier.N0,
                verifier.CELL_LOW,
                verifier.CELL_HIGH,
            ),
            verifier.N0,
        )
        constrained_residue, constrained_modulus = verifier.generalized_crt(
            ((residue, verifier.M4), (verifier.N0 % 40, 40))
        )
        self.assertEqual(constrained_modulus, verifier.L_CONSTRAINED)
        self.assertEqual(constrained_residue, verifier.N0 % verifier.L_CONSTRAINED)

    def test_crt_artifact_shape_is_verified(self) -> None:
        residue = verifier.crt_p4(verifier.N0_TUPLE)
        row = {
            "tuple": list(verifier.N0_TUPLE),
            "r_mod_M4": residue,
            "count": verifier.count_congruence_in_interval(
                residue, verifier.M4, verifier.CELL_LOW, verifier.CELL_HIGH
            ),
            "nearest_to_n0": verifier.N0,
        }
        self.assertEqual(verifier.verify_crt_artifact({"rows": [row]}), 1)
        row["r_mod_M4"] += 1
        with self.assertRaises(verifier.VerificationError):
            verifier.verify_crt_artifact({"rows": [row]})

    def test_rejects_incompatible_generalized_crt(self) -> None:
        with self.assertRaises(verifier.VerificationError):
            verifier.generalized_crt(((0, 2), (1, 2)))

    def test_serialization_has_no_padding(self) -> None:
        self.assertEqual(verifier.FULL_ROW.size, 10)
        self.assertEqual(verifier.ARGMAX_ROW.size, 8)
        row = verifier.serialize_full_row((2, 41, 74, 504), 216)
        self.assertEqual(row, struct.pack("<HHHHH", 2, 41, 74, 504, 216))


if __name__ == "__main__":
    unittest.main()
