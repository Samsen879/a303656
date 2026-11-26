# Moving square-factor compression and its exact failure boundary

For all sufficiently large \(n\) coprime to 15, a rectangular logarithmic exponent window contains candidates with
\[
 n-3^c-5^d=D^2 w,\qquad D^2\asymp(\log n)^2,\quad w>0,\quad w\equiv1\bmod15.
\]
A true two-square representation of \(w\) transfers by scaling, but there are infinitely many representable \(n\) for which every candidate of the maximal-scale rule below fails.

Let \(D=3^t5^u\), \(t,u\ge1\). Impose \(c\ge2t+1,d\ge2u+1\) and solve
\[
 3^c\equiv n-D^2\bmod5^{2u+1},\qquad
 5^d\equiv n-D^2\bmod3^{2t+1}.
\]
These are independent discrete logarithms in the full unit groups: 3 generates the units at \(5^k\), checking order 4 modulo 5 and a simple lift modulo 25; 5 similarly generates at \(3^k\) using order 2 and a simple lift. Thus the two exponent periods are \(4\cdot5^{2u}\) and \(2\cdot3^{2t}\). At these exponent lower bounds the other power vanishes in each modulus. CRT gives the stated \(D^2 w\) with \(w\equiv1\bmod15\).

Write \(C=\lfloor\log_3(n/3)\rfloor,\ J=\lfloor\log_5(n/3)\rfloor\). Use the largest \(t,u\) with \(3^{2t}\le J/4,\ 5^{2u}\le C/8\). In the rectangles \(2t+1\le c\le C,\ 2u+1\le d\le J\), each progression has at least one full period for large \(n\); both powers are at most \(n/3\). Maximality makes \(3^{2t}\asymp J\) and \(5^{2u}\asymp C\), so the candidate count is bounded and \(0<w<n/D^2\). For fixed \(t=u=1\), \(n=377,594377\) both select just \((3,3)\) in their rectangles. The reduced residuals are \(1\) and \(19\cdot139\); the latter fails even though \(594377=3+1+78^2+767^2\).

## Infinite simultaneous failure of the maximal-scale candidates

Take \(K=3^{2t}\to\infty\), \(L=5^{2u}\le K\) the largest even power of 5 below \(K\), and \(N=3^{8K}\). Across \(N\le n\le2N\), the prescribed maximal exponents \(t,u\) are exactly these for large \(t\): \(C=8K-1\), \(L<K\), and \(J/4=(2\log3/\log5)K+O(1)\) lies between \(K\) and \(9K\). Enforce \(n\equiv n_0=3^{2t+1}+5^{2u+1}+KL\bmod16\cdot3^{2t+1}5^{2u+1}\). This fixes the candidate progressions, and even using \(2N\) for the outer window yields at most \(50\cdot3=150\) rows, since \(1\le K/L<25\). Call their offsets \(r_i\).

Use a fixed list of 150 distinct inert primes \(p_i>5\) with \(\operatorname{ord}_{p_i}25>150\). They exist by discarding the finitely many prime divisors of \(\prod_{j=1}^{150}(25^j-1)\) from the infinite inert primes. In \(u-150\le j\le u\), the potential escape offset \(r_*=3+25^j\) collides with each \(r_i\bmod p_i\) for at most one \(j\). Choose an unexcluded \(j\). Seek \(n=r_*+a^2+b^2\) and impose \(a^2+b^2=r_i-r_*+p_i\bmod p_i^2\). Its target is a unit, so the finite-field norm map and a simple coordinate lift solve it.

The base modulus can also be imposed: \(n_0-r_*\) is 5 or 13 modulo 16 (both two-square residues), a unit modulo 3, and an arbitrary residue modulo 5. At 3 the unit norm lifts; at the split prime 5 every residue, including zero, is obtainable with a coordinate unit and hence lifts. Apply CRT separately to \(a,b\). The joint modulus is \(O(K^2)\), with fixed outside primes, so choose \(a=\sqrt N+O(K^2)\) with \(a\ge\sqrt N\), and \(0\le b=O(K^2)\). This puts \(n\) in \([N,2N]\) for all large \(t\). It is representable by the genuine escape label \((1,2j)\), but every maximal-scale candidate satisfies \(v_{p_i}(n-r_i)=1\) and fails. This rules out only the given maximal-scale search, not smaller squares or unrestricted representations.

## A separate family where the cofactor panel is conclusive

Take a sufficiently large multiple \(k\) of 42, \(k\le T<2k,\ T\equiv106\bmod196\), and \(n=5^k+9^kT\). For \(e\equiv1\bmod21,\ k^{1/3}\le9^e\le k/4\) use \((c,d)=(2k+2e,k)\). Both powers are at most \(n/4\) for large \(k\), and
\[
 R=n-3^c-5^d=9^k(T-9^e),\quad
 0<T-9^e<2k,\quad T-9^e\equiv97\bmod196 .
\]
The congruence follows from \(9^{21}\equiv1\bmod196\). The cofactor is \(1\bmod4\). If every inert prime at most \(\sqrt{2k}\) has even valuation in it, two outside odd-valuation inert primes would have product greater than \(2k\), impossible; hence this panel certifies a genuine norm. It is contained in the usual \(\sqrt{\log n}\) panel. The origin is not a norm, since \(n-2\equiv7\bmod49\) (both 5 and 9 raised to \(k\) are 1 modulo 49).

There are unconditionally at least \(\Omega(\sqrt{k})\) such targets \(T\) with a non-origin witness for each large \(k\). Fix one indicated \(e\), which exists for large \(k\) since the ratio of the two bounds tends to infinity. Take \(T=9^e+A^2+9\) for positive \(A\equiv26\bmod196\) and \(k\le T<2k\). The interval for \(A\) has length \(\Theta(\sqrt k)\), the residue condition gives \(T\equiv106\bmod196\), and the cofactor is a two-square norm. This proves a count, not a fixed positive fraction of all \(T\) in the congruence class.

At \(k=420,T=694,e=1\), direct replay gives \(w=685=26^2+3^2\); the actual residual at \((842,420)\) has valuations \(840,0,0,0,0\) at \(3,7,11,19,23\). At the same \(k,T=498,e=1\), the cofactor is \(489=3\cdot163\) and the actual 3-adic valuation is 841, so the row is rejected. Both targets have the exact origin obstruction.
