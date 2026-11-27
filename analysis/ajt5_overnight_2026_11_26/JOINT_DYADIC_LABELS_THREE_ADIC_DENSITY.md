# Exact 3-adic correlation along the actual two-label Pell orbit

Use the [actual Pell family](JOINT_LABEL_PELL_ORBIT.md)
\[
 X_n+p_n\sqrt5=(3577+1599\sqrt5)\,(9+4\sqrt5)^{387860n},\qquad
 N_K(n)=5p_n^2+K .
\]
The two existing labels remain genuine for every n. For any two extra offsets \(K,K'\equiv9\bmod27\), \(K'\ne K\), define \(d=v_3((K'-K)/27)\). The natural density in the nonnegative index n of passing the 3-adic even-valuation condition at **both** extra offsets is exactly
\[
 \frac14(1-3^{-d}).
\]
In particular this is an upper bound on the density of actual four-label hits (other primes still act).

Write the norm-one step as \(a+b\sqrt5\). Modular powering gives \(a\equiv1\bmod3,\ v_3(b)=2\). In the unramified ring \(\mathbb Z_3[\sqrt5]\), the norm-one step lies at distance exactly \(3^{-2}\) from 1, since \((a-1)(a+1)=5b^2\). Raising a unit this close to 1 to the integer power k raises the valuation of its difference from 1 by \(v_3(k)\) (by binomial expansion first for units k and then for repeated cubing). Its rational-part difference has twice the valuation of its \(\sqrt5\) coefficient by the same norm identity. The orbit keeps \(p_n\equiv6\bmod9\), and \(X_n\) is a 3-adic unit from \(X_n^2-5p_n^2=10924\). Using the Pell multiplication formula thus gives \(v_3(p_n-p_m)=2+v_3(n-m)\) for distinct indices: the term in \(b_k X_m\) has that valuation and the term in \((a_k-1)p_m\) has higher valuation. Since \(v_3(p_n+p_m)=1\), one obtains exactly
\[
 v_3(N_K(n)-N_K(m))=3+v_3(n-m).
\]
The offsets \(K\equiv9\bmod27\) make \(N_K(n)\) divisible by 27. Consequently \(N_K(n)/27\) is a bijection on every 3-power residue ring, by the exact difference identity. The valuation condition at \(N_K\) asks that this uniform 3-adic variable have odd valuation, giving density \(1/4\) for one target.

For two targets write the normalized variables \(z,z+3^d u\), where u is a unit. At \(v_3(z)<d\) their valuations agree; summing the acceptable geometric series gives \(\frac14(1-3^{-d})\) for even d or \(\frac14(1-3^{-(d-1)})\) for odd d. On the complementary ball divide by \(3^d\): the two remaining variables differ by a unit, so they cannot both have odd valuation. For odd d they both need even valuation; inside this ball the fraction is \(1/2\) (one of the three residues gives two units, and each other residue contributes probability \(1/12\) for even valuation at least two). Combining the contributions gives the same formula for odd d. The density statement follows from finite congruence counts with discarded tails of density tending to zero.

The actual offsets \(K=10836,10188\) (\((e,f)=(2,4),(2,6)\)) give \(d=1\) and bound \(1/6\). The two actual labels \((2,4),(20,4)\) have \(d=0\), so they cannot both be true anywhere on this Pell orbit. This does not prove that a further attainable pair occurs infinitely often or settle actual density.

~~~javascript
const mod=(a,m)=>(a%m+m)%m;
function power(e,M){
  const mul=([a,b],[c,d])=>[mod(a*c+5n*b*d,M),mod(a*d+b*c,M)];
  let x=[1n,0n],y=[9n,4n];
  while(e){if(e&1n)x=mul(x,y);y=mul(y,y);e>>=1n}
  return x;
}
const [a,b]=power(387860n,27n);
if(a%3n!==1n||b%9n!==0n||b===0n||1599n%9n!==6n)
  throw Error("valuation seed");
const K=(e,f)=>10942n-5n**e-3n**f;
if(K(2n,4n)!==10836n||K(2n,6n)!==10188n||
   mod(K(2n,6n)-K(2n,4n),81n)!==0n||
   mod(K(2n,6n)-K(2n,4n),243n)===0n||
   mod(K(20n,4n),27n)!==9n||mod(K(20n,4n)-K(2n,4n),81n)===0n)
  throw Error("offset data");
~~~
