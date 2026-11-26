# Sign protection against zero fibres in exact finite norm obstructions

**A sign choice removes an entire class of zero-fibre obstructions from the exact finite-modulus test.** On the actual \(7,19\to\{9603931,32913511\}\) panel, one parity sector loses all four cells to an aligned zero reader. At the same target, a second parity sector makes that reader a unit throughout and leaves three cells passing the exact square-sum modulus. [Pinned two-relay classification](https://github.com/Samsen879/a303656/commit/f11897ee7d1061b073ab30329242cc93df5593b0)

### Separate the two costs

For a modulus factor \(q^e\) with \(q\equiv3\bmod4\), a residual is rejected exactly when its residue is nonzero and has odd valuation below \(e\). At a nonzero observation \(n\bmod q\), the rejected cells are contained in the Sidon hit set, so its difference bound applies at every finite depth. At a zero observation the rejected cells are contained in the quotient fibres. Those fibres can cost the whole palette.

Fix the exponent parities \((\epsilon,\delta)=(c\bmod2,d\bmod2)\). A zero observation at \(q>3\) is automatically a **unit residual throughout the sector** if
\[
\left(\frac3q\right)^\epsilon=\left(\frac5q\right)^\delta.
\]
Indeed, \(3^c=-5^d\bmod q\) would require opposite quadratic characters because \((-1/q)=-1\). Thus the palette budget charges the union of the remaining zero fibres and the Sidon caps of the nonzero readers separately. [Exact prime-power square-sum test](https://github.com/Samsen879/a303656/blob/1c648df/analysis/ajt5_overnight_2026_11_26/EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md)

### Consequence for a finite obstruction

Suppose a parity sector satisfies
\[
n-3^\epsilon-5^\delta\bmod8\ \in\ \{0,1,2,4,5\}.
\]
If every inert prime \(q>3\) with \(q^2\mid M\) that is Wieferich to both bases divides \(n\) and satisfies the sign equality above, then \(n\) has a representation modulo \(M\) in that sector.

To obtain the seed at \(3\), take \(c\ge3\) and choose \(d\) in its specified parity class modulo 18. If the residual is divisible by 3, powers of \(25\) let it be set to \(9\bmod27\). At 2, varying \(c\) by 2 runs through the four lifts of \(3^c\bmod8\) modulo 32. This lets residual classes 0 and 4 be set to \(8\bmod32\) and \(4\bmod16\), respectively. The other admitted classes already pass. At the remaining ordinary inert rows, process primes in increasing order. If a row is hit, vary an ordinary base on that row with a step preserving the seed and all earlier tests. The step is prime to the current prime after taking a multiple of its order, so the principal-unit motion gives exact valuation two. The sign-protected rows stay units throughout. CRT joins the local square coordinates. [Ordinary-axis lifting](https://github.com/Samsen879/a303656/blob/bf3bcc076b383913a1c9d8790122fb70e29ebb4c/analysis/ajt5_overnight_2026_11_26/FIXED_PANEL_EVEN_VALUATION_CONSTRUCTION.md)

There is a stronger necessary condition on a restricted class. **If \(n\not\equiv1\bmod3\) and either \(n\equiv3\bmod4\) or \(n\equiv4\bmod8\), an all-exponent obstruction needs at least eight common Wieferich primes with \(q\nmid n\).** On the even-even sector the 2-adic test passes for every even \(d\), and row 3 is inactive. Choose even \(c\bmod30\) to mute row 31. Then use the pinned ordinary-base-3 correction at each base-5-only exceptional row while preserving \(c\bmod30\). On the resulting fixed-\(c\), even-\(d\) slice, common Wieferich primes dividing \(n\) supply no rigid seeds by the sign test. The pinned eight-seed bound therefore counts only nonzero observations on this slice. [Fixed-slice eight-seed bound and correction](https://github.com/Samsen879/a303656/blob/1c648df/analysis/ajt5_overnight_2026_11_26/EXACT_MODULUS_BRIDGE_COMMON_EXCEPTION_BOUND.md)

### Actual panel and replay

Both relays are rooted in the odd-\(c\), even-\(d\) sector. The even-\(c\), odd-\(d\) sector keeps the exact repair at 7 and makes 19 a unit. The zero reader \(9603931\) then costs zero cells. The nonzero reader \(32913511\) costs exactly one cell in the four-cell palette. Both readers are ordinary controls. [Known two-relay orders](https://github.com/Samsen879/a303656/blob/a9560b603bc37767b1d6e9afd3c79445f000c2f5/analysis/ajt5_overnight_2026_11_26/JOINT_QUOTIENT_TWO_ALIGNED_SOURCES.md)

```python
from itertools import product
from math import isqrt, lcm, prod

p,t,r,s = 7,19,9603931,32913511
assert all(z%4==3 and all(z%d for d in range(2,isqrt(z)+1))
           for z in (p,t,r,s))
D = lcm(8,p*p*(p-1),t*t*(t-1),r*(r-1),s*(s-1))
C = prod(z*((z-1)//2) for z in (p,t,r,s))

def step(m):
    b = D//m
    return b*pow(b,-1,m)

U,V = step(p*p),step(t*t)
assert U%(t*t*(t-1)) == V%(p*p*(p-1)) == 0
assert U%8 == V%8 == 0
for q,W,k in ((p,U,1),(t,V,11)):
    assert pow(3,W,q*q)==pow(5,k*W,q*q)!=1
    for z in (r,s):
        assert q*W%(z*(z-1))==0
        assert pow(3,W,z*z)==pow(5,k*W,z*z)!=1

for z in (p,t,r,s):
    assert pow(3,C,z*z)==z*z-1
    assert pow(3,D,z*z)==pow(5,D,z*z)==1
    assert pow(5,C,z*z)==(z*z-1 if z==p else 1)
assert all(pow(b,z-1,z*z)!=1 for z in (r,s) for b in (3,5))

def total(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

pairs = ((0,p*p),(0,t*t),(r,r*r),
         ((total(D+U,C+U,s*s)+s)%(s*s),s*s),
         ((total(D,C,32)+8)%32,32),(0,27))
M = prod(m for _,m in pairs)
n = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs)%M
assert n==41184447183008253571556007453044574

def rem(c,d,m):
    return (n-total(c,d,m))%m

for good in (False,True):
    for x,y in product((1,2),(0,1)):
        c,d = (D,C) if good else (C,D)
        c,d = c+U*x+V*y,d+U*x+11*V*y
        for q,W in (((p,U),) if good else ((p,U),(t,V))):
            assert rem(c,d,q*q)==0
            if rem(c,d,q**3)==0:
                c+=q*W
            assert rem(c,d,q**3) in range(q*q,q**3,q*q)
        assert rem(c,d,3)!=0
        if good:
            assert rem(c,d,32)==8 and rem(c,d,t)!=0 and rem(c,d,r)!=0
            if (x,y)==(1,0):
                assert rem(c,d,s*s)==s
            else:
                assert rem(c,d,s)!=0
        else:
            assert rem(c,d,8)==2 and rem(c,d,r*r)==r and rem(c,d,s)!=0
assert {pow(25,j,27) for j in range(9)}=={x for x in range(27) if x%3==1}
for n in range(32):
    if n%4==3 or n%8==4:
        for c in range(0,8,2):
            for d in range(0,8,2):
                v=(n-pow(3,c,32)-pow(5,d,32))%32
                if n%4==3: assert v%4==1
                else: assert v%8==2
print("OK")

```

A single sufficiently large lift of the target by a multiple of \(32\cdot27\cdot7^3 19^3 r^2s^2\) makes all the tested remainders positive. The three passing cells give square-sum residues at that exact modulus. Their integer residuals still require the other inert-prime valuations to prove genuine square sums.

### Applying the newer source bound within the same sector

The eight-source consequence in the text uses only the older modulus bridge. On this same restricted class of integers, the newer [fifteen-source proof](RANK_SEVEN_FOURTEEN_SOURCE_ESCAPE.md) applies as well. Keep both exponent parities even: the assumed modulo-8 condition preserves the 2-adic norm test on this entire sector, while \(n\not\equiv1\bmod3\) keeps row 3 inactive at every positive even \(c\). The simultaneous muting of rows \(31,5167,71,19531\) preserves the fixed even parity of \(d\) and the reservation for \(c\). The singly exceptional lifts still preserve that reservation. Every common-exception row dividing \(n\) remains a unit by the sign test and therefore supplies no rigid source. All four pivot exclusions in the fifteen-source proof and its all-linear count use the number and order positions of actual rigid sources on precisely such a slice. Thus **at least fifteen common-exception primes not dividing \(n\)** are necessary on this restricted class. No claim is made about those primes existing or about a specified integer having a genuine square-sum witness.