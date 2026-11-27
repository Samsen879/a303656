# A degree-12 double-moving integer orbit at a different true label

On the original j-line, take the genuine parent/child exponents \((d,c;e,f)=(1,2;2,3)\). This is a **different label** from \((10,2;11,3)\) in [the degree-20 construction](BOTH_ENDPOINTS_MOVING_DEG20.md); the cubic restriction for that fixed earlier factor is not being reversed. The construction here gives degree 12 for the common leading coordinate, and degrees 6 and 8 for the two leading-direction gaps.

Write \(L=363,\ \rho=2-L=-361,\ A=4-L^2,\ B=-L^2\). For the j-line
\[
 g=(j+219)^2+(2j+801)^2+2,\quad w=5j+1821,\quad n=25g+2,
 \quad 5g=w^2+L^2+10 .
\]
Its parent at \(\lfloor n/5\rfloor=5g\) subtracts \(3^2+5^1=14\); its child at n subtracts \(3^3+5^2=52\). The desired norms are \(w^2-A\) and \(5(w^2-B)\).

Put
\[
 h=\frac{361}{4}(T^3+T),\quad X=\rho h^2-2,\quad
 W=\frac{X^2+16+B}{8},\quad D=\frac{\rho^2h^2+A}{4},
 \quad G=W-D+ih(D-\rho),\quad F=W-4+iX .
\]
Expansion using \(\rho^2+A=4\rho\) gives \(N(G)=W^2-A,\ N(F)=W^2-B\).

## Pulling back a proper factor by a real cubic

Let \(\delta=4/361,\ q=1+i\delta,\ P=T^2+q\). Here \(8F=(X+4i-L)(X+4i+L)\), with \(X+4i+L=\rho(h^2-q)\), and
\[
 h^2-q=(T^2+q)\big(T^4+(2-q)T^2+(1-q)^2\big)/\delta^2 .
\]
This illustrates a transferable sufficiency condition: for a factor \(s^2-q\), \(q=c+i\delta\) with rational \(c,\delta\) and \(\delta\ne0\), the substitution \(s=(T^3+cT)/\delta\) produces \(T^2+q\) as a factor, since mod that factor \(T^2=-q\) and \(T^2+c=-i\delta\). An integral anchor remains a separate requirement.

Swap the proper factor by \(Z=\bar P F/P\). Its norm is \(W^2-B\), and its leading coefficient agrees with W. The expression \(Z=F-2i\delta F/P\) gives \(\deg\Im Z=10\): the leading coefficient of \(F/P\) is real, its degree is 10, and \(\Im F\) has degree 6. The identity \((W-\Re Z)(W+\Re Z)=(\Im Z)^2+B\) then gives real gap degree 8. The parent gap D has degree 6. Both are genuinely nonconstant.

## Real integral anchor and all-parameter congruences

At \(T_0=4\), \(h(T_0)=6137\). The constant rotation \(\gamma=(6137+4i)/(6137-4i)\) sends \(Z(4)\) to \(F(4)\). Then \(C=(1+2i)\gamma Z\) gives the true child norm. Exact anchor values are
\[
 W=23107284426213717446,\quad n=2669732967769695045495431335693624473477,
\]
with parent coordinates \((23107283199151320675,7530481931199084)\) and child coordinates \((23107284453406236664,46214568838831175273)\).

The coefficients of W and G have denominators dividing 2048 directly. For Z, the displayed quotient formula gives \(\bar P\) and the quartic factor with combined denominator dividing \(361^3\), canceled by \(\rho/(8\delta^2)=-361^3/128\). The remaining factor \(X+4i-L\) has denominator dividing 16, so 2048 also clears Z. For C it suffices to multiply the denominator by \(6137^2+16\). Take \(T=4+2314001510400k\), with step \(30\cdot2048(6137^2+16)\). The constant terms are the integral anchor; every nonconstant term of W, G and C is a multiple of 30. Thus \(W\equiv26\bmod30\), \(j=(W-1821)/5\) is integral, and both representations hold for every k. This proves a genuine unbounded degree-12 fixed-label integer orbit with moving endpoints, not a varying-label result or a proof of the original conjecture.

### Exact arithmetic replay

~~~javascript
const abs=x=>x<0n?-x:x,gcd=(a,b)=>b===0n?abs(a):gcd(b,a%b);
function rat(a,b=1n){const g=gcd(a,b)*(b<0n?-1n:1n);return [a/g,b/g]}
function plus([a,b],[c,d]){return rat(a*d+b*c,b*d)}
function neg([a,b]){return [-a,b]}
function sub(a,b){return plus(a,neg(b))}
function mul([a,b],[c,d]){return rat(a*c,b*d)}
const num=x=>[x,1n], sc=(r,x)=>mul(r,num(x)), div=(r,d)=>mul(r,rat(1n,d)),sq=x=>mul(x,x);
function cm([a,b],[c,d]){return [sub(mul(a,c),mul(b,d)),plus(mul(a,d),mul(b,c))]}
function cn([a,b]){return plus(sq(a),sq(b))}
function eq(a,b){return a[0]===b[0]&&a[1]===b[1]}
function ok(x){if(!x)throw Error("failed exact replay")}
const m=6137n,M=m*m+16n,step=30n*2048n*M;
ok(step===2314001510400n);
const rot=cm([num(1n),num(2n)],[rat(m*m-16n,M),rat(8n*m,M)]);
function f(t){
 const h=rat(361n*(t*t*t+t),4n),X=sub(sc(sq(h),-361n),num(2n));
 const W=div(plus(sq(X),num(16n-131769n)),8n),D=div(plus(sc(sq(h),361n**2n),num(-131765n)),4n);
 const G=[sub(W,D),mul(h,plus(D,num(361n)))],r=361n*(t*t+1n);
 const Z=cm([sub(W,num(4n)),X],[rat(r*r-16n,r*r+16n),rat(-8n*r,r*r+16n)]);
 return [W,D,G,Z,cm(rot,Z)];
}
const lines=[];
for(let j=-12n;j<=12n;j++){
 const [W,D,G,Z,C]=f(j);
 ok(eq(cn(G),plus(sq(W),num(131765n))));
 ok(eq(cn(Z),plus(sq(W),num(131769n))));
 ok(eq(cn(C),sc(plus(sq(W),num(131769n)),5n)));
 lines.push([W,D,Z[1],sub(W,Z[0])]);
}
function degree(a){let d=-1;while(a.some(x=>x[0]!==0n)){d++;a=a.slice(1).map((v,i)=>sub(v,a[i]))}return d}
ok(lines[0].map((_,i)=>degree(lines.map(row=>row[i]))).join(",")==="12,6,10,8");
for(const k of [-1n,0n,1n]){
 const [W,,G,,C]=f(4n+step*k);
 ok([W,...G,...C].every(x=>x[1]===1n)&&W[0]%30n===26n);
 const j=(W[0]-1821n)/5n,g=(j+219n)**2n+(2n*j+801n)**2n+2n,n=25n*g+2n;
 ok(5n*g===W[0]**2n+363n**2n+10n);
 ok(cn(G)[0]+14n===n/5n&&cn(C)[0]+52n===n);
 if(!k)ok(W[0]===23107284426213717446n&&n===2669732967769695045495431335693624473477n&&G.map(x=>x[0]).join(",")==="23107283199151320675,7530481931199084"&&C.map(x=>x[0]).join(",")==="23107284453406236664,46214568838831175273");
}

~~~
