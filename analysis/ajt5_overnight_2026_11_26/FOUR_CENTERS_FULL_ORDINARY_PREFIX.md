# Four centers through the full ordinary inert prefix at 1291

**Four local-phase centers are available for every target \(n\), even after repairing the full ordinary inert prefix through \(1291\).** They have one common \(3\)-exponent and four distinct \(5\)-exponents drawn from five consecutive offsets. Each genuine common-Wieferich reader can hit at most one center, with unrestricted full orders. Thus three such readers cannot cover the menu. For some targets all five centers survive, and four readers cannot cover it.

### How the centers are chosen and retained

The published head policy fixes \(d\) after the tests at \(2\) and \(3\), and then adjusts \(c\). The construction here expands that menu. It keeps a common \(d\bmod8\) and allows the five \(5\)-exponents \(D+i\Delta\), \(0\le i\le4\), with \(\Delta=8\cdot31\) for the prefix through \(1291\). Each surviving center receives its own legal mod-\(3960\) head. [Published head policy](https://github.com/Samsen879/a303656/blob/4a33a5d51aa0e617fb108629f84b782beebd7977/analysis/ajt5_overnight_2026_11_26/DUAL_LOCKED_HEAD_UNIT_EXTENSION.md)

Choose \(c,d\bmod8\) to pass the tests at \(2\) and \(3\). For every even \(\Delta\) coprime to \(3\), the exact \(7,19\) table in the replay gives a choice of \(c,d\bmod18\) with those parities that keeps at least four indices. It keeps all five unless \(n=0\bmod7\) and the parities differ. The steps of size \(72\) at \(11\) and \(360\) at \(23\) can keep every surviving index. At \(11\), the only case requiring more than a count is five indices. The five candidate powers on each axis then range over the order-five subgroup \(U\). A total cover would give \(n-U=U\), so summing forces \(n=0\bmod11\). But \(-U\ne U\).

For a general finite retained ordinary panel \(P\), build the gap before reading any terminal. Start with \(\Delta=248\). In increasing order, multiply it by \(s\in P\) only if \(s\nmid\Delta\), base \(5\) is ordinary there, and \(5^{k\Delta}=1\bmod s\) for some \(1\le k\le4\). Write the final gap as \(248J\). Later multipliers cannot create an earlier collision because they exceed every earlier order.

Now repair each ordinary row on either fast axis, using common exponent increments for all centers. Two centers that need repair at \(s\) have the same \(5\)-power modulo \(s\). They also have the same power modulo \(s^2\): either \(s\mid\Delta\), or base \(5\) already has unchanged order modulo \(s^2\). Thus they need the same first repair digit. Each forbids at most one top digit, and there are at most five centers and \(s>23\). The common top digit gives exact valuation two at all tied centers. The other centers stay units. Taking increments divisible by the earlier \(t^2(t-1)\) preserves every earlier test.

### Why exceptional readers cannot reuse a hit

Two hits by the same reader \(q\) imply \(\operatorname{ord}_q(5)\mid(i-j)\Delta\). For inert \(q\), the order has at most one factor of \(2\), so it divides \(186J\). If the order is coprime to \(J\), it divides \(186\); a base-\(5\) Wieferich hit would then require \(q^2\mid5^{186}-1\).

The two short factor identities in the replay certify that the only squared prime factors of \(5^{186}-1\) are at \(2,3,31\). They also show that \(1303\) is the first inert prime above \(31\) that can enter \(J\). All 101 inert rows from \(31\) through \(1291\) are ordinary by direct modular checks, so this full prefix has \(J=1\). For larger panels, a reader that hits more than one center must have an order dividing \(186J\) and sharing a prime with \(J\). The argument includes zero observations. The inert candidates 3 and 7 are already handled by the head and 31 is ordinary (checked in the replay), so none of the squared factors 2, 3, 31 allows an untreated repeated hit.

### Exact controls

- **Five and four centers.** For the actual retained prefix through \(67\), target residue \(n=5\) gives \((C,D)=(8336678197773066122577,72)\) and indices \(0,1,2,3,4\). Target residue \(n=7\) gives \((576,17)\) and indices \(0,1,3,4\). The loss at \(7\) is forced in this five-offset template: the tests at \(2,3\) force \(C\) even and \(D\) odd, so the five \(5\)-powers traverse all three nonsquares modulo \(7\), including \(-3^C\).
- **The first gap multiplier is necessary on a frozen lower phase.** At \(s=1303\), keep the five-center control’s exponents and take \(n=58146852412578862298771812862088485\), which preserves its entire prefix through \(67\). With gap \(248\), indices \(0,3\) have remainders \(107s,306s\bmod s^2\). They tie modulo \(s\) and require different first digits on either common fast axis. The gap rule does insert \(1303\).

These are finite-phase statements. For positive-remainder versions of the controls, add a sufficiently large multiple of all checked moduli to the target. The uniform theorem gives no bound placing its representatives inside the ordinary exponent window of the input \(n\).

```python
from itertools import product
from math import gcd, isqrt, lcm, prod

def trial(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p)+1))

cert = {
    625552508473588471: (25654001,391337),
    172974812463239310024750410929: (13393417,118258507),
    53345671490722200466369: (95217791,487709093),
}
def prime(p):
    if p not in cert:
        return trial(p)
    fs = cert[p]
    F = prod(fs)
    return (F*F > p and (p-1)%F == 0 and pow(2,p-1,p) == 1
            and all(trial(f) and gcd(pow(2,(p-1)//f,p)-1,p) == 1 for f in fs))

minus = (1861,148429,878851,625552508473588471,172974812463239310024750410929)
plus = (7,1303,21207101,258065887,28086211607,75005167927,53345671490722200466369)
assert len(set(minus+plus+(2,3,31))) == 15
assert all(map(prime,minus+plus+(2,3,31)))
assert 5**93-1 == 4*31**2*prod(minus)
assert 5**93+1 == 18*prod(plus)
assert min(p for p in minus+plus if p > 31 and p%4 == 3) == 1303

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m)) % m

def good2(u):
    k = u & -u
    return bool(k and k <= 8 and u//k%4 == 1)

def mask(n7,n19,c,d,h):
    return tuple(i for i in range(5)
                 if (n7-S(c,d+i*h,7))%7 and (n19-S(c,d+i*h,19))%19)

for n,e in product(range(32),range(2)):
    assert any(good2((n-S(c,d,32))%32)
               for c,d in product(range(8),range(e,8,2)))
for n7,n19,a,b,h in product(range(7),range(19),range(2),range(2),(2,4,8,10,14,16)):
    k = max(len(mask(n7,n19,c,d,h)) for c,d in
            product(range(a,18,2),range(b,18,2)))
    assert k == (4 if n7 == 0 and a != b else 5)

def gap(P):
    h = 248
    for p in P:
        if h%p and pow(5,p-1,p*p)!=1 and any(pow(5,k*h,p)==1 for k in range(1,5)):
            h *= p
    return h

def centers(n,P):
    h = gap(P)
    a,b = next((a,b) for a,b in product(range(8),repeat=2)
               if good2((n-S(a,b,32))%32) and (n-pow(5,b,3))%3)
    def I(c,d):
        return mask(n%7,n%19,c,d,h)
    u,v = max(product(range(a%2,18,2),range(b%2,18,2)),key=lambda z:len(I(*z)))
    ix = I(u,v)
    c = next(k for k in range(1,73) if k%8==a and k%18==u)
    d = next(k for k in range(1,73) if k%8==b and k%18==v)
    for p,B,k in ((11,72,5),(23,360,11)):
        c = next(c+B*t for t in range(k) if all((n-S(c+B*t,d+i*h,p))%p for i in ix))
    K = 3960
    for p in P:
        B = lcm(K,p-1)
        assert B%p
        roots = [i for i in ix if (n-S(c,d+i*h,p))%p==0]
        if roots:
            b = next(b for b in (3,5) if pow(b,p-1,p*p)!=1)
            def R(i,t,m):
                return (n-S(c+(b==3)*B*t,d+i*h+(b==5)*B*t,m))%m
            assert len({R(i,0,p*p) for i in roots}) == 1
            j, = [j for j in range(p) if R(roots[0],j,p*p)==0]
            k = next(k for k in range(p) if all(R(i,j+p*k,p**3) for i in roots))
            c += (b==3)*B*(j+p*k)
            d += (b==5)*B*(j+p*k)
        K = lcm(K,p*p*(p-1))
    for i in ix:
        assert good2((n-S(c,d+i*h,32))%32)
        assert all((n-S(c,d+i*h,p))%p for p in (3,7,11,19,23))
        for p in P:
            u = (n-S(c,d+i*h,p**3))%(p**3)
            assert u%p or (u and u%p**2==0)
    return c,d,ix

P0 = tuple(p for p in range(27,1303,4) if trial(p))
assert len(P0)==101 and P0[-1]==1291 and gap(P0)==248
assert all(any(pow(b,p-1,p*p)!=1 for b in (3,5)) for p in P0)

P = tuple(p for p in P0 if p<=67)
c,d,I = centers(5,P)
assert (c,d,I)==(8336678197773066122577,72,(0,1,2,3,4))
assert centers(7,P)==(576,17,(0,1,3,4))

p = 1303
assert gap(P+(p,)) == 248*p
M = 32*3*7*11*19*23*prod(t**3 for t in P)
n = 58146852412578862298771812862088485
assert n%M == 5
assert [(n-S(c,d+i*248,p*p))%(p*p) for i in (0,3)] == [107*p,306*p]
```
