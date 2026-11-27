# A mixed direction needs full 343 precision on a real source remainder

With the original capture exponent verified and fixed, the order-7 two-axis chart may be viewed as points a_p in F_7² and a set S of projected labels. If a_p belongs to S, no number of order-7 linear reads eliminates that matching tag. Otherwise each nonzero a_p−s forbids one of the eight projective directions, and one directional read suffices if their union does not exhaust those directions. Two independent reads always distinguish the point from each incorrect tag, but only if they are applied to the same tag before taking the union over tags.

At order 49 suppose the same tag actually matches and write the full actual logarithm vector as e(1,k)+49δ modulo 343. A direction w matches some high digit iff w·δ=j w·(1,k) mod 7 for some j. If the full vector fails that tag, the only projective direction capable of eliminating it is perpendicular to (1,k) mod 7: for every other direction the scalar equation always has a j. This makes distinct full-depth matching directions potentially necessary; it also explains why strengthening just the order without direction choice may not help.

For the actual (32,305) remainder Q the independently reconstructed menu is {(25,27),(31,97),(31,146),(31,244)}. The certified prime 8756387804994449437096567 has logs (74,136), matching the first tag modulo 49, but its full lift E=74 predicts the second log 283 modulo 343. All k are 6 mod 7, hence use w=(1,1), base 15. On the whole specified remainder the certified exponent F has full base-15 primary coverage and the three candidate gcds are p,p,1 for precisions 7,49,343. This excludes the stated chart remainder, not arbitrary n. A different native source may not admit the same direction or any usable supplied exponent.

```python
from math import gcd, isqrt, prod

Q=1226529180174843075531420358020848179
x=329367279535621018558882955258773074
p=8756387804994449437096567
F=248222047941250322838116481372
T=((25,27),(31,97),(31,146),(31,244))

proof={p:[2728072661359,82086187],
       2728072661359:[132971,2269],82086187:[1009,149]}
def prime(n):
    if n<200000:
        assert n>1 and all(n%d for d in range(2,isqrt(n)+1))
        return
    fs=proof[n]
    f=prod(fs)
    assert f*f>n and (n-1)%f==0 and pow(2,n-1,n)==1
    for l in fs:
        prime(l)
        assert gcd(pow(2,(n-1)//l,n)-1,n)==1
prime(p)
assert Q%p==0 and p%1372==687 and F%7
assert pow(x,343,Q)==1 and gcd(Q,pow(x,49,Q)-1)==1
assert (1-x+pow(x,32,Q)-pow(x,305,Q))%Q==0
assert pow(3,F,p)==pow(x,74*F,p) and pow(5,F,p)==pow(x,136*F,p)
assert (74%49,136%49)==(25,25*27%49) and 74*27%343!=136

for u,v in [(1,j) for j in range(7)]+[(0,1)]:
    b=pow(3,u,p)*pow(5,v,p)%p
    c=u+27*v
    assert pow(b,7*F,p)==pow(x,25*c*7*F,p)
    if c%7:
        j=(u-11*v)*pow(c,-1,7)%7
        assert pow(b,F,p)==pow(x,(25+49*j)*c*F,p)
    else:
        assert (u,v)==(1,1)

assert all(k%7==6 for e,k in T)
A,z=pow(15,F,Q),pow(x,F,Q)
assert pow(A,2401,Q)==1
def survivors(d):
    return gcd(Q,prod(pow(A,d,Q)-pow(z,d*e*(1+k),Q) for e,k in T))
assert [survivors(d) for d in (49,7,1)]==[p,p,1]
```
