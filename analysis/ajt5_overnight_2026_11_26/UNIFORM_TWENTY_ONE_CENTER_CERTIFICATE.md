# Uniform twenty-one centers through a sharper seven-phase count

**The same 37-offset menu gives twenty-one centers uniformly.** The seven-phase stage costs at most **one** deletion. The ternary stage keeps its existing allowance of one at \(379\). Together they leave at least \(23-1-1=21\) centers for every target, with the same separate-axis locks. The squarefree certificate is unchanged, so a genuine common-Wieferich reader can hit at most one center in the selected menu.

### The seven-phase saving

Write \(L=990\) and vary the seed by \((C,D)\mapsto(C+Lx,D+Ly)\), with \(x,y\in\mathbf F_7\). At \(71\), at least four \(x\)-choices make the whole selected set units. The order-seven and order-five cosets there have intersection cap three under nonzero translation, and cap one at zero. Let \(X\) be the allowed \(x\)-set.

At each of \(43,127,211,631\), a repeated hit costs one deletion. Fix \(x\). As \(y\) varies, the \(5\)-power at each index traverses its order-seven coset. A hit can occur in only one such coset.

- At \(43,127\), the index period is \(21\). The possible repeated representatives \(0,\ldots,15\) occupy the three cosets in counts \(6,5,5\). The average cost is at most \(6/7\) per row. If its observation is nonzero, the bound is strict: at most three \(x\)-choices at \(43\), and two at \(127\), can reach the six-representative coset. There are at least four allowed choices.
- At \(211,631\), the index period is \(35\). The possible repeated representatives \(0,1\) lie in distinct cosets. The average is at most \(1/7\) per row. For a nonzero observation, the combined two-coset caps are respectively three and two **pairs** \((x,y)\) in the whole grid. Dividing by \(7|X|\ge28\) makes each bound strict.

Thus the average total cost is at most two, with strict inequality if any of the four observations is nonzero. If equality holds, all four observations are zero and each individual average attains its bound. In particular, at each of 43 and 127 the cost is one except at its one missing value of \(y\), for each admissible \(x\). At \(43,127\) the unique missing \(y\)-values are affine lines of slopes \(2,5\) in \(x\). At \(211\) its unique hit line has slope \(6\). The latter meets the two missing lines at at most two \(x\)-values. Some allowed \(x\) therefore gives a point with cost at least three. An integer-valued cost of average two with such a point must also have a point of cost at most one.

Choose that one phase and lock both coordinates modulo \(6930\). All subsequent ternary and late increments preserve it. In the [verified twenty-center constructor](https://github.com/Samsen879/a303656/blob/a00176489cff6c1882530aaac183d3ec12a0f720/analysis/ajt5_overnight_2026_11_26/UNIFORM_TWENTY_CENTER_CERTIFICATE.md), the only changes are `cost(G7,u,v,I)<=1` and the final assertion `len(J)>=21`.

### Same-target sharp control

Take \(C=45,D=30\) and the 23 indices \(i\not\equiv1\bmod3\), omitting \(2,5\). Use zero observations at \(43,127,211,631\), and observation \(26\) at \(71\).

The six \(71\)-unit choices \(x=0,\ldots,5\) have mean cost exactly two and minimum cost one. The remaining choice \(x=6\) ties four indices at \(71\), so **one deletion is unavoidable on this frozen head**, even if ordinary repair at \(71\) is attempted.

On the same CRT target:

| Seven-phase choice | Repeated pairs | Outcome |
|---|---|---|
| \((x,y)=(0,0)\) | \(127:(6,27)\) | Drop \(27\). The remaining 22 centers pass the full ordinary prefix through \(211\). |
| \((x,y)=(0,2)\) | \(43:(12,33)\), \(127:(0,21)\) | Two disjoint pairs require two deletions. Their respective first readings are \((6,27)\) and \((61,66)\). |

The positive repairs have exact residuals \(10\cdot43^2\bmod43^3\), \(73\cdot127^2\bmod127^3\), and \(147\cdot211^2\bmod211^3\). This is a **finite-phase theorem**. It gives no ordinary exponent-height bound for the input \(n\).

```python
from collections import Counter
from itertools import product
from math import isqrt, lcm, prod

L, Q = 990, (43,127,211,631)
def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p))%p

def cap(p,b=7,two=False):
    H={pow(x,(p-1)//7,p) for x in range(1,p)}
    K={pow(x,(p-1)//b,p) for x in range(1,p)}
    seen,best=set(),0
    for a in range(1,p):
        if a in seen:
            continue
        Y={a*y%p for y in K}
        seen |= Y
        if two:
            Y |= {pow(5,8,p)*y%p for y in Y}
        count=Counter((x+y)%p for x in H for y in Y)
        best=max(best,max(v for n,v in count.items() if n))
    return best

assert [cap(p) for p in Q[:2]]==[3,2]
assert [cap(p,two=True) for p in Q[2:]]==[3,2]
assert cap(71,5)==3
for p,m,k in zip(Q,(21,21,35,35),(2,5,6,4)):
    assert next(j for j in range(1,p) if pow(5,8*j,p)==1)==m
    assert pow(5,L,p)!=1 and pow(5,7*L,p)==1
    assert pow(3,L,p)==pow(5,L*k,p)
assert pow(5,L,71)==1 and pow(3,L,71)!=1 and pow(3,7*L,71)==1

c,d=45,30
I=[i for i in range(37) if i%3!=1 and i not in (2,5)]
def hit(p,x,y,r=0):
    return [i for i in I if S(c+L*x,d+L*y+8*i,p)==r]

X=[x for x in range(7) if not hit(71,x,0,26)]
assert X==list(range(6)) and hit(71,6,0,26)==[9,14,24,29]
loss=[sum(max(0,len(hit(p,x,y))-1) for p in Q)
      for x,y in product(X,range(7))]
assert min(loss)==1 and sum(loss)==2*len(loss)
assert [hit(p,0,0) for p in Q]==[[18],[6,27],[30],[]]
assert [hit(p,0,2) for p in Q]==[[12,33],[0,21],[],[]]

# The same 40 tie primes and 5-axis lock as in the 37-offset certificate.
T={31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,
   4159,5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,
   595123,3981071,5096867,9384251,12207031,16018507,190771747,
   28086211607,386478495679,6090817323763,42272797713043,625552508473588471}
def prime(p):
    return p>1 and all(p%k for k in range(2,isqrt(p)+1))

P=tuple(p for p in range(27,212,4) if prime(p))
assert all(any(pow(b,p-1,p*p)!=1 for b in (3,5)) for p in P)
V=lcm(3960,*range(2,71,4))
assert all(pow(5,V,p)==1 for p in T)

J=[i for i in I if i!=27]
active={43:18,127:6,211:30}
R=[(32,29),(3,0),(71,26),(631,0)]
D=d
trace=[]
for p,i in active.items():
    B=lcm(V,p-1,*(q*q*(q-1) for q in P if q<p))
    r=(S(c,D+8*i,p**3)+p)%p**3
    R.append((p**3,r))
    j=pow(((pow(5,B,p*p)-1)//p)*pow(5,D+8*i,p),-1,p)
    D+=B*j
    if (r-S(c,D+8*i,p**3))%p**3==0:
        D+=B*p
    trace.append((p,j,(r-S(c,D+8*i,p**3))%(p**3)//(p*p)))
assert trace==[(43,5,10),(127,66,73),(211,91,147)]

for p in (T|set(P)|{7,11,19,23})-{71,631,*active}:
    forbidden={S(c,d+8*i,p) for i in I}
    R.append((p,next(r for r in range(p) if r not in forbidden)))
M=prod(p for p,r in R)
n=sum(r*(M//p)*pow(M//p,-1,p) for p,r in R)%M

assert len(J)==22 and (n-S(c,D,32))%32==1
for i in J:
    assert all((n-S(c,D+8*i,p))%p for p in (3,7,11,19,23,31))
    for p in P:
        r=(n-S(c,D+8*i,p**3))%p**3
        assert r%p or (r and r%(p*p)==0)

assert [(n-S(c,d+1980+8*i,p*p))%(p*p)//p
        for p in (43,127) for i in hit(p,0,2)]==[6,27,61,66]
```
