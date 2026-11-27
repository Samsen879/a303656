# Both P2 factors need a nontrivial low cyclotomic part

Take the [second four-square pattern](FOURTH_SQUARE_COMPLETE_LOCAL_COVER.md) with \(A=3^a,B=5^b\) balanced, \((a,b)=(22,4)\bmod720\), and \(11^r\mid a-1,b+2\) for \(r\ge3\). Such compatible independent progressions have cofinal balanced pairs by irrational rotation. Set \(d=2(A+75B), e=20A+25B, f=182A-6B\). The roots of the first and third residuals must be even since their squares differ by 4 modulo 8, and all four residuals have the same class modulo 4. In any actual solution let \(u=R+Y,v=R-Y\) with \(R,Y\) the first two positive half-roots. Then \(uv=d\), and \((u+v)^2-4e,(u+v)^2-4f\) must be squares.

Put \(X=3^{(a-1)/11^r},Y_0=5^{(b+2)/11^r}\). The factorization is
\[
 d=24 L C,\qquad L=(X^{121}+Y_0^{121})/4,\qquad
 C=\prod_{j=3}^{r}\frac{X^{11^j}+Y_0^{11^j}}{X^{11^{j-1}}+Y_0^{11^{j-1}}}.
\]
Here \(v_2(d)=3,v_3(d)=1\) by the exponent parities and \(11\nmid d\) by the fixed exponent classes modulo ten. The high quotients have mutually distinct exact residue orders \(2\cdot11^j\) on their prime factors (the only exceptional factor 11 cannot occur). They are coprime to the low part. Every prime factor \(p>3\) of \(d\) is \(1\bmod3\) because \((3^{a/2}/(5\cdot5^{b/2}))^2=-3\bmod p\), and hence every divisor of \(L\) is \(1\bmod6\). Every prime factor of the high quotients is moreover \(1\bmod 2\cdot11^j\), so every divisor of \(C\) is \(1\bmod7986\).

Both \(u,v\) are even since they have the same parity and even product. Each has form \(kwz\) with \(k\in\{2,4,6,12\}, w\mid L, z\mid C\). If \(w=1\), the factor is congruent to \(k\bmod 1331\) and the exact complement is determined by \(uv=d\) there, because 11 is a unit on the factors. For these four choices the residual \((u+v)^2-4e\) is respectively \(255,968,1315,22\bmod1331\), none a square. For 968 the smaller modulus 121 admits zero, showing why the third 11-digit matters. These residues are fixed over the family: \(a,b\) are fixed modulo ten and modulo \(11^3\), which fixes both modular powers. Thus all actual solutions must distribute nontrivial factors of \(L\) to **both** sides; allocating the whole low part to one side is excluded regardless of \(K\). The remaining allocations are open.

For the explicit \(r=3\) exponent example, the replay checks all 24 possible low-factor classes in a \(7986\)-period for each \(k\) and their actual divisibility into \(L\). It yields sharp necessary lower bounds from this one period: \(7987,727,283,7987\) respectively. Indeed if no divisor works through 7986 then any valid positive divisor is larger. In the ordinary window \(S_3<K\le729A+625B\), the short side has \(4\sqrt A<v<(21/2)\sqrt A\), from the endpoint bounds on the two half-roots. Therefore a required high-block divisor \(Q\) assigned to the short side is impossible when \(k w_{\min}Q\ge(21/2)\sqrt A\). After fixing a true low divisor \(w\) and high factor \(Q\) on that side, one must still find \(z\mid C/Q\) in the resulting short open interval with \(z=1\bmod7986\), and check the two exact extra squares. No complete exclusion of the example's entire \(K\)-window is claimed.

~~~python
from math import gcd

a, b = 3874963491717839302, 2645074082853640084
q = 11**3
A, B = pow(3, a, q), pow(5, b, q)
d, e, f = 2*(A+75*B) % q, (20*A+25*B) % q, (182*A-6*B) % q
squares = {x*x % q for x in range(q)}

def residuals(v):
    s = (v + d*pow(v, -1, q))**2
    return (s-4*e) % q, (s-4*f) % q

ks = (2, 4, 6, 12)
assert [residuals(k)[0] for k in ks] == [255, 968, 1315, 22]
assert all(residuals(k)[0] not in squares for k in ks)
for k in ks:
    good = [w for w in range(1, 6*q, 6) if gcd(w, q) == 1
            and all(x in squares for x in residuals(k*w))]
    assert len(good) == 24
    print(k, [w for w in good if
              (pow(3, (a-1)//11, 4*w) + pow(5, (b+2)//11, 4*w)) % (4*w) == 0])

~~~
