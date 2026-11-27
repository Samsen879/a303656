# A target-independent load test for protected chronological prefixes

A protected closure admits a **target-independent capacity test**. The test can certify families of chronological prefixes without bounding the total number of ordinary rows. At \(431\), it certifies the entire prefix even with 15 rows deliberately protected. The actual chain \(7\to43\to431\) shows why the closure must include transitive ancestors.

### A test using only the protected orders

Fix a chart \(c=c_0+Ax\) on the \(3\)-axis, and fix \(d\). Start the protected set \(S\) with the terminals where a unit is required, the earlier nonordinary rows on this axis, and any inert rows whose first primary digit is unavailable for repair, including every earlier inert prime \(p\mid A\). Close \(S\) downward: if \(t\in S\) and an earlier inert prime \(p>3\) divides \(\operatorname{ord}_t(3)\), include \(p\). Handle \(2,3\) in the initial anchor.

For each \(p\in S\), put
\[
m_p=\frac{\operatorname{ord}_p(3)}
          {\gcd(\operatorname{ord}_p(3),A)}.
\]
Assign each protected row a prime \(\ell(p)\mid m_p\). A sufficient condition is
\[
L_\ell=\sum_{\substack{p\in S\\\ell(p)=\ell}}
\ell^{-v_\ell(m_p)}<1
\qquad\text{for every assigned prime }\ell.
\]

For any target \(n\), the collision \(3^{c_0+Ax}=n-5^d\bmod p\) is empty or one class modulo \(m_p\). Its projection onto the assigned primary coordinate occupies a fraction \(\ell^{-v_\ell(m_p)}\). Each coordinate therefore has a choice avoiding all rows assigned to it, and CRT combines those choices. The protected unit phases have relative mass at least \(\prod_\ell(1-L_\ell)\) before repairs.

Repair the remaining ordinary rows in increasing prime order. At \(p\), varying its own primary coordinate makes any collision have exact valuation two. It preserves the protected rows by closure and all earlier repairs by prime order. Thus **every prefix satisfying the capacity test admits a phase for every target compatible with its initial anchor**, with exact valuations zero or two at the odd inert unit rows. The number of ordinary rows outside \(S\) does not enter the test. New nonordinary rows and their ancestors must fit in the protected capacities. A cofinal family satisfying this condition would exclude every finite local phase obstruction. I have no cofinal-family proof. [Finite-obstruction and ordinary-primary repair framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

### Actual certificate and transitive omission

For \(A=8\) through \(431\), the replay checks all 41 inert unit rows and finds \(11\) as the sole earlier nonordinary row on the \(3\)-axis. It verifies a closed 15-row protected set with loads
\[
(5/9,\ 2/5,\ 3/7,\ 3/11,\ 2/13,\ 1/23,\ 1/43)
\]
at primary primes \(3,5,7,11,13,23,43\), respectively. The ungrouped sum \(\sum_{p\in S}1/m_p=45775901/44549505>1\), so the corresponding single union bound gives no certificate. The initial \(2,3\) tests admit an anchor \(c\bmod8\) and \(d\in\{2,3\}\) for every \(n\), as checked on the 96 relevant residue classes below.

For the omission control, use the narrower chart \(c\equiv0\bmod24,\ d=2\), and impose
\[
n\equiv75\bmod7^3,\qquad
n\equiv1875\bmod43^3,\qquad
n\equiv457\bmod431^2.
\]
The orders of \(3\) modulo \(7,43,431\) are \(6,42,43\). Thus \(431\) reads \(43\), and \(43\) reads \(7\). The terminal has no direct read of \(7\).

- At \(7\), an even valuation requires \(7\mid c\), since the remainder is already divisible by \(7\) and \(\operatorname{ord}_{49}(3)=42\).
- With \(7\mid c\), an even valuation at \(43\) requires \(43\mid c\), by the same argument using \(\operatorname{ord}_{43^2}(3)=42\cdot43\).
- With \(43\mid c\), the terminal cannot be a unit. If its primary digit is frozen by \(c\equiv0\bmod431\), its valuation is exactly one.

Deleting \(7\) from the minimal protected closure leaves projected orders \(5,7,43\) at \(11,43,431\). Those pass the capacity test, and the reduced panel really does admit unit phases. Restoring the omitted row destroys every terminal-unit phase on this chart. All other earlier inert rows can be made units at the same target.

The replay constructs such a target as \(n=34+a^2+b^2\). Thus **the same integer has a genuine quarter-box witness at \(c=d=2\)**, outside the obstructed anchor.

```python
from fractions import Fraction
from math import gcd, isqrt, prod

q = 431
def prime(p):
    return p > 1 and all(p % k for k in range(2, isqrt(p)+1))
P = [p for p in range(7, q+1, 4) if prime(p)]
def order(p):
    return next(k for k in range(1,p) if pow(3,k,p) == 1)
def v(a,p):
    k = 0
    while a % p == 0:
        a //= p
        k += 1
    return k

owner = {7:3,11:5,19:3,23:11,31:5,43:7,47:23,71:7,79:13,
         127:3,131:13,199:11,211:7,331:11,431:43}
O = {p:order(p) for p in owner}
assert len(P) == 41
assert [p for p in P if p<q and pow(3,p-1,p*p)==1] == [11]
assert all(p in owner for p in P if any(o%p==0 for o in O.values()))
m = {p:o//gcd(o,8) for p,o in O.items()}
assert all(m[p]%ell==0 for p,ell in owner.items())
for ell in set(owner.values()):
    assert sum(Fraction(1,ell**v(m[p],ell))
               for p in owner if owner[p]==ell) < 1
assert sum(Fraction(1,o) for o in m.values()) == Fraction(45775901,44549505)

def two(z):
    return z%4==1 or z%8==2 or z%16==4 or z%32==8
assert all(any((n-5**d)%3 and two(n-5**d-3**c)
               for d in (2,3) for c in range(8)) for n in range(96))
for p,o in [(7,6),(43,42),(431,43)]:
    assert O[p]==o and pow(3,o,p*p)!=1

mod = {p:p for p in P} | {2:4,3:3,7:7**3,43:43**3,q:q*q}
target = {p:25 for p in P} | {2:3,3:0,7:75,43:1875,q:457}
def local_coordinates(p, modulus):
    z = target[p]-34
    if p==2:
        return 1,0
    sq = {x*x%p:x for x in range(p)}
    x,y = next((sq[(z-y*y)%p],y) for y in range(p) if (z-y*y)%p in sq)
    if x%p==0:
        x,y = y,x
    h = p
    while h < modulus:
        x += h*((z-x*x-y*y)//h * pow(2*x,-1,p) % p)
        h *= p
    assert (x*x+y*y-z)%modulus==0
    return x,y

M = prod(mod.values())
def crt(values):
    return sum(x*(M//h)*pow(M//h,-1,h)
               for x,h in zip(values,mod.values())) % M
a,b = map(crt,zip(*(local_coordinates(p,h) for p,h in mod.items())))
n = 34+a*a+b*b
assert all((n-target[p])%h==0 for p,h in mod.items())
assert n>=100
print(n,a,b)  # n = a²+b²+3²+5²
```

The family criterion gives local phases without a bound on their least integer exponents. The omission control concerns a prescribed chart with a frozen terminal. The actual terminal \(431\) is ordinary, and the separate square-coordinate construction supplies the height-bounded witness for that particular target.

Independent BigInt verified the closed 15-row assignment and exact union-bound sum, all 96 initial classes, and the 634-bit genuine target constructed with the obstructed frozen anchor. The criterion does not provide any exponent height bound or an infinite sequence of suitable closed prefixes.
