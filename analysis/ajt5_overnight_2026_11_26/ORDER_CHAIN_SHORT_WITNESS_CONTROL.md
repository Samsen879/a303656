# An order-chain phase can delay the first local survivor

For d=0 inspect both x−1−3^f and x−5−3^f in f≡1 mod 30. Impose x≡7511586 mod 271³ and x≡0 mod 1627³. The orders of 3 are 30 and 1626 respectively, and 271 is ordinary for base 3. In this phase the coarse period is 8130. At 271 the short-side residual modulo 271² is zero only when f≡8101 mod 8130; otherwise its valuation is exactly 1. The surviving class can be witnessed at f=8101 with an even valuation of 2. At 1627 both residuals are units on that first index. Thus the actual smallest nonnegative simultaneous locally even index is 8101, not a small fraction of the coarse period.

```python
from math import isqrt
p,q=271,1627
assert all(all(s%d for d in range(2,isqrt(s)+1)) for s in (p,q))
assert pow(3,30,p)==1 and all(pow(3,30//d,p)!=1 for d in (2,3,5))
assert pow(3,1626,q)==1 and all(pow(3,1626//d,q)!=1 for d in (2,3,271))
assert pow(3,30,p*p)!=1
def v(n,p):
    assert n
    j=0
    while n%p==0: n//=p; j+=1
    return j
hits=[f for f in range(1,8130,30)
      if (7511586-5-pow(3,f,p*p))%(p*p)==0]
assert hits == [8101]
assert [v(7511586-a-pow(3,8101,p**3),p) for a in (1,5)] == [0,2]
assert all((-a-pow(3,8101,q))%q for a in (1,5))
```

This is an exact local result for the prescribed class. At a fixed true parent parameter n=m−5^d−3, both child residuals are strictly positive only when 3^f<5n+19 for r=4. Merely raising d does not help this boundary. No claim about the actual norm representation of both residuals, the minimal true-parent height of this class, or unbounded chains with those extra conditions is made here.
