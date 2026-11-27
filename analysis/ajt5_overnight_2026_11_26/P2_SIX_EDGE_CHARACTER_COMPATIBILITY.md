# Six edge characters and a true-divisor control for P2

A necessary six-edge norm restriction couples the possible signs of four half-roots. A true pinned divisor passes all six characters and the finite local tests in the replay below, so these restrictions do not decide the ordinary divisor match. [Pinned family](P2_COPRIME_RATIO_EXACT_INTERSECTION.md)

### The integer restriction

Use \(g=468741\), \(N=1331g\), \(a=Nh+1\), \(b=Nk-2\), \(A=3^a\), and \(B=5^b\). The shifts are
\[
(S_0,S_1,S_2,S_3)=(A+25B,\ 9A+625B,\ 81A+125B,\ 729A+B).
\]
Write \(X_i=\sqrt{K-S_i}/2\). These are integer half-roots at a solution, since \(S_2-S_0\equiv4\pmod8\) forces the full roots even. For the six ordered edges below, the positive difference \(\delta_{ij}=X_i-X_j\) divides \((S_j-S_i)/4\).

| Edge | Product | Quadratic discriminant |
|---|---|---:|
| \(01\) | \(2A+150B\) | \(-3\) |
| \(02\) | \(20A+25B\) | \(-20\) |
| \(03\) | \(182A-6B\) | \(273\) |
| \(21\) | \(-18A+125B\) | \(40\) |
| \(13\) | \(180A-156B\) | \(780\) |
| \(23\) | \(162A-31B\) | \(248\) |

For a product \(\alpha A+\beta B\), every prime divisor outside \(2,3,5,7,13,31\) sees \(-\alpha\beta\) as a square, since \(A,B\) are squares. Thus, after stripping those six primes from each *true* \(\delta_{ij}\), its character for the displayed discriminant must be \(+1\). The local contributions must multiply to \(+1\) **for the same four root signs**. For example, in the control below, flipping the signs of \(X_2,X_3\) at \(31\) preserves the local squares but makes the \(23\) character negative.

### True-divisor countercontrol

With \(x=3^h,y=5^k\), keep
\[
H=w_*R=\Phi_{242g}(x,y)\!\!\prod_{j\in\{g,3939,1717\}}\!\Phi_{2662j}(x,y),
\qquad E=6(x^{11g}+y^{11g}),
\]
using homogeneous cyclotomic factors. The replay checks
\(\ell=2245463313841658548916704452\mid E\), so \(v=H\ell\) and \(u=d/v\) are actual integers. The first two half-roots are exactly \((u+v)/2,(u-v)/2\); the last two entries in each replay row are local root choices.

The displayed true divisor is a control for this finite set of constraints. There is no claim that the last two roots are integers or that the control solves the ordinary-height matching problem.

```python
from itertools import combinations
from math import prod

a = 37870754619013993871747199180569871088107623520881950822
b = 25850811692797692250022937755626071902314272651677455204
g = 468741
h, k = (a-1)//(1331*g), (b+2)//(1331*g)
assert (a,b) == (1331*g*h+1,1331*g*k-2)
ell = 2245463313841658548916704452
assert (pow(3,11*g*h,ell//6)+pow(5,11*g*k,ell//6)) % (ell//6) == 0

def strip(x,p):
    assert x
    d = 0
    while x%p == 0:
        x //= p
        d += 1
    return d,x

def half_pair(p,n):
    m = p**n * (2 if p==2 else 1)
    H = 1
    for j,ps in ((3,(3,7,13,17,101)),(3,(3,13,101)),(3,(17,101)),
                 (2,(3,7,13,17,101))):
        index, depth = 11**j * prod(ps), 0
        for i in range(len(ps)+2):
            for sub in combinations((11,)+ps,i):
                t, big = index//prod(sub), m*p**8
                d,unit = strip((pow(3,h*t,big)+pow(5,k*t,big))%big,p)
                depth += (-1)**i*d
                H = H*pow(unit,(-1)**i,m)%m
        assert depth == 0
    d,unit = strip(ell,p)
    A,B = pow(3,a,m*p**d),pow(5,b,m*p**d)
    u = 2*(A+75*B)//p**d * pow(unit*H,-1,m)%m
    v = ell*H%m
    half = lambda x: x//2 if p==2 else x*pow(2,-1,m)
    return half(u+v),half(u-v),20*A+25*B,182*A-6*B

def char(p,c,x):
    if p != 2:
        y = pow(x,(p-1)//2,p)
        assert y in (1,p-1)
        return 1 if y==1 else -1
    s,t = (-1)**((x-1)//2), (1 if x%8 in (1,7) else -1)
    return {4:s,8:t,-8:s*t}[c]

edges = ((0,1),(0,2),(0,3),(2,1),(1,3),(2,3))
chi = ({3:1},{2:4,5:1},{3:1,7:1,13:1},{2:8,5:1},
       {2:4,3:1,5:1,13:1},{2:-8,31:1})
rows = ((2,10,8,(175,235,58,1)),(3,6,2,(1,7,3,4)),
        (5,3,2,(18,16,12,6)),(7,6,3,(222,23,119,3)),
        (13,4,3,(2009,995,927,316)),(31,3,1,(29,1,8,11)))
signs = [1]*6
for p,n,L,r in rows:
    S,X,e,f = half_pair(p,n)
    assert (S%p**L,X%p**L) == r[:2]
    for y,c in zip(r[2:],(e,f)):
        power = L+strip(y,p)[0]+(p==2)
        assert power<=n and (y*y-S*S+c)%p**power==0
    for i,((j,l),C) in enumerate(zip(edges,chi)):
        d,t = strip((r[j]-r[l])%p**L,p)
        if p in C:
            signs[i] *= char(p,C[p],t)
        signs[i] *= prod(char(q,c,p)**d for q,c in C.items() if q!=p)
assert signs == [1]*6
S,_,e,f = half_pair(11,3)
assert (4*(S*S-e)%1331,4*(S*S-f)%1331) == (363,531)
print("true divisor, exact quotient, six compatible signs")
# The same local squares permit another sign choice that fails edge 23.
p,L=31,1
old=(29,1,8,11)
new=(29,1,-8,-11)
for j in (2,3):
    assert (old[j]**2-new[j]**2)%p**L == 0
old_diff=(old[2]-old[3])%p
new_diff=(new[2]-new[3])%p
assert old_diff and new_diff and char(31,1,old_diff)==-char(31,1,new_diff)
assert ell%6==0
from math import lcm
# The H factors' indices are valid pairwise distinct factors of x^N+y^N.
indices=[242*g,*[2662*j for j in (g,3939,1717)]]
m=1331*g
assert len(set(indices))==4
assert all(i%2==0 and m%(i//2)==0 and m//(i//2)%2==1 for i in indices)
assert all(11*g%(i//2)!=0 for i in indices)
print("edge-23 flip; exact disjoint cyclotomic factors")

```

Each character applies after removal of the six exceptional primes, so the remaining factor is coprime to its conductor. For a prime not in that list, divide the edge product identity by a nonzero square modulo the prime to see that the square class of minus the coefficient product is trivial. The factors of the stripped edge difference inherit the same property individually. The finite test preserves a common choice of all four root signs at a prime. It does not impose any independent choices of edge signs and does not imply global integrality of the last two roots.
