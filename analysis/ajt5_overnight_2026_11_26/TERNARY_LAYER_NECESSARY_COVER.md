# A necessary ternary-layer cover for a terminal-blind first blocker

**The full head menu excludes a class of first blockers by an exact ternary-order test.** It also gives a finite necessary cover condition when earlier exceptional rows can interfere. The test depends on which rows are reached by ordinary repairs, their actual orders, and whether their observations are zero. I took no numerical credit. The verified exception bound remains **below \(0.000062192085\%\)**. [Verified terminal-blind menu](https://github.com/Samsen879/a303656/commit/c5d6995b07d64c35ec87329ee9873f65c0b7ea33)

### A necessary cover for first blocking

Fix a proposed first blocker \(q\) of that menu. Suppose every prime factor of either base order at \(q\) is at most \(81\), and put \(b_q=v_3(\operatorname{ord}_q(5))\ge3\). This includes the base-5-deep \(D=81\) case. Start from any full older survivor. Keep \(c\) fixed initially and vary only the 3-primary coordinate of \(d\), keeping \(d\equiv0\bmod3\).

The small head allows this release. The tests at \(2,3,7,11,23\) are unchanged. At \(19\), the order of \(5\) is \(9\), so at most one of the three \(d\bmod9\) readings is forbidden. In particular, **at least one of the two readings with \(v_3(d)=1\) is legal**. Outside the head, a row directly reading the change must be \(19\bmod36\). The only candidate through \(81\) besides \(19\) is the composite \(55\).

For each ordinary row that can be reached, choose one ordinary repair axis. Follow that axis’s primary digit to every later row that reads it, continuing through ordinary rows and stopping at common-Wieferich rows. Every reached repair prime exceeds \(81\), so its repair preserves the terminal orders and the chosen ternary coordinates. A singly exceptional row uses its ordinary axis. Unreached rows preserve their **full** observations, including higher valuations, since lifting an order at a distinct row only introduces powers of that row’s own prime. No dropped row is discarded in this comparison. Each affected row is either restored in increasing order or required to be a unit. [Protected repair criterion](https://github.com/Samsen879/a303656/commit/29e0e8f6ef234eabfd795e993ce1e8709ec5d827)

Assume that each reached common-Wieferich row has zero target reading modulo its prime. Rows with equal quadratic signs at such a reading are discarded from the cover by sign protection; the test is applied to the rest. For such a row \(p\), put
\[
a=v_3(\operatorname{ord}_p(3)),\qquad b=v_3(\operatorname{ord}_p(5)).
\]
The head keeps \(c\) a 3-adic unit. On a layer \(v_3(d)=k\ge1\), cancellation requires the two 3-primary components to have the same order, since \(-1\) has order two. Thus it requires
\[
a=\max(0,b-k).
\]
If \(a>0\), the row can hit only the layer \(k=b-a\). In that layer it forbids at most one class of \(d/(3^k c)\bmod3^a\), obtained by a discrete logarithm of the two actual 3-primary components. If \(a=0\), its possible hits lie in the tail \(k\ge b\). Equal quadratic characters of the two powers remove the entire row from this test. These are necessary conditions for a hit, so testing their union remains safe even when the prime-to-3 components change during repair. [Sign protection for zero observations](https://github.com/Samsen879/a303656/commit/01da98288734948b95f4d0f307aa83b88d77bedf)

Consequently, **in each legal first-digit class of \(d/(3c)\bmod3\), first blocking requires the forbidden classes to leave at most one residue modulo \(3^{b_q-1}\) in projection.** Two different surviving residues give different base-5 powers at \(q\), and ordinary restoration preserves them. At least one shift then gives a unit for the actual \(n_q\), including a nonzero terminal observation.

A simple excluded class follows. After sign protection, suppose no reached common-Wieferich row has either \(a=0,\ b\le1\) or \(a>0,\ b=a+1\). Then no row hits the layer \(v_3(d)=1\). A legal first digit permits all three next digits, so \(q\) cannot first block. More generally, in a legal class \(e\), the sum of the weights \(3^{1-a}\) of its matching slope restrictions must be at least \(1-3^{2-b_q}\), unless a tail restriction covers the layer. This follows by counting the measure of the \(3^{b_q-2}\) terminal residue classes in that cylinder.

### Actual control and the boundary

At the integer below, the ordinary rows \(1783,3079,3187\) have ternary depths \((3,4),(1,3),(0,3)\). On a single legal slice their exact valuation-one masks occupy, respectively, the first layer, the second layer, and the deeper tail. Two first-layer choices extend through the **full** prefix below \(3187\) and give terminal shifts \(2056,2099\).

The same integer also has a nonzero observation at ordinary \(151\) that kills **every** point on the frozen slice. Releasing its own ordinary digit repairs it without changing either terminal shift. This shows the precise limitation of the ternary cover test. A reached **nonzero exceptional** row needs its actual observation-dependent hit set, or a separate proof that its test can be preserved. The zero-layer condition alone supplies neither. The example uses ordinary primes throughout.

```python
from math import isqrt, lcm

def prime(p):
    return p > 1 and all(p % j for j in range(2, isqrt(p)+1))

def order(b, p):
    return next(j for j in range(1, p) if pow(b, j, p) == 1)

def S(c, d, m):
    return (pow(3, c, m) + pow(5, d, m)) % m

q = 3187
rows = (1783, 3079, q)
head = (7, 11, 19, 23)
small = tuple(p for p in range(31, 82, 4) if prime(p))
assert [p for p in range(19, 82, 36) if prime(p)] == [19]
assert order(5, 19) == 9
assert [(order(3,p), order(5,p)) for p in rows] == [
    (594,162), (114,513), (118,3186)]
assert all(pow(b,p-1,p*p) != 1 for p in rows+(151,) for b in (3,5))

n = 7693492956813644214704828744497799903237253
c, T = 162887720214735395, 6515508808589415800
digits = range(0, 81, 3)
assert (n%3,n%32,c%6,T%8,T%3) == (0,5,5,0,2)

def exact_one(a, b, p):
    z = (n-S(a,b,p*p)) % (p*p)
    return z % p == 0 and z != 0

for j in digits:
    d = T*j
    assert (n-S(c,d,32))%4 == 1 and (n-pow(5,d,3))%3
    assert all((n-S(c,d,p))%p for p in head+small)

assert [n%(p*p) for p in rows] == list(rows)
assert [[j for j in digits if exact_one(c,T*j,p)] for p in rows] == [
    [33], [9,36,63], [0,27,54]]
assert n%151 and all(exact_one(c,T*j,151) for j in digits)
assert [S(c,T*j,q) for j in (6,12)] == [2056,2099]

old = [p for p in range(31, q, 4) if prime(p)]
M = lcm(3960, q-1, *(p*p*(p-1) for p in old))
for j in (6,12):
    a,d = c,T*j
    for p in old:
        z = (n-S(a,d,p**3)) % p**3
        if z%p:
            continue
        assert p>81 and p not in rows
        L = M
        while L%p==0:
            L //= p
        f = ((pow(3,L,p*p)-1)//p)*pow(3,a,p)%p
        a += L*(z//p*pow(f,-1,p)%p)
        if (n-S(a,d,p**3))%p**3 == 0:
            a += p*L
    for p in old:
        z = (n-S(a,d,p**3)) % p**3
        assert z%p or z in range(p*p,p**3,p*p)
    assert (n-S(a,d,151**3))%151**3 in range(151**2,151**3,151**2)
    assert (a-c)%3960 == 0 and S(a,d,q) == S(c,d,q)
```

The weight inequality uses Haar measure in the legal first-layer cylinder; any set projecting to at most one terminal residue has measure at most \(3^{2-b_q}\) relative to that cylinder. The forbidden classes are conservative supersets of actual vetoes. A reached exceptional row with nonzero reading is not covered by this theorem. No numerical deduction is taken.
