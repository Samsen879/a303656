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

### Infinite controls and the fixed-rough-part limit

With panel \(\{2,3,5\}\), set \(n=160\cdot9^t+5^b\) for \(t,b\ge0\). The two actual labels \((2t+1,b),(2t+3,b)\) give \(157\cdot9^t,133\cdot9^t\). Their stripped parts \(157,133\) are both \(1\bmod4\) and above the one-label threshold \(7\cdot11\). The difference is \(24\cdot9^t\), so no outside prime is shared, and \(157\cdot133=20881<33649=7\cdot11\cdot19\cdot23\). Thus the product test certifies a true residual without needing coordinates in advance. Only the first survives, because \(133=7\cdot19\). Here \(n\) is odd, so no pair of the powers alone equals \(n\).

A second family, \(n=3^{2t+5}+5^{b+6}\), gives residuals \(3^{2t}(3^5-1),5^b(5^6-1)\) at labels \((2t,b+6),(2t+5,b)\). The stripped parts \(121,217\) have product \(26257<33649\), and the two fixed differences have gcd two before stripping the base powers. This time both exponents vary between the labels, but there is a cross-label zero residual. Two sharpness controls with panel \(\{2,3,5\}\) are \(n=213\), residuals \(209,161\) (coprime, both fail, product exactly \(33649\)), and \(n=165\), residuals \(161,133\) (below threshold, both fail, share 7).

In fact a fixed-panel, bounded-stripped-part family with both exponents different generally cannot avoid the cross-label degeneracy. Fix a finite panel containing 3 and 5 and a bound for both stripped parts. Require positive different residuals, stripped parts greater than one, \(c_1\ne c_2,\ d_1\ne d_2\). Except for finitely many solutions, \(n=3^{c_1}+5^{d_2}\) or \(n=3^{c_2}+5^{d_1}\).

To prove this, all six signed terms in
\[
 R_1+3^{c_1}+5^{d_1}-R_2-3^{c_2}-5^{d_2}=0
\]
belong to one finitely generated rational multiplicative group, since the panel is fixed and the remaining parts are bounded. Partition into minimal vanishing subsums. Within each block, dividing by one signed term reduces the ratio problem to a nondegenerate \(S\)-unit equation; [Evertse–Schlickewei–Schmidt, Theorem 1.1](https://annals.math.princeton.edu/2002/155-3/p04) gives finitely many possible ratio lists. A block containing both a power of 3 and a power of 5 has only finitely many absolute choices, since their ratio uniquely determines those exponents. A block with just one residual and powers of only one base needs both opposite-sign powers of that base: a single power equal to the residual would have stripped part one. The equation with both powers gives a cross-label zero. A block containing both residuals with at most one base leaves two opposite powers of the other base; those alone are distinct, and adding a single odd power of the first base cannot cancel their even difference. With no base terms in the block it would require equal residuals. Finally, a block with no residual and only one base cannot vanish because the corresponding exponents differ. Hence, when no cross-label zero is permitted, every block has both bases, which yields only finitely many six-tuples. This does not give a useful bound for a panel or a stripped-part allowance growing with \(n\).

## A sparse panel that grows unconditionally with height

For an odd prime \(\ell\ge5\), let \(Q_\ell\) consist of all inert primes \(q\) for which \(\operatorname{ord}_q3\) is \(\ell\) or \(2\ell\). There are fewer than \(\ell\) of them: their product divides \(3^{2\ell}-1\), whereas each is at least \(2\ell+1>9\). For \(\ell\equiv3\bmod4\) the panel \(Q_\ell\) is nonempty, since \((3^\ell+1)/4\equiv3\bmod4\) has an inert factor, and its odd prime factors all have order \(2\ell\). The \(Q_\ell\) for distinct \(\ell\) are disjoint.

For each \(n\), retain the above parity test and lift at 3 by fixing \(d\in[0,17]\). Then use only \(c\). Avoid 7, 11 and 43 via one forbidden class respectively modulo 3, 5, 7 (their orders of 3 are 6, 5, 42); if there is a root, its projection modulo the chosen divisor of the order is one forbidden class, and avoiding it is sufficient. For every \(11\le\ell\le Y\) other than 19, avoid all \(q\in Q_\ell\) by the same method, projecting their bad classes modulo \(\ell\). There are fewer than \(\ell\) prohibited classes, and CRT combines the separate coordinates with the fixed parity. At 19 the order of 3 is 18 and \(3^{18}\not\equiv1\bmod19^2\). None of the chosen coordinates is divisible by 19; the current progression times 18 thus allows the exact 19-adic lift to valuation two if needed. Its final period divides
\[
 P=227430\prod_{\substack{11\le\ell\le Y\\\ell\ {\rm prime},\ \ell\ne19}}\ell
   \ \le\ 227430\,4^Y .
\]
Here \(227430=\operatorname{lcm}(2,3,5,7,18\cdot19^2)\). The elementary primorial bound follows by induction: primes in \((m+1,2m+1]\) divide \(\binom{2m+1}{m}\le4^m\), and even integers greater than two add no new prime. Choose \(3\le c\le P+2\); positivity follows if \(n>3^{P+2}+5^{17}\). Thus any \(Y\) of order \(\log\log n\) with a constant less than \(1/\log4\) eventually fits the window. This is a sparse family of primes of unbounded size as a panel, not a guarantee for all inert primes below a growing cutoff.

For an exact control, \(Q_{11}=\{23,67,3851\}\), obtained by factoring \(3^{22}-1\) and testing orders. At \(c=6934,d=0\) consider
\[
 n_+=3^{6934}+1+(19\cdot31)^2\cdot16993,\qquad
 n_-=3^{6934}+1+19^2\cdot31\cdot47\cdot41.
\]
Both residuals are units at \(7,11,43\) and \(Q_{11}\), and both have exact valuation two at 19. In the first case, after removing \(19^2\) and the split prime 16993, the remaining \(31^2\) is strictly below \(31\cdot47\), the product of the first two untested inert primes. Its parity certifies a true norm, also checked by coordinates \(42997,63612\) for the original remainder. In the second case, removing \(19^2\) and 41 leaves exactly \(31\cdot47\), with both valuations odd. This same-panel control demonstrates why the stopping inequality is strict.

### A narrow window and a common-scale obstruction for growing panels

Write \(q_1<q_2<q_3<q_4\) for the first four inert primes above \(Y\), \(L=q_1q_2,\ U=q_3q_4\). If both labels fail the one-label size test and pass the two-label product test, then \(L\le w_1,w_2<U\). This is immediate from \(w_1w_2<LU\). The interval does not force triviality: the abstract coprime rough parts \(q_2^2,q_1q_3\) lie in it, and their product has ratio \(q_2/q_4<1\) to the threshold. One is a norm and one is not. The missing step is realizing such a pair with actual power offsets at one \(n\) for growing \(Y\).

For a concrete restriction take labels \((\ell,0),(0,\ell)\) with odd prime \(\ell\) and \(Y\le2\ell\). Their offset difference is \(\Delta=5^\ell-3^\ell\). Every odd prime dividing \(\Delta\) gives order exactly \(\ell\) to \(5/3\), since order one would force it to divide 2. Hence each such prime is at least \(2\ell+1>Y\), and \(v_2(\Delta)=1\). If the residuals are \(R_i=A_iw_i\) with \(A_i\) the stripped small-prime parts, then \(\gcd(A_1,A_2)\mid2\) and \(\max(A_1,A_2)>\Delta/U\) when both targets meet the narrow window. In particular a common \(A_1=A_2\) would require \(\Delta<2(U-L)\). For \(\ell=7,Y=14\), direct arithmetic gives \(\Delta=75938=2\cdot43\cdot883,\ L=437,\ U=1333\), so a common scaling cannot work.

There is a weaker positive control with growing \(Y\) and no zero label, not requiring the product test. Let \(m\) be the product of odd primes up to a parameter tending to infinity and take \(n=3^{2m}+3^{4m}+5^{2m}+5^{4m}\). The labels \((2m,4m),(4m,2m)\) leave \(9^{2m}+5^{2m}\) and \(3^{2m}+25^{2m}\). Their ratio tends to zero, and all prime factors of both residuals are at most \(Y=28^{2\varphi(m)}=n^{o(1)}\): for odd \(m\) their homogeneous cyclotomic factors have indices \(4d,\ d\mid m\), degrees \(2\varphi(d)\), and absolute values at most \(28^{2\varphi(d)}\), using the product over roots of unity. Euler's product gives \(\varphi(m)/m\to0\). No inert prime divides a sum of these two coprime even powers. Finally \(n\equiv4\bmod8,\ n\equiv2\bmod3\) exclude any zero label: the first congruence would force odd \(c\) and even \(d\), giving \(n\equiv1\bmod3\). This proves growth under two changing labels, but both rough parts are one, so it does not solve the genuinely joint narrow-window problem.

## At most four simultaneous Wieferich primes cannot obstruct a finite panel

Let \(Q\) be any fixed finite inert-prime panel. If at most four of its primes other than 3 satisfy both \(3^{p-1}\equiv5^{p-1}\equiv1\bmod p^2\), then for every sufficiently large \(n\) the panel and the earlier modulo-eight normalization can be passed. Single-base Wieferich primes are unrestricted. The following proof does not assert that simultaneous primes are known or absent.

Fix exponent parities and \(d\bmod18\) as before. Mark every simultaneous prime for avoidance rather than lifting. For a marked \(q\), let \(g(q)\) be the largest odd prime factor of the least common multiple of the two orders modulo \(q\). Draw the edge \(q\to g(q)\). Such a factor exists because \(q\equiv3\bmod4\) forces the two-part of the orders to be at most two, and \(\operatorname{ord}_q3\mid2\) would give \(q\mid8\). Mark each endpoint in \(Q\setminus\{3\}\) as well and repeat. All paths strictly descend (an order divides \(q-1\)). If there were \(k\) initial marks, each coordinate receives at most \(k\) edges, because each edge is on a root path and no such path can enter the same coordinate twice.

Choose the prime-power coordinates of the two exponent residues in increasing prime order. At coordinate \(\ell\), the lower parts of the two orders of each incoming edge are already determined. The two powers depend injectively on each available \(\ell\)-part of their exponent classes. Accordingly a single incoming edge \(q\to\ell\) forbids at most a fraction \(\ell^{-a_\ell(q)}\), where \(a_\ell(q)\) is the larger of \(v_\ell(o_{3,q})\) and \(v_\ell(o_{5,q})-2\,\mathbf1_{\ell=3}\); the subtraction accounts for the already fixed \(d\bmod18\). At \(\ell=3\), only \(q=7\) can have weight \(1/3\): every other inert \(q\) with \(g(q)=3\) has \(9\mid o_{3,q}\), because \(3^6-1=2^3\cdot7\cdot13\). All other weights there are at most \(1/9\). For \(\ell\ge5\) each weight is at most \(1/\ell\), so no coordinate can be filled by \(k\le4\) edges.

At an unmarked panel prime \(p\) at least one base has a non-Wieferich lift, and no avoidance edge ends there. The residual modulo \(p\) only depends upon already fixed lower prime coordinates of both orders and the fixed parities. The free \(p\)-coordinate can therefore be used at the non-Wieferich base to set the residual to \(p^2\bmod p^3\) when needed. Later, larger coordinates do not disturb this. The entire procedure fits the modulus \(\operatorname{lcm}(18,\{o_{b,q}\})\prod_{q>3,\ q\in Q}q^2\), which gives a uniform height threshold as in the fixed-panel proof.

With exactly five initial marks, only the \(\ell=5\) coordinate can be fully forbidden. To fill it would require five incoming edges, each with \(a_5=1\), saturating its bound of five cells out of 25. If only one base varies, the five cells form a coordinate line. If both vary, saturation means two order-five cosets agree under \(x\mapsto n-x\) modulo \(q\). The two cosets each sum to zero; thus \(q\mid n\), and then discrete logs within the common subgroup make the forbidden set a line. Covering all 25 cells requires five parallel lines, since two nonparallel lines intersect. In particular a double-variable row with \(q\nmid n\), or two different directions, breaks this chosen possible obstruction. For \(q=11\) both orders are five and the maximum over all \(n\bmod11\) is just three forbidden cells, checked by the \(5\times5\) table.

Exact field tests show why marking matters. At \(n=40119,\ c=4+6u,\ d=1+18v\), all 49 coarse choices modulo 7 satisfy \(7\mid R\), and \(49\mid R\) exactly when \(v=3u\bmod7\), which is also exactly when \(43\mid R\). Thus lifting the 7 valuation and insisting that 43 be a unit is impossible in this chosen phase; \((c,d)=(6,1)\) gives both units and the true residual \(24^2+197^2\). This never established a full-panel obstruction.

### Two unequal smooth parts must share exactly one integer parameter

Take the crossed labels \((a,b+v),(a+u,b)\), with \(a,b,u,v>0\), and assume the original residuals are \(A w_1,B w_2\) where \(A=3^a,\ B=5^b\). Write \(C=3^u-1,\ D=5^v-1\). Equality of the two values of \(n\) implies \(A(w_1-C)=B(w_2-D)\); since \(A,B\) are coprime, both conditions must use the same integer \(k\):
\[
w_1=C+kB,\quad w_2=D+kA,\quad
n=3^{a+u}+5^{b+v}+kAB.
\]
Conversely these equations suffice for the two actual residual identities. If the panel includes \(2,3,5\), both \(w_i\) are stripped, \(a\) is even from the inert parity test, and \(w_i\equiv1\bmod4\), then the equations force \(k\equiv1\bmod4\), \(v\) odd, and \(u\equiv2\bmod4\): modulo 4 the second equation for \(w_i\) forces \(k=1\bmod4\), then the first makes \(u\) even; the unit condition modulo 5 excludes \(u=0\bmod4\), and the one modulo 3 makes \(v\) odd.

Two genuinely joint, coprime observed examples are \(n=1231,Y=5\) with \((a,b,u,v,k)=(2,1,2,1,25)\) and \((w_1,w_2)=(133,229)\), and \(n=536131,Y=19\) with \((6,1,6,5,-3)\) and \((713,937)\). Both parts in each example meet or exceed the individual size cutoff, but their products are respectively \(30457<33649\) and \(668081<(23\cdot31)(43\cdot47)\). Both first labels fail by exact odd valuations (\(133=7\cdot19,\ 713=23\cdot31\)), so the second is certified, also checked by \(229=15^2+2^2,\ 937=24^2+19^2\). Both \(n\) are odd, hence there is no zero label. Changing \(v\) to 7 in the first candidate while fixing its coarse pair makes the two values of \(k\) equal to 25 and \(-8655\); the separately valid divisibilities cannot match a common integer.

For the positive-\(k\) branch in a genuinely joint window \(L\le w_i<U\), we have \(A,B<U\) directly, and \(n=A(w_1+1)+B(w_2+1)-kAB<2U^2\). Thus this branch cannot supply a large \(n\) for a fixed \(U\), and must track the size of the rough-part window as it grows. The negative-\(k\) branch is not ruled out by that argument; these two examples give no growing family.

## Coupled low coordinates raise the finite-panel allowance to ten

The preceding descending graph works for up to **ten** simultaneous base-3/base-5 Wieferich primes, using a joint choice of the coordinates at \(3,5,7\) before treating all larger coordinates. The \(d\bmod18\) and parity constraints stay fixed. This upgrades the finite-panel sufficiency; it does not supply a bound on the actual count of simultaneous primes.

For every row with \(g(q)\in\{3,5,7\}\), the free \(c\)-coordinates in this block range over the entire odd part of its order (the 2-part is at most two). With \(d\) fixed, a hit forbids at most the reciprocal of that odd part. The only possibilities below 21 are 3, 5, 7, 9 and 15: use the prime divisors of \(3^{2m}-1\), and test the exact odd part for these five \(m\). The resulting inert-prime exceptions, including the two full orders, are

| odd part | \(q\) | \((\operatorname{ord}_q3,\operatorname{ord}_q5)\) |
|---:|---:|---:|
| 3 | 7 | (6,6) |
| 5 | 11 | (5,5) |
| 7 | 547 | (14,546) |
| 9 | 19 | (18,9) |
| 15 | 31, 271 | (30,3), (30,27) |

The row 547 points outside the block, since \(13\mid546\). At 11 a sharper bound is \(3/25\), from the complete modulo-11 root table on the two free 5-coordinates. Every root path contributes at most one entry into the joint block; the only possible further internal edge is the single shared \(7\to3\), since 3 and 5 terminate. Thus there are at most eleven rows in the block, whose total forbidden fraction is bounded by
\[
 1/3+3/25+1/9+2/15+6/21=1549/1575<1.
\]
This remains an upper bound if some exceptional rows are absent. If an unmarked 7 is to be lifted afterwards, no block row depends on its 7-coordinate, since there is no incoming edge at 7. At all remaining coordinates \(\ell\ge11\) the earlier path count gives loss at most \(10/\ell<1\). The ordinary lifting and positive height threshold then apply.

The difference between fixed and jointly chosen low coordinates is real. For \(q=31,271\), take \(n\equiv6747\bmod201624\), \(c\) even, and \(d\equiv0\bmod54\). The row restrictions depend on \(c\bmod3\) and \(x=c\bmod5\), and are independent of the free \(d\bmod5\). At \(c\equiv1\bmod3\) they forbid \(x=4\) and \(x=0\) respectively, two distinct parallel lines. At \(c\equiv0\) or \(2\bmod3\) both restrictions are empty. Exact modular powering verifies all 30 choices. These are ordinary rows, not examples of simultaneous Wieferich primes.
