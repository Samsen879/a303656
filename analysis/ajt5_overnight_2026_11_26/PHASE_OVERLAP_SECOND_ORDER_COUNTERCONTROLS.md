# Actual exponent-box countercontrols for pairwise phase overlap

This concerns the [true-origin external phase window](STRATIFIED_ARBITRARY_PHASE_SURVIVAL.md), with even-even offsets \(9^i+25^j\). A hit means that the residue \(n-9^i-25^j\) has valuation exactly one at its assigned inert prime. All phases below are realizable at real origin norms \(n=2+u^2+v^2\) by the same coordinate CRT, keeping any disjoint fixed observation panel. They are finite-certificate hits, not claims of genuine norms at surviving cells.

## A genuinely shared order factor need not produce overlap

For primes 619 and 1031 the two order pairs are \((103,309)\) and \((515,515)\). For \(X=2^{1600000}\), both lie in the upper half-window \(z/2<q\le z,\ z=\sqrt{\log X}\), and share the divisor \(103>z^{11/20}\) in both axes. Fix n modulo their squares to be 1 and 8 respectively. The weak roots modulo the respective primes, projected onto \((i,j)\bmod103\) across complete periods, are disjoint. Consequently no common strong hit can occur even in a larger box. Both have individual exact hits in small boxes (verified below). Changing only the 1031 phase from 8 to 1 gives the same count 257 of full-period weak roots at that prime, and the actual index \((86,545)\) becomes an exact hit at both primes. Setting all the other external primes to zero phases is permitted by the true-origin construction.

## Exact equality in orders one and two, with different order three

For primes \((7,19,31)\), compare phases \((3,1,13)\) and \((3,4,9)\) modulo the respective squares. In the common weak period \(45\times9\) the singleton counts are \((90,20,18)\), and pair counts (in lexicographic order) \((5,9,1)\) in both cases. The triple counts are 0 and 1. Fix the column and an index \(i\bmod45\). A weak hit for a given q lifts along \(i+45r\): since \(9^{45}\equiv1\bmod q\) but not modulo \(q^2\), the quotient has exactly one excluded congruence class modulo q where the hit is *not* exact valuation one. For a \(k\)-fold intersection this makes precisely the fraction \(\prod_q(1-1/q)\) exact over every complete r-period of \(\prod_q q\). It is independent of the chosen phases, the fixed column, and the chosen weak row.

It follows that in any box whose side lengths are multiples of \(45(7\cdot19\cdot31)=185535\) and \(9\), respectively, all singleton and pairwise **exact** hit counts still agree, but the surviving fractions differ by \(\prod_q(1-1/q)/(45\cdot9)=8/4123\). One actual active rectangle of this form has sides \(185535,126648\); choosing X as the larger of \(4\cdot9^{I-1},4\cdot25^{J-1}\) gives both required floors because it is less than \(4\min(9^I,25^J)\), checked exactly in the replay. The count gap is 45,593,280.

The same fractional discrepancy persists as a leading term with many active nonzero phases. There are arbitrarily large common active rectangles of the indicated complete-period form: at \(\log(X/4)=(I-1)\log9\) and I a positive multiple of 185535, the fractional sequence modulo \(9\log25\) is dense by irrationality of \(\log9/\log25\), so J can be a multiple of 9 infinitely often. Choose \(\Theta(z/\log z)\) other inert primes in \((z/2,z]\) (for example from [the large-order family](AXIAL_PERIOD_AND_MIXED_RETURN.md)). Use the same tail assignments for the two heads. For each tail prime, average its phase uniformly over nonzero residues different from 2 modulo q; these are all legal, and the probability of even a weak hit at a cell is at most \(1/(q-2)\). The expected sum of their covered fractions is \(O(1/\log z)\), so a single assignment realizes that bound. Tail singleton and tail-tail data then agree exactly. The summed normalized absolute differences for the three head-tail pairs per tail prime are \(O(1/\log z)\), since a difference is bounded by the corresponding tail covered fraction. The surviving fraction difference remains \(8/4123+O(1/\log z)\), while all singleton counts are equal and the total second-order discrepancy tends to zero. This rules out recovery of the survivor leading fraction from first and second order data alone in this class. It does not preclude a positive lower bound using more structure.

~~~javascript
function check(x){if(!x)throw Error("certificate mismatch")}
function mod(x,n){return (x%n+n)%n}
function pow(b,e,n){let r=1;while(e){if(e%2)r=r*b%n;b=b*b%n;e=Math.floor(e/2)}return r}
function order(b,n){let x=b%n,k=1;while(x!==1){x=x*b%n;k++}return k}
function hit(q,n,i,j){
  const d=mod(n-pow(9,i,q*q)-pow(25,j,q*q),q*q);
  return d%q===0&&d!==0;
}
function weak(q,n,R,T){
  let cnt=0, set=new Set();
  for(let i=0;i<R;i++)for(let j=0;j<T;j++)
    if(mod(n-pow(9,i,q)-pow(25,j,q),q)===0){cnt++;set.add([i%103,j%103].join(","))}
  return [cnt,set];
}
for(const q of [619,1031,7,19,31])
  for(let d=2;d*d<=q;d++)check(q%d!==0);
check([order(9,619),order(25,619),order(9,1031),order(25,1031)].join()==="103,309,515,515");
const [a,A]=weak(619,1,103,309),[b,B]=weak(1031,8,515,515);
check(b===257&&weak(1031,1,515,515)[0]===257);
check(![...A].some(x=>B.has(x)));
for(const [q,n,R,T] of [[619,1,103,309],[1031,8,515,515]]){
  let has=false;
  for(let i=0;i<R&&!has;i++)for(let j=0;j<T;j++)if(hit(q,n,i,j)){has=true;break;}
  check(has);
}
check(hit(619,1,86,545)&&hit(1031,1,86,545));
const qs=[7,19,31];
for(const q of qs)check(pow(9,45,q)===1&&pow(9,45,q*q)!==1&&pow(25,9,q)===1);
for(const [phase,tri] of [[[3,1,13],0],[[3,4,9],1]]){
  let ct=Array(8).fill(0);
  for(let i=0;i<45;i++)for(let j=0;j<9;j++){
    let m=0;
    qs.forEach((q,k)=>{if(mod(phase[k]-pow(9,i,q)-pow(25,j,q),q)===0)m|=1<<k});
    for(let t=1;t<8;t++) if((m&t)===t)ct[t]++;
  }
  check([ct[1],ct[2],ct[4],ct[3],ct[5],ct[6],ct[7]].join()===[90,20,18,5,9,1,tri].join());
}
const I=185535n,J=126648n, a0=9n**(I-1n),b0=25n**(J-1n),W=a0>b0?a0:b0;
check(W<a0*9n&&W<b0*25n&&I*J*8n/4123n===45593280n);
~~~
