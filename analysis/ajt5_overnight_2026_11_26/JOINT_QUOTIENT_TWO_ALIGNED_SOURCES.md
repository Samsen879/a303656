# Two aligned sources and a summable short joint-order tail

**Two aligned sources can force a short-order joint quotient even when both single-source quotients have large order.** That gives a summable tail without any independence assumption. In the actual \(7,19\to32913511\) control, the single-source orders are \(4701930\) and \(173229\), but the joint quotient has order \(2190\). A second actual reader passes both alignment tests and retains large order in all three quotients. [Pinned short-quotient result](https://github.com/Samsen879/a303656/blob/5fbace8e9d63b8a2edbd85952500ce03d1841737/analysis/ajt5_overnight_2026_11_26/SHORT_QUOTIENT_ALIGNED_TAIL.md)

### The joint relation and its summable regime

Let \(p,t\) be distinct doubly ordinary homogeneous sources, write \(D=pt\), and let \(\mu_p,\mu_t\) be their actual Fermat-quotient slopes. The two-source relation lattice is
\[
\Lambda=\{(a,b)\in\mathbb Z^2:
a\mu_p+b\equiv0\pmod p,\quad a\mu_t+b\equiv0\pmod t\}.
\]
It has index \(D\). Fix a nonzero vector in this lattice with \(\max(|a|,|b|)\le\lceil\sqrt D\rceil\), using the CRT slope and the same residue-bin argument as for one source. Write \(\gamma=3^a5^b=A/B\) in lowest terms. Its logarithmic height is \(O(\sqrt D)\).

If \(q\) reads and aligns both sources at depth one, \(\gamma\bmod q\) has trivial \(p\)- and \(t\)-primary components. Its order \(e\) divides \(M=|\langle3,5\bmod q\rangle|/D\). If \(\lambda_q=\min_{j=3,5}v_q(j^{q-1}-1)\), then \(q^{\lambda_q}\mid A^e-B^e\). In particular, a genuine common Wieferich reader contributes its square. The local Fermat-quotient equations also hold for this **same** \(\gamma\) at both relays.

For \(\beta>0\) and \(0\le\eta<1/4\), the integers admitting such a zero branch with
\[
q>Z,\qquad e\le \frac{D^\eta\sqrt q}{(\log q)^\beta}
\]
have upper density \(O_{\beta,\eta}((\log Z)^{-2\beta})\). This includes pairs whose two individual quotients lie outside the previous short-order regime.

For fixed \(p,t\), the distinct \(q\in[X,2X)\) with \(e\le E\) contribute at most
\[
\sum_q\lambda_q\log q\le \sum_{j\le E}\log|A^j-B^j|
\ll \sqrt D\,E^2 .
\]
The branch requires \(D^2q\mid n\). Using \(\lfloor N/(D^2q)\rfloor\le N/(D^2q)\), the dyadic density bound is therefore at most a constant times
\[
\frac{1}{(\log X)^{1+2\beta}}\sum_{p<t}(pt)^{-3/2+2\eta}.
\]
The prime-pair sum and the dyadic tail both converge. The proof needs no premise about earlier common Wieferich rows, so it also bounds this part of the first-terminal case.

### What the simultaneous test leaves open

For single-source exponent vectors \(\mathbf v_p,\mathbf v_t\), let \(\Delta\) be their determinant. If \(t\nmid\Delta\), the first quotient has **exact** \(t\)-primary order \(t\). If \(p\nmid\Delta\), the second has exact \(p\)-primary order \(p\). Moreover, for \(\Delta\ne0\), after removing the \(p,t\) parts of the two orders, the lcm of the remaining orders lies between \(M/\gcd(M,|\Delta|)\) and \(M\) in divisibility. The exponent lattice spanned by the two vectors contains \(\Delta\mathbb Z^2\), so their images in the common cyclic complement contain its \(\Delta\)-th powers.

This explains why even determinant one does not give a small-order bound. Both quotients can have large orders supported by the **same** cyclic complement. The new estimate uses cancellation in a particular short joint direction. If that direction also has order \(\asymp q\), the numerator-product estimate still costs \(O_{p,t}(X^2)\) in a dyadic layer. A square at \(q\) contributes only \(2\log q\) to that budget.

For \(7,19\), the three actual quotients are
\[
\alpha_7=3/5,\qquad \alpha_{19}=9/125,\qquad
\gamma=\alpha_7^{19}\alpha_{19}^{-7}=6075.
\]
The controls distinguish the regimes:

| Ordinary reader \(q\) | \(\operatorname{ord}_q\alpha_7\) | \(\operatorname{ord}_q\alpha_{19}\) | \(\operatorname{ord}_q\gamma\) | \(M\) |
|---:|---:|---:|---:|---:|
| 32913511 | 4701930 | 173229 | 2190 | 247470 |
| 9603931 | 457330 | 252735 | 14442 | 72210 |

The first satisfies the joint bound with \(\beta=1/4,\eta=0\), while both individual orders exceed \(\sqrt q\). The second is outside that bound even without the logarithmic factor. Its period has no split prime above \(q^{1/4}\).

### Standard-library replay

The replay verifies both order controls and all 133 repairs at one target for the first reader. Each repair has exact valuations \(2,2,1\) at \(7,19,q\). The same target has the true representation \(n=3+1+u^2+v^2\). The readers are ordinary, so these checks do not supply a genuine common Wieferich terminal.

```python
from math import isqrt, lcm, prod

p,t,D = 7,19,133
def prime(v):
    return v>1 and all(v%d for d in range(2,isqrt(v)+1))
def mu(v):
    a,b = ((pow(z,v-1,v*v)-1)//v for z in (3,5))
    assert a and b
    return a*pow(b,-1,v)%v

assert (mu(p),mu(t))==(1,11)
data = (
    (32913511,(2,3,5,7,19,73,113),(32913510,5485585,4701930,173229,2190)),
    (9603931,(2,3,5,7,19,29,83),(9603930,960393,457330,252735,14442)),
)
for q,F,expected in data:
    assert prime(q) and all(prime(f) for f in F) and prod(F)==q-1
    def order(a):
        e = q-1
        for f in F:
            while e%f==0 and pow(a,e//f,q)==1:
                e //= f
        return e
    bases = (3,5,3*pow(5,-1,q),9*pow(125,-1,q),6075)
    assert tuple(map(order,bases))==expected
    assert all(pow(a,q-1,q*q)!=1 for a in (3,5))
    assert all(pow(a,(q-1)//s,q)!=1 for a in (3,5) for s in (p,t))
    assert ((q-1)//expected[-1])%D==0

q = data[0][0]
H = lcm(6*p*p,18*t*t,q*(q-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
U,V = step(p*p),step(t*t)
u,v = 3772784479960991364283,15121816040215636502328
n = 4+u*u+v*v
for x in range(p):
    for y in range(t):
        c = 3*q*((q-1)//2)+U*x+V*y
        d = U*x+V*(11*y%t)
        def rem(m):
            return (n-pow(3,c,m)-pow(5,d,m))%m
        for a,j in ((p,U),(t,V)):
            if rem(a**3)==0:
                c += a*j
            assert rem(a**3) in range(a*a,a**3,a*a)
        assert rem(q*q)==q and rem(3)==rem(4)==1
```

Increasing \(u\) by a sufficiently large multiple of \(6p^3t^3q^2\) activates the replay while preserving the tests and the true representation. The large joint-order tail for genuinely common Wieferich readers remains open.

For the displayed two-source control choose the short lattice vector \((5,2)\); it satisfies both congruences and the stated height cap. The estimate holds for any choice rule fixed per pair independently of the terminal; this example uses that displayed choice for the pair \(7,19\). A complement of large order is still possible even with determinant one.
