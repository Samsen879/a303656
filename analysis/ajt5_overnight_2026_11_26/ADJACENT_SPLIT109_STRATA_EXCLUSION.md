# Adjacent 109-depth strata admit a joint exclusion

Extend the [fixed-stratum depth spacing test](FIXED_STRATUM_EVEN_DEPTH_SPACING.md). Fix actual labels \(X=3^a,Z=5^b,\ \Delta=Z-X\ge0\), fixed \(2,3,5\) parts \(s_0,D_0\), and \(Y=109\). Write the shallow residual \(S_fu\), \(S_f=s_0\,109^f\), and the deep residual \(D_0p^Ew\), where \(p\ge7\) is inert and absent from \(S_f,D_0\). Impose the one-sided branch, positive ordinary height, \(L\le u,w<U\), and the strict product bound, where \(L=127\cdot131,\ U=139\cdot151\). Across any two adjacent \(109\)-depth slots \(f,f+1\), at most one actual candidate occurs per two consecutive even-\(E\) slots at \(E\ge380\). This does not cover changing the other smooth factors.

Put \(W=(U-1)^2/L^2\). If depth \(E+2\) changes the \(109\)-valuation by \(\varepsilon\in\{-1,0,1\}\), comparing both magnitude windows from \(D_0p^Ew=\Delta+S_fu\) gives
\[
 r^{E+2}/p^E\le109^{\max(\varepsilon,0)}W,\qquad
 p^E/r^{E+2}\le109^{\max(-\varepsilon,0)}W .
\]
This uses \(\Delta\ge0\). The first bound excludes \(r>p\): for \(r\ge19\) the lower bound \(r^2\) suffices, and for \(p=7,r=11\) already \(11^4/7^2>109W\). If \(p>r\), then \(p/r\ge107/103,\ r\le103\), so the second bound excludes the pair from \(E=256\) when \(f\) stays or increases, and from \(E=380\) even when \(f\) decreases. At equal depths two distinct primes in the two \(f\)-slots are excluded from \(E=136\) by the analogous ratio test.

The genuinely new obstruction for the **same** prime comes from the integer conditions. If both \(f\) and \(f+1\) have actual solutions (at possibly different targets), subtract their common-gap equations. Since \(p\) does not divide \(S_f\), this forces \(p^{\min(E,E')}\mid109u'-u\). But \(0<109u'-u\le109(U-1)-L=2271055<7^8\); no such pair exists at depths at least 8. This argument works for both signs of \(\Delta\). The same prime cannot occupy two distinct depths with unchanged \(f\) once the common magnitude interval has ratio below \(p^2\). Finally at each fixed tuple, two distinct shallow rough parts would have to differ by a nonzero multiple of \(p^E\), which is impossible at these depths. Together the inequalities prove the count.

## Exact size-window overlap that fails to lift

Use actual labels \((0,385),(564,0)\), \(s_0=3^{414},D_0=5^{67}\). The pairs \((f,E)=(32,256),(33,258)\) both have the same size candidate \(p=7\) even after the product and positivity cuts. Their exact final \(w\)-intervals are \([19549,19878]\), \([16637,16736]\); neither admits the required congruence. This demonstrates why magnitude alone does not replace the same-prime divisibility argument.

```python
L,U=127*131,139*151
assert 11**4*L**2>109*7**2*(U-1)**2 and 19**2*L**2>109*(U-1)**2
assert 107**256*L**2>103**258*(U-1)**2
assert 107**380*L**2>109*103**382*(U-1)**2
assert 107**136*L**2>109*103**136*(U-1)**2
assert 7**8>109*(U-1)-L==2271055
X,Z=3**564,5**385
delta=Z-X
assert delta>0 and (delta%7,delta%109)==(4,85)
for f,E,lo,hi in ((32,256,19549,19878),(33,258,16637,16736)):
    S,D=3**414*109**f,5**67*7**E
    keep=[]
    for w in range(L,U):
        x=D*w-delta; n=X+1+D*w
        if S*L<=x<S*U and x*w<S*L*U and max(X,Z)+1<n<X+Z:
            keep.append(w)
            assert x%S
    assert keep==list(range(lo,hi+1))
```
