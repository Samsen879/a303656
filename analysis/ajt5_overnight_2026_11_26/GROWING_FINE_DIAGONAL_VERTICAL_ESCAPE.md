# Growing quadratic diagonal reads and a full-chart vertical escape

**Chebotarev realizes the growing quadratic reads, but the \(3,7\) native repair does not force their fine diagonal.** On the actual repair chart, a single reader of odd vertical order \(m\) can erase a whole column only if \(m\mid21\), provided the vertical index reaches \(125\). With one order-\(7^d\) reader at each of arbitrarily many depths \(d\ge2\), a vertical budget linear in the reader count preserves every column that passes the fixed \(3571\) test.

## The native restriction

Retain the previous chart
\[
R(u,v)=n-3^{C+Au}-5^{Bv},\qquad
n\equiv82\pmod{243},\qquad
49\mid R(u,v)\ \Longleftrightarrow\ v\equiv1-u\pmod7.
\]
Here \(C\ge5\), \(B\) is even with \(v_3(B)=2\), and the \(7\)-line has a nonzero first lifting coefficient. A native survivor must have \(v\equiv0\bmod3\) and lie on the \(7\)-line. Outside either condition the corresponding valuation is exactly \(3\) or \(1\).

At a fixed \(u\), take the least \(v_0<21\) satisfying both conditions and try \(v=v_0+21i\) for \(0\le i<6\). The exact valuation-four test at \(3\) excludes one \(i\bmod3\), and the exact valuation-two test at \(7\) excludes one \(i\bmod7\). At least three lifts pass both. A reader of odd vertical order \(m\nmid21\) has order \(m/\gcd(m,21)\ge3\) on these lifts. It can collide at most twice in the six trials, leaving a native survivor that is a unit at that reader. This needs only \(v\le125\), and it uses divisibility at the higher row, so any deeper valuation there is immaterial.

The same argument gives the precise tie restriction. The native tests determine \(v\bmod m\) when \(m\mid21\). For every other odd \(m\), the six trials contain native survivors in at least two distinct phases modulo \(m\).

For several higher readers of vertical orders \(7^{d_i}\), \(d_i\ge2\), use \(v\equiv0\bmod9\) on the native line and try \(J\) consecutive lifts spaced by \(63\). At any column where \(3571\) is a unit, the number passing all specified tests is at least
\[
J-\left\lceil J/7\right\rceil-
\sum_i\left\lceil J/7^{d_i-1}\right\rceil .
\]
The first subtraction is the exact native \(7\)-test. Each other subtraction counts one possible collision class on the lift index. With at most one reader per depth, the sum of their reciprocal periods is at most \(1/6\). Taking \(J=2(h+1)\) for \(h\) deeper readers makes the bound positive (use \(\lceil x\rceil\le x+1\) in each subtraction), so \(v\le126(h+1)-1\) suffices.

## Growing quadratic reads with that same native tie

For each \(2\le d\le D_{\max}\), put \(m=7^d\). Choose a distinct inert prime \(q\) with \(v_7(q-1)=d\), \(v_3(q-1)\le2\), and
\[
3^{(q-1)/m}\equiv5^{(q-1)/m}\pmod q
\quad\text{of exact order }m.
\]
Chebotarev gives such primes by prescribing the cyclotomic congruences and choosing both Kummer multipliers to be \(\zeta_m\). The two radical classes are independent over the cyclotomic field. If a positive \(m\)th root of \(3^a5^b\) belongs to that abelian field, the real field it generates is normal over \(\mathbb Q\). The defining odd-power polynomial has only one real root, forcing that root to be rational and \(m\mid a,b\). [Tschebotareff’s original density theorem](https://link.springer.com/article/10.1007/BF01206606) · [Stevenhagen and Lenstra’s exposition](https://websites.math.leidenuniv.nl/algebra/chebotarev.pdf)

Include \(Q=3571\) with order seven. Set
\[
B=\operatorname{lcm}\bigl(18,\{q(q-1)/m_q\}\bigr),\qquad
C=\operatorname{lcm}\bigl(\{q(q-1)\}\bigr),\qquad
A=\lambda B,\quad \lambda\equiv1\bmod7^{D_{\max}},
\]
where both prime sets include \(Q\). Then \(v_3(B)=2\), \(7\nmid B\), and at each reader the two steps coincide in an element \(g\) of order \(m_q\) modulo \(q^2\). Indeed, \(q\mid B\) freezes the lift of the order, and reduction is injective on the subgroup of order dividing \(q-1\). The anchor satisfies \(3^C\equiv1\bmod q^2\).

Use \(n\equiv3\bmod4\), \(n\equiv82\bmod243\), and impose \(R(4,18)\equiv49\bmod343\). This gives the native line \(u+v\equiv1\bmod7\). On the finer diagonal \(u+v\equiv22\bmod7^{D_{\max}}\), the read at a depth-\(d\) prime is \(g^u+g^{22-u}\). Assign it the symmetric pair
\[
u\equiv11\pm7^{d-1}\pmod{7^d}
\]
by setting \(n\) equal to their common offset plus \(q\bmod q^2\). Multiplication by \(g^u\) gives a quadratic with exactly those two roots modulo \(q\), and both have exact valuation one on the diagonal. At \(Q\), use the pair \(0,1\bmod7\).

These deep pairs can all be tested at exact native valuations. Their \(u\)-coordinates are \(4\bmod7\). Choose \(v\equiv0\bmod9\) on the fine diagonal. Its offset agrees with that of \((4,18)\) modulo \(343\). Indeed, relative to that point the two indices change by \(7j,7k\) with \(j+k\equiv0\bmod7\), and both seventh-step multipliers have the same linear coefficient modulo \(343\). Thus the native valuations are \(4,2\). By enlarging \(\lambda\) in its prescribed class, a quarter-height box can include the least representatives of all these pairs and their vertical lifts.

The full chart still has a short survivor. At \(u=2\), the \(Q\)-row is a unit, and the linear vertical bound above avoids every deeper reader. For the same CRT class, let \(n_-\) be the last target below \(4X\), \(X=3^{C+2A}\), and \(n_+\) the next. The target modulus is at most \(4\cdot243\cdot343B^2<X\). Their quarter-height horizontal maxima are \(1\) and \(2\). The former box is fully blocked by the native rows and \(Q\), and the latter has the short survivor once \(\lambda\) supplies the stated vertical budget.

## Exact replay

The order-\(49\) control uses \(q=6763\). At the same wide target, \((4,18)\) and \((18,396)\) hit the fine diagonal at exact valuation one, while \((4,81)\) and \((18,18)\) pass every specified test. At the first activation of column \(2\), the short positive is \((2,27)\).

```python
from math import isqrt, lcm, prod

Q, q = 3571, 6763
C = lcm(Q*(Q-1), q*(q-1))
B = lcm(18, Q*(Q-1)//7, q*(q-1)//49)
A = 4117*B

def S(u,v,m):
    return (pow(3,C+A*u,m) + pow(5,B*v,m)) % m

for p,m in ((Q,7),(q,49)):
    assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
    g = pow(3,A,p*p)
    assert g == pow(5,B,p*p) and pow(3,C,p*p) == 1
    assert pow(g,m,p*p) == 1 != pow(g,m//7,p)
assert pow(5,B,27) == 1 != pow(5,B,81)
assert pow(5,9*B,243) == 1
assert pow(3,A,49) == pow(5,B,49) != 1

eq = [(4,3),(243,82),(343,S(4,18,343)+49),
      (Q*Q,S(0,1,Q*Q)+Q),(q*q,S(4,18,q*q)+q)]
M = prod(m for m,_ in eq)
a = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq) % M

for p,m,t,roots in ((Q,7,1,[0,1]),(q,49,22,[4,18])):
    assert [u for u in range(m) if (a-S(u,(t-u)%m,p))%p == 0] == roots
    assert all((a-S(u,(t-u)%m,p*p))%(p*p) == p for u in roots)

def vals(u,v):
    return tuple(next(k for k in range(6)
                      if (a-S(u,v,p**(k+1)))%p**(k+1))
                 for p in (3,7,Q,q))

assert vals(4,18) == vals(18,396) == (4,2,0,1)
assert vals(2,27) == vals(4,81) == vals(18,18) == (4,2,0,0)
assert 3**(2*4117) > 5**396

for f in (2,18):
    E = C+A*f
    delta = 1+(4*pow(3,E,M)-1-a)%M
    assert 1 <= delta <= M and E > M.bit_length()
    # Exact targets 4*3**E-delta and 4*3**E-delta+M.
    print(f, E, M, delta)
```

For \(f=2\), these are the failed and surviving quarter-height boxes. For \(f=18\), the upper target contains both diagonal failures and both same-column escapes. The positive controls certify local survival. A stronger native mechanism or enough readers to exhaust the remaining vertical lifts would be needed to turn the growing diagonal reads into a full-chart obstruction.
