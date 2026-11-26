# Joint chart occupancy gives representation density above 99.981590%

**The exception-density bound improves to below \(0.018410\%\)** without enlarging the search. The finite \(D=81\) charge falls from \(0.00010897636\) to \(0.00009636386\) in density units. Every other charge in the predecessor’s rational total carries forward. [Predecessor certificate](https://github.com/Samsen879/a303656/blob/7fcaf635f009790f3e44e453f4f1fd956279a564/analysis/ajt5_overnight_2026_11_26/OCCUPANCY_AND_CATALOGUE_DENSITY_BOUND.md)

| \(D=81\) calculation | Outward-rounded charge |
|---|---:|
| Predecessor | \(0.00010897636\) |
| Separate shallow and deep occupancy, same integration range | \(0.00010523665\) |
| Use the actual dyadic branch endpoint | \(0.00009784517\) |
| Also account for the auxiliary-axis recovery | **\(0.00009636386\)** |

### Which readers the auxiliary axis can clear

Let \(b\) be the axis giving nine distinct terminal shifts. Drop its older readers \(\mathcal B\), and also drop the readers \(\mathcal A\) that see the auxiliary axis but do not see the released \(b\)-digits. Choose a phase satisfying the retained rows before reading either group. After reading \(\mathcal A\), keep this phase if it passes \(\mathcal A\), and otherwise use a retained-prefix extension if one exists. The reference nine-phase chart is therefore chosen before reading \(\mathcal B\).

A shallow \(b\)-only reader can kill the same prefix on every auxiliary chart. The exact ordinary control below does this at \(379\). It also shows that \(D=81\) need not make both terminal axes visible: the orders at \(3727\) have \(3\)-depths \(4,2\).

A shallow reader that also sees the auxiliary axis behaves differently. For such a reader \(p_*\), vary the auxiliary digit at its highest \(3\)-order position. This gives three charts, all preserving the locked small head. The \(3\times3\) array of shifts at \(p_*\) is a sum of two order-three cosets. A nonzero observation can match at most two cells. Three matches would be a full matching, and summing them would force the observation to be zero. Thus if \(p_*\) kills a prefix on the reference chart at a nonzero observation, **one alternate chart has no hit at all from \(p_*\)**. At the ordinary reader \(1567\), both alternate charts in the replay have this property.

### A disjoint saving in the cover count

Write \(s,t\) for the shallow and deep weights on axis \(b\), and set \(J=53/250\), the existing upper bound on \(s+t\). Let \(M_b\) be the weight of the verified shallow readers \(p\le3456\) that also see the auxiliary axis. No new reader window is used.

Consider exactly three shallow hits on the reference chart, one from a named reader \(p_*\) in \(M_b\) and two from outside that set. Require the hits to kill different prefixes. At least four of the six assignments give a nonzero observation at \(p_*\). For its three charts, all \(\mathcal A\)-rows pass with probability at least \(1-3J\). On a chart where \(p_*\) has no hit, the other two named hits leave at least one full prefix. Choose two distinct terminal shifts there before reading the remaining \(\mathcal B\)-rows.

For any other shallow reader, forbid its three possible reference-chart hits and its two possible hits on the selected alternate phases. For a deep reader, forbid only the two alternate hits. The product of the resulting pass probabilities is at least \(1/3\), using \(w_p\le1/164\) and \((820/159)J<\log3\). These events are disjoint across triples and assignments because exactly those three shallow readers hit the reference chart. They are counted in its cover event, while the alternate chart supplies two old survivors with distinct terminal shifts.

Consequently the following quantity can be subtracted from the reference-chart cover bound:
\[
\delta_b\left[(s-M_b)^2-\frac{s-M_b}{164}\right]_+,
\qquad \delta_b=\frac23(1-3J)M_b.
\]
This uses independence between distinct prime observations. It imposes no independence between two phases at the same prime.

Use the predecessor’s single-cell occupancy bound \(U(x)=ax-(ax)^2/2+(ax)^3/6\), with \(a=327/326\), at **both** depths. The resulting cover bound is \(P(U(s),U(t))\) minus the saving above, where \(P(x,y)=x^3+9x^2y^2+18xy^5+9y^8\). For fixed \(t\), this expression increases with \(s\). After padding \(s+t\) to the existing envelope \(L\), it is maximized at the verified deep lower bound \(t=\tau_b\). The replay checks the derivative bound for \(t\le L/2\), and a separate upper bound for \(t\ge L/2\).

Finally, \(D=81\) is selected only when \(81>\lfloor(4/5)\log Y\rfloor\) in the dyadic interval \([Y,2Y)\). Hence \(\log q<405/4+\log2<102\). This sharpens the previous endpoint \(108\) using the same branch rule. [Original dyadic selection rule](https://github.com/Samsen879/a303656/blob/7fcaf635f009790f3e44e453f4f1fd956279a564/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_EXPLICIT_DENSITY_BOUND.md)

### Standalone rational replay

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt

W = 10**11

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s,s+2*z**25/(25*(1-z*z))

l2,u2 = series(Q(2))
def logs(x):
    y,k = Q(x),0
    while y>=2:
        y /= 2
        k += 1
    a,b = series(y)
    return Q(floor(W*(a+k*l2)),W),Q(ceil(W*(b+k*u2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)

def depth(b,p):
    m = p-1
    while m%3==0 and pow(b,m//3,p)==1:
        m //= 3
    k = 0
    while m%3==0:
        k += 1
        m //= 3
    return k

a,J,b,d,ell = Q(327,326),Q(53,250),Q(89,100),Q(39,50),Q(1,8)
T,E = Q(11,1000),Q(1,400)
assert Q(405,4)+hi(2)<102 and lo(9*10**14)>34
assert 1-a*J/2>=b and a*(1-a*J)>=d and a*J<1
assert 0<1-3*J and Q(820,159)*J<lo(3)
assert 3*b*b*d>Q(4,3)

j = J/2
D = 3*d-18*a*a*j-90*a**5*j**3/b-72*a**8*j**5/b**2
assert D*b*b*ell/2>2*E          # decreasing for t <= L/2
coarse = a**3/8+9*a**4*J/16+18*a**6*J**3+9*a**8*J**5
assert coarse<Q(1,2)<(b*(1-T/ell))**3-E/ell
assert 3*a**3+18*a**4*T*T/ell+18*a**6*T**5/ell**2<4
assert 4<18*34*ell/2           # terminal weight decreases after /q

stats = []
for g,h,c in ((3,5,Q(47,50)),(5,3,Q(221,250))):
    rows = [(p,depth(g,p),depth(h,p)) for p in range(55,3457,108)
            if all(p%i for i in range(2,isqrt(p)+1))]
    total = sum(Q(1,p+1) for p,k,_ in rows if k>=3)
    tau = sum(Q(1,p+1) for p,k,_ in rows if k>=4)
    M = sum(Q(1,p+1) for p,k,l in rows if k==3 and l>=3)
    delta = Q(2,3)*(1-3*J)*M
    assert lo(lo(32))-Q(1,34)-18*total>c
    assert (hi(108)-c)/18<J and (lo(34)-c)/18>ell
    assert tau<T and M+tau<ell and delta<E
    stats.append((c,tau,M,delta))

def U(s):
    x = a*s
    return x-x*x/2+x**3/6

def P(x,y):
    return x**3+9*x*x*y*y+18*x*y**5+9*y**8

def num(u,mode):
    vals = []
    for c,t,M,delta in stats:
        L = (hi(u)-c)/18
        s = L-t
        F = U(L)**3-t*L*L/8 if mode==0 else P(U(s),U(t))
        if mode==2:
            F -= delta*max(0,(s-M)**2-(s-M)/164)
        vals.append(F)
    return max(vals)

l,u = logs(324)
def charge(end,mode):
    return up((num(end,mode)/(end-u)+sum(
        num(t+1,mode)*hi((t+1-l)/(t-u)) for t in range(34,end)))/54)

old,new = charge(108,0),charge(102,2)
assert (old,charge(108,1),charge(102,1),new)==tuple(
    Q(i,W) for i in (10897636,10523665,9784517,9636386))
base = Q(9835340121236751,50000000000000000000)
answer = base-old+new
assert answer==Q(9204715121236751,50000000000000000000)
assert answer<Q(18410,10**8)

# Ordinary controls: one reader keeps its hits, the other loses them.
n,C,L,q = 122548072133633223,3960,10980630211320,3727
assert pow(3,9*L,q)==1 and pow(3,3*L,q)!=1 and pow(5,L,q)==1
assert all(pow(b,p-1,p*p)!=1 for p in (379,1567,q) for b in (3,5))
for j in range(3):
    for p in (379,1567):
        bad = [i for i in range(9)
               if (n-pow(3,C+L*i,p*p)-pow(5,C+L*j,p*p))%(p*p)
               in range(p,p*p,p)]
        assert bad==([0,3,6] if p==379 or j==0 else [])
print("OK:",float(100*answer),"%")
```

The replay gives \(0.0184094302424735\ldots\%\). The controls are ordinary, while the bound applies to the genuine exceptional terminals in the first-blocker sum without assuming any exist. The result bounds growth-box misses and hence all-exponent exceptions.

For the subtraction, conditional on retained observations, use the reference chart chosen without the \(\mathcal B\) observations. If no retained extension through \(\mathcal A\) exists, the initial older prefix has no survivor and this terminal cannot be the first blocker. In the subtracted event the original phase passes \(\mathcal A\) on all three charts, so it is the reference. At the named shallow reader, summing the three hypothetical matches would give three times the nonzero observation equal to zero, which is impossible since \(p_*>3\). The bound \(820/159\) comes from \(-\log(1-5w)\le 5w/(1-5w)\) at \(w\le1/164\); it also bounds the smaller deep charge.

The optimization in the replay compares the \(t\)-derivative along \(s=L-t\) on \(t\le L/2\) after factoring out \(U(s)^2\). On \(t\ge L/2\) the coarse expression bounds the whole numerator by \(L^3/2\), below its value at the verified \(\tau_b\). The inherited terms outside the \(D=81\) charge are unchanged.
