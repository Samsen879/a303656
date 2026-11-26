# A genuine fifth column at the seed, and the common-denominator capacity check

The seed \(m=108052591109526,\ x=5m+4\) of [the first-248 infinite four-column family](FIRST_248_FOUR_COLUMNS_TWO_DIRECTIONS_PELL.md) actually has **exactly five** true parent columns with their adjacent children: \(d=4,8,12,16,20\). The fifth is
\[
 m-5^{20}-1=3294138^2+1354184^2,\qquad
 x-5^{21}-9=5234092^2+6002506^2.
\]
The original 20 earlier-root blockers still hold. The replay proves that every other active parent exponent fails by an inert prime of odd valuation, and \(d\ge21\) is not active at this seed. The [exact fixed-conic capacity result](FIXED_FOUR_COLUMN_CONIC_CAPACITY.md) excludes this fifth target as a rational-function identity on the earlier four-column Pell curve; the seed itself shows why that exclusion is not an arithmetic pointwise impossibility.

## A finite transferable check for four or more affine base columns

For a general base b, suppose \(Z_d(s)=(q_d+is)/\gamma_d\) with \(\gamma_d\in\{\gamma,\bar\gamma\}\), where \(\gamma=a+ic\) is a Gaussian integer of norm g. Any common divisor of a and c can first be divided out, since at an integer anchor it divides both \(q_d\) and s. Thus assume \((a,c)=1\). If the norms have a common parent function plus translation \(-b^d\), one needs \(q_d^2+g b^d=C\) independent of d. Replacing \(q_d\) by its negative can switch from \(\bar\gamma\) to \(\gamma\) (conjugate and multiply by -1). For fixed orientation \(\gamma\), simultaneous integrality is then exactly that the signed \(q_d\)'s have a common residue modulo g. Indeed \((a,g)=1\), and \(s\equiv c a^{-1}q_d\bmod g\) makes the two coordinates integral and is necessary. The unit norm g=1 is the trivial residue case.

For three distinct chosen exponents in order, put \(\Delta_1=b^{d_1}-b^{d_0},\ \Delta_2=b^{d_2}-b^{d_1}\). Change all signs if necessary so \(q_0>0\). Then \(k=(q_0-q_1)/g>0\) divides \(\Delta_1\), and \(\ell=(q_1-q_2)/g\ne0\) is a signed divisor of \(\Delta_2\). Their sum is nonzero, since otherwise \(q_0=q_2\). Consequently
\[
 g=\frac{\Delta_1/k-\Delta_2/\ell}{k+\ell},\qquad
 q_0=(\Delta_1/k+kg)/2,\qquad C=q_0^2+g b^{d_0}.
\]
Only positive integral g and \(q_0\) are allowed. For g to have a primitive Gaussian representative, it must have no prime factor 3 modulo 4 and \(4\nmid g\); these conditions suffice by choosing one Gaussian prime above each split odd prime. For any additional d check that \(C-gb^d\) is a nonnegative square with a signed root in the common residue. This is a complete finite test once three exponents are fixed.

For base 5 and first three \(4,8,12\) the exact count is 185 integer configurations, 20 with primitive Gaussian g, and \(\max\lfloor C/g\rfloor=38147265937<5^{16}\). None of the other \(0\le d\le15\) passes. The replay also excludes affine common-denominator models for every choice of four out of the five seed exponents. As a portability check, ordinary offsets \(1,9,18,22\) do permit a four-column shared denominator \(2+i\): the signed \(q=(11,-9,6,-4)\) are all 1 modulo 5, their \(q^2+5\cdot\text{offset}\) equals 126, and \(s=3\bmod5\) provides integral coordinates. The obstruction is specific to the listed exponential offsets and the common-denominator model, not a general limit on three or more simultaneous base columns. No infinite five-column family is proved here.

~~~javascript
const b=5n;
function mod(a,p){return (a%p+p)%p}
function ok(x){if(!x)throw Error("certificate mismatch")}
function divs(n){
 let out=[1n];
 for(let p=2n;p*p<=n;p++)if(n%p===0n){const start=out.slice();let v=1n;while(n%p===0n){n/=p;v*=p;out.push(...start.map(x=>x*v))}}
 if(n>1n)out.push(...out.map(x=>x*n));return out;
}
function primitive(g){
 if(g%4n===0n)return false;
 for(let p=2n;p*p<=g;p++)if(g%p===0n){if(p%4n===3n)return false;while(g%p===0n)g/=p}
 return g%4n!==3n;
}
function sqrt(n){if(n<0n)return -1n;let l=0n,r=1n<<BigInt(Math.ceil(n.toString(2).length/2)+1);while(r-l>1n){const t=(l+r)/2n;if(t*t>n)r=t;else l=t}return l*l===n?l:-1n}
function configs(d){
 const P=d.map(e=>b**BigInt(e)),D=P[1]-P[0],E=P[2]-P[1];
 const dd=divs(D),ee=divs(E);let out=[];
 for(const k of dd)for(const l0 of ee)for(const l of [l0,-l0]){
  const den=k+l,num=D/k-E/l;
  if(!den||num%den!==0n)continue;
  const g=num/den;
  if(g<=0n)continue;
  const s=D/k+k*g;
  if(s%2n||s<=0n)continue;
  const q=s/2n,c=q*q+g*P[0];
  out.push([g,c,q]);
 }
 return out;
}
function check(a,e){
 const [g,c,q]=a;
 const s=sqrt(c-g*b**BigInt(e));
 return s>=0n&&(mod(s-q,g)===0n||mod(-s-q,g)===0n);
}
const raw=configs([4,8,12]),good=raw.filter(([g])=>primitive(g));
ok(raw.length===185&&good.length===20);
ok(good.reduce((p,[g,c])=>c/g>p?c/g:p,0n)===38147265937n);
for(let d=0;d<=15;d++)if(![4,8,12].includes(d))ok(good.every(a=>!check(a,d)));
const ex=[4,8,12,16,20];
for(let q=0;q<5;q++){
 const d=ex.filter((_,j)=>q!==j);
 ok(configs(d.slice(0,3)).filter(([g])=>primitive(g)).every(a=>!check(a,d[3])));
}
const m=108052591109526n,x=5n*m+4n;
ok(m-5n**20n-1n===3294138n**2n+1354184n**2n);
ok(x-5n**21n-9n===5234092n**2n+6002506n**2n);
ok(m-5n**21n-1n<0n);
for(const [q,h] of [[11n,1n],[-9n,9n],[6n,18n],[-4n,22n]])
 ok(q*q+5n*h===126n&&(2n*q+3n)%5n===0n&&(6n-q)%5n===0n);

for(const [d,p] of [[0n,127n],[1n,3n],[2n,607n],[3n,47n],[5n,3n],[6n,9562176203n],[7n,3n],[9n,7n],[10n,23n],[11n,3n],[13n,3n],[14n,37463n],[15n,3n],[17n,3n],[18n,859339603n],[19n,3n]]) {
  ok(p%4n===3n);
  for(let j=2n;j*j<=p;j++)ok(p%j!==0n);
  let n=m-5n**d-1n,e=0;
  while(n%p===0n){n/=p;e++}
  ok(e%2===1);
}
~~~
