# An actual product-norm certificate reduces to shift-difference gcds

Fix one integer \(n\) and distinct ordinary shifts \(h_i=3^{c_i}+5^{d_i}\) with positive residuals \(R_i=n-h_i\). Suppose the actual integer product \(P=\prod_iR_i\) has a two-square certificate. Then, exactly,
\[
 R_i\text{ is a two-square norm}\quad\Longleftrightarrow\quad
 \gcd\left(R_i,\prod_{j\ne i}(h_i-h_j)\right)\text{ is a two-square norm}.
\]
For an inert prime \(p\equiv3\bmod4\), the \(p\)-adic exponents of \(R_i\) and \(P/R_i\) have the same parity, since their sum is even. Their minimum has this same parity. This proves the equivalence using the ordinary two-square criterion. The gcd equality holds because \(R_j\equiv h_i-h_j\bmod R_i\). Thus only inert primes in actual differences of shifts need checking once an actual product certificate has been supplied.

## A sharp two-row gap

Suppose that in addition both residuals have odd part \(1\bmod4\), and \(v_3(R_1),v_3(R_2)\) are even. If \(0<|h_1-h_2|<154\), both residuals are norms. In fact the product certificate gives identical odd-valuation inert prime sets for the two rows. If nonempty that set has even cardinality (the odd-part test) and omits \(3\). Its squarefree product \(K\) is at least \(7\cdot11\). It divides the shift difference, which is even, so \(2K\) divides it.

The bound is attained at \(n=360\), shifts \(3^3+5^2=52\), \(3^4+5^3=206\), residuals \(308,154\), and product \(154^2+154^2\). Both residuals pass the two stated tests while both fail at \(7\) and \(11\).

## What enlarging the menu changes

Use the bipartite graph with row vertices and inert-prime vertices, including an edge for every actual divisibility \(p\mid R_i\) by a prime dividing at least two rows. The odd-valuation edges form an even-degree subgraph: each prime vertex has even degree by the product condition, and each row vertex has even degree by the odd-part condition. No odd-valuation edge can belong to a private prime. Consequently if the incidence graph is a forest all rows are norms. For at least one true row it suffices that no even-degree subgraph touches every row.

At \(n=345\), labels \((1,0),(1,3),(5,2)\) give \(341=11\cdot31\), \(217=7\cdot31\) and \(77=7\cdot11\). Each residual passes the odd-part and \(3\)-valuation tests. The odd edges form a six-cycle and the product is \(2387^2\), but none of the three selected residuals is a norm. This concerns only the selected menu: \(345=16^2+9^2+3+5\).

These conditions do not supply a product certificate at arbitrary \(n\), or any pointwise coverage bound.
