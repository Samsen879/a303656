# A pointwise middle-band saving from the one-axis reciprocal-order moment

For the cubic panel of GROWING_CUBIC_PANEL.md, write $A_p$ for the smaller of the two orders of $9,25$ and $U_p$ for their product. Put $L=\log Y$ and $\eta=0.0153$. The primes in the residual band satisfying
$$
 A_p^3\le U_p L^{3/2+3\eta/4}
$$
have total worst-phase normalized occupied-block count $O(L^{-\eta/2})$. This is an asymptotic pointwise saving for this sublayer only.

Indeed [Pappalardi, Corollary 2.4](https://papparnta.github.io/pappa/papers/J_Num_Theory_57_1996.pdf#page=7), at rank one, gives $\sum_{Y<p\le2Y}1/\operatorname{ord}_p(a)\ll_a \sqrt{Y}/L^{1+\eta}$ for $a=3,5$. Squaring each base changes the order by at most a factor of two, and the reciprocal of the smaller order is at most the sum of the two reciprocals. Hence $\sum_p 1/A_p\ll\sqrt{Y}/L^{1+\eta}$. The singleton [Mit'kin estimate](https://arxiv.org/pdf/1302.3839#page=10) in the residual band gives normalized occupancy $O(U_p^{-2/3})$. Under the displayed restriction it is at most $O(L^{1+\eta/2}/A_p^2)$. Using $A_p\ge\sqrt{Y}/100$ and the reciprocal moment proves the saving. The bounded truncation factor and the extra one root per prime do not affect the conclusion. The range $U_p\asymp Y^\theta$ for fixed $\theta<3/2$ is not captured eventually by this condition.

A nonempty finite companion sublayer uses $Y=500000$, $A_p\le93$ and $Y\le U_p<2Y$, restricted to inert primes of the cubic panel. The actual prime $541447$ belongs (see MIXED_SUBGROUP_ENERGY_CONTROL.md). Every prime in the sublayer divides $\prod_{j=1}^{93}(9^j-1)(25^j-1)<225^{4371}<Y^{2000}$, so there are fewer than 2000. Its ordinary root proportion is at most $A_p/U_p\le93/Y$ because the roots are a partial matching. If both box lengths are at least $4Y$, the truncation penalty is at most $25/16$ since both orders are at most $(p-1)/2\le Y$. Therefore this finite sublayer covers strictly less than $2000(93/Y)(25/16)=93/160$ of that box at every phase. This concerns a sublayer of a finite divisibility panel, not odd-valuation or genuine-norm coverage.

```python
Y=500000
assert 225**4371<Y**2000
assert Y<=93*8733<2*Y and 93**3<93*8733
assert 2000*93*25*160==93*Y*16
```
