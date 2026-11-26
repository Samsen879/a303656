# Separating repeated and unbalanced inert factors in p²+2188

Let $F(p)=p^2+2188$ on primes $X<p<2X$. For $3<z<X^{2/3}$, the number of $p$ for which some prime $q>z$ satisfies $q^2\mid F(p)$ is $O(X/z+X^{2/3}\log X)$. Exclude the finitely many primes dividing $2\cdot2188$ from consideration (they cannot satisfy $q^2\mid F(p)$ for prime inputs $p$ large enough). For $q\le X^{2/3}$ the congruence has at most two roots modulo $q^2$, giving $O(X/z+X^{2/3})$ after summing $X/q^2+1$. For $q>X^{2/3}$ write $F(p)=kq^2$, so $k=O(X^{2/3})$. Fixing $k$ and a dyadic $q$ interval $[Q,2Q)$, the reduced fractions $p/q$ are all within $2188/Q^2$ of $\sqrt k$ on its left, and distinct ones are separated by at least $1/(4Q^2)$. They are reduced because the only possibility $p=q$ would force $p\mid2188$. There are thus $O(1)$ fractions per fixed $k$ and box, giving the stated bound.

For a parity sieve leaving four inert factors $q_1,\ldots,q_4\ge X^{1/2-\epsilon}$, counted with multiplicity, the products $L=q_1q_2$ and $R=q_3q_4$ are both at least $X^{1-2\epsilon}$ and retain the same roughness (lack of small prime factors). If $F(p)=E^2bLR$, the matrix with rows $(L,p)$ and $(p,E^2bR)$ has determinant $2188$, and $b=O(X^{4\epsilon})$. These algebraic facts reduce the four-factor case to a balanced-block counting problem; they do not on their own bound the number of prime inputs in it.

The two-factor case does not automatically have that balance, even with $E=b=1$. The replay gives one genuine unbalanced failure and one exact four-factor example for the grouping argument. This note does not prove a prime-norm lower bound.

```python
from math import isqrt
def prime(n):
    return n>1 and all(n%j for j in range(2,isqrt(n)+1))
D=2188
X,p,q,r=970,971,47,20107
assert all(prime(v) and v%4==3 for v in (p,q,r))
assert p*p+D==q*r
assert q**100>X**49 and q**4<X**3 and r**4>X**5
p=195863
s=(191,227,811,1091)
assert all(prime(v) and v%4==3 for v in (p,*s))
L,R=s[0]*s[1],s[2]*s[3]
assert p*p+D==L*R
```
