#!/usr/bin/env python3
"""Independent small oracles, malformed certificates, and R2 custody checks."""
from __future__ import annotations

import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ajt5_gates import (certificate, classify_exact, exponents, forbidden36,  # noqa: E402
                        lambda_dp, margins, powers, summary, verify_gate)
from verify_ajt5_gates import (check_ledger, describe, make_complete, rows,  # noqa: E402
                                verify_directory)

EVIDENCE = ROOT / "analysis/ajt5_gate_certificates/results"


class GateTests(unittest.TestCase):
    def test_abstract_soundness_and_nondominance(self):
        for L in range(5):
            for offset in range(min(20, 4 * 5 ** L)):
                m = 5 ** L + offset
                if m < 2:
                    continue
                F = forbidden36(m, L)
                for d in range(1 << (L + 1)):
                    D = exponents(d)
                    if D & F:
                        continue  # residue proof requires D disjoint F
                    for e in range(1 << (L + 2)):
                        E = exponents(e)
                        values = margins(summary(m, D, E))
                        if any(values[name] > 0 for name in ("gF", "gB", "PB2", "delta36", "PB36")):
                            self.assertTrue(any(x in E or x + 1 in E for x in D))
        control = margins(summary(125, {0, 3}, {0, 1}))
        self.assertEqual((control["gF"], control["PB2"], control["K"]), (1, 0, 1))

    def test_lambda_independent_exhaustive_and_single_vertex_deletions(self):
        # Independent enumeration of every eligible X, including empty X.
        for L in range(6):
            for e in range(1 << (L + 2)):
                E, oracle = exponents(e), {}
                for d in range(1 << (L + 1)):
                    X = exponents(d)
                    key = len(X), sum(i - 1 not in X for i in X)
                    edges = {(i, j) for i in X for j in E if j in (i, i + 1)}
                    oracle[key] = min(oracle.get(key, 10**9), len(edges))
                for (size, runs), optimum in oracle.items():
                    self.assertEqual(lambda_dp(L, size, runs, E), optimum)
                for d in range(1 << (L + 1)):
                    X = exponents(d)
                    key = len(X), sum(i - 1 not in X for i in X)
                    if oracle[key] >= 3:
                        for side, vertices in ((0, X), (1, E)):
                            for vertex in vertices:
                                left = X - {vertex} if side == 0 else X
                                right = E - {vertex} if side == 1 else E
                                self.assertTrue(any(i in right or i + 1 in right for i in left))

    def test_mod36_positive_residual_classes(self):
        for k in range(1000):
            t = 24 + 36 * k
            for c, three in enumerate(powers(3, t)):
                x = t - three
                self.assertGreater(x, 0)
                if c % 2 == 0:
                    self.assertEqual(x % 4, 3)
                else:
                    self.assertEqual(x % 9, 3 if c == 1 else 6)
                    self.assertNotEqual(x % 9, 0)  # v3 exactly 1

    def test_certificate_mutations_partial_and_scope_routes(self):
        examples = json.loads((EVIDENCE / "examples.json").read_text())
        for rec in examples["complete"] + examples["lower"]:
            self.assertEqual(verify_gate(rec)["status"], "SUFFICIENT_BRIDGE")
            self.assertEqual(classify_exact(rec), "UNKNOWN")
        original = examples["complete"][0]
        mutated = []
        for key, value in (("m", 10_000_001), ("r", 5), ("r", True), ("schema", True),
                           ("mode", "untrusted"), ("parent", {}), ("child", None), ("summary", {})):
            c = copy.deepcopy(original); c[key] = value; mutated.append(c)
        c = copy.deepcopy(original); c["summary"]["d_parity"][0] += 1; mutated.append(c)
        c = copy.deepcopy(original); c["summary"]["e_size"] = float(c["summary"]["e_size"]); mutated.append(c)
        c = copy.deepcopy(original); c["child"]["by_d"].pop(); mutated.append(c)
        c = copy.deepcopy(original); c["parent"]["mask"] ^= 1; mutated.append(c)
        p = copy.deepcopy(examples["lower"][0]); p["parent"]["witnesses"][0][1] += 1; mutated.append(p)
        p = copy.deepcopy(examples["lower"][0]); p["parent"]["witnesses"].append(p["parent"]["witnesses"][0]); mutated.append(p)
        for c in mutated:
            self.assertEqual(verify_gate(c)["status"], "UNKNOWN")
            self.assertEqual(classify_exact(c), "UNKNOWN")
        # True integer cases remain UNKNOWN when their partial data proves no gate.
        empty = certificate(2, 0, {"n": 2, "witnesses": []}, {"n": 10, "witnesses": []}, "lower")
        self.assertEqual(verify_gate(empty)["status"], "UNKNOWN")
        self.assertEqual(classify_exact(empty), "UNKNOWN")
        for n in (5, 6, 24, 25, 26, 124, 125, 126):
            m = max(2, n // 5)
            r = n - 5 * m
            if 0 <= r < 5:
                self.assertEqual(verify_gate(certificate(m, r, make_complete(m), make_complete(n)))["status"], "SUFFICIENT_BRIDGE")
        zero = {"n": 2, "mask": 1, "by_d": [[0, 0, 0]]}
        self.assertEqual(verify_gate(certificate(2, 0, zero, make_complete(10)))["status"], "SUFFICIENT_BRIDGE")
        bad = copy.deepcopy(zero); bad["by_d"] = [[[3, 1]]]; bad["mask"] = 0
        self.assertEqual(verify_gate(certificate(2, 0, bad, make_complete(10)))["status"], "UNKNOWN")

    def test_ledger_mutations_and_zero(self):
        actual = rows(EVIDENCE / "hard_ledger.csv")
        targets = {r["n"] for r in actual}
        self.assertEqual(check_ledger(actual, targets)["alternatives"], 469)
        for field, value in (("p", 15), ("v", 2), ("residual", 0), ("c", 100)):
            changed = copy.deepcopy(actual)
            next(row for row in changed if row["p"])[field] = value
            with self.assertRaises(ValueError):
                check_ledger(changed, targets)
        with self.assertRaises(ValueError):
            check_ledger(actual[:-1], targets)
        good = [{"n": 2, "d": 0, "c": 0, "residual": 0, "a": 0, "b": 0, "p": 0, "v": 0}]
        self.assertEqual(check_ledger(good, {2})["zero_residual_witnesses"], 1)
        good[0].update(a=-1, b=-1, p=3, v=1)
        with self.assertRaises(ValueError):
            check_ledger(good, {2})

    def test_stored_evidence_and_semantic_mutations(self):
        self.assertEqual(verify_directory(EVIDENCE)["critical_pairs"], 534)
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "evidence"
            for mutation in ("critical_omit", "accounting", "summary", "cert", "ledger"):
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(EVIDENCE, dest)
                if mutation == "critical_omit":
                    p = dest / "critical.csv"; p.write_text("\n".join(p.read_text().splitlines()[:-1]) + "\n")
                if mutation in ("summary", "accounting"):
                    p = dest / (mutation + ".json"); value = json.loads(p.read_text())
                    if mutation == "summary": value["PB2"]["1"][0] += 1
                    else: value["lambda_below_3_by_r"][0] += 1
                    p.write_text(json.dumps(value))
                if mutation == "cert":
                    p = dest / "certificates.jsonl"; p.write_text("\n".join(p.read_text().splitlines()[:-1]) + "\n")
                if mutation == "ledger":
                    p = dest / "hard_ledger.csv"; p.write_text("\n".join(p.read_text().splitlines()[:-1]) + "\n")
                with self.subTest(mutation=mutation), self.assertRaises((ValueError, KeyError)):
                    verify_directory(dest, False)

    def test_native_full_small_domain_and_bad_tables(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = Path(tmp)
            for source, binary in (("ajt5_scan.cpp", "input"), ("ajt5_gate_scan.cpp", "gate")):
                subprocess.run(["g++", "-std=c++17", "-O2", "-Wall", "-Wextra", "-Werror", str(ROOT / "src" / source), "-o", str(p / binary)], check=True)
            subprocess.run([str(p / "input"), "200", str(p / "input-data")], check=True, capture_output=True)
            table = p / "input-data/masks.u16le"
            subprocess.run([str(p / "gate"), "200", str(table), str(p / "output")], check=True, capture_output=True)
            data = table.read_bytes()
            masks = [int.from_bytes(data[i:i + 2], "little") for i in range(0, len(data), 2)]
            got = json.loads((p / "output/summary.json").read_text())
            independent = {key: {} for key in ("PB2", "PB36", "delta36", "K")}
            for m in range(2, 201):
                for r in range(5):
                    v = margins(summary(m, exponents(masks[m]), exponents(masks[5 * m + r])))
                    for key in independent:
                        bucket = independent[key].setdefault(str(v[key]), [0] * 5); bucket[r] += 1
            self.assertEqual({key: got[key] for key in independent}, independent)
            for changed in (data[:-1], data + b"\0", b"\xff\xff" + data[2:]):
                table.write_bytes(changed)
                self.assertNotEqual(subprocess.run([str(p / "gate"), "200", str(table), str(p / "bad")], capture_output=True).returncode, 0)
            table.write_bytes(data)
            for bound in ("1", "10000001", "-1", "2x", "18446744073709551616"):
                self.assertNotEqual(subprocess.run([str(p / "gate"), bound, str(table), str(p / "bad")], capture_output=True).returncode, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
