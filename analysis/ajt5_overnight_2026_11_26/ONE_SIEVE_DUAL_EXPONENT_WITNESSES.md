# One shifted-form sieve gives two witnesses changing both exponents

Unconditionally, **\(\gg X/(\log X)^{3/2}\) distinct targets \(n\le X\)** in the original family \(n=5p+52\), \(p\equiv1\pmod{12}\), have two distinct composite, primitive two-square remainders at **\((3,2)\) and \((7,1)\)**. Both exponent labels change. The proof uses a single prime-value theorem.

### Two witnesses from one shifted form

The offsets are \(52\) and \(2192\), with \(2192-52=5\cdot428\). Take primes
\[
p=5(u^2+v^2)+428,\qquad \gcd(u,v)=1,\qquad p\equiv1\pmod3.
\]
The shifted-form theorem of Fuchs–Hsu–Rickards–Schindler–Stange counts \(\asymp Y/(\log Y)^{3/2}\) distinct such primes up to \(Y\). Its parameters are \(f=u^2+v^2\), discriminant \(-4\), multiplier \(5\), shift \(428\), and progression \(1\bmod3\). The leading coefficient is \(1\), the multiplier and shift are coprime, the shift is even, and \(\gcd(3,40)=\gcd(3,1-428)=1\). Theorem 1.1(2) directly gives the congruence-restricted lower bound, and part (1) gives the unrestricted upper bound. [Shifted quadratic forms, Theorem 1.1 and Proposition 3.8](https://arxiv.org/html/2504.20289v1)

For odd \(p\), the odd norm \(u^2+v^2\) is \(1\bmod4\), so \(p\equiv1\pmod{12}\). At \(n=5p+52\) the two remainders are
\[
R_{3,2}=5p,\qquad R_{7,1}=5(p-428)=25(u^2+v^2).
\]
The first is a norm because \(p\equiv1\pmod4\), and it is primitive because \(5p\) is squarefree for \(p>5\). For the second, multiply \(u+iv\) by one of \(3\pm4i\). The two matrices have determinant \(25\), and their kernels modulo \(5\) are the distinct lines \(v=2u\) and \(v=3u\). A primitive input lies on at most one, so at least one sign gives coprime output coordinates. Both cells lie in the \(n/4\) box once \(n\ge8748\).

At **\(p=2053,\ n=10317\)** the two certificates are
\[
10317=3^3+5^2+67^2+76^2
     =3^7+5^1+58^2+69^2.
\]
At the previously pinned \(n=2157\), the cells \((3,1)\) and \((1,0)\) also change both labels, with remainders \(19^2+42^2\) and \(28^2+37^2\). [Pinned shifted-form control](https://github.com/Samsen879/a303656/commit/3b9025c59347a9de572f6348abd057d502fc5512)

The reusable step is to choose offsets with \(F_1-F_0=MA\), where \(M\) is an odd norm and \(A\) is a nonzero multiple of \(4\). A single prime value \(p=B(u^2+v^2)+A\), with \(B\) an odd norm coprime to \(A\), gives remainders \(Mp\) and \(MB(u^2+v^2)\) at \(n=Mp+F_0\). The prime count supplies targets in this constructed family.

### Exact fixed-menu obstruction

In the \(5p+52\) family, \((7,1)\) is the smallest cell on both axes among viable alternatives that change both labels and keep the remainder divisible by \(5\). For \(d\ge1\), divisibility forces \(c\equiv3\pmod4\), hence \(c\ge7\) when \(c\ne3\). For \(d=0\), it forces \(c\equiv0\pmod4\), which makes the remainder \(3\bmod4\).

More generally, a fixed finite menu supplies a second norm for **relative density zero** among primes \(p\equiv1\pmod{12}\). For any offset \(F\ne52\) and any inert prime \(q\nmid60(52-F)\), exactly \(q-1\) of the \(q(q-1)\) unit classes modulo \(q^2\) give \(v_q(5p+52-F)=1\). For a fixed finite set of such primes, CRT and the prime number theorem in progressions therefore bound the limiting upper proportion of norms by \(\prod_q(1-1/q)\). This tends to zero as the fixed set is enlarged, by divergence of the reciprocal sum of primes \(3\bmod4\). A finite union gives the menu claim, since \((3,2)\) is the unique label at offset \(52\).

For a control in the same \(p\equiv13\pmod{60}\) class as the positive example, take \(p=1933,\ n=9717\). The \((7,1)\) remainder is \(7525=25\cdot7\cdot43\), with \(v_7=1\), while \((3,2)\) still gives \(16^2+97^2\). Finding a second witness for every prescribed target using a growing menu remains open.

### Standalone replay

```python
from math import gcd, isqrt

def F(c, d):
    return 3**c + 5**d

def R(p, c, d):
    n = 5*p + F(3, 2)
    assert p % 12 == 1 and all(p % q for q in range(2, isqrt(p)+1))
    assert 4*max(3**c, 5**d) <= n
    return n - F(c, d)

p, u, v = 2053, 1, 18
assert p == 5*(u*u + v*v) + 428 and gcd(u, v) == 1
assert F(7, 1) - F(3, 2) == 5*428
assert R(p, 3, 2) == 67**2 + 76**2 == 10265
x, y = 3*u - 4*v, 4*u + 3*v
assert gcd(x, y) == 1 and R(p, 7, 1) == x*x + y*y == 8125
assert R(421, 3, 1) == 19**2 + 42**2
assert R(421, 1, 0) == 28**2 + 37**2

assert 1933 % 60 == 2053 % 60 == 13
assert R(1933, 3, 2) == 16**2 + 97**2
assert R(1933, 7, 1) == 25*7*43
assert [a for a in range(49) if gcd(a,49) == 1
        and (5*a-2140) % 7 == 0
        and (5*a-2140) % 49 != 0] == [1, 8, 15, 22, 29, 43]
print("all exact controls passed")
```

For the fixed-menu claim, the prime number theorem in arithmetic progressions is applied only to each fixed combined modulus, with the limit in target size taken first. The result is compatible with the quantitative lower bound above: relative to the prime base family, the counted second witnesses still have density zero.
