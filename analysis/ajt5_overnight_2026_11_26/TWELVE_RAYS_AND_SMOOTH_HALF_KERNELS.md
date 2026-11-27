# Twelve interlaced sphere rays and a smooth half-kernel obstruction

**Phase \(178/9\) closes the \(18\)–\(22\) gap**, using the exact seed \((m,e)=(178,50)\). Two further certified phases, \(70/3\) and \(158/3\), reduce the largest consecutive ratio to \(17/15\). The resulting twelve rays give, in each odd class modulo \(4\),
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{15/34}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}},
\qquad \lambda=1,3,
\]
effectively for sufficiently large \(X\). Here \(A_\lambda\) counts distinct generated targets. With \(178/9\) alone, the exponent is \(11/26\).

The structural result is an unconditional restriction on **how smooth the varying squarefree kernels can be**. It uses the actual orders of \(5,3,-3\) at every binary depth.

### A restriction on smooth half-kernels

Write \(H_\pm=(5^u\pm3^v)/2\) with \(u,v\) odd and \(5^u>3^v\). For an admissible seed, both halves are Eisenstein norms, since they are coprime and \(5^{2u}-3^{2v}=4H_-H_+\). Their squarefree kernels contain only primes \(p\equiv1\bmod3\). Among such primes, the exact condition for divisibility by *some* odd-exponent half is
\[
\begin{array}{ll}
H_-:&\operatorname{ord}_p(5)_2=\operatorname{ord}_p(3)_2,\\
H_+:&\operatorname{ord}_p(5)_2=\operatorname{ord}_p(-3)_2 ,
\end{array}
\]
where the subscript denotes the \(2\)-part. Necessity follows because odd powers preserve that part. For sufficiency, first kill the odd-order parts by odd exponents, then match the two generators of the same cyclic \(2\)-subgroup. An additional period on \(u\) enforces \(5^u>3^v\).

**For each sign this candidate prime set has density \(5/28\).** At \(v_2(p-1)=1\) the contribution is \(1/8\) for each sign, by the quadratic characters. For \(k=v_2(p-1)\ge2\), take
\[
E_k=\mathbb Q(\zeta_{2^{k+1}},\zeta_3),\qquad
L_k=E_k(5^{1/2^k},3^{1/2^k}).
\]
The two relative degrees are \(2^k\) and \(2^{k-1}\). The first follows by Eisenstein at \(5\). For the second, \(E_k\) contains \(\sqrt3\), the first radical extension is unramified at \(3\), and \(\sqrt3\) still has valuation one at primes over \(3\). Above the base Frobenius specified by \(p\equiv1\bmod3\) and \(v_2(p-1)=k\), the two radical exponents are therefore uniform and independent, one modulo \(2^k\) and one among the even residues. Replacing \(3\) by \(-3\) adds \(2^{k-1}\) to the even residue, preserving its distribution. The fraction with equal \(2\)-parts is
\[
\sum_{j=1}^{k-1}2^{-j-1}2^{-j}+2^{-k}2^{1-k}
=\frac16+\frac{4}{3\cdot4^k}.
\]
The base Frobenius has density \(2^{-k-1}\). Summing yields \(1/8+1/24+1/84=5/28\). The omitted depths \(k\ge K\) lie in \(p\equiv1\bmod 2^K\), whose density tends to zero, so the argument needs Chebotarev only at fixed finite depths. [Chebotarev density theorem, Lagarias–Odlyzko](https://aareyanmanzoor.github.io/assets/articles/lagarias-odlyzko.pdf)

Consequently, for fixed \(c>0\) and either sign, the number of \(u\le U\) admitting a partner with that half’s kernel supported on primes at most \(y=c\log U\log\log U\) is at most
\[
U^{(5\log 2/28)c+o(1)}.
\]
Indeed, there are at most \(2^{(5/28+o(1))y/\log y}\) kernel choices. Each fixed kernel \(C\) gives only \(O(1)\) exponent pairs, uniformly in \(C\). To see this, set \(x=5^{(u-1)/2}\) in \(H_\pm=Cz^2\). The elements \(5x\pm z\sqrt{10C}\) have product \(\mp5\cdot3^v\) and sum \(10x\). Dividing by the sum gives a two-term unit equation over a field of degree at most two, with support above \(2,3,5\). Its normalized product fixes \(3^v/5^u\), hence both exponents. [Evertse–Schlickewei–Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04)

In particular, for \(c<28/(5\log2)\), restricting either base half to such smooth kernels gives only \(o(U)\) heights even after cubing, which adds at most a logarithmic factor. This excludes a growing-kernel family without assuming anything about the supply of unrestricted admissible seeds. The missing step toward bounded spacing is an arithmetic source of admissible pairs at uniformly bounded additive gaps, with \(3^e\le5^{(1-\eta)m}\) for some fixed \(\eta>0\). For finite interlacing, achieving maximum ratio \(1+\delta\) requires at least \(\lceil\log3/\log(1+\delta)\rceil\) phases.

### Spacing and exact controls

The phases are \(18,178/9,22,70/3,26,82/3,30,34,38,42,142/3,158/3,54\), with \(54\) starting the next cycle. The largest gap is \(30\)–\(34\). The fixed-height count applies to the three new rays in both classes, since each has \(e\le m\) and the same cubing, ternary and discriminant conditions. The last completed window ends above \(X^{15/17}\). At \(X=5^{34\cdot3^j}\), the preceding lower power is \(5^{30\cdot3^j}\). Even allowing all norm orientations there gives only \(Q^{1/2+o(1)}\) targets, so \(15/34\) is sharp in the liminf for these rays. [Effective orientation count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The replay checks both growing labels and both odd classes. At the main new height, the signed controls satisfy the signed identities but fail at their specified positive pairs by exact odd valuation at \(11\) or \(59\). It also checks \(7\) as a genuine minus-half kernel prime and \(409\) as a prime passing the quadratic test whose quartic values exclude both halves.

```python
from fractions import Fraction as F

def norm(z):
    a,b = z
    return a*a+3*b*b

def orient(z,c,d):
    a,b = z
    pairs = [(a*c-3*b*j*d, abs(b*c+a*j*d)) for j in (1,-1)]
    return max((t for t in pairs if t[1]%3), key=lambda t:t[1])

rows = [
    (178,50,(864628499047610352872414574679,5165003202750419893724442650860),
            (8758694168436087439775796460666,1163992147515793112014306664024)),
    (70,22,(1162027941367,186978239660),(1203553078268,47086836902)),
    (158,142,(1549433092358916625250394569,1398935692807614571625943724),
             (465336456740622196289819728,1638624230623397052913769278)),
]
for m,e,U,V in rows:
    q,s = 5**(m//2),3**(e//2)
    assert 2*norm(U) == q-s and 2*norm(V) == q+s
    Q,Z = q*q,s*s
    v,w = (4*a for a in orient(U,*V))
    for k,(j,p,h) in enumerate(((25,11,66),(61,59,2419))):
        assert Q == 5**(m*3**k) and Z == 3**(e*3**k) == s*s
        assert norm((v,w)) == 4*(Q-Z) and w > s and w%3
        tests = [(True,w)] + ([(False,s+j)] if m == 178 else [])
        for good,t in tests:
            for lam,x,y in ((1,t-s,t),(3,t+s,t-2*s)):
                r,S = t+s,x*x+y*y
                n = 5*Q+lam*Z-S
                assert Q < n < 5*Q and S > lam*Z
                assert 2*lam*Z-S == r*r-3*t*t
                assert n%24 == (21 if lam == 1 else 3)
                R = n-Q-(4-lam)*Z
                assert R == v*v+r*r if good else R%(p*p) == h
        v,w = orient((v,w),(Q-Z)//2,(Q+Z)//2)
        Q,Z,s = Q**3,Z**3,s**3

assert ((5**89-3**25)//2)%49 == 35
assert [pow(a,102,409) for a in (5,3,-3)] == [1,408,408]
p = [F(18),F(178,9),F(22),F(70,3),F(26),F(82,3),F(30),F(34),
     F(38),F(42),F(142,3),F(158,3),F(54)]
assert max(b/a for a,b in zip(p,p[1:])) == F(17,15)
```

The population bound concerns generated targets, and the failed signed controls concern their prescribed positive pairs.
