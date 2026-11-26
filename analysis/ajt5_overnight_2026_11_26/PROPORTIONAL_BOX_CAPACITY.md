# The proportional active box requires cross-row prime sharing

At n in [X,2X), a fixed 1/4 power box contains Θ(L²) common cells for L=log X, with c≤C=floor(log_3(X/4)), d≤D=floor(log_5(X/4)). Assigning a distinct prime to every cell requires log product(p)≥log((C+1)(D+1))!=Omega(L² log L). This alone does not give a lower bound on the least representative of a particular reduced class. In the explicit finite-rectangle generator whose coordinates are chosen past M, the two high roots themselves become true witnesses with both powers below n/4, so the finite-rectangle result cannot prove proportional failure by that generator.

For any one c, each prime p can hit at most one phase of d modulo ord_p(5), with 5^ord≥p+1. If each prime serves at most r rows, splitting at Y gives the first-power capacity
```
(C+1)(D+1) <= r * [Y*(D+1) + (W/log Y)*(1+D*log(5)/log Y)]
```
where W=log product(p). This uses Y as a crude upper bound on the number of small primes and W/log Y on the number of large ones. Choose Y=sqrt(L). For r=1, W must be Omega(L(log L)^2); for W=O(L), r needs to be at least order (log L)^2. The same argument applies to column-sharing. More generally with W=O(L), primes larger than exp(L^(1/2+eps)) have total capacity o(L²) even without any row-sharing limit: there are at most O(L^(1/2−eps)) such primes, each can hit at most 1+O(L^(1/2−eps)) indices per row, and there are O(L) rows.

This deliberately counts mere divisibility. At n=85 in the 3×2 box, inert divisors of the listed six cells in row-major order may be chosen as 83,79,3,7,3,71. All six divide, yet 85−3−1=81 is a true norm and has v3=4. Thus the bound is a necessary condition on a proposed odd-valuation cover, not such a cover itself, or a theorem for arbitrary proportional boxes.
