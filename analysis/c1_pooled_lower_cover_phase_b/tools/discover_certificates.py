#!/usr/bin/env python3
"""Optional SymPy discovery, NOT needed by the sealed standard-library verifier.

Usage: python3 tools/discover_certificates.py --output /tmp/certificates.json
The arithmetic conclusions require independent verification of the output.
"""
from pathlib import Path
import argparse
import json

TARGETS = [3, 4861, 11419697846380955982026777206637491,
           1783, 5023, 2066067271380136212224701233463]


def discover() -> dict:
    import sympy  # Optional discovery dependency only.
    certs: dict[str, dict] = {}
    def certify(n: int) -> None:
        key = str(n)
        if key in certs:
            return
        if n == 2:
            certs[key] = {"method": "base"}
            return
        factors = {int(p): int(e) for p, e in sympy.factorint(n - 1).items()}
        for p in factors:
            certify(p)
        for a in range(2, min(n, 10000)):
            if pow(a, n - 1, n) == 1 and all(pow(a, (n - 1) // p, n) != 1 for p in factors):
                certs[key] = {"method": "lucas_full_order", "base": a,
                              "factors_n_minus_one": {str(p): e for p, e in sorted(factors.items())}}
                return
        raise RuntimeError(f"No small full-order witness found for {n}")
    for n in TARGETS:
        certify(n)
    return {"targets": [str(n) for n in TARGETS], "certificates": certs}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    output = args.output.resolve()
    if root == output or root in output.parents:
        parser.error("output must be outside the immutable package")
    obj = discover()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(obj, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    print("DISCOVERY ONLY:", len(obj["certificates"]), "nodes written; run an exact verifier before trusting them")
