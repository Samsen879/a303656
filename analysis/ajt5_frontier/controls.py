#!/usr/bin/env python3
"""Five actual bridges and finite local-screen controls. Standard library only."""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parents[1] / "src"))
from ajt5_integer_certificates import verify


def require(condition, detail):
    if not condition:
        raise ValueError(detail)


def check_five_digits():
    fixture = HERE.parent / "ajt5_integer_certificates/fixtures/no3_23_window.json"
    original = json.loads(fixture.read_text())
    m, parent = original["m"], original["seed"]
    require(parent["d"] == 7, "expected parent d=7")
    require(m == parent["a"]**2 + parent["b"]**2 + 5**parent["d"] + 3**parent["c"],
            "parent identity")
    controls = json.loads((HERE / "controls_five_digits.json").read_text())
    require([row["r"] for row in controls] == list(range(5)), "missing digit")
    edges = []
    for row in controls:
        r, e, c, a, b = (row[k] for k in ("r", "e", "c", "a", "b"))
        require(all(type(v) is int and v >= 0 for v in (r, e, c, a, b)), "child fields")
        require(e in (7, 8) and 5*m + r == a*a + b*b + 5**e + 3**c, "child identity")
        record = dict(kind="NO_BRIDGE", m=m, r=r, negative=[],
                      positive=[dict(side="parent", **parent),
                                dict(side="child", d=e, c=c, a=a, b=b)])
        verdict = verify(record)
        require(verdict["status"] == "REFUTED" and verdict["bridge"] == [7, e], verdict)
        edges.append(dict(r=r, parent_d=7, child_e=e, child_c=c))
    return edges


def proven_at_prefix(z, p, modulus):
    """A true result certifies every integer in this residue class."""
    z %= modulus
    if z == 0:
        return False
    valuation = 0
    while z % p == 0:
        z //= p
        modulus //= p
        valuation += 1
    if p == 2:
        return modulus >= 4 and z % 4 == 1
    return valuation % 2 == 0


def prefix_masks(roots, p, modulus):
    return {sum(1 << i for i, k in enumerate(roots) if proven_at_prefix(x-k, p, modulus))
            for x in range(modulus)}


def columns(mask, count):
    # Within each side there are three consecutive row bits per exponent.
    return sum(1 << d for d in range(count) if (mask >> (3*d)) & 7)


def has_bridge(rows, child_count):
    parents = columns(rows, 4)
    children = columns(rows >> 12, child_count)
    return bool(parents & (children | (children >> 1)))


def combined_survives(z):
    require(z > 0, "expected active positive residual")
    odd = z // (z & -z)
    parity = 0
    while z % 3 == 0:
        z //= 3
        parity ^= 1
    return odd % 4 == 1 and parity == 0


def check_local():
    counts = []
    for r in range(5):
        roots = [5*(5**d + 3**c) for d in range(4) for c in range(3)]
        roots += [5**e + 3**c-r for e in range(5) for c in range(3)]
        require(max(roots) < 5*135, "strict activation")
        two = prefix_masks(roots, 2, 2**11)
        three = prefix_masks(roots, 3, 3**6)
        # With the 3-only screen, also verify the smaller child box e<=3.
        require(all(has_bridge(mask, 4) for mask in three), (r, "3-only", 3))
        for a in two:
            require(all(has_bridge(a & b, 5) for b in three), (r, "combined", 4))
        counts.append([len(two), len(three)])
    # With both screens, reducing the child cap to 3 has a genuine local miss.
    m, r = 770, 2
    def surviving_columns(n, highest):
        return [d for d in range(highest+1)
                if any(combined_survives(n - 5**d - 3**c) for c in range(3))]
    require(surviving_columns(m, 3) == [3], "combined control parent")
    require(surviving_columns(5*m+r, 4) == [0, 1, 2, 4], "combined control child")
    return counts


if __name__ == "__main__":
    print(json.dumps(dict(actual_bridges=check_five_digits(),
                          local_mask_counts_mod_2048_and_729=check_local())))
