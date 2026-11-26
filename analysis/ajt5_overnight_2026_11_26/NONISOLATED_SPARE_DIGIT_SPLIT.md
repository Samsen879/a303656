# Spare primary digits preserve terminal splits in some nonisolated repair cones

A spare digit restores the split at \(331\). The original repair sends both probes to shift \(80\bmod331\). Allowing the base‑3 digit at \(11\) to move, then compensating on the base‑5 axis, gives two phases passing the named older rows with shifts \(80\) and \(145\). The same arithmetic gives a genuine sum-of-two-squares witness on the repaired phase for an infinite family of positive targets.

### A criterion for a relay that the terminal reads

Let \(p<q\) be inert primes greater than \(5\). For \(b\in\{3,5\}\), write
\[
h_b=v_p(\operatorname{ord}_q(b)),\qquad
\lambda_b=v_p(b^{p-1}-1).
\]
Number the exponent’s \(p\)-primary digits from zero and hold its other prime-primary coordinates fixed. Suppose one axis \(a\) is ordinary at \(p\), so \(\lambda_a=1\). On the other axis \(b\), put \(j_0=\max(0,h_a+1-\lambda_b)\). **If \(j_0<h_b\) and the required digits are free, every incoming phase has a repair at \(p\) with at least \(p^{h_b-j_0}\) distinct terminal shifts.** In particular, two incoming probes can be repaired to distinct shifts.

If the incoming remainder is a unit at \(p\), vary the digits \(j_0,\dots,h_b-1\) on axis \(b\). Otherwise, use the ordinary axis to match \(n\bmod p^{h_a+1}\). An exponent change starting at digit \(j\) on axis \(b\) changes its power by a multiple of \(p^{j+\lambda_b}\), by LTE. The spare block therefore preserves this match. For each spare choice, use digits at indices \(\ge h_a\) on axis \(a\) to reach exact valuation \(2\lceil(h_a+1)/2\rceil\). The ordinary derivative is a unit at each successive lift. Those final digits are invisible at \(q\), so the base‑\(a\) term there is fixed. The spare block gives distinct base‑\(b\) terms because it lies below \(h_b\).

There is also a fixed-head version. If the first \(k_a,k_b\) digits are locked, set \(m=\max(h_a,k_a)\) and \(j_0=\max(k_b,m+1-\lambda_b)\). The same proof applies if the incoming valuation is even below \(k_a+1\), or the remainder is divisible by \(p^{k_a+1}\). The \(331\) example uses the first \(11\)-digit and thus requires a head that leaves that digit free.

### Consequence for a nonisolated cone

Choose an output-visible relay \(p\) with no output-visible descendants in the older inert order graph. This permits the original source’s cone to read into \(q\), including through \(p\). Apply the criterion at \(p\), then repair its descendants in increasing order. Those repairs preserve the new terminal shifts.

More precisely, let \(C_q(p)\) be the older descendants of \(p\), \(M=p^{h_b-j_0}\), and \(\beta_r\) the probability of an odd valuation below \(\min_{b=3,5}v_r(b^{r-1}-1)\). With the requisite digits free, the first-blocker bound is
\[
\Pr(E_q)\le
\beta_q\min\!\left(1,\frac{M}{M-1}\sum_{r\in C_q(p)}\beta_r\right).
\]
Freeze observations outside the pivot and its descendants, and choose the entering phase without reading the descendant or terminal observations. Each probe has failure probability at most the displayed sum over descendants. First blocking needs at least \(M-1\) failed probes, so Markov gives the factor \(M/(M-1)\). The terminal factor follows after conditioning on the older observations. If all descendants are ordinary, the local no-cover conclusion is deterministic. For \(p\ge q^\gamma\), the predecessor’s subfamily tail also applies with the same constant, since it counts the same paths from \(p\) and \(M/(M-1)\le5/4\). [Pinned cone and tail proof](https://github.com/Samsen879/a303656/blob/2e2c5d54904e266ee271fb9ea237dcd12cc86780/analysis/ajt5_overnight_2026_11_26/ISOLATED_REPAIR_CONE_TAIL.md)

### Arithmetic controls

- **Successful spare at \(331\).** At \(n=2478857844897\), the original root at \((865,3)\) repairs to \((865,1803)\), where the shift has already collapsed to \(80\) and \(67\) needs repair. Instead, change \(c\) to \(1225\) and then \(d\) to \(5763\). The first change preserves the shift modulo \(11^2\). The second restores exact valuation \(2\) at \(11\) while preserving the new shift \(145\bmod331\). The resulting remainder is a unit at \(67\). The replay also constructs positive targets with an actual Gaussian norm at \((1225,5763)\) and exact valuation \(1\) at \(331\) on both old probes.
- **Whole-slice failure at \(683\).** At the ordinary relay \(31\), both axes have terminal depth one and both are ordinary. In the indicated slice the repair equation is \(k=14+20j\bmod31\). Every solution has terminal shift zero. Higher digits can obtain exact valuation \(2\) at \(31\), while the shift at \(683\) stays zero. The \(331\) fixture also supplies a quotient countercontrol. The two base‑3 terms lie in distinct cosets of the order‑\(11\) subgroup, yet the repaired *sums* coincide. Distinct componentwise cosets alone cannot certify a terminal split. [Pinned \(683\) resonance](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_COMPENSATED_DENSITY_BOUND.md)

Both terminals in the replay are ordinary. The conditional theorem applies to a genuine common-Wieferich terminal when its hypotheses hold. I made no unconditional ledger subtraction. The \(9\cdot10^{14}\) cutoff, all three infinite tails, and the **\(0.0000909120846076457\ldots\%\)** asymptotic growing-box exception bound remain as published. The local theorem supplies no finite-height guarantee for an arbitrary \(n\). [Pinned density ledger](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/DISTINCT_FACTORIAL_ALLOWANCE_REPLACEMENT.md)

Standalone Python replay, run successfully. In the true-target check, multiplying `5**45363` by any positive integer gives the same assertions.

```python
from math import isqrt, prod

def order(b, p):
    return next(k for k in range(1, p) if pow(b, k, p) == 1)

def shift(cd, m):
    c, d = cd
    return (pow(3, c, m) + pow(5, d, m)) % m

def rem(n, cd, m):
    return (n - shift(cd, m)) % m

def exact(n, cd, p, k):
    return rem(n, cd, p**(k+1)) in range(p**k, p**(k+1), p**k)

for p in (7, 11, 19, 23, 31, 67, 331, 683):
    assert p % 4 == 3 and all(p % i for i in range(2, isqrt(p)+1))

q, n = 331, 2478857844897
assert [tuple(order(b, p) for b in (3, 5)) for p in (11, 67, q)] == [
    (5, 5), (22, 22), (330, 165)]
assert pow(3, 10, 11**2) == 1 != pow(3, 10, 11**3)
assert pow(5, 10, 11**2) != 1 and pow(5, 66, 67**2) != 1
A, B, C, D, E, F = ((73, 3), (865, 3), (865, 1803), (865, 45363),
                     (1225, 1803), (1225, 5763))
assert [shift(cd, q) for cd in (A, B, C, D, E, F)] == [80, 172, 80, 80, 145, 145]
assert exact(n, B, 11, 1) and exact(n, C, 11, 2) and exact(n, C, 67, 1)
assert exact(n, D, 11, 2) and exact(n, D, 67, 2)
assert rem(n, E, 11**3) == 0 and exact(n, F, 11, 2)
assert all(rem(n, cd, 32) == 1 and all(rem(n, cd, p) for p in (3, 7, 19, 23))
           for cd in (A, B, C, D, E, F))
assert all(rem(n, cd, 67) for cd in (A, F))
assert pow(3, (865-73)*11, q) != 1 and pow(5, (45363-3)*11, q) == 1

shifts = set()
for i in range(11):
    c, d = 865+360*i, 1803
    if rem(n, (c, d), 11**3) == 0:
        d += 3960
    assert exact(n, (c, d), 11, 2)
    shifts.add(shift((c, d), q))
assert len(shifts) == 11

mods = (32, 3, 7, 11**3, 19, 23, 67**3, q**2)
x = 6990984771239277600 + prod(mods)*5**45363
y = 4883932019012997599
N = x*x + y*y + 3**F[0] + 5**F[1]
assert all((N-n) % m == 0 for m in mods[:-1])
assert N % q**2 == 80+q and rem(N, F, q) != 0
assert all(exact(N, cd, q, 1) for cd in (A, D))
assert all(N > 3**c+5**d for c, d in (A, B, C, D, E, F))

r, q, step, n = 31, 683, 3960, 2996020970895
assert all(pow(b, q-1, q**2) != 1 for b in (3, 5) for q in (331, 683))
assert all(pow(b, r-1, r**2) != 1 for b in (3, 5))
assert all(pow(b, step, q) != 1 == pow(b, r*step, q) for b in (3, 5))
for j in range(r):
    c = 8+step*j
    hits = [k for k in range(r) if rem(n, (c, 55+step*k), r**2) == 0]
    assert hits == [(14+20*j) % r]
    k = hits[0]
    assert shift((c, 55+step*k), q) == 0
    if rem(n, (c, 55+step*k), r**3) == 0:
        k += r
    assert exact(n, (c, 55+step*k), r, 2)
print("331 spare-digit split, true target, and 683 collapse verified")
```

The criterion uses a true single-primary CRT variation and assumes its relevant digits are free while other fixed coordinates are held unchanged. In the probabilistic projection, choose probes without reading descendant observations. Although their losses can be dependent, summing their individual upper bounds gives the stated Markov estimate. The true Gaussian-norm family is a same-phase construction of positive targets, not a witness at every arbitrarily specified integer.
