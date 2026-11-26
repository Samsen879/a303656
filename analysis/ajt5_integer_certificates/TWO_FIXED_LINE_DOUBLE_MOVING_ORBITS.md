# Two integral double-moving Gaussian orbits on the fixed line

**Scope.** Explicit infinite families for two fixed exponent labels in AJT5; no implication of coverage of arbitrary integers. The completeness and minimal-degree statements below concern only the specified fixed-line factor template.

Write \(j=(W-1821)/5\) and \(n=25((j+219)^2+(2j+801)^2+2)+2\). Direct expansion gives \(n=5W^2+658897\). If \(W\equiv26\bmod30\), then \(j\) is an integer and \(\lfloor n/5\rfloor=W^2+131779\). For labels \((d,c;e,f)\) put \(A=5^d+3^c-131779\) and \(B=(5^e+3^f-658897)/5\). The two target residuals are \(W^2-A\) and \(5(W^2-B)\).

## Exactly two labels in this template

Impose \(e=d\) or \(d+1\), and \(A-B=b^2\). Fix nonzero rationals \(\rho,m\). A nonreal root-square \(q\) of \((\rho s^2-b+im)^2+B\) exists in \(\mathbb Q(i)\) if and only if \(-B\) is a square there. Indeed \(\rho q-b+im=\pm\sqrt{-B}\); when the square root is imaginary, at least one sign leaves \(q\) nonreal since \(m\ne0\). A rational number is a square in \(\mathbb Q(i)\) exactly when it is a signed rational square.

If \(B\) is nonintegral then \(v_5(B)=-1\). For integral \(B\), \(e=0\) forces \(f\equiv0\bmod4\), and \(B\equiv5\bmod8\). For \(e\ge1\) we have \(f\equiv3\bmod4\), and \(B\equiv3\) or \(7\bmod8\) as \(e\) is odd or even. Thus \(B\) has to be negative and \(e\) positive even. The bound \(5^e+3^f<658897\) leaves only \(e\in\{2,4,6,8\}\) and \(f\in\{3,7,11\}\); testing the twelve pairs gives \((e,f,\sqrt{-B})=(2,3,363),(8,11,135)\). The four expressions for \(A-B\) are \(3^c-5,3^c+15,3^c-35429,3^c+277071\). Odd \(c\) fails modulo 8 in all four. For even \(c\), factor the difference of squares \(b^2-(3^{c/2})^2\) and test the divisor pairs of the four nonzero constants. The only labels that survive are \((1,2;2,3)\) and \((2,0;2,3)\), with \(b=2,4\) respectively.

## Integral orbit formulas

In both cases take \(L=363,\ B=-L^2,\ \rho=b-L,\ m=2b,\ A=b^2-L^2\). For the indicated \(h=h(T)\), define
\[
X=\rho h^2-b,\quad W=(X^2+m^2-L^2)/(2m),\quad D=(\rho^2h^2+A)/m,\quad
G=W-D+ih(D-\rho),\quad F=W-m+iX .
\]
Expansion, or \(\rho^2+A=m\rho\), gives \(N(G)=W^2-A\) and \(N(F)=W^2+L^2\). Also \(2mF=(X+im-L)(X+im+L)\). The following polynomials \(P\) divide \(F\) in \(\mathbb Q(i)[T]\) (direct polynomial division):
 
| \(b\) | \(h\) | \(P\) | \(T_0\) | \(D_0\) |
|---|---|---|---:|---:|
| 2 | \((T^2+2)/361\) | \(T^2-19(1-i)T+2-361i\) | 2229 | \(8\cdot361^2\) |
| 4 | \(359(T^3+T)/8\) | \(359(T^2+1)+8i\) | 72 | \(2\cdot8^5\) |

Set \(Z=\overline P(F/P)\) and \(C=(1+2i)P(T_0)Z/\overline{P(T_0)}\). Then \(N(C)=5(W^2+L^2)\). Expanding in \(T\), the coefficients of \(W,G,Z\) have denominators dividing \(D_0\); the extra denominator for \(C\) divides \(N(P(T_0))\). At \(T_0\), \(W,G,F\) have integral coordinates and \(C(T_0)=(1+2i)F(T_0)\). Substituting \(T=T_0+Sk,\ S=30D_0N(P(T_0))\), therefore gives integer polynomials whose nonconstant coefficients are all divisible by 30. This verifies the congruence and both witnesses for every integer \(k\).

| \(b\) | \(W(T_0)\) | \(S\) | degrees of \(W,D,\operatorname{Im}Z,W-\operatorname{Re}Z\) |
|---|---:|---:|---|
| 2 | 584489691941016981296 | 759035759173366330560 | 8, 4, 7, 6 |
| 4 | 634471019058071105066606174917196 | 6812203356564357120 | 12, 6, 10, 8 |

These degrees are obtainable by Gaussian polynomial division followed by ordinary expansion; in particular both normalized differences are nonconstant. For the fixed \(b=2,\rho=-361,m=4\) atom, each of its two Gaussian quadratics is irreducible: the Gaussian norm of the root-square numerator is \((L\pm b)^2+m^2\), strictly between consecutive integer squares. After affine substitution their factors, and hence any conjugate-factor replacement, remain even about the same center. The leading normalized term is real up to a constant phase. After removing that phase the imaginary coordinate has degree at most two, so \(W-\operatorname{Re}Z\) is constant by the norm identity. Thus degree four cannot give two moving normalized differences in the affine-and-factor-conjugation model, and the degree-eight construction is minimal in this particular polynomial composition model. No analogous minimum over all rational parameterizations or all labels is asserted.

## Addendum: degree eight for the second label as well

The second label \(b=4,\rho=-359,m=8\) also has a quadratic pullback with an integral anchor, at a different rational vertex. It can use the original fixed line without the optional \(W\equiv26\bmod30\) refinement. Define
\[
\begin{aligned}
K&=3396423802945926559710546764301829676144,\\
J&=76273465814291347810541470372466491323521,\\
x&=-276108016454435220001+1527312164800256i,\\
y&=-6150534574215264056-34022142478336i,\qquad q=1+8i/359 .
\end{aligned}
\]
Then \(2xy=K,\ x^2+y^2q=J\). Take \(h=(T^2-J)/K\) and \(P=T^2-2xT+2x^2-J\). Multiplication gives \(P(T)P(-T)=K^2(h^2-q)\); since \(X+8i+363=-359(h^2-q)\), \(P\mid F\) for the same formulas \(X,W,D,G,F\) above. In particular \(F/P=-359P(-T)(X+8i-363)/(16K^2)\). Direct expansion gives degrees \(8,4,7,6\) for \(W,D,\operatorname{Im}Z,W-\operatorname{Re}Z\), with \(Z=\overline P(F/P)\).

At \(T_0=1069489203513072441433941376198344249\), the exact value \(h(T_0)=336768089847601474780357706171045\) is \(5\bmod10\). Substitution gives integral \(W,G,F\) with \(W\equiv1\bmod30\), so \(j=(W-1821)/5\) is still integral and the same parent and child residual formulas hold. The denominators for \(W,G,Z\) divide \(16K^4\), as seen using the formula for \(F/P\); the normalization \(C=(1+2i)P(T_0)Z/\overline{P(T_0)}\) adds at most \(N(P(T_0))\). Thus \(T=T_0+480K^4N(P(T_0))k\) makes the coordinates of \(G,C\) and \(W\) integer polynomials, all their nonconstant coefficients being divisible by 30. Consequently each integer \(k\) gives the same real label \((2,0;2,3)\) on an integral degree-eight double-moving orbit. The argument rules neither on other rational vertices nor on a degree reduction outside the fixed model.

## Finite prime tests cannot rule out every quadratic pullback

For the second label \((2,0;2,3)\), the stronger integral congruence \(W\equiv26\bmod30\) is still open in degree eight. For every prescribed finite set of rational primes, however, there is a single quadratic pullback that is globally reducible over the Gaussian rationals and that has a local preimage of \(s=15\) at every prime in the set. At that anchor value the original \(W(s)\) is an integer congruent to 26 modulo 30. This result does not give a common rational preimage.

Take \(\delta=8/359,\ N=1+\delta^2\) and use the curve \(E:y^2=x((x-1)^2+\delta^2)\) with \(P=(1,\delta)\). Its good reduction group sizes at \(3,7\) are \(6,10\), respectively, checked by directly counting the points. Prime-to-characteristic torsion injects on reduction, so a rational torsion point has order dividing two; \(P\) has nonzero \(y\), and hence is not torsion. In the product of the finitely many compact groups \(E(\mathbb Q_p)\), nonzero multiples \(Q\) of \(P\) approach the identity simultaneously. For \(Q=(x,y)\), set
\[
 J=(y/x)^2,\quad \mu=(x^2-N)/(2y),\quad
 \tau=-J/4-\delta^2/J .
\]
Then \(\mu^2=1+J/4-\delta^2/J\). Choose \(\alpha\) with \(\alpha^2=1+i\delta\), and put
\[
 a=-\mu\tau/(2J),\quad b=(\mu^4-N)/(2\mu\tau),\quad
 u=1+(1-\mu^2+i\delta)/\tau,\quad v=\bar u/\mu .
\]
Expansion gives \(2auv=1\), \(a(u^2+v^2\alpha^2)+b=0\); thus \(a(u+v\alpha)^2+b=\alpha\), furnishing a quadratic factor of \((aT^2+b)^2-(1+i\delta)\).

To reach \(s\), the condition is that \(J R(s)\) be a square, with \(R(s)=\mu^4-N-2\mu\tau s\): this follows by dividing \(s-b\) by \(a\). Near the elliptic identity \(J,\tau\) have pole order two and \(\mu\) has pole order one (the usual pole orders of \(x,y\) are two and three). Consequently \(R(15)/\mu^4\) tends to 1 at each chosen place. The square units contain an open neighborhood of 1, including at 2. Since \(J\) is already a rational square, taking \(Q\) sufficiently close gives the simultaneous local preimages.

For a finite check, take \(Q=6P\) by the ordinary chord-and-tangent law. Its \(\mu\) in lowest terms has denominator divisible by \(4\cdot3\cdot5\cdot359\) and numerator divisible by 43. At 43 the formulas are integral, and for every integer \(s\) we have \(R(s)\equiv-N\bmod43\), a nonsquare unit. Thus this specific globally reducible pullback has no integer anchor preimage, despite substantial denominators at the small primes governing the desired congruence. The obstruction can lie outside a fixed chosen panel.

## An exact numerator test in the first-atom elliptic branch

For the elliptic family used in the preceding local test, the first-atom numerator has an explicit cancellation rule. Put \(p_0=359,\ N=p_0^2+64\), and use the integral curve
\[
 Y^2=X(X^2-2p_0^2X+p_0^2N).
\]
For \(R=(A/B^2,C/B^3)\), \(B>0,\ \gcd(A,B)=1\), suppose \(A,B\) have opposite parity and \(C\ne0\). Set \(\Delta=A^2-p_0^2NB^4\). The rational parameter \(\mu=(X^2-p_0^2N)/(2p_0Y)\) has absolute reduced numerator
\[
 U=\frac{|\Delta|}{p_0^{\,2\mathbf1_{p_0\mid A}}\gcd(A,N)} .
\]

Indeed, before cancellation the denominator is \(2p_0BC\). The numerator is odd and coprime to \(B\). A common odd prime \(\ell\nmid p_0N\) of \(C,\Delta\) would, on reducing the curve equation and \(\Delta=0\bmod\ell\), force \(A=p_0^2B^2\bmod\ell\), then \(\ell\mid64p_0^2\), impossible. At \(\ell\mid N\) the numerator has valuation exactly one if \(\ell\mid A\) and zero otherwise, using the squarefreeness \(N=5\cdot17\cdot37\cdot41\); in the first case \(C\) also vanishes modulo \(\ell\). At \(p_0\mid A\), write \(A=p_0A_1\). The bracket \(A^2-2p_0^2AB^2+p_0^2NB^4\) has valuation two since \(A_1^2+64B^4\) is a nonzero unit modulo \(p_0\), by inertness. Consequently \(v_{p_0}(A)\) is a positive even integer and the numerator has valuation exactly two, all canceled. If \(p_0\nmid A\) its numerator valuation is zero.

All canceled factors are \(1\bmod4\). When \(B\) is even, \(\Delta\equiv1\bmod4\); otherwise \(A\) is even and \(\Delta\equiv-1\bmod4\). Thus the wrong sign of \(\Delta\) forces \(U\equiv3\bmod4\) and excludes a primitive Gaussian norm. Passing this sign test does not suffice; a reduced odd numerator \(U\) is free of all \(3\bmod4\) primes exactly when it admits a two-square representation with coprime coordinates.

For exact finite controls take \(P=(359^2,8\cdot359^2)\) and \(Q=(134865,2437560)\) on the integral curve. At \(2P\), the reduced numerator is the primitive norm \(23108^2+126825^2\) but \(v_3(\mu)=0\). At \(6P\), the three valuations at \(2,3,359\) are \((-3,-1,-1)\) and \(U\equiv1\bmod4\), yet \(v_{43}(U)=1\). At \(Q-3P\), \(B\) is even and \(\Delta<0\), so its numerator fails by sign alone. These controls are obtained by the rational chord-and-tangent law. They do not yield an anchor with \(W\equiv26\bmod30\).
