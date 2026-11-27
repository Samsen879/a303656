# Improved explicit coverage: lower density above 99.3454%

The exact exceptional density from [the all-exponent theorem](EXACT_DENSITY_ALL_EXPONENTS.md) is less than \(0.006546\). In fact this bounds the larger miss density within the studied two-growth-axis box. The upward rational bound in the replay displays as \(0.006545125372\). This improves the [original 1.6% bound](SINGLE_WITNESS_EXPLICIT_DENSITY_BOUND.md), using the same published Dorais–Klyve finite search, prime cutoffs, and outward rounding. It does not decide density one or pointwise coverage.

## Two sharper reset estimates

Keep the previous notation \(D=r^a\), the dependent earlier inert rows \(\mathcal D\), their reciprocal sum \(S=\sum_{p\in\mathcal D}(p+1)^{-1}\), terminal bound \(\beta_q\), and
\[
 G_k(S)=\min(1,\ kS/(k-1),\ (kS)^{k-1}/(k-1)!).
\]
If a reset has \(k\) phases passing the prime \(r\), the earlier dependent rows must remove at least \(k-1\) before the terminal can block. The phase selection and this choice of phases do not read the dependent observations; the same probability argument gives \(\beta_q G_k(S)\).

For inert \(r\) where the moved base \(b\) is a unit, put \(d=a-1+v_r(b^{r-1}-1)\). The exceptional \(r\)-readings (no chosen phase with even valuation below \(d\), but some surviving reading matching modulo \(r^d\)) still have probability at most \(r^{-\lceil d/2\rceil}\). When \(d\) is even, select one matching phase. Its \(r\) reset shifts fill the lifts of the residue at the next digit because variation along the base has exact depth \(d\), giving different lifts for all distinct increments modulo \(r\). Discard the one that may match at depth \(d+1\); all other \(r-1\) phases have exact valuation \(d\) and pass. Thus the former exception cost can be replaced by \(r^{-\lceil d/2\rceil}G_{r-1}(S)\) when \(d\) is even; for odd \(d\) retain \(r^{-\lceil d/2\rceil}\). Add the robust cost \(G_r(S)\) and multiply by \(\beta_q\).

Also there is no depth cost at the smallest source primes. Given readings at \(2,3,7,11,19,23\), choose one class \((c,d)\bmod3960\). Pick \(d\)'s parity for a unit at 3 and satisfy 2 by choosing the two exponents modulo 8; the replay checks all 32 residues of \(n_2\bmod32\) for either parity. The achieved valuation and odd part are stable in the selected class. Keeping \(d\) fixed, impose unit residuals at \(7,19,11,23\) in that order by adjusting \(c\) in steps \(8,24,72,360\), respectively, with \(3,3,5,11\) distinct choices. The shifts modulo each previous prime remain unchanged. This class passes all earlier inert primes through 23. An original blocker must also block this particular class, whose own first blocker is common Wieferich: at any later ordinary prime \(q\) its free own primary digits can repair, since \(q\nmid3960\). Work conditionally on these small head readings. Every high reset with \(D\ge28\) preserves the chosen class because \(a-1\ge v_r(3960)\) and moves only \(r\)-primary digits. Therefore the charged \(r\)-depth term is zero for \(r\le23\) (and as before at split \(r\)).

## Bounds carried into the computation

The low-order dyadic bound and explicit Brun–Titchmarsh bounds \(S_D,R_D\) are precisely the ones in the [first explicit bound](SINGLE_WITNESS_EXPLICIT_DENSITY_BOUND.md). At \(r\ge29\) the same endpoint comparison for factorials gives \(G_r(S_D)\le2^{1-r}\) and \(G_{r-1}(S_D)\le2^{2-r}\). The finite depth factor uses the worse of the two base valuations: no independence across axes is assumed. At higher powers \(D=r^a>10^6\), \(a\ge2\), the depth cost is at most \(D^{-1/2}/5\). For odd \(a\), the ceiling gives a factor \(r^{-1/2}<1/5\) (or the depth cost is already zero); for even \(a\), an odd depth is at least \(a+1\), while an even depth has the extra \(2^{2-r}\) factor. The Markov term is also at most \(D^{-1/2}/5\), using \((3/2)S_D\le (9/4)(\log D+1/2)/D\) and the monotone endpoint check at \(10^6\). The high-power tail is therefore one fifth of the former tail. Prime and low-order tails are unchanged.

The ending local countercontrol uses the same older readings for both axes at \(r=31\): their two exceptional events are the same class \(n_{31}=2\bmod31\), not independent classes. The terminal \(17299\) in that replay is an ordinary example, not a common Wieferich witness.

~~~python
from fractions import Fraction as Q
from math import ceil, factorial, floor, isqrt, prod

B, P, H, W, C = 9*10**14, 10**5, 10**6, 10**11, 3960

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

L2,U2 = series(Q(2))

def logs(x):
    y,k = Q(x),0
    assert y >= 1
    while y >= 2:
        y /= 2
        k += 1
    l,u = series(y)
    return Q(floor(W*(l+k*L2)),W), Q(ceil(W*(u+k*U2)),W)

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
    for dp in (0,1):
        assert any(good2((n-pow(3,c,32)-pow(5,d,32))%32)
                   for c in range(8) for d in range(dp,8,2))
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
        prime+=up(bounds(r,r)[1]/r)
    D,a=r*r,2
    while D<=H:
        if D>=28:
            S,R=bounds(D,r)
            G=min(Q(1),Q(r,r-1)*S,(r*S)**(r-1)/factorial(r-1)) if r<29 else Q(0)
            power+=up(R*(deep(r,a)+G))
        D,a=D*r,a+1

z=Q(21,125)
low=hi(3)/(34*exp_lo(34*z,32)*(1-1/exp_lo(z*L2,12)))
assert 3**13>H
kill=Q(13,2**27)
assert Q(P+1,P-1)<Q(10001,10000)
prime_tail=Q(10001,10000)*(hi(P)+Q(3,2))/P
assert Q(45,4)*(hi(H)+Q(1,2))<isqrt(H)
assert lo(2*H)>6 and 11**6<2*H<2**21
power_tail=Q(27,10)/H*(2*(hi(2*H)+Q(1,2))+2*U2)
parts=(low,prime,power,kill,prime_tail,power_tail)
assert sum(parts)<Q(6546,10**6)
print(*(f"{float(x):.12f}" for x in parts))
print(f"{float(sum(parts)):.12f}")

n,r,q=4062208227,31,17299
s=lambda c,d,m:(pow(3,c,m)+pow(5,d,m))%m
assert n%4==3 and all(n%p==0 and s(C,C,p)!=0 for p in (3,7,11,19,23))
assert all(q%i for i in range(2,isqrt(q)+1))
assert (q-1)%(r*r)==0 and all(pow(b,(q-1)//r,q)!=1 for b in (3,5))
for p in range(7,q,4):
    if all(p%i for i in range(2,isqrt(p)+1)):
        assert (p-1)%(r*r)
        assert any(pow(b,p-1,p*p)!=1 for b in (3,5))
for axis in (0,1):
    f=lambda j,m,h: s(C+j*h*(axis==0),C+j*h*(axis==1),m)
    assert {f(j,r*r,C) for j in range(r)}==set(range(2,r*r,r))
    assert len({f(j,q,C*r) for j in range(r)})==r
    assert (n-f(0,r**3,C*r))%r**3==0
    assert all((n-f(j,r**3,C*r))%r**3 in range(r*r,r**3,r*r)
               for j in range(1,r))

~~~
