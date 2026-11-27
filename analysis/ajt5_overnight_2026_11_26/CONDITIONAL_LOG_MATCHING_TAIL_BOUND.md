# Quantitative conditional lower tails for logarithmic matchings

**At least \(90.1\%\) of targets have a true matching of size at least \(10^{-9}\log X\) in every fixed residue class whose modulus is supported on \(2,3,5,7,19\).** At coefficient \(10^{-11}\), the lower proportion is \(92.6\%\). These are dyadic limit-inferior bounds in \(X<n\le2X\), in the same ordinary-height rectangle
\[
X^{1/8}\le 3^c\le X^{1/4},\qquad X^{1/3}\le 5^d\le X^{1/2}.
\]
The constants are independent of the five read depths. Each modulus is fixed before taking \(X\to\infty\). The gain over the all-class majority theorem is a direct upper bound on the bad family, at a smaller fixed coefficient. [Verified all-class majority theorem](https://github.com/Samsen879/a303656/commit/c70df2323a686370f55a15bdff285a88e17119a8)

### A uniform conditional bound

Let \(F,G\) be the unweighted capped endpoint profiles, and let \(\nu_X\) denote the maximum matching size. Write \(\mathcal C\) for any of the fixed classes above. For \(0<u<1\) and \(\delta>0\), the bound is
\[
\limsup_{X\to\infty}\Pr_{\mathcal C,X}(\nu_X<\delta\log X)
\ \le\
\frac{0.0712}{0.0712+(1-u)^2}
+\frac{3000\delta}{(0.124u)^2}.
\tag{1}
\]
The inputs are a positive phase family at four observed primes, a relative variance bound on its remaining norm profile, and a conditional endpoint-energy bound.

**At the observed primes.** For each target residue mod \(8\cdot27\), choose \(c=a\bmod2\) and \(d=b\bmod18\) so the remainder is \(1\bmod4\) for odd targets or \(2\bmod8\) for even targets, and has valuation 0 or 2 at 3. To see this, for even targets the four exponent parity pairs give all four even shifts mod 8. For odd targets, \(c\bmod2\) determines the required shift mod 4. Within the selected \(d\)-parity, if \(5^d\equiv n\bmod3\), choose \(5^d\equiv n-9\) or \(n-18\bmod27\). The order of 5 mod 27 is 18, so this preserves the selected parity.

Write \(c=a+2s\), \(d=b+18t\). At 7 and 19 the \(d\)-term is fixed. The orders of 9 at those primes are 3 and 9. Requiring unit remainders removes at most one class of \(s\bmod3\) and one class of \(s\bmod9\). At least five of the nine residues of \(s\) remain. Thus the selected phase family has Haar mass at least \(5/324\), and its norm densities at \(2,3,7,19\) are exactly \(2,4/3,8/7,20/19\). The density at 5 is always at least \(4/5\).

**At the remaining primes.** Let \(T\) be the limiting profile formed by averaging the remaining local norm factors over the normalized selected phase family. The finite-prime averages form a mean-one martingale over the unread target coordinates. The second-moment bound below gives \(L^2\) convergence and
\[
\mathbb E(T\mid\mathcal C)=1,\qquad
\operatorname{Var}(T\mid\mathcal C)<0.0712,\qquad
F\ge \pi\,\frac5{324}\frac{4}{5}\,2\frac43\frac87\frac{20}{19}\,T
>0.124T
\]
on \(T>0\). To apply this when \(\mathcal C\) does not specify the initial read depths, refine it by the initial modulus and average the bounds. Extra reads at the five primes do not change the law of the unread target coordinates. [Local norm densities and correlation kernels](https://github.com/Samsen879/a303656/blob/c6236506eedd64362571564f33c8f43bd50cb691/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_PROFINITE_LIMIT.md)

### Certifying the variance without a common exponent period

For two selected phases, let \(h_q\) be their shift difference at an unread prime \(q\). Integrating the target coordinate gives the exact kernel
\[
(1-q^{-2})\sum_{j\ge0}q^{-j}\mathbf1_{q^j\mid h_q}.
\]
For a set of simultaneous first-residue collisions, put \(L_c=\operatorname{lcm}_q\operatorname{ord}_q(9)\) and \(L_d=\operatorname{lcm}_q\operatorname{ord}_q(5^{18})\), with the lcms over that set. The collision probability is at most
\[
\min\!\left\{\frac{A_{\gcd(L_c,9)}}{L_c},\,\frac1{L_d}\right\},
\qquad (A_1,A_3,A_9)=(1,39/25,9/5).
\tag{2}
\]
Indeed, with both \(d\)-phases fixed, the congruences define a partial matching between the two \(s\bmod L_c\) values. Each value determines at most one partner in either direction. Cauchy–Schwarz bounds its mass by the squared \(\ell^2\)-norm of the distribution of \(s\bmod L_c\). For \(\gcd(L_c,9)=3\), the worst allowed mask has row sizes \(3,2,0\), giving \(3(3^2+2^2)/5^2=39/25\). Fixing both \(c\)-phases gives the uniform \(1/L_d\) bound. This calculation preserves the shared phase across the collision tests.

The rational certificate expands the kernel through 61. It also bounds each joint collision by the smallest of its exact single-prime collision probabilities, computed from histograms of the two power cosets. At the largest selected prime \(q\), if either base lifts ordinarily, the factor \(1/(q-1)\) improves to \(q/(q^2-1)\). After conditioning on the first residues, that base’s \(q\)-primary exponent makes the difference uniform in its residue ball. The smaller selected primes read none of that coordinate.

Above 61, expand by the largest selected prime and bound the preceding product by \(\prod_{p<q}p/(p-1)\) over unread primes. Sum through \(Y=2^{21}\) using (2). Above \(Y\), the product is bounded by \((8/15)\log q\). In each dyadic block \(U<q\le2U\), split the orders of 9 at \(\sqrt U\). Short-order primes of order \(o\) divide \(9^o-1\), and the product of the long-order primes divides \(\binom{2U}{U}\). This bounds the analytic tail by
\[
\frac95\,\frac8{15}\,\frac72\,\frac{18}{5}\,\frac1{\sqrt Y}.
\]
The resulting second-moment upper bound is less than \(1.0712\). The calculation uses prime orders and small local histograms. [Rosser–Schoenfeld product bound](https://doi.org/10.1215/ijm/1255631807)

### Transferring to true matchings

The conditional endpoint energy satisfies \(\mathbb E(G\mid\mathcal C)<3000\). At the four observed primes use the squared pointwise bounds above. At 5, the average of the squared local density over \(c\) is at most \(67/50\) for every target coordinate, since the powers of 3 fill the 5-adic units. For a moving \(c\)-pair, Cauchy–Schwarz gives the same bound at each fixed difference. At the other primes the one-axis pair kernels depend only on the exponent difference. Their average product is less than \(7/6\) for each base, using the lcm expansion and the same order tail. Thus
\[
\mathbb E(G\mid\mathcal C)
\le
\pi^2\!\left(2\frac43\frac87\frac{20}{19}\right)^2
\frac{67}{50}\,\frac76\,(8\log3+6\log5)<3000.
\]

Cantelli bounds \(\Pr(T\le u\mid\mathcal C)\) by the first term of (1). On \(T>u\), the event \(F^2\le\delta G\) forces \(G\ge(0.124u)^2/\delta\). Markov gives the second term. The verified capped matching inequality and joint convergence transfer this closed-event bound to actual matchings in the fixed class. Substituting \((u,\delta)=(3/20,10^{-9})\) and \((1/20,10^{-11})\) gives bad-family bounds below \(0.099\) and \(0.074\). [Capped endpoint transfer](https://github.com/Samsen879/a303656/commit/c92bb115bf6404a70b1344d2337835f108e4db7e)

The independently rebuilt BigInt replay below verifies the directed-rounding variance bound and the endpoint bounds, plus a true norm and exact odd valuation 1 at 11 at the same actual target.

The exact modular obstruction union still gives the zero atom. Bound (1) has a positive variance floor as \(\delta\downarrow0\), so it leaves open a power bound for the positive mass near that atom, the exact density at a fixed coefficient, and pointwise coverage. [Verified zero-atom identity](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e)

The independent replay deliberately takes the maximum single-prime collision probability over all five-element masks and all indicated initial parities, slightly widening the intermediate variance bound to \(0.0712\). It still gives failure below \(0.099\) at \((u,\delta)=(3/20,10^{-9})\) and below \(0.074\) at \((1/20,10^{-11})\). All modular multiplications using JavaScript Numbers are performed below \(2^{53}\): the prime cutoff is \(2^{21}\), and the local squared-prime checks are only at primes at most 61. The aggregate weights use directed BigInt rounding.

```javascript

const S=10n**20n,Y=2**21;
const ck=x=>{if(!x)throw Error("assert");};
const gcd=(a,b)=>{while(b)[a,b]=[b,a%b];return a;};
const lcm=(a,b)=>a/gcd(a,b)*b;
const ceil=(a,b)=>(a+b-1n)/b;
const skip=new Set([2,3,5,7,19]);
const sp=new Uint32Array(Y+1),pr=[];
for(let i=2;i<=Y;i++){
 if(!sp[i]){sp[i]=i;pr.push(i);if(i*i<=Y)for(let j=i*i;j<=Y;j+=i)if(!sp[j])sp[j]=i;}
}
function pow(a,n,p){let r=1;a%=p;for(;n;n>>=1,a=(a*a)%p)if(n&1)r=(r*a)%p;return r;}
function order(b,p){
 let d=p-1,t=d;
 while(t>1){const q=sp[t];while(t%q===0)t/=q;while(d%q===0&&pow(b,d/q,p)===1)d/=q;}
 return d;
}
const pop=(x)=>{let i=0;while(x){x&=x-1;i++;}return i;};
function collide(p,o,d){
 const g=Number(gcd(BigInt(o),9n)),period=o/g;
 let best=0;
 for(let aa=0;aa<2;aa++)for(let bb=0;bb<18;bb++)for(let mask=0;mask<512;mask++){
   if(pop(mask)!==5)continue;
   const h=Array(p).fill(0);
   for(let j=0;j<9;j++)if(mask&(1<<j))
     for(let u=0;u<period;u++)for(let v=0;v<d;v++)
       h[(pow(3,aa+2*(j+9*u),p)+pow(5,bb+18*v,p))%p]++;
   best=Math.max(best,h.reduce((s,x)=>s+x*x,0));
 }
 return [BigInt(best),BigInt(5*period*d)**2n];
}
function min(a,b){return a[0]*b[1]<=b[0]*a[1]?a:b;}
function bound(l,m,one){
 const g=gcd(l,9n),[u,v]=g===1n?[1n,1n]:g===3n?[39n,25n]:[9n,5n];
 return min(min([u,v*l],[1n,m]),one);
}
const small=pr.filter(p=>p<=61&&!skip.has(p)).map(p=>{
 const o=order(9,p),d=order(pow(5,18,p),p);
 return {p:BigInt(p),o:BigInt(o),d:BigInt(d),mx:collide(p,o,d),
   okay:pow(3,p-1,p*p)!==1||pow(5,p-1,p*p)!==1};
});
function smallbound(b){
 let nn=1n,dd=1n;
 for(const {p} of small){nn*=p*p-1n;dd*=p*p;}
 let total=S;
 for(let mask=1;mask<(1<<small.length);mask++){
    let l=1n,m=1n,z=1n,one=[1n,1n],u=1n,largest=null;
    small.forEach((q,i)=>{
      if(!(mask&(1<<i)))return;
      if(largest)z*=largest.p-1n;
      l=lcm(l,q.o);m=lcm(m,q.d);one=min(one,q.mx);
      if(b)u=lcm(u,BigInt(order(b,Number(q.p))));
      largest=q;
    });
    const p=largest.p;
    let [n,d]=b?[1n,u]:bound(l,m,one);
    if(largest.okay){n*=p;d*=p*p-1n;}else d*=p-1n;
    total+=ceil(S*n,d*z);
 }
 return [total,nn,dd];
}
function run(b){
 let [start,n,d]=smallbound(b),W=S;
 for(const pp of pr){
  if(skip.has(pp))continue;
  const q=BigInt(pp);
  if(pp>61){
    const [u,v]=b?[1n,BigInt(order(b,pp))]:
       bound(BigInt(order(9,pp)),BigInt(order(pow(5,18,pp),pp)),[1n,1n]);
    start+=ceil(W*u,v*(q-1n));
  }
  W=ceil(W*q,q-1n);
 }
 // Remove the five observed prime factors from the full Mertens product.
 // Keeping the looser 8/15 constant works for both endpoint bases as well.
 const [a,c,e]=b?[1n,1n,31n]:[9n,5n,36n];
 start+=ceil(S*a*8n*7n*e,c*15n*2n*10n*1448n);
 return ceil(start*n,d);
}
const results=[run(0),run(3),run(5)];
ck(10000n*results[0]<10712n*S && 6n*results[1]<7n*S && 6n*results[2]<7n*S);
const x=[10000000000n,10000804849n];
const p=3n**3n,q=5n**5n;
ck(x[0]<x[1]&&x[1]<2n*x[0]&&p**8n>=x[0]&&p**4n<=x[0]&&q**3n>=x[0]&&q*q<=x[0]);
ck(x[1]-p-q===100004n**2n+41n**2n);
const bad=x[1]-3n**5n-q;
ck(bad%11n===0n&&bad%121n!==0n);
for(const r of [x[1]-p-q,bad])ck(r%4n===1n&&r%3n&&r%7n&&r%19n);
text(results.map(x=>Number(x)/Number(S)));
```
