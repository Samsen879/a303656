# Exact seventh-power layers and an infinite plus-layer veto

The seventh-power lift has an exact two-layer norm test. Its plus layer can fail even on an admissible base, and \(113\) forces that failure on an explicit infinite family. The test also excludes the first possible seventh-lift insertion in the \(178/9\) to \(22\) gap. No new ray is certified by these tests, so the largest phase ratio stays \(99/89\).

### Exact seventh-layer criterion

Let \(A=5^u>B=3^v\) with \(u,v\) positive and odd. Call the base admissible if \(A^2-B^2=a^2+3b^2\) for integers \(a,b\). At step \(j\ge1\), put \(C=A^{7^{j-1}}, D=B^{7^{j-1}}\) and
\[
M_j=\frac{C^7-D^7}{C-D},\qquad P_j=\frac{C^7+D^7}{C+D}.
\]
On an admissible base, \(A^{2\cdot7^h}-B^{2\cdot7^h}\) is admissible **if and only if**, at every \(1\le j\le h\),

- every odd-valuation prime of \(M_j\), except \(7\), lies in \(1,3,7,9\bmod20\);
- every odd-valuation prime of \(P_j\) lies in \(\{\pm1\}\bmod5\).

For a prime \(p\ne7\) in the two layers, the geometric sums give exact orders \(7^j\) and \(2\cdot7^j\) for \(A/B\bmod p\), respectively. Thus the layers have disjoint support away from \(7\), and their primes are fresh relative to \(A^2-B^2\). In the minus layer \(A/B\) is a square, giving \((15/p)=1\) and \((-3/p)=(-5/p)\). In the plus layer \(-A/B\) is a square, giving \((-15/p)=1\) and \((-3/p)=(5/p)\). The prime \(7\) splits in the Eisenstein field. The result follows from the even-valuation criterion at every inert prime. To pass from an Eisenstein norm to \(a^2+3b^2\), an odd-norm Eisenstein integer can be multiplied by a unit to become \(1\bmod2\). An even norm can first have its square power of \(2\) removed.

The polynomial identities explain the change from the fifth-power case:
\[
\begin{aligned}
M_j&=(C-D)^6+7CD(C^2-CD+D^2)^2,\\
P_j&=(C+D)^6-7CD(C^2+CD+D^2)^2.
\end{aligned}
\]
Expanding the second identity gives the alternating degree-six sum, and substituting \(-D\) gives the first. Here \(7CD=105\) times a square. The plus identity is a norm from the real quadratic field \(\mathbb Q(\sqrt{105})\). [Brent’s general Aurifeuilian identities](https://maths-people.anu.edu.au/brent/pub/pub135.html)

There is also a ratio-free kernel consequence. Always \(P_j\equiv7\bmod8\), and \(7\nmid P_j\) because \(A/B\) is a square modulo \(7\). If \(u+v\equiv0\bmod6\), then \(A\equiv B\bmod7\), \(v_7(M_j)=1\), and \(M_j/7\equiv7\bmod8\). Hence **every admissible step in this class adds a fresh odd-valuation prime from each layer**, each at least \(6\cdot7^j+1\). The actual base \((A,B)=(125,27)\) gives \(43\) and \(10039\) at the first step.

### Actual failure and the phase gap

For \((A,B)=(125,3)\), the base norm is \(112^2+3\cdot32^2\). Its seventh plus layer has \(v_{113}=1\). More generally, on an admissible base the conditions
\[
3u-v\equiv8\pmod{16},\qquad 3u+4v\not\equiv0\pmod{113}
\]
force a seventh plus-layer veto. Indeed, \(3\) has order \(112\) modulo \(113\), and \(5\equiv3^{83}\). The first condition gives \((A/B)^7=-1\bmod113\). Modulo \(113^2\), the coefficient of \(113\) in \((A/B)^{112}-1\) is \(110u-4v\). The second condition makes this nonzero. The order of \(A/B\bmod113\) cannot be \(2\), since that would put the odd valuation in the admissible base. Thus its order is \(14\), with the odd valuation in the new plus layer. Taking \((u,v)=(3^{k+1},3^k)\) gives admissible bases by repeated cubing, and the veto holds for every \(k\ge0\).

In the open phase gap, scale \(1\) contains no eligible lower exponent \(m\equiv2\bmod4\). Scale \(3\) leaves only \(m=62\), and an exact inert-prime check excludes every eligible \(e\) with \(3^e<5^{62}\). At scale \(9\), the only seventh-lift candidate has \(m=182=7\cdot26\). Its reduced base must itself be admissible because multiplying by \(7\) preserves the valuations at old inert primes. For \(m=26\), the only eligible reduced upper exponent is \(e=10\). Its seventh lift fails in the **minus** layer at \(197\), with valuation one. This leaves the non-seventh candidates at scale \(9\) and finer scales open. The existing seventeen-ray generated-population exponent stays \(89/198\) in both odd classes. This is a count of constructed targets.

### True positive and signed-only controls at the same height

The valid seventh lift \(5^{14}-3^{14}=23816^2+3\cdot42940^2\) supplies the controls. Write \(m=14\cdot3^k,\ Q=5^m,\ Z=3^m,\ s=3^{m/2}\), and start with \((v,w)=(47632,85880)\). At each cubing multiply \(v+w\sqrt{-3}\) by
\[
\frac{Q-Z}{2}+(-1)^{k+1}\frac{Q+Z}{2}\sqrt{-3}.
\]
This preserves \(v^2+3w^2=4(Q-Z)\), \(v,w\in4\mathbb Z\), and alternates \(w/v\bmod3\) between \(2\) and \(1\). It also keeps \(w>\sqrt Q/8\). The initial angle exceeds \(\pi/3\) by \(\arctan t_0\) with \(1/5<t_0<1/4\). The alternating shell angles have decreasing excesses \(\arctan(\sqrt3 Z/(2Q+Z))<1/100\). Thus \(w^2>3Z\) at every depth.

For \(\lambda=1,3\), set \(S=(w-s)^2+w^2\) or \(S=(w+s)^2+(w-2s)^2\), respectively. Then
\[
n=5Q+\lambda Z-S=Q+(4-\lambda)Z+v^2+(w+s)^2,\qquad Q<n<5Q .
\]
These give the classes \(21\) and \(3\bmod24\), with both positive exponents growing. At \(k=0\), the true targets are \(16142468445\) and \(16132902507\). Replacing \(w\) only in \(S\) by \(s+5\) gives signed witnesses at the same height and in the same classes, but the proposed positive residual is \(24399691673\equiv14\bmod49\) in both cases. That excludes the selected exponent pair. [Earlier sphere construction and per-height count](https://github.com/Samsen879/a303656/blob/837c80bde48f8b7df9da0daa1efb6a63e95a486b/analysis/ajt5_overnight_2026_11_26/EFFECTIVE_FIVE_RAY_SPHERE_POPULATION.md)

The following exact replay verifies the finite calculations.

```python
from fractions import Fraction
from math import isqrt

def layers(a, b):
    return (a**7-b**7)//(a-b), (a**7+b**7)//(a+b)

def vp(n, p):
    e = 0
    while n % p == 0:
        n //= p
        e += 1
    return e

assert layers(5, 3) == (43*883, 10039)
M, P = layers(125, 27)
assert vp(M, 7) == vp(M, 43) == vp(P, 10039) == 1
assert M//7 % 8 == 7
assert 125**2-3**2 == 112**2+3*32**2
assert vp(layers(125, 3)[1], 113) == 1
assert pow(3,56,113) == 112 and pow(3,16,113) != 1
assert pow(3,83,113) == 5
assert [pow(a,112,113**2) for a in (5,3)] == [1+110*113,1+4*113]

for m, E, ps in [
    (62, 90, [2,11,2,28493,2,17,11,23,2,17,2,11,2,83,953,353897,
              2,17,2,5477,2,11,15473]),
    (26, 38, [17,2,0,23,11,2,53,113,17,2]),
]:
    es = range(2, E+1, 4)
    assert len(ps) == len(es) and 3**E < 5**m < 3**(E+4)
    for e, p in zip(es, ps):
        N = 5**m-3**e
        if p:
            assert all(p%d for d in range(2,isqrt(p)+1))
            assert p%3 == 2 and vp(N,p)%2 == 1
        else:
            assert N == 1220699108**2+3*1808048**2
assert vp(layers(5**13,3**5)[0],197) == 1

g = list(map(Fraction, ("18 178/9 22 70/3 74/3 26 82/3 30 290/9 "
                        "34 110/3 38 42 46 142/3 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:])) == Fraction(99,89)

Q,Z,v,w = 5**14,3**14,47632,85880
for k,(j,p,h) in enumerate([(5,7,14),(13,23,92)]):
    s = isqrt(Z)
    assert s*s == Z and v*v+3*w*w == 4*(Q-Z)
    for L in (1,3):
        for t in (w,s+j):
            x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
            S = x*x+y*y
            n = 5*Q+L*Z-S
            R = n-Q-(4-L)*Z
            assert Q<n<5*Q and S>L*Z and n%24 == {1:21,3:3}[L]
            assert 2*L*Z-S == (t+s)**2-3*t*t
            if t == w:
                assert R == v*v+(t+s)**2
            else:
                assert R > 0 and p%4 == 3 and R%(p*p) == h
    a,b = (Q-Z)//2,(-1)**(k+1)*((Q+Z)//2)
    v,w,Q,Z = a*v-3*b*w,a*w+b*v,Q**3,Z**3
```
