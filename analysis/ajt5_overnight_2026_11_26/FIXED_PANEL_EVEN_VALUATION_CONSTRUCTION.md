# A fixed-panel lift with two necessary outside blockers

Let \(Q\) be a finite set of primes \(3\bmod4\). Assume that for each \(p\in Q\setminus\{3\}\) at least one \(b\in\{3,5\}\) satisfies \(b^{p-1}\not\equiv1\bmod p^2\). Put
\[
 M=18\prod_{p\in Q\setminus\{3\}}p^2(p-1).
\]
For every integer \(n>3^{M+2}+5^{M-1}\), there are \(3\le c\le M+2,\ 0\le d<M\) such that \(R=n-3^c-5^d>0\), its valuations at \(Q\cup\{3\}\) are all 0 or 2, and its odd part is \(1\bmod4\). If this particular residual is not a sum of two squares, it therefore has at least two distinct odd-valuation primes \(3\bmod4\) **outside** \(Q\cup\{3\}\). No estimate here guarantees that such outside primes are absent.

Choose \(c=3\) or \(4\) and \(d=0\) or \(1\) to make \(R\equiv1\bmod8\) for odd \(n\), or \(R\equiv2\bmod8\) for even \(n\). This is possible since the four sums \(3^c+5^d\bmod8\) give all even classes. Hold the exponent parities fixed. At 3, \(3^c\) is zero modulo 27. If \(R\) is divisible by 3, adding twice an integer to \(d\) lets \(5^d\) run through all residues modulo 27 with its original value modulo 3: \(25\) generates the order-nine principal-unit subgroup. Choose the shift making \(R\equiv9\bmod27\). Otherwise it is already a unit. Start the common period at 18. Future shifts by multiples of 18 preserve this exact test and the modulus-eight test as long as \(c\ge3\).

Process the remaining \(p\)'s in ascending order. Let \(M_0\) be the accumulated period for previous primes. Its prime factors are all smaller than \(p\), so \(p\nmid M_0\). If \(R\) is zero modulo \(p\), increase the exponent of an allowed base \(b\) by \(M_0(p-1)t\). The multiplier \(b^{M_0(p-1)}\) has \(v_p(\,\cdot-1)=1\) by binomial lifting; its powers run through the full principal-unit subgroup modulo \(p^3\). The base's existing power is a unit, so these shifts run through all residues of \(R\bmod p^3\) with its fixed value modulo \(p\). Choose \(R\equiv p^2\bmod p^3\). If the starting residual is a unit no lift is needed. Enlarge the period by the factor \(p^2(p-1)\); both unit bases then have that period modulo \(p^3\). In the end replace the exponents by representatives in the indicated ranges. They preserve all tests; the given bound on \(n\) ensures positivity.

Removing powers of two from \(R\) leaves an integer \(1\bmod4\), so the number of its inert primes with odd valuation is even. If it fails the two-square criterion this number is nonzero, hence at least two. The same parity argument thus works for **even** \(n\), not just odd \(n\).

Independent controls for \(Q=\{3,7\}\), \(M=5292\), and \(X=5^{5294}+3^{5294}\): at \(n=X+9\), take \((c,d)=(868,2)\); at \(n=X+22\), take \((c,d)=(2812,17)\). Both have exact \(v_3=v_7=2\), checked modulo \(3^3,7^3\); the residuals are respectively 1 and 2 modulo 8. These are genuine positive integer residuals. The bound is for fixed \(Q\) and does not address simultaneous Wieferich primes or control the joint occurrence of outside blockers.
