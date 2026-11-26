# The fourth square rules out an exponent class modulo 30

For permutation \((2,4,3,0)\) in [the shared-height model](ALL_DISTINCT_SHARED_MATCHING.md), there is no \(K\) making all four residuals square if \(b-3a\equiv8\bmod30\). This excludes one genuine exponent class at all heights, not the permutation in full.

Let \(A=3^a,B=5^b\), and denote the half roots at offsets \(3,2,4,0\) by \(h,R,Y,J\). The first three require \(a,b\) even, as shown in [the three-square reduction](THREE_SQUARES_PRECLUDE_AUXILIARY_NORM.md). The last root is also even before division by two, since its raw residual differs from that at offset 3 by \(4\bmod8\). The exact differences give
\[
 R^2=h^2+20A+25B,\quad Y^2=h^2+18A-125B,\quad J^2=h^2-162A+31B .
\]
Modulo 61, \(3=5^3\), \(5\) has order 30, and \(5^{-8}=16\). Therefore \(A/B=16\bmod61\). Dividing by the unit square \(B\), the four conditions are that \(z,z+40,z+41,z+1\) are squares modulo 61, with \(z=h^2/B\). The first three allow exactly \(1,5,16,20,25,34,36\); the last removes every one.

There are arbitrarily high balanced exponent pairs of the forbidden class still passing all eight old local square tests. Take \((a,b)\equiv(42,14)\bmod17075520\) and \(K\equiv264731101406030\bmod20206524571833600\). The irrationality of \(\log3/\log5\) permits unbounded pairs of these exponent classes with \(19A<20B<22A\). In that band the maximum shift is \(729A+B\), and the admissible interval \(729A+B<K<729A+625B-\min(A,B)\) grows unbounded in length. The following verifies the fixed congruences and genuine local squares (using the unit part after valuation), including the failure at 61. It does not claim the three surviving local squares are integer squares in these examples.

~~~python
from math import prod
Q = {i*i%61 for i in range(61)}
z = sorted(i for i in Q if (i+40)%61 in Q and (i+41)%61 in Q)
assert z == [1,5,16,20,25,34,36] and all((i+1)%61 not in Q for i in z)
assert pow(5,3,61)==3 and pow(5,22,61)==16 and pow(5,30,61)==1
assert all(pow(5,30//p,61)!=1 for p in (2,3,5))
a,b,T,K = 42,14,17075520,264731101406030
S = [3**(a+2*i)+5**(b+d) for i,d in enumerate((2,4,3,0))]
pq = ((2,256),(3,27),(5,25),(7,343),(11,1331),(13,13),(17,17),(19,19),(61,61))
assert prod(q for p,q in pq)==20206524571833600
assert (b-3*a)%30 == 8 and T%30 == 0
def local_square(r,p):
    if not r: return False
    v=0
    while r%p==0:
        v+=1
        r//=p
    return v%2==0 and (r%8==1 if p==2 else pow(r,(p-1)//2,p)==1)
for p,q in pq:
    assert pow(3,a+T,q)==pow(3,a,q) and pow(5,b+T,q)==pow(5,b,q)
    assert all(local_square((K-s)%q,p) for s in (S[:3] if p==61 else S))
assert not local_square((K-S[3])%61,61)
~~~
