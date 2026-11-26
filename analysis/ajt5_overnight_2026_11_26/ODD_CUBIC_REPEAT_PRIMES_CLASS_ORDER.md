# Repeated primes and a class-order obstruction to an odd cubic

Continue [the global numerator obstruction](ODD_CUBIC_GLOBAL_NUMERATOR_OBSTRUCTION.md) with \(t=A/D^3,\ w=Dz,\ w^2(w-D)=Au\). Put \(F^-=\mathbb Q(\eta)\), \(\eta=i\sqrt B\); write \(n=N_{E/F^-}(w)\), and remove its rational integer content to get the primitive \(n_0\). For a rational prime p split in \(F^-\), let \(d_p\) be the absolute difference of the exponents of n at its two primes. This gives the exponent of p in the norm of \(n_0\).

Every solution has (i) some \(d_p>0\) at a split prime \(p\nmid2BN\), where \(N=N_{E/\mathbb Q}u\), or (ii) \(d_5\ge3\) or \(d_p\ge2\) for some \(p\in\{17,368793917,3434854150155653\}\). In (i), \(v_p(A)=2r>0\) must be even, because the coprime ideal factorization of \(w^2(w-D)\) permits an upstairs exponent only of 0 or r. In the fully split case \(p\equiv1\bmod4,(B/p)=1\), \(d_p=r\) or \(2r\). In the case \(p\equiv3\bmod4,(B/p)=-1\), the local extension over each of the two primes of \(F^-\) has residue degree two, so \(d_p=2r\). Moreover at least one of the roots \(s^2=-B\bmod p\) must satisfy
\[
   ( (K+4+4s)/p )=1,\qquad K=m^2-B.
\]
Indeed where \(v(w)=r\), divide the original equation by the even valuation of A. The rational residue factors are squares in \(\mathbb F_{p^2}\); this forces u square there, equivalent to its norm \(K+4+4s\) being square in \(\mathbb F_p\). At \(p=31\) both signs fail, regardless of the repetition exponent. Inert primes in \(F^-\) cannot contribute to \(d_p\) at all.

## Why the old norm support cannot suffice, even with repetitions

If neither (i) nor (ii) holds, the norm of \(n_0\) is among the previous 96 classes. At ramified primes 173,233, rational integer content removes all but parity in the downstairs exponent even without an upper bound upstairs. At 239 the relative residue degree two makes the exponent even, also removed by content. At 2 the prime is inert in \(F^-\), and any contribution is removed. So by the old exact enumeration, and the nonreal relative-norm argument, \(n_0=\pm(K+4\pm4\eta)\). Taking respectively \(\nu=u\) or \(\bar u\) makes \(N_{E/F^-}(z/\nu)\) rational. As in the previous relative-norm argument, this means \(z=(r+is)v\nu\) for some \(v\in\mathbb Q(\sqrt B)^\times\) and \((r:s)\in\mathbb P^1(\mathbb Q)\).

Let \(J=u\bar u,\ C=(r+is)\nu,\ H=C^2\bar u,\ U=\Im H,\ V=\Im(CH)\). The equation is \(tJ=v^2(vCH-H)\), whose imaginary part gives \(vV=U\). If \(V=0\) then H and CH are both real, forcing C real, impossible because \(2s\pm r(\sqrt B-m)\ne0\) for these projective pairs. Substitution, using \(\Re(CH)U-\Re(H)V=-\Im(C)|H|^2\), gives
\[
 t=-(r^2+s^2)^2 J^2\,\Im(C)U^2/V^3 .
\]
Thus the \(\sqrt B\) coefficient of \(J^2\Im(C)U^2(V^\sigma)^3\) must vanish, with \(\sigma\) flipping \(\sqrt B\). This is a homogeneous integral form. The exact projective checks below, modulo 11 for \(\nu=u\) and modulo 7 for \(\nu=\bar u\), reject every point, including infinity. This proves the claimed necessity of new or expanded asymmetric support.

## Exact 3-power restriction

If \(A=\pm3^k\), then \(k>0\) and \(78\mid k\). In fact 3 is the only possible support of the primitive relative norm, and it is split in \(F^-\). The local square test just derived permits only the side \(\mathfrak p=(3,\eta-1)\). Nonreality of \(n_0\) forces \(k=2r>0\), with \((n_0)=\mathfrak p^{\,k}\). The class of \(\mathfrak p\) has exact order 78: the displayed norm certificate below gives a primitive element of norm \(3^{78}\) and the three reduced lattice certificates rule out primitive norm at \(3^{39},3^{26},3^6\). These are the three possible maximal proper divisors of 78. A nonreal generator on either branch would give a primitive norm vector in the indicated lattice, after conjugation if necessary. As before, completeness of the coefficient range \([-2,2]\) follows from reduced angle and the norm floor \(M=3^e\).

In contrast, \(t=9\) has a genuine 3-adic asymmetric solution. At \(\eta\equiv1\pmod3\), put \(z=3y\); reduction gives \(y^2=i\), solved by \(1-i\) with unit derivative. On the other side use the simple \(z\equiv1\) root. Hensel lifting on both sides gives the locally allowed \(d_3=2\), which the class order excludes globally for this A. No admissible repeated-prime numerator or integer-anchored cubic is constructed. This gives a conditional restriction on the class of a product of several support primes, not a general elimination.

~~~javascript
const B=9633851n,m=4816930n;
const mod=(x,p)=>(x%p+p)%p,abs=x=>x<0n?-x:x;
function ok(x){if(!x)throw Error("certificate mismatch")}
function table(p,side){
 const ar=(a,b)=>[mod(a[0]+b[0],p),mod(a[1]+b[1],p)],neg=a=>a.map(x=>mod(-x,p));
 const mul=(a,b)=>[mod(a[0]*b[0]+B*a[1]*b[1],p),mod(a[0]*b[1]+a[1]*b[0],p)];
 function pow(a,n){let r=[1n,0n];for(let i=0;i<n;i++)r=mul(r,a);return r}
 const cm=(a,b)=>[ar(mul(a[0],b[0]),neg(mul(a[1],b[1]))),ar(mul(a[0],b[1]),mul(a[1],b[0]))];
 const y=[mod(-m,p),1n],nu=[[2n,0n],side===1?y:neg(y)],un=[[2n,0n],neg(y)],J=ar([4n,0n],mul(y,y));
 const f=(r,s)=>{
  const C=cm([[r,0n],[s,0n]],nu),H=cm(cm(C,C),un),U=H[1],V=cm(C,H)[1];
  return mul(mul(pow(J,2),C[1]),mul(pow(U,2),pow([V[0],mod(-V[1],p)],3)))[1];
 };
 return [...Array(Number(p)).keys()].map(j=>f(1n,BigInt(j))).concat([f(0n,1n)]);
}
ok(table(11n,1).join(",")==="1,8,7,7,9,7,7,4,2,3,2,9");
ok(table(7n,-1).join(",")==="1,5,3,4,3,6,2,6");
const dot=(a,b)=>a[0]*b[0]+B*a[1]*b[1];
for(const [e,r,v,w] of [
 [6n,145n,[729n,0n],[145n,1n]],
 [26n,886074159376n,[-53568847n,-22195n],[79040173n,-14702n]],
 [39n,1003740489962199883n,[-47683533149n,12889351n],[-141810095652n,-46655835n]]
]){
 const M=3n**e;
 ok(r%3n===1n&&mod(r*r+B,M)===0n);
 ok([v,w].every(([x,y])=>mod(x-r*y,M)===0n));
 ok(abs(v[0]*w[1]-v[1]*w[0])===M&&2n*abs(dot(v,w))<=dot(v,v)&&dot(v,v)<=dot(w,w));
 for(let a=-2n;a<=2n;a++)for(let b=-2n;b<=2n;b++){
  const xy=[a*v[0]+b*w[0],a*v[1]+b*w[1]];
  ok(!(xy[1]%3n!==0n&&(xy[0]-xy[1])%2n===0n&&dot(xy,xy)===4n*M));
 }
}
const xy=[1408359708906741425n,-2571589103253541n];
ok(xy[1]%3n!==0n&&(xy[0]-xy[1])%2n===0n&&dot(xy,xy)===4n*3n**78n);
const K=m*m-B;const sq=new Set(Array.from({length:31},(_,i)=>BigInt(i*i%31)));
ok([9n,22n].every(s=>mod(s*s+B,31n)===0n&&!sq.has(mod(K+4n+4n*s,31n))));
ok(mod(K+4n+4n,3n)===1n&&mod(K+4n-4n,3n)===2n);

~~~
