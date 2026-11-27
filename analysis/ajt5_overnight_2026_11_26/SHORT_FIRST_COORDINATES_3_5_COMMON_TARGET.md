# Excluding short first displacements 3 and 5 at a genuine shared target

For first displacement (d,a−2u) and start (x,u), the true gap 2D gives dx=au+D−e with e=(a²+d²)/2. Therefore a(a−2u)=2D modulo d, and for any prime not dividing d a necessary first-norm condition is that W=2e(n−H)−(D−e)² is a square. On the same n, a second-rotation factor m+i forces n=J−2E modulo every prime dividing m²+1, giving W=4e(10B−13A)−(D−e)² on that prime.

At the exact K=5684 target verified below, all three second rotations give genuine primitive critical chords. The two first endpoint norms are 1,3 modulo 5. Both coordinates of a displacement with one coordinate divisible by 5 are impossible: the starting pair needs squared residues 0,1 and the upper pair needs 4,4. This rules out coordinate ±5 without using its angle.

For coordinate ±3, the identity 2d² S−(a²+d²)q=2D(2dx−D) makes the strict critical window restrict the other slope to |a|=3b+j with j∈{−7,−5,−3,−1,1,3,5,7} in the specified narrow sqrt(128)K band. The residues use modulo 3 for j=±3, modulo 5 for ±5, modulo 29 for −7,−1,1, and modulo 53 for j=7. The final case really survives the first two split primes and fails only at the extra common-target read from (b+2)²+1. The same residue table repeats under L=71 mod 546 and b=2830 mod 15370, compatible with infinitely many narrow angle windows by irrational rotation; the second constructions continue with the same CRT primitivity argument for these progressions.

The negative and positive controls are deliberately separate: a second target n' at the same height has an actual first primitive coordinate-3 chord. It agrees with n modulo 3·5·29 but differs by 16 modulo 53. This shows that the extra prime is not cosmetic. Neither example settles unrestricted first directions or arbitrary n.

```python
from math import gcd, isqrt, lcm

T,K,b = 68,5684,64310
L = T+3
A,B = 9**L,25**L
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
ms = (b-2,b,b+2)

def crt(r,P,s,M):
    d = gcd(P,M)
    assert (s-r)%d == 0
    return r+P*((s-r)//d*pow(P//d,-1,M//d)%(M//d)),lcm(P,M)

r,M = 7,21
for m in ms:
    r,M = crt(r,M,-m*(c+1),m*m+1)
X = isqrt(1<<K)
lo = (4*X+4)//5
t = lo+(r-lo)%M
n = 2*(t*t+c*c)+J

def check(n,P,Q,H,D):
    S = n-H
    assert 25**(16*(L+1)) <= n <= 9**(32*L)
    assert 2**K <= S < 2**(K+1)
    assert sum(z*z for z in P)==S and sum(z*z for z in Q)==S+2*D
    d,w = Q[0]-P[0],Q[1]-P[1]
    q,h = (d*d+w*w)//2,d*P[1]-w*P[0]
    assert d%2 and w%2 and gcd(d,w)==1 and h%2==0
    assert 2*q*S==(D-q)**2+h*h and 64*K*K*q<S<64*K*(K+1)*q
    return q

qs = set()
for m in ms:
    v,rem = divmod(t+m*(c+1),m*m+1)
    assert rem==0
    f,g = (m*m-1)*v-m*(c+1),2*m*v-c-1
    qs.add(check(n,(t-c,t+c),(f-g,f+g),J,E))
assert len(qs)==3 and n.bit_length()==5685
assert ((n-H)%5,(n-H+2*D)%5)==(1,3)

lo,hi = 128*9*K*K,128*9*K*(K+1)
aa = [a for a in range(isqrt(lo-9),isqrt(hi-9)+2)
      if a%2 and lo<a*a+9<hi]
assert [a-3*b for a in aa]==list(range(-7,8,2))
for a,p in zip(aa,(29,5,3,29,29,3,5,53)):
    if p==3:
        assert a%3==0 and D%3
    else:
        e = (a*a+9)//2
        W = (2*e*(n-H)-(D-e)**2)%p
        assert (n-J+2*E)%p==0 and W not in {x*x%p for x in range(p)}

a = 3*b+7
C = D-(a*a+9)//2
goal = (27*X//8-C)//a
u = goal+(174-goal)%1305
x,rem = divmod(a*u+C,3)
assert rem==0
n1 = x*x+u*u+H
assert (n1-n)%435==0 and (n1-n)%53==16
check(n1,(x,u),(x+3,a-u),H,D)
```
