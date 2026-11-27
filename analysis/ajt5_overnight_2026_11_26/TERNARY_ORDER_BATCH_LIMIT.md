# A limitation on ternary-order batching

Use the two columns of GROWING_TWO_COLUMN_PREFIX.md, fixed T=1, and a work prime p>3 different from every auxiliary prime. For odd f both residuals are 3 mod 4, so a batch need only consider f=2t. Set N=floor(F/2)+1. Consider batching with short auxiliary orders n_q=ord_q(9)<N all of the form 3^k, at most 45 distinct primes per level, and any number of long-order primes n_q≥N. Count only the first column S=5p²+10941−9^t; a lower bound there suffices.

Order 1 gives no inert prime. The only inert primes of orders 3,9,27 are 7,19,19927 respectively, by factoring 9^3−1, 9^9−1, 9^27−1. The 7 cannot divide S, since 10941 vanishes modulo 7 and 5 is a nonsquare. The inert prime 3 cannot hit this column either. At any other q there is at most one residue of t modulo n_q for a hit. Even allowing all first-power hits and ignoring parity, short primes cover at most
```
N*(1/9+1/27+45*sum(3^(-k), k>=4)) + O(log N)
= (53/54)*N + O(log N).
```
Each long prime can cover one remaining row at most, and q≥2N+1 because n_q divides (q−1)/2. Thus the logarithm of any successful batch CRT modulus in this restricted strategy is Omega(F log F). This is not a lower bound on mixed short orders or on the real first bridge.

For an actual CRT lift, first-power hits need not agree on consecutive periods. For the second column and p=1847 the residuals at f=10 and f=28 both hit 19, with valuations 1 and 2 respectively. Conversely p=31 has a common 11-hit on the first column at f=8 and the second at f=0, both of valuation 1; the order-5 period of 9 is already frozen mod 121. These assertions, and the short factorizations, can be checked directly:
```python
assert 9**3-1 == 2**3*7*13
assert 9**9-1 == 2**3*7*13*19*37*757
assert 9**27-1 == 2**3*7*13*19*37*109*433*757*8209*19441*19927
def v(x,p):
    j = 0
    while x%p == 0: x //= p; j += 1
    return j
assert (v(5*1847**2+10937-3**10,19),v(5*1847**2+10937-3**28,19)) == (1,2)
assert v(5*31**2+10941-3**8,11) == v(5*31**2+10937-1,11) == 1
assert pow(9,5,121) == 1
```

Even O(F) cost would leave a constant to control: to close all active even exponents, the next even E must satisfy 3^E>5p²+10941−1 (strict variant). A bound p=O(M^L) from a CRT modulus M with log M≤gamma*F+O(1) only suffices automatically when gamma<log(3)/(2L).
