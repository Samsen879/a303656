# An all-prime criterion for dense multiplicative seed phases

**The known \(7\)- and \(17\)-multiplier seeds cannot generate dense phases by multiplicative closure.** Both are genuine seeds for \(25-9=4^2\). But inert primes veto their mixed product and higher powers. More generally, there is an exact criterion for when a fixed seed can generate dense phases by multiplication. The criterion leaves density of the unrestricted seed set open.

### Exact obstruction to multiplicative closure

Take a moving seed \(A=5^m,\ B=3^e\) with \(A-B=a^2+3b^2>0\). Both \(m,e\) are even, by reduction modulo \(3\) and \(8\). For an odd prime \(q\equiv2\pmod3\), \(q\ne5\), set
\[
o_q=\operatorname{ord}_q(A/B),\qquad b_q=v_q(A^{o_q}-B^{o_q}).
\]
For every multiplier \(k\), LTE gives the exact rule
\[
v_q(A^k-B^k)=
\begin{cases}
0,&o_q\nmid k,\\
b_q+v_q(k),&o_q\mid k.
\end{cases}
\]
At \(2\), the valuation is \(v_2(A-B)+v_2(k)\). The integral norm test is even valuation at every prime \(q\equiv2\pmod3\), including \(2\). Sufficiency follows from Eisenstein factorization: after removing an even power of \(2\), a unit makes an odd-norm Eisenstein integer congruent to \(1\bmod2\), placing it in \(\mathbb Z[\sqrt{-3}]\).

Suppose a multiplicatively closed set of valid multipliers contains a multiple of a prime \(\ell\ne3\). Then **every inert \(q\) whose order is an \(\ell\)-power must have \(b_q\) even**. Otherwise a sufficiently large even power of that multiplier activates \(q\) and contributes an even \(v_q(k)\), leaving the valuation odd. Thus adjoining repair primes cannot save a generator inside a closed family.

Conversely, if a prime \(\ell\ne3\) meets that test, every \(3^a\ell^{2b}\) is valid. The inert-prime orders are coprime to \(3\), and the multiplier contributes only even valuations. Since \(\log_3\ell\) is irrational, the phases are dense. This gives an **if and only if** for a dense multiplicatively closed family at a fixed seed slope.

There is a universal obstruction at \(\ell=2\). For every moving seed, \((A+B)/2\) is odd and \(2\bmod3\). It therefore has an odd inert prime divisor to odd exponent. That prime has order \(2\) and odd \(b_q\).

### Actual \(3,5\) controls

For \(A=25,\ B=9\), the admitted multipliers \(7\) and \(17\) have witnesses \((77992,2308)\) and \((758993440348,44742038272)\). The following exact gates apply.

| Inert prime \(q\) | Exact order \(o_q\) | \((25^{o_q}-9^{o_q})/q\bmod q\) |
|---:|---:|---:|
| \(197\) | \(7^2\) | \(7\) |
| \(239\) | \(7\cdot17\) | \(185\) |
| \(135372803\) | \(17^3\) | \(32118877\) |

Thus within the actual multipliers \(3^a7^b17^c\), the only possible non-\(3\) parts are \(1,7,17,289\). The first three are valid. The obstruction does not require deciding \(289\). Even allowing it leaves a phase gap, so this particular multiplicative route cannot approach uniform exponent \(1/2\).

### What the obstruction does and does not cover

There is also an algebraic obstruction to a **universal rational powering identity**, even when the original norm coordinates are available. Let \(X=Y+x^2+3y^2\) with independent \(x,y,Y\), and put \(z=X/Y\). The rational function fields in \((x,y,Y)\) and \((x,y,z)\) agree, since \(Y=(x^2+3y^2)/(z-1)\). If \(k\) has a prime divisor \(\ell\ne3\), then \(\Phi_\ell(z)\) occurs to exponent one in \(X^k-Y^k\), and \(Y\) is a unit there. This factor stays irreducible over \(\mathbb Q(\sqrt{-3},x,y)\), since \(\mathbb Q(\zeta_3,\zeta_\ell)=\mathbb Q(\zeta_{3\ell})\). Conjugation fixes the corresponding valuation, which must therefore be even in any rational norm. Cubing gives the converse for powers of \(3\).

A finite inert panel cannot settle the unrestricted density question. For \(25,9\), take \(L\) even and divisible by every \(q-1\) on the panel, and set \(h=1+3L\). All \(3^a h^b\) pass that panel: at each odd inert \(q\ne5\) the order is greater than one, coprime to \(3\), and the multiplier is \(3^a\bmod(q-1)\). At \(2\) the valuation remains \(4\), and \(5\) never divides the difference. These panel-surviving phases are already dense. The missing step is the simultaneous test at *all* inert primes.

If a prime passed the exact all-orders criterion, a finite set of its phases would give height ratios arbitrarily close to one. The existing sphere argument would then give \(\gg_\epsilon X^{1/2-\epsilon}\) constructed targets up to \(X\) in **both** odd classes. The unconditional five-seed uniform bound remains \(13/34\), and the per-height exponent remains \(1/2\).

```python
from math import isqrt

for k,a,b in ((1,4,0), (7,77992,2308), (17,758993440348,44742038272)):
    assert 25**k-9**k == a*a+3*b*b

for q,o,divs,u in (
    (17,2,(2,),15),
    (197,49,(7,),7),
    (239,119,(7,17),185),
    (135372803,4913,(17,),32118877),
):
    assert q%3 == 2 and all(q%d for d in range(2,isqrt(q)+1))
    assert pow(25,o,q) == pow(9,o,q)
    assert all(pow(25,o//d,q) != pow(9,o//d,q) for d in divs)
    assert (pow(25,o,q*q)-pow(9,o,q*q)) % (q*q) == u*q

# Same moving powers, one true target in each odd class.
Q,W,t,v,u = 5**18,3**18,1536256,2859544,3**9
assert v*v+3*t*t == 4*(Q-W)
for lam,x,y in ((1,t-u,t),(3,t+u,t-2*u)):
    r,S,P,A = t+u,x*x+y*y,lam*W,(4-lam)*W
    n = 5*Q+P-S
    assert Q<n<5*Q and n%4 == lam and (n-5*Q)%3
    assert 2*P-S == r*r-3*t*t and n == Q+A+v*v+r*r
```

Independent BigInt replay checked the small witnesses, exact orders, valuation-one gates including the 135372803 prime, and the two real positive representations. The all-orders criterion does not assert the existence of a prime satisfying it; finite-panel examples give no such evidence by themselves.
