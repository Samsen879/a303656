# Grid size and complementary divisors in the neutral chart

For an eligible prime \(q\mid R\), write \(q-1=7^v s\), \(7\nmid s\), and take \(L\) to be the 7-free part of \(\operatorname{lcm}(1,\ldots,20000)\). A collision-free grid of 5329 words from [mixed-word masking](https://github.com/Samsen879/a303656/commit/aa4159bd639bd2866c341d5ed96bd9449f8b092f) forces \(s/\gcd(s,L)\ge5329\). Since \(s=2\bmod4\), the minimum allowed \(s\) under this particular test is 40022; the short check below is exact. Thus with an independently established lower cutoff \(Q\), every eligible prime obeys \(q\ge\max(Q+1,1+40022\cdot7^v)\).

For \(Z=7^v\), exact depth means \(q=1+jZ\bmod7Z\) for some \(1\le j\le6\), and \(q=3\bmod4\). Consequently the complement \(R/q\) is congruent to \(R(1-jZ)\bmod7Z\) and \(3R\bmod4\). One may test joint progression intervals and exact divisions without assuming that a congruence-compatible integer is a factor. The replay gives an exact weighted-square factor extraction on one actual residual and a second prime that passes all four grid tests and has both projected orders 343 but fails the actual same-root phase tag. This demonstrates why the grid and size constraints do not by themselves settle the chart. No aggregate residual partition is asserted here.

~~~python
from math import gcd, isqrt, lcm

R, X, Y = 172129585633726019666179, 3319080477541, 1317511035
assert X*X - Y*Y == 64*R and X % 686 == 17
assert gcd(X+Y, R) == 103762437143

R, q, x = 15386889653148214699904869, 45574318763, 13129993496012691450693331
assert R % q == 0 and all(q%d for d in range(2, isqrt(q)+1))
assert q % 1372 == 687 and pow(x,343,q) == 1 and pow(x,49,q) != 1
assert (1 + pow(x,40,q) - x - pow(x,86,q)) % q == 0
s = (q-1)//343
assert q-1 == 343*s and s%7 and s%3
assert [pow(b,s,q) for b in (3,5)] == [pow(x,s*j,q) for j in (60,120)]
assert (60%49, 120*pow(60,-1,343)%343) not in {(3,200),(15,255)}
for L in (R-1, R+1, lcm(*range(1,4001)), lcm(*range(1,20001))):
    while L%7 == 0:
        L //= 7
    A, B = ([pow(b,343*L*i,q) for i in range(73)] for b in (3,5))
    assert len({a*b % q for a in A for b in B}) == 5329

L=lcm(*range(1,20001))
while L%7==0:
    L//=7
assert next(s for s in range(2,40023,4) if s%7 and s//gcd(s,L)>=5329)==40022
~~~
