# Exact Pell index lifting with two genuine period-dependence controls

Use the fixed orbit \(X_n+p_n\sqrt5=(3577+1599\sqrt5)G^n,\ G=(9+4\sqrt5)^{387860}\), of [the real joint labels](JOINT_LABEL_PELL_ORBIT.md), and write \(N_K(n)=5p_n^2+K,\ C=10924\). Let \(\ell\equiv3\bmod4\) be prime, and let m be the smallest positive integer with \(G^m\equiv\pm1\bmod\ell\) in the quadratic residue algebra. On any progression \(n=r+mj\), select the common sign of the step to write \(U+V\sqrt5\equiv1\bmod\ell\); removing sign factors does not change \(p_n^2,X_n^2\). Put \(s=v_\ell(V)\). For any nonzero j, writing \(U_j+V_j\sqrt5=(U+V\sqrt5)^j\) gives
\[
 v_\ell(V_j)=s+v_\ell(j),\quad v_\ell(U_j-1)=2s+2v_\ell(j).
\]
These follow by binomial expansion near 1, since \((U_j-1)(U_j+1)=5V_j^2\) and \(U_j+1\) is a unit. The argument works in the quadratic residue algebra even at a split prime; the minimum valuation of the two coefficients increases exactly as stated under powering. At least one of \(p_r,X_r\) is a unit as no odd prime square divides C.

If \(a=v_\ell(p_r),b=v_\ell(X_r)\) are both below s, the valuations stay constant on the progression and
\[
 v_\ell\big(N_K(r+mj)-N_K(r+mk)\big)=s+a+b+v_\ell(j-k).
\]
Indeed \(V_{j-k}X\) dominates in the coordinate difference of p, and its sum with the other p has valuation a. Put \(h=s+a+b\). If the initial residual has valuation less than h, this valuation never changes on the progression. Otherwise divide by \(\ell^h\) and its values biject every \(\ell\)-power residue ring as j varies. The conditional even-valuation density is \(1/(\ell+1)\) for odd h, or \(\ell/(\ell+1)\) for even h. As in [the 3-adic correlation proof](JOINT_DYADIC_LABELS_THREE_ADIC_DENSITY.md), the assertion follows by counting finite congruences and then bounding the discarded high-valuation tail.

If either coordinate instead has valuation at least s, that coordinate divided by \(\ell^s\) itself gives a bijective index variable \(z\), since the other coordinate is a unit and dominates the difference formula. Thus the original residual becomes exactly \(K+5\ell^{2s}z^2\) when p is the large-valuation coordinate, or \(K-C+\ell^{2s}z^2\) when it is X. For \(\ell=7\) and label \((e,f)=(4,14)\) it is the latter case, with \(s=1\), giving quotient \(z^2+5\bmod7\) after removing 49. Here \(z\equiv n\bmod7\), with two simple roots at \(n\equiv3,4\). Each lifts to all powers. The odd-valuation density is \((2/7)(7/8)=1/4\), so the even-valuation density is \(3/4\).

## Two genuine dependence examples

* For \(K=10936\), the coarse periods at 79 and 8527 are 13 and 26. Their bad residues reduce to respectively 4 and 7 modulo 13. Each really gives positive odd-valuation density (the corresponding step has \(s=1\) and the input coordinates are units), but their overlap is empty.
* For \(K=10908\), the coarse periods at 19 and 2699 are 3 and 1349, which are coprime. At 2699 the two active classes \(133,1122\bmod1349\) equally contribute odd hits and fix \(n\equiv0,1\bmod19\), respectively. At 19 its only active class is \(n\equiv1\bmod3\), and its first lifted zero mod \(19^2\) inside this class fixes \(n\equiv0\bmod19\). Outside that lifted class the valuation is exactly one; inside, the odd-valuation density is \(1/20\) by the lifting formula. All later 19 powers and the powers of 2699 are coprime after accounting for this shared digit. Hence the probability of odd 19-valuation conditioned on odd 2699-valuation is \((1+1/20)/(2\cdot3)=7/40\), whereas the unconditional probability is \(19/60\).

A sequence of pairwise coprime **complete finite obstruction periods**, with excluded fractions having divergent sum, would imply density zero by finite CRT products. These two controls show why neither distinct obstruction primes nor coprimality of their coarse periods is enough. No infinite independent family or density-zero result is asserted.

~~~javascript
const S=[3577n,1599n],mod=(x,p)=>(x%p+p)%p;
function mul([a,b],[c,d],p){return [mod(a*c+5n*b*d,p),mod(a*d+b*c,p)]}
function power(e,p){
  let r=[1n,0n],a=[9n,4n];
  while(e){if(e&1n)r=mul(r,a,p);a=mul(a,a,p);e>>=1n}
  return r;
}
function check(x){if(!x)throw Error("certificate mismatch")}
function coarse(p,K){
  const G=power(387860n,p);
  let r=[1n,0n],n=0n,hits=[];
  do {
    const py=mul(S,r,p)[1];
    if(mod(5n*py*py+K,p)===0n)hits.push(n);
    r=mul(r,G,p);n++;
  } while(r[1]!==0n);
  return [n,hits];
}
for(const [p,K,m,rs] of [
 [79n,10936n,13n,[4n]],[8527n,10936n,26n,[20n]],
 [19n,10908n,3n,[1n]],[2699n,10908n,1349n,[133n,1122n]]
]){
  const [d,rr]=coarse(p,K);
  check(d===m&&rr.join(",")===rs.join(","));
  check(power(387860n*m,p*p)[1]%p===0n&&power(387860n*m,p*p)[1]!==0n);
  for(const r of rs)check(mul(S,power(387860n*r,p),p).every(x=>x!==0n));
}
let roots=[];
for(let j=0n;j<19n;j++){
  const n=1n+3n*j,p=19n*19n;
  const y=mul(S,power(387860n*n,p),p)[1];
  if(mod(5n*y*y+10908n,p)===0n)roots.push(n%19n);
}
check(roots.join(",")==="0"&&133n%19n===0n&&1122n%19n===1n);
const [a,b]=power(387860n,49n),K=10942n-5n**4n-3n**14n;
check(a===48n&&b===7n&&S[0]%49n===0n&&5n*S[1]%7n===1n);
check((K-10924n)%49n===0n&&mod((K-10924n)/49n,7n)===5n);
~~~
