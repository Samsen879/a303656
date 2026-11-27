# Wrong-half character constraints do not ensure exact factorization

**The full factorization forces the two inert witnesses to have the same quadratic character at the wrong-half prime. That constraint does not force either witness to be small by local tests alone.** I verified this with a pair of primes that passes the factorization-shape test, the exact cofactor congruences, and all order-component tests through \(9000\), but fails actual divisibility. I also found that the earlier \(\ell=853\) correct-half control fails the full factorization hypothesis.

### What full parity adds

Write \(H=(5^\ell+3^\ell)/8=d s^2q_1q_2\), where \(d=6\ell+1\) and \(q_1,q_2\) are distinct inert primes. Suppose \(p=4\ell+1\) is an inert prime in the minus half. Put \(\zeta=3^\ell\bmod p\). Then \(5^\ell\equiv3^\ell\bmod p\), \(\zeta^2=-1\), and \(d\equiv-1/2\bmod p\). Consequently
\[
C=H/d\equiv-\zeta/2=\big((1-\zeta)/2\big)^2\bmod p.
\]
Since \(s,q_1,q_2\) are units modulo \(p\), this forces \((q_1/p)=(q_2/p)\). More precisely, writing \(q_i=2u_i\ell+1\) gives
\[
s^2(u_1-2)(u_2-2)\equiv-2\zeta\pmod p.
\]

There is a precise limitation to using this identity with a fixed congruence panel. For any multiple \(M\) of \(30\ell p\) coprime to \(C\), choose a unit class \(a\bmod M\) with \(a\equiv1\bmod2\ell\), \(a\equiv2\bmod3\), and \(a\equiv\pm2\bmod5\). The class \(C/a\bmod M\) satisfies the same requirements because \(C\equiv1\bmod6\ell\) and \(C\) is a square unit modulo \(5\). Dirichlet’s theorem supplies arbitrarily large distinct primes in these two classes. Their product has the exact residue \(C\bmod M\), including the matching-character constraint. Choosing \(d\mid M\) when \(v_d(H)=1\) also preserves that exact valuation in the replacement \(d q_1q_2\). The missing test is divisibility of the actual \(5^\ell+3^\ell\) by each proposed prime. [Dirichlet’s theorem on primes in progressions](https://www.jstor.org/stable/1969454)

### Exact controls

- **Genuine full factorization.** At \(\ell=23\), \(H=139\cdot47\cdot228092436443\), with both witness primes inert.
- **A correct-half anchor with failed full parity.** At \(\ell=853\), \(76771\equiv1\bmod3\) is an additional split prime with \(H\bmod76771^2=38134\cdot76771\). Its odd valuation rules out the full factorization with \(d=5119\), despite the genuine small inert divisor \(3413\).
- **Wrong-half local control.** At \(\ell=2293\), take \(p=9173\), \(d=13759\), and \(M=120\ell p d\). The primes \(578805053903\) and \(1356529815760013\) have the required inert classes and product \(C\bmod M\). They pass every prime-primary order test through \(9000\). Each odd prime dividing the residual index \((q-1)/\ell\) is larger than \(9000\), and the exact \(2\)-primary tests pass. Both primes fail the final divisibility test.

Thus the local method can pass with both proposed factors far beyond the first eligible coefficients. A small-witness theorem for **genuine** full factorizations, or a genuine wrong-half counterexample to such a theorem, remains unresolved.

```python
from math import gcd, isqrt, prod

def prime(n):
    return n > 1 and all(n % t for t in range(2, isqrt(n)+1))

def H(n):
    return (5**n+3**n)//8

assert H(23) == 139*47*228092436443
assert all(map(prime, (139,47,228092436443)))
assert prime(76771) and 76771 % 3 == 1
assert H(853) % 76771**2 == 38134*76771

ell = 2293
p,d = 4*ell+1,6*ell+1
assert all(map(prime, (ell,p,d)))
assert H(ell) % d**2 == 8982*d and pow(15,ell,p) == p-1
D = 25**ell-9**ell
assert D % p == 0 and D % p**2 != 0 and H(ell) % p != 0

C,M = H(ell)//d,120*ell*p*d
rows = [(578805053903,5,2,(13759,9173),416265844866),
        (1356529815760013,2,4,(155921,948551),267148824856597)]
assert (prod(row[0] for row in rows)-C) % M == 0
for q,a,t,R,rem in rows:
    assert q % 3 == 2 and q % 5 in (2,3)
    assert q-1 == ell*t*prod(R) and all(r > 9000 and prime(r) for r in R)
    # The complete factorization of q-1 and these checks certify primality.
    assert pow(a,q-1,q) == 1
    assert all(gcd(pow(a,(q-1)//r,q)-1,q) == 1 for r in (2,ell,*R))
    g = -5*pow(3,-1,q) % q
    assert pow(g,(q-1)//t,q) == 1
    assert (pow(5,ell,q)+pow(3,ell,q)) % q == rem != 0
```

Independent BigInt checked complete modular prime certificates for both false factors, the exact product residue, the valuation-one split contaminant at exponent 853, and the failed actual divisibilities. The Dirichlet construction does not preserve an upper product-size bound and is not a counterexample with genuine divisors.
