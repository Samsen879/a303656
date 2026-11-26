# Common rational pullbacks and the remaining same-point seed requirement

Use \(f_i(s)=s^2+h_i\), \(i=0,3\), on the actual three-column trajectory from [the dyadic quadratic-pullback limit](FIRST_248_QUADRATIC_PULLBACK_DYADIC_LIMIT.md). Here \(v_2(h_0)=-1,\ v_2(h_3)=3\). At a sufficiently active parameter in the integer progression the first-root and third-column conditions are respectively that \(f_0,f_3\) be rational Gaussian norms, since the scaling factors are rational Gaussian norms. The original residuals are integers, so a rational two-square representation implies an integer one by the two-square criterion: at an inert prime the valuation of a rational Gaussian norm is even.

## Formal rational parametrization

Set \(\Delta=h_0-h_3\), \(r_0=(\Delta+1)/2\), \(r_3=(\Delta-1)/2\), \(c=h_0-r_0^2=h_3-r_3^2\). Then, with
\[
 s=(t-c/t)/2,\qquad y=(t+c/t)/2,
\]
one has \(f_i(s)=y^2+r_i^2\) for both i. This is an actual degree-two rational function because \(v_2(r_0)=-2\) implies \(v_2(c)=-4\). It cannot attain any integral 2-adic s: for such s the purported square \((s^2+c)/r_0^2\) is 7 modulo 8, using \(v_2(h_0/r_0^2)=3\) and \(v_2(s^2/r_0^2)\ge4\).

## A local competitor and a conditional global converse

Let \(s_*\ne0\) with both \(f_i(s_*)\ne0\), and put
\[
 \lambda_i=1/f_i(s_*),\quad
 b=s_*(\lambda_0+\lambda_3)-1/s_*,\quad
 u_i=s_*\lambda_i-b/2,\quad a=\lambda_i-u_i^2 .
\]
The two choices give the same a, because \(u_0-u_3=s_*(\lambda_0-\lambda_3)\) and \(u_0+u_3=1/s_*\). Provided \(b\ne0\), set
\[
 X=\frac{bt^2}{1-at^2},\quad Y=\frac{bt}{1-at^2},\quad s=s_*+X .
\]
Indeed \(Y^2=aX^2+bX\), so \(\lambda_i f_i(s)=(1+u_iX)^2+Y^2\). On the actual progression \(b\ne0\): otherwise \(s_*^4=h_0h_3\), whose right-hand valuation is 2. In particular, whenever a genuine norm seed exists on the active integer progression, the multipliers \(\lambda_i\) are rational Gaussian norms, giving simultaneous rational-function norms and a degree-two map retaining that seed (t=0). Conversely any such rational-function norm representation specializing regularly at an active integer-progression parameter gives a genuine seed. The seed criterion is an equivalence, not a method of producing a new arithmetic point.

Over \(\mathbb Q_2\) this construction can actually hit a compatible 2-adic progression. Choose the free odd first coordinate of \(U_*\bmod4\) so that \(s_*=1\) is in the local progression. Writing \(H_E=5^{E+1}-239\), the data \(H_E\equiv6\bmod8,\ g\equiv1\bmod4,\ q\equiv2\bmod4\) give \(2f_0(1)\equiv1\bmod4\); \(h_3\equiv8\bmod16\) gives \(f_3(1)\equiv1\bmod8\). Both are norms over \(\mathbb Q_2\): for an odd unit, the norm condition is \(1\bmod4\), and 2 itself is a norm. Thus unlike the polynomial no-integral-hit theorem, the degree-two rational model does not impose a universal local impossibility. This local result and the global formal parametrization use different choices of map and do not establish a global integer point.

For symbolic replay, check \(Y^2-aX^2-bX=0\) directly, then compare the constant, linear and quadratic terms of \(\lambda_i f_i(s_*+X)\); these are \(1\), \(2u_i+b\), and \(u_i^2+a\), respectively. The real-trajectory modular inputs are reproduced in the linked earlier note.
