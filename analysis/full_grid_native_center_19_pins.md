# All 361 internal lift pins at the actual center 19

Yes. At center **19**, the exact native guards **191 and 2851** can pin every point of \(\mathbb F_{19}^2\). Their full prime-square orders share exactly the modulus 19 in each coordinate. For each of the 361 digit pairs there is a choice of unit targets for which both guards are essential to the pin. There is also a choice for every pair that admits an exact center hit at the fixed center residue \(19\bmod361\). For **342** pairs, one choice does both.

The full grid uses several unit-target orbits. I proved a private-order barrier for obtaining the grid from just **one multiplicative translation orbit per guard**. I did not establish such pinning at unboundedly many centers.

## Barrier for two fixed translation orbits

Let \(A,B\subseteq\mathbb F_p^2\) be the two seed masks, and suppose the target translations move them along independent directions \(u,v\). If every \(A+iu\) and \(B+jv\) meet in exactly one point, then the differences \(A-B\) cover \(\mathbb F_p^2\) exactly once. In the nonredundant case \(|A|=|B|=p\).

Moreover, at least one seed must be an affine line. For each nonzero linear functional, summing a primitive \(p\)-th root of unity over the unique difference representations gives a product of two sums equal to zero. A sum of \(p\) such roots vanishes only when every residue occurs once. Thus at least one mask omits the direction given by the kernel of the functional. The masks have disjoint sets of determined directions. Two nonlinear \(p\)-point sets cannot do this, since each determines at least \((p+3)/2\) directions by the Rédei–Megyesi theorem. [Somlai, *A new proof of Rédei’s theorem on the number of directions*](https://arxiv.org/html/2212.12823v1)

Now consider a native guard with actual orders \(h_3=pr_3,\ h_5=pr_5\), each divisible by \(p\) exactly once, and a unit target \(t\bmod q\). If its mask contains a full affine line, then for any integers \(0\le a,b<p\) with \((a+1)(b+1)>p\),
\[
p\ \le\ a r_3+b r_5.
\]
Indeed, normalize the two digit coordinates using the order-\(p\) characters \(x\mapsto x^{r_3}\) and \(y\mapsto y^{r_5}\). Pigeonholing coefficient pairs in the box \([0,a]\times[0,b]\) gives a nonzero normal to the line with coefficients \(A,B\) satisfying \(|A|\le a,\ |B|\le b\). All pairs of power values on the line then satisfy \(x^{Ar_3}(t-x)^{Br_5}=\text{constant}\). Clearing denominators gives a nonzero polynomial of degree at most \(a r_3+b r_5\). It is nonzero because \(0\) and \(t\) are distinct and at least one exponent is nonzero. The \(p\) digit cells require \(p\) distinct solutions.

Thus two guards are too small for this fixed-orbit construction if each admits a box with \(a r_3+b r_5<p\). For example, it is impossible if both have \(\lfloor\sqrt p\rfloor(r_3+r_5)<p\). This bound allows varying the actual order ratios and leaves the multiple-orbit construction open.

## Native two-dimensional family

| Row | Orders of \(3,5\bmod q\) | Orders modulo \(q^2\) |
|---:|---:|---:|
| 19 | \(18,9\) | \(342,171\) |
| 191 | \(95,19\) | \(18145,3629\) |
| 2851 | \(38,95\) | \(108338,270845\) |

The guard lift factors 191 and 2851 are private. A prime-level match can therefore be made an exact hit without changing the shared digit pair. In the replay, the unit residues select the masks, then the prime-square target lifts are chosen explicitly from a witness. The center uses its full prime-square orders.

The largest unit mask has only 14 cells at 191 and 5 at 2851. Neither guard has a \(19\)-cell seed. Nevertheless, varying the unit targets makes all 361 singleton intersections possible, with both individual masks larger than the singleton.

For a fixed deletion control, use
\[
n=69\,445\,834\,912\,649,\qquad
n\equiv(19,26352,5542236)\pmod{(19^2,191^2,2851^2)}.
\]
The two guards pin \((c,d)\equiv(0,0)\pmod{19}\), and \((171,513)\) hits all three rows. At the **same** target, removing guard 191 admits \((3,66)\), and removing guard 2851 admits \((47,86)\). Both alternatives hit the center and change the pinned pair.

This certifies a two-dimensional family at one center, with a separate actual target for each selected pin. It gives neither an unbounded family of centers nor a growing minimal inconsistent star.

## Inline exact replay

The standard-library replay independently verifies the three counts in the opening paragraph, constructs actual targets and exact witnesses for all 361 center-usable pins, and checks both deletions at the fixed control.

```python
from math import gcd, isqrt

p, q, r = 19, 191, 2851
P = (p, q, r)

def cycle(base, m):
    a = [1]
    while a[-1]*base % m != 1:
        a.append(a[-1]*base % m)
    return a

assert all(all(m % d for d in range(2, isqrt(m)+1)) for m in P)
A = {m: tuple(cycle(b,m) for b in (3,5)) for m in P}
h = {m: tuple(map(len,A[m])) for m in P}
L = {
    m: tuple(k*(m if pow(b,k,m*m) != 1 else 1)
             for b,k in zip((3,5),h[m]))
    for m in P
}
assert list(h.values()) == [(18,9),(95,19),(38,95)]
assert list(L.values()) == [(342,171),(18145,3629),(108338,270845)]
assert tuple(gcd(x,y) for x,y in zip(L[q],L[r])) == (p,p)
for u in (q,r):
    assert all(k % u for m in P if m != u for k in L[m])
    assert any(x != y for x,y in zip(h[u],L[u]))

def rows(m):
    masks, odd, witness = [0]*m, [0]*m, {}
    X,Y = A[m]
    for c,x in enumerate(X):
        for d,y in enumerate(Y):
            t = (x+y) % m
            bit = 1 << (c % p*p + d % p)
            masks[t] |= bit
            witness[t,bit,False] = (c,d)
            if c % 2:
                odd[t] |= bit
                witness[t,bit,True] = (c,d)
    return masks, odd, witness

a,_,Wq = rows(q)
b,bodd,Wr = rows(r)
assert max(x.bit_count() for x in a[1:]) == 14
assert max(x.bit_count() for x in b[1:]) == 5

both, usable, usable_both = {}, {}, {}
for t,x in enumerate(a[1:],1):
    for u,y in enumerate(b[1:],1):
        bit = x & y
        if not bit or bit & (bit-1):
            continue
        if x != bit and y != bit:
            both[bit] = (t,u)
        if bodd[u] & bit:
            usable[bit] = (t,u)
            if x != bit and y != bit:
                usable_both[bit] = (t,u)
assert [len(s) for s in (both,usable,usable_both)] == [361,361,342]

def crt(eqs):
    x,M = 0,1
    for y,m in eqs:
        g = gcd(M,m)
        assert (y-x) % g == 0
        z = m//g
        x += M*((y-x)//g*pow(M//g,-1,z) % z)
        M *= z
    return x % M

def shift(m,c,d):
    return (pow(3,c,m*m)+pow(5,d,m*m)) % (m*m)

def hit(n,m,c,d):
    z = (n-shift(m,c,d)) % (m*m)
    return z != 0 and z % m == 0

def join_at_center(bit,t,u):
    X,Y = Wq[t,bit,False], Wr[u,bit,True]
    for d0,y in enumerate(A[p][1]):
        c0 = A[p][0].index(-y % p)
        w = tuple(crt(((X[i],h[q][i]),(Y[i],h[r][i]),(z,h[p][i])))
                  for i,z in enumerate((c0,d0)))
        if hit(p,p,*w):
            return w
    raise AssertionError("no exact center hit")

for bit,(t,u) in usable.items():
    t,u = usable_both.get(bit,(t,u))
    w = join_at_center(bit,t,u)
    assert 1 << (w[0] % p*p + w[1] % p) == bit
    T = (p,(shift(q,*w)+q) % (q*q),(shift(r,*w)+r) % (r*r))
    assert (T[1] % q,T[2] % r) == (t,u)
    n = crt(zip(T,(m*m for m in P)))
    assert all(hit(n,m,*w) for m in P)

T = (19,26352,5542236)
n = crt(zip(T,(m*m for m in P)))
assert n == 69445834912649
assert (T[1] % q,T[2] % r) == (185,2743)
assert a[185] & b[2743] == 1 and a[185] != 1 and b[2743] != 1
assert all(hit(n,m,171,513) for m in P)
for removed,w in [(q,(3,66)),(r,(47,86))]:
    assert (w[0] % p,w[1] % p) != (0,0)
    assert {m for m in P if hit(n,m,*w)} == set(P)-{removed}
```