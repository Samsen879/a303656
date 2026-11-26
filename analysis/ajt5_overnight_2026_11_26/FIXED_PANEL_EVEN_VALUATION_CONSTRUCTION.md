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

## Exact lifting when a coarse phase is fixed

Let \(Q'\) omit 3 from the panel; treat the modulo-eight and 3-adic conditions as above. For \(p\in Q'\) and \(b=3,5\), put \(o_{b,p}=\operatorname{ord}_p b\), \(s_{b,p}=v_p(b^{o_{b,p}}-1)\), and take \(L_3=\operatorname{lcm}(2,\{o_{3,p}\})\), \(L_5=\operatorname{lcm}(18,\{o_{5,p}\})\). In a fixed compatible phase \(c\bmod L_3,d\bmod L_5\), define
\[
 t_p=\min(s_{3,p}+v_p(L_3),s_{5,p}+v_p(L_5)).
\]
All residuals in the phase agree modulo \(p^{t_p}\). The phase can realize even valuations simultaneously at every \(p\in Q'\) if and only if this common residue at each \(p\) is zero or has even valuation. A nonzero residue fixes the valuation. For a zero residue, choose a base attaining the minimum and keep the other base's progression parameter zero modulo \(p^2\). The chosen base's progression generates the full principal moves starting at \(p^{t_p}\), by LTE. It can make the residual \(p^e\bmod p^{e+1}\) with \(e\) the smallest even integer at least \(t_p\). Prescribing the selected base progression parameter modulo \(p^{e+1-t_p}\), at most \(p^2\), suffices; combine the prescriptions across \(p\) by CRT for the two bases separately. Reducing parameters to residues modulo \(\prod p^2\), with an appropriate representative to keep \(c\ge3\), gives a finite height bound for strict activity. This characterizes one phase, not whether a feasible phase always exists.

A phase can be locked even by primes where neither base is Wieferich. For \(Q'=\{7,43\}\), both bases have order 42 modulo 43, so \(L_3=42,L_5=126\). In phase \((0,0)\) both base powers are 1 modulo 49. For \(a=5+12642\cdot3^{42}\), \(n=82+a^2\equiv9\bmod49\); the phase is then uniformly bad at 7 with exact valuation one. The pair \((42,0)\) is active, while the same integer has the true representation \(n=a^2+0^2+3^4+5^0\). This is a genuine phase restriction, not a counterexample to the original conjecture.

## A two-label product test

Take two positive actual residuals \(R_i=n-3^{c_i}-5^{d_i}\). Strip factors \(p\le Y\) and call the resulting positive integers \(w_i\). Assume all stripped inert prime exponents are even, both \(w_i\equiv1\bmod4\), and \(w_1,w_2\) share no inert prime. If \(w_1w_2\) is less than the product of the first four \(3\bmod4\) primes exceeding \(Y\), then one of the original \(R_i\) is a true two-square norm. Indeed, if either remaining factor is not a norm it requires two distinct odd-valuation inert primes, and simultaneous failure would require four distinct ones. Disjointness can be checked without factoring both residuals: any common prime must divide the difference of the two removed power-sums.

For \(n=355,\ Y=7\) take offsets \(2,14\), giving \(w_1=353,\ w_2=341=11\cdot31\). No factor at most 7 was stripped. Both exceed the one-label bound \(11\cdot19\), but their product is \(120373<11\cdot19\cdot23\cdot31\). Here the first residual equals \(17^2+8^2\). The test does not yet provide such a pair for every \(n\).
