# A mixed-axis read can exclude a real source that neither pure axis excludes

For a native order-343 root x and 7-unit F, let b=3^u5^v, A=b^(49F), z=x^(49F). A coarse tag (e,k) requires A=z^((ue+vek) mod 7) on any admissible prime. Prior to using this implication with an F intended to erase the non-7 component, verify coverage b^(2401F)=1 on the block. The gcd of the product of candidate differences implements a union over tags on covered prime support; independent axes must retain tag identity if combined.

The whole true source (149,11) has two e residues {1,5}. Base 3 alone has full coverage and candidate gcd 1. Removing 4127 leaves candidate gcd 1 but loses a real sign-gate prime, so that smaller exponent fails to certify the whole source.

The true (14,83) remainder has projected tags {(1,1),(6,6)}. A certified prime 502280207962079 gives a full first-axis match for one coarse tag and a full second-axis match for a different tag. Thus every pure power of either individual covered read still has at least one legal candidate on that prime. The actual mixed base 15 uses projected residues {2,5}, has full coverage, and its candidate gcd is 1, excluding the entire identified remainder. Removing 618923831 likewise gives false confidence if one ignores coverage. Verification below uses modular arithmetic plus exact resultant/menu regeneration; discovery of the exponent used known integer splits. There is no universal discovery procedure or arbitrary-n conclusion.

```python
from math import gcd, isqrt, prod
from sympy import symbols, resultant

def menu(target):
    out = set()
    for a in range(36,343,49):
        g,h = (pow(b,a+343*(-a%6),2401) for b in (3,5))
        inv = {pow(h,j,2401):j for j in range(343)}
        for u0,I,J in ((17,(33,12,47),(39,11,46)),
                       (24,(40,5,26),(46,4,25)),(38,(5,40,33),(11,39,32))):
            for u in range(u0,343,49):
                for v in range((1-u)%7,343,7):
                    w = inv[(pow(h,v,2401)+pow(g,u,2401)-pow(g,u+1,2401))%2401]
                    if v%49 in I or w%49 in J:
                        continue
                    for k in range(1,343):
                        if not k%7:
                            continue
                        P,Q = (0,k*v-u),(1,k*w-u)
                        b,c,d = min(((S[1-i]-S[i])*t%343,(T[1-j]-S[i])*t%343,d)
                            for S,T in ((P,Q),(Q,P)) for i in (0,1) for j in (0,1)
                            if (d:=(T[j]-S[i])%343)%7 for t in [pow(d,-1,343)])
                        if (b,c)==target:
                            out.add((pow(a*d,-1,343)%49,k))
    return out

from math import gcd, isqrt, prod

def read(n,x,F,b,S):
    assert F%7 and gcd(n,b)==1
    A=pow(b,49*F,n)
    z=pow(x,49*F,n)
    return gcd(n,pow(A,49,n)-1), gcd(n,prod(A-pow(z,r,n) for r in S))

R=1074371768446207135818266115803395888627338703111368059
x=818132082190313776589802800642746690113454285520427524
p,q=7814334187802563,137487307635652428200953519838139221993
F=24417137309193648266870834816474793794675218104
assert p*q==R and p%1372==687
assert pow(x,343,R)==1 and gcd(R,pow(x,49,R)-1)==1
assert (1-x+pow(x,149,R)-pow(x,11,R))%R==0
assert F%4127==0
assert read(R,x,11*17*F,3,{1,5})==read(R,x,F,3,{1,5})==(R,1)
assert read(R,x,F//4127,3,{1,5})==(q,1)

Q=36828898125435086120827238149468646159
y=6372979547770614536168470230517270604
p,q=502280207962079,73323410999733406157521
E=11180016746373599434824816717480
assert p*q==Q and p%1372==687
assert pow(y,343,Q)==1 and gcd(Q,pow(y,49,Q)-1)==1
assert (1-y+pow(y,14,Q)-pow(y,83,Q))%Q==0
assert read(Q,y,E,3,{1,6})==read(Q,y,E,5,{1,6})==(Q,p)
assert read(Q,y,E,15,{2,5})==(Q,1)
assert E%618923831==0
for b,S in ((3,{1,6}),(5,{1,6}),(15,{2,5})):
    assert read(Q,y,E//618923831,b,S)==(q,1)

ell=618923831
assert all(ell%d for d in range(2,isqrt(ell)+1))
assert ell*ell>p and (p-1)%ell==0 and pow(2,p-1,p)==1
assert gcd(p,pow(2,(p-1)//ell,p)-1)==1
assert 274%49==29 and pow(3,E,p)==pow(y,274*E,p)
assert 293%49==48 and pow(5,E,p)==pow(y,293*260*E,p)

t=symbols("t")
for a,b,mod,r,tag in ((149,11,R,x,{1,5}),(14,83,Q,y,{(1,1),(6,6)})):
    z=resultant(sum(t**i for i in range(0,343,49)),1-t+t**a-t**b,t)
    assert z%(7*mod)==0
    if mod==R: assert z==7*mod
    W=menu((a,b))
    assert ({e%7 for e,k in W} if mod==R else {(e%7,e*k%7) for e,k in W})==tag
    if mod==Q: assert {(29,8),(48,260)}<=W
    for j in range(1,343):
        if j%7:
            y0=pow(r,j,mod)
            assert gcd(1-y0+pow(y0,a,mod)-pow(y0,b,mod),mod)==(mod if j==1 else 1)
print("PASS")
```
