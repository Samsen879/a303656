# Split-axis panel survival and a matched full-chart CRT cover

This follows [adaptive exact 5-adic peels](https://github.com/Samsen879/a303656/commit/3822ebb51c517146b5aa550d05c142c0f5e07d33). In the first proof, the vertical period-5 choice at 11 is shared with 71 and belongs before the horizontal choice. That order lowers the remaining vertical ceiling budget below one. The result guarantees an actual unit survivor inside the explicit ordinary exponent box for the chosen finite panel, not a norm witness or a universal guarantee over freely chosen primes. Further primes can be added with summably small reciprocal orders; the required interval width then grows to absorb the rounding costs.

In the second proof, one independently assigned omitted inert prime rejects each raw label, which automatically rejects every adaptive sublane within that finite chart, without making any claim about other labels. The 812-bit combined CRT modulus yields at least \(2^{387}\) solutions in that particular 1,200-bit window. Its cost is for that one finite box; it does not give an efficient cover as height grows. Independently replayed all early orders at multiple \(j\), the exact ceiling budgets, the 192,000-bit such panel survivor, and all 32 matched CRT marker valuations.

**A split-axis argument rules out a simultaneous cover by all inert primes through \(137\) and by a leftover \(17\) after peeling, at ordinary exponent height.** A matched 1,200-bit control goes the other way: 32 omitted inert primes cover every label in the selected chart, across all adaptive valuation lanes, while the old panel readings agree with a target that has a certified witness.

### A split-axis bound inside the exponent box

Write one repaired lane as \(c=C+16\cdot5^j i,\ d=D+144k\), with \(j\ge1\) and the quotient’s nonzero residue mod \(5\) fixed. Let \(V=(n-3^c-5^d)/(wA5^j)\) as before. Suppose the actual box contains at least **18 consecutive \(i\)** and **290 consecutive \(k\)**. Then some in-box label has \(V\) coprime to \(17\) and to every inert prime \(7\le p\le137\).

The choice uses three steps.

1. **Choose \(k\bmod5\) at \(11\).** The horizontal period at \(11\) is one, and the vertical period is five. At most one \(k\bmod5\) is forbidden.
2. **Choose \(i\) at \(7,19,31,71\).** The vertical powers at \(7,19,31\) are constant, and the horizontal periods are \(3,9,3\). They exclude at most seven of the nine classes mod \(9\). On a surviving class, 18 consecutive \(i\) give two choices nine apart. At \(71\), the vertical class is already fixed and the horizontal period is seven, so at least one of those two choices survives.
3. **Finish within the chosen vertical class.** Write \(k=k_0+5t\). At each remaining prime \(p\), there is at most one forbidden class of \(t\bmod\operatorname{ord}_p(5^{720})\). If \(A=17\), the extra factor at \(17\) likewise forbids at most one class mod \(17\), since \(5^{144}\equiv103\bmod17^2\). If \(A=1\), the head already gives a unit there.

The remaining moduli, including the extra \(17\), are
\[
11,7,23,29,11,13,41,17,53,7,13,17.
\]
Their reciprocal sum is \(21217326014/24664286647<1\). For every \(K\ge58\), the sum of \(\lceil K/m\rceil\) over this list is less than \(K\). The replay checks \(58\le K<86\), and the reciprocal sum proves the rest. Thus any interval of 58 or more eligible \(t\) contains a survivor. Charging all the original vertical readers together gives a reciprocal sum above one. Fixing the shared phase first is what makes the finite box bound work.

For example, the actual box \([\lceil H/32\rceil,\lfloor H/4\rfloor]\) supplies these widths for \(H\ge192000\) whenever its span is at least \(18\cdot16\cdot5^j\). The same argument allows additional primes if their moduli satisfy the same ceiling budget. This gives panels of arbitrarily large size: choose additional inert primes with \(\operatorname{ord}_p(5^{720})\ge64s^2\) for the \(s\)-th added prime. Bounded orders occur at only finitely many primes, and the added reciprocal cost is at most \(1/32\). The height requirement grows with the number of rows through the ceiling budget.

### Matched full-box failure

The replay constructs a 1,200-bit target in the same head and with the same readings mod \(25\) and all inert \(p^3\) through \(137\) as the earlier base-\(3\) success at \((51,145)\). It assigns a distinct inert prime \(q>137\) to each of the 32 raw chart labels, imposing
\[
n-3^c-5^d\equiv q\pmod{q^2}.
\]
Every label therefore has exact odd valuation at its assigned prime. This rules out a true two-square remainder at every label, regardless of the adaptive peel or base. The combined CRT modulus has 812 bits, so this single residue class supplies at least \(2^{387}\) blocked inputs in the same 1,200-bit window.

```python
from fractions import Fraction
from itertools import count, islice, product
from math import gcd, isqrt, prod

def prime(p):
    return p > 1 and all(p % d for d in range(2,isqrt(p)+1))

def order(a,p):
    z = 1
    for k in range(1,p):
        z = z*a % p
        if z == 1:
            return k
    raise AssertionError

P = [p for p in range(7,138,4) if prime(p)]
early = {7:(3,1), 11:(1,5), 19:(9,1), 31:(3,1), 71:(7,5)}
assert {p:(order(pow(3,80,p),p), order(pow(5,144,p),p))
        for p in early} == early
ms = [order(pow(5,720,p),p) for p in P if p not in early] + [17]
rho = sum(Fraction(1,m) for m in ms)
assert rho == Fraction(21217326014,24664286647)
assert all(sum((k+m-1)//m for m in ms)<k for k in range(58,86))
assert 86*(1-rho)>len(ms) and pow(5,144,289)==103

def clean(n,c,d,ps):
    return all((n-pow(3,c,p)-pow(5,d,p))%p for p in ps)

# Positive control at the guaranteed height, with exact norm coordinates.
H = 192000
lo,hi = H//32,H//4
c,d = lo+(3-lo)%16,lo+(1-lo)%144
t = 3*2**(H//2-5)
t += (85-t)%510
n = 3**c+5**d+85*(t*t+16)
assert n.bit_length()==H and n%8==5 and n%3!=2
assert (7*t-24)**2+(6*t+28)**2 == n-3**c-5**d
C,D = range(c,hi+1,80),range(d,hi+1,144)
assert len(C)>=18 and len(D)//5>=58
d0 = next(y for y in D[:5] if clean(n,c,y,[11]))
c0 = next(x for x in C[:18] if clean(n,x,d0,[7,19,31,71]))
d1 = next(y for y in range(d0,hi+1,720)
          if clean(n,c0,y,P) and (n-pow(3,c0,289)-pow(5,y,289))%289)
R = n-3**c0-5**d1
assert R>0 and R%85==0 and gcd(R//85,5*17*prod(P))==1

# Matched 1,200-bit success and complete chart cover.
W = 1728*17*prod(p**3 for p in P if p<=75)
p = 2**1195+1109
q0 = 2**1193
q = q0+(p*pow(5,-1,W)-q0)%W+413*W
S = 3**51+5**145
good = S+85*q
r = pow(3,(q-1)//4,q)
assert r*r%q == q-1 and clean(good,51,145,P)
grid = list(product(range(51,301,16),(145,289)))
assert len(grid)==32 and good%8==5 and good%3!=2 and good%17==S%17
Q = 25*1728*17*prod(p**3 for p in P)
markers = list(islice((p for p in count(139,4) if prime(p)),len(grid)))
B = prod(p*p for p in markers)
t = 0
for (c,d),p in zip(grid,markers):
    m = p*p
    u = (3**c+5**d+p-good)*pow(Q,-1,m)%m
    t += u*(B//m)*pow(B//m,-1,m)
bad = good+Q*(t%B)
assert bad>good and bad.bit_length()==good.bit_length()==1200
assert (Q*B).bit_length()==812 and (bad-good)%Q==0
for (c,d),p in zip(grid,markers):
    R = bad-3**c-5**d
    assert R>0 and R%p**2==p
```

The exclusion theorem guarantees a panel survivor. The finite cover rules out true norms on the tested chart. A cover by one fixed panel across unbounded heights, and almost-all certification for the adaptive selector, remain unresolved. A303656 ranges over all nonnegative exponents.
