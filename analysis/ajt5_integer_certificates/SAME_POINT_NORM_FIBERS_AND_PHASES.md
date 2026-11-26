# Same-point norm fibers and actual phase bridges

Scope: individual complete Gaussian coordinate fibers with fixed offset and period; adjacent exponent crossings for explicit 3,5 labels. No general bridge or conjecture is claimed.

## A lossless key for a complete coordinate fiber

For fixed integers \(S,L\) with \(L>0\), the height set of a residue vector \(w\) is \(S+\{\|u\|^2:u\equiv w\bmod L\}\). Two such height sets agree precisely when the residue vectors are in the same global signed-permutation orbit. In particular the comparison is unchanged if we retain only heights above any fixed cutoff.

To see this, take the unique canonical representative \(0\le a\le b\le L/2\). The first unshifted height is \(h_0=a^2+b^2\). The gap \(\Delta\) to the next distinct height is \(L^2-2Lb\) if \(2b<L\), \(L^2-2La\) if \(2b=L>2a\), and \(2L^2\) if \(2a=2b=L\). These are obtained by changing one coordinate to its next distinct absolute value. The exceptional gap identifies the corner; otherwise \((L^2-\Delta)/(2L)\) equals \(b\) in the interior or \(a\) on the boundary. The other coordinate recovered from \(h_0\) is respectively at most this value or greater than it, so the first two heights identify the orbit. The orbit conversely gives an isometry on the entire residue class.

For the cutoff assertion choose a prime \(p\equiv3\bmod4\) dividing \(4L-1\), so \(p\nmid L\), and a power \(z=p^e\equiv1\bmod L\). For an unshifted positive integer \(v\) and any coordinate fiber, \(v\) belongs to its spectrum iff \(z^2v\) does: on the reverse implication, \(p^e\) divides both coordinates by inertness. Thus a positive discrepancy survives arbitrary scaling. If one fiber has minimum zero and the other does not, the latter's positive minimum is below the former's first positive value \(L^2\). This supplies the positive discrepancy in that case also. For example the first two heights *after* a cutoff are not a valid identification key: modulo 21 the fibers \((0,8)\), \((2,9)\) after cutoff 443 both start 505, 610, but only the second contains 673.

For a CRT splitting into pairwise coprime odd moduli, all one- and two-factor checks suffice for a common global signed permutation. Indeed, after excluding empty sets of admissible directions, each local admissible set is the full group, a singleton, or a two-element coset of a reflection stabilizer. A nonzero vector cannot be fixed by a nontrivial rotation over an odd modulus, and the product of two distinct reflections is a nontrivial rotation. The two-element sets are edges of a bipartite graph (rotation versus reflection). Pairwise intersecting edges in a bipartite graph share a vertex, as otherwise three edges give a triangle. The odd-modulus hypothesis is necessary: \((1,34)\to(22,13)\) passes all pairs of the factors \(2,3,7\) but fails modulus 42.

## Actual adjacent phase bridges at the same height

For \(u\ge1,d\ge0\), let \(q=3^u,\ k=2u+1,\ m=5^d+40q^2+4q+65,\ e=d+1\). With \(r=3\) the four residuals are
\[
\begin{aligned}
m-5^d-3^k &=(1-6q)^2+(8+q)^2,\\
m-5^d-3^{k+2} &=(4-3q)^2+(7+2q)^2,\\
5m+3-5^e-3^k &=(2+14q)^2+(18-q)^2,\\
5m+3-5^e-3^{k+2} &=(2-13q)^2+(18+2q)^2.
\end{aligned}
\]
Expansion verifies the identities, strict positivity and zero 3-adic valuation. At \(u=1,d=0\) the shared parameter is \(m=438\), with residuals \(410,194,2161,1945\).

The existence of an old bridge and agreement of the two phases at 3 do not guarantee a new bridge at the same height. At \(m=110,d=e=0,r=1\), the phase \(k=2\) gives \(100=10^2\) and \(541=10^2+21^2\); phase \(k+2=4\) gives \(28=4\cdot7\) and \(469=7\cdot67\), which are not norms. All four residuals are positive and none is divisible by 3. Nonempty phase marginals likewise cannot replace a common height: with \(d=0\) and the two parent exponents 2 and 4, the window \(\{170,171\}\) gives parent residuals \((160,88)\) and \((161,89)\) respectively. Exactly 160 and 89 are norms, so the phases have disjoint true parent heights in this window.

## An exact first-height change when the offset classes are retained

For \(m\equiv97\bmod343\), allow the entire menu \(c,f,d\ge0,\ \epsilon\in\{0,1\},\ 0\le r\le4\) and put \(C=3^c+5^d,\ D=3^f+5^{d+\epsilon}-r,\ A=m-C,\ B=5m-D\). Require \(A,B>0,\ v_7(A)=2,\ v_7(B)=0\). First activity means these conditions alone; a first true bridge additionally requires both \(A,B\) to be sums of two squares.

* If the offset classes \(C\equiv48,\ D\equiv68\bmod343\) are retained, first activity and first true bridge both occur at \(m=783\). Below 783 the only candidate heights are \(97,440\). Up to 783 the eligible positive offsets \(48,391,734\) give just one actual \(3,5\) power sum, \(734=3^6+5\). At 783, taking \(D=3^6+25=754\) gives \(A=49=7^2,\ B=3161=5^2+56^2\) with the required exact valuations.
* If the offset classes are released but the input class and exact valuations are retained, both first heights are \(440\). At 97, \(v_7(A)=2\) and \(0<A<97\) force \(A=49\), so \(C=48\), which is not an actual power sum. At 440 take \(C=3^5+1=244,\ D=1+5=6\). The residuals are \(196=14^2,\ 2194=13^2+45^2\), with the required valuations.

The finite power-sum check here is exhaustive: for a positive parent residual the parent powers are each strictly below 783, so one need only test \(3^0,\ldots,3^6\) and \(5^0,\ldots,5^4\). This control distinguishes the two different congruence interfaces. It does not infer equality of the two first-height notions for other fibers.
