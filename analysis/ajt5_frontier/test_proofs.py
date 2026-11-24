"""Mutate the R5 proof format and independently check the orientation reduction."""
import gzip
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import empty_verify
import global_verify as g


class ProofChecks(unittest.TestCase):
    def test_direction_geometry(self):
        for r in range(5):
            base = {5 * (5**d + 3**c) for d in range(8) for c in range(13)
                    if (d, c) != (7, 12)}
            tails = g.systems("no3_24", r, 0)
            self.assertEqual(tails, [base | {1953140},
                                     base | {(390628, 390633, 390866, 390631, 390702)[r]}])
            closure = set()
            for mask in range(256):
                inside = {d for d in range(8) if mask & (1 << d)}
                edges = inside | {d+1 for d in inside}
                kept = {d for d in range(8) if {d, d+1} <= edges}
                closed = sum(1 << d for d in kept)
                self.assertEqual(closed, mask | ((mask >> 1) & (mask << 1) & 255))
                closure.add(closed)
                parents = {5 * (5**d + 3**c) for d in range(8) if d not in inside
                           for c in range(13) if (d, c) != (7, 12)}
                for kind, count in (("all15", 14), ("no3_24", 13)):
                    children = {5**e + 3**c-r for e in edges for c in range(count)}
                    if kind == "all15" or mask:
                        self.assertEqual(g.systems(kind, r, mask), [parents | children])
            self.assertEqual(len(closure), 114)

    def test_bad_inequalities_and_branches(self):
        active = {0, 7, 1, 8}
        classes = g.catalogue(active)
        default = [None, [1, [1, 1, 1, 1]]]
        a, b = [0, [1, [1, 1]]], [1, [1, [1, 1]]]
        g.check_tree([7, [default, a, b]], active, classes, 1, Counter())
        for bad in (None, [True, [1]*4], [1, [1, 0, 0, 0]], [1, [1]*3],
                    [7, [a, b]], [7, [default, a]], [7, [default, a, a]],
                    [7, [[None, [7, [a, b]]], a, b]]):
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                g.check_tree(bad, active, classes, 1, Counter())

    def test_independent_mod27_refinement(self):
        refined = []
        with gzip.open(g.HERE / "global_all15.jsonl.gz", "rt") as src:
            for line in src:
                r, mask, tree = json.loads(line)
                for residue, (mode, subtrees) in enumerate(tree[1:]):
                    if mode != "exact":
                        continue
                    roots = sorted(g.systems("all15", r, mask)[0])
                    # Odd valuation means exactly one, or at least three.
                    # Removing all depths >=3 gives a sufficient upper mask.
                    masks = set()
                    for x in range(residue, 27, 3):
                        hit = sum(1 << i for i, k in enumerate(roots) if
                                  (x-k) % 3 == 0 and ((x-k) % 9 != 0 or (x-k) % 27 == 0))
                        masks.add(hex(hit))
                    self.assertEqual({tag for tag, _ in subtrees}, masks)
                    refined.append((r, mask, residue, len(masks)))
        self.assertEqual(refined, [(4, m, 1, 9) for m in (65, 80, 97, 112)])

    def test_missing_ternary_mask(self):
        # Test the actual refined global case even if its weights change.
        with gzip.open(g.HERE / "global_all15.jsonl.gz", "rt") as src:
            for line in src:
                r, mask, tree = json.loads(line)
                exact = next((p for kind, p in tree[1:] if kind == "exact" and p), None)
                if exact:
                    exact.pop()
                    break
            else:
                self.fail("no exact ternary control")
        active, = g.systems("all15", r, mask)
        with self.assertRaisesRegex(ValueError, "missing 3-adic mask"):
            g.check_all(tree, active, g.catalogue(active), Counter())
        proof = json.loads((g.HERE / "empty_proof.json").read_bytes())
        proof["with3"].pop()
        with self.assertRaisesRegex(ValueError, "missing maximal 3-mask"):
            empty_verify.replay(proof)

    def test_wrong_first_direction(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "bad.gz"
            with gzip.open(path, "wt") as stream:
                stream.write("[0,1,[]]\n")
            with self.assertRaisesRegex(ValueError, "incorrect proof order"):
                g.replay("all15", path)


if __name__ == "__main__":
    unittest.main(verbosity=2)
