# Adaptive split cofactor and a checked inert budget

An adaptive split divisor can grow without making the second norm automatic. On a cofinal refinement of the actual pinned \(3,5\) phase, **a shared split divisor \(5\cdot281^j\) is available at genuine ordinary targets, yet every split-only shared divisor is \(o(A)\)** along the refinement. At the same powers and with the same divisor, there are also ordinary first-label targets whose second remainder fails an inert valuation test.

### What a checked budget can certify

Fix \(n\) and an actual first representation \(\alpha\) of \(m_0=n-S_0\). If a Gaussian divisor \(\pi\mid\alpha\) has norm \(c\) supported only on split primes and \(c\mid m_2=n-S_2\), set \(Q=m_2/c\). The largest *candidate* \(c\) is the split part of \(\gcd(m_0,4e)\), where \(e=20A+25B\). At each split prime, the required exponent can be allocated between the two Gaussian primes using the exponents available in \(\alpha\). Removing \(c\) preserves every inert valuation. [Prior oriented transfer](https://github.com/Samsen879/a303656/commit/84927fd56df913568289c9c952ee82002c035b19)

A partial factorization can still certify the quotient. Check that every inert prime up to \(Y\) occurs to even depth, strip those powers and the power of \(2\), and call the remainder \(R\). If \(R\equiv1\bmod4\) and \(R\le Y^2\), then \(Q\) is a norm: a failure would require at least two distinct inert primes greater than \(Y\) at odd depth. This is a test on the prescribed target’s quotient.

Ordinary height has a separate check. For a cofactor with normalized coordinates \(x\ge y\ge0\), one quotient representation \(u^2+v^2=Q\), with \(u\ge v\ge0\), gives first coordinate \(xu+yv\). Its square is at least
\[
Q\min\{x^2,(x+y)^2/2\}.
\]
This follows by minimizing \((x+yz)^2/(1+z^2)\) on \(0\le z\le1\). Thus if this lower bound exceeds \(S_3-S_2\) and \(n\le729A+625B\), the formal norm gives an ordinary witness.

### A cofinal size obstruction on the actual progression

The pinned exponent progression admits simultaneous exact depths \(v_{281}(e)=j\) and \(v_q(e)=\ell\), with \(q=126736826507\) Gaussian-inert. The replay verifies the two nonzero lifting slopes. Each lift permits any prescribed exact positive depth, the two digit conditions combine by CRT, and irrational rotation gives cofinally many balanced pairs in each resulting phase.

Every split-only shared divisor \(c\) divides \(e\) and is coprime to \(q\). Consequently, for **every** target with an ordinary second height,
\[
c\le e/q^\ell,\qquad
Q=\frac{n-S_2}{c}>\frac{S_3-S_2}{e}\,q^\ell>11q^\ell .
\]
Taking odd \(\ell\to\infty\) gives the asserted \(o(A)\) bound. Even the maximal adaptive divisor cannot bring the **raw** quotient below a fixed height cutoff. The residual budget above can still apply if additional even powers are verified and removed.

The bound coexists with genuinely growing split cofactors. Use \(\pi=(2+i)(16+5i)^j\), of norm \(c=5\cdot281^j\). Infinitely many \(j\) have normalized angle with \(1/2\le y/x\le4/7\): the angle of \(16+5i\) is irrational modulo a quadrant, since its ideal and its conjugate are distinct primes. On that subsequence the projection bound is at least \(3cQ/4\). Put \(D=e/c\) and \(w=\lfloor\sqrt{A/c}\rfloor\). Choosing \(r\sim1.5w\) and rounding \(u=(D+r^2+1)/r\) to the nearest integer gives \(v=D+r^2+1-ru\), with
\[
u^2+v^2-4D=(u-2r)^2+(v-2)^2.
\]
This supplies two genuine norms at one target near \(986A\)–\(1051A\), where the projection bound puts both heights in the ordinary window. For the negative target on the same powers, choose \(X\sim31w\) divisible by \(q^{(\ell+1)/2}\) and use \(n_-=S_0+cX^2\). Its first norm is ordinary, while \(X^2-4D\) has exact odd \(q\)-depth \(\ell\). The same candidate cofactor cannot transfer. These are constructed controls for the fixed-target criterion.

### Standalone paired replay

This smaller control uses actual even \(3,5\) exponents in the same balanced strip, with \(c=5\cdot701\).

```python
from math import isqrt

a, b = 87582, 59784
A, B = 3**a, 5**b
assert 39*A < 40*B and 125*B < 122*A
S0, S2, S3, U = A+25*B, 81*A+125*B, 729*A+B, 729*A+625*B
e = 20*A+25*B
c = 57**2+16**2
assert c == 5*701 and e%c == 0
assert 4*57**2 >= 3*c and 2*(57+16)**2 >= 3*c
D, w = e//c, isqrt(A//c)

r = 3*w//2
F = D+r*r+1
u = (2*F+r)//(2*r)
v = F-r*u
n = S0+c*(u*u+v*v)

def place(x, y):
    x,y = sorted((abs(x),abs(y)), reverse=True)
    return 57*x+16*y, 16*x-57*y

L,t = place(u,v)
M,T = place(u-2*r,v-2)
assert n-S0 == L*L+t*t and n-S2 == M*M+T*T
assert S3 < min(S0+L*L, S2+M*M) <= n <= U

# Same powers and candidate cofactor, exact inert failure at 3.
assert D%3 == 1
j = 1 if 4*D%9 != 1 else 2
X = 31*w+(j-31*w)%9
n_bad = S0+c*X*X
assert S3 < S0+(57*X)**2 <= n_bad <= U
assert n_bad-S2 == c*(X*X-4*D)
assert (X*X-4*D)%3 == 0 and (X*X-4*D)%9 != 0
```

At a prescribed \(n\), the reusable result is the quotient budget plus the projection inequality. The construction supplies actual examples and the cofinal bound rules out uniform linear-size split cofactors on this refinement. It leaves the norm test for an unrestricted target open.

The following independently selected seed verifies the simultaneous lifting modulo both primes. At a prime `p`, changing `a` by `L*p**(k-1)` changes the next normalized digit by a unit. Multiples of the other prime's required power avoid altering that other condition. To retain the lift on the increasing balanced sequence, take the exponents in the resulting residue classes modulo their respective full periods at both primes, along with the original phase classes. Irrational rotation still gives arbitrarily large balanced pairs in these classes, so (A/c) can be taken large enough for each chosen pair of depths.

```python
# Verify a simultaneous lifting seed in the pinned phase.
from math import isqrt
p1,p2 = 281,126736826507
a,b,L = 2427822995702,64,17743155710840
assert a%10==2 and b%110==64
assert p1%4==1 and p2%4==3
assert all(p%k for p in (p1,p2) for k in range(2,isqrt(p)+1))
for p,slope in [(p1,182),(p2,103266759460)]:
    assert L%p!=0 and pow(3,L,p)==1
    assert (4*pow(3,a,p)+5*pow(5,b,p))%p==0
    assert ((pow(3,L,p*p)-1)//p)%p==slope!=0
```
