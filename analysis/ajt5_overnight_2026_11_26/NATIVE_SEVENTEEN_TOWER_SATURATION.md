# Saturation of the native 17-tower and failure of two independent extensions

Let \(r\) be admissible if \(25^r-9^r=x^2+3y^2\) for integers \(x,y\). For this native construction every admissible \(r\) is odd, and every admissible \(r\) has \(v_{17}(r)\le2\). In particular the admissible \(r\) supported on \(\{3,17\}\) are exactly \(17^j3^k\) with \(0\le j\le2\) and \(k\ge0\). The factors 7 and 19 both work alone, but neither works together with 17, even after arbitrary extra multipliers. This does not exclude all independent multipliers.

## Primitive obstruction and persistence

For any odd prime \(p\nmid15\) put \(D_p=\operatorname{ord}_p(25/9)\) and \(F_d=\Phi_d(25,9)\) (homogeneous). By LTE/Möbius inversion, the valuation in \(F_{D_p}\) is \(v_p(25^{D_p}-9^{D_p})\); the only further nonzero valuations are one in each \(F_{D_p p^a}\), \(a\ge1\). Indeed the valuation in \(25^m-9^m\) is zero if \(D_p\nmid m\) and otherwise is \(v_p(25^{D_p}-9^{D_p})+v_p(m/D_p)\). This also proves that a nonprimitive odd prime of \(F_d\) must be the largest prime dividing \(d\), because \(D_p\mid p-1\).

Suppose \(p\equiv2\bmod3\), \(D_p\mid r\), and its initial valuation is odd. Admissibility would force \(p\mid r\), since an inert odd prime has even valuation in every nonzero \(x^2+3y^2\). Then \(D_p p\mid r\), and \(F_{D_p p}\) contains \(p\) exactly once. This shell is odd: \(v_2(25^m-9^m)=4+v_2(m)\), so only powers of two (or index 1) carry factors of two in the cyclotomic factorization. Also \(F_{D_p p}\equiv1\bmod3\), by specializing the homogeneous polynomial at \(25\equiv1,9\equiv0\). The shell therefore contains a second inert prime occurring to odd valuation. Since \(p\) is the only possible nonprimitive odd prime in it, that second prime \(p'\) has exact order \(D_pp\) and exceeds \(p\). Admissibility forces \(p'\mid r\) as well. Iterate to get infinitely many increasing primes dividing fixed \(r\), a contradiction. This is the same persistence mechanism as [the native inert forcing chain](https://github.com/Samsen879/a303656/commit/4020a67a75d39843dac87cdb5cd1a5ca693abd43).

The rows below certify the new exact orders and initial valuations. The signed value's other factor cannot vanish at the same odd prime because the prime divides neither 3 nor 5. The \(d=2\) row excludes all even indices; the \(d=4913\) row excludes all multiples of \(17^3\). This leaves precisely the stated \(\{3,17\}\) family by [the \(17^2\) norm and cubing extension](https://github.com/Samsen879/a303656/commit/034aeec734a16e295e9288307ea94a4774da7abb). Native \(d=119,323\) exclude the two proposed mixes, even though their constituent primes are admissible separately.

The admissible restricted family's lower \(5\)-axis exponents are \(2\cdot17^j3^k\). Removing powers of three from \(r\) gives the three phases \(1,289/243,17/9\), with successive multiplicative ratios \(289/243,27/17,27/17\) after closing the cycle. This is a restricted generated-family height statement, not a selector for arbitrary \(n\) or a claim of novelty for the general mechanism.

```python
from math import gcd, isqrt

positive = [
    (7,1,-1,137,80), (7,1,1,74,39),
    (19,1,-1,3038279,318864), (19,1,1,89884,889991),
    (17,1,-1,512959,198560), (17,1,1,225833,121632),
    (17,2,-1,
     114792319219011872638986807213188904428103962881996076399055656581752532318254975178592131870177,
     949000774563177791679267766261510284095096949312078684882906281270969451930408387143300308152),
    (17,2,1,
     114746667825705859742939384182460424698468167451742156138753413107539473812088533428645444702263,
     1704843785569940513994802227007735596776032265007690562713118199648764056324264413790273367768),
]
for q,j,s,x,y in positive:
    assert (5**(q**(j-1)) + s*3**(q**(j-1)))*(x*x+3*y*y) == 5**(q**j)+s*3**(q**j)

for d,p,s,ds in [
    (2,17,1,(2,)), (119,239,-1,(7,17)), (2023,8093,-1,(7,17)),
    (323,647,1,(17,19)), (4913,135372803,1,(17,)),
]:
    assert p%3 == 2 and all(p%i for i in range(2,isqrt(p)+1))
    z = 25*pow(9,-1,p)%p
    assert pow(z,d,p) == 1 and all(pow(z,d//i,p) != 1 for i in ds)
    a = (pow(5,d,p*p) + s*pow(3,d,p*p))%(p*p)
    assert a and a%p == 0

H = (5**4913 + 3**4913)//(5**289 + 3**289)
assert gcd(pow(2,2*4913*23*599,H)-1,H) == 135372803
```
