# K701 repeated-split-prime Gaussian allocations

**A new K701 target has a true first chord and three true second seeds at the same \(n\).** Its first terminal norm contains exactly \(13^{14}17^{14}\). With the other Gaussian factors fixed, all 225 allocations of those two powers are primitive. Exactly one, \((7,11)\), hits the strict window.

There is also a quantitative limit on this mechanism: **two repeated split primes cover less than \(1/2000\) of arbitrary residual phases** if one CRT period must fit the fixed-\(K\) target window.

### Budget, angle, and primitivity

For distinct split primes \(p_i\) with prescribed exponents \(e_i\), write \(M=\prod_i p_i^{e_i}\). With the residual representations fixed, conjugate allocation supplies at most \(N=\prod_i(e_i+1)\) relative phases. If there are \(k\) primes, the weighted arithmetic–geometric mean inequality gives
\[
N\le
\frac{\bigl((\log M+\sum_i\log p_i)/k\bigr)^k}
     {\prod_i\log p_i}.
\]
The two signed critical arcs together occupy a fraction \((1+o(1))/(2\sqrt2\pi K^2)\) of the circle modulo quarter turns. This follows by differentiating \(q=S+D-\sqrt{SR}\cos\theta\) across the strict window, where \(\theta\sim1/(4\sqrt2K)\).

For the scope in which the two half-norms are both coprime to 5 (as at the exact target below), any two distinct split primes in the switch have sizes at least 13 and 17 after ordering. If a full period fits the fixed-\(K\) window, \(M=O(2^{K/2})\). The covered fraction for two primes and one fixed residual pair is therefore at most
\[
\frac{(\log 2)^2}{32\sqrt2\pi\,\log13\,\log17}+o(1)
<\frac1{2000}
\]
for sufficiently large \(K\). This bounds uniform coverage. The actual residual phase at K701 lands in the small covered set. The bound leaves open a suite of many distinct cheap primes.

There is a separate exact primitivity test. With \(\gcd(S,D)=1\), an allocation is nonprimitive at an odd prime \(\ell\mid D\) exactly when \(Z/S=1\) in the norm-one group modulo \(\ell\), where \(Z=\bar P Q\). If switch \(i\) has order \(o_{\ell,i}\) in this group, freezing the other indices gives at most \(1+\lfloor e_i/o_{\ell,i}\rfloor\) forbidden indices. Also, if \(\ell>\sqrt M\), **the whole allocation box is injective modulo \(\ell\)**. A collision would give a Gaussian product of norm at most \(M\) whose imaginary part is nonzero by unique factorization, yet divisible by \(\ell\). Thus each such prime forbids at most one allocation. The K701 replay checks the stronger finite result directly: 225 distinct residues modulo \(D\), with zero forbidden allocations.

### Independent exact check

The target, endpoint coordinates, all allocations, and the neighbouring miss are below. The outcome concerns the two fixed switch axes and fixed residual coordinates, not optimization over all possible Gaussian factorizations or a solution of A303656.

~~~python
from math import gcd
from itertools import product

L,K = 7,701
A,B = 9**L,25**L
H,D,J,E = 27*A+5*B,9*A+2*B,3*A+125*B,A+50*B
c = (E-1)//2
t = 2594797483547436815560120314511538932489755040423270019710209296669240500998748068695605013445255426187105
P = (1829666755337538302527498130337368845654447658058662833189216962628011451703103617159632221685015397784716,
    -3180922433141183343276113673824123949575385474794983086010908844015987852535352860519838761683692241292970)
tail = (87384217701224654814779341347135703136647289099846391006003528903549011798395167053087383,
        112586160895102250395583157473001044367046833757077524882326180597053471713870585147044187)

def norm(z): return z[0]**2 + z[1]**2
def bar(z): return z[0],-z[1]
def mul(z,w): return z[0]*w[0]-z[1]*w[1],z[0]*w[1]+z[1]*w[0]

def power(z,a):
    w = (1,0)
    for _ in range(a):
        w = mul(w,z)
    return w

def alloc(z,j):
    return mul(power(z,j),power(bar(z),14-j))

def band(q,S):
    return 64*K*K*q<S<64*K*(K+1)*q

def chord(P,Q,S,D):
    assert norm(P)==S and norm(Q)==S+2*D
    x,y = Q[0]-P[0],Q[1]-P[1]
    q,h = (x*x+y*y)//2,x*P[1]-y*P[0]
    assert x%2 and y%2 and h%2==0 and gcd(x,y)==1
    assert 2*q*S==(D-q)**2+h*h
    return q

n = 2*(t*t+c*c)+J
S,R,T = n-H,n-H+2*D,n-J
assert n.bit_length()==702 and 25**128<=n<=9**224
assert all(2**K<=v<2**(K+1) for v in (S,R,T))
assert gcd(S,D)==1 and R==norm(tail)*13**14*17**14
assert gcd(norm(tail),13*17)==1

second = set()
for m in (7932,7934,7936):
    v,r = divmod(t+m*(c+1),m*m+1)
    assert r==0
    a,b = (m*m-1)*v-m*(c+1),2*m*v-c-1
    q = chord((t-c,t+c),(a-b,a+b),T,E)
    assert band(q,T)
    second.add(q)
assert len(second)==3

residues,wins = set(),[]
for i,j in product(range(15),repeat=2):
    Q = mul(tail,mul(alloc((2,3),i),alloc((1,4),j)))
    q = chord(P,Q,S,D)
    Z = mul(bar(P),Q)
    assert norm(Z)==S*R and q==S+D-Z[0] and gcd(q,D)==1
    residues.add(tuple(v%D for v in Z))
    if band(q,S):
        wins.append((i,j))
    if (i,j)==(8,11):
        assert 64*K*K*q>S
assert len(residues)==225 and wins==[(7,11)]
print("verified",K,len(second),len(residues),wins)
~~~
