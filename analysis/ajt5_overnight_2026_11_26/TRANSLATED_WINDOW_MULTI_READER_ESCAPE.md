# Translated windows combine moving-coefficient reader bounds

**Yes. Several short steps can be combined into a many-reader escape on the same release grid.** The required structure is a block of short ratios for multiples of one spare step. In that regime the hit bound becomes sublinear, and the number of readers may grow. A finite version certifies an escape for two actual moving-coefficient \(3,5\) readers, even though adding their individual three-hit bounds gives no certificate. [Pinned three-hit result](https://github.com/Samsen879/a303656/blob/3c844081349a2da3c14dc097018b9c9920b03b27/analysis/ajt5_overnight_2026_11_26/MOVING_COEFFICIENT_THREE_HIT_BOUND.md)

### A joint window bound

Keep the pinned setup: a spare label \(j\in\mathbb F_h\), a singly ordinary relay \(p\) whose forced fast digit is \(Cw^j\bmod p\), and nonzero readers with shallow reads of \(h\) and of only the fast axis at \(p\). At each reader the slow coefficient character moves, so it is injective on the order-\(h\) label group.

Fix \(d\ne0\bmod h\) and a window length \(L<h\). For each \(1\le k\le\lfloor(L-1)/2\rfloor\), take a positive rational representative \(a_k/b_k\equiv w^{kd}\pmod p\). For reader \(r\), let \(E_{r,k}\) bound the number of starting labels at which \(j,j+kd,j+2kd\) are all hits. The three-hit polynomial gives \(E_{r,k}\le a_k+b_k\). A tighter certified bound is the number of roots of that polynomial on the actual slow-character coset.

Let \(R_m(L)\) be the largest subset of \(\{0,\ldots,L-1\}\) that can be coloured with \(m\) colours and contain no monochromatic nonconstant three-term progression. If \(B\) is the union of the hit sets of the \(m\) readers, then
\[
\boxed{\displaystyle
\frac{|B|}{h}\le
\frac{R_m(L)}{L}
+\frac1{hL}\sum_r\sum_k(L-2k)E_{r,k}.}
\]
Colour each hit by one reader it hits. In each translated window \(j+\{0,\ldots,L-1\}d\), remove at most one label per monochromatic triple. At most \(R_m(L)\) coloured labels remain. Each actual triple of step \(kd\) appears in exactly \(L-2k\) windows, and each label appears in \(L\) windows. Summing proves the bound. This proof uses neither independence nor disjoint hit sets.

The bound is useful even from **one** short ratio. If \(w^d=a/b\) with \(H=\max(2,a,b)\), take \(a_k=a^k,\ b_k=b^k\) and \(L=\lfloor\log h/\log H\rfloor\). The error is \(O(mh^{-1/2})\). If \(H=h^{o(1)}\), then \(L\to\infty\). Since \(R_m(L)\le mR_1(L)\), the Bloom–Sisask bound gives \(|B|=o(h)\) for fixed \(m\), and also for \(m\le \exp(c'(\log L)^{1/9})\) with a sufficiently small absolute \(c'>0\). Any retained set of positive relative size then contains a simultaneous escape. These are conditions on the actual orders and ratios. They do not assert an infinite family of singly ordinary relays satisfying them. [Bloom–Sisask, three-term progression bound](https://arxiv.org/abs/2309.02353)

Zero observations stay separate. A nonzero forced fast digit protects a zero reader through its \(p\)-primary component. If the forced digit vanishes in the common-scaling rooted case, the earlier \(p^2\mid n\) argument applies in its stated regime. None of the nonzero hits counted here implies divisibility of \(n\) by the reader.

### Two actual moving readers

Use \(h=653,\ p=40487\), two older readers \(10250810005031,\ 83354871477263\), and terminal \(83354871555623\). The actual slopes from \(h\) are \(401,315,159,649\), respectively. The slope-\(401\) release keeps the relay rooted and the terminal avoided on all 652 nonzero labels.

Use \(d=263\), for which \(w^d=7/27\bmod p\). For both readers, the four three-hit polynomials for \(d,2d,3d,4d\) have **no roots on the actual coset**. A finite check gives \(R_2(9)\le8\), so the window bound certifies at least \(652-\lfloor8\cdot653/9\rfloor=72\) simultaneous escapes. The separate exact phase replay finds 650. The two readers hit labels \(1,2\), respectively, each with valuation \(1\). Both are ordinary controls.

```python
from math import isqrt, lcm

h,p = 653,40487
R = (10250810005031,83354871477263)
q = 83354871555623
n = 5876287000060657202950467015460482075793645557875570177493028174478665292305806831
for z in (h,p,*R,q):
    assert z%2 and all(z%d for d in range(3,isqrt(z)+1,2))
assert pow(3,p-1,p*p)!=1 and pow(5,p-1,p*p)==1

def slope(v):
    k=(v-1)//h
    assert (v-1)%h==0 and k%h
    g,b=pow(3,k,v),pow(5,k,v)
    assert g!=1 and b!=1
    return next(j for j in range(1,h) if pow(b,j,v)==g)

assert [slope(v) for v in (p,*R,q)]==[401,315,159,649]
for r in R:
    k=(r-1)//p
    assert (r-1)%p==0 and k%p
    assert pow(3,k,r)!=1 and pow(5,k,r)==1
    assert all(pow(a,r-1,r*r)!=1 for a in (3,5))
assert (q-1)%p

H=lcm(p*p*(p-1),*(r*(r-1) for r in R),q*(q-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
J,U=step(h),step(p*p)
C,D=H,(p-1)//2*p*R[0]*R[1]*q
assert 27*pow(pow(3,-J,p),263,p)%p==7
assert (n%(p*p),n%q)==(p,0)

triples=[(i,i+k,i+2*k) for k in range(1,5) for i in range(9-2*k)]
assert all(any(len({(mask>>j)&1 for j in T})==1 for T in triples)
           for mask in range(512))

for r in R:
    N=n%r
    assert N
    B,g,b=pow(5,D,r),pow(3,J,r),pow(5,401*J,r)
    for k in range(1,5):
        a,v=7**k,27**k
        alpha,beta=pow(g,263*k,r),pow(b,263*k,r)
        for j in range(h):
            z=B*pow(b,j,r)%r
            lhs=pow(N-z,a,r)*pow(N-beta**2*z,v,r)
            rhs=pow(alpha,v-a,r)*pow(N-beta*z,a+v,r)
            assert (lhs-rhs)%r

def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

hits=[[],[]]
for x in range(1,h):
    c,d=C+J*x,D+J*(401*x%h)
    assert rem(c,d,p*p)==p
    A=pow(3,c,p*p)*((pow(3,U,p*p)-1)//p)%p
    c+=U*pow(A,-1,p)
    if rem(c,d,p**3)==0:
        c+=p*U
    assert rem(c,d,p**3) in range(p*p,p**3,p*p) and rem(c,d,q)
    assert rem(c,d,3)==rem(c,d,4)==1
    for i,r in enumerate(R):
        if rem(c,d,r)==0:
            assert rem(c,d,r*r)==r
            hits[i].append(x)
assert hits==[[1],[2]]
```

Adding a sufficiently large multiple of \(12p^3q\prod_{r\in R}r^2\) to the target makes every replayed remainder positive and preserves the tests. The result is a simultaneous escape criterion for the stated phase family. Arbitrary read graphs and panels without enough admissible releases remain open.

The asymptotic error follows by summing a geometric series in \(H^k\), with \(H^{L/2}\le\sqrt h\); the vanishing-density conclusion still requires the short-ratio regime. The finite window removal counts triples by reader after one reader has been assigned to each hit, so overlaps cannot invalidate the upper bound.
