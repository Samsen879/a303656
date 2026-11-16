#!/usr/bin/env python3
"""One-parameter controls for the covering engine (exact CP-SAT + independent re-verification).

(a) POSITIVE CONTROL.  Toy model with bases (2, b2), b2 = 1 modulo every prime used, so that
    s = 2^alpha + 1 and a fibre is a residue class alpha = r (mod ord_p 2).  We let the solver
    search for a covering using ONLY inert primes p = 3 (mod 4).  A covering found here shows the
    search engine returns "Y" when a covering exists, and that the one-parameter analogue of the
    ACP has a positive answer.
(b) LINE RESTRICTION of the real problem.  Restricting a covering of a parity class to a line
    beta = const gives a covering of Z by residue classes  a = r_p (mod h3(p)), one class per
    inert prime (and every such system arises on a single line).  We decide exactly whether such
    a 1-D system exists with all h3(p) | N (resp. h5(p) | N).

usage: toy_1d.py weights.json out.json
"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from ortools.sat.python import cp_model
from arith import sieve, order_by_iteration
from core_tools import load_weights

def solve_cover(N, moduli, tlimit=120):
    """moduli: list of (label, m) with m | N.  Exact: is there one class per label covering Z/N?"""
    model = cp_model.CpModel()
    y = {}
    for k, (lab, m) in enumerate(moduli):
        vs = [model.NewBoolVar(f"y{k}_{r}") for r in range(m)]
        model.AddAtMostOne(vs)
        y[k] = vs
    for x in range(N):
        model.AddBoolOr([y[k][x % m] for k, (lab, m) in enumerate(moduli)])
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = tlimit
    solver.parameters.num_workers = 2
    st = solver.Solve(model)
    if st in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        sol = []
        for k, (lab, m) in enumerate(moduli):
            rs = [r for r in range(m) if solver.Value(y[k][r])]
            if rs:
                sol.append((lab, m, rs[0]))
        # independent re-verification
        assert all(any(x % m == r for _, m, r in sol) for x in range(N))
        return "COVERING", sol
    return ("INFEASIBLE" if st == cp_model.INFEASIBLE else "UNKNOWN(time limit)"), None

def main():
    rows = load_weights(sys.argv[1])
    out = {}
    # (a0) base 2, all odd primes, N = 24: the solver must FIND a covering (Erdos' system exists)
    N = 24
    mods = [(p, order_by_iteration(2, p)) for p in sieve(300) if p > 2 and pow(2, N, p) == 1]
    st, sol = solve_cover(N, mods)
    print(f"(a0) base 2, all odd primes with ord_p(2) | 24: {mods} -> {st}")
    assert st == "COVERING"
    assert all(any(pow(2, al, p) == pow(2, r, p) for p, m, r in sol) for al in range(N))
    print("     covering found:", sol)
    out["a0"] = {"N": N, "status": st, "solution": sol}
    # (a) base 2, inert primes only (orders are odd or 2*odd)
    for N, tl in ((630, 60), (6930, 60)):
        mods = [(p, order_by_iteration(2, p)) for p in sieve(3 * 10 ** 6) if p % 4 == 3 and pow(2, N, p) == 1]
        dens = sum(1 / m for _, m in mods)
        t0 = time.time()
        st, sol = solve_cover(N, mods, tlimit=tl)
        print(f"(a) base 2, inert primes p<3e6 with ord_p(2) | {N}: {len(mods)} primes, sum 1/m = {dens:.3f} -> {st} [{time.time()-t0:.0f}s]", flush=True)
        if sol:
            assert all(any(pow(2, al, p) == pow(2, r, p) for p, m, r in sol) for al in range(N))
            print("    covering:", sol)
        out[f"a_{N}"] = {"status": st, "solution": sol, "available": mods, "density": dens}
    # (b) line restrictions of the real problem
    for which in ("h3", "h5"):
        for N, tl in ((315, 120), (3465, 120)):
            mods = [(r["p"], r[which]) for r in rows if N % r[which] == 0]
            dens = sum(1 / m for _, m in mods)
            t0 = time.time()
            if dens < 1:
                st, sol = "INFEASIBLE (sum of 1/m < 1)", None
            else:
                st, sol = solve_cover(N, mods, tlimit=tl)
            print(f"(b) {which}-line, N={N}: {len(mods)} inert primes with {which} | N, sum 1/m = {dens:.3f} -> {st} "
                  f"[{time.time()-t0:.0f}s]", flush=True)
            if sol:
                print("    covering:", sol)
            out[f"b_{which}_{N}"] = {"status": st, "n_primes": len(mods), "density": dens, "solution": sol}
    json.dump(out, open(sys.argv[2], "w"))

if __name__ == "__main__":
    main()
