# Chebotarev realizes anchored digit tilings at every odd prime and depth

**Yes, unconditionally.** For every odd primary prime \(\ell\) and every digit depth \(k\ge2\), there are \(\ell\) actual inert primes and one integer target that tile an anchored \(\ell\times\ell\) digit square with exact valuation-one lines. At the same target, the zero lower anchor leaves \(\ell^2-\ell\) cells. The construction uses Chebotarev to prescribe the order ratios and CRT to set the valuations.

### Prescribing the order ratios

Put \(m=\ell^k\) and \(\kappa_j=1+\ell^{k-1}j\) for \(0\le j<\ell\). For each \(j\) we need a prime \(p_j\) with
\[
p_j\equiv7\pmod{12},\qquad p_j\equiv1+m\pmod{\ell m},
\qquad
5^{(p_j-1)/m}=\bigl(3^{(p_j-1)/m}\bigr)^{\kappa_j}\pmod{p_j},
\]
where \(3^{(p_j-1)/m}\) has exact order \(m\).

Take \(F=\mathbb Q(\zeta_{\operatorname{lcm}(12,\ell m)})\) and \(K=F(3^{1/m},5^{1/m})\). The Kummer group over \(F\) is \((\mathbb Z/m)^2\). Indeed, a proper subgroup of the two radical multipliers would have a nonzero annihilating character, giving \(3^{a/m}5^{b/m}\in F\) for some \((a,b)\ne(0,0)\bmod m\). This positive real radical would generate a real Galois subfield of the abelian field \(F\). Its minimal polynomial divides \(X^m-3^a5^b\), which has only one real root, so the radical would have to be rational. Its valuations at \(3,5\) rule that out. This also handles \(\ell=3,5\).

The two prescribed congruences select a cyclotomic automorphism fixing \(\zeta_m\), and they are compatible even at \(\ell=3\). Extend it to \(K\) and use the full Kummer group to set the radical multipliers to \(\zeta_m,\zeta_m^{\kappa_j}\). Chebotarev supplies infinitely many primes in that Frobenius class. The prescribed ratio is invariant under Frobenius conjugacy: since the chosen Frobenius fixes \(\mu_m\), conjugation multiplies both radical exponents by the same unit modulo \(m\). Reducing the radical equations at a prime above \(p_j\) gives the required power relations in \(\mathbb F_{p_j}\). The residue \(7\bmod12\) also gives \(3^{(p_j-1)/2}=-1\bmod p_j\). [Stevenhagen and Lenstra, *Chebotarëv and his density theorem*](https://link.springer.com/article/10.1007/BF03027290)

### One target controls both full cycles

Choose \(D=\operatorname{lcm}_j\bigl(p_j(p_j-1)/m\bigr)\), \(E\equiv0\bmod D,\ E\equiv1\bmod m\), and \(C=mD/2\). In the full chart
\[
c=C+EU,\qquad d=EV,\qquad 0\le U,V<m,
\]
the \(p_j\)-collision at \(n\equiv0\bmod p_j\) is exactly \(U=\kappa_jV\bmod m\). Here \(3^C=-1\bmod p_j\), and the factor \(p_j\) in \(D\) keeps the other primary coordinates fixed through the precision \(p_j^2\).

Each row has exactly \(m\) collision cells. They rule out at most \(m\) choices of \(n\bmod p_j^2\) among the \(p_j\) lifts of zero. Since \(p_j\ge2m+1\), choose a remaining lift. CRT makes these choices at one target, with \(n\equiv1\bmod4\) and \(n\equiv0\bmod3\) so that the \(2,3\) tests pass throughout.

Now take the lower anchor \(U=a+\ell^{k-1}x,\ V=a+\ell^{k-1}y\). The \(j\)-th collision line becomes
\[
x-y\equiv aj\pmod\ell.
\]
If \(\ell\nmid a\), the lines partition the square. If \(\ell\mid a\), they coincide. On the **full** \(m\times m\) chart the same rows block exactly \(m(\ell-1)+m/\ell\) cells: each \(V\) prime to \(\ell\) has \(\ell\) blocked partners, and each other \(V\) has one.

The first-digit result has a different hypothesis. When both orders have \(\ell\)-part exactly \(\ell\) and the first digits are fully free, every nonempty zero-collision line passes through the common phase \(c\equiv d\equiv0\bmod\ell\). The critical \(\ell\)-line tiling therefore cannot occur there.

### Exact replay

At depth two, the ternary control blocks 21 of 81 full-chart cells, and the quinary control blocks 105 of 625. The survivor vectors on the equal lower anchors are \((6,0,0)\) and \((20,0,0,0,0)\).

```python
from itertools import product
from math import isqrt, lcm, prod

def replay(r, P):
    m = r*r
    assert len(set(P)) == r
    assert all(p%12==7 and (p-1)%m==0 and (p-1)%(r*m)!=0
               and all(p%d for d in range(2,isqrt(p)+1)) for p in P)
    D = lcm(*(p*((p-1)//m) for p in P))
    E, C = D*pow(D,-1,m), m*D//2

    def off(p,u,v):
        return (pow(3,C+E*u,p*p)+pow(5,E*v,p*p)) % (p*p)

    mod = [(4,1),(3,0)]
    G = list(product(range(m),repeat=2))
    for j,p in enumerate(P):
        g,h = (pow(b,E,p) for b in (3,5))
        assert pow(3,C,p)==p-1 and pow(g,m,p)==1 and pow(g,r,p)!=1
        assert h == pow(g,1+r*j,p)
        forbidden = {off(p,u,v) for u,v in G if off(p,u,v)%p==0}
        mod.append((p*p,next(i*p for i in range(1,p)
                            if i*p not in forbidden)))
    M = prod(q for q,_ in mod)
    n = sum(a*(M//q)*pow(M//q,-1,q) for q,a in mod)%M

    blocked = set()
    for j,p in enumerate(P):
        for u,v in G:
            z = (n-off(p,u,v))%(p*p)
            assert z and (z%p==0)==((u-(1+r*j)*v)%m==0)
            if z%p==0:
                blocked.add((u,v))
    assert len(blocked)==m*(r-1)+m//r
    counts = [sum((a+r*x,a+r*y) not in blocked
                  for x,y in product(range(r),repeat=2)) for a in range(r)]
    assert counts == [r*r-r]+[0]*(r-1)
    assert n%4==1 and n%3==0 and C%2==1 and E%2==0
    return n, len(blocked), counts

print(replay(3,(883,19,1747)))
print(replay(5,(136651,51151,103651,6151,130651)))
```

The construction chooses the target after the chart. A sufficiently large positive CRT lift makes every displayed exponent active, but gives no ordinary-height bound for a prescribed target. The prime-selection argument controls multiplicative orders, with no claim of common-Wieferich behavior. The tiling blocks anchored phases and leaves other phases available, so it supplies neither a complete finite obstruction nor a two-square conclusion.

Independent BigInt rebuilt both CRT targets and every incidence of both full charts, including 21/81 and 105/625 blocked cells. The existence argument uses order data only and does not assert nonordinary or common-Wieferich primes.
