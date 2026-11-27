# The unit-at-seven head chart and matched conditional spacing exclusions

**The cited mod-3960 head policy makes the rooted valuation-two \(7\)-chart empty.** It fixes a unit at \(7\), and changes within a mod-\(3960\) head preserve both powers modulo \(7\). The earlier rooted-chart exclusion therefore applies only under a different head policy. The legal replacement is a **unit-at-\(7\) chart**, with no excluded diagonal. On that chart, finite-prime spacing can exclude a cover by shallow and deep readers together, including an active terminal. [Published head policy](https://github.com/Samsen879/a303656/commit/4a33a5d51aa0e617fb108629f84b782beebd7977)

### A matched exclusion on the legal chart

Assume all \(49^2=2401\) phases of the two free \(7\)-digits on each axis preserve the retained constraints. Test any reader that is constant on the chart separately. Suppose every remaining veto, including the terminal if active, comes from an inert common-Wieferich prime in \((B,q]\), where \(B=9\cdot10^{14}\). This includes the terminal in the union bound, so a surviving phase passes both the earlier readers and the terminal. [Published cutoff input](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)

| Exact reader depths, up to swapping axes | Maximum vetoed phases at a nonzero observation |
|---|---:|
| \((1,0)\) | 343 |
| \((1,1)\) | 98 |
| \((2,0)\), or any depth at least three | 49 |
| \((2,1)\) | 14 |
| \((2,2)\) | 2 |

Injectivity along a reading axis gives the single-axis and higher-depth bounds. The two-axis bounds count at most two hits in the projected grid, then multiply by the number of lifts of each hit. For \((1,1)\), the order-\(7\) determinant norm suffices since \(8^6<B\). The \((2,1)\) and \((2,2)\) entries use the separate finite certificate below.

An active depth-one prime occupies \(15\bmod28\), and a prime reading depth two occupies \(99\bmod196\). Counting progression positions, without testing them for primality, gives these **strict** upper limits on \(q\) for exclusion.

| Matched chart and active readers | Cover excluded for \(q<\) |
|---|---:|
| Full chart, any active depths | \(900000000000179\) |
| Full chart, nonzero observations and no \((1,0)\) readers | \(900000000000683\) |
| Full chart, no shallow readers | \(900000000009531\) |
| Full chart, only nonzero \((2,1)\) and \((2,2)\) readers | \(900000000033639\) |
| Both lower digits fixed, both upper digits free, all constant checks pass | \(900000000001299\) |

The first and third rows also allow zero observations. They use only injectivity, which bounds any active reader by 343 phases and any depth-two reader by 49. In the last row a shallow reader is constant, and each active deep reader vetoes at most 7 of the 49 upper cells. The thresholds are respectively the 7th, 25th, 49th, 172nd, and 7th progression positions for the indicated depths.

**Missing digits can invalidate the full-grid count.** On an arbitrary retained phase set, weight each projected cell by its number of remaining lifts. A reader active on both axes hits a matching of projected cells, so the corresponding maximum-weight matching bounds its veto. A reader active on one axis can take the weight of an entire projected row or column. If its only digit is fixed, that weight can be the whole chart. Its constant observation must then be checked before using spacing.

### What the small-order certificate adds

The uniform mixed-reader norm lemma from the previous round assumes that a triple uses three distinct deep lower digits. A unit grid need not have that property. The finite \(r=7\) check handles it explicitly.

If a triple stays in one lower coset on each axis, its varying multipliers have order \(7\), and the smaller norm argument applies. Otherwise normalize a unit deep difference to \(1\), swapping axes for depth \((2,2)\) if needed. For the other normalized differences \(b,c,d\), examine
\[
F(z)=(z-1)(z^d-1)-(z^b-1)(z^c-1)
\]
at a primitive \(49\)th root. Its norm is nonzero for a nonzero target. Indeed, a vanishing determinant would induce a complex affine map between three points on each unit circle, fixing \(1\). It must be the identity, which would make the two multiplier changes equal and force the target to be zero.

The certificate checks 1,410 mixed and 106,032 doubly deep tuples. After harmless factors are removed, the maximum norms are \(1172032910903\) and \(732771193638709\), respectively, both below \(B\). A prime above \(B\) therefore cannot support a triple in either projected grid. Under an alternate policy that really provides a rooted valuation-two \(7\)-chart, this also extends the old mixed-only bound. With \(s\) shallow, \(m\) mixed, and \(d\) doubly deep nonzero readers of depth at most two, a cover requires \(42(7-2s)_+\le12m+2d\).

### Same-target controls and replay

On one legal \(3,5\) head, the four ordinary readers below leave **2,045** phases in the full chart. Fixing only the first lower digit to zero leaves 343 candidate phases, all vetoed by \(71\). Fixing both lower digits to one makes the shallow checks pass and leaves **42** phases. Every observed veto in the replay has exact valuation one.

```python
from math import gcd, isqrt, prod
from operator import add, sub
from collections import Counter

B = 9*10**14
small = (7**6,79,197,883,5881,8527,22639,55469,78401,6719077)
assert max(small) < B
K = prod(small)

def norm(terms):
    # Relative norm to Q(zeta_7), followed by its absolute norm.
    v = [1]+[0]*48
    for u in range(1,49,7):
        w = [0]*49
        for e,s in terms:
            k = e*u%49
            w = list(map(add if s==1 else sub, w,
                         v[-k:]+v[:-k] if k else v))
        v = w
    R, v = v[::7], [1]+[0]*6
    for u in range(1,7):
        v = [sum(v[(i-u*j)%7]*R[j] for j in range(7)) for i in range(7)]
    return abs(v[0]-v[1])

for mixed, want in ((True,(1410,0,1172032910903)),
                    (False,(106032,47,732771193638709))):
    C = range(7,49,7) if mixed else range(1,49)
    top = count = zeros = 0
    for b in range(2,49):
        for c in C:
            for d in C:
                if c == d:
                    continue
                N = norm(((1+d,1),(b+c,-1),(1,-1),(d,-1),(b,1),(c,1)))
                H, rem = divmod(N, 7**8 if mixed else 49)
                assert rem == 0
                if not H:
                    assert not mixed and c==1 and d==b
                    zeros += 1
                if not mixed:
                    H //= gcd(H,K)
                top, count = max(top,H), count+1
    assert (count,zeros,top)==want and top<B

n,W = 554982816610987187148605091,1050155013231720
depths = {71:(1,0),43:(1,1),9311:(2,1),491:(2,2)}
def S(x,y,m):
    return (pow(3,2+W*x,m)+pow(5,3+W*y,m))%m

assert W%3960==0 and W%7 and (n%32,n%3)==(3,0)
assert [(n-S(0,0,p))%p for p in (7,11,19,23)]==[1]*4
assert [n%p for p in depths]==[63,5,2713,406]
for p,ds in depths.items():
    assert p%4==3 and all(p%d for d in range(2,isqrt(p)+1))
    for b,d in zip((3,5),ds):
        assert pow(b,p-1,p*p)!=1 and pow(b,W*7**d,p*p)==1
        if d:
            assert pow(b,W*7**(d-1),p)!=1

survive, counts = [0,0,0], Counter()
for x in range(49):
    for y in range(49):
        assert (n-S(x,y,7))%7==1
        hit = {p for p in depths if S(x,y,p)==n%p}
        assert all(S(x,y,p*p)!=n%(p*p) for p in hit)
        counts.update(hit)
        if not hit:
            survive[0] += 1
            survive[1] += x%7==0
            survive[2] += x%7==y%7==1
assert counts=={71:343,43:49,9311:7,491:8}
assert survive==[2045,0,42]
assert all(S(1,1,p)!=n%p for p in (71,43))
assert [pow(5,p-1,p*p) for p in (11,1006003)]==[78,31695130519]

def pos(d,k):
    a = next(x for x in range(B+1,B+4*d+1) if x%(4*d)==2*d+1)
    return a+(k-1)*4*d

assert [pos(d,k) for d,k in ((7,7),(7,25),(49,7),(49,49),(49,172))]==[
    900000000000179,900000000000683,900000000001299,
    900000000009531,900000000033639]
```

The new exclusions are pointwise for the specified matched charts. Chart availability and any subsequent repair that changes a retained or terminal reading still require their own checks.

Independent exact replay verified the cited policy, all 107442 determinant tuples, the two stripped norm maxima, the full 2401-cell phase chart and both restricted-chart controls. These are conditional exclusions once the chart is available; they do not construct a full legal chart while preserving arbitrary earlier and terminal readings.
