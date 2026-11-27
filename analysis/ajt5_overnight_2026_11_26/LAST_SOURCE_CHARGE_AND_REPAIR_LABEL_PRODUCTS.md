# Last-source charging and independent repair-label products

**A matched lower anchor can support a genuine product of future repair choices.** The sufficient condition is that the repair sources do not read one another and each higher protected row reads at most one source. When higher rows read several sources, a chronological rule still gives a branching lower bound. In the actual \(3,5\) prefix through \(827\), each of two matched lower anchors retains \(46\times58=2668\) independent repair choices at the same integer target.

### Charge each higher reader to its last repair source

Start from one surviving cell for each chosen lower-anchor pair. Let \(R\) be a set of inert repair primes, ordinary on both bases, with their first two native digits free on both axes. Their CRT moves must preserve the anchor tests. A stride that fixes the required first digit disqualifies that axis.

At \(p\in R\), condition on the earlier source choices. If the remainder is divisible by \(p\), its vanishing modulo \(p^2\) imposes an affine line \(y=\lambda x+\mu\) on the two first \(p\)-primary digits, with \(\lambda\ne0\). Every point of this line has a second-digit refinement giving exact valuation two. If the remainder is a unit, any such line can be used. [Ordinary-primary repair framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

Assign each higher protected row \(q\) to the **largest** source \(p\in R\) it reads on either axis. Require \(q\) to read at most the first native digit on each axis of every source it sees. The second-digit refinements then preserve its residue. When \(p\) is reached, all other source reads of \(q\) have been settled.

A row reading just one axis forbids at most one line parameter. For a row reading both axes, use the actual order-\(p\) subgroup at \(q\) to write its collision equation on the repair line as
\[
A g^x+B g^{kx}=n\bmod q,
\qquad \operatorname{ord}_q(g)=p.
\]
For \(k\ne1\), two hits at \(x,x+\delta\), with \(\delta\ne0\), determine \(g^x\) uniquely. The two equations have determinant proportional to \(g^{k\delta}-g^\delta\), which is nonzero. Thus \(H\) hits use \(H(H-1)\) distinct nonzero directed differences, giving
\[
H\le \rho(p)=\max\{h:h(h-1)\le p-1\}.
\]
For a zero reading with \(k\ne1\), direct division gives at most one hit. For \(k=1\), there is at most one hit except when \(n\equiv0\bmod q\) and the coefficients cancel, in which case the whole line is lost. That exception must be checked on the actual branch.

If the total charge at each source is at most \(B_p<p\) uniformly over earlier choices, each matched anchor has at least \(\prod_{p\in R}(p-B_p)\) completions in its source digits. Later sources preserve the rows already protected. Other rows in a chronological prefix must already pass or have an ordinary repair axis unread by the protected rows, including the native repair rows. **The product counts a branching tree in general.** It is a Cartesian product of repair labels if the native rows do not read one another and each higher protected row sees at most one source.

### Exact \(3,5\) control through \(827\)

Use the ternary lower-anchor pairs \((1,2)\) and \((2,1)\), which both pass the zero reading at \(19\). Release both native axes at \(47\) and \(59\). Row \(283\) reads both axes of \(47\), and row \(827\) reads both axes of \(59\). Neither reads the other source. Their target residues are \(22\) and \(15\), respectively. Each deletes exactly one line parameter in each anchor branch. The replay checks every combination against the 73 inert unit rows through \(827\), as well as the tests at \(2,3\).

```python
from math import isqrt, lcm, prod

R = (47,59)
Q = {47:283, 59:827}
P = [p for p in range(7,828,4) if all(p%d for d in range(2,isqrt(p)+1))]
assert len(P) == 73 and {19,*R,*Q.values()} <= set(P)
assert all((q-1)%p for p in R for q in R+tuple(Q.values())
           if q not in (p,Q[p]))
m = {p:p for p in P} | {2:4,3:3,47:47**3,59:59**3}
L = lcm(8, *(a-a//p for p,a in m.items() if p!=3))

def step(p):
    a = p
    while L%(a*p)==0:
        a *= p
    return (L//a)*pow(L//a,-1,a)

E = {p:step(p) for p in (3,)+R}
c0,d0 = L+9,L
anchors = [(c0+i*E[3],d0+j*E[3]) for i,j in [(1,2),(2,1)]]

def off(p,c,d):
    if p==3:
        return pow(5,d%2,3)
    a = m[p]
    T = a-a//p
    return (pow(3,c%T,a)+pow(5,d%T,a))%a

t = {2:1,3:0,19:0,283:22,827:15}
assert all(off(19,c,d) for c,d in anchors)
line = {}
for p in R:
    assert all(pow(g,E[3],m[p])==1 for g in (3,5))
    t[p] = (off(p,c0,d0)+p)%m[p]
    a,b = [(pow(g,E[p],m[p])-1)//p*pow(g,z,p)%p
           for g,z in [(3,c0),(5,d0)]]
    assert a and b
    line[p] = []
    for x in range(p):
        y = (1-a*x)*pow(b,-1,p)%p
        s,w = x*E[p],y*E[p]
        if off(p,c0+s,d0+w)==t[p]:
            s += p*E[p]
        line[p].append((s,w))
    q = Q[p]
    assert (q-1)%(p*p)
    assert all(pow(g,E[p],q)!=1 and pow(g,p*E[p],q)==1 for g in (3,5))

for p in P:
    if p not in t:
        reads = [r for r in R if (p-1)%r==0]
        assert len(reads)<=1
        moves = line[reads[0]] if reads else [(0,0)]
        banned = {off(p,c+s,d+w) for c,d in anchors for s,w in moves}
        t[p] = next(z for z in range(p) if z not in banned)

M = prod(m.values())
n = sum(t[p]*(M//a)*pow(M//a,-1,a) for p,a in m.items())%M
for c,d in anchors:
    good = [[(s,w) for s,w in line[p] if (n-off(Q[p],c+s,d+w))%Q[p]]
            for p in R]
    assert list(map(len,good)) == [46,58]
    for s,w in good[0]:
        for u,v in good[1]:
            x,y = c+s+u,d+w+v
            assert (n-off(2,x,y))%4==1 and (n-off(3,x,y))%3
            for p in P:
                z = (n-off(p,x,y))%m[p]
                assert (z and z%(p*p)==0) if p in R else z%p
```

The two lower anchors remain paired. The independent choices are the new \(47\)- and \(59\)-primary repair labels *within each pair*. The full-prefix example uses one constructed CRT target. A sufficiently large positive lift activates the displayed exponents, while the argument gives no height bound at a prescribed target and no two-square certificate.

Independent BigInt rebuilt the complete CRT target and checked all 5,336 displayed repair combinations against all 73 inert unit rows and the initial 2,3 tests. The product counts local digit choices, not a least-height guarantee, not a Cartesian product of the original lower matches, and not a sum-of-two-squares certificate.
