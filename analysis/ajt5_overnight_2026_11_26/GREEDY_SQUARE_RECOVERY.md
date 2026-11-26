# Greedy square-coordinate recovery and its sparse range

Write \(n=a^2+b^2+r\), where \(r=3^c+5^d\) and all parameters are nonnegative integers. The two greedy integer square roots give exactly \(a\) and \(b\) if and only if
\[
 b^2+r\le2a,\qquad r\le2b.
\]
Indeed the first remainder must be strictly below \((a+1)^2-a^2\), and the same comparison at \(b\) gives the second test. If just the first test holds, the representation can still be recovered by enumerating the power-sums up to \(n-a^2\) and testing whether the difference is a square. The greedy first-square route can recover a representation for at most \(O(X^{3/4}(\log X)^2)\) targets \(n\le X\): sum the \(O(1+\sqrt a)\) possible second coordinates for each \(a\le\sqrt X\), and multiply by the \(O((\log X)^2)\) possible power-sums. Thus it cannot by itself recover a positive-density set.

## Prescribing new square factors within a certificate class

Fix classes \((a_0,b_0)\bmod Q\) with \(\gcd(a_0,b_0,Q)=1\), and fix \(r=3^c+5^d\). Let \(N\) be large and \(D\) coprime to \(Q\), with \(D\le N^{1/16}\), \(r\le2DQ\), and \(Q=N^{o(1)}\). Choose \(y\in[Q,2Q)\) congruent to \(D^{-1}b_0\bmod Q\) and put \(b=Dy\). Choose \(x\equiv D^{-1}a_0\bmod Q\), and require \(x\equiv1\) modulo every prime divisor of \(y\) not dividing \(Q\). CRT gives one class of modulus at most \(Qy\); the other prime factors of \(y\) already cannot divide \(x\). Taking the first resulting \(a=Dx\) at least \(\sqrt N\) gives \(a=\sqrt N+O(DQ^2)\) and \(\gcd(a,b)=D\). Both greedy inequalities hold for large \(N\); the target \(n=a^2+b^2+r=N+o(N)\) lies in the original class modulo \(Q\). If \(D=pq\) with distinct inert primes, their valuations in \(n-r\) are exactly two: after removing \(D^2\), coprime coordinates cannot both vanish at either inert prime. This construction chooses targets, rather than guaranteeing these factors for a supplied arbitrary \(n\).

## Small exact controls

The least \(n\) with a nonempty greedy first-square power-sum menu and no success in that menu is \(80\). The first remainder is \(16\); none of the offsets \(2,4,6,8,10,14\) leaves a square. Nevertheless \(80=7^2+5^2+3^0+5^1\).

For a different menu, require that the positive residual have odd part \(1\bmod4\) and be divisible by squares of at least two distinct primes greater than five. The least nonempty menu with all entries failing the square-sum criterion occurs at \(n=124511\). Any failed residual in this menu is at least \(7^2\,11^2\cdot3\cdot7\): two distinct square factors cost at least \(7^2\,11^2\), and among the remaining factors the failure and the odd-part condition force two distinct inert primes of odd valuation, costing at least \(3\cdot7\). At \(n=124511\), the offset \(2\) attains the bound, so all other offsets leave less than the minimum failed residual; direct enumeration shows they are not in this menu. The failed residual \(124509=3\cdot7^3\cdot11^2\) is not a claim of exact even valuation at both selected primes. The same target has the true representation \(52^2+349^2+3^0+5^1\).

```python
from math import isqrt

def offsets(limit):
    a = 1
    while a+1 <= limit:
        b = 1
        while a+b <= limit:
            yield a+b
            b *= 5
        a *= 3

def factors(n):
    f = {}
    for d in range(2,isqrt(n)+1):
        while n%d == 0:
            f[d] = f.get(d,0)+1
            n //= d
    if n > 1:
        f[n] = f.get(n,0)+1
    return f

def reject_greedy(n):
    r = n-isqrt(n)**2
    choices = [r-s for s in offsets(r)]
    return choices and all(isqrt(v)**2 != v for v in choices)

assert [n for n in range(2,81) if reject_greedy(n)] == [80]
assert 80 == 7**2+5**2+1+5
n = 124511
menu = []
for s in offsets(n-1):
    f = factors(n-s)
    oddpart = (n-s)//2**f.get(2,0)
    if oddpart%4 == 1 and sum(p>5 and e>=2 for p,e in f.items()) >= 2:
        menu.append((s,f))
assert menu == [(2,{3:1,7:3,11:2})] and n == 52**2+349**2+1+5
```
