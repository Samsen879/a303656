# A rank-zero certificate eliminates every rational quadratic vertex

For the actual label \((10,2;11,3)\), use \(B=9633851,\ m=4816930,\ d=m/2,\ K=m^2-B\). The [quadratic square-class test](QUADRATIC_PULLBACK_SQUARE_CLASS_TEST.md) needed \(q^2=b^2-u\) in \(E=\mathbb Q(i,\sqrt B)\), where \(u=2-im+i\sqrt B\). In fact \(q^2=s+i(m-\sqrt B)\) has no solution in E for **any** rational s. This excludes all rational quadratic pullbacks of the fixed factor \(f(T)=(T^2-2+im)^2+B\), and implies irreducibility under iterated rational quadratics.

## Reduction to an elliptic curve

Write \(q=g+h\sqrt B\) with \(g,h\in\mathbb Q(i)\). Comparing the \(\sqrt B\) term gives \(2gh=-i\). If \(g^2=T+iS,\ R=N(g)\), and \(\xi=B/(4R^2)\), then comparison of the other imaginary coefficient gives \((1+\xi)S=m\). Taking \(U=(1+\xi)R,\ V=(1-\xi)R,\ X=(1+\xi)T\) yields \(U^2-V^2=B,\ U^2-X^2=m^2\). Thus
\[
 (U^2,UVX)\in J(\mathbb Q),\qquad J:\ y^2=x(x-B)(x-m^2).
\]
It has \(x>m^2\), because equality would make \(K=m^2-B=73\cdot317846643713\) a square. The certificate below proves \(J(\mathbb Q)=J[2]\).

## Exact 2-descent and pairing

Use root order \(0,B,m^2\), with Kummer coordinates \(x-r_i\). At an odd or even prime where x has a pole all valuations are equal and even. At an integral x a prime in the squarefree support must divide two coordinates and hence their root difference. The real signs are \(+,\epsilon,\epsilon\). It follows that every locally soluble class is represented by
\[
 (ba,\epsilon bc,\epsilon ac),\quad b\mid B,\quad a\mid m,\quad c\mid K,\quad \epsilon=\pm1,
\]
where the three root-difference supports are disjoint and \(B,m,K\) are squarefree. At \(p\mid B\), the unit third coordinate must have Legendre sign \((-1/p)\) if \(p\mid b\), and sign +1 otherwise. In the first case \(x\equiv0\) and \(x-m^2\equiv-m^2\); in the second the first two colliding factors have ratio a square unit modulo p. If both were divisible by p without p in their square classes, their valuations would both have to be even, impossible since their difference has valuation one. At \(p\mid K\) the analogous argument gives Legendre sign +1 for the first coordinate in both cases, since at collision \(x\equiv m^2\). At odd \(p\mid m\) with \(p\mid a\), the middle coordinate has residue \(-B\equiv9\bmod p\). These are necessary local tests. At 2 take integral x modulo 256, allowing arbitrary square classes for factors divisible by 64; all other differential factors have their unit class and valuation parity determined. Negative valuations are negative even; at valuation -2 the unit residues are \(u-4r_i\bmod8\) and at deeper poles all equal odd u. This leaves exactly 16 candidates.

They form the span of torsion classes \((B,-B,-1),(1,K,K)\) and \(\lambda=(d,1,d),\ \mu=(2330,-17009,-730)\). The embedded replay verifies local points for \(\lambda,\mu\) at every bad finite prime. At the real place choose \(x>m^2\) or \(0<x<B\) respectively. At any odd good prime the Kummer image consists of all four unit-square-class triples of square product: every image is unit in square class, and the finite reduction's quotient by 2 has size four because it has full 2-torsion (the formal kernel is uniquely 2-divisible). These observations show that the 16 possible classes are all in the 2-Selmer group.

Use the pairing formula as in [Shukla and Stoll, §3.2](https://arxiv.org/pdf/2302.01640v1). For each class \(C=(C_1,C_2,C_3)\), omit one coordinate \(z_i\) from its 2-cover equations to give the three diagonal conics used in the replay. Multiply the diagonal coefficients by the corresponding rational tangent point coordinates to get a tangent linear form \(L_i\). Take \(\prod_{v,i}(L_i(P_v),C'_i)_v\) using the stated local lift on the left-hand cover. At finite good primes neither coordinate of the class nor any tangent scale is nonunit. The conic is smooth, and projection of a primitive cover point to its three coordinates is still primitive: if all three were zero modulo p, the other cover equation would force the omitted coordinate to be zero too. If the tangent value vanishes modulo p then the projected point reduces to the smooth tangent point, as intersection multiplicity is two. Locally the conic in that chart has form \(aXZ+bY^2+cYZ+eZ^2=0\) with a and b units and tangent \(Z=0\). Its tangent value then has even valuation, hence Hilbert symbol +1 with the target unit. The embedded bad-place calculations give finite product +1 forward and -1 reverse. At the real place the reverse class is positive in all slots. For the forward pairing use positive \(z_i\) with x large on the \(\lambda\)-cover: \(L_2=(d-1)z_3-(d+1)z_1+4d<0\) and \(L_3=2dz_1-3z_2-B>0\) eventually, so the target signs of \(\mu\) give precisely one negative symbol. Both global pairings are therefore -1.

The pairing has rank at least two and the rational points modulo 2 are in its kernel. As the Selmer dimension is four and the torsion classes already supply two independent dimensions, the rational rank is zero. The good reductions at 7 and 11 have 4 and 12 points and bound torsion by four, attained by the full rational 2-torsion. This proves the claimed rational point set.

## Stability under right composition by a quadratic

Let \(k=\mathbb Q(i)\), let \(\alpha^2=u\), and put \(L_0=k(\alpha)=E(\alpha)\); irreducibility of f is established in [the root-field calculation](BOTH_ENDPOINTS_MOVING_DEG28.md). Writing a square root of \((\alpha-b)/a\) as \(x+y\alpha\) would force \(q^2=b^2-u\) by the earlier square-class calculation. Thus every nonzero rational multiple of \(\alpha-b\), for rational b, is nonsquare in \(L_0\).

If \(G\in\mathbb Q[T]\) of degree n and leading coefficient \(g_n\) gives \(f(G)\) irreducible, choose \(G(\beta)=\alpha\). Then \((G(T)-\alpha)/g_n\) is the minimal polynomial of \(\beta\) over \(L_0\), by the tower law. A reducible quadratic \(a(T-\eta)^2+b-\beta\) would make \((\beta-b)/a\) a square. Its relative norm is \((-1)^n(G(b)-\alpha)/(a^n g_n)\), which is nonsquare by the preceding assertion. Hence \(f(G(Q))\) stays irreducible when any rational quadratic Q is appended. An even quartic after rational translation is a chain of two quadratics, so there is no proper factor to swap in that symmetric degree-16 orbit model. This does not address general cubic, indecomposable quartic, or other factor-swap models.

### Offline replay (JavaScript with BigInt)

~~~javascript
const B=9633851n,m=4816930n,d=m/2n,K=m*m-B,rt=[0n,B,m*m];
const PB=[173n,233n,239n],PM=[2n,5n,481693n],PK=[73n,317846643713n], ps=[...PB,...PM,...PK];
const mod=(a,p)=>(a%p+p)%p;
function pow(a,n,p){a=mod(a,p);let r=1n;while(n){if(n&1n)r=r*a%p;a=a*a%p;n>>=1n}return r}
function ok(x){if(!x)throw Error('bad certificate')}
function split(a,p){ok(a!==0n);let v=0n;while(a%p===0n){a/=p;v++}return [v,a]}
function inv(a,M){let [r,s,x,y]=[a,M,1n,0n];while(s){const q=r/s;[r,s,x,y]=[s,r-q*s,y,x-q*y]}ok(r===1n||r===-1n);return mod(x*r,M)}
function cls(a){const [v,u]=split(a,2n);return [v%2n,mod(u,8n)].join(',')}
function bit(u,p){ok(u%p!==0n);return pow(u,(p-1n)/2n,p)===1n?0n:1n}
const prod=x=>x.reduce((u,v)=>u*v,1n);
for(const p of ps)for(let j=2n;j*j<=p;j++)ok(p%j!==0n);
ok(prod(PB)===B&&prod(PM)===m&&prod(PK)===K);
function dvs(ps){let n=[1n];for(const p of ps)n=n.concat(n.map(x=>x*p));return n}
let odd=0,rows=[];
for(const b of dvs(PB))for(const a of dvs(PM))for(const c of dvs(PK))for(const e of [-1n,1n]){
 const C=[b*a,e*b*c,e*a*c],goal=C.map(cls);
 if(PB.some(p=>bit(C[2],p)!==(b%p===0n?bit(-1n,p):0n)))continue;
 if(PK.some(p=>bit(C[0],p)!==0n))continue;
 if(PM.slice(1).some(p=>a%p===0n&&bit(C[1],p)!==0n))continue;
 odd++;
 let good=[1n,3n,5n,7n].some(u=>goal.every((v,j)=>v==='0,'+u)||goal.every((v,j)=>v==='0,'+mod(u-4n*rt[j],8n)));
 for(let x=0n;x<256n&&!good;x++)good=rt.every((r,j)=>(x-r)%64n===0n||cls(x-r)===goal[j]);
 if(good) rows.push([b,a,c,e].join(','));
}
const ex=[];for(const [b,aa,cc,e] of [[1n,[1n,d],[1n,K],1n],[B,[1n,d],[1n,K],-1n],[233n,[10n,963386n],PK,-1n],[41347n,[10n,963386n],PK,1n]])for(const a of aa)for(const c of cc)ex.push([b,a,c,e].join(','));
ok(odd===20&&rows.sort().join(';')===ex.sort().join(';'));
function tangent(C,pts){
 const [a,b,c]=C,forms=[[0n,b,-c,-K],[-a,0n,c,m*m],[a,-b,0n,-B]];
 return pts.map((P,i)=>{ok(forms[i].reduce((r,x,j)=>r+x*P[j]*P[j],0n)===0n);return forms[i].map((x,j)=>x*P[j])})
}
const lam=[d,1n,d],mu=[2330n,-17009n,-730n];
const L=tangent(lam,[[0n,m+3n,4n,1n],[d+1n,0n,d-1n,1n],[2n,3n,0n,1n]]);
const T=tangent(mu,[[0n,41109377n,198512215n,31n],[3371851n,0n,5298623n,45n],[45n,17n,0n,1n]]);
const data=[
[2n,23202814624964n,10n,[1n,1n,1n],[1n,1n,1n],'000','000'],
[5n,10n,5n,[2n,2n,2n],[1n,2n,2n],'000','101'],
[173n,1n,1n,[57n,1n,68n],[77n,56n,20n],'000','000'],
[233n,8n,23202814624938n,[42n,63n,103n],[111n,74n,77n],'110','000'],
[239n,1n,7n,[79n,1n,58n],[51n,83n,44n],'000','000'],
[73n,3n,9634362n,[3n,20n,18n],[28n,6n,21n],'011','000'],
[481693n,9633860n,2n,[2n,3n,2n],[76781n,176390n,134951n],'000','001'],
[317846643713n,2n,1n,[157947891272n,154125553803n,109005557090n],
 [22689800380n,120851660140n,154186108259n],'000','000']];
function lift(p,num,den,s){
 let [v,u]=split(num,p),[w,t]=split(den,p);let e=v-w,M=p**16n;
 ok(e%2n===0n);const U=mod(u*inv(t,M),M);
 if(p===2n){ok(U%8n===1n&&s%2n===1n);for(let j=3n;j<16n;j++)s+=mod((U-s*s)/2n**j,2n)*2n**(j-1n)}
 else{
  ok(mod(s*s-U,p)===0n&&s%p!==0n);
  const v=inv(2n*s,p);
  for(let j=1n;j<16n;j++)s+=mod((U-s*s)/p**j*v,p)*p**j;
 }
 ok(mod(s*s-U,M)===0n);
 return [e/2n,-s,(p===2n?15n:16n)+e/2n]
}
function hilbert(n,u,e,v,p){
 if(p===2n){u=mod(u,8n);v=mod(v,8n);return mod((u-1n)*(v-1n)/4n+n*((v*v-1n)/8n)+e*((u*u-1n)/8n),2n)}
 return mod(n*e*((p-1n)/2n)+e*bit(u,p)+n*bit(v,p),2n)
}
function calc(p,x,seeds,left,right,lines,ds){
 const Z=rt.map((r,j)=>lift(p,x-r,left[j],seeds[j]));let out='';
 for(let i=0;i<3;i++){
  const terms=[];
  for(let j=0;j<3;j++)if(lines[i][j]!==0n) terms.push([Z[j][0],lines[i][j]*Z[j][1],Z[j][2]+split(lines[i][j],p)[0]]);
  terms.push([0n,lines[i][3],1000n]);
  const min=terms.reduce((n,[v])=>v<n?v:n,0n);
  const sum=terms.reduce((n,[v,u])=>n+u*p**(v-min),0n);
  let [val,unit]=split(sum,p),[dv,du]=split(ds[i],p),[e,v]=split(right[i],p);
  val+=min;
  const small=p===2n?8n:p;
  ok(terms.every(([,,prec])=>prec-val>=(p===2n?3n:1n)));
  out+=hilbert(val-dv,unit*inv(du,small),e,v,p);
 }
 return out
}
let forward=1,reverse=0;
for(const [p,x,y,s,t,f,r] of data){
 const ff=calc(p,x,s,lam,mu,L,[1n,d,1n]),rr=calc(p,y,t,mu,lam,T,[1n,1n,1n]);
 ok(ff===f&&rr===r);
 forward+=Array.from(ff).filter(x=>x==='1').length;
 reverse+=Array.from(rr).filter(x=>x==='1').length;
}
ok(forward%2===1&&reverse%2===1);
for(const [p,want] of [[7n,4],[11n,12]]){let ct=1;for(let x=0n;x<p;x++)for(let y=0n;y<p;y++)if((y*y-x*(x-B)*(x-m*m))%p===0n)ct++;ok(ct===want)}
console.log("20 odd-place candidates, 16 survivors; forward and reverse pairings -1; good reductions 4 and 12");
~~~
