# Three real rows distinguish triple from pairwise phase overlap

Use the [exact pre-lift boundary test](BOUNDARY_CRT_ELIMINATION.md). On \(\Omega\) let \(E_i\) be the actual bad sets and \(S_j=\sum_{|J|=j}|\cap_{i\in J}E_i|\), with \(S_0=|\Omega|\). Intersections can be evaluated with the signed congruence-rectangle calculus. Inclusion–exclusion truncated after an odd order gives a lower bound for the number passing, and after an even order an upper bound: at a point in \(u>0\) bad sets the degree-\(j\) truncated contribution is \((-1)^j\binom{u-1}{j}\). If \(S_{d+1}=0\), the depth is at most \(d\) and order \(d\) is exact. Only cliques in the actual pair-overlap graph can contribute. If the graph has degeneracy \(\delta\) and each row contains at most \(K\) signed rectangles, charging each clique to its earliest row in a degeneracy ordering bounds the number of high-order CRT combinations by \(O(rK(1+K)^\delta)\), apart from computing pairs, checking clique adjacency, and integer arithmetic.

Identical rectangles can be merged and complete sibling subdivisions with equal weights can be coalesced pointwise. Axis marginals cannot in general be substituted for rectangles. In the actual panel \(Q=\{7,11,463\}\), put \(A=152790,B=291690,M=30503851224\) and use \(c=c_0+Ax,\ d=By\), \(0\le x<7,0\le y<11\). For the two controls:

| \(c_0\) | \(n\bmod M\) | bad cells of row 463 |
|---:|---:|---|
| 27 | 19677787997 | (0,4), (6,0) |
| 258 | 22289016899 | (0,0), (6,4) |

Both rows 7 and 11 reject exactly at \(x\ne0\) and \(y\ne0\), respectively. Each row's full two axial marginals and each pair's intersection size agree between the controls. Yet \((S_0,S_1,S_2,S_3)=(77,138,62,0)\) in the first and \((77,138,62,1)\) in the second. Thus one control gives one extension and the other gives zero; any forest bound is at least 77 bad cells here. With only two rows, a forest containing their one possible edge gives the exact bad count, so three rows are minimal for this type of failure.

The true positive side takes \(n=3^{27}+1+(5167167313+7625962806h)^2\) for nonnegative \(h\); its surviving cell \((0,0)\) is a genuine square. Both residue classes can be taken high enough that every displayed coarse cell is strictly active. The obstruction is only for this boundary on this finite panel. It is not a statement about the width or overlap of every prefix, or about the original conjecture.

```python
from itertools import combinations,product
from math import gcd,lcm
Q=(7,11,463)
A,B,M=152790,291690,30503851224
assert all(M%(p*p)==0 for p in Q)
def order(a,p):
    return next(j for j in range(1,p) if pow(a,j,p)==1)
def valuation(x,p):
    k=0
    while x%p==0:
        x//=p
        k+=1
    return k
for b,D,T in ((3,A,7),(5,B,11)):
    assert [order(b,p) for p in Q]==[6,5,462]
    assert lcm(*(order(b,p)//gcd(D,order(b,p)) for p in Q))==T
for p in Q:
    assert min(valuation(b**order(b,p)-1,p)+valuation(D*T,p)
               for b,D,T in ((3,A,7),(5,B,11)))==2
U=set(product(range(7),range(11)))
for C,n,tail,s3 in [(27,19677787997,{(0,4),(6,0)},0),
                    (258,22289016899,{(0,0),(6,4)},1)]:
    E=[{(x,y) for x,y in U
        if (n-pow(3,C+A*x,p*p)-pow(5,B*y,p*p))%(p*p) in range(p,p*p,p)}
       for p in Q]
    assert E==[{(x,y) for x,y in U if x},{(x,y) for x,y in U if y},tail]
    assert [len(e) for e in E]==[66,70,2]
    assert [len(a&b) for a,b in combinations(E,2)]==[60,1,1]
    assert len(set.intersection(*E))==s3 and len(U-set.union(*E))==1-s3
r,H=5167167313,7625962806
assert (pow(3,27,M)+1+r*r)%M==19677787997
assert (2*r*H)%M==(H*H)%M==M//2  # combined coefficient is h(h+1)
```
