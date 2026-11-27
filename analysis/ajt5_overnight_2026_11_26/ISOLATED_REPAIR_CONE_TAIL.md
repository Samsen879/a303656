# Output-isolated repair cones and a separate summable blocker tail

**A first blocker can be charged to an earlier interacting cone of the order graph.** For an output-isolated source that can be freely released, the charge is zero when its cone contains no earlier common Wieferich prime. The bound also gives a summable tail for large releasable sources without a catalogue beyond \(B=9\cdot10^{14}\). The pinned unconditional density ledger, including all three tails, stays intact. [Pinned conditional first-blocker bridge](https://github.com/Samsen879/a303656/blob/6530b152698faaa4f75bd583b9fe4bad0510ab2b/analysis/ajt5_overnight_2026_11_26/SEVENTEEN_SOURCE_CONDITIONAL_TAIL.md)

### A directed-cone bound

Fix a terminal \(q\). Draw \(t\to p\) when \(p<q\) is inert and the order of either base at \(p\) is divisible by the prime \(t<p\). Let \(C_q(s)\) be the earlier rows reachable from \(s\) by a nonempty directed path. Let \(L_q\) be the set of prime divisors of the two orders at \(q\).

Choose \(s\in L_q\), \(s>3\), with
\[
C_q(s)\cap L_q=\varnothing .
\]
This isolation condition holds automatically for the largest prime in \(L_q\). The source is freely releasable if it is split, or if it is inert and has an ordinary axis whose order at \(q\) is coprime to \(s\). In the second case the spare axis can repair the source without changing the output at \(q\).

Write \(\beta_p\) for the Haar probability of an odd valuation below \(\min_b v_p(b^{p-1}-1)\). It vanishes at ordinary rows and is at most \(1/p\). Then the unrestricted first-block event satisfies
\[
\boxed{\displaystyle
\Pr(E_q)\le \beta_q\min\!\left(1,\frac{s}{s-1}
               \sum_{p\in C_q(s)}\beta_p\right).
}
\]

Freeze observations outside the cone and choose a phase passing those tests, omitting the source test when the spare axis will repair it. If no such phase exists, \(q\) cannot be the first blocker. Release the top \(s\)-digit on an axis read at \(q\), giving \(s\) probes with distinct terminal shifts. Restore the source with the spare axis if needed. Restore the cone rows in increasing order using their own primary digits. The cone contains every earlier row that these changes can affect, and isolation keeps the \(q\)-shifts fixed during restoration.

For each probe, the shift entering a row \(p\) is chosen before reading \(n_p\). The chance that restoration fails there is at most \(\beta_p\), so the expected number of failed probes is at most \(s\sum_{p\in C_q(s)}\beta_p\). A first blocker needs at least \(s-1\) failures. Markov gives the displayed bound, followed by the terminal factor after conditioning on the older observations. This charges a reachable earlier failure without requiring independence between different probes. [Exact terminal projection and lifts](https://github.com/Samsen879/a303656/blob/6530b152698faaa4f75bd583b9fe4bad0510ab2b/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_TERMINAL_PROJECTION.md)

The finite test can treat every cone row above \(B\) as potentially common. For example, an inert \(q=2s+1\) with split prime \(s>3\) has an empty cone and cannot first block. At \(q=6s+1\) with split \(s\), the only possible cone vertices are \(2s+1\) and its relay \(4s+3\). The class is excluded whenever both possibilities are composite or certified ordinary. In particular, the published cutoff suffices for this test when \(4s+3\le B\).

### Finite-to-tail bound

For terminals admitting such a source \(s\ge q^\gamma\), with \(\gamma>1/4\), the total first-blocker mass above \(Z\ge B\) is at most
\[
\frac{75}{4}\,
\frac{Z^{-(4\gamma-1)/3}}{1-2^{-(4\gamma-1)/3}} .
\]
This also applies with the pinned small head for these large sources, since its locked prime coordinates lie below \(s\) and all cone vertices.

On \(q\in[X,2X)\), write each edge of a path as \(p_i=k_i p_{i-1}+1\), with \(k_i\equiv2\bmod4\). At exponent \(4/3\), the sum of \(k_i^{-4/3}\) over allowed multipliers is below \(9/10\), by taking the first three terms and an integral. Since an endpoint in the interval satisfies \(\prod k_i\le2X/s\), summing all nonempty paths bounds its cone’s reciprocal mass by \(9(2X/s)^{1/3}/s\). For fixed \(s\), the terminal progression modulo \(4s\) has reciprocal mass at most \(5/(4s)\), and \(s/(s-1)\le5/4\). Summing over integers \(s\ge X^\gamma\) gives the dyadic bound \((75/4)X^{-(4\gamma-1)/3}\). This uses the path count even for nonzero observations because the isolation condition preserves **distinct shifts** during repair. [Earlier path count for zero observations](https://github.com/Samsen879/a303656/blob/6530b152698faaa4f75bd583b9fe4bad0510ab2b/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_SPLIT_RELEASE_TAIL.md)

### Real relay countercontrol

At \(n=2478857844897\), release \(s=5\) by changing \(c=73\) to \(865\), then repair at \(11\) and \(67\) by moving \(d=3\) to \(1803\) and \(45363\). The actual path is \(5\to11\to67\), and \(67\) is blind to \(5\). The same repairs preserve two distinct shifts at \(q=31\), while the repair at \(11\) makes the two shifts coincide at \(q=331\), whose output reads \(11\).

| Phase \((c,d)\) | Valuations at \(11,67\) | Shift mod \(31\) | Shift mod \(331\) |
|---|---|---:|---:|
| \((73,3)\) | \(0,0\) | 25 | 80 |
| \((865,3)\) | \(1,0\) | 7 | 172 |
| \((865,1803)\) | \(2,1\) | 7 | 80 |
| \((865,45363)\) | \(2,2\) | 7 | 80 |

These are finite-panel arithmetic controls at ordinary terminals. The second shows why the repair argument needs output isolation and why direct readers alone omit a genuine relay.

### Inline replay

The script checks the named primes and the exact arithmetic above. It also certifies a tail bound of \(5.437\cdot10^{-9}\) in density units for the protected subfamily with \(\gamma=3/4\) and \(Z=B\). This is a separate subfamily bound, so no subtraction is made from the pinned total.

```python
from fractions import Fraction as Q
from math import isqrt

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

def order(b,p):
    return next(d for d in range(1,p) if (p-1)%d==0 and pow(b,d,p)==1)

def reads(s,p):
    return any(order(b,p)%s==0 for b in (3,5))

def cone(s,rows):
    reached = {s}
    for p in sorted(rows):
        if any(t<p and reads(t,p) for t in reached):
            reached.add(p)
    return reached-{s}

n = 2478857844897
rows = (7,11,19,23,67)
assert all(prime(q) and q%4==3 for q in rows+(31,331))
assert (order(3,31),order(5,31)) == (30,3)
assert (order(3,331),order(5,331)) == (330,165)
assert reads(5,11) and reads(11,67) and not reads(5,67)
assert cone(5,rows) == {11,23,67}
assert cone(5,tuple(p for p in rows if p<31)) == {11,23}
assert not any(reads(p,31) for p in (11,23))
assert reads(11,331)
assert all(pow(5,p-1,p*p)!=1 for p in (11,23,67))
assert all(pow(b,q-1,q*q)!=1 for b in (3,5) for q in (31,331))

def shift(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

def val3(c,d,p):
    z = (n-shift(c,d,p**3))%(p**3)
    if not z:
        return 3
    k = 0
    while z%p == 0:
        z //= p
        k += 1
    return k

points = ((73,3),(865,3),(865,1803),(865,45363))
assert [(val3(c,d,11),val3(c,d,67)) for c,d in points] == [
    (0,0),(1,0),(2,1),(2,2)]
assert [shift(c,d,31) for c,d in points] == [25,7,7,7]
assert [shift(c,d,331) for c,d in points] == [80,172,80,80]
assert [j for j in range(11) if val3(865,3+360*j,11)>=2] == [5]
assert all((n-shift(c,d,32))%32==1 and (n-pow(5,d,3))%3
           and all((n-shift(c,d,p))%p for p in (7,19,23))
           for c,d in points)

# Bounds for k=2,6,10 and the integral from index 2.
assert Q(2,5)**3*2**4 > 1
assert Q(1,10)**3*6**4 > 1
assert Q(1,20)**3*10**4 > 1
assert (Q(7,20)/Q(3,4))**3*10 > 1
assert sum((Q(2,5),Q(1,10),Q(1,20),Q(7,20))) == Q(9,10)
assert Q(4,3)**3 > 2 and Q(63,100)**3 > Q(1,4)

def icbrt(n):
    a,b = 0,1 << ((n.bit_length()+2)//3)
    while b-a > 1:
        t = (a+b)//2
        if t**3 <= n:
            a = t
        else:
            b = t
    return a

B = 9*10**14
bound = Q(75,4)/((1-Q(63,100))*icbrt(B*B))
assert bound < Q(5437,10**12)
print("relay controls passed")
print("protected-source tail bound in density units",float(bound))
assert Q(9)*Q(4,3)*Q(5,4)*Q(5,4)==Q(75,4)
# For z>=8, summing s^{-7/3} from ceil(z) is bounded by z^{-4/3}.
# Integral comparison from ceil(z)-1 and the worst ratio z/(z-1).
assert Q(3,4)**3*Q(8,7)**4 < 1

```

On a terminal interval of length X, the progression contains at most X/(4s)+1 candidates and s≤X, giving the stated reciprocal bound. The path estimate combined with this bound is proportional to X^(1/3) times the sum of s^(-7/3) over s≥X^γ; the final two replay inequalities verify the coarse constants used in the integral comparison. The probability calculation freezes only observations outside the repair cone, never the observations of a cone row before choosing its input phase. The published unconditional ledger is unchanged.
