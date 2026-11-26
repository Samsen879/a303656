# Root-pair budget across shared phase blocks

Let $\mu_\ell$ be the multiplicative subgroup of order $\ell$ in $\mathbb F_p^\times$. For fixed $n\ne0$ in $\mathbb F_p$, partition the nonzero-coordinate solutions of $A+B=n$ by the cosets $(A\mu_\ell,B\mu_\ell)$. Across all blocks the number of unordered pairs of distinct solutions in the same block is at most $(\ell-1)(\ell-2)/2$. Indeed write a second solution as $(zA,wB)$. Both ratios differ from one, and they cannot be equal since $n\ne0$. A choice of distinct $z,w$ determines the ordered pair via $A=n(1-w)/(z-w)$ and $B=n(z-1)/(z-w)$. Each unordered pair occurs in the two orientations. Thus root multiplicities in different blocks are coupled even though each block separately has a capacity bound.

For $\ell=3$, there is at most one double-root coset block per prime. In the five-prime example of SHARED_ORDER_PHASE_CAPACITY.md, every complete weak cover must use at least four double-root primes, hence two completely covered blocks must share at least three such primes and agree on the cosets those primes read.

For the same fixed residues of $n$ as in the example, put $c=2x,d=2y$. The full shared periods for $x,y$ are $3\cdot10465,3\cdot2093$. Fixing $x\bmod10465,y\bmod2093$ specifies a coarse block with nine fine positions. Of the 21,903,245 blocks exactly three have a weak cover: $(0,0),(5915,2002),(9100,1092)$. The untouched position $(c,d)=(2,0)$ proves there is no weak cover of the entire exponent menu by this panel.

For $n=2+(505707993+14242455829t)^2+8768372146^2$, all three covered blocks are active for $t\ge5^{20930}$. When $t\equiv63437\bmod75919$, the positions $(c,d)=(0,0),(53690,33306),(39130,2184)$ have precisely one panel divisor each, respectively $139,79,31$, with valuation exactly two. The first position is a genuine square sum; the other two are only certified against this panel.

The following independent exhaustive replay uses Python standard library (several seconds):

```python
from math import lcm
P = (7,31,79,43,139)
A,B,M = 505707993,8768372146,14242455829
N = 2+A*A+B*B

def order(a,p):
    return next(k for k in range(1,p) if pow(a,k,p)==1)

orders = [(order(9,p),order(25,p)) for p in P]
assert all(i%3==j%3==0 and i%9 and j%9 for i,j in orders)
periods = [(i//3,j//3) for i,j in orders]
DX,DY = (lcm(*(pair[k] for pair in periods)) for k in (0,1))
assert (DX,DY)==(10465,2093)
tables=[]
for p,(h,k) in zip(P,periods):
    tables.append([[sum(1<<(3*u+v) for u in range(3) for v in range(3)
        if (pow(9,next(z for z in range(a,3*h,h) if z%3==u),p)
          +pow(25,next(z for z in range(b,3*k,k) if z%3==v),p)-N)%p==0)
        for b in range(k)] for a in range(h)])
found=[]
for a in range(DX):
    f,g,h,i,j = [T[a%u] for T,(u,v) in zip(tables,periods)]
    for b in range(DY):
        if f[b%len(f)]|g[b%len(g)]|h[b%len(h)]|i[b%len(i)]|j[b%len(j)] == 511:
            found.append((a,b))
assert found == [(0,0),(5915,2002),(9100,1092)]
assert all((N-3**2-1)%p for p in P)
t0,S = 63437,75919
a0=A+M*t0
n=2+a0*a0+B*B
for phase,c,d,p in [(found[0],0,0,139),(found[1],53690,33306,79),(found[2],39130,2184,31)]:
    assert (c//2%DX,d//2%DY)==phase
    assert [q for q in P if (n-pow(3,c,q)-pow(5,d,q))%q==0] == [p]
    q=p**3
    v=(n-pow(3,c,q)-pow(5,d,q))%q
    assert v=={139:19321,79:156025,31:10571}[p] and v%p**2==0 and v!=0
    assert 2*a0*M*S%q == (M*S)**2%q == 0
assert M>2 and max(3**60060,5**33306)<(M*5**20930)**2//4
```
