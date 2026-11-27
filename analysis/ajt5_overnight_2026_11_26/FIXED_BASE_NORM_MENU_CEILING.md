# An annular coverage ceiling for fixed-base norm menus

Suppose n in [X,2X) is certified by 3^c,5^d<=n/4 and n−3^c−5^d=D U, with a divisor menu and a cofactor set. For each U, D is in [X/(2U),2X/U]. There are O((log X)^2) offsets, so total coverage is at most that factor times the sum, over U, of the number of available divisors in these annuli. This is an upper bound even when the divisor is selected after n is known.

For binomials with two fixed exponential bases, positive fixed coefficients, and fixed denominators, the larger term has only O(1) exponent choices in a given multiplicative annulus, and the smaller has O(log X). Thus for a cofactor set of size K the menu covers at most O((log X)^3 K). Even using every divisor of polynomial-height binomial seeds only yields X^(o(1)) targets for polylogarithmically many cofactors, by the divisor bound. If one instead uses norm coordinates with one unrestricted integer and the other in a catalogue of H(Y) values at norm height Y, an annulus contains at most O(sqrt(Y) H(Y)) such values. Positive-proportion coverage with polylogarithmically many cofactors would need a restricted-coordinate catalogue of size almost X^(1/2) in at least one annulus. This is a necessary capacity test, not a congruence coverage guarantee.

The logarithmic bound is attained in the following sparse bands. For large even m set B=5^(2m), X=mB/2. Choose odd a in [m/4,m/3], odd c in [1,m/4], even d in [m,3m/2], and U in [m,2m) with U=1 mod 24. Put D=(3^(2a)+B)/2 and n=UD+3^c+5^d. The two norm coordinates (5^m±3^a)/2 are coprime and D=5 mod 8. The target lies in [X,2X) and is 9 mod 24. The disjoint bands determine m; division of 2n by B recovers U; the largest power of 5 in half the tail recovers 5^d; the largest power of 3 in the quotient of the remaining tail by U recovers 3^(2a). The leftover is twice 3^c. The stated ranges give the needed digit separations for sufficiently large m. Thus the decoding is injective and gives on the order of m³ K targets for K allowed U. Keeping only norm U gives true two-square remainders by composition, and the small-cofactor inert-prime test of ADAPTIVE_GAUSSIAN_DIVISOR_BANDS.md applies. The covered fraction still tends to zero.

```python
from math import gcd

def largest_power(x, g):
    assert x >= 1
    e, v = 0, 1
    while v*g <= x:
        e, v = e+1, v*g
    return e, v

def recover(n):
    m, B = 16, 5**32
    while (m+2)*625*B <= 2*n:
        m, B = m+2, 625*B
    U, h = divmod(2*n, B)
    d, p5 = largest_power(h//2, 5)
    h -= 2*p5
    e, p9 = largest_power(h//U, 3)
    c, p3 = largest_power((h-U*p9)//2, 3)
    assert h == U*p9+2*p3 and e%2 == 0
    return m, e//2, c, d, U

D = (3**70+5**240)//2
for t in (193,217):
    n = 3**23+5**140+t*D
    m,a,c,d,U = recover(n)
    assert (m,a,c,d,U) == (120,35,23,140,t)
    u,v = (5**m+3**a)//2, (5**m-3**a)//2
    R = n-3**c-5**d
    assert n%24 == 9 and 4*max(3**c,5**d) < n
    assert u*u+v*v == D and gcd(u,v) == 1 and D%8 == 5
    assert R == U*D
    if U == 193:
        assert R == (12*u-7*v)**2+(7*u+12*v)**2
    else:
        assert R%7 == R%31 == 0 and R%49 and R%961
print("Target-only divisor recovery, true norm, and exact negative control verified")

# Independent grid checks for distinctness within manageable height bands.
for m0 in (24,48):
    B0=5**(2*m0)
    X=m0*B0//2
    seen=set()
    for a0 in range((m0+3)//4,m0//3+1):
        if a0%2==0: continue
        for c0 in range(1,m0//4+1,2):
            for d0 in range(m0,3*m0//2+1,2):
                for U0 in range(m0+(1-m0)%24,2*m0,24):
                    n0=U0*((3**(2*a0)+B0)//2)+3**c0+5**d0
                    assert X<=n0<2*X and n0%24==9 and n0 not in seen
                    assert recover(n0)==(m0,a0,c0,d0,U0)
                    seen.add(n0)
    assert seen
print("Independent small-band decoding and uniqueness checks passed")
```
