# Cross-prime overlap requires synchronized exponent labels

**Equal cofactor cosets do not force overlap.** At the genuine base-\(5\) exceptional primes \(20771\) and \(40487\), I constructed one integer \(N\) for which both bases range over the same order-\(31\) subgroup at each prime. Both rows even have the same diagonal target relation \(N\equiv2\cdot3^C\bmod p\) for a common \(C\). Yet on the **full** \(d_{31}\) component, their forbidden sets are \(\{6\}\) and \(\{7\}\).

### What forces overlap

Suppose that at each guard prime \(p\), the allowed powers of \(3\) and \(5\) range over the same coset \(A_pH_p\). Write \(d(j)\) for a common exponent phase with primary label \(j\). If two distinct labels \(j,k\) satisfy
\[
N\equiv5^{d(j)}+5^{d(k)}\pmod{pq},
\]
then **both labels are forbidden at both guards**. At label \(j\), the complementary value \(5^{d(k)}\) is an allowed \(3\)-power at each prime, and conversely for \(k\). This forces overlap at least two. The common labels in the target relation are the essential synchronization.

For a diagonal target \(N\equiv2\cdot3^C\bmod p\), let \(j_p\) be the \(d\)-label corresponding to \(3^C\bmod p\). Scaling by \(3^{-C}\) reduces the forbidden-value calculation to \(H_p\cap(2-H_p)\). In particular, if
\[
H_p\cap(2-H_p)=\{1\},
\]
then the forbidden set is exactly \(\{j_p\}\). A common \(C\) need not give the same \(j_p\) at different primes: the two bases can identify the same exponent group with \(H_p\) at different slopes. [Coupled-block baseline](https://github.com/Samsen879/a303656/blob/4884b1f845fccf55349fff3b75930c9001ed89bd/analysis/ajt5_overnight_2026_11_26/COUPLED_GUARD_BLOCK_ELIMINATION.md)

### Full-component controls at two genuine exceptional primes

Use the same prelocks in both controls:
\[
c\equiv0\bmod14437830,\qquad d\equiv0\bmod1312530.
\]
Neither modulus contains \(31\). Write \(g_p\) for the \(5\)-power at \(d_{31}=1\), and take the common \(c\)-anchor \(C=288756600\), with \(C\equiv1\bmod31\).

| Prime \(p\) | Actual orders \(o_3,o_5\) | \(g_p\) | \(3^C\bmod p\) | Diagonal forbidden label |
|---|---:|---:|---:|---:|
| \(20771\) | \(335\cdot31,\ 335\cdot31\) | \(1758\) | \(g_p^6\) | \(6\) |
| \(40487\) | \(653\cdot31,\ 1306\cdot31\) | \(33068\) | \(g_p^7\) | \(7\) |

At each prime the exact gcd of \(X^{31}-1\) and \((2-X)^{31}-1\) is \(X-1\).

- **Disjoint target.** Take \(N=10+9752781853725239220214221361^2+11075246640031221347570696376^2\). At the two primes, \(N\bmod p=2\cdot3^C\bmod p\). With \(D_6=23625540\) and \(D_7=27563130\), respectively, the genuine hard checks are \(N-3^C-5^{D_j}\equiv p\bmod p^2\). The full forbidden sets are \(\{6\}\) and \(\{7\}\).
- **Aligned target.** With the same orders and prelocks, take \(N'=10+6578376574912837139033024437^2+10819062133018046639052260688^2\). Here \(N'\equiv1+5^{3937590}\bmod pq\), using common \(d\)-labels \(0,1\). At \(c=0,d=3937590\), both residues have exact valuation \(1\). The two full forbidden sets are exactly \(\{0,1\}\), attaining the lower bound of two.

In both controls, \(5^{p-1}\equiv1\bmod p^2\) at the two guard primes. The separate lift at \(31\) is ordinary: the replay chooses a surviving \(d_{31}\) and uses the free \(c_{31}\) coordinate to change valuation \(1\) to \(2\). Both displayed integers have actual square representations at \(c=2,d=0\).

```python
from math import isqrt
c_mod,d_mod=14437830,1312530
C=288756600
def d_phase(j): return d_mod*(j*pow(d_mod,-1,31)%31)
P=(20771,40487)
for p,U,V,g,k in ((20771,335,335,1758,6),(40487,653,1306,33068,7)):
    assert all(p%j for j in range(2,isqrt(p)+1))
    for base,m in ((3,U),(5,V)):
        o=31*m
        assert pow(base,o,p)==1
        assert all(pow(base,o//l,p)!=1 for l in (2,5,31,67,653) if o%l==0)
    assert c_mod%U==d_mod%V==C%c_mod==0 and C%31==1
    H={pow(3,c_mod*j,p) for j in range(31)}
    assert H=={pow(5,d_phase(j),p) for j in range(31)} and len(H)==31
    assert pow(5,d_phase(1),p)==g and pow(3,C,p)==pow(g,k,p)
    assert {x for x in H if (2-x)%p in H}=={1}
    assert pow(5,p-1,p*p)==1 and pow(3,p-1,p*p)!=1
X=(9752781853725239220214221361,6578376574912837139033024437)
Y=(11075246640031221347570696376,10819062133018046639052260688)
for typ,(x,y) in enumerate(zip(X,Y)):
    N=10+x*x+y*y
    forb=[{j for j in range(31)
           if pow((N-pow(5,d_phase(j),p))%p,31,p)==1} for p in P]
    assert forb==([{6},{7}] if typ==0 else [{0,1},{0,1}])
    for p,label in zip(P,(6,7)):
        c,d=(C,d_phase(label)) if typ==0 else (0,d_phase(1))
        assert (N-pow(3,c,p*p)-pow(5,d,p*p))%(p*p)==p
    def rem(c,d,m):return (N-pow(3,c,m)-pow(5,d,m))%m
    d=next(d_phase(j) for j in range(31) if j not in set.union(*forb) and rem(0,d_phase(j),31**2) in range(31,31**2,31))
    c=c_mod*next(i for i in range(31**2) if rem(c_mod*i,d,31**3)==31**2)
    assert all(rem(c,d,p) for p in P)
print("OK")
```

These controls fully exhaust the shared 31-primary component, not all exponents. Neither is an all-exponent obstruction.
