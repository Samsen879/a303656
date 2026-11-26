# Unweighted simultaneous column growth with first root 248

**Scope.** For every sufficiently large $X$, in the fixed class of FIRST_248_PRIMITIVE_SIEVE_SEED.md, at least $\gg_M X/\sqrt{\log X}$ integers $m\in[X,2X)$ have $248$ as the first admissible numerical root at $x=5m+4$ and at least $c_M\sqrt{\log X}$ distinct indices $d$ in the fixed progression $d=4+kP$ such that both $m-5^d-1$ and $x-5^{d+1}-9$ are positive sums of squares. The count is a positive proportion of the first-root-248 points in this class, not a positive proportion of the entire class. Constants and starting scales are not evaluated. This is an unconditional statement for the specified class, not an all-integer result or an argument for the original conjecture.

## Lower first moment

Write $Y=\sqrt X$, $\ell_0=100M$, and take shifts $H_d=5^{d+1}-239$ with $5^{d+1}\le Y$. Use the fixed vector residues from the seed and the integer relation $(a,b)\cdot(u,v)=H_d$, $\gcd(a,b)=1$. The recovered difference and sum give the two representations as in the seed note. Restrict $a,b$ to $[\gamma Y,1.01\gamma Y)$, with fixed $\gamma=1/(5000M)$, and $u\in[3.6Y,3.7Y)$, with $v=(H_d-au)/b$. For large $Y$ the coordinates of $V=((u,v)-(a,b))/2$ in absolute value lie between $7Y/4$ and $2Y$, which puts $m$ strictly in $[X,2X)$. All norms are positive. This also fixes $v_5(\|V\|^2)=2$ and $v_5(\|S\|^2)=0$ by the seed residues.

For one compatible primitive residue vector modulo $\ell$, where $\ell_0\mid\ell$, the count is
$$
 \frac{|I_a||I_u|\log(101/100)}{\ell^3}\prod_{p\nmid\ell}(1-p^{-2})
 +O_{M,\epsilon}(Y^{3/2+\epsilon}\ell^2). \tag{1}
$$
Here is the uniform estimate used in (1). Fix $b\equiv b_0\bmod\ell$ and write $a=a_0+\ell t$, $u=u_0+\ell j$, $v=v_0+\ell k$. For $\gcd(a,b)=1$, the condition is $j\equiv (K-u_0t)/a\bmod b$ with $K=(H_d-a_0u_0-bv_0)/\ell$. Complete the interval sums in $t,j$ modulo $b$. The zero frequency gives the product of interval lengths in these variables divided by $b$, multiplied by $\prod_{p\mid b,\ p\nmid\ell}(1-1/p)$. If $p\mid(b,\ell)$ the fixed residue $a_0$ is a unit, so it contributes no such factor. Expand the product by Möbius inversion and sum $1/b$ in the resulting progressions; the main term is the one displayed and endpoint errors are absorbed by the stated error.

For nonzero frequencies write $b=b_1b_2$, where $b_1$ contains the prime powers supported on $\ell$ and $(b_2,\ell)=1$. Use the trivial bound on the $b_1$ part. On $b_2$ substitute $a=a_0+\ell t$ to obtain a Kloosterman sum with coefficients equal to unit multiples of the two Fourier frequencies $r,sH_d$. The usual [Weil–Estermann bound](https://epubs.siam.org/doi/full/10.1137/25M1794905) bounds the full completed sum by
$$
 b^{1/2} b_1^{1/2}\tau(b_2)(H_d,b_2)^{1/2}(r,s,b_2)^{1/2}.
$$
For a divisor $q$ of $b_2$, the sum of normalized absolute interval coefficients over nonzero frequencies divisible by $q$ is $O_M(\log(2b)/q)$, by the geometric-sum bound; the zero coefficient is $O_M(1)$. Expanding the greatest-common-divisor weight over such divisors and omitting the double zero bounds the total frequency factor by $O_M(\tau(b_2)\log^2(2b))$. Finally expand $b_1^{1/2}$ over $c\mid b$ supported on $\ell$ and $(H_d,b_2)^{1/2}$ over $j\mid(b,H_d)$ coprime to $\ell$. The number of $b$ terms divisible by $cj$ is $O_M(Y/(cj))$. The resulting factor is at most
$$
 O_M\!\left(Y\prod_{p\mid\ell}(1-p^{-1/2})^{-1}\sum_{j\mid H_d}j^{-1/2}\right)
 \ll_{M,\epsilon}Y^{1+\epsilon}\ell^2.
$$
This proves (1), uniformly for $0<H_d\le Y$, without assuming $(b,H_d)=1$.

Use one Gaussian orientation on each side, with deletion density $(2+1_{p\mid H_d})/(p+1)$ as proved in FIRST_248_TWO_SIDED_ORIENTATION.md. For a squarefree sieve modulus $q$, sum (1) over at most $q^3$ residue vectors at $\ell=\ell_0q$. The error is $O(Y^{3/2+\epsilon}q^5)$, summable to $o(X/\log X)$ at level $D=Y^{1/100}$ with $\epsilon=1/100$. Sieve to $z=D^{1/s}$, with $s$ fixed sufficiently large. The uniform dimension-three product condition follows from $(1-g(p))^{-1}\le(1-1/p)^{-3}$ at the split primes $p\ge13$ (the prime 5 is omitted). The [fundamental lemma](https://ford126.web.illinois.edu/sieve2023.pdf#page=38) gives a fixed multiple of the local product minus the summed error. For a positive proportion of the shifts, the bounded divisor average in the two-sided orientation note gives $\sum_{p\mid H_d}1/p=O_M(1)$. For these shifts the product is $\asymp_M (\log z)^{-1}$, by Mertens for split primes. Hence at least $\gg_M X/\log X$ representation pairs survive per such shift.

The number of surviving vectors on each side for each fixed norm is bounded independently of $X$: at small split primes all exponents must use the one permitted orientation; at 5 its valuation was frozen; the total multiplicity of split primes above $z$ is at most $\log(O(X))/\log z=O(1)$. Inert and ramified primes contribute no choices, and the four units are harmless. So at least $\gg_M X/\log X$ distinct $m$ are obtained per good shift.

## Uniform upper moments and the relative proportion

Let $B_2(n)$ be the indicator of a positive sum of squares and put $n=5m-244$. The progression in $m$ is $m_*\pmod{4M}$ with $m_*=5150158917+3M$; write $n_*=5m_*-244$. The exact contents of the three lines $n,n-H_d,n-H_e$ in the progression parameter are $2,20,20$ respectively. Indeed $n_*\equiv6\bmod20$, the shifts are $6\bmod20$, and
$$
 \gcd(M,10(25750794589-248)(25750794589-3134))=1
$$
using the exact seed constants and $5^P\equiv1\bmod M$. Removing the contents preserves $B_2$, since 2 and 5 do not impose odd-valuation obstructions. The three primitive affine forms have respective slopes $10M,M,M$ and pairwise resultants of absolute values $MH_d/2$, $MH_e/2$, and $M|H_d-H_e|/20$. In particular the bad primes apart from $10M$ divide $H_dH_e(H_d-H_e)$.

Apply [Henriot's corrected Theorem 5](https://doi.org/10.1017/S0305004114000280) to the product of (up to) three $B_2$ weights. This nonnegative multiplicative function is at most one, and satisfies the theorem's submultiplicativity condition including zeros. Distinct shifts give distinct primitive irreducible linear factors; the coefficient norm of their product is $O_M(X^{3/2})$. The counting interval for the progression variable has position and length $\asymp_M X$, so $\alpha=\delta=1/2$ and $\epsilon=1/2000$ meet the size and exponent conditions for all three slots. At the ordinary primes the roots are distinct. For $k$ slots the ordinary local factor is $1+O(p^{-2})$ on split primes, and $1-k/p+O(p^{-2})$ on inert primes. Indeed there is only one positive slot at a time; at split primes that slot contributes $1/p$, while on inert primes the positive even exponents contribute $1/[p(p+1)]$. For a bad prime $p\ge5$, an exponent vector of maximum $j>0$ has density at most $p^{-j}$ by a primitive linear factor at a slot attaining the maximum. The corrected zero-slot conditions can only lower this. Summing $(j+1)^k-j^k$ such bounds makes the local factor at most $1+13/p$; comparison with the ordinary factor, at least $1-k/p$, costs at most $e^{40/p}$. Fixed primes are absorbed into the constant. Thus the $k$-slot sum is at most $O_M(X/(\log X)^{k/2})$ times this exponential bad-prime weight.

Put $T_X(m)=B_2(n)\sum_d B_2(n-H_d)$. The lower first moment above, two-slot upper bound, three-slot upper bound and bounded bad-factor averages give
$$
 \#\{B_2(n)=1\}\ll_M X/\sqrt{\log X},\quad
 \sum_m T_X(m)\asymp_M X,\quad
 \sum_m T_X(m)^2\ll_M X\sqrt{\log X}.
$$
The diagonal of the second moment uses the two-slot bound, and its off-diagonal uses the three-slot bound. Below a sufficiently small fixed multiple of $\sqrt{\log X}$, the contribution to the first moment is at most half its lower bound by the first displayed count. Cauchy–Schwarz on the remaining points proves the stated $\gg_M X/\sqrt{\log X}$ lower count. The prime valuations from the seed ensure that every one of these points has first root 248, not merely that 248 is a root.
