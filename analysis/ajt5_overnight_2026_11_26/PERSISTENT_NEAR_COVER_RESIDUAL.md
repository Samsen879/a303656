# Near-full coverage can preserve fixed active rows

For C=10941 or 10937 and j=0,…,4, put B=5(9^j−C), which is negative. Let K be the lcm of 60060 and all ten 4|B|. Choose auxiliary primes only in q≡−1 mod K. Then q≡7 mod 8, so (−1/q)=−1 and (2/q)=1. For every odd prime ell dividing |B|, q≡−1 mod ell and q≡3 mod 4, so quadratic reciprocity gives (ell/q)=1. Thus B is a nonsquare modulo q, and no work residue p can satisfy (5p)²≡B there. Neither column at t=j can be paid by an auxiliary prime, although these ten rows are always strictly active. For finite panel Q the five common survivor classes modulo D=lcm ord_q(9) have relative density min(5,D)/D. The nonsmooth near-cover construction still works in this narrower reduced progression, so there is no inherent contradiction between arbitrarily high density of coverage and these fixed exceptional indices.

For a fixed surviving phase t≡b mod D, one may also add a finite group of ordinary primes q>3 not dividing D and still retain positive periodic density. Process the added primes in increasing order, preassigning all required exponent coordinates not belonging to the added group. At each q, its order uses only smaller primes. The current q-digit is free, and the columns differ by 4, so only one can contact q. If h=v_q(M)=2, keeping the one extension that is zero mod q² avoids locking an odd valuation. If h≥3, keep the fraction (q−1)/q² giving valuation exactly 2. In either case the relative loss is bounded by a factor q^(−h/2) from below. In particular the absolute surviving density is at least D^(-1) times the product of those factors. For a fixed actual p instead require exact even valuations by using two available digits at every contacted q. This is a statement about such allowed appendages, not arbitrary shared primes or actual success as a norm.

```python
from math import lcm

C = (10941, 10937)
B = [5*(9**j-c) for c in C for j in range(5)]
assert max(B) < 0
assert lcm(60060, *(4*abs(b) for b in B)) == 86016394928554255140088713600

# q=47 普通，但 t=0 mod 1081 固定了它所需的指数数位。
assert pow(9, 23, 47**2) != 1 and pow(9, 1081, 47**2) == 1
assert (5*31**2 + C[0] - 1) % 47**2 == 6*47

# q=11 不整除种子周期 5，但在 t=4 mod 5 冻结奇赋值。
assert pow(9, 5, 11**2) == 1
assert (5*31**2 + C[0] - 9**4) % 11**2 == 10*11

assert 5*7**2  + C[0] - 1 == 24**2 + 103**2
assert 5*31**2 + C[0] - 1 == 5*47*67
```
