# Recover a large primitive Gaussian divisor from a target band

For odd m>=3 put D=(5^(2m)+1)/2. It is the sum of squares of (5^m+1)/2 and (5^m−1)/2, consecutive integers, hence has no inert prime divisor. It is odd and nonsquare, being 5 mod 8.

The bands mD<=n<2mD are disjoint and recover m from the target. Divide n by D to get quotient U and residue r. Accept r=3^c+5^d with odd 1<=c<=floor(m/2) and even ceil(m/2)<=d<=m. The largest power of 5 at most r recovers 5^d, since 3^c<5^d, then the difference recovers 3^c. These offsets are below D. With U=17 mod 24 we have n=9 mod 24, and the remainder D U has cofactor m<=U<2m. If every inert prime at most floor(sqrt(2m)) has even valuation in U, then U is a norm: because U=1 mod 4, a failure would need at least two distinct larger inert primes, whose product is too large. The two original powers are both smaller than n/4.

For sufficiently large odd m there are on the order of m² distinct accepted exponents and residues. Taking U=s²+1 with s=4 mod 12 in the quotient band gives on the order of sqrt(m) coefficients, and thus at least a constant times m^(5/2) certified targets. This is sparse: even allowing all active exponents, the number of offset residues is O(m²), limiting band coverage by this one divisor to O(m²/D). Also ord_D(5)=4m: 5^(2m)=-1 mod D, and any proper divisor of 4m other than 2m is smaller than 2m, where 5^d−1<D. At the actual height n<5^(4m), each fixed c can therefore match at most one compatible d.

At m=109 the real offset (35,80) gives positive controls with U=185=13²+4² and a threshold negative control with U=209=11*19. Both pass the inert panel through 7. Gaussian multiplication certifies the positive remainder directly; the other has exact odd valuations at the first two omitted inert primes. This proves a restricted constructive family only, without changing the density or all-target conclusions.

```python
def largest_power(x, base):
    assert x >= 1
    e, p = 0, 1
    while p*base <= x:
        e, p = e+1, p*base
    return e, p

def extract(n):
    m, w = 1, 25
    while (m+2)*((625*w+1)//2) <= n:
        m, w = m+2, 625*w
    D = (w+1)//2
    U, r = divmod(n,D)
    assert m <= U < 2*m and U%24 == 17
    d, p5 = largest_power(r,5)
    c, p3 = largest_power(r-p5,3)
    assert r == p3+p5 and 1 <= c <= m//2 and (m+1)//2 <= d <= m
    assert c%2 == 1 and d%2 == 0 and 4*max(p3,p5) < n
    return m,c,d,D,U

for t in (185,209):
    n = 3**35+5**80+((5**218+1)//2)*t
    m,c,d,D,U = extract(n)
    assert (m,c,d,U) == (109,35,80,t)
    assert n%24 == 9 and D%8 == 5 and n.bit_length() == 513
    a,b = (5**m+1)//2, (5**m-1)//2
    R = n-3**c-5**d
    assert R == D*U and D == a*a+b*b
    assert R%3 and R%7
    if t == 185:
        assert R == (13*a-4*b)**2+(4*a+13*b)**2
    else:
        assert U == 11*19
        assert R%11 == R%19 == 0 and R%121 and R%361
print("Recovered both divisors and exponents; verified norm and threshold failure")

# Independent recognition and distinctness checks in several bands.
for m0 in (17,31,109,193):
    D0=(5**(2*m0)+1)//2
    assert 2*m0*D0 < (m0+2)*(5**(2*m0+4)+1)//2
    assert D0%24==13 and pow(5,2*m0,D0)==D0-1
    assert all(pow(5,k,D0)!=1 for k in range(1,2*m0))
    pairs=[(c,d) for c in range(1,m0//2+1,2)
           for d in range((m0+1)//2,m0+1) if d%2==0]
    assert len({3**c+5**d for c,d in pairs})==len(pairs)
    U0=m0+(17-m0)%24
    if U0<2*m0:
        for c,d in pairs:
            assert extract(D0*U0+3**c+5**d)==(m0,c,d,D0,U0)
print("Adaptive recognition independently checked across disjoint bands")
```
