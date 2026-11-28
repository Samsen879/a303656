# Cubic construction of short primitive displacements for norm differences

Let \(\Delta=2\cdot3^c+4\cdot5^d\) be the difference between adjacent actual labels, with \(c\) odd and \(d\ge0\). Assume \(\Delta\) is an integer sum of two squares. Then every address in the exact displacement menu of [#97](https://github.com/Samsen879/a303656/pull/97) has a primitive representative, and the maximum length is \(O_\Delta(Q^{3/10})\), where \(Q=27\cdot2^k\), \(k\ge5\). The constant may depend on this fixed difference. In particular, the assumption does not hold for all odd-\(c\) labels.

Use the orientation \(D=-\Delta\), write \(A\) for the squared displacement length, and \(H=(A-\Delta)/2\). Thus the dyadic prescriptions are exact \(v_2(H)=r\) and the terminal divisibility \(2^{\lceil k/2\rceil}\mid H\); at each depth there are four unit-norm addresses modulo 9.

## Exact dyadic valuations with the four three-adic addresses

Let \(w_0\in\mathbb Z^2\), \(\|w_0\|^2=\Delta\), and let \(J\) rotate a vector by \(90^\circ\). Set
\[
P_z(t)=1-2t^2-4zt^3,\quad B_z(t)=2t+2zt^2-(1+z^2)t^3,\quad
w=P_z(t)w_0+B_z(t)Jw_0.
\]
Then \(A/\Delta=P_z^2+B_z^2\) and
\[
P_z^2+B_z^2-1=t^5(a_z+b_zt),\quad
a_z=4z(3-z^2),\quad b_z=1+18z^2+z^4.
\]
At \(z=1,28,-8,-80,-224\), \((v_2(a_z),v_2(b_z))\) equals \((3,2),(4,0),(5,0),(6,0),(7,0)\). The five values of \(v_2(a_z)\) cover all classes modulo 5. For \(r\ge43\), take the matching \(e=v_2(a_z)\), \(s=(r-e)/5\), \(t=2^s u\) with odd \(u\). Then \(v_2(b_z)+s>e\), so \(v_2(H)=r\), since \(v_2(\Delta)=1\). The restriction on \(r\) avoids the lower unstable cancellation layers. As each \(z=1\bmod9\), the expression \(A/\Delta\) as \(t\) runs through the six unit classes modulo 9 runs through all six units. There is an odd \(u\bmod18\) giving any requested address. For a terminal address choose \(r=\lceil k/2\rceil\). The finitely many shallow addresses are supplied by the elementary CRT construction in #96, with constant length. As long as the additional constraints on \(u\) have fixed modulus, \(|t|=O_\Delta(2^s)\) and \(\|w\|=O_\Delta(2^{3r/5})\), hence the claimed exponent.

## Genuine primitivity at every prime, even with a nonprimitive base

Let \(g_0=\gcd(w_0)\), \(w'_0=w_0/g_0\). As \(v_2(\Delta)=1\) and \(3\nmid\Delta\), every \(p\mid g_0\) is at least 5. For each such prime let \(e_p=v_p(g_0)\), \(s_p=e_p\bmod2\), \(r_p=(e_p+3s_p)/2\). Replace each chosen \(z\) by a rational number with \(v_p(z)=-r_p\) at these primes, no other denominator primes, and the original residues modulo \(2^9\) and 9. These constraints are compatible: choose denominator \(\prod_{p\mid g_0}p^{r_p}\), then choose numerator by CRT so it is a unit at its denominator primes. They preserve the dyadic types and unit address map above.

Also require that the resultant of \(P_z(t)\) and \(B_z(t)/t\) is nonzero. This excludes only finitely many rational \(z\), since the resultant as a polynomial in \(z\) is nonzero (the replay gives nonzero value at \(z=1\)). At each \(p\mid g_0\), enforce \(v_p(t)=s_p\) by a fixed condition on \(u\) modulo \(p^{s_p+1}\). Now \(-z^2t^3\) is the unique lowest-valuation term of \(B_z\), of valuation \(-e_p\), while \(v_p(P_z)>-e_p\). Thus \(g_0 B_z\) is a unit and \(g_0 P_z\) is divisible by \(p\); the output is integral and nonzero as a coordinate pair modulo \(p\), using the primitive vector \(Jw'_0\).

At a prime not dividing \(6g_0\), possible common divisors of both coordinates belong to a finite set: primes dividing \(\Delta\) or the numerator of the nonzero resultant. Indeed for \(p\nmid\Delta\) the matrix with columns \(w_0,Jw_0\) is invertible, so a common divisor would give \(P_z=B_z=0\bmod p\). If \(t=0\bmod p\) that is impossible; otherwise it gives a common root with \(B_z/t\). At every such bad prime not dividing \(g_0\), take \(t=0\bmod p\), so the output is \(w_0\) there, which is a primitive pair modulo \(p\). All extra congruences on \(u\) have fixed moduli independent of \(s\) and are coprime to 18. The resulting vector is integral and primitive, rather than just having a primitive direction. At 2 and 3 this follows from the required norm addresses. The argument gives no constant uniform as \(\Delta\) varies.

## Exact controls

For \(\Delta=2554=23^2+45^2\), the five integer parameters suffice and the replay checks that each tested deep address has a primitive choice among 64 candidates; the verified root-count bound is uniform in the depth. The near example \(\Delta=312554=2\cdot3^3+4\cdot5^7\) has \(v_{11}(\Delta)=1\) and is outside the theorem. For \(\Delta=490=7^2+21^2\), any base contains 7, but the rational parameter \(z=4657/49\) and \(t=1792\) give a genuinely primitive integer displacement for the exact depth 43. The two original labels are used to check a true common target on its line. Coverage of an externally specified integer and optimality of the exponent are not asserted.

```python
from itertools import permutations
from math import gcd, isqrt, prod

Z = (1,28,-8,-80,-224)
F = ((5,), (424635577,), (31,4073),
     (258333971209,), (5,1097,4597648361))

def v2(n):
    assert n
    return (abs(n)&-abs(n)).bit_length()-1

def pq(z,t):
    return 1-2*t*t-4*z*t**3, 2*t+2*z*t*t-(1+z*z)*t**3

def w(z,t,x=23,y=45):
    p,q = pq(z,t)
    return p*x-q*y,p*y+q*x

def A(z,t):
    return sum(x*x for x in w(z,t))

def sylvester(z):
    p,b = [-4*z,-2,0,1],[-(1+z*z),2*z,2]
    M = ([[0]*j+p+[0]*(1-j) for j in range(2)]
         + [[0]*j+b+[0]*(2-j) for j in range(3)])
    return sum((-1)**sum(pi[i]>pi[j] for i in range(5)
                         for j in range(i+1,5))
               *prod(M[i][pi[i]] for i in range(5))
               for pi in permutations(range(5)))

assert tuple(abs(sylvester(z)) for z in Z) == (
    200,424635577,126263,258333971209,126090506300425)
for p in {1277}|set(sum(F,())):
    assert all(p%d for d in range(2,isqrt(p)+1))
assert tuple(prod(f)*c for f,c in zip(F,(40,1,1,1,5))) == (
    200,424635577,126263,258333971209,126090506300425)
assert [sum(3*((64+p-1)//p) for p in set(f+(1277,)))
        for f in F] == [42,6,15,6,48]

for z,e in zip(Z,range(3,8)):
    a,b = 4*z*(3-z*z),1+18*z*z+z**4
    f = 2 if z==1 else 0
    assert (v2(a),v2(b)) == (e,f)
    assert tuple(A(z,t)%9 for t in (1,2,4,5,7,8)) == (5,4,8,7,2,1)
    for s in range(11):
        for u in range(1,18,2):
            t=2**s*u
            p,q=pq(z,t)
            assert p*p+q*q-1 == t**5*(a+b*t)
            v=5*s+min(e,f+s)
            if e==f+s:
                v+=v2(a//2**e+(b//2**f)*u)
            assert v2((A(z,t)-2554)//2)==v

for r in range(43,91):
    e=3+(r-3)%5
    z,s=Z[e-3],(r-e)//5
    for adr in (7,1,2,5):
        h=next(h for h in range(1,18,2) if h%3 and A(z,2**s*h)%9==adr)
        t=next(2**s*(h+18*j) for j in range(64)
               if gcd(*w(z,2**s*(h+18*j)))==1)
        assert v2((A(z,t)-2554)//2)==r and A(z,t)%9==adr

assert gcd(*w(1,28))==5
assert w(1,1792)==(-11946063337,-1300677443027)
assert w(1,1)==(-205,-179)
assert 67056==3206+43**2+249**2==652+248**2+70**2
assert w(1,1,7,21)==(-77,-91)
assert 7704==734+9**2+83**2==244+86**2+8**2
print("PASS")

from fractions import Fraction
r, t = Fraction(4657,49), 1792
p, q = pq(r,t)
a, b = 7*p-21*q, 21*p+7*q
assert a.denominator == b.denominator == 1
a,b = int(a),int(b)
assert (a,b) == (1076369325218311,-409835834940907)
assert gcd(a,b) == 1
S = a*a+b*b
H = (S-490)//2
assert S%9 == 8 and v2(H)==43
y=H*pow(b,-1,a)%a
x=(H-b*y)//a
assert a*x+b*y==H
assert 734+x*x+y*y==244+(x-a)**2+(y-b)**2
print("PASS rational nonprimitive-base repair")
assert 312554 == 2*3**3+4*5**7 and 312554%11==0 and 312554%121!=0
```
