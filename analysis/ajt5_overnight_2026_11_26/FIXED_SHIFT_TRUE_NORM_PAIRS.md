# Two genuine coprime square sums in a fixed actual shift bucket

Use the ordinary window and the fixed-per-scale \(h=t-s=3^c(3^{24}-1)\) from [FIXED_NONZERO_SHIFT_BUCKET.md](FIXED_NONZERO_SHIFT_BUCKET.md). For each admissible common \(d\), there are \(\gg X/(\log X)^{15}\) distinct \(n\equiv319055\bmod480480\) with both \(n-s,n-t\in[X,3X/2)\) positive, coprime, composite sums of two squares. This is an elementary unweighted count, not a lower bound on the signed mixed moment. Summing over \(d\) counts pairs \((n,d)\).

## Count ordered square-coordinate pairs

Use \(a,w\in\mathbb Z^2\), with \(a\cdot w=h/4\). Set \(r_+=|w+a|^2,\ r_-=|w-a|^2\); then \(r_+-r_-=h\) and \(n=s+r_+=t+r_-\).

Choose a fixed modulus \(L\) with prime-power factors from \(480480\), \(29^2,37^2\), and the (fixed) set of prime divisors of \(h\). Impose \(r_+\equiv319055-s\bmod480480\), \(r_+\equiv29\bmod29^2\), \(r_-\equiv37\bmod37^2\), and make \(r_+,r_-\) both units at primes dividing \(h\). The imposed residues at \(3,5,7,13\) from the class mod \(480480\) are already units, by the exponent phases. At other primes dividing \(h\) choose the common residue to be 1 wherever it was not already prescribed.

These are compatible with a single residue class for \(a,w\), with \(a\) nonzero modulo each prime dividing \(L\). For the odd factors modulo a prime, write both specified residues as squares plus squares (the two sets of possible individual squares each have more than half the field elements available). When their residues differ the two representing vectors are necessarily distinct; when the common residue is nonzero choose opposite vectors. At \(29^2,37^2\), use the factorization \((x+iy)(x-iy)\) with a square root \(i\) of \(-1\) mod the prime square to represent each prescribed residue, and the vectors are distinct mod the prime because \(p\nmid h\). Taking half the sum and half the difference gives \(w,a\). At 32 both required residuals are 13, and one may take \(a=(5,0),\ w=(5^{-1}h/4,2)\bmod32\), using \(v_2(h)=5\). CRT gives the claimed class; in particular \(a\cdot w\equiv h/4\bmod L\).

Let \(\delta=1/(1000L)\). There are \(\gg_L X\) primitive \(a\) in that class with both coordinates in \([\delta\sqrt X,2\delta\sqrt X]\): the elementary Möbius count has positive density factor \(\prod_{p\nmid L}(1-1/p^2)\), with error \(O_L(\sqrt X\log X)\) by counting multiples on each coordinate. For each primitive \(a\), the exact equation \(a\cdot w=h/4\) has solutions in the specified \(w\) class by Bézout. Along their line, the parallel component has length \(h/(4|a|)=O_L(X^{-1/4})\), while the perpendicular component advances by \(L|a|<\sqrt X/24\). It can therefore be chosen in \([9\sqrt X/8,7\sqrt X/6]\). The norms of \(w\pm a\) are then in \([\sqrt X,\sqrt{3X/2})\) for all sufficiently large \(X\). Each ordered pair recovers \(a,w\), so there are \(\gg X\) ordered pairs of actual square-coordinate vectors. Any common prime of the two residuals would divide \(h\); those primes were all excluded. The forced 29 and 37 factors make the respective residuals composite for large \(X\).

## Remove representation multiplicity (elementary bound)

For \(m=r_+\), the number of ordered pairs over \(m\) is at most \(W(m)=r_2(m)r_2(m-h)\), where \(r_2\) counts signed ordered square-coordinate pairs. Cauchy–Schwarz and \(r_2(j)\le4\tau(j)\) give \(\sum W(m)^2\ll X(1+\log X)^{15}\). Indeed \(\tau(j)^4\le d_{16}(j)\): at each exponent \(e\), encode four integers in \([0,e]\) by recording how many levels \(1,\ldots,e\) have each of the 16 subsets of the four integers reaching that level. These counts recover the four integers and sum to \(e\). Also \(\sum_{j\le Y}d_{16}(j)\le Y(1+\log Y)^{15}\) by summing the first 15 factors harmonically. Applying Cauchy–Schwarz a second time to the \(\gg X\) ordered pairs gives the asserted distinct-n lower bound.

## Explicit control

```python
from math import gcd
X,c,d=2**329,26,50
s,t=3**c+5**d,3**(c+24)+5**d
h=t-s
assert h%24==0 and h==717897987689310722941920
u=(h//12+12)//2
v=u-12
z=36973391824248183962187094096698550182498006866275
r,R=z*z+u*u,z*z+v*v
n=s+r
assert n==t+R and n%480480==319055
assert X<=min(r,R) and 2*max(r,R)<3*X
assert gcd(r,R)==1 and r%29**2==29 and R%37**2==37
```
