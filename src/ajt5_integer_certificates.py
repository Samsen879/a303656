#!/usr/bin/env python3
"""Verify submitted evidence for a single integer. No factorization or search required."""
import argparse
import errno
import json
import sys
from math import gcd
from pathlib import Path


MAX_BYTES = 8 * 1024 * 1024
MAX_BITS = 4096


class ResourceLimit(Exception):
    pass


def check(condition, message):
    if not condition:
        raise ValueError(message)


def unique_object(pairs):
    obj = {}
    for key, value in pairs:
        check(key not in obj, "duplicate JSON key")
        obj[key] = value
    return obj


def no_fraction(token):
    raise ValueError("only JSON integers are admissible numeric tokens")


def parse_integer(token):
    if len(token.lstrip("-")) > 1234:
        raise ResourceLimit("integer token exceeds bit budget")
    digits = token.lstrip("-")
    value = 0
    for start in range(0, len(digits), 80):
        chunk = digits[start:start+80]
        value = value * 10**len(chunk) + int(chunk)
    if token.startswith("-"):
        value = -value
    if value.bit_length() > MAX_BITS:
        raise ResourceLimit("integer exceeds bit budget")
    return value


def parse(raw):
    if len(raw) > MAX_BYTES:
        raise ResourceLimit("certificate exceeds byte budget")
    # Bound nesting before invoking the host JSON decoder. Brackets inside
    # strings have no structural effect, including after an escaped quote.
    depth = 0
    quoted = escaped = False
    for token in raw:
        if quoted:
            if escaped:
                escaped = False
            elif token == 92:
                escaped = True
            elif token == 34:
                quoted = False
        elif token == 34:
            quoted = True
        elif token in (91, 123):
            depth += 1
            if depth > 64:
                raise ResourceLimit("JSON nesting exceeds 64")
        elif token in (93, 125):
            depth -= 1
    return json.loads(raw.decode("utf-8"), object_pairs_hook=unique_object,
                      parse_int=parse_integer, parse_float=no_fraction, parse_constant=no_fraction)


def fields(record, expected):
    check(type(record) is dict and set(record) == set(expected), "unexpected or missing field")


def natural(value):
    check(type(value) is int and value >= 0, "expected a nonnegative integer")
    if value.bit_length() > MAX_BITS:
        raise ResourceLimit("integer exceeds bit budget")
    return value


def sequence(value):
    check(type(value) is list, "expected an array")
    return value


def powers(base, bound):
    result = []
    value = 1
    while value <= bound:
        result.append(value)
        value *= base
    return result


def unit_proves_negative(residual, u):
    return (residual > 0 and u > 0 and u % 4 == 3 and residual % u == 0
            and gcd(u, residual // u) == 1)


def edge_verdict(parent_count, parent_positive, child_positive, parent_negative, child_negative):
    """Only called with independently established positive / complete-negative column sets."""
    for j in sorted(parent_positive):
        for e in (j, j + 1):
            if e in child_positive:
                return {"status": "REFUTED", "bridge": [j, e]}
    if not parent_positive and len(parent_negative) == parent_count:
        return {"status": "REFUTED", "reason": "certified empty parent"}
    if not parent_positive:
        return {"status": "PARTIAL", "reason": "missing parent witness"}
    for j in range(parent_count):
        for e in (j, j + 1):
            if j not in parent_negative and e not in child_negative:
                return {"status": "PARTIAL", "uncovered_edge": [j, e]}
    return {"status": "VERIFIED_NO_BRIDGE"}


def empty_verdict(active_count, positives, negatives):
    if positives:
        return {"status": "REFUTED", "positive_d": min(positives)}
    for d in range(active_count):
        if d not in negatives:
            return {"status": "PARTIAL", "uncovered_d": d}
    return {"status": "VERIFIED_EMPTY_D"}


def child_classification(active_count, positives, negatives):
    if positives:
        return "AJT5_ONLY_AT_CHILD"
    if len(negatives) == active_count:
        return "SUN_FAILURE_AT_CHILD"
    return "CHILD_EXISTENCE_UNKNOWN"


def verify(record):
    check(type(record) is dict, "expected an object")
    kind = record.get("kind")
    if kind == "NO_BRIDGE":
        fields(record, ("kind", "m", "r", "positive", "negative"))
        m, r = natural(record["m"]), natural(record["r"])
        check(m >= 2 and r <= 4, "outside the AJT5 domain")
        numbers = {"parent": m, "child": 5*m+r}
    elif kind == "EMPTY_D":
        fields(record, ("kind", "n", "positive", "negative"))
        n = natural(record["n"])
        check(n >= 2, "outside the Sun domain")
        numbers = {"target": n}
    else:
        raise ValueError("unknown claim kind")

    fives = {side: powers(5, x-1) for side, x in numbers.items()}
    threes = powers(3, max(numbers.values())-1)
    positive = {side: set() for side in numbers}
    negative = {side: set() for side in numbers}
    seen_positive = set()
    seen_negative = set()

    def column(row):
        side, d = row["side"], natural(row["d"])
        check(type(side) is str and side in numbers, "unknown side")
        check(d < len(fives[side]), "inactive d")
        return side, d, numbers[side] - fives[side][d]

    def residual(bound, c):
        natural(c)
        check(c < len(threes) and threes[c] <= bound, "inactive c")
        return bound - threes[c]

    for row in sequence(record["positive"]):
        fields(row, ("side", "d", "c", "a", "b"))
        side, d, bound = column(row)
        c = row["c"]
        value = residual(bound, c)
        a, b = natural(row["a"]), natural(row["b"])
        check(a*a+b*b == value, "false square identity")
        key = (side, d, c)
        check(key not in seen_positive, "duplicate positive atom")
        seen_positive.add(key)
        positive[side].add(d)

    for row in sequence(record["negative"]):
        fields(row, ("side", "d", "units"))
        side, d, bound = column(row)
        check((side, d) not in seen_negative, "duplicate negative column")
        seen_negative.add((side, d))
        indices = set()
        for atom in sequence(row["units"]):
            fields(atom, ("c", "u"))
            c = atom["c"]
            value = residual(bound, c)
            check(c not in indices, "duplicate negative atom")
            check(unit_proves_negative(value, natural(atom["u"])), "invalid unitary divisor")
            indices.add(c)
        # Admissible indices form an initial interval. Each supplied c was
        # checked in range and distinct, so cardinality proves exact coverage.
        if len(indices) == len(threes) or threes[len(indices)] > bound:
            negative[side].add(d)

    if kind == "EMPTY_D":
        result = empty_verdict(len(fives["target"]), positive["target"], negative["target"])
        if result["status"] == "VERIFIED_EMPTY_D":
            result["n"] = numbers["target"]
        return result

    # A parent (d,c) active at m has both child exponents active at 5m+r.
    result = edge_verdict(len(fives["parent"]), positive["parent"], positive["child"],
                          negative["parent"], negative["child"])
    if result["status"] == "VERIFIED_NO_BRIDGE":
        result["classification"] = child_classification(
            len(fives["child"]), positive["child"], negative["child"])
        result["n"] = numbers["child"]
    return result


def inspect(raw):
    try:
        return verify(parse(raw))
    except (ResourceLimit, RecursionError, MemoryError) as exc:
        return {"status": "UNKNOWN_RESOURCE", "reason": str(exc) or "resource limit"}
    except ValueError as exc:
        return {"status": "INVALID", "reason": str(exc)}


class CertificateParser(argparse.ArgumentParser):
    def error(self, message):
        raise ValueError(message)


def main(argv=None):
    parser = CertificateParser(description=__doc__)
    parser.add_argument("certificate", type=Path)
    try:
        args = parser.parse_args(argv)
        with args.certificate.open("rb") as handle:
            outcome = inspect(handle.read(MAX_BYTES + 1))
    except OSError as exc:
        status = ("UNKNOWN_RESOURCE" if exc.errno in (errno.ENOMEM, errno.EMFILE, errno.ENFILE)
                  else "INVALID")
        outcome = {"status": status, "reason": "cannot read certificate: " + (exc.strerror or "I/O error")}
    except MemoryError:
        outcome = {"status": "UNKNOWN_RESOURCE", "reason": "insufficient memory to read certificate"}
    except ValueError as exc:
        outcome = {"status": "INVALID", "reason": str(exc)}
    print(json.dumps(outcome, sort_keys=True))
    return {"VERIFIED_NO_BRIDGE": 0, "VERIFIED_EMPTY_D": 0, "REFUTED": 1,
            "INVALID": 2, "PARTIAL": 3, "UNKNOWN_RESOURCE": 4}[outcome["status"]]


if __name__ == "__main__":
    sys.exit(main())
