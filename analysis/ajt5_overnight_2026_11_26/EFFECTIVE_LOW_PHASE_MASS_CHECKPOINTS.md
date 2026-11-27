# Effective low-phase-mass bounds via sparse checkpoints

**The positive low-mass classes have an effective uniform bound.** For the actual \(3,5\) phase martingale,
\[
\Pr\!\left(0<\alpha_z<\frac1{\log z}\right)
=O\!\left(e^{-c\log^* z}\right)
\]
for an absolute \(c>0\). The bound holds after any fixed finite set of earlier target reads once the first checkpoint contains those primes. It also gives a rate for the mass of modular obstructions that a finite panel has yet to detect. The rate is very slow.

### Explicit bound

Let \(\mathcal G_x\) reveal the complete target coordinates at primes through \(x\). Use the verified support mass \(\alpha_x\) and its mean-one normalization
\[
D_x=\frac12\prod_{\substack{p\le x\\p\equiv3\pmod4}}\frac p{p+1},
\qquad H_x=\frac{\alpha_x}{D_x}.
\]
Set \(x_0=2^{14}\), \(x_{j+1}=2^{24x_j+4}\), and let \(k\) be the largest index with \(x_k\le\log z\). For \(k\ge1\), put \(i=\lfloor k/2\rfloor\). Then, almost surely,
\[
\boxed{\quad
\Pr\!\left(0<\alpha_z<\frac1{\log z}\,\middle|\,\mathcal G_{x_i}\right)
\le
R(z):=\min\!\left\{1,\,
(1-2^{-82})^{k-i}
+\frac{9216}{x_i^{1/4}\sqrt{\log x_i}}\right\}.
\quad}
\]
This conditions on the full earlier panel, including arbitrary depths at its primes. The number of checkpoints is comparable to \(\log^* z\). [Verified support mass and variance](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5)

### Proof

**A positive head has a uniform floor.** Fix both exponent residues modulo \(L_x=\operatorname{lcm}(2,\{p-1:p\le x\})\). The local shift balls are independent across the panel after this choice. At an inert prime \(p\), the smallest positive average of the normalized norm density on a ball is \(1/p\). It occurs when the ball is centered at the target and starts at odd valuation depth. At 2, the smallest positive average is 1. Therefore one surviving pair of coarse exponent residues contributes at least
\[
H_x\ge L_x^{-2}\prod_{\substack{p\le x\\p\equiv3\pmod4}}p^{-1}.
\]
For \(x\) a power of two, \(\log\operatorname{lcm}(1,\ldots,x)\le2x\log2\), by summing the central-binomial bound over dyadic intervals. Thus \(H_x>0\) implies \(H_x\ge2^{-6x}\). [Verified finite-ball construction](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e)

**Each positive checkpoint has a uniform chance to reach the next checkpoint above its threshold.** The uniform conditional second-moment bound from the zero-atom proof applies to \(H\) by using only the unread inert factors in the same product majorant. One may take
\[
\mathbb E(H_y^2\mid\mathcal G_x)\le 2^{80}H_x^2
\qquad(y\ge x\ge2^{14}).
\]
Conditional Paley–Zygmund gives probability at least \(2^{-82}\) of \(H_{x_{j+1}}\ge H_{x_j}/2\) when \(H_{x_j}>0\). The schedule ensures \(H_{x_j}/2\ge x_{j+1}^{-1/4}\). Call a checkpoint good when \(H_{x_j}\ge x_j^{-1/4}\). Zero is absorbing, so the conditional probability of \(H_z>0\) with no good checkpoint from \(i\) through \(k\) is at most \((1-2^{-82})^{k-i}\).

**A good checkpoint controls the final low-mass event.** The verified variance estimate applied to the surviving family at \(x\), with only inert primes in the unread panel, gives
\[
\operatorname{Var}(H_z/H_x\mid\mathcal G_x)
\le \frac{18}{\alpha_x\sqrt x\log x}
\quad\text{on }H_x>0.
\]
The explicit bound \(D_x\ge1/(128\sqrt{\log x})\) holds for \(x\ge2^{14}\). To obtain it, take \(s=1+1/\log x\). The square of \(\prod_{p\equiv3\ (4)}(1+p^{-s})\) is at most \(\zeta(s)/L(s,\chi_4)\le3\log x\). Changing \(p^{-s}\) to \(1/p\) through \(x\) costs a factor below 32 by \(\sum_{p\le x}\log p/p\le4\log2(1+\log x)\), from the same dyadic binomial bound.

At a good checkpoint \(x\le\log z\), the event \(\alpha_z<1/\log z\) forces \(H_z<H_x/2\), since \(128/\sqrt{\log z}\le \tfrac12 x^{-1/4}\) when (xge 2^{32}). For (i=0) the displayed bound is (R(z)=1) and requires no such comparison; for (ige1) the checkpoint is already above (2^{32}). Chebyshev bounds its conditional probability by \(9216/(x^{1/4}\sqrt{\log x})\). Apply this at the **first** good checkpoint. This uses the conditional bound once and gives the second term of \(R(z)\).

For the numerical second-moment constant, fix both phases’ exponent components at primes through \(x\) in the verified largest-prime expansion. The prime range \((x,x^{16}]\) costs at most 32 by the explicit Mertens bound. In dyadic blocks \((U,2U]\) above \(x^{16}\), orders of 5 at most \(U^{1/3}\) contribute total \(\sum 1/(q-1)<1\) by grouping primes dividing \(5^o-1\). Primes with \((q-1)_{\le x}\ge U^{1/6}\) contribute less than 46. Indeed, the clipped prime-power weight through \(\sqrt U\) is at least \((\log U)/6\) at each such prime, and interval Brun–Titchmarsh bounds their count by \(480U\log x/(\log U)^2\). At the remaining primes the free part of the order exceeds \(U^{1/6}\), so the largest-prime expansion costs less than \(1+8\sum_{m>x^{16}}\log m/m^{7/6}<2\). The combined bound \(64e^{47}<2^{80}\) works uniformly over the fixed exponent components. [Conditional product argument](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e) · [Montgomery–Vaughan](https://doi.org/10.1112/S0025579300004708) · [Rosser–Schoenfeld](https://doi.org/10.1215/ijm/1255631807)

### Consequences and replay

For a fixed earlier class \(\mathcal C\), let \(\beta_{\mathcal C}\) be its conditional measure of the full modular obstruction union. On \(\alpha_z\ge1/\log z\), the conditional probability that the terminal normalized mass is zero is at most \(18/\sqrt z\), by the same variance estimate and the unit deviation from its conditional mean. Hence
\[
0\le \beta_{\mathcal C}-\Pr_{\mathcal C}(\alpha_z=0)
\le R(z)+18/\sqrt z .
\]
In the previously verified conditional matching bound, the finite low-mass term can therefore be replaced by \(\beta_{\mathcal C}+R(z)\). The resulting bound for true logarithmic matchings has error \(R(z)+3072/\sqrt z\) above the obstruction mass, at the coefficient from the verified amplification theorem. A power of \(\log z\) and pointwise coverage remain open. [Verified matching transfer](https://github.com/Samsen879/a303656/commit/d9050a0ef401ac2211911da9ee4ee22d2cfa26e5)

The exact independent replay below checks all 1008 target residues for the 2,3,7 support panel. The mean phase mass is 21/64; the minimum is 21/128, and the minimum normalized head is 1/2.

For the clipped-weight count, the interval Brun–Titchmarsh estimate at moduli at most \(\sqrt U\) is at most \(4U/(\varphi(d)\log U)\). Summing the weights uses \(\sum_{a\ge1}\varphi(r^a)^{-1}\le 4/r\) and \(\sum_{r\le x}(\log r)/r\le4\log 2(1+\log x)\). Dividing by the required \((\log U)/6\) gives the stated conservative 480 constant for \(x\ge2^{14}\). The error rate is effective but extraordinarily slow and says nothing about zero density of the exact obstruction set.

```javascript

const q=504,L=6,Q=1008;
const check=x=>{if(!x)throw Error("assert");};
const mod=(x,m)=>(x%m+m)%m;
function pwr(b,k,m){let a=1;for(let i=0;i<k;i++)a=a*b%m;return a;}
const norms=Array(q).fill(0);
for(let x=0;x<q;x++)for(let y=0;y<q;y++)norms[(x*x+y*y)%q]++;
const shifts=[];
for(let c=L;c<2*L;c++)for(let d=L;d<2*L;d++)
 shifts.push((pwr(3,c,q)+pwr(5,d,q))%q);
const h=Array.from({length:Q},(_,n)=>shifts.reduce((s,z)=>s+norms[mod(n-z,q)],0));
check(Math.min(...h)*2===q*L*L);
check(h.reduce((s,x)=>s+x,0)===Q*q*L*L);
check(2**14<2**32);
```
