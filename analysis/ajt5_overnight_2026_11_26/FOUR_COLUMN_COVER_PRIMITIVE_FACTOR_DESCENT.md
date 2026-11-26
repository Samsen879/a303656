# Primitive factor pairs for the remaining four-column cover

Continue [oriented descent](FOUR_COLUMN_COVER_ORIENTED_DESCENT.md) on the actual \(d=4,16\) base direction, with \(S=137672257015\), \(F_i=S^2+h_i\), \(i=0,8,12\), and \(A-SB=2KD\), where \(A/B\) is the reduced branch point, \(B>0\), and the scale has been normalized to 1. Let
\[
 J_i=D/F_i,\qquad
 \theta_i^2=-h_i,\quad \theta_i=\tau_i\sqrt{-n_i},
 \qquad \tau_i=(1/10,2,38),\quad C_i=\tau_iJ_i .
\]
All \(J_i,C_i,n_i\) are integers, with \(n_i>0\) squarefree. The three remaining square conditions have the exact integral form
\[
 r_it_i=-KC_i,\qquad
 B=n_it_i^2-r_i^2-2KSJ_i,\qquad \gcd(r_i,t_i)=1.
\]
Here a viable branch has \(K\ne0\).

To see this, divide the square test \(-(\theta_i-S)(B\theta_i-A)\) by \((\theta_i-S)^2\), yielding \(-B-2KJ_i(S+\theta_i)\). A square root is an algebraic integer because this element is integral. In the quadratic integer ring its two coordinates are integers or both strict half-integers; in the latter case twice their product is not an integer, contrary to the \(\sqrt{-n_i}\) coefficient. Comparing coefficients of \((r_i+t_i\sqrt{-n_i})^2\) gives the two stated equations. Since \(\gcd(A,B)=1\), also \(\gcd(B,2KD)=1\). A prime dividing both \(r_i,t_i\) forces its square to divide \(KC_i\). If it divides K or D this would make it divide B by the second equation. The only other prime factors of any \(C_i\) are 2 and 19 (from \(\tau_i\)); 2 cannot divide both since B is odd, and the extra 19 appears to exponent one. Thus the pairs are primitive. For fixed K one can assign complete prime powers of \(KC_i\) separately to the two coordinates, including signs, and check whether the three computations give the same positive B. No height scan over A and B is needed.

Modulo 5, 7, and 23, intersecting the three image sets of \((K,B)\) forces \(K=0\) at each prime; at 7 the only B residues are \(0,3,5,6\). The coprimality of B with K excludes 0, hence \(805\mid K\) and B is nonsquare. The exact finite elimination is included below.

## A further uniform height obstruction

The column 8 value \(n_8\) is a nonsquare at each \(p\in\{97,1097,51546439829\}\), which divide \(J_8\). At each such p the square-scale proof gives \((B/p)=1\), so if p divided \(r_8\), the second equation would give \((B/p)=(n_8/p)=-1\). Thus these primes divide \(t_8\). Also \(r_8\) is odd from \(n_8\) even and B odd, so \(2\mid t_8\). Consequently
\[
 T=2\cdot97\cdot1097\cdot51546439829\mid t_8,\qquad
 |r_8|\le455733301\,|K|.
\]
The formula for A is \(A=S(n_8t_8^2-r_8^2)+2Kh_8J_8\). This gives the decreasing lower bound \(S n_8 T^2-S(455733301)^2|K|^2-2h_8J_8|K|\) on A, while \(\max(|A|,B)\ge2D|K|/(S+1)\) increases. A certified split at \(|K|=438368906230000891\) gives
\[
 \max(|A|,B)\ge346568729614919635896119905996253689159992218464686819 .
\]
This constrains the actual branch point, not every candidate on the weaker genus-five locus.

If a positive B is ever found with all three exact factor pairs and the oriented and coprimality conditions, it gives the required three field-square tests, not merely their norms. On the genus-zero shared cover, simple target zeros then have residue fields containing i, so all conjugation-fixed factors of each target in the rational function field have even order; poles are even, as targets are quadratic in s. The remaining constant can be checked at the genuine rational seed \(s=S\) (the target is a nonzero rational norm there), giving all three rational-function identities. Then nonsquare B allows a Pell step in \((2Bs-A-BS)^2-B(2Y)^2=(A-BS)^2\); a suitable power preserves the seed congruences and yields unbounded integer s, using the sign of the norm-one point to select the branch with s unbounded in absolute value. This is conditional. No new branch point or infinite four-column family is proved.

~~~javascript
const S=137672257015n,D=54420943797756604224326386906204441996505463449n;
const H=[28173484023085671807211n,2817344150684665342984n,2814690812686254405484n];
const M=[10n,1n,1n],F=H.map((h,i)=>h+M[i]*S*S);
const J=F.map((f,i)=>D*M[i]/f),C=[J[0]/10n,2n*J[1],38n*J[2]];
const ns=[10n*H[0],H[1]/4n,H[2]/1444n];
function ok(x){if(!x)throw Error("certificate mismatch")}
function mod(x,p){return (x%p+p)%p}
function pow(a,e,p){let x=1n;a=mod(a,p);while(e){if(e&1n)x=x*a%p;a=a*a%p;e>>=1n}return x}
const fac=[[2n,5n,17n,1291n,17959n,71479785808007n],
 [2n,149n,288044681n,8205476117n],[7n,137n,4776641n,425522269n]];
fac.forEach((row,i)=>{
  ok(row.reduce((x,p)=>x*p,1n)===ns[i]&&new Set(row).size===row.length);
  for(const p of row)for(let d=2n;d*d<=p;d++)ok(p%d!==0n);
});
ok(ns[1]*4n===H[1]&&ns[2]*1444n===H[2]);
ok(F.every((f,i)=>f*J[i]===M[i]*D));
for(const p of [5n,7n,23n]){
  const set=ns.map((n,i)=>{
    let t0=new Set();
    for(let k=0n;k<p;k++) for(let r=0n;r<p;r++) for(let t=0n;t<p;t++)
      if(mod(r*t+k*C[i],p)===0n)t0.add(k+","+mod(n*t*t-r*r-2n*k*S*J[i],p));
    return t0;
  });
  const both=[...set[0]].filter(x=>set[1].has(x)&&set[2].has(x));
  ok(both.length>0&&both.every(x=>x.startsWith("0,")));
  if(p===7n)ok(both.sort().join(";")==="0,0;0,3;0,5;0,6");
}
const forced=[97n,1097n,51546439829n];
for(const p of forced)ok(J[1]%p===0n&&pow(ns[1],(p-1n)/2n,p)===p-1n);
const T=forced.reduce((x,p)=>x*p,2n);
ok(C[1]/T===455733301n&&C[1]%T===0n&&ns[1]%2n===0n);
const cut=438368906230000891n;
const lower=(2n*D*cut+S)/(S+1n);
const r=cut-1n;
ok(S*(ns[1]*T*T-(455733301n*r)**2n)-2n*H[1]*J[1]*r>=lower);
ok(lower===346568729614919635896119905996253689159992218464686819n);
~~~
