#!/usr/bin/env python3
"""Independent recomputation of the fibre statistics (max_z N_z, N_0, number of nonempty fibres).
 - every catalogue prime with h3*h5 <= SMALL: pure-Python Counter over pow();
 - a deterministic sample of the remaining primes: plain numpy outer sum (no big-int convolution).
usage: verify_weights.py weights.json [SMALL=60000] [NSAMPLE=40]"""
import sys, json, random
from collections import Counter
import numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])

def main():
    rows = json.load(open(sys.argv[1]))["rows"]
    SMALL = int(sys.argv[2]) if len(sys.argv) > 2 else 60000
    NS = int(sys.argv[3]) if len(sys.argv) > 3 else 40
    n = 0
    for r in rows:
        p, h3, h5 = r["p"], r["h3"], r["h5"]
        if h3 * h5 > SMALL: continue
        for cs, v in r["cls"].items():
            A = [pow(3, int(cs[0]) + 2 * i, p) for i in range(h3)]
            Bv = [pow(5, int(cs[1]) + 2 * j, p) for j in range(h5)]
            assert len(set(A)) == h3 and len(set(Bv)) == h5
            cnt = Counter((x + y) % p for x in A for y in Bv)
            assert (v["maxN"], v["N0"], v["nonempty"]) == (max(cnt.values()), cnt.get(0, 0), len(cnt)), (p, cs)
            assert cnt[v["argz"]] == v["maxN"]
        n += 1
    print(f"[PASS] {n} primes with h3*h5 <= {SMALL}: all four classes recomputed with pow() and Counter")
    rng = random.Random(2026)
    rest = [r for r in rows if SMALL < r["h3"] * r["h5"] <= 3 * 10 ** 7 and r["p"] < 10 ** 8]
    for r in rng.sample(rest, min(NS, len(rest))):
        p, h3, h5 = r["p"], r["h3"], r["h5"]
        for cs, v in r["cls"].items():
            A = np.array([pow(3, int(cs[0]) + 2 * i, p) for i in range(h3)], dtype=np.int64)
            Bv = np.array([pow(5, int(cs[1]) + 2 * j, p) for j in range(h5)], dtype=np.int64)
            u, c = np.unique(((A[:, None] + Bv[None, :]) % p).ravel(), return_counts=True)
            assert (v["maxN"], v["nonempty"]) == (int(c.max()), len(u)), (p, cs)
            assert v["N0"] == (int(c[0]) if u[0] == 0 else 0)
    print(f"[PASS] random sample of {min(NS, len(rest))} larger primes recomputed with a plain outer sum")
    ub = [r["p"] for r in rows if any(v.get("upper_bound_only") for v in r["cls"].values())]
    for r in rows:
        for v in r["cls"].values():
            assert v["maxN"] <= min(r["h3"], r["h5"])
    print(f"[PASS] maxN <= min(h3,h5) everywhere; {len(ub)} huge primes carry only this trivial bound: {ub}")

if __name__ == "__main__":
    main()
