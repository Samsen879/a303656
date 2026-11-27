# The five-label Gaussian-switch family is polylogarithmically sparse

Allow **all** legal inputs of [the five-label construction](FIVE_LABEL_GAUSSIAN_SWITCH.md), including all positive odd \(x,y\) solving \(x^2-10y^2=-3^{2k}\) with \(5\nmid y\). The number of distinct resulting targets
\(n=3^{2k+5}+5^D+242x^2\le X\), with \(k\ge4\) and even \(D\ge4\), is \(\Theta((\log X)^4)\). Their centers \(H=n-5^D\le X\) have count \(\Theta((\log X)^3)\). This concerns one explicit mechanism rather than all targets with five true exponent labels.

**Upper bound.** Write \(r=\sqrt{10}\), remove the common \(3^s\) from \(x+yr\), and set \(m=k-s\ge0\); the remaining element is primitive at 3, of norm \(-3^{2m}\). If \(m>0\), its coefficients \(a,b\) are 3-adic units and \(a=\pm b\bmod9\) (since \(a^2-b^2=0\bmod9\) and only one of \(a\pm b\) can vanish mod 3). Divide by \(r+1\) in the plus case, or by \(r-1\) in the minus case; the quotient is integral by rationalizing with denominator 9. The mod-3 evaluation where the dividend is nonzero remains nonzero because the dividing factor is a unit at that evaluation. Therefore one may repeat in the same direction \(m\) times. The result is a positive unit. Every positive unit is a power of \(3+r\): multiply by its powers to reduce to \([1,3+r)\); a unit \(\xi>1\) there would have positive integer coefficients \(a=(\xi\pm1/\xi)/2,\ b=(\xi\mp1/\xi)/(2r)\), with \(b\ge1\) and \(a^2=10b^2\pm1\ge9\), forcing \(\xi\ge3+r\). Thus each input is
\[
 x+yr=3^{k-m}(r\pm1)^m(3+r)^\ell .
\]
The choices of \(k,D,m\) each number \(O(\log X)\); for each \(k,m,\pm\), the condition \(1<x+yr\ll\sqrt X\) leaves \(O(\log X)\) powers \(\ell\). Removing \(D\) gives the center bound.

**Matching lower bound without collisions.** Take \(X^{1/100}\le3^k\le X^{1/50}\), odd \(1\le m<k\) with \(5\nmid m\), and
\[
 \alpha=x+yr=3^{k-m}(1+r)^m(19+6r)^{10j},\qquad
 4X^{1/8}\le\alpha\le X^{1/6}.
\]
For each of the \(\gg\log X\) choices of \(k\) there are \(\gg\log X\) choices of \(m\), and for each pair \(\gg\log X\) nonnegative \(j\)'s in the displayed range. The norm is correct. Reduction modulo 2 shows odd coordinates, modulo 5 gives \(y\ne0\) since the unit factor is 1 there, and the two mod-3 evaluations give \(v_3(x)=k-m\). The identity \(2x=\alpha-3^{2k}/\alpha\) yields \(X^{1/8}\le x\le X^{1/6}\) for sufficiently large \(X\). If two centers have different \(x\), the gap of their \(242x^2\) terms is \(\gg X^{1/8}\), greater than the maximum \(O(X^{1/25})\) variation in \(3^{2k+5}\). Therefore a center determines \(x\), then \(k\), then \(m\) by the valuation, then \(j\) by strict growth. Finally there are \(\gg\log X\) even \(D\)'s with \(\sqrt X\le5^D\le X/2\), and their intervals after adding \(H=O(X^{1/3})\) are disjoint and below \(X\). Every such input still has the five true labels of the earlier construction and the same false diagonal. All the resulting labels have exponents of order \(\log X\) for this lower-bound portion. The target count, the input count, and the number of constructed distinct \((n,c,d)\) all have the stated fourth-power order; none imply positive density.
