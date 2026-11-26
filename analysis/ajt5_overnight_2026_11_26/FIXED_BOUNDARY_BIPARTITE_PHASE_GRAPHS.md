# Fixed height-independent phase boundaries can realize an arbitrary bipartite graph

Let \(G\) be a finite simple bipartite graph with no isolated vertices. There is a finite panel of true inert primes for bases \(3,5\) and fixed boundary strides such that the effective row-coordinate graph of the finite pre-lift tests is exactly \(G\). Each edge is indispensable for describing the **whole set** of passing phase pairs. This is a fixed-boundary result, not a lower bound for finding some solution: setting all the left coordinates nonzero passes. It does not give a bound after the boundary is removed or an unconditional statement about a full prefix.

Assign distinct primes \(\ell_i,r_j\ge7\) to vertices. For each edge, choose a distinct inert prime \(p\) so that \(v_{\ell_i}(p-1)=v_{r_j}(p-1)=1\), all other vertex primes fail to divide \(p-1\), and the mod-\(p\) orders of \(3,5\) include respectively just \(\ell_i\) and just \(r_j\) from the two candidate primes. Also arrange that no row prime divides a different row's \(p-1\). To do this, use cyclotomic congruences for the specified restrictions and \(p\equiv3\bmod4\). In the cyclotomic field \(K\) over this modulus, put \(m=\ell_i r_j\) and adjoin \(3^{1/m},5^{1/m}\). The first polynomial is Eisenstein above \(3\); its field is unramified at \(5\) since its discriminant can involve only primes over \(3m\). Thus the second polynomial is Eisenstein above \(5\). The two cyclic radical actions over \(K\) can be chosen independently, and the prescribed cyclotomic Frobenius fixes \(\zeta_m\). Choose its lift to act on the first radical by a root of order \(\ell_i\), and on the second by one of order \(r_j\). Chebotarev (for example [Theorem 28.9](https://math.mit.edu/classes/18.785/2025/LectureNotes28.pdf#page=6)) realizes the conjugacy class; the orders of the radical multipliers are invariant under conjugacy. Since each specified prime divides \(p-1\) only once, the multiplier detects exactly the corresponding order factors. Impose \(p\not\equiv1\) modulo each previously selected row prime and take \(p\) larger than them, giving the nondivisibility in both directions. These choices never introduce 3 or 5 into the cyclotomic conductor.

Also omit the finitely many primes that can cause distinct sums \(81u+v\), with \(u\in\mu_{\ell_i},v\in\mu_{r_j}\), to coincide after reduction. The sums are distinct in characteristic zero: if both components differ, an equality would force the differences of two distinct roots from the disjoint prime cyclotomic fields to be rational, which is impossible for these orders by their cyclotomic polynomials. If just one component differs the difference is nonzero immediately. Only rational prime divisors of the finitely many nonzero algebraic norms can fail injectivity.

Write \(o_b(p)\) for the original mod-\(p\) order. Use
\[
 B_3=\operatorname{lcm}(2,\{p\},\{o_3(p)/\ell_i\}),\qquad
 B_5=\operatorname{lcm}(18,\{p\},\{o_5(p)/r_j\})
\]
over the rows, and \(c=4+B_3x,d=B_5y\). Each row has the stated two free coordinate primes, while its own row prime is frozen in both strides. Take \(n\equiv82+p\bmod p^2\) at every row. The mod-\(p\) injection implies rejection exactly when \(x=0\bmod\ell_i,y=0\bmod r_j\): at that pair the free periods do not change either power modulo \(p^2\), and the residual has exact valuation one. All nonroot pairs give units. For each edge, putting its two vertices at zero and all other coordinates at one isolates its failure. On the \(k\times k\) grid, removing \(s<k\) vertices leaves the union of full untouched rows and columns in one connected component of size at least \(k^2-s^2\). Hence a separator leaving components of size at most \(2k^2/3\) has at least \(k/\sqrt3\) vertices even though every row has arity two.

A true target can be constructed as \(n=3^{4+B_3}+1+a^2+b^2\). The right side's needed square sum modulo each \(p^2\) is a unit, since \(3^{B_3}\not\equiv1\bmod p\). Finite-field norm surjectivity and lifting a nonzero coordinate provide a solution; CRT combines the local coordinates. Increasing \(a\) in its fixed class makes the finite list of phase representatives strictly active, without treating their passing residuals as globally certified norms.

## Exact four-row control

```python
from math import gcd,isqrt,lcm
rows=[(7,13,281191,7210,20085),(7,17,472907,13909,67558),
      (11,13,146719,418,6669),(11,17,4073983,239646,370362)]
B3=lcm(2,*(p for l,r,p,o,v in rows),*(o//l for l,r,p,o,v in rows))
B5=lcm(18,*(p for l,r,p,o,v in rows),*(v//r for l,r,p,o,v in rows))
def prime(p):
    return p>=2 and all(p%d for d in range(2,isqrt(p)+1))
for l,r,p,o,v in rows:
    assert prime(p) and p%4==3
    assert all((q-1)%p for _,_,q,_,_ in rows if q!=p)
    for b,B,j,e in ((3,B3,o,l),(5,B5,v,r)):
        assert pow(b,j,p)==1 and pow(b,j,p*p)!=1 and j//gcd(j,B)==e
        assert all(pow(b,j//q,p)!=1 for q in range(2,j+1) if j%q==0 and prime(q))
        assert B%p==0 and B%(p*p)!=0
    vals={(pow(3,4+B3*x,p)+pow(5,B5*y,p))%p
          for x in range(l) for y in range(r)}
    assert len(vals)==l*r and (82+p-pow(3,4,p*p)-1)%(p*p)==p
assert sum(all(x%l or y%r for l,r,*_ in rows)
           for x in range(77) for y in range(221))==16524
```

All four rows are ordinary in this concrete example. If their own prime factors are removed from both strides, no other row period or seed introduces them back, so all four pre-lift depths fall to one. Thus this concrete fixed-boundary lower-bound mechanism is lost under unlocked ordinary-row deletion.
