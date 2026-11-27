# Parity-filtered intercepts give representation density above 99.964159%

**The exception-density bound improves to below \(0.035841\%\)** at the same cutoff. The outward-rounded result is \(0.035840708\%\). The finite depth-one charge falls from \(0.00005679678\) to \(0.00001531769\) in density units. The other finite and infinite charges carry forward. The numerical saving uses a terminal-blind parity choice and the actual source Legendre signs. It does not require two heads to survive the retained prefix. [Previous distinct-reader certificate](https://github.com/Samsen879/a303656/blob/84fb8015f31b11919dfe54d40d5e54213aa7e560/analysis/ajt5_overnight_2026_11_26/DISTINCT_READER_MOMENT_DENSITY_BOUND.md)

### When the two-head switch works

Fix a retained-prefix phase, and use absolute source digits \(x=c\bmod r\), \(y=d\bmod r\). Put \(A=3^c\bmod r\), \(B=5^d\bmod r\), and \(f_b=(b^{r-1}-1)/r\bmod r\). At a doubly ordinary source the repair slope is \(-Af_3/(Bf_5)\). At a terminal reading both first digits, write the shift as \(C g^x+D h^y\), where \(C,D\) have order prime to \(r\). With \(\mu=\log_h g\), the constant-line test is exactly
\[
\frac AB=\rho:=-\mu f_5/f_3,\qquad C+D=0,\qquad
n_r\equiv [A]+[B]\pmod{r^2}.
\]
Here \([A]\) and \([B]\) are the torsion lifts. The intercept in absolute digits must be zero: the prime-to-\(r\) factors cannot absorb a nontrivial \(r\)-th root of unity.

If two heads have retained-prefix extensions chosen before reading the dropped rows, and their cancellation loci are disjoint, one can switch after reading \(n_r\). The selected repairs are still fixed before the dropped observations, so the distinct-reader moments remain valid. The older alignment allowance must account for both boundaries: a shallow reader can have one exceptional source reading per boundary.

Distinct head classes do not guarantee distinct loci. The ordinary pair \((r,q)=(59,2243)\) has two legal heads \((23,1),(471,1)\bmod3960\) with the **same** constant-line reading \(n_r=1407\bmod3481\). The replay checks the two lines directly. Thus I take no unconditional numerical credit for the switch.

### Unconditional saving from parity and the source ratio

Choose the parity pair \(v=(c\bmod2,d\bmod2)\) using only \(n\bmod32\) and \(n\bmod3\), then run the usual small-head adjustments. The table below gives counts \((40,19,19,18)\) for the pairs \(00,01,10,11\) among the 96 equally weighted observations. The replay verifies legality at \(2\) and \(3\) in every case.

Let \(u_p\) be the pair of Legendre bits of \(3,5\) at \(p\), with bit 1 denoting a nonresidue. Terminal cancellation requires \(u_q\cdot v=1\). The source ratio additionally requires \(u_r\cdot v\) to equal the Legendre bit of \(\rho\). Thus for fixed \(q,r\) the terminal alignment allowance is at most \(\eta_r(u_q)/r^2\), where \(\eta_r(u)\) is the larger parity mass over the two possible signs of \(\rho\), subject to both conditions. In particular:

- \(u_q=00\) excludes cancellation.
- Distinct nonzero \(u_q,u_r\) leave at most one parity pair, of mass at most \(19/96\).
- In all cases the mass is at most \(19/48\). This also multiplies the old shallow-alignment allowance, since those cancellations likewise require a negative Legendre product.

The source condition can be decisive. At the ordinary pair \((83,167)\), the exact ratio is \(\rho=12\), a square modulo \(83\), and both sign pairs are \(01\). The terminal requires \(d\) odd, while the source ratio requires \(d\) even.

For the numerical sum, split the existing \(q\equiv1\bmod r,\ q\equiv3\bmod4\) progression modulo \(60r\). Each terminal sign pair has two residue classes. Use the smaller of the original total reciprocal envelope times \(\max\eta_r\) and the sum of the eight separate progression bounds weighted by \(\eta_r\). The moment term is unchanged. The parity policy is fixed before any terminal or dropped observation is read. [Montgomery–Vaughan progression bound](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED)

### Standalone rational replay

```python
from collections import Counter
from fractions import Fraction as Q
from itertools import product
from math import ceil, floor, isqrt, lcm

W, P = 10**11, 10**5
pairs = dict(zip("0XYZ", product(range(2), repeat=2)))
table = ("XY000Y00", "XZZXZZXX", "YY000Y00")

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p)) % p

def good2(u):
    t = u & -u
    return t and t<=8 and u//t%4==1

counts = Counter()
for n3,n32 in product(range(3),range(32)):
    label = "Z" if (n3,n32) in ((1,0),(0,1)) else table[n3][n32%8]
    a,b = pairs[label]
    assert (n3-pow(5,b,3))%3
    assert any(good2((n32-S(c,d,32))%32)
               for c in range(a,8,2) for d in range(b,8,2))
    counts[a,b] += 1
assert [counts[v] for v in pairs.values()] == [40,19,19,18]

def dot(x,y):
    return sum(a*b for a,b in zip(x,y)) % 2

def sign(p):
    return tuple(int(pow(b,(p-1)//2,p)==p-1) for b in (3,5))

def eta(s,t):
    return Q(max(sum(m for v,m in counts.items()
                     if dot(t,v)==1 and dot(s,v)==k)
                 for k in (0,1)),96)

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s,s+2*z**25/(25*(1-z*z))

l2,u2 = series(Q(2))
def logs(x):
    y,k = Q(x),0
    while y>=2:
        y /= 2
        k += 1
    a,b = series(y)
    return Q(floor(W*(a+k*l2)),W),Q(ceil(W*(b+k*u2)),W)

def hi(x): return logs(x)[1]

def progression(r,m,scale):
    l,u = logs(m*r)
    U,V = Q(4*r,3)-u,34-u
    assert U>V>0
    return (1/U+hi((Q(4*r,3)-l)/V))/(scale*(r-1))

flags = bytearray(b"\x01")*(P+1)
flags[:2] = b"\x00\x00"
for r in range(2,isqrt(P)+1):
    if flags[r]:
        flags[r*r::r] = b"\x00"*((P-r*r)//r+1)

old = new = Q(0)
kappa = Q(19,48)
for r in range(31,P+1,4):
    if not flags[r]:
        continue
    s = (hi(r)+Q(1,2))/(r-1)
    R = min(s,progression(r,4,1))
    old_r = new_r = R/r
    if all(pow(b,r-1,r*r)!=1 for b in (3,5)):
        K = (1+isqrt(4*r-3))//2
        H = r-K
        whole = Q(1,r*r)+(Q(1,r)-Q(1,r*r))*min(1,r*s/H)
        psi = moment = Q(1)
        for j in range(6):
            if H-j*K<=0:
                break
            moment *= r*s/(H-j*K)
            psi = min(psi,moment)
        sh = (1+Q(1,2*r+1))*s
        old_r = R*min(whole,psi/r+(1-psi)*min(Q(1,r),(1+sh)/r**2))
        v = [eta(sign(r),t) for t in pairs.values()]
        A = min(R*max(v),2*progression(r,60,8)*sum(v))
        new_r = min(old_r,R*psi/r+(1-psi)*(A+kappa*sh*R)/r**2)
    old += Q(ceil(W*old_r),W)
    new += Q(ceil(W*new_r),W)

assert (old,new)==(Q(5679678,W),Q(1531769,W))
answer = Q(39988617,W)-old+new
assert answer==Q(35840708,W)<Q(35841,10**8)

# Ordinary controls for the exact ratio test and shared cancellation locus.
def ratio(r,q,L):
    f,g = [(pow(b,r-1,r*r)-1)//r for b in (3,5)]
    m = next(j for j in range(1,r) if pow(5,L*j,q)==pow(3,L,q))
    return m,(-m*g*pow(f,-1,r))%r

assert ratio(83,167,2)==(11,12)
assert sign(83)==sign(167)==(0,1) and pow(12,41,83)==1

r,q,d,n = 59,2243,1,49072891701351441
L = lcm(3960,29,19,38)
assert ratio(r,q,L)==(44,9)
assert all(pow(b,p-1,p*p)!=1 for p in (r,q) for b in (3,5))
for c in (23,4431):
    assert (n-S(c,d,32))%32==1 and (n-pow(5,d,3))%3
    assert all((n-S(c,d,p))%p for p in (7,11,19,23))
    x = c+L*(-c*pow(L,-1,r)%r)
    y = d+L*(-d*pow(L,-1,r)%r)
    for i in range(r):
        a,b = x+L*i,y+L*(44*i%r)
        assert (n-S(a,b,r*r))%(r*r)==0 and S(a,b,q)==0
assert n%(r*r)==1407
print("OK:",float(100*answer),"%")
```

The control primes are ordinary. They verify the exact ratio exclusion and the shared-locus obstruction, while the numerical bound applies without assuming any genuine common Wieferich examples.

The source slope is calculated in absolute primary coordinates: decomposing an ordinary base into its Teichmüller part and its principal part modulo \(r^2\) gives the same factor \(-r\) for the two principal linear terms, leaving the stated quotient of Fermat quotients. The terminal and older-reader parity events are averaged over \(n\bmod 96\) independently of the \(r\)- and reader-prime observations. The retained phase may still depend on \(n\bmod96\); the cancellation criteria are necessary for every such phase, so no independence of the phase itself is assumed. For the terminal progression split, the eight admissible classes modulo \(60r\) split evenly among the four sign pairs and \(\varphi(60r)/\varphi(4r)=8\) for the sources in the replay.
