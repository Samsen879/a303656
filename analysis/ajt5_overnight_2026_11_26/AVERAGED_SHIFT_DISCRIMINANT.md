# A bounded average of the actual shift discriminant factors

In [the deduplicated norm-pair count](DEDUPLICATED_TRUE_NORM_SHIFT_COUNT.md), write \(d\) for the \(K\asymp\log X\) possible common 5 exponents, in one consecutive progression of step 120. For ordered distinct \(d,e\), put \(g=5^e-5^d\) and \(\Delta=h g(g-h)(g+h)\ne0\). For any fixed \(A>0\),
\[
 {\mathbb E}_{d\ne e}\prod_{p\mid\Delta}(1+A/p)\ll_A1.
\]
This replaces the worst-case \((\log\log X)^{O(1)}\) in the summed off-diagonal upper bound by a constant. The distinct-target exponent there stays unchanged because its diagonal truncation still dominates.

Outside the fixed support of \(h\) and the prime 5, the event \(I_p=1_{p\mid\Delta}\) means \(g=0,h,-h\bmod p\). At fixed \(d\) it gives at most three reduced progression-index classes mod \(o_p=\operatorname{ord}_p(5^{120})\); if a required residue is zero or is not a power in that progression there is no class. Thus \({\mathbb E}I_p\ll 1/o_p+1/K\). The exceptional primes \(o_p\le p^{1/4}\) have summable reciprocals: those in \([Y,2Y]\) divide \(\prod_{j\le(2Y)^{1/4}}((5^{120})^j-1)\), whose log is \(O(Y^{1/2})\). There are \(O(Y^{1/2}/\log Y)\) such primes in that dyadic block.

Since \(\log|\Delta|=O(K)\), the factors \(p>K^2\) give \(1+O_A(1/K)\) deterministically. Exceptional primes above a threshold \(P\) contribute a deterministic factor \(1+O_A(P^{-1/2})\) by the reciprocal estimate. For the other primes \(P<p\le K^2\), set \(S=\sum_{p>P}1/(p\log p)\), finite by the elementary prime-count upper bound. Choose \(P\) large enough that \(AS\le1/8\). Apply Jensen to \(\exp(\sum A I_p/p)\) with weights \(1/(S p\log p)\), assigning unused weight to zero in the exponent. After subtracting 1 and using \(e^u-1\le ue^u\), the expected surplus is at most
\[
 O_A\left(\sum_{P<p\le K^2}p^{-1+1/8}
 \left(p^{-1/4}+K^{-1}\right)\right)
 =O_A(P^{-1/8}+K^{-3/4}).
\]
This argument assumes no independence. The fixed factors \(p\le P\) are uniformly bounded at fixed \(P\), and have deterministic upper bound \((\log P)^{O_A(1)}\) as \(P\) varies. It follows both that the full average is bounded and that its truncation at \(P\) has vanishing mean error as first \(K\to\infty\), then \(P\to\infty\). For a fixed larger tuple of distinct common exponents, use the product of all cross-pair differences; a union bound per prime gives the same estimate with constants depending on tuple size.

## Exact arithmetic check

```python
X=2**50000
c=3986
ds=list(range(7250,10731,120))
assert len(ds)==30
assert all(X<=3**(8*k) and 3**(4*k)<=X for k in (c,c+24))
assert all(X<=5**(3*d) and 5**(2*d)<=X for d in ds)
assert 5**(3*(ds[0]-120))<X<5**(2*(ds[-1]+120))
for p,o,want in ((17,2,870),(19,3,470),(97,4,196),(193,8,84),
                 (257,32,4),(1009,21,18)):
    assert next(j for j in range(1,p) if pow(5,120*j,p)==1)==o
    h=(pow(3,c+24,p)-pow(3,c,p))%p
    vs=[pow(5,d,p) for d in ds]
    assert sum(h*(b-a)*((b-a)**2-h*h)%p==0
               for i,a in enumerate(vs) for j,b in enumerate(vs)
               if i!=j)==want
```

Separately, in the elementary fixed-\(d\) fallback, one can replace the power 15 by 7. For \(f=r_2/4\) one has \(f(m)^4\le f^{*8}(m)\) by comparison at every prime power. At split primes the eightfold convolution has coefficient \(\binom{e+15}{15}\ge(e+1)^4\), and the comparisons at inert and ramified primes are immediate. The lattice count gives \(\sum_{m\le Y}f(m)=O(Y)\) and hence \(\sum_{m\le Y}f(m)/m=O(\log Y)\). Summing seven convolution factors harmonically gives \(\sum_{m\le Y}f(m)^4\ll Y(1+\log Y)^7\). The same two Cauchy–Schwarz steps as in the elementary note give \(\gg X/(\log X)^7\) distinct targets per fixed \(d\), still weaker than the separate analytic bound across \(d\).
