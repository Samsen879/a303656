#!/usr/bin/env python3
"""A303656 Phase 3: arithmetic realizability of l-adic prefix frontiers.

Read-only, standard-library reference implementation.

This program:
  * scans admitted row primes up to the frozen finite bound B=10^7;
  * reconstructs the exact l=3, beta<=3 parameter-labelled abstract catalog;
  * applies order/lifting/support filters candidate by candidate;
  * builds compressed inventory catalogs for l=67, beta<=3;
  * verifies actual shared-residue beta=1,2,3 fibers based on (67,20771)
    with regular order-support primes 80803 and 6616787;
  * audits dynamic and rigid two-anchor common-residue conditions.

No bounded absence is promoted to a universal theorem.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
from dataclasses import dataclass
from functools import lru_cache
import hashlib
import itertools
import json
import math
from pathlib import Path
from typing import Iterable, Iterator

AUTHORITY = {
    "repository": "Samsen879/a303656",
    "repository_id": 1333945235,
    "main_sha": "1100eb5ba01d90e5b1001be0bdfa464860fdbb92",
    "main_tree": "ad1269916bf420c564e34887a96c808033fe538b",
    "state": {
        "PROJECT": "PAUSED",
        "ACTIVE_PROMOTED_ROUTE": "NONE",
        "A303656": "UNRESOLVED",
    },
}
BOUND = 10_000_000
TARGET_L = (3, 67)
MAX_BETA = 3


class AuditError(ValueError):
    pass


def canonical_json_bytes(obj: object) -> bytes:
    return (json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("utf-8")


def write_json(path: Path, obj: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(canonical_json_bytes(obj))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def sieve_primes(bound: int) -> tuple[list[int], bytearray]:
    sieve = bytearray(b"\x01") * (bound + 1)
    sieve[:2] = b"\x00\x00"
    for p in range(2, math.isqrt(bound) + 1):
        if sieve[p]:
            start = p * p
            sieve[start : bound + 1 : p] = b"\x00" * (((bound - start) // p) + 1)
    return [i for i, flag in enumerate(sieve) if flag], sieve


def factor_with_primes(n: int, trial_primes: list[int]) -> dict[int, int]:
    if n < 1:
        raise AuditError("factor requires n>=1")
    out: dict[int, int] = {}
    for p in trial_primes:
        if p * p > n:
            break
        if n % p == 0:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            out[p] = e
        if n == 1:
            break
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def order_mod_prime(base: int, q: int, q_minus_one_factor: dict[int, int]) -> int:
    order = q - 1
    for p, multiplicity in q_minus_one_factor.items():
        for _ in range(multiplicity):
            if pow(base, order // p, q) != 1:
                break
            order //= p
    if pow(base, order, q) != 1:
        raise AssertionError("order computation failed")
    return order


def lifting_depth(base: int, q: int, order: int, cap: int = 8) -> int:
    if pow(base, order, q) != 1:
        raise AuditError("invalid order")
    for s in range(1, cap):
        if pow(base, order, q ** (s + 1)) != 1:
            return s
    raise AuditError(f"lifting depth reached cap={cap}")


def vp_nonzero(n: int, p: int) -> int:
    if n == 0:
        raise AuditError("zero has no finite valuation")
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e


def clipped_valuation(value: int, p: int, precision: int) -> int | None:
    value %= p**precision
    if value == 0:
        return None
    return vp_nonzero(value, p)


def valuation_in_order(order: int, l: int) -> int:
    e = 0
    while order % l == 0:
        order //= l
        e += 1
    return e


def list_record(values: list[int], path: Path) -> dict[str, object]:
    data = "".join(f"{v}\n" for v in values).encode("ascii")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    return {
        "count": len(values),
        "file": str(path.name),
        "sha256": sha256_bytes(data),
        "first": values[:20],
        "last": values[-20:] if values else [],
    }


def scan_resources(outdir: Path) -> tuple[dict, dict[int, dict[str, dict[int, list[int]]]], dict[int, dict[str, int]]]:
    primes, _ = sieve_primes(BOUND)
    trial = [p for p in primes if p <= math.isqrt(BOUND)]
    admitted = [q for q in primes if q % 4 == 3 and q != 5]

    rows: dict[int, dict[str, dict[int, list[int]]]] = {
        l: {
            "support": {e: [] for e in range(1, MAX_BETA + 1)},
            "order_signature": {e: [] for e in range(1, MAX_BETA + 1)},
            "active_nonregular": {e: [] for e in range(1, MAX_BETA + 1)},
        }
        for l in TARGET_L
    }
    nonregular: list[dict[str, object]] = []
    order_cache: dict[int, tuple[int, dict[int, int], int]] = {}

    for q in admitted:
        fac_qm1 = factor_with_primes(q - 1, trial)
        w = order_mod_prime(5, q, fac_qm1)
        fac_w = factor_with_primes(w, trial)
        is_nonregular = pow(5, w, q * q) == 1
        s = lifting_depth(5, q, w) if is_nonregular else 1
        order_cache[q] = (w, fac_w, s)
        if is_nonregular:
            nonregular.append({
                "q": q,
                "w_q": w,
                "factorization_w_q": {str(p): e for p, e in sorted(fac_w.items())},
                "s_q": s,
                "largest_order_prime": max(fac_w),
                "largest_order_prime_exponent": fac_w[max(fac_w)],
            })
        for l in TARGET_L:
            e = fac_w.get(l, 0)
            if not (1 <= e <= MAX_BETA):
                continue
            rows[l]["support"][e].append(q)
            if max(fac_w) == l:
                rows[l]["order_signature"][e].append(q)
                if s >= 2:
                    rows[l]["active_nonregular"][e].append(q)

    result: dict[str, object] = {
        "schema": "a303656.phase3.resource-scan.v1",
        "authority": AUTHORITY,
        "domain": {
            "bound_inclusive": BOUND,
            "predicate": "q prime, q == 3 (mod 4), q != 5",
            "admitted_prime_count": len(admitted),
            "method": "bytearray Eratosthenes sieve; exact factorization of q-1; exact order reduction; pow(5,w,q^2) nonregularity test",
            "no_universal_inference_from_bounded_absence": True,
            "bound_selection_note": "Exploratory Phase-3 follow-up bound; exact finite result, not a pre-registered universal search boundary.",
        },
        "all_nonregular_rows": nonregular,
        "targets": {},
    }
    capacities: dict[int, dict[str, int]] = {}
    for l in TARGET_L:
        target: dict[str, object] = {
            "l": l,
            "dynamic": {
                "admitted": l % 4 == 3 and l != 5,
                "w_l": order_cache[l][0],
                "s_l": order_cache[l][2],
                "s_parity": order_cache[l][2] % 2,
            },
            "depths": {},
        }
        for e in range(1, MAX_BETA + 1):
            depth_record: dict[str, object] = {}
            for kind in ("support", "order_signature", "active_nonregular"):
                values = rows[l][kind][e]
                filename = f"l{l}_e{e}_{kind}.txt"
                depth_record[kind] = list_record(values, outdir / "prime_lists" / filename)
            target["depths"][str(e)] = depth_record
        result["targets"][str(l)] = target
        capacities[l] = {
            **{f"support_{e}": len(rows[l]["support"][e]) for e in range(1, MAX_BETA + 1)},
            **{f"order_{e}": len(rows[l]["order_signature"][e]) for e in range(1, MAX_BETA + 1)},
            **{f"active_{e}": len(rows[l]["active_nonregular"][e]) for e in range(1, MAX_BETA + 1)},
        }

    result["result_sha256"] = sha256_bytes(canonical_json_bytes(result))
    return result, rows, capacities


@dataclass(frozen=True, order=True)
class Cylinder:
    depth: int
    residue: int


def cylinder_cells(l: int, beta: int, cyl: Cylinder) -> frozenset[int]:
    mod = l**cyl.depth
    return frozenset(range(cyl.residue % mod, l**beta, mod))


def shell_cells(l: int, beta: int, j: int, center: int = 0) -> frozenset[int]:
    out = []
    mod = l**beta
    for x in range(mod):
        diff = (x - center) % mod
        if diff and vp_nonzero(diff, l) == j:
            out.append(x)
    return frozenset(out)


@lru_cache(maxsize=None)
def complete_frontiers(l: int, beta: int, root: Cylinder) -> tuple[tuple[Cylinder, ...], ...]:
    if root.depth == beta:
        return ((root,),)
    options: list[tuple[Cylinder, ...]] = [(root,)]
    modulus = l**root.depth
    children = tuple(Cylinder(root.depth + 1, root.residue + digit * modulus) for digit in range(l))
    child_options = [complete_frontiers(l, beta, child) for child in children]
    for choice in itertools.product(*child_options):
        options.append(tuple(sorted(itertools.chain.from_iterable(choice))))
    return tuple(options)


def branch_roots(l: int, j: int) -> tuple[Cylinder, ...]:
    return tuple(Cylinder(j + 1, digit * l**j) for digit in range(1, l))


def allowed_shells(m: int, s_parity: int) -> tuple[int, ...]:
    return tuple(j for j in range(m) if (s_parity + j) % 2 == 1)


def inventory(rigid: tuple[Cylinder, ...], beta: int) -> tuple[int, ...]:
    c = Counter(x.depth for x in rigid)
    return tuple(c[e] for e in range(1, beta + 1))


def exact_cover_check(l: int, beta: int, accepted_j: tuple[int, ...], rigid: tuple[Cylinder, ...]) -> tuple[bool, bool]:
    events: list[frozenset[int]] = []
    if accepted_j:
        dyn: set[int] = set()
        for j in accepted_j:
            dyn.update(shell_cells(l, beta, j, 0))
        events.append(frozenset(dyn))
    events.extend(cylinder_cells(l, beta, c) for c in rigid)
    universe = set(range(l**beta))
    covered = set().union(*events) if events else set()
    full = covered == universe
    minimal = full
    if full:
        for i in range(len(events)):
            other = set().union(*(events[:i] + events[i + 1:])) if len(events) > 1 else set()
            if other == universe:
                minimal = False
                break
    return full, minimal


def classify_candidate(record: dict, l: int, beta: int, capacities: dict[str, int], actual_s_parity: int) -> tuple[str, dict[str, bool]]:
    inv = record["rigid_inventory"]
    dynamic = record["kind"] == "dynamic"
    parity_ok = (not dynamic) or record["s_parity"] == actual_s_parity
    order_ok = all(inv[e - 1] <= capacities[f"order_{e}"] for e in range(1, beta + 1))
    lifting_ok = all(inv[e - 1] <= capacities[f"active_{e}"] for e in range(1, beta + 1))
    support_ok = inv[beta - 1] > 0 or capacities[f"support_{beta}"] > 0
    local_zero_ok = bool(record["center_covered_by_rigid"])
    filters = {
        "dynamic_admissibility_and_parity": parity_ok,
        "bounded_order_inventory": order_ok,
        "bounded_nonregular_lifting_inventory": lifting_ok,
        "bounded_exact_ambient_beta_support": support_ok,
        "local_zero_fail_closed": local_zero_ok,
        "one_anchor_center_placement": True,
    }
    if not parity_ok:
        status = "DYNAMIC_PARITY_BLOCKED"
    elif not order_ok:
        status = "ORDER_BLOCKED"
    elif not lifting_ok:
        status = "LIFTING_BLOCKED"
    elif not support_ok:
        status = "SUPPORT_BLOCKED"
    elif not local_zero_ok:
        status = "LOCAL_ZERO_BLOCKED"
    else:
        status = "ARITHMETICALLY_REALIZABLE"
    return status, filters


def build_l3_catalog(capacities: dict[str, int]) -> dict:
    l = 3
    actual_s_parity = 1
    groups: list[dict] = []
    all_records: list[dict] = []
    sequence = 0
    for beta in range(1, MAX_BETA + 1):
        records: list[dict] = []
        # Rigid-only frontiers.
        per_digit = [complete_frontiers(l, beta, Cylinder(1, digit)) for digit in range(l)]
        for choice in itertools.product(*per_digit):
            rigid = tuple(sorted(itertools.chain.from_iterable(choice)))
            full, minimal = exact_cover_check(l, beta, (), rigid)
            rec = {
                "kind": "rigid_only",
                "l": l,
                "beta": beta,
                "m": 0,
                "s_parity": None,
                "accepted_j": [],
                "center_depth": None,
                "rigid_leaves": [{"depth": c.depth, "residue": c.residue} for c in rigid],
                "rigid_inventory": list(inventory(rigid, beta)),
                "center_covered_by_rigid": any(c.residue % (l**c.depth) == 0 for c in rigid),
                "abstract_valid": full and minimal,
            }
            status, filters = classify_candidate(rec, l, beta, capacities, actual_s_parity)
            rec["status"] = status
            rec["filters"] = filters
            records.append(rec)
        # Dynamic parameter-labelled frontiers.
        for s_parity in (0, 1):
            for m in range(1, beta + 1):
                allowed = allowed_shells(m, s_parity)
                for size in range(1, len(allowed) + 1):
                    for J in itertools.combinations(allowed, size):
                        for e in range(1, beta + 1):
                            if not any(j < e for j in J):
                                continue
                            branch_options = []
                            for j in range(e):
                                if j < m and j in J:
                                    continue
                                for root in branch_roots(l, j):
                                    branch_options.append(complete_frontiers(l, beta, root))
                            products = itertools.product(*branch_options) if branch_options else [()]
                            for selected in products:
                                side = tuple(sorted(itertools.chain.from_iterable(selected))) if selected else ()
                                rigid = tuple(sorted((Cylinder(e, 0),) + side))
                                full, minimal = exact_cover_check(l, beta, J, rigid)
                                rec = {
                                    "kind": "dynamic",
                                    "l": l,
                                    "beta": beta,
                                    "m": m,
                                    "s_parity": s_parity,
                                    "accepted_j": list(J),
                                    "center_depth": e,
                                    "rigid_leaves": [{"depth": c.depth, "residue": c.residue} for c in rigid],
                                    "rigid_inventory": list(inventory(rigid, beta)),
                                    "center_covered_by_rigid": any(c.residue % (l**c.depth) == 0 for c in rigid),
                                    "abstract_valid": full and minimal,
                                }
                                status, filters = classify_candidate(rec, l, beta, capacities, actual_s_parity)
                                rec["status"] = status
                                rec["filters"] = filters
                                records.append(rec)
        records.sort(key=lambda r: (
            r["kind"], r["m"], -1 if r["s_parity"] is None else r["s_parity"],
            r["accepted_j"], -1 if r["center_depth"] is None else r["center_depth"],
            tuple(r["rigid_inventory"]), tuple((x["depth"], x["residue"]) for x in r["rigid_leaves"]),
        ))
        status_counts = Counter(r["status"] for r in records)
        for rec in records:
            sequence += 1
            rec["candidate_id"] = f"L3-B{beta}-{sequence:04d}"
            rec["candidate_sha256"] = sha256_bytes(canonical_json_bytes(rec))
            if not rec["abstract_valid"]:
                raise AssertionError("generator emitted invalid frontier")
        groups.append({
            "l": l,
            "beta": beta,
            "candidate_count": len(records),
            "status_counts": dict(sorted(status_counts.items())),
            "records": records,
        })
        all_records.extend(records)
    expected = {1: 2, 2: 16, 3: 1413}
    if {g["beta"]: g["candidate_count"] for g in groups} != expected:
        raise AssertionError("l=3 catalog count mismatch")
    result = {
        "schema": "a303656.phase3.l3-literal-catalog.v1",
        "authority": AUTHORITY,
        "semantics": "parameter-labelled centered prefix-frontiers; bounded statuses use q<=10^7 inventory and are not universal absence theorems",
        "actual_dynamic": {"l": 3, "s_l": 1, "s_parity": 1},
        "capacities": capacities,
        "groups": groups,
        "candidate_total": len(all_records),
        "PASS": True,
    }
    result["catalog_sha256"] = sha256_bytes(canonical_json_bytes(result))
    return result


# Multivariate inventory-polynomial utilities.  A polynomial is a map
# exponent tuple (n_1,...,n_beta) -> exact labelled multiplicity.
Poly = dict[tuple[int, ...], int]


def p_add(*polys: Poly) -> Poly:
    out: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for p in polys:
        for mon, coeff in p.items():
            out[mon] += coeff
    return dict(out)


def p_mul(a: Poly, b: Poly) -> Poly:
    out: defaultdict[tuple[int, ...], int] = defaultdict(int)
    for ma, ca in a.items():
        for mb, cb in b.items():
            out[tuple(x + y for x, y in zip(ma, mb))] += ca * cb
    return dict(out)


def p_pow(a: Poly, n: int, beta: int) -> Poly:
    out: Poly = {(0,) * beta: 1}
    base = a
    while n:
        if n & 1:
            out = p_mul(out, base)
        n >>= 1
        if n:
            base = p_mul(base, base)
    return out


def var_poly(beta: int, depth: int) -> Poly:
    mon = [0] * beta
    mon[depth - 1] = 1
    return {tuple(mon): 1}


def frontier_polys(l: int, beta: int) -> dict[int, Poly]:
    H: dict[int, Poly] = {beta: var_poly(beta, beta)}
    for d in range(beta - 1, 0, -1):
        H[d] = p_add(var_poly(beta, d), p_pow(H[d + 1], l, beta))
    return H


def dynamic_family_poly(l: int, beta: int, m: int, J: tuple[int, ...], H: dict[int, Poly]) -> Poly:
    total: Poly = {}
    for e in range(1, beta + 1):
        if not any(j < e for j in J):
            continue
        term = var_poly(beta, e)
        for j in range(e):
            if j < m and j in J:
                continue
            term = p_mul(term, p_pow(H[j + 1], l - 1, beta))
        total = p_add(total, term)
    return total


def classify_profile(mon: tuple[int, ...], beta: int, capacities: dict[str, int], parity_ok: bool) -> str:
    if not parity_ok:
        return "DYNAMIC_PARITY_BLOCKED"
    if any(mon[e - 1] > capacities[f"order_{e}"] for e in range(1, beta + 1)):
        return "ORDER_BLOCKED"
    if any(mon[e - 1] > capacities[f"active_{e}"] for e in range(1, beta + 1)):
        return "LIFTING_BLOCKED"
    if mon[beta - 1] == 0 and capacities[f"support_{beta}"] == 0:
        return "SUPPORT_BLOCKED"
    return "ARITHMETICALLY_REALIZABLE"


def build_compressed_catalog(l: int, capacities: dict[str, int], actual_s_parity: int) -> dict:
    """Closed-form compressed beta<=3 catalog for l=67.

    The status predicates are exact for the stored q<=10^7 inventory.  The
    formulas, rather than a literal expansion, mark every abstract candidate.
    """
    if l != 67 or actual_s_parity != 1:
        raise AuditError("closed-form compressed catalog is frozen to l=67, s parity odd")

    # beta=1
    b1_families = [
        {
            "family": "rigid_only_x1^l",
            "candidate_count": "1",
            "status_partition": {"LIFTING_BLOCKED": "1"},
            "status_rule": "the unique candidate needs l=67 distinct depth-1 nonregular rows; bounded active capacity is 1",
        },
        {
            "family": "dynamic_J0_m1_x1",
            "candidate_count": "1",
            "status_partition": {"ARITHMETICALLY_REALIZABLE": "1"},
            "status_rule": "one depth-1 leaf supplied by q=20771",
        },
    ]
    b1_status = {"ARITHMETICALLY_REALIZABLE": 1, "LIFTING_BLOCKED": 1}

    # beta=2. H1=x1+x2^l and H1(1)=2.
    two_l = 2**l
    two_lm1 = 2 ** (l - 1)
    b2_families = [
        {
            "family": "rigid_only_H1^l",
            "inventory_formula": "choose t refined top branches: (n1,n2)=(l-t,l*t), multiplicity C(l,t)",
            "candidate_count": str(two_l),
            "status_partition": {"LIFTING_BLOCKED": "1", "ORDER_BLOCKED": str(two_l - 1)},
            "status_rule": "t=0 is lifting-blocked; every t>=1 needs at least l=67 depth-2 order rows, exceeding bounded order capacity 35",
        },
        {
            "family": "dynamic_J0_m1_H1",
            "candidate_count": "2",
            "status_partition": {"ARITHMETICALLY_REALIZABLE": "1", "ORDER_BLOCKED": "1"},
            "status_rule": "center depth 1 is realized; center refined to depth 2 needs 67 depth-2 rows",
        },
        {
            "family": "dynamic_J0_m2_H1",
            "candidate_count": "2",
            "status_partition": {"ARITHMETICALLY_REALIZABLE": "1", "ORDER_BLOCKED": "1"},
            "status_rule": "same event family as m=1 but retained as a parameter label",
        },
        {
            "family": "dynamic_J1_m2_x2*H1^(l-1)",
            "candidate_count": str(two_lm1),
            "status_partition": {"DYNAMIC_PARITY_BLOCKED": str(two_lm1)},
            "status_rule": "actual s_67=1 is odd, so only even j are admissible",
        },
    ]
    b2_status = {
        "ARITHMETICALLY_REALIZABLE": 2,
        "DYNAMIC_PARITY_BLOCKED": two_lm1,
        "LIFTING_BLOCKED": 1,
        "ORDER_BLOCKED": two_l + 1,
    }
    b2_total = sum(b2_status.values())

    # beta=3. H2=x2+x3^l, H1=x1+H2^l, F=H1(1)=1+2^l.
    F = 1 + two_l
    rigid_count = F**l
    j0_count = F
    j02_count = F
    j2_count = (2 * F) ** (l - 1)
    j1_each_count = 2 * F ** (l - 1)
    b3_families = [
        {
            "family": "rigid_only_H1^l",
            "candidate_count": str(rigid_count),
            "status_partition": {"LIFTING_BLOCKED": "1", "ORDER_BLOCKED": str(rigid_count - 1)},
            "status_rule": "all-depth-1 is the sole order-feasible profile and needs 67 nonregular rows; any refinement creates >=67 depth-2 or depth-3 leaves",
        },
        *[
            {
                "family": f"dynamic_J0_m{m}_H1",
                "candidate_count": str(j0_count),
                "status_partition": {"ARITHMETICALLY_REALIZABLE": "1", "ORDER_BLOCKED": str(j0_count - 1)},
                "status_rule": "the depth-1 centered leaf is realized; every proper refinement creates >=67 deeper leaves",
            }
            for m in (1, 2, 3)
        ],
        {
            "family": "dynamic_J02_m3_[x1+(x2+x3)H2^(l-1)]",
            "candidate_count": str(j02_count),
            "status_partition": {"ARITHMETICALLY_REALIZABLE": "1", "ORDER_BLOCKED": str(j02_count - 1)},
            "status_rule": "the e=1 overlap-tail template is realized; every e>=2 option exceeds bounded deeper-order capacity",
        },
        {
            "family": "dynamic_J2_m3_x3*H1^(l-1)*H2^(l-1)",
            "candidate_count": str(j2_count),
            "status_partition": {"ORDER_BLOCKED": str(j2_count)},
            "status_rule": "the H2^(l-1) factor alone forces either 66 depth-2 leaves or at least 67 depth-3 leaves",
        },
        *[
            {
                "family": f"dynamic_J1_m{m}_H2*H1^(l-1)",
                "candidate_count": str(j1_each_count),
                "status_partition": {"DYNAMIC_PARITY_BLOCKED": str(j1_each_count)},
                "status_rule": "actual s_67=1 is odd",
            }
            for m in (2, 3)
        ],
    ]
    b3_status = {
        "ARITHMETICALLY_REALIZABLE": 4,
        "DYNAMIC_PARITY_BLOCKED": 4 * F ** (l - 1),
        "LIFTING_BLOCKED": 1,
        "ORDER_BLOCKED": rigid_count + j2_count + 4 * F - 5,
    }
    b3_total = sum(b3_status.values())

    groups = [
        {
            "l": l,
            "beta": 1,
            "candidate_count": "2",
            "candidate_count_digits": 1,
            "status_counts": {k: str(v) for k, v in sorted(b1_status.items())},
            "families": b1_families,
        },
        {
            "l": l,
            "beta": 2,
            "frontier_polynomial": "H1=x1+x2^l",
            "candidate_count": str(b2_total),
            "candidate_count_digits": len(str(b2_total)),
            "status_counts": {k: str(v) for k, v in sorted(b2_status.items())},
            "families": b2_families,
        },
        {
            "l": l,
            "beta": 3,
            "frontier_polynomials": {"H2": "x2+x3^l", "H1": "x1+H2^l", "F": str(F)},
            "candidate_count_formula": "F^l+(2F)^(l-1)+4F+4F^(l-1)",
            "candidate_count": str(b3_total),
            "candidate_count_digits": len(str(b3_total)),
            "status_counts": {k: str(v) for k, v in sorted(b3_status.items())},
            "families": b3_families,
        },
    ]
    result = {
        "schema": "a303656.phase3.compressed-inventory-catalog.v1",
        "authority": AUTHORITY,
        "l": l,
        "actual_dynamic_s_parity": actual_s_parity,
        "capacities": capacities,
        "groups": groups,
        "bounded_status_scope": "ORDER_BLOCKED/LIFTING_BLOCKED/SUPPORT_BLOCKED use only q<=10^7 resources; absence outside the bound remains UNKNOWN.",
        "status_predicate": "Apply actual s_l parity, then n_e<=order_e, then n_e<=active_e, then require n_beta>0 or support_beta>0.",
        "PASS": True,
    }
    result["catalog_sha256"] = sha256_bytes(canonical_json_bytes(result))
    return result

def exact_prime_properties(q: int, trial: list[int]) -> dict[str, object]:
    fac = factor_with_primes(q - 1, trial)
    w = order_mod_prime(5, q, fac)
    fw = factor_with_primes(w, trial)
    s = lifting_depth(5, q, w)
    return {
        "q": q,
        "q_mod_4": q % 4,
        "w_q": w,
        "factorization_w_q": {str(p): e for p, e in sorted(fw.items())},
        "s_q": s,
    }


def fiber_audit(beta: int, m: int, anchor: int, lower: int, accepted_j: tuple[int, ...], support_q: int | None, trial: list[int]) -> dict:
    l, q = 67, 20771
    selected_orders = [22, 10385]
    if support_q is not None:
        selected_orders.append(int(exact_prime_properties(support_q, trial)["w_q"]))
    U = math.lcm(*selected_orders)
    M = U // (l**beta)
    if U % (l**beta) != 0 or U % (l ** (beta + 1)) == 0:
        raise AssertionError("ambient beta mismatch")
    if not (1 <= m <= beta) or any(j >= m for j in accepted_j):
        raise AuditError("invalid dynamic m/J")
    dynamic_K = 1 + m
    dynamic_E = {1 + j for j in accepted_j}
    dynamic_r = 2
    rigid_r = 13471
    N = l**beta
    assignment = bytearray()
    dynamic_count = rigid_count = overlap_count = hole_count = zero_count = 0
    zero_indices = []
    for t in range(N):
        d = lower + M * t
        vd = clipped_valuation(dynamic_r - 3**anchor - pow(5, d, l**dynamic_K), l, dynamic_K)
        vr = clipped_valuation(rigid_r - 3**anchor - pow(5, d, q*q), q, 2)
        a = vd in dynamic_E
        b = vr == 1
        dynamic_count += int(a)
        rigid_count += int(b)
        overlap_count += int(a and b)
        hole_count += int(not (a or b))
        if vd is None:
            zero_count += 1
            if len(zero_indices) < 20:
                zero_indices.append(t)
        assignment.append(3 if not (a or b) else 2 if (a and b) else 0 if a else 1)
    expected_holes = 0
    expected_zero_count = l ** (beta - m)
    if hole_count != expected_holes or zero_count != expected_zero_count:
        raise AssertionError("actual fiber failed")
    return {
        "beta": beta,
        "m": m,
        "anchor": anchor,
        "lower_assignment": lower,
        "coordinate_step_M": M,
        "U": U,
        "accepted_j": list(accepted_j),
        "dynamic_K": dynamic_K,
        "dynamic_E": sorted(dynamic_E),
        "fiber_size": N,
        "dynamic_fatal_count": dynamic_count,
        "rigid_fatal_count": rigid_count,
        "overlap_count": overlap_count,
        "hole_count": hole_count,
        "dynamic_local_zero_count": zero_count,
        "dynamic_local_zero_indices_first": zero_indices,
        "assignment_sha256": sha256_bytes(bytes(assignment)),
    }


def build_actual_embeddings() -> dict:
    primes, _ = sieve_primes(100_000)
    trial = primes
    props = {q: exact_prime_properties(q, trial) for q in (67, 20771, 80803, 6616787)}
    expected = {
        67: (22, 1),
        20771: (10385, 2),
        80803: (80802, 1),
        6616787: (6616786, 1),
    }
    for q, (w, s) in expected.items():
        if (props[q]["w_q"], props[q]["s_q"]) != (w, s):
            raise AssertionError("prime property mismatch")
    cases = []
    labelled_templates = [
        (1, 1, (0,), None),
        (2, 1, (0,), 80803),
        (2, 2, (0,), 80803),
        (3, 1, (0,), 6616787),
        (3, 2, (0,), 6616787),
        (3, 3, (0,), 6616787),
        (3, 3, (0, 2), 6616787),
    ]
    for beta, m, J, support in labelled_templates:
        for anchor, lower in ((0, 2728), (1, 1639)):
            cases.append(fiber_audit(beta, m, anchor, lower, J, support, trial))
    result = {
        "schema": "a303656.phase3.actual-embeddings.v1",
        "authority": AUTHORITY,
        "shared_residues": {
            "dynamic_67": 2,
            "rigid_20771": 13471,
            "support_rows": 0,
        },
        "row_parameters": {
            "dynamic_67": "K=1+m, E={1+j:j in J}",
            "rigid_20771": {"K": 2, "E": [1]},
            "regular_support": {"K": 2, "E": [1], "coarse_inert_reason": "s_q=1 and beta_q=0 in the selected finite system"},
        },
        "prime_properties": {str(q): props[q] for q in props},
        "cases": cases,
        "scope": "Actual shared-residue pointwise fibers at both anchors, using different lower assignments. Not uniform lower-coordinate saturation and not a complete certificate.",
        "PASS": True,
    }
    result["result_sha256"] = sha256_bytes(canonical_json_bytes(result))
    return result


def qadic_minimum_criterion(delta: int, q: int, K: int, h0: int, h1: int) -> bool:
    delta %= q**K
    nu = K if delta == 0 else min(vp_nonzero(delta, q), K)
    vals = (nu, h0, h1)
    m = min(vals)
    return sum(v == m for v in vals) >= 2


def brute_qadic_criterion(q: int, K: int) -> dict:
    modulus = q**K
    checked = 0
    for delta in range(modulus):
        attainable: set[tuple[int, int]] = set()
        for x in range(modulus):
            vx = clipped_valuation(x, q, K)
            vy = clipped_valuation(x + delta, q, K)
            if vx is not None and vy is not None:
                attainable.add((vx, vy))
        for h0 in range(K):
            for h1 in range(K):
                predicted = qadic_minimum_criterion(delta, q, K, h0, h1)
                actual = (h0, h1) in attainable
                checked += 1
                if predicted != actual:
                    raise AssertionError((q, K, delta, h0, h1, predicted, actual))
    return {"q": q, "K": K, "cases_checked": checked, "PASS": True}


def compatible_pairs_k2_h1(q: int, trial: list[int]) -> dict:
    w = order_mod_prime(5, q, factor_with_primes(q - 1, trial))
    lookup: dict[int, int] = {}
    x = 1
    for b in range(w):
        lookup[x] = b
        x = x * 5 % q
    pairs = []
    x = 1
    for b0 in range(w):
        b1 = lookup.get((x - 2) % q)
        if b1 is not None:
            pairs.append([b0, b1])
        x = x * 5 % q
    payload = json.dumps(pairs, separators=(",", ":")).encode("ascii")
    return {
        "q": q,
        "w_q": w,
        "pair_count": len(pairs),
        "pairs_sha256": sha256_bytes(payload),
        "first_pairs": pairs[:20],
        "contains_6528_2": [6528, 2] in pairs,
        "contains_0_0": [0, 0] in pairs,
    }


def dynamic_common_possible(l: int, trial: list[int]) -> tuple[bool, int, int, list[int]]:
    w = order_mod_prime(5, l, factor_with_primes(l - 1, trial))
    s = lifting_depth(5, l, w)
    modulus = l**s
    H = []
    x = 1
    # ord modulo l^s remains w by the lifting formula.
    for _ in range(w):
        H.append(x)
        x = x * 5 % modulus
    HS = set(H)
    possible = any((x - 2) % modulus in HS for x in H)
    return possible, w, s, H


def build_common_residue_audit() -> dict:
    primes, _ = sieve_primes(100_000)
    trial = primes
    failures = []
    for l in primes:
        if l >= 10_000:
            break
        if l % 4 != 3 or l == 5:
            continue
        possible, w, s, H = dynamic_common_possible(l, trial)
        if not possible:
            failures.append({
                "l": l,
                "w_l": w,
                "s_l": s,
                "group_modulus": l**s,
                "group_size": len(H),
                "group_values": H if len(H) <= 150 else H[:150],
                "group_values_truncated": len(H) > 150,
            })
    qadic_tests = [brute_qadic_criterion(3, 4), brute_qadic_criterion(5, 3)]
    pair_audit = compatible_pairs_k2_h1(20771, trial)
    result = {
        "schema": "a303656.phase3.common-residue-audit.v1",
        "authority": AUTHORITY,
        "rigid_two_anchor_criterion": {
            "notation": "Delta=5^b0-5^b1-2; nu=min(v_q(Delta),K)",
            "iff": "a shared r with prescribed finite valuations h0,h1<K exists iff min(nu,h0,h1) is attained at least twice",
            "special_h0_h1_1": "5^b0-5^b1 == 2 (mod q)",
            "qadic_exhaustive_tests": qadic_tests,
        },
        "q20771_k2_h1": pair_audit,
        "dynamic_two_anchor_criterion": {
            "prescribed_centers": "5^d0-5^d1 == 2 (mod l^K)",
            "existence_all_precisions": "2 belongs to <5>-<5> modulo l^s_l; a solution at l^s_l lifts to every K>=s_l",
            "scan_domain": "l prime, l<10000, l==3 (mod4), l!=5",
            "blocked_l": failures,
            "blocked_count": len(failures),
            "no_universal_density_inference": True,
        },
        "PASS": True,
    }
    result["result_sha256"] = sha256_bytes(canonical_json_bytes(result))
    return result


def build_summary(resource: dict, l3: dict, l67: dict, actual: dict, common: dict) -> dict:
    status_l3 = {
        str(g["beta"]): g["status_counts"]
        for g in l3["groups"]
    }
    status_l67 = {
        str(g["beta"]): g["status_counts"]
        for g in l67["groups"]
    }
    result = {
        "schema": "a303656.phase3.summary.v1",
        "authority": AUTHORITY,
        "verdict": "ONE-ANCHOR REALIZABILITY THEOREM + COMPLETE SYMBOLIC BETA<=3 CLASSIFICATION + EXACT FINITE AUDIT",
        "universal_theorem_scope": (
            "fixed odd coordinate and anchor; select actual resources and support first, let their orders "
            "and retained rows induce final U, then fix or compatibly extend one lower-coordinate point; "
            "preservation of an externally frozen U, global certificate extension, and simultaneous "
            "two-anchor assembly are separate"
        ),
        "bounded_scan": {
            "bound": BOUND,
            "nonregular_rows": resource["all_nonregular_rows"],
        },
        "l3_status_counts": status_l3,
        "l67_status_counts": status_l67,
        "actual_embedding_case_count": len(actual["cases"]),
        "dynamic_common_residue_blocked_under_10000": [x["l"] for x in common["dynamic_two_anchor_criterion"]["blocked_l"]],
        "authority_state_unchanged": True,
        "github_mutations": [],
    }
    result["result_sha256"] = sha256_bytes(canonical_json_bytes(result))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--bound", type=int, default=BOUND)
    args = parser.parse_args()
    if args.bound != BOUND:
        raise AuditError(f"frozen reference bound is {BOUND}")
    out = args.output_dir
    out.mkdir(parents=True, exist_ok=True)

    resource, _, capacities = scan_resources(out)
    write_json(out / "resource_scan_B10000000.json", resource)

    l3 = build_l3_catalog(capacities[3])
    write_json(out / "l3_beta_le_3_literal_catalog.json", l3)

    l67 = build_compressed_catalog(67, capacities[67], actual_s_parity=1)
    write_json(out / "l67_beta_le_3_compressed_catalog.json", l67)

    actual = build_actual_embeddings()
    write_json(out / "actual_67_beta_1_2_3_embeddings.json", actual)

    common = build_common_residue_audit()
    write_json(out / "common_residue_audit.json", common)

    summary = build_summary(resource, l3, l67, actual, common)
    write_json(out / "summary.json", summary)
    print(json.dumps({
        "PASS": True,
        "output_dir": str(out),
        "summary_sha256": summary["result_sha256"],
        "l3_catalog_sha256": l3["catalog_sha256"],
        "l67_catalog_sha256": l67["catalog_sha256"],
    }, sort_keys=True))


if __name__ == "__main__":
    main()
