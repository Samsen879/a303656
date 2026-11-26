# Two preselected mod-3960 classes suffice for one terminal

**The first genuine common Wieferich terminal cannot block if the mod \(3960\) policy retains two head classes.** The two classes can be chosen using only the small-head readings, before the terminal is known. This rules out whole-line cancellation across the two-class menu for the requested two-axis case. The proof also covers other order shapes and does not require discrete logarithms.

### Two head classes suffice

Use the existing policy to choose \(c,d\bmod8\) so the \(2\)-adic test passes and \(n-5^d\) is a unit at \(3\). Keep \(d\) fixed. The four successive adjustments to \(c\) are as follows. [Published mod \(3960\) head policy](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md)

| Row made a unit | Step in \(c\) | Choices |
|---|---:|---:|
| \(7\) | \(8\) | \(3\) |
| \(19\) | \(24\) | \(3\) |
| \(11\) | \(72\) | \(5\) |
| \(23\) | \(360\) | \(11\) |

Each stage preserves the preceding tests and excludes at most one choice. At the \(7\) stage, choose two survivors with different \(c\bmod3\). Extend both through \(19\). At \(11\) and \(23\), choose extensions with different \(c\bmod5\) and \(c\bmod11\), respectively. Later steps preserve every earlier difference. This gives two legal classes \((c_0,d),(c_1,d)\bmod3960\) that differ in \(c\) modulo **each** of \(3,5,11\).

**Unit-extension theorem.** For any inert prime \(p>23\), suppose every required inert row strictly between \(23\) and \(p\) is ordinary, meaning at least one base has Fermat-quotient valuation \(1\). For every set of local readings, some extension of the two head classes passes all those rows and makes \(n-3^c-5^d\) a unit at \(p\). The terminal \(p\) can have arbitrary lifting depths.

*Proof.* Let \(s\) be the largest prime factor of either multiplicative order at \(p\). There is an odd factor of \(\operatorname{ord}_p(3)\), since \(p\equiv3\bmod4\) and \(3^2\not\equiv1\bmod p\).

- If \(s\le23\), choose an odd factor \(\ell\) of \(\operatorname{ord}_p(3)\). For \(\ell\in\{3,5,11\}\), the two head classes already distinguish \(3^c\bmod p\) with the same \(d\). Otherwise \(\ell\nmid3960\), and two choices of its free primary coordinate distinguish the shifts within one head class. Choose a shift different from \(n\bmod p\). Every subsequent ordinary repair uses a prime \(>23\), so it preserves that shift.
- If \(s>23\) is inert, apply the theorem inductively at \(s<p\), as an auxiliary terminal if necessary. This fixes all required rows below \(s\) and makes the row at \(s\) a unit. If \(s\) is split, repair all required rows below \(s\) directly and impose no test at \(s\). In either case, varying the \(s\)-primary coordinate on one axis that reads it gives two distinct shifts at \(p\). It preserves all rows through \(s\), since their unit-base orders modulo the row prime have no factor \(s\). Choose a shift different from \(n\bmod p\), then repair the required rows strictly between \(s\) and \(p\) in increasing order. Their own prime coordinates cannot change the shift at \(p\), by maximality of \(s\).

An ordinary repair uses the row’s own primary coordinate on a fast axis. If the residual is already a unit, leave it there. Otherwise the fast axis fills the lifts of its first residue and can give exact valuation \(2\), while leaving earlier rows unchanged. This completes the induction.

Taking \(p\) to be the first genuine common Wieferich prime gives the requested result. More generally, **any finite panel with at most one genuine common Wieferich inert row is nonblocking**, even if the panel omits some smaller primes. Apply the theorem at the exceptional row and repair the ordinary rows above it in increasing order. A single class frozen in advance has a different guarantee. [Earlier fixed-class peeling theorem](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/LOCKED_HEAD_MAX_PRIME_POWER_PEELING.md)

### Same-integer control at \(683\)

The original \((8,55)\) head still exhibits whole-line cancellation. Its \(31\)-repair line is exactly the zero set at \(683\). The equally valid head \((16,55)\), with the same \(d\) and the same residues modulo \(8\), instead gives \(n-S\equiv23\bmod31\) and \(S\equiv542\bmod683\) on the same integer. The replay repairs the entire older inert prefix while preserving this latter shift. Both bases are ordinary at \(683\). The original integer also has an explicit positive Gaussian norm with exact \(683\)-valuation \(2\).

```python
from itertools import product
from math import isqrt, lcm

C, r, q = 3960, 31, 683
rows = ((7,8,3), (19,24,3), (11,72,5), (23,360,11))

def S(c, d, m):
    return (pow(3,c,m) + pow(5,d,m)) % m

def good2(u):
    t = u & -u
    return bool(t and t <= 8 and u//t % 4 == 1)

def prime(p):
    return p > 1 and all(p % j for j in range(2,isqrt(p)+1))

# Check the universal small-head tables.
assert all(any(good2((n-S(c,d,32))%32)
               for c,d in product(range(8),range(dp,8,2)))
           for n,dp in product(range(32),range(2)))
for i,(p,h,k) in enumerate(rows):
    assert h%8 == 0 and len({pow(3,j*h,p) for j in range(k)}) == k
    assert all(pow(3,h,t)==1 for t,_,_ in rows[:i])
    assert all(pow(b,C,p)==1 for b in (3,5))

x = 878689324483835865 + 1818491925553156392*5**(55+30*C)
y = 764664689757674474
R = x*x + y*y
n = 3**8 + 5**55495 + R
assert n > 3**(8+30*C) + 5**(55+30*C)
assert R%r**3 == r*r and R%q**3 == q*q and n%q == 0
assert [next(j for j in range(1,q) if pow(b,j,q)==1)
        for b in (3,5)] == [31,682]
assert [pow(b,q-1,q*q) for b in (3,5)] == [28004,379749]

for c in (8,16):
    assert good2((n-S(c,55,32))%32) and (n-pow(5,55,3))%3
    assert all((n-S(c,55,p))%p for p,_,_ in rows)

for i,j in product(range(r),repeat=2):
    c,d = 8+C*i,55+C*j
    line = (j-14-20*i)%r == 0
    assert (n-S(c,d,r))%r == 0
    assert ((n-S(c,d,r*r))%(r*r)==0) == line
    assert (S(c,d,q)==0) == line

c,d,K = 16,55,lcm(C,31,682)
assert (n-S(c,d,r))%r == 23 and S(c,d,q) == 542
old = [p for p in range(27,q,4) if prime(p)]
for p in old:
    B = lcm(K,p-1)
    if (n-S(c,d,p))%p == 0:
        assert B%p and pow(3,p-1,p*p)!=1
        c += B*next(t for t in range(p)
                    if (n-S(c+B*t,d,p*p))%(p*p)==0)
        if (n-S(c,d,p**3))%p**3 == 0:
            c += B*p
    K = lcm(K,p*p*(p-1))
assert c%C == 16 and S(c,d,q) == 542
for p in old:
    u = (n-S(c,d,p**3))%p**3
    assert u%p or (u and u%(p*p)==0)
print("OK")
```

**Scope.** The unconditional result is a finite-local exclusion: any blocking panel must contain at least two genuine common Wieferich inert primes. If there is at most one such prime globally, the existing finite-blocker reduction gives density one in the two growing exponent windows. The argument gives no new all-tail numerical bound, so **\(0.0876\%\)** remains the established upper bound. The repaired prefix in the replay uses local phase representatives and makes no height claim for those representatives. The original pointwise conjecture remains open. [Finite-blocker reduction](https://github.com/Samsen879/a303656/blob/53cf8088328d1356559955c6c078042555fcd9f6/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

The unrestricted ten-target result is stronger as a count bound. The new feature here is that the same two small-head classes can be selected before the terminal or its reading is known, and the proof uses only one free primary source at each recursive step. No stronger all-tail or raw target-count bound is claimed.
