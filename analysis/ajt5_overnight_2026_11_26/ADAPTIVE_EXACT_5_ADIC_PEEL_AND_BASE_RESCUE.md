# Adaptive exact 5-adic peels rescue positive proportions in the blocked heads

This responds to [the mod-5 obstruction](https://github.com/Samsen879/a303656/commit/d66e646f58bdfe5f3f8f03453c8de9260517bb77). It changes the horizontal residue phase to enforce an exact 5-adic valuation and selects a base from \(2,3,5\) after peeling that actual valuation. It recovers a positive proportion in every specified blocked subclass, uniformly in the stated growing valuation range. It does not give density one or a witness on every preassigned input.

For the energy estimate, a fixed horizontal label has \(O(H)\) column choices, whose pair weights sum to \(O(H^2)\) by the true base-5 order average; it costs \(O(Z)\). A fixed vertical label has \(m\) horizontal choices, and at most \(m\) pairs at each gap, so their pair weights sum to \(O(mH)\) even though the horizontal step grows. It costs \(O(Z m/H)\). The diagonal terms obey the same bounds, and the additive sieve errors are polylogarithmic, negligible compared with \(Z\). Summing gives \(O(Zm)\) total degree energy. Summing the uniform per-\(j\) success lower bounds over the allowed \(j\), and using the maximum possible number \(O(\log H)\) of such successes on any target, proves the positive-proportion multiple-valuation claim without independence.

Independently replayed the same-label rescue of the old 1,200-bit blocked control, the base-5 success after a base-3 failure, the exact \(j=2\) peel, and the stationary-divisor gcd \(64\cdot17\). An exclusion of one stationary prime is not an exclusion of composite coverings by several primes.

**The mod-\(5\) failure class admits an adaptive rescue on both exponent axes.** Fix \(\epsilon>0\) and let \(X=2^H\). Uniformly for \(1\le j\) with \(5^j\le H^{1-\epsilon}\), a positive fraction of targets in **every** blocked subclass mod \((1728\cdot17)5^{j+1}\) have a matching of \(\gg H/5^j\) certified labels with exact \(v_5(R)=j\). Both exponents stay in the original box \([H/32,H/4]\). These are new successes except for a negligible set that the previous selector already certified.

### Adaptive phase and base

Keep the previous head \(c\equiv c_0\bmod16,\ d\equiv d_0\bmod144\), normalization \(w=2^a9^b\), and \(17\)-peel \(A\in\{1,17\}\). Write \(M=1728\cdot17\). On the blocked class \(n\equiv3^{c_0}\bmod5\), prescribe \(j\ge1\) and a unit \(\lambda\bmod5\). For \(d\ge j+1\), impose
\[
3^{c_0+16i}\equiv n-wA5^j\lambda\pmod{5^{j+1}}.
\]
There is exactly one \(i\bmod5^j\). Indeed \(3^{16}\equiv21\bmod25\), so \(3^{16}\) generates the kernel of reduction to mod \(5\). The resulting horizontal step is \(16\cdot5^j\). Every label on this lane has exact \(v_5(R)=j\) and \(V=R/(wA5^j)\equiv\lambda\bmod5\).

The old head already determines \(\beta=V\bmod3\) for a given \(j\), since \(3wA\mid M\) and \(5\) is invertible mod \(3\). Choose the base as follows.

| Observed phase | Allowed \(\lambda\) | Base |
|---|---:|---:|
| \(j\) even, so \(V\equiv5\bmod8\) | Any unit | \(2\) |
| \(j\) odd and \(\beta=2\) | Any unit | \(3\) |
| \(j\) odd and \(\beta=1\) | \(2\) or \(3\) | \(5\) |

In each row the selected base \(g\) is a quadratic nonresidue whenever \(V\) is prime. The actual certificate computes \(r=g^{(V-1)/4}\bmod V\) and verifies \(r^2\equiv-1\bmod V\). The Gaussian gcd then has norm \(V\). Multiplying it by \(3^b(1+i)^a(2+i)^j\) and, when \(A=17\), by \(4+i\), gives the full norm \(R\). No primality test is required for acceptance.

### Uniform count with a growing valuation

Fix a blocked target class mod \(M5^{j+1}\) and one allowable \(\lambda\). Put \(Z=X/5^j\) and \(m=|\mathcal C|\asymp H/5^j\) on the selected lane. There are \(\asymp H\) vertical labels. The quotient \(V\) at each label lies in a reduced residue class mod
\[
\frac{M5^{j+1}}{wA5^j}=\frac{5M}{wA}.
\]
This modulus is independent of \(j\). Counting primes \(V\in[9X/(16wA5^j),3X/(4wA5^j)]\) gives \(\asymp Z/H\) edges per label and \(\asymp Zm\) edges in total. All these targets lie in \([X/2,X)\), and the tested primes exceed the inert panel cutoff \(\lfloor H/16\rfloor\). [Fixed-modulus prime number theorem](https://doi.org/10.1112/S0010437X12000802)

The row and column degree squares sum to \(O(Zm)\), uniformly in \(j\). For a row, the two-prime sieve uses the shift \((5^{d'}-5^d)/(wA5^j)\). For a column it uses \((3^{c'}-3^c)/(wA5^j)\). The singular-series weight \(W(k)=\prod_{p\mid k,\ p>2}(1+1/(p-2))\) satisfies \(\sum_{r\le H}W(g^r-1)\ll H\) for \(g=3,5\). Expand into squarefree divisor weights and group by multiplicative order. The divisors of order at most \(T\) use primes in \(\prod_{r\le T}(g^r-1)\), whose log is \(O(T^2)\). Their total weight is polylogarithmic in \(T\), by splitting the primes at \(T^4\), so dyadic summation bounds the weight divided by order. In the column estimate we can sum over **all** differences \(r\le H\), giving \(O(mH)\) for the pair weights. This avoids a constant depending on the growing horizontal step. [Uniform prime-pair upper sieve, Ding–Verwee, Lemma 3.2](https://arxiv.org/html/2602.14368v1)

Deleting edges incident to degrees above a sufficiently large fixed constant costs a bounded fraction of the edges. The surviving graph has \(O(m)\) edges per target, so \(\gg Z\) targets have a matching of size \(\gg m\). The previous selector’s composite successes on the blocked class are \(o(X/(\log X)^B)\) for every fixed \(B\), by the pseudoprime bound and the \(O(H^2)\) labels. Removing them preserves this conclusion uniformly in \(j\). Summing the indicator of success over these \(j\) also gives a positive fraction of blocked targets with certificates at \(\gg\log H\) different exact valuations. [Li–Pomerance pseudoprime bound, Theorem 1](https://math.dartmouth.edu/~carlp/evenpspsfinal.pdf)

There is also an exact limit on repeating the original obstruction. **No single prime divides every peeled quotient on a full repaired lane** with two consecutive labels on each axis. For \(p\ne2,3,5,17\), such a prime would divide both \(3^{16\cdot5^j}-1\) and \(5^{144}-1\). The gcd check below excludes this for every \(j\): any relevant \(p<5^{144}\) has \(v_5(\operatorname{ord}_p3)<144\). At \(17\), the case \(A=1\) is already a unit, and after the peel \(3^{16}\equiv171\bmod17^2\) prevents the extra factor from being constant across the horizontal step. This excludes a single stationary divisor and leaves open simultaneous obstructions involving several primes.

### Matched replay

The earlier 1,200-bit blocked target still fails at all 32 labels under both old base-\(2\) branches. It now succeeds at the **same** label \((51,145)\) with \(j=1\) and base \(3\), preserving all the matched inert-panel readings. The replay also checks a native base-\(5\) case and an exact \(j=2\) peel.

```python
from math import gcd, prod

def head(n):
    a = 0 if n % 2 else 3
    Q, L = 1 << (a+3), 1 << (a+1)
    c,e = next((c,e) for e in (0,1) for c in range(3,3+L)
               if (n-pow(3,c,Q)-pow(5,e,Q)) % Q == 5*2**a)
    b = int(n % 3 == pow(5,e,3))
    d = next(d for d in range(1,145)
             if (d-e) % L == 0 and
             (not b or (n-pow(5,d,27)) % 27 == 9))
    A = 17 if (n-pow(3,c,17)-pow(5,d,17)) % 17 == 0 else 1
    return c,d,a,b,A

def root(g,V):
    r = pow(g,(V-1)//4,V)
    return r if r*r % V == V-1 else None

def norm(V,r):
    assert r is not None
    a,b,c,d = V,0,r,1
    while c or d:
        D = c*c+d*d
        x = (2*(a*c+b*d)+D)//(2*D)
        y = (2*(b*c-a*d)+D)//(2*D)
        a,b,c,d = c,d,a-x*c+y*d,b-x*d-y*c
    assert a*a+b*b == V
    return a,b

def repair(n,c,d):
    C,D,a,b,A = head(n)
    H = n.bit_length()
    assert (H+31)//32 <= min(c,d) <= max(c,d) <= H//4
    assert (c-C)%16 == (d-D)%144 == 0
    R, k = n-3**c-5**d, 2**a*9**b*A
    assert R > 0 and R % k == 0
    V,j = R//k,0
    while V % 5 == 0:
        V //= 5
        j += 1
    assert V % 8 == (5 if j%2 == 0 else 1)
    g = 2 if j%2 == 0 else 3 if V%3 == 2 else 5
    assert g != 5 or V%5 in (2,3)
    x,y = norm(V,root(g,V))
    for (u,v), count in [((1,1),a), ((3,0),b), ((4,1),A==17), ((2,1),j)]:
        for _ in range(count):
            x,y = x*u-y*v,x*v+y*u
    assert x*x+y*y == R
    return j,g

P = (7,11,19,23,31,43,47,59,67,71)
W = 1728*17*prod(p**3 for p in P)
p = 2**1195+1109
q0 = 2**1193
q = q0+(p*pow(5,-1,W)-q0)%W+413*W
S = 3**51+5**145
good,bad = S+17*p,S+85*q
assert head(good) == head(bad) == (3,1,0,0,17)
assert (good-bad)%W == 0 and good.bit_length() == bad.bit_length() == 1200
R = [bad-3**c-5**d for c in range(51,301,16) for d in (145,289)]
assert len(R) == 32 and all(r>0 and r%85 == 0 for r in R)
assert sum(all(r%p for p in P) for r in R) == 23
assert all(root(2,r) is None and root(2,r//17) is None for r in R)
assert all((bad-S)%p for p in P)
assert repair(good,51,145) == (0,2)
assert repair(bad,51,145) == (1,3)

v = 2**1193+8465
assert root(3,v) is None and repair(S+85*v,51,145) == (1,5)
assert repair(S+17*25*p,51,145) == (2,2)

T = 5**144-1
assert gcd(pow(3,16*5**144,T)-1,T) == 64*17
assert pow(3,16,17**2) == 171 and pow(3,16,25) == 21
```

The base list is fixed, while the peel, horizontal phase, and applicable base depend on the actual target and label. The theorem gives positive proportions in the previously blocked classes. It leaves open almost-all success and certification for every preassigned \(n\).
