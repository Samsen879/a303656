# Overlapping Pell periods and an obstruction at a genuine anchor

Continue [the exact index lift](PELL_INDEX_LIFT_AND_PERIOD_DEPENDENCE.md) at the actual extra label \(K=10936\). Its residual at \(n=0\) is the genuine norm \(3554^2+405^2\). Distinct obstruction primes can overlap in their complete periods even when they introduce fresh large factors. There is also a uniform reason that progressively new primes cannot delete a fixed fraction of **every** old surviving class.

## Exact conditional rate

Let L be the lcm of the previous finite sieve periods. For a new simple lift at prime q with \(q\nmid L\), let m be its coarse period, \(R_q\) the active coarse residues, \(g=(L,m)\), and \(b=m/g\). In an old class \(a\bmod L\), the compatible coarse classes have equal weight \(1/b\). Each active one loses \(1-1/q\) to exact valuation one, by the simple lift. Thus the conditional deletion rate is exactly
\[
 (1-1/q)\,\#\{r\in R_q:r\equiv a\bmod g\}/b .
\]
For q outside the finite exceptional set (including divisors of \(2K(K-C)\), \(C=10924\)), there are at most two active classes. In fact \(T=G^{2n}\) traverses a cyclic group of order m and the weak condition is a nonzero quadratic in T (see below). In the simple-lift setting, let \(\gamma_i\) denote the fraction of previously surviving classes compatible with at least one active class. The actual conditional deletion in step i is therefore between \((1-1/q_i)\gamma_i/b_i\) and \(2\gamma_i/b_i\). The product of the remaining fractions tends to zero iff \(\sum_i\gamma_i/b_i\) diverges (no finite deletion is total, and convergence/divergence of the sum governs the product). This is a criterion, not a proof of divergence on the actual orbit. For example if each \(b_i\) contains two primes both new to the accumulated modulus, Cauchy–Schwarz gives \(\sum_i1/b_i\le\sum_i1/(P_iQ_i)<\infty\), as the two prime sequences have convergent reciprocal-square sums.

Actual bias occurs at \(q=1051,9043\), with coarse periods 35 and 2261 and sole active classes 28 and 2065, respectively. The full simple-lift periods \(35\cdot1051\) and \(2261\cdot9043\) meet in the factor 7; both active classes are 0 modulo 7. The old event at 1051 deletes marginal fraction \(30/1051\), or \(210/1051\) conditional on class 0 modulo 7. The new deletion has zero rate outside that class and its average rate given old survival is only \(841/1021\) of its own marginal rate, by CRT conditional on the shared digit. This is despite its several new factors.

## Anchor obstruction via a resultant

For \(\alpha=3577+1599\sqrt5\) and its conjugate \(\bar\alpha\), define \(P(T)=\alpha^2 T^2+(4K-2C)T+\bar\alpha^2\), with \(T=G^{2n}\). Direct expansion of \(p_n=(\alpha G^n-\bar\alpha G^{-n})/(2\sqrt5)\) gives \(P(T)=4T N_K(n)\). If \(n\equiv0\bmod L\) and the new prime q hits (even weakly), then \(T^b=1\bmod q\) and \(P(T)=0\bmod q\) in the quadratic residue algebra. Thus q divides the rational integer
\[
 R_b=\operatorname{Res}(T^b-1,P(T)).
\]
Indeed \(R_b=\prod_{\zeta^b=1}P(\zeta)\) is integral, and conjugating \(\sqrt5\) makes P reciprocal without changing this product. It is nonzero: on \(|T|=1\), the imaginary part of \(P(T)/T\) is \((\alpha^2-\bar\alpha^2)\Im T\), so a zero could only occur at \(T=\pm1\), where direct evaluation is nonzero. On the unit circle \(|P(T)|\le\alpha^2+\bar\alpha^2+|4K-2C|=51179764\), hence \(q\le51179764^b\).

The class \(0\bmod L\) always survives all prior genuine odd-valuation tests because it contains \(n=0\). Therefore at a new prime either it has zero deletion or \(b\ge\log q/\log51179764\), with deletion at most \(2/b\) by the active-root bound. This gives \(O(1/\log q)\) uniformly on that anchored class, and rules out a fixed positive minimum deletion over all surviving classes. It does not rule out a divergent weighted aggregate.

~~~javascript
const p0=1599n,x0=3577n,K=10936n,C=10924n;
const mod=(a,p)=>(a%p+p)%p;
function mult([a,b],[c,d],p){return [mod(a*c+5n*b*d,p),mod(a*d+b*c,p)]}
function power(e,p){let r=[1n,0n],a=[9n,4n];while(e){if(e&1n)r=mult(r,a,p);a=mult(a,a,p);e>>=1n}return r}
function ok(x){if(!x)throw Error("certificate mismatch")}
ok(x0*x0-5n*p0*p0===C&&5n*p0*p0+K===3554n**2n+405n**2n);
ok(2n*(x0*x0+5n*p0*p0)+4n*K-2n*C===51179764n);
ok(2n*(x0*x0+5n*p0*p0)!==4n*K-2n*C);
for(const [p,m,r] of [[1051n,35n,28n],[9043n,2261n,2065n]]){
  for(let i=2n;i*i<=p;i++)ok(p%i!==0n);
  const G=power(387860n,p);
  let u=[1n,0n],h=[],j=0n;
  do{
    const y=mult(u,[x0,p0],p)[1];
    if(mod(5n*y*y+K,p)===0n)h.push(j);
    j++;u=mult(u,G,p);
  }while(u[1]!==0n);
  ok(j===m&&h.length===1&&h[0]===r&&r%7n===0n);
  const step=power(387860n*m,p*p)[1];
  ok(step%p===0n&&step!==0n);
  ok(mult(power(387860n*r,p),[x0,p0],p).every(x=>x!==0n));
}
~~~
