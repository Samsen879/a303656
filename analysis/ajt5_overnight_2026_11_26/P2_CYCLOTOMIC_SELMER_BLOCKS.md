# Independent necessary square-class equations from P2 cyclotomic blocks

Take the [second four-square pattern](FOURTH_SQUARE_COMPLETE_LOCAL_COVER.md), with \(A=3^a,B=5^b\), \(a,b\) positive even, and write
\[
 d=(S_1-S_0)/4=2(A+75B),\quad e=(S_2-S_0)/4=5(4A+5B).
\]
The first three translated square conditions give a rational point on \(E:y^2=x(x-d)(x-e)\) (take \(x=(K-S_0)/4\) and use the rational half-roots). Below we obtain arbitrarily many independent *necessary equations* for the local 2-descent classes on this curve along a cofinal set of even, balanced, prime-locally admissible exponent pairs. We do not claim rank zero or that the four-square pattern fails at all these pairs.

## One isolated collision prime

Write \((s_0,s_d,s_e)\) for squarefree Kummer representatives with product a square, coming at each place from the local map \(x\mapsto(x,x-d,x-e)\). At the roots use the usual continuous extension, or the root formulas in [Skorobogatov–Swinnerton-Dyer, §2](https://www.ma.imperial.ac.uk/~anskor/SSD.PDF).

Suppose \(p\) is odd, \(p\mid d\), \(p\nmid e\); put \(h=v_p(d)\) and \(\chi=(\frac{-e}{p})\). Then \(p\nmid s_e\), and
\[
 \left(\frac{s_e}{p}\right)^h=\chi^{v_p(s_0)}.
\]
Indeed, for \(v_p(x)\le0\), \(x(x-d)\) is a local square and hence \(x-e\) is a square. Here the asserted right side is 1 as well: when \(v_p(x)<0\), the product of the three factors has valuation \(3v_p(x)\), forcing \(v_p(x)\) even. For \(v_p(x)>0\), \(x-e\) is a unit of character \(\chi\). If \(\chi=-1\), \(v_p(x)<h\) is impossible since \(x(x-d)=x^2(1-d/x)\) would be a square. Then the minimum of \(v_p(x)\) and \(v_p(x-d)\) is \(h\) and they have the same parity because their product, times the unit \(x-e\), is a square. Thus \(v_p(s_0)\equiv h\bmod2\). When \(\chi=1\) both sides are already 1. The identities extend at the roots by local continuity.

## A factorization-free rank certificate

For each \(r\ge1\), put \(M=11^r\) and impose the independent congruences
\[
 (a,b)=(334,228)\pmod{720},\qquad (a,b)=(1,-2)\pmod{29M}.
\]
The first retains the all-prime separate local cover. As \(\log3/\log5\) is irrational, each pair of progressions has arbitrarily large members with \(19A<20B<22A\): modulo the \(b\)-step times \(\log5\), the values \(a\log3\) give a dense irrational rotation, with infinitely many hits in the allowed interval.

Set \(U=3^{(a-1)/M}\), \(V=5^{(b+2)/M}\), so \(d=6(U^M+V^M)\). Let \(F_j\) for \(1\le j\le r\) be the quotient of \(U^{11^j}+V^{11^j}\) by \(U^{11^{j-1}}+V^{11^{j-1}}\). It is the degree ten alternating polynomial in \(U^{11^{j-1}},V^{11^{j-1}}\). Remove the factor 11 from \(F_j\) if present, to give \(C_j\); lifting the exponent shows this factor has valuation exactly one and occurs precisely when \(11\mid U+V\).

The \(F_j\) are prime to \(2,3,5,59\): they are odd, either variable zero at 3 or 5 leaves a unit monomial, and \(U=V=1\bmod59\) by the exponents being multiples of 29 and the orders of 3 and 5 dividing 29. At every \(p\mid C_j\), \(U/V\) has exact order \(2\cdot11^j\) modulo \(p\). In fact the numerator forces its \(11^j\)-th power to be \(-1\), and a smaller such order would make the quotient polynomial equal to 11 times a unit. The blocks are thus pairwise coprime, with \(v_p(C_j)=v_p(d)\). At these primes \(A=-75B\bmod p\), so \(-e=25\cdot59B\bmod p\) is nonzero, with character \((\frac{59}{p})\) since \(b\) is even. There are no collisions with \(e\) in the blocks.

Also \(U=-1,\ V=1\bmod4\), so \(F_j=11\bmod4\). Reciprocity with \(F_j=1\bmod59\) gives \((\frac{59}{F_j})=-1\); stripping 11 preserves this since \((\frac{59}{11})=1\). Multiplying the collision-prime identities with the exponents already incorporated on the left gives
\[
 \left(\frac{s_e}{C_j}\right)=
 \left(\frac{59}{\gcd(s_0,C_j)}\right).
\]
Each is a linear sign condition on the ambient bad-prime square classes with \(s_e\) a unit along the blocks. The test triples \(([C_i],[C_i],1)\) are in that ambient space. The signs for violating the equations on these triples are -1 on the diagonal and +1 off the diagonal; hence the \(r\) equations are independent there. This argument does not require that the test triples be in the actual Selmer group. The ambient support can grow, so the rank certificate does not bound the remaining dimension independently of \(r\).

## Four blocks, without expanding the powers

The example below verifies the progression, balance, and the four block signs. The identity and reciprocity above certify the rank; the finite example does not assert an actual global point.

~~~python
from fractions import Fraction as F

a,b = 70114852900030281454, 47860832915034320388
r = 4
M = 11**r
assert (a%720,b%720)==(334,228)
assert (a-1)%(29*M)==(b+2)%(29*M)==0

def ln_interval(k,n=150):
    t=F(k-1,k+1)
    lo=2*sum(t**(2*j+1)/(2*j+1) for j in range(n))
    return lo,lo+2*t**(2*n+1)/((2*n+1)*(1-t*t))
l3,u3=ln_interval(3)
l5,u5=ln_interval(5)
assert -F(1,25)<b*l5-a*u3<=b*u5-a*l3<F(1,25)
# exp(-1/25)>1-1/25>19/20 and exp(1/25)<25/24<22/20.

i,j=(a-1)//M,(b+2)//M
assert (pow(3,i,4),pow(5,j,4))==(3,1)
assert pow(3,i,59)==pow(5,j,59)==1
assert (pow(3,i,11)+pow(5,j,11))%11!=0
assert pow(59,5,11)==1
for h in range(r):
    for m,expected in [(4,3),(59,1)]:
        u,v=pow(3,i*11**h,m),pow(5,j*11**h,m)
        assert sum((-1)**k*u**(10-k)*v**k for k in range(11))%m==expected
~~~
