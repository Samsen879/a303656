# A certified logarithmic matching majority in every residue class modulo 15

**Every class mod 15 has a certified majority with a matching of size at least \((\log X)/57\).** Here a matching uses distinct \(c\) labels and distinct \(d\) labels, and every matched cell has a positive two-square remainder. The rectangle is the same as in the verified endpoint theorem,
\[
X^{1/8}\le 3^c\le X^{1/4},\qquad X^{1/3}\le 5^d\le X^{1/2}.
\]

The bounds are lower limits of the relative proportions over \(X<n\le 2X\). Each table entry applies separately to every class it describes.

| \(n\bmod 3\) | \(n\bmod 5\) | Certified lower proportion |
|---|---|---:|
| \(0\) | \(0\) | \(0.674\) |
| \(0\) | nonzero | \(0.672\) |
| nonzero | \(0\) | \(0.506\) |
| nonzero | nonzero | \(0.504\) |

The exact rational bounds before rounding give an **unconditional lower proportion greater than \(56\%\)**. The two changes from the \(0\bmod15\) proof are a positive row weight computed mod 25 and a parity-dependent upper bound on the endpoint ratio. [Verified \(0\bmod15\) baseline](https://github.com/Samsen879/a303656/commit/c4c1c82a33a4855c243f48bd93255a8382e6df9b)

### Local weights and conditional moments

Multiply the capped representation count for \(R=n-3^c-5^d\) by
\[
w(R)=
\begin{cases}
1&5\nmid R,\\
1/2&5\parallel R,\\
4/13&25\mid R.
\end{cases}
\]
This preserves the positive-edge graph. The weighted grand mean and endpoint energy converge jointly to profiles \(F_w,G_w\) by the verified capped argument. For large \(X\), the weight depends only on \(n-3^c\bmod25\). For rows it is a bounded multiplier. For columns, split the \(c\)-average into the 20 classes of \(\operatorname{ord}_{25}(3)\), apply the one-axis approximation on each class, then take the weighted sum. On a fixed class, the nonzero differences divisible by an order \(o\) still have proportion \(O(1/o)\), by counting multiples of \(\operatorname{lcm}(20,o)\). Thus the order-tail estimate and the vanishing capped diagonal carry over. Fixed-class convergence follows by taking the finite moduli divisible by 30. [Verified capped endpoint theorem](https://github.com/Samsen879/a303656/commit/c92bb115bf6404a70b1344d2337835f108e4db7e)

At **5**, write the local norm factor as \((4/5)(v_5(R)+1)\). After weighting, the normalized factor has conditional mean 1 in every residue mod 25. In the terminal residue the conditional mean of \(v_5(R)+1\) is \(13/4\) and its variance is \(5/16\). If \(5\nmid n\), averaging over the starting \(c\)-phase and the target lifts gives terminal probability \((1/4)(1/5)\). The normalized second moment is therefore \(677/676\). For a moving \(c\)-pair, Cauchy–Schwarz gives this same upper bound **at each fixed difference** \(k\), since both starting phases have the same marginal. If \(5\mid n\), the corresponding bound is 1.

At **3**, the normalized factor is the indicator of even valuation. If \(3\nmid n\), half the \(d\)-phases collide mod 3, and conditional on collision the even-valuation probability is \(1/4\). The first moment is \(5/8\), and the frozen-pair ratio is \(8/5\). For a moving \(d\)-pair the exact ratio to the square of the first moment is
\[
M(k)=
\begin{cases}
16/25&k\ \text{odd},\\
8/5-(8/25)3^{-v_3(k)}&k\ \text{even}.
\end{cases}
\]
For odd \(k\) the roots are in opposite unit classes. For even \(k\), their separation has valuation \(e=1+v_3(k)\), by the actual order of 5 and \(v_3(5^2-1)=1\). Within the colliding class the joint even probability is \((1-3^{1-e})/4\). This follows by subtracting the two noncolliding residue classes from the full 3-adic pair kernel. When \(3\mid n\), both normalized factors are always 1. [Local norm densities and pair kernels](https://github.com/Samsen879/a303656/blob/c6236506eedd64362571564f33c8f43bd50cb691/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_PROFINITE_LIMIT.md)

At **2**, conditional on odd \(n\), the pair kernel is 2 for base 5 and \(2\mathbf1_{2\mid k}\) for base 3. Conditional on even \(n\), it is twice the full binary kernel minus the odd kernel. In particular the parity factor and \(M(k)\) must be averaged with the **same** \(k\).

### From the moments to a matching

Let \(\epsilon\) be the parity of \(n\), \(i=\mathbf1_{3\nmid n}\), \(j=\mathbf1_{5\nmid n}\), \(r_i=(8/5)^i\), and \(\lambda_j=(677/676)^j\). Conditional on these classes, the endpoint moment bound is
\[
\frac{\mathbb E G_w}{(\mathbb E F_w)^2}
\le D_{\epsilon i j}
=\lambda_j\bigl(8(1.099)B_{5,\epsilon,i}
          +6(1.610)r_i B_{3,\epsilon}\bigr),
\]
using the following rational upper bounds for the remaining order averages.

| Parity | \(B_3\) | \(B_5\), \(3\mid n\) | \(B_5\), \(3\nmid n\) |
|---|---:|---:|---:|
| Even | 1.458 | 1.233 | 1.542 |
| Odd | 1.228 | 2.247 | 2.390 |

The replay certifies these constants using orders up to \(2^{14}\) and an analytic tail. In the expansion through 61, products of order tests are grouped by their lcm \(l\). For the even-\(k\) part of \(M(k)\), its conditional mean given \(l\mid k\) is \(8/5-(6/25)3^{-v_3(l)}\). The binary factor uses the \(2\)-primary part of the same \(l\). Above 61, the largest-prime term is bounded by
\[
\frac{2}{(q-1)\operatorname{ord}_q(b)}
\prod_{7\le p<q}\frac p{p-1},
\]
times \(8/5\) when \(M\) is present. Above \(2^{14}\), the Mertens product bound and a dyadic split at order \(\sqrt U\) give a tail of at most \((16/15)(7/2)(31/10)/128\), before that same \(8/5\) multiplier. In a block \(U<q\le2U\), the short orders use \(q\mid b^{\operatorname{ord}_q(b)}-1\), and the long orders use the central binomial coefficient. [Rosser–Schoenfeld, Theorem 7](https://doi.org/10.1215/ijm/1255631807)

Set \(\Psi_w=F_w^2/G_w\), with value zero where \(F_w=0\). For odd \(n\), only one parity of \(c\) can give a norm, since \(5^d\equiv1\bmod4\). For \(3\nmid n\), the surviving \(d\)-phase measure at 3 is exactly \(5/8\) for each fixed target, since the powers of 5 fill the 3-adic units. Applying Cauchy–Schwarz on these two endpoint supports gives
\[
\Psi_w\le h_{\epsilon i}
=\bigl(8(1+\epsilon)(1.098)+6r_i(1.609)\bigr)^{-1}.
\]
Conditional Cauchy–Schwarz also gives \(\mathbb E\Psi_w\ge 1/D_{\epsilon i j}\). Thus for \(t=1/57\) the conditional lower bound is \((D_{\epsilon i j}^{-1}-t)/(h_{\epsilon i}-t)\). The two parities have equal weight in each mod-15 class. The matching inequality and the open event \(F_w^2>tG_w\) transfer their average to the stated lower proportions.

### Exact controls and scope

At \(X=10^{10}\), the odd target \(n=10011115577\equiv2\bmod15\) has the two active edges
\[
n-3^3-5^5=3180^2+100005^2,\qquad
n-3^5-5^6=3178^2+100005^2.
\]
Their weights are \(4/13\) and 1. The standalone replay below independently certifies the conditional-order table and both actual edges.

The weight is bounded below by \(4/13\), so \(F_w\) has the same zero set as \(F\) up to null sets. The theorem gives explicit lower proportions at a fixed positive logarithmic threshold. The exact density at that threshold, density one, and pointwise coverage remain open. [Verified zero-atom comparison](https://github.com/Samsen879/a303656/commit/d11b5bd3209a45b0485c7200e30567e1349aa32e)

At a fixed exponent difference the tail local correlations at primes \(\ge7\) depend on the difference alone, since the starting base power is a local unit. This leaves the small-place conditional factors to be averaged jointly only over the corresponding primary components. The constants certify a lower bound, not a limit theorem at this fixed coefficient.

```python
from fractions import Fraction as F
from math import isqrt, lcm

N = 2**14
s = [True]*(N+1)
s[0] = s[1] = False
for p in range(2,isqrt(N)+1):
    if s[p]:
        s[p*p::p] = [False]*((N-p*p)//p+1)
P = [p for p in range(2,N+1) if s[p]]

def order(b,p):
    rem = o = p-1
    for q in P:
        if q*q > rem:
            break
        if rem % q == 0:
            while rem % q == 0:
                rem //= q
            while o % q == 0 and pow(b,o//q,p) == 1:
                o //= q
    if rem > 1:
        while o % rem == 0 and pow(b,o//rem,p) == 1:
            o //= rem
    return o


def vp(l,p):
    z=0
    while l%p==0:l//=p;z+=1
    return z
def local(b,e,i,l):
    r=vp(l,2)
    def val(rr):
        K=F(1,2) if b==3 and rr==0 else (
            F(5,4) if rr==0 else 2-F(1,2**(rr+1)))
        O=F(2 if b==5 or rr>0 else 0)
        return O if e else 2*K-O
    M0=F(8,5)-F(6,25)*F(1,3**vp(l,3)) if i else F(1)
    M1=F(16,25) if i else F(1)
    return val(r)*M0 if r else (val(0)*M1+val(1)*M0)/2
def bound(b,e,i):
    D,bg={1:F(1)},F(1)
    S=10**12
    W,mid=S,0
    for p in P[3:]:
        o=order(b,p)
        if p<=61:
            for l,a in list(D.items()):
                k=lcm(l,o);D[k]=D.get(k,0)+a/(p-1)
            bg*=1-F(1,p*p)
        else:
            d=(p-1)*o
            mid+=(2*W+d-1)//d
        W=(W*p+p-2)//(p-1)
    tail=F(16,15)*F(7,2)*F(31,10)/128
    return bg*(sum(a*local(b,e,i,l)/l for l,a in D.items())+
               (F(mid,S)+tail)*(F(8,5) if i else 1))
B3=[F(1458,1000),F(1228,1000)]
B5=[[F(1233,1000),F(1542,1000)],[F(2247,1000),F(2390,1000)]]
for e in (0,1):
    assert bound(3,e,0)<B3[e]
    for i in (0,1):assert bound(5,e,i)<B5[e][i]
def lower(i,j):
    out=[]
    for e in (0,1):
        r=F(8,5)**i;lam=F(677,676)**j
        D=lam*(8*F(1099,1000)*B5[e][i]+6*F(1610,1000)*r*B3[e])
        h=1/(8*(1+e)*F(1098,1000)+6*r*F(1609,1000))
        t=F(1,57)
        out.append((1/D-t)/(h-t))
    return sum(out)/2
L=[lower(i,j) for i,j in ((0,0),(0,1),(1,0),(1,1))]
assert all(x>y for x,y in zip(L,map(lambda n:F(n,1000),(674,672,506,504))))
assert sum(k*z for k,z in zip((1,4,2,8),L))/15>F(56,100)
X,n=10**10,10011115577
pairs=((3,5,3180,100005),(5,6,3178,100005))
assert X<n<=2*X and n%15==2
for c,d,x,y in pairs:
    a,b=3**c,5**d
    assert X<=a**8 and a**4<=X and X<=b**3 and b*b<=X
    assert n-a-b==x*x+y*y
assert (n-3**3-5**5)%25==0 and (n-3**5-5**6)%5!=0
print([float(v) for v in L])
```
