# Elliptic quotient and a finite integer exclusion for the shared cover

Continue [the necessary genus-five locus](FIRST_248_FOUR_COLUMN_MULTICOVER_LIMIT.md), with \(S=137672257015\), \(F_i=S^2+h_i\), and \(w_i^2=(\sigma^2+h_i)/F_i\) for the first root and columns 8 and 12. Write \(A_i=10F_i\), \(L=435419568970\). The product of the three \(A_i\) is \(DL^2\), with
\[
D=54420943797756604224326386906204441996505463449.
\]
An elliptic quotient is
\[
 E:\ Y^2=\prod_i (X+DA_i),\qquad
 X=10D(\sigma^2-S^2),\qquad Y=D^2 L\prod_i w_i.
\]
Here \(X+DA_i=DA_i w_i^2\), so the square classes lie in the 2-descent class of the seed \(P=(0,D^2L)\). This is a necessary extra structure, not just another finite residue screen. The two good reductions at 7 and 11 have 12 and 16 points. Prime-to-characteristic torsion reduction at these two primes bounds rational torsion by 4, and the three distinct rational 2-torsion points attain it. Since \(P\) is not a 2-torsion point, it has infinite order. Thus the elementary square-class restriction to this elliptic quotient alone cannot establish finiteness of the candidate set: its coset \(P+2E(\mathbb Q)\) is infinite. The extra condition that \(S^2+X/(10D)\) be a square remains.

## An exact bounded integer result

Let \(C_i=10,1,1\) respectively, \(H_i=C_i h_i\) and \(B_i=C_i F_i\). The \(B_i\) are squarefree integers and the union of their prime factors has product D. If \(\sigma=a/b\) in lowest terms, the necessary equations force \(B_i(w_i b)^2=C_i a^2+H_i b^2\). A rational number whose square multiplied by a squarefree integer is integral must already be integral. Thus for every prime \(p\mid B_i\) one has \(a^2\equiv S^2 b^2\bmod p\), since \(p\nmid C_i\). The replay checks all 64 corresponding CRT classes; for integral \(\sigma\) in \([-D,D]\) the only candidates satisfying all three full equations are \(\sigma=\pm S\). These two values do not furnish an unbounded common-cover family: \(+S\) is the degenerate double-root case, and \(-S\) with positive leading coefficient would require all \(a F_i\) to be squares for a single positive rational a, which fails by the differing 2-adic parities. With negative leading coefficient the real s-domain for opposite endpoints is bounded.

This note does not classify rational \(\sigma\) of arbitrary height or prove a global four-column obstruction.

~~~javascript
const S=137672257015n, C=[10n,1n,1n];
const H=[28173484023085671807211n,2817344150684665342984n,2814690812686254405484n];
const B=H.map((h,i)=>h+C[i]*S*S);
const ps=[97n,1097n,455733301n,43541956897n,51546439829n,500000368697n];
const D=ps.reduce((x,y)=>x*y,1n), L=435419568970n;
const A=[B[0],10n*B[1],10n*B[2]];
function check(ok) { if (!ok) throw Error("certificate mismatch"); }
check(A.reduce((x,y)=>x*y,1n)===D*L*L);
for (const p of ps) {
  for (let d=2n;d*d<=p;d++) check(p%d!==0n);
  check(B.some(b=>b%p===0n));
  check(B.every((b,i)=>b%(p*p)!==0n&&C[i]%p!==0n));
}
for (const b of B) check(ps.reduce((x,p)=>b%p===0n?x*p:x,1n)===b);
for (const [p,cnt] of [[7n,12],[11n,16]]) {
  check(new Set(A.map(k=>(D*k)%p)).size===3);
  let total=1;
  for(let x=0n;x<p;x++) for(let y=0n;y<p;y++)
    if((y*y-A.reduce((t,k)=>t*(x+D*k),1n))%p===0n) total++;
  check(total===cnt);
}
function pow(a,e,p){let r=1n;while(e){if(e&1n)r=r*a%p;a=a*a%p;e>>=1n}return r}
function sq(x){
  let l=0n,r=1n<<BigInt(Math.ceil(x.toString(2).length/2)+1);
  while(r-l>1n){const t=(l+r)/2n;if(t*t>x)r=t;else l=t}
  return l*l===x;
}
let hits=[];
for(let mask=0;mask<64;mask++){
  let r=0n;
  for(let j=0;j<6;j++){
    const p=ps[j], q=D/p;
    r+=(mask>>j&1?S:-S)*q*pow(q%p,p-2n,p);
  }
  r=(r%D+D)%D;
  for(const x of [r-D,r]){
    if(B.every((b,i)=>{const u=C[i]*x*x+H[i];return u%b===0n&&sq(u/b)}))
      hits.push(String(x));
  }
}
check(hits.sort().join(",")===[String(-S),String(S)].sort().join(","));
~~~
