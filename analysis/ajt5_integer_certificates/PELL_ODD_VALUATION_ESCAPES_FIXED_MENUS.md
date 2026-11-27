# The Pell residual escapes every fixed odd-valuation menu

Let \(\alpha=3577+1599\sqrt5,\ G=(9+4\sqrt5)^{387860}\), and write \(\alpha G^n=X_n+Y_n\sqrt5\) for \(n\ge0\). Put \(R_n=X_n^2+12\). For each positive integer \(L\) and finite set \(S\) of primes congruent to 3 modulo 4, there is an infinite arithmetic progression of nonnegative \(n\), of step divisible by \(L\), such that at every point some prime \(q\equiv3\bmod4\) outside \(S\cup\{67\}\) has odd \(v_q(R_n)\). The new prime may depend on \(n\); the residue class of the progression is chosen by the construction. This is not a claim about independently prescribed residue classes, coprime activation periods, or the full conjecture.

## Proof

In \((\mathbb Z/67^2\mathbb Z)[\sqrt5]\), modular exponentiation gives \(G^{17}=1-67\sqrt5\) and \(R_{12+17t}/67=2+7t\bmod67\). The computation is in the quadratic residue algebra; no choice of a square root in \(\mathbb Z_{67}\) is necessary. The simple lift continues: for \(j\ge0\), incrementing \(t\) by \(67^j a\) changes \(R_{12+17t}\) by \(67^{j+1}(7a)\bmod67^{j+2}\). Indeed \((G^{17})^{67^j a}\equiv1-67^{j+1}a\sqrt5\bmod67^{j+2}\), and the derivative coefficient depends only on the fixed reduction \(\alpha G^{12}\bmod67\), giving the same \(7\) as the initial step. Consequently there is a unique \(t_*\in\mathbb Z_{67}\) and \(v_{67}(R_{12+17t})=1+v_{67}(t-t_*)\).

Set \(D=\operatorname{lcm}(L,17,\{r^2-1:r\in S\setminus\{67\}\})\), with \(a_0=v_{67}(D)\). Choose \(n_*=12+17t\ge0\) with \(t\equiv t_*\bmod67^{a_0}\) and put \(e_r=v_r(R_{n_*})\) for every \(r\in S\setminus\{67\}\). Enlarge \(D\) to \(D'=\operatorname{lcm}(D,\{(r^2-1)r^{e_r}:r\in S\setminus\{67\}\})\). Its 67-adic valuation is still \(a_0\). The unit \(G\) has order dividing \(r^2-1\) modulo \(r\), since \(r\ne2,5\) and the residue algebra of \(\mathbb Z[\sqrt5]\) is a field of order \(r^2\) or two copies of the field of order \(r\). Its order modulo \(r^{e_r+1}\) divides \((r^2-1)r^{e_r}\) by binomial lifting. Therefore all the old valuations \(e_r\) stay constant on \(n=n_*+D'j\).

In the parameter \(t=(n-12)/17\), the step \(D'/17\) has valuation \(a_0\). The single lifted root criterion now permits \(v_{67}(R_n)=a_0+1\) or \(a_0+2\), according to the choice of \(j\bmod67^2\). Choose the parity for which the sum of valuations over \(S\cup\{67\}\) is odd, and fix that \(j\)-class. The resulting step is \(67^2D'\). Since \(X_n\) is odd (reduce the Pell product modulo 2), \(R_n\equiv1\bmod4\). Its total valuation over all primes \(3\bmod4\) is even, so an odd valuation outside the fixed menu is required at every point. In particular, including every prime \(3\bmod4\) at most \(B\) in \(S\) forces \(q>B\), independently of the value of \(L\).

## Small reproducible controls

Multiplication modulo \(M\) uses \((a,b)(c,d)=(ac+5bd,ad+bc)\bmod M\), with binary exponentiation. Below, \(R_n\bmod r^j\) is computed using this multiplication, without constructing the large Pell integers.

| \(n\) | \(v_{67}(R_n)\) | Notes |
|---:|---:|---|
| 658 | 2 | All \(r\equiv3\bmod4\) below 67 have valuation zero. |
| 10268743 | 3 | The same old valuations are zero, and \(v_{79}(R_n)=1\). |

The two indices agree modulo 67. In contrast, restricting to \(n=658+17\cdot67^2j\) fixes \(v_{67}=2\) identically by the lifted root criterion. This distinguishes a mod-prime activation from the actual ability to change its valuation parity on a prescribed subprogression.

## Prescribed classes: a uniform result for up to five prime divisors

For every \(L\) with at most five distinct prime factors, every prescribed \(a\bmod L\), and every finite \(S\) as above, a subprogression inside \(n\equiv a\bmod L\) has an odd-valuation prime outside \(S\) at each point.

The following six pivots prove this. Here \(m\) is the first positive exponent with \(G^m=\pm1\bmod q\) in the quadratic residue algebra; \(r\) is an activated class modulo \(m\); and \(\rho\bmod q\) is the first digit of the unique index root for that class. The verification uses the modular multiplication above: check the first \(m\) powers modulo \(q\), evaluate \(R_r\) for \(0\le r<m\), and check that \(R_{r+mt}/q\bmod q\) has nonzero slope and a single root, at \(r+mt\equiv\rho\bmod q\).

| \(q\) | \(m\) | \(r\) | \(\rho\bmod q\) |
|---:|---:|---:|---:|
| 67 | 17 | 12 | 55 |
| 79 | 13 | 4 | 39 |
| 139 | 23 | 17 | 5 |
| 487 | 61 | 49 | 293 |
| 619 | 103 | 7 | 145 |
| 1039 | 173 | 37, 108 | 346, 607 respectively |

For the lift at any of these simple roots, choose the sign of \(G^m\) that is 1 modulo \(q\); replacing its sign does not change \(R\). Raising this signed unit to \(q^j\) gives the same nonzero derivative coefficient at the next \(q\)-adic digit, as in the proof at 67. Thus to have arbitrarily deep valuations in the prescribed class, the exact compatibility tests are \(a\equiv r\bmod\gcd(L,m)\) and \(a\equiv\rho\bmod q^{v_q(L)}\), where \(\rho\) is the full lifted root.

The six products \(qm\) are pairwise coprime. When \(L\) has at most five distinct prime factors, one product is coprime to \(L\) and both compatibility tests for that pivot are automatic. More generally any compatible pivot suffices: set \(D=\operatorname{lcm}(L,m,\{s^2-1:s\in S\setminus\{q\}\})\) and \(e=v_q(D)\). Use CRT to choose \(n_*\equiv a\bmod L,\ n_*\equiv r\bmod m,\ n_*\equiv\rho\bmod q^e\). Enlarge the step by powers of the old primes to freeze their valuations, without changing its \(q\)-adic valuation \(e\). On the resulting progression one can select \(v_q=e+1\) or \(e+2\); the parity argument above then forces a prime outside \(S\cup\{q\}\).

For example \(a=0,\ L=5083=17\cdot13\cdot23\) excludes the first three pivots but admits 487: \(n=182988\) belongs to this class and \(R_n\equiv467\cdot487\bmod487^2\). Conversely \(a=0,\ L=17\cdot13\cdot23\cdot61\cdot103\cdot173\) excludes every row of the fixed table. This shows a limit of this table, not a counterexample to an arbitrary prescribed-class claim. In fact \(R_0=12794941\) is a prime \(1\bmod4\); for any fixed finite menu of pivot primes \(3\bmod4\), a common period modulo those primes makes the zero class miss all their activations. Arbitrary prescribed classes therefore need a varying pivot or another method.

## Why a genuine pivot need not have a coprime period

A prescribed class can retain a parity-changing pivot even when the pivot's period shares a prime with its modulus. For example the following exact finite local data use the same orbit, the same least signed period \(m\), and the slope of \(R_{r+mt}/q\bmod q\).

| \(q\) | \(m\) | All activated phases \(r\bmod m\) | Slopes, in phase order |
|---:|---:|---|---|
| 79 | 13 | 4 | 23 |
| 103 | 13 | none | none |
| 1051 | 35 | 28 | 224 |
| 1423 | 178 | 53, 59 | 172, 1251 |
| 3727 | 466 | 316 | 1900 |

For replay, compute \(G^j\bmod q\) in the quadratic residue algebra for \(1\le j\le m\) and the residual for \(0\le j<m\); the slopes are \((R_{r+m}-R_r)/q\bmod q\) using the two residues modulo \(q^2\). The same signed binomial lift as above then applies to every listed activated phase.

For \(q=1051\) the order of the activated element \(G^{2r}\) modulo \(q\) is \(m/\gcd(m,r)=5\), even though the signed period is 35. For every \(k\ge1\), phase \(28\bmod35\) is compatible with \(n\equiv0\bmod7^k\), and \(1051\nmid7^k\), so deep valuation and both parities remain possible inside that class. Two controls at \(k=2\) are \(n=126518,126273\), with \(v_{1051}=1,2\) respectively. For any class \(a\bmod2^k\), an odd \(a\) can use phase 53 at 1423 and an even \(a\) can use phase 316 at 3727; again the odd-prime lifting remains free, although the period is even in each case. Thus the parity proof on a prescribed class cannot by itself guarantee that a newly forced prime also has period coprime to the class modulus. Conversely, 79 and 103 show that knowing an exact period alone does not guarantee even one activation of the actual residual.

## A positive-density set of moduli with arbitrarily many prime factors

Let \(B=17\cdot13\cdot23\cdot61\cdot103\cdot173\). Every prescribed residue class modulo \(L\) has the menu-escape property whenever
\[
 2B\mid L,\qquad \gcd(L,89\cdot233\cdot1423\cdot3727)=1.
\]
This set of integer moduli has positive natural density: the four excluded primes are distinct and coprime to \(2B\); its density is \((2B)^{-1}\prod_{p\in\{89,233,1423,3727\}}(1-1/p)\). Its moduli can have arbitrarily many distinct prime factors. In particular these \(L\) absorb all six periods of the original table, so the five-divisor lemma is not what proves this extension.

For a prescribed odd class use the verified phase \(53\bmod178\) at 1423; for a prescribed even class use \(316\bmod466\) at 3727. In both cases the period meets \(L\) in precisely a factor two and the phase has the required parity. Further, the pivot prime does not divide \(L\), so the simple lift permits any depth of valuation within this class. Freeze the old menu and choose the needed parity by the earlier CRT argument. This establishes the claim with one pivot selected according to the class, not a single pivot usable in all classes.

More generally the exact coarse compatibility condition for phase \(r\bmod m\) on class \(a\bmod L\) is \(\gcd(L,m)\mid r-a\). In the zero class, writing \(d=m/\gcd(m,r)\) for the activated element's order, this is equivalent to \(d\mid m/\gcd(L,m)\). Once coarse compatibility holds, the simple lift still needs to be checked against the prescribed \(q\)-adic digits when \(q\mid L\). At \(q=1051,\ m=35,\ r=28\), the modulus \(L=7357=7\cdot1051\) gives a useful distinction: the zero class matches the coarse phase but its matched points have valuation exactly one, as \(R_{29428}\equiv282\cdot1051\bmod1051^2\) and this residue is fixed on the matched subprogression. For \(a=1204\bmod7357\) at the same pivot, the indices \(15918,14067788\) lie on the matched phase and have exact valuations two and three, respectively. Both descriptions follow by the direct Pell modular replay. The remaining all-moduli, all-classes problem is not settled by either family.

## A formal-root obstruction for every zero-class exponent

Write \(F=\mathbb Q(\sqrt5)\), \(C=N(\alpha)=10924\), \(E=F(\sqrt{-3},\sqrt{-2734})\) and \(\beta_\pm=(2\sqrt{-3}\pm2\sqrt{-2734})/\alpha\). On the zero class \(n=Lt\) the actual parameter is \(Z=G^t\), but the formally free function is
\[
 R_L(Z)=\left(\frac{\alpha Z^L+C/(\alpha Z^L)}{2}\right)^2+12 .
\]
After clearing the denominator its numerator is \(P_L(Z)=\alpha^4 Z^{4L}+(2C+48)\alpha^2Z^{2L}+C^2\), with roots determined by \(Z^L\in\{\pm\beta_+,\pm\beta_-\}\).

For every positive \(L\), \(P_L\) is irreducible over \(F(i)\). Choose a prime above 2731 with \((\sqrt5,\sqrt{-3},\sqrt{-2734})\equiv(1220,893,-893)\). The denominator \(\alpha\) is a unit of residue 1692. The numerator of \(\beta_+\) vanishes and its partner has residue 841; the product of the two numerators is \(4\cdot2731\). The constant field \(E(i)\) is unramified here, so \(\beta_+\) has valuation one and \(Z^L-\beta_+\) is Eisenstein. Also \(F(\beta_+)=E\), since one recovers the two radicals from the sum and difference of the numerator and its partner (which is \(C\) divided by the numerator). The square classes of \(5,-3,-2734,-1\) are independent, so \([E(i):F(i)]=4\). A root with \(Z^L=\beta_+\) therefore has degree \(4L\) over \(F(i)\). In particular \(R_L(Z)\) cannot be a sum of two rational-function squares over \(F(Z)\): its valuation at \(P_L\) is one, while this prime stays inert in the constant extension by \(i\), so norms there have even valuation.

This function-field obstruction is not an odd-valuation witness on the discrete orbit. For \(L=11050025194,\ q=3739\), work in a split branch modulo \(q\) with the least nonnegative square roots of \(5,-3,-2734\), and lift \(\sqrt5\) modulo \(q^2\). At the free parameter \(Z=1325\), direct powering in the formula for \(R_L\) gives \(3443q\bmod q^2\). In contrast, \(G\bmod q\) is a seventh power, and the \((q-1)/7\) powers of \(\beta_+,\beta_-\) are 3071 and 2926. Their negatives give the same seventh-power test since \((q-1)/7\) is even. Therefore no integer power of \(G\) reaches any of the four targets. Direct reduction of the Pell recurrence has period 89 and no residual zero in that period. The positive odd valuation in the free parameter thus cannot be transferred to any genuine index at this prime.

## A bounded-index lift certificate and a family absorbing nine old periods

At a split good prime \(q\) in the Pell field, choose a simple actual residual target \(\beta\) for \(G^n\) in the local field \(\mathbb Q_q\). Put \(G=\phi^{6\cdot387860}\), \(\phi=(1+\sqrt5)/2\). For the prescribed class \(n=a+Lt\), set \(A=6\cdot387860L,\ H=\phi^A,\ \eta=\beta G^{-a},\ N=q-1\). Let \(i\) be the index of the subgroup generated by \(\bar\phi\) in \(\mathbb F_q^\times\). Given a verified multiple \(I\) of \(i\), put
\[
 m_0=N/\gcd(N,AI),\qquad h=v_q(H^N-1).
\]
Then \(\eta^{m_0}=1\bmod q^h\) is sufficient for the phase to activate and for its valuation parity to be freely chosen by deeper lifting. In fact the true period is \(m=N/\gcd(N,Ai)\), a multiple of \(m_0\). The order of \(H\) modulo \(q^h\) is still \(m\), since \(h=v_q(H^m-1)\). The unit group modulo \(q^h\) is cyclic, so the single test puts \(\eta\) into this actual subgroup. On the resulting phase the logarithm on principal units gives \(v_q(H^t-\eta)=h+v_q(j-j_*)\), where \(j\) is the index within the phase. The target is simple, so the residual takes the same valuations. In particular both parities occur. If \(I=i\) the same argument shows this test is necessary for varying parity on that activated phase; when the target differs before depth \(h\), its valuation is constant.

For an independent application use \(q=354757260218899,\ m=59126210036483\) from the exact signed-period replay in [Genuine Pell activation](../ajt5_overnight_2026_11_26/PELL_ACTIVATION_AND_BOUNDED_OVERLAP_MASS.md), with activation at \(n=38125102841913\). Direct quadratic-ring powering gives the additional lift certificate
\[
 G^m\equiv1+q\cdot330144670341035\sqrt5\pmod{q^2}.
\]
It is nontrivial, so this activation has a free simple valuation lift. Let \(P=8020053035679230\), the least common multiple of \(17,13,23,61,103,173,35,178,466\). One verifies \(\gcd(P,qm)=1\). For every \(L\) with \(P\mid L,\ \gcd(L,qm)=1\), the zero class can reach the activated phase and vary its parity. It follows by freezing all other old valuations that any finite menu can be escaped within that zero class. This set of moduli has positive natural density, because the restrictions are a divisibility and a coprimality condition with fixed coprime moduli. It absorbs all nine earlier small periods, but makes no claim when \(L\) also absorbs this pivot.
