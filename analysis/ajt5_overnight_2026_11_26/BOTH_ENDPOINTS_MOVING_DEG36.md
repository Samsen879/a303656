# An actual integer orbit with both endpoint differences moving

At the true label $(10,2;11,3)$, use the rational polynomial orbit and the exact rotations from MOVING_PARENT_QUARTIC.md. Retain its notation $w(s), A,B,H,m$ and let $G(s)=(w(s)-D(s))+is(D(s)-1)$ be the unrotated parent polynomial, $F(s)=w(s)-m+i(s^2-2)$ the normalized child. Thus $N(G)=w^2-A$, $N(F)=w^2-B$, where $N$ is coefficient conjugation followed by multiplication. At $s_0=8404257$, both actual pairs can be rotated to integer coordinates (and the child scaled by $1+2i$), with $w(s_0)=517841637563222283536\equiv26\bmod30$.

Define
$$
 h(T)=T\left(1+\frac{s_0-1}{N(F(1))}N(F(T))\right),\quad W(T)=w(h(T)).
$$
The denominator is nonzero since the imaginary part of $F(1)$ is $-1$. The polynomial $h$ is odd of degree nine, and $h(1)=s_0$. The quotient
$$
 J(T)=F(h(T))/F(T)
$$
is in $\mathbb Q(i)[T]$: $h-T$ is divisible by $F(T)$, so the polynomial difference $F(h(T))-F(T)$ is divisible as well. Replace the normalized child by $\widetilde F(T)=\overline{F(T)}J(T)$. Its norm is exactly $W^2-B$, and the parent $G(h(T))$ has norm $W^2-A$.

Both endpoints move in the sense that after choosing their constant highest-degree direction to make the leading real part agree with $W$, their real differences from $W$ are nonconstant. For the parent that difference is $D(h(T))$, degree 18. For the child,
$$
 \overline{F(T)}/F(T)=1-2iH T^{-2}+O(T^{-4}).
$$
As $W$ has degree 36 and the imaginary part of $F(h(T))$ only degree 18, the new imaginary part has degree 34. The leading real part agrees with $W$, so the difference has degree less than 36. Expanding the norm in terms of that difference gives $D(2W-D)=Q^2+B$ with $Q$ the imaginary coordinate. Consequently the difference has degree 32.

At $T=1$, $\widetilde F(1)$ differs from $F(s_0)$ by the norm-one unit $\overline{F(1)}/F(1)$ in $\mathbb Q(i)$, which can be undone by a constant rational rotation. After applying this rotation, the existing rational parent rotation and the factor $1+2i$ to the child, all four anchor coordinates are integers. Choose $S$ a multiple of 30 times every coefficient denominator of the resulting polynomials and of $W$. Then the progression $T=1+Sn$ gives integer coefficients (the constants are the integral anchor, and every nonconstant coefficient is divisible by 30). This preserves $W\equiv26\bmod30$ and gives an unbounded genuine integral orbit with both endpoint differences moving. The claim is for this fixed label and degree 36; it does not give a quartic two-moving orbit or close the general representation problem.
