# A reserved ordinary row preserves terminal units without an exact sum

**All 140 cells are recoverable when the terminal only needs to remain a unit.** The exact-sum obstruction still holds. On the original \(43\to431\) fixture, a base-3 repair at \(43\) already leaves every \(431\) and terminal reading a unit. Two companion targets exercise the harder cases: an earlier repair can create a terminal hit, and the terminal can veto the first legal \(431\)-repair choice.

### Reserve the last ordinary repair row

Let \(r\) be an ordinary row with both axes fast and both first \(r\)-digits free. Assume retained readings are blind to the proposed edits and each active terminal reads at most the first \(r\)-digit. Fix the earlier repairs first.

If the remainder at \(r\) is a unit, take the diagonal of first-digit choices. Otherwise, lifting to zero modulo \(r^2\) gives an affine line \(y=\lambda x+\mu\bmod r\), with \(\lambda\ne0\). In either case there are \(r\) choices. The second digit finishes any needed lift to exact valuation two while preserving the terminal readings.

On this line, each active terminal sees \(A X^x+B Y^x\), where \(X,Y\) have order dividing \(r\) and at least one is nontrivial. If \(X\ne Y\), two hits at a fixed nonzero difference \(d\) determine \(A X^x,BY^x\) uniquely from the two sum equations. There is therefore at most one ordered hit pair for each \(d\ne0\). A terminal vetoes at most
\[
\left\lfloor\frac{1+\sqrt{4r-3}}2\right\rfloor
\]
choices. If \(X=Y\), the function is injective or identically zero. A nonzero observation \(n\bmod q\) excludes the whole-line veto in the latter case. For zero observations, that cancellation must be checked separately. [Predecessor fibre argument](https://github.com/Samsen879/a303656/commit/33e3b88d306125d55cc8f99c440d2356becb194e)

If the sum of terminal veto bounds is less than \(r\), some choice passes all terminals. Check terminals blind to \(r\) before selecting the line, since their value is constant throughout it. Any subsequent ordinary repairs must preserve the selected terminal readings. At \(r=431\), one terminal vetoes at most 21 choices, so testing the first 22 suffices even after an earlier repair has created a terminal hit. [Protected ordinary continuation](https://github.com/Samsen879/a303656/commit/2e2c5d54904e266ee271fb9ea237dcd12cc86780)

### Replay of the interacting fixture

The original target gives 140 failures under exact sum preservation modulo \(q^2\) and **zero failures** under the terminal-unit rule. At cell \((0,7)\), retain the same upstream readings and use the earlier two-axis \(43\)-repair. Now \(431\) needs a lift and its line is \(y=51x+73\bmod431\). Two companion targets, obtained by changing only the terminal congruence, give these controls.

| Terminal observation | Effect | Selected \(x\) | Final terminal shift |
|---:|---|---:|---:|
| 3,871,968 | The \(43\)-repair creates a terminal hit | 0 | 1,688,684 |
| 1,688,684 | The first legal \(431\) choice hits the terminal | 1 | 5,340,749 |

Both finish with exact valuation two at \(43,431\) and a unit at \(q\). The other ordinary repairs in the same earlier inert prefix can still be made afterward: their own prime digits are blind to \(q\), \(43^3\), \(431^3\), and the retained \(31^3\) reading. This establishes phase availability for the fixture. It leaves the exact-sum obstruction intact and supplies neither an ordinary exponent-height bound nor a density subtraction.

```python
from math import isqrt, lcm

p,t,q = 43,431,23611043
m,Q = p*t,q*q
n = 178924623518619438474129205419586877315
D = lcm(3960,49,31**2,q*(q-1)//m)
W = lcm(3960,31**2,q*(q-1)//49,p*p,t*t)
c0,d0 = m*D,D
Hp,Ht = D*t*t,D*p*p

def S(c,d,M):
    return (pow(3,c,M)+pow(5,d,M))%M

assert q-1==2*49*13*p*t and t-1==10*p
assert all(z%4==3 and all(z%i for i in range(2,isqrt(z)+1))
           for z in (p,t,q))
for b in (3,5):
    assert all(pow(b,r-1,r*r)!=1 for r in (p,t))
    assert pow(b,Ht,q)!=1 and pow(b,t*Ht,q)==1
assert n%q==20234200
assert all((n-S(c0,d0,z))%z==1 for z in (3,7,11,19,23,31**3))

def adjust(N,c,d,r,h,k,target):
    M=r**(k+1)
    R=(N-S(c,d,M))%M
    delta=(S(c+h,d,M)-S(c,d,M))%M
    assert (R-target)%r**k==delta%r**k==0
    digit=(R-target)//r**k*pow(delta//r**k,-1,r)%r
    return c+h*digit,d

def early(N,c,d):
    if (N-S(c,d,p))%p:
        return c,d
    c,d=adjust(N,c,d,p,Hp,1,0)
    return adjust(N,c,d,p,p*Hp,2,p*p)

def reserve(N,c,d):
    R=(N-S(c,d,t*t))%(t*t)
    if R%t:
        la,mu=1,0
    else:
        a=((pow(3,c+Ht,t*t)-pow(3,c,t*t))%(t*t))//t
        b=((pow(5,d+Ht,t*t)-pow(5,d,t*t))%(t*t))//t
        la,mu=-a*pow(b,-1,t)%t,(R//t)*pow(b,-1,t)%t
    cap=(1+isqrt(4*t-3))//2
    for x in range(cap+1):
        y=(la*x+mu)%t
        C,E=c+Ht*x,d+Ht*y
        if (N-S(C,E,q))%q:
            if not R%t:
                C,E=adjust(N,C,E,t,t*Ht,2,t*t)
            return C,E,x,la,mu
    raise AssertionError("capacity exceeded")

# Recompute the exact-sum failures for comparison.
def bad(c,d,r):
    z=(n-S(c,d,r*r))%(r*r)
    return z%r==0 and z!=0

X=[pow(3,D*i,Q) for i in range(m)]
Y={pow(5,D*i,Q):i for i in range(m)}
assert len(set(X))==len(Y)==m
fibres={}
failed=0
for i in range(49):
    for j in range(49):
        c,d=c0+W*i,d0+W*j
        a,b=pow(3,c,Q),pow(5,d,Q)
        k=a*pow(b,-1,Q)%Q
        if k not in fibres:
            fibres[k]=[(u,Y[y]) for u,x in enumerate(X)
                       if (y:=(1+k*(1-x))%Q) in Y]
        failed+=not any(not any(bad(c+D*u,d+D*v,r) for r in (p,t))
                        for u,v in fibres[k])
        C,E=early(n,c,d)
        assert (n-S(C,E,t))%t and (n-S(C,E,q))%q
        assert (n-S(C,E,p))%p or (n-S(C,E,p**3))%p**3==p*p
        assert (C-c)%lcm(3960,49)==(E-d)%lcm(3960,49)==0
assert failed==140 and len(fibres)==49

# Stress the last repair at the exact-sum-obstructed cell (0,7).
def piece(u):
    return t*t*(u*pow(t*t,-1,p*p)%(p*p))
off=(c0,d0+7*W)
mid=(off[0]+D*piece(5348),off[1]+D*piece(18532))
L=32*3*7*11*19*23*31**3*p**3*t**3

for T,chosen,shift in ((3871968,0,1688684),(1688684,1,5340749)):
    N=n+L*((T-n)*pow(L,-1,q)%q)
    C,E,x,la,mu=reserve(N,*mid)
    assert (x,la,mu)==(chosen,51,73)
    assert S(*off,q)==15162440 and S(*mid,q)==3871968
    assert S(C,E,q)==shift and shift!=T
    assert (N-S(*mid,p**3))%p**3==p*p
    assert (N-S(*mid,t*t))%t==0 and (N-S(*mid,t*t))%(t*t)!=0
    assert (N-S(C,E,p**3))%p**3==p*p
    assert (N-S(C,E,t**3))%t**3==t*t
    if chosen==1:
        assert S(mid[0],mid[1]+73*Ht,q)==T
```

Independent BigInt checked the earlier base-3 repair and later units on all 2401 cells, as well as both companion CRT targets and their exact valuation-two endings. The distinction between exact sum and unit preservation is essential; no ordinary-height conclusion follows.
