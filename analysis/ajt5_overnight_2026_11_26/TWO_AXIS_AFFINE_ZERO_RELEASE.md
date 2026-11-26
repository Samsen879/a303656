# Two-axis affine zero-fibre release and a genuine boundary lock

**The pinned countercontrol does admit a two-axis release.** Two joint choices pass while preserving both raw powers \(3^c\) and \(5^d\) modulo the squares of \(271,4159,19\). The known reader \(163\) gives a sharp boundary: it reads the released \(c\)-digit and leaves the released \(d\)-digit free. An exact valuation-one test at \(163\) can close both joint choices. [Pinned nine-cell control](https://github.com/Samsen879/a303656/commit/cfd194ad04e6df6b3d264089a58dd0c97b3b524f) · [Known reader orders](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md#3-exact-selected-cyclotomic-arithmetic)

### Two-axis certificate

Let two released base-\(\ell\) digits give \(c_x=c+Sx,\ d_y=d+Dy\) for \(x,y\in\mathbb F_\ell\). First check that their steps preserve both observed powers at the external moduli. At an internal zero reader \(q\ne\ell\), suppose the step multipliers \(3^S,5^D\) have order dividing \(\ell\). A nonconstant collision equation is then an affine line in \((x,y)\): taking exponents in the order-\(\ell\) subgroup turns \(3^{c_x}=-5^{d_y}\) into one linear congruence. Exact odd rejections occupy a subset of that line.

With at most \(\ell\) such rows and no constant failing row, a full lock requires \(\ell\) distinct parallel lines, each entirely rejecting. Indeed, each line has \(\ell\) cells, and any intersection makes their total coverage strictly less than \(\ell^2\). This gives a direct certificate of release when the actual order characters produce different directions.

### Exact release and lock

For the original countercontrol, the three internal rejection lines over \(\mathbb F_3\), in reader order \(1783,5023,Q\), are
\[
y=0,\qquad y=2+x,\qquad y=1+2x.
\]
Here \(Q=11419697846380955982026777206637491\). All their collisions have exact valuation one. The safe choices are \((1,1)\) and \((1,2)\). From the baseline \((c,0)\), varying \(c\) alone in this ternary plane leaves the \(1783\) rejection. Varying \(d\) alone anywhere in the pinned nine-cell anchor also fails.

At \(163\), the orders of \(3\) and \(5\) have 3-parts \(81\) and \(27\), respectively. Preserving its raw readings therefore forces \(x=0\) and allows all \(y\). At the original target this extra row is a unit throughout the plane, so phase preservation is the constraint in that comparison. For the stronger countercontrol, change the target only modulo \(163^2\) to make the line \(x=1\) reject at exact valuation one. The four lines are then the four directions through \((1,0)\), covering the plane. The lock is for the ternary block with the other digits frozen. Releasing reader-primary digits is outside that restriction.

### Runnable replay

```python
from itertools import product
from math import gcd, isqrt, lcm, prod

q0,q1,q2 = 1783,5023,11419697846380955982026777206637491
Q = (q0,q1,q2)
r,s,h,k = 271,4159,19,163
R = (r,s,h)
chain = (1838773,871578403,1770336106919153,584210915283320491,
         143715885159696840787,q2)
for q in (q0,q1,*R,k,chain[0]):
    assert all(q%d for d in range(2,isqrt(q)+1))
for p,q in zip(chain,chain[1:]):
    assert p*p>q and (q-1)%p==0 and pow(2,q-1,q)==1
    assert gcd(pow(2,(q-1)//p,q)-1,q)==1

P = prod(Q+R)
c = 27*lcm(11,31,70491962014697259148313439547145)*P
A = 18*P
S,D = 56*k*c,12*k*A
assert S%81==D%81==54
assert (s-1)%27==0 and (s-1)%81 and pow(3,(s-1)//3,s)!=1
assert pow(5,27,r)==1 and pow(5,9,r)!=1

pairs = [(9,24),(pow(3,c,h*h),h*h)] + [(q,q*q) for q in Q]
for u,q in enumerate((r,s),1):
    m = q*q
    pairs.append(((pow(3,c,m)+pow(5,A*u,m)+q)%m,m))
M = prod(m for _,m in pairs)
n = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs)%M

def rem(n,c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

assert all(pow(5,9*A,q*q)==1 for q in Q+R)
for u,v in product(range(3),repeat=2):
    q = (q0,q2,q1)[v] if u==0 else (r,s)[u-1]
    assert rem(n,c,A*(u+3*v),q*q)==q

for m in (32,27,*(q*q for q in R)):
    assert pow(3,c+S,m)==pow(3,c,m) and pow(5,D,m)==1
assert all(pow(3,3*S,q*q)==pow(5,3*D,q*q)==1 for q in Q)
for x,y in product(range(3),repeat=2):
    c1,d = c+S*x,D*y
    hits = {q for q,j in zip(Q,(0,(2+x)%3,(1+2*x)%3)) if y==j}
    assert {q for q in Q if rem(n,c1,d,q)==0}==hits
    assert all(rem(n,c1,d,q*q)==q for q in hits)
    assert all(rem(n,c1,d,q) for q in R)
    assert (not hits)==(x==1 and y!=0)

# Actual boundary reader. Its d term is frozen and its c term moves.
assert pow(3,162,k)==1 and pow(3,54,k)!=1
assert pow(5,54,k)==1 and pow(5,18,k)!=1 and pow(5,27,k)!=1
assert pow(5,D,k*k)==pow(3,3*S,k*k)==1 and pow(3,S,k)!=1
assert all(rem(n,c+S*x,0,k) for x in range(3))
z = (pow(3,c+S,k*k)+1+k)%(k*k)
n1 = n+M*((z-n)*pow(M,-1,k*k)%(k*k))
assert n1%M==n and n1%k==0
for x,y in product(range(3),repeat=2):
    c1,d = c+S*x,D*y
    assert (pow(3,c1,k)==pow(3,c,k))==(x==0)
    assert rem(n1,c1,d,k*k)==k if x==1 else rem(n1,c1,d,k)!=0
    assert any(rem(n1,c1,d,q*q) in range(q,q*q,q) for q in Q+(k,))
lines=[{(x,y) for x,y in product(range(3),repeat=2) if g(x,y)}
       for g in (lambda x,y:y==0,lambda x,y:y==(2+x)%3,
                 lambda x,y:y==(1+2*x)%3,lambda x,y:x==1)]
assert set.intersection(*lines)=={(1,0)} and len(set.union(*lines))==9
print("OK")

```

The cube-period checks cover all lifts of these released ternary digits at the stated precision. Both outcomes concern the specified finite tests.

The affine-line description is for a nonempty collision in the order subgroup. If the required ratio lies outside that subgroup the collision set is empty; if both characters are trivial the row is constant and must be checked separately. The line proof uses only modulo-prime collisions, and the arithmetic replay verifies which of those collisions are actual odd-valuation vetoes. Neither locked control is a whole finite-modulus obstruction.
