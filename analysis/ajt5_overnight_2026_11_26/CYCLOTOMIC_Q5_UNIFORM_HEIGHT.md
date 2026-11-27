# Uniform height lower bounds for the smallest positive-q branch

Use CYCLOTOMIC_TWO_QUOTIENT_HEIGHT.md with $q=5$, $U=5^{73^k}$, $k\ge1$, $x=365U^5$, $A=5U-131770$, and $F=x^2-4x+A$. The gcd $g=\gcd(F,A)$ is **exactly 15** for every $k$.

To see this, put $C=26354$. Both $F$ and $A=5(U-C)$ have valuation exactly one at 5. Away from 5, $\gcd(U-C,x)=1$: $U$ is a power of 5, and at 73 one has $U\equiv5$ and $C\equiv1$. Thus $\gcd(F,A)=5\gcd(U-C,365C^5-4)$ by reducing $x-4$ modulo $U-C$. The exact factorization is
$$
 365C^5-4=2^2\cdot3\cdot19^2\cdot415903109\cdot2575401579137.
$$
Here $U-C$ is odd, is divisible by 3, and is not divisible by 19 since $U\equiv5$ and $C\equiv1\bmod19$ (the order of 5 divides 9 there and $73^k\equiv1\bmod9$). For each of the two large prime factors, $5$ and $C$ have different quadratic characters; the odd exponent $73^k$ therefore prevents equality of $U$ and $C$ modulo that prime.

The bound $|n|^3\ge V^2/(8000\cdot366gAb)$ for an actual anchor $t=n/b$, together with $b^2\mid A$ and $V=U^5$, now gives $\max(|n|,b)\gg U^{17/6}$ with an absolute constant. If the actual parameter is integral ($b=1$), this improves to $\gg U^3$. These bounds require no assertion that a globally feasible anchor exists at $q=5$.

```python
from math import isqrt
C=26354
P=(415903109,2575401579137)
assert 365*C**5-4==4*3*19**2*P[0]*P[1]
for p in P:
    assert all(p%d for d in range(2,isqrt(p)+1))
    assert {pow(x,(p-1)//2,p) for x in (5,C)}=={1,p-1}
assert pow(5,9,19)==1 and 73%9==1 and C%19==1
assert 73%72==1 and C%73==1 and C%3==2 and C%5!=0
```
