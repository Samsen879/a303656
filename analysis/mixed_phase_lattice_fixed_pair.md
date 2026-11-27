# Mixed phase lattice: a fixed-pair mean bound

This note concerns a **scoped weight of local obstruction triples** for A303656, not two-square representability of every target. It is independently reviewable from main; the larger [research archive](https://github.com/Samsen879/a303656/pull/57) is not a dependency.

Fix primes \(r,s\asymp R\), \(r\ne s\), and a chart head \(C,E\), independently of the target. For the physical primes retained in this chart, both \(x=3^{720}\) and \(y=5^{720}\) have order at least \(rs\); assume \(p\nmid n\). Use the short chart of side \(J\asymp R^{4/3}\) with coordinates \(\alpha x^i+\beta y^j\) where \(\alpha=3^C,\beta=5^E\). Two displacements of one oriented triple are \((ah,bk),(ch,dk)\), where \(a,b,c,d>0\) are \(O(\sqrt R)\), \(h,k\ne0\) are signed, actual displacements are \(O(R)\), and \(0\ne ad-bc\equiv0\bmod r\). Retain the long-step condition \(720|h|>\log_3\max(a,b,c,d)\), so the displacement determinant is nonzero over the rationals. Let \(W_n\) count the retained hits with weight \(\log p\) per physical prime and labelled triple; requiring exact valuation 1 or restricting to ordinary orbits can only reduce it.

For an interval of length \(X\) with \(X\ge R^4\),
\[
\frac1X\sum_n W_n\ll_\epsilon R^{35/16+\epsilon}.
\]
The same bound holds **pointwise only for the short-relation primes** with \(\lambda_p\le R^{7/48}\), defined below. Since \(55/24-35/16=5/48\), the mean gives an exceptional fraction \(O_\epsilon(R^{-5/48+\delta+\epsilon})\) at the threshold \(R^{55/24-\delta}\), for \(0<\delta<5/48\). This is fixed \(r,s\). A direct sum over varying pairs costs up to \(O(R^2)\), losing that threshold saving.

## Proof

1. **Compatibility of both axes.** For a fixed prime and displacement tuple, subtract the equations for a hit and its first translate. With \(A=x^{ah}, B=y^{bk}\), a hit requires \(A\ne B\): otherwise \(n\ne0\) forces \(A=B=1\), excluded by the actual orders and short steps. Hence
   \(\alpha x^i=n\rho,\ \beta y^j=n(1-\rho)\), with \(\rho=(1-B)/(A-B)\).
   When the ratio is compatible the pairs \((i,j)\) lie in a coset of \(\Lambda_p=\{(u,v)\in\mathbb Z^2:x^u=y^v\bmod p\}\). Its index is \(L_p=\operatorname{lcm}(\operatorname{ord}_p x,\operatorname{ord}_p y)\), since the two groups are subgroups of one cyclic group. If the shortest nonzero vector has length \(\lambda_p\), parallel lines through the coset are spaced \(L_p/\lambda_p\) apart. Each such line contributes \(O(1+J/\lambda_p)\) points. The standard planar bound \(\lambda_p^2\ll L_p\) gives \(O(1+J/\lambda_p+J^2/L_p)\) points. Distinct eligible starts supply distinct residues of \(n\), by injectivity of each axis on the short chart. Over full periods, the ratio condition instead leaves exactly the size of the intersection of the two cyclic subgroups. If \(m\) hits must have exact valuation 1, lifting an eligible \(n\bmod p\) to \(p^2\) forbids at most \(m\) of its \(p\) lifts.

2. **Short relations.** The sum of \(\log p\) for primes with \(\lambda_p\le T\) is \(O(T^3)\): such a prime divides the numerator of a nonzero \(x^u-y^v\) with \(|u|,|v|\le T\), of which there are \(O(T^2)\), each of logarithmic height \(O(T)\). At fixed \(p,n\) there are \(O(R)\) viable starts and \(O(R^{3/4})\) first displacements per start. For these bounds use a square of independent shifts of side \(L\) in a phase box of side \(L\): each hit generates \(L^2\) point-line incidences in a Cartesian product of two sets of size \(O(L)\) with \(L^2\) distinct lines. The lines are obtained by multiplying the coefficients by \(x^{-u}\) and \(y^{-v}\); normalization by the nonzero right-hand side makes the line labels injective. Distinct hit/shift pairs give distinct incidences. [Stevens–de Zeeuw, Theorem 4](https://arxiv.org/pdf/1609.06284v4#page=3) applies since \(L^3\ll p^2\), for \(L\asymp J\) and for \(L\asymp R\), using \(p\gg R^2\). It bounds the incidences by \(O(L^{11/4})\), hence hits by \(O(L^{3/4})\). For fixed first displacement, factoring its two coordinates gives \(O_\epsilon(R^\epsilon)\) labels \((a,b,h,k)\). The integer \(j=(ad-bc)/r\) is bounded and nonzero, \(\gcd(a,b)\mid j\) for large \(R\), and \(\max(a,b)\gg\sqrt R\); hence \(ad-bc=rj\) permits only \(O(1)\) choices of \(c,d\) per \(j\). The short-relation contribution is \(O_\epsilon(R^{7/4+\epsilon}T^3)\).

3. **Long relations and averaging.** The cleared nonzero displacement determinant has logarithmic height \(O(R)\) per template: for \(X=x^h,Y=y^k\), the putative equality
   \((X^a-1)/(X^c-1)=(Y^b-1)/(Y^d-1)\) would either give identical displacements, or contradict the long-step condition by comparing 3-adic valuations. For \(h>0\) subtract 1 first: the valuations are \(720h\min(a,c)\) and \(v_3(b-d)-v_3(d)\). For \(h<0\) compare the ratios directly: they have valuations \(720h(a-c)\) and \(v_3(b)-v_3(d)\). The height comes from the \(O(R)\) displacement lengths. There are \(O_\epsilon(R^{2+\epsilon})\) templates: \(O_\epsilon(R^{1+\epsilon})\) normalized quadruples by charging \(ad\equiv bc\bmod r\) and counting factorizations of the two products, and \(O(R)\) step pairs because one of the two products is \(\gg R\). Before the phase tests the prime weight is \(O_\epsilon(R^{3+\epsilon})\). For \(\lambda_p>T\), dividing the lattice bound by \(p\gg R^2\) and using \(L_p\gg R^2\) bounds the fraction of eligible residues by \(O(R^{-2}+R^{-2/3}/T+R^{-4/3})\). Counting actual integers in the interval introduces endpoint error \(O_\epsilon(R^{3+\epsilon}J/X)\), since each template has at most \(J\) eligible residues. Choose \(T=R^{7/48}\) and combine with step 2 to obtain the asserted mean. No bound for the long-relation contribution at one prescribed \(n\) is asserted.

## Same-target controls

The exact replay builds the common target via its two explicit CRT coordinates. At \(p=1259\), \(r=17,\ s=37\), three distinct ordinary four-hit trajectories with crossed-product keys \(11,7,5\) use the **same** start \((17,249)\) and phase \(233\). Their shared forbidden lift is \(997\); the target uses \(971\). Two other templates pass both full-period phase tests but recover the unique start \((195,456)\), outside the short chart of side 310. Thus neither key independence nor separate full-period membership is a safe replacement for short-chart compatibility.

~~~python
from math import gcd

p,r,s,J,t,H = 1259,17,37,310,155521,3720000
D,P,Q,L,M = r*s,p*p,8807**2,H//2-4,146651884329720
C,E = 3*t+80,t+144
assert gcd(M,Q) == 1 and M*Q < 1<<(L-4)
assert max(2*(C+720*(J-1)),3*(E+720*(J-1))) < H-5

# Read the two coordinates of the original CRT target modulo p^2.
def coord(a,b):
    c = a+M*((b-a)*pow(M,-1,Q)%Q)
    return (pow(2,L,P)+(c-pow(2,L,M*Q))%(M*Q))%P

U,V = coord(61827877807697,0),coord(135417323161960,39021647)
N = (pow(3,C,P)+pow(5,E,P)+85*(U*U+V*V))%P
assert N == 1223507
x,y = pow(3,720,p),pow(5,720,p)
for z in (x,y):
    assert pow(z,D,p) == 1 and all(pow(z,D//a,p) != 1 for a in (r,s))
assert pow(x,16,p)*y%p == 1
logs = [{pow(b,e+720*i,p):i for i in range(D)}
        for b,e in ((3,C),(5,E))]

def solve(shape,h,k):
    a,b,c,d = shape
    A,B,F,G = pow(x,a*h,p),pow(y,b*k,p),pow(x,c*h,p),pow(y,d*k,p)
    assert A != B and ((A-1)*(G-1)-(F-1)*(B-1))%p == 0
    z = (1-B)*pow(A-B,-1,p)%p
    return z,(logs[0][N*z%p],logs[1][N*(1-z)%p])

def read(i,j):
    assert 0 <= i < J and 0 <= j < J
    X,Y = pow(3,C+720*i,P),pow(5,E+720*j,P)
    S = (X+Y)%P
    assert (N-S)%P in range(p,P,p)
    z = X*pow(N,-1,p)%p
    assert pow(z,(p-1)//2,p) == pow(1-z,(p-1)//2,p) == p-1
    return z,S//p

def mob(z):
    u,v = pow(z,-1,p),pow(1-z,-1,p)
    return z,1-z,u,1-u,v,1-v

rows = [
 (1,806,(148,16),(1,5,7,1),12,-3,(171,9),408,173,87),
 (1,443,(1,268),(37,47,55,23),2,-5,(47,143),289,141,26),
 (11,233,(17,249),(5,14,19,43),3,-4,(38,181),51,22,13),
 (7,233,(17,249),(5,53,46,49),6,-2,(73,226),306,10,61),
 (5,233,(17,249),(27,37,64,60),2,-3,(83,150),34,6,15)]
keys,bad = set(),[]
for I,z,o,shape,h,k,f,e,m,l in rows:
    assert solve(shape,h,k) == (z,o)
    a,b,c,d = shape
    assert a*d%r == b*c%r == I and a*d != b*c
    v,w = (a*h,b*k),(c*h,d*k)
    assert gcd(v[0],w[0]) == abs(h) and gcd(v[1],w[1]) == abs(k)
    assert all(e*(F-O) == m*A+l*B for F,O,A,B in zip(f,o,v,w))
    assert e%r == 0 and 0<m and 0<l and m+l<e<=408 and gcd(e,gcd(m,l)) == 1
    i,j = o
    vals = [read(*q) for q in (o,(i+v[0],j+v[1]),(i+w[0],j+w[1]),f)]
    assert vals[0][0] == z
    orbit = {tuple(sorted(u%p for u in T))
             for T in zip(*(mob(u) for u,_ in vals[:3]))}
    assert all(sum(T)%p != 1 for T in orbit)
    keys.add(min(orbit))
    if z == 233:
        bad.append({b for _,b in vals})
assert len(keys) == 5
assert set.intersection(*bad) == {997}
assert len(set.union(*bad)) == 10 and N//p == 971

for I,shape in [(2,(7,11,11,10)),(13,(7,11,12,14))]:
    a,b,c,d = shape
    assert a*d%r == b*c%r == I
    assert solve(shape,5,-9) == (220,(195,456)) and 456 >= J
print("OK")
~~~
