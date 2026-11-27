# Common-center redundancy and a sharp rational-angle window

Use the fixed-weight affine certificates in [cross-pair collisions](AFFINE_CROSS_PAIR_COLLISIONS.md), with positive integral weights \(A+B=C+D=W\), \(D\notin\{A,B\}\), and target shift distinct from the source shifts. Write \(u=z_1-z_2,\ v=z_*-z_3\), \(M=N(u),N=N(v),F=u\cdot v,h=\det(u,v)\), \(\alpha=AB,\delta=CD\). Put
\[
 K=W(DS_*+CS_3-AS_1-BS_2).
\]
Then \(\alpha M-\delta N=K\) and \(F^2+h^2=MN\).

## One center, not three independent conditions

Given actual integer \(u,v\), require \(b=(Au-Dv)/W\) integral. Writing the endpoints in order as \(a+u,a,a+b,a+b+v\), put \(R=S_2-S_1-M,\ T=S_3-S_*-N-2b\cdot v\). The dot equations \(2a\cdot u=R,\ 2a\cdot v=T\) fix the rational center when \(h\ne0\). The remaining norm difference has error
\[
 2a\cdot b-(S_2-S_3-|b|^2)=(K-\alpha M+\delta N)/W^2,
\]
by plugging in \(b,R,T\). Hence it is already fixed by the variance equality. The cross-pair chords in the two matchings (oriented as \(z_1-z_*,z_3-z_2\) and \(z_2-z_*,z_3-z_1\)) are obtained by premultiplying the two original chord rows by
\[
 W^{-1}\begin{pmatrix}B&-C\\A&-D\end{pmatrix},\qquad
 W^{-1}\begin{pmatrix}-A&-C\\-B&-D\end{pmatrix}.
\]
The corresponding dot-equation right sides transform by the same matrices. Both matrices are invertible, so these are the same center once the integer chords and variance identity are retained. At \(p^j\Vert h\) with \(p\nmid 2WM(A-D)(B-D)\), its integrality is the one congruence \(MT-FR=0\bmod p^j\): \(Mv=Fu+h\,iu\), where \(i\) denotes rotation by \(90^\circ\), and \(u\) is primitive at \(p\) because \(M\) is a unit. Globally Cramer's rule checks divisibility of both coordinate numerators by \(2h\). The redundancy does not apply to independent projections that have discarded the common chord directions.

## Exact count in a narrow angle window

Fix an integer direction \((r,s)\ne(0,0)\). Among all labels with \(S_i\ll\sqrt X\), all distinct targets in \(X\le n\le2X\) satisfying \(K\ne0,\ h\ne0,\ |rF+sh|\le U\) number \(O_\epsilon((U+1)X^\epsilon)\). Define \(j=rF+sh,\ y=sF-rh,\ d=r^2+s^2\), and eliminate \(N\) using the variance equation:
\[
 d(2\alpha M-K)^2-4\alpha\delta y^2=dK^2+4\alpha\delta j^2.
\]
For each fixed label and \(j\), the right side is positive. If the form splits, count divisor pairs; otherwise, after multiplying by \(d\) and extracting square factors, count ideal divisors of the nonzero norm in the corresponding real quadratic field, then units in a logarithmic interval. The coordinates and both embeddings have polynomial height, so this gives \(X^{o(1)}\) solutions (the divisor bound and argument are as in [cross-pair collisions](AFFINE_CROSS_PAIR_COLLISIONS.md)). Each determines the Gram data. These also determine \(|a|^2\) using the inverse Gram matrix and \(R,T\), since \(b\cdot v=(AF-DN)/W\) is determined. Thus \(n=S_2+|a|^2\) is determined, regardless of rotation of the realized chords. The \(O((\log X)^8)\) label quadruples are absorbed into \(X^\epsilon\).

This exponent is attained at \(U\asymp\sqrt X\). For the first family below, \(23F+11h=-143520t-48576\), \(K=2384640\), and both \(|F|,|h|\asymp n\). The bounds on \(t\) for any sufficiently large dyadic interval contain \(\gg\sqrt X\) odd integers. The norm gcd is exactly two on odd \(t\): \(117M-128N=158976=2^8 3^3 23\), \(M/256\) has no root at \(3,23\), and \(N=2\bmod4\). Both cross-pair offsets are distinct in each matching, so the preceding collision bound is not what gives the angle bound. For the second family, the two determinants and \(h\) are zero and a common free coordinate survives; both pairings still have distinct offsets. This checks that the nonparallel premise cannot simply be removed.

### Exact replay

The shift labels for \((26,634,754,706)\) are \((0,2),(2,4),(6,2),(4,4)\). The second family exchanges the second and third shifts. Three distinct inputs verify the polynomial identities of degree at most two that are used above.

~~~python
from math import gcd

def norm(z): return sum(x*x for x in z)
def sub(z, w): return tuple(x-y for x, y in zip(z, w))

def check(z, S, weights, n):
    A, B, C, D = weights
    assert [norm(w)+s for w, s in zip(z, S)] == [n]*4
    assert all(A*x+B*y == C*v+D*w for x,y,v,w in zip(*z))
    a,b,c,e = S
    for j,k in [((A*A-D*D)*(a-e), (C*C-B*B)*(c-b)),
                ((B*B-D*D)*(b-e), (C*C-A*A)*(c-a))]:
        assert len({0,j,k}) == 3
    u,v = sub(z[0],z[1]),sub(z[3],z[2])
    return norm(u),norm(v),sum(x*y for x,y in zip(u,v)),u[0]*v[1]-u[1]*v[0]

for t in range(3):
    M,N,F,h = check(((65*t+23,27),(-63*t-25,16*t-5),
                     (-39*t-13,52*t+19),(-7,-65*t-23)),
                    (26,634,754,706),(27,65,60,32),(65*t+23)**2+755)
    assert M == 256*(65*t*t+44*t+13)
    assert N == 15210*t*t+10296*t+1800
    assert (F,h) == (6864*t*t-432*t-1056, -14352*t*t-12144*t-2208)
    assert check([(t,k) for k in (27,1,11,7)], (26,754,634,706),
                 (8,18,13,13), t*t+755) == (676,16,-104,0)
assert all((65*t*t+44*t+13)%p for p in (3,23) for t in range(p))

~~~
