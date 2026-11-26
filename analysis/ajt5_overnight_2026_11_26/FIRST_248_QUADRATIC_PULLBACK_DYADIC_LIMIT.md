# A 2-adic integrality obstruction for simultaneous quadratic norm pullbacks

Let \(h_0,h_3\) be rational with \(v_2(h_0)=-1\) and \(v_2(h_3)=3\). Suppose \(s=\alpha t^2+\beta\), with \(\alpha,\beta\) rational and \(\alpha\ne0\), makes both \(s^2+h_i\) sums of two squares of rational polynomials in t. Then this substitution cannot take a rational t to \(\mathbb Z_2\). The statement concerns a common polynomial parametrization; it does not say that the two original norm conditions cannot hold at the same integer s.

Indeed, for each i rotate the leading coordinates to \((\alpha,0)\) by a rational norm-one rotation. Comparing cubic and linear coefficients then gives coordinates \(\alpha t^2+b,ct+d\) with \(cd=0\). If \(c=0\), the \(t^2\) coefficient gives \(b=\beta\) and \(h_i=d^2\), impossible by odd valuation. Thus \(d=0\), and setting \(u=\beta-b\) yields
\[
 u(2\beta-u)=-h_i,\qquad (ct)^2=2u(s-\beta),\qquad
 (\beta-u)^2=\beta^2+h_i.
\]

Assume \(s\in\mathbb Z_2\). The last identity for \(h_0\) excludes integral \(\beta\) by the odd valuation of its right side. It excludes \(v_2(\beta)=-1\) because multiplying by 4 makes the right side an odd unit congruent to 3 or 7 modulo 8. Write \(v_2(\beta)=-a\), \(a\ge2\).

For either \(h_i\), write \(w=v_2(h_i)\). Since \(w>2(1-a)\), the two roots of \(u(2\beta-u)=-h_i\), if they exist, have valuations \(w+a-1\) and \(1-a\): their sum has valuation \(1-a\) and their product has valuation w, so the valuations must be unequal. For the root of valuation \(w+a-1\), \(2u(s-\beta)\) has valuation w and cannot be a square. For the root of valuation \(1-a\), write \(u=2\beta(1+e)\); then \(v_2(e)=w+2a-2\), and
\[
 \frac{2u(s-\beta)}{(2\beta)^2}=(1+e)(s/\beta-1).
\]
At \(h_0\), if \(a\ge3\), this unit is 7 modulo 8. Thus \(a=2\) is necessary. At \(h_3\), when \(a=2\), one has \(v_2(e)=5\) and \(v_2(s/\beta)\ge2\), giving 3 or 7 modulo 8. This excludes both roots for the second identity.

## Real column data

Use the modulus M, exponent period P, and original primitive direction from [the compatible column pair proof](FIRST_248_COMPATIBLE_COLUMN_PAIRS.md). Put \((i,E,j)=(4,4+10P,4+4P)\), \(J=(5^E-5^i)/16\), \(B=(5^E-5^j)/4\). Choose a primitive vector G in the original class modulo \(4M\), with \(G\equiv(1,0)\bmod83^2\). Such a lift exists: fix a positive second coordinate in its class, then choose the first coordinate to avoid its prime divisors outside the common modulus; at primes of the modulus the pair is not simultaneously zero. Write \(g=\|G\|^2,\ q=J-g\). Choose \(U_*\) on \(G\cdot U_*=q\) with the prescribed compatible classes, including \(U_*\equiv(2880,0)\bmod83^2\). This last class satisfies the dot equation because \(J\equiv2881\bmod83^2\). The original mod M requirement is \(U_*\equiv-G\bmod M\); for mod 4 choose the second coordinate \(J-1\) and the first of opposite parity. Combining the classes and correcting their dot product by a multiple of the common modulus times a Bézout vector yields the claimed exact \(U_*\).

Put \(U_n=U_*+4M83^2 n\,G^\perp\), \(s=G^\perp\cdot U_n\), and \(m=5^E+1+4\|U_n\|^2\). The two base columns remain genuine norms by the same dot identity as the compatible pair proof. The two additional targets, namely \(5m+4-248\) and the parent residual \(m-5^j-1\), are respectively the following two expressions times known rational norm constants \(20/g\) and \(4/g\):
\[
 s^2+h_0,\quad s^2+h_3,\qquad
 h_0=q^2+g(5^{E+1}-239)/20,\quad h_3=q^2+gB.
\]
The old earlier-root obstructions persist modulo M. Also \(g\equiv1\bmod4\), \(J\equiv3\bmod16\) and \(B\equiv4\bmod16\). This gives \(h_3\equiv8\bmod16\). Meanwhile \(5^{E+1}-239\equiv6\bmod8\), giving \(v_2(h_0)=-1\). The prime 83 is not an odd-valuation obstruction for either new target: the three parent residuals in order \(i,E,j\) are \(4938,176,6830\) modulo \(83^2\), and \(5m+4-248\equiv20\bmod83^2\), all units modulo 83. The obstruction is instead to a common quadratic polynomial parametrization which can attain the integer s progression. It neither rules out a common rational-function pullback nor settles actual double success.

Offline residue replay (use M and P from the primitive seed and pair notes):
~~~python
P = 6794538543090173141159605868485890378482780024489277462090887580403986045899337581148450
i, E, j = 4, 4+10*P, 4+4*P
def diff(hi, lo, den, mod):
    return (pow(5, hi, den*mod)-pow(5, lo, den*mod)) % (den*mod) // den
assert diff(E,i,16,16) == 3 and diff(E,j,4,16) == 4
assert (pow(5,E+1,8)-239) % 8 == 6
r = 83**2
assert diff(E,i,16,r) == 2881
m = (pow(5,E,r)+1+4*2880**2) % r
assert m == 5564
assert [(m-pow(5,d,r)-1) % r for d in (i,E,j)] == [4938,176,6830]
assert (5*m+4-248) % r == 20
~~~
