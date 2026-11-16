#!/usr/bin/env python3
"""Validation suite for the Phase-1 formalisation (exact, brute force).

usage: validate.py [path-to-audit-zip-root]   (the path enables the comparison with
       the frozen C21 certificate.json; without it hard-coded rationals are used)
"""
import sys, json, itertools, random
from fractions import Fraction as F
from math import gcd
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import model, acp
from arith import factorint, order_by_iteration, odd_part, prime_factors, is_prime_td

OK = []
def check(name, cond, info=""):
    assert cond, f"FAILED: {name} {info}"
    OK.append(name)
    print(f"[PASS] {name} {info}", flush=True)

# ---------------------------------------------------------------- V0 beta zero rule
for pk, (p, k) in {2: (2, 1), 4: (2, 2), 8: (2, 3), 16: (2, 4), 32: (2, 5), 64: (2, 6), 3: (3, 1), 9: (3, 2),
                   27: (3, 3), 81: (3, 4), 7: (7, 1), 49: (7, 2), 343: (7, 3), 11: (11, 1), 121: (11, 2),
                   5: (5, 1), 25: (5, 2), 13: (13, 1), 19: (19, 1), 361: (19, 2)}.items():
    tab = model.beta_table(pk)
    assert sum(tab) == pk * pk
    assert all((tab[y] == 0) == model.beta_zero_rule(p, k, y) for y in range(pk)), pk
check("V0 beta_{p^k}(y)=0 rule (p=2; p=3 mod 4; p=1 mod 4) vs brute force", True, "20 prime powers")
check("V0b beta_8 = (1,2,2,0,1,2,0,0) as in PROOF.md", [F(x, 8) for x in model.beta_table(8)] == [1, 2, 2, 0, 1, 2, 0, 0])

# ---------------------------------------------------------------- V1 A2 audit numbers at q = 120
vals = [model.F_q(120, a) for a in range(120)]
check("V1 q=120: min F = 7/15 exactly at residues 50,70,80,100",
      min(vals) == F(7, 15) and [a for a in range(120) if vals[a] == F(7, 15)] == [50, 70, 80, 100])
check("V1 q=120: mean F = 1, mean F^2 = 107/96", sum(vals) / 120 == 1 and sum(v * v for v in vals) / 120 == F(107, 96))
for q in (240, 360, 600):
    assert all(model.F_q(q, a) == vals[a % 120] for a in range(0, q, 7))
check("V1 q=240,360,600 are pullbacks of q=120 (sampled a)", True)

# ---------------------------------------------------------------- V2 2-adic class rule
R = {(0, 0): 2, (1, 0): 4, (0, 1): 6, (1, 1): 0}   # s mod 8 on the class (alpha mod 2, beta mod 2)
for k in range(3, 9):
    q = 2 ** k
    N1, N2, res = model.s_residues(q)
    t1, t2 = res[q]
    tab = model.beta_table(q)
    for a in range(q):
        for c in R:
            tot = sum(tab[(a - t1[al] - t2[be]) % q] for al in range(c[0], N1 * 2, 2) for be in range(c[1], N2 * 2, 2)
                      ) if False else sum(tab[(a - pow(3, al, q) - pow(5, be, q)) % q]
                                          for al in range(c[0], 2 * max(N1, 2), 2) for be in range(c[1], 2 * max(N2, 2), 2))
            assert (tot == 0) == ((a - R[c]) % 8 in (3, 6, 7)), (k, a, c)
check("V2 2-adic: class c is fully killed iff (a - r_c) mod 8 in {3,6,7}, r=(2,4,6,0); k=3..8, all a", True)
kills = {a: sorted(c for c in R if (a - R[c]) % 8 in (3, 6, 7)) for a in range(8)}
check("V2b a odd kills one alpha-parity (2 classes); a even kills exactly one class",
      all(len(kills[a]) == (2 if a % 2 else 1) for a in range(8)), str(kills))

# ---------------------------------------------------------------- V3 prime 3
for k in range(1, 6):
    q = 3 ** k
    per = 2 * 3 ** (k - 1)
    tab = model.beta_table(q)
    for a in range(q):
        bad = {be for be in range(per) if tab[(a - pow(5, be + per, q)) % q] == 0}
        if a % 3 == 0:
            assert not bad
            continue
        b0 = next(be for be in range(per) if pow(5, be, q) == a % q)
        def v3(n):
            n %= 3 ** (k - 1) if k > 1 else 1
            if n == 0: return 10 ** 6
            v = 0
            while n % 3 == 0: n //= 3; v += 1
            return v
        pred = {be for be in range(per) if (be - b0) % 2 == 0 and v3(be - b0) % 2 == 0 and v3(be - b0) <= k - 2}
        assert bad == pred, (k, a)
        assert F(len(bad), per) == F(1, 2) * sum(F(2, 3) * F(1, 3) ** j for j in range(0, k - 1, 2))
check("V3 prime 3: bad set = {beta = b0 mod 2, v_3(beta-b0) even <= k-2}; a = 0 mod 3 gives no zero; k=1..5", True)

# ---------------------------------------------------------------- V4 regular primes create no zero alone
for q in (49, 343, 121, 361, 529):
    assert all(model.F_q(q, a) > 0 for a in range(q)), q
check("V4 F_q(a) > 0 for all a, q in {7^2,7^3,11^2,19^2,23^2} (real bases 3,5)", True)

# ---------------------------------------------------------------- V5 lift lemma on a jointly non-regular toy
p = 7
b1, b2 = pow(3, 7, 49), pow(5, 7, 49)          # Teichmuller lifts mod 49: (31, 19)
assert (b1, b2) == (31, 19) and pow(b1, 6, 49) == 1 and pow(b2, 6, 49) == 1
def vp(n, p, cap=50):
    if n == 0: return cap
    v = 0
    while n % p == 0: n //= p; v += 1
    return v
w1, w2 = vp(pow(b1, 6, 7 ** 8) - 1, 7), vp(pow(b2, 6, 7 ** 8) - 1, 7)
w = min(w1, w2)
assert w >= 2
for k in (2, 3, 4):
    q = p ** k
    tab = model.beta_table(q)
    N1 = model.order_mod(b1, q); N2 = model.order_mod(b2, q)
    om1, om2 = pow(b1, 7 ** (k - 1), q), pow(b2, 7 ** (k - 1), q)     # Teichmuller lifts mod 7^k
    for a in range(q):
        for ta in range(6):
            for tb in range(6):
                tot = sum(tab[(a - pow(b1, al, q) - pow(b2, be, q)) % q]
                          for al in range(ta, max(N1, 6), 6) for be in range(tb, max(N2, 6), 6))
                tau = (pow(om1, ta, q) + pow(om2, tb, q)) % q
                v = vp((a - tau) % q, 7)
                pred = (v % 2 == 1 and v < min(k, w))
                assert (tot == 0) == pred, (k, a, ta, tb)
check(f"V5 joint-nonregular toy (bases 31,19 at p=7; Wieferich depths w1={w1}, w2={w2}): class is bad iff "
      f"v_7(a - tau) is odd and < min(k, w); k=2,3,4, all a, all 36 tame classes", True)
for z in range(7):
    fib = [(ta, tb) for ta in range(6) for tb in range(6) if (pow(b1, ta, 7) + pow(b2, tb, 7)) % 7 == z]
    lifts = [a for a in range(z, 49, 7) if all((pow(b1, ta, 49) + pow(b2, tb, 49)) % 49 != a for ta, tb in fib)]
    assert len(fib) < 7 and len(lifts) >= 7 - len(fib) and lifts
check("V5b pigeonhole (Lemma L1): every z mod 7 has a lift a mod 49 making the WHOLE fibre bad", True)

# ---------------------------------------------------------------- V6 positive control: an exact zero in a toy model
P = [7, 11, 19]
Bb = 2 * (7 * 11 * 19) ** 2 - 1
q = (7 * 11 * 19) ** 2
def crt(res):
    x, m = 0, 1
    for r, n in res:
        x += m * ((r - x) * pow(m, -1, n) % n); m *= n
    return x % m
a = crt([(2 + 7, 49), (11, 121), (-2 + 19, 361)])
check("V6 toy bases (B,B), B=2*1463^2-1: F_q(a) == 0 exactly for q=1463^2 (definition-level engine)", model.F_q(q, a, Bb, Bb) == 0)
check("V6 the same a without the 19-factor is NOT a zero", model.F_q(49 * 121, a % (49 * 121), Bb, Bb) > 0)
for c in acp.CLASSES:
    r = acp.coverage(c, [(7, 2), (11, 0), (19, -2 % 19)], Bb, Bb)
    assert r["uncovered"] == 0
    r2 = acp.coverage(c, [(7, 2), (11, 0)], Bb, Bb)
    assert (r2["uncovered"] == 0) == (c != (1, 1))
check("V6b ACP decision procedure reports the same covering (all 4 classes) and the same non-covering", True)

# ---------------------------------------------------------------- V7 coverage() vs naive enumeration
rng = random.Random(1)
for trial in range(40):
    ps = rng.sample([7, 11, 19, 23, 31, 43], rng.randint(1, 4))
    tg = [(pp, rng.randrange(pp)) for pp in ps]
    c = rng.choice(acp.CLASSES)
    r = acp.coverage(c, tg)
    N1, N2 = r["N1"], r["N2"]
    unc = sum(1 for i in range(N1) for j in range(N2)
              if all((pow(3, c[0] + 2 * i, pp) + pow(5, c[1] + 2 * j, pp)) % pp != z for pp, z in tg))
    assert unc == r["uncovered"], (tg, c)
check("V7 coverage() == naive pow() enumeration on 40 random target sets", True)

# ---------------------------------------------------------------- V8 C21 / C22 reproduction from an independent catalogue
cat = json.load(open(__file__.rsplit('/', 2)[0] + "/certs/catalogue_B512.json"))
def smooth19(n):
    return all(l <= 19 for l in prime_factors(n))
rows = []
for r in cat["rows"]:
    p = r["p"]
    if p <= 3 or p % 4 != 3:
        continue
    o3, o5 = order_by_iteration(3, p), order_by_iteration(5, p)
    assert (o3, o5) == (r["ord3"], r["ord5"])
    if smooth19(o3) and smooth19(o5):
        d = acp.PrimeData(p)
        wex = max(acp.weight(d, c) for c in acp.CLASSES)
        rows.append({"p": p, "H": d.H, "Pplus": max(prime_factors(o3 * o5 // gcd(o3, o5))), "wexact": wex})
check("V8 19-smooth, H<512 sub-catalogue has exactly 46 inert primes (as in C21)", len(rows) == 46,
      f"(full H<512 catalogue: {cat['n_inert']} inert primes)")
wx = {r["p"]: r["wexact"] for r in rows}
check("V8 exact weights of 11, 71, 271 equal 3/25, 4/175, 1/81", (wx[11], wx[71], wx[271]) == (F(3, 25), F(4, 175), F(1, 81)))
check("V8 exact weight <= 1/H for all 46 rows", all(r["wexact"] <= F(1, r["H"]) for r in rows))
def budgets(K, core_gain):
    w = {r["p"]: (r["wexact"] if r["p"] in (11, 71, 271) else F(1, r["H"])) for r in rows}
    tau = F(1, 512)
    top = lambda ws, k: sum(sorted(ws + [tau] * k, reverse=True)[:k], F(0))
    out = {("base", 7): w[7] + top([w[r["p"]] for r in rows if r["p"] > 7 and r["Pplus"] <= 7], K)}
    for M in (11, 13, 17, 19):
        core = sum(w[r["p"]] for r in rows if 7 <= r["p"] <= M) - core_gain
        act = [w[r["p"]] for r in rows if r["p"] > M and r["Pplus"] == M]
        ina = [w[r["p"]] for r in rows if r["p"] > M and r["Pplus"] < M]
        for t in range(M, K + 1):
            out[(M, t)] = core + top(act, t) + top(ina, K - t)
    return out
b21 = budgets(21, F(0)); b22 = budgets(22, F(1, 25))
check("V8 C21: 29 budgets, all < 1, worst = 875703733/878169600 at (M,t)=(11,11)",
      len(b21) == 29 and max(b21.values()) == F(875703733, 878169600) and b21[(11, 11)] == max(b21.values()))
check("V8 C22: 33 budgets, all < 1, base = 155932663/190512000, worst = 4238011529/4390848000",
      len(b22) == 33 and b22[("base", 7)] == F(155932663, 190512000) and max(b22.values()) == F(4238011529, 4390848000))
if len(sys.argv) > 1:
    cj = json.load(open(sys.argv[1].rstrip('/') + "/c21_frozen/certificate.json"))
    theirs = {r["p"]: (r["ord3"], r["ord5"]) for r in cj["catalog"]["inert_candidate_rows"]}
    mine = {r["p"] for r in rows}
    check("V8 same 46 primes and orders as the frozen certificate.json", set(theirs) == mine and
          all(theirs[p] == (order_by_iteration(3, p), order_by_iteration(5, p)) for p in mine))
    check("V8 all 29 frozen inequalities reproduced", sorted(F(v["budget"]) for v in cj["inequalities"]) == sorted(b21.values()))

# ---------------------------------------------------------------- V9 one-parameter positive control (Erdos covering)
PP = [3, 7, 5, 17, 13, 241]
b2 = 1 + 3 * 5 * 7 * 13 * 17 * 241
cls = [(0, 2), (0, 3), (1, 4), (3, 8), (7, 12), (23, 24)]
tg = [(pp, (pow(2, r, pp) + 1) % pp) for pp, (r, m) in zip(PP, cls)]
r = acp.coverage((0, 0), tg, 2, b2, require_inert=False, step=1)
check("V9 toy bases (2, b2=1 mod P): Erdos covering {3,5,7,13,17,241} is recognised as a covering", r["uncovered"] == 0, str(r))
r = acp.coverage((0, 0), tg[:-1], 2, b2, require_inert=False, step=1)
check("V9 ... and dropping the prime 241 leaves uncovered classes", r["uncovered"] > 0, str(r))

print(f"\nALL {len(OK)} VALIDATION CHECKS PASSED")
