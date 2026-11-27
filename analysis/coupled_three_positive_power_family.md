# A coupled three-positive ordinary-height family and its fixed-offset ceiling

There is an **explicit two-parameter family with three positive labels**, with all three \(3\)-exponents distinct and all three \(5\)-exponents distinct. It gives \(\Theta((\log X)^2)\) distinct targets up to \(X\), with both exponent axes growing and the largest \(5\)-power at the ordinary height. For these particular three exponent offsets, an inert-prime upper sieve also gives a ceiling of \(O(Q/\sqrt{\log Q})\) per ordinary layer, even when all eligible \(V\) are used.

### One construction enforcing both determinant equations

Let \(T=5^U,\ W=3^V\), where \(U\ge1\) and \(\lceil U/2\rceil\le V\le U\). Set
\[
n=1025T^2+960TW+835W^2,\qquad Q=625T^2=5^{2U+4}.
\]
The three representations are given by the following table.

| \(c\) | \(d\) | First square coordinate | Second square coordinate |
|---:|---:|---:|---:|
| \(2V+4\) | \(2U\) | \(32T+15W\) | \(23W\) |
| \(2V+1\) | \(2U+3\) | \(30T+16W\) | \(24W\) |
| \(2V+5\) | \(2U+4\) | \(20T+24W\) | \(4W\) |

The \(T^2\) coefficients agree because \(32^2+1=30^2+125=20^2+625=1025\). Choosing the common inner product \(480\) forces the first \(W\)-coefficients \(15,16,24\). The three \(W^2\) completions are
\[
15^2+23^2+81=16^2+24^2+3=24^2+4^2+243=835.
\]
Thus the same first norm vector satisfies both determinant differences \(124T^2-78W^2\) and \(624T^2+162W^2\) against the second and third vectors. The two coordinate-difference vectors have determinant \(2W(25T-14W)>0\). The construction couples the three norms on one target.

Since \(W\le T\), one has \(Q<n\le2820T^2<5Q\). Also \(n\equiv20\bmod120\) for \(U,V\ge1\). For fixed \(U\), \(n\) increases strictly with \(V\), and the ordinary windows for different \(U\) are disjoint. In the stated growing range, the number of distinct targets up to \(X\) is
\[
\frac1{16}(\log_5 X)^2+O(\log X).
\]

### Local densities and finite phases

Write \(s_i=3^{c_i}+5^{d_i}\). At odd \(p\), the local density for the two coupled equations is the integral over \(t\in\mathbb Z_p\) of the product of the three binary norm densities at \(t-s_i\). Thus a determinant divisor changes the **joint** factor.

- **Split primes.** The binary norm density is \((1-1/p)(1+v_p(t))\) off zero. Giving the norm weight \(1,1/2,0\) at valuations \(0,1,\ge2\) gives the exact joint factor
  \[
  (1-1/p)^3\left(1-\frac{\nu_{p^2}}{p^2}\right),
  \]
  where \(\nu_{p^2}\) counts the distinct shifts modulo \(p^2\). For one colliding pair of depth \(e\), with the third shift separate modulo \(p\), the **unweighted** integral has an extra term \((1-p^{-e})(p+1)/(p-1)^2\) inside the factor \((1-1/p)^3\). It comes from summing \(p^{-\max(r,s)}\) over \(r,s\ge1\) with \(\min(r,s)\le e\).
- **Inert primes.** The binary norm density is \((1+1/p)\mathbf1_{v_p(t)\ {\rm even}}\). With three distinct roots modulo \(p\), the joint factor is \((1+1/p)^3(1-3/(p+1))\). For one colliding pair of depth \(e\), replace the survival term by
  \[
  (1-1/p)\sum_{\substack{0\le j<e\\ j\ {\rm even}}}p^{-j}
  +\mathbf1_{2\mid e}\,p^{-e}\left(1-\frac2{p+1}\right)-\frac1{p+1}.
  \]
  Below depth \(e\), both valuations agree. At depth \(e\), the pair separates into two unit-distance roots, which explains the parity term.
- **Triple collisions.** The coefficient determinant is \(124\cdot162+78\cdot624=2^3 3^2 5\cdot191\). Outside \(2,3,5\), a triple collision would require \(p=191\) and \(T^2/W^2\equiv53\bmod191\). But \(53^{95}\equiv-1\bmod191\). Thus at every \(p\ge7\) there is at most one colliding pair.

There is also an explicit deeper class. Taking \(U\equiv0\bmod144\) and \(V\equiv0\bmod16\) gives \(n\equiv6020\bmod17280\). The periods used are \(\operatorname{ord}_{128}(25)=\operatorname{ord}_{128}(9)=16\) and \(\operatorname{ord}_{27}(25)=9\). The class restriction retains \(1/(144\cdot16)\) of the leading parameter count.

### The density ceiling for these offsets

At an inert prime \(p\ge11\) away from the determinant divisors, the three roots forbid \(3(p-1)\) classes modulo \(p^2\) by the exact-valuation-one test. An upper-bound sieve at a fixed-power level, with CRT remainder \(O(3^{\omega(d)}d)\), gives
\[
O\!\left(\frac{Q}{(\log Q)^{3/2}}F_C(\Delta)\right)
\]
targets for one label, where \(\Delta=\prod_{i<j}(s_j-s_i)\) and \(F_C(m)=\prod_{p\mid m}(1+C/p)\). [Upper-bound fundamental lemma, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

The actual differences are \(124T^2-78W^2,\ 624T^2+162W^2,\ 500T^2+240W^2\). On a phase \(V=v_0+rj\), after removing primes dividing the coefficients or 3, each divisor test is a congruence in \((9^r)^j\). The order cost is explicitly
\[
\frac1{\operatorname{ord}_d(9^r)}
=\frac{\gcd(r,\operatorname{ord}_d(9))}{\operatorname{ord}_d(9)}
\le\frac{r}{\operatorname{ord}_d(9)},
\]
plus the progression endpoint error \(O(r/U)\) on a full layer. To sum the costs, truncate the expansion of \(F_C\) at \(d\le U\) at bounded cost. For this, primes above a small fixed power \(U^\delta\) have bounded total reciprocal weight, and the remaining weighted divisors have mean \(\log d=O_C(\delta\log U)\). The order-weighted sum converges by dyadic summation, since all divisors of order at most \(t\) divide \(\prod_{j\le t}(9^j-1)\), whose logarithm is \(O(t^2)\). Hölder combines the three differences. Thus the unrestricted mean is bounded, and a step-\(r\) phase has mean \(O_C(r)\) when it contains \(\asymp U/r\) labels.

Summing the upper bound over \(V\le U\) proves the layer ceiling. Positive density for arbitrary triples of exponent labels remains a separate question, as does any prescribed-\(n\) assertion.

### Inline exact replay

The ordinary-height control is \(47{,}540\), with labels \((6,2),(3,5),(7,6)\). The replay also checks an actual split collision at each of depths one and two. The script includes an independent modular enumeration of the weighted split factors.

```python
from math import prod

rows = ((4,0,32,15,23), (1,3,30,16,24), (5,4,20,24,4))
def box(U,V):
    T,W = 5**U,3**V
    n = 1025*T*T + 960*T*W + 835*W*W
    s = [3**(2*V+c)+5**(2*U+d) for c,d,_,_,_ in rows]
    for h,(_,_,a,b,e) in zip(s,rows):
        assert n == h + (a*T+b*W)**2 + (e*W)**2
    assert 625*T*T < n < 3125*T*T and n%120 == 20
    return n,s

assert box(1,1) == (47540,[754,3152,17812])
assert box(144,80)[0]%17280 == 6020
assert 124*162+78*624 == 2**3*3**2*5*191
assert 78*pow(124,-1,191)%191 == 53 and pow(53,95,191) == 190

p,m = 13,13**2
fiber = [0]*m
for a in range(m):
    for b in range(m):
        fiber[(a*a+b*b)%m] += 1
weight = [0 if t==0 else fiber[t]*(2-(t%p==0)) for t in range(m)]
for U,V,e in ((3,3,1),(13,9,2)):
    _,s = box(U,V)
    h = s[2]-s[1]
    assert h%p**e == 0 and h%p**(e+1)
    assert sum(prod(weight[(t-a)%m] for a in s) for t in range(m)) == (
        8*(m-m//p)**3*(m-len({a%m for a in s}))
    )
```