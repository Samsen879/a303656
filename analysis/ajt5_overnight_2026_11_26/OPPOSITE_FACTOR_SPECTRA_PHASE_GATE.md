# Neighboring factor spectra can have opposite grouped signs, with an exact phase gate

Use [the complete cofactor grouping formula](COMPLETE_COFACTOR_GROUP_POSITIVE_MASS.md) with the same separated shifts, cofactor band and \(B\)-factor spectrum. Write \(r=Bp_1p_2b,\ P=p_1p_2,\ m=Pb,\ R=X^{1/4}\). Label the former choice \(p_i\in[X^{3/16},X^{19/100}]\) the minus spectrum. In the plus spectrum take \(p_i\in[X^{11/64},X^{45/256}]\) instead. Both permit the same complete legal grouping, with \(cp_i<R\) for \(c=B/a\), and \(R<P\). The resulting weighted sum on one side, after requiring coprimality with a growing small-prime panel \(W\), is
\[
 S(r)=-\frac{\log(P/R)}{\log m}+
   \sum_{\ell\mid B,\ \ell\ {\rm prime},\ \ell\nmid W}
           \frac{\log\ell}{\log(\ell m)} .
\]
In the plus spectrum let \(u=1-9663/81664\). From \(r\ge X\) one has \(\log m\ge u\log X\); each \(\ell\mid B\) is at most \(X^{1/44}\), and \(\log B\ge(13/120)\log X\). Since \(\log(P/R)\le(13/128)\log X\),
\[
 (\log m)S(r)\ge \frac{u}{u+1/44}\bigl((13/120)\log X-\log W\bigr)
                   -(13/128)\log X .
\]
The positive coefficient of \(\log X\) exceeds \(1/250\), hence \(S(r)\gg1\) for \(\log W=o(\log X)\). In the minus spectrum the earlier upper bound gives \(S(r)\ll-1\). Both scales are for fixed \(y\) as in the earlier construction.

The actual shifted values are restricted: for \(c,d\equiv2\bmod24\), each shift is \(34\bmod65\). Therefore on one actual \(n\), the two residuals cannot have different mod-65 tags. A tag such as 1 on the plus side and 2 on the minus side forbids **all** pairs, although both separately retain main-scale true witnesses and same-spectrum pairs: use exactly the earlier fixed-modulus PNT and common-prime subtraction with the additional reduced target class modulo 65. The number of allowed shift labels and all coprimality conditions remain of the stated scale. This exact obstruction emphasizes why two separate second-moment lower bounds cannot be multiplied. A common tag gives no implication of a mixed growth lower bound.

## An exact common-tag negative pair

At \(n=17082583399785026743694594367904998214738016015\), use original-box labels \((26,2),(2,2)\). The cofactor factors of \(B\), the medium primes, and the large prime are:
- \(17,61,89;\ 7511837,7512893;\ 3279679668159310047597252097\);
- \(29,37,53;\ 146242541,146243693;\ 14045172846521515346379073\).

Both residuals are coprime squarefree norms, with common mod-65 tag 1. All candidate \(L\)'s in both complete cofactor groups are composite. With \(R=\lfloor n^{1/4}\rfloor=361525043815\), the first complete coefficient is positive and the second negative. This checks the finite sign mechanism, not membership of both finite rows in the asymptotic narrow spectra.

```python
from math import gcd,isqrt,prod
def prime(x):
    return x>=2 and all(x%k for k in range(2,isqrt(x)+1))
n=17082583399785026743694594367904998214738016015
R=361525043815
assert R**4<=n<(R+1)**4 and n%672==527
rows=[
 (n-3**26-25,(17,61,89),(7511837,7512893),3279679668159310047597252097,
  (3313,4766726264933)),
 (n-34,(29,37,53),(146242541,146243693),14045172846521515346379073,
  (265921,795865451))]
for r,F,G,b,C in rows:
    B,P=prod(F),prod(G)
    assert r==B*P*b and r%65==1 and b%4==1 and b>R
    assert all(prime(p) and p%4==1 for p in F+G)
    assert all(prime(p) for p in C) and (b-1)%prod(C)==0 and prod(C)**2>b
    assert pow(2,b-1,b)==1 and all(gcd(pow(2,(b-1)//p,b)-1,b)==1 for p in C)
    aa=[a for a in range(1,B+1) if B%a==0 and a**16>=n and a**8<=n]
    assert aa==sorted([B]+[B//p for p in F])
    assert all(B//a*max(G)<R for a in aa) and P>R
r,F,G,b,_=rows[0]
B,P=prod(F),prod(G)
assert P*b>=max(F)**9 and B**9*R**10>P**10  # rigorous lower bound for positive sum
r,F,G,b,_=rows[1]
assert prod(G)>prod(F)*R                         # rigorous upper bound for negative sum
assert gcd(rows[0][0],rows[1][0])==1
```
