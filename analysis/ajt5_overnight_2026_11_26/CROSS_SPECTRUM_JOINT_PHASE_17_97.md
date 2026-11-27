# Common exponent phases correlate the mod-17 and mod-97 factors

Use the actual cross-spectrum grid of [the mod-11 obstruction](CROSS_SPECTRUM_INERT_ROOT_PHASE_OBSTRUCTION.md), with fixed target classes \(n\equiv527\bmod672,\ n\equiv35\bmod65,\ n\equiv0\bmod11\). Keep \(c_+,d_+\equiv(26,50)\) and \(c_-,d_-\equiv(50,50)\pmod{120}\) on their respective spectra. Fix \(y\ge17\) and exclude any residual with a factor of 97; this additional fixed omission preserves the fixed-modulus first moment, by restricting the small factors and placing the large prime in a unit class. Both spectra now contain only residues that are units at 17 and 97.

The base-3 and base-5 free orders at 17 are \((2,2)\); at 97 they are \((2,4)\). Hence a single index pair \(i\bmod2,j\bmod4\) determines the offsets on both moduli, and identities must use these shared indices. In the 64 pairs of actual phases, the cases \((17\mid h,97\mid h)=(0,0),(0,1),(1,0),(1,1)\), \(h=s_--s_+\), occur \(40,0,16,8\) times. In particular a collision at \(97\) always accompanies a collision at \(17\). Yet each fine target residue admits at least three of the eight phases on each side (the maximum removals are four and one), so this is not an example with a whole forbidden fine class.

With \(Z_\pm\) the actual hit counts and \(\mu_\pm\) their coarse means, fixed-modulus PNT gives conditional multiplication by \(\ell/(\ell-1)\) on a noncollision class for each \(\ell=17,97\), with zero on a collision class. The average product for a fixed pair of phases therefore contributes \(F_\ell(h)=\ell(\ell-2+1_{\{\ell\mid h\}})/(\ell-1)^2\). Averaging those products over the same index pairs yields
\[
 \mathbb E[\mathbb E(Z_+\mid U)\mathbb E(Z_-\mid U)]/(\mu_+\mu_-)
 = \frac{19294949}{18874368}+o_y(1),\qquad U=n\bmod(17\cdot97).
\]
Multiplying the separately averaged factors would give \(51450449/50331648\), smaller by \(8245/150994944\). Consequently a model using the latter to predict the actual normalized mixed moment would need a nonzero compensating conditional covariance at this scale. This is a statement about conditional first moments and shared exponent phases, not a calculation of the true mixed moment or a lower bound for simultaneous true hits.

```python
from fractions import Fraction
from itertools import product
M=17*97
def phases(c):
    return [(pow(3,c+120*i,M)+pow(5,50+120*j,M))%M
            for i,j in product(range(2),range(4))]
A,B=phases(26),phases(50)
pairs=[(int((v-u)%17==0),int((v-u)%97==0)) for u,v in product(A,B)]
assert [pairs.count(t) for t in product(range(2),repeat=2)]==[40,0,16,8]
assert all(sum((t-r)%17!=0 and (t-r)%97!=0 for t in S)>=3
           for S in [A,B] for r in range(M))
def F(p,h):
    return Fraction(p*(p-2+h),(p-1)**2)
joint=sum(F(17,a)*F(97,b) for a,b in pairs)/64
separate=(sum(F(17,a) for a,b in pairs)*sum(F(97,b) for a,b in pairs))/64**2
assert (joint,separate,joint-separate)==(
    Fraction(19294949,18874368),Fraction(51450449,50331648),Fraction(8245,150994944))
```
