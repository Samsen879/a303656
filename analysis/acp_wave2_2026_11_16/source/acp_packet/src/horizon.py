#!/usr/bin/env python3
"""Horizon of every measure / union-bound / LP-dual argument (Proposition H).

For each inert prime p the fibres F_p^c(z), z in F_p, PARTITION the class c, into n_p <= p
nonempty parts.  Hence for every probability measure mu
        sum_z mu(F_p(z)) = 1   and   max_z mu(F_p(z)) >= 1/n_p >= 1/p,
so   sum_{p in T} max_z mu(F_p(z)) >= sum_{p in T} 1/p.
This script finds, with exact integer arithmetic, the least X0 such that
        sum_{7 <= p <= X0, p = 3 mod 4} 1/p >= 1.
For T = {inert primes in [7, X0]} no measure certificate exists (the fractional relaxation of the
covering problem is feasible), although nothing is said about genuine (integral) coverings.
usage: horizon.py out.json"""
import sys, json
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from arith import sieve
S = 10 ** 40
acc = 0; n = 0; X0 = None
for p in sieve(10 ** 6):
    if p >= 7 and p % 4 == 3:
        acc += S // p          # lower bound for S/p
        n += 1
        if acc >= S:
            X0 = p
            break
assert X0 is not None
# upper bound check for X0 minimal: the sum without the last prime is < 1
acc_up = sum(-(-S // p) for p in sieve(X0 - 1) if p >= 7 and p % 4 == 3)
assert acc_up < S
print(f"[PASS] sum of 1/p over the {n} inert primes 7 <= p <= {X0} is >= 1, and < 1 without p = {X0}")
json.dump({"X0": X0, "n_primes": n}, open(sys.argv[1], "w"))
