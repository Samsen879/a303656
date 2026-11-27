# A second infinite first-248 family: columns 4, 8, 12, and 20

The [first-248 seed and base parametrization](FIRST_248_FOUR_COLUMNS_TWO_DIRECTIONS_PELL.md) can be extended with column \(20\) instead of \(16\). We get infinitely many actual integers for each of the two four-column choices, not a five-column identity.

Keep \(S=5409768750,\ g=270850,\ q_{12}=19499950\) and \(m(s)=5^{12}+1+(s^2+q_{12}^2)/g,\ x=5m(s)+4\). The base columns \(4,8,12\) have Gaussian coordinate functions affine in \(s\), as in the linked proof. The other residuals have the form of a positive rational multiple of \(s^2+h_j\), with
\[
 h_0=446373525337120,\quad h_{16}=-40882056637497500,\quad
 h_{20}=-25829822486324997500.
\]
Here \(j=0\) denotes \(x-248\) and has scale \(5/g\); the other two are parent remainders and have scale \(1/g\). At the seed \(s=S\), respective Gaussian coordinates are \(4609381+22781935i,\ 10028076+2708818i,\ 3294138+1354184i\). These identities follow by direct substitution.

Choose rational \(\tau,r\) and define \(D=(S^2+h_0)/(1+\tau^2)\), \(C=D-h_0\). If \(D>0\) is not a rational square and \(C+h_j=Dr^2\), then on \(s^2-Dt^2=C\) we have
\[
  s^2+h_0=D(1+t^2),\qquad s^2+h_j=D(r^2+t^2).
\]
For either residual, given its seed Gaussian coordinate \(z\), its new coordinate is \(z(r_*+it)/(r_*+i\tau)\), with \(r_*=1\) for \(h_0\) and \(r_*=r\) for \(h_j\). Its norm scales by exactly \((s^2+h)/(S^2+h)\). The point \((S,\tau)\) lies on the conic.

| \(j\) | \((u,w,v)\) giving \((\tau,r)=(u/v,w/v)\) | exact \(D\) | nonsquare reduction |
|---:|---|---|---:|
| 16 | (34253989886155, 601805666935, 1421958879284) | 219059910670945169866766751040/4351058232317 | mod 3 |
| 20 | (354673167315, 249318512345, 1214575917614) | 159822589426252415108177586640/5926698097 | mod 7 |

The rational identities in the table can be replayed by \((h_j-h_0)(v^2+u^2)=(S^2+h_0)(w^2-v^2)\). Both denominators in the last column are units at the indicated prime.

Write \(D=d\gamma^2\) with a positive nonsquare integer \(d\) and rational \(\gamma>0\). Multiplication of \(S+\tau\sqrt D\) by positive powers of a norm-one Pell unit in \(\mathbb Z[\sqrt d]\) gives other conic points. Their \(s,t\) coordinates and every displayed Gaussian coordinate are affine rational expressions in the two integer Pell coordinates \(U,V\). Choose a positive modulus divisible by their coefficient denominators times \(4gM'\), where \(M'\) is the product of the squared earlier-root blockers in the linked first-248 seed proof. Choose a power of the unit which is the identity in the finite quadratic ring modulo this modulus. Its positive iterates preserve all the seed Gaussian coordinate integrality and force \(s-S\equiv0\bmod4gM'\); the original early-shift exclusions therefore persist and \(248\) stays first. Since \(S+\tau\sqrt D>0\), the iterated \(s\) grows without bound and all the designated norms are eventually strictly positive. For each parent \(m-5^d-1\) in these columns, the adjacent child \(x-5^{d+1}-9\) equals five times that parent, so multiply the parent Gaussian coordinate by \(2+i\).

This establishes two independent infinite adjacent-column families based on the same seed. It does not claim a single infinite progression retaining all five columns, and does not further constrain the original universal conjecture.
