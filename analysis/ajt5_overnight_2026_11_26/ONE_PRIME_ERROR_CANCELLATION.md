# One-prime errors vanish in the cofactor-band pair expansion

In [the fixed cofactor band](FIXED_COFACTOR_BAND_PAIR_LOWER_BOUND.md), take an actual fixed offset pair \(s\ne t\), and sum over eligible \(a,a'\) with \(\gcd(a,a')=\gcd(aa',s-t)=1\). Write the two prime candidates on \(n=n_0+Maa'k\) as \(L_1(k)=(n_0-s)/a+Ma'k\) and \(L_2(k)=(n_0-t)/a'+Mak\). The variable \(k\) stays in the interval \(X\le n<2X\). Put \(P_i=1_{\{L_i\text{ prime}\}}\), \(z=\lfloor\sqrt{\log\log X}\rfloor\), and \(W=\prod_{\ell\le z}\ell\). Define
\[
u_i(k)=\frac{q_i}{\varphi(q_i)\log L_i(k)}1_{\{\gcd(L_i(k),W)=1\}},\qquad
(q_1,q_2)=(Ma'W,MaW).
\]
Then, uniformly in the actual offsets and for every fixed \(A>0\),
\[
\sum_{a,a'}\sum_k u_2(k)(P_1(k)-u_1(k))=O_A\bigl(X(\log X)^{-A}\bigr),
\]
and the analogous swapped term obeys the same bound.

For the first term, fix \(a\in[B,2B)\) and \(k\bmod W\). The first prime is now in one progression of step \(q_1\). If its base residue is not reduced, both its prime indicator and its model vanish: any prime divisor of \(Ma'\) outside \(W\) cannot divide \(L_1\), by the reduced mod-\(M\) class and the assumed \(\gcd(aa',s-t)=1\); a divisor in \(W\) cannot equal the large \(L_1\). In the reduced case the model sums to the partial summation prime main term \(1/\varphi(q_1)\) times the integral of \(1/\log u\), up to a bounded endpoint discrepancy on subintervals. On the slice, \(u_2\) is zero or is a smooth weight of bounded size and total variation, so the contribution is bounded by a constant times the maximum progression error plus the endpoint discrepancy. For fixed \(a\) and slice, distinct \(a'\) give distinct moduli, all at most \(X^{1/8+o(1)}\), while the prime scale is \(X/B\ge X^{7/8}\). Apply [Bombieri–Vinogradov](https://www.cambridge.org/core/journals/mathematika/article/abs/on-the-large-sieve/4AE92826645F6F3393D30AF0D2767346) in the version taking a maximum over reduced residues and interval endpoints. Summing over the \(O(B)\) first cofactors cancels the \(1/B\) on \(X/B\). The endpoint discrepancies are \(O(X^{1/4+o(1)})\) even after the sums, and \(W=(\log X)^{o(1)}\) and the dyadic partition cost only logarithmic factors. The same proof applies after swapping sides.

After summing over actual offset pairs, the identity
\[
P_1P_2=u_1u_2+u_2(P_1-u_1)+u_1(P_2-u_2)+(P_1-u_1)(P_2-u_2)
\]
therefore reduces the problem to the explicit finite local term \(u_1u_2\) and the centered covariance on the **same** progression. This note does not claim to evaluate the limiting local term or bound the covariance by little-oh. In particular \(aL_1-a'L_2=t-s\), so any affine reparametrization preserving that identity still has proportional linear parts.

## Exact joint-period control

For the same finite original-box example as the previous note, \(L_1=5546605612829+19488k,\ L_2=3339109008497+11424k\), take \(W=2310\). The actual forbidden-root counts at \(2,3,5,7,11\) are \(0,0,1,0,2\), giving 1512 joint viable classes. The merged root at 5 occurs because the two forms come from the same \(n\) with that gap. This is only a local control, not a theorem of joint primality.

```python
ps=(2,3,5,7,11)
a,b=5546605612829,3339109008497
assert 17*19488==29*11424==331296
assert [sum((a+19488*k)%p==0 or (b+11424*k)%p==0 for k in range(p))
        for p in ps]==[0,0,1,0,2]
assert sum(all((a+19488*k)%p and (b+11424*k)%p for p in ps)
           for k in range(2310))==1512
```
