# An exact factor-gap lower bound for the unresolved (17,188) source

At each prime dividing the actual source R, the native root has exact order 343; hence every integer factor a|R is 1 mod 343. Since R is 3 mod 4, for a factor pair ab=R the product (a−1)(b−1) is divisible by 8·7^6. Thus the candidate sum S=a+b must lie in a single progression S=S0+(8·7^6)j, where S0 is the first eligible value above sqrt(4R), and S²−4R must be a square.

On the entire initial block 0≤j<7^6, the mod 9,25 tests and the 7-adic square test leave 4804 candidates. The subsequent square-residue tests at 11,13,…,53 empty this set. Every factor pair therefore has gap at least 18725675439105696. This conclusion does not depend on either factor being prime.

The exact menu {(5,276),(15,165)} gives a separate condition on a candidate pair whose prime endpoint p would pass the menu. Set T=R+1−S=(a−1)(b−1) and D=3/(5 x^4) mod R. At such a prime p, p−1 divides T, and the first digit relation e(1−k)=4 mod 7 forces D^(49 T_{7'})=1 mod p. A product-gcd on the exact initial 4804 sums rejects them all for such a prime endpoint, as does a separate pure order check. No extra reduction beyond the pure order check is claimed here. The source remains unfactored and is not excluded globally.

```python
from math import gcd, isqrt

R = 626751537547263614426465772417729978972491
x = 252568635021313874012910903862214825457075
assert R%4==3 and pow(x,343,R)==1 and gcd(R,pow(x,49,R)-1)==1
assert (1-x+pow(x,17,R)-pow(x,188,R))%R==0
assert {(e*(1-k))%7 for e,k in ((5,276),(15,165))}=={4}

M=8*7**6
s=1+isqrt(4*R)
s+=(R+1-s)%M
assert s==1583352819238041815588
def disc(j): return (s+M*j)**2-4*R
def gap(j):
    d=disc(j)
    a=isqrt(d)
    return a+(a*a<d)
def v7(d):
    v=0
    while d%7==0:
        d//=7
        v+=1
    return v
def ok7(d):
    v=v7(d)
    return v%2==0 and d//7**v%7 in (1,2,4)

assert isqrt(disc(0))**2!=disc(0) and gap(1)==60360012342528
sq9={a*a%9 for a in range(9)}
sq25={a*a%25 for a in range(25)}
assert {j for j in range(9) if disc(j)%9 in sq9}=={2,5,8}
rs=[j for j in range(75) if j%3==2 and disc(j)%25 in sq25]
assert rs==[11,26,35,41,56,62,71]

B=7**6
C=sorted((j,disc(j)) for r in rs for j in range(r,B,75) if ok7(disc(j)))
assert len(C)==4804 and C[0][0]==26 and gap(26)==279562660994285

D=3*pow(5,-1,R)*pow(x,-4,R)%R
a=b=1
for j,_ in C:
    T=R+1-s-M*j
    a=a*(pow(D,49*(T//7**v7(T)),R)-1)%R
    b=b*(pow(3,T,R)-1)%R
assert gcd(R,a)==gcd(R,b)==1

ds=[d for _,d in C]
counts=[]
for p in (11,13,17,19,23,29,31,37,41,43,47,53):
    sq={z*z%p for z in range(p)}
    ds=[d for d in ds if d%p in sq]
    counts.append(len(ds))
assert counts==[2617,1408,676,326,150,81,33,20,8,5,1,0]
assert gap(B)==18725675439105696
```
