# Ordinary phase rows can survive a strict positive height window

The [finite-panel lifting test](FIXED_PANEL_EVEN_VALUATION_CONSTRUCTION.md) can remove ordinary rows when exponents may grow, but this does not project faithfully to a prescribed positive exponent window. Two exact examples use the original bases \(3,5\).

At \(n=269\), require \(c\ge3\) and positive residual \(R=n-3^c-5^d\equiv1\bmod8\). The complete menu is \(\{3,5\}\times\{0,2\}\):
\[
\begin{pmatrix}241&217\\25&1\end{pmatrix}.
\]
All rows are units at 3, and only \((3,2)\) fails at 7 (valuation one). Both axis projections are still full after removing the failed cell. This is a smallest possible complete four-cell menu under the stated seed rule: at fixed \(n\bmod8\), \(R\equiv1\bmod8\) fixes the parities of both exponents, as the four possible offset classes are distinct. Two same-parity exponents require \(c_{\max}\ge5\), \(d_{\max}\ge2\), and positivity then forces \(n>268\).

To repair the rejected point while preserving its mod-7 power phase, write \(c=3+6u,d=2+6v\), with \(u,v\) nonnegative. For \(n\equiv269\bmod1176\), binomial reduction modulo 49 gives \(R/7\equiv3-u-3v\bmod7\). Reaching depth at least two needs \(u+3v=3\bmod7\). The smallest eligible power sum is \(3^3+5^8=390652\): beneath this bound, \(u\le1,v\le1\), and the only solution among those is \((0,1)\). The first target in the progression above that power sum is 390701, and its residual is exactly \(49\). At 269 no such representative can enter the positive window.

For \(n=3028\), instead allow \(c\ge3\) and retain positive residuals with odd part \(1\bmod4\) and even \(v_3\). Exactly three labels remain:
\[
 (3,1;2996),\quad(5,3;2660),\quad(7,1;836).
\]
Row 7 rejects the first two; row 11 rejects the last. Each row alone admits a passing label. The unrestricted original target nevertheless has the representation \(55^2+1^2+3^0+5^0\), outside the specified \(c\)-window.

In the one-row repair calculation there is also a useful sufficient margin. Suppose varying an exponent by a period \(M\) preserves the mod-\(p\) power phase, \(p\nmid M\), and the chosen base is ordinary at \(p\) so \(v_p(b^M-1)=1\). If the residual collides mod \(p\), among any \(2p\) consecutive legal step parameters one gives exact \(v_p=2\). The unique mod-\(p\) class of parameters giving a zero mod \(p^2\) occurs twice; their difference in parameter is \(p\), and the residuals then differ by a nonzero multiple of \(p^2\bmod p^3\). At most one fails the exact-depth-two test. This check requires actual legal height margin on each step and is not an unconditional multi-row guarantee.

```python
def v(n,p):
    k=0
    while n%p==0:
        n//=p; k+=1
    return k
def rows(n):
    out=[]
    for c in range(3,n.bit_length()):
        for d in range(n.bit_length()):
            r=n-3**c-5**d
            if r>0:
                out.append((c,d,r))
    return out
a=[(c,d,r) for c,d,r in rows(269) if r%8==1]
assert a==[(3,0,241),(3,2,217),(5,0,25),(5,2,1)]
assert all(v(r,3)==0 for c,d,r in a) and [v(r,7) for c,d,r in a]==[0,1,0,0]
assert (390701-269)%1176==0 and 390701-1176<=390652
assert 390701-3**3-5**8==49
b=[(c,d,r) for c,d,r in rows(3028) if r//2**v(r,2)%4==1 and v(r,3)%2==0]
assert b==[(3,1,2996),(5,3,2660),(7,1,836)]
assert [(v(r,7),v(r,11)) for c,d,r in b]==[(1,0),(1,0),(0,1)]
assert 3028==55**2+1+1+1
```
