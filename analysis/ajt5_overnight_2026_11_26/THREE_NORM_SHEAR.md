# A same-point shear preserves a true parent and two true child roots

Let N(V)=V·V. Start with x=24+N(V), T=x−N(V+A), R=x−N(V+B), and det(A,B)=D nonzero. The parent is genuine if V=(2u+v,u−2v), since N(V)=5(u²+v²). For integer t divisible by 10MD, put A'=A+tB, let Bperp=(-B_y,B_x), and set
```
s=(2t*(V+A)·B+t²*N(B))/(2D),  V'=V+s*Bperp.
```
Then B·Bperp=0 and A·Bperp=−D. Expansion shows that both differences N(V'+A')−N(V') and N(V'+B)−N(V') stay unchanged. Also s is divisible by 5M, so the transformed parent coordinates remain integral and x'≡x mod 5M. Consequently every prescribed odd-valuation obstruction already frozen by M is preserved. Taking unbounded t gives genuine unbounded simultaneous parent/first/late witnesses at fixed roots, not a proof about an arbitrary late root.

In FIRST_ROOT_AND_LATE_BRIDGE_CONTROL.md the actual m=5150158917 gives D=6521638444 using the listed pairs in their original orientation. Trial factorization supplies a fixed modulus M retaining at least one odd inert prime greater than 3 per each earlier root. The shear also preserves the countercontrol v3(x−2188)=1 if 9|M. Thus the same unbounded family has both true late roots and a locally viable nonnorm. The two-norm test uses all coordinates at the same integer, not separate witnesses.

A second purely local growth statement: if K freezes all target valuations at the selected primes and is coprime to 15, the grid 5^(e0+i*ord_K(5))+3^(f0+j*ord_K(3)) repeats the target residue. There are order (log x)^2 strictly active such roots below x, even after deduplication. Indeed in a collision with distinct e the smaller f is v3(5^(e−e')−1)=O(log log x) by LTE, so the number of points lost is O(log x log log x). No implication that this grid consists of true norms is claimed.
