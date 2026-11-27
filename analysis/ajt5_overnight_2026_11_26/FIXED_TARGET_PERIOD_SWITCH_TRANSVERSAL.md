# Fixed-target period switching and a height-budgeted transversal

A fixed-target switch clears \(43\) and every other inert prime through \(271\) on the original 910,448-bit target. The switch changes the exponent pair from \((32622,337927)\) to \((32622,336937)\). The starting remainder has \(v_{43}=v_{107}=1\). The new remainder is a unit at both primes and retains the same split divisor \(125\). A second switch on the same target makes \(v_{43}=2\) exactly and leaves every other inert prime through \(271\) a unit. [Pinned baseline](https://github.com/Samsen879/a303656/commit/26541d2489a9a43d174a857b78d70eb446ef0de9)

### A transversal with an explicit height budget

Keep \(n\) fixed. Write \(A=3^a,\ B=5^b\), \(P=A+125B\), \(S_3=729A+B\), and \(U=729A+625B\). Use the prior hypotheses \(2S_3-P<n\le U\), \(v_{43}(n-P)=1\), and unit remainders at \(3,7,11,19,23,31\). Let \(c=5^j\) be the smaller shared split divisor from the baseline, with \(j\) odd and \(c\asymp\sqrt a\). Put
\[
D=4c/5,\qquad H=\operatorname{lcm}(D,6930),\qquad
x=a-H,\qquad y_t=b+3-990-6930t.
\]
For sufficiently large balanced exponents, the labels \(S_t=3^x+5^{y_t}\) with \(0\le t\le m=\lfloor b/27720\rfloor\) are positive, distinct, and retain \(c\). Both exponents differ from those of \(P\).

The first shift by \(990\) moves off the \(43\) root because \(5^{990}\not\equiv1\pmod{43}\). The subsequent stride \(6930\) preserves that unit and all six earlier unit checks. If any other prime \(q\ne5\) divides the remainders at two different indices \(s,t\), then subtraction forces
\[
q\mid 5^{6930|t-s|}-1.
\]
Hence **any prescribed list of at most \(m\) inert primes larger than \(5^{6930m}-1\)** excludes at most \(m\) of the \(m+1\) labels. Some label passes the entire list at the same \(n\), with no independence assumption. For example, this gives \(\Theta(\log n)\) prescribed readers from \(5^{b/4}<q<5^{b/3}\) along the cofinal family. The fixed-modulus prime number theorem supplies more than enough inert primes in that band.

For smaller primes on any fixed row, the exact exclusion is either empty or one class \(t\bmod\operatorname{ord}_q(5^\lambda)\), where \(\lambda\) is the stride. On the replay row with stride \(990\), only eight such classes are active through \(271\). The classes for \(43\) and \(107\) are \(0\bmod7\) and \(0\bmod53\). The index \(t=1\) avoids all eight.

### Switching an active small prime to even depth

There is also a rule that works when the tame phase must stay fixed. Start from a label passing the old panel and use coordinate strides \(h_3=\operatorname{lcm}(D,990)\) and \(h_5=990\). Process additional primes \(q>31\) in **increasing order**, maintaining a multiplier \(T\), initially \(1\), that protects all earlier checks. Set
\[
L=\operatorname{lcm}\bigl(T,\operatorname{ord}_q(3^{h_3}),
                            \operatorname{ord}_q(5^{h_5})\bigr).
\]
If the current remainder is a unit at \(q\), keep the label and set \(T=L\). Otherwise, choose a base \(\beta\in\{3,5\}\) with \(v_q(\beta^{q-1}-1)=1\). Increasing order ensures \(q\nmid h_\beta L\). Thus \(w=\beta^{-h_\beta L}\) has \(v_q(w-1)=1\).

Decreasing its exponent \(E\) by \(h_\beta L t\) changes the remainder \(r\) to \(r-\beta^E(w^t-1)\). Modulo \(q^2\), this is linear in \(t\) and determines a unique \(t_0\bmod q\) making the remainder divisible by \(q^2\). The two choices \(t_0\) and \(t_0+q\) give remainders differing at exact depth two. At least one gives \(v_q=2\). Set \(T=Lq^2\) to preserve that valuation under later changes of either coordinate.

If \(E_{\rm lift}\) is the set of primes actually lifted, the final multiplier satisfies
\[
T\le \operatorname{lcm}_{q\text{ processed}}(q-1)
       \prod_{q\in E_{\rm lift}}q^2.
\]
The drop on each axis is less than \(h_\beta T\). This gives a deterministic room check. For primes through \(Z\), the bound is \(T\le2^{12Z}\), using \(\operatorname{lcm}(1,\ldots,Z)\le2^{4Z}\) from the central binomial coefficient. On the balanced family this fits the exponent room for \(Z=\lfloor(\log_2 b)/30\rfloor\) at sufficiently large height. An active prime at which both bases lack a depth-one lift remains outside this guarantee.

The order matters on the actual fixture. The starting remainder is \(35\bmod431\), and both stride powers have order \(43\) modulo \(431\). Freezing those phases first absorbs the \(43\) digit. Imposing the tame period \(7\) at \(43\) then leaves both powers unchanged modulo \(43^2\), trapping the original \(v_{43}=1\). This is a failure of that order of phase locking.

### Exact replay and scope

The standalone Python below reconstructs the exact prior target, derives the eight forbidden classes, verifies both switches, and checks the 431 control.

| Label exponents | \(v_{43}\) | \(v_{107}\) |
|---|---:|---:|
| \((32622,337927)\) | 1 | 1 |
| \((32622,336937)\) | 0 | 0 |
| \((32622,130027)\) | 2 | 0 |

Both switched labels satisfy the ordinary height inequality \(S+\tfrac45(n-S)>S_3\). If the quotient by \(c\) is a sum of two squares, multiplication by \(5^{(j-1)/2}(2+i)\) in the suitable orientation puts its height key in \((S_3,U]\). The replay establishes finite-panel survival. Each switched remainder is \(1\bmod4\), so any remaining failure of square-sum status requires at least two distinct odd-valuation inert primes above \(271\). Their presence or absence is unresolved.

For the lift budget, at a step that lifts \(q\) the previous drop on each axis is less than \(h_\beta L\), and the new increment is less than \(2qh_\beta L\). The exact choices have \(t+1\le2q\le q^2\), so the cumulative drop is strictly less than \(h_\beta Lq^2\); a no-lift step only enlarges the protecting multiplier. This is a sufficient room check, not an assertion that all primes that can divide a quotient fit into it.

```python
from math import gcd, lcm

a, b = 574422, 392104
A, B = 3**a, 5**b
R, V = 5**(b//4), 5**(b//2-b//4)
panel = (3, 7, 11, 19, 23, 31)
J = 3*7*11*19*23*31

def pair(z, m):
    sq = {i*i % m: i for i in range(m)}
    return next((i, sq[(z-i*i) % m])
                for i in range(m) if (z-i*i) % m in sq)

rows = [(20, 1, 0), (11, 0, 0)]
rows += [(p*p, *pair(d*R*R+p, p*p)) for p, d in [(43, 100), (47, 600)]]
for p in (3, 7, 19, 23, 31):
    z = next(z for z in range(p) if (z-100*R*R) % p and (z-600*R*R) % p)
    rows.append((p, *pair(z, p)))

X = Y = 0
M = 1
for m, u, v in rows:
    inv = pow(M, -1, m)
    X += M*((u-X)*inv % m)
    Y += M*((v-Y)*inv % m)
    M *= m
X = V*(X+M*((917*R//25-X)//M+1))
Y = V*(Y+M*((R//200-Y)//M+1))
S0, S3, U, P = A+25*B, 729*A+B, 729*A+625*B, A+125*B
n = S0+X*X+Y*Y
assert 39*A < 40*B and 125*B < 122*A
assert 2*S3-P < n <= U and S3 < S0+X*X and n % 121 == 36


from math import isqrt

def prime(q):
    return q > 1 and all(q%d for d in range(2,isqrt(q)+1))

def order(a,q):
    x=a%q; j=1
    while x!=1: x=x*a%q; j+=1
    return j

def rem(x,y,q):
    return (n-pow(3,x,q)-pow(5,y,q))%q

P0=[q for q in range(3,272,4) if prime(q)]
x, y, c = 32622, 337927, 125
active={}
for q in P0:
    if q<=31: continue
    ell=order(pow(5,-990,q),q)
    hits=[t for t in range(ell) if rem(x,y-990*t,q)==0]
    assert len(hits)<=1
    if hits: active[q]=(hits[0],ell)
assert len(active)==8 and active[43]==(0,7) and active[107]==(0,53)
assert all(1%ell != v for v,ell in active.values())
assert 0<rem(x,y,43**2) and rem(x,y,43)==0
assert 0<rem(x,y,107**2) and rem(x,y,107)==0
for j in (336937,130027):
    s=3**x+5**j
    assert 0<s<n and (n-s)%c==0 and (n-s)%4==1
    assert 5*s+4*(n-s)>5*S3
assert all(rem(x,336937,q) for q in P0)
assert rem(x,130027,43**2)==0 and rem(x,130027,43**3)!=0
assert all(rem(x,130027,q) for q in P0 if q!=43)
assert rem(x,y,431)==35
h3,h5=lcm(100,990),990
assert order(pow(3,h3,431),431)==order(pow(5,h5,431),431)==43
assert pow(3,7*43*h3,43**2)==pow(5,7*43*h5,43**2)==1
# Stride and shared-factor arithmetic in the general transversal.
assert all(pow(5,6930,q)==1 for q in (3,7,11,19,23,31,43))
assert pow(5,990,43)!=1
assert pow(3,6930,43)==1
print("all 271-panel, two switch, and crossed-order controls passed")
```
