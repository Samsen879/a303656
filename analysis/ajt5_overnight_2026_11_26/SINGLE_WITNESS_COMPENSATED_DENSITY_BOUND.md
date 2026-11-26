# Explicit miss density below 0.175%

The natural density of integers lacking any A303656 representation, which exists by [the exact density theorem](EXACT_DENSITY_ALL_EXPONENTS.md), is less than \(0.00175\). The same upper bound holds for the larger set of misses in the growing exponent box, via [finite head blockers](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md). The upward rational sum in the replay displays as \(0.001749368139\). This shows genuine representation density exceeding \(99.825\%\); it does not settle density one or the pointwise conjecture.

The proof builds on [the preceding quantitative bound](SINGLE_WITNESS_IMPROVED_DENSITY_BOUND.md), with the same small-head preload modulo 3960, Dorais–Klyve published base-3 search cutoff and exact residue checks, Brun–Titchmarsh reciprocal envelopes \(S_D,R_D\), and high-power bounds. The improvements here are a second-axis repair for first-depth order primes and a sharper low-order count.

## Complementing a first-depth digit

Let \(r\) be inert, \(r\ge29\), with a factor \(r\) in one terminal axis order at \(q\), and with both terminal \(r\)-order depths at most one. Assume both bases are ordinary at \(r\). Let \(\mathcal D_b,\mathcal D_c\) be the old inert rows reading the respective axis \(r\)-primary digits, excluding \(r\) itself; let \(S\) be the sum of \(1/(p+1)\) over their union, bounded by \(S_D\) for \(D=r\). Pick a phase \(\omega\) passing the rows outside that union and \(r\), without reading their observations.

If there is a phase after dropping only \(\mathcal D_b,r\) whose residual at \(r\) is a unit, its \(r\) variants on axis \(b\) remain units there. As in the prior bound, the old rows must then kill at least \(r-1\) variants, costing \(G_r(S)\). The choice of phase in this case does not read \(\mathcal D_b\).

Otherwise, if the residual of \(\omega\) is a unit at \(r\), all its \(r\) variants on axis \(c\) have that same unit property. The only way none can be a candidate for the previous branch is that \(\mathcal D_c\setminus\mathcal D_b\) kills all \(r\) variants; a row kills at most one by first-residue distinctness, so this costs at most \((rS)^r/r!\).

In the remaining case \(n_r\) matches \(\omega\)'s root modulo \(r\), an event of probability \(1/r\). With first digit \(t\) on axis \(b\), one can pick the first digit \(s=s_0+\lambda t\bmod r\) on axis \(c\) to reach valuation at least two, because its derivative on that digit is a unit. One further digit on \(c\) makes the valuation exactly two and is invisible at \(q\). These \(r\) phases have terminal shifts \(A\xi^t+B\upsilon^{s_0+\lambda t}\), where \(\xi\) has order \(r\), \(\upsilon\) has order dividing \(r\), and \(A,B\ne0\). Linear independence of distinct characters on the cyclic group of order \(r\) shows this function is constant only when the two nontrivial characters agree and their coefficients cancel. There is at most one such intercept \(s_0\), uniform as \(n_r\) moves through the \(r\) lifts of the matched root. For any nondegenerate intercept choose two phases with different terminal shifts before reading the union of old dependent rows. With probability at most \(\min(1,2S)\) one of them is killed by those rows, the only way first blocking can happen. This remains true even if the second repair digit is read by some of the dropped rows, which are already in the union.

The depth charge is therefore at most \(\min(1/r,\ 1/r^2+\min(1,2S)/r)\), in addition to the two separate tail terms \(G_r(S)\) and \((rS)^r/r!\); multiplying by the terminal \(\beta_q\) is legitimate upon conditioning on the old observations. The minimum uses the previous estimate. Select the largest order power for the chosen \(r\) across the two axes, so the depth-one bound is only used when both terminal depths are at most one. At an exceptional \(r\) where either axis is nonordinary retain \(1/r\). The finite \(r\)-sum implements these choices. The extra factorial term is at most \(2^{-r}\) for \(r\ge29\) by the same monotone endpoint test (or the \(G_r\)-factorial term's bound times \(S\)). The displayed \(14/2^{27}\) dominates the finite large-\(r\) contributions of both factorial terms over prime powers: \(G_r\) costs at most \(13/2^{27}\), and the added term only applies to the prime power of exponent one. Beyond the finite cutoffs use the older unconditional prime and power tails, which need not use compensation.

## Low-order certification

On the low-order branch in \([Y,2Y)\), write \(d=\operatorname{ord}_q(3)\mid L=\operatorname{lcm}(1,\ldots,\lfloor(4/5)\log Y\rfloor)\). For a potentially blocking prime \(q\), \(q^2\mid3^d-1\) by the lifting formula, and \(q\equiv1\bmod d\). Thus the number for a given \(d\) is at most \(\min(d\log3/(2\log Y),Y/d+1)\). The first 24 dyadic intervals sum these explicit bounds over all \(d\mid L\) before dividing by \(Y\); the logarithm is bounded on the safe side at each rounding. For later intervals use \(\min(ad,b/d+c)\le\sqrt{ab}+c\) and \(\tau(L)\le9L^{1/4}\). To check the latter, the factor \((k+1)^4/p^k\) is at most 1 for \(p\ge17\); at smaller primes its maximum is in \(0\le k\le6\), as one sees by the ratio at \(k=6\). The finite product of those maxima is \(<9^4\). Now \(L\le Y^{104/125}\) by the same Rosser–Schoenfeld inequality. The two per-interval terms decay with exponents \(73/250,99/125\), giving the geometric tails in the replay.

The last replay examines actual ordinary target 683. For two old heads with the same observations other than the source reading at 31, compensation produces respectively 31 distinct terminal shifts and complete zero-sum cancellation. Thus ignoring the exceptional intercept would not be justified by first-digit structure alone.

~~~python
from fractions import Fraction as Q
from math import ceil, factorial, floor, isqrt, prod

B,P,H,C = 9*10**14,10**5,10**6,3960
W,Z = 10**11,10**25

def series(y):
    z=(y-1)/(y+1)
    s=2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s,s+2*z**25/(25*(1-z*z))
L2,U2=series(Q(2))

def logs(x):
    y,k=Q(x),0
    assert y>=1
    while y>=2:
        y/=2
        k+=1
    l,u=series(y)
    return Q(floor(W*(l+k*L2)),W),Q(ceil(W*(u+k*U2)),W)
def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)
def exp_lo(x,n): return sum(x**j/factorial(j) for j in range(n))

assert 150000*prod((2,3,5,7,11,13,17,19,23,29))==970453984500000>B
assert lo(B)>34
for p,y in [(11,78),(1006003,31695130519)]:
    assert pow(3,p-1,p*p)==1 and pow(5,p-1,p*p)==y!=1

def good2(x):
    t=x&-x
    return bool(t and t<=8 and (x//t)%4==1)
for n in range(32):
    for parity in (0,1):
        assert any(good2((n-pow(3,c,32)-pow(5,d,32))%32)
                   for c in range(8) for d in range(parity,8,2))
assert pow(3,8,32)==pow(5,8,32)==1 and pow(5,C,3)==1
rows=((7,8,3),(19,24,3),(11,72,5),(23,360,11))
for k,(p,step,digits) in enumerate(rows):
    assert pow(3,C,p)==pow(5,C,p)==pow(3,step*digits,p)==1
    assert all(pow(3,step,old[0])==1 for old in rows[:k])
    assert len({pow(3,j*step,p) for j in range(digits)})==digits

A=sum(Q(1,4*j+2) for j in range(32))
assert A<lo(34) and A-lo(lo(32))+Q(1,34)<Q(1,5)
assert hi(Q(4,3))<Q(3,10)
assert Q(3,2)*(hi(28)+Q(1,2))/28<1
assert 3*Q(29,28)**2*(hi(29)+Q(1,2))/29<Q(1,2)
assert 3*Q(29,27)*(hi(29)+Q(1,2))/29<Q(1,2)
assert 2**27>29 and 2**28>29**2

def bounds(D,r):
    phi=D-D//r
    l,u=logs(4*D)
    Um,Up,Vm=Q(4*D,3)-u,Q(4*D,3)-l,34-u
    assert 0<Vm<Um
    S=(hi(D)+Q(1,2))/phi
    return S,min(S,(1/Um+hi(Up/Vm))/phi)

def deep(r,a):
    if r<=23 or r%4==1:
        return Q(0)
    vals=[]
    for b in (3,5):
        e=1
        while pow(b,r-1,r**(e+1))==1:
            e+=1
        d=a-1+e
        vals.append(Q(1,r**((d+1)//2)*(2**(r-2) if d%2==0 else 1)))
    return max(vals)

flags=bytearray(b'\x01')*(P+1)
flags[:2]=b'\x00\x00'
for r in range(2,isqrt(P)+1):
    if flags[r]:
        flags[r*r::r]=b'\x00'*((P-r*r)//r+1)

prime=power=Q(0)
for r in range(3,P+1,2):
    if not flags[r]:
        continue
    if r>=29 and r%4==3:
        S,R=bounds(r,r)
        E=Q(1,r)
        if all(pow(b,r-1,r*r)!=1 for b in (3,5)):
            E=min(E,Q(1,r*r)+min(1,2*S)/r)
        prime+=up(R*E)
    D,a=r*r,2
    while D<=H:
        if D>=28:
            S,R=bounds(D,r)
            G=min(Q(1),Q(r,r-1)*S,(r*S)**(r-1)/factorial(r-1)) if r<29 else Q(0)
            power+=up(R*(deep(r,a)+G))
        D,a=D*r,a+1

J=24
L,U=logs(B)
low_count=0
for j in range(J):
    Y=B*2**j
    T=floor(Q(4,5)*(U+j*U2))
    ds=[1]
    for p in range(2,T+1):
        if not flags[p]:
            continue
        pp=[1]
        while pp[-1]*p<=T:
            pp.append(pp[-1]*p)
        ds=[d*t for d in ds for t in pp]
    A=hi(3)/(2*(L+j*L2)*Y)
    low_count+=sum(ceil(Z*min(A*d,Q(1,d)+Q(1,Y))) for d in ds)

assert 8**4<2*7**4
assert prod(max(Q((a+1)**4,p**a) for a in range(7))
            for p in (2,3,5,7,11,13))<9**4
t=L+J*L2
def geom(z):
    return 1/(exp_lo(z*t,100)*(1-1/exp_lo(z*L2,12)))
root=Q(isqrt(floor(hi(3)*Z*Z/(2*t)))+1,Z)
low=Q(low_count,Z)+9*(root*geom(Q(73,250))+geom(Q(99,125)))

assert 3**13>H
kill=Q(14,2**27)
assert Q(P+1,P-1)<Q(10001,10000)
prime_tail=Q(10001,10000)*(hi(P)+Q(3,2))/P
assert Q(45,4)*(hi(H)+Q(1,2))<isqrt(H)
assert lo(2*H)>6 and 11**6<2*H<2**21
power_tail=Q(27,10)/H*(2*(hi(2*H)+Q(1,2))+2*U2)

parts=(low,prime,power,kill,prime_tail,power_tail)
assert sum(parts)<Q(175,10**5)
print(*(f"{float(x):.12f}" for x in parts))
print(f"{float(sum(parts)):.12f}")

r,q,c,d=31,683,8,55
site=lambda j,k,m:(pow(3,c+C*j,m)+pow(5,d+C*k,m))%m
pr=lambda p:p>=2 and all(p%i for i in range(2,isqrt(p)+1))
assert pr(q) and pr(r) and (q-1)%r==0 and (q-1)%(r*r)!=0
assert all(pow(b,C,q)!=1 and pow(b,r-1,r*r)!=1 for b in (3,5))
assert [p for p in range(7,q,4) if pr(p) and (p-1)%r==0]==[311]
assert all(any(pow(b,p-1,p*p)!=1 for b in (3,5))
           for p in range(7,q,4) if pr(p))

for base,n in ((0,2637872320959),(14,2996020970895)):
    assert [n%m for m in (4,3,7,11,19,23,311)]==[3,0,1,7,12,6,0]
    assert all((n-site(0,0,p))%p==1 for p in (7,11,19,23))
    shifts=set()
    for j in range(r):
        k=(base+20*j)%r
        assert (n-site(j,k,r*r))%(r*r)==0
        if (n-site(j,k,r**3))%r**3==0:
            k+=r
        assert (n-site(j,k,r**3))%r**3 in range(r*r,r**3,r*r)
        assert site(j,k,311)!=0
        shifts.add(site(j,k,q))
    assert len(shifts)==r if base==0 else shifts=={0}

~~~
