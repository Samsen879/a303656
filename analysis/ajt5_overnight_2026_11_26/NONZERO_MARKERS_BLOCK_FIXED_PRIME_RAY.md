# Nonzero reads can block a whole fixed prime-parameter ray

The [linear zero-read cost bound](https://github.com/Samsen879/a303656/commit/0f7693e7002dd83f0875b0b20535e37b43061252) does not extend to mixed reads on a fixed ray. For actual F(t)=27^t+5^t at primes t=1+720k, one ordinary inert prime suffices on the nonempty target class n≡18 mod 49. The exact powers give 27^720≡29 and 5^720≡43 mod 49. Expanding once to precision 49 gives F(t)≡32+35k. This is always 4 mod 7, while equality to 18 mod 49 is exactly k≡1 mod 7, the class 7|t. It is absent from all large prime parameters. Therefore p=7 marks every prime-ray label at valuation one, at constant modulus cost. The finite control gives a matching true target with valuation two at one same label and shows that moving off the ray within the actual chart can evade p=7.

A related fixed-refinement construction is possible even after prescribing old reads. Pick a new inert prime p not dividing the old finite modulus or original period. Include the orders of 27 and 5 modulo p in a fixed refined period L. The resulting F(1+Lk) modulo p² is affine in k. At nonzero slope, choose the mod-p² read so the sole exception is the class p|t; at zero slope choose a distinct lift modulo p². The refined ray then has the same obstruction. This shrinks the set of parameters and does not cover the entire original chart.

## Two simultaneous nonzero-sector necessary bounds

If one prime hits t,t+h,t+k with 0<h<k, then it divides the nonzero determinant
D=(27^k−1)(5^h−1)−(27^h−1)(5^k−1)<135^k. Positivity follows since (27^j−1)/(5^j−1) is a constant times an increasing weighted mean of (27/5)^i for i<j. Thus a marker can hit at most 2+2W log(135)/log p parameters in an interval of width W, by separating odd and even positions in the ordered hit list. At cost o(H), primes with log p≥sqrt(H log H) cannot supply more than o(H/log H) hits.

For p∤n write r=ord_p(27/5) and ℓ=lcm(ord_p 27,ord_p 5). Two hits in one class mod r must differ by a multiple of ℓ: both powers advance by the same factor, which must be one to preserve a nonzero read. Thus there are at most r hits per period. If ℓ≥ηH and r≤R=o(H^(1/3)), all actual primes in this sector supply at most O_η(R³/log H) hits: for each r they divide 27^r−5^r and are >ℓ, giving O(r/log H) possibilities, each hitting O_η(r) labels. These estimates do not exclude the remaining short nonzero sectors.

## Exact replay

The 7 case is complemented by an actual ordinary 47 marker reusing three distinct mod-46 exponent classes, verified on a matched 319,692-bit target. Both controls retain the stated earlier reads and have witnessed true residuals in the matching targets. This is a result about the selected prime ray, not a cover of the entire chart or an obstruction to every exponent of the original conjecture.

~~~python
from math import gcd, isqrt, lcm, prod

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

def F(t,m=None):
    return 27**t+5**t if m is None else (pow(27,t,m)+pow(5,t,m))%m

def order(a,p):
    x = 1
    for e in range(1,p):
        x = x*a%p
        if x == 1:
            return e
    raise AssertionError

def matched(p,ts,reading):
    H = 12*max(ts)
    assert prime(p) and p%4==3
    assert all(prime(t) and t%720==1 and H<=32*t for t in ts)
    old = [q for q in (7,11,19,31) if q!=p]
    assert all(pow(27,720,q)==pow(5,720,q)==1 for q in old)
    Q = 25*1728*17*prod(q**3 for q in old)
    S = F(ts[0])
    z = (3*2**(H//2-5))//p
    z += (25-z)%30
    good = S+85*p*p*(z*z+16)
    bad = good+Q*((reading-good)*pow(Q,-1,p*p)%(p*p))
    assert bad>good and bad.bit_length()==good.bit_length()==H
    assert (bad-good)%Q==0 and good%8==5 and good%3==1
    assert good%17==S%17 and (good-S)%25==10*(p*p%5)%25
    assert good-S==(p*(7*z-24))**2+(p*(6*z+28))**2
    assert (good-S)%p**2==0 and (good-S)%p**3!=0
    assert all((good-S)%q for q in old)
    for t in ts:
        R = bad-F(t)
        assert R>0 and R%p==0 and R%p**2!=0
    assert bad%p==good%p!=0
    return H,good,bad

assert pow(3,6,49)==43
assert (pow(27,720,49),pow(5,720,49))==(29,43)
assert [k for k in range(7) if F(1+720*k,49)==18]==[1]
H,g,b = matched(7,(2161,),18)
assert 2161%7!=0 and (3*2161-80)*32>=H
assert (b-pow(3,3*2161-80,7)-pow(5,2161,7))%7

p,ts = 47,(16561,19441,26641)
ell = lcm(order(27,p),order(5,p))
assert ell==46 and len({t%ell for t in ts})==3
assert [F(t,p*p) for t in ts]==[878,1865,455]
h,k = ts[1]-ts[0],ts[2]-ts[0]
assert ((pow(27,k,p)-1)*(pow(5,h,p)-1)
        -(pow(27,h,p)-1)*(pow(5,k,p)-1))%p==0
H,g,b = matched(p,ts,32)
assert all((g-F(t))%p==0 and (g-F(t))%p**2 for t in ts[1:])
L = lcm(720,p*(p-1))
assert all(gcd(t,L)==1 for t in ts)
~~~
