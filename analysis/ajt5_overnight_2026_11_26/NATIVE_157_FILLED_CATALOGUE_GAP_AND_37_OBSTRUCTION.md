# Native index 157 fills the former 28-ray gap, and the 37 candidate is obstructed

The two exact integral half-norms certify an actual new ray from the native seed. The former largest gap of [the 28-ray catalogue](https://github.com/Samsen879/a303656/commit/31be464193ce17f59e13a9fd8964b3e3ce17d257) splits at \(314/9\). The largest ratio is now \(29/27\), at \(30,290/9\), so the effective uniform lower exponent of the augmented sphere construction improves from \(51/110\) to \(27/58\). This is an improvement for actual generated targets in two classes, not a proof for prescribed integers, density one, or an update to the strongest separate coverage-density bound.

The upper-end candidate \((13,5,37)\) instead has exact primitive inert obstruction \(272098451777771\) to valuation one. Its independence from rediscovery is checked by an exact Lucas certificate and direct \(p^2\) arithmetic. Persistence under further odd multipliers follows from [the inert forcing lemma](https://github.com/Samsen879/a303656/commit/4020a67a75d39843dac87cdb5cd1a5ca693abd43). For the smallest-total-exponent assertion, the only smaller odd products in the gap with an odd step r>1 after removing factors of 3 are 53 and 155. The former has actual primitive inert prime 107; in the latter, all placements of a fifth-divisible multiplier fail the [11-support gate](https://github.com/Samsen879/a303656/commit/1f0f7e9f1bd3bff2dfa7ff21f0b276cf4b8f4f01). The remaining placement \(u=5,r=31\) has only \(v=1,3,5,7\), each with an inert valuation-one witness for the base, which remains odd at multiplier 31. No claim is made here about exhaustive exclusion of larger unequal seeds.

The [effective orientation and sphere estimate](https://github.com/Samsen879/a303656/commit/cf322a1000d6a9a387531f53ec7a16f1624996dc) applies to the new odd-exponent seed and hence to its cubed rays. It gives \(\gg_\epsilon Q^{1/2-\epsilon}\) distinct actual targets in each of residues 3 and 21 mod 24 for its native windows \((Q,5Q)\). The same estimate holds for the previous certified rays. Selecting the latest full window below a given bound yields the claimed \(27/58\). Both same-height positives and both failed indicated labels in the replay are exact integer controls.


```python
from fractions import Fraction as F
from math import gcd,isqrt,prod
p=272098451777771
Fct=(2,5,37,283,587,4426901)
assert prod(Fct)==p-1 and p%3==2
assert all(all(q%d for d in range(2,isqrt(q)+1)) for q in Fct)
assert pow(6,p-1,p)==1 and all(gcd(pow(6,(p-1)//q,p)-1,p)==1 for q in Fct)
A,B=5**13,3**5
H,r=divmod(A**37-B**37,A-B)
z=A*pow(B,-1,p)%p
assert not r and z!=1 and pow(z,37,p)==1
assert H%(p*p)==90510437349314*p
G=H//(223*11071807)
assert G*(223*11071807)==H and gcd(pow(2,p-1,G)-1,G)==p

for v,p,z in ((1,17,17),(3,197,23837),(5,11,77),(7,83,1909)):
    assert 3**v<5**5 and p%3==2 and all(p%d for d in range(2,isqrt(p)+1))
    assert (5**10-3**(2*v))%(p*p)==z and z%p==0 and z
assert 3**9>5**5
p=107
a=25*pow(9,-1,p)%p
assert all(p%d for d in range(2,isqrt(p)+1)) and p%3==2 and a!=1
assert pow(a,53,p)==1 and (pow(5,106,p*p)-pow(3,106,p*p))%(p*p)==4387

A,B=5**157,3**157
x,y=3828386844926185621897122075416879034698137738825807,3020435728764877449653512600806505929143255888545590688
a,b=862272495261288964512619431520630418204585718543506297,1425805480158717309073067742724622156371225404177459922
assert 2*(x*x+3*y*y)==A-B and 8*(a*a+3*b*b)==A+B
V,W=8*(x*a-3*y*b),8*(x*b+y*a)
if W%3==0: V,W=(V-3*W)//2,(V+W)//2
Q,Z=A*A,B*B
assert V*V+3*W*W==4*(Q-Z) and W%3
for L,k in ((1,21),(3,3)):
    n=Q+(4-L)*Z+V*V+1
    assert Q<n<5*Q and n%24==k
    assert n-V*V-1==5**314+3**(315 if L==1 else 314)
    t=B+677
    x,y=(t-B,t) if L==1 else (t+B,t-2*B)
    n=5*Q+L*Z-x*x-y*y
    assert Q<n<5*Q and n%24==k
    assert (n-Q-(4-L)*Z)%49==21

g=list(map(F,("18 166/9 170/9 178/9 182/9 62/3 190/9 22 70/3 74/3 26 "
 "82/3 86/3 30 290/9 34 110/3 38 118/3 122/3 42 130/3 134/3 46 "
 "142/3 50 470/9 158/3 54").split()))
assert max(b/a for a,b in zip(g,g[1:]))==F(55,51)
g=sorted(g+[F(314,9)])
assert max(b/a for a,b in zip(g,g[1:]))==F(29,27)
assert F(27,58)-F(51,110)==F(3,1595)
```
