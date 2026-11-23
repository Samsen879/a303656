#!/usr/bin/env python3
"""Cross-check concrete claims, proof algebra, malformed submissions and tail boundaries."""
import copy
import itertools
import json
import math
import sys
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "src"), str(ROOT / "scripts")]
import ajt5_integer_certificates as cert
import verify_ajt5_palette as palette
from ajt5_first_c import construct

FIX = ROOT / "analysis/ajt5_integer_certificates/fixtures"


def fixture(name):
    return json.loads((FIX / name).read_bytes())


def square(value):
    for a in range(math.isqrt(value)+1):
        b = math.isqrt(value-a*a)
        if a*a+b*b == value:
            return a, b
    return None


def oracle(x, side):
    positives, negatives = [], []
    for d in range(x.bit_length()):
        if 5**d+1 > x:
            break
        units = []
        first = None
        for c in range(x.bit_length()):
            v = x-5**d-3**c
            if v < 0:
                break
            witness = square(v)
            if witness is None:
                # Trial division to extract an entire odd inert prime power.
                for p in range(3, v+1, 4):
                    if v % p or any(p % j == 0 for j in range(2, math.isqrt(p)+1)):
                        continue
                    cofactor = v
                    while cofactor % p == 0:
                        cofactor //= p
                    u = v//cofactor
                    if u % 4 == 3:
                        units.append(dict(c=c, u=u))
                        break
                else:
                    raise ArithmeticError(v)
            elif first is None:
                first = dict(side=side, d=d, c=c, a=witness[0], b=witness[1])
        if first is None:
            negatives.append(dict(side=side, d=d, units=units))
        else:
            positives.append(first)
    return positives, negatives


class IntegerCertificates(unittest.TestCase):
    def test_unitary_equivalence(self):
        for v in range(1501):
            blocked = any(cert.unit_proves_negative(v, u) for u in range(1, v+1))
            self.assertEqual(blocked, square(v) is None)
        self.assertFalse(cert.unit_proves_negative(45, 15))
        self.assertTrue(cert.unit_proves_negative(60, 15))
        self.assertTrue(cert.unit_proves_negative(27, 27))
        self.assertFalse(cert.unit_proves_negative(0, 3))

    def test_independent_oracle(self):
        for m in range(2, 160):
            pp, pn = oracle(m, "parent")
            ep, en = oracle(m, "target")
            self.assertEqual(cert.verify(dict(kind="EMPTY_D", n=m, positive=ep,
                                              negative=en))["status"], "REFUTED")
            for r in range(5):
                cp, cn = oracle(5*m+r, "child")
                row = dict(kind="NO_BRIDGE", m=m, r=r, positive=pp+cp, negative=pn+cn)
                verdict = cert.verify(row)
                true_edges = {(x["d"], y["d"]) for x in pp for y in cp if y["d"]-x["d"] in (0, 1)}
                self.assertEqual(verdict["status"], "REFUTED")
                self.assertIn(tuple(verdict["bridge"]), true_edges)
                row["positive"] = pp
                self.assertEqual(cert.verify(row)["status"], "PARTIAL")

    def test_unknown_and_covered_edges(self):
        # All three-valued column assignments on three parent and four child bits.
        for assignment in itertools.product("+-?", repeat=7):
            p, q = assignment[:3], assignment[3:]
            pos = lambda v: {i for i, s in enumerate(v) if s == "+"}
            neg = lambda v: {i for i, s in enumerate(v) if s == "-"}
            result = cert.edge_verdict(3, pos(p), pos(q), neg(p), neg(q))
            edges = [(p[j], q[e]) for j in range(3) for e in (j, j+1)]
            if ("+", "+") in edges or p == ("-", "-", "-"):
                expected = "REFUTED"
            elif "+" in p and all("-" in edge for edge in edges):
                expected = "VERIFIED_NO_BRIDGE"
            else:
                expected = "PARTIAL"
            self.assertEqual(result["status"], expected)
        for assignment in itertools.product("+-?", repeat=3):
            positive = {i for i, symbol in enumerate(assignment) if symbol == "+"}
            negative = {i for i, symbol in enumerate(assignment) if symbol == "-"}
            result = cert.empty_verdict(3, positive, negative)
            expected = "REFUTED" if positive else ("PARTIAL" if "?" in assignment else "VERIFIED_EMPTY_D")
            self.assertEqual(result["status"], expected)
        self.assertEqual(cert.child_classification(3, {2}, {0, 1}), "AJT5_ONLY_AT_CHILD")
        self.assertEqual(cert.child_classification(3, set(), {0, 1, 2}), "SUN_FAILURE_AT_CHILD")
        self.assertEqual(cert.child_classification(3, set(), {0, 1}), "CHILD_EXISTENCE_UNKNOWN")

    def test_composite_mutant(self):
        row = fixture("nonunitary_1339.json")
        bad = []
        covered = {"parent": set(), "child": set()}
        for col in row["negative"]:
            side, d = col["side"], col["d"]
            bound = (1339 if side == "parent" else 6698) - 5**d
            self.assertEqual([a["c"] for a in col["units"]],
                             [c for c in range(10) if 3**c <= bound])
            for atom in col["units"]:
                u = atom["u"]
                v = bound-3**atom["c"]
                self.assertEqual(v % u, 0)
                self.assertEqual(u % 4, 3)
                self.assertNotEqual(v//u % u, 0)  # weak exact order-one test
                if math.gcd(u, v//u) != 1:
                    bad.append((v, u))
            covered[side].add(d)
        self.assertEqual(bad, [(6664, 119), (6570, 15)])
        self.assertEqual(cert.edge_verdict(5, {1}, set(), covered["parent"],
                                          covered["child"])["status"], "VERIFIED_NO_BRIDGE")
        with self.assertRaisesRegex(ValueError, "unitary"):
            cert.verify(row)
        pp, _ = oracle(1339, "parent")
        cp, _ = oracle(6698, "child")
        self.assertEqual({(x["d"], y["d"]) for x in pp for y in cp if y["d"]-x["d"] in (0, 1)},
                         {(1, 2), (2, 2), (2, 3), (3, 3)})
        row.update(positive=pp+cp, negative=[])
        self.assertEqual(cert.verify(row)["status"], "REFUTED")

    def test_tail_and_crt(self):
        row = fixture("c12_partial.json")
        self.assertEqual(cert.verify(row)["status"], "PARTIAL")
        self.assertEqual([m-125-3**12 for m in (531565, 531566, 531567)], [-1, 0, 1])
        for m in range(531566, 531583):
            at12 = square(m-125-3**12)
            earlier = any(square(m-125-3**c) for c in range(12))
            self.assertEqual(at12 is not None and not earlier, m == 531582)
        row["positive"] = [dict(side="target", d=3, c=12, a=0, b=4)]
        self.assertEqual(cert.verify(row)["status"], "REFUTED")
        for m, a in ((531566, 0), (531567, 1)):
            row.update(n=m, negative=[], positive=[dict(side="target", d=3, c=12, a=a, b=0)])
            self.assertEqual(cert.verify(row)["status"], "REFUTED")
        row["n"] = 531565
        with self.assertRaisesRegex(ValueError, "inactive c"):
            cert.verify(row)
        self.assertEqual([m-5**7-3**12 for m in (547067, 609565, 609566)],
                         [-62499, -1, 0])
        self.assertEqual([5*m+r-25-3**14 for m,r in ((956598, 3), (956598, 4), (956599, 3))],
                         [-1, 0, 4])
        for d in (0, 3, 8):
            for c in (0, 1, 12, 15):
                point = construct(d, c)
                n = point["m"]
                self.assertEqual(n-5**d-3**c, point["a"]**2+point["b"]**2)
                prior = point["prior"]
                self.assertEqual(len({a["u"] for a in prior}), c)
                for j, atom in enumerate(prior):
                    v = n-5**d-3**j
                    p = atom["u"]
                    self.assertEqual((atom["c"], p % 4, v % (p*p)), (j, 3, p))
                    self.assertTrue(all(p % k for k in range(2, math.isqrt(p)+1)))

    def test_strict_input(self):
        row = dict(kind="EMPTY_D", n=2, positive=[dict(side="target", d=0, c=0, a=0, b=0)],
                   negative=[])
        for key,value in (("hidden_mask", 1), ("n", True), ("n", 2.0), ("positive", {}),
                          ("positive", row["positive"]*2), ("n", 1)):
            raw = json.dumps({**row, key: value}).encode()
            self.assertEqual(cert.inspect(raw)["status"], "INVALID")
        for raw in (b'{"n":2,"n":3}', b'{"x":NaN}', b'{"x":Infinity}', b'{} trailing', b'\xff'):
            self.assertEqual(cert.inspect(raw)["status"], "INVALID")
        self.assertEqual(cert.inspect(b'['*2000+b']'*2000)["status"], "UNKNOWN_RESOURCE")
        self.assertEqual(cert.inspect(b'1'*1300)["status"], "UNKNOWN_RESOURCE")
        self.assertEqual(cert.inspect(b' '*(cert.MAX_BYTES+1))["status"], "UNKNOWN_RESOURCE")
        self.assertEqual(cert.parse(b'9'*1000) % 100, 99)
        for d,c,u in ((1, 0, 3), (0, 1, 3), (0, 0, 3), (0, 0, False)):
            row["negative"] = [dict(side="target", d=d, units=[dict(c=c, u=u)])]
            self.assertEqual(cert.inspect(json.dumps(row).encode())["status"], "INVALID")
        base = dict(kind="EMPTY_D", n=16, positive=[],
                    negative=[dict(side="target", d=1, units=[dict(c=0, u=3)])])
        # 16-5-1=10 is positive S2. An unused bogus row must still fail.
        self.assertEqual(cert.inspect(json.dumps(base).encode())["status"], "INVALID")
        row = fixture("nonunitary_1339.json")
        row["negative"] = row["negative"][:1]
        self.assertEqual(cert.verify(row)["status"], "PARTIAL")
        for mutate in (lambda r: r["negative"].append(r["negative"][0]),
                       lambda r: r["negative"][0]["units"].append(r["negative"][0]["units"][0]),
                       lambda r: r["positive"][0].update(a=1),
                       lambda r: r["positive"][0].update(side="target"),
                       lambda r: r.update(n=6698)):
            corrupt = copy.deepcopy(row)
            mutate(corrupt)
            self.assertEqual(cert.inspect(json.dumps(corrupt).encode())["status"], "INVALID")

    def test_false_palette_edge(self):
        def surviving(x, d):
            for c in range(x.bit_length()):
                v = x-5**d-3**c
                if v < 0:
                    return False
                if v == 0:
                    return True
                h = 0
                while v % 3 == 0:
                    v //= 3
                    h += 1
                if h % 2 == 0:
                    return True
            return False
        for x, d in ((16, 0), (83, 1)):
            self.assertTrue(surviving(x, d))
            self.assertNotIn(d, {row["d"] for row in oracle(x, "target")[0]})

    def test_root_difference_completeness(self):
        roots = {-2, 0, 5, 8, 14, 16, 27, 28, 31, 36, 78, 130}
        expected = {}
        for p in range(7, max(roots)-min(roots)+1, 4):
            if any(p % k == 0 for k in range(2, p)):
                continue
            groups = {k: {a for a in roots if a % p == k} for k in range(p)}
            repeated = {k: g for k, g in groups.items() if len(g) > 1}
            if repeated:
                expected[p] = repeated
        self.assertEqual(palette.catalogue(roots), expected)
        # The last of 129 distinct roots must survive integer-mask indexing.
        large = list(range(128)) + [391]
        self.assertTrue(any(mask & (1 << 128) for mask in palette.maximal_masks(large, 1)))

    def test_fixed_no3_window(self):
        point = fixture("no3_23_window.json")
        m, q, seed = point["m"], point["palette"], point["seed"]
        self.assertEqual(len(set(q)), 23)
        for p in q:
            self.assertTrue(p > 3 and p % 4 == 3 and all(p % t for t in range(2, math.isqrt(p)+1)))
        a, b = seed["a"], seed["b"]
        self.assertEqual((seed["d"], seed["c"], m), (7, 0, a*a+b*b+5**7+1))
        self.assertEqual(5*m+4, (a-2*b)**2+(2*a+b)**2+5**8+9)
        used = set()
        for d in range(7):
            for c in range(13):
                v = m-5**d-3**c
                self.assertGreater(v, 0)
                hits = {p for p in q if v % p == 0 and v % (p*p)}
                self.assertTrue(hits)
                used.update(hits)
        self.assertEqual(used, set(q))

    def test_palette_semantics(self):
        rows = palette.labels("no3_22", 3, 2)
        self.assertEqual((len(rows), len(set(rows.values()))), (104, 103))
        self.assertEqual(list(rows.values()).count(140), 2)
        self.assertEqual(palette.labels("all14_d7", 4, 1)["Q", 0, 0], -2)
        self.assertIn(("P", 7, 4), palette.labels("no3_23", 0, 0))
        self.assertNotIn(("P", 7, 12), palette.labels("no3_23", 0, 0))
        self.assertIn(("Q", 8, 12), palette.labels("no3_23", 4, 128))
        self.assertEqual(len(palette.labels("no3_23", 4, 128)), 117)
        roots = [-2, 1, 4, 7, 25, 82]
        for k in range(3):
            found = set()
            for x in range(k, 3**7, 3):
                mask = 0
                for i, a in enumerate(roots):
                    v = x-a
                    sign = False
                    while v and v % 3 == 0:
                        v //= 3
                        sign = not sign
                    if sign:
                        mask |= 1 << i
                found.add(mask)
            self.assertEqual(palette.maximal_masks(roots, k),
                             {v for v in found if v and not any(v != w and v & w == v for w in found)})
        cat = palette.catalogue({0, 7, 1, 8})
        self.assertEqual(cat, {7: {0: {0, 7}, 1: {1, 8}}})
        # With one color, paying 7 covers one class; the other class survives.
        leaf = [1, [1, 1]]
        none = [1, [1]*4]
        tree = [7, [[None, none], [0, leaf], [1, leaf]]]
        palette.check_tree(tree, {0, 1, 7, 8}, cat, 1, Counter())
        for bad in ([7, tree[1][1:]], [7, tree[1][:-1]], [7, tree[1]+[tree[1][1]]],
                    [7, [[None, [1, [0, 0, 0, 1]]], *tree[1][1:]]],
                    [1, [0, 1, 0, 0]], [1, [True, 1, 1, 1]], [1, [1]*3]):
            with self.assertRaises(ValueError):
                palette.check_tree(bad, {0, 1, 7, 8}, cat, 1, Counter())


if __name__ == "__main__":
    unittest.main(verbosity=2)
