# Full-window Gaussian weights and the multiplicity barrier

Covering the whole ordinary window removes the height-box support gap. The remaining split primes still create substantial multiplicity. For the full-support Gaussian proxy \(P_z\), with \(z=B^{1/(40s)}\) and sufficiently large fixed \(s\), I obtain in both target classes
\[
\boxed{\frac{\sum P_z^2}{\sum P_z}>\frac{23}{10},
\qquad
\frac{\sum P_z}{T_r}>\frac75,}
\]
where \(T_r\) counts distinct true target–label pairs. The original mixed moment certificate fails for all sufficiently large fixed \(s\), regardless of box coverage. The sign of \(T_0-T_-\) remains open.

### Full-window coverage

Keep the original 147 compatible phases, \(n=S_0+45u\), and \(k=(S_0-S_i)/45\). Here \(8\mid k\) and \(k=S_0/45+O(B^{1/3})\). The proxy \(P_z\) counts all ordered Gaussian representation pairs for \(u,u+k\) satisfying the split-prime orientation tests below \(z\), divided by \(16\).

For an ordered pair of vectors, use their **raw** difference \(g(m,d)\), where \((m,d)=1\), and their sum \((w,e)\). Then
\[
mw+de=k/g,\qquad (w,e)\equiv g(m,d)\pmod2.
\]
Pivot on the larger raw coordinate difference. It has magnitude \(\asymp\sqrt B\) because \(k\asymp B\) and all four sum and difference coordinates are \(O(\sqrt B)\). The two pivot regions are disjoint by assigning ties to the first. Swapping coordinates in the second region exchanges the Gaussian orientation, with the same local counts.

The previous distribution argument extends to \(q=98\ell\), including extra split primes in \(\ell\). Use \(h\) equal to the **entire part of \(q\) supported on primes dividing \(m\)**. The congruence is \(de\equiv k/g-mw_0\bmod mh\), and the progression step \(q/h\) is coprime to \(m\). The zero-frequency count remains \(\varphi(mh)/\varphi(h)\). The same Kloosterman estimate and gcd-weighted completion give \(O(\ell^4X^{3/2+o(1)})\) error per \(g\) and modulus, where \(X=\sqrt B\). Contents \(g>X^{1/20}\) contribute \(O(\sum_{g\mid k,\ g>X^{1/20}}B/g)=X^{2-1/20+o(1)}\). For fixed \(g,m,d\), the admissible \(e\)'s occupy one class modulo \(|m|\), which gives this bound. [Kloosterman bound, equation (1.4)](https://londmathsoc.onlinelibrary.wiley.com/doi/full/10.1112/jlms.70291)

In scaled coordinates, approximate each whole pivot region by inner and outer rectangles. The volume element is \(dm'\,dd'\,de/|m'|\), where \((m',d')=g(m,d)\). The normalized pivot stays bounded away from zero. For fixed \(m',d'\), the expression for \(u\) is quadratic in \(e\), with leading coefficient at least \(1/4\). A mesh of width \(\delta\) therefore costs \(O(\sqrt\delta)\) in relative volume at the window endpoints. The pivot boundary costs \(O(\delta)\). These estimates are uniform for the actual shifts, which differ from \(S_0/45\) by \(O(B^{1/3})\). This gives common inner and outer counts for every label and both classes, with arbitrarily small fixed relative error. [Shared upper and lower sieve weights, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

The local factors simplify after summing the depth of \(g\).

- At \(2\), for \(t=v_2(k)\ge3\), the parity factor is \((1+3\sum_{j=1}^{t-1}2^{-j})/6\). At depth zero there is one primitive parity row. At depths \(1\le j<t\) there are three, and at \(j=t\) there are none.
- At \(7\), in units of 49 residue pairs, the factor is **64** for a unit alternative, **56** for an alternative zero modulo \(49\), and **0** for depth one. If \(7\mid k\), the primitive depth-zero count loses eight coincident vectors. The positive-depth terms restore exactly \(8(6\sum_{j=1}^{t-1}7^{-j}+7^{1-t})=8\), where \(t=v_7(k)\). To count those terms, the unit anchor gives eight sum vectors modulo \(7\). Each has six or seven primitive difference rows according as \(k/g\) is zero or nonzero modulo \(7\), and each solution lifts 49 ways.
- At the sifted split primes, summing depths gives \((p-1)/(p+1)\) as before. Other odd primes apart from \(7\) contribute their divisor factors, common to the two classes for each label.

Dividing by the parity and nonsifted divisor factors gives a **full-support label-normalized weighted** comparison. Its main-term ratio is
\[
\frac{147\cdot64}{98\cdot64+7\cdot56}=\frac{24}{17}.
\]
Thus the normalized weighted ratio exceeds \(7/5\) with suitably small sieve and mesh errors.

### The extra statistic and the obstruction

Under the probability measure proportional to the **raw** \(P_z\) in either class, count
\[
J=\#\{p\equiv1\bmod4:\ z\le p<z^2,\ p\nmid k,\ p\mid u(u+k)\}.
\]
At such a prime, the local fraction of ordered representation pairs counted by the condition is
\[
\frac{2(2p-1)(p-1)}{p(p^2-1)}
=\frac4p+O(p^{-2}).
\]
The two norms cannot both vanish since \(p\nmid k\). A zero norm has \(2p-1\) representations modulo \(p\), and a nonzero norm has \(p-1\).

One or two of these prime conditions can be inserted into the same CRT count. Their densities multiply in the main term. With \(D=X^{1/20}\), the summed two-prime distribution error is bounded by \(X^{3/2+o(1)}D^5(z^2)^{10}=o(B/\log B)\). Primes dividing \(k\) change the density sum by \(o(1)\) uniformly. Mertens in the split progression gives, to within arbitrarily small fixed relative error for sufficiently large \(s\),
\[
\mathbb E_{P_z}J=2\log2,\qquad
\mathbb E_{P_z}[J(J-1)]=(2\log2)^2.
\]
These are estimates from the one- and two-prime counts. No independence assumption on true pairs is needed.

Since \(P_z\ge2^J\), the first estimate gives \(\sum P_z^2/\sum P_z\ge1+\mathbb E_{P_z}J>23/10\). The two estimates give \(\Pr_{P_z}(J\ge1)>4/7\) by Cauchy–Schwarz. Hence \(T_r/\sum P_z=\mathbb E_{P_z}(1/P_z)<5/7\), proving the second bound.

There is also a direct obstruction to the previous **mixed** criterion. The full-window count gives \(\Pi_-=\sum_{r_-}P_z\gg BK/\log z\gg sBK/\log B\), with an absolute implied constant for sufficiently large \(B\) depending on \(s\). The distinct-pair upper bound is \(T_0\ll BK/\log B\), independently of \(s\). Its per-label correction \(\prod_{p\mid k,\ p\equiv3(4)}(1+1/(p-2))\) has bounded grid mean by the divisor expansion and the order bound along a phase. Therefore every weight supported on true pairs satisfies
\[
\frac{W_0^2}{M_{2,0}}-\Pi_-
\le T_0-\Pi_-<0
\]
for sufficiently large fixed \(s\). Better coverage alone cannot make this certificate positive in that cutoff range. [Distinct-pair upper bound input, Theorem 3.1](https://arxiv.org/pdf/2403.19320#page=4)

### Exact control

This real \(r_-\) target has a true alternative \(S\) and a blocked alternative \(T\). At the finite cutoff \(z=13\), the primes \(17,37\) both contribute to \(J\), so one distinct pair has proxy weight at least four.

```python
from math import isqrt

a,b = 7864,5368
A,B = 3**a,5**b
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
S,T = 3**1144+5**1212,3**1064+5**1086
k,rem = divmod(S0-S,405)
assert rem == k%8 == 0

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
assert all(u%p==0 and v%p!=0 for p in (17,37))
```

Independent BigInt checked the exact true and blocked remainders, the unsifted split-prime multiplicity control, the local pair formula at four primes, and the strict moment margins. The normalized comparison and the raw moment estimates use different weights. Neither gives the sign of the distinct true counts.
