# Mixed return points are Sidon; fixed phases admit a weaker modulus

Let \(z=\sqrt{\log X}\), with even-even index box \(0\le i<I,\ 0\le j<J\), where \(I,J\asymp z^2\), and use the external inert prime window Q from [the axial-period proof](AXIAL_PERIOD_AND_MIXED_RETURN.md). A mixed return is an index where \(9^i+25^j\equiv2\) at every q in Q. For sufficiently large X, **no nonzero difference between return points occurs twice**. This holds already modulo the prime product and hence also modulo the squared product.

Indeed, suppose \(P,P+D,R,R+D\) are returns with \(D\ne0,\ P\ne R\). For each distinct large prime \(\ell>z^{11/20}\) from the axial-period proof choose a q whose two base orders both contain \(\ell\). Put \(a=9^{D_1}, b=25^{D_2}\) in the units modulo q. For either starting point its powered coordinates satisfy \(x+y=ax+by=2\). If \(a=b\), they both equal one, so \(\ell\) divides both components of D. If \(a\ne b\), there is a unique \((x,y)\) for the two right-hand sides, so \(\ell\) divides both components of \(P-R\). Each nonzero difference vector has at least one nonzero component and its gcd is \(O(z^2)\). It can contain at most three such distinct \(\ell\) for large z, since the product of four exceeds \(z^{11/5}\). Seven distinct \(\ell\) therefore suffice for a contradiction, and the earlier bound supplies many more. In particular no nontrivial three-term arithmetic progression or parallelogram occurs. On a line with N consecutive admissible integer parameters, the positive differences are distinct and at most \(N-1\); the number of returns is at most \(1+\sqrt{2N}\). This does not forbid an isolated second return.

## The fixed-phase sufficient rule

For a specified genuine origin \(n=2+u^2+v^2\), a q with \(n\equiv0\bmod q\) never hits any even-even cell: a sum of two nonzero squares is nonzero at an inert q. At a remaining q with \(n\not\equiv2\bmod q\), a return modulo q suffices to avoid valuation one, because the difference is a unit. With \(n\equiv2\bmod q\), a return modulo \(q^2\) suffices, since \(n-2\) must itself be zero modulo \(q^2\) for an inert q. This does not require a universal return at all primes simultaneously.

Here is an explicit mixed construction using that distinction. At 11, the orders modulo 121 divide 5 for base 9 and 55 for base 25, and \(9+25^{19}\equiv2\bmod121\). Let E be a subset of Q excluding 11, containing all the other primes to be allowed nonzero phases, and \(B=\operatorname{lcm}_{q\in E}q(q-1)\), with the empty lcm 1. If \((B,55)=1\) and \(55B<\min(I,J)\), the two exponent CRT equations
\[
 i\equiv0\bmod B,\ i\equiv1\bmod5;\qquad
 j\equiv0\bmod B,\ j\equiv19\bmod55
\]
give a non-origin point in the box. It returns modulo \(q^2\) at every \(q\in E\cup\{11\}\). All other phases are chosen zero modulo q; the external certificate therefore misses this point. For instance E can grow with height by taking primes \(q\equiv167\bmod220\) up to \(\log\log X/(10\log\log\log X)\), omitting panel primes. These q are \(3\bmod4\) and neither \(q\) nor \(q-1\) has a factor 5 or 11. The box bound follows even from \(B\le\prod_{q\in E}q^2\) and the trivial bound on how many such primes there are. To realize legal zero phases, impose \(u^2+v^2\equiv-2\bmod q^2\), which is possible by the nonzero norm-fiber lifting argument. The full coordinate CRT still has modulus \(X^{o(1)}\) and the earlier height construction applies.

For an exact small contrast, \((i,j)=(1,19)\) works across all external phase choices at 11 when 7,19,23 have zero phases. At 31 the shifted value \(\delta=9+25^{19}-2\) is a unit (see replay); requiring the coordinate norm to be \(\delta+31\bmod31^2\) produces valuation one without changing any of those phases or the true origin. Thus fixed-window survival is not arithmetic norm survival. Arbitrary fixed phases throughout the full growing window are not settled here.

~~~python
assert pow(9,5,121)==pow(25,55,121)==1
assert (9+pow(25,19,121))%121==2
assert (9+pow(25,19,31)-2)%31!=0
~~~
