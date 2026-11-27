# A valuation-preserving three-label selector on a constructed ordinary-height family

This follows [the exact-read height obstruction and cofactor gate](https://github.com/Samsen879/a303656/commit/36c1c12a2de81214c292f0626f65a66c03da5137). The construction shows that reselection using valuations alone can work for an infinite growing family and can fail for matching local data. Only the \(5\)-axis grows in this family (\(C=2\)); no arbitrary-target or two-axis coverage is asserted.

The existential construction uses the prime factor of a purposely constructed integer of residue \(3\bmod4\) to mark each losing label. This is not part of the actual selector on the supplied target. The selector only tries three exponents and small cofactors, and never factors a large remainder. Both winning fixtures and both same-read failing controls below were independently recreated.

**A three-exponent menu can turn valuation-preserving reselection into a true witness on a growing family.** For each sufficiently large panel cutoff \(Y\), there are exponentially many distinct inputs \(n\) with \(\log n=\Theta(Y)\) for which the seed passes the entire panel but fails the two-square test. Exactly one of two alternate exponents works, and either alternate can be the winner. The selector takes only \(n,Y\). It uses exact division and integer square roots, with no factorization of the large remainders and no supplied representation.

### Selection rule

Let \(\mathcal P_Y\) contain all primes \(p\le Y\) with \(p\equiv3\bmod4\), and let \(q_1<q_2\) be the first two such primes above \(Y\). Fix \(C=2\) and use
\[
D=\{d_0,d_0+72,d_0+144\},\qquad d_0=2Y+1.
\]
For each \(e\in D\), form \(R_e=n-9-5^e\). Require \(R_e>0\), \(R_e\equiv1\bmod4\), \(v_3(R_e)=2\), and \(v_p(R_e)=0\) at the other panel primes. Accept if integer square roots certify
\[
R_e=9u t^2,\qquad 1\le u<q_1q_2,\qquad u\equiv1\bmod4.
\]
The panel conditions force \(u\) to be coprime to all its primes. If any inert prime occurred to odd exponent in \(u\), the congruence \(u\equiv1\bmod4\) would require at least two distinct such primes, giving \(u\ge q_1q_2\). Thus \(u\) passes the two-square criterion. One can extract coordinates by searching only the small cofactor \(u\) and scaling by \(3t\).

### Why both alternate branches occur

Take \(Y\ge11\) and any \(u<q_1q_2\) that is \(1\bmod4\) and coprime to the panel. To realize either alternate \(d\), put
\[
n=9+5^d+9ut^2,\qquad R_e=9ut^2+\Delta_e,\qquad
\Delta_e=5^d-5^e.
\]
Choose \(t\) odd and a unit at \(3\). All the shifts are divisible by \(27\) and \(32\), so the three remainders have exact valuation two at \(3\) and the same reading mod \(32\). At each other panel prime, choose \(t\ne0\bmod p\) and avoid the roots of the two losing remainder polynomials. There are at most four forbidden nonzero choices and \(p-1\ge6\). The raw reads nevertheless differ between any two labels at every panel prime outside the fixed divisors of \(5^{144}-1\).

To make each losing label genuinely fail, use \(v_7(\Delta_e)=1\) for \(e\ne d\). This follows from \(v_7(5^6-1)=1\) and the gaps \(72,144\). Put \(K=-u\Delta_e\), so \(v_7(K)=1\). There is an elementary way to obtain an omitted inert prime \(q\) where \(K\) is a nonzero square:

- Choose \(x\) odd, divisible by \(7\), and \(1\bmod (|K|/7)\). At each remaining panel prime and any previously used marker prime, avoid the at most two roots of \(x^2-4K\). Primes dividing \(K\), other than \(7\), are already avoided.
- Take \(x>2\sqrt{|K|}\). The integer \((x^2-4K)/7\) is positive and \(3\bmod4\). It has an inert prime divisor \(q\) outside the panel and previous markers. At this prime \(K\equiv(x/2)^2\ne0\bmod q\).

Now \((3ut)^2=K\bmod q\) gives a simple root of \(R_e\bmod q\). Of its \(q\) lifts, exactly one vanishes mod \(q^2\). Choose a different lift to force \(v_q(R_e)=1\). Use distinct marker primes for the two losing labels. CRT combines the marker and panel requirements on \(t\). Taking \(t\ge 5^{\max D}\) makes all three remainders positive. The selector consequently finds the unique winning label, without reading either marker.

For a quantitative growing family, choose \(u\) prime, \(1\bmod4\), in \((2Y,3Y)\). For all sufficiently large \(Y\), such a prime exists and \(q_1<u<q_1q_2\). Thus the squarefree cofactor actually exceeds the single-omitted-prime threshold. The panel prime product is \(\exp(O(Y))\). In the marker construction, \(x\) can be taken within one CRT period above \(2\sqrt{|K|}\), so both successive marker primes and the final modulus for \(t\) are \(\exp(O(Y))\). Taking \(5^{\max D}\) consecutive lifts of one admissible class gives \(\exp(\Omega(Y))\) distinct \(n\) per branch, all with \(\log n=\Theta(Y)\). The prime distribution input here is only the fixed-modulus prime number theorem mod \(4\). [Explicit bounds for primes in arithmetic progressions, v3](https://doi.org/10.1112/S0010437X12000802)

### Exact replay

At \(Y=31\), use \(u=53\) and \(D=(63,135,207)\). The two fixtures have winners \(135\) and \(207\), respectively. On each input the other two remainders pass the whole panel and have certified odd valuations outside it. The replay also makes a matched target with the same reads mod \(32\) and every panel \(p^3\), on which **all three** candidates fail.

```python
from itertools import count
from math import isqrt, prod

def prime(p):
    return p > 1 and all(p % k for k in range(2, isqrt(p) + 1))

def panel(Y):
    return [p for p in range(3, Y + 1, 4) if prime(p)]

def labels(Y):
    return [2*Y + 1 + 72*j for j in range(3)]

def select(n, Y):
    P = panel(Y)
    tail = (p for p in count(Y + 1) if p % 4 == 3 and prime(p))
    bound = next(tail) * next(tail)
    for d in labels(Y):
        R = n - 9 - 5**d
        if R <= 0 or R % 4 != 1 or R % 27 not in (9, 18):
            continue
        if any(R % p == 0 for p in P[1:]):
            continue
        for u in range(1, min(bound, R//9 + 1), 4):
            t = isqrt(R // (9*u))
            if 9*u*t*t == R:
                return d, u, t
    return None

def replay(winner, markers):
    Y, u = 31, 53
    D, P = labels(Y), panel(Y)
    shift = {e: 5**winner - 5**e for e in D}
    residues = {2: 1, 3: 1}
    for p in P[1:]:
        residues[p] = next(t for t in range(1, p)
                           if all((9*u*t*t + a) % p for a in shift.values()))
    for e, q in markers.items():
        assert q > Y and q % 4 == 3 and prime(q)
        r = next(t for t in range(1, q) if (9*u*t*t + shift[e]) % q == 0)
        residues[q*q] = next(r+k*q for k in range(q)
                              if (9*u*(r+k*q)**2 + shift[e]) % (q*q))
    M = prod(residues)
    t = sum(r*(M//m)*pow(M//m, -1, m) for m, r in residues.items()) % M
    B = 5**max(D)
    t = B + (t-B) % M
    n = 9 + 5**winner + 9*u*t*t
    R = {e: n - 9 - 5**e for e in D}
    assert all(r > 0 and r % 4 == 1 and r % 27 in (9, 18) for r in R.values())
    assert all(r % p for p in P[1:] for r in R.values())
    assert len({r % 32 for r in R.values()}) == 1
    assert len({r % 11 for r in R.values()}) == 3
    assert select(n, Y) == (winner, u, t)
    assert R[winner] == (6*t)**2 + (21*t)**2

    step = 32 * prod(p**3 for p in P) * prod(q*q for q in markers.values())
    q = 47
    assert prime(q) and q > Y and q % 4 == 3
    bad = n + step * ((9 + 5**winner + q - n)*pow(step, -1, q*q) % (q*q))
    assert bad > n
    for e, q in {**markers, winner: 47}.items():
        for target in ((bad,) if e == winner else (n, bad)):
            r = target - 9 - 5**e
            assert r > 0 and r % q == 0 and r % (q*q) != 0
    assert select(bad, Y) is None
    print(winner, tuple(R[e] % 11 for e in D), R[winner] % 32, t-B)

replay(135, {63: 67, 207: 43})
replay(207, {63: 43, 135: 67})
```

This gives genuine positive remainders at ordinary exponent height for the constructed inputs. The matched failing targets show exactly what the panel alone cannot guarantee for this menu. Coverage for arbitrary \(n\), or for labels outside the three tested exponents on those failing targets, remains open here.
