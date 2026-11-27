# A shared-character restriction for the primitive factor model

In [the primitive factor descent](FOUR_COLUMN_COVER_PRIMITIVE_FACTOR_DESCENT.md), any genuine second branch point has \(A-SB=2KD\) and three primitive pairs satisfying \(r_it_i=-KC_i,\ B=n_it_i^2-r_i^2-2KSJ_i\). The exponent variable here is the signed integer K of that construction, not a Pell target offset in a different model.

For an odd prime \(p\nmid K\), put \(u_i=t_i^2/K,\ v_i=r_i^2/K,\ z=B/K\bmod p\). Each row must meet
\[
 u_iv_i=C_i^2,\qquad z=n_i u_i-v_i-2SJ_i .
\]
Every nonzero \(u_i,v_i\) must have Legendre sign \((K/p)\). For primes p at which an \(F_i\) is a nonsquare unit, \(p\) cannot divide B: the exact quotient-square condition for \(F_i\) from the [elliptic quotient](FOUR_COLUMN_COVER_ELLIPTIC_QUOTIENT.md) would force that \(F_i\) be a square modulo p, since A would be a unit. This removes \(z=0\). The finite sets of allowable common z are:
 
| \(p\) | \(K\) quadratic residue | \(K\) quadratic nonresidue |
|---:|---|---|
| 11 | 1 | empty |
| 17 | 6 | empty |
| 19 | empty | 3 |
| 37 | empty | 34 |
| 73 | empty | 14, 69 |
| 113 | empty | empty |

In particular \(113\mid K\), and with the three earlier prime conditions \(90965\mid K\). These are necessary for every K, without a height bound. The character sieve depends only on the modular coefficient data and the shared K, so it remains applicable without any enumeration of large integer factorizations.

If every prime of \(|K|\) belongs to \(\{2,5,7,23,113\}\), the five relevant character conditions (at 11,17,19,37,73) allow only the signed square classes \(-161,-5198\). The first is odd and 3 modulo 4 up to an odd square, contradicting \(K\equiv0,1\bmod4\) from [oriented descent](FOUR_COLUMN_COVER_ORIENTED_DESCENT.md). Thus such a restricted-support K can only be negative, in class \(-5198\), and have \(v_2(K)\ge3\) (its valuation is odd and it is 0 modulo 4). Positive K or odd K must use a prime outside the listed support. No compatible global primitive factor pairs or new branch point are produced.

~~~javascript
const S=137672257015n,D=54420943797756604224326386906204441996505463449n;
const H=[28173484023085671807211n,2817344150684665342984n,2814690812686254405484n],M=[10n,1n,1n];
const F=H.map((h,i)=>h+M[i]*S*S),J=F.map((f,i)=>D*M[i]/f);
const C=[J[0]/10n,2n*J[1],38n*J[2]], n=[10n*H[0],H[1]/4n,H[2]/1444n];
const mod=(a,p)=>(a%p+p)%p;
function pow(a,e,p){let x=1n;a=mod(a,p);while(e){if(e&1n)x=x*a%p;a=a*a%p;e>>=1n}return x}
function sign(a,p){return pow(a,(p-1n)/2n,p)}
function ok(v){if(!v)throw Error("character certificate")}
const rows=[[11n,"1",""],[17n,"6",""],[19n,"","3"],
            [37n,"","34"],[73n,"","14,69"],[113n,"",""]];
for (const [p,a,b] of rows){
  ok(F.some((f,i)=>sign(f*M[i],p)===p-1n));
  for(const [k,want] of [[1n,a],[p-1n,b]]){
    const pool=[0n];
    for(let x=1n;x<p;x++)if(sign(x,p)===k)pool.push(x);
    const sets=n.map((v,i)=>{
      const s=new Set();
      for(const u of pool)for(const w of pool)
        if(mod(u*w-C[i]*C[i],p)===0n)s.add(mod(v*u-w-2n*S*J[i],p));
      return s;
    });
    const both=[...sets[0]].filter(v=>v!==0n&&sets[1].has(v)&&sets[2].has(v));
    ok(both.map(Number).sort((a,b)=>a-b).join(",")===want);
  }
}
const s=[2n,5n,7n,23n,113n],classes=[];
for(let mask=0;mask<32;mask++)for(const pol of [1n,-1n]){
  const k=s.reduce((a,p,i)=>(mask>>i&1)?a*p:a,pol);
  if(rows.slice(0,-1).every(([p,a])=>sign(k,p)===(a?1n:p-1n)))classes.push(String(k));
}
ok(classes.sort().join(",")==="-161,-5198");
~~~
