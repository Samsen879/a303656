# Joint 2-adic and 11-adic sieve for true complementary earlier divisors

**The two square requirements give a joint sieve on true earlier divisors.** For fixed \(H=w_*R\), the divisors \(\ell\) and \(E/\ell\) give identical residuals modulo \(11^3\), but at most one can pass the \(2\)-adic test. The sieve leaves 144 classes modulo \(64\cdot1331=85184\). [Pinned earlier-share result](https://github.com/Samsen879/a303656/commit/2313d76afde388f48413278365672876a4f9257a)

### The joint restriction

Use the same exact pair \(v=H\ell,\ u=d/v\), and write \(S=(u+v)/2\). The remaining square tests are \(S^2-e\) and \(S^2-f\). On the pinned progression, \(H\equiv1\bmod16\), \(d/8\equiv13\bmod16\), \(E/8\equiv5\bmod16\), \(e\equiv29\bmod32\), and \(f\equiv0\bmod8\).

The \(2\)-adic test forces both factors even. Writing \(\ell=2^\nu t\) with \(t\) odd, \(S^2-f\) is then a unit square, and \(S^2-e\) is a square exactly when \(S\equiv\pm1\bmod16\). Substituting the exact quotient gives
\[
\begin{array}{c|c}
\nu & t\bmod16\\ \hline
1 & 3,\ 13\\
2 & 1,\ 15
\end{array}
\]
or \(\ell\equiv4,6,26,38,58,60\bmod64\).

At \(11\), \(H\equiv1\) and \(E\equiv d\equiv543\bmod1331\). The first residual has four simple roots modulo \(11\). To avoid odd valuation, \(\ell\) must first lift to \(4,45,76,117\bmod121\). Each has six lifts modulo \(1331\) that pass the square test there. Five give a stable square and one requires higher precision. The second residual is automatically a unit square on these classes. Thus 120 of the 144 joint classes give stable lifts at both primes, and 24 require more precision at \(11\).

For the **true complementary divisor** \(\ell'=E/\ell\), the two exact factors swap residues modulo \(1331\). At \(2\), however, \((\nu,t)\) changes to \((3-\nu,5/t\bmod16)\). Every admitted row of the table then gives \(S'^2-e\equiv20\bmod32\), whose unit after division by \(4\) is \(5\bmod8\). So the complement fails at \(2\).


The replay checks the pinned exponent progression under both moduli, evaluates the actual cyclotomic products by their Möbius product, and enumerates the unit residue classes without factoring any enormous integer. The modulo-1331 checks use \(4(S^2-e)\) and \(4(S^2-f)\), which have the same square status at 11. No claim here establishes a true divisor inside the ordinary interval or either required integer square.

```python
from itertools import product
from math import prod
g=468741
P=21112080
h,k=12416651,10186
a,b=1331*g*h+1,1331*g*k-2
def divs(n):
    fs=[]
    m=n
    j=2
    while j*j<=m:
        if m%j==0:
            fs.append(j)
            while m%j==0:m//=j
        j+=1
    if m>1:fs.append(m)
    return [(n//prod(w for w,e in zip(fs,bits) if e),(-1)**sum(bits)) for bits in product((0,1),repeat=len(fs))]
def phi2(m,mod):
    m0=4*mod if mod==16 else mod
    val=1
    for d,sign in divs(m):
        s=(pow(3,h*d,m0)+pow(5,k*d,m0))%m0
        if mod==16:
            assert s%4==0
            s//=4
        val=val*pow(s,sign,mod)%mod
    return val
assert all(pow(z,P,m)==1 for z in (3,5) for m in (64,1331))
N0=1331*g
H=lambda m:prod(phi2(j,m) for j in (1331*468741,1331*3939,1331*1717,N0//11))%m
assert H(16)==H(1331)==1
d=lambda m:2*(pow(3,a,m)+75*pow(5,b,m))%m
E=lambda m:6*(pow(3,11*g*h,m)+pow(5,11*g*k,m))%m
assert d(128)//8==13 and E(128)//8==5
A,B=pow(3,a,1331*32),pow(5,b,1331*32)
e,f=20*A+25*B,182*A-6*B
assert e%32==29 and f%8==0
assert d(1331)==E(1331)==543
out=[]
for nu in (1,2):
 for t in range(1,16,2):
    z=(2**(nu-1)*t+2**(2-nu)*13*pow(t,-1,16))%16
    if (z*z-e)%32==4:
        out+=[j for j in range(64) if j%2**(nu+4)==2**nu*t%2**(nu+4)]
        tp=5*pow(t,-1,16)%16
        cp=3-nu
        y=(2**(cp-1)*tp+2**(2-cp)*13*pow(tp,-1,16))%16
        assert (y*y-e)%32==20
assert sorted(out)==[4,6,26,38,58,60]
mod=1331
squares={j*j%mod for j in range(mod)}
good,stable=[],[]
for l in range(1,mod):
 if l%11==0:continue
 u=d(mod)*pow(l,-1,mod)%mod
 t=(l+u)**2
 G,J=(t-4*e)%mod,(t-4*f)%mod
 if G in squares and J in squares:
    good.append(l)
    if G:stable.append(l)
assert len(good)==24 and len(stable)==20 and {l%121 for l in good}=={4,45,76,117}
print("OK")
```
