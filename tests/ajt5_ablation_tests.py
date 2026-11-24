#!/usr/bin/env python3
"""R3 exhaustive tiny oracles, strict modular proofs, and artifact mutations."""
import copy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from ajt5_ablation import diagnostics, optimum_dp, optimum_enumeration  # noqa: E402
from ajt5_gates import forbidden36  # noqa: E402
from ajt5_modular import (bounded_admissible_negative, child_summary, forbidden_residues,  # noqa: E402
                          residue_data, strict_negative, verify_residue_gate)
from verify_ajt5_ablation import compute, frozen_inputs, verify_directory  # noqa: E402
from verify_ajt5_reports import powers  # noqa: E402

EVIDENCE = ROOT / "analysis/ajt5_ablation/results"


class AblationTests(unittest.TestCase):
    def test_dp_every_tie_against_cartesian_oracle(self):
        # Both empty B and nonempty A, all mask pairs and several F patterns.
        for L in range(4):
            for m in sorted({max(2, 5**L), max(2, 5**L + 23)}):
                actualL = len(powers(5, m)) - 1
                F = sum(1 << i for i in forbidden36(m, actualL))
                if actualL != L:
                    continue
                for d in range(1, 1 << (L + 1)):
                    if d & F:
                        continue
                    for e in range(1 << (L + 2)):
                        self.assertEqual(optimum_dp(m, d, e), optimum_enumeration(m, d, e), (m, d, e))

    def test_recovery_soundness_on_abstract_masks(self):
        # Supplied complements really are complements of exact D/E here.
        for L in range(4):
            m = 5**L + 1
            for d in range(1, 1 << (L + 1)):
                for e in range(1 << (L + 2)):
                    _, tied = optimum_dp(m, d, e)
                    for a, b in tied:
                        z = diagnostics(m, d, e, a, b)
                        self.assertLessEqual(z["gF"], 0)
                        self.assertLessEqual(max(z["h"]), 0)
                        if max(z["parent_negative_margins"] + [z["gFH"]] + z["weight_gaps"]) > 0:
                            self.assertTrue(z["bridge"])

    def test_modular_entire_orbit_and_same_exponent(self):
        for M in (2, 3, 9, 16, 36, 144):
            s2, orbit, start = residue_data(M)
            brute_s2 = {(a*a + b*b) % M for a in range(M) for b in range(M)}
            self.assertEqual(s2, brute_s2)
            # A separately computed power sequence includes transient and cycles.
            self.assertEqual(set(orbit), {pow(3, c, M) for c in range(3*M)})
            self.assertEqual(3 * orbit[-1] % M, orbit[start])
            for t in range(M):
                negative = all((t - pow(3, c, M)) % M not in brute_s2 for c in range(3*M))
                self.assertEqual(strict_negative(t, M), negative)
        self.assertEqual(residue_data(144)[1:], ((1, 3, 9, 27, 81, 99), 2))
        self.assertEqual(forbidden_residues(144), (15, 24, 60, 87, 96, 111, 132, 141))
        # Separate existential c's at factors are insufficient; same c matters.
        self.assertFalse(strict_negative(141, 9))
        self.assertFalse(strict_negative(141, 16))
        self.assertTrue(strict_negative(141, 144))
        self.assertTrue(bounded_admissible_negative(0, 144))
        self.assertFalse(strict_negative(0, 144))
        # Every actual small square witness, including zero square residual,
        # survives the strict negative test. Modular passes are not witnesses.
        for a in range(9):
            for b in range(9):
                for c in range(6):
                    self.assertFalse(strict_negative(a*a + b*b + 3**c, 144))
        self.assertFalse(strict_negative(57, 144))  # passes modulo, not a square+3^c
        for M in (True, 1, 513, -1, 144.0, "144"):
            with self.assertRaises((ValueError, TypeError)):
                residue_data(M)

    def test_modular_certificate_positive_zero_and_malicious_mutations(self):
        control = json.loads((EVIDENCE / "controls.json").read_text())["mod144"]["certificate"]
        self.assertEqual(verify_residue_gate(control)["status"], "SUFFICIENT_BRIDGE")
        zero = copy.deepcopy(control)
        zero["negative_exponents"] = []
        zero["summary"] = child_summary(82, {0}, {0, 1}, set())
        self.assertEqual(verify_residue_gate(zero)["status"], "UNKNOWN")
        altered = []
        for key, value in (("schema", True), ("m", 10_000_001), ("m", 1), ("r", 5),
                           ("r", False), ("modulus", 513), ("modulus", 144.0),
                           ("negative_exponents", [0]), ("negative_exponents", [3, 3]),
                           ("negative_exponents", [-1]), ("negative_exponents", [10**9]),
                           ("negative_exponents", [True]), ("negative_exponents", [3]*10000),
                           ("summary", {}), ("child", None), ("parent", {})):
            c = copy.deepcopy(control); c[key] = value; altered.append(c)
        c = copy.deepcopy(control); c["parent"]["witnesses"][0][1] += 1; altered.append(c)
        c = copy.deepcopy(control); c["child"]["witnesses"].append(c["child"]["witnesses"][0]); altered.append(c)
        c = copy.deepcopy(control); c["summary"]["gFH"] = True; altered.append(c)
        for c in altered:
            self.assertEqual(verify_residue_gate(c)["status"], "UNKNOWN")
        # Valid zero-residual bit: 2=0²+0²+3⁰+5⁰, certified without exclusion.
        zero = {"schema": 1, "m": 2, "r": 0, "parent": {"n": 2, "witnesses": [[0, 0, 0, 0]]},
                "child": {"n": 10, "witnesses": []}, "modulus": 144, "negative_exponents": [],
                "summary": child_summary(2, {0}, set(), set())}
        self.assertEqual(verify_residue_gate(zero)["status"], "UNKNOWN")
        zero["parent"]["witnesses"][0][1] = -1
        self.assertIn("reason", verify_residue_gate(zero))

    def test_fixed_corpus_complete_optimum_replay_and_controls(self):
        result = verify_directory(EVIDENCE)
        self.assertEqual((result["keys"], result["states"]), (534, 3232))
        controls = json.loads((EVIDENCE / "controls.json").read_text())
        single = controls["single_child_bit"]
        self.assertEqual(single["result"]["status"], "UNKNOWN")
        self.assertTrue(single["retained_bridge"])
        self.assertEqual(controls["shared_global_mask_infeasible"]["keys"], [[2, 0], [10, 0]])
        selected, _, _ = frozen_inputs()
        with tempfile.TemporaryFile() as f:
            report, _ = compute(selected, f)
            f.seek(0)
            raw = f.read()
            self.assertEqual(hashlib.sha256(raw).hexdigest(), report["states_sha256"])
            self.assertEqual(len(raw.splitlines()), report["optimal_states"])

    def test_artifact_tampering_even_with_rehashed_manifest(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / "evidence"
            for mutation in ("report", "keys", "controls", "comparison", "receipt"):
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(EVIDENCE, dest)
                if mutation == "keys":
                    p = dest / "keys.csv"
                    p.write_text("\n".join(p.read_text().splitlines()[:-1]) + "\n")
                else:
                    p = dest / (mutation + ".json")
                    value = json.loads(p.read_text())
                    if mutation == "report": value["optimal_states"] -= 1
                    if mutation == "controls": value["mod144"]["certificate"]["negative_exponents"] = [0]
                    if mutation == "comparison": value["observed"]["sum_minimal_deletions"] += 1
                    if mutation == "receipt": value["input_sha256"] = {}
                    p.write_text(json.dumps(value))
                manifest = json.loads((dest / "manifest.json").read_text())
                manifest[p.name] = hashlib.sha256(p.read_bytes()).hexdigest()
                (dest / "manifest.json").write_text(json.dumps(manifest))
                with self.subTest(mutation=mutation), self.assertRaises(ValueError):
                    verify_directory(dest)

    def test_caps_and_invalid_abstract_masks(self):
        for m, d, e in ((1, 1, 0), (10_000_001, 1, 0), (True, 1, 0),
                        (2, 0, 0), (2, 2, 0), (2, 1, 4), (25, 1, 0)):
            with self.assertRaises(ValueError):
                optimum_dp(m, d, e)


if __name__ == "__main__":
    unittest.main(verbosity=2)
