# Twenty interlaced sphere rays and an exact scale-three exponent strip

**The \(38\)–\(42\) gap contains two new certified phases, \(118/3\) and \(122/3\).** The smallest nonempty strip has exactly three admissible exponent pairs \((m,e)=(118,70),(122,74),(122,78)\). The last two share a phase. The twenty-ray construction now has largest adjacent phase ratio \(235/213\), giving a uniform generated-population exponent of **\(213/470\)** in both odd classes.

### Exact strip and reusable arithmetic filter

Scale \(1\) has no \(m\equiv2\bmod4\) strictly between \(38\) and \(42\). At scale \(3\), \(m=118,122\), and the respective bounds on \(e\equiv2\bmod4\) under \(3^e<5^m\) are \(170,178\). This gives 88 pairs. The replay certifies the three survivors by direct norm identities and rejects the other 85 by exact odd valuations at primes \(p\equiv2\bmod3\).

Three exponent rules alone reject 57 of the 88 pairs. Write \(u=m/2,\ v=e/2,\ A=5^u,\ B=3^v\).

- **At \(2\)**, \(v_2(A-B)=1\), so admissibility requires \(v_2(A+B)\) odd. For any \(r\ge3\), there is a unique \(\beta_r\bmod2^{r-2}\) with \(5^{\beta_r}\equiv-3\bmod2^r\). Thus \(2^r\mid A+B\) exactly when \(u\equiv\beta_r v\bmod2^{r-2}\). This gives the full valuation from congruences on the exponents.
- **At \(11\)**, \(2v\equiv u\bmod5\) and \(11\nmid u\) force valuation one in \(25^u-9^v\).
- **At \(17\)**, \(v\equiv5u\bmod8\) and \(v\not\equiv8u\bmod17\) force valuation one in the same difference.

The odd-prime rules follow from a common-order test. If \(a^u\equiv b^v\bmod p\) and \(L\) is a common multiple of the two orders with \(p\nmid L\), raising both terms to \(L\) preserves the valuation. Writing \(a^L\equiv1+p\alpha\) and \(b^L\equiv1+p\beta\bmod p^2\), the valuation is one whenever \(\alpha u-\beta v\not\equiv0\bmod p\). Here \((L,\alpha,\beta)=(5,7,0)\) at \(11\) and \((8,12,10)\) at \(17\). These rules apply across exponent strips.

### Growing true witnesses and same-height failures

The replay gives both half-norm integers for each seed. Its row \((m,e,h,a,b,c,d)\) certifies
\[
A+B=2^h(a^2+3b^2),\qquad A-B=2(c^2+3d^2).
\]
Multiplying these norms gives \(V^2+3W^2=4(Q-Z)\) at \(Q=5^m,\ Z=3^e\), with both coordinates divisible by \(8\). Cubing \(Q,Z\) multiplies the norm element by \((Q-Z)/2+(Q+Z)\sqrt{-3}/2\), preserving that divisibility.

At every depth, the three unit rotations by \(1,\epsilon,\epsilon^2\), where \(\epsilon=(1+\sqrt{-3})/2\), give all three ratios \(W/V\bmod3\) and keep the coordinates divisible by \(4\). The two rotations with \(3\nmid W\) are separated by \(\pi/3\) modulo \(\pi\). At least one has \(3W^2\ge Q-Z\). Taking \(W>0\) in that rotation gives \(W^2>3Z\), since \(Q>10Z\) throughout these rays.

Put \(s=\sqrt Z\), \(S_1(t)=(t-s)^2+t^2\), and \(S_3(t)=(t+s)^2+(t-2s)^2\). At \(t=W\),
\[
n_\lambda=5Q+\lambda Z-S_\lambda(W)
          =Q+(4-\lambda)Z+V^2+(W+s)^2,\qquad Q<n_\lambda<5Q.
\]
The classes are \(21\bmod24\) for \(\lambda=1\) and \(3\bmod24\) for \(\lambda=3\). The true positive exponent pairs are \((e3^k+1,m3^k)\) and \((e3^k,m3^k)\), respectively.

Replacing \(t\) by \(s+j\) gives signed witnesses in the same windows and classes. The selected positive residual has the same value in both classes. At depth \(0\), the three seeds give residues \(55\bmod11^2\), \(12319\bmod127^2\), and \(13761\bmod139^2\), respectively. Each is an exact valuation-one obstruction at a Gaussian inert prime. The replay checks both sides again at depth \(1\). These failures concern the selected exponent pair.

### Phase spacing and population

The old gap splits into ratios \(59/57,\ 61/59,\ 63/61\). The new maximum is \((470/9)/(142/3)=235/213\). For the effective per-height count, both sphere values \(3W^2+2\lambda Z\) have the required residues \(2\) or \(6\bmod8\) and \(3\bmod9\). Writing either as \(3Df^2\) gives \(W^2-Df^2=-2\cdot3^{e3^k-1}\) or \(-2\cdot3^{e3^k}\), so the bounded discriminant multiplicity argument still applies. Unit rotations preserve the distinct shell ideals, and \(Z=Q^\gamma\) with fixed \(\gamma<1\) preserves the power saving in height trimming. The resulting cumulative lower bound in each class is
\[
A_\lambda(X)\gg_\varepsilon
\frac{X^{213/470}}{(\log X)^{1+\log 2-\log_3 2+\varepsilon}}.
\]
The exponent is sharp as a lower limiting exponent for these generated sphere populations by the largest gap and the \(Q^{1/2+o(1)}\) per-height upper bound. This gives no coverage claim for prescribed integers. [Effective sphere count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md) · [De la Bretèche–Tenenbaum, mean-value input](https://arxiv.org/abs/2403.19320)

### Inline replay

The self-contained Python replay checks both the finite strip and the norm fixtures. An independent BigInt implementation confirmed all 88 classifications and the six controls.

```python
from fractions import Fraction as F
from math import isqrt

# m, e, h, plus coordinates, minus coordinates, [(j, p, residue) by depth]
rows = [
 (118,70,3,141153760009142392898,24218859627650530745,
           39180679721577737321,168524032050224715916,[(25,11,55),(25,67,4288)]),
 (122,74,3,661443829269635519269,186720064056574162380,
           1472012643098564822209,22971892455680776380,[(1,127,12319),(13,23,345)]),
 (122,78,5,109568599911781408742,202912126690397707667,
           1373328890101822521973,306796406205975162630,[(13,139,13761),(5,11,66)]),
]
panel = [2,17,11,23,53,47,83,113,239,383,443,467,677,977,1019,2657,
         4793,5333,34457,36653,169283,183971,674393,1112093,3468233,
         319092419,13921061569643]

def prime(p):
    return p > 1 and all(p%i for i in range(2,isqrt(p)+1))

def vp(n,p):
    r = 0
    while n%p == 0:
        r,n = r+1,n//p
    return r

assert all(prime(p) and p%3 == 2 for p in panel)
assert [m for m in range(115,126) if m%4 == 2] == [118,122]
assert (pow(25,5,121),pow(9,5,121)) == (78,1)
assert (pow(25,8,289),pow(9,8,289)) == (205,171)
assert pow(9,5,17) == 25%17 and pow(9,4,17) == 16
survivors, structural = set(),0
for m,E in ((118,170),(122,178)):
    assert 3**E < 5**m < 3**(E+4)
    for e in range(2,E+1,4):
        N,u,v = 5**m-3**e,m//2,e//2
        if all(vp(N,p)%2 == 0 for p in panel):
            survivors.add((m,e))
        structural += any((vp(N,2)%2,(2*v-u)%5 == 0,
                           (v-5*u)%8 == 0 and (v-8*u)%17 != 0))
assert survivors == {(r[0],r[1]) for r in rows} and structural == 57

for m,e,h,a,b,c,d,tests in rows:
    A,B = 5**(m//2),3**(e//2)
    assert 2**h*(a*a+3*b*b) == A+B and 2*(c*c+3*d*d) == A-B
    f = 2**((h+3)//2)
    Q,Z,u,z = A*A,B*B,f*(a*c-3*b*d),f*(a*d+b*c)
    for j,p,rem in tests:
        W,V = max((abs(y),abs(x)) for x,y in
                  [(u,z),((u-3*z)//2,(u+z)//2),
                   ((-u-3*z)//2,(u-z)//2)] if y%3)
        s = isqrt(Z)
        assert s*s == Z and V*V+3*W*W == 4*(Q-Z)
        assert 3*W*W >= Q-Z > 9*Z
        assert prime(p) and p%4 == 3 and 0 < rem < p*p and rem%p == 0
        for L in (1,3):
            for t in (W,s+j):
                x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
                S = x*x+y*y
                n = 5*Q+L*Z-S
                R = n-Q-(4-L)*Z
                assert Q < n < 5*Q and S > L*Z and n%24 == {1:21,3:3}[L]
                if t == W:
                    assert R == V*V+(W+s)**2
                else:
                    assert R > 0 and R%(p*p) == rem
        x,y = (Q-Z)//2,(Q+Z)//2
        u,z,Q,Z = x*u-3*y*z,x*z+y*u,Q**3,Z**3

g = list(map(F, ("18 178/9 182/9 22 70/3 74/3 26 82/3 30 290/9 34 110/3 "
                 "38 118/3 122/3 42 46 142/3 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == F(235,213)
print("PASS")
```
