# Exact equal-depth collapse loci and the distinction between one line and a full chart

**Two legal old heads can have the same whole-line cancellation locus, even when they differ in \(c\bmod 3,5,11\).** The real \(59\to2243\) example below has a shared locus \(n\equiv1407\bmod59^2\). At higher equal depth, there is a stronger distinction. A single top line can collapse even when almost all top lines in the full source chart split. At \(71\to715823\), exactly **2 of 5041** top lines collapse on the same target.

### Exact collapse test

Let \(p<q\) be inert, with both bases ordinary at \(p\), and suppose both orders at \(q\) have \(p\)-adic depth \(h\ge1\). Take \(p\nmid3960\), so changing the \(p\)-primary digits preserves each old head. Fix all other primary coordinates. Write the shift at \(q\) as \(C g^x+D t^y\), where \(C,D\) have order prime to \(p\), \(g,t\) have order \(p^h\), and \(g=t^\mu\). Here \(x,y\) are the absolute exponent residues modulo \(p^h\).

Modulo \(p^{h+1}\), write the two powers as \(A U^x,B V^y\), where \(A,B\) are the Teichmüller lifts of the source residues and \(U,V\in1+p\mathbb Z_p\). Put
\[
W=V^\mu,\qquad
\rho=-\frac{(W-1)/p}{(U-1)/p}\pmod p,\qquad
F(x)=A U^x+B W^x.
\]
The denominator in \(\rho\) is a unit. A rooted repair chart solves \(A U^x+B V^y\equiv n\pmod{p^{h+1}}\). For each \(x\) it has a unique \(y\bmod p^h\). Digits invisible at \(q\) can then make the source valuation exactly even.

A **top line**, obtained by fixing \(x\bmod p^{h-1}\) and moving its last digit, collapses precisely when
\[
C=-D,\qquad A/B=\rho\pmod p,\qquad n\equiv F(x)\pmod{p^{h+1}}.
\]
Indeed, the compensation on that line is affine in the last digit. Both terminal characters are nontrivial. Their sum can be constant only at zero, by summing over the line. Vanishing requires the two characters to agree and the coefficients to cancel. Since the fixed coefficients have order prime to \(p\), this is equivalent to \(C=-D\) and \(y=\mu x\bmod p^h\) throughout the line. The source equation at its initial point gives \(F(x)\), and its last-digit derivative gives \(\rho\). [Earlier depth-one test](https://github.com/Samsen879/a303656/blob/debfafbeee90f7b79045a21085a60d5e327e3103/analysis/ajt5_overnight_2026_11_26/PARITY_FILTERED_INTERCEPT_DENSITY_BOUND.md)

**Depth one.** An eligible anchor has the single collapse locus \(n\equiv A+B\bmod p^2\). Two eligible anchors have disjoint loci exactly when \(\rho\ne-1\) and their base‑5 source residues differ. This follows from \(A+B\equiv(1+\rho)B\bmod p\) and uniqueness of the torsion lifts. In particular, for anchors sharing \(d\), let
\[
L=\operatorname{lcm}\bigl(\operatorname{ord}_p(3),\operatorname{ord}_q(3)/p\bigr).
\]
A difference in \(c\bmod L\) prevents simultaneous collapse. Equality in \(c\bmod L\) gives identical loci, including the possibility that both are empty. Picking the anchors without reading \(n_p\) does not make their events independent. A shared locus costs exactly \(1/p^2\) under a uniform source observation.

**Depth \(h\ge2\).** If \(\rho\ne-1\), at most \(2/p\) of the top lines collapse. Under the slope condition, the binomial expansion of \(F(x)\bmod p^3\) has linear difference divisible by \(p^2\). Its second difference, divided by \(p^2\), is \(A a(a-b)\ne0\bmod p\), where \(a=(U-1)/p\) and \(b=(W-1)/p\). Thus the necessary congruence modulo \(p^3\) is a quadratic in the first digit of \(x\).

If \(\rho=-1\), the slope condition gives \(A=-B\). Put \(s=v_p(U-W)\), truncated at \(h+1\). For \(s\le h\), LTE gives
\[
v_p(F(x)-F(y))=s+v_p(x-y)
\]
whenever the right side is below the working precision. To see this, take \(x=y+j\) and expand \(U^{y+j}-W^{y+j}-(U^y-W^y)\). The term \(U^y(U^j-W^j)\) has valuation \(s+v_p(j)\), and \((U^y-W^y)(W^j-1)\) has strictly larger valuation. Consequently there are exactly \(p^{s-2}\) collapsing top lines if \(p^s\mid n\), and zero otherwise. **Whole-chart collapse at \(h\ge2\) requires \(U=W\bmod p^{h+1}\), \(A=-B\), \(C=-D\), and \(n=0\bmod p^{h+1}\).** Those conditions also suffice.

### Controls and scope

- At \(31\to683\), the heads \((8,55)\) and \((16,55)\) pass the small-head tests on the same positive target with a known square-sum witness. The first repair line collapses. The second head is a unit at \(31\) and has shift \(542\bmod683\). At \(59\to2243\), the heads represented by \((23,8817)\) and \((8839,8817)\) both pass the small head and the full prefix below \(59\) at \(n=1772213347634616708129\). Their difference in \(c\) is divisible by \(L=551\), so both lines collapse on the same source reading. [Pinned \(683\) control](https://github.com/Samsen879/a303656/blob/4a33a5d51aa0e617fb108629f84b782beebd7977/analysis/ajt5_overnight_2026_11_26/DUAL_LOCKED_HEAD_UNIT_EXTENSION.md)
- At \(71\to715823\), the published zero top line survives the replay. The full chart has collapsing lower coordinates \(x=0,1041\bmod71^2\). At \(11\to331\), the earlier spare repair remains valid on its named panel. Base \(3\) is exceptional at \(11\), and \(3960\) locks the first \(11\)-digit. That repair falls outside the doubly ordinary, fixed-head criterion. [Pinned \(71\) top line](https://github.com/Samsen879/a303656/blob/64768956ad32075ae297d35e6a76ec08003d7385/analysis/ajt5_overnight_2026_11_26/ORDINARY_INERT_CUBE_DENSITY_BOUND.md) · [Pinned \(331\) repair](https://github.com/Samsen879/a303656/blob/62fcf9dfa8ca3fbb7e1f9f4bca3cb22db01a6545/analysis/ajt5_overnight_2026_11_26/NONISOLATED_SPARE_DIGIT_SPLIT.md)

The whole-chart bound can replace a single-line charge only where the older rows allow access to the lower digits and later repairs preserve the resulting split, or where loss of those probes is separately charged. All replay terminals are ordinary. No unconditional ledger change follows. The cutoff, three tails, and **\(0.0000909120846076457\ldots\%\)** growing-box exception bound carry forward. [Pinned ledger](https://github.com/Samsen879/a303656/blob/fae2ba78b6490ab08368482a1aa37cc58c626d34/analysis/ajt5_overnight_2026_11_26/DISTINCT_FACTORIAL_ALLOWANCE_REPLACEMENT.md)

### Standalone replay

```python
from math import isqrt, lcm

def S(c, d, m):
    return (pow(3, c, m) + pow(5, d, m)) % m

def head(n, c, d, extra=()):
    u = (n - S(c, d, 32)) % 32
    t = u & -u
    return (t in (1, 2, 4, 8) and u//t % 4 == 1
            and (n-pow(5, d, 3)) % 3
            and all((n-S(c, d, r)) % r for r in (7, 11, 19, 23)+extra))

def model(p, q, h, co3, co5):
    P, M = p**h, p**(h+1)
    for r in (p, q):
        assert r % 4 == 3 and all(r % i for i in range(2, isqrt(r)+1))
    for b, co in ((3, co3), (5, co5)):
        assert pow(b, co*P, q) == 1 != pow(b, co*(P//p), q)
        assert pow(b, p-1, p*p) != 1 and pow(b, q-1, q*q) != 1
    g, t = [pow(b, co*pow(co, -1, P), q) for b, co in ((3, co3), (5, co5))]
    mu, z = 0, pow(t, P//p, q)
    for i in range(h):
        a = pow(g*pow(t, -mu, q)%q, P//p**(i+1), q)
        mu += p**i * next(j for j in range(p) if pow(z, j, q) == a)
    u, v = [pow(b, (p-1)*pow(p-1, -1, P), M) for b in (3, 5)]
    return mu, u, pow(v, mu, M)

def depth1(p, q, L, n, c, d):
    assert L % p and L % 3960 == 0
    assert all(pow(b, L, p) == pow(b, L*p, q) == 1 for b in (3, 5))
    shifts = set()
    for j in range(p):
        a = c+L*j
        ks = [k for k in range(p) if n%(p*p) == S(a, d+L*k, p*p)]
        assert len(ks) == 1
        b = d+L*ks[0]
        shifts.add(S(a, b, q))
        if n%p**3 == S(a, b, p**3):
            b += p*L
        assert (n-S(a, b, p**3))%p**3 in range(p*p, p**3, p*p)
    return shifts

p, q = 31, 683
assert model(p, q, 1, 1, 22) == (20, 435, 187)
x = 878689324483835865 + 1818491925553156392*5**118855
n = x*x + 764664689757674474**2 + 3**8 + 5**55495
assert all(head(n, c, 55) for c in (8, 16))
assert n%q == 0 and depth1(p, q, 3960, n, 8, 55) == {0}
assert (n-S(16, 55, p))%p == 23 and S(16, 55, q) == 542

p, q, n = 59, 2243, 1772213347634616708129
assert model(p, q, 1, 19, 38) == (44, 1063, 886)
assert n%32 == 1 and n%3 == 0 and n%(p*p) == 1407 and n%(q*q) == q
L = lcm(3960, 58, 38, 30, 42, 46)
for c in (23, 8839):
    assert head(n, c, 8817, (31, 43, 47)) and c%3 and 8817%3 == 0
    assert depth1(p, q, L, n, c, 8817) == {0}
assert all((8839-23)%r for r in (3, 5, 11))

p, q, n, c, d = 71, 715823, 2420068764704544, 10082, 45369
mu, u, w = model(p, q, 3, 1, 2)
assert (mu, u, w) == (321174, 16945571, 8621531)
assert head(n, c, d) and (u-w)%(p*p)
L = lcm(3960, p-1)*p*p
line = [(c+L*j, d+L*((19+41*j)%p)) for j in range(p)]
assert {S(a, b, q) for a, b in line} == {0}
assert all(n%p**4 == S(a, b, p**4) for a, b in line)
P, M = p**3, p**4
A, B = [pow(b, e*P*pow(P, -1, p-1), M) for b, e in ((3, c), (5, d))]
def F(j):
    return (A*pow(u, j, M) + B*pow(w, j, M)) % M
roots = [j for j in range(p) if F(j)%P == n%P]
assert roots == [0, 47]
assert sorted(j+p*k for j in roots for k in range(p)
              if F(j+p*k) == n%M) == [0, 1041]

p, q, n = 11, 331, 2478857844897
assert pow(3, 10, p*p) == 1 != pow(5, 10, p*p)
assert all(pow(b, q-1, q*q) != 1 for b in (3, 5))
assert S(865, 45363, q) == S(73, 3, q) == 80
assert S(1225, 5763, q) == 145
assert (n-S(1225, 5763, p**3))%p**3 in range(p*p, p**3, p*p)
assert head(n, 73, 3) and not head(n, 1225, 5763)
assert 3960%11 == 0 and (1225-865)%11
print("31 split, shared 59 alignment, 71 depth, and locked 11 verified")
```

For the low-digit bound at depth at least two, the binomial expansion yields a quadratic in x modulo p after subtracting the common residue modulo p² and dividing by p²; its second difference is nonzero. In the aligned A=−B case, the displayed LTE equality makes x modulo p^(h+1−s) biject onto the multiples of p^s at working precision, so the stated count follows. These structural statements do not license replacing a fixed-top-line charge by full-chart average without an actual simultaneous release of the lower digits.
