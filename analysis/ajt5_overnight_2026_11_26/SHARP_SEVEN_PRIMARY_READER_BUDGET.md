# Sharp reader budget on the actual seven-primary repair chart

## The reader budget gives a sharp exponential bound

For \(h=6k+r\), \(0\le r<6\), put
\[
F(h)=(r+1)7^k-1.
\]
**The \(7^{h/6}\) scale is optimal in the following actual two-base model.** Each higher reader sees a \(7\)-power order on the \(3\)-axis and order dividing \(7\) on the \(5\)-axis. If the periodic chart has a survivor, a quarter-height box with maximum indices \(U\ge 7F(h)+6\) and \(V\ge1238\) contains a survivor. When each reader deletes a single class on the native repair line, the horizontal bound improves to \(U\ge F(h)\). Actual \(3,5\) charts attain that sharper bound for every \(h\ge1\).

### Why arbitrary non-prefix covers cannot do better

Suppose \(h\) forbidden classes, each modulo a positive power of \(7\), leave an integer \(w\) uncovered. An interval of \((r+1)7^k\) consecutive integers meets all six siblings of the path to \(w\) at every depth \(1,\ldots,k\). A forbidden class can meet at most one of these disjoint siblings, since any class containing two also contains \(w\). This charges \(6k\) readers. The interval also has \(r+1\) points in \(w\bmod7^k\), with distinct next digits. Those cost \(r+1\) additional readers. Thus the longest fully deleted interval has length at most \(F(h)\).

Equality is attained by deleting
\[
 u\equiv(a+1)7^{j-1}-1\pmod{7^j}
 \qquad(1\le j\le k,\ 0\le a<6),
\]
and another \(r\) classes of the same form at depth \(k+1\), using \(0\le a<r\). These erase \([0,F(h)-1]\) and leave \(F(h)\).

This also forces shallow orders in extremal covers. For a gap of length exactly \(F(h)\), six readers of **exact** depth \(j\) are necessary for each \(j<k\). When \(r>0\), they are necessary at \(j=k\) as well. Indeed, the sibling charges and the points on the remaining path exhaust the budget. Each of the indicated siblings contains at least two consecutive points in its own progression, so its single assigned reader must have that sibling’s modulus. This conclusion allows arbitrary placements of all the forbidden classes.

### Transfer to the physical repair chart

Write \(c=c_0+Au,\ d=d_0+Bv\), and \(R=n-3^c-5^d\). The native rows are \(7,59\). Assume both strides preserve the base powers modulo each native prime, the anchor collides there, and both first lifting coefficients are units. The simultaneous tests \(p^2\mid R\) then give a line \(v\equiv su+t\pmod{413}\). At fixed \(u\), among the least nonnegative lift \(v_0\) and \(v_0+413,v_0+826\), each native prime spoils at most one choice by lifting its valuation above two. One choice therefore has both valuations exactly two.

For each higher reader \(q\), assume
\[
\operatorname{ord}_q(3^A)=7^{j_q},\qquad
\operatorname{ord}_q(5^B)\mid7 .
\]
The bound applies to unit tests. It also applies to exact odd-valuation deletions whenever the deletion decision is constant on each \((u\bmod 7^{j_q},v\bmod7)\) class. The construction below satisfies that condition through exact valuation one.

Freeze the residue \(u=a\bmod7\) of a surviving phase. The native line now fixes \(v\bmod7\). On \(u=a+7b\), the \(5\)-term is constant and the \(3\)-term is injective modulo \(q\) over its remaining period. Each reader deletes at most one class of \(b\bmod7^{j_q-1}\). A constant reader passes because the chosen phase survives. The gap bound gives \(b\le F(h)\), hence \(u\le7F(h)+6\). The three native lifts preserve \(v\bmod7\), and all are at most \(1238\). If each reader already deletes one class in \(u\) on the whole line, apply the gap bound directly and obtain \(u\le F(h)\).

### Realizing equality with \(3,5\)

Here is an unconditional realization with growing strides. For every prescribed stripe of depth \(j\), let \(m=7^j\). Choose a distinct \(q\equiv11\pmod{12}\), \(q\equiv2\pmod{59}\), \(q\equiv1+m\pmod{7m}\), such that \(g_0=3^{(q-1)/m}\) has order \(m\) and \(5^{(q-1)/m}=g_0^{m/7}\). Chebotarev gives these primes by prescribing the cyclotomic action and the two radical multipliers \(\zeta_m,\zeta_m^{m/7}\). The Kummer classes are independent over the cyclotomic field. If the positive \(m\)th root of \(3^a5^b\) lay in that abelian field, the real field it generates would be normal over \(\mathbb Q\). Its defining odd-power polynomial has only one real root, so the radical would be rational, forcing \(m\mid a,b\). [Stevenhagen and Lenstra, *Chebotarëv and His Density Theorem*](https://websites.math.leidenuniv.nl/algebra/chebotarev.pdf)

Take \(D=\operatorname{lcm}(522,\{q(q-1)/7^{j_q}\})\), \(A=424D,\ B=11D\), and anchors \((99,0)\). Prescribe \(R(F,0)\equiv p^2\bmod p^3\) at \(p=7,59\), where \(F=F(h)\). The native line is \(v\equiv27(F-u)\pmod{413}\), hence \(v\equiv u-F\bmod7\). The coefficient ratio \(27\) can be checked at \(D=522\) and is unchanged by scaling \(D\) by a unit at \(7,59\). At an assigned stripe \(u=b\bmod m\), prescribe \(R(b,(b-F)\bmod7)\equiv q\bmod q^2\). Both step orders are unchanged modulo \(q^2\) because \(q\mid A,B\).

Each chosen prime can be made to have exactly that stripe on the native line. In characteristic zero, for \(g=\zeta_m\), the expression \(3^{99}g^u+(g^{m/7})^{u-F}\) is injective in \(u\bmod m\). For \(j\ge2\), compare in the basis \(1,g,\ldots,g^{m/7-1}\) over \(\mathbb Q(\zeta_7)\). Equality for different exponents would force both exponents to be multiples of \(m/7\), where their seventh-root terms agree and their first terms differ. For \(j=1\) the expression is a nonzero constant times \(g^u\). Excluding prime divisors of the finitely many nonzero difference norms preserves injectivity upon reduction.

Include \(n\equiv9\bmod12\), so the remainders are \(1\bmod4\) and \(2\bmod3\). The common target modulus \(M=12\cdot413^3\prod q^2\) satisfies \(M\le12\cdot413^3D^2< X=3^{99+AF}\). Let \(n_-\) be the last target in this class below \(4X\) and \(n_+=n_-+M\). At \(n_-\), the quarter-height box ends at \(u=F-1\), and every column fails a native or higher reader at exact valuation one. At \(n_+\), \((F,0)\) enters the box, has both native valuations two, and is a unit at every higher reader. The construction uses one actual integer per box and maintains positive remainders throughout. For small \(h\), if desired one can force the lower-bound box also to meet \(V\ge1238\) by replacing the \(3\)-stride with \((424+50\cdot413)D\). This preserves all native first digits up to common scaling and all exact projected order requirements, while \(3^{424+50\cdot413}>5^{11\cdot1239}\) and the target lift then gives the needed vertical size.

### Independent replay

The twelve readers below give maximum quarter-height indices \((47,1262)\) at \(n_-\) and \((48,1262)\) at \(n_+\). Each reader is essential at the **same** failed target \(n_-\). Removing it opens a cell with both native valuations exactly two and all other higher rows units.

```python
from math import isqrt, lcm, prod

groups = ((911,2423,3011,3767,6203,6791),
          (9311,29303,36947,51647,59879,115151))
rows = [(q, 7**(j+1), (i+1)*7**j-1)
        for j,g in enumerate(groups) for i,q in enumerate(g)]
F, P = 48, 413
D = lcm(522, *(q*((q-1)//m) for q,m,b in rows))
A, B = 424*D, 11*D

def S(u,v,m):
    return (pow(3,99+A*u,m) + pow(5,B*v,m)) % m

for p in (7,59):
    x, y = pow(3,A,p*p)-1, pow(5,B,p*p)-1
    assert x and y and x%p == y%p == 0
    assert (pow(3,99,p)*(x//p)-27*(y//p)) % p == 0
for q,m,b in rows:
    assert q%12 == 11 and all(q%d for d in range(2,isqrt(q)+1))
    for base,step,t in ((3,A,m),(5,B,7)):
        assert pow(base,step*t,q*q) == 1
        assert pow(base,step*(t//7),q) != 1
    assert len({S(u,(u-F)%7,q) for u in range(m)}) == m

eqs = [(12,9)] + [(p**3,S(F,0,p**3)+p*p) for p in (7,59)]
eqs += [(q*q,S(b,(b-F)%7,q*q)+q) for q,m,b in rows]
M = prod(m for m,_ in eqs)
a = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eqs) % M
e = 99+A*F
delta = 1 + (4*pow(3,e,M)-1-a) % M
# The exact targets are 4*3**e-delta and 4*3**e-delta+M.
assert 1 <= delta <= M and e > M.bit_length()
assert D >= 202 and 3**(424*F) > 5**(11*1262)
assert 3**(2*424*F+1) < 5**(2*11*1263)

def exact(u,v,p,k):
    return ((a-S(u,v,p**k)) % p**k == 0
            and (a-S(u,v,p**(k+1))) % p**(k+1) != 0)

assert [sum(u%m == b for q,m,b in rows) for u in range(49)] == [1]*48+[0]
for q,m,b in rows:
    v0 = 27*(F-b) % P
    assert any(exact(b,v,q,1) and all(exact(b,v,p,2) for p in (7,59))
               for v in range(v0,v0+3*P,P))
assert all(exact(F,0,p,2) for p in (7,59))
assert all((a-S(F,0,q)) % q for q,m,b in rows)
print((47,1262), (48,1262))
```

The theorem concerns the specified panel and anchored exponent box. The sharp examples let the strides grow, and the upper bound uses a common shallow axis and an existing periodic survivor. Arbitrary two-axis depths and primes outside the panel remain open here. The positive control certifies local survival of a positive remainder. Its full two-square status, and the global conjecture, are unchanged by this result.
