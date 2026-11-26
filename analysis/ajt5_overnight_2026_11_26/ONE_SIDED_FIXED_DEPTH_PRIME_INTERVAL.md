# Fixed-depth prime intervals and an exact one-sided rough-part test

Use the \(109\)-supported negative cross-offset model with actual \(X=3^a,\ Z=5^b,\ \Delta=Z-X\) and \(\max(X,Z)+1<n<X+Z\). In the one-sided branch write
\[
 R_s=n-1-Z=Sw_s,\qquad R_d=n-1-X=D_0p^Ew_d.
\]
Here \(S,D_0\) are the fixed smooth factors at \(2,3,5,109\), and \(p>5\) is an additional inert prime absent from \(S,D_0\). We require \(p\nmid\Delta\) to give \(v_p(R_s)=0\) when the second residual has \(v_p=E>0\). Both rough parts must lie in \([L,U)\) and their product be below \(LU\), where \(L,U\) are the products of the first two and next two inert primes outside the panel.

For fixed \(S,D_0,E\), the equality \(R_d-R_s=\Delta\) first implies
\[
 \frac{\Delta+SL}{D_0(U-1)}\le p^E
 \le\frac{\Delta+S(U-1)}{D_0L}.
\]
If \(\Delta\ge0\) the endpoints have ratio at most \(K^2\), with \(K=(U-1)/L\). Thus the candidate prime powers yield \(p\)-values in a multiplicative interval of width at most \(K^{2/E}\). In a further interval \([P,P+H]\cap[7,Y]\), with upper endpoint \(B\) and nonempty intersection, there are at most \(1+\lfloor\min(H,B(1-K^{-2/E}))/4\rfloor\) inert candidates. At \(Y=109\), \(L=127\cdot131,\ U=139\cdot151\); the integer inequality \(105^{14}(U-1)^2<109^{14}L^2\) makes the possible span strictly below four at \(E\ge14\), hence at most one prime for these fixed data. This does not combine different depths, nor bound the \(\Delta<0\) case by the same multiplicative interval.

For exact assessment of a surviving \(p\) set \(D=D_0p^E,\ g=\gcd(D,S)\) and \(w=w_d\). There is no candidate if \(g\nmid\Delta\). Otherwise impose \(w\equiv(\Delta/g)(D/g)^{-1}\bmod S/g\) (trivial condition when \(S/g=1\)). Then impose the active height, \(L\le w,(Dw-\Delta)/S<U\), and the strict product test, equivalently \(Dw^2-\Delta w\le SLU-1\). Finally check the actual smooth-factor depths and the two-square criterion or exact witnesses. The congruence, height, and product tests work for either sign of \(\Delta\).

## Two exact one-sided examples

Both examples have two genuine two-square residuals and the correct individual rough-part bounds. One passes the stronger product window and one fails it. The primes and depths here are illustrative, with \(E=2\), rather than examples of the \(E\ge14\) width bound.

```python
from math import gcd
L,U=127*131,139*151
assert 105**14*(U-1)**2<109**14*L**2
rows=[
 (1389699015,18,13,47,3**4*109,5**2,19141,18149,(1017,12960),(4418,31349),True),
 (246390495,14,12,23,109,5**2,20641,18269,(430,1437),(4255,14950),False)]
for n,a,b,p,S,D0,ws,wd,sq1,sq2,passes in rows:
    X,Z=3**a,5**b; delta=Z-X
    assert max(X,Z)+1<n<X+Z
    rs,rd=n-1-Z,n-1-X
    assert rs==S*ws==sum(z*z for z in sq1)
    assert rd==D0*p*p*wd==sum(z*z for z in sq2)
    assert delta%p and rs%p and rd%p**3
    assert L<=ws<U and L<=wd<U and gcd(ws,wd)==1 and ws%4==wd%4==1
    assert (ws*wd<L*U)==passes
```
