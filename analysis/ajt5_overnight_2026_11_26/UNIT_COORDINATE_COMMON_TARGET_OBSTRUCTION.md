# An actual common-target obstruction to unit-coordinate first chords

For A=9^L,B=25^L, set H=27A+5B,D=9A+2B,J=3A+125B,E=A+50B. A first chord with one displacement coordinate ±1 is equivalent by signed permutation to P=(au+D−e,u), Q=(au+D−e+1,a−u) with e=(a²+1)/2, a odd. The prescribed second-label rotation with even slope m has upper endpoint divisible by the Gaussian factor m+i, so a shared target n satisfies n=J−2E=A+25B modulo p=m²+1. The first lower norm then entails
```
(2e u+a(D−e))² = 4e(10B−13A)−(D−e)² mod p.
```
This is an actual common-target restriction, not an independent angle condition.

Take T=26 mod 42 and L=T+3. Choose b=0 mod 10, b=±12 mod 29, and b−59/20<sqrt(128) K<b−57/20. At sufficiently large ordinary heights in the constructed family, the strict q windows restrict the first |a| to b−1,b+1 and the second |m| to b−2,b,b+2. Indeed for the first unit displacement, 2S−(a²+1)q=2D(2P_x−D); dividing by q makes the right side o(1) since S is exponentially larger than D². For the second rotation, the triangle inequality gives |sqrt(q)−sqrt(2R/p)|≤1, again making 2S/q−p=o(1) in its strict window. Endpoint equality with 128K² or 128K(K+1) is excluded by the parity class of the slope square plus one. The displayed band then gives exactly the stated possibilities.

For outer m, p is divisible by 5 and the displayed congruence has nonsquare right side 2. For middle m, p is divisible by 29, A=9 and B=25 modulo 29, and the two possible right sides are 2 and 10, both nonsquares. With K=90L the slope band occurs infinitely often by irrational rotation modulo 290. For each such height the three second rotations can share t: the three p are coprime except for the outer pair sharing gcd 5, and 5 divides (E+1)/2, making the residues t=−m(E+1)/2 compatible. For each prime dividing E there are at most three forbidden residues of the common parameter to preserve a primitive displacement; these primes are all ≥5. If that prime divides one p, the other two parameter values are automatically units because the slope differences are ±2 or ±4 and (E+1)/2 is a unit there. The CRT modulus is at most a constant times E lcm(p_i), far below the ordinary t-window of scale 2^(K/2). Thus this construction can have three genuine second critical representations while none of the paired first unit-coordinate directions is possible.

The exact finite replay gives K=5684 with two 5685-bit targets, each supplying all three genuine second chords. One target has both first endpoint remainders units modulo 3 and 7 and still meets this obstruction; the other has v_7=1 at the first lower norm. This excludes the specified first directions only. Longer primitive directions and unrestricted double-label growth remain open.

```python
from math import gcd, isqrt, lcm

def crt(r,P,s,M):
    d = gcd(P,M)
    assert (s-r)%d == 0
    return r+P*((s-r)//d*pow(P//d,-1,M//d)%(M//d)), lcm(P,M)

T,K,b = 68,5684,64310
L = T+3
A,B = 9**L,25**L
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
ms = (b-2,b,b+2)
assert (20*b-59)**2 < 400*128*K*K < (20*b-57)**2
lo,hi = isqrt(128*K*K-1),isqrt(128*K*(K+1)-1)+1
assert [z for z in range(lo,hi+1)
        if 128*K*K < z*z+1 < 128*K*(K+1)] == list(range(b-2,b+3))

r,P = 0,1
for m in ms:
    p,ell = m*m+1, 29 if m==b else 5
    assert p%ell==0
    for a in (b-1,b+1):
        e = (a*a+1)//2
        assert all(((a*u+D-e)**2+u*u-20*B+26*A)%ell
                   for u in range(ell))
    r,P = crt(r,P,-m*(c+1),p)

for bad in (False,True):
    t49 = (2 if (2*(4+c*c)+J-H)%49 else 9) if bad else 0
    s,M = crt(r,P,t49+49*((1-t49)%3),147)
    X = isqrt(1<<K)
    lo = (4*X+4)//5
    t = lo+(s-lo)%M
    S,n = 2*(t*t+c*c), 2*(t*t+c*c)+J
    assert 4*X <= 5*t and 6*t <= 5*X
    assert 25**(16*(L+1)) <= n <= 9**(32*L)
    assert all(2**K <= z < 2**(K+1) for z in (S,n-H,n-H+2*D))
    if bad:
        assert (n-H)%49 == 28
    else:
        assert gcd((n-H)*(n-H+2*D),21)==1

    U,qs = (t-c,t+c),set()
    for m in ms:
        v,rem = divmod(t+m*(c+1),m*m+1)
        assert rem==0
        f,g = (m*m-1)*v-m*(c+1),2*m*v-c-1
        V = (f-g,f+g)
        x,y = V[0]-U[0],V[1]-U[1]
        q,h = (x*x+y*y)//2,x*U[1]-y*U[0]
        assert sum(z*z for z in U)==S and sum(z*z for z in V)==S+2*E
        assert x%2 and y%2 and gcd(x,y)==1 and h%2==0
        assert 2*q*S==(E-q)**2+h*h and 64*K*K*q<S<64*K*(K+1)*q
        qs.add(q)
    assert len(qs)==3
```
