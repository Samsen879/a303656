# Repricing the finite prime-source component

The finite prime-source subtotal decreases from 40,008 to 30,214 units of 10^(-11) density. Against SHIFTED_TERMINAL_D243_REPRICE.md, the finite subtotal is now 56,462 units and natural exception density is **below 0.000074376085%**. All non-prime rows, the cutoff and three infinite tails are unchanged.

The original finite range is identical to RECONCILED_DENSITY_LEDGER.md. It is split into three disjoint parts. For the 45 ranked rows with 31<=D<=499, preserve every endpoint and phase charge. Clip the first nine log bins at the cutoff B and apply shifted [Brun–Titchmarsh](https://doi.org/10.1112/S0025579300004708) as in the D=81 and D=243 repricings. Keep the catalogue and the upper union over optional-factor subsets without overlap subtraction. This gives 16,370 units instead of 21,648. Clipping and refining the absolute rather than shifted bound gives 19,163. The separately identified exceptional source D=20771 preserves its R_D/D formula and moves from 1,648 to 1,634 by the same continuous shifted integral used for the cube rows.

For the rest of the original finite prime-source rows, use the original formulas and replace the lower log 34 with an outward lower bound for log B in both progression envelopes. The endpoints, phase branches, and exceptional-source test are unchanged. The independent direct replay over exactly the old source list verifies 16,712 old units and 16,646 after clipping if every source is rounded to a whole unit. Instead, round each new bound up to (1/100) of a unit, sum, and round that sum up once. This yields 12,210 units as a certified bound for this disjoint part. It is smaller mostly because the old rows were individually rounded. No charge from outside the finite source list is removed or from a search of new terminal primes.

The exact ledger difference is 9,794/10^11 in density units. This is an upper bound on exceptions, not a pointwise proof.

```python
from fractions import Fraction as Q
from functools import cache
from math import ceil, floor, isqrt, prod

B,W,P,G = 9*10**14,10**11,10**5,10**30

def series(y):
    z=(y-1)/(y+1)
    s=2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s,s+2*z**25/(25*(1-z*z))

l2,h2=series(Q(2))
@cache
def logs(x):
    y,k=Q(x),0
    assert y>=1
    while y>=2:
        y/=2
        k+=1
    a,b=series(y)
    return Q(floor(W*(a+k*l2)),W),Q(ceil(W*(b+k*h2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(G*x),G)

@cache
def exps(n):
    s=t=Q(1)
    for j in range(1,161):
        t*=Q(n,j)
        s+=t
    return s,s+t*Q(n,161)/(1-Q(n,162))

@cache
def inv_exp(n):
    z=1<<(2*n+64)
    return Q(ceil(z*Q(10**7,27182818)**n),z)

def prog(p,m,scale=1,lower=Q(34)):
    l,h=logs(m*p)
    u=Q(4*p,3)
    return (1/(u-h)+hi((u-l)/(lower-h)))/(scale*(p-1))

def units(p,R,plain,lower=Q(34),raw=False):
    s=(hi(p)+Q(1,2))/(p-1)
    if any(pow(b,p-1,p*p)==1 for b in (3,5)):
        return W*R/p if raw else ceil(W*R/p)
    K=(1+isqrt(4*p-3))//2
    h=p-K
    whole=Q(1,p*p)+(Q(1,p)-Q(1,p*p))*min(1,p*s/h)
    psi=moment=Q(1)
    for j in range(6):
        if h-j*K<=0:
            break
        moment*=p*s/(h-j*K)
        psi=min(psi,moment)
    f,g=[int(pow(b,(p-1)//2,p)==p-1) for b in (3,5)]
    weights=((0,0,40),(0,1,19),(1,0,19),(1,1,18))
    v=[Q(max(sum(w for a,b,w in weights if (a*x+b*y)%2 and (a*f+b*g)%2==j)
             for j in (0,1)),96) for x,y in ((0,0),(0,1),(1,0),(1,1))]
    align=R*max(v)
    if plain:
        align=min(align,2*prog(p,60,8,lower)*sum(v))
    sh=(1+Q(1,2*p+1))*s
    out=W*min(R*whole,R*psi/p+(1-psi)*(align+Q(19,48)*sh*R)/p**2)
    return out if raw else ceil(out)

@cache
def data(a,b):
    return 1/a-1/b,lo(a),hi(b),lo(b-B),lo(a-B) if a>B else 0,hi(b/a)

def segment(C,E,L,a,b,shift):
    d,la,hb,sb,sa,ratio=data(a,b)
    best=[C[-1]*d]
    for j,(l,h) in enumerate(L):
        if h>=hb:
            break
        if la>h:
            best.append(C[j]*d+E[j]*hi((hb-l)/(la-h)))
        if shift and sb>h:
            best.append(d*(C[j]+E[j]*(b-B)/(sb-h)))
        if shift and sa>h:
            best.append(C[j]*d+E[j]*(ratio-B*d)/(sa-h))
    return up(min(best))

# Fixed small-prime list from the original ranked calculation.
ps=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,
    89,97,101,103,107,109,113,127,131,137,139,149,151,157,163,167,173,
    179,181,191,193,197,199,211,223,227,229,233,239,241,251,257,263,
    269,271,277,281,283,293,307,311,313,317,331,337,347,349,353,359,
    367,373,379,383,389,397,401,409,419,421,431,433,439,443,449,457,
    461,463,467,479,487,491,499)

def sym(xs):
    e=[Q(1)]+[Q(0)]*len(xs)
    for x in xs:
        for j in range(len(xs),0,-1):
            e[j]+=x*e[j-1]
    return e

def ranked(r):
    pp=[p for p in ps if p<r]
    mm=[max(p**j for j in range(1,6) if p**j<=r) for p in pp]
    scale=2*r*prod(m//p for m,p in zip(mm,pp))*hi(3)/68
    C=[Q(0)]
    for z in sym(pp):
        C.append(C[-1]+scale*z)
    E=[e/(r-1) for e in sym([Q(1,m-m//p) for m,p in zip(mm,pp)])]
    L=[logs(4*r)]
    for m in sorted(mm,reverse=True):
        l,h=L[-1]
        a,b=logs(m)
        L.append((l+a,h+b))
    def old(u,isbin):
        x=inv_exp(u)*(Q(2,3) if isbin else 1)
        return min([up(C[-1]*x)]+[up(C[j]*x)+up(E[j]/(u-h))
                   for j,(_,h) in enumerate(L) if h<u])

    v=ceil(Q(5*r,4)+h2)
    vals=[old(v,False)]*3
    for u in range(34,v):
        z=old(u,True)
        vals[0]+=z
        if u<43:
            a,b=max(B,floor(exps(u)[0])),ceil(exps(u+1)[1])
            cut=[a+Q((b-a)*i,16) for i in range(17)]
            for j in (1,2):
                vals[j]+=min(z,sum(segment(C,E,L,x,y,j==2)
                                   for x,y in zip(cut,cut[1:])))
        else:
            vals[1]+=z
            vals[2]+=z
    return vals

small=[]
for p in (p for p in ps if p>=31 and p%4==3):
    plain=units(p,min(prog(p,4),(hi(p)+Q(1,2))/(p-1)),True)
    z=tuple(units(p,r,False) for r in ranked(p))
    assert z[0]<plain
    small.append((p,*z))
assert len(small)==45 and (127,1059,929,747) in small
assert tuple(sum(z[i] for z in small) for i in (1,2,3))==(21648,19163,16370)

p=20771
assert pow(5,p-1,p*p)==1!=pow(3,p-1,p*p)
Y,start=128*B,Q(B,2048)
h=hi(4*p)
assert lo(start)>h and hi(Y)<Q(4*p,3)
cuts={B+start,Q(Y)}
for j in range(-11,7):
    y=B*Q(2)**j
    cuts.update(B+y*(1+Q(i,4)) for i in range(5)
                if B+start<B+y*(1+Q(i,4))<Y)
pts=sorted(cuts)
head=start*(1/Q(B)-1/(B+start))/(lo(start)-h)
head+=sum((hi(b/a)+B/b-B/a)/(lo(a-B)-h) for a,b in zip(pts,pts[1:]))
row=units(p,prog(p,4,lower=lo(Y))+head/(p-1),True)
assert (units(p,prog(p,4),True),row)==(1648,1634)

is_prime=bytearray(b'\x01')*(P+1)
is_prime[:2]=b'\x00\x00'
for p in range(2,isqrt(P)+1):
    if is_prime[p]:
        is_prime[p*p:P+1:p]=bytes((P-p*p)//p+1)
old_rows=clipped=0
safe100=0
for p in range(503,P+1,4):
    if p==20771 or not is_prime[p]: continue
    reader=(hi(p)+Q(1,2))/(p-1)
    old_rows+=units(p,min(prog(p,4),reader),True)
    v=units(p,min(prog(p,4,lower=lo(B)),reader),True,lo(B),raw=True)
    clipped+=ceil(v)
    safe100+=ceil(100*v)
assert old_rows==16712
remaining=ceil(Q(safe100,100))
assert (clipped,remaining)==(16646,12210)

prime_new=16370+row+remaining
delta=Q(40008-prime_new,W)
assert (prime_new,delta)==(30214,Q(9794,W))
assert 66256-W*delta==56462
old_percent_hi=Q(841700846076458,10**19)
assert old_percent_hi-100*delta<Q(74376085,10**12)
print(prime_new,"units; revised bound < 0.000074376085%")
```
