# Middle-prime transversals after protected exponent lifting

After the protected small-prime step, the same ordinary target admits a transversal against any prescribed list of \((\log n)^{1/2-o(1)}\) inert primes of size \(\asymp\log n\), drawn from an explicitly defined set containing almost all inert primes in that band. The proof uses their actual orders under the protected stride. It needs no independence of root phases.

The cardinality condition matters. On a separate cofinal family of genuine targets, \(m\) distinct middle primes of order at least \(m\) can block all \(m\) sampled labels at exact odd depth. On the original pinned target, a short-order prime can itself block several columns. [Verified switching baseline](https://github.com/Samsen879/a303656/commit/55ac4fc3ad0341a73adb69f3c8017805c88b755d)

### Middle-prime bound at a fixed target

After a successful protected step, hold \(n,x,y_0\) fixed and write
\[
r_t=n-3^x-5^{y_0-\Lambda t},\qquad 0\le t<m .
\]
Here \(\Lambda\) preserves the small-prime checks, and \(W\) is the available downward room in the \(5\)-exponent. For \(q\ne5\), set \(d_q=\operatorname{ord}_q(5^\Lambda)\). If \(q\) divides two remainders, subtraction gives \(d_q\mid t-s\). Thus a prime with \(d_q\ge m\) can eliminate at most one column.

Take the middle band \([X,2X]\) and suppose every prime factor of \(\Lambda\) is at most \(Y=\max(31,\lceil\log_2 X\rceil)\). Define
\[
k=\lceil\log_2Y\rceil,\quad G=Y^{11k},\quad
R=\left\lfloor\frac{\sqrt X}{Y}\right\rfloor,\quad
m=\min\!\left(1+\left\lfloor\frac W\Lambda\right\rfloor,
                    \left\lfloor\frac R G\right\rfloor\right).
\]
Discard primes with \(\operatorname{ord}_q(5)<R\) or \(\gcd(q-1,\Lambda)>G\). Every remaining prime has \(d_q\ge m\), so **any list of at most \(m-1\) remaining primes leaves a column passing the whole list**.

Both discard counts are \(O(X/(\log X)^3)\).

- A prime of raw order below \(R\) divides \(\prod_{1\le d<R}(5^d-1)\), whose logarithm is at most \(R(R-1)\log 5/2\). Each distinct prime in the band costs at least \(\log X\).
- For the gcd exception, count all integers \(q\le2X\) with a divisor \(d>G\) of both \(q-1\) and \(\Lambda\). With \(s=1/k\), their number is at most
  \[
  2X\sum_{\substack{d\mid\Lambda\\d>G}}\frac1d
  \le 2XG^{-s}\prod_{p\mid\Lambda}(1-p^{-1+s})^{-1}
  \le \frac{2X}{Y^3}.
  \]
  The product is at most \(Y^8\) since \(p^s\le2\), \(p^{-1+s}\le 2^{-1/2}\), and \(\sum_{p\le Y}1/p\le\log Y\).

Set \(X=b\) on the balanced family. The previous successful lifts through \(Z=\lfloor(\log_2 b)/30\rfloor\) use only primes at most \(Y\) in the stride, with \(\Lambda=O(b^{2/5})\). With \(W\asymp b\), this gives \(m=b^{1/2-o(1)}\). The fixed-modulus prime number theorem gives \(\sim X/(2\log X)\) inert primes in the band, so the discarded fraction tends to zero. The guarantee concerns a sublist of that size, and still requires a successful small-prime step.

### Two arithmetic controls

**The original target.** Use \((x,y_0)=(32622,336937)\), stride \(6930\), and \(0\le t<34\). All columns retain \(125\) and the original protected checks, including the unit at \(43\). In the same band \([70,140]\), the following are the complete hit sets for these three primes. Every listed hit has exact valuation one.

| \(q\) | \(d_q\) | Hit indices |
|---:|---:|---|
| 83 | 41 | 18 |
| 107 | 53 | 15 |
| 131 | 13 | 4, 17, 30 |

**A sharp cardinality countercontrol.** Fix stride \(6930\) and \(m=\lfloor\sqrt{b/6930}\rfloor\). For all sufficiently large balanced baseline exponent pairs, choose distinct inert \(q_t\in[10b,20b]\), one for each label \(S_t\), with \(d_{q_t}\ge m\) and \(q_t\nmid S_t-S_0\). The supply is \(\sim5b/\log b\). The product \(\prod_{d<m}(5^{6930d}-1)\) rules out at most \((\tfrac12\log5+o(1))b/\log b\) of them on order grounds. The difference \(S_t-S_0\) rules out at most \((\log5+o(1))b/\log b\) more for each choice.

Build a new target in the baseline Gaussian-coordinate CRT by imposing \(n-S_t\equiv q_t\pmod{q_t^2}\). Each required norm residue for the first representation is a unit, so it is a sum of two squares modulo \(q_t\) and lifts modulo \(q_t^2\). The added CRT modulus has logarithm \(O(m\log b)=o(b)\), leaving room to round both coordinates into the original ordinary-height intervals. Once built, this one target is held fixed across all \(m\) labels. Each designated reader hits exactly its own column. The finite replay constructs seven such readers near \(3.92\) million.

In both controls, the remainders are positive and satisfy \(S_t+\tfrac45(n-S_t)>S_3\) with \(n\le U\). This is the ordinary-height condition for orienting a putative representation using the common split divisor. Passing the selected primes leaves square-sum status unresolved.

The standalone replay reconstructs the original target and independently verifies both controls, including prime orders, exact odd depths, and ordinary-height inequalities.

```python
from math import gcd, lcm

a, b = 574422, 392104
A, B = 3**a, 5**b
R, V = 5**(b//4), 5**(b//2-b//4)
panel = (3, 7, 11, 19, 23, 31)
J = 3*7*11*19*23*31

def pair(z, m):
    sq = {i*i % m: i for i in range(m)}
    return next((i, sq[(z-i*i) % m])
                for i in range(m) if (z-i*i) % m in sq)

rows = [(20, 1, 0), (11, 0, 0)]
rows += [(p*p, *pair(d*R*R+p, p*p)) for p, d in [(43, 100), (47, 600)]]
for p in (3, 7, 19, 23, 31):
    z = next(z for z in range(p) if (z-100*R*R) % p and (z-600*R*R) % p)
    rows.append((p, *pair(z, p)))

X = Y = 0
M = 1
for m, u, v in rows:
    inv = pow(M, -1, m)
    X += M*((u-X)*inv % m)
    Y += M*((v-Y)*inv % m)
    M *= m
X = V*(X+M*((917*R//25-X)//M+1))
Y = V*(Y+M*((R//200-Y)//M+1))
S0, S3, U, P = A+25*B, 729*A+B, 729*A+625*B, A+125*B
n = S0+X*X+Y*Y
assert 39*A < 40*B and 125*B < 122*A
assert 2*S3-P < n <= U and S3 < S0+X*X and n % 121 == 36


from math import isqrt

def prime(q):
    return q > 1 and all(q%d for d in range(2,isqrt(q)+1))

def order(a,q):
    x=a%q; j=1
    while x!=1: x=x*a%q; j+=1
    return j

def rem(x,y,q):
    return (n-pow(3,x,q)-pow(5,y,q))%q

P0=[q for q in range(3,272,4) if prime(q)]
x, y, c = 32622, 337927, 125
active={}
for q in P0:
    if q<=31: continue
    ell=order(pow(5,-990,q),q)
    hits=[t for t in range(ell) if rem(x,y-990*t,q)==0]
    assert len(hits)<=1
    if hits: active[q]=(hits[0],ell)
assert len(active)==8 and active[43]==(0,7) and active[107]==(0,53)
assert all(1%ell != v for v,ell in active.values())
assert 0<rem(x,y,43**2) and rem(x,y,43)==0
assert 0<rem(x,y,107**2) and rem(x,y,107)==0
for j in (336937,130027):
    s=3**x+5**j
    assert 0<s<n and (n-s)%c==0 and (n-s)%4==1
    assert 5*s+4*(n-s)>5*S3
assert all(rem(x,336937,q) for q in P0)
assert rem(x,130027,43**2)==0 and rem(x,130027,43**3)!=0
assert all(rem(x,130027,q) for q in P0 if q!=43)
assert rem(x,y,431)==35
h3,h5=lcm(100,990),990
assert order(pow(3,h3,431),431)==order(pow(5,h5,431),431)==43
assert pow(3,7*43*h3,43**2)==pow(5,7*43*h5,43**2)==1
# Stride and shared-factor arithmetic in the general transversal.
assert all(pow(5,6930,q)==1 for q in (3,7,11,19,23,31,43))
assert pow(5,990,43)!=1
assert pow(3,6930,43)==1
print("all 271-panel, two switch, and crossed-order controls passed")

# Middle-band checks on the already reconstructed target.
x,y0,stride=32622,336937,6930
for p,expected in ((83,[18]),(107,[15]),(131,[4,17,30])):
    assert [i for i in range(34) if rem(x,y0-stride*i,p)==0]==expected
    assert all(rem(x,y0-stride*i,p*p) for i in expected)
assert [order(pow(5,stride,p),p) for p in (83,107,131)]==[41,53,13]

# Rebuild one different signed-coordinate target with seven independent real vetoes.
q=10*b+((3-10*b)%4)
picked=[]
extra=[]
for i in range(7):
    y=y0-stride*i
    while True:
        if prime(q) and all(pow(5,stride*z,q)!=1 for z in range(1,7)):
            qq=q*q
            delta=(pow(3,x,qq)+pow(5,y,qq)-S0)%qq
            if delta%q:
                rhs=(delta+q)*pow(pow(V,2,qq),-1,qq)%qq
                for aa in range(q):
                    bb=pow((rhs-aa*aa)%q,(q+1)//4,q)
                    if (aa*aa+bb*bb-rhs)%q==0:break
                err=(rhs-aa*aa-bb*bb)//q
                if aa: aa+=q*(err*pow(2*aa,-1,q)%q)
                else: bb+=q*(err*pow(2*bb,-1,q)%q)
                assert (aa*aa+bb*bb-rhs)%qq==0
                extra.append((qq,aa,bb));picked.append(q);q+=4;break
        q+=4
assert len(set(picked))==7 and max(picked)<20*b
s=t=0
M=1
for mod,u,v in rows+extra:
    inv=pow(M,-1,mod)
    s+=M*((u-s)*inv%mod);t+=M*((v-t)*inv%mod)
    M*=mod
s+=M*((917*R//25-s)//M+1)
t+=M*((R//200-t)//M+1)
n1=S0+(V*s)**2+(V*t)**2
assert 2*S3-P<n1<=U and n1%121==36
for i,p in enumerate(picked):
    y=y0-stride*i
    assert (n1-pow(3,x,p*p)-pow(5,y,p*p))%(p*p)==p
    assert all((n1-pow(3,x,p)-pow(5,y0-stride*j,p))%p
               for j in range(7) if j!=i)
    S=3**x+5**y
    assert 0<S<n1 and 5*S+4*(n1-S)>5*S3 and (n1-S)%125==0
print("middle-order controls and seven distinct exact vetoes passed")
```
