# Independent cubing ideal choices and forced inert multiplier steps

**I obtained a growing family of genuine norm witnesses and an exact rule for searching for new height rays.** Independent ideal choices give at least \(2^k\) distinct witnesses after \(k\) cubing steps. The new-height rule either constructs the least admissible multiple of a proposed exponent or, if it runs forever, proves that no admissible multiple exists. I did not establish termination at a new independent height.

### A variable ideal construction

Let \(X=5^a>Y=9^b\), with \(b\ge0\), and call \(n\) admissible when \(D_n=X^n-Y^n\) is \(x^2+3y^2\). If \(N\) is admissible and \(d\mid N\), a norm witness at \(N\) supplies a divisor ideal of norm \(D_d\) **exactly when** every inert prime has even valuation in \(D_d\).

Indeed, \(D_d\mid D_N\). At a split prime, distribute the required exponent of \(D_d\) between the two orientations without exceeding the exponents in the given witness ideal. At an inert prime the only choice is half the exponent, and at \(3\) use the ramified ideal. The Eisenstein ring is principal, so multiplying generators gives the witness. A unit can put its coordinates in \(\mathbb Z[\sqrt{-3}]\).

There is also an explicit growing choice that needs no factoring. Starting from a certified witness \(\eta\) at \(n\), write \(A_j=X^{n3^j}\), \(B_j=Y^{n3^j}\), and \(u=\sqrt{-3}\). Independently at each step choose
\[
\gamma_j=\frac{A_j-B_j}{2}+\frac{A_j+B_j}{2}u
\quad\text{or}\quad \overline{\gamma_j}.
\]
Both have norm \(D_{n3^{j+1}}/D_{n3^j}\). Each shell is odd and greater than 3; its 3-adic valuation is at most one by LTE when 3 does not divide \(AB\), and zero otherwise. It therefore has a prime \(p\ne3\). The order of \(X/Y\bmod p\) then has \(3\)-adic valuation \(v_3(n)+j+1\), so \(p\) is absent from every other shell and the starting norm. The two coordinates of \(\gamma_j\) are coprime, so the two choices put that prime on opposite ideals. Consequently the \(2^k\) products give distinct ideals, hence distinct genuine witnesses up to units. This grows the choices **within** a height ray.

### An exact rule for new heights

At the current exponent \(n\), find the least inert prime \(q\) occurring to odd valuation in \(D_n\), and replace \(n\) by \(qn\). Stop when none remains.

For odd \(q\nmid XY\), put \(o_q=\operatorname{ord}_q(X/Y)\). The exact test is
\[
v_q(D_n)=
\begin{cases}
0,&o_q\nmid n,\\
v_q(D_{o_q})+v_q(n),&o_q\mid n.
\end{cases}
\]
At \(2\), the formula is \(v_2(D_n)=v_2(X-Y)+v_2(n)\), since \(X,Y\equiv1\bmod4\). Once an inert prime is active, every admissible multiple must have the required exponent parity there. Multiplication by the selected \(q\) can only create new obligations at larger primes, since a newly activated \(o_p\) must be divisible by \(q\), and \(o_p\mid p-1\).

Thus every intermediate exponent divides every admissible multiple of the starting exponent. If the process stops, the output is the least such multiple. An infinite run rules out every finite admissible multiple. An implementation can factor just the newly activated cyclotomic factors, since old tests at primes other than \(q\) are unchanged.

The concrete missing condition for a new ray is **termination from a start whose forced \(3\)-free core lies outside the five known cores**. For the actual \(25,9\) base, starting at \(49\) already forces both \(197\) and \(6236819\) to odd exponent. Each has exact order \(49\) and valuation one in \(25^{49}-9^{49}\). So the pure \(7\)-power tower cannot continue, even after cubing, and any hypothetical admissible multiple would carry those additional primes. In fact, for the fixed 25,9 seed, the [earlier active-inert nonrepair theorem](DIVISOR_CLOSED_CYCLOTOMIC_SEED_ORDERS.md) already rules out any admissible multiple of 49; the forced steps are necessary, not sufficient.

There is a genuine infinite failure control. For odd \(a\) and \(b>0\), \(v_2(5^a-9^b)=2\), so a repair started at an odd exponent stays odd. Every resulting difference is \(2\bmod3\), so it can never be a norm. Starting at \(125-81\), the first required prime is \(11\), and \(2399\) is already required after multiplication by \(11\).

### Exact replay

```python
from itertools import product
from math import isqrt

def norm(z):
    a,b = z
    return a*a + 3*b*b

def mul(z,w):
    a,b = z
    c,d = w
    return a*c-3*b*d, a*d+b*c

def v_one(A,B,n,p):
    r = (pow(A,n,p*p)-pow(B,n,p*p)) % (p*p)
    return r != 0 and r % p == 0

# A terminating nontrivial repair, used as a control.
assert 5**2-1 == 24 and 5**4-1 == norm((24,4))

assert 125-81 == 4*11 and v_one(125,81,11,2399)
for p in (197,6236819,2399):
    assert p % 3 == 2 and all(p % d for d in range(2,isqrt(p)+1))
for p in (197,6236819):
    g = 25*pow(9,-1,p) % p
    assert pow(g,49,p) == 1 and pow(g,7,p) != 1
    assert v_one(25,9,49,p)

# Four independent ideal choices at the genuine seed index 7 * 3**2.
z = (23816,42940)
A,B = 25**7,9**7
assert norm(z) == A-B
shells = []
for _ in range(2):
    shells.append(((A-B)//2,(A+B)//2))
    A,B = A**3,B**3

hits = set()
for signs in product((-1,1), repeat=2):
    w = z
    for (a,b),s in zip(shells,signs):
        w = mul(w,(a,s*b))
    assert norm(w) == A-B and w[0] % 4 == w[1] % 4 == 0
    hits.add(w)
assert len(hits) == 4
assert {b*pow(a,-1,3) % 3 for a,b in hits} == {0,1,2}
```

Independent BigInt checked all four exact conjugation choices, both order-49 odd valuations, and the general procedure's terminating and nonterminating controls. The infinite-run implication is logical; finite search without a termination proof cannot certify that a run goes on forever. No new independent height ray is established here.
