# Deterministic base-2 Gaussian gcd selector with all heads and a forced composite branch

This extends the [base-5 fixed-head selector](https://github.com/Samsen879/a303656/commit/df0491cfde32034f48dfca129ab4be4202206ff8). Every congruence head has a compatible growing two-axis chart, and a positive proportion within each class modulo \(1728\cdot17\) obtain many actual matching labels. A compatible head is not itself a successful candidate on every input. The forced-composite cases establish real success with the prescribed peel, not a general primality test.

Independent integer replay verified all 6,912 head-and-period combinations and the three positive/negative native controls. For the odd head, the four exponent parity pairs give the four even shifts mod 8. For the even head, the order-16 orbit of 3 mod 64 covers each chosen parity coset among powers of 3, and hence the required class mod 8 inside mod 64. The second-axis congruences are compatible with the mod-27 branch because their powers of two and the order of 5 mod 27 agree on the already chosen parity. The 17-peel preserves \(5\bmod8\) and the Gaussian gcd computes an actual norm factor even for a composite \(V\). For the density proof, a fixed target class supplies a reduced arithmetic progression for prime \(V\); prime-pair restrictions can be dropped for the upper-bound sieve.

**The selector now has a deterministic head for every residue class mod \(1728\), using base \(2\) alone.** It also has a forced-composite branch. In each class mod \(1728\cdot17\), a positive proportion of targets have \(\gg\log n\) certified labels with distinct exponents on both axes. In the classes assigned to the composite branch, every label in the chart has normalized remainder divisible by \(17\), and the counted certificates have normalized remainder \(17p\) with \(p\asymp n\) prime.

### Head selection and certificate

Given \(n\), set \(a=0\) for odd \(n\) and \(a=3\) for even \(n\). Select exponent phases so that
\[
R=n-3^c-5^d\equiv 5\cdot2^a\pmod {2^{a+3}}.
\]
For odd \(n\), the four exponent parity pairs give the four even shifts mod \(8\). For even \(n\), first choose the parities from the shift mod \(8\). Fix \(d\) to its parity representative mod \(16\), then lift \(c\) mod \(16\). Powers of \(3\) of the chosen parity fill the required class mod \(8\) inside mod \(64\).

Take \(c\ge3\). If the selected parity of \(d\) gives \(3\nmid n-5^d\), set \(b=0\). Otherwise set \(b=1\) and choose \(5^d\equiv n-9\bmod27\). The order of \(5\bmod27\) is \(18\), and the solution has the already selected parity. It combines with the power-of-two phase by CRT. Freeze the resulting chart at \(c\equiv c_0\bmod16,\ d\equiv d_0\bmod144\).

Every positive remainder in this chart satisfies
\[
R=wU,\qquad w=2^a9^b,\qquad U\equiv5\bmod8,\qquad 3\nmid U .
\]
The chart freezes the shift \(S=3^c+5^d\) mod \(1728\) and mod \(17\). If \(n\equiv S\bmod17\), set \(A=17\); otherwise set \(A=1\). Compute \(V=U/A\), and test
\[
r=2^{(V-1)/4}\bmod V,\qquad r^2\equiv-1\bmod V.
\]
On success, \(\gcd_{\mathbb Z[i]}(V,r+i)\) has norm \(V\): its ideal is the kernel of the map \(i\mapsto-r\) onto \(\mathbb Z/V\mathbb Z\), of index \(V\). Multiply by \(3^b(1+i)^a\) and, in the composite branch, by \(4+i\). This certifies the full remainder by exact arithmetic, with no primality test. Every prime \(V\equiv5\bmod8\) passes by the supplementary law for \(2\).

### Positive proportion in each class

Fix any target class mod \(1728\cdot17\) and let \(X=2^H\). Take both exponent axes in \([H/32,H/4]\) with the phases above. Count edges for which \(V\) is prime in \([9X/(16wA),3X/(4wA)]\). The shifts are \(o(X)\), so these are targets in \([X/2,X)\). The target class imposes a fixed reduced progression on \(V\) mod \(1728/w\). When \(A=1\) it also gives a nonzero residue mod \(17\). When \(A=17\), one may impose \(V\equiv1\bmod17\) to certify exact valuation one at \(17\). Every counted edge has exact valuation \(2b\) at \(3\) and units at the other inert primes through \(\lfloor H/16\rfloor\). The fixed-modulus prime number theorem gives \(\asymp X/H\) edges per label, hence \(\asymp XH\) in total. [Fixed-modulus prime number theorem](https://doi.org/10.1112/S0010437X12000802)

The row and column degree second moments are each \(O(XH)\). In a fixed row, apply the uniform two-prime upper sieve with nonzero shift \((5^{d'}-5^d)/(wA)\); in a column use \((3^{c'}-3^c)/(wA)\). For either base \(g=3,5\), the singular-series weight has bounded average over \(g^j-1\), \(j\le H\). To see this, expand the weight with squarefree divisor weights \(\prod_{p\mid d}1/(p-2)\) over odd primes. Divisors of order at most \(T\) use primes in \(\prod_{j\le T}(g^j-1)\), whose log is \(O(T^2)\). The weight product is polylogarithmic in \(T\) by the reciprocal-prime bound up to \(T^4\), with bounded contribution above \(T^4\). Dyadic summation therefore bounds the sum of divisor weights divided by their orders. This gives \(O(X)\) per row or column. [Uniform prime-pair upper sieve, Ding–Verwee, Lemma 3.2, v1](https://arxiv.org/html/2602.14368v1)

Delete edges incident to degrees above a sufficiently large constant \(D_0\). This costs \(O(XH/D_0)\) edges and leaves \(\gg XH\). Each target retains at most \(D_0H\), so \(\gg X\) targets retain \(\gg H\) edges. Greedy matching keeps at least a \(1/(2D_0-1)\) fraction, giving distinct exponents on both axes. In particular, the even forced-composite classes add a family disjoint from the original odd head.

### Sharp limit of the unsplit power test

For odd \(U>1\) with \(U\equiv1\bmod4\), **some base** \(z\) satisfies \(z^{(U-1)/2}\equiv-1\bmod U\) if and only if
\[
v_2(p-1)\ge v_2(U-1)\qquad\text{for every prime }p\mid U.
\]
Over \(p^k\parallel U\), the unit group is cyclic of order \(N_p=p^{k-1}(p-1)\). With \(E=(U-1)/2\), the power equation is solvable exactly when \(\gcd(E,N_p)\mid N_p/2\), and then has \(\gcd(E,N_p)\) solutions. CRT gives the criterion and the exact number of successful bases. In particular, an omitted inert square can leave a genuine norm on which **every** unsplit base fails.

The replay checks all 1,728 heads and three native controls. The first accepts \(U=3277=29\cdot113\) directly. The second has the same old panel readings and a true norm containing \(43^2\), which defeats every unsplit base. The third has even target, \(U=17\cdot13\), and succeeds after the prescribed \(17\)-peel.

```python
from math import gcd, prod

M = 1728

def head(n):
    a = 0 if n % 2 else 3
    Q = 1 << (a + 3)
    L = Q // 4
    c, e = next((c, e) for e in (0, 1) for c in range(3, 3 + L)
                if (n - pow(3,c,Q) - pow(5,e,Q)) % Q == 5*2**a)
    b = int(n % 3 == pow(5,e,3))
    d = next(d for d in range(1,145)
             if (d-e) % L == 0 and
             (not b or (n-pow(5,d,27)) % 27 == 9))
    return c, d, a, b

def mul(z, w):
    a, b = z
    c, d = w
    return a*c-b*d, a*d+b*c

def norm2(U):
    assert U % 8 == 5
    r = pow(2, (U-1)//4, U)
    if r*r % U != U-1:
        return None
    a, b, c, d = U, 0, r, 1
    while c or d:
        D = c*c+d*d
        x = (2*(a*c+b*d)+D)//(2*D)
        y = (2*(b*c-a*d)+D)//(2*D)
        a, b, c, d = c, d, a-x*c+y*d, b-x*d-y*c
    assert a*a+b*b == U
    return a, b

def cert(n, c, d):
    C, D, a, b = head(n)
    assert c >= 3 and d >= 1 and (c-C) % 16 == (d-D) % 144 == 0
    R, w = n-3**c-5**d, 2**a*9**b
    if R <= 0:
        return None
    assert R % w == 0
    U = R//w
    A = 17 if U % 17 == 0 else 1
    z = norm2(U//A)
    if z is None:
        return None
    z = mul(z, (4,1) if A == 17 else (1,0))
    z = mul(z, (3**b,0))
    for _ in range(a):
        z = mul(z, (1,1))
    assert sum(t*t for t in z) == R
    return z

for h in range(M):
    c, d, a, b = head(h)
    w = 2**a*9**b
    for i, j in ((0,0), (1,0), (0,1), (1,1)):
        R = (h-pow(3,c+16*i,M)-pow(5,d+144*j,M)) % M
        assert R % w == 0 and (R//w) % 8 == 5
        assert gcd(R//w, M//w) == 1

P = (7,11,19,23,31)
u, v, q = 3277, 739334841505104954229, 43
hit, miss = 32+u, 32+q*q*v
assert u == 29*113 and head(hit) == head(miss) == (3,1,0,0)
assert (miss-hit) % (M*17*prod(p**3 for p in P)) == 0
assert all(u % p for p in P)
assert sum(pow(z,(u-1)//2,u) == u-1 for z in range(u)) == 196
assert cert(hit,3,1) is not None and cert(miss,3,1) is None
assert sum((q*t)**2 for t in norm2(v)) == miss-32
assert q % 4 == 3 and v % q != 0

even = 3**3 + 5**16 + 8*17*13
assert head(even) == (3,16,3,0)
assert norm2(17*13) is None and cert(even,3,16) is not None
print(hit, cert(hit,3,1), miss, even, cert(even,3,16))
```

Every input now has an available **head**. The density proof supplies successful labels for a positive fraction within each head class. Finding one for every preassigned \(n\) remains open.
