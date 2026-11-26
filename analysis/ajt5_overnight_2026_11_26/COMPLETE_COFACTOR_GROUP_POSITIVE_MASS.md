# Complete legal cofactor grouping still leaves positive tail mass on one factor spectrum

Use the fixed-\(y\) separated shift grid and cofactor band from [the preceding signed-tail result](COFACTOR_MOVE_SIGN_AND_POSITIVE_GROUP.md). Write an actual residual as \(r=Bp_1p_2b\), with squarefree split factors, and put \(P=p_1p_2,\ m=Pb,\ R=X^{1/4}\). Suppose \(p_1,p_2,b>X^{1/8}\), \(b>R\), \(P>R\), and the legal cofactors are the divisors \(a\mid B\) in the band, including \(B\) and \(B/\ell\) for each prime \(\ell\mid B\). Also require \(cp_i<R\) for every such cofactor, \(c=B/a\).

For candidate \(L=cm\), the low divisors are exactly \(d,dp_1,dp_2\) for \(d\mid c\). They give \(\Lambda_R(L)=1_{c=1}\log(P/R)-\Lambda(c)\), using \(\sum_{d\mid c}\mu(d)\log d=-\Lambda(c)\). Since all these candidates are composite, the exact normalized signed sum over **all** legal cofactors is
\[
 S(r)=-\frac{\log(P/R)}{\log m}+
             \sum_{\ell\mid B}\frac{\log\ell}{\log(\ell m)}
 \ \le -\frac{\log(P/(BR))}{\log m}.
\]
Only choices \(c=1\) and \(c\) prime contribute. Under the small-prime panel restriction, \(c=1\) is still allowed when \(m\) is coprime to the panel; excluded prime \(c\)'s only remove nonnegative terms. For two coprime residuals on the same \(n\), all pairs of cofactors satisfy the original mutual and gap coprimality conditions. Their paired sum is the product of the two one-side sums. If \(P/(BR)\ge X^\epsilon\) on both sides, this is bounded below by a positive constant.

One main-scale factor spectrum is
\[
 B=A_0\prod_{i=1}^4u_i\prod_{j=1}^2q_j,
\]
where \(A_0\le X^{1/256}\) is a squarefree split-supported product of primes in \((y,X^\xi]\) for fixed small \(\xi>0\); \(u_i,q_j,p_i\) are split primes respectively in exponent bands \([1/60,1/58]\), \([1/48,1/44]\), \([3/16,19/100]\), distinct and ordered within each band. These ranges give \(X^{13/120}\le B\le X^{9663/81664}<X^{1/8}\); each \(B/\ell\ge X^{1/16}\) for sufficiently small \(\xi\). The inequality \(9663/81664-1/16+19/100<1/4\) ensures the low-divisor conditions, and \(9663/81664+38/100<1/2\) leaves a unique last prime \(b>\sqrt{2X}\) throughout a length-\(X\) residual interval. Also \(P/(BR)>X^{1/200}\).

For fixed large \(y\), the same weighted Mertens argument gives \(A_0\) reciprocal mass \(\gg\sqrt{\log X/\log(3y)}\), and each disjoint named prime band gives constant reciprocal mass. Fixed-modulus PNT counts \(b\) in the reduced progression for each actual shift, with the factorization uniquely decodable. Cauchy–Schwarz over \(n\), removing the diagonal and subtracting the [same-gap common-prime error](COPRIME_LARGE_PRIME_PAIR_MASS.md), leaves \(\gg XK_X^2/(\log X\log(3y))\) genuine coprime pairs. Thus grouping all legal cofactors on this one factor spectrum cannot be an absolute error. The signed sum over other spectra may still compensate; the full correlation is not evaluated.

## Exact factorized original-box control

The example uses the ordinary active box at the displayed \(n\), rather than the narrower asymptotic grid. For the two large \(b\)'s, the code verifies the size and modular conditions of Pocklington's criterion alongside trial-division proofs for the known factors of \(b-1\). Both complete feasible cofactor sets are enumerated.

```python
from math import gcd,isqrt,prod
def prime(n):
    return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
n=16451439060685934546204690619841313884086963887
R=358138469455
assert n%672==527 and R**4<=n<(R+1)**4
pairs=[
 (n-3**26-25,(17,61,89),(186300601,186304081),5135686510165284729456001,
  (5441,482642474219),[1037,1513,5429,92293]),
 (n-34,(29,37,53),(146241149,146241397),13526591786484733860972329,
  (1252661,12464416451),[1073,1537,1961,56869])]
for r,Bf,Pf,b,F,expected in pairs:
    B,P=prod(Bf),prod(Pf)
    assert all(prime(p) and p%4==1 for p in Bf+Pf)
    assert (b-1)%prod(F)==0 and prod(F)**2>b and all(prime(f) for f in F)
    assert pow(2,b-1,b)==1 and all(gcd(pow(2,(b-1)//f,b)-1,b)==1 for f in F)
    assert b%4==1 and r==B*P*b and P**4>B**4*n
    allowed=[a for a in range(1,B+1) if B%a==0 and a**16>=n and a**8<=n]
    assert allowed==expected and all(B//a*max(Pf)<R for a in allowed)
assert gcd(pairs[0][0],pairs[1][0])==1
```
