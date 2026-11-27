# Uniform twenty centers from one 37-offset menu

**The previous nineteen-center guarantee strengthens to twenty.** For every target \(n\) and every finite ordinary inert panel, one can choose a single seed \((C,D)\) and twenty indices from \(0,\ldots,36\) so that the centers \((C,D+8i)\) pass the small-head and ordinary valuation tests. Each genuine common-Wieferich reader can hit at most one center. Thus a finite blocker requires at least twenty such readers.

The extra center comes from clearing \(199\) jointly with \(23,67\). The later deletion bounds still hold with 23 candidates entering those stages.

### Audit of the phase increments

The table uses a **period** to mean a multiple of the orders of every reading already fixed on the corresponding axis.

| Rows addressed | Free increments | Period after the choice |
|---|---|---|
| \(23,67,199\) | \(90x,90y\), \(0\le x,y<11\) | \(990\) on both axes |
| \(43,127,71,211,631\) | \(990x,990y\), \(0\le x,y<7\) | \(6930\) on both |
| \(271\) | \(6930y\) on \(D\), \(0\le y<3\) | \(D\) at \(20790\), \(C\) still at \(6930\) |
| \(4159,379\) | \(6930x\) on \(C\), \(0\le x<3\) | \(C\) at \(20790\) |
| \(163\), then \(487\) | \(20790x\), then \(62370x\), on \(C\), each with \(0\le x<3\) | \(C\) at \(187110\), \(D\) held fixed |
| \(191,6271\) | \(187110x,187110y\), \(0\le x,y<19\) | \(3555090\) on both |

The replay checks **each actual increment on each axis** against the orders of all previously fixed rows. In particular, the \(C\)-change at \(4159\) preserves \(271\) because \(\operatorname{ord}_{271}(3)=30\). The \(D\)-reading at \(271\) is already fixed.

**\(23,67,199\).** The head table supplies 25 candidates through \(7,11,19,31\). Fix a \(C\bmod11\) that clears at least one of \(23,67\) if possible. If both rows force hits, their observations are zero. The slopes \(16,7\bmod11\) then let \(C\equiv0\bmod11\) align their forbidden index classes. In either case, varying \(D\) by \(90\) moves the one class to be deleted through all eleven positions. At least three positions contain at most two candidates, since nine positions with at least three would require 27 candidates. At \(199\), the repeated representatives are \(0,1,2,3\bmod33\). As \(D\) varies, a hit traverses one class modulo \(3\) in \(\mathbb Z/33\mathbb Z\). It can land on at most two repeated representatives. A third choice therefore leaves **23 candidates** and clears every repeated hit at \(199\).

**\(43,127,71,211,631\).** At \(71\), at most three of the seven \(C\)-choices can hit any of the five \(5\)-powers. At least four choices remain. The deletion-cost bounds, averaged over those choices and all seven \(D\)-choices, are:

| Row | Nonzero observation | Zero observation |
|---:|---:|---:|
| \(43\) | \(33/28\) | \(6/7\) |
| \(127\) | \(22/28\) | \(6/7\) |
| \(211\) | \(4/28\) | \(1/7\) |
| \(631\) | \(4/28\) | \(1/7\) |

For nonzero readings the replay checks the coset caps \(3,2,2,2\). With 23 candidates there are at most eleven repeated classes, and at \(211,631\) there are at most two. For zero readings only one index class modulo \(3\) contributes at \(43,127\), and only one modulo \(5\) at \(211,631\). The sum of the rowwise maxima is \(65/28<3\), so some choice costs at most two deletions.

**\(271,4159,163,487,379\).** The three \(D\)-choices at \(271\) move a hit by steps of \(9\bmod27\). They cannot all land in the repeated range \(0,\ldots,9\). At each of \(4159,163,487\), three bad \(C\)-choices would require three distinct repeated \(5^{8i}\) values to be a translate of a scaled order-three subgroup. Such a triple satisfies \(3\sum x^2=(\sum x)^2\), and the replay excludes every triple in the relevant ten-value range. These four rows cost zero. Row \(379\) can cost one deletion: its index period is \(21\), so no target residue on that row hits more than two among the 37 offsets.

**\(191,6271\).** Each row has at most eleven repeated classes. The nonzero coset caps are \(6,2\). One zero row leaves at least \(19(19-11)=152\) phase pairs, more than the \(66\) a nonzero companion can rule out. With two zero rows, the distinct slopes \(16,3\bmod19\) permit simultaneous avoidance. This stage costs zero.

All remaining rows are cleared by the certified late increments in the replay. Thus the total loss after the early stage is at most \(2+1\), leaving twenty.

### Same-target positive and failed controls

The CRT fixture below has \(C=22\) and two choices \(D=1,181\). Both leave 23 centers through the head rows and \(67\). At \(D=1\), indices \(0,33\) are tied at \(199\) with remainders \(160\cdot199\) and \(54\cdot199\bmod199^2\). No shared first digit repairs both. At \(D=181\), only index \(27\) needs repair there. On the same target, the base-\(5\) repair yields \(191\cdot199^2\bmod199^3\) and preserves the full earlier ordinary prefix.

This is a **finite-phase** result. It gives no bound placing the exponents inside the ordinary height window for the original target.

### Standalone replay

```python
from collections import Counter
from itertools import combinations, product
from math import gcd, isqrt, lcm, prod

F = {
 1:(2,2,2,3), 3:(3,7,31), 5:(11,71,521), 7:(29,449,19531),
 9:(3,19,829,5167), 11:(23,67,5281,12207031),
 13:(5227,38923,305175781), 15:(61,181,1741,7621),
 17:(409,3061,41540861,466344409), 19:(191,761,6271,19609,3981071,213029),
 21:(7,43,127,379,7603,519499), 23:(47,8971,42272797713043,332207361361),
 25:(101,251,401,1901,9384251,50150933101),
 27:(3,109,163,271,487,4159,31051,16018507),
 29:(59,35671,5096867,22125996444329,6090817323763),
 31:(1303,1861,21207101,28086211607,625552508473588471),
 33:(199,595123,190771747,386478495679),
 35:(211,631,4201,15216601,85280581,4698932281)}
W = {42272797713043:(13967,4523),332207361361:(9781,293),
 50150933101:(201167,277),22125996444329:(13624382047,),
 6090817323763:(2061161,37),28086211607:(453003413,),
 625552508473588471:(391337,25654001),386478495679:(5855734783,)}

def prime(n):
    if n not in W:
        return n>1 and all(n%d for d in range(2,isqrt(n)+1))
    u=prod(W[n])
    return (u*u>n and (n-1)%u==0 and pow(2,n-1,n)==1
            and all(prime(p) and gcd(pow(2,(n-1)//p,n)-1,n)==1 for p in W[n]))

T=set()
for m in F:
    f=Counter(q for d,fs in F.items() if m%d==0 for q in fs)
    assert all(map(prime,f)) and prod(q**v for q,v in f.items())==5**(2*m)-1
    assert all(v==1 for q,v in f.items() if q>23)
    T.update(q for q in f if q>23 and q%4==3)

A=(2,3,5,7,11,13,17,19,23,29,31,37,41,67,71,127,181,373,499,521,911,
   1367,3701,4523,13967,37537,87877,391337,2061161,25654001,453003413,5855734783)
assert len(T)==40 and all(map(prime,A))
def order(b,q):
    r=u=q-1
    for p in A:
        while r%p==0: r//=p
        while u%p==0 and pow(b,u//p,q)==1: u//=p
    assert r==1
    return u

O={q:(order(3,q),order(5,q)) for q in T|{7,11,19,23}}
U,V=lcm(3960,*(q-1 for q in T)),lcm(3960,*(2*m for m in F))
assert [p for p in range(27,71,4) if prime(p) and V%p==0]==[31]
assert all(V%p and pow(5,p-1,p*p)!=1
           for p in A if p>23 and p%4==3 and p!=31)

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p
def good2(x):
    z=x&-x
    return bool(z and z<=8 and x//z%4==1)
def fresh(q,k):
    return tuple(o//gcd(o,k) for o in O[q])
def period(q):
    return O[q][1]//gcd(8,O[q][1])

# One bit per pair (n mod 11, n mod 31).
bad=[]
for a,b in product(range(2),repeat=2):
    rows=[]
    for c,d,k in product(range(a,90,2),range(b,18,2),range(3)):
        X,Y,Z=[{S(c,d+8*i,p) for i in range(9) if i%3!=k}
               for p in (7,19,31)]
        M=sum(1<<(31*u+v) for u,v in product(range(11),range(31))
              if v not in Z and (u-pow(3,c,11))%11 not in (1,3,4,5,9))
        rows.append((X,Y,M))
    for u,v in product(range(7),range(19)):
        M=0
        for X,Y,Z in rows:
            if u not in X and v not in Y: M |= Z
        if M!=(1<<341)-1:
            bad.extend((a,b,u,v,j//31,j%31) for j in range(341) if not (M>>j)&1)
assert bad==[(1,1,2,0,8,27)]
assert sum(all(S(89,89+8*i,p)!=r for p,r in ((7,2),(19,0),(11,8),(31,27)))
           for i in range(37))==27
assert fresh(23,90)==fresh(67,90)==(11,11)
assert pow(5,16,23)==3 and pow(5,7,67)==3 and O[199]==(198,33)

def cap(q,a,b):
    X={pow(i,(q-1)//a,q) for i in range(1,q)}
    Y={pow(i,(q-1)//b,q) for i in range(1,q)}
    seen,best=set(),0
    for r in range(1,q):
        if r in seen: continue
        Z={r*y%q for y in Y}
        seen |= Z
        counts=Counter((x+z)%q for x in X for z in Z)
        best=max(best,max((v for n,v in counts.items() if n),default=0))
    return best

G7=(43,127,211,631)
assert all(fresh(q,990)==(7,7) for q in G7) and fresh(71,990)==(7,1)
assert [period(q) for q in G7]==[21,21,35,35]
assert [cap(q,7,7) for q in G7]==[3,2,2,2] and cap(71,7,5)==3
k=6930
assert fresh(271,k)==(1,3) and fresh(379,k)==(3,1)
for q in (4159,163,487):
    assert fresh(q,k)[0]==3 and period(q)==27
    for X in combinations([pow(5,8*i,q) for i in range(10)],3):
        assert (3*sum(x*x for x in X)-sum(X)**2)%q
    k*=3
assert k==187110
assert [cap(q,19,19) for q in (191,6271)]==[6,2]
for q,z in ((191,16),(6271,3)):
    assert fresh(q,k)==(19,19)
    assert pow(3,990,q)==pow(5,990*z,q) and pow(5,990,q)!=1

G=[(7,(19531,1303,519499)),(1,(251,)),(1,(47,31051)),
   (1,(8971,)),(1,(59,)),(1,(5167,35671))]
G += [(1,(q,)) for q in (12207031,5227,38923,3981071,7603,42272797713043,
      9384251,16018507,5096867,6090817323763,28086211607,625552508473588471,
      595123,190771747,386478495679)]
def budget(Q):
    return sum(min(11,period(q),37-period(q)) for q in Q)

k=187110*19
used={31,67,199,71,*G7,271,379,4159,163,487,191,6271}
for s,Q in G:
    assert not used.intersection(Q)
    assert all(fresh(q,s*k)[0]>budget(Q) for q in Q)
    used.update(Q)
    k=lcm(k,*(O[q][0] for q in Q))
assert used==T and k%4==2

def seed(n):
    def hit(q,u,v,I):
        return [i for i in I if (n-S(u,v+8*i,q))%q==0]
    def units(Q,u,v,I):
        return all(not hit(q,u,v,I) for q in Q)
    def cost(Q,u,v,I):
        return sum(max(0,len(hit(q,u,v,I))-1) for q in Q)

    b=int(n%3==1)
    a=next(a for a in (0,1) if (n-S(2-a,2-b,8))%8 in (0,1,2,4,5))
    small={7,11,19,31}
    if (a,b,n%7,n%19,n%11,n%31)==bad[0]:
        c=d=89
        I=[i for i in range(37) if units(small,c,d,[i])][:25]
    else:
        c,d,h=next((c,d,h) for c,d,h in product(range(a,90,2),range(b,90,2),range(3))
                   if units(small,c,d,[i for i in range(45) if i%3!=h]))
        d+=8*((h-1)%3)
        I=[i for i in range(37) if i%3!=1]
    c,d=c or 90,d or 90
    assert len(I)==25 and units(small,c,d,I)

    locked=set(small)
    def move(u,v,Q):
        nonlocal c,d
        assert all((u-c)%O[q][0]==(v-d)%O[q][1]==0 for q in locked)
        c,d=u,v
        locked.update(Q)

    u,v,J=next((u,v,J) for u,v in product(range(c,c+990,90),range(d,d+990,90))
               for J in [[i for i in I if units((23,67),u,v,[i])]]
               if len(J)>=23 and cost((199,),u,v,J)==0)
    move(u,v,(23,67,199))
    I=J[:23]
    u,v=next((u,v) for u,v in product(range(c,c+6930,990),range(d,d+6930,990))
             if units((71,),u,v,I) and cost(G7,u,v,I)<=2)
    move(u,v,(71,*G7))

    k=6930
    move(c,next(d+k*j for j in range(3) if cost((271,),c,d+k*j,I)==0),(271,))
    for q in (4159,163,487):
        u=next(c+k*j for j in range(3) if cost((q,),c+k*j,d,I)==0)
        move(u,d,(q,379) if q==4159 else (q,))
        k*=3
    u,v=next((u,v) for u,v in product(range(c,c+19*k,k),range(d,d+19*k,k))
             if cost((191,6271),u,v,I)==0)
    move(u,v,(191,6271))
    k*=19
    for s,Q in G:
        move(next(c+s*k*j for j in range(budget(Q)+1)
                  if cost(Q,c+s*k*j,d,I)==0),d,Q)
        k=lcm(k,*(O[q][0] for q in Q))
    move(next(c+k*j for j in range(4) if good2((n-S(c+k*j,d,32))%32)),d,())
    drop={i for q in T for i in hit(q,c,d,I)[1:]}
    J=[i for i in I if i not in drop]
    assert len(J)>=20 and units(small|{3,23,67},c,d,J) and cost(T,c,d,J)==0
    return c,d,J

def repair(n,c,d,I,P):
    k=1
    for p in sorted(set(P)):
        assert p>23 and p%4==3 and prime(p)
        assert any(pow(b,p-1,p*p)!=1 for b in (3,5))
        hits=[i for i in I if (n-S(c,d+8*i,p))%p==0]
        if hits:
            i,=hits
            B,b=next((B,b) for B,b in ((lcm(k,V,p-1),5),(lcm(k,U,p-1),3))
                     if B%p and pow(b,p-1,p*p)!=1)
            e=c if b==3 else d+8*i
            r=(n-S(c,d+8*i,p*p))%(p*p)
            u=(r//p)*pow(pow(b,e,p)*((pow(b,B,p*p)-1)//p),-1,p)%p
            if b==3: c+=B*u
            else: d+=B*u
            if (n-S(c,d+8*i,p**3))%p**3==0:
                if b==3: c+=B*p
                else: d+=B*p
        k=lcm(k,p*p*(p-1))
    return c,d

def crt(R):
    M=prod(q for q,v in R)
    return sum(v*(M//q)*pow(M//q,-1,q) for q,v in R)%M

p=199
P=tuple(q for q in range(27,p,4) if prime(q))
H={7,11,19,23,31,67}
I={d:[i for i in range(37) if all(S(22,d+8*i,r) for r in H)] for d in (1,181)}
assert len(I[1])==len(I[181])==23
R=[(32,15),(3,1),(p**3,2843094)]+[(q,0) for q in H]
for q in (T|set(P))-(H|{p}):
    Z={S(22,181+8*i,q) for i in I[181]}
    R.append((q,next(v for v in range(24) if v not in Z)))
n=crt(R)
assert [(n-S(22,1+8*i,p*p))%(p*p) for i in (0,33)]==[160*p,54*p]
assert [i for i in I[181] if (n-S(22,181+8*i,p))%p==0]==[27]
c,d=repair(n,22,181,I[181],P+(p,))
assert (n-S(c,d+8*27,p**3))%p**3==191*p*p
assert good2((n-S(c,d,32))%32)
assert all((n-S(c,d+8*i,q))%q for i in I[181] for q in (T|H|set(P)|{3})-{p})
assert all((n-S(c,d+8*i,p))%p for i in I[181] if i!=27)

for v in (0,1,7,372715,n,crt([(32,1),(3,1),(7,2),(19,0),(11,8),(31,27)])):
    c,d,J=seed(v)
    c,d=repair(v,c,d,J,P+(p,))
    for q,i in product(P+(p,),J):
        r=(v-S(c,d+8*i,q**3))%q**3
        assert r%q or (r and r%(q*q)==0)
```
