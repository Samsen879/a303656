# An ordered closure test for even valuations in power differences

Fix $b\ge2$ and a set of imposed primes. We ask which positive $n$ have even valuations at all these primes in $b^n-1$. For the inert primes of an imaginary quadratic maximal order of class number one this is exactly the integral-norm test. For more general norm problems the parity condition alone need not suffice.

First fix the allowed 2-adic branch. If 2 is not imposed or $b$ is even, start with $n_0=1$, with no restriction on the even part of other solutions. If 2 is imposed and $b$ is odd, start the odd branch with $n_0=1$ only when $v_2(b-1)$ is even. In the even branch take $n_0=2^j$, where $j$ is 1 or 2 and makes $v_2(b-1)+v_2(b+1)+j-1$ even. The standard dyadic lifting formula explains these choices. In each allowed branch the starting value divides every solution, and multiplying the starting value by odd numbers preserves its 2-adic condition.

Process the odd imposed primes $q\nmid b$ in increasing order. Write $h_q=\operatorname{ord}_q(b)$ and $e_q=v_q(b^{q-1}-1)$. Insert $q$ once into the current exponent if and only if $h_q$ divides it and $e_q$ is odd. This is a triangular rule because every prime factor of $h_q$ is smaller than $q$. If the set of inserted primes is finite, the final product times $n_0$ is the minimal solution in its branch and divides every solution there. If infinitely many enter, that branch has no solution. This is an exact characterization, not a guarantee of a terminating decision procedure.

For the proof, if $h_q\nmid n$ the valuation is zero, and otherwise odd-prime lifting gives $v_q(b^n-1)=e_q+v_q(n)$, since both $h_q$ and $(q-1)/h_q$ are units at $q$. Inductively the current exponent divides any solution in the branch. Whenever an insertion is triggered, the order therefore divides any such solution, so the latter must contain $q$ to repair the odd valuation. On the constructed chain, each final order condition is already fixed when $q$ is processed: later primes cannot affect divisibility by $h_q$. The final finite product thus satisfies every imposed condition. An infinite set of forced primes contradicts divisibility by a fixed integer solution.

The entire solution set is closed under gcd, by $\gcd(b^n-1,b^m-1)=b^{\gcd(n,m)}-1$. It need not be closed under lcm. For Gaussian norms at base 3, exponents 2 and 3 succeed, but exponent 6 triggers the inert prime 7 of order 6. For Eisenstein norms at base 2, exponents 2 and 5 succeed, but 10 triggers the inert prime 11 of order 10. In the Eisenstein case at base 56, the base primes 5 and 11 are forced by 55, and the occurrence of 5 in the exponent forces the further inert prime 2002661, of order 5. That last example does not determine whether its entire branch terminates.

```python
from math import isqrt
assert 3**2-1==2**2+2**2 and 3**3-1==1+5**2
assert (3**6-1)%7==0 and (3**6-1)%49!=0
assert all(pow(3,j,7)!=1 for j in range(1,6))
assert 2**2-1==1+1+1 and 2**5-1==5**2+5+1
assert (2**10-1)%11==0 and (2**10-1)%121!=0
assert all(pow(2,j,11)!=1 for j in range(1,10))
p=2002661
assert p%3==2 and all(p%d for d in range(2,isqrt(p)+1))
assert 56-1==5*11 and 56**5-1==5**2*11*p
assert pow(56,5,p)==1 and 56%p!=1
```
