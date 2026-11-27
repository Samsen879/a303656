# Exact directional energy in an active CRT box

Let H be the hits of 3^c+5^d=n modulo Q in the exponent box [0,C]×[0,D], with gcd(Q,15)=1 and both orders longer than the corresponding widths. No two hits share a coordinate. For a direction (u,v), set x=3^u,y=5^v as units modulo Q, g=gcd(Q,x−y), and m=Q/g. Both endpoint equations give 3^c(x−y)=n(1−y) and 5^d(x−y)=n(x−1) modulo Q. If the right sides are not divisible by g no start is possible. Otherwise divide by g, obtaining unique required residues a,b modulo m. Count eligible c and d starts (with both endpoints in the box) by their lift digits (3^c−a)/m and (5^d−b)/m modulo g. If the two histograms are L,R, the exact direction count is sum_t L(t) R((n−a−b)/m−t). The lift congruence restores the starting hit and then the endpoint equation holds. Thus this is exact at prime-power precision. Since neither starting coordinate can appear twice, the count is bounded by min(sum L,sum R).

For positive u the directional counts sum to binomial(|H|,2), and the additive energy is |H|² plus twice the sum of their squares. Translating H by a U-by-V rectangle and applying Cauchy–Schwarz to the translate multiplicities gives
h²(UV)² / [(C+U)(D+V)] <= hUV + 2 sum_{u>0,v} (U−u)_+(V−|v|)_+ r(u,v).
Directional caps can replace the exact counts on the right.

At Q=169, actual direction (6,4) has lift-independent cap 3 but exact count 2. At Q=2197 the caps sum to 11, limiting the full ordinary box to five hits. The exact five hits have ten distinct positive-u differences and energy 45. The replay checks these controls and the weighted identity. A zero pair count cannot distinguish zero from one hit, and the formula does not select a suitable Q for arbitrary n.

```python
from collections import Counter
from itertools import combinations, product
from math import gcd

def direction(n,Q,C,D,u,v):
    x,y = pow(3,u,Q),pow(5,v,Q)
    g = gcd(Q,x-y)
    if n*(1-y)%g:
        return 0,0
    m = Q//g
    inv = pow((x-y)//g,-1,m) if m>1 else 0
    a,b = n*(1-y)//g*inv%m,n*(x-1)//g*inv%m
    k = (n-a-b)//m % g
    J = range(max(0,-v),min(D,D-v)+1)
    L,R = [Counter((pow(base,e,Q)-t)//m%g for e in I
                   if pow(base,e,m)==t)
           for base,I,t in ((3,range(C-u+1),a),(5,J,b))]
    count = sum(v*R[(k-i)%g] for i,v in L.items())
    return count, min(sum(L.values()),sum(R.values()))

cases = [
    (976564617,169,17,12,[(3,4),(9,8),(10,6),(15,12)],32,10),
    (100000000015521,2197,28,19,[(2,2),(8,18),(16,17),(23,6),(26,14)],45,11)
]
for n,Q,C,D,want,E,B in cases:
    assert gcd(n,Q)==1 and 4*3**C<=n<4*3**(C+1) and 4*5**D<=n<4*5**(D+1)
    assert all(pow(3,i,Q)!=1 for i in range(1,C+1))
    assert all(pow(5,i,Q)!=1 for i in range(1,D+1))
    H = [(c,d) for c,d in product(range(C+1),range(D+1))
         if (n-pow(3,c,Q)-pow(5,d,Q))%Q==0]
    assert H == want
    direct = Counter((x-c,y-d) for (c,d),(x,y) in combinations(H,2))
    stat = {(u,v):direction(n,Q,C,D,u,v)
            for u,v in product(range(1,C+1),range(-D,D+1)) if v}
    assert all(r==direct[w] for w,(r,_) in stat.items())
    assert sum(b for _,b in stat.values())==B
    assert len(H)**2+2*sum(r*r for r,_ in stat.values())==E

assert direction(976564617,169,17,12,6,4) == (2,3)
print("Exact energies, lift correction, and scattered hits verified")

# Independent weighted-translate calculation on the last actual fixture.
for U,V in product(range(1,6),repeat=2):
    z=Counter((c+a,d+b) for c,d in H for a,b in product(range(U),range(V)))
    rhs=len(H)*U*V+2*sum(max(0,U-u)*max(0,V-abs(v))*m for (u,v),m in direct.items())
    assert rhs==sum(k*k for k in z.values())
    assert len(H)**2*(U*V)**2<=rhs*(C+U)*(D+V)
print("Weighted directional identity independently checked")
```
