"""Optional SciPy search for the W1 cover exclusion. Write one line per case."""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from generate_ajt5_palette_proofs import catalogue, solve


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    roots = set()
    for d in [1, 2, 3, 4, 5, 7]:
        for c in range(12 if d == 7 else 10):
            roots.add(5 * (5**d + 3**c))
    for e in [0, 1, 6, 7]:
        for c in range(12 if e == 0 else 11):
            roots.add(5**e + 3**c - 4)
    roots = sorted(roots)
    colors = catalogue(roots)
    with args.output.open("x") as stream:
        for residue in [None, *range(27)]:
            live = set(range(len(roots)))
            if residue is not None:
                live = {i for i in live if (residue - roots[i]) % 3
                        or (residue - roots[i]) % 9 == 0 and (residue - roots[i]) % 27 != 0}
            tree = solve(live, colors, 15 if residue is None else 14)
            print(json.dumps([residue, tree], separators=(",", ":")), file=stream)


if __name__ == "__main__":
    main()
