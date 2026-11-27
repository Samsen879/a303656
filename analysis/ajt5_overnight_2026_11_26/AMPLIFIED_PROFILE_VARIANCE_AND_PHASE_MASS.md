# Phase mass and decaying conditional variance after a prime panel

**Revealing primes gives a decaying conditional variance on almost every surviving branch.** More precisely, after reading all primes through \(z\), any selected exponent subfamily of Haar mass \(a>0\) has a normalized unread-prime profile with conditional variance at most
\[
\boxed{\frac{18}{a\sqrt z\log z}}\qquad(z\ge 2^{14}).
\]
This bound holds uniformly in the earlier readings and in the selected subfamily. For the canonical family of all surviving phases, its mass is asymptotic to a positive, target-dependent multiple of \((\log z)^{-1/2}\) almost everywhere off the modular obstruction union. The resulting conditional variance is \(O_n((z\log z)^{-1/2})\). There is also a sharp one-prime loss in an actual ordinary-height \(3,5\) family.

### Uniform amplification after a prime panel

Let \(\mathcal G_z\) reveal the complete target coordinates \(n_p\) for \(p\le z\). Given these readings, choose a measurable exponent family \(A\) of mass \(a\) in \(\widehat{\mathbb Z}^2\). Let \(T_{z,A}\) average the unread local norm densities over normalized Haar measure on \(A\), taking the limit over finite unread panels. Its conditional mean is 1.

To bound its second moment, fix one phase \(\theta\) and draw the second phase \(\phi\) from full Haar measure. Write \(I_q\) for equality of their actual shifts modulo \(q\). After fixing the second \(5\)-exponent, a collision fixes at most one class of the second \(3\)-exponent modulo \(\operatorname{ord}_q(3)\). For \(q>z\) the norm pair kernel is bounded by \(1+I_q/(q-1)\). Expanding the product by its largest selected prime therefore bounds the mean excess over 1 by
\[
\sum_{q>z}
\frac{1}{(q-1)\operatorname{ord}_q(3)}
\prod_{z<p<q}\frac p{p-1}
\le
\frac{2}{\log z}
\sum_{q>z}\frac{\log q}{(q-1)\operatorname{ord}_q(3)}.
\]
The denominator \(\log z\) follows because the Euler product through \(z\) contains the harmonic sum through \(z\). The numerator uses the explicit Mertens product upper bound. In a dyadic block \((U,2U]\), the orders up to \(\sqrt U\) contribute at most \((\log3)/\sqrt U\), by grouping primes dividing \(3^o-1\) at each order \(o\). The longer orders contribute at most \(2\log2/\sqrt U\), since the product of primes in the block divides \(\binom{2U}{U}\). Summing gives \(18/(\sqrt z\log z)\), uniformly in the first phase. Restricting the second draw to \(A\) costs at most \(1/a\) on this nonnegative excess. The finite-panel bounds give the asserted \(L^2\) limit and variance. [Verified local pair kernels](https://github.com/Samsen879/a303656/blob/c6236506eedd64362571564f33c8f43bd50cb691/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_PROFINITE_LIMIT.md) · [Explicit Mertens bound](https://doi.org/10.1215/ijm/1255631807)

The same argument controls the **full profile** \(F\). Put \(F_z=\mathbb E(F\mid\mathcal G_z)\), and let \(W_z(\theta)\) be the product of the observed norm densities. For the symmetric excess kernel, \(2W_z(\theta)W_z(\phi)\le W_z(\theta)^2+W_z(\phi)^2\) gives
\[
\operatorname{Var}(F\mid\mathcal G_z)
\le \frac{18\pi^2}{\sqrt z\log z}\int W_z^2.
\]
The integral divided by \(2\prod_{3\le p\le z}(1+1/p)\) is a mean-one nonnegative martingale. Indeed, integrating each new target coordinate gives the same squared local norm mean for every phase. The martingale is almost surely bounded along the prime reads, and its denominator is \(O(\log z)\). Since \(F_z\to F\), this proves
\[
\frac{\operatorname{Var}(F\mid\mathcal G_z)}{F_z^2}
=O_n(z^{-1/2})\qquad\text{almost surely on }\{F>0\}.
\]

### The surviving mass and the exact obstruction

Let \(\alpha_z\) be the mass of **all** phases passing the exact norm-support tests at 2 and the inert primes through \(z\). Put
\[
D_z=\frac12\prod_{\substack{p\le z\\p\equiv3\pmod4}}\frac p{p+1}.
\]
The ratio \(\alpha_z/D_z\) is the conditional mean of \(F/\pi\) given those target coordinates. At each observed prime the local density is constant on its support, and each unobserved density integrates to 1. Consequently \(\alpha_z/D_z\) tends almost surely to a limit \(H\). The verified zero-atom identity implies \(H=0\) exactly where \(F=0\), up to null sets. The obstruction union is measurable in the 2-adic and inert coordinates because split primes impose no norm-support restriction. Since \(D_z\sim D/\sqrt{\log z}\) for some \(D>0\),
\[
\alpha_z\sim \frac{DH(n)}{\sqrt{\log z}}
\quad\text{on }\{F>0\},
\qquad
\alpha_z=0\text{ eventually on }\{F=0\}.
\]
Thus bare phase mass does go to zero even on surviving branches. Its natural decay is slow enough for the relative variance to go to zero. [Verified zero-atom identity](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e) · [Mertens in arithmetic progressions](https://doi.org/10.1016/0022-314X(74)90032-8)

The test on \(\alpha_z\) is finite. Take \(L_z=\operatorname{lcm}(2,\{p-1:p\le z\})\). On fixing the two exponents mod \(L_z\), the shift at \(p\le z\) is uniform in a ball of depth \(\min_{b\in\{3,5\},\,p\nmid b}v_p(b^{L_z}-1)\), by lifting the unit powers. These balls are independent across the panel after fixing the coarse phases. Averaging the norm-support indicators over them computes \(\alpha_z\) from that finite target modulus. Any earlier finite read at the same primes can be retained by taking the lcm with its modulus.

**Sharp local loss.** At a new ordinary inert prime \(q\), suppose the surviving phase family leaves the ordinary axis’s \(q\)-primary coordinate free. If a fraction \(r\) of its phases collide with the target mod \(q\), the exact retained fraction after the full read is
\[
1-\frac{q}{q+1}r.
\]
Among colliding phases the remainder is uniform in \(q\mathbb Z_q\), whose even-valuation probability is \(1/(q+1)\). The case \(r=1\) occurs at \(q=11\) in the actual family \(c,d\equiv5\bmod90\). Set \(X=5^{550}\), let \(x\) be the least multiple of \(8778\) at least \(5^{275}\), and put \(n=x^2+121+3^{185}+5^{275}\). The whole anchored family passes the old \(2,3,7,19\) tests and collides at 11. The full read retains exactly \(1/12\). In the ordinary-height box at this same \(n\), \((185,275)\) gives the true norm \(x^2+121\), while \((185,185)\) gives exact valuation 1 at 11.

### Consequence for logarithmic matchings

For any previously certified fixed target class \(\mathcal C\) supported on \(2,3,5,7,19\), define \(B_z=\prod_{p\le z,\ p\equiv1\ (4)}(1-1/p)\) and \(K_z=\pi B_z/D_z\to8\). On \(\alpha_z>0\), the observed split-prime lower bounds give \(F\ge K_z\alpha_z T_{z,A_z}\). Using the verified conditional bound \(\mathbb E(G\mid\mathcal C)<3000\), Cantelli, Markov, and the capped matching transfer yield, for each fixed \(z\),
\[
\limsup_{X\to\infty}\Pr_{\mathcal C,X}
 \left(\nu_X<\frac{K_z^2}{4\sqrt z(\log z)^2}\log X\right)
\le
\Pr_{\mathcal C}\!\left(\alpha_z<\frac1{\log z}\right)
+\frac{3072}{\sqrt z}.
\]
Here the two error contributions use \(T_{z,A_z}>1/2\) and \(\alpha_z\ge1/\log z\). The finite residue probability on the right tends to the exact conditional obstruction mass. This gives a polynomial read-depth error **outside the measured low-mass classes**. A uniform rate for the measure of those classes approaching the zero atom, and a pointwise representation theorem, remain open. [Verified conditional energy bound](https://github.com/Samsen879/a303656/commit/9c56fd1f5368e11d2445897762f52001571f8555) · [Capped matching transfer](https://github.com/Samsen879/a303656/commit/c92bb115bf6404a70b1344d2337835f108e4db7e)

The event \(F=0\) is measurable in the 2-adic and inert coordinates by the already proved eventual blocker identity, so its conditional expectation over the remaining split coordinates gives the same zero event almost surely. The variance estimate requires selection using the observed coordinates only. It is not a uniform target-independent lower bound on phase mass and does not assert a rate for the approach to the zero atom.

### Independent BigInt replay

```javascript

const mod=(x,m)=>(x%m+m)%m;
function pw(x,n,m){let r=1n;x=mod(x,m);for(;n;n>>=1n,x=x*x%m)if(n&1n)r=r*x%m;return r;}
function iv(a,m){let b=m,x=1n,y=0n;a=mod(a,m);
  while(b){const q=a/b;[a,b]=[b,a-q*b];[x,y]=[y,x-q*y];}
  if(a!==1n)throw Error("inverse");return mod(x,m);}
const check=(x)=>{if(!x)throw Error("assert");};
const isPrime=(p)=>{for(let i=2n;i*i<=p;++i)if(p%i===0n)return false;return p>1n;};
function crt(rows){let x=0n,M=1n;for(const [m,v] of rows){x+=M*mod((v-x)*iv(M,m),m);M*=m;}return [x,M];}

const X=5n**550n,z=5n**275n;
const x=8778n*((z+8777n)/8778n),n=x*x+121n+3n**185n+5n**275n;
check(X<n&&n<=2n*X&&n%11n!==0n);
for(const [c,d] of [[185n,275n],[185n,185n]]){
 const a=3n**c,b=5n**d;
 check(X<=a**8n&&a**4n<=X&&X<=b**3n&&b*b<=X);
}
check(n-3n**185n-5n**275n===x*x+121n);
const bad=n-3n**185n-5n**185n;check(bad%11n===0n&&bad%121n!==0n);
for(const p of [8n,7n,19n,11n]){
 ckOrder(3n,p);ckOrder(5n,p);
}
function ckOrder(b,m){check(pw(b,90n,m)===1n);}
const r8=mod(n-3n**5n-5n**5n,8n);check(r8%4n===1n);
check(mod(n-5n**5n,3n)!==0n);
check([7n,19n].every(p=>mod(n-3n**5n-5n**5n,p)!==0n));
check(mod(n-3n**5n-5n**5n,11n)===0n);
check(pw(5n,10n,121n)!==1n);
```
