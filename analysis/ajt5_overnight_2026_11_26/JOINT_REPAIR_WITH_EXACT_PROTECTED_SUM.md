# Joint ordinary repair with an exact protected terminal sum

**Two interacting ordinary repairs can preserve the terminal sum even when neither has a private fast axis.** In the exact \(3,5\) example below, \(43\) reads the \(7\)-chart, \(431\) reads \(43\), and both terminal axes read both repair primes. A joint repair exchanges the terminal powers modulo \(q^2\) and preserves their sum. At another cell of the same target, exact sum preservation prevents repair. The full count is **2,261 available cells out of 2,401** under these constraints.

### An exact test for first-digit reads

Fix the provisional chart cell and the exponent coordinates outside a set \(P\) of ordinary repair primes. Suppose the following hold.

- Across the protected sum moduli, each base reads the first digit of every \(p\in P\), and no protected modulus reads a second \(p\)-digit.
- The separately protected component readings are blind to \(P\).
- For distinct \(p,t\in P\), the orders at \(t^3\) read at most the first \(p\)-digit.

Enumerate the attainable terminal power profiles for each base. With one modulus and initial powers \(A,B\), these are cosets \(AG_3,BG_5\). Match \(A'\in AG_3\) with \(B'=A+B-A'\in BG_5\). For several protected sums, do the same with vectors of residues. A hash lookup tests the complement of each profile, with no need to enumerate a Cartesian product. Each matched pair fixes all the first repair digits.

**A matched pair is repairable exactly when its first digits leave no selected row at valuation one.** The second \(p\)-digit cannot change the reading modulo \(p^2\), so a valuation-one row is stuck. A unit already passes. If the remainder is divisible by \(p^2\), the second digit on an ordinary fast axis can give exact valuation two. The depth hypotheses keep this edit invisible to the protected sums and every other repair row. This permits a joint first-digit assignment across the relay before completing the individual lifts. [Predecessor output-isolated repair rule](https://github.com/Samsen879/a303656/commit/2e2c5d54904e266ee271fb9ea237dcd12cc86780)

### Same-target contrast

Take \(q=23{,}611{,}043\). Both terminal orders contain \(43\) and \(431\) exactly once, and the orders at \(431\) are \(43,215\). At the corner, the fibre of the exact sum modulo \(q^2\) has two profiles, the identity and the exchange. Only the exchange passes the valuation-one test.

| Corner phase | \(v_{43}(n-S)\) | \(v_{431}(n-S)\) | Terminal sum |
|---|---:|---:|---|
| Provisional | 1 | 0 | Original |
| After the \(43\)-coordinate edit | 2 | 1 | Changed |
| After the \(431\)-coordinate edit | 2 | 2 | Original |

The exchange requires a nonzero \(431\)-digit change. Thus a \(43\)-only first step cannot both repair \(43\) and preserve the sum at that step. The joint edit succeeds. At cell \((0,7)\), the sum has only its identity profile and the valuation-one failure at \(43\) is unavoidable under exact sum preservation.

All 2,401 provisional cells start with a terminal unit. The replay finds 140 cells with no admissible sum-preserving repair. The other 2,261 extend through the earlier inert prefix. Every other earlier inert prime above 23 is ordinary and its own digit is invisible to the readings at \(43^3,431^3,q^2\), with \(31^3\) separately retained. Those repairs therefore neither obstruct the available cells nor rescue the 140 excluded cells. These counts concern a fixed phase chart and exact sum preservation. Maintaining a terminal unit alone is a weaker condition, and a prescribed ordinary exponent window requires a separate height argument. [Published small-head policy](https://github.com/Samsen879/a303656/commit/4a33a5d51aa0e617fb108629f84b782beebd7977)

### Standalone replay

```python
from collections import Counter
from math import gcd, isqrt, lcm

p,t,q = 43,431,23611043
m,Q = p*t,q*q
D = lcm(3960,49,31**2,q*(q-1)//m)
W = lcm(3960,31**2,q*(q-1)//49,p*p,t*t)
c0,d0 = m*D,D
n = 178924623518619438474129205419586877315

def powers(c,d,M):
    return pow(3,c,M), pow(5,d,M)

def S(c,d,M):
    return sum(powers(c,d,M)) % M

def order(b,e,z,factors):
    assert (z-1)%e==0 and pow(b,e,z)==1
    assert all(pow(b,e//f,z)!=1 for f in factors if e%f==0)

assert all(z%4==3 and all(z%i for i in range(2,isqrt(z)+1))
           for z in (p,t,q))
assert q-1==2*49*13*p*t and t-1==10*p and gcd(D,m)==1
for b,e in ((3,(q-1)//2),(5,q-1)):
    order(b,e,q,(2,7,13,p,t))
    assert all(pow(b,z-1,z*z)!=1 for z in (p,t,q))
order(3,43,t,(5,43))
order(5,215,t,(5,43))
assert W%7 and W%3960==D%3960==0
assert (n-S(c0,d0,32))%4==1
assert all((n-S(c0,d0,z))%z==1 for z in (3,7,11,19,23,31**3))

def cycle(g):
    out = [1]
    for _ in range(m-1):
        out.append(out[-1]*g%Q)
    assert len(set(out))==m and out[-1]*g%Q==1
    return out

U,V = pow(3,D,Q),pow(5,D,Q)
X,Y = cycle(U),cycle(V)
rev = {y:i for i,y in enumerate(Y)}
assert X[5348]==V

def piece(a,r,s):
    return s*s*(a*pow(s*s,-1,r*r)%(r*r))

def move(c,d,r,s):
    return c+D*piece(5348,r,s), d+D*piece(18532,r,s)

corner = (c0,d0)
middle = move(*corner,p,t)
final = move(*middle,t,p)
assert powers(*final,Q)==powers(*corner,Q)[::-1]
assert S(*middle,Q)!=S(*corner,Q)
assert [[(n-S(c,d,z**3))%z**3 for z in (p,t)]
        for c,d in (corner,middle,final)] == [
            [72799,17068142],[1849,50542939],[1849,185761]]
assert [S(*phase,t) for phase in (corner,middle)]==[385,65]
assert all(powers(c,d,31**3)==powers(*corner,31**3)
           for c,d in (middle,final))

fibres = {}
def fibre(c,d):
    a,b = powers(c,d,Q)
    k = a*pow(b,-1,Q)%Q
    if k not in fibres:
        fibres[k] = [(u,rev[z]) for u,x in enumerate(X)
                     if (z:=(1+k*(1-x))%Q) in rev]
    return fibres[k]

def bad(c,d,z):
    a = (n-S(c,d,z*z))%(z*z)
    return a%z==0 and a!=0

assert fibre(*corner)==[(0,0),(5348,18532)]
assert 5348%t and 18532%t
assert fibre(c0,d0+7*W)==[(0,0)] and bad(c0,d0+7*W,p)
counts = Counter()
for i in range(49):
    for j in range(49):
        c,d = c0+W*i,d0+W*j
        assert (n-S(c,d,q))%q
        f = fibre(c,d)
        good = sum(not any(bad(c+D*u,d+D*v,z) for z in (p,t))
                   for u,v in f)
        counts[len(f),good] += 1
assert Counter(map(len,fibres.values()))=={1:48,2:1}
assert counts=={(1,1):2212,(1,0):140,(2,2):42,(2,1):7}

# Exact ordinariness check for this comparator's earlier inert prefix.
P = bytearray(b'\1')*q
P[:2] = b'\0\0'
for k in range(2,isqrt(q-1)+1):
    if P[k]:
        P[k*k:q:k] = bytes((q-1-k*k)//k+1)
total = 0
for z in range(27,q,4):
    if P[z]:
        assert pow(3,z-1,z*z)!=1 or pow(5,z-1,z*z)!=1
        total += 1
assert total==742296
```

Independent BigInt checked all 49 distinct signed profile cases across 2401 cells, the exact distribution including 140 failures, both same-target joint repairs, and ordinariness of the full 742296-prime earlier inert prefix. This characterizes exact sum preservation on the stipulated chart, not terminal-unit failure or ordinary height.
