#!/usr/bin/env python3
"""Lazy counterexample-guided search for finite p^2 covers (Method B).

Candidate variables for p are (q_p, h_p) with t_p = q_p + p*h_p.
For an exponent pair whose local sum is q + p*h modulo p^2, p covers it iff
q_p == q and h_p != h.

The exact adversarial oracle does NOT materialize L3 x L5.  It has local
residues c_p mod ord_{p^2}(3), d_p mod ord_{p^2}(5), imposes pairwise
generalized-CRT compatibility, and uses the exact p-adic lift formula for
powers modulo p^2.  Pairwise compatibility is necessary and sufficient for a
simultaneous global exponent by the generalized CRT.
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

try:
    import z3
except ImportError as exc:  # pragma: no cover
    raise SystemExit("z3-solver is required: python -m pip install z3-solver") from exc


@dataclass(frozen=True)
class PrimeData:
    p: int
    r: int
    s: int
    r2: int
    s2: int
    lift3: int
    lift5: int


def distinct_prime_factors(n: int) -> list[int]:
    out: list[int] = []
    q = 2
    while q * q <= n:
        if n % q == 0:
            out.append(q)
            while n % q == 0:
                n //= q
        q = 3 if q == 2 else q + 2
    if n > 1:
        out.append(n)
    return out


def multiplicative_order_prime(a: int, p: int) -> int:
    order = p - 1
    for q in distinct_prime_factors(p - 1):
        while order % q == 0 and pow(a, order // q, p) == 1:
            order //= q
    return order


def is_prime_trial(n: int) -> bool:
    if n < 2:
        return False
    if n % 2 == 0:
        return n == 2
    q = 3
    while q * q <= n:
        if n % q == 0:
            return False
        q += 2
    return True


def make_data(p: int) -> PrimeData:
    if not is_prime_trial(p) or p % 4 != 3 or p in (3, 5):
        raise ValueError(f"ineligible p={p}")
    pp = p * p
    r = multiplicative_order_prime(3, p)
    s = multiplicative_order_prime(5, p)
    r2 = r if pow(3, r, pp) == 1 else p * r
    s2 = s if pow(5, s, pp) == 1 else p * s
    lift3 = ((pow(3, r, pp) - 1) // p) % p
    lift5 = ((pow(5, s, pp) - 1) // p) % p
    return PrimeData(p, r, s, r2, s2, lift3, lift5)


def parse_primes(text: str) -> list[int]:
    values = [int(x.strip()) for x in text.split(",") if x.strip()]
    if not values or len(values) != len(set(values)):
        raise ValueError("--primes must be a nonempty duplicate-free comma list")
    return values


def exact_local_alpha(d: PrimeData) -> tuple[int, int, int]:
    """Return maxfiber, numerator, denominator for beta_p."""
    p = d.p
    a: list[int] = []
    x = 1
    for _ in range(d.r):
        a.append(x)
        x = x * 3 % p
    b: list[int] = []
    x = 1
    for _ in range(d.s):
        b.append(x)
        x = x * 5 % p
    counts: dict[int, int] = {}
    best = 0
    for av in a:
        for bv in b:
            z = (av + bv) % p
            value = counts.get(z, 0) + 1
            counts[z] = value
            best = max(best, value)
    return best, best, d.r * d.s


def covered_by_prime(d: PrimeData, t: int, c: int, e: int) -> bool:
    pp = d.p * d.p
    sm = (pow(3, c, pp) + pow(5, e, pp)) % pp
    return (t - sm) % d.p == 0 and t != sm


def crt_pair(a: int, m: int, b: int, n: int) -> tuple[int, int]:
    g = math.gcd(m, n)
    if (b - a) % g:
        raise ValueError("incompatible congruences")
    m1, n1 = m // g, n // g
    k = ((b - a) // g * pow(m1, -1, n1)) % n1 if n1 != 1 else 0
    modulus = m * n1
    return (a + m * k) % modulus, modulus


def crt_many(congruences: Iterable[tuple[int, int]]) -> tuple[int, int]:
    value, modulus = 0, 1
    for residue, mod in congruences:
        value, modulus = crt_pair(value, modulus, residue, mod)
    return value, modulus


class ExactCRTOracle:
    """Exact finite-state oracle using local residues plus generalized CRT."""

    def __init__(self, data: list[PrimeData], timeout_ms: int):
        self.data = data
        self.solver = z3.Solver()
        if timeout_ms > 0:
            self.solver.set(timeout=timeout_ms)
        self.cp = {d.p: z3.Int(f"oracle_c_{d.p}") for d in data}
        self.dp = {d.p: z3.Int(f"oracle_d_{d.p}") for d in data}
        self.qp = {d.p: z3.Int(f"oracle_q_{d.p}") for d in data}
        self.hp = {d.p: z3.Int(f"oracle_h_{d.p}") for d in data}

        for d in data:
            p, pp = d.p, d.p * d.p
            cvar, evar = self.cp[p], self.dp[p]
            self.solver.add(cvar >= 0, cvar < d.r2, evar >= 0, evar < d.s2)
            self.solver.add(self.qp[p] >= 0, self.qp[p] < p, self.hp[p] >= 0, self.hp[p] < p)

            arr3 = z3.Array(f"pow3_table_{p}", z3.IntSort(), z3.IntSort())
            arr5 = z3.Array(f"pow5_table_{p}", z3.IntSort(), z3.IntSort())
            for i in range(d.r):
                self.solver.add(z3.Select(arr3, i) == pow(3, i, pp))
            for j in range(d.s):
                self.solver.add(z3.Select(arr5, j) == pow(5, j, pp))

            base3 = z3.Select(arr3, cvar % d.r)
            base5 = z3.Select(arr5, evar % d.s)
            # If the order does not lift, lift3/lift5 is zero; the same formula applies.
            x = (base3 * (1 + p * d.lift3 * ((cvar / d.r) % p))) % pp
            y = (base5 * (1 + p * d.lift5 * ((evar / d.s) % p))) % pp
            sm = (x + y) % pp
            # Noncoverage by p: q differs, or q agrees but h is exactly the forbidden lift.
            self.solver.add(z3.Or(self.qp[p] != sm % p, self.hp[p] == sm / p))

        # Generalized-CRT consistency. Pairwise gcd compatibility is sufficient.
        for i, a in enumerate(data):
            for b in data[i + 1 :]:
                g3 = math.gcd(a.r2, b.r2)
                if g3 > 1:
                    self.solver.add((self.cp[a.p] - self.cp[b.p]) % g3 == 0)
                g5 = math.gcd(a.s2, b.s2)
                if g5 > 1:
                    self.solver.add((self.dp[a.p] - self.dp[b.p]) % g5 == 0)

    def query(self, t_values: dict[int, int]) -> dict:
        self.solver.push()
        for d in self.data:
            t = t_values[d.p]
            self.solver.add(self.qp[d.p] == t % d.p, self.hp[d.p] == t // d.p)
        started = time.perf_counter()
        status = self.solver.check()
        elapsed = time.perf_counter() - started
        result: dict = {"backend": "exact-crt-z3", "seconds": elapsed, "status": str(status)}
        if status == z3.sat:
            model = self.solver.model()
            local_c = [(model.eval(self.cp[d.p]).as_long(), d.r2) for d in self.data]
            local_d = [(model.eval(self.dp[d.p]).as_long(), d.s2) for d in self.data]
            c, L3 = crt_many(local_c)
            e, L5 = crt_many(local_d)
            # Independent direct arithmetic check of the reconstructed global witness.
            if any(covered_by_prime(d, t_values[d.p], c, e) for d in self.data):
                self.solver.pop()
                raise AssertionError("oracle model failed direct witness verification")
            result.update({"c": c, "d": e, "L3": L3, "L5": L5})
        self.solver.pop()
        return result


def heuristic_oracle(
    data: list[PrimeData],
    t_values: dict[int, int],
    rng: random.Random,
    random_samples: int,
) -> dict | None:
    grid = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 50, 100]
    for c in grid:
        for e in grid:
            if all(not covered_by_prime(d, t_values[d.p], c, e) for d in data):
                return {"backend": "exact-witness-grid", "status": "sat", "c": c, "d": e, "seconds": 0.0}
    L3 = math.lcm(*(d.r2 for d in data))
    L5 = math.lcm(*(d.s2 for d in data))
    started = time.perf_counter()
    for _ in range(random_samples):
        c = rng.randrange(L3)
        e = rng.randrange(L5)
        if all(not covered_by_prime(d, t_values[d.p], c, e) for d in data):
            return {
                "backend": "exact-witness-random",
                "status": "sat",
                "c": c,
                "d": e,
                "seconds": time.perf_counter() - started,
            }
    return None


def pruning_result(data: list[PrimeData]) -> dict:
    from fractions import Fraction

    loose = sum((Fraction(1, max(d.r, d.s)) for d in data), Fraction())
    result: dict = {
        "loose_sum": f"{loose.numerator}/{loose.denominator}",
        "loose_sum_decimal": float(loose),
    }
    if loose < 1:
        result.update({"status": "PROVED_IMPOSSIBLE_BY_1_OVER_MAX_LEMMA"})
        return result

    exact_terms = []
    for d in data:
        maxfiber, num, den = exact_local_alpha(d)
        exact_terms.append((d.p, maxfiber, Fraction(num, den)))
    exact_sum = sum((x[2] for x in exact_terms), Fraction())
    result.update({
        "exact_sum": f"{exact_sum.numerator}/{exact_sum.denominator}",
        "exact_sum_decimal": float(exact_sum),
        "exact_terms": [{"p": p, "maxfiber": mf, "alpha": str(a)} for p, mf, a in exact_terms],
    })
    if exact_sum < 1:
        result.update({"status": "PROVED_IMPOSSIBLE_BY_EXACT_LOCAL_CAPACITY"})
    else:
        result.update({"status": "NOT_PRUNED"})
    return result


def run_lazy(args: argparse.Namespace, data: list[PrimeData]) -> dict:
    rng = random.Random(args.seed)
    candidate = z3.Solver()
    if args.candidate_timeout_ms > 0:
        candidate.set(timeout=args.candidate_timeout_ms)
    qvar = {d.p: z3.Int(f"candidate_q_{d.p}") for d in data}
    hvar = {d.p: z3.Int(f"candidate_h_{d.p}") for d in data}
    for d in data:
        candidate.add(qvar[d.p] >= 0, qvar[d.p] < d.p, hvar[d.p] >= 0, hvar[d.p] < d.p)

    exact_oracle: ExactCRTOracle | None = None
    seen_signatures: set[tuple[int, ...]] = set()
    iterations: list[dict] = []
    started = time.perf_counter()

    for iteration in range(1, args.max_iterations + 1):
        check_started = time.perf_counter()
        candidate_status = candidate.check()
        candidate_seconds = time.perf_counter() - check_started
        if candidate_status != z3.sat:
            return {
                "status": "COMPUTATIONAL_OBSERVATION_CANDIDATE_" + str(candidate_status).upper(),
                "warning": "No formal SAT proof certificate was generated; this is not certified UNSAT.",
                "iterations_completed": iteration - 1,
                "constraints": len(seen_signatures),
                "candidate_seconds_last": candidate_seconds,
                "elapsed_seconds": time.perf_counter() - started,
                "iteration_log": iterations,
            }

        model = candidate.model()
        t_values = {
            d.p: model.eval(qvar[d.p], model_completion=True).as_long()
            + d.p * model.eval(hvar[d.p], model_completion=True).as_long()
            for d in data
        }

        oracle_result = None
        if not args.disable_heuristic:
            oracle_result = heuristic_oracle(data, t_values, rng, args.heuristic_samples)
        if oracle_result is None:
            if exact_oracle is None:
                exact_oracle = ExactCRTOracle(data, args.oracle_timeout_ms)
            oracle_result = exact_oracle.query(t_values)

        entry = {
            "iteration": iteration,
            "candidate_seconds": candidate_seconds,
            "oracle": oracle_result,
            "t_values": {str(p): t for p, t in t_values.items()},
        }
        iterations.append(entry)

        if oracle_result["status"] == "unsat":
            return {
                "status": "CANDIDATE_COVER_FROM_EXACT_ORACLE_UNSAT",
                "warning": "A separate solver-independent cover verifier is still required before certification.",
                "t_values": {str(p): t for p, t in t_values.items()},
                "iterations_completed": iteration,
                "elapsed_seconds": time.perf_counter() - started,
                "iteration_log": iterations,
            }
        if oracle_result["status"] != "sat":
            return {
                "status": "UNRESOLVED_ORACLE_" + oracle_result["status"].upper(),
                "iterations_completed": iteration,
                "elapsed_seconds": time.perf_counter() - started,
                "iteration_log": iterations,
            }

        c, e = int(oracle_result["c"]), int(oracle_result["d"])
        signature = tuple((pow(3, c, d.p * d.p) + pow(5, e, d.p * d.p)) % (d.p * d.p) for d in data)
        if signature in seen_signatures:
            return {
                "status": "INTERNAL_DUPLICATE_SIGNATURE",
                "iterations_completed": iteration,
                "elapsed_seconds": time.perf_counter() - started,
                "iteration_log": iterations,
            }
        seen_signatures.add(signature)
        clause = []
        for d, sm in zip(data, signature):
            clause.append(z3.And(qvar[d.p] == sm % d.p, hvar[d.p] != sm // d.p))
        candidate.add(z3.Or(*clause))

    return {
        "status": "UNRESOLVED_ITERATION_LIMIT",
        "iterations_completed": args.max_iterations,
        "constraints": len(seen_signatures),
        "elapsed_seconds": time.perf_counter() - started,
        "iteration_log": iterations,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--primes", required=True)
    ap.add_argument("--max-iterations", type=int, default=100)
    ap.add_argument("--candidate-timeout-ms", type=int, default=5000)
    ap.add_argument("--oracle-timeout-ms", type=int, default=30000)
    ap.add_argument("--heuristic-samples", type=int, default=2000)
    ap.add_argument("--seed", type=int, default=303656)
    ap.add_argument("--disable-pruning", action="store_true")
    ap.add_argument("--disable-heuristic", action="store_true")
    ap.add_argument("--json", type=Path)
    args = ap.parse_args()

    primes = parse_primes(args.primes)
    data = [make_data(p) for p in primes]
    L3 = math.lcm(*(d.r2 for d in data))
    L5 = math.lcm(*(d.s2 for d in data))
    result: dict = {
        "method": "B-lazy-constraint-generation",
        "z3_version": z3.get_version_string(),
        "primes": primes,
        "prime_data": [asdict(d) for d in data],
        "L3": str(L3),
        "L5": str(L5),
        "torus_cardinality": str(L3 * L5),
        "torus_materialized": False,
    }

    prune = pruning_result(data)
    result["pruning"] = prune
    if not args.disable_pruning and prune["status"].startswith("PROVED_"):
        result["search"] = {"status": prune["status"]}
    else:
        result["search"] = run_lazy(args, data)

    text = json.dumps(result, indent=2)
    print(text)
    if args.json:
        args.json.write_text(text + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
