# Exact rational-function capacity of the genuine first-248 four-column conic

On the fixed Pell conic of [the infinite first-248 family](FIRST_248_FOUR_COLUMNS_TWO_DIRECTIONS_PELL.md), the only nonnegative d for which the parent remainder \(m-5^d-1\) has a rational-function two-square identity are
\[
 d=4,\ 8,\ 12,\ 16.
\]
The same assertion holds for the corresponding adjacent children, since their remainders differ by the norm multiplier 5. This is a capacity statement for that exact conic, not a restriction on incidental arithmetic extra columns at some of its integer points.

## General reusable test

On \(Y^2=a(s-S)^2+b(s-S)\) with rational nonzero b, use the rational coordinate \(t=Y/(s-S)\), so \(s=S+b/(t^2-a)\). Take a rational target \(c(s^2+h)\) with \(c\ne0\) and \(F=S^2+h\ne0\). If it is a two-square norm, \(cF\) is a rational norm by specialization at the real rational anchor \(t=\infty\): poles in two real square coordinates cannot cancel. Suppose \(cF\) is a rational norm. Divide by it and multiply by \((t^2-a)^2\) to get the monic quartic
\[
 t^4+B_1 t^2+D_1,\qquad
 B_1=-2a+2Sb/F,\qquad D_1=a^2+(b^2-2aSb)/F .
\]
A monic rational polynomial that is a norm from \(\mathbb Q(i)(t)\) is already a norm of a monic polynomial: fixed irreducible factors have even multiplicity, and conjugate pairs are assigned to opposite factors. Here the monic factor is quadratic, \(t^2+i v t+r+i w\) with rational coefficients, by the zero cubic coefficient. Its linear term forces \(vw=0\). If \(v=0\), comparison requires \(w^2=D_1-B_1^2/4=b^2h/F^2\). If \(w=0\), it instead requires \(r^2=D_1,\ v^2=B_1-2r\). Thus the exact test is \(h\) a rational square, or \(D_1\) and at least one \(B_1\pm2\sqrt{D_1}\) rational squares. This accounts for arbitrary rational-function coordinates on the conic, not just those used in its original parametrization.

## Applying it at the exact four-column seed

Use \(g=270850,\ S=5409768750,\ q=19499950\) and \(h_d=q^2+g(5^{12}-5^d)\), with \(c=1/g\). For every \(d\ge21\) the anchor already has \(m-5^d-1<0\), so no rational norm identity exists. In the range \(0\le d\le20\), the four included exponents are known norms by the original proof. At each of the other 17, the following replay gives a nonresidue obstruction both to \(h_d\) being square and to \(D_1\) being square, with invertible reduced denominator. This rules out the two alternatives regardless of the anchor norm status. At any odd-degree finite pullback, a new identity would by field norm transitivity give an odd power of the original target as a Gaussian norm; its even powers are already norms. Hence the exclusions persist under odd-degree pulls. Even-degree covers, different base conics and purely arithmetic subsequences remain outside this result.

~~~javascript
const S=5409768750n,g=270850n,q=19499950n,m=108052591109526n;
const abs=x=>x<0n?-x:x,gcd=(a,b)=>b===0n?abs(a):gcd(b,a%b);
function rat(a,b){const u=gcd(a,b)*(b<0n?-1n:1n);return [a/u,b/u]}
function plus([a,b],[c,d]){return rat(a*d+b*c,b*d)}
function times([a,b],[c,d]){return rat(a*c,b*d)}
const scale=(r,n)=>times(r,[n,1n]), sq=r=>times(r,r);
const lam=[446373525337120n,-40882056637497500n].map(h=>rat(1n,S*S+h));
const b=plus(scale(plus(...lam),S),rat(-1n,S));
const a=plus(lam[0],scale(sq(plus(scale(lam[0],S),times(b,[-1n,2n]))),-1n));
const mod=(x,p)=>(x%p+p)%p;
function pow(a,e,p){let x=1n;a=mod(a,p);while(e){if(e&1n)x=x*a%p;a=a*a%p;e>>=1n}return x}
function reduce(r,p){if(r[1]%p===0n)throw Error("bad denominator");return mod(r[0]*pow(r[1],p-2n,p),p)}
function ok(x){if(!x)throw Error("failed witness")}
const t=[[0,17,5,7,6],[1,7,5,7,5],[2,13,7,7,3],[3,7,6,11,8],
 [5,7,3,13,5],[6,13,7,7,6],[7,7,5,7,5],[9,7,6,11,6],
 [10,13,7,13,6],[11,7,3,17,7],[13,7,5,7,5],[14,13,7,7,3],
 [15,7,6,41,12],[17,7,3,11,10],[18,13,7,7,6],[19,7,5,7,5],[20,19,15,7,3]];
for(const [d,p,u,l,v] of t.map(row=>row.map(BigInt))){
 const h=q*q+g*(5n**12n-5n**d),F=S*S+h;
 ok(F!==0n&&mod(h,p)===u&&pow(u,(p-1n)/2n,p)===p-1n);
 const D=plus(sq(a),times(plus(sq(b),scale(times(a,b),-2n*S)),rat(1n,F)));
 ok(reduce(D,l)===v&&pow(v,(l-1n)/2n,l)===l-1n);
}
ok(t.map(r=>r[0]).join(",")===[...Array(21).keys()].filter(d=>![4,8,12,16].includes(d)).join(","));
ok(m-5n**21n-1n<0n);

~~~
