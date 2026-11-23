#!/usr/bin/env python3
"""Construct an integer whose first representation in a chosen column occurs at c=C."""
import argparse
import json
from math import isqrt


def prime(p):
    return p >= 2 and all(p % k for k in range(2, isqrt(p)+1))


def norm_lift(target, p):
    # target is a unit modulo p. At least one coordinate is a unit.
    for a in range(p):
        rest = (target-a*a) % p
        b = pow(rest, (p+1)//4, p)
        if b*b % p == rest:
            if b == 0:
                a, b = b, a
            correction = ((target-a*a-b*b)//p) * pow(2*b, -1, p) % p
            return a, b + p*correction
    raise ArithmeticError("missing norm residue")


def construct(d, first):
    if min(d, first) < 0:
        raise ValueError("nonnegative exponents required")
    a = b = 0
    modulus = 1
    p = 3
    blockers = []
    for c in range(first):
        delta = 3**first - 3**c
        while not prime(p) or delta % p == 0:
            p += 4
        x, y = norm_lift(p-delta, p)
        pp = p*p
        inverse = pow(modulus, -1, pp)
        a += modulus * ((x-a)*inverse % pp)
        b += modulus * ((y-b)*inverse % pp)
        modulus *= pp
        blockers.append({"c": c, "u": p})
        p += 4
    return {"m": 5**d + 3**first + a*a+b*b, "d": d, "c": first,
            "a": a, "b": b, "prior": blockers}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("d", type=int)
    parser.add_argument("C", type=int)
    args = parser.parse_args()
    print(json.dumps(construct(args.d, args.C)))


if __name__ == "__main__":
    main()
