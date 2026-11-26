# Phase-dependent repair palettes for incompatible reader slopes

**Two rays suffice on an actual incompatible \(3,5\) panel, with the choice depending on the shared label.** On \(3\to7\to\{32913511,9603931\}\), the palette \(\{0,2\}\) covers all three labels at one target. Ray 0 fails at label 0 and ray 2 fails at label 1, so the choice must switch within this palette. At a second target both rays fail at label 0, and ray 3 gives an exact even repair. [Pinned compatibility criterion](https://github.com/Samsen879/a303656/blob/d3eada75e94b8499598570f439c3267621e46398/analysis/ajt5_overnight_2026_11_26/SHORT_CHARACTER_DIRECTION_BOUND.md) · [Earlier actual reader orders](https://github.com/Samsen879/a303656/blob/a9560b603bc37767b1d6e9afd3c79445f000c2f5/analysis/ajt5_overnight_2026_11_26/JOINT_QUOTIENT_TWO_ALIGNED_SOURCES.md)

### Palette bound at a shared label

At label \(j\), write the first-digit repair line at \(p\) as \(g=\mu f+b_j\), where \(b_j\ne0\). The admissible finite rays \(\lambda\ne\mu\) give distinct digits \(f=b_j/(\lambda-\mu)\). For a shallow two-axis reader with nonzero observation \(N_r\), the hit equation along this line has the form
\[
A_jG^f+B_jK^f=N_r,
\]
where \(G,K\) both have order \(p\). Let \(\kappa_r\) bound the number of rays this reader can block at a fixed label.

Two hits at a prescribed nonzero difference in \(f\) determine both character values if the two multipliers differ. If the multipliers agree, a hit pair would force their common value to be 1, since \(N_r\ne0\). Hence ordered hit differences are distinct and \(\kappa_r(\kappa_r-1)\le p-1\) for the maximum hit count. A short relation between \(G\) and \(K\) can improve the bound by the character-polynomial degree. In particular, \(G=K\) gives \(\kappa_r=1\).

Put \(\kappa=\sum_r\kappa_r\). Every preselected palette with more than \(\kappa\) rays covers every retained label. A smaller palette can be chosen after the target is fixed. From a pool of \(P\) admissible rays, some \(k\)-ray palette has at most
\[
|S|\frac{\binom{\kappa}{k}}{\binom Pk}
\]
failed labels in \(S\), with \(\kappa\) capped at \(P\). This follows by counting pairs of a label and a palette entirely contained in that label’s bad-ray set. A bound below one covers all of \(S\). In particular, with \(P=p-1\), \(h<p\), and a fixed number of nonzero readers, **three adaptive rays suffice for all sufficiently large \(p\)** in this one-relay setup, even using the ordered-difference bound.

The gcd certificates give a direct selection rule. For each ray, project the reader gcd roots back to label sets and take their union \(C_\lambda\). The labels left uncertified by the palette lie in \(\bigcap_\lambda C_\lambda\). An implementation can test the first ray everywhere and restrict fallback checks to its certified candidate set. The argument requires the other retained conditions to be invariant under the ray choice or checked as part of the panel. A zero-observation reader with \(G=K\) needs its own test, since it can block an entire phase.

### Actual two-ray switch

The homogeneous ray at \(7\) is 1, and both readers have the same two order-7 generators, giving \(\kappa_r=1\) for each. The first reader’s direct phase moves only on the \(3\)-axis, so a relation of height at most 2 requires ray 0. At the second reader the direct ratio is 2. Ray 0 admits no relation of height at most 2 there, while ray 2 admits \((2,-1)\).

At the first target, the four relaxed gcd cells have exactly the following true hit labels.

| Ray | \(32913511\) | \(9603931\) |
|---:|---:|---:|
| 0 | \(\{0\}\) | ∅ |
| 2 | ∅ | \(\{1\}\) |

Choose ray 2 at label 0 and ray 0 at labels 1 and 2. The second target puts both odd-valuation hits at label 0. This also explains sharpness for **preselected** palettes required to cover every label uniformly over targets on this graph. Any two preselected rays can be blocked at label 0 by assigning one nonzero observation to each reader through CRT. Three preselected rays always suffice under the two pointwise caps.

### Runnable replay

```python
from math import isqrt, lcm, prod
from sympy import Poly, symbols

h,p,R = 3,7,(32913511,9603931)
H = lcm(p*p*(p-1),*(r*(r-1) for r in R))
def step(m):
    b = H//m
    return b*pow(b,-1,m)

J,U,C,D = step(h),step(p*p),3*p*prod(R),H
assert all(r%4==3 and all(r%d for d in range(2,isqrt(r)+1)) for r in (p,*R))
assert pow(3,J,p*p)==pow(5,2*J,p*p)
assert (pow(3,C,p*p)+pow(5,D,p*p))%(p*p)==0
assert pow(3,U,p)==pow(5,U,p)==1 and J%2==U%2==0
a,b = ((pow(v,U,p*p)-1)//p*pow(v,e,p)%p for v,e in ((3,C),(5,D)))
assert (a,b,pow(3,-J,p))==(6,1,2)

def exponents(j,ray):
    f=pow((a+ray*b)%p,-1,p)*pow(2,j,p)%p
    return C+J*j+U*f,D+2*J*j+ray*U*f

def rem(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

def target(labels):
    pairs=[(5,12),(p,p*p)]
    for r,ray,j in zip(R,(0,2),labels):
        c,d=exponents(j,ray)
        pairs.append(((pow(3,c,r*r)+pow(5,d,r*r)+r)%(r*r),r*r))
    M=prod(q for _,q in pairs)
    return sum(v*(M//q)*pow(M//q,-1,q) for v,q in pairs)%M

x=symbols("x")
n=target((0,1))
assert n==56794955108785268897951156173313
for i,r in enumerate(R):
    assert (r-1)%(h*p)==0 and p*U%(r*(r-1))==0
    A,B,alpha,beta,G = pow(3,C,r),pow(5,D,r),pow(3,J,r),pow(5,2*J,r),pow(3,U,r)
    assert alpha!=1 and pow(alpha,h,r)==1 and beta==pow(alpha,2*i,r)
    assert G!=1 and pow(G,p,r)==1 and G==pow(5,U,r) and n%r
    for ray in (0,2):
        k=ray+p*((2*i-ray)%h)
        poly=lambda f: Poly(f,x,modulus=r)
        g=poly(x**(h*p)-1).gcd(poly(A*x+B*x**k-n%r))
        root={(0,0):20344933,(1,2):3966388}.get((i,ray))
        assert g==poly(1 if root is None else x-root)
        if root is not None:
            assert pow(root,p,r)==pow(alpha,i,r)
            c,d=exponents(i,ray)
            assert pow(3,c,r)==A*root%r and rem(n,c,d,r*r)==r

def good(n,j,ray):
    c,d=exponents(j,ray)
    if rem(n,c,d,p**3)==0:
        c+=p*U
    assert rem(n,c,d,p**3) in range(p*p,p**3,p*p)
    assert rem(n,c,d,3)==rem(n,c,d,4)==1
    assert all(rem(n,c,d,r) for r in R)

for j,ray in ((0,2),(1,0),(2,0)):
    good(n,j,ray)

n2=target((0,0))
assert n2==47309108046762083560549487339237 and all(n2%r for r in R)
assert all(rem(n2,*exponents(0,ray),r*r)==r for ray,r in zip((0,2),R))
good(n2,0,3)
# At the fixed label 0 both readers have nonzero values on every admissible ray.
for r in R:
    assert all((pow(3,exponents(0,ray)[0],r)+pow(5,exponents(0,ray)[1],r))%r
               for ray in range(p) if ray!=1)
print("OK")
```

A single sufficiently large lift of each target by a multiple of \(12p^3\prod_r r^2\) makes all tested remainders positive while preserving the exact valuations. The certificates establish simultaneous repair for this finite panel. A square-sum witness still requires controlling the other inert primes.

For the ordered-difference bound, fix a difference of two labels in the repair digit. The two hit equations are linear in the two character values at the first digit. Distinct multipliers give a unique solution, and equal multipliers would have to equal 1 since the observation is nonzero. A nonzero difference cannot give multiplier 1 for either character of order p. A single character value then identifies the first digit. In the fixed-reader regime, the bad-ray count is O(sqrt(p)); the three-ray averaging failure bound is O(h/p^(3/2)), which is less than one for sufficiently large p. It applies to the stated graph and retained conditions, not an existence result for arbitrary reader graphs.
