# Native 19-square saturation and sharp restricted sphere exponent

This follows [the actual mixed native 133 extension](https://github.com/Samsen879/a303656/commit/cf322a1000d6a9a387531f53ec7a16f1624996dc). The two new full-order inert certificates are exact and were independently recomputed by a separate modular implementation, including primality, both shell quotients, valuations and discovery gcds. The sharp population exponent concerns only the restricted sphere construction with native indices supported on \(\{3,7,17,19\}\), not the full catalogue or A303656.

For sharpness, the \(O_\epsilon(Q^\epsilon)\) upper bound counts every ordered norm orientation via the Eisenstein divisor count (integer \(x^2+3y^2\) representations form a subset). Every one has only \(O(\sqrt Q)\) possible free coordinate values at height \(Q\). The number of earlier height windows is \(O(\log\log X)\), absorbed by an arbitrarily small power of \(X\). At the bottom of the maximum gap, the next window has not begun; combine with the previously proved effective lower bound.

**The native \(19\)-tower stops at \(19\).** The plus shell at \(19^2=361\) has the primitive inert prime \(305879633\) to valuation one. The mixed plus shell at \(7\cdot19^2=2527\) independently has the primitive inert prime \(1283717\) to valuation one. These certificates complete the restricted classification:
\[
\boxed{\ \text{Admissible indices supported on }\{3,7,17,19\}
       =3^k\{1,7,17,19,133,289\},\quad k\ge0.\ }
\]

### Exact pure and mixed certificates

The relevant plus shells are
\[
H_{361}=\frac{5^{361}+3^{361}}{5^{19}+3^{19}},
\qquad
H_{2527}=\frac{(5^{2527}+3^{2527})(5^{19}+3^{19})}
{(5^{361}+3^{361})(5^{133}+3^{133})}.
\]

| Index \(d\) | Inert prime \(p\) | Exact order of \(5/3\bmod p\) | \(H_d\bmod p^2\) |
|---:|---:|---:|---:|
| \(361\) | \(305879633\) | \(722\) | \(43966420p\) |
| \(2527\) | \(1283717\) | \(5054\) | \(974738p\) |

The mixed witness reads the full order \(2\cdot7\cdot19^2\). It is a different obstruction from the pure \(19^2\) failure. Both primes can be recovered by a single exact gcd, \(\gcd(2^{p-1}-1,H_d)=p\), with \(p-1=16\cdot361\cdot52957\) and \(p-1=4\cdot2527\cdot127\), respectively.

```python
from math import gcd, isqrt, prod

def S(d):
    return 5**d + 3**d

rows = [
    (361,305879633,[(2,4),(19,2),(52957,1)],(19,),43966420),
    (2527,1283717,[(2,2),(7,1),(19,2),(127,1)],(7,19),974738),
]
for d,p,fac,qs,c in rows:
    assert p%3 == 2 and prod(q**e for q,e in fac) == p-1
    assert all(all(q%i for i in range(2,isqrt(q)+1)) for q,e in fac)
    assert pow(3,p-1,p) == 1
    assert all(gcd(pow(3,(p-1)//q,p)-1,p) == 1 for q,e in fac)
    z = 5*pow(3,-1,p)%p
    assert pow(z,d,p) == p-1
    assert all(pow(z,2*d//q,p) != 1 for q in qs)
    H = S(d)//S(19) if d==361 else S(d)*S(19)//(S(361)*S(133))
    assert H%(p*p) == c*p
    assert gcd(pow(2,p-1,H)-1,H) == p
```

These obstructions persist under arbitrary further native multipliers. If an inert prime \(p\) has odd initial valuation at its exact squared-ratio order \(D\mid r\), admissibility of \(r\) would force \(p\mid r\) by LTE. Then \(\Phi_{Dp}(25,9)\) contains \(p\) once as its sole possible nonprimitive prime. This shell is odd and \(1\bmod3\), so it contains another inert prime of odd valuation, now of exact order \(Dp\). That prime is larger and would also have to divide \(r\). Iteration contradicts finiteness. Within the restricted support, the witnesses already lie outside the support, so LTE alone excludes every multiple of the indicated indices.

Combining the new \(19^2\) cap with the existing obstructions at \(49,119,323,4913\) leaves exactly the six positive rays above. The matched positive controls \(19\) and \(133\) retain both signed norms.

### Consequence for restricted height

The restricted catalogue’s largest phase ratio is exactly \(399/289\). It recurs from \(r=289\cdot3^k\) to \(r=399\cdot3^k\). The effective sphere lower bound therefore retains the uniform exponent \(289/798\).

This exponent is also sharp for the restricted sphere construction, even allowing every norm orientation. At a height \(Q=5^{2r}\), the number of orientations representing \(4(Q-Z)\) is \(O_\epsilon(Q^\epsilon)\) by the divisor bound in the Eisenstein ring. Each orientation contributes \(O(\sqrt Q)\) values of the free squared coordinate. At \(X_k=5^{798\cdot3^k}-1\), the next ray has yet to enter, so the total through the preceding height is \(O_\epsilon(X_k^{289/798+\epsilon})\). Together with the lower bound, this gives the exact lower population exponent \(289/798\) in both odd classes for this restricted construction.

