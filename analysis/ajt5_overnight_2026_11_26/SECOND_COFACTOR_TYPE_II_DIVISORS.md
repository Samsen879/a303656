# Type II cancellation in the long second-cofactor sum

This extends the controlled part of [the short-divisor estimate](SECOND_COFACTOR_SHORT_DIVISORS.md) for the original nine-prime spectrum. It does not bound the entire signed tail and does not yield a new true-norm lower bound.

Retain \(M_0=480480,\ w=450061,\ h=3^c(3^{24}-1)\), the original residue class of \(z\) modulo \(M_0\), and the prime \(a\asymp X^{1/16}\) in the second cofactor. Write \(C_h(q)=\#\{z\in\mathcal P:z\equiv h\bmod q\}\) for the original positive spectrum \(\mathcal P\), and \(E=\operatorname{rad}(M_0 h)\), a fixed support. For any fixed \(\epsilon,J>0\),
\[
\sum_{a}\sum_{\substack{X^{83/400}<j\le X^{23/50-\epsilon}\\(j,Ea)=1}}
   \chi_4(j) C_h(aj)
   \ll_{\epsilon,J} X(\log X)^{-J}.
\]

Use [Maynard, *Primes in arithmetic progressions to large moduli III*, Proposition 5.3](https://arxiv.org/pdf/2006.08250#page=9) on the convolution of the first eight primes and the last prime \(p_9\asymp X^{27/50}\). The prime sequence is unrestricted within its short fixed-relative-width interval and is Siegel–Walfisz. Use disjoint slots, so the first-eight coefficient is bounded by one. For \(j\asymp X^\kappa\), the split modulus is \(q_1=M_0j,\ q_2=a\). The CRT class \(z\equiv w\bmod M_0,\ z\equiv h\bmod aj\) is primitive, and its reduction modulo \(q_1\) is independent of \(a\). This is the residue-class order required by the two nested suprema in the proposition. The power tests, leaving fixed slack, are
\[
 7\kappa+3/4<4,\qquad 3\kappa-7/8<27/50<1-\kappa .
\]
They hold up to \(23/50-\epsilon\), including when the actual shift \(h\) grows. The hypothesis \(NM\asymp X\) follows from the slot sum. The proposition bounds the sum of absolute distribution errors over each dyadic block; summing the \(O(\log X)\) blocks is harmless.

In the main term, the unrestricted last prime recovers the specified residue modulo \(M_0\) via the prime number theorem in that fixed progression, since the product of the first eight primes is \(1\bmod M_0\). Those primes are in size bands separate from \(a\), and the last prime exceeds \(aj\) throughout this range. The correction omitting first-eight factors dividing \(j\) is negligible: for each such factor \(\ell\gg X^\eta\) for a fixed \(\eta>0\), use \(\sum_{j\le X,\ell\mid j}\varphi(j)^{-1}\ll(\log X)/(\ell-1)\). The main term is then \(|\mathcal P|/(\varphi(a)\varphi(j))\) in the summed estimate.

To see its signed cancellation, \(g(v)=\chi_4(v)1_{(v,Ea)=1}\) has uniformly bounded partial sums by inclusion-exclusion (the support of \(E\) is fixed and \(a\) is prime). Expand \(1/\varphi(j)=j^{-1}\sum_{u\mid j}\mu^2(u)/\varphi(u)\). The resulting convolution, split at \(u=Y\) and summed by parts in \(v\), gives \(\sum_{j>Y}g(j)/\varphi(j)\ll_E\log(2Y)/Y\). This makes the signed main term negligible too. The original smooth hyperbola weight equals one in the added range, which lies a fixed power below the top.

The upper endpoint needed in the original hyperbola is at exponent \(15/32\). The uncontrolled width is thus \(7/800+\epsilon\). At that endpoint the natural split has \(7(15/32)+12(1/16)=129/32>4\). More generally for total modulus exponent \(\rho\), a split admitting Proposition 5.3 would require its first exponent \(b_1\) to satisfy \((12\rho-4)/5<b_1<1-\rho\). This implies \(\rho<9/17<17/32\), so a mere regrouping within this proposition cannot justify the complete tail.
