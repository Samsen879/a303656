# A factor-free aggregate 49th-power mismatch and an invisible native control

This follows [the septic reciprocity certificate](https://github.com/Samsen879/a303656/commit/7b514b6bb0e77a41016d13c3dd7a393bd54de811). Unlike that earlier known-split closure, the first example here uses no split. It proves that at least one prime in a native composite fails; it does not give its identity or close the row. A verified second example shows why even all the locally trivial rational words do not recover primewise joint phases.

For \(P=1+X^{15}-X-X^{131}\), set \(M=26717908551918972727509122511988955591425904906909\) and \(x=3088177783201613341856596606977577493764097037402\). The frozen three-band enumerator from [the paired-product replay](https://github.com/Samsen879/a303656/commit/26575f9c2ca06e032a2947555db77561d5840438), requesting the pair \((15,131)\), gives exactly \(E=24\bmod49,k=145\). The ring calculation below forms \(\alpha=N_{\mathbf Q(\zeta_{343})/\mathbf Q(\zeta_{49})}P(\zeta_{343})\). Its absolute norm is \(7M\) by the independently verified raw resultant. Evaluation at \(x^7\) is zero modulo \(M\), so the ideal \((M,\zeta_{49}-x^7)\) divides \((\alpha)\). Its index is \(M\), hence it accounts for the full non-7 part, with multiplicities. Independently repeated CRT checks of the raw resultant modulo 26 primes gave the equality \(N(\alpha)=7M\), using the bound \(4^{294}\).

Let \(W=3^25^5\). It is a 49th power in \(\mathbf Q_7\) since \(W^6\equiv1\bmod343\); the 7-adic principal units have logarithm in \(7\mathbf Z_7\), and exponent 49 takes them onto \(343\mathbf Z_7\). The wild local symbol is trivial. The [Hilbert product formula and tame-symbol formula](https://openmaths.org/courses/NT-CFT/power-residue-symbols-and-reciprocity-laws.html) then identify the aggregate log of \(W\) with the sum of \(2\) times the log of \(\alpha\bmod3\) and \(5\) times the log of \(\alpha\bmod5\). These inert fields have sizes \(3^{42}\) and \(5^{42}\). Their logs are \(7\) and \(45\), giving \(43\bmod49\). If every prime passed the native menu, the log would instead be \(15\): sum the local weights \((p-1)/343\) with their multiplicities, which is \((M-1)/343\bmod49\) by multiplication of \(p\equiv1\bmod343\). These agree modulo 7; the two independent septic symbols also pass with logs \((6,2)\). The septic replay below removes the single \((1-\zeta_7)\) factor from the lower norm and makes the remaining generator primary.

For the control \((66,129)\), the distinct native root gives the complete menu \(E=44\bmod49,k=180\). At the certified \(p=633553982769970403\) the actual projection logs \((205,339)\) disagree with the permitted prediction \((240,325)\). Their difference \((-35,14)\) is invisible modulo 7, and is killed by both weak word families: at levels 49 and 343 the kernel of local rational words is generated respectively by \((2,5)\) and \((11,3)\). This follows from the principality condition modulo \(7^{j+1}\) and the fact that \(3^6\) generates its principal unit quotient, so each verified primitive kernel vector with invertible second coordinate exhausts the full kernel. Their dot products are \(0,-343\), respectively. These probes can thus all agree with the *same* wrong lift. Also \(I+(\beta)\), for the evaluation ideal \(I=(M,\zeta-y)\), merely has index \(\gcd(M,\beta(y))\); ideal saturation by itself gives no extra localization.


```python
from math import gcd,isqrt,prod
def add(v,i,k,s):
    i%=7*s
    if i<6*s: v[i]+=k
    else:
        for j in range(6): v[i-6*s+j*s]-=k
def elem(s,j=0):
    return [int(i==j) for i in range(6*s)]
def mul(a,b,s):
    c=[0]*(6*s)
    for i,x in enumerate(a):
        if x:
            for j,y in enumerate(b):
                if y: add(c,i+j,x*y,s)
    return c
def power(a,n,p,s):
    c=elem(s)
    while n:
        if n%2: c=[x%p for x in mul(c,a,s)]
        a=[x%p for x in mul(a,a,s)]
        n//=2
    return c
def transfer(a,s):
    c=elem(s)
    for k in range(7):
        v=[0]*(6*s)
        for i,t in enumerate(a): add(v,i*(1+s*k),t,s)
        c=mul(c,v,s)
    assert all(t==0 for i,t in enumerate(c) if i%7)
    return c[::7]
def log(a,b,m,s):
    v=power(a,(b**(6*s)-1)//m,b,s)
    return next(j for j in range(m) if power(elem(s,1),j,b,s)==v)

M=26717908551918972727509122511988955591425904906909
x=3088177783201613341856596606977577493764097037402
assert pow(2,M-1,M)!=1 and pow(x,343,M)==1 and gcd(pow(x,49,M)-1,M)==1
assert (1+pow(x,15,M)-x-pow(x,131,M))%M==0
u=elem(49)
u[15],u[1],u[131]=1,-1,-1
a=transfer(u,49)
assert sum(t*pow(x,7*i,M) for i,t in enumerate(a))%M==0
assert [log(a,b,49,7) for b in (3,5)]==[7,45]
assert pow(3**2*5**5,6,343)==1
assert (2*7+5*45)%49==43
assert (M-1)//343*24*(2+5*145)%49==15
a=transfer(a,7)
v=mul(a,[6,5,4,3,2,1],1)
assert all(t%7==0 for t in v)
a=[t//7 for t in v]
for k in range(7):
    # Use exact (not reduced mod 7) representation of zeta^k.
    base=[0]*6
    add(base,k,1,1)
    v=mul(a,base,1)
    if sum(v)%7 and sum(j*t for j,t in enumerate(v))%7==0: break
assert [log(v,b,7,1) for b in (3,5)]==[6,2]

R=237581583404462689945386635341
x=216785655954312809247291330593
p=633553982769970403
F=(2,7,7,7,61,139,108921816233)
assert prod(F)==p-1 and all(all(d%i for i in range(2,isqrt(d)+1)) for d in F)
assert pow(2,p-1,p)==1 and all(gcd(pow(2,(p-1)//d,p)-1,p)==1 for d in F)
assert R%p==0 and pow(x,343,R)==1
assert (1+pow(x,66,R)-x-pow(x,129,R))%R==0
e=(p-1)//343
assert [pow(b,e,p) for b in (3,5)]==[pow(x,e*j,p) for j in (205,339)]
assert 240%49==44 and 180*240%343==325
for m,a,b in ((49,2,5),(343,11,3)):
    assert pow(3,6*(m//7),7*m)!=1 and pow(3**a*5**b,6,7*m)==1
    assert (-35*a+14*b)%m==0
```
