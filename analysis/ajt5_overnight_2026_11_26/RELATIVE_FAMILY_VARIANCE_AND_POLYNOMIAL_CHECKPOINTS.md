# Relative-family variance and polynomially spaced checkpoints

For the actual \(3,5\) phase martingale and each fixed earlier panel \(\mathcal G_{x_0}\),
\[
\Pr(0<\alpha_z<1/\log z\mid\mathcal G_{x_0})
 \ll_{x_0}(\log\log\log z)^{-c}
\]
for some effective absolute \(c>0\), uniformly in that panel's observed target values. This improves the previous inverse-tower-scale checkpoint estimate. The argument does not prove that the limiting modular obstruction mass is zero or that every specified integer admits a representation.

## Relative conditional variance

Let \(A_x\) be the phase family surviving the tests through \(x\), with Haar mass \(\alpha_x\), and let \(H_x=\alpha_x/D_x\), where \(D_x=\frac12\prod_{p\le x,\ p\equiv3\bmod4}p/(p+1)\). Use the [support-pair kernels](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5) and the [earlier floor and uniform second moment](EFFECTIVE_LOW_PHASE_MASS_CHECKPOINTS.md). For \(w\ge y\ge x^{16}\) and \(\alpha_y>0\),
\[
\operatorname{Var}(H_w/H_y\mid \mathcal G_y)
 \ll \frac{\alpha_x}{\alpha_y}\frac{\log x}{\log y}
 \ll \frac{H_x}{H_y}\sqrt{\frac{\log x}{\log y}}. \tag{1}
\]

Fix a first phase, and draw the second uniformly from \(A_x\). Membership in \(A_x\) is measurable in both exponents' primary coordinates through \(x\); coordinates above \(x\) remain independent Haar. At an inert prime \(q>y\), fix these old coordinates and the entire second \(3\)-exponent. Collision of the shifts fixes at most one residue of the second \(5\)-exponent modulo \(o_q=\operatorname{ord}_q(5)\), so its conditional probability is at most the reciprocal of the part of \(o_q\) supported on primes above \(x\).

In \(U<q\le2U\), set aside \(o_q\le U^{1/3}\) and \((q-1)_{\le x}\ge U^{1/6}\). The first count is \(O(U^{2/3}/\log U)\), by grouping the prime divisors of \(5^j-1\) for \(j\le U^{1/3}\). In the second set the clipped weight \(\sum_{r\le x,\ r^a\mid q-1,\ r^a\le\sqrt U}\log r\) is at least \((\log U)/6\). This is immediate if there is no clipping; otherwise a clipped factor already contributes at least \(\log(\sqrt U/x)\). Interval Brun–Titchmarsh bounds the count by \(O(U\log x/(\log U)^2)\): for each \(r^a\le\sqrt U\) use \(4U/(\varphi(r^a)\log U)\), then sum the weights. Thus the set-aside primes' reciprocal charge is \(O(\log x/\log y)\). The remaining primes have a free order part \(>U^{1/6}\).

The pair-kernel product is bounded by \(\prod_q(1+\mathbf 1_{\rm collision}/(q-1))\). Pay for the set-aside primes deterministically, at multiplicative cost \(1+O(\log x/\log y)\). In the other factors expand by the largest selected prime and bound the smaller factors by the deterministic Mertens product (even the all-prime \(O(\log q)\) bound suffices). The expected excess for this part is \(O(y^{-1/6}\log y)\); the argument uses just one collision expectation per term and never samples fresh phases at successive primes. The expected total excess is now \(O(\log x/\log y)\), uniformly in the fixed first phase. Restrict the second phase from \(A_x\) to \(A_y\) at cost \(\alpha_x/\alpha_y\), using nonnegative excess. Average over the first phase in \(A_y\) at no additional cost. This proves the first bound; the second uses \(D_x\asymp(\log x)^{-1/2}\). Sources: [Montgomery–Vaughan](https://personal.science.psu.edu/rcv4/personal/Publications/large_sieve.pdf) and [Williams](https://people.math.carleton.ca/~williams/papers/pdf/057.pdf).

## Crossing argument

Choose a fixed power of two \(x_0\ge 2^{14}\) containing any primes under prior conditioning. Set \(x_{j+1}=x_j^{16}\), keep checkpoints through the last \(x_k\le(\log\log z)/(24\log2)\), and append \(z\). Every positive nonterminal head is at least \(2^{-6x_j}\ge(\log z)^{-1/4}\). On the event in the theorem the terminal head is positive and \(O((\log z)^{-1/2})\).

At each positive restart point \(j\) independently draw \(u\) uniformly in \([\eta,2\eta]\), and restart at the first later head below \(uH_{x_j}\), with the terminal head included. Zero or absence of a crossing stops the active process. The previous uniform conditional second moment gives a fixed \(p_0>0\) lower bound for \(H_z\ge H_{x_j}/2\). At a crossing the conditional probability of this event is at most \(2u\) by the martingale property, also at a terminal crossing. Hence the crossing probability is at most \(1-p_0/2\) if \(4\eta\le p_0/2\).

For a crossing more than \(m\ge1\) checkpoints later, either there is no such index or the intermediate checkpoint \(y=x_{j+m}\) is nonterminal and \(H_y/H_{x_j}\ge u\). The chance it lies in \([u,u+\delta]\) is at most \(\delta/\eta\), by independent randomization of the threshold. If it is larger, a subsequent crossing forces normalized deviation at least \(\delta/(2\eta+\delta)\), while the conditional variance (1) is \(O_\eta(16^{-m/2})\). The martingale maximal inequality and \(\delta=16^{-m/6}\) give an exponentially small upper bound \(O_\eta(16^{-m/6})\) on such delayed crossings. All bounds are conditional on the history up to the restart, before drawing its threshold.

For sufficiently small effective \(\lambda>0\), the conditional expected \(e^{\lambda\ell}\) on the crossing event, where \(\ell\) is the number of checkpoint steps to the crossing, is at most 1: at \(\lambda=0\) there is a fixed deficit, and the uniform exponential tail controls the increase. The weight \(e^{\lambda j}\) at successive restarts is therefore a supermartingale if unsuccessful paths receive zero and terminal arrivals retain their weight. The terminal-arrival probability is at most \(e^{-\lambda(k+1)}\). Every threshold sequence reaches the terminal checkpoint on the positive low-mass event for large \(z\), by the positive floor and the terminal upper bound. Since \(k=\lfloor\log_{16}(\log((\log\log z)/(24\log2))/\log x_0)\rfloor\), this gives the announced rate.

For the full obstruction mass \(\beta_{\mathcal C}\) in an earlier class \(\mathcal C\), the same rate bounds \(\beta_{\mathcal C}-\Pr_{\mathcal C}(\alpha_z=0)\) after adding \(18/\sqrt z\), by the earlier variance estimate on \(\alpha_z\ge1/\log z\) and the verified zero-atom identity. This is a quantitative approximation to the obstruction mass; no change to its numerical bound is claimed.

## Independent exact control

At a genuine cell, the old exponent cylinder modulo 90 fixes the prime-to-local-prime order residues at the inert primes 3, 7, 11 and 19, but need not fix their full support tests. At \(q=47\), the \(5\)-order is 46; with fixed first axis, one old residue class gives exactly one collision in the free 23-point orbit while the opposite-parity class gives none. The test illustrates the order mechanism, not the asymptotic tail bound.

~~~javascript
const n = 10000804849n;
function pw(b,e,m) { let a=1n; while(e--) a=a*b%m; return a; }
const check = x=>{ if(!x) throw Error("assert"); };
check(n-3n**3n-5n**5n===100004n**2n+41n**2n);
let d=1; while (pw(5n,d,47n)!==1n) ++d;
check(d===46);
function hits(j) {
  return Array.from({length:23},(_,i)=>i)
    .filter(i=>pw(5n,j+90*i,47n)===pw(5n,5,47n));
}
check(hits(5).join(",")==="0");
check(hits(4).length===0);
~~~
