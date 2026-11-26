# Two-axis phase blocks and a genuine edge-error obstruction

In the [true-origin box](PROPORTIONAL_BOX_EXTERNAL_COVER.md), keep all tiny-prime and medium-factor allowances of the [one-axis grouped Brun proof](PRIME_FACTOR_BRUN_PHASE_SURVIVAL.md). Write \(z=\sqrt{\log X}\) and orient the medium groups along axis 1. The two tiny-prime protection steps may be different; each is at most \(z^{1/3+o(1)}\). Take \(N_1=\lfloor z^{3/2}\rfloor\) stepped indices on axis 1. On every fixed axis-2 row the medium block leaves at least \((29/125-o(1))N_1\) indexed cells, uniformly in all its phases. No independence from the next block is assumed.

## Combining blocks in the same short rectangle

From the [large-order prime supply](AXIAL_PERIOD_AND_MIXED_RETURN.md), each of \(\gg z^{11/20}\) distinct \(\ell>z^{11/20}\) occurs in both axis orders of at least one prime \(q\in(z/2,z]\). Take one distinct q per such factor (each q has at most one factor this large), disjoint from the medium block. The steps do not remove \(\ell\).

* Take \(N_2=\lceil z^{11/20}\rceil\) and at most \(\lfloor c z^{11/20}\rfloor\) of these primes for small c. At fixed axis-1 index, a weak hit fixes at most one residue modulo \(\ell\) in axis 2, thus at most one point in the \(N_2\) consecutive stepped parameters. These primes delete at most a tenth of the whole grid by taking c small. Keeping all those distinct \(\ell\) inside the original first-axis third-order absolute error bound instead gives a cubic error term of order \(z^{33/20}\) in the worst case with one forbidden residue per factor, beyond that short edge budget.
* Alternatively take \(N_2=\lceil z\rceil\) and at most \(\lfloor c' z^{11/15}\rfloor\) eligible large primes (the primes themselves need not have distinct associated factors). The two true orders have product \(>z^{11/10}\) after stepping. The [Mit'kin/Jacobi bound](STRATIFIED_ARBITRARY_PHASE_SURVIVAL.md) gives \(O(z^{-11/15})\) weak-hit fraction at each prime; multiplicity after truncation costs at most four because both edge lengths are at least z and each true order is at most \(q-1\). The union again deletes at most a tenth for small \(c'\). There are enough eligible primes by the same earlier supply result.

Subtracting either block's cap from the guaranteed first block survivors gives fraction at least \(33/250-o(1)\) of the *whole* grid, despite any correlation between blocks. The two rectangles contain respectively \(\gg z^{41/20}\) and \(\gg z^{5/2}\) surviving cells, both indices positive. Stepped indices fit the true active box because each exponent is \(o(z^2)\). The fixed phases and genuine origin are jointly realizable by the square-coordinate CRT in the original height band. All nonselected external primes are set to zero phase. This is not yet whole-window arbitrary phase survival, or evidence of a second true norm.

## Why both boundary terms matter

For an intersection with periodic residue set \(C\subset(\mathbb Z/U)\times(\mathbb Z/V)\), \(|C|=h\), write \(r_x,s_y\) for its two degrees. In an actual \(N_1\times N_2\) box let the multiplicities be \(N_1/U+\epsilon_x\) and \(N_2/V+\eta_y\). The sums of the errors vanish on the respective complete residue lists. Exact expansion gives the deviation from \(hN_1N_2/(UV)\) as
\[
 \frac{N_2}{V}\sum_x\epsilon_x(r_x-h/U)
 +\frac{N_1}{U}\sum_y\eta_y(s_y-h/V)
 +\sum_{(x,y)\in C}\epsilon_x\eta_y .
\]
The last term is bounded by h, but the first two need not be. At the real inert prime 7 and legal phase \(n\equiv17\bmod49\), the exact valuation-one set has 84 hits per \(21\times21\) period, with six in row 0 instead of the mean four. For \((21m+1)\times21k\) beginning at zero, this gives discrepancy \(2k\) purely from one boundary term. At \(m=k=1000\), the exact count is 84,006,000 versus 84,004,000. These boxes can be made strictly active at arbitrarily large n while keeping an honest origin norm, since the phase corresponds to nonzero norm residue \(n-2\) at 7. Thus a general estimate retaining only an h-sized corner error is false even for a single exact arithmetic hit set.

~~~javascript
function pow(b,e,m){let r=1;while(e){if(e%2)r=r*b%m;b=b*b%m;e=Math.floor(e/2)}return r}
function ok(x){if(!x)throw Error("certificate mismatch")}
ok(pow(9,21,49)===1&&pow(25,21,49)===1);
let h=0,edge=0;
for(let i=0;i<21;i++)for(let j=0;j<21;j++){
  const d=((17-pow(9,i,49)-pow(25,j,49))%49+49)%49;
  if(d%7===0&&d!==0){h++;if(i===0)edge++}
}
ok(h===84&&edge===6);
const m=1000,k=1000;
ok(m*k*h+k*edge===84006000&&((21*m+1)*21*k*h/441)===84004000);
~~~
