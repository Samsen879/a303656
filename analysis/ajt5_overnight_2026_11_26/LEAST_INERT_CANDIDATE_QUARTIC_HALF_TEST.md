# Least inert candidate and the quartic same-half test

**Exact divisibility by \(d=6\ell+1\) gives a shortcut to the least eligible inert prime in the full \(25,9\) difference. The half it lands in is automatic in one branch and depends on an additional quartic test in the other.** Actual prime exponents \(853\) and \(2293\) have the same phase modulo \(120\), and \(d\) divides the plus half exactly once in both cases. Their least eligible inert primes land in opposite halves.

### The two branches

Let \(\ell>5\) be prime, let \(H_+=(5^\ell+3^\ell)/8\) and \(H_-=(5^\ell-3^\ell)/2\), and suppose \(d=6\ell+1\) is prime and divides \(H_+\). Set \(g=-5/3\). The order of \(g\bmod d\) is \(\ell\), so \(g\) is a square. Since \(d\equiv1\bmod3\), quadratic reciprocity gives \((5/d)=1\), hence \(\ell\equiv3\bmod5\). Conversely, in that phase \(g\) is already a square modulo \(d\), and
\[
d\mid H_+\quad\Longleftrightarrow\quad 45^{2\ell}\equiv1\bmod d.
\]
Indeed, the remaining test is whether \(g\) is a cube, and \(45/g=(-3)^3\).

An inert prime divisor of \(H_+\) must be \(q=2u\ell+1\) with \(q\equiv2\bmod3\) and \((5/q)=-1\). The latter condition gives \(u\equiv1,2\bmod5\). Thus the least eligible candidate is as follows.

- **\(\ell\equiv2\bmod3\).** The candidate is \(p=2\ell+1\). If it is prime, \(g\) is a square modulo \(p\) and the square subgroup has order \(\ell\). Therefore \(p\mid H_+\) automatically.
- **\(\ell\equiv1\bmod3\).** The candidate is \(p=4\ell+1\). If it is prime, both \((3/p)\) and \((5/p)\) equal \(-1\). Thus \(5^\ell\) and \(3^\ell\) are both square roots of \(-1\) modulo \(p\), and
  \[
  15^\ell\equiv
  \begin{cases}
  +1\bmod p &\Longleftrightarrow p\mid H_+,\\
  -1\bmod p &\Longleftrightarrow p\mid H_-.
  \end{cases}
  \]
  The plus-half criterion is exactly that \(15\) be a fourth power modulo \(p\).

Both prime candidates divide \(25^\ell-9^\ell\). In either branch, their valuation in that difference equals their valuation in \(5^{p-1}-3^{p-1}\). For the second branch, the extra factor is \(5^{2\ell}+3^{2\ell}\equiv-2\bmod p\). Thus unequal base-\(5\) and base-\(3\) Fermat quotients modulo \(p\) certify valuation one and supply an actual inert witness in the indicated half.

### Matched exact controls

| \(\ell\) | \(d=6\ell+1\) | \(p=4\ell+1\) | \(H_+\bmod d^2\) | \(15^\ell\bmod p\) | Half containing \(p\) to valuation one |
|---:|---:|---:|---:|---:|---|
| 853 | 5119 | 3413 | \(619d\) | \(1\) | Plus |
| 2293 | 13759 | 9173 | \(8982d\) | \(-1\) | Minus |

At \(\ell=2293\), the eligible plus-half coefficients \(u\le26\) are \(2,11,17,26\). None divides the exact plus half. This refutes an implication from exact \(d\)-divisibility to a plus-half witness in that initial range, even with the least candidate prime. It does not settle what follows if one additionally assumes a complete factorization \(H_+=d s^2q_1q_2\). The genuine \(\ell=23\) factorization \(H_+=139\cdot47\cdot228092436443\) supplies a control for that stronger hypothesis.

```python
from math import isqrt

def prime(n):
    return n > 1 and all(n % j for j in range(2, isqrt(n)+1))

for ell, sign, a, b in [(853,1,619,566), (2293,-1,8982,2781)]:
    d, p = 6*ell+1, 4*ell+1
    assert ell % 120 == 13 and all(map(prime, (ell,d,p)))
    H, G = (5**ell+3**ell)//8, (5**ell-3**ell)//2
    assert H % d**2 == a*d and pow(45,2*ell,d) == 1
    assert pow(15,ell,p) == sign % p
    assert (H if sign == 1 else G) % p**2 == b*p
    delta = 25**ell-9**ell
    assert delta == 16*H*G and delta % p == 0 and delta % p**2 != 0

assert all(H % (2*u*ell+1) for u in (2,11,17,26))
assert (5**23+3**23)//8 == 139*47*228092436443
assert all(map(prime, (139,47,228092436443)))
```

Independent BigInt verified both exact first-kernel divisibilities, opposite quartic outcomes at the same residue phase, and the complete eligible coefficient range through 26 at exponent 2293. The negative result assumes exact first-kernel divisibility only; it does not refute a stronger implication under a complete prescribed half factorization.
