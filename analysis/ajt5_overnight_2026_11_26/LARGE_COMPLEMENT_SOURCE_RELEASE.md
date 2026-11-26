# Large complement factors as independently released sources

**Yes. A large factor \(s\mid M\) can be released while keeping both earlier homogeneous sources fixed, unless its own even repair line aligns with the terminal or an older common Wieferich test blocks the repair.** For a doubly ordinary inert \(s\ge q^\gamma\) with a shallow read at \(q\), the aligned-line exception has upper-density tail \(O_\gamma(Z^{-\gamma})\) over \(q>Z\). This includes **nonzero** observations at \(s\), where \(s\mid n\) cannot be assumed. [Pinned smooth-complement result](https://github.com/Samsen879/a303656/blob/e6cf8efaa12572fce12599e3bc54fdbe148c6c5c/analysis/ajt5_overnight_2026_11_26/ALIGNED_SMOOTH_COMPLEMENT_TAIL.md)

### Release and the exact obstruction

Take \(s>\max(p,t)>5\), where \(p,t\) are the two earlier sources. Use absolute \(s\)-digits \(x=c\bmod s,\ y=d\bmod s\). At the zero-observation terminal \(q\), cancellation requires \(g^x=h^y\), where \(g,h\) are its \(s\)-primary components of \(3,5\). A mismatch makes the terminal a unit and survives changes to every other primary. The earlier sources cannot read \(s\).

A split \(s\) has no own inert-prime test. At a doubly ordinary inert \(s\), a unit branch leaves both digits free. A rooted branch has an affine first-digit repair line, with a second digit available to make \(v_s=2\) exact. For a shallow read, the only way the whole line can fail the mismatch test is for **both axes to be read and the repair line to equal the forbidden line through the origin**. A deeper read also gives an escape. At depth two, the second-digit grid loses at most one line to the exact-even repair and at most \(s\) points to the terminal equality. At higher depth, an unread-by-the-repair digit is free.

After choosing the mismatch, repair affected older ordinary rows in increasing order along the actual read graph. Those repairs touch neither \(s\) nor the two earlier sources. Thus the pointwise exclusion applies when the reachable older rows are ordinary or otherwise repairable. An earlier common Wieferich row in that graph can be a separate obstruction, even if it passed before the release.

### A summable bound for the shallow aligned line

For fixed \(q,s\), let \(m\) be the terminal’s forbidden slope. On a rooted branch at \(s\), denote the actual base values modulo \(s\) by \(A,B\) and their Teichmüller lifts by \([A],[B]\). Alignment and zero intercept force
\[
\rho:=A/B=-m\,f_s(5)/f_s(3)\pmod s,\qquad
n\equiv(1+[\rho])[B]\pmod{s^2}.
\]
Here \(f_s(a)=(a^{s-1}-1)/s\bmod s\). If \(\rho=-1\), this is \(s^2\mid n\). Otherwise it puts \(n\bmod s^2\) in one multiplicative coset of the Teichmüller group, independently of the remaining phases. Since \(q\mid n\), writing \(n=qk\) puts \(k\) in one such coset as well.

The short interval in \(k\) matters. A CRT residue count with an \(O(s)\) error would not suffice. Let \(K=\lfloor N/q\rfloor\) and let \(L\) count the coset members in \([1,K]\). Products of \(a\) members lie in a single coset modulo \(s^2\), of size \(s-1\). The elementary divisor bound for ordered \(a\)-fold products gives, for fixed \(a\),
\[
L^a\ll_{a,\epsilon}s(1+K^a/s^2)K^{a\epsilon}.
\]
For \(q\le N^{1-\delta}\) and \(K\le s\), take \(a=\lfloor2\log s/\log K\rfloor\). This is bounded in terms of \(\delta\), and with \(\epsilon=1/8\) gives \(L\ll_\delta K^{7/8}\). For \(s\le K<s^2\), take \(a=2\), which gives \(L/K\ll s^{-1/4}\le K^{-1/8}\). For \(K\ge s^2\), full periods give \(L\le2K/s\).

For \(s\ge q^\gamma\), each \(q\) has at most \(1/\gamma\) eligible factors. The full-period contribution over \(q>Z\) is \(O_\gamma(\sum_{q>Z}q^{-1-\gamma})=O_\gamma(Z^{-\gamma})\). The short-period contribution for \(q\le N^{1-\delta}\) tends to zero after division by \(N\). The remaining \(q>N^{1-\delta}\) cost \(O(\delta)+o(1)\) by \(q\mid n\) and the prime harmonic sum. Letting \(\delta\downarrow0\) gives the stated upper-density tail.

### Actual aligned control

At \(q=592654651\), the complement after removing \(7,19\) contains the inert prime \(s=487>q^{1/4}\). The actual slopes \(1,11,250\) align all three homogeneous repair lines. At the fixed target below, every choice on the three lines lifts to exact even relay valuations, while the terminal has exact valuation \(1\) with its own digit frozen. **This terminal is ordinary.** The replay verifies the obstruction to releasing \(s\) on its repair line without claiming a genuine common Wieferich example.

```python
from math import isqrt, lcm

P, q = (7,19,487), 592654651
for a in (*P,q):
    assert a%4==3 and all(a%d for d in range(2,isqrt(a)+1))
s = P[-1]
assert (q-1)%(7*19*s)==0 and (q-1)%(s*s) and s**4>q
assert all(pow(a,q-1,q*q)!=1 for a in (3,5))

u,v = 16238273819774727413281142760361,316442812450330709135622626554716
n,c0 = 4+u*u+v*v,243*q*((q-1)//2)
H = lcm(*(a*a*(a-1) for a in P),q*(q-1))
def rem(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert rem(c0,0,q*q)==q and rem(c0,0,3)==rem(c0,0,4)==1
for a,m in zip(P,(1,11,250)):
    f3,f5 = ((pow(b,a-1,a*a)-1)//a for b in (3,5))
    assert f3 and f5 and f3*pow(f5,-1,a)%a==m
    J = H//(a*a)*pow(H//(a*a),-1,a*a)
    assert J%6==0 and (a*J)%(q*(q-1))==0
    assert all(J%(b*b*(b-1))==0 for b in P if b!=a)
    assert pow(3,J,q)!=1 and pow(5,J,q)!=1
    assert pow(3,J,q*q)==pow(5,m*J,q*q)
    for x in range(a):
        c,d = c0+J*x,J*(m*x%a)
        if rem(c,d,a**3)==0:
            c += a*J
        assert rem(c,d,a**3) in range(a*a,a**3,a*a)
        assert rem(c,d,q*q)==q
```

The modular identities combine these individual checks for all \(7\cdot19\cdot487\) choices at the same \(n\). Increasing \(u\) by a sufficiently large multiple of the test moduli activates the exponents while preserving the true representation \(n=3+1+u^2+v^2\). The remaining large-factor cases include singly ordinary relays whose fixed axis is the only one read, and reachable older common Wieferich tests that cannot be repaired after the release.

For \(K\le s\), writing \(x=\log s/\log K\ge1\) gives \(x/\lfloor2x\rfloor<3/4\), yielding the claimed short-range exponent with the fixed divisor-bound margin (for the density limiting argument \(K\to\infty\)). The special case \(\rho=-1\) is bounded directly by \(\lfloor N/(qs^2)\rfloor\); it does not need the coset estimate.
