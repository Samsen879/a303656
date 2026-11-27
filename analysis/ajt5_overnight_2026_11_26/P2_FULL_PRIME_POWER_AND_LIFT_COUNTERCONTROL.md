# Full prime powers in the pinned share and a genuine height countercontrol

The full-prime-power hypothesis is automatic on the pinned P2 progression: **\(\gcd(H,d/H)=1\)**. I also found a cofinal refinement that realizes a forbidden residue with a **true prime divisor of \(e\)**. On that same refinement, an ordinary integer height can pass both congruences modulo \(H^2\) and every local square test at primes up to 169, while the independent edge fails modulo 173. The ordinary short-divisor window remains open.

### Exact prime support

Put \(g=468741,\ N=1331g,\ a=Nh+1,\ b=Nk-2,\ A=3^a,\ B=5^b\), and \(x=3^h,\ y=5^k\). The four shifts are
\[
(S_0,S_1,S_2,S_3)=(A+25B,\ 9A+625B,\ 81A+125B,\ 729A+B).
\]
The two edge products are \(d=(S_1-S_0)/4=6(x^N+y^N)\) and \(e=(S_2-S_0)/4=20A+25B\). Write \(J=d/H\), where \(H\) is the product of the homogeneous cyclotomic factors with indices \(242g,\ 2662g,\ 2662\cdot3939,\ 2662\cdot1717\).

If \(p\mid H\), then \(p\) divides one of the two top blocks \(\Phi_{2\cdot11^j}(x^g,y^g)\), \(j=2,3\). The primes \(2,3,5\) are absent from these blocks, and \(d\equiv4\pmod{11}\) on the pinned phase. If the denominator of the top-block quotient vanished modulo \(p\), the quotient polynomial would reduce to \(11\) times a unit. Thus \(\operatorname{ord}_p((x/y)^g)=2\cdot11^j\), so \(p>101\) and \(p\nmid 2N\). The polynomial \(T^N+1\) is squarefree modulo \(p\). Only one of its cyclotomic factors can vanish at \(x/y\), so **all** of \(v_p(d)\) lies in \(H\). This also identifies the order of \(x/y\) as one of the four displayed indices. In particular, every \(p\mid H\) is at least \(4{,}570{,}655\).

For a true \(z\mid e\), put \(L=z+e/z\). At \(p\mid H\), one has \(e\equiv-1475B=-59(5\sqrt B)^2\). With \(t=z/(5\sqrt B)\bmod p\), the exact forbidden residues are \(t^2=59\). An inert \(59\)-character gives no restriction at that prime. When \(59\) splits, either forbidden residue makes \(L\equiv0\pmod p\), and
\[
H\ell^2-L\ell+J\equiv0\pmod{H^2}
\]
has no solution. The replay below gives \(p=562190443\) with \(v_p(H)=1\), and a true prime divisor \(q=126736826507\) of \(e\) with \(q^2\equiv-e\pmod p\). On the very same progression, the true divisor \(5\) passes at \(p\). The fixed divisor \(q\) tests attainable residues. Ordinary short divisors grow on the scale of \(\sqrt A\).

### Ordinary-height countercontrol

Let \(W=\sqrt A\), and keep \(39/40<B/A<122/125\). Set \(z_0=37\cdot5^{b/2-2}\). Modulo \(H\), prescribe \(L\equiv z_0+e/z_0\), using the modular inverse of \(z_0\). Both \(z_0^2+e\) and \(z_0^2-e\) are units modulo \(H\): up to the unit \(B/625\), their residues are \(-920506\) and \(923244\), smaller in absolute value than every prime of \(H\). Consequently the quadratic in \(\ell\) has its unique lift modulo \(H^2\), and \(Z^2-LZ+e\) has a simple root that lifts modulo \(H^2\) as well.

On the refinement below, impose the finite local square conditions up to 169 and \(L\equiv11\pmod{173}\) by CRT. Their moduli are fixed and coprime to \(H\). Since \(H\asymp A^{28088000/56717661}\) and this exponent is less than \(1/2\), the CRT class contains an integer \(L\) in \(32W<L<33W\) for every sufficiently large balanced member. Then \(K=S_0+L^2\) lies in the ordinary window \(S_3<K\le729A+625B\). But the four remainders modulo 173 are \((121,92,131,151)\), and only \(131\) is a nonsquare. In particular, no true divisor \(z\mid e\) can give this \(L\), since that would make \(K-S_2=(z-e/z)^2\).

The lifted \(Z\) and \(\ell\) in this countercontrol are **residues**. The construction gives neither a true \(e\)-divisor nor an earlier divisor \(\ell\mid E=6(x^{11g}+y^{11g})\) in the short interval. Those are the remaining ordinary-height conditions.

### Inline replay

Take \(h,k\) in the classes shown modulo `T`. All modular checks are then fixed. The balanced strip is cofinal by irrationality of \(\log 3/\log 5\). The inline replay checks the original pinned exponent classes and the required modular data.

```python
from math import isqrt, lcm

def prime(p):
    return p > 1 and all(p % i for i in range(2, isqrt(p)+1))

def square(v, p):
    return v % p == 0 or pow(v, (p-1)//2, p) == 1

N, P = 623894271, 23894400218362914240
h, k = 645806464976090519188845783659560241603756891, 19848674835359031706
p, q, m = 562190443, 126736826507, 2662*1717
panel = [r for r in range(3, 170, 2) if prime(r)]
T = lcm(P, p*(p-1), q-1, 64, 172, *(r*r*(r-1) for r in panel))
assert (h % P, k % P) == (6540501655095556571, 19848674835359031706)

a, b = N*h+1, N*k-2
def AB(r):
    return pow(3, a, r), pow(5, b, r)
def e(r):
    A, B = AB(r)
    return (20*A+25*B) % r

assert prime(p) and prime(q)
u = pow(3, h, p)*pow(5, -k, p) % p
assert pow(u, m, p) == 1 and all(pow(u, m//j, p) != 1 for j in (2,11,17,101))
A, B = AB(p*p)
assert 2*(A+75*B) % (p*p) == 145824271*p
assert e(q) == (q*q+e(p)) % p == 0 and (25+e(p)) % p
assert max(abs(37**2+s*1475*625) for s in (-1,1)) < m

for r in (128, 173, *panel):
    A, B = AB(r)
    S = [(9**i*A+5**j*B) % r for i,j in enumerate((2,4,3,0))]
    if r == 128:
        assert [(S[0]+4-s) % r for s in S] == [4,100,16,4]
    elif r == 173:
        v = [(S[0]+121-s) % r for s in S]
        assert v == [121,92,131,151]
        assert [square(x,r) for x in v] == [True,True,False,True]
    else:
        assert any(S.count(K) <= 1 and all(square(K-s,r) for s in S)
                   for K in range(r))
from math import gcd,prod
assert gcd(37**2-1475*625,37**2+1475*625)==2
# The 173 test fails already at the base prime; force L=11 directly.
assert (11**2-4*e(173))%173==131
print("OK")
from fractions import Fraction as Q
M=21112080
assert h%M==12416651%M and k%M==10186%M
assert h%437==k%437==0
assert 2*(AB(11)[0]+75*AB(11)[1])%11==4
assert min(242*468741,2662*468741,2662*3939,2662*1717)+1==4570655
for b_ratio in [Q(39,40),Q(122,125)]:
    assert 729+b_ratio < 1+25*b_ratio+32**2
    assert 1+25*b_ratio+33**2 < 729+625*b_ratio- min(1,b_ratio)
print("pinned and ordinary endpoint checks")

```

For an odd panel prime where the witness hits one shift modulo \(r\), moving \(K\) to that shift plus \(r^2\) modulo \(r^3\) gives valuation exactly two and preserves the other unit-square conditions. This is why the finite replay certifies local squarehood over \(\mathbb Z_r\), including at the zero residues.

The compatible progression here preserves the original period \(21112080\) and \(19\cdot23\mid h,k\). It need not satisfy the additional \(59,467\) phase refinement of the separate coprime-trio count. For the height construction, CRT prescribes \(L\) only modulo \(H\) and a fixed modulus; both roots then lift to \(H^2\) for every integer \(L\) in that class. Therefore the CRT spacing is \(O(H)\), not \(O(H^2)\); this difference makes the ordinary-height construction possible. For each odd local prime choose a root of \(L^2=K-S_0\bmod r\). If \(K=S_0\bmod r\), set \(L=r\bmod r^2\); if a different remainder is zero, adjust the unit \(L\) by Hensel lifting to give that remainder valuation exactly two. At \(2\), \(L=2\bmod128\) suffices for the listed valuations and odd parts. This is a countercontrol to a finite family of tests, not an ordinary representation or exclusion of the full pinned family.