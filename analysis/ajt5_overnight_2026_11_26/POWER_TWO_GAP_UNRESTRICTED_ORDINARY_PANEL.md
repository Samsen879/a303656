# Power-of-two center gaps through arbitrary finite ordinary panels

**The \(1303\) multiplier can be bypassed uniformly.** Every gap \(h=8\cdot2^a\), \(a\ge0\), gives four centers \((C,D+ih)\) for every target \(n\), after any finite panel of ordinary inert rows has been repaired. A genuine common-Wieferich reader can hit at most one center on each template, with no restriction on its full orders. Thus three such readers cannot cover the four centers.

The change is to handle the only possible tie above 23, at \(31\), while choosing the head. The rest of the ordinary repair uses a single common exponent increment at each row.

### Head choice and exact repair

Choose \(C,D\bmod8\) to pass the tests at \(2,3\). The exact \(7,19\) table below gives at least four surviving indices among \(0,\ldots,4\), with these parities, for every allowed \(h\bmod18\). Keep four.

At \(31\), the \(5\)-powers repeat precisely on indices equal modulo \(3\), since \(\operatorname{ord}_{31}(5)=3\). There are at most two repeated classes among the four indices. Vary \(C\) in steps of \(72\). Since \(\operatorname{ord}_{31}(3)=30\), the five choices give distinct \(3\)-powers, and each repeated class excludes at most one. Choose \(C\) so every repeated class is a unit.

Now vary **\(D\)** in steps of \(72\) to pass \(11\). Its five choices run through the order-five subgroup, and the four retained indices exclude at most four choices. This step preserves the \(31\) readings because \(3\mid72\). Finally vary \(C\) in steps of \(360\) to pass \(23\). This preserves the earlier tests, including the units at \(31\).

If two centers tie modulo another inert prime \(s>23\), then \(\operatorname{ord}_s(5)\mid(i-j)h\). The order has at most one factor of \(2\), so it divides \(6\). The identity
\[
5^6-1=2^3\cdot3^2\cdot7\cdot31
\]
rules out every such tie except at \(31\), where the repeated classes are already units. Consequently at each ordinary row there is at most one center needing repair. On either fast axis, a common exponent increment divisible by \(s-1\) and the earlier protected periods gives a unique first digit and a top digit with exact valuation two. All other centers stay units. The increment leaves earlier readings fixed.

The same identity handles genuine exceptional readers. A two-hit reader would have order dividing \(6\), and the base-\(5\) Wieferich condition would force \(q^2\mid5^6-1\). This is impossible for \(q>23\). The primes in the small head are already safe at every retained center. The argument also covers zero observations. Gaps \(8\) and \(16\) are two simple choices. If identical small-head phases are required, use \(8\) and \(8\cdot2^{60}\), which agree modulo \(3960\). More generally, for any fixed finite retained panel, the exponent of \(2\) can be chosen to make the two gaps congruent modulo all its protected periods, giving identical retained readings at the same final \(C,D\).

### Same-target controls

At \(s=1303\), both bases are ordinary and \(\operatorname{ord}_{1303}(5)=62\). The replay constructs one target with \(C=D=2\) for which all five centers pass every smaller inert row and the small-head tests. Its \(1303\)-readings are as follows.

| Gap | Indices needing repair | Remainders divided by \(1303\), modulo \(1303\), before repair |
|---:|---|---|
| \(8\) or \(16\) | \(0\) | \(772\) |
| \(248\) | \(0,1,2,3,4\) | \(772,508,244,1283,1019\) |
| \(248\cdot1303\) | \(0,1,2,3,4\) | \(772,772,772,772,772\) |

With gap \(248\), the unequal readings make a common first digit impossible on either axis on this frozen lower phase. For either new gap, the fully prefix-preserving first digit is \(581\), and the repaired remainder at index \(0\) is \(628\cdot1303^2\bmod1303^3\). The old multiplied gap also repairs all five on this target.

The steering at \(31\) is necessary. At \(n=11407011\), \(C=D=2\), and gap \(8\), indices \(0,3\) have remainders \(28\cdot31\) and \(3\cdot31\bmod31^2\). Changing \(C\) to \(74\) leaves the small-head tests legal and makes all five centers units at \(31\).

These are **finite-phase** results. The controls can be made positive throughout by adding a sufficiently large multiple of the checked moduli to the target. The uniform construction supplies no ordinary exponent-height bound for the original input \(n\).

```python
from itertools import product
from math import isqrt, lcm, prod

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

def good2(x):
    t = x & -x
    return bool(t and t <= 8 and x//t % 4 == 1)

def order(b,p):
    return next(k for k in range(1,p) if pow(b,k,p) == 1)

assert 5**6-1 == 2**3*3**2*7*31
assert (order(3,31),order(5,31),order(5,1303)) == (30,3,62)
assert (order(5,11),order(3,23)) == (5,11)
assert all(pow(b,1302,1303**2) != 1 for b in (3,5))
assert (8*2**60-8) % 3960 == 0

def live(n7,n19,c,d,h):
    return tuple(i for i in range(5) if (n7-S(c,d+i*h,7))%7
                 and (n19-S(c,d+i*h,19))%19)

for n,e in product(range(32),range(2)):
    assert any(good2((n-S(c,d,32))%32)
               for c,d in product(range(8),range(e,8,2)))
for u,v,a,b,h in product(range(7),range(19),range(2),range(2),(2,4,8,10,14,16)):
    k = max(len(live(u,v,c,d,h))
            for c,d in product(range(a,18,2),range(b,18,2)))
    assert k == (4 if u==0 and a!=b else 5)

p = 1303
small = (3,7,11,19,23)
P = tuple(t for t in range(27,p,4) if prime(t))
assert len(P) == 101 and P[-1] == 1291
assert all(any(pow(b,t-1,t*t)!=1 for b in (3,5)) for t in P)
M = prod(small+P)
a = 3*pow(M,-1,4)%4
n = M*(a+4*((34*pow(M,-1,p)-a)*pow(4,-1,p)%p))
assert n%p**3 == 724272584 and n%32 == 7
B = lcm(3960,p-1,*(t*t*(t-1) for t in P))
F = (pow(3,B,p*p)-1)//p
j = 772*pow(9*F,-1,p)%p
assert j == 581

def R(n,c,d,h,i,s,k):
    return (n-S(c,d+i*h,s**k)) % s**k

for h,first,top in [
    (8,[772],[628]), (16,[772],[628]), (8*2**60,[772],[628]),
    (248,[772,508,244,1283,1019],None),
    (248*p,[772]*5,[628,364,100,1139,875]),
]:
    assert all(good2((n-S(2,2+i*h,32))%32) for i in range(5))
    assert all(R(n,2,2,h,i,t,1) for t in small+P for i in range(5))
    roots = [i for i in range(5) if not R(n,2,2,h,i,p,1)]
    assert [R(n,2,2,h,i,p,2)//p for i in roots] == first
    if top is not None:
        c = 2+B*j
        assert [R(n,c,2,h,i,p,3) for i in roots] == [p*p*t for t in top]
        assert all(R(n,c,2,h,i,p,1) for i in set(range(5))-set(roots))
        assert all(R(n,c,2,h,i,t,3)==R(n,2,2,h,i,t,3)
                   for t in P for i in range(5))

n31 = 11407011
assert [R(n31,2,2,8,i,31,2) for i in (0,3)] == [28*31,3*31]
assert all(R(n31,74,2,8,i,31,1) for i in range(5))
for c in (2,74):
    assert all(good2((n31-S(c,2+8*i,32))%32) for i in range(5))
    assert all(R(n31,c,2,8,i,t,1) for t in small for i in range(5))
```
