# Exact cyclotomic cofactors and a square-kernel gap bound

**Two genuine divisibilities give an effective cofactor bound and, when the cofactor is square, an exponential gap bound.** The effective bound already rules out the smallest possible cofactor for the genuine pair \(2153,3767\) at \(\ell=269\). The square-cofactor result applies at unbounded height, with an ineffective threshold.

### The exact cofactor is confined to one residue class

Let \(\ell>5\) be prime and put \(H_-=(5^\ell-3^\ell)/2\), \(H_+=(5^\ell+3^\ell)/8\), so \(25^\ell-9^\ell=16H_-H_+\). Suppose distinct inert primes \(q_1,q_2\) both divide the same half \(H\), and set \(R=H/(q_1q_2)\).

Every prime divisor \(p\) of \(H\) has \(\operatorname{ord}_p(5/3)=\ell\) in the minus half or \(\operatorname{ord}_p(-5/3)=\ell\) in the plus half. The signed ratio has \(\ell\)th power \(1\), and it cannot equal \(1\) because the only prime that could divide \(5-3\) or \(5+3\) is \(2\). Thus every such prime is \(1\bmod 2\ell\). Also, \(H\equiv q_1q_2\equiv1\bmod3\). Together these give \(R\equiv1\bmod6\ell\).

Set \(M=24\ell^2\), and let \(r_0\) be the least positive residue of
\[
H(q_1q_2)^{-1}\pmod M.
\]
The inverse exists since the two primes are coprime to \(24\ell^2\), and the two exact divisibilities imply \(R\equiv r_0\bmod M\). **If \(r_0\nmid H\), then \(R\ge r_0+M\)** and \(q_1q_2\le H/(r_0+M)\). Both tests use modular powers of \(5\) and \(3\). In particular, below \(M\) there is only one possible cofactor to test.

At \(\ell=269\) in the plus half, the genuine pair \(2153,3767\) forces \(r_0=288907\). This candidate is prime and satisfies the cofactor congruence, but \(H_+\equiv14063\bmod288907\). Thus \(R\ge2{,}025{,}571\). For comparison, at \(\ell=11\) the genuine pair \(23,266333\) gives \(r_0=R=1\).

### Exponential separation with a square cofactor

**For each \(\varepsilon>0\), for all sufficiently large prime \(\ell\), every same-half pair with \(R\) square satisfies**
\[
R(q_2-q_1)^2>5^{(1/2-\varepsilon)\ell}.
\]
In particular, a pair exhausting a half cannot have gap \(\le 5^{(1/4-\eta)\ell}\) for any fixed \(\eta>0\), once \(\ell\) is sufficiently large.

To prove it, write \(R=s^2\), \(\Delta=q_2-q_1\), and \(N=s(q_1+q_2)/2\). The exact factorization gives the integer identity \(N^2=H+s^2\Delta^2/4\). If the claimed inequality fails, then \(N-\sqrt H=O(5^{-\varepsilon\ell})\). Write \(\ell=2n+1\) and \(H=A25^n+B9^n\), with \((A,B)=(5/2,-3/2)\) or \((5/8,3/8)\). The first two terms of the square-root expansion give
\[
N=\alpha5^n+\beta(9/5)^n+O(\rho^n),\qquad
\alpha=\sqrt A,\quad \beta=\frac{B}{2\alpha},\quad
\rho=\max(5^{-2\varepsilon},81/125)<1.
\]

Apply the \(p\)-adic Subspace Theorem to the integer vector \(X=(5^nN,25^n,9^n)\). At infinity take the forms \(X_0-\alpha X_1-\beta X_2,X_1,X_2\), and at \(3,5\) take the coordinate forms. The product of their absolute values is \(O(\rho^n)\). The factors \(25^n\) and \(9^n\) cancel at \(5\) and \(3\), and the factor \(5^n\) in the approximation error cancels against \(|X_0|_5\le5^{-n}\). The vector is primitive since \(\gcd(25^n,9^n)=1\). Since \(\|X\|\asymp25^n\), infinitely many exceptions would give a fixed nonzero rational relation \(aX_0+bX_1+cX_2=0\) along an infinite subsequence. Here \(a\ne0\) because \(X_1/X_2\) varies. Dividing by \(25^n\) and taking the limit gives \(a\alpha+b=0\), contradicting the irrationality of \(\alpha\) in both halves. [Schlickewei’s \(p\)-adic Subspace Theorem](https://doi.org/10.1515/crll.1976.288.86)

The square hypothesis is a genuine restriction. At \(\ell=23\), the plus half is \(47\cdot139\cdot228092436443\). Its two inert primes both have valuation one, but the remaining split prime \(139\) makes \(R\) nonsquare. The gap proof leaves such variable nonsquare cofactors untreated and yields no density estimate for general witness pairs.

### Exact replay

```python
from math import isqrt

def prime(p):
    return p > 1 and all(p % d for d in range(2, isqrt(p) + 1))

def replay(ell, p, q):
    assert all(map(prime, (ell, p, q)))
    H = (5**ell + 3**ell) // 8
    for r in (p, q):
        assert r % 3 == 2 and r % (2*ell) == 1
        assert H % r == 0 and H % (r*r) != 0
    R = H // (p*q)
    M = 24*ell*ell
    r0 = H * pow(p*q, -1, M) % M
    assert R % M == r0
    return H, R, r0, M

assert replay(11, 23, 266333)[1:3] == (1, 1)
assert replay(23, 47, 228092436443)[1:3] == (139, 139)
assert prime(139) and 139 % 3 == 1
H, R, r0, M = replay(269, 2153, 3767)
assert r0 == 288907 and prime(r0) and H % r0 == 14063
assert R >= r0 + M == 2025571
```

Independent BigInt replay verified all three exact cofactor examples, both prime valuations in each, and the rejected least cofactor at exponent 269. The exponential gap statement has an ineffective threshold and does not apply uniformly to variable nonsquare cofactors.
