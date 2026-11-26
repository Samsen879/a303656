# Weighted paths for depth-one read DAGs

**Yes. Charging a hit to the last parent whose repair differs from its fixed template gives a weighted-path bound for any depth-one read DAG.** The charge retains the joint character saving from all later parents. On the actual \(3,5\) chain \(7\to43\to431\), with \(8043323\) reading all three relays, the bound gives at most \(863\) hits out of \(129731\) choices using the measured deviation counts. The exact replay finds **one** hit, at odd valuation \(1\), with all three relay valuations even. [Pinned triangular result](https://github.com/Samsen879/a303656/blob/9f2a7f96a3203534da04365d588c7cfa091b90ca/analysis/ajt5_overnight_2026_11_26/NESTED_TRIANGULAR_RELAY_AVOIDANCE.md)

### Weighted-path criterion

Fix the integer \(n\) and the exponent primaries outside the adjustable relays. Order the relays topologically. Assume both bases are ordinary at each relay and every cross-read is at depth one. Give each relay \(p\) a fixed first-digit template line with both coordinates moving. On a unit branch use that template. On a root branch use its affine repair line, with a second digit chosen to make the valuation exactly \(2\). For a source relay, its repair line is fixed and can itself be the template.

Sample the first-coordinate **labels** independently and uniformly from their respective \(\mathbb F_p\). The resulting exponent digits can be dependent. Write \(d_p\) for the fraction of ancestor configurations on which relay \(p\) uses a different line from its template. Put
\[
K(N)=\left\lfloor\frac{1+\sqrt{4N-3}}2\right\rfloor,\qquad
\eta(N)=\frac{K(N)}N.
\]
For a reader \(v\) with nonzero observation, let \(J_v\) be its ordered set of adjustable parents, \(N_v=\prod_{p\in J_v}p\), and \(N_{v,p}=\prod_{u\in J_v,\ u\ge p}u\). Then its first-modulus hit fraction satisfies
\[
\boxed{\displaystyle
 B_v\le \eta(N_v)+\sum_{p\in J_v}d_p\,\eta(N_{v,p}).}
\]

With no deviation, embed the hits in the product of the template lines and use the joint character bound. Otherwise, partition by the **last deviating parent** \(p\). Its deviation and its actual line are determined before sampling its own label. Fix that prefix. On the event being counted, all later read parents use their templates. Dropping the restriction that they actually do so embeds the hits in a product of size \(N_{v,p}\), on which the jointly injective character pair again gives the \(K(N_{v,p})\) bound. Averaging over prefixes gives the displayed inequality. The higher digits used for even repair are invisible to these shallow reads.

For a nonzero-observation relay, \(d_v\le B_v\), so the formula recurses along the DAG. Expanding it gives a sum over directed paths with edge weights \(\eta(N_{v,p})\). This is a finite obstruction criterion: if the sum of the terminal budgets on the same label space is below one, an exact even repair avoids every listed terminal. The sum of incoming weights is at most
\[
\frac1{\sqrt P-1}+\frac1{2(P-1)}<1
\]
when all adjustable primes are at least \(P\ge7\), regardless of indegree. This follows by bounding each successive suffix product below by \(P^j\). Known deviation counts can replace recursive bounds at any relay.

### Zero observations

On each fixed prefix and suffix product, the zero hit condition is \(\chi/\psi=-B/A\). Its conditional fraction is zero if the right side lies outside the image, and exactly \(1/|\operatorname{im}(\chi/\psi)|\) otherwise. The image order is the product of the suffix primes on which the two characters differ. These kernel fractions can replace \(\eta\) in the same decomposition, using conditional counts or uniform upper bounds. **There is no automatic contraction for zero observations.**

An actual example is \(7\to379\), with \(n=4884173\). For \(0\le x<7\), take \(c=71631+20466x,\ d=15918+20466x\), adding \(7\cdot20466\) to \(d\) if needed for the relay lift. All seven choices have exact \(v_7=2\) and exact \(v_{379}=1\). The fixed diagonal has trivial quotient and no deviations. The reader \(379\) is ordinary with its own digit frozen here.

### Short replay

For the three-relay chain, the deviation counts are \(0,2,11\), so \(d_{43}=2/7\) and \(d_{431}=11/301\). The terminal bound in counts is \(360+2\cdot136+11\cdot21=863\). Using the recursive bounds alone gives \(2238\).

```python
from math import isqrt, lcm

P, r = (7,43,431), 8043323
n = 1423297603928357024471133488945
edges = {(7,43),(43,431),*((z,r) for z in P)}
for z in (*P,r):
    assert z%4==3 and all(z%i for i in range(2,isqrt(z)+1))
    assert all(pow(a,z-1,z*z)!=1 for a in (3,5))
    for p in P:
        if p>=z:
            continue
        assert ((z-1)%p==0) == ((p,z) in edges)
        if (p,z) in edges:
            assert (z-1)%(p*p) and all(pow(a,(z-1)//p,z)!=1 for a in (3,5))

H = lcm(*(z*z*(z-1) for z in P),r*(r-1))
def step(k):
    return (H//k)*pow(H//k,-1,k)
J = [step(z*z) for z in P]
D = step(H//(7*43*431)**2)
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m
def even(c,d,z):
    f = rem(c,d,z**3)
    return f%z or (f and f%(z*z)==0)

dev, hits = [0,0,0], []
def walk(i,c,d,path):
    if i==len(P):
        assert all(even(c,d,z) for z in P)
        if rem(c,d,r)==0:
            assert rem(c,d,r*r)==r
            hits.append(path)
        return
    z,j = P[i],J[i]
    f = rem(c,d,z*z)
    m,b = 1,0
    if f%z==0:
        a3 = pow(3,c,z*z)*((pow(3,j,z*z)-1)//z)
        a5 = pow(5,d,z*z)*((pow(5,j,z*z)-1)//z)
        inv = pow(a5,-1,z)
        m,b = (-a3*inv)%z,(f//z*inv)%z
    dev[i] += (m,b)!=(1,0)
    for x in range(z):
        C,D1 = c+j*x,d+j*((m*x+b)%z)
        if rem(C,D1,z**3)==0:
            C += z*j
        walk(i+1,C,D1,path+(x,))

assert (n%43,n%431,n%r)==(13,117,7380079)
walk(0,H+5*D,4*D,())
assert (dev,hits)==([0,2,11],[(0,0,0)])

n = 4884173
for x in range(7):
    c,d = 71631+20466*x,15918+20466*x
    if rem(c,d,343)==0:
        d += 7*20466
    assert rem(c,d,343) in range(49,343,49)
    assert rem(c,d,379**2)==379
```

These are finite phase results. Each replay can be activated by adding a sufficiently large multiple of its test moduli to its own fixed target. Deeper reads and unbounded zero-observation kernels remain outside the nonzero contraction bound.

The normalized suffix bounds refer to the same uniform independent label space; they do not require independence of induced phases or of row hits.
