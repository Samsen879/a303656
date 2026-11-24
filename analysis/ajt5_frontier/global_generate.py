#!/usr/bin/env python3
"""Search for R5 proofs. Optional SciPy dependency, no role in acceptance."""
import argparse
import gzip
import json
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "scripts"))
import generate_ajt5_palette_proofs as search


def prove_all(r, mask):
    roots = search.obligations(r, mask, 7, 13)
    groups = search.catalogue(roots)
    active = set(range(len(roots)))
    result = [search.solve(active, groups, 15)]
    for residue in range(3):
        coarse = {i for i in active if roots[i] % 3 == residue}
        kept = active - coarse
        classes = [(p, k, live) for p, k, group in groups
                   if len(live := [i for i in group if i in kept]) >= 2]
        leaf = search.dual(kept, classes, 14)
        if leaf:
            result.append(["coarse", leaf])
        else:
            refined = [[hex(sum(1 << i for i in m)), search.solve(active - m, groups, 14)]
                       for m in search.maximal3(roots) if m and m <= coarse]
            result.append(["exact", refined])
    return result


def prove_no3(r, mask):
    roots = search.obligations(r, mask, 7, 12)
    if mask:
        systems = [roots]
    else:
        # If d=8 survives, child e=8 must be blocked. Otherwise the
        # parent at d=8 must be blocked. Each is a separate obligation.
        c = (1, 2, 5, 2, 4)[r]
        systems = [sorted(set(roots) | {5 * (5**8 + 3)}),
                   sorted(set(roots) | {5**8 + 3**c - r})]
    return [search.solve(set(range(len(s))), search.catalogue(s), 24) for s in systems]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("variant", choices=("all15", "no3_24"))
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    prove = prove_all if args.variant == "all15" else prove_no3
    with tempfile.TemporaryDirectory(dir=args.output.parent) as tmp:
        path = Path(tmp) / "proof"
        with path.open("wb") as raw, gzip.GzipFile(filename="", fileobj=raw, mode="wb", mtime=0) as out:
            for r in range(5):
                for mask in range(256):
                    if args.variant == "no3_24" and mask != (mask | ((mask << 1) & (mask >> 1) & 255)):
                        continue
                    try:
                        tree = prove(r, mask)
                    except Exception as exc:
                        raise RuntimeError((args.variant, r, mask)) from exc
                    out.write((json.dumps([r, mask, tree], separators=(",", ":")) + "\n").encode())
                print(args.variant, "completed digit", r, flush=True)
        path.replace(args.output)


if __name__ == "__main__":
    main()
