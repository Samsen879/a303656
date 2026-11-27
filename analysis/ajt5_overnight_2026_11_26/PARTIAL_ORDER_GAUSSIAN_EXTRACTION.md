# Partial order tests recover full split prime powers

No verified global order exponent is needed. For an odd positive current cofactor C, chosen base a, odd K and level 1<=j<s, compute h=gcd(C,a^(2^j K)+1). A prime not dividing a is detected iff the odd part of its local order divides K and the two-part equals 2^(j+1). Thus it is split. For h>1, D=gcd(C,h^bit_length(C)) recovers every full prime power in C detected by h. The exponent a^(2^(j−1)K) is a root of minus one modulo each prime dividing D. Newton iteration modulo D doubles the error valuation and is well-defined since the derivative is a unit there. Its resulting root modulo D supplies a Gaussian gcd norm certificate as in ORDER_CHAIN_GAUSSIAN_DESCENT.md. Dividing C by D and continuing cannot double-count factors.

A split prime p with odd part of p−1 dividing K and v2(p−1)<=s is detected if the list includes a quadratic nonresidue there. Base 2 gives this when p=5 mod 8. This is a local smooth-order condition, not a uniform prescribed-target guarantee; the prime powers need not themselves have order dividing the chosen exponent.

On the same target n=5277, bases 3 and 5 with K=9,s=2 extract complementary factors 125 and 37 at (3,4); neither has a^36=1 modulo the remainder. At (3,2), the same tests leave cofactor 209=11*19 with exact odd valuations, reaching the failure threshold. The replay checks genuine full-power lifts and the explicit positive norm 64²+23². No global density or pointwise change follows.

```python
from math import gcd, prod

def extract(R, bases, K, s):
    C, blocks = R, []
    for a in bases:
        t = pow(a,K,R)
        for _ in range(1,s):
            z = t*t % R
            h = gcd(C,z+1)
            if h > 1:
                D = gcd(C,pow(h,C.bit_length(),C))
                x = t % D
                while (x*x+1)%D:
                    x = (x-(x*x+1)*pow(2*x,-1,D))%D
                blocks.append((a,h,D,x))
                C //= D
            t = z
    assert C*prod(D for _,_,D,_ in blocks) == R
    return C,blocks

n = 5277
for d,want in ((4,(1,[(3,5,125),(5,37,37)])),
               (2,(209,[(3,5,25)]))):
    R = n-3**3-5**d
    assert R%4==1 and R%3 and R%7 and 4*max(3**3,5**d)<n
    assert all(pow(a,36,R)!=1 for a in (3,5))
    C,L = extract(R,(3,5),9,2)
    assert (C,[b[:3] for b in L]) == want
    assert all((x*x+1)%D==0 for _,_,D,x in L)
    if d == 4:
        assert R == 64**2+23**2
        assert extract(R,(3,),9,2)[0] == 37
        assert extract(R,(5,),9,2)[0] == 125
        assert extract(R,(3,5),3,2)[0] == 37
    else:
        assert C==11*19 and R%11==R%19==0 and R%121 and R%361
print("Complementary bases, full prime-power lifts, and threshold failure")

# Independent full-power lift check on a larger genuine split factor power.
C,L=extract(5**9*37**4,(3,5),9,2)
assert C==1 and {D for _,_,D,_ in L}=={5**9,37**4}
assert all((x*x+1)%D==0 for _,_,D,x in L)
print("Independent mixed-power Hensel checks passed")
```
