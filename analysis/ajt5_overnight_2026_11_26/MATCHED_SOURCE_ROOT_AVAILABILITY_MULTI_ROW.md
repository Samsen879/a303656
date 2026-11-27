# Matched source-root availability across finite prime-source rows

**The matched root-availability bound saves 1,878 units of \(10^{-11}\) density across 39 existing finite prime-source rows.** The largest saving is \(D=83\), from 665 to 465 units. The finite-prime subtotal falls from 30,144 to **28,266**, and the full finite subtotal falls from 56,392 to **54,514**. The resulting exception-density bound is **below \(0.000063506085\%\)**. The cutoff and all three infinite tails carry forward. [Verified \(D=59\) baseline](https://github.com/Samsen879/a303656/commit/16085199c57d44f21c9e55e73b11d8578543ee46)

### Matched availability theorem

Fix the original mod-\(3960\) head and an eligible terminal \(q\) assigned to a doubly ordinary prime source \(D=r\). Let \(P_r\) be the largest prime dividing either source order. Suppose one source order contains a free digit \(L=\ell^a\nmid3960\), with either \(L\ge P_r\) or \(P_r\le23\). Define
\[
g=\begin{cases}
1-1/\ell,&\ell>23\text{ inert},\\
1,&\text{otherwise}.
\end{cases}
\]

Remove \(r\), its older readers on both axes, and the retained common-Wieferich rows \(J\). In the free inert case also remove \(\ell\) temporarily. Choose an anchor from the reduced observations. The original first-blocker event implies that such an anchor exists. Vary the free digit through its \(\ell\) values on one axis to obtain \(\ell\) distinct roots modulo \(r\). Repair the affected reduced rows in increasing prime order. The first affected rows exceed \(L\), and every later repair is at a larger prime. If \(P_r\le23\), all repair rows above the head already exceed \(P_r\). Thus the repairs preserve the source roots. Singly exceptional repair rows have one ordinary axis, which suffices. Doubly exceptional rows are in \(J\). [Protected repair criterion](https://github.com/Samsen879/a303656/commit/29e0e8f6ef234eabfd795e993ce1e8709ec5d827)

If \(\ell>23\) is inert, it is retained because \(\ell<r\). All probes have the same shift modulo \(\ell\), since the changed digit and subsequent repairs are invisible there. Requiring a unit at \(\ell\) therefore retains the entire menu with probability \(g\), measured before reading \(n_\ell\). This gate explains the boundary for an inert prime that reads back into the source. On a rooted reading, repairing \(\ell\) can change the source roots. The known \(31\to683\) control forces a singleton on such a reading, so the unit gate cannot simply be deleted. [Singleton control](https://github.com/Samsen879/a303656/commit/29e0e8f6ef234eabfd795e993ce1e8709ec5d827)

Restore \(J\) by requiring units. Let \(t\) be a uniform lower bound on \(\prod_{p\in J}(1-1/p)\). Each probe survives with probability at least \(t\), so the number \(X\) of surviving roots has \(\mathbb E X\ge\ell t\). Since \(X\le1\) on failure and \(X\le\ell\) always,
\[
\Pr(X\ge2)\ge\frac{\ell t-1}{\ell-1}.
\]
A fixed pair separately gives a lower bound \(t^2\), using \(1-2/p\) directly or the common reciprocal exponent bound for two probes. In the replay, \(t\) is rounded down from
\[
\exp\!\left[-\left(1+\frac2{B-1}\right)
 \left(\frac1U+\log\frac UV\right)\right],
\quad U=\frac{5r}{4}-\log2,\quad V=\log B-\log4.
\]
The same exponent doubled bounds the two-probe product. The resulting success bound is \(s=g\max(t^2,(\ell t-1)/(\ell-1))\). The first moment uses no independence between probes. [Ranked terminal endpoint and reciprocal envelope](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/MAX_ORDER_RANKED_TERMINAL_DENSITY_BOUND.md)

The restoration screen reads only retained coordinates. After fixing those readings, \(n_r\), the dropped readers, and \(n_q\) retain their original conditional laws. On success use two distinct roots and the factorial bound \(G_r=(rS_r)^{r-1}/(r-1)!\). On failure use the original single-anchor depth bound. Consequently the valid replacement is \((1-s)C_r+R_rG_r\), where \(C_r\) is the original unrounded parity-filtered depth charge and \(R_r\) the ranked reciprocal envelope. The separate robust-reader allowance stays in the ledger. The replaced sources are all doubly ordinary. The singly exceptional source \(20771\) retains its 1,634-unit row, and the calculation assumes no absence of doubly exceptional sources above \(B\).

| Source | Free digit | Current units | New units |
|---:|---:|---:|---:|
| 83 | 41 | 665 | 465 |
| 107 | 53 | 626 | 481 |
| 79 | 13 | 523 | 378 |
| 47 | 23 | 255 | 118 |
| 103 | 17 | 642 | 508 |
| 59 | 29 | 284 | 203 |
| All 39 replaced rows | | **14,757** | **12,879** |


The prime \(q\) and the exceptional-reader set \(J\) are fixed by the structural chart before reading observations. In the inert-source gate, \(\ell<r\le499<B\) on the audited rows, so it is separate from \(J\); pure \(\ell\)-primary changes preserve its orders modulo \(\ell\), while all subsequent repairs occur at larger primes. A unit guarantees a pass regardless of the full precision. The quantities \(t\) and \(t^2\) in this note are explicit lower estimates from the reciprocal bound, not an assertion that two probe events are independent. In the small-head branch the fixed mod-3960 head retains the original unit and residue tests; no new assumption about large common-Wieferich primes is used.

### Standalone rational replay of the existing 45-row inventory

The ranges and formulas are inherited from the [finite-prime ledger](https://github.com/Samsen879/a303656/blob/c12d0e2/analysis/ajt5_overnight_2026_11_26/FINITE_PRIME_SOURCE_REPRICE.md). Approximate arithmetic only picks a candidate among competing upper bounds; its value is then recomputed with outward rational arithmetic. A nonoptimal pick can only increase the envelope. The replay requires the full 45-row subtotal to match the pinned 16,370 before subtracting any row charges. The separate (D=59) admitted charge of 284 is substituted only after that check. The final short control checks all 53 roots on an ordinary-terminal chart.

```python
from math import factorial
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

@cache
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
        fx=float(x)
        cand=[(float(C[-1])*fx,len(C)-1)]
        cand+=[(float(C[j])*fx+float(E[j])/float(u-h),j)
               for j,(_,h) in enumerate(L) if h<u]
        _,j=min(cand)
        return up(C[j]*x)+(up(E[j]/(u-L[j][1])) if j<len(L) else 0)

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


from math import log
def segment(C,E,L,a,b,shift):
    d,la,hb,sb,sa,ratio=data(a,b)
    df,bf,rat=float(d),float(b-B),float(ratio-B*d)
    options=[(float(C[-1])*df,0,len(C)-1)]
    Cf=list(map(float,C)); Ef=list(map(float,E))
    laf,hbf,sbf,saf=map(float,(la,hb,sb,sa))
    for j,(l,h) in enumerate(L):
        if h>=hb: break
        lf,hf=float(l),float(h)
        if la>h: options.append((Cf[j]*df+Ef[j]*log((hbf-lf)/(laf-hf)),1,j))
        if shift and sb>h: options.append((df*(Cf[j]+Ef[j]*bf/(sbf-hf)),2,j))
        if shift and sa>h: options.append((Cf[j]*df+Ef[j]*rat/(saf-hf),3,j))
    _,k,j=min(options)
    if not k:return up(C[j]*d)
    l,h=L[j]
    if k==1:return up(C[j]*d+E[j]*hi((hb-l)/(la-h)))
    if k==2:return up(d*(C[j]+E[j]*(b-B)/(sb-h)))
    return up(C[j]*d+E[j]*(ratio-B*d)/(sa-h))
def ordp(a,p):
    return next(i for i in range(1,p) if pow(a,i,p)==1)

def free(r):
    orders=[ordp(a,r) for a in (3,5)]
    plist=[p for p in ps if any(o%p==0 for o in orders)]
    mx=max(plist,default=1)
    return [(p, max(p**j for j in range(1,16) if o%p**j==0))
            for o in orders for p in plist if o%p==0
            if any(o%p**j==0 and 3960%p**j and (p**j>=mx or mx<=23) for j in range(1,16))]
def screen(r):
    U,V=Q(5*r,4),lo(B)-hi(4)
    z=(1+Q(2,B-1))*(1/(U-hi(2))+hi((U-lo(2))/V))
    z=Q(ceil(W*z),W)
    assert 0<z<4
    t=s=Q(1)
    for j in range(1,28):
        t*=z/j
        s+=t
    return Q(floor(W/(s+t*z/28/(1-z/29))),W)

rows=[]
for r in (p for p in ps if p>=31 and p%4==3 and all(pow(a,p-1,p*p)!=1 for a in (3,5))):
    digits=free(r)
    if not digits: continue
    t=screen(r)
    s,ell,L=max(((1-Q(1,p) if p>23 and p%4==3 else 1)*max(t*t,(p*t-1)/(p-1)),p,l) for p,l in digits)
    R=ranked(r)[2]
    C=units(r,R,False,raw=True)
    sigma=(hi(r)+Q(1,2))/(r-1)
    factor_charge=(r*sigma)**(r-1)/factorial(r-1)
    old=284 if r==59 else ceil(C)
    new=ceil((1-s)*C+W*R*factor_charge)
    if new<old:
        rows.append((r,ell,L,old,new))
print(len(rows),sum(x[3] for x in rows),sum(x[4] for x in rows))
print([x for x in rows if x[0] in (83,107,79,47,103,59)])

catalog=[p for p in ps if p>=31 and p%4==3]
assert len(catalog)==45
assert sum(units(p,ranked(p)[2],False) for p in catalog)==16370
assert (len(rows),sum(x[3] for x in rows),sum(x[4] for x in rows))==(39,14757,12879)
assert [row for row in rows if row[0] in (83,107,79,47,103,59)] == [
    (47,23,23,255,118),(59,29,29,284,203),(79,13,13,523,378),
    (83,41,41,665,465),(103,17,17,642,508),(107,53,53,626,481)]
saved=sum(old-new for _,_,_,old,new in rows)
assert (30144-saved,56392-saved)==(28266,54514)
assert Q(653840846076458,10**19)-100*Q(saved,W)<Q(63506085,10**12)
print(saved,flush=True)
```

```python
from math import isqrt, lcm

def prime(q):
    return q>1 and all(q%k for k in range(2,isqrt(q)+1))

def order(a,q):
    return next(i for i in range(1,q) if pow(a,i,q)==1)

r,q,ell=107,643,53
assert all(prime(p) and p%4==3 for p in (r,q))
assert order(3,q)==order(5,q)==214
assert all(pow(a,q-1,q*q)!=1 for a in (3,5))
a=next(a for a in (3,5) if order(a,r)%ell==0)

def keep(p):
    return p!=r and all(order(a,p)%r for a in (3,5))

P=[p for p in range(31,q,4) if prime(p) and keep(p)]
L=lcm(3960,*(p*p*order(a,p) for p in P))
assert L%ell!=0 and order(a,r)%ell==0
seeds=[(23+i*L,55) if a==3 else (23,55+i*L) for i in range(ell)]
def F(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m
assert len({F(c,d,r) for c,d in seeds})==ell
mods=[32,3,7,11,19,23]+P
n,tot=0,1
for p in mods:
    assert len({F(c,d,p) for c,d in seeds})==1
    n+=tot*((F(23,55,p)+1-n)*pow(tot,-1,p)%p)
    tot*=p
assert n>0 and all((n-F(c,d,p))%p==1 for c,d in seeds for p in mods)
print("53 retained source roots at 107 -> 643")
```

The resulting natural representation density exceeds **99.999936493915%**; no pointwise conclusion follows.
