# Quantitative native-digit refinement and an aligned height obstruction

**The independent repair product gives a bound in terms of the CRT modulus, and maximal branching alone cannot give a shorter one.** In the actual \(3,5\) example below, 413 first-digit choices give 59,358,012 exact refined residue pairs. Yet the ordinary quarter-box contains no repair in the anchored chart. The obstruction is the aligned congruence \(u+v\equiv412\bmod413\).

### Branching, modulus, and height

Write \(c=c_0+Au,\ d=d_0+Bv\), and let \(P\) be the product of the ordinary repair primes. Assume the two strides preserve the offsets modulo each \(p\mid P\) and leave both first native digits free. At a target that collides modulo every \(p\mid P\), the condition for lifting to \(p^2\) is
\[
a_pu+b_pv=\tau_p\pmod p,\qquad a_pb_p\ne0.
\]
If the higher readers retain \(s_p\) first-digit pairs independently at each source, there are \(\prod_p s_p\) first-digit branches. For any retained pair, the second digits have \(p^2\) choices, of which exactly \(p\) push the remainder to zero modulo \(p^3\). Thus the exact number of valuation-two cells in the index period \((\mathbb Z/P^2)^2\) is
\[
\left(\prod_{p\mid P}s_p\right)P^2\prod_{p\mid P}(1-1/p).
\]
This assumes the higher readers are insensitive to the second digits. Relative to the \(P^4\) cells in the period, even maximal branching gives density only \(\prod_{p\mid P}(1-1/p)/P\). [Ordinary-primary repair framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

There is a quantitative height guarantee under the same hypotheses. Choose a retained first-digit pair with \(0\le u,v<P\). Moving only \(u\) to \(u+Pt\) preserves all first-digit reads. Each \(p\mid P\) forbids one class of \(t\bmod p\) for exact valuation two. Therefore a block \(0\le t<T\) contains a simultaneous refinement whenever
\[
T\left(1-\sum_{p\mid P}p^{-1}\right)>|R|,
\]
where \(R\) is the set of repair primes. The resulting indices satisfy \(u<PT,\ v<P\). This becomes an ordinary-height guarantee whenever those exponent bounds fit the actual target.

The converse limitation is already present at the first digits. CRT combines the lines into \(a u+b v=\tau\bmod P\). Varying \(n\bmod p^2\) with its collision modulo \(p\) fixed realizes all \(P\) intercepts, with maximal native branching at every intercept. A box of \(U\times V\) index pairs can hit at most \(UV\) intercepts. For the aligned line \(u+v=\tau\bmod P\), it can hit at most \(U+V-1\). Branch counts by themselves therefore give neither short representatives nor a square-root height guarantee for every intercept.

### Exact \(3,5\) control

Take \(R=\{7,59\}\), \(P=413\), and
\[
c=96+174u,\qquad d=174v.
\]
The two native coefficients agree at each prime. They are \(6\bmod7\) and \(3\bmod59\). The target below imposes \(u+v=-1\bmod413\), so every simultaneous even-valuation phase requires \(u+v\ge412\). The balanced phase \((206,206)\) has exact valuation two at both primes.

Yet at this same target the quarter-box has \(0\le u\le146,\ 0\le v\le100\). It contains 14,847 index pairs and misses every repair.

```python
from math import prod

R = (7, 59)
P = prod(R)
A, c0 = 174, 96
M = 12*P**3
n = 563536059 + 4*M*5**(A*100)

def offset(m, u, v):
    return (pow(3, c0+A*u, m) + pow(5, A*v, m)) % m

for p, a in [(7, 6), (59, 3)]:
    assert pow(3,A,p) == pow(5,A,p) == 1
    assert ((pow(3,A,p*p)-1)//p * pow(3,c0,p)) % p == a
    assert ((pow(5,A,p*p)-1)//p) % p == a
    assert (n-offset(p*p,0,0)) % (p*p) == (-p*a) % (p*p)
    assert (n-offset(p**3,206,206)) % (p**3) == p*p

assert n%4 == 3 and n%3 == 0
assert 3**(c0+A*146) <= n//4 < 3**(c0+A*147)
assert 5**(A*100) <= n//4 < 5**(A*101)
assert 146+100 < P-1
assert P*prod(p*(p-1) for p in R) == 59_358_012
```

The obstruction is to repair **within this anchored chart**. Each active pair has exact valuation one at one of the two inert primes. The repaired phases outside the box are local congruence certificates. Other exponent charts and genuine two-square representations remain separate questions.

Independent BigInt checked both prime lifts at the repaired phase, the exact refined cell count, and all 14,847 active index pairs in the prescribed quarter-box. The obstruction concerns the stated chart only. The upper bound on local refinement is not a true norm guarantee.
