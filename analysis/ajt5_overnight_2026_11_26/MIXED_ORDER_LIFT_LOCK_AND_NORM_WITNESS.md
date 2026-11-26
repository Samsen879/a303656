# Mixed-order persistence of a ternary lock and a same-phase norm repair

The pinned four-line lock survives **every higher ternary digit** at the original steps. At the same target, the coarse cell \((x,y)=(0,1)\) has a different escape: free the large reader’s own prime-primary exponent digits, keep the ternary phase and every other reader’s raw powers, and change its unique obstruction from exact valuation \(1\) to exact valuation \(2\). Opening a lower ternary digit has an asymmetric result: the lower \(d\)-digit leaves all 27 cells blocked, while the lower \(c\)-digit gives an escape and necessarily changes a boundary read. [Pinned two-axis certificate](https://github.com/Samsen879/a303656/commit/8baff5d22cbbd9d4317f9f48b45f45ec8e625b72)

### Mixed-order criterion

Write \(R=n-A g^x-B h^y\), where \(A=3^{c_0}\), \(B=5^{d_0}\), \(g=3^S\), and \(h=5^D\). At a zero reader \(q\mid n\), take \(q\nmid 15\ell\) and suppose \(g,h\) have \(\ell\)-power orders modulo \(q^e\). Reduction modulo \(q\) is injective on their subgroup because its kernel is a \(q\)-group. If \(-B/A\bmod q\) belongs to that subgroup, let \(\eta\) be its unique lift there. The collision condition is one primitive linear congruence modulo \(\ell^j\), where \(\ell^j=\max(\operatorname{ord}g,\operatorname{ord}h)>1\). On this congruence,
\[
R\equiv n-W h^y\pmod{q^e},\qquad W=A\eta+B.
\]
Thus the exact odd shells below depth \(e\) are read from \(n-Wh^y\). For example, if \(n\) and \(W\) have unequal valuations, the smaller valuation holds throughout the collision set. If both have valuation \(a<e\), it holds except where \(h^y\equiv(n/q^a)/(W/q^a)\pmod q\). On that exceptional class the whole truncated residue is constant by injectivity.

In a fibre with \(x,y\) fixed modulo \(\ell^k\), all rows of depth \(j\le k\) have constant decisions at the chosen reader precision. A row of depth \(j>k\) either misses the fibre or has collision fraction \(\ell^{k-j}\) when counted through depth \(j\). The exact odd fraction is at most that. At \(j=k+1\) this is ordinary affine-line counting: \(\ell\) lines can cover the plane only if they are disjoint and each rejects everywhere. A pencil of \(\ell+1\) full lines can cover. Mixed depths require counting in the individual fibres.

### What happens at the pinned target

Let \(q=11419697846380955982026777206637491\) and use the steps \(S,D\) reconstructed below.

- **Higher ternary digits.** The two step powers cube to \(1\) modulo every reader square. The four exact valuation-one lines \(y=0,\ y=2+x,\ y=1+2x,\ x=1\) therefore repeat on every higher digit fibre.
- **Lower ternary digits.** With step \(D/3\), the classes \(y\equiv1,2\pmod3\) reject at exact valuation one at \(271,4159\), respectively. The class \(y\equiv0\) returns to the four-line lock. With step \(S/3\), the cell \((c+S/3,D)\) is a unit at all seven readers. At \(5023,q,163\), the new \(c\)-character has order nine and the \(d\)-character has order at most three. The order-nine component breaks their zero collisions. If both lower digits are opened while preserving the old raw sums at \(271\) and \(4159\), the first reader forces \(3\mid y\) and then the second forces \(3\mid x\). This returns to the locked lattice.
- **Same ternary phase, exact repair.** At \((c,D)\), only \(q\) rejects. Choose \(L\) divisible by the prime-to-\(q\) part of \(3S\), by \(q-1\), and by the other reader periods. The replay verifies \(3^L=1+q\gamma\bmod q^2\) with \(\gamma\ne0\bmod q\). In \(c+Lt\), the first \(q\)-digit of \(t\) uniquely makes \(q^2\mid R\). Adding \(qu\) to \(t\) then changes \(R\bmod q^3\) by \(-q^2u\,3^c\gamma\), so one choice makes \(R\equiv q^2\bmod q^3\). A genuine common Wieferich reader with the same valuation-one collision would retain it under both axes’ order-preserving shifts.

The least CRT representative is below the activation height. There are arbitrarily large representatives of the same class where the finite lock is active and the repaired cell is a **true sum of two squares**. To construct one, preserve the target modulo \(24\), the other reader squares, and \(q^3\). At the repaired cell, choose square coordinates locally for its remainder. Use \((q,0)\) modulo \(q^3\). At the other odd moduli the remainder is a unit, so finite-field norm surjectivity and a unit derivative give coordinates. Modulo \(8\) the remainder is \(1\) or \(5\). Combine the two coordinates separately by CRT and increase one by multiples of the CRT modulus. Defining the target as the repaired offset plus those two squares preserves every tested residue and eventually activates every cell of the finite lock. This construction quantifies over chosen representatives of the class.

### Runnable replay

```python
from itertools import product
from math import gcd, isqrt, lcm, prod

a, b, q = 1783, 5023, 11419697846380955982026777206637491
r, s, h, k = 271, 4159, 19, 163
Q, B = (a, b, q), (r, s, h)
panel = Q + B + (k,)
chain = (1838773, 871578403, 1770336106919153, 584210915283320491,
         143715885159696840787, q)
for p in (a, b, *B, k, chain[0]):
    assert all(p % i for i in range(2, isqrt(p) + 1))
for p, j in zip(chain, chain[1:]):
    assert p*p > j and (j-1) % p == 0 and pow(2, j-1, j) == 1
    assert gcd(pow(2, (j-1)//p, j) - 1, j) == 1
assert all(p % 4 == 3 for p in panel)

P = prod(Q + B)
c = 27*lcm(11, 31, 70491962014697259148313439547145)*P
A = 18*P
S, D = 56*k*c, 12*k*A
pairs = [(9, 24), (pow(3, c, h*h), h*h)] + [(p, p*p) for p in Q]
pairs += [(pow(3, c, p*p) + pow(5, A*u, p*p) + p, p*p)
          for u, p in enumerate((r, s), 1)]
pairs += [(pow(3, c+S, k*k) + 1 + k, k*k)]
M = prod(m for _, m in pairs)
n = sum(z*(M//m)*pow(M//m, -1, m) for z, m in pairs) % M

def R(C, E, m):
    return (n - pow(3, C, m) - pow(5, E, m)) % m

def order(g, step, p):
    return next(j for j in (1, 3, 9) if pow(g, step*j, p*p) == 1)

assert [(order(3,S//3,p), order(5,D,p), order(5,D//3,p))
        for p in panel] == [
    (3,3,9), (9,3,9), (9,3,9), (1,1,3), (3,1,3), (1,1,1), (9,1,3)]
assert all(pow(3,3*S,p*p) == pow(5,3*D,p*p) == 1 for p in panel)
for x, y in product(range(3), repeat=2):
    roots = {p for p,j in zip(Q+(k,), (y,y-x-2,y-2*x-1,x-1)) if j%3==0}
    assert roots and {p for p in panel if R(c+S*x,D*y,p)==0} == roots
    assert all(R(c+S*x,D*y,p*p) == p for p in roots)
    for u, p in enumerate((r,s), 1):
        assert R(c+S*x,(D//3)*(3*y+u),p*p) == p
assert all(R(c+S//3,D,p) for p in panel)

T = 3*S
while T % q == 0:
    T //= q
L = lcm(T,32,27,q-1,*(p*(p-1) for p in panel if p != q))
z = pow(3,L,q**3)
assert L%q and z%q == 1 and z%(q*q) != 1
g = pow(3,c,q)*((z-1)//q) % q
assert R(c,D,q*q) == q
t0 = pow(g,-1,q)
v = R(c+L*t0,D,q**3)
assert v%(q*q) == 0
C = c + L*(t0 + q*((v//(q*q)-1)*pow(g,-1,q) % q))
assert R(C,D,q**3) == q*q
assert all(pow(3,C,p*p) == pow(3,c,p*p) and R(C,D,p)
           for p in panel if p != q)
assert R(C,D,4) == 1 and R(C,D,3) == 2
print("ternary lock, lower-axis asymmetry, exact valuation-two repair verified")
# Construct and verify square coordinates for the repaired finite residue.
from math import prod
def sample_pair(m):
    target=R(C,D,m)
    if m==q**3:
        assert target==q*q
        return q,0
    if m in (8,3):
        return next((i,j) for i in range(m) for j in range(m) if (i*i+j*j)%m==target)
    p=isqrt(m)
    assert p*p==m
    sq={j*j%p:j for j in range(p)}
    u,v=next((i,sq[(target-i*i)%p]) for i in range(p) if (target-i*i)%p in sq)
    if u==0: u,v=v,u
    u+=p*((target-u*u-v*v)//p*pow(2*u,-1,p)%p)
    return u,v
ms=[8,3,q**3]+[p*p for p in panel if p!=q]
uv=[sample_pair(m) for m in ms]
def join(rs):
    P=prod(ms)
    return sum(v*(P//m)*pow(P//m,-1,m) for v,m in zip(rs,ms))%P
X,Y=map(join,zip(*uv))
assert all((X*X+Y*Y)%m==R(C,D,m) for m in ms)
print("CRT witness coordinates replayed")

for a0,b0 in product(range(9),repeat=2):
    stays=all(R(c+(S//3)*a0,(D//3)*b0,p*p)==R(c,0,p*p) for p in (r,s))
    assert stays==(a0%3==b0%3==0)

```

The final replay independently builds square coordinates modulo each specified prime power and combines them by CRT. This gives an actual infinite family of positive targets in the residue class, not a claim at the least CRT representative. The two lower-axis replays also verify what happens when both old boundary sums are preserved simultaneously. No full finite-modulus obstruction or density improvement is inferred.
