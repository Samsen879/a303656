# Rational pullbacks: signed norm separation and the quadratic 3-adic discriminant

This continues [the monomial pullback norm criterion](https://github.com/Samsen879/a303656/commit/53716fada8d4975e523654933b5a1f664328cbc8). The first result concerns any degree of a common rational pullback with a rational lift of 1. The quadratic residue table is an exact local test, not a sufficiency claim for global squarehood. All nine rows (both signs) were replayed independently by polynomial arithmetic in the three full cyclotomic quotient rings over \(\mathbb F_3\), rather than a selection of residue places.

A finite nonzero evaluation at the rational lift defines the norm evaluation: the constant quadratic field extends the rational place inertly, so the valuation of a rational-function norm there is twice the valuation of its preimage. A preimage for a finite nonzero value is thus regular and nonzero at that place. The two native shell values are odd here because the odd-index signed factorizations have their full 2-parts already in \(5\pm3\). Their coprime positive native values allow the inert-valuation condition to be checked separately.

**A common rational pullback cannot make the two signed shells cancel a norm obstruction if it has a rational lift of the native input.** For quadratic pullbacks, there is a complete \(3\)-adic discriminant test on the growing families \(17^a\), \(17^a7\), and \(17^a19\).

### The two signs cannot cancel

Put \(K=\mathbb Q(\sqrt{-3})\) and \(P_d^\pm(U)=\Phi_d(5U,\mp3)\), with homogeneous cyclotomic notation. Let \(d>1\) be odd and let \(f\in\mathbb Q(T)\) be nonconstant, with \(f(t_0)=1\) at a rational point \(t_0\). Then
\[
P_d^+(f)\,P_d^-(f)\in N_{K(T)/\mathbb Q(T)}K(T)^\times
\quad\Longleftrightarrow\quad
P_d^+(f),\ P_d^-(f)\in N_{K(T)/\mathbb Q(T)}K(T)^\times.
\]

The two zero sets are disjoint because the target roots are \(3\zeta_d/5\) and \(-3\zeta_d/5\), with different root-of-unity orders. At each pole of \(f\), the pole multiplicity of either shell is even since \(\varphi(d)\) is even. A norm product therefore forces even multiplicity in each shell at every irreducible polynomial that stays irreducible over \(K\). Each shell is then a rational constant times a norm.

At \(t_0\), the two native integer values are coprime. They divide \(5^d+3^d\) and \(5^d-3^d\), and both are odd and prime to \(3\). The product norm at \(t_0\) forces both integers to be norms individually, by inert-prime valuation parity. This removes both rational constants. The argument applies to every degree of a common pullback.

### Exact quadratic test

Write a degree-two map as \(f=A/B\) with coprime polynomials, and set \(\Delta(U)=\operatorname{disc}_T(A(T)-UB(T))\). Assume \(3\nmid d\) and \(\varphi(d)>2\). Put \(L=\mathbb Q(\zeta_d)\) and \(u_\pm=\mp3\zeta_d/5\). For a map with a rational lift of \(1\), the full criterion for either sign is
\[
P_d^\pm(f)\text{ is a norm}
\quad\Longleftrightarrow\quad
P_d^\pm(1)\text{ is a norm and }
\Delta(u_\pm)/(-3)\in L^{\times2}.
\]
Indeed \(u_\pm\) is neither a branch value nor a value where the fiber loses degree, since its degree exceeds two. If \(\Delta(u_\pm)\) splits over \(L\), the simple inverse images have residue field \(L\), which lacks \(K\). Otherwise their residue field is \(L(\sqrt{\Delta(u_\pm)})\), which contains \(K\) exactly under the stated square condition. Once the inverse-image factors split over \(K\), native evaluation tests the sole remaining rational constant.

Here is the complete test at primes above \(3\) for \(d=17^a b\), \(a\ge1\), \(b=1,7,19\). Let \(\delta\) be the minimum \(3\)-adic valuation of the coefficients of \(\Delta(3X/5)\), and reduce
\[
R(X)=-3^{-\delta}\Delta(3X/5)\pmod3.
\]
There is no cancellation at a primitive root, whose residue degree is at least \(16\). An even \(\delta\) fails both signs. For odd \(\delta\), the table gives the square characters of \(R(\zeta_d)\) and \(R(-\zeta_d)\), respectively, at **every** prime above \(3\). Multiplying \(R\) by a nonzero scalar in \(\mathbb F_3\) preserves the characters. Replacing \(X\) by \(-X\) swaps the entries.

| Representative \(R\) | \(17^a\) | \(17^a7\) | \(17^a19\) |
|---|:---:|:---:|:---:|
| \(1,\ X,\ X^2,\ (X-1)^2,\ X^2+1\) | \(+,+\) | \(+,+\) | \(+,+\) |
| \(1+X,\ X(1+X)\) | \(+,-\) | \(+,-\) | \(+,+\) |
| \(X^2-1\) | \(-,-\) | \(-,-\) | \(+,+\) |
| \(X^2+X-1\) | \(+,+\) | \(-,-\) | \(+,+\) |

The base residue degrees at \(a=1\) are \(16,48,144\). Since \(3^{16}\equiv171\bmod289\), increasing \(a\) multiplies the residue degree by \(17\). The relative norm sends \(R(\zeta_d)\) to \(R(\zeta_d^{17})\). To see this, factor \(R\) over \(\mathbb F_9\) and take the norm of each linear factor. Its root is fixed by seventeenth powering, and the conjugates of \(\zeta_d\) run through its multiples by seventeenth roots of unity. The relative norm preserves quadratic characters, so the three base checks prove the table for all \(a\).

### Native controls and replay

The genuine quadratic rational map
\[
f(T)=\frac{5T^2-3}{T^2+1}
\]
has \(f(1)=1\), \(\Delta(U)=60+8U-4U^2\), and \(R=1-X\). Its minus pullback fails at \(3\) on both \(17^a\) and \(17^a7\). At the actual native index \(17\), both integer shells pass, with witnesses \(512959^2+3\cdot198560^2\) and \(225833^2+3\cdot121632^2\). Thus the failure for this map persists even with a valid native point.

The sharp local countercontrol is \(323=17\cdot19\). The same map passes both \(3\)-adic tests there, while the actual native plus shell has valuation one at the inert prime \(647\), of exact order \(323\) for \(25/9\). Passing the local discriminant test supplies no compatible mixed multiplier.

The four base character checks can be replayed in PARI/GP. Here \(2\) denotes \(-1\) in \(\mathbb F_3\).

```gp
for(i=1,3,d=[17,119,323][i]; P=Mod(1,3)*polcyclo(d); e=(3^znorder(Mod(3,d))-1)/2; R=[1+x,1-x,x^2+x-1,x^2-x-1]; print([d,vector(4,j,lift(lift(Mod(Mod(1,3)*R[j],P)^e)))]));
```

The outputs are `[17,[1,2,1,1]]`, `[119,[1,2,2,2]]`, and `[323,[1,1,1,1]]`. 
