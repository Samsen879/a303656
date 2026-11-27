# Exact band reciprocals and an obstruction to finite-moment sign tests

Exact reciprocal reweighting preserves a **raw weighted gap** after removing any fixed accessible band \([z,z^L)\) of split primes. The gap also holds within each fixed prime-count stratum of that band. The sign for distinct true pairs remains open. I found an exact moment obstruction: low-order moments of both the prime count and the multiplicity can agree phase by phase while the reciprocal-weighted sign reverses.

### Exact reciprocal and the signed test

Keep the original 147 compatible phases and the two classes \(r_0=0,r_-\bmod49\). For label \(i\), put \(k_i=(S_0-S_i)/45\), and let \(P_z\) be the raw full-support Gaussian weight. On a true pair, the exact weight for one distinct pair is \(P_z(1/P_z)\).

For \(z=B^{1/(40s)}\) with fixed \(s\), remove pairs where a split prime \(p\ge z\) divides both norms or divides either norm to depth at least two. Per label these exceptions occupy \(O_s(B/z+\sqrt B)\) targets. For the square divisors, sum \(O(B/p^2+1)\) up to \(p\ll\sqrt B\). For common divisors, use the \(O_s(1)\) possible primes \(p\mid k_i\). Since \(P_z\) is bounded in terms of \(s\), the exceptions have negligible weighted mass on the \(BK/\log B\) scale.

On the remaining true pairs,
\[
P_z=2^J,\qquad J=\#\{p\ge z:p\equiv1\bmod4,\ p\mid u(u+k_i)\}.
\]
Here \(J\le80s+1\) for large \(B\). Define the **raw** factorial sums \(F_{r,j}=\sum_r P_z\binom{J}{j}\). Alternating binomial truncation gives the sufficient signed test
\[
\sum_{j=0}^{2h+1}(-1/2)^jF_{0,j}
-
\sum_{j=0}^{2h}(-1/2)^jF_{-,j}
\gg BK/\log B.
\]
The odd truncation bounds the first class from below, and the even truncation bounds the second from above. Using label-normalized weights in this formula instead bounds a label-weighted distinct count. At fixed \(s\), all moments through the height cap recover the reciprocal sum.

### A signed result on the actual grid

Fix \(L>1\), put \(Y=z^L\), and write \(J_{\rm band}\) for the count restricted to \([z,Y)\). For any fixed stratum \(j\), the raw \(P_z\)-mass with \(J_{\rm band}=j\), as a fraction of the raw \(P_z\)-mass, is within any prescribed error of
\[
e^{-\lambda}\lambda^j/j!,\qquad \lambda=2\log L,
\]
uniformly on each admissible label and class, by taking \(s\) sufficiently large and then \(B\) large.

The proof uses the full-window CRT count. At a marked split prime \(p\nmid k_i\), the local fraction is \(2(2p-1)/(p(p+1))=4/p+O(p^{-2})\). For a fixed number \(m\) of distinct marks the main factors multiply. The summed distribution error is \(X^{3/2+o(1)}D^5Y^{5m}\), with \(X=\sqrt B\) and \(D=X^{1/20}\), so \(s>mL\) leaves a power saving. Mertens gives the factorial moments of mean \(2\log L\) to the required accuracy. To isolate a fixed \(j\), truncate
\[
\mathbf1_{J_{\rm band}=j}
=\sum_{\ell\ge0}(-1)^\ell
\binom{j+\ell}{j}\binom{J_{\rm band}}{j+\ell}
\]
at successive even and odd orders. This argument uses finitely many controlled CRT statistics for each fixed \(L,j\) and accuracy. [Kloosterman bound, equation (1.4)](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70291), [Shared sieve bounds, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

The full-window local factors at \(7\) are 64 throughout \(r_0\), and 64, 56, 0 on respectively 98, 7, 42 cells in \(r_-\). The raw label factor multiplying them is common to the two classes, bounded below, and has bounded grid mean. For the latter, expand the odd inert divisor factor with weight \(1/d\), and use the hit bound \(O(1/\log d+1/a)\) along the \(x\)-axis. The inert divisor weights up to \(t\) sum to \(O(\sqrt{\log(2t)})\). Thus the 42 blocked cells supply a positive raw main-term gap large enough to absorb a sufficiently small relative error. The same argument gives a positive raw weighted gap within every fixed \(J_{\rm band}=j\).

Removing the band’s multiplicity **exactly** gives \(P_Y\):
\[
P_z\prod_{\substack{z\le p<Y\\p\equiv1\ (4)}}
\frac1{(v_p(u)+1)(v_p(u+k_i)+1)}=P_Y.
\]
The mass in each class falls by a factor \(1/L\) to arbitrarily small fixed relative error, and the raw gap at cutoff \(Y\) is \(\gg BK/\log Y\). The remaining reciprocal concerns the primes at least \(Y\).

### A quantitative moment obstruction

One can preserve moments of both the count and the multiplicity. For requested orders \(d,m\), choose a power of two \(q\ge4(d+1)+1\) and form
\[
C(t)=\prod_{\ell=0}^{m}(1-t/q^\ell)^{d+1}
    =\sum_j(-1)^j c_jt^j.
\]
The even and odd \(c_j\)'s have equal total mass. Normalize each to a probability law on \(Q=q^j,\ J=j\log_2q\). The two laws agree on every mixed moment \(\mathbb E[J^iQ^\ell]\) with \(i\le d,\ell\le m\), since \((t\partial_t)^iC(q^\ell)=0\).

Their reciprocal expectations have ratio
\[
\frac{1+\rho}{1-\rho},\qquad
\rho=\frac{C(1/q)}{C(-1/q)}
\ge1-\frac{2(d+1)}{q-1}\ge\frac12.
\]
Thus they differ by a factor of at least three. Assigning these laws to the two classes in opposite orders reverses the reciprocal-weighted sign while preserving the phase masses and all the stated moments. In particular it reverses the sign for the label-normalized phase ratio \(24/17\). For a specified raw mass ratio, increasing \(q\) permits a larger reciprocal contrast.

These are synthetic moment controls with maximum count \((d+1)(m+1)\log_2q\), inside the necessary height cap for sufficiently small power cutoffs. They show what the moment data alone leave undecided. They do not prescribe the distribution on the actual grid.

### Exact real control

This true \(r_-\) pair has one split factor in \([13,19)\) and a further split factor beyond that band. Both have exact depth one in the anchor and are absent from the alternative. The same target has the blocked label \(T\).

```python
from math import isqrt

a,b = 7864,5368
A,B = 3**a,5**b
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
S,T = 3**1144+5**1212,3**1064+5**1086
k,rem = divmod(S0-S,405)
assert rem==k%8==0
mid = ((lo-S0)//405+(hi-S0)//405)//2
m = (isqrt(mid+k)-isqrt(mid))//2+4
w,e = divmod(k//4,m)
w,e = w+4,e-4*m
u = 9*((w-m)**2+(e-1)**2)
v = 9*((w+m)**2+(e+1)**2)
n = S0+45*u
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
assert lo<n<=hi and n%49==r==45
assert n-S==45*v and (n-T)%49==7
assert (u%17**2,v%17,u%37**2,v%37)==(238,2,37,35)
```

At this pair the exact band removal divides the proxy weight by two, and the remaining reciprocal still has a factor \(1/2\) from \(37\).

Independent BigInt verified the exact ordinary pair and both depth-one split factors, and checked all mixed moments and the reversal margin in the explicit synthetic case d=m=2, q=16. The synthetic laws certify insufficiency of those moment summaries, not reversal for the actual exponent grid.
