#!/usr/bin/env python3
"""Exact fibre statistics for every inert prime of a catalogue.
usage: compute_weights.py catalogue.json out.json"""
import sys, json, time
sys.path.insert(0, __file__.rsplit('/', 1)[0])
from acp import PrimeData, CLASSES
from arith import prime_factors

def main():
    cat = json.load(open(sys.argv[1]))
    rows = [r for r in cat["rows"] if r["p"] > 3 and r["mod4"] == 3]
    out = []
    t0 = time.time()
    for k, r in enumerate(rows):
        d = PrimeData(r["p"])
        assert (d.o1, d.o2, d.h1, d.h2) == (r["ord3"], r["ord5"], r["h3"], r["h5"])
        rec = {"p": d.p, "ord3": d.o1, "ord5": d.o2, "h3": d.h1, "h5": d.h2, "H": d.H,
               "supp": prime_factors(d.h1 * d.h2), "cls": {}}
        for c in CLASSES:
            if d.p > 6 * 10 ** 6 and d.h1 * d.h2 > 5 * 10 ** 7:
                # huge prime with a huge quotient: keep only the trivial bound max_z N_z <= min(h3,h5),
                # i.e. weight <= 1/H_p (flagged; every later use only needs an upper bound)
                rec["cls"][f"{c[0]}{c[1]}"] = {"maxN": min(d.h1, d.h2), "argz": None, "N0": None,
                                               "nonempty": None, "upper_bound_only": True}
                continue
            m, z, n0, ne = d.max_count(c)
            rec["cls"][f"{c[0]}{c[1]}"] = {"maxN": m, "argz": z, "N0": n0, "nonempty": ne}
        out.append(rec)
        if k % 200 == 0 or d.p > 6 * 10 ** 6:
            print(k, len(rows), d.p, f"{time.time()-t0:.0f}s", flush=True)
    json.dump({"B": cat["B"], "rows": out}, open(sys.argv[2], "w"))
    print("done", len(out), f"{time.time()-t0:.0f}s")

if __name__ == "__main__":
    main()
