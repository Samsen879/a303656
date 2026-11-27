# Fixed-budget lattice survival independent of large reader periods

**A fixed number of readers gives a survival bound independent of their deepest order.** The bound applies to arbitrary actual higher-reader orders when those readers are required to be units. It reduces global compatibility to a bounded residue test, then gives an explicit exponent-height condition.

### Freeze only the small periods

Work on an affine first-repair lattice with basis \(b_1,b_2\). The native rows already have remainders divisible by \(p^2\), and we seek exact valuation two. Let \(h\) count the native rows and higher unit tests, and put
\[
L=2h^2+h+1.
\]

For a higher row at \(q\), the two terms along a basis direction have the form \(aG^t+bH^t\) modulo \(q\), with \(a,b\ne0\). Use the actual directional period
\[
d=
\begin{cases}
\operatorname{ord}_q(G/H),& n\equiv0\bmod q,\\
\operatorname{lcm}(\operatorname{ord}_q G,\operatorname{ord}_q H),
   & n\not\equiv0\bmod q.
\end{cases}
\]
For a native exact-two test, use period \(p\) in each direction. On the first-repair lattice, the remainder divided by \(p^2\) is a polynomial of degree at most two modulo \(p\), by expansion of the two powers modulo \(p^3\). [Ordinary-primary repair framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Start with \(M_1=M_2=1\). Whenever a row has **both** remaining periods \(d_i/\gcd(d_i,M_i)<L\), with at least one greater than one, replace each \(M_i\) by \(\operatorname{lcm}(M_i,d_i)\). That row becomes constant on each coset of the resulting sublattice. At most \(h\) such steps are needed, so
\[
M_i\le (L-1)^h.
\]
Check the constant rows on the \(M_1M_2\) residue classes. If no class passes, the entire chart is blocked. If one passes, **every \(L\times L\) grid of scaled basis steps in that class contains at least \(L\) survivors**.

The key count is on a line of length \(L\) in a direction with remaining period at least \(L\).

- A zero reading hits at most once, by the ratio character.
- For a nonzero reading, two hits at \(t,t+\delta\) determine \(G^t,H^t\) uniquely if \(G^\delta\ne H^\delta\), by the two linear equations. If the factors agree, the nonzero target forces both factors to be \(1\), impossible for \(0<\delta<L\). Thus no positive difference repeats among the hits, so their number \(s\) satisfies \(\binom{s}{2}\le L-1\), giving \(s\le2h+1\).
- Here the native rows form the full first-repair coset for distinct ordinary primes with both first-power digits free. Every remaining native row has \(p\ge L\). No scale \(M_i\) is divisible by such a \(p\), since all newly absorbed factors are smaller than \(L\). Thus both basis directions retain their full reduction modulo \(p\). The divided remainder is a nonzero polynomial of degree at most two on this grid. For a nonzero target residue, its quadratic coefficient is nonzero in a direction with unit first coordinate. For a zero target residue, the quadratic part vanishes, but the full lattice step \((P,0)\), with \(P\) the squarefree native product, changes the divided remainder by a nonzero residue. Scaling both basis steps by units preserves this nonconstancy. Either way the polynomial deletes at most \(2L\) cells.

Each remaining row deletes at most \(L(2h+1)\) cells. The total is at most \(L(L-1)\).

Writing \(w_i=M_i b_i\), an index box with side lengths at least
\[
L(|w_{1,u}|+|w_{2,u}|),\qquad L(|w_{1,v}|+|w_{2,v}|)
\]
fits such a grid by the centered fundamental parallelogram. This is a sufficient ordinary-height condition after multiplying by the actual exponent strides.

### Actual controls at adjacent targets

Use \(c=99+522u,\ d=522v\) and the \(7,59\) line \(27u+v\equiv380\bmod413\). At one constructed target the quarter-box is \([0,28]\times[0,19]\). It contains one first-level repair point, \((14,2)\), which has exact valuation one at \(43\). At the next target in the **same CRT class**, the box gains column \(29\). The new point \((29,10)\) has exact valuation two at \(7,59\) and passes every other local test through \(1063\).

For the four core rows the directional periods are \(7,59,7,59\) in both basis directions. With \(h=4\), the rule uses \(L=37\) and absorbs only \(7\). The full-prefix controls below additionally check the other primes at the two actual candidates.

```python
from math import isqrt, prod

A,c,P = 522,99,413
def off(m,u,v):
    return (pow(3,c+A*u,m)+pow(5,A*v,m))%m

S = [(14,2),(29,10)]
Q = [p for p in range(7,1064,4) if all(p%d for d in range(2,isqrt(p)+1))]
t = {4:1,3:0,7**3:294,59**3:44633,
     43**2:(off(43**2,*S[0])+43)%43**2,1063:561}
for p in Q:
    if p not in (7,59,43,1063):
        t[p]=next(z for z in range(p) if all(z!=off(p,*s) for s in S))
M=prod(t)
r=sum(z*(M//m)*pow(M//m,-1,m) for m,z in t.items())%M
X=3**(c+A*29)
n0=4*X-1-(4*X-1-r)%M
n1=n0+M
assert 4*max(3**(c+A*28),5**(A*19))<=n0<4*X<=n1
assert n1<4*min(3**(c+A*30),5**(A*20))

for p,q in ((7,43),(59,1063)):
    b=(pow(5,A,p*p)-1)//p%p
    a=(pow(3,A,p*p)-1)//p*pow(3,c,p)%p
    assert pow(3,A,p)==pow(5,A,p)==1 and b and a==27*b%p
    assert n0%p**2==off(p*p,0,380)
    assert all(pow(g,A*p,q)==1 and pow(g,A,q)!=1 for g in (3,5))
    for s in S:
        z=(n0-off(p**3,*s))%p**3
        assert z and z%p**2==0

for U,expected in [(28,S[:1]),(29,S)]:
    assert [(u,v) for u in range(U+1) if (v:=(380-27*u)%P)<=19]==expected
for s in S:
    assert (n0-off(4,*s))%4==1 and (n0-off(3,*s))%3
    assert all((n0-off(p,*s))%p for p in Q if p not in (7,59,43))
assert (n0-off(43**2,*S[0]))%43**2==43
assert (n1-off(43,*S[1]))%43
```

The fixed-budget bound concerns one anchored chart, with height measured in its actual exponent strides. It rules out arbitrarily long truncated failures at fixed budget and fixed lattice shape once a compatible residue exists. The positive control supplies a positive remainder passing the local prefix. Its remaining inert divisors are unchecked.
