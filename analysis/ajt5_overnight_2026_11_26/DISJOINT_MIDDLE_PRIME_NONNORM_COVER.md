# Disjoint middle-prime supports can still cover every sampled nonnorm

Disjoint middle-prime supports, long orders, and a small joint witness product can all hold while **every sampled label at one fixed ordinary target is a genuine nonnorm**. I constructed a cofinal family with \(\Theta(b/\log b)\) labels, where \(b\asymp\log n\). Every prime divisor in the entire band \([b^3,2b^3]\) hits at most one sampled label, and each label has two distinct inert primes in that band at exact depth one. [Verified middle-prime baseline](https://github.com/Samsen879/a303656/commit/b68aa14dc8f1b3d42c7090987d50d3ea1552418f)

### Construction and height budget

Keep the balanced phase \(A=3^a,\ B=5^b\), \(39/40<B/A<122/125\), and the baseline labels \(S_0=A+25B\), \(P=A+125B\), \(S_3=729A+B\), and \(U=729A+625B\). Put
\[
X=b^3,\qquad L=\lceil\log_2(2X)\rceil,\qquad m=\left\lfloor\frac{b}{16L}\right\rfloor .
\]
Use \(S_t=3^x+5^{y_0-\Lambda t}\) for \(0\le t<m\), where \(y_0=b+3-990\). Take \(c=5^j\) with \(j\) the largest odd integer satisfying \(c^2\le a\), and set \(x=a-\operatorname{lcm}(4c/5,\Lambda)\).

The stride \(\Lambda\) is the lcm of \(6930\) and the \(q-1\) for additional inert primes \(q\le Z\), where \(Z=\max(31,\lfloor\log_2\log_2 b/16\rfloor)\). Thus \(\Lambda=O((\log b)^{1/4})\), and \(m\Lambda=o(b)\). The baseline CRT retains the \(S_0\) witness and the original \(43,47\) depths at \(P,A+625B\). At the sampled labels the shift by \(990\) clears \(43\). For additional small primes, choose the target residue to avoid the seed label and preserve it along the stride. When \(47\) enters the small panel its seed is already a unit, since \(5^{991}\ne1\bmod47\).

Assign two distinct inert primes \(q\in[X,2X]\) to each column \(t\), requiring \(q\nmid S_t-S_0\) and \(\operatorname{ord}_q(5^\Lambda)\ge m\). These choices exist for all sufficiently large \(b\). The prime number theorem modulo \(4\) supplies \(\sim X/(2\log X)\) primes. A given \(S_t-S_0\) excludes \(O(b/\log X)\), and all short-order primes together number
\[
E\le \frac{\Lambda m(m-1)\log 5}{2\log X},
\]
by the product of \(5^{\Lambda d}-1\) for \(1\le d<m\). Both exclusions and the primes already assigned are smaller than the supply.

Write \(n=S_0+C(u^2+v^2)\), with \(R=5^{\lfloor b/4\rfloor}\) and \(C=B/R^2\) an integer square. For each assigned \(q\), impose \(n-S_t\equiv q\bmod q^2\). The required residue of \(u^2+v^2\) is a unit modulo \(q\), so a solution modulo \(q\) lifts modulo \(q^2\). The combined coordinate modulus satisfies \(\log_2 M\le b/4+o(b)\). The **joint product of all \(2m\) witnesses is at most \(2^{b/8}\)**.

### Controlling every actual divisor in the band

Round \(v\) and an initial \(u_0\) into the baseline coordinate intervals. Vary \(u=u_0+Mh\) for \(0\le h\le 2mE\). For each short-order prime \(q\) and each column \(t\), the equation \(n=S_t\bmod q\) is quadratic in \(h\) and excludes at most two residues. Since \(2mE=o(X)\), each excluded residue removes at most one trial index. There are at most \(2mE\) exclusions, so a trial survives. The added coordinate displacement is \(o(R)\), leaving the ordinary-height room intact.

Fix \(n\) at that trial. No short-order prime in the band divides **any** sampled remainder. This conclusion includes split primes. A prime of order at least \(m\) cannot divide two remainders, since subtraction would force its order to divide the nonzero difference of their column indices. Meanwhile the two assigned inert primes still have exact valuation one at each column. Thus disjointness applies across the **whole band**, and every sampled remainder fails the integer sum-of-two-squares criterion.

The construction preserves \(2S_3-P<n\le U\) and an ordinary true witness at \(S_0\). Every sampled remainder is positive, is \(1\bmod4\), and has exact \(5\)-part \(c\) by LTE. The other split factors are unrestricted. Also \(S_t+\tfrac45(n-S_t)>S_3\), so the nonnorms occur within the ordinary height window. This obstructs a cover-escape argument based on band disjointness, order, parity, and a joint size budget alone. It gives no claim for a target prescribed before construction or for labels outside the sampled progression.

### Standalone replay

The independently rebuilt BigInt replay below uses the original exponent pair and every one of the 457 primes in [4000,8000]. It certifies 16 labels, 32 exact-depth-one witnesses with a 386-bit joint product, and zero shared band primes. An imposed pre-filter repeated hit at 4159 is removed by the coordinate filter, after which the target is held fixed.

Asymptotically the 5-adic part is exactly \(c\): the 5-part of \(\Lambda\) is smaller than \(5^{j-1}\), so the exponent difference has 5-adic depth \(j-1\), and LTE gives \(j\) at the difference of the two 3-powers. Other terms are much deeper. When filtering short-order band primes, none divides the protecting modulus \(M\); assigned band primes have long order, and the baseline and small-panel factors lie below the band. Thus the quadratic coefficient in the filter is nonzero at each short-order prime.

```javascript

const mod=(x,m)=>(x%m+m)%m;
function pw(x,n,m){let r=1n;x=mod(x,m);for(;n;n>>=1n,x=x*x%m)if(n&1n)r=r*x%m;return r;}
function iv(a,m){let b=m,x=1n,y=0n;a=mod(a,m);
  while(b){const q=a/b;[a,b]=[b,a-q*b];[x,y]=[y,x-q*y];}
  if(a!==1n)throw Error("inverse");return mod(x,m);}
const check=(x)=>{if(!x)throw Error("assert");};
const isPrime=(p)=>{for(let i=2n;i*i<=p;++i)if(p%i===0n)return false;return p>1n;};
function crt(rows){let x=0n,M=1n;for(const [m,v] of rows){x+=M*mod((v-x)*iv(M,m),m);M*=m;}return [x,M];}

const gcd=(a,b)=>{while(b)[a,b]=[b,a%b];return a;};
const lcm=(a,b)=>a/gcd(a,b)*b;
function square(x,y,q,rad){return mod(x*x+y*y-rad,q)===0n;}
function pair(rad,q,e){
  let a,b;for(a=0n;a<q;a++){
     b=pw(rad-a*a,(q+1n)/4n,q);
     if(square(a,b,q,rad))break;
  }
  check(a<q);
  if(e===2){
    const z=(rad-a*a-b*b)/q;
    if(a)a+=q*mod(z*iv(2n*a,q),q);
    else b+=q*mod(z*iv(2n*b,q),q);
    check(square(a,b,q*q,rad));
  }
  return [a,b];
}
const a=574422n,b=392104n,A=3n**a,B=5n**b;
const V=5n**(b/4n),C=V*V;
const S0=A+25n*B,P=A+125n*B,S3=729n*A+B,U=729n*A+625n*B;
const rr=5n**(b/4n);
const stride=6930n,c=125n,x=a-lcm(4n*c/5n,stride),y0=b+3n-990n,count=16;
const ys=Array.from({length:count},(_,t)=>y0-stride*BigInt(t));
const sm=(i,q)=>mod(pw(3n,x,q)+pw(5n,ys[i],q),q);
const prs=[];
for(let q=4000n;q<=8000n;q++)if(isPrime(q))prs.push(q);
const short=prs.filter(q=>Array.from({length:count-1},(_,j)=>pw(5n,stride*BigInt(j+1),q)).some(z=>z===1n));
const data=[[20n,1n,0n],[11n,0n,0n]];
for(const [q,K] of [[43n,100n],[47n,600n]]){
  const [u,v]=pair(K*rr*rr+q,q,2);data.push([q*q,u,v]);
}
for(const q of [3n,7n,19n,23n,31n]){
  let z=0n;while(mod(z-100n*rr*rr,q)===0n||mod(z-600n*rr*rr,q)===0n)z++;
  const [u,v]=pair(z,q,1);data.push([q,u,v]);
}
const used=new Set(),ass=[];
for(let i=0;i<count;i++){
  const row=[];for(let j=0;j<2;j++){
    const q=prs.find(q=>q%4n===3n&&!short.includes(q)&&!used.has(q)&&mod(sm(i,q)-S0,q)!==0n);
    check(q);used.add(q);row.push(q);
    const qq=q*q,T=mod((sm(i,qq)-S0+q)*iv(C,qq),qq);
    const [u,v]=pair(T,q,2);data.push([qq,u,v]);
  }ass.push(row);
}
const [aa,M]=crt(data.map(([m,x])=>[m,x]));
const [bb]=crt(data.map(([m,x,y])=>[m,y]));
let u0=aa+M*((917n*rr/25n-aa)/M+1n);
const v=bb+M*((rr/200n-bb)/M+1n);
let forced=null;
for (const q of short){
  const hit=ys.findIndex((_,i)=>ys.some((_,j)=>i!==j&&sm(i,q)===sm(j,q)));
  if(hit<0)continue;
  const rhs=mod((sm(hit,q)-S0)*iv(C,q)-v*v,q);
  let w=0n;while(w<q&&w*w%q!==rhs)w++;
  if(w===q)continue;
  u0+=M*mod((w-u0)*iv(M,q),q);
  forced=q;break;
}
check(forced!==null);
const oldn=S0+C*(u0*u0+v*v);
check(ys.filter((_,i)=>mod(oldn-sm(i,forced),forced)===0n).length>=2);
let h=0;
for(;h<=2*count*short.length;h++){
  if(short.every(q=>{const u=mod(u0+M*BigInt(h),q),n=mod(S0+C*(u*u+v*v),q);return ys.every((_,i)=>n!==sm(i,q));})) break;
}
check(h>0&&h<=2*count*short.length);
const u=u0+M*BigInt(h),n=S0+C*(u*u+v*v);
check(5n*n>5n*(2n*S3-P)&&n<=U&&S3<S0+C*u*u&&n%121n===36n);
for(const q of prs)check(ys.filter((_,i)=>mod(n-sm(i,q),q)===0n).length<=1);
for(let i=0;i<count;i++){
 const s=3n**x+5n**ys[i],v=n-s;
 check(v>0n&&v%4n===1n&&v%c===0n&&v%(5n*c)!==0n&&5n*s+4n*v>5n*S3);
 for(const q of ass[i])check(v%(q*q)===q);
}
text({band:prs.length,short:short.length,forced:String(forced),skip:h,labels:count,vetoes:used.size,
      bits:[...used].reduce((a,b)=>a*b,1n).toString(2).length});
```
