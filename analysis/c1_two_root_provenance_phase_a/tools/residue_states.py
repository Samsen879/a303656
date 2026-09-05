"""Exact finite paired-mask quotient by a low-digit p-adic trie.

Only integer operations and the Python standard library are used. The input
centers and local period are fixed by the original row, never by a macro.
"""
from __future__ import annotations
from collections import defaultdict
from dataclasses import dataclass
from math import gcd

@dataclass(frozen=True)
class StateClass:
    mask: int
    representative: int
    residue_count: int


def power_cycle(p: int, precision: int, base: int = 5) -> list[int]:
    if p < 3 or precision < 2 or gcd(p, base) != 1:
        raise ValueError('Require p>=3, K>=2, gcd(p,base)=1.')
    modulus = p ** precision
    values = [1]
    v = base % modulus
    while v != 1:
        values.append(v)
        if len(values) > modulus:
            raise ValueError('Invalid multiplicative cycle.')
        v = v * base % modulus
    return values


def direct_mask(p: int, precision: int, accepted: frozenset[int],
                powers: list[int], residue: int) -> int:
    """Independent literal local valuation at every anchor-period demand."""
    modulus = p ** precision
    result = 0
    period = len(powers)
    for c, shift in enumerate((1, 3)):
        for d, v in enumerate(powers):
            delta = (residue - shift - v) % modulus
            if delta == 0:
                continue                    # local zero is unresolved
            order = 0
            while delta % p == 0:
                order += 1
                delta //= p
            if order in accepted:
                result |= 1 << (c * period + d)
    return result


def trie_quotient(p: int, precision: int, accepted: frozenset[int],
                  powers: list[int]) -> tuple[list[StateClass], dict]:
    """Compress ALL p**K residues, without visiting every residue.

At a node of depth h, absent next digits are one bucket: each of the still
matching centers then has valuation exactly h. The bucket weight counts all
absent digits and all unrestricted higher digits. Present digits recurse.
Masks are subsequently quotiented exactly, retaining one genuine residue.
"""
    if precision < 2 or any(h <= 0 or h >= precision or h % 2 != 1 for h in accepted):
        raise ValueError('Accepted valuations must be positive odd values below K.')
    if not accepted:
        raise ValueError('The admitted accepted set must be nonempty.')
    modulus = p ** precision
    period = len(powers)
    centers: dict[int, int] = {}
    for c, shift in enumerate((1, 3)):
        for d, v in enumerate(powers):
            t = (shift + v) % modulus
            centers[t] = centers.get(t, 0) | (1 << (c * period + d))
    data: dict[int, list[int]] = {}  # mask -> [representative, weight]
    stats = {'distinct_centers': len(centers), 'trie_nodes': 0,
             'emitted_buckets': 0, 'zero_leaves': 0}

    def emit(mask: int, representative: int, count: int) -> None:
        stats['emitted_buckets'] += 1
        if mask not in data:
            data[mask] = [representative, count]
        else:
            data[mask][0] = min(data[mask][0], representative)
            data[mask][1] += count

    def visit(items: list[tuple[int, int]], depth: int,
              prefix: int, accepted_mask: int, place: int) -> None:
        stats['trie_nodes'] += 1
        if depth == precision:
            # Items matching all K digits are precisely unresolved local zeros.
            stats['zero_leaves'] += 1
            emit(accepted_mask, prefix, 1)
            return
        groups: dict[int, list[tuple[int, int]]] = defaultdict(list)
        all_remaining = 0
        for center, demand_mask in items:
            groups[(center // place) % p].append((center, demand_mask))
            all_remaining |= demand_mask
        if len(groups) < p:
            missing = next(a for a in range(p) if a not in groups)
            output_mask = accepted_mask
            if depth in accepted:
                output_mask |= all_remaining
            emit(output_mask, prefix + missing * place,
                 (p - len(groups)) * p ** (precision - depth - 1))
        for digit, group in sorted(groups.items()):
            next_mask = accepted_mask
            if depth in accepted:
                group_mask = 0
                for _, demand_mask in group:
                    group_mask |= demand_mask
                next_mask |= all_remaining ^ group_mask
            visit(group, depth + 1, prefix + digit * place,
                  next_mask, place * p)

    visit(list(centers.items()), 0, 0, 0, 1)
    states = [StateClass(mask, item[0], item[1]) for mask, item in sorted(data.items())]
    assert sum(s.residue_count for s in states) == modulus
    stats.update(raw_residues=modulus, exact_states=len(states), local_period=period,
                 residue_weight_sum=sum(s.residue_count for s in states))
    return states, stats


def k2_signature(p: int, powers: list[int], residue: int) -> tuple:
    """Independent K=2 analytic signature, using a mod-p cycle and p^2 zeros.

For regular rows this records (base log, excluded zero log), and for a
nonregular row it records one rigid class or the empty event. No trie is used.
"""
    first = {}
    for j, v in enumerate(powers):
        first.setdefault(v % p, j)
    full_logs = {v: j for j, v in enumerate(powers)}
    w = len(first)
    result = []
    for shift in (1, 3):
        base_log = first.get((residue - shift) % p)
        if base_log is None:
            result.append(None)
        elif len(powers) == w:
            if (residue - shift) % (p * p) in full_logs:
                result.append(None)
            else:
                result.append(('rigid', base_log))
        else:
            zero = full_logs.get((residue - shift) % (p * p))
            assert zero is not None
            result.append(('dynamic', base_log, zero))
    return tuple(result)
