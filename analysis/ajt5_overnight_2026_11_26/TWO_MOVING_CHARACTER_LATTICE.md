# Exact character-lattice elimination for a coupled two-moving reader

**A rank-two character lattice gives an exact test for the coupled orbit.** It reproduces both pinned \(3319\) results and handles the genuinely two-moving, nonaligned \(3011\) graph with a degree-11 first polynomial. Direct CRT substitution on that graph gives degree 247. The replay checks only roots of the gcd and recovers the shared label from one direct character. [Pinned degree-29 certificate](https://github.com/Samsen879/a303656/blob/c4eb6031b2132aa27b395d0351dc0defba5bff4c/analysis/ajt5_overnight_2026_11_26/NONALIGNED_RELAY_POLYNOMIAL_GCD.md)

### Elimination and exact coupling

Write the reader equation as \(AX+BY=N\), with the two phase products \(X,Y\) normalized by their fixed coefficients. For each visible prime-order coordinate \(m_i\), let \((a_i,b_i)\) be its exponents in \(X,Y\). The two direct spare characters use **one** coordinate of order \(h\). Define
\[
\Lambda=\{(s,t)\in\mathbb Z^2:\ sa_i+tb_i=0\pmod {m_i}\ \text{for every }i\}.
\]
The index is \(T=\prod_i m_i\). To see why a basis suffices, let \(L\) be the product of the orders visible in \(X\) and \(M=T/L\). CRT combines the ratios \(b_i/a_i\) on the first set into \(k\bmod L\). The lattice then has basis \((L,0),(-kM,M)\), whose monomial equations are exactly \(X^L=1\) and \((Y/X^k)^M=1\).

Reduce this basis and substitute \(Y=(N-AX)/B\) into its two monomial equations. Clearing negative powers turns a relation \((s,t)\) into a polynomial of degree at most \(\max(|s|,|t|,|s+t|)\). For \(N\ne0\), a nonzero relation gives a nonzero polynomial because \(X\) and \((N-AX)/B\) vanish at distinct points. Gauss reduction guarantees a first relation of degree \(O(\sqrt T)\). The second equation can be reduced by binary powering modulo the first, so the gcd arithmetic stays at the first degree. The short replay below expands the second polynomial, whose degree is at most 59 on these controls.

For each gcd root with \(XY\ne0\), project the term with a moving direct character onto its order-\(h\) component. That component determines \(j\) by a discrete log of order \(h\). Baby-step giant-step costs \(O(\sqrt h)\) per candidate. Reconstruct the relay digits \(f_p(0)w_p^j\) at that **same** label and compare both reader terms. This last check turns the relaxed gcd into an exact orbit test.

| Reader | \(n\bmod r\) | Gcd roots | True hit labels |
|---:|---:|---|---|
| 3319 | 1136 | none | none |
| 3319 | 2609 | \(1381,2422\) | none |
| 3011 | 1050 | none | none |
| 3011 | 823 | \(900\) | \(1\), exact valuation one |

At \(3011\), the direct generators are \(2854,561=2854^2\), both of order seven. The ray is 26, and the order-43 reader exponent ratio is 32. The basis \((8,-11),(-15,-17)\) gives \(X^8=Y^{11}\) and \(X^{15}Y^{17}=1\). The positive control uses \(n=54056085512691\) and preserves the relay phase of the earlier target. [Earlier \(3011\) control](https://github.com/Samsen879/a303656/blob/f0c2bac68b965850151c8a12a314f980930c72e4/analysis/ajt5_overnight_2026_11_26/DOUBLE_RELAY_CANCELLATION_CRITERION.md)

### Runnable replay

```python
from math import isqrt, lcm, prod
from sympy import Poly, symbols

x = symbols("x")

def dlog(g, z, h, r):
    m = isqrt(h-1)+1
    baby = {pow(g,j,r): j for j in range(m)}
    stride = pow(g,-m,r)
    for i in range(m):
        if z in baby and i*m+baby[z] < h:
            return i*m+baby[z]
        z = z*stride % r
    raise ValueError("phase outside its subgroup")

def check(h,r,C,D,relays,E,tests):
    P = [p for p,_,_ in relays]
    T = h*prod(P)
    H = lcm(*(p*p*(p-1) for p in P), r*(r-1))

    def step(m):
        b = H//m
        return b*pow(b,-1,m)

    J = step(h)
    A,B,alpha,beta = pow(3,C,r),pow(5,D,r),pow(3,J,r),pow(5,2*J,r)
    assert (r-1)%T == 0 and beta != 1
    assert pow(beta,h,r) == pow(alpha,h,r) == 1
    (a,b),(c,d) = E
    assert abs(a*d-b*c) == T
    assert all(pow(alpha,a,r)*pow(beta,b,r)%r == 1 for a,b in E)

    data = []
    for p,ray,k in relays:
        U,q = step(p*p),p*p
        assert (pow(3,C,q)+pow(5,D,q))%q == 0
        assert pow(3,J,q) == pow(5,2*J,q)
        assert p*U%(r*(r-1)) == 0
        assert all(U%(v*v*(v-1)) == 0 for v in P if v != p)
        assert pow(3,U,p) == pow(5,U,p) == 1
        a,b = ((pow(base,U,q)-1)//p for base in (3,5))
        g,w = pow(3,U,r),pow(3,-J,p)
        assert a and b and g != 1 and pow(g,p,r) == 1 and k not in (0,1)
        assert pow(5,ray*U,r) == pow(g,k,r)
        assert all((a+k*b)%p == 0 for a,b in E)
        assert w != 1 and pow(w,h,p) == 1
        f0 = pow((a*pow(3,C,p)+ray*b*pow(5,D,p))%p,-1,p)
        data.append((p,ray,U,w,f0))

    proj = T//h*pow(T//h,-1,h)
    for n,roots,expected in tests:
        assert n%r and all(n%(p*p) == p for p in P)
        Y = (n%r-A*x)*pow(B,-1,r)
        def F(a,b):
            return Poly(x**max(a,0)*Y**max(b,0)
                        - x**max(-a,0)*Y**max(-b,0), x, modulus=r)
        f,g = (F(a,b) for a,b in E)
        assert f.gcd(g) == Poly(prod(x-u for u in roots),x,modulus=r)
        hits = []
        for X in roots:
            y = (n-A*X)*pow(B,-1,r)%r
            assert X and y
            gen,z = (alpha,X) if alpha != 1 else (beta,y)
            j = dlog(gen,pow(z,proj,r),h,r)
            c,d = C+J*j,D+2*J*j
            for p,ray,U,w,f0 in data:
                digit = f0*pow(w,j,p)%p
                c,d = c+U*digit,d+ray*U*digit
            if (pow(3,c,r),pow(5,d,r)) != (A*X%r,B*y%r):
                continue
            def rem(m):
                return (n-pow(3,c,m)-pow(5,d,m))%m
            for p,_,U,_,_ in data:
                if rem(p**3) == 0:
                    c += p*U
            assert all(rem(p**3) in range(p*p,p**3,p*p) for p in P)
            assert rem(r*r) == r
            hits.append(j)
        assert hits == expected

check(3,3319,214742619,79168445538,[(7,3,5),(79,71,36)],[(29,-3),(2,57)],
      [(16548479088281,[],[]),(16625594332193,[1381,2422],[])])
check(7,3011,1169141190,2718933,[(43,26,32)],[(8,-11),(-15,-17)],
      [(92767221879,[],[]),(54056085512691,[900],[1])])
print('OK')
```

The two coefficients of each relay repair equation scale together for every label, which proves the digit formula uniformly. The \(pU\) correction gives exact valuation two and is invisible at the other relays and modulo \(r^2\). A common sufficiently large lift by a multiple of \(12hr^2\prod_p p^3\) makes the tested remainders positive. These certificates control the specified finite panels. The method’s cost still depends on the shortest lattice relation and the number of gcd roots.

The lattice claim assumes distinct prime-order coordinates, each visible in at least one of the terms. The relaxed variety is restricted to the algebraic torus; discard a polynomial gcd root if either reader term vanishes after substitution. The finite example confirms both an actual positive hit and several false relaxed or absent hits. This is not a uniform small-degree bound as a function of the number of labels alone or a density claim.
