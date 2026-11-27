# A signed Gaussian representation count with genuine zero-weight pairs

The shared Gaussian sieve gives a signed inequality across the original 147 compatible phases. For all sufficiently large balanced \((a,b)\), the sifted representation count satisfies
\[
\boxed{W_0\ge \tfrac54 W_-}.
\]
This also holds with \(W_-\) truncated at any fixed \(7\)-depth. The sign for distinct true pairs remains open. The same sieve gives **zero weight** to \(\gg BK/\log B\) genuine target–label pairs in each class, already among alternatives of \(7\)-depth zero.

### The signed Gaussian count

Use even \(a,b\), \(A=3^a\), \(B=5^b\), and \(39/40<B/A<122/125\). Keep \(n=S_0+45u\) in the ordinary window, where \(S_0=A+25B\). In the original steps-\((4,2)\) grid of size \(K\), restrict to \(y\equiv b+2\bmod6\). Each of the 147 compatible phase cells has \(K/441+o(K)\) labels. For \(S_i=3^x+5^y\), put \(k_i=(S_0-S_i)/45\) and \(H_i=k_i/4\). The target classes are \(r_0=0\) and \(r_-=3^{a+4}+5^{b+2}+7\bmod49\).

For \(W_r\), count ordered Gaussian representation pairs with vectors \((w\pm gm,e\pm gd)\), where \(mw+de=H_i/g\), \((m,d)=1\), and \(7\nmid m\). Use the same boxes and split-prime orientations in both classes. The boxes can be chosen jointly for every label: \(k_i=S_0/45+O(B^{1/3})\), so the box centered using \(S_0/45\) still fits inside the ordinary window with a uniform interior margin. Let \(g\) range over the same squarefree products of small split primes dividing \(H_i\), with \(g\le X^{1/20}\), \(X=\sqrt B\).

Apply the upper and lower sieve weights at level \(X^{1/20}\) and cutoff \(z=X^{1/(20s)}\), with a sufficiently large fixed \(s\). The audited distribution error summed over the sieve moduli and \(g\) is \(X^{7/4+o(1)}\) per label. Summing the local choices of \(g\) gives the common label factor
\[
\Delta_i=\prod_{\substack{p<z,\ p\equiv1\ (4)\\p^2\mid H_i}}
\left(1-\frac1{p(p-1)}\right).
\]
The omitted large-\(g\) mass is \(o(1)\) uniformly. Thus \(W_r\) is within relative \(1/100+o(1)\) of a common positive multiple of \(\sum_i\Delta_i L_r(i)\), with the multiple \(\asymp B/\log B\). Here \(49L_r(i)\) is the number of permitted Gaussian residue pairs modulo \(49\). Also \(37/40\le\Delta_i\le1\). Indeed the possible losses sum to at most \(1/20+\frac1{16}\sum_{j\ge3}(j^2-1/4)^{-1}=3/40\), using the factor at \(5\) and the next possible split prime \(13\). [Shared upper and lower sieve weights, Theorem 2.2](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

For unit norm residues \(u,v\bmod7\), let \(N_t(x)=\#\{y:x^2+y^2=t\bmod7\}\). Requiring \(7\nmid m\) means the first coordinates differ modulo \(7\), giving \(L_r=64-\sum_xN_u(x)N_v(x)\). Each unit vector has seven lifts to its prescribed norm modulo \(49\). If the alternative norm is zero modulo \(49\), its vector has both coordinates divisible by \(7\), giving \(L_r=7(8-N_u(0))\).

With \(\gamma=4B/A\bmod7\), the resulting table is

| Class | \(x\equiv a\pmod{12}\) | \(x\equiv a+4\pmod{12}\) | \(x\equiv a+8\pmod{12}\) |
|---|---:|---:|---:|
| \(r_0,\ \gamma=1\) | 50 | 56 | 52 |
| \(r_0,\ \gamma=2\) | 48 | 56 | 56 |
| \(r_0,\ \gamma=4\) | 48 | 52 | 56 |
| \(r_-\) | 50 | 0 in 42 cells, 42 in 7 cells | 60 |

Each column has 49 cells. In cell units, the \(r_-\) main sum is at most \(5684\). For the signed main sum, use \(37/40\) on positive differences and \(1\) on negative differences, retaining the same \(\Delta_i\) in the two classes. The worst row gives
\[
\frac{37}{40}(49\cdot52-7\cdot42)-49(2+4)
=\frac{35819}{20}.
\]
Even after the shared upper and lower sieve errors, \(\frac{99}{101}(1+(35819/20)/5684)>5/4\). This proves the weighted inequality.

### True pairs of zero weight

In **every** compatible phase cell, refine to \(y\equiv b+2\bmod54\). This retains \(1/9+o(1)\) of its labels and forces \(9\mid k_i\), since \(5^{54}\equiv1\bmod81\) and \(x,a\ge4\). For these labels, require \(u=9v\) and apply the true-pair lower bound to \(v,v+k_i/9\), in the interval scaled by \(1/9\). The shift is still a multiple of \(8\) and of ordinary size. The class modulo \(49\) is transported by the unit \(9\). In each unit phase this yields \(\gg B/\log B\) genuine pairs per refined label.

Both original norms are divisible by \(9\). Every Gaussian representation of either norm therefore has both coordinates divisible by \(3\). In any integral half-difference parametrization, \(3\mid g\). All the sieve weights above exclude that \(g\), regardless of the box or the individual split-prime orientations.

Writing \(T_r\) for the distinct true-pair count and \(\mu_r=W_r/T_r\), a sufficient comparison for a positive true gap on its natural scale is \(\limsup\mu_0/\mu_-<5/4\). The shared sieve does not bound that ratio. Its missing support already has the same order as the signed comparison being sought.

### Exact control

The replay constructs a true pair of zero sieve weight in each class. At the second target, the label \(T\) has exact \(7\)-depth one while \(S\) has an ordinary-height witness.

```python
from math import isqrt

R = {t: [sum((x*x+y*y-t)%7 == 0 for y in range(7)) for x in range(7)]
     for t in range(1,7)}
def L(u,v):
    return 64-sum(a*b for a,b in zip(R[u%7],R[v%7]))

assert [[L(2*(1+c),2*(p+c)) for p in (1,4,2)] for c in (1,2,4)] == [
    [50,56,52], [48,56,56], [48,52,56]]
assert (L(1,1),L(1,3),7*(8-R[1][0])) == (50,60,42)

a,b = 7864,5368
A,B = 3**a,5**b
S0,S3 = A+25*B,729*A+B
lo,hi = 2*S3-(A+125*B),729*A+625*B
r = (pow(3,a+4,49)+pow(5,b+2,49)+7)%49
S,T = 3**1144+5**1212,3**1064+5**1086
assert (1144-a)%84 == (1212-b-2)%378 == 0
k,rem = divmod(S0-S,405)
assert rem == k%8 == 0
mid = ((lo-S0)//405+(hi-S0)//405)//2

for cls,offset,t in [(0,22,-2),(r,4,-4)]:
    m = (isqrt(mid+k)-isqrt(mid))//2+offset
    w,e = divmod(k//4,m)
    w,e = w-t,e+m*t
    n = S0+405*((w-m)**2+(e-1)**2)
    assert lo < n <= hi and n%49 == cls
    assert (n-S0)%405 == (n-S)%405 == 0 and (n-S)%7
    for label,p,q in [(S0,w-m,e-1),(S,w+m,e+1)]:
        p,q = sorted((9*abs(p),9*abs(q)), reverse=True)
        assert n == label+(2*p+q)**2+(p-2*q)**2
        assert S3 < label+(2*p+q)**2 <= hi
    if cls:
        assert (n-T)%49 == 7
```

Independent BigInt checked the full mod-7 weight table, the exact rational margin for the 5/4 ratio, and both true target–label pairs receiving zero sieve weight. The signed inequality is for ordered, sifted Gaussian representation pairs only. It cannot be substituted for a true-pair inequality without a new comparison of the lost support and multiplicities.
