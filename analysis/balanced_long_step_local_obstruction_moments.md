# Moment bounds for balanced long-step local obstruction weights

For fixed \(r,s\asymp R\) and a fixed chart, the weighted second moment gives an exceptional fraction of \(O_\epsilon(R^{-11/9+\epsilon})\) at the \(R^{55/24}\) threshold. The fourth moment improves this to \(O_\epsilon(R^{-83/36+\epsilon})\), enough to take a union over all \(O(R^2)\) pairs at that scale. **A prescribed target still requires a pointwise argument.** The exact shared-prime interaction and the CRT maximum criterion below identify two constraints that such an argument must handle.

**Scope.** Fix the chart exponents independently of the targets. Both base orders are divisible by the fixed pair product \(rs\), so \(p\equiv1\bmod rs\). Restrict to \(p\nmid n\), side \(J\asymp R^{4/3}\), balanced long steps and nonzero determinant as in the [mixed-phase lattice note](https://github.com/Samsen879/a303656/pull/58). Work on an interval of length \(X\) with \(R=o(\log X)\), so endpoint errors are negligible. An exact valuation-1 hit is a local obstruction, not a two-square representation.

### Shared primes and actual phase numerators

For a fixed trajectory \(t\), write its forced normalized starting phase as \(\rho_t=U_t/V_t\), where \(U_t=1-y^{bk}\), \(V_t=x^{ah}-y^{bk}\), \(x=3^{720}\), and \(y=5^{720}\). For two trajectories \(t,u\) at the same physical prime and target, their starts must differ by \((d,e)\) satisfying
\[
\begin{aligned}
p&\mid \operatorname{num}\!\left(U_tV_u x^d-U_uV_t\right),\\
p&\mid \operatorname{num}\!\left((V_t-U_t)V_u y^e-(V_u-U_u)V_t\right).
\end{aligned}
\]
The denominators are units at the primes considered. Because the chart is shorter than half either order, there is at most one possible translation \((d,e)\). Equal normalized phases force zero translation.

For each common target residue \(\nu\bmod p\), let \(F_t(\nu)\) be the set of forbidden lift digits obtained from the actual shifted sums modulo \(p^2\). The exact number of joint lifts is
\[
p-\lvert F_t(\nu)\cup F_u(\nu)\rvert .
\]
Thus repeated forbidden digits are charged once. For distinct physical primes, CRT gives the exact product of the accepted residue counts modulo the product of their squared moduli.

The original \(n\), with \(p=1259\), gives the following controls.

| Two trajectories | Common residues mod \(p\) | Start translation | Accepted joint lifts mod \(p^2\) |
|---|---:|---|---:|
| \(I=11\) and \(I=5\), both at phase \(233\) | 34 | \((0,0)\) | 42,568 |
| \(I=1\) at phase \(806\) and \(I=11\) at phase \(233\) | 9 | \((-131,233)\) | 11,260 |

All 34 residues of the \(I=5\) trajectory overlap the \(I=11\) trajectory. At the original target, the \(I=5,7,11\) trajectories share forbidden lift digit \(997\) from their common start. Their union has ten forbidden digits, and the target uses digit \(971\). In the first row of the table, the mixed numerators reduce to \(1105p\) and \(154p\bmod p^2\). In the second row they reduce to \(365p\) and \(792p\). **Both numerators can have valuation exactly one while both trajectories give true four-hits at the same target.** This rules out an extra factor of \(p\) in the mixed-divisibility condition.

### Weighted moments and parameter costs

Write \(W=\sum_p(\log p)C_p(n)\), with \(C_p\) counting labelled balanced long-step triples. Its exact-once version is periodic modulo \(p^2\) at each prime. Let \(m_p\) be the number of templates with determinant divisible by \(p\). The established determinant charge gives \(\sum_p m_p\log p=O_\epsilon(R^{3+\epsilon})\), and every contributing prime has \(\log p=O(R)\).

The uniform bound \(C_p(n)=O_\epsilon(R^{7/4+\epsilon})\) uses \(O(R)\) chart hits, \(O(R^{3/4})\) first displacements near each hit, and \(O_\epsilon(R^\epsilon)\) labels per displacement. The hit bounds follow by translating the two geometric progressions and applying the Cartesian incidence theorem. [Stevens–de Zeeuw, Theorem 4](https://arxiv.org/pdf/1609.06284v4#page=3)

Take a small fixed \(\sigma>0\) and cut at
\[
T=R^{13/72-\sigma},\qquad P_0=R^{61/24-\sigma}.
\]
The primes with a phase relation of length at most \(T\) contribute \(O_\epsilon(R^{7/4+\epsilon}T^3)\) pointwise, by charging the numerators of \(x^i-y^j\) for \(|i|,|j|\le T\). The primes \(p\le P_0\) contribute \(O_\epsilon(R^{7/4+\epsilon}(1+P_0/R^2)\log R)\) pointwise, since \(p\equiv1\bmod rs\). Both contributions are \(o(R^{55/24})\) with sufficiently small incidence slack.

For the remaining primes, the mixed phase lattice allows at most
\[
K=O(1+J/T+J^2/(rs))=O(R^{83/72+\sigma})
\]
target residues per template modulo \(p\). Put \(X_p=(C_p-\mathbb E_{p^2}C_p)\log p\). For \(j=2,4\), the per-prime maximum and \(\mathbb E_{p^2}C_p\le m_pK/p\) give
\[
\sum_p\mathbb E_{p^2}|X_p|^j
\ll_\epsilon
R^{(j-1)7/4+\epsilon} R^3K
\frac{(\log P_0)^{j-1}}{P_0}.
\]
This uses the decrease of \((\log p)^{j-1}/p\) above \(P_0\). The remaining mean is \(O(R^{29/18+2\sigma})\). CRT eliminates cross-prime terms in the centred second moment. In the fourth moment, the surviving terms are the individual fourth moments and the products of two variances. Averaging over an actual \(H\)-bit interval changes either expansion by at most \(R^{O(1)}e^{O(R)}/2^H\), since each term involves at most four squared prime moduli.

The second and fourth moments are therefore \(O_\epsilon(R^{121/36+2\sigma+\epsilon})\) and \(O_\epsilon(R^{247/36+2\sigma+\epsilon})\) for small enough \(\sigma\). Dividing by the appropriate powers of the threshold gives the stated exceptional fractions after absorbing slack. A union over \(r,s\) costs \(O(R^2)\), so the fourth moment gives an **almost-all simultaneous bound for each pair separately**, with exceptional fraction \(O_\epsilon(R^{-11/36+\epsilon})\). This uses one fixed chart head across the target interval. It does not bound the sum of the weights over all pairs at the single-pair threshold.

The pointwise barrier has a precise form. For any panel \(\mathcal Q\) with \(\prod_{p\in\mathcal Q}p^2\le|\mathcal N|\), every interval \(\mathcal N\) of that length contains a target realizing all local maxima simultaneously. Hence
\[
\max_{n\in\mathcal N} W_n
\ \ge\
\sum_{p\in\mathcal Q}(\log p)\max_{a\bmod p^2}C_p(a).
\]
A panel exceeding the threshold would give an actual target counterexample. No such growing panel is established here. This criterion explains why CRT independence and small moments alone cannot exclude a prescribed target.

### Standalone replay

The `8807` trajectory supplies a distinct-prime control at the same actual constructed integer. The code also checks the exact two mixed numerators and the repeated lift.

~~~python
from math import gcd,isqrt

p,q,r,s,J,t,H = 1259,8807,17,37,310,155521,3720000
P,Q,L,M = p*p,q*q,H//2-4,146651884329720
C,E = 3*t+80,t+144
assert all(a>1 and all(a%d for d in range(2,isqrt(a)+1)) for a in (p,q,r,s))
assert gcd(M,Q)==1 and M*Q<1<<(L-4)
assert max(2*(C+720*(J-1)),3*(E+720*(J-1)))<H-5

def target(m):
    def coord(a,b):
        c=a+M*((b-a)*pow(M,-1,Q)%Q)
        return (pow(2,L,m)+(c-pow(2,L,M*Q))%(M*Q))%m
    u,v=coord(61827877807697,0),coord(135417323161960,39021647)
    return (pow(3,C,m)+pow(5,E,m)+85*(u*u+v*v))%m

def track(a,row,I):
    n,m=target(a*a),a*a
    o=row[0]
    v,w,f=[(i-o[0],j-o[1]) for i,j in row[1:]]
    def det(u,v): return u[0]*v[1]-u[1]*v[0]
    e,b,c=det(v,w),det(f,w),det(v,f)
    if e<0:
        e,b,c=-e,-b,-c
    g=gcd(e,gcd(b,c))
    h,k=[gcd(u,z)*(1 if u>0 else -1) for u,z in zip(v,w)]
    assert (v[0]//h)*(w[1]//k)%r==(w[0]//h)*(v[1]//k)%r==I
    assert 0<b and 0<c and b+c<e and (e//g)%r==0 and e//g<=408
    for B in (3,5):
        assert all(pow(B,720*((a-1)//d),a)!=1 for d in (r,s))
    A,B=([pow(b,c+720*i,m) for i in range(J)] for b,c in ((3,C),(5,E)))
    log={z%a:j for j,z in enumerate(B)}
    X,Y=pow(3,720*v[0],m),pow(5,720*v[1],m)
    U,V=1-Y,X-Y
    rho=U*pow(V,-1,a)%a
    hits={}
    for i,x in enumerate(A):
        nu=x*pow(rho,-1,a)%a
        j=log.get(nu*(1-rho)%a)
        if j is None:
            continue
        pts=[(i+u,j+z) for u,z in ((0,0),v,w,f)]
        if not all(0<=u<J and 0<=z<J for u,z in pts):
            continue
        sums=[(A[u]+B[z])%m for u,z in pts]
        assert all(z%a==nu for z in sums)
        hits[nu]=((i,j),{z//a for z in sums})
    assert hits[n%a][0]==o and n//a not in hits[n%a][1]
    return rho,hits,(U,V)

rows=[
 ((148,16),(160,1),(232,13),(171,9)),
 ((17,249),(32,193),(74,77),(38,181)),
 ((17,249),(47,143),(293,151),(73,226)),
 ((17,249),(71,138),(145,69),(83,150))]
data=[track(p,row,I) for row,I in zip(rows,(1,11,7,5))]
assert [rho for rho,_,_ in data]==[806,233,233,233]
A,B,C0,D=[x[1] for x in data]
assert list(map(len,(A,B,C0,D)))==[109,48,11,34]

def overlap(A,B):
    keys=A.keys()&B.keys()
    shifts={tuple(y-x for x,y in zip(A[n][0],B[n][0])) for n in keys}
    return len(keys),shifts,sum(p-len(A[n][1]|B[n][1]) for n in keys)

assert overlap(B,D)==(34,{(0,0)},42568)
assert overlap(A,B)==(9,{(-131,233)},11260)
n=target(P)
bad=[S[n%p][1] for S in (B,C0,D)]
assert set.intersection(*bad)=={997} and len(set.union(*bad))==10 and n//p==971

def mixed(i,j,u,v):
    U,V=data[i][2]
    X,Y=data[j][2]
    return ((U*Y*pow(3,720*u,P)-X*V)%P,
            ((V-U)*Y*pow(5,720*v,P)-(Y-X)*V)%P)

assert mixed(1,3,0,0)==(1105*p,154*p)
assert mixed(0,1,-131,233)==(365*p,792*p)

rho,F,_=track(q,((34,175),(277,148),(292,169),(266,159)),9)
assert rho==396 and target(Q)==54 and target(P*Q)==50857136483868
assert sum(p-len(Z) for _,Z in B.values())==60240
assert sum(q-len(Z) for _,Z in F.values())==61621
print("OK")
~~~
