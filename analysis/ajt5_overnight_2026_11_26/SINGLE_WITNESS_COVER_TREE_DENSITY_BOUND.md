# Coverage trees give representation density above 99.9124%

The natural exception density from [the all-exponent theorem](EXACT_DENSITY_ALL_EXPONENTS.md) is less than \(0.000876\), i.e. \(0.0876\%\); the same bound holds for the larger miss set in the growth box. The fully rational upper bound below displays as \(0.0008758955274613264\). It replaces one finite term and one infinite tail in the [nine-phase bound](SINGLE_WITNESS_NINE_PHASE_DENSITY_BOUND.md), retaining all other contributions, including the published finite search. It does not settle density one.

## Tree recursion for a read-depth hierarchy

For a selected axis and terminal prime, suppose the terminal reads \(a\) digits at source \(r\) and the basic phase fixes \(h\). Choose \(1\le k\le a-h\) and move along the \(r^k\) variants of step \(r^{a-k}\). Earlier primes outside \(r\) with order depth at most \(a-k\) never see the move. Any other older inert prime sees a prefix of length \(j=\min(k,v_r(\operatorname{ord}_p(b))-a+k)\). On one prefix its powers at every \(p\)-adic depth agree (order lifting only adds \(p\)-powers), and on different prefixes they differ modulo \(p\). It can therefore kill at most one whole prefix cell, with probability \(1/(p+1)\) for a specified cell. Work on a robust source branch, or when the source is in the preloaded small head; other source exceptions remain charged by the previous estimate. Choose the initial phase without reading the observations of any readers to be charged.

Let \(s_j\) be the sum of the reciprocal weights \(1/(p+1)\) for rows reading prefix length \(j\). Write \(F_j\) for complete subtree coverage, \(L_j\) for complete coverage using only internal nodes, and \(P_j\) for covering all but one unspecified leaf. Initialize at leaves as \((F_k,L_k,P_k)=(s_k,0,1)\), then use
\[
 F_j=s_j+F_{j+1}^r,\qquad L_j=s_j+L_{j+1}^r,\qquad
 P_j=r P_{j+1}F_{j+1}^{r-1}.
\]
These are upper bounds on the sum of assignment weights, not probabilities of independent subtrees. Choose a prefix-free covering subcollection of the actual killed cells. If it covers everything via internal nodes, use \(L_1^r\). If it covers everything and a leaf is present, discard that leaf cell; the remaining cover omits one leaf. That case and an actual cover omitting one leaf are charged by \(rP_1 F_1^{r-1}\). Each actual assignment uses different observer primes, whose observations are independent, and dropping the distinctness restriction when summing products gives a safe upper bound. Two survivors have distinct terminal shifts, so this near-complete cover is necessary for first blocking. This gives a family of bounds over all usable axes and \(k\); taking the minimum needs no independence of the resulting bounds.

## Replacing the two terms

For \(r=3,k=2\), the polynomial with shallow and deep weight sums \(s,t\) is \(s^3+9s^2t^2+18st^5+9t^8\). It is at most \((s+t)^3\) when \(s+t\le0.3\). Indeed with \(L=s+t\), \(L^3-s^3\ge tL^2\); the remaining terms divided by \(tL^2\) are bounded by \(\frac43L+18L^3+9L^5<1\). For \(D=81\), enumerate the actual readers of order depth at least 3 through \(128\cdot27\), giving finite weight sums \(\rho_3,\rho_5\). The [Montgomery–Vaughan](https://doi.org/10.1112/S0025579300004708) long-end reciprocal estimate then yields \(s+t\le(\log u-22/25)/18\) for \(u=\log q\in[34,108]\), since \(\log\log32-1/34-18\max_b\rho_b>22/25\). As in the previous bound, apply partial summation in the terminal class modulo 324, keeping the upper endpoint and using upper numerators on unit log-intervals. The new weight is decreasing after division by \(q\) since \(u(\log u-22/25)>3\) there. This exactly replaces the finite \(D=81\) charge after rounding.

For the entire high-power tail \(D>H=10^6\), use the one-digit bound \(rS_D^{r-1}\le3S_D^2\) since \(S_D<1/2\). The earlier bounds for the source-depth term and terminal reciprocal contribution give \(\eta\le D^{-1/2}/5\) and \(R_D\le S_D\le(3/2)(\log D+1/2)/D\). Thus the summand is at most \((3/10)(\log D+1/2)D^{-3/2}+(81/8)(\log D+1/2)^3D^{-3}\). The first term is half of the previous perfect-power dyadic bound. For the second bound by all integers and integrate the decreasing function from \(H\) to infinity; the closed-form integral is in the replay. The full tail is still counted and only these two old contributions are replaced.

The same old-head replay below gives one survivor when four different node kills are coordinated and two when two different observer rows kill the same leaf. It is an actual 3,5 order and valuation control at an ordinary terminal, not an identified rare obstruction.

~~~python
from fractions import Fraction as Q
from math import ceil, floor, isqrt, prod

W,H=10**11,10**6

def series(y):
    z=(y-1)/(y+1)
    s=2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s, s+2*z**25/(25*(1-z*z))

L2,U2=series(Q(2))

def logs(x):
    y,k=Q(x),0
    assert y>=1
    while y>=2:
        y/=2
        k+=1
    a,b=series(y)
    return Q(floor(W*(a+k*L2)),W),Q(ceil(W*(b+k*U2)),W)

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]
def up(x): return Q(ceil(W*x),W)
def prime(p): return p>=2 and all(p%i for i in range(2,isqrt(p)+1))

def depth(b,p):
    m=p-1
    while m%3==0 and pow(b,m//3,p)==1:
        m//=3
    j=0
    while m%3==0:
        j+=1
        m//=3
    return j

def tree_budget(r,s):
    F,L,P=s[-1],Q(0),Q(1)
    for w in reversed(s[:-1]):
        F,L,P=w+F**r,w+L**r,r*P*F**(r-1)
    return L**r+r*P*F**(r-1)

s,t=Q(1,11),Q(1,31)
assert tree_budget(3,[s,t])==s**3+9*s*s*t*t+18*s*t**5+9*t**8
assert Q(4,3)*Q(3,10)+18*Q(3,10)**3+9*Q(3,10)**5<1

def early(b):
    return sum((Q(1,p+1) for p in range(55,3457,108)
                if prime(p) and depth(b,p)>=3),Q(0))

c=Q(22,25)
assert lo(lo(32))-Q(1,34)-18*max(early(3),early(5))>c
assert lo(34)-c>Q(3,34)

l,u=logs(324)
Um,Up,Vm=108-u,108-l,34-u
S=(hi(81)+Q(1,2))/54
R=min(S,(1/Um+hi(Up/Vm))/54)
assert 3*S<=Q(3,10)

def weighted(k):
    rhs=(hi(108)+k)**3/Um
    rhs+=sum((hi(t+1)+k)**3*hi((t+1-l)/(t-u))
             for t in range(34,108))
    return Q(27,54**4)*rhs

old81=up(min(R*Q(9,2)*S*S,R*3*S*S,R*27*S**3,weighted(Q(1,5))))
new81=up(weighted(-c))
assert new81<old81

oldtail=Q(27,10)/H*(2*(hi(2*H)+Q(1,2))+2*U2)
L=hi(H)+Q(1,2)
newtail=oldtail/2+Q(81,8)/H**2*(L**3/2+3*L*L/4+3*L/4+Q(3,8))
answer=Q(111020555,10**11)-(old81-new81)-(oldtail-newtail)
assert answer<Q(876,10**6)
print([float(x) for x in (old81,new81,oldtail,newtail,answer)])

q=3727
ps=(379,1567,163,487)
step=9*96850378533865880
assert step%3960==0 and (step//9)%3
assert all(prime(p) and p%4==3 for p in ps+(q,))
assert tuple(depth(3,p) for p in ps+(q,))==(3,3,4,5,4)
assert pow(3,q-1,q*q)!=1

def z(j,m):
    return (pow(3,3960+step*j,m)+pow(5,3960,m))%m

assert len({z(j,q) for j in range(9)})==9
a,b=358993985011945285403524431,203500256289356407333471827
assert (a-b)%prod((4,3,7,11,19,23,379**2,1567**2,163**2))==0
assert (a-b)%487**2!=0
for n,want in ((a,{8}),(b,{5,8})):
    assert n%4==3 and all(n%p==0 for p in (3,7,11,19,23))
    hits=set()
    for p in ps:
        k=min(2,depth(3,p)-2)
        bad={j for j in range(9) if (n-z(j,p*p))%p==0}
        assert all((n-z(j,p*p))%(p*p)!=0 for j in bad)
        if bad:
            v=min(bad)%3**k
            assert bad=={j for j in range(9) if j%3**k==v}
            hits.add((k,v))
    def live(k,j):
        if (k,j) in hits: return set()
        if k==2: return {j}
        return set.union(*(live(k+1,j+d*3**k) for d in range(3)))
    assert live(0,0)==want
    print("surviving leaves",sorted(want))

~~~
