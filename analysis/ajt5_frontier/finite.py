"""Verify the J7 no-3 finite endpoint in its own bounded window."""
import hashlib
import json
import sys
from math import isqrt
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "scripts"))
from check_ajt5_integer_boundary import mask_table, native, require


def positive_units(limit):
    """Return U[k]=1 iff k>0 and no prime p=3 mod 4 other than 3 divides k."""
    prime = bytearray(b"\x01") * (limit + 1)
    for p in range(2, isqrt(limit) + 1):
        if prime[p]:
            first = p*p
            prime[first::p] = bytes((limit - first) // p + 1)
    unit = bytearray(b"\x01") * (limit + 1)
    unit[0] = 0
    for p in range(7, limit + 1, 4):
        if prime[p]:
            unit[p::p] = bytes(limit // p)
    return unit


def main():
    last = 547066
    limit = 5*last + 4
    unit = positive_units(limit)
    # Use a uint16 lane for each value; mask_table shifts by exact powers.
    lanes = bytearray(2 * len(unit))
    lanes[::2] = unit
    masks = native(mask_table(limit, int.from_bytes(lanes, "little"), 12))
    failures = []
    pairs = 0
    for m in range(2, last + 1):
        parent = masks[m] & 511
        for r in range(5):
            child = masks[5*m+r] & 511
            if not parent & (child | (child >> 1)):
                failures.append((m, r))
            pairs += 1
    require(pairs, 2735325)
    require(failures, [(2, r) for r in range(5)])
    # The parent m=2 has d=c=a=b=0. These five children use e=0.
    require(0**2 + 0**2 + 3**0 + 5**0, 2)
    for r, (c, a, b) in enumerate(((0, 2, 2), (0, 0, 3), (0, 1, 3),
                                   (1, 0, 3), (1, 1, 3))):
        require(5**0 + 3**c + a*a + b*b, 10 + r)
        require(unit[a*a+b*b], 1)
    print(json.dumps(dict(pairs=pairs, positive_unit_exceptions=failures,
                          zero_parent_actual_bridges=5, max_d_e=8, max_c=12,
                          unit_bytes_sha256=hashlib.sha256(unit).hexdigest())))


if __name__ == "__main__":
    main()
