# Uniform overlap bounds for two norm offsets

For a rectangular menu of \(K=L_3L_5\) cells, put \(\ell=\max(L_3,L_5)\). The ordered overlap count, summed over primes \(p\le X\), \(p\equiv1\pmod{12}\), is
\[
\boxed{\quad
\ll \frac{XK^2}{(\log X)^2}
\left(1+\frac{\log\log X}{\ell}\right).
\quad}
\]
This counts pairs of active cells with **distinct numerical offsets** whose remainders are both true two-square norms at \(n=5p+52\). The constant is absolute, and the rectangle may move and grow with \(X\). The bound includes pairs changing both exponent labels. Equal offsets can be deduplicated, since they test the same remainder.

### Exact local overlap

Write \(h=52-3^c-5^d\) and \(k=52-3^{c'}-5^{d'}\). Activity means \(4\max(3^c,5^d)\le n\). Even \(c\) gives a remainder \(3\bmod4\), so retain odd \(c\). For those cells, \(3\) never divides the remainder in this prime family.

For an inert prime \(q\ge7\), take \(p\) uniformly in the \(q\)-adic units. The root for \(5p+h\) is reachable exactly when \(q\nmid h\). Write \(a_q=q/(q^2-1)\), the probability of odd valuation at one reachable root.

| Reachable roots | Unit classes rejected modulo \(q^2\) by valuation exactly one | Probability both valuations are even |
|---|---:|---:|
| Neither | \(0\) | \(1\) |
| One | \(q-1\) | \(1-a_q\) |
| Both, \(s=v_q(h-k)=0\) | \(2(q-1)\) | \(1-2a_q\) |
| Both, \(s=1\) | \(q\) | \(1-a_q-1/(q^2-1)\) |
| Both, \(s\ge2\) | \(q-1\) | \(1-a_q-q^{1-s}/(q^2-1)\) |

For a unit root, the shell of valuation \(j\ge1\) has mass \(q^{-j}\). When the roots agree to depth \(s\ge1\), the valuations can differ only when one equals \(s\) and the other exceeds \(s\). The deeper shells of parity opposite to \(s\) have total mass \(q^{1-s}/(q^2-1)\) on each side. The two odd-valuation events therefore have union mass \(a_q+q^{1-s}/(q^2-1)\). At \(h=k\), the correction is zero. For any **fixed finite panel**, CRT gives the product of the exact local probabilities as a relative prime density. One first fixes a depth cutoff and uses prime distribution in progressions, then lets the cutoff grow. The unresolved root balls have vanishing mass.

### Uniform averaging over actual exponents

For distinct shifts define
\[
E_q=\mathbf1_{q\mid h}+\mathbf1_{q\mid k}
     +\mathbf1_{q\nmid hk,\ q\mid h-k},
\qquad
\mathfrak S(h,k)=\prod_{\substack{q\ge7\\q\equiv3\ (4)}}(1-1/q)^{-E_q}.
\]
The valuation-one column of the table, together with rejecting \(q\mid p\), gives local survival at most \((1-1/q)^{3-E_q}\) for inert \(q\). At split primes use \(1-1/q\). Thus the uniform Selberg argument gives, for each distinct pair,
\[
N_{h,k}(X)\ll \frac{X}{(\log X)^2}\mathfrak S(h,k).
\]
In the previous proof, the rejected density is now at most \(3/q\). The same support \(T=X^{1/20}\), with \(z=T^\eta\) for a sufficiently small absolute \(\eta\), still gives weights bounded by \(d^2\). Counting the rejected classes modulo \([d,e]^2\) still costs at most \(T^{10}=X^{1/2}\) in total. The two inert-prime factors over the generic prime sieve give the power \((\log X)^{-2}\). [Verified uniform single-cell sieve](https://github.com/Samsen879/a303656/commit/2a0ae20ddfcadd833d6a9008b96325995020ad79)

Set \(Y=\log(3X)\). The shifts of retained cells and their differences are \(O(X)\), so the product over \(q>Y\) is bounded. Since \(E_q\le2\), expanding the rest by its largest contributing prime gives
\[
\mathfrak S(h,k)\ll
1+\sum_{\substack{q\le Y,\ q\equiv3\ (4)\\q\mid hk(h-k)}}
\frac{\log(2q)}q.
\]
For each divisibility condition, vary one exponent along the longer side, fixing the other coordinates. Use the cell corresponding to the shift for the one-shift conditions; either cell works for the difference. Each condition \(q\mid h\), \(q\mid k\), or \(q\mid h-k\) then has at most one class modulo \(\operatorname{ord}_q(b)\), where \(b=3\) or \(5\). Its proportion is at most \(1/\operatorname{ord}_q(b)+1/\ell\).

The order contribution is summable. In a dyadic block \([U,2U)\), primes of order at most \(U^{1/3}\) divide \(\prod_{j\le U^{1/3}}(b^j-1)\), so there are \(O(U^{2/3}/\log U)\) of them. The other primes have order greater than \(U^{1/3}\). Together these give \(O(U^{-1/3})\) for the block’s contribution to \(\sum_q\log(2q)/(q\,\operatorname{ord}_q(b))\). The \(1/\ell\) terms contribute \(O(\log Y/\ell)\). This proves the displayed averaged bound.

**The missing lower input** is a uniform first moment for *true* active norms. If \(M(p)\) counts distinct successful non-anchor offsets, the needed estimate is
\[
\sum_{p\le X,\ p\equiv1\ (12)} M(p)\gg \frac{XK}{(\log X)^{3/2}}
\]
for a specified growing ordinary-height rectangle. At \(K\gtrsim\sqrt{\log X}\), this and the upper second moment would give a positive relative proportion with a second witness by Cauchy–Schwarz. If \(K/\sqrt{\log X}\to\infty\) and both sides grow, it would also give a positive proportion with **two non-anchor witnesses differing on both axes**. Indeed, all hits at a prime lacking such a pair lie in one row or one column. Applying the pair bound on those lines makes the same-axis contribution \(O(XK(\ell+\log\log X)/(\log X)^2)\), negligible at that scale. The fixed-panel CRT densities alone supply neither first-moment estimate.

### Exact controls and replay

At \(q=7\), the pair \((1,0),(5,3)\) has collision depth one. Both are true norms at \(p=421\). At \(p=1009\), the same modulo-\(49\) phase passes the \(7\)-test, while \(11\) blocks the first remainder. The depth-two pair \((5,5),(7,1)\) gives an even sharper control. At \(p=3613\) both pass the valuation-one test modulo \(49\), but their exact \(7\)-valuations are \(3,2\). At \(p=4789\), in the same phase modulo \(49\), both valuations are \(2\) and both remainders are true norms.

```python
from fractions import Fraction
from math import isqrt

def F(z):
    c,d = z
    return 3**c + 5**d

def R(p,z):
    c,d = z
    n = 5*p + 52
    assert p % 12 == 1 and all(p % q for q in range(2,isqrt(p)+1))
    assert 4*max(3**c,5**d) <= n
    return n-F(z)

def v7(r):
    assert r
    e = 0
    while r % 7 == 0:
        r //= 7
        e += 1
    return e

a,b,c,d = (1,0),(5,3),(5,5),(7,1)
for (i,j),s,killed,density in [
    ((a,d),0,12,Fraction(17,24)),
    ((a,b),1,7,Fraction(5,6)),
    ((c,d),2,6,Fraction(143,168)),
]:
    assert v7(F(i)-F(j)) == s
    H = [52-F(i),52-F(j)]
    assert sum(m % 7 != 0 and any(v7(5*m+h)==1 for h in H)
               for m in range(1,49)) == killed
    total = Fraction()
    for m in range(1,343):
        if m % 7 == 0:
            continue
        r = [(5*m+h) % 343 for h in H]
        assert r.count(0) <= 1
        if all(x == 0 or v7(x) % 2 == 0 for x in r):
            total += Fraction(1,8) if 0 in r else 1
    assert total/(343-49) == density

assert R(421,a)==28**2+37**2 and R(421,b)==5**2+42**2
assert 421%49==1009%49 and R(1009,a)==11*463
assert R(1009,b)==45**2+52**2
assert 3613%49==4789%49==36
assert R(3613,c)==7**3*43 and R(3613,d)==7**2*325
assert R(4789,c)==98**2+105**2 and R(4789,d)==14**2+147**2
assert [v7(R(4789,z)) for z in (c,d)]==[2,2]
print("all exact controls passed")
```

For the conditional two-axis conclusion, apply Cauchy–Schwarz on primes with no cross-axis pair. Their squared counts comprise the diagonal and same-axis pairs only. The diagonal is \(O(XK/(\log X)^{3/2})\) in the stated growing rectangle by the single-cell bound, and the same-axis contribution is \(o(XK^2/(\log X)^2)\) if both sides grow. If \(K/\sqrt{\log X}\to\infty\), those primes contribute \(o(XK/(\log X)^{3/2})\) to the first moment, leaving the stated positive proportion, conditional on the true-norm lower first moment. This lower input is not proved here.
