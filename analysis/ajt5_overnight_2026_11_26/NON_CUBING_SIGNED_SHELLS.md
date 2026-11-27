# Non-cubing signed shells: exact order tests and symbolic boundary

For an admissible seed \(A=5^u,B=3^v\) with \(u,v\) odd, the plus and minus shells of a common odd raising \(r\) are the products of \(\Phi_{2d}(A,B)\) and \(\Phi_d(A,B)\), respectively, over \(d\mid r,d>1\). To track inert prime valuations, if \(p\notin\{2,3,5\}\) and \(t=\operatorname{ord}_p(A/B)\), its contributions to the homogeneous cyclotomic factors are \(v_p(A^t-B^t)\) at index \(t\), one at each index \(tp^j,\ j\ge1\), and zero elsewhere. This follows by LTE and summing valuations in the product for \(A^N-B^N\). For \(r=3^a5^b7^c\), each contributing inert prime has only one possible layer, since no inert prime outside 2 and 5 divides \(r\) and 5 divides no factor. Layers with \(3\mid d\) are automatically norms: an inert prime's order cannot retain that factor of 3, and any exceptional layer power at 3 concerns only the ramified prime.

Every plus factor with \(5\mid d\) has a direct root of \(-3\) modulo \(H=\Phi_{2d}(A,B)\). Put \(T=-A/B\) and \(z=T^{d/5}\). The order rule shows \(z\) has order 5 at every prime divisor of \(H\), even if the divisor is a layer prime other than 5. Thus \(1+2(z+z^{-1})\) squares to 5; it is a unit. Writing \(A=5X^2,\ B=3Y^2\), the element \(T^{(d+1)/2}(3Y/X)\) squares to \(-15\), so the quotient gives the root. This works on individual prime-power and mixed factors.

The entire minus shell after substitution \(A=5s^2,B=3\) is a rational-function norm from \(\mathbb Q(\sqrt{-3})(s)\) exactly when \(r\) is a power of 3. The plus shell is such a norm exactly when \(r=3^a5^b\). For each odd \(d>1\), the root fields of the respective factors are \(F(\sqrt{15}),F(\sqrt{-15})\), \(F=\mathbb Q(\zeta_d)\): square roots of the \(d\)-th roots of unity already lie in \(F\). The roots are simple and disjoint across factors. A rational irreducible factor splits into conjugates over \(\mathbb Q(\sqrt{-3})\) precisely when the root field contains that quadratic field; if not, it must occur to even exponent in a rational-function norm. When \(3\nmid d\), minus containment would require \(\sqrt{-5}\in F\), impossible by ramification at 2, while plus containment requires \(\sqrt5\in F\), equivalent to \(5\mid d\). If \(3\mid d\) containment is automatic. The leading coefficients are squares, so the splitting criterion is sufficient as well. This is a symbolic restriction, not a ban on individual integer lifts.

For actual norm seeds, the first-prime digits in \(A^{2r}-B^{2r}\) give necessary conditions \(11\mid u\) at \(r=5\), \(3u=2v\bmod71\) at \(r=35\), and \(u=2v\bmod197\) at \(r=49\). A nonzero first digit gives valuation one and vetoes the final signed norm pair. The replay gives a genuine fifth and seventh lift and valuation-one failures at their second iterations. The two successes occupy old normalized phases and do not change the [28-ray generated exponent](https://github.com/Samsen879/a303656/commit/31be464193ce17f59e13a9fd8964b3e3ce17d257). The layer rule ensures these obstructions persist under further cubings and further powers of the same generator. Whether other seeds support an infinite run remains open.

~~~python
from fractions import Fraction
from math import gcd, isqrt

def N(x,y): return x*x+3*y*y

def vp(n,p):
    e = 0
    while n%p == 0: n,e = n//p,e+1
    return e

def veto(u,v,r,p,sign,t,residue):
    assert p%3 == 2 and all(p%d for d in range(2,isqrt(p)+1))
    A,B = 5**u,3**v
    z = A*pow(B,-1,p)%p
    assert pow(z,t,p) == 1 and all(pow(z,j,p) != 1 for j in range(1,t))
    assert (pow(A,r,p*p)+sign*pow(B,r,p*p))%(p*p) == residue
    assert 0 < residue < p*p and residue%p == 0

for row in [(1,1,5,11,-1,5,99),(11,3,25,7451,-1,25,52097392),
            (1,1,49,197,-1,49,9653),(1,1,35,71,-1,35,568),
            (3,1,7,113,1,14,10057)]:
    veto(*row)

for r,p,eps,a,b in [(5,11,1,7,0),(35,71,1,48,32),(49,197,-1,7,14)]:
    assert tuple(eps*pow(z,2*r,p*p)%(p*p) for z in (5,3)) == (1+p*a,1+p*b)
assert [(gcd(25**r-1,9**r-1),gcd(25**r+1,9**r+1))
        for r in (5,7,25,35,49)] == [(88,2),(8,2),(88,2),(6248,2),(8,394)]
assert 5**101 < 3**149 and 5**103 < 3**152 and 5**2 < 3**3
assert 3**151 < 5**105 and vp(5**(98*105)-3**(98*151),197) == 2
assert 3**47 < 5**55
assert all(vp(5**(70*55)-3**(70*47),p) == 2 for p in (11,71))

def plus_root(u,v,d,H):
    A,B = 5**u,3**v
    T = -A*pow(B,-1,H)%H
    z = pow(T,d//5,H)
    assert pow(T,d,H) == 1 and gcd(z-1,H) == 1 and pow(z,5,H) == 1
    R = 1+2*(z+pow(z,-1,H))
    S = pow(T,(d+1)//2,H)*3**((v+1)//2)*pow(5**((u-1)//2),-1,H)
    assert R*R%H == 5 and S*S%H == (-15)%H
    assert pow(S*pow(R,-1,H),2,H) == (-3)%H

A,B = 5**11,3**3
assert A*A-B*B == N(45401686,10374210)
m,p = (A**5-B**5)//(A-B),(A**5+B**5)//(A+B)
assert m == N(594392000783087,1333047033266432)
assert m == 1381637266888500**2+1943044902219479**2
assert p == N(A*A-3*A*B+B*B,5**6*3*(A-B))
plus_root(11,3,5,p)
plus_root(11,3,25,(A**25+B**25)//(A**5+B**5))
plus_root(1,1,35,(5**35+3**35)*8//((5**5+3**5)*(5**7+3**7)))
assert (5**7-3**7)//2 == N(137,80)
assert (5**7+3**7)//8 == N(74,39)
assert 125**2-3**2 == N(112,32)

A,B = 5**55,3**15
a,b,c,d = 500457685620124756,3388412195726285909,5496675473631834569,6015658368394901204
assert (A+B)//8 == N(a,b) and (A-B)//2 == N(c,d)
for Q,Z,v,w,p,r in [(A*A,B*B,8*(a*c-3*b*d),8*(a*d+b*c),23,368),
                    (5**14,3**14,47632,85880,7,14)]:
    s = isqrt(Z)
    W,V = max((abs(y),abs(x)) for x,y in
              [(v,w),((v-3*w)//2,(v+w)//2),
               ((-v-3*w)//2,(v-w)//2)] if y%3)
    assert N(V,W) == 4*(Q-Z) and p%4 == 3 and 0 < r < p*p and r%p == 0
    for L in (1,3):
        for t in (W,s+5):
            x,y = (t-s,t) if L == 1 else (t+s,t-2*s)
            S = x*x+y*y
            n = 5*Q+L*Z-S
            R = n-Q-(4-L)*Z
            assert Q < n < 5*Q and S > L*Z and n%24 == {1:21,3:3}[L]
            if t == W: assert R == V*V+(W+s)**2
            else: assert R > 0 and R%(p*p) == r

g = list(map(Fraction,("18 166/9 170/9 178/9 182/9 62/3 190/9 22 70/3 74/3 26 82/3 "
                        "86/3 30 290/9 34 110/3 38 118/3 122/3 42 130/3 134/3 46 "
                        "142/3 50 470/9 158/3 54").split()))
assert len(g) == 29 and [x for x in g[:-1] if x.numerator%11 == 0] == [22,Fraction(110,3)]
assert max(b/a for a,b in zip(g,g[1:])) == Fraction(55,51)
print("PASS")
~~~
