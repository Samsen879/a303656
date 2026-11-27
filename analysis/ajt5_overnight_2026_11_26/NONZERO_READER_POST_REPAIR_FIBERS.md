# Nonzero reader fibers after ordinary restoration

**A frozen character-fiber bound can fail after ordinary restoration.** In the actual \(163\to8803\) control, a nonzero reading rejects one of three frozen ternary probes and two of the same probes after a one-axis repair. Both hits have exact valuation one. All ordinary rows below \(8803\) can be completed while preserving those hits and the three distinct shifts at the terminal \(103951\).

A deterministic bound survives if the last ordinary parent’s repair line is kept free. This gives a new sufficient condition for excluding first blocking on a selected legal ternary cylinder. The verified exception-density bound remains **below \(0.000062192085\%\)**. [Predecessor ternary-cover criterion](https://github.com/Samsen879/a303656/commit/3700a5b245e6a77cd15b8a6147041b6fb0cc1016)

### A post-repair bound at the last parent

Fix a legal ternary probe and its incoming phase at a doubly ordinary inert row \(r\). Suppose the row is rooted modulo \(r\), both first \(r\)-primary digits are free, and all retained requirements other than the assigned readers can be preserved on those digits or restored later without changing the assigned shifts or the terminal value. The first digits required for a repair satisfy \(j=j_0+\lambda i\bmod r\), with \(\lambda\ne0\). Use second digits to make the valuation exactly two.

Assign to \(r\) some nonzero exceptional readers. Require each to read at least one first \(r\)-digit and neither second digit. Suppose later repairs preserve its assigned shift. With the other primary coordinates fixed, the shift at such a reader \(p\) has the form
\[
A X^i+B Y^i,\qquad X^r=Y^r=1.
\]
At least one character is nontrivial. If the characters are distinct and nontrivial, two hits at a prescribed nonzero difference \(h\) determine \(AX^i,BY^i\) uniquely. The determinant is \(Y^h-X^h\ne0\), so at most one ordered pair of hits has difference \(h\). A nonzero target therefore has at most
\[
K_r=\left\lfloor\frac{1+\sqrt{4r-3}}2\right\rfloor
\]
hits. If just one character varies, the bound is one. If the characters agree, the shift is injective or identically zero, so the nonzero observation still costs at most one digit.

Thus **the sum of those per-reader costs being less than \(r\) suffices to restore the entire assigned group to units**. This counts a union of actual forbidden digits and uses no independence between readers. Apply it separately to two ternary probes that pass the zero-row cover test and have distinct terminal residues. Under the stated preservation conditions, both extend through the older prefix and the terminal cannot first block.

The qualification about available digits is essential. If only one repair axis is ordinary and its first digit is forced, a reader of that axis can see a single constant nonzero shift. Likewise, fixing one deterministic point on a doubly ordinary repair line can create a collision that the frozen ternary character never had. The bound above counts the **remaining repair choices for each probe**, rather than bounding the number of bad ternary probes after an arbitrary choice of repair. [Earlier fixed-repair and spare-digit comparisons](https://github.com/Samsen879/a303656/blob/62fcf9dfa8ca3fbb7e1f9f4bca3cb22db01a6545/analysis/ajt5_overnight_2026_11_26/NONISOLATED_SPARE_DIGIT_SPLIT.md)

### Actual control

The three probes share one legal class modulo \(3960\), with \(c\not\equiv0\bmod3,\ d\equiv0\bmod3\), and vary the third ternary digit of \(d\). At \(8803\) their frozen shifts are \(134,8429,267\). The observation has residue \(8429\). The third probe roots at \(163\), where the one-axis repair forces first digit \(78\) and changes its shift at \(8803\) to \(8429\). Keeping both repair axes free instead gives **160 distinct shifts on the 163-point repair line**, with only one point hitting \(8429\).

All three primes in this fixture are ordinary. It tests the arithmetic with the reader’s own digits held fixed. The deterministic theorem applies to a genuinely common-Wieferich reader under its stated availability conditions. A bound for arbitrary interacting nonzero exceptional readers would still require such a repair allocation or their actual post-repair hit sets.

```python
from math import isqrt, lcm

def prime(p):
    return p > 1 and all(p % j for j in range(2, isqrt(p)+1))

def order(b,p):
    return next(j for j in range(1,p) if pow(b,j,p)==1)

def strip(m,p):
    while m%p==0:
        m//=p
    return m

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

r,p,q = 163,8803,103951
assert all(prime(v) and v%4==3 for v in (r,p,q))
assert [(order(3,v),order(5,v)) for v in (r,p,q)] == [
    (162,54),(2934,8802),(9450,51975)]
assert all(pow(b,v-1,v*v)!=1 for v in (r,p,q) for b in (3,5))

n = 253027766117386375380531341684196440580006012099
c,d,T,L = 2,3,198875615400,96664529946600

def R(c,d,m):
    return (n-S(c,d,m))%m

def exact(c,d,p,e):
    return R(c,d,p**(e+1)) in range(p**e,p**(e+1),p**e)

assert (n%3,n%32,n%p)==(0,3,8429)
assert T%3960==0 and T%27 and L%3960==0 and L%(r-1)==0 and L%r
assert all(pow(b,L,q)==pow(b,r*L,p*p)==1 for b in (3,5))
assert all(pow(b,L,p)!=1 for b in (3,5))
ds = [d+T*j for j in range(3)]
assert [S(c,b,p) for b in ds]==[134,8429,267]
assert [j for j,b in enumerate(ds) if exact(c,b,p,1)]==[1]

head = (7,11,19,23)
lo = [u for u in range(31,r,4) if prime(u)]
mid = [u for u in range(r+4,p,4) if prime(u)]
M = lcm(3960,q-1,p*p*(p-1),*((u-1)*u*u for u in lo+[r]+mid))

def finish(a,b):
    saved = S(a,b,p*p),S(a,b,q)
    for u in mid:
        z = R(a,b,u**3)
        if z%u:
            continue
        assert all((v-1)%u for v in (p,q))
        U = strip(M,u)
        f = ((pow(3,U,u*u)-1)//u)*pow(3,a,u)%u
        a += U*(z//u)*pow(f,-1,u)
        if not R(a,b,u**3):
            a += U*u
    assert all(R(a,b,u) or exact(a,b,u,2) for u in lo+[r]+mid)
    assert all(R(a,b,u) for u in head)
    assert R(a,b,32)%4==1 and (n-pow(5,b,3))%3
    assert (a-c)%3960==(b-d)%3960==0
    assert saved==(S(a,b,p*p),S(a,b,q))
    return a,b

assert all(R(c,b,r) for b in ds[:2]) and not R(c,ds[2],r)
assert [j for j in range(r) if not R(c+L*j,ds[2],r*r)]==[78]
a = c+78*L
if not R(a,ds[2],r**3):
    a += r*L
post = [finish(c,ds[0]),finish(c,ds[1]),finish(a,ds[2])]
assert [j for j,(x,y) in enumerate(post) if exact(x,y,p,1)]==[1,2]
assert [S(x,y,q) for x,y in post]==[S(c,b,q) for b in ds]
assert len({S(x,y,q) for x,y in post})==3

line = []
for i in range(r):
    a = c+L*i
    j, = [j for j in range(r) if not R(a,ds[2]+L*j,r*r)]
    b = ds[2]+L*j
    if not R(a,b,r**3):
        a += r*L
    assert exact(a,b,r,2) and S(a,b,q)==S(c,ds[2],q)
    line.append(S(a,b,p))
assert [i for i,x in enumerate(line) if x==8429]==[78]
assert len(set(line))==160
```

The collision count concerns choices that remain free at the last ordinary parent, not a bound on a previously frozen chart. A unit at the assigned prime is an admissible residue at every precision, so avoiding the conservative congruence collision is sufficient. The arithmetic control uses a nonzero reading at an ordinary analogue of the exceptional reader; it does not claim an actual common-Wieferich first blocker.
