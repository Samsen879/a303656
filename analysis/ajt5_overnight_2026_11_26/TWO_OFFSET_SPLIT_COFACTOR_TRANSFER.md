# Two-offset split-cofactor transfer

Two offsets can help at a fixed target, but their arithmetic matters. **Two pure \(5\)-offsets give an exact transfer rule with the same split divisor \(B\). Two mixed offsets can share a growing split divisor and still fail simultaneously at the same inert prime.** Both results use actual \(3,5\) labels and retain the ordinary height window.

### Compatibility at a fixed target

Let \(m=n-S_0\) have a supplied Gaussian representation, and let \(D_i=S_i-S_0\) be two offsets. The largest candidate norm of a split-only Gaussian divisor shared by all three labels is the split part of \(\gcd(m,D_1,D_2)\). Each required split-prime exponent can be taken from the supplied Gaussian integer. Whether the two resulting quotients are norms is a separate test. [Checked split-cofactor framework](https://github.com/Samsen879/a303656/commit/ded83dbd0a7847f7604d3ad8bc3058c3f07d4cfd)

There are two useful restrictions.

- **Fixed nonparallel offsets cap the shared divisor.** Clear the fixed denominators and write the offsets as \(u_iA+v_iB\). A common divisor divides both \((u_1v_2-u_2v_1)A\) and \((u_1v_2-u_2v_1)B\), hence divides the determinant.
- **Inert depths can lock together.** If \(q^{\ell+1}\mid m\) and both offsets have exact odd \(q\)-depth \(\ell\), both second remainders have odd depth \(\ell\). No split divisor removes it. An offset that is a unit at \(q\) escapes this particular obstruction.

### Exact transfer with two pure \(5\)-offsets

Keep the balanced strip and ordinary window, and take the two actual labels
\[
P=A+125B,\qquad Q=A+625B.
\]
Suppose the prescribed \(n\) satisfies \(n\equiv S_0\bmod121\), \(B\mid n-S_0\), and \(n\le U=729A+625B\). Assume its supplied \(S_0\) representation has ordinary height. Put \(k=(n-S_0)/B\). The height bounds give \(720<k<1347\), and the congruence gives \(121\mid k\). The supplied norm rules out \(726,847,1331\) by odd inert depths at \(3,7,11\), respectively. The exact remaining cases are:

| \(k\) | Quotient for \(P\) | Quotient for \(Q\) |
|---:|---|---|
| 968 | \(868\), odd depth at \(7\) | \(368\), odd depth at \(23\) |
| 1089 | \(989\), odd depth at \(23\) | \(489\), odd depth at \(3\) |
| 1210 | \(1110\), odd depth at \(3\) | \(610=23^2+9^2\) |

At \(k=1210\), choose any oriented Gaussian divisor \(\pi\) of norm \(B=5^b\) from the supplied first representation. The second representative \(\pi(23+9i)\) can be rotated by a unit to put at least \(305B\) in its first square. Its height is then at least \(A+930B>S_3\), and at most \(n\le U\). Thus this is a fixed-target transfer rule with a common divisor of order \(A\). The other two rows give genuine simultaneous failures. This shell cannot contain the previous deeply \(q\)-divisible targets, since \(q\nmid B\) and \(k<q\).

### Cofinal mixed failure with a growing common divisor

Use the checked lifts \(v_{281}(e)=j\) and \(v_q(e)=\ell\), with \(q=126736826507\) and odd \(\ell\). Set
\[
c=5\cdot281^j,\qquad
M=\operatorname{lcm}\bigl(4,280\cdot281^{j-1},(q-1)q^\ell\bigr).
\]
Along this phase take \(a+4\ge M\), and use \(S_2=81A+125B\) and \(S_*=3^{a+4-M}+125B\). Their difference is divisible by \(c q^{\ell+1}\). Both offsets from \(S_0\) therefore admit \(c\) and have exact odd \(q\)-depth \(\ell\).

There are actual ordinary first witnesses at targets satisfying the locking condition. Put \(\pi=(2+i)(16+5i)^j\) and choose a point of \(11q^{(\ell+1)/2}\pi\mathbb Z[i]\) near the real coordinate \(\sqrt{U-A/10-S_0}\), by rounding its Gaussian quotient. Its norm gives \(m\), and \(n=S_0+m=U-A/10+o(A)\) as the balanced height grows in this phase. The first witness is ordinary and \(n\equiv S_0\bmod121\). Moreover,
\[
U-(2S_3-S_*)=748B-729A+3^{a+4-M}>0.3A.
\]
Thus \(n>2S_3-S_*\). If either quotient were a norm, putting its larger coordinate first would give an ordinary witness sharing \(\pi\). Both quotients instead fail at \(q\). For each fixed \(j,\ell\) the offsets are fixed on a cofinal phase. Growing \(c\) in this mixed construction allows the second offset to change, as the determinant bound requires.

### Standalone replay

The following code checks real \(3,5\) targets, including an ordinary transfer and a simultaneous mixed failure.

```python
from math import isqrt

a,b = 574422,392104
A,V = 3**a,5**(b//2)
B = V*V
assert 39*A < 40*B and 125*B < 122*A
S0,S3,U = A+25*B,729*A+B,729*A+625*B
P,Q = A+125*B,A+625*B
n = S0+1210*B
assert n%121 == 36
assert n-S0 == (33*V)**2+(11*V)**2
assert n-Q == (23*V)**2+(9*V)**2
assert S3 < min(S0+33**2*B,Q+23**2*B) <= n <= U
assert ((n-P)//B)%9 == 3

n0 = S0+1089*B
assert n0%121 == 36 and n0-S0 == (33*V)**2 and S3 < n0 <= U
assert 989%23 == 0 and 989%23**2 != 0 and 489%9 == 3

# Smaller actual mixed-offset control with a common split candidate.
a,b = 87582,59784
A,B = 3**a,5**b
assert 39*A < 40*B and 125*B < 122*A
S0,S3,U = A+25*B,729*A+B,729*A+625*B
S2,Sstar = 81*A+125*B,3**(a+4-700)+125*B
c = 57**2+16**2
assert c == 5*701 and (S2-S0)%c == (Sstar-S0)%c == 0
assert (S2-Sstar)%(9*c) == 0
z = isqrt((U-S0-A//10)//c)
r = 1 if (S2-S0)//c%9 != 1 else 2
X = z+(r-z)%9
n = S0+c*X*X
assert n > 2*S3-Sstar and S3 < S0+(57*X)**2 <= n <= U
for S in (S2,Sstar):
    assert (n-S)//c%3 == 0 and (n-S)//c%9 != 0
```

The pure-\(5\) result decides the second label for **every prescribed target satisfying its hypotheses**. The mixed result rules out uniform escape even when a useful common split divisor and ordinary placement are available. Neither result asserts transfer for unrestricted targets or changes the original single-label existence question.

The simultaneous large-prime lifting seed is in the linked cofactor note. For the mixed construction, \(S_2-S_*=3^{a+4-M}(3^M-1)\); the listed periods cover each of 5, \(281^j\), and \(q^{\ell+1}\). The fixed-depth phases can be taken arbitrarily large before increasing \(j,\ell\), so the lattice spacing stays negligible relative to the square root of \(A\). The smaller standalone fixture illustrates the same simultaneous-failure mechanism at inert prime 3.
