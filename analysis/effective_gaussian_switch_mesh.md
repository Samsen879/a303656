# Explicit effective mesh for the actual Gaussian switch angles

The actual \(13,17,37\) Gaussian switch box has an **unconditional effective angular mesh of order \(K^{-1/89000}\)** when its three exponent ranges grow linearly in \(K\). The bound comes from the 13 and 17 axes jointly. It also gives a congruence-preserving rotation at a fixed target, provided the Gaussian endpoints already exist and the requested arc is wide enough. The critical \(t=8\) mesh of order \(K^{-2}\) remains open asymptotically. At \(K=703\), the exact 990-phase box covers every quarter-turn interval of length \(1/300\), while an exact resonance defeats uniform coverage at the physical critical width.

### Effective bound for the actual angles

Let \(z=(2+3i,1+4i,1+6i)\) and \(\beta_j=(2/\pi)\arg(z_j/\bar z_j)\pmod 1\). Write \(\|x\|\) for distance to the nearest integer. Put \(C=89000\) and \(L(H)=\max(e^{1000},40H)\). For every integer \(h\ge1\),
\[
\max\bigl(\|h\beta_{13}\|,\|h\beta_{17}\|\bigr)>L(h)^{-C}. \tag{1}
\]

To prove (1), take \(\alpha_1=(12+5i)/13\) and \(\alpha_2=(15+8i)/17\), with positive arguments \(\theta_1,\theta_2\). Their normalized arguments agree with the first two switch angles up to sign and an integer. Their valuations at the Gaussian primes above 13 and 17 prove multiplicative independence. For \(h\ge2\), let \(m_j\) be the nearest integer to \(2h\theta_j/\pi\). Both \(m_j\) are positive since \(\theta_j>\pi/8\). The two approximations share the same \(h\), which cancels:
\[
|m_2\log\alpha_1-m_1\log\alpha_2|
\le(\theta_1+\theta_2)\max_j\|2h\theta_j/\pi\|
<\max_j\|2h\theta_j/\pi\|.
\]
In Gouillon’s Corollary 2.2 the degree parameter is \(2/2=1\). The absolute logarithmic heights are \(\tfrac12\log13,\tfrac12\log17\), so the permissible height cutoffs are \(a_1=1.283,\ a_2=1.417\). The coefficient parameter satisfies \(b\le (1/a_1+1/a_2)h<3h/2\). The coefficient of \(\max(1000,\log b+3.1)\) in the exponent is \(9400(3.317+1.888)a_1a_2<89000\), and \(\log b+3.1<\log(40h)\). For \(h=1\), the first axis alone gives \(\|\beta_{13}\|\ge (2/\pi)(5/13)>5/26\). [Gouillon, Corollary 2.2](https://www.numdam.org/item/JTNB_2006__18_1_125_0.pdf#page=5)

For integer ranges \(0\le j_i\le e_i\), put \(E=\min e_i\). **Every open interval of normalized length \(5/H\)** contains a phase \(\sum j_i\beta_i\) if \(H\ge6\) and \(E\ge5L(H)^C\). Indeed, scale the lattice \((m+\sum j_i\beta_i,j_1,j_2,j_3)\) by \((2/w,2/e_1,2/e_2,2/e_3)\), with \(w=5/H\). The squared length of the shortest dual vector with first index \(h\ne0\) is
\[
\tfrac14\left((wh)^2+\sum_i e_i^2\|h\beta_i\|^2\right).
\]
For \(|h|\ge H\) the first term inside parentheses is at least 25. For \(0<|h|<H\), (1) makes one of the other terms greater than 25. A nonzero dual vector with \(h=0\) has length at least \(E/2\). Banaszczyk’s covering-radius bound therefore gives radius less than 1. Centering at \(j_i=e_i/2\) gives the stated integer box and open interval. In particular, for \(E\ge5e^{1000C}\) the same proof gives the explicit width \(200(5/E)^{1/C}\). [Banaszczyk, *New bounds in some transference theorems in the geometry of numbers*](https://doi.org/10.1007/BF01445125)

**Fixed-target consequence.** Suppose an actual endpoint has the Gaussian factors \(z_i^{j_i}\bar z_i^{e_i-j_i}\) and a fixed integral Gaussian cofactor. To preserve its coordinates modulo \(m\), with \(\gcd(m,13\cdot17\cdot37)=1\), fix each \(j_i\bmod M\), where \(M\) is a common multiple of the orders of \(z_i/\bar z_i\) in \((\mathbb Z[i]/m)^\times\). If each resulting progression has at least \(F+1\) positions and \(F\ge20L(MH)^C\), the rotations hit every arc of length \(5/H\) **in full-turn units**, with the same coordinates modulo \(m\). For full-turn angles \(\gamma_i\), the one change in the proof is \(\|hM\gamma_i\|\ge\|hM\beta_i\|/4\). The norm, target and other endpoint stay fixed. This preserves parity and any previously verified coprimality tests modulo \(m\). Residual norm existence, coprimality at primes outside \(m\), and the physical critical angle still require their own checks.

### What the critical scale requires

A uniform \(O(E^{-2})\) one-arc mesh for boxes with all three sides comparable to \(E\) is equivalent, up to constants, to
\[
\inf_{h\ge1}\sqrt h\,\max_{i=1,2,3}\|h\beta_i\|>0.
\]
For necessity, multiplication by \(h\) puts the phase set in an arc of length at most \(\sum_i e_i\|h\beta_i\|\). A mesh of width \(w\) requires \(hw+\sum_i e_i\|h\beta_i\|\ge1\). Take \(E\) a sufficiently large constant times \(\sqrt h\). Sufficiency follows from the same dual-vector test by splitting at \(|h|=5/w\). The logarithmic-form estimate (1) supplies a much weaker exponent.

The finite check below gives both sides of the \(K=703\) calibration. The largest gap has tangent exactly \(993240/190300729\). For the actual labels \(A=9^7,B=25^7\), the first shift is \(27A+5B\) and \(D=9A+2B\). In the \(t=8\) band, each signed critical arc has normalized width below \(1/(8K^2)\). Indeed, \(D<q\) throughout the band and the angular derivative of \(q=S+D-\sqrt{S(S+2D)}\cos\theta\) has magnitude at least \(\sqrt{qS}\). At \(h=58381\), the image of the phase set and either critical arc have combined length below \(3/20\). Even two such arcs cannot cover every residual phase. The native same-target fixture is verified separately in [#69](https://github.com/Samsen879/a303656/pull/69). Its original phase hits at \((7,2,1)\), and the three second-label seeds survive.

```python
from fractions import Fraction as F
from itertools import product
from math import factorial

def mul(z,w):
    x,y=z
    u,v=w
    return x*u-y*v,x*v+y*u

def gp(z,k):
    a=(1,0)
    while k:
        if k&1: a=mul(a,z)
        z=mul(z,z)
        k//=2
    return a

def quarter(z):
    x,y=z
    while x<=0 or y<0: x,y=-y,x
    return x,y

for a,p in [(F(1283,500),13),(F(1417,500),17)]:
    assert sum(a**k/factorial(k) for k in range(14))>p
assert 9400*F(5205,1000)*F(1283,1000)*F(1417,1000)<89000

z=((2,3),(1,4),(1,6))
powers=[[gp(mul(a,a),j) for j in range(e+1)]
        for a,e in zip(z,(10,9,8))]
rays=sorted((quarter(mul(mul(a,b),c)) for a,b,c in product(*powers)),
            key=lambda a:F(a[1],a[0]))
gaps=[F(x*v-y*u,x*u+y*v)
      for (x,y),(u,v) in zip(rays,rays[1:]+[(0,1)])]
G=max(gaps)
assert len(gaps)==990 and min(gaps)>0
assert G==F(993240,190300729) and 300*100*G<157  # pi > 3.14

h,K=58381,703
assert 64*K*(K+1)*(9*9**7+2*25**7)<2**K
for a,r in zip(z,(6,3,6)):
    lo,hi=sorted(map(abs,gp(a,2*h)))
    assert 1000*lo<r*hi
assert F(h,8*K*K)+F(135,1000)<F(3,20)
print("verified",len(rays),G,h)
```

The replay prints `verified 990 993240/190300729 58381`. The finite resonance concerns uniform angular coverage. The actual successful allocation shows why that obstruction does not decide a prescribed target.