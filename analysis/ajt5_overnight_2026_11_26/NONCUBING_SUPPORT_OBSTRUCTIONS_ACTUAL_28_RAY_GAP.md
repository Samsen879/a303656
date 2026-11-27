# Actual non-cubing support obstructions in the largest 28-ray gap

The [28-ray catalogue](https://github.com/Samsen879/a303656/commit/31be464193ce17f59e13a9fd8964b3e3ce17d257) normalizes phases to \([18,54)\). Its largest open gap is \((34,110/3)\). This note verifies the exact support gate for all fifth and twenty-fifth proposed steps from these phases, and five definitive exclusions for the named \(7,17,19\) representatives. It does not claim an exhaustive exclusion of all unequal exponent choices at a matching phase, nor that all possible interior rays fail. The full catalogue's effective exponent \(51/110\) is unchanged.

Let \(A=5^u>B=3^v\) for positive odd \(u,v\), and let \(r\) be a positive odd multiplier. For any odd inert prime \(p\equiv2\bmod3,\ p\ne5\), put \(T_p=\operatorname{lcm}(\operatorname{ord}_p(25),\operatorname{ord}_p(9))\) and write \(25^{T_p}\equiv1+pc_5,\ 9^{T_p}\equiv1+pc_3\bmod p^2\). If \(T_p\mid r\) and \(A^{2r}-B^{2r}\) is a norm \(x^2+3y^2\), then \(c_5u\equiv c_3v\bmod p\) and \(p\nmid r\). If the congruence fails, the valuation at \(T_p\) is one, and hence the initial valuation at the exact ratio order is one since \(p\nmid T_p\). It persists under extra multipliers by [the native inert forcing chain](https://github.com/Samsen879/a303656/commit/4020a67a75d39843dac87cdb5cd1a5ca693abd43), whose proof only needs the homogeneous squared bases to be units at \(p\), the second base to be divisible by 3, and the first base to be \(1\bmod3\). If \(p\mid r\) directly, the first new shell at the exact ratio order times \(p\) has \(p\) once as sole possible nonprimitive prime; its residue \(1\bmod3\) forces a larger primitive inert prime of odd valuation, initiating the same chain.

At \(p=11\), \(T_p=5,(c_5,c_3)=(7,0)\). For any fifth-divisible multiplier, \(11\mid u\) and \(11\nmid r\). Only catalogued phases \(22,110/3\) have numerators divisible by 11. Neither their fifth nor their twenty-fifth steps enter the gap. The positive control is \(u=11,v=3,r=5\), which reaches the endpoint \(110/3\) and has two exact half-norm certificates at its starting and final height. The explicit phase scan and primitive order/valuation proof below check the five \(7,17,19\) candidates. The other appearance of \(950/27\) under fifth or twenty-fifth multiplication is ruled out by the support gate, not by assuming equal phases have equal upper exponents.

The candidate \((u,v,r)=(13,5,37)\) at \(962/27\) starts from a true half-norm seed; its extension remains unresolved here. Swapping the first and third numbers to \((37,5,13)\) gives the same phase and fails by the exact primitive inert prime \(53\). This is a same-phase scope control, not a claim that the candidate succeeds.


```python
from fractions import Fraction as F
from math import isqrt
P=list(map(F,("18 166/9 170/9 178/9 182/9 62/3 190/9 22 70/3 74/3 26 "
 "82/3 86/3 30 290/9 34 110/3 38 118/3 122/3 42 130/3 134/3 46 "
 "142/3 50 470/9 158/3").split()))
def phase(a):
    while a>=54: a/=3
    return a
def inside(r):
    return [(p,phase(p*r)) for p in P if 34<phase(p*r)<F(110,3)]
assert {(p,r) for p in P for r in (5,25) if 34<phase(p*r)<F(110,3)}=={
    (F(62,3),5),(F(190,9),5),(F(38),25),(F(118,3),25)}
assert all(p.numerator%11 for r in (5,25) for p,_ in inside(r))
assert [(r,p,z) for r in (7,17,19) for p,z in inside(r)]==[
    (7,F(134,3),F(938,27)),(7,F(46),F(322,9)),
    (17,F(166,9),F(2822,81)),(17,F(170,9),F(2890,81)),
    (19,F(50),F(950,27))]
assert [(pow(b,5,121)-1)//11 for b in (25,9)]==[7,0]
for u,v,r,p in [(67,83,7,3767),(69,85,7,4733),(83,27,17,1689053),
                (85,31,17,137),(75,11,19,520031),(37,5,13,53)]:
    assert p%3==2 and all(p%d for d in range(2,isqrt(p)+1))
    z=pow(25,u,p)*pow(pow(9,v,p),-1,p)%p
    assert z!=1 and pow(z,r,p)==1
    h=(pow(5,2*u*r,p*p)-pow(3,2*v*r,p*p))%(p*p)
    assert h and h%p==0
for u,v,x,y,z,w in [
    (11,3,214,1421,4807,660),
    (55,15,519972140161437256,3387432582010160909,5672065516204784191,5961139456458111376),
    (13,5,7217,5788,24329,2480),
]:
    assert 8*(x*x+3*y*y)==5**u+3**v
    assert 2*(z*z+3*w*w)==5**u-3**v
assert phase(F(110))==F(110,3)
assert phase(F(2*13*37))==F(962,27)
```
