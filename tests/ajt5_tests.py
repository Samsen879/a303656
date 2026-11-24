#!/usr/bin/env python3
"""AJT5 small brute oracle, abstract gates, and adversarial evidence tests."""
from __future__ import annotations

import copy
import csv
import io
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from verify_ajt5_reports import (CAP, FIELDS, check_certificate, describe,  # noqa: E402
                               powers, verify_directory)


class AJT5Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.evidence = ROOT / "analysis/ajt5_exact_audit/results"
        cls.records = [json.loads(line) for line in (cls.evidence / "certificates.jsonl").read_text().splitlines()]

    def test_stored_evidence(self):
        self.assertEqual(verify_directory(self.evidence)["gate1_rows"], 220)

    def test_every_abstract_gate_at_small_levels(self):
        # Arbitrary masks, including empty ones: no representability assumption.
        for L in range(6):
            for parent in range(1 << (L + 1)):
                for child in range(1 << (L + 2)):
                    row = describe(5 ** L, 0, parent, child)
                    if row["defect1"] > 0 or row["defect2"] > 0:
                        self.assertGreater(row["bridge_edges"], 0)

    def test_boundaries_and_zero_residual(self):
        for base in (3, 5):
            for k in range(12):
                q = base ** k
                if q > CAP:
                    break
                self.assertEqual(powers(base, q)[-1], q)
                self.assertNotIn(q, powers(base, q - 1))
        self.assertEqual(check_certificate({"n": 2, "mask": 1, "by_d": [[0, 0, 0]]}), (2, 1))
        # A forged nonmembership at residual zero must fail closed.
        with self.assertRaises(ValueError):
            check_certificate({"n": 2, "mask": 0, "by_d": [[[3, 1]]]})
        # 5^d=n has no admissible c, and its empty blocker list is complete.
        self.assertEqual(check_certificate({"n": 5, "mask": 1, "by_d": [[1, 0, 1], []]}), (5, 1))
        self.assertEqual(check_certificate({"n": 26, "mask": 7, "by_d": [[0, 4, 2], [2, 4, 0], [0, 0, 0]]}), (26, 7))
        composite = {"n": 25, "mask": 2, "by_d": [[[23, 1], [3, 1], [15, 1]], [1, 4, 1], []]}
        with self.assertRaisesRegex(ValueError, "must be prime"):
            check_certificate(composite)

    def test_certificate_mutations(self):
        record = next(x for x in self.records if any(isinstance(e, list) and e and isinstance(e[0], list) for e in x["by_d"]))
        missing_d = next(i for i, e in enumerate(record["by_d"]) if e and isinstance(e[0], list))
        mutations = []
        r = copy.deepcopy(record); r["mask"] ^= 1; mutations.append(r)
        r = copy.deepcopy(record); r["by_d"].pop(); mutations.append(r)
        r = copy.deepcopy(record); r["by_d"][missing_d].pop(); mutations.append(r)
        r = copy.deepcopy(record); r["by_d"][missing_d][0][0] = 15; mutations.append(r)
        r = copy.deepcopy(record); r["by_d"][missing_d][0][0] = 5; mutations.append(r)
        r = copy.deepcopy(record); r["by_d"][missing_d][0][1] += 2; mutations.append(r)
        r = copy.deepcopy(record); r["by_d"][missing_d][0][1] = 2; mutations.append(r)
        r = copy.deepcopy(record); r["n"] = CAP + 1; mutations.append(r)
        r = copy.deepcopy(record); r["extra"] = 0; mutations.append(r)
        r = copy.deepcopy(record); r["mask"] = True; mutations.append(r)
        r = copy.deepcopy(record); r["mask"] |= 1 << 20; mutations.append(r)
        r = copy.deepcopy(self.records[0]); r["by_d"][0][0] += 1; mutations.append(r)
        r = copy.deepcopy(self.records[0]); r["by_d"][0][2] = 100000000; mutations.append(r)
        for r in mutations:
            with self.subTest(mutation=r), self.assertRaises(ValueError):
                check_certificate(r)

    def test_report_mutations_without_hash_shortcut(self):
        # Skip manifest checks here so the semantic checker must find the defect.
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp) / "evidence"
            for mutation in ("duplicate", "omitted", "forged_bridge", "mask", "gate", "fake_failure", "missing_cert"):
                if p.exists():
                    shutil.rmtree(p)
                shutil.copytree(self.evidence, p)
                rows = list(csv.DictReader(io.StringIO((p / "hard_cases.csv").read_text())))
                if mutation == "duplicate": rows.append(rows[0])
                if mutation == "omitted": rows.pop()
                if mutation == "forged_bridge": rows[0]["bridge_edges"] = "0"
                if mutation == "mask": rows[0]["parent_mask"] = "0"
                if mutation == "gate": rows[0]["defect2"] = "-1"
                if mutation == "fake_failure":
                    with (p / "failures.csv").open("w", newline="") as f:
                        w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerow(rows[0])
                if mutation == "missing_cert":
                    lines = (p / "certificates.jsonl").read_text().splitlines()
                    (p / "certificates.jsonl").write_text("\n".join(lines[:-1]) + "\n")
                with (p / "hard_cases.csv").open("w", newline="") as f:
                    w = csv.DictWriter(f, fieldnames=FIELDS); w.writeheader(); w.writerows(rows)
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    verify_directory(p, False)

    def test_native_small_brute_and_corrupted_raw_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            for source, binary in [("ajt5_scan.cpp", "scan"), ("ajt5_valuation_replay.cpp", "valuation")]:
                subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror",
                                str(ROOT / "src" / source), "-o", str(p / binary)], check=True)
            subprocess.run([str(p / "scan"), "200", str(p / "a")], check=True, capture_output=True)
            subprocess.run([str(p / "valuation"), "200", str(p / "a"), str(p / "b")], check=True, capture_output=True)
            end = 1004
            s2 = {a * a + b * b for a in range(32) for b in range(32) if a * a + b * b <= end}
            oracle = [0] * (end + 1)
            for d, five in enumerate(powers(5, end)):
                for three in powers(3, end - five):
                    for norm in s2:
                        if norm + three + five <= end:
                            oracle[norm + three + five] |= 1 << d
            data = (p / "a/masks.u16le").read_bytes()
            self.assertEqual(oracle, [int.from_bytes(data[i:i + 2], "little") for i in range(0, len(data), 2)])
            for file in ("s2.bits", "t.bits", "masks.u16le"):
                target = p / "a" / file
                original = target.read_bytes()
                for changed in (bytes([original[0] ^ 1]) + original[1:], original[:-1], original + b"\0"):
                    target.write_bytes(changed)
                    result = subprocess.run([str(p / "valuation"), "200", str(p / "a"), str(p / "b")], capture_output=True)
                    self.assertNotEqual(result.returncode, 0)
                target.write_bytes(original)
            for value in ("1", "10000001", "-2", "2x", "18446744073709551616"):
                for binary, extra in (("scan", [str(p / "a")]), ("valuation", [str(p / "a"), str(p / "b")])):
                    self.assertNotEqual(subprocess.run([str(p / binary), value, *extra], capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
