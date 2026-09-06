#!/usr/bin/env python3
"""Exact reference laboratory. Standard library only; no repository imports.

Tests mathematical formulations, not a proof-assistant formalization.
All primality/order/valuation decisions are exact. Configuration labels in
synthetic experiments are explicitly not actual prime resources.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations, product
from math import gcd, isqrt, lcm, prod
from pathlib import Path
import hashlib
import json
import random

ROOT = Path(__file__).resolve().parents[1]
DEMANDS = {"FALSE": 0, "BOTH": 8, "A0": 10, "A1": 12, "EITHER": 14, "TRUE": 15}


def dump_json(path: Path, obj: object) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def frac(x: Fraction) -> str:
    return str(x)


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    return all(n % a for a in range(3, isqrt(n) + 1, 2))


def factor_trial(n: int) -> dict[int, int]:
    if n < 1:
        raise ValueError("factorization input must be positive")
    out: dict[int, int] = {}
    p = 2
    while p * p <= n:
        while n % p == 0:
            out[p] = out.get(p, 0) + 1
            n //= p
        p = 3 if p == 2 else p + 2
    if n > 1:
        out[n] = out.get(n, 0) + 1
    return out


def vp_clipped(n: int, p: int, K: int) -> int:
    """Return K for a local zero. Fatal tests must still require h < K."""
    n %= p ** K
    if not n:
        return K
    h = 0
    while n % p == 0:
        h += 1
        n //= p
    return h


def signature(q: int) -> dict:
    if q == 5 or q % 4 != 3 or not is_prime_trial(q):
        raise ValueError("not an admitted actual prime")
    w = q - 1
    for p in factor_trial(w):
        while w % p == 0 and pow(5, w // p, q) == 1:
            w //= p
    fw = factor_trial(w)
    assert pow(5, w, q) == 1
    assert all(pow(5, w // p, q) != 1 for p in fw)
    s = 1
    while pow(5, w, q ** (s + 1)) == 1:
        s += 1
    return {"q": q, "w": w, "s": s, "factor_w": {str(p): e for p, e in fw.items()},
            "prime_method": "complete trial division", "order_method": "all prime divisors tested"}


def powers(period: int, modulus: int) -> list[int]:
    vals = []
    a = 1
    for _ in range(period):
        vals.append(a)
        a = a * 5 % modulus
    assert a == 1
    return vals


def accept(value: int, p: int, K: int, E: frozenset[int]) -> bool:
    h = vp_clipped(value, p, K)
    return h < K and h in E


def row_normal_form(p: int, K: int, E: frozenset[int], r: int, c: int,
                    sig: dict, vals: list[int]) -> dict:
    """Classify using low logarithm and independent full-power lookup."""
    w, s = sig["w"], sig["s"]
    a = max(0, K - s)
    target = (r - 3 ** c) % (p ** K)
    logs = {vals[b] % p: b for b in range(w)}
    b = logs.get(target % p)
    if b is None:
        return {"type": "inactive", "b": None}
    h = vp_clipped(target - vals[b], p, K)
    if h < min(s, K):
        return {"type": "rigid" if h in E else "inactive", "b": b, "h": h}
    if K <= s:
        return {"type": "local_zero_guard", "b": b}
    dlog = {v: d for d, v in enumerate(vals)}
    if target not in dlog:
        raise AssertionError("principal subgroup lifting classification failed")
    return {"type": "dynamic", "b": b, "center": dlog[target] % (p ** a), "a": a, "s": s}


def coarse_from_form(x: int, beta: int, p: int, E: frozenset[int], sig: dict, form: dict) -> bool:
    if form["b"] is None or x % sig["w"] != form["b"]:
        return False
    if form["type"] == "rigid":
        return True
    if form["type"] != "dynamic":
        return False
    m = min(beta, form["a"])
    j = vp_clipped(x - form["center"], p, m)
    return j < m and sig["s"] + j in E


def audit_small_rows() -> dict:
    panels = [(p, K) for p in (3, 7, 11) for K in (2, 3)] + [(3, 4)]
    counts = {"residue_accepted_set_systems": 0, "full_anchor_cells": 0,
              "coarse_anchor_cells": 0, "mismatches": 0}
    kinds: dict[str, int] = {}
    rows = []
    for p, K in panels:
        sig = signature(p)
        w, s = sig["w"], sig["s"]
        a = max(0, K - s)
        ell = w * p ** a
        vals = powers(ell, p ** K)
        odd = list(range(1, K, 2))
        local_systems = 0
        for Ebits in range(1, 1 << len(odd)):
            E = frozenset(odd[j] for j in range(len(odd)) if (Ebits >> j) & 1)
            for r in range(p ** K):
                forms = [row_normal_form(p, K, E, r, c, sig, vals) for c in (0, 1)]
                full = [[accept(r - 3 ** c - v, p, K, E) for v in vals] for c in (0, 1)]
                assert not any(x and y for x, y in zip(*full))
                if forms[0]["b"] is not None and forms[1]["b"] is not None:
                    assert forms[0]["b"] != forms[1]["b"]
                for c in (0, 1):
                    kinds[forms[c]["type"]] = kinds.get(forms[c]["type"], 0) + 1
                    for beta in range(a + 1):
                        U = w * p ** beta
                        for x in range(U):
                            direct = all(full[c][d] for d in range(x, ell, U))
                            formula = coarse_from_form(x, beta, p, E, sig, forms[c])
                            assert direct == formula, (p, K, E, r, c, beta, x, forms[c])
                            counts["coarse_anchor_cells"] += 1
                counts["full_anchor_cells"] += 2 * ell
                counts["residue_accepted_set_systems"] += 1
                local_systems += 1
        rows.append({"p": p, "K": K, "w": w, "s": s, "ell": ell, "systems": local_systems,
                     "beta_tested": list(range(a + 1))})
    return {"classification": "ACTUAL ROW-LEVEL ARITHMETIC; beta is a prescribed local support parameter",
            "scope": "all listed residues and nonempty odd accepted sets, not all admitted multirow systems",
            "counts": counts, "form_histogram": kinds, "panels": rows}


def eval_demand(code: int, covered: int) -> bool:
    return bool(code & (1 << covered))


def residual_demand(code: int, word: tuple[int, ...]) -> int:
    return sum((1 << lower) for lower in range(4)
               if all(eval_demand(code, lower | top) for top in word))


def audit_demands() -> dict:
    hist: dict[str, int] = {}
    names = {v: k for k, v in DEMANDS.items()}
    words = 0
    evaluations = 0
    for n in range(1, 5):
        for word in product(range(4), repeat=n):
            words += 1
            sat0 = all(t & 1 for t in word)
            sat1 = all(t & 2 for t in word)
            sat_or = all(t != 0 for t in word)
            for name, code in DEMANDS.items():
                residual = residual_demand(code, word)
                assert residual in names
                key = name + " -> " + names[residual]
                hist[key] = hist.get(key, 0) + 1
                for lower in range(4):
                    x0, x1 = bool(lower & 1), bool(lower & 2)
                    formula = {
                        "FALSE": False,
                        "TRUE": True,
                        "A0": x0 or sat0,
                        "A1": x1 or sat1,
                        "BOTH": (x0 or sat0) and (x1 or sat1),
                        "EITHER": x0 or x1 or sat_or,
                    }[name]
                    assert formula == eval_demand(residual, lower)
                    evaluations += 1
    split = (1, 2, 1)
    assert residual_demand(DEMANDS["EITHER"], split) == DEMANDS["TRUE"]
    assert residual_demand(DEMANDS["BOTH"], split) == DEMANDS["BOTH"]
    return {"top_words": words, "truth_evaluations": evaluations, "transition_histogram": hist,
            "mismatches": 0, "split_either_residual": "TRUE", "split_both_residual": "BOTH"}


def crt_pair(a: int, m: int, b: int, n: int) -> tuple[int, int] | None:
    g = gcd(m, n)
    if (b - a) % g:
        return None
    v = n // g
    k = 0 if v == 1 else (((b - a) // g) * pow(m // g, -1, v)) % v
    M = lcm(m, n)
    return (a + m * k) % M, M


def actual_split() -> dict:
    U, lower = 228470, 3410
    specs = [(67, 2), (20771, 20775)]
    arrays: list[list[list[bool]]] = []
    for p, r in specs:
        sig = signature(p)
        ell = sig["w"] * p ** max(0, 2 - sig["s"])
        vals = powers(ell, p * p)
        arrays.append([[accept(r - 3 ** c - v, p, 2, frozenset({1})) for v in vals] for c in (0, 1)])
    covered = [[False] * U for _ in (0, 1)]
    mask_digest = hashlib.sha256()
    for d in range(U):
        bits = []
        for c in (0, 1):
            for ri in (0, 1):
                tab = arrays[ri][c]
                bits.append(int(tab[d % len(tab)]))
            covered[c][d] = any(arrays[ri][c][d % len(arrays[ri][c])] for ri in (0, 1))
        mask_digest.update(bytes(bits))
    sat = [[y for y in range(lower) if all(covered[c][y + lower * k] for k in range(67))] for c in (0, 1)]
    slices = {}
    for ri, (p, r) in enumerate(specs):
        for c in (0, 1):
            hits = []
            for z in range(67):
                result = crt_pair(0, lower, z, 67)
                assert result is not None
                d = result[0]
                tab = arrays[ri][c]
                if tab[d % len(tab)]:
                    hits.append(z)
            slices[f"q={p},c={c}"] = hits
    assert slices["q=67,c=0"] == list(range(1, 67))
    assert slices["q=67,c=1"] == []
    assert slices["q=20771,c=0"] == []
    assert slices["q=20771,c=1"] == [0]
    common_safe = [d for d in range(U) if not covered[0][d] and not covered[1][d]]
    assert sat == [[], [1705]]
    return {"classification": "ACTUAL SHARED-RESIDUE LOCAL SPLIT; NOT A COMPLETE POOLED COVER",
            "U": U, "L": U, "lower_modulus": lower, "rows": specs,
            "exact_slices": slices, "Sat0": sat[0], "Sat1": sat[1],
            "safe_counts": [U - sum(v) for v in covered],
            "common_safe_count": len(common_safe), "first_common_safe": common_safe[0],
            "mask_byte_order": "for d increasing: q67c0,q20771c0,q67c1,q20771c1",
            "mask_sha256": mask_digest.hexdigest(), "E0": [0], "E1": list(range(1, 67))}


def paired_rigid_examples() -> dict:
    cases = []
    for q, r in [(20771, 96315155), (40487, 25919)]:
        sig = signature(q)
        vals = powers(sig["w"], q * q)
        logs = []
        for c in (0, 1):
            hits = [d for d, v in enumerate(vals) if accept(r - 3 ** c - v, q, 2, frozenset({1}))]
            assert len(hits) == 1
            logs.append(hits[0])
        assert logs[0] != logs[1]
        assert (pow(5, logs[0], q) - pow(5, logs[1], q) - 2) % q == 0
        p = max(map(int, sig["factor_w"]))
        h = p ** sig["factor_w"][str(p)]
        u = sig["w"] // h
        cases.append({"q": q, "r": r, "w": sig["w"], "s": sig["s"], "logs": logs,
                      "top_p": p, "h": h, "u": u,
                      "lower_classes": [b % u for b in logs], "top_positions": [b % h for b in logs]})
    assert cases[0]["logs"] == [6528, 2]
    assert cases[1]["logs"] == [3968, 14260]
    assert cases[1]["lower_classes"] == [0, 0]
    return {"classification": "ACTUAL SHARED-RESIDUE ROW MASKS, NOT COMPLETE COVERS", "cases": cases}



def audit_mixed_row() -> dict:
    # An actual nonregular row can be dynamic at one anchor and rigid at
    # the other. No gigantic full period is enumerated or claimed.
    q, w, K = 20771, 10385, 4
    b0, b1 = 6528, 2
    r = (1 + pow(5, b0, q ** K)) % (q ** K)
    E = frozenset({1, 3})
    delta = (pow(5, b0, q * q) - pow(5, b1, q * q) - 2) % (q * q)
    assert vp_clipped(delta, q, 2) == 1
    samples = []
    for k in (0, 1, q, q + 1, q * q, q * q + q):
        d0, d1 = b0 + w * k, b1 + w * k
        h0 = vp_clipped(r - 1 - pow(5, d0, q ** K), q, K)
        h1 = vp_clipped(r - 3 - pow(5, d1, q ** K), q, K)
        expected0 = min(K, 2 + vp_clipped(k, q, K))
        assert h0 == expected0 and h1 == 1
        samples.append({"k": k, "h0_clipped": h0, "h1_clipped": h1,
                        "fatal0": h0 < K and h0 in E, "fatal1": True})
    return {"classification": "ACTUAL SHARED-RESIDUE SINGLE ROW; SELECTED EXPONENT CHECKS PLUS SYMBOLIC LTE PROOF",
            "q": q, "K": K, "E": [1, 3], "r": r, "w": w, "s": 2,
            "anchor0_type": "dynamic", "anchor0_guard": b0,
            "anchor1_type": "rigid, valuation 1", "anchor1_guard": b1,
            "guard_modulus": w, "full_period_not_enumerated": w * q * q,
            "samples": samples}


def cylinder_mask(p: int, beta: int, depth: int, pos: int) -> int:
    return sum(1 << z for z in range(p ** beta) if z % (p ** depth) == pos % (p ** depth))


def shell_mask(p: int, beta: int, center: int, J: frozenset[int]) -> int:
    return sum(1 << z for z in range(p ** beta) if vp_clipped(z - center, p, beta) in J)


def prefix_maximal(cylinders: list[tuple[int, int]], p: int, beta: int) -> list[tuple[int, int]]:
    unique = set(cylinders)
    out = []
    for depth, pos in sorted(unique):
        if not any(depth >= e and pos % (p ** e) == a for e, a in out):
            out.append((depth, pos))
    return out


def audit_prefix() -> dict:
    p, beta = 3, 2
    universe = (1 << (p ** beta)) - 1
    rigids = [(e, a) for e in (1, 2) for a in range(p ** e)]
    stats = []
    for J in (frozenset(), frozenset({0}), frozenset({1})):
        dynamic_primitives = [(j + 1, k * p ** j) for j in J for k in range(1, p)]
        dynamic = shell_mask(p, beta, 0, J)
        assert dynamic == (sum(cylinder_mask(p, beta, e, a) for e, a in dynamic_primitives))
        full_count = 0
        for bits in range(1 << len(rigids)):
            chosen = [rigids[i] for i in range(len(rigids)) if (bits >> i) & 1]
            union = dynamic
            for e, a in chosen:
                union |= cylinder_mask(p, beta, e, a)
            frontier = prefix_maximal(chosen + dynamic_primitives, p, beta)
            frontier_union = 0
            kraft = Fraction(0)
            for e, a in frontier:
                mask = cylinder_mask(p, beta, e, a)
                assert not (frontier_union & mask)
                frontier_union |= mask
                kraft += Fraction(1, p ** e)
            assert union == frontier_union
            assert (union == universe) == (kraft == 1)
            full_count += union == universe
        stats.append({"J": sorted(J), "subsets": 4096, "full_covers": full_count})
    return {"classification": "ABSTRACT PREFIX GEOMETRY; J={1} IS NOT AN ACTUAL DYNAMIC-3 EVENT",
            "checks": 12288, "panels": stats, "mismatches": 0}


@dataclass(frozen=True)
class Clause:
    masks: tuple[int, ...]
    tokens: frozenset[tuple[int, int]]
    provenance: tuple[str, ...]


def join_tokens(*sets: frozenset[tuple[int, int]]) -> frozenset[tuple[int, int]] | None:
    d: dict[int, int] = {}
    for tokens in sets:
        for row, state in tokens:
            if row in d and d[row] != state:
                return None
            d[row] = state
    return frozenset(d.items())


def minimal_slice_covers(masks: list[int], full: int) -> list[tuple[int, ...]]:
    out: list[tuple[int, ...]] = []
    for size in range(1, len(masks) + 1):
        for I in combinations(range(len(masks)), size):
            if any(set(J).issubset(I) for J in out):
                continue
            u = 0
            for i in I:
                u |= masks[i]
            if u == full:
                out.append(I)
    return out


def contract(clauses: list[Clause], sizes: tuple[int, ...]) -> list[Clause]:
    """Named exact slice-cover witnesses, compatible tokens, inherited guards."""
    active = [a for a in clauses if all(a.masks)]
    if not sizes:
        return active
    if not active:
        return []
    full = (1 << sizes[-1]) - 1
    top = [a.masks[-1] for a in active]
    output: dict[tuple, Clause] = {}
    for I in minimal_slice_covers(top, full):
        token = join_tokens(*(active[i].tokens for i in I))
        if token is None:
            continue
        guards = [(1 << n) - 1 for n in sizes[:-1]]
        for i in I:
            for j in range(len(guards)):
                guards[j] &= active[i].masks[j]
        if not all(guards):
            continue
        provenance = tuple(sorted(set(v for i in I for v in active[i].provenance)))
        # Exact geometry/token duplicates need just one witness for existence;
        # every retained term still has a named original provenance.
        key = (tuple(guards), token)
        output.setdefault(key, Clause(tuple(guards), token, provenance))
    return list(output.values())


def root_clauses(clauses: list[Clause], sizes: tuple[int, ...]) -> list[Clause]:
    while sizes:
        clauses = contract(clauses, sizes)
        sizes = sizes[:-1]
    return clauses


def audit_stateful_contraction() -> dict:
    rng = random.Random(20260905)
    systems = assignments = comparisons = derived = 0
    both_count = pooled_count = 0
    for sizes in ((9,), (3, 5)):
        for _ in range(180):
            rows = 3
            tagged = []
            # One nonempty side in each state is allowed. There are 6 original
            # state events, keeping exhaustive minimal-cover enumeration small.
            for q in range(rows):
                for state in (0, 1):
                    c = rng.randrange(2)
                    masks = []
                    rank = rng.randrange(len(sizes))
                    for k, n in enumerate(sizes):
                        if k > rank or (k < rank and rng.randrange(2)):
                            masks.append((1 << n) - 1)
                        else:
                            # On 3^2 use actual 3-adic cylinders (or a shell).
                            if n == 9:
                                if rng.randrange(4) == 0:
                                    masks.append(shell_mask(3, 2, rng.randrange(9), frozenset({0})))
                                else:
                                    e = rng.choice((1, 2))
                                    masks.append(cylinder_mask(3, 2, e, rng.randrange(3 ** e)))
                            else:
                                masks.append(1 << rng.randrange(n))
                    atom = Clause(tuple(masks), frozenset({(q, state)}), (f"q{q}s{state}c{c}",))
                    tagged.append((c, atom))
            symbolic = {}
            for tag in ("A0", "A1", "EITHER"):
                chosen = [a for c, a in tagged if tag == "EITHER" or c == int(tag[-1])]
                symbolic[tag] = root_clauses(chosen, sizes)
                derived += len(symbolic[tag])
            for s in product((0, 1), repeat=rows):
                original = {(q, s[q]) for q in range(rows)}
                covered0 = covered1 = pooled = True
                for point in product(*(range(n) for n in sizes)):
                    cov = [False, False]
                    for c, atom in tagged:
                        if atom.tokens.issubset(original) and all((m >> v) & 1 for m, v in zip(atom.masks, point)):
                            cov[c] = True
                    covered0 &= cov[0]
                    covered1 &= cov[1]
                    pooled &= any(cov)
                for tag, direct in (("A0", covered0), ("A1", covered1), ("EITHER", pooled)):
                    symbolic_truth = any(a.tokens.issubset(original) for a in symbolic[tag])
                    assert direct == symbolic_truth
                    comparisons += 1
                both_count += covered0 and covered1
                pooled_count += pooled
                assignments += 1
            systems += 1
    assert join_tokens(frozenset({(1, 0)}), frozenset({(1, 1)})) is None
    assert join_tokens(frozenset({(1, 0)}), frozenset({(1, 0)})) == frozenset({(1, 0)})
    return {"classification": "ABSTRACT CONFIGURATION MODELS, NOT ACTUAL PRIME REALIZATION",
            "seed": 20260905, "systems": systems, "global_state_assignments": assignments,
            "root_comparisons": comparisons, "root_terms": derived, "both_covers": both_count,
            "pooled_covers": pooled_count, "mismatches": 0,
            "scope": "three rows, two one-sided configurations per row; paired rigidity tested separately with actual q"}


def audit_blocker_models() -> dict:
    # Coordinate sizes 3^2 and 7. One paired rigid row at rank 7 is assigned
    # to the full-depth 3^2 blocker, despite an original dynamic 3-bundle.
    cases = direct_cells = 0
    cells = [(x, z) for x in range(9) for z in range(7)]
    for center in range(9):
        dyn3 = {x for x in range(9) if x % 3 != center % 3}
        for a in cells:
            for b in cells:
                if a == b:
                    continue  # rowwise anchor exclusion
                banned = {a[0], b[0]}
                budget = Fraction(len(dyn3), 9) + Fraction(len(banned), 9)
                assert budget < 1
                x = next(x for x in range(9) if x not in dyn3 and x not in banned)
                # A later dynamic-7 row has the lower guard x==0 (mod3).
                z = 2 if x % 3 == 0 else 0
                assert (x, z) != a and (x, z) != b
                assert x not in dyn3
                assert not (x % 3 == 0 and z != 2)
                # Direct original events, not projected blocker strips.
                direct_safe = sum(xx not in dyn3 and not (xx % 3 == 0 and zz != 2)
                                  and (xx, zz) not in (a, b) for xx, zz in cells)
                lower_bound = (1 - budget) * Fraction(1, 7) * 63
                assert direct_safe >= lower_bound > 0
                direct_cells += 63
                cases += 1
    return {"classification": "ABSTRACT TRIANGULAR NORMAL-FORM SYSTEMS",
            "models": cases, "direct_cells": direct_cells, "mismatches": 0,
            "new_feature": "a rank-7 rigid paired row blocked at depth 2 in an occupied dynamic-3 coordinate"}


def verify_lucas_certificates(data: dict) -> set[int]:
    certs = data["certificates"]
    done: set[int] = set()
    visiting: set[int] = set()
    def verify(n: int) -> None:
        if n in done:
            return
        if n in visiting:
            raise AssertionError("cyclic primality certificate")
        visiting.add(n)
        cert = certs[str(n)]
        if n == 2:
            assert cert["method"] == "base"
        else:
            assert n > 2 and n % 2 == 1 and cert["method"] == "lucas_full_order"
            f = {int(p): int(e) for p, e in cert["factors_n_minus_one"].items()}
            assert f and all(p >= 2 and e >= 1 for p, e in f.items())
            assert prod(p ** e for p, e in f.items()) == n - 1
            for p in f:
                assert p < n
                verify(p)
            a = int(cert["base"])
            assert 1 < a < n and pow(a, n - 1, n) == 1
            assert all(pow(a, (n - 1) // p, n) != 1 for p in f)
        visiting.remove(n)
        done.add(n)
    for t in data["targets"]:
        verify(int(t))
    return done


def audit_cyclotomic() -> dict:
    data = json.loads((ROOT / "results/primality_certificates.json").read_text())
    done = verify_lucas_certificates(data)
    factorizations = {
        81: [4861, 11419697846380955982026777206637491],
        162: [3, 1783, 5023, 2066067271380136212224701233463],
    }
    result = []
    for m, factors in factorizations.items():
        value = 5 ** 54 + (5 ** 27 if m == 81 else -(5 ** 27)) + 1
        assert len(factors) == len(set(factors))
        assert all(p in done for p in factors)
        assert prod(factors) == value
        # Every factor's precise q-adic valuation in the cyclotomic is one.
        assert all(value % p == 0 and value % (p * p) != 0 for p in factors)
        result.append({"m": m, "value": str(value), "factors": [str(p) for p in factors], "squarefree": True})
    return {"classification": "EXACT FINITE CERTIFICATE, NO PRIME-SIZE CUTOFF",
            "primality_nodes_verified": len(done), "factorizations": result,
            "new_theorem": "R_(3,4) is empty",
            "combined_with_source_depths_1_to_3": {"minimum_rigid_depth": 5,
                  "pooled_rigid_only_prime_lower_bound": 122, "pooled_dynamic_allowed_prime_lower_bound": 31,
                  "one_anchor_rigid_only_prime_lower_bound": 243, "one_anchor_dynamic_allowed_prime_lower_bound": 61},
            "warning": "necessary lower bounds, not sharpness or existence claims"}


def audit_sparse_subclass() -> dict:
    sigs = [signature(q) for q in (3, 67, 20771, 40487, 1645333507)]
    budget3 = Fraction(3, 4) + Fraction(2, 27)
    assert budget3 == Fraction(89, 108) < 1
    for p in (3, 7, 11, 19, 31, 67):
        assert Fraction(p, p + 1) + Fraction(2, p * p) < 1
    return {"classification": "SYMBOLIC UNIFORM COROLLARY WITH EXACT ARITHMETIC SIGNATURE CHECKS",
            "signatures": sigs, "assignments": [
                {"q": 20771, "coordinate": 5, "depth": 1, "worst_pair_load": "2/5", "dynamic_load": "0"},
                {"q": 40487, "coordinate": 653, "depth": 1, "worst_pair_load": "2/653", "dynamic_load": "0"},
                {"q": 1645333507, "coordinate": 3, "depth": 3, "worst_pair_load": "2/27", "dynamic_load_supremum": "3/4"}],
            "budget_3": frac(budget3), "slack_3": frac(1 - budget3),
            "universal_scope": "all nonregular rows contained in {20771,40487,1645333507}; all other rows regular of arbitrary size",
            "not_claimed": "no claim that this is the inventory up to 1645333507"}


def audit_boundary_and_skeleton() -> dict:
    # Genuine boundary example: q11 K2 r0; K2(two-adic)=2, r2=1.
    U, L = 5, 55
    boundary_unsafe = [[(1 - 3 ** c - pow(5, d, 4)) % 4 == 3 for d in range(L)] for c in (0, 1)]
    odds = [[accept(-3 ** c - pow(5, d, 121), 11, 2, frozenset({1})) for d in range(L)] for c in (0, 1)]
    cov = [[a or b for a, b in zip(boundary_unsafe[c], odds[c])] for c in (0, 1)]
    assert all(cov[0]) and not all(cov[1])
    # Boundary-inclusive S1 example with a genuine maximal original odd rank.
    # P={3,7}: U=6, L=42; the dynamic 3-row has beta_3=1.
    s1_rows = ((3, 2), (7, 0))
    s1_cov = []
    for c in (0, 1):
        s1_cov.append([((1 - 3 ** c - pow(5, d, 4)) % 4 == 3) or
                       any(accept(r - 3 ** c - pow(5, d, p * p), p, 2,
                                  frozenset({1})) for p, r in s1_rows)
                       for d in range(42)])
    assert all(s1_cov[0]) and not all(s1_cov[1])
    # Actual regular rows on an EXTERNALLY supplied period, not an actual
    # terminal nonregular seed or an induced-U whole-system construction.
    T = (3, 7, 31)
    Uext = 1302
    sigs = [signature(p) for p in T]
    assert all(s["s"] == 1 for s in sigs)
    assert lcm(*(s["w"] for s in sigs)) == 6
    assert lcm(*(s["w"] * s["q"] for s in sigs)) == Uext
    escape = []
    cov_counts = [0, 0]
    for d in range(Uext):
        cv = [any(accept(2 - 3 ** c - pow(5, d, p * p), p, 2, frozenset({1})) for p in T) for c in (0, 1)]
        for c in (0, 1):
            cov_counts[c] += cv[c]
        if not any(cv):
            escape.append(d)
    assert escape == [0, 651]
    return {"boundary_counterexample": {"classification": "ACTUAL COMPLETE BOUNDARY-INCLUSIVE POOLED COVER, NOT FULL CERTIFICATE",
                "q": 11, "K": 2, "r": 0, "E": [1], "K_two": 2, "r_two": 1, "U": U, "L": L,
                "covered_counts": [sum(x) for x in cov], "pooled_complete": True, "both_complete": False},
            "s1_boundary_example": {"classification": "ACTUAL BOUNDARY-INCLUSIVE POOLED LOWER COVER WITH NONEMPTY TOP EVENT",
                "rows": [{"q": 3, "r": 2}, {"q": 7, "r": 0}], "K_all": 2, "E_all": [1],
                "K_two": 2, "r_two": 1, "U": 6, "L": 42, "maximal_original_odd_rank": 3,
                "lower_domain": "Z/2Z", "A0": [0, 1], "A1": [],
                "full_anchor_covered_counts": [sum(v) for v in s1_cov], "both_complete": False},
            "regular_skeleton": {"classification": "ACTUAL SHARED-RESIDUE FULL-PERIOD SKELETON; PROMOTING L TO COARSE U REQUIRES A SEED",
                "T": list(T), "actual_induced_U_without_seed": 6, "actual_induced_L_without_seed": Uext, "prescribed_coarse_U_with_hypothetical_seed": Uext,
                "r_all": 2, "K_all": 2, "E_all": [1], "common_escapes": escape,
                "anchor_covered_counts": cov_counts, "terminal_nonregular_seed": None}}


def audit_false_potentials() -> dict:
    # State-conflict regression: independently chosen anchor options can pass
    # while no one-hot global configuration realizes the apparent cover.
    options = [(("a", "u"), ("b", "v")), (("a", "v"), ("b", "u"))]
    demands = {"a", "b", "u", "v"}
    actual = [states for states in product((0, 1), repeat=2)
              if set(options[0][states[0]]) | set(options[1][states[1]]) == demands]
    assert actual == []
    # Fractional half of each option covers every demand exactly once.
    for d in demands:
        assert sum(Fraction(d in opt, 2) for row in options for opt in row) == 1
    masks = [1, 1, 2]
    witnesses = minimal_slice_covers(masks, 3)
    assert len(witnesses) == 2
    return {"classification": "ABSTRACT COUNTEREXAMPLES ONLY",
            "configuration_integrality": {"global_assignments": 4, "complete_assignments": 0,
                                           "fractional_half_each_option_feasible": True},
            "macro_mass": {"original_mass": "3/2", "witnesses": [list(w) for w in witnesses],
                           "derived_sum_mass": "2", "geometry_union_mass": "1"},
            "potential_scope": "these defeat these specific counts; no assertion against every possible arithmetic potential"}


def run_all(output: Path) -> dict:
    output = output.resolve()
    if output == ROOT or ROOT in output.parents:
        raise ValueError("replay output must be outside the immutable package")
    output.mkdir(parents=True, exist_ok=True)
    tasks = {
        "demand_audit": audit_demands,
        "row_geometry": audit_small_rows,
        "actual_split": actual_split,
        "paired_rigid": paired_rigid_examples,
        "mixed_row": audit_mixed_row,
        "prefix_geometry": audit_prefix,
        "stateful_contraction": audit_stateful_contraction,
        "blocker_models": audit_blocker_models,
        "cyclotomic_depth4": audit_cyclotomic,
        "sparse_subclass": audit_sparse_subclass,
        "boundary_and_skeleton": audit_boundary_and_skeleton,
        "false_potentials": audit_false_potentials,
    }
    summaries = {}
    for name, task in tasks.items():
        obj = task()
        dump_json(output / (name + ".json"), obj)
        summaries[name] = hashlib.sha256((output / (name + ".json")).read_bytes()).hexdigest()
        print(name + ": PASS", flush=True)
    dump_json(output / "replay_receipt.json", {"schema": 1, "result_sha256": summaries,
              "all_exact_checks_pass": True, "github_writes_performed": "NONE"})
    return summaries
