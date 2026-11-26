# A conditional joint-index window and the missing mixed moment

In the cubic band let $R,S$ be the orders of $9,25$ modulo $p$, $U=RS$, and $I_9=(p-1)/R$, $I_{25}=(p-1)/S$. On $Y<p\le2Y$ the sufficient bound $\sum U^{-2/3}=o(1)$ over a residual panel is equivalent to $\sum (I_9I_{25})^{2/3}=o(Y^{4/3})$, since $UI_9I_{25}=(p-1)^2$. For each fixed-product layer $U\asymp Y^\theta$, the desired condition is $o(Y^{2\theta/3})$ primes, but bounds across many layers also need uniform summation. This is a sufficient condition for a weak-occupancy bound from Mit'kin, not a necessary condition for absence of a cover.

Here is one window that can be controlled **assuming GRH for the Dedekind zeta functions of the stated Kummer fields**. Put $Z=Y^{1/6}/(\log Y)^{2/3}$. Restrict the residual panel to primes $p$ at which some prime $q\in[Z,2Z]$ divides both $I_9$ and $I_{25}$. This restriction has $\sum U^{-2/3}=O((\log Y)^{-2/3})$.

Indeed, for $q>5$ outside the ramification set, the two index requirements mean $p\equiv1\bmod q$ and both bases are $q$th powers modulo $p$. This is complete splitting in $K_q=\mathbb Q(\zeta_q,9^{1/q},25^{1/q})$. Kummer independence follows from valuations at primes over 3 and 5, which are unramified in the cyclotomic base and detect the two exponents separately modulo $q$. Thus $[K_q:\mathbb Q]=q^2(q-1)$. Its normalized log discriminant is $O(\log q)$ by [Sgobba, Proposition 13](https://arxiv.org/html/2006.05417v2#S3.SS2). The GRH complete-splitting estimate (equivalently the prime ideal count divided by the degree, with higher residue degrees discarded for this upper bound) gives
$$
 O\!\left(Y/(q^3\log Y)+\sqrt Y\log Y\right)
$$
primes in $(Y,2Y]$ per $q$ in this window. See the effective counting input in [Sgobba, section 4](https://arxiv.org/html/2006.05417v2#S4). Summing over $O(Z/\log Z)$ primes gives $O(Y^{2/3}/(\log Y)^{2/3})$ primes. On the original residual band $U\ge Y/10^4$, so the weighted estimate follows. The exact joint density per fixed $q$ is $1/(q^2(q-1))$, which is $q-1$ times the product of the marginal densities: ignoring the common cyclotomic condition would give the wrong answer.

The bound does not address two large but differently factored indices with no shared prime in this window. It neither proves the residual mixed moment without GRH nor covers the whole panel under GRH, and gives no conclusion about actual square-sum representations.
