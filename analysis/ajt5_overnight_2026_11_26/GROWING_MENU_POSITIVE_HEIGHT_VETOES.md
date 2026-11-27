# Growing positive-height menus can all be vetoed on signed targets

**A growing menu can be blocked at every sufficiently large height \(B=5^D\).** Fix \(0<\alpha<1/4\). For any menu of at most \(\alpha\log B/\log\log B\) exponent pairs \((c_i,d_i)\) with \(3^{c_i}\le B/10\) and \(0\le d_i<D\), there are \(B^{1-4\alpha-o(1)}\) or more distinct simultaneous-norm targets in **each** odd class modulo \(4\) for which every menu residual is positive and has exact valuation one at an inert prime. The menu can depend on \(D\). For example, both axes vary in \(c_i=2i+\mathbf 1_{P=1}\), \(d_i=D-i\), where \(P=1\) or \(3\) selects the odd class. [Fixed-menu baseline](https://github.com/Samsen879/a303656/commit/7e28591a56704f7e06a4d9b4c0c9d88f596a617d)

### One prime digit per move

Write \(n=B+P-S\) and \(K_i=B+P-3^{c_i}-5^{d_i}\). Choose distinct primes \(q_i\equiv3\pmod4\) in \([32D,64D]\) with \(q_i\nmid K_i(2P-K_i)\). The prime number theorem in progressions supplies asymptotically \(16D/\log D\) candidates. Each product excludes at most \((2\log B+O(1))/\log(32D)\) of them, so greedy assignment works at the actual \(D\), without restricting \(D\) to a progression. [Prime number theorem in progressions](https://dlmf.nist.gov/27.11#i)

The key local step works for **every** nonzero \(s\bmod q_i\). Drop the subscript and impose
\[
x^2+y^2=K,\qquad r^2-3t^2=T=2P-K,\qquad x+y+r-3t=s.
\]
Put \(u=x+y\), \(v=x-y\), \(w=s-u\), and \(z=2t+w\). The two square conditions become
\[
v^2=2K-u^2,\qquad z^2=(w^2+2T)/3.
\]
The quadratics are separable and have different centers because \(s\ne0\). Expanding the two square-root counts and applying the quadratic character bound gives at least \(q-2-3\sqrt q\) solutions. If the quadratics share one root, removing its square factor changes the product character sum by at most one. [Weil’s character-sum bound](https://pmc.ncbi.nlm.nih.gov/articles/PMC1079093/)

In the signed parametrization \(a=x-t,\ b=y-t\), with \(s\) fixed, the derivative of \(S=x^2+y^2\) is
\[
S_a=\frac{2}{s}\bigl(ru+wx\bigr).
\]
At a zero of this derivative, \(u=0\) is impossible since \(sK\ne0\). For \(u\ne0\), eliminating \(r,t\) gives
\[
3Tu^2=(s-u)^2(K-2u^2).
\]
This quartic leaves at most eight solutions, since each \(u\) gives at most two \(x\) and then determines \(r,t\). Thus a local phase with \(S_a\ne0\) exists at every selected prime.

Set \(Q=\prod_i q_i\), **squarefree**. For every \(m\) coprime to \(6Q\), take \(s=2m\) and impose the local phases on \(a,b\) modulo \(Q\), along with the original norm congruence modulo \(m\) and \(a\equiv3,\ b\equiv0\pmod6\). After CRT, change \(a\) by \(6mQj\). At \(q_i^2\), the derivative makes \(K_i-S\) vanish for exactly one \(j\bmod q_i\). Each prime therefore forbids at most one of \(j=0,\ldots,L\), where \(L\) is the menu size. A single common \(j\) leaves every residual divisible by \(q_i\) and indivisible by \(q_i^2\). The second digits never need to be put into the CRT modulus.

### Height and population

Use representatives modulo \(6mQ\), add \(12mQ\) to \(a\) before the common shift, and take \(m\in[Y/2,Y]\), where
\[
Y=\frac{\sqrt B}{1000Q^2(L+1)^2}.
\]
The original coordinate formulas bound all four coordinates by \(150sQ^2(L+1)^2\), and \(|x-y|>3sQ\). Hence \(S<0.18B\) and \(S\gg B/[Q^2(L+1)^4]\). In the stated range this gives \(0.82B<n<B\). Every menu shift is at most \(0.3B\), so every residual exceeds \(B/2\).

There are \(\gg Y\) eligible \(m\): excluding multiples of the selected primes removes \(O(YL/D+L)=o(Y)\). Each \(m\) supplies at least \(\varphi(m)\ge m/[2(1+\log m)]\) seeds. The chosen lift preserves injectivity, since the final coordinates recover \(m,a,b\) and reduction modulo \(6mQ\) recovers the original seed. This gives \(\gg B/[Q^4(L+1)^4(1+\log B)]\) quadruples. The original divisor and unit-orbit argument bounds each target’s multiplicity by \(B^{o(1)}\), using an \(O(\log B)\) unit-orbit bound here. Since \(Q\le(64D)^L=B^{\alpha+o(1)}\), the distinct-target count follows. [Original norm parametrization and projection](https://github.com/Samsen879/a303656/commit/df03dc909f37a1117a2ba91cd3523f28292a332a)

The height budget of this box is \(Q^2(L+1)^2\ll\sqrt B\). Even one target can be guaranteed for \(L=\lfloor\log B/(4\log(64D))-3\rfloor\). Conversely, \(Q\ge L!\) for distinct primes, so the same box cannot guarantee a larger leading coefficient than \(1/4\). This is a limit of the construction.

The standalone BigInt replay checks three genuinely moving pairs at D=100 and five at D=160, forcing an initial bad second digit and verifying a single common shift avoids all bad digits. This is an obstruction to the prescribed menu, not to all representations.

The order of the quantifiers matters: for each size and prescribed menu the real targets are constructed to veto that menu. The result is not a claim that an arbitrary specified target fails, or that failure persists when the menu is chosen after inspecting the target.

```javascript

const mod=(x,m)=>(x%m+m)%m;
function pw(x,n,m){let r=1n;x=mod(x,m);for(;n;n>>=1n,x=x*x%m)if(n&1n)r=r*x%m;return r;}
function iv(a,m){let b=m,x=1n,y=0n;a=mod(a,m);
  while(b){const q=a/b;[a,b]=[b,a-q*b];[x,y]=[y,x-q*y];}
  if(a!==1n)throw Error("inverse");return mod(x,m);}
const check=(x)=>{if(!x)throw Error("assert");};
const isPrime=(p)=>{for(let i=2n;i*i<=p;++i)if(p%i===0n)return false;return p>1n;};
function crt(rows){let x=0n,M=1n;for(const [m,v] of rows){x+=M*mod((v-x)*iv(M,m),m);M*=m;}return [x,M];}
const sqrt=(x,p)=>{x=mod(x,p);let y=pw(x,(p+1n)/4n,p);return y*y%p===x?y:null;};
function local(q,P,K,s){
  const i2=iv(2n,q),i3=iv(3n,q),T=2n*P-K;
  for(let u=0n;u<q;u++){
    const w=s-u,v=sqrt(2n*K-u*u,q),z=sqrt(i3*(w*w+2n*T),q);
    if(v===null||z===null)continue;
    for(const ee of [1n,-1n])for(const ff of [1n,-1n]){
      const x=mod((u+ee*v)*i2,q), y=mod((u-ee*v)*i2,q);
      const t=mod((ff*z-w)*i2,q),r=mod(w+3n*t,q);
      if(mod(r*u+w*x,q)!==0n){
        check(mod(x*x+y*y-K,q)===0n&&mod(r*r-3n*t*t-T,q)===0n);
        return [x-t,y-t];
      }
    }
  }throw Error("missing derivative-unit phase");
}
for(const [D,L,P] of [[100n,3,1n],[160n,5,3n]]){
  const B=5n**D,m=11n,s=2n*m,moves=[],ar=[[6n,3n],[m,1n]],br=[[6n,0n],[m,P===1n?0n:1n]];
  let q=32n*D+3n;
  for(let i=1;i<=L;i++){
    const c=BigInt(2*i)+(P===1n?1n:0n),d=D-BigInt(i),K=B+P-3n**c-5n**d;
    while(!isPrime(q)||K%q===0n||(2n*P-K)%q===0n)q+=4n;
    check(q<64n*D);
    const [aa,bb]=local(q,P,K,s); moves.push([q,K,c,d]);ar.push([q,aa]);br.push([q,bb]);q+=4n;
  }
  const [a0,M]=crt(ar),[b]=crt(br);
  function value(j){const a=a0+M*BigInt(j+2),t=(P-a*a-a*b-b*b)/s+a+b-s/2n;return (t+a)**2n+(t+b)**2n;}
  const [p,K]=moves[0];
  const off=Number(mod(((K-value(0))/p)*iv((value(1)-value(0))/p,p),p));
  check((K-value(off))%(p*p)===0n);
  let n=null,chosen=-1;
  for(let j=0;j<=L;j++){
    const a=a0+M*BigInt(j+off+2),num=P-a*a-a*b-b*b;check(num%s===0n);
    const t=num/s+a+b-s/2n,x=t+a,y=t+b,r=t+s-a-b,S=x*x+y*y;
    check(S%4n===1n&&S%3n===2n&&r*r-3n*t*t===2n*P-S);
    check(moves.every(([q,K])=>(K-S)%q===0n));
    if(moves.every(([q,K])=>(K-S)%(q*q)!==0n)){n=B+P-S;chosen=j;break;}
  }
  check(chosen>0&&n!==null&&100n*n>82n*B&&n<B&&n%4n===P);
  check(moves.every(([, ,c,d])=>n>3n**c+5n**d));
  text([String(D),chosen,moves.map(([q])=>String(q))]);
}
```
