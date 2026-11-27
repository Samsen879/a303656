# Distinct old readers give representation density above 99.960011%

**The exception-density bound improves to below \(0.039989\%\)** at the same cutoff. The outward-rounded replay gives \(0.039988617\%\). The finite depth-one charge falls from \(0.00032230937\) to \(0.00005679678\) in density units. All other charges, including the \(D=81\) term and both tails, carry forward. [Previous whole-line certificate](https://github.com/Samsen879/a303656/blob/a476e9ca22a16358c763229700f7bf07a9f5212b/analysis/ajt5_overnight_2026_11_26/WHOLE_REPAIR_LINE_DENSITY_BOUND.md)

### Use both second digits

At a doubly ordinary source \(r\), a collision modulo \(r\) gives the first-digit repair line \(j=s_0+\lambda i\). For each of its \(r\) low points, vary **both** second digits. The condition that the residual vanish modulo \(r^3\) excludes one affine line in this second-digit grid. The other \(r(r-1)\) repairs all have exact valuation two and share the same terminal shift modulo \(q\).

For each dropped older reader \(p\), let \(X_p\) count the phases it kills, divided by \(r(r-1)\). Conditional on the retained observations and \(n_r\), the phases are predetermined, so \(\mathbb E X_p\le r/(p+1)\). There are two observer bounds.

- A **shallow** reader sees only first digits. If its shift is nonconstant along the repair line, the order-\(r\) fiber bound gives \(X_p\le K_r\), where \(K_r=\lfloor(1+\sqrt{4r-3})/2\rfloor\).
- A **deep** reader sees a second digit on at least one axis. For each fixed value of the other second digit, its \(r\) shifts modulo \(p\) are distinct. It kills at most \(r\) repairs per low point, hence \(X_p\le r/(r-1)\le K_r\). This explicitly allows the second repair digit to be visible.

On a nonconstant terminal line, a first blocker requires at least \(H=r-K_r\) bundles to be entirely killed. Thus \(\sum_p X_p\ge H\). For \(H-(m-1)K_r>0\), the sum of products over ordered \(m\)-tuples of **distinct** readers is at least \(\prod_{j=0}^{m-1}(H-jK_r)\) on this event. This follows by extending each tuple: previously used readers remove at most \(K_r\) each from the available sum. Distinct prime observations are independent after the stated conditioning. The probability is therefore at most
\[
\psi=\min\!\left(1,\ \min_{\substack{1\le m\le6\\H-(m-1)K_r>0}}
              \prod_{j=0}^{m-1}\frac{rS}{H-jK_r}\right),
\]
where \(S\) is the published reciprocal-weight envelope.

### Charge the alignments separately

A constant terminal line occurs at at most one intercept, giving charge \(1/r^2\). A shallow older reader is constant only if its two nontrivial characters agree along the line and their coefficients cancel. Its constant shift is then zero. This takes at most one intercept and can kill a phase only if \(n_p\equiv0\bmod p\). Since \(p\ge2r+1\), the total older-alignment charge is at most
\[
\frac{\widehat S}{r^2},\qquad \widehat S=\left(1+\frac1{2r+1}\right)S.
\]

For fixed \(n_r\), the observations of the constant older readers are disjoint from those used in the moment calculation. Thus a valid combined source-depth charge is
\[
\frac{\psi}{r}+(1-\psi)
       \min\!\left(\frac1r,\frac{1+\widehat S}{r^2}\right).
\]
The replay takes its minimum with the previous whole-line charge at each source. The unchanged terminal factor is applied after all older observations. The other compensation branches and sources with a nonordinary axis retain their previous charges.

The remaining finite depth-one term is mostly the terminal constant-intercept allowance. Its upward-rounded subtotal over the doubly ordinary sources is \(0.00005068521\), compared with the entire revised term \(0.00005679678\). Higher distinct-reader moments alone cannot remove that allowance.

### Standalone replay

```python
from fractions import Fraction as Q
from math import ceil, floor, isqrt

W,P = 10**11,10**5

def series(y):
    z = (y-1)/(y+1)
    s = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return s,s+2*z**25/(25*(1-z*z))

l2,u2 = series(Q(2))
def logs(x):
    y,k = Q(x),0
    while y>=2:
        y /= 2
        k += 1
    a,b = series(y)
    return Q(floor(W*(a+k*l2)),W),Q(ceil(W*(b+k*u2)),W)

def hi(x):
    return logs(x)[1]

flags = bytearray(b"\x01")*(P+1)
flags[:2] = b"\x00\x00"
for r in range(2,isqrt(P)+1):
    if flags[r]:
        flags[r*r::r] = b"\x00"*((P-r*r)//r+1)

old = new = constant = Q(0)
for r in range(31,P+1,4):
    if not flags[r]:
        continue
    l,u = logs(4*r)
    S = (hi(r)+Q(1,2))/(r-1)
    R = min(S,(1/(Q(4*r,3)-u)+hi((Q(4*r,3)-l)/(34-u)))/(r-1))
    E0 = E1 = Q(1,r)
    if all(pow(b,r-1,r*r)!=1 for b in (3,5)):
        K = (1+isqrt(4*r-3))//2
        H = r-K
        E0 = Q(1,r*r)+(Q(1,r)-Q(1,r*r))*min(1,r*S/H)
        psi = moment = Q(1)
        for j in range(6):
            if H-j*K<=0:
                break
            moment *= r*S/(H-j*K)
            psi = min(psi,moment)
        cap = min(Q(1,r),(1+(1+Q(1,2*r+1))*S)/r**2)
        E1 = min(E0,psi/r+(1-psi)*cap)
        constant += Q(ceil(W*R/r**2),W)
    old += Q(ceil(W*R*E0),W)
    new += Q(ceil(W*R*E1),W)

assert (old,new,constant) == tuple(
    Q(x,W) for x in (32230937,5679678,5068521))
answer = Q(66539876,W)-old+new
assert answer==Q(39988617,W)<Q(39989,10**8)

# Ordinary controls: 683 kills an aligned line; 17299 sees digit two.
n,c,d,r,p,C = 6028380249757748835,59811986528,55,31,683,3960
def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

assert (n-S(c,d,4))%4==1 and (n-pow(5,d,3))%3
assert all((n-S(c,d,t))%t for t in (7,11,19,23))
L = C*p
assert pow(3,L,p*p)==pow(5,20*L,p*p) and pow(3,L,p)!=1
assert all(pow(b,L*r,p*p)==1 for b in (3,5))
for i in range(r):
    j = (14+20*i)%r
    x,y = c+L*i,d+L*j
    assert (n-S(x,y,r*r))%(r*r)==0
    assert (n-S(x,y,p*p))%(p*p)==p
p = 17299
L = C*p
assert (p-1)%(r*r)==0 and pow(5,(p-1)//r,p)!=1
assert len({S(c,d+L*(14+r*v),p) for v in range(r)})==r
print("OK",float(100*answer),"%")
```

The ordinary controls demonstrate why both exceptions matter. At \(683\), every exact-two repair on the aligned line has valuation one at the fixed reader phase. At \(17299\), changing the second digit produces \(31\) distinct shifts. Neither example is a genuine exceptional terminal. The new numerical result bounds growth-box misses and hence all-exponent exceptions.

For the moment estimate, fix the source observation first and exclude the constant shallow rows from the distinct tuple sum. Each remaining \(X_p\) depends on the observation at \(p\) alone, since the retained phases and both sets of source digits are chosen without those observations. If no constant shallow row kills any bundle, the first-blocker event is bounded by \(\psi\); if one does so, use the trivial bound. For each such source observation the two groups of rows are disjoint, so the corresponding probability is at most \(a+(1-a)\psi\), where \(a\) is the probability of the constant-reader event. Integrating in the \(r\)-observation and including the possible constant terminal intercept gives the combined charge. No independence across the individual repairs of one reader is used.
