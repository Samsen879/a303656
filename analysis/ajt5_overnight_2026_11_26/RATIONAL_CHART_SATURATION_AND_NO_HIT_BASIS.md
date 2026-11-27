# Saturation reduces the denominator but may destroy hit-basis availability

Write v=(ah,bk), w=(ch,dk), Δ=ad−bc with each axis reduced. For r|Δ and r not dividing hk, the original lattice has rank one modulo r. Choose w≡τv mod r after exchanging if necessary, and write T=(w−τv)/r. Its one-step r-saturation is Z v+Z T, of index r over the old lattice. A proposed e f=m v+l w with e=r d0 and integer f satisfies m+τl=r j, hence d0 f=jv+lT. This reparameterization is one-to-one. It does not convert T or any other lattice basis vector into an actual hit. An exact necessary relation for fourth y-read Omega is Omega^d0=5^(720(j v_y+l T_y)); at d0=1 this directly eliminates the earlier powered false positive. The original third point w must still use its original read.

In the exact e=17 control, the saturated grid in the prescribed short window has 193 points and just four modular hits (each exact-once). The four possible triangles of genuine hits have normalized lattice indices 5,5,7,17. Hence no three actual hits generate the saturated lattice, with any choice of origin. The short candidate basis points from T,v−7T individually fail. The same target has a separate true denominator-34 coarse-axis control.

## A restricted aggregate bound

In the sublinear interior sector r|e≤Cr, r|Δ≠0, r not dividing hk, |h|,|k|≤T0, let R0=min(R,M T0), with the usual short charts (2R<D=rs, chart widths <D, p not dividing n). Assume M(log_3 M+log_5 M)<720r. Across all these denominators, the number of realized (prime, shape with start) pairs is O_C(R0³ M³/(r log D)).

Indeed integrality forces r|P,Q for P=ma+lc,Q=mb+ld. At fixed h,k the fourth offsets are h(P/r)/d0,k(Q/r)/d0; as d0 ranges over at most C choices, the two axis candidate counts are O_C(A),O_C(B) where A=max(a,c), B=max(b,d). The first two hits determine the start. Exact order and a short chart make the hit graph injective in either axis, giving O_C(min(A,B)) fourth points.

The three-hit cross determinant cannot vanish over Q. Its ratio form has one axis close to 1 and the other bounded away from 1 if h,k have opposite signs. If both are positive, LTE in the 3-axis equation gives 720h min(a,c)=v_3(d−b)−v_3(b), and its dual gives a corresponding bound on min(b,d) with base 5. Equality of ratios forces the smaller coefficients to lie in the same column, giving |Δ|≤M(log_3 M+log_5 M)/720<r. For both negative, LTE instead bounds |a−c| and |b−d| by the same respective logarithmic terms/720, yielding the same determinant bound. This contradicts r|Δ≠0. Axis repeats already preclude a genuine hit.

Each nonzero determinant has log height O(R0), hence O(R0/log D) possible primes. There are O(R0²/(AB)) possible h,k, so each coefficient tuple costs O_C(R0³/(max(A,B) log D)). In a box of coefficients up to L there are O(L^4/r) tuples with nonzero Δ divisible by r: fix the coprime first-axis coefficients a,c, bound possible multiples rj by O(max(a,c)L/r), then each affine line of (b,d) has O(1+L/max(a,c)) points. Dyadic summation gives the bound. For R≈r≈H^(3/4), M≈sqrt(r), it reaches O(H²/log H) when T0≤r^(2/9). At full width it only gives O(H^(21/8)/log H), so the full middle is unclosed.

```python
from itertools import combinations
from math import gcd, isqrt

H,J,t,r,s,p = 3720000,310,155521,17,37,1259
D = r*s
def prime(q):
    return q>2 and q%2 and all(q%d for d in range(3,isqrt(q)+1,2))
assert all(map(prime,(t,r,s,p))) and p==2*D+1 and p%4==3
assert t%720==1 and 16*t<=H<=24*t and J==H//12000 and 2*J<D
for q in (3,5):
    assert pow(q,720*D,p)==1
    assert all(pow(q,720*(D//a),p)!=1 for a in (r,s))

M,z = 146651884329720,1<<(H//2-4)
x,y = (z+(a-z)%M for a in (61827877807697,135417323161960))
S0 = 3**(3*t+80)+5**(t+144)
n = S0+85*(x*x+y*y)
assert n.bit_length()==H and n>3**(3*t+80+720*(J-1))+5**(t+144+720*(J-1))
assert n-S0==(7*x-6*y)**2+(6*x+7*y)**2 and n%(p*p)==1223507

def sub(a,b):
    return tuple(x-y for x,y in zip(a,b))
def det(a,b):
    return a[0]*b[1]-a[1]*b[0]

mod = p*p
X = [pow(3,3*t+80+720*u,mod) for u in range(J)]
Y = [pow(5,t+144+720*v,mod) for v in range(J)]
def read(z):
    u,v = z
    assert 0<=u<J and 0<=v<J
    return (n-X[u]-Y[v])%mod
def once(z):
    return read(z) in range(p,mod,p)

o,v,w,T = (26,83),(193,161),(266,179),(27,20)
assert tuple(a+b for a,b in zip(v,w))==tuple(r*a for a in T)
assert det(v,w)==-17*487 and det(v,T)==-487
assert read((53,103))%p==559 and read((30,104))%p==60
assert read((161,183))==755*p and read((80,123))%p==1210
rho = (n-X[80])*pow(Y[123],-1,p)%p
assert rho==1008 and pow(rho,17,p)==1

I = abs(det(v,T))
grid = [(i,j) for i in range(J) for j in range(J)
        if det(sub((i,j),o),T)%I == det(v,sub((i,j),o))%I == 0]
hits = [z for z in grid if read(z)%p==0]
assert len(grid)==193 and hits==[(26,83),(161,183),(219,244),(292,262)]
assert all(map(once,hits))
assert sorted(abs(det(sub(b,a),sub(c,a)))//I
              for a,b,c in combinations(hits,3))==[5,5,7,17]

o,v,w = (219,244),(-187,-51),(-68,-162)
h,k = -gcd(v[0],w[0]),-gcd(v[1],w[1])
a,b,c,d = v[0]//h,v[1]//k,w[0]//h,w[1]//k
e,m,l = 34,12,17
P,Q = m*a+l*c,m*b+l*d
assert (h,k,a*d-b*c)==(-17,-3,526) and (a*d-b*c)%r
assert P%r and Q%r==0 and h%r==0 and k%r
assert (h*P//e,k*Q//e)==(-100,-99) and h*P%e==k*Q%e==0
assert all(map(once,[o,(32,193),(151,82),(119,145)]))
assert read((119,145))==122*p
```
