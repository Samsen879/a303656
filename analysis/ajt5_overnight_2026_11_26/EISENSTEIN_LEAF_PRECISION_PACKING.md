# Three distinct Eisenstein leaf-precision requirements

For odd split primes p_i≡1 mod 3 with required powers p_i^e_i, fix a single Eisenstein direction for each prime. Subject only to the leaf norm cap B, the exact multiplicative packing loads are respectively (i) one p_i when a mod-p read may subsequently be Hensel-lifted; (ii) e_i copies of p_i when the total exponent can be accumulated across aligned leaves; and (iii) one indivisible p_i^e_i when the full power must occur in one leaf. Sufficiency here is for norm and orientation only, not independent bounds on coordinates, trace weights, or all aspects of a complete phase.

Indeed the Eisenstein integers are Euclidean for the norm, and a generator above each p_i can be made integral in the basis 1,√−3: mod 2 the maximal order has residue field F4, whose nonzero classes are reached by units. Multiplying by the appropriate unit puts the generator in 1+2O, in the indicated suborder; the norm is unchanged. Products of aligned prime generators have exactly the prescribed norm and remain primitive: no rational split prime divides the element, as that requires both conjugate factors, and the norm is prime to 2 and 3. A primitive coordinate denominator cannot be divisible by any p_i in the norm, since the norm equation would then force both coordinates divisible by p_i. For the first requirement, the simple root mod p_i lifts uniquely since 2r is a unit for r²+3=0. Conversely, leaf norms must be divisible by the selected loads, giving necessity. The recursive exact replay fixes a largest remaining load in its next bin.

For the complete true half H=(5^9−3^9)/2=7²·109·181, the three optimal bin counts are (2,3,3) at B=1000 and (2,2,3) at B=1267. Merely comparing H with B² misses the first failure. The aligned product (863,272) and mixed product (161,560) have the same exact norm H; the latter has common factor 7 and cannot read the mod-49 root by coordinate division.

On the partial true half (5^229−3^149)/2, the selected powers are 7,67²,23827. At B=31000 the three optima are (2,3,3). The finite five-trace menu lacks a simultaneous unique-side read at 7 and 67; τ=18/13 repairs that particular pair at full precision 7·67². The full half remains unclassified.

The replay also checks a negative stage only: 992 of the 1011 labels at U∈{227,229,233} have exact inert-norm vetoes, with 19 labels undecided. An **odd** unit divisor d≡2 mod 3 contains some inert prime to odd exponent; coprimality with the complement certifies that valuation in the full product 25^U−9^V. Its odd prime factors cannot divide both halves since 5 and 3 are coprime. Thus one half fails the norm criterion. This does not assert a new phase or any improvement of the generated-family exponent 45/94.

## Exact Python replay

```python
from functools import lru_cache
from itertools import combinations
from math import gcd,isqrt,prod

def N(a,b):
    return a*a+3*b*b

def mul(z,w):
    a,b=z
    c,d=w
    return a*c-3*b*d,a*d+b*c

def optimum(loads,B):
    @lru_cache(None)
    def count(S):
        if not S:
            return 0
        best=999
        for size in range(len(S)):
            for J in combinations(range(len(S)-1),size):
                if S[-1]*prod(S[j] for j in J)<=B:
                    T=tuple(s for i,s in enumerate(S[:-1]) if i not in J)
                    best=min(best,1+count(T))
        return best
    return count(tuple(sorted(loads)))

H=(5**9-3**9)//2
assert H==966721==7**2*109*181
for B,expected in [(1000,(2,3,3)),(1267,(2,2,3))]:
    loads=((7,109,181),(7,7,109,181),(49,109,181))
    assert tuple(optimum(S,B) for S in loads)==expected
assert N(16,13)==763 and N(13,2)==181 and N(32,9)==1267
good,bad=mul((16,13),(32,-9)),mul((16,13),(32,9))
assert (good,bad)==((863,272),(161,560))
assert N(*good)==N(*bad)==H and gcd(272,H)==1 and gcd(*bad)==7

H=(5**229-3**149)//2
assert all(H%p**e==0 and H%p**(e+1)!=0 for p,e in ((7,1),(67,2),(23827,1)))
assert N(13,10)==469 and N(8,89)==23827
d=gcd(H,pow(gcd(H,469),H.bit_length(),H))
r=13*pow(10,-1,d)%d
r=(r-(r*r+3)*pow(2*r,-1,d))%d
assert (d,r)==(31423,16557) and (r*r+3)%d==0
loads=((7,67,23827),(7,67,67,23827),(7,4489,23827))
assert tuple(optimum(S,31000) for S in loads)==(2,3,3)

T=[(-1,3,21,29),(1,3,21,25),(2,3,3,11),(2,1,7,15),(4,5,35,3)]
assert [(a,b) for a,b,t,s in T if gcd(t*s*b,7)==1]==[(2,3)]
tau=2*pow(3,-1,67)%67
X=[x for x in range(67) if ((2*tau*tau-1)*x**3
   -(2*tau**3-1)*x*x+tau**3-tau*tau)%67==0]
assert X==[18,23,52]
assert all(((1-x**3)**2-(1-x*x)**3)%67 for x in X)

a,b=18,13
t,s=b*(2*a*a-b*b),2*a**3-b**3
Delta=(a-b)*(8*a**3-3*a*b*b-b**3)
assert (t,s)==(6227,9467)
assert all(pow(Delta,(p-1)//2,p)==p-1 for p in (7,67))
k=t*s*pow(b**3*r,-1,d)%d
assert k==11362 and gcd(H,(t*s)**2+3*b**6*k*k)==d
for q,other in ((7,5),(4489,2110)):
    dif=[]
    for z in (r,-r):
        u=(t+k*z)*pow(2*t,-1,q)%q
        v=(s+k*z)*pow(2*s,-1,q)%q
        dif.append((u*u-v**3)%q)
    assert dif==[0,other]

vetoes={
227:{9:27187973,33:1576521239,57:4966589271767,65:36497,73:284897,
     75:356492806379,105:185310385607877797,187:27653,265:116273,
     267:1752879071033,275:8295317,307:14583303141851,315:9181631,329:22634771},
229:{69:45971,101:310648073,125:69718864224137,189:20814129593,
     269:5637707,271:620259383,293:382356917,309:722726531711,319:38538659},
233:{1:43997,33:3437374172579,35:75773,43:114077,107:1546342445624450657,
     121:10227436867237858553,145:8029811,163:3436793,177:823638366659,
     201:107759417,225:14382071357,305:46759735088411}}

def oddval(D,p):
    e=0
    while D%p==0:
        D//=p
        e+=1
    return e%2

small=[p for p in range(2,20001,3)
       if all(p%d for d in range(2,isqrt(p)+1))]
for U,end,left in [(227,332,[27,115,169,227,313]),
                   (229,335,[5,21,93,109,149,165,223,229]),
                   (233,341,[25,217,267,283,317,331])]:
    A=5**U
    assert 3**end<A<3**(end+1)
    tail={V for V in range(end+1)
          if not any(oddval(A*A-9**V,p) for p in small)}
    assert tail-set(vetoes[U])==set(left)
    assert set(vetoes[U])<=tail
    for V,d in vetoes[U].items():
        D=A*A-9**V
        assert d%2==1 and d%3==2 and D%d==0 and gcd(d,D//d)==1
print("PASS")
```
