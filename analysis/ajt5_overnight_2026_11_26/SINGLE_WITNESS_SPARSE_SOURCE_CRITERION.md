# A sparse source criterion for simultaneous local survival

This is a **conditional** criterion, not verification of the infinite hypothesis. It separates true common Wieferich targets from ordinary auxiliary sources in the [released-primary-block test](SINGLE_WITNESS_TEN_TARGET_AVOIDANCE.md).

A simple refinement of the block test is to promote an ordinary inert source prime \(p\) to a unit-residual target only if the retained targets read at least one of its primary digits on **every** ordinary axis. Otherwise leave a wholly unread ordinary axis available for higher lifting at \(p\). For a fixed block, choose which \(p\)'s to promote in descending order, because each newly promoted test involves primary variables at *smaller* order primes. First satisfy the unaffected lower conditions, then pick a block point avoiding the marked targets, then repair unmarked ordinary rows in the block in ascending order. An unread ordinary axis can reach exact valuation two if needed without modifying a target. Its own digit is invisible to every smaller prime regardless of axis. Outside the block, the same order-of-repair rule applies. Promoting all inert sources read by a higher test is always a conservative alternative.

## Separate numerical weights

Write \(u_p=\operatorname{ord}_p(9),\ v_p=\operatorname{ord}_p(25),\ D(p)=\max(u_p,v_p)\) for inert \(p>3\). Let \(R(p)\) be the largest prime dividing \(\operatorname{lcm}(u_p,v_p)\), and \(e_r(p)=\max(v_r(u_p),v_r(v_p))\). Take \(\mathcal W\) to be the common Wieferich inert primes, and \(E\) a set of primes containing all \(R(t)>7\) for \(t\in\mathcal W\) and closed under moving from an ordinary inert \(s\in E\) to \(R(s)>7\). At a source layer \(r>7\), descending one digit charges the weights \(r^{-e_r(p)}\) for true targets of source \(r\), and the same weights for ordinary auxiliary targets in \(E\) of source \(r\), each source counted once. Resolving a promoted ordinary \(r\) creates a smaller source; if \(r\) itself is common Wieferich it was already counted as a true target. The same accounting applies with a finite initial set of common primes and its finite recursive closure.

A sufficient condition that no finite head obstructs is
\[
 \sum_{t\in\mathcal W:R(t)=r}r^{-e_r(t)}
 +\sum_{s\in E,\ s\ {\rm ordinary\ inert}:\ R(s)=r}r^{-e_r(s)}<1
 \quad\text{for every }r>7,
\]
together with
\[
 \sum_{t\in\mathcal W:R(t)\le7}\frac1{D(t)}
 +\sum_{s\in E,\ s\ {\rm ordinary\ inert}:\ R(s)\le7}\frac1{D(s)}<\frac23 .
\]
Indeed this lets the finite descending construction pass on each layer and reserves \(1/3\) for a possible unit test at 7 in the bottom block. Parities first handle 2 and a unit at 3; 5 is split. Each finite prefix therefore has a survivor. Conversely if a finite head first blocks, its own finite closure necessarily fails at least one of these **sufficient** budgets. Failure of a budget is not itself a blocker. The infinite sufficient criterion, if verified, would give density one by the [actual miss density theorem](EXACT_DENSITY_ALL_EXPONENTS.md).

For a true target with fixed exact odd orders \(u,v\), its square divides \(G_{u,v}=\gcd(9^u-1,25^v-1)\), by lifting from \(2u,2v\) to \(p-1\) with \(p\)-unit multipliers. Thus the number of possible true targets with these orders is at most the largest \(k\) with \((2\operatorname{lcm}(u,v)+1)^{2k}\le G_{u,v}\), even without factoring \(G_{u,v}\). This does not apply to ordinary auxiliary sources. The current estimate does not control the infinite sums.

In the replay at the same integer, the ordinary auxiliary 31 contributes only its first power to the relevant gcd but still needs its norm condition enforced. Then 7 can be repaired along its unread axis without changing either root target or the complete checked deep value at 31.

~~~python
from math import gcd, isqrt

n = 1721507384409
T, P = (71, 311), (7, 31)
D = (1, 31, 28861)

def order(a, p):
    return next(k for k in range(1, p) if pow(a, k, p) == 1)

def shift(d, m):
    return (3 + pow(5, d, m)) % m

for p in T + P:
    assert p % 4 == 3 and all(p % j for j in range(2, isqrt(p)+1))
    assert any(pow(a, p-1, p*p) != 1 for a in (3, 5))

assert [(order(3,p), order(5,p)) for p in T] == [(35,5), (155,155)]
assert gcd(9**15-1, 25**3-1) == 2**3 * 7 * 31
assert all((n-shift(d,4))%4==1 and (n-shift(d,3))%3 for d in D)
assert all((n-shift(d,p))%p for d in D for p in T)

assert [(n-shift(d,31**3)) % 31**3 for d in D] == [11005,961,961]
assert [(n-shift(d,7**3)) % 7**3 for d in D] == [63,91,49]
assert [shift(D[1],m) for m in T+(31**3,)] == [
       shift(D[2],m) for m in T+(31**3,)]

~~~
