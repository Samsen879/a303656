# Oriented residue descent for an actual four-column shared cover

Use the original four-column seed and the \(d=4,16\) direction of [the shared-cover model](FIRST_248_FOUR_COLUMN_MULTICOVER_LIMIT.md). Write \(S=137672257015,\ f_i(s)=s^2+h_i,\ F_i=S^2+h_i\), with \(i=0,8,12\). Put \(D=54420943797756604224326386906204441996505463449\), the product of the prime factors of the three normalized numerators, as in [the elliptic quotient](FOUR_COLUMN_COVER_ELLIPTIC_QUOTIENT.md). Write the second rational branch point \(\sigma=A/B\) in lowest terms, \(B>0\).

For a shared cover \(Y^2=c(s-S)(Bs-A)\), \(c>0\), to support the three norm identities, it is necessary that
\[
 A\equiv SB\bmod D,\qquad c\in\mathbb Q^{\times2},\qquad
 A\equiv1\bmod8,\quad B\equiv1\ \text{or}\ 7\bmod8.
\]
Thus every nontrivial viable branch point has height \(\max(|A|,B)\) at least \(790586934177042056496684738076618648\). This applies to the genuine shared cover, not to every rational point of its genus-five necessary locus.

## From unsigned to oriented conditions

At \(\theta_i^2=-h_i\), the inert-residue criterion requires
\[
 c\big(Bh_i-SA+(A+BS)\theta_i\big)
       =-c(\theta_i-S)(B\theta_i-A)
\]
to be a square in \(\mathbb Q(\theta_i)\). Taking the field norm gives the previously verified conditions \(w_i^2=(\sigma^2+h_i)/F_i\). They give \(A\equiv\pm SB\bmod p\) for \(p\mid D\), and imply \(B\) is prime to D. They also force B odd, since \(v_2(F_0)=-1\) would make \(v_2((\sigma^2+h_0)/F_0)=1-2v_2(B)\) odd for an even B.

If p is odd and some \(h_i,F_i\) are both p-adic units, at least one of the two coefficients \(Bh_i-SA,\ A+BS\) is a unit, since their transformation from the primitive pair A,B has determinant \(-F_i\). The algebra defined by \(\theta_i^2=-h_i\) is unramified or split, and in at least one factor the expression without c is a unit. This forces \(v_p(c)\) even. Except for \(p_*=43541956897\) this applies to every odd p: the gcd of the three products of their h and F numerators is exactly \(p_*\); at 5 use the column 8 units.

At \(p_*\), all three \(F_i\) have valuation one and the two roots modulo \(p_*\) are \(\pm S\) with S a unit. If \(A\equiv-SB\), at the positive root \(\theta_i\) one has \(\theta_i-S=-F_i/(\theta_i+S)\) and \(B\theta_i-A\equiv2SB\). Therefore \(v_{p_*}(c)\) must be odd and the symbol of the resulting normalized unit is the symbol of \(B(c/p_*^{v_{p_*}(c)})(F_i/p_*)\). The three \(F_i/p_*\) have signs \(+,-,+\), so the required symbols cannot all be +. If \(A\equiv+SB\), evaluating at the negative root makes both factors units and forces \(v_{p_*}(c)\) even. Thus c has even valuation at all odd primes. Returning to any \(p\mid D\), a negative sign would force odd valuation of c at its positive root by the same argument. Hence every sign is positive.

At any \(p\mid D\) use the negative root: the normalized unit after removing the even p-power of c has sign of \(-cB\), with the p-power removed from c. Every p in D is 1 modulo 4. As \(c>0\), its square class is now 1 or 2; call it \(c_0\). Thus \((B/p)=(c_0/p)\). On the other hand, for each prime \(\ell\mid B\) the square condition for \(F_{12}\) forces \((F_{12}/\ell)=1\), since \(F_{12}(w_{12}B)^2=A^2+h_{12}B^2\) and \(w_{12}B\) is integral. The odd squarefree \(F_{12}\equiv5\bmod8\) has all its factors in D. Quadratic reciprocity gives \(1=(F_{12}/B)=(B/F_{12})=(c_0/F_{12})\). Since \((2/F_{12})=-1\), c is a square.

## Dyadic condition and height

Absorb c's square and write \(k=2h_0\), a 2-adic unit. In the first target field, use \(\pi=2\theta_0\) with \(\pi^2=-2k\). The target without c has valuation \(-2\) in the normalized ramified valuation, so multiply by the square \(\pi^2\) to test the integral square. Its constant and \(\pi\) coefficients are \(-Bk^2+2kSA\) and \(-k(A+BS)\). In the column 8 field, use \(\pi=\theta_8/2\), with \(\pi^2=-h_8/4\) of exact 2-adic valuation one. Both rings of integers are \(\mathbb Z_2[\pi]\): the constant and \(\pi\) terms have distinct valuation parity. The column 8 target has integral coefficients \(Bh_8-SA,\ 2(A+BS)\) in that basis. In each ring the coefficients of \((x+y\pi)^2\) are \(x^2+\pi^2 y^2,\ 2xy\). The finite checks modulo 8 below leave exactly the stated \(A,B\) residues as necessary conditions.

Now \(A-SB=jD\); since \(S\equiv7\bmod8\) and D is odd, \(v_2(j)=1\) when \(B\equiv1\), and \(8\mid j\) when \(B\equiv7\). Nontrivial \(\sigma\ne S\) has \(|j|\ge2\), yielding the height bound \(\lceil2D/(S+1)\rceil\). If \(B\) is a square and \(A\ne SB\), completing the square gives
\[
  (2Bs-A-BS)^2-B(2Y)^2=(A-BS)^2,
\]
a fixed nonzero integer factor-pair equation at integral s (then rational Y is integral). Thus an unbounded Pell family on this branch requires nonsquare B and the full three field-square conditions. No such new genuine branch point is asserted.

~~~javascript
const S=137672257015n, C=[10n,1n,1n];
const H=[28173484023085671807211n,2817344150684665342984n,2814690812686254405484n];
const F=H.map((h,i)=>h+C[i]*S*S);
const G=43541956897n;
const primes=[97n,1097n,455733301n,G,51546439829n,500000368697n];
function mod(x,p){return (x%p+p)%p}
function gcd(a,b){return b===0n?a:gcd(b,a%b)}
function pow(a,e,p){let x=1n;a=mod(a,p);while(e){if(e&1n)x=x*a%p;a=a*a%p;e>>=1n}return x}
function ok(x){if(!x)throw Error("certificate mismatch")}
ok(gcd(gcd(H[0]*F[0],H[1]*F[1]),H[2]*F[2])===G);
ok(H[1]%5n!==0n&&F[1]%5n!==0n&&S%G!==0n);
for(const p of primes){
  for(let d=2n;d*d<=p;d++)ok(p%d!==0n);
  ok(p%4n===1n&&S%p!==0n&&F.some(f=>f%p===0n));
}
for(const f of F)ok(primes.reduce((x,p)=>f%p===0n?x*p:x,1n)===f);
ok(F[2]%8n===5n);
ok(F.map((f,i)=>pow(f/G*pow(C[i],G-2n,G),(G-1n)/2n,G)).join(",")===[1n,G-1n,1n].join(","));
function match(r,c,d){
  for(let x=0n;x<8n;x++)for(let y=0n;y<8n;y++)
    if(mod(x*x+r*y*y-c,8n)===0n&&mod(2n*x*y-d,8n)===0n)return true;
  return false;
}
const k=mod(H[0]*5n,8n);
let vals=[];
for(let a=0n;a<8n;a++)for(let b=1n;b<8n;b+=2n)
  if(match(-2n*k,-b*k*k+2n*k*S*a,-k*(a+b*S))&&
     match(-H[1]/4n,b*H[1]-S*a,2n*(a+b*S))) vals.push(String(a)+","+String(b));
ok(vals.join(";")==="1,1;1,7"&&H[1]%16n===8n);
const D=primes.reduce((x,y)=>x*y,1n);
ok((2n*D+S)/(S+1n)===790586934177042056496684738076618648n);
~~~
