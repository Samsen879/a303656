# Opposed order tests for neutral-depth cofactors

For an eligible odd prime \(q\equiv687\bmod1372\), real multiplicative orders divide \(q-1\) and the order of \((2+i)/(2-i)\) divides \(q+1\). To force the full \(\ell\)-part of an exponent \(E\) into an order, test the \(E\)-th power for identity and the \(E/\ell\)-th power for nonidentity. For the Gaussian ratio the test is equivalent to vanishing of the imaginary part of \((2+i)^E\); denominators are units at eligible primes. One may verify the high and low tests simultaneously on a composite component by congruence and gcd. This gives opposite signed constraints \(q\equiv+1\) and \(q\equiv-1\), which can conflict or narrow a complementary divisor search, without requiring a verified factorization of that component. These examples supplement the [earlier composite-support tests](https://github.com/Samsen879/a303656/commit/3ba8922902df390ac6a5a74dab22089a1ba1831a).

In the first example below an eligible divisor would force both \(3\mid q-1\) and \(3\mid q+1\); in the second it would force \(16\mid q-1\), impossible for an inert allowed prime. The last example tightens the modulus in the complementary-divisor test. There is no claim of exhaustive neutral-chart closure.

~~~python
from math import gcd

def gp(e,m):
    def mul(a,b):
        x,y=a
        u,v=b
        return (x*u-y*v)%m,(x*v+y*u)%m
    r,z=(1,0),(2,1)
    while e:
        if e&1:
            r=mul(r,z)
        z=mul(z,z)
        e//=2
    return r

R=26052694331581
E=R-1
assert 534743861*R==13931518356322438174241
assert E%3==0 and pow(3,E,R)==1 and gp(E,R)[1]==0
assert pow(3,E//3,R)==1172482034703 and gp(E//3,R)[1]==13548824463861
assert gcd(1172482034702,R)==gcd(13548824463861,R)==1

R=40194389731217
E=R-1
assert E%32==16 and pow(3,E,R)==1 and pow(3,E//2,R)==R-1

R=3575252473051289311
E=R+1
assert gp(E,R)==(5,0)
assert E%23==0 and E%(43**2)==0
for ell,want in [(23,1210463685363015221),(43,179010966536215489)]:
    assert gp(E//ell,R)[1]==want and gcd(want,R)==1
m,q0=58347044,40825919
assert q0%1372==687 and q0%(23*43**2)==23*43**2-1
r0=R*pow(q0,-1,m)%m or m
out=[r for r in range(r0,R//(4*10**9)+1,m)]
assert len(out)==16 and [r for r in out if R%r==0]==[1]
~~~
