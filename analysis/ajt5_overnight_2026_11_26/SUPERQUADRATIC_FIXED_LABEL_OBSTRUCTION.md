# A fixed label with no uniform quadratic modulus-height bound

Fix the actual AJT label (d,c;e,f;r)=(0,0;1,1;1). The two residuals are R=m−2 and S=5R+3. For every C>0, there are infinitely many primes p≡3 mod 4, p>3, for which the progression m≡2 mod p passes its local test at p, but has **no** strictly positive simultaneous bridge with m≤2+Cp². Local compatibility is witnessed by R=0, S=3 in the p-adics: every unit at an inert odd prime is a norm from the unramified quadratic extension. If required, use R=p² and S=5p²+3 instead, also locally represented.

For a true positive bridge in this range, inert-prime divisibility of an integral sum of two squares forces R=ap² with 1≤a≤C itself a sum of two squares. For each of these finitely many a choose a distinct auxiliary prime q_a≡3 mod 4 not dividing 30a such that 5a x²+3 has a root modulo q_a. To see these choices exist, the quadratic fields Q(sqrt(−15a)) and Q(i) are distinct: v_3(a) is even, hence v_3(15a) is odd. The quadratic fields are linearly disjoint, so the splitting/inert pair of Frobenius signs (+1,−1) occurs at infinitely many primes by Chebotarev in their biquadratic compositum. At such a q_a the root is nonzero and simple. Lift it to a nonzero class b_a modulo q_a² where the polynomial vanishes exactly once at q_a (avoid the unique root lift).

Use CRT to require p≡3 mod 4 and p≡b_a mod q_a² simultaneously. The resulting class is reduced, hence contains infinitely many primes by Dirichlet. Each positive candidate S=5ap²+3 then has odd valuation at its corresponding q_a, ruling it out. The label constants are independent of p. This argument obstructs uniform quadratic height for this **specified label**, not the existence of other labels, and gives no fixed power improvement over the quadratic lower bound. It does not claim priority; it uses standard prime-in-progression and splitting results.

Concrete replay for C=5:
```python
from math import isqrt
p = 10332369811
assert p % 4 == 3 and all(p % d for d in range(2,isqrt(p)+1))
for a,q,r in [(1,19,323),(2,11,11),(4,23,23),(5,7,28)]:
    assert (5*a*p*p+3) % q**2 == r
    assert r and r % q == 0
```
Here a=3 is already impossible by the inert prime 3. The construction uses finite fresh-prime obstruction on the candidate coefficients while ensuring the *variable itself is prime*. Merely finding a composite CRT representative would not establish this height obstruction.
