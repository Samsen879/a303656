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

### Fifth-column diagnostic on this exact orbit

The fifth residual of interest has numerator
\[
  g(m(s)-5^{20}-1)=s^2-25829822486324997500.
\]
Writing the Pell multiplier as \(U+V\sqrt A\) and multiplying the seed \((T,Z)=(B,0)\) gives \(s=S+B(U-1)/(2A)\). In particular there is no term \(WV\) in \(s\); such a term would belong to a different seed. Take \(W\) to be the square root of the reduced denominator of \(a\) above (this denominator is an exact square), \(A=W^2a,\ B=W^2b\).

Reduction gives the following complete local zero tests for the numerator. All entries in the first four numeric columns are residues modulo the stated prime; \(e=B/(2A)\), and \(C=25829822486324997500\).

| \(p\) | \(A\) | \(S\) | \(e\) | \(C\) | \((U,V)\) with \(U^2-AV^2=1,\ (S+e(U-1))^2=C\) |
|---:|---:|---:|---:|---:|---|
| 19 | 16 | 1 | 1 | 4 | none |
| 103 | 7 | 72 | 37 | 25 | \((66,\pm28),(88,\pm49)\) |
| 419 | 210 | 252 | 9 | 225 | none |

The rows are directly reproducible by testing every pair modulo the respective prime. At 103 the four zero pairs all have 51st power \((-1,0)\) under quadratic-algebra multiplication. But a multiplier with \(U\equiv1\bmod16A,\ V\equiv0\bmod16\), an admissible strengthening of the original preservation modulus, is itself a norm-one square. Indeed \((U+1)/2\) is odd and coprime to \(A\). Its prime valuations are all even by \((U-1)(U+1)=AV^2\) and \(\gcd(U-1,U+1)\mid2\). Write \((U+1)/2=h^2\); then \(h\mid V\), and \(h\) is odd while \(V\) is even. Thus
\[
  U+V\sqrt A=(h+(V/(2h))\sqrt A)^2,
\]
with integral coefficients and norm one in the parentheses. Every such square has 51st power 1 modulo 103 (the norm-one group has order 102 here; \(7\) is a square modulo 103). It cannot hit any of the four zero pairs. This supplies three local primes that cannot obstruct the fifth residual on this strengthened orbit. It does not imply that the residual is a norm or that a second five-column point exists.

### A power-pullback obstruction for the fifth column at 131

On the same Pell conic with the same projection \(s=S+e(U-1)\), no positive power pullback of \(f/g=(s^2-C)/270850\) can be a sum of two rational-function squares. Here a power pullback means composing with \([n]\colon U+V\sqrt A\mapsto(U+V\sqrt A)^n\) on the entire rational norm-one conic; this does not assert failure at individual integral points of the much thinner preservation orbit.

Modulo 131 the residues of \((A,e,S,C)\) are \((69,71,86,44)\); 69 is nonsquare. Solving the norm equation and \(f=0\) gives \((75,\pm22)\). For \(R=(75,22)\), the third, eleventh and thirty-third powers are respectively \((126,60),(65,79),(1,0)\), so \(R\) has order 33. Its unique order-33 lift \(\tau\) to the unramified norm-one torus has reduction \((10031,7227)\bmod131^2\): this pair has norm one, 33rd power one, and the required reduction. Direct substitution gives \(f(\tau)\equiv13\cdot131\bmod131^2\). For comparison the actual zero lift has residue \((5708,10371)\bmod131^2\). All the arithmetic uses multiplication \((a,b)(c,d)=(ac+Abd,ad+bc)\).

For a given positive \(n\), put \(r=3^{v_3(n)}11^{v_{11}(n)}\). The group over the finite field of order \(131^r\) is cyclic of order \(131^r+1\), since \(r\) is odd and 69 stays nonsquare. For \(\ell=3,11\), lifting the odd power gives \(v_\ell(131^r+1)=1+v_\ell(r)\). Hence \(33\mid(131^r+1)/\gcd(n,131^r+1)\), so \(R\) has an \(n\)-th root in this finite norm-one group. Lift that root multiplicatively to the unramified degree-\(r\) extension of \(\mathbb Q_{131}\). Its \(n\)-th power is exactly \(\tau\). The pulled-back \(f/g\) therefore takes an odd valuation (one) on an open neighborhood of this point. The residue field still has \(-1\) nonsquare; every nonzero sum of two squares there in the local field has even valuation, as the terms of least valuation cannot cancel. Evaluating any proposed rational-function identity at a point of this open neighborhood outside its finitely many poles gives a contradiction.

The least odd finite-field extension degree in which either residual zero has an \(n\)-th root is exactly \(r\), by the same cyclic-group criterion and valuations for every odd degree. This local obstruction says something about rational-function parametrizations, not the number of integer fifth-column witnesses.

### Actual fifth-coordinate line fibers

For an integer line \(a u+b v=c\) with \(D=a^2+b^2>0\), the fifth norm equation \(g(u^2+v^2)=s^2-C\) is exactly equivalent to the following generalized Pell equation **with** its reconstruction conditions:
\[
 z^2-gD\,t^2=D^2C+gD c^2,\quad z=Ds,\quad
 D\mid ac+bt,\quad D\mid bc-at .
\]
Here \(t=bu-av\); the two divisibilities recover \(u=(ac+bt)/D,\ v=(bc-at)/D\). In one direction this follows from \(D(u^2+v^2)=c^2+t^2\), and the converse uses the recovered coordinates. When intersecting with the original four-column construction, \(s\) must still be \(S+B(U-1)/(2A)\) from that construction; the new equation alone does not impose this.

For example, fixing the seed's first coordinate \(3294138\) gives \(s^2-270850v^2=28768909323735464900\), with \(s=S,\ v=1354184\) at the seed. The reconstruction conditions genuinely matter: for \((a,b)=(1,2)\) on this same witness, \(c=6002506,\ D=5\), and \(t=5234092\) works but replacing it by \(-5234092\) still solves the Pell equation and fails the divisibilities.

The original \(A\) has \(v_{227}(A)=1\) for the denominator clearer used above, as follows from the stated \(a\) formula. Since \(227\equiv3\bmod4\), both \(g=367^2+369^2\) and \(D\) have even valuation there. Therefore if \(gD\) is nonsquare this second Pell field is distinct from \(\mathbb Q(\sqrt A)\). The field distinction and line reduction do not exclude unrestricted integer fifth coordinates.

### A p-adic obstruction to an integer Gaussian-square displacement

Put \(p=9949\), \(z_0=3294138+1354184i\), and \(\delta=e(U-1)\) as in the original \(y=0\) track. At any nonseed integer Pell multiplier that lies in the norm-one square subgroup modulo \(p\), a fifth integer witness cannot have the form
\[
 z=z_0+\lambda\delta(a+bi)^2
 \quad (a,b,\lambda\in\mathbb Q,\ \lambda\ne0,\ v_p(\lambda)\text{ even}).
\]
This permits both the direction and its scalar to vary with the point. It applies to the strengthened preservation orbit above, but not to arbitrary fifth coordinates.

The exact coefficients have \(p\nmid Ag,\ v_p(e)=1,\ e/p\equiv2S/p\equiv3059\bmod p\). Also \(N(z_0)\equiv4491\bmod p\) is nonsquare, and \(A\) is square modulo \(p\). The split norm-one group has order \(p-1=4\cdot2487\); its square subgroup cannot have an element with \(U=0\), since that would have order four. Thus \(v_p(2S+\delta)=1\) by \((2S+\delta)/p\equiv3059U\bmod p\). Meanwhile \(v_p(\delta)\) is odd: it is one if \(U\not\equiv1\bmod p\), and otherwise \((U-1)(U+1)=AV^2\) makes it \(1+2v_p(V)\).

Define \(Q(a,b)=3294138(a^2-b^2)+2\cdot1354184ab\). Nonsquareness of \(N(z_0)\) makes \(Q\) anisotropic modulo \(p\); for \(k=\min(v_p(a),v_p(b))\) and nonzero \((a,b)\) it has valuation \(2k\). The minimum valuation of the two coordinates of \((a+bi)^2\) is also \(2k\), since their reductions cannot both vanish after removing \(p^{2k}\). Integrality of \(z\) therefore forces \(v_p(\lambda\delta)+2k\ge0\), and this value is odd, so it is positive. Expanding the exact norm and dividing by \(\lambda\delta\) gives
\[
  2gQ(a,b)+g\lambda\delta(a^2+b^2)^2=(2S+\delta)/\lambda .
\]
The left side has valuation \(2k\), as its second term has valuation strictly greater than \(2k\); the right side has odd valuation. This is a contradiction. If \(a=b=0\), the same norm equation already fails since \(\delta(2S+\delta)\ne0\).

The scalar parity condition is genuine. With \(U\equiv1\bmod p\) and \(\lambda=p\), the normalized equation modulo \(p\) has a nonsingular solution \((a,b)=(7191,3)\), of \(a\)-derivative \(9932\bmod p\). This passes the \(p\)-adic test by lifting, without claiming a global fifth point.
