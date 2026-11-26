# Cross-pair collisions in a fixed-weight affine transfer

For fixed positive integers \(A,B,C,D\) with \(A+B=C+D\) and \(D\notin\{A,B\}\), suppose the four labels are shifts \(S_i=3^{c_i}+5^{d_i}\), with \(S_*\ne S_1,S_2,S_3\). Consider certificates of
\[
 N(z_i)=n-S_i,\quad Az_1+Bz_2=Cz_3+Dz_*,\quad z_i\in\mathbb Z[i],
\]
for \(X\le n\le 2X\) and \(S_i\ll X^\eta\), with fixed \(0<\eta<1\). The following bounds count distinct targets, not representations. They concern a restricted construction, not the number of solutions of the original conjecture.

Write \(m=Az_1-Dz_*=Cz_3-Bz_2\), \(U=-Dz_1+Az_*\), \(V=-Bz_3+Cz_2\), \(L=N(m)\). Expanding norms gives
\[
N(U)=L+J,\quad N(V)=L+J',\quad
\lambda N(U-m)-\mu N(V-m)=K',
\]
where \(J=(A^2-D^2)(S_1-S_*)\), \(J'=(C^2-B^2)(S_3-S_2)\),
\(\lambda=-AD/(A+D)^2\), \(\mu=-BC/(B+C)^2\), and \(K'=(A-D)(CS_3-BS_2-AS_1+DS_*)\). Here \(J\ne0\), \(\lambda,\mu<0\), and \(\lambda\ne\mu\): equality would give either \(AC=BD\) or \(AB=CD\); the common sum then gives \(D=A\) or \(D=B\). The triangle inequalities give \(L\asymp X\), since \(A\ne D\) and all original squared lengths are \(n+o(n)\).

**Bound.** Targets for which \(J'=J\) or \(J'=0\) number at most
\[
 O_\epsilon\bigl(X^{\max(2/3,(1+\eta)/2)+\epsilon}\bigr).
\]
The same applies if this holds after swapping sources \(1,2\) and their weights. For shifts \(O(\sqrt X)\) this is \(O_\epsilon(X^{3/4+\epsilon})\).

### Counting argument

In an equal-norm pair \(w\beta,w\zeta\overline\beta\), take \(w\) to be its Gaussian gcd, and \(\zeta\) a unit. This form holds because the coprime equal-norm quotients have no inert or ramified factors and use opposite primes with equal exponents at each split prime. Write \(T=N(w)\) and \(M=N(\beta)=\kappa(x^2+y^2)\) using integer coordinates along the reflection of \(\zeta\overline\beta\). Here \(\kappa=1\) or \(1/2\), and \(y=0\) is the fixed axis.

* If \(J'=J\), factor \(U,V\) this way. Put \(\ell=\lambda-\mu\), \(k=\lambda+\mu\), \(Q=\kappa(\ell^2x^2+k^2y^2)\). The Gram identity for \(m,\lambda U-\mu V\) gives the necessary square
\[
 4(TM-J)TQ-[\ell(2TM-J)-K']^2.
\]
At fixed \(\beta\) with \(y\ne0\), the coefficient of \(T^2\) is \(4M(Q-\ell^2M)>0\). The constant is \(-(\ell J+K')^2\); if it vanishes, the coefficient of \(T\) is \(-4JQ\ne0\). Thus the discriminant is nonzero. At fixed \(T,y\) the expression is \(a_y x^2+b_y\) (the \(x^4\) terms cancel). The leading \(y^2\) coefficient of \(a_y\) and leading \(y^4\) coefficient of \(b_y\) are both \(4T^2\kappa^2(k^2-\ell^2)\ne0\). If \(y=0\) then \(U=V\) and \(E=N(U-m)=K'/\ell\) is fixed, leading instead to the square \(4EL-(J-E)^2\). The case \(E=0\) is impossible since \(J\ne0\).

* If \(J'=0\), factor \(m,V\) instead. Put \(L=TM\), \(S=N(V-m)=4\kappa T y^2\), \(k_0=K'/\lambda\), \(r=\mu/\lambda>0\) with \(r\ne1\). The Gram identity for \(m,U\) gives the necessary square
\[
 4L(k_0+rS)-(J-k_0-rS)^2.
\]
At fixed \(T,y\) it is \(a_yx^2+b_y\); \(a_y=4T\kappa(k_0+4r\kappa Ty^2)\) and the leading \(y^4\) coefficient of \(b_y\) is \(16r(1-r)\kappa^2T^2\ne0\). At fixed \(\beta\), the constant in \(T\) is \(-(J-k_0)^2\); if zero then the linear coefficient is \(4JM\ne0\). A nonzero quadratic with vanishing discriminant must therefore have negative leading coefficient, giving at most one solution. A zero quadratic coefficient means \(S=0\) or \(rS=4L\). These reduce to the linear squares \(4k_0L-(J-k_0)^2\) and \(4(2J-k_0)L-(J-k_0)^2\), respectively, with no solutions at zero slope.

Fixed denominators in these square tests are cleared by a fixed square. In a polynomial-size box a quadratic with nonzero leading coefficient and discriminant takes square values at \(X^{o(1)}\) integers, uniformly when its coefficients have polynomial size. Indeed completion of the square gives \(v^2-a u^2=\Delta\ne0\) with polynomially bounded variables. For square \(a\), count divisor pairs of \(\Delta\). Otherwise use ideals dividing \((\Delta)\) in the quadratic field after moving square factors of \(a\) into \(u\). There are at most \(\tau(|\Delta|)^2\) ideal choices; generators in each real unit orbit lying in the box number \(O(\log X)\) (both conjugates are bounded above by a power of \(X\), below by the nonzero norm and the upper bound on the other conjugate; the fundamental unit is bounded away from 1). Imaginary unit groups are bounded.

For \(T\le X^{1/3}\), enumerate \(w\) and \(O(\sqrt{X/T})\) choices of \(y\), allowing the boundedly many roots of \(a_y b_y\) to use \(O(\sqrt{X/T})\) choices of \(x\) each. The result is \(X^{2/3+o(1)}\). For \(T>X^{1/3}\), enumerate \(\beta\) of norm \(O(X^{2/3})\). The quadratic test gives \(X^{o(1)}\) choices of \(T\) per \(\beta\), and there are \(X^{o(1)}\) choices of \(w\) per \(T\). For the nonexceptional pairs the third Gaussian vector is on a given circle and a line with nonzero normal, hence there are at most two choices. In the first case this normal is \(\lambda U-\mu V\ne0\) because \(N(U)=N(V)>0\); in the second case it is proportional to \(m\ne0\).

For the linear exceptions, \(L=O(X)\), the slope and the square root of the magnitude of the constant are \(O(X^\eta)\), and the square root ranges over \(O(X^{(1+\eta)/2})\) possibilities. A nonzero slope gives at most one \(L\) per square. No coordinate count is needed: \(E=N(U-m)\) is determined by \(L\) in these exceptions, and
\[
 L=(A-D)(A(n-S_1)-D(n-S_*))+
             AD\,E/(A+D)^2
\]
determines \(n\). Summing over \(O((\log X)^8)\) label quadruples preserves the asserted bound.

### Exact finite controls

Each row below has squared shifts at most \(n\), both original inner product and determinant at least \(n/4\) in absolute value, and \(\gcd(N(z_1-z_2),N(z_*-z_3))=2\). Coordinates and labels list three sources followed by the target. The last row has three distinct offsets in both pairings, so neither power bound applies there.

~~~python
from math import gcd

cases = [
 (9114, [(4,1),(2,0),(4,0),(1,1)],
  [(-82,-48),(-52,80),(-94,14),(-9,-95)], (18,7,19,6)),
 (13280, [(0,1),(1,2),(3,0),(4,1)],
  [(-115,-7),(-16,114),(114,-16),(-75,87)], (5590,10943,2233,14300)),
 (67542, [(1,0),(3,0),(3,2),(4,0)],
  [(-143,-217),(115,233),(-97,-241),(-238,-104)], (47939,1459,35952,13446)),
]
def norm(z): return sum(i*i for i in z)
def sub(x,y): return tuple(a-b for a,b in zip(x,y))
for n, labels, z, (A,B,C,D) in cases:
    S = [3**c + 5**d for c,d in labels]
    assert A+B == C+D and max(S)**2 <= n
    assert all(norm(v) == n-s for v,s in zip(z,S))
    assert all(A*a+B*b == C*c+D*d for a,b,c,d in zip(*z))
    u,v = sub(z[0],z[1]),sub(z[3],z[2])
    F,h = sum(a*b for a,b in zip(u,v)), u[0]*v[1]-u[1]*v[0]
    assert 4*min(abs(F),abs(h)) >= n and gcd(norm(u),norm(v)) == 2
    assert labels[3][0] not in [c for c,d in labels[:3]]
    J,J1=(A*A-D*D)*(S[0]-S[3]),(C*C-B*B)*(S[2]-S[1])
    Q,Q1=(B*B-D*D)*(S[1]-S[3]),(C*C-A*A)*(S[2]-S[0])
    print(n, (J,J1), (Q,Q1))
    if n == 9114: assert J == J1 != 0
    if n == 13280: assert J1 == 0 != J
    if n == 67542: assert len({0,J,J1}) == len({0,Q,Q1}) == 3
~~~

The all-distinct small-gcd case is outside this bound. No result here says that affine transfers exhaust possible representations or gives a density conclusion for the original conjecture.
