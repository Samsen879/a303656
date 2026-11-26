# A genuine infinite first-248 family with four adjacent columns

There are infinitely many integers \(m\) whose \(x=5m+4\) has least true shift \(248=5+3^5\), and for which all four specified columns \(d=4,8,12,16\) have genuine parent and adjacent child norms simultaneously. This meets the challenge left by [the earlier isolated four-column seed](FIRST_248_FOUR_COLUMN_SEED_AND_OLD_LIMIT.md). It does so on a different congruence class and different base path; the [old common-cover obstructions](FOUR_COLUMN_COVER_PRIMITIVE_FACTOR_DESCENT.md) are unchanged.

## Exact seed and three preserved base columns

Take \(m=108052591109526\), \(x=540262955547634\). The first shift has \(x-248=4609381^2+22781935^2\). The four parent coordinate pairs in increasing d order are
\[
 (7398776,7301418),\quad (-7341524,7358982),\quad
 (-7343726,7356768),\quad (10028076,2708818).
\]
The 20 earlier shifts each have exact valuation one at a listed inert prime \(>3\); the offline replay checks the complete set and primality. Let \(M'\) be the product of the squares of the distinct blocking primes.

Set \(Q=367+369i,\ g=N(Q)=270850,\ S=5409768750\). For \(d=4,8,12\), take
\[
 (q_d)=(21127550,21125050,19499950),\qquad
 (\gamma_d)=(Q,\bar Q,\bar Q).
\]
The exact identities \(q_d^2-q_{12}^2=g(5^{12}-5^d)\) give a common parent curve
\[
 m(s)=5^{12}+1+(s^2+q_{12}^2)/g,\qquad
 Z_d(s)=(q_d+is)/\gamma_d,\quad
 N(Z_d(s))=m(s)-5^d-1.
\]
At \(s=S\) these are the stated integer anchors. For \(s-S\) divisible by g, all three coordinates remain Gaussian integers because \(g/\gamma_d=\bar\gamma_d\). Taking \(s-S\) divisible by \(4gM'\) in addition fixes \(m\bmod M'\) by expanding the difference \(s^2-S^2\), so the earlier-shift exclusions persist.

## Propagate the first root and fourth column by one Pell curve

The fourth parent \(m(s)-5^{16}-1\) and first-root remainder \(5m(s)+4-248\) are \(g^{-1}(s^2+h_{16})\) and \(5g^{-1}(s^2+h_{248})\) respectively, with
\[
 h_{16}=-40882056637497500,\qquad h_{248}=446373525337120 .
\]
Use the [two-gate seed identity](FIRST_248_RATIONAL_PULLBACK_SEED_EQUIVALENCE.md):
\[
 F_i=S^2+h_i,\quad \lambda_i=1/F_i,\quad
 b=S(\lambda_{248}+\lambda_{16})-1/S,\quad
 u_i=S\lambda_i-b/2,\quad a=\lambda_i-u_i^2.
\]
The same a works for both i. If \(Y^2=a\xi^2+b\xi\), then \(\lambda_i((S+\xi)^2+h_i)=(1+u_i\xi)^2+Y^2\). The replay gives exact \(a,b>0\) and \(4S^2a\equiv2\bmod3\), so a is nonsquare. Choose a positive denominator clearer W so \(A=W^2a,\ B=W^2b\) are positive integers. On the Pell orbit
\[
 T^2-AZ^2=B^2,\qquad \xi=(T-B)/(2A),\qquad Y=Z/(2W),
\]
start with \(T=B,Z=0\), and take a norm-one unit to a power preserving this pair modulo a common multiple of \(2A\cdot4gM'\), \(2A\) times both denominators of \(u_i\), and \(2W\). Such a power exists because multiplication by a norm-one unit is invertible modulo the chosen modulus. Iteration gives unbounded positive \(\xi\), with \(s-S\) in the required progression and \(u_i\xi,Y\) integral. Therefore genuine coordinates for the two extra residuals are obtained by multiplying their original seed coordinates by \(1+u_i\xi+iY\).

For each of the four positive parent norms the adjacent child \(x-5^{d+1}-3^2\) is exactly five times the parent, so multiplication by \(2+i\) gives the child integer coordinates. This verifies an infinite genuine four-column family, including all earlier-root blockers at the same point. It neither asserts five columns nor proves the universal representation conjecture.

### Exact offline seed and coefficient replay

~~~javascript
const m=108052591109526n,x=5n*m+4n,S=5409768750n,g=270850n;
const rows=[[4n,21127550n,7398776n,7301418n,1n],[8n,21125050n,-7341524n,7358982n,-1n],[12n,19499950n,-7343726n,7356768n,-1n],[16n,0n,10028076n,2708818n,0n]];
const bs=[[2n,9749851n],[4n,7n],[6n,2543n],[8n,23n],[10n,211n],[14n,127n],[26n,3371n],[28n,3643n],[32n,7n],[34n,450219129623n],[52n,4987n],[82n,23351614607n],[86n,20856491n],[106n,223n],[126n,107n],[128n,31n],[134n,607n],[152n,43n],[206n,443n],[244n,9391n]];
function ok(x){if(!x)throw Error("certificate mismatch")}
const early=new Set();
for(let e=0n;e<4n;e++)for(let f=0n;f<6n;f++){const j=5n**e+3n**f;if(j<248n)early.add(j)}
ok(early.size===bs.length);
for(const [r,p] of bs){
  ok(early.delete(r)&&p>3n&&p%4n===3n);
  for(let d=2n;d*d<=p;d++)ok(p%d!==0n);
  ok((x-r)%p===0n&&(x-r)%(p*p)!==0n);
}
ok(x-248n===4609381n**2n+22781935n**2n);
ok(367n**2n+369n**2n===g&&m===5n**12n+1n+(S*S+rows[2][1]**2n)/g);
for(const [d,q,a,b,sgn] of rows){
  ok(m-5n**d-1n===a*a+b*b);
  ok(x-5n**(d+1n)-9n===(2n*a-b)**2n+(a+2n*b)**2n);
  if(sgn){
    ok(a*367n-b*369n*sgn===q&&a*369n*sgn+b*367n===S);
    ok(q*q-rows[2][1]**2n===g*(5n**12n-5n**d));
  }
}
const q=rows[2][1];
const hh=[q*q+g*(5n**13n-239n)/5n,q*q+g*(5n**12n-5n**16n)];
ok(hh.join(",")==="446373525337120,-40882056637497500"&&g%5n===0n);
const abs=x=>x<0n?-x:x,gcd=(a,b)=>b===0n?abs(a):gcd(b,a%b);
function rat(a,b){const g=gcd(a,b)*(b<0n?-1n:1n);return [a/g,b/g]}
function add([a,b],[c,d]){return rat(a*d+b*c,b*d)}
function neg(a){return [-a[0],a[1]]}
function mul([a,b],[c,d]){return rat(a*c,b*d)}
const L=hh.map(h=>rat(1n,S*S+h));
const b=add(mul([S,1n],add(...L)),rat(-1n,S));
const a=L.map(l=>{const u=add(mul([S,1n],l),mul(neg(b),[1n,2n]));return add(l,neg(mul(u,u)))});
ok(a[0].join(",")===a[1].join(",")&&a[0][0]>0n&&b[0]>0n);
const v=mul([4n*S*S,1n],a[0]);
ok(v[1]%3n!==0n&&(v[0]-2n*v[1])%3n===0n);

~~~
