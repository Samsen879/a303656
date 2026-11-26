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
