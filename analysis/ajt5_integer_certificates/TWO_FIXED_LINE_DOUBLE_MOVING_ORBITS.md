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
