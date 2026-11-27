# Simultaneous root avoidance on shallow split-source diamonds

A diamond gives a joint saving across its two relay lines. In the actual \(3,5\) example below, **154 of the 169 split pairs retain a simultaneous repair**. The older row \(443\) and the downstream row both read the split source directly. Both relay valuations are checked at the same integer \(n\). This extends the [pinned two-edge result](https://github.com/Samsen879/a303656/blob/9e939d8bf2f6dfbf6204b28093f945b75acce38d/analysis/ajt5_overnight_2026_11_26/SPLIT_RELEASE_NONZERO_TWO_EDGE.md).

### Simultaneous avoidance on a diamond

Fix the split digits and all exponent primaries outside a set of mutually nonreading relays. Assume both axes at each relay \(p\) are ordinary. On a root branch, the first \(p\)-digits that admit even repair form an affine line with both coordinates moving. Each point can be lifted to exact valuation \(2\) using a second digit. On a unit branch, use the diagonal of the free first digits. Downstream rows may also read the split source directly. For this argument, require that they read the relays only at depth one.

For a downstream reader \(r\), let \(G=\prod_{p\to r}\mathbb Z/p\mathbb Z\) be the product of the relay lines it reads, and \(N=|G|\). On \(G\), the sum it sees is \(A\chi(x)+B\psi(x)\). The two characters are jointly injective because at least one axis moves nontrivially on each read prime coordinate.

If \(n\not\equiv0\pmod r\), the set of hits has at most
\[
K(N)=\left\lfloor\frac{1+\sqrt{4N-3}}2\right\rfloor
\]
points. For a nonzero difference \(d\), two hit equations at \(x,x+d\) determine \(A\chi(x),B\psi(x)\) uniquely if \(\chi(d)\ne\psi(d)\). If the characters agree on \(d\), the common value must be \(1\) because the observation is nonzero. Joint injectivity then forces \(d=0\). Thus every nonzero difference accounts for at most one ordered pair of hits, giving \(K(K-1)\le N-1\).

For several downstream rows, add their \(K(N_r)/N_r\) bounds **on the same product of relay choices**. If the sum is below one, every retained split pair has a simultaneous repair. No independence of the hit events is needed. The fraction of split pairs retained is therefore at least
\[
1-s^{-d_s(q)}-\sum_{w} s^{-d_s(w)},
\]
where \(w\) runs over earlier rows required to be units with their digits frozen and which read no adjustable relay. Relay roots and downstream roots need not be removed at the split stage. At a zero-observation downstream row, the hit set instead comes from a single equation for \(\chi/\psi\). It can fill the product if that quotient is trivial, so the nonzero hypothesis in the joint bound matters.

### Exact \(3,5\) replay

Use \(s=13\), relays \(79,131\), fixed earlier row \(w=443\), downstream reader \(r=9955739\), and zero-observation terminal \(q=9956311\). Both bases give the exact edges
\[
s\to79,131,w,r,q,\qquad 79,131\to r .
\]
All tested rows are ordinary on both axes. The bound gives at least \(11/13\) of the split pairs, and at most \(102/10349\) hits on each downstream relay product. The replay finds **154** retained split pairs. Across those pairs there are only two downstream hits on the chosen products, one each at split pairs \((0,3)\) and \((1,0)\). The latter starts with exact valuations \(2,2,1\) at \(79,131,r\), so the downstream test exercises a real odd valuation before the joint choice.

```python
from math import isqrt, lcm

s,p,t,w,r,q = 13,79,131,443,9955739,9956311
n = 437110530694833428703052343166119315
parents = {p:{s}, t:{s}, w:{s}, r:{s,p,t}, q:{s}}
for z in (s,*parents):
    assert all(z % j for j in range(2,isqrt(z)+1))
for z, ps in parents.items():
    assert {a for a in (s,p,t,w,r) if a<z and (z-1)%a==0} == ps
    for a in ps:
        assert (z-1)%(a*a)
        assert all(pow(b,(z-1)//a,z)!=1 for b in (3,5))
    assert all(pow(b,z-1,z*z)!=1 for b in (3,5))

H = lcm(p*p*(p-1),t*t*(t-1),w-1,r*(r-1),q-1)
def step(k):
    return (H//k)*pow(H//k,-1,k)
E,U,V = map(step,(s,p*p,t*t))

def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

def line(c,d,z,J):
    m = z*z
    f = rem(c,d,m)
    if f%z:
        return [(i,i) for i in range(z)]
    a = pow(3,c,m)*(pow(3,J,m)-1)//z%z
    b = pow(5,d,m)*(pow(5,J,m)-1)//z%z
    return [(i,(f//z-a*i)*pow(b,-1,z)%z) for i in range(z)]

assert n%q==0 and n%r and n%w
assert [rem(H+E,0,z) for z in (p**3,t**3,r*r)] == [p*p,t*t,r]
good, hits = 0,[]
for x in range(s):
    for y in range(s):
        c,d = H+E*x,E*y
        if pow(3,E*x,q)==pow(5,E*y,q) or not rem(c,d,w):
            continue
        a,b = line(c,d,p,U),line(c,d,t,V)
        left = [(pow(3,c+U*i,r),pow(5,d+U*j,r)) for i,j in a]
        right = [(pow(3,V*i,r),pow(5,V*j,r)) for i,j in b]
        bad = {(i,j) for i,(A,B) in enumerate(left)
                     for j,(C,D) in enumerate(right) if (n-A*C-B*D)%r==0}
        if bad:
            hits.append((x,y,len(bad)))
        i,j = next((i,j) for i in range(2) for j in range(2) if (i,j) not in bad)
        c += U*a[i][0]+V*b[j][0]
        d += U*a[i][1]+V*b[j][1]
        for z,J in ((p,U),(t,V)):
            if rem(c,d,z**3)==0:
                c += J*z
            f = rem(c,d,z**3)
            assert f%z or (f and f%(z*z)==0)
        assert all(rem(c,d,z) for z in (w,r,q))
        assert rem(c,d,4)==rem(c,d,3)==1
        good += 1
assert (good,hits)==(154,[(0,3,1),(1,0,1)])
```

These are finite phase results. Adding a sufficiently large multiple of \(12p^3t^3wr^2q\) to \(n\) makes the finitely many replayed remainders positive while preserving their tests. The argument leaves open panels with interdependent relays, deeper downstream reads, or zero-observation rows whose character quotient is trivial.

The split-pair count assumes fully available split digits at the start. Any additional earlier frozen reads must be included among the removed events or in the actual retained subset. With changes only to the designated relay coordinates, any other frozen row that reads them must be included in the downstream test family.
