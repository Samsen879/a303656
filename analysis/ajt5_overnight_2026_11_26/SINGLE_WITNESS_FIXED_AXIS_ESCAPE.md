# Fixed-axis escape from a finite obstruction to the growing box

Use the [finite local obstruction test](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md), with modulus depths \(k_p\) and modulus of the double-growth panel \(Q_0\). Consider a class which the whole panel blocks. Let \(A=k_3\) if 3 is in the panel and \(A=0\) otherwise.

Any actual pair of nonnegative exponents with \(c\ge A\) also fails that panel, regardless of \(d\). Indeed the only changes from the double-growth phases are at the two nonunit bases' primes. The 3-power is still zero at depth \(A\), and at 5 every residue is a local norm (\(-1\) is a square and the norm splits). Thus the only possible escapes have fixed \(c=C<A\). No bounded choice of the 5 exponent alone can escape when \(c\ge A\).

A candidate old phase can only be rescued at 3. For it to survive after replacing the 3-power there by \(3^C\), the old residual must have known odd valuation \(t<A\). When \(C>t\) the residual is unchanged in valuation and fails. When \(C<t\) the new valuation is exactly \(C\), so only even \(C\) succeed. When \(C=t\) the leading digit has to cancel and the next valuation must be tested. Hence it suffices to inspect \(0\le C\le 2\lfloor A/2\rfloor-1\), with no candidates when \(A\le1\).

## Exact check after freezing the 3-axis

Use the old common phase period \(R\). After freezing \(c=C\) and restricting \(d=j\bmod R\), use depths
\[
 \widetilde k_2=v_2(R)+2,\qquad
 \widetilde k_p=v_p(R)+v_p(5^{p-1}-1)
       \quad(p\text{ odd inert in the panel}).
\]
The prime 5 needs no test. Use \(Q=\operatorname{lcm}(Q_0,\prod p^{\widetilde k_p})\), with only 2 and the inert tests included in the product as applicable. In each fine class \(n=a\bmod Q\), the test is precisely that \(a-3^C-5^j\) is a finite norm at the respective new depths. At odd inert primes accept a zero class or even valuation, and at 2 accept either the last zero or single-digit residual class, or known odd part \(1\bmod4\). This is sufficient for remaining local conditions: \(5^R\) generates the respective principal-unit balls, so free primary digits give finite exact good valuations simultaneously and CRT permits unbounded actual nonnegative \(d\). It is not sufficient for a norm at all primes. If all these finitely many candidate windows fail their exact local tests on the fine class, the same finite panel rules out *all* nonnegative exponent pairs there.

## Actual positive-proportion hits on a surviving fixed window

Fix a fine class and passing \(C,j\). Average \(r_2(n-3^C-5^d)\) over the \(K\asymp_R\log X\) allowed \(d=j\bmod R\) in \(X^{1/3}\le5^d\le X^{1/2}\); denote this average by \(B_X(n)\). Every such shift has the same prescribed coordinates at the modulus used for the norm tests. If split primes were present in the finer modulus, retain one further fixed period for \(d\) so that the shift is constant there too; this makes no norm restriction. Then the annulus lattice count gives
\[
 X^{-1}\sum_{X<n\le2X,\ n=a\bmod Q} B_X(n)
    =\pi N_Q/Q^2+O_Q(X^{-1/2}),
\]
where \(N_Q>0\) counts the norm coordinates modulo \(Q\).

The unrestricted dyadic second moment is \(O_R(1)\) (with the refined period included in the constant when used). The diagonal is \(O(\log X/K)\), using the elementary bound in the [single-witness limit note](SINGLE_WITNESS_PROFINITE_LIMIT.md). For distinct exponents, Chamizo's uniform two-shift asymptotic applies as before. At each odd \(p\ne5\) the shift difference is zero modulo \(p\) only when the index difference is a multiple of \(\operatorname{ord}_p(5^R)\). The frequency on distinct indices is \(O(1/\operatorname{ord}_p(5^R))\): if the order is at least \(K\) the frequency is zero. Hence the [order-tail bound](AVERAGED_SHIFT_DISCRIMINANT.md) gives a uniform mean of the product in the kernel. Cauchy–Schwarz then gives a positive proportion of genuine hits in this fine class for all sufficiently large dyadic intervals. The diagonal need not be \(o(1)\), so this argument alone does not give a limit law or density one on a fixed window.

The examples \(n=8,49\) show actual rescue of specified phases at 3 and extend to unbounded choices of the 5 exponent in the required size window. The small panel does not block the whole growth box on any class. At \(n=12104\), the first rescued fixed window's panel passes but its only eligible exponent in the finite range gives a nonsquare-sum residual. Finally \(20771\) shows why freezing the 3-axis can increase required depth: base 5 is Wieferich there, base 3 is ordinary.

~~~python
from math import isqrt
def shifts(c,d,m): return (pow(3,c,m)+pow(5,d,m))%m
norms={m:{(x*x+y*y)%m for x in range(m) for y in range(m)} for m in (16,9,7)}
for n in range(1008):
 assert any((n-shifts(c,d,16))%16 in norms[16] and
            (n-pow(5,d,9))%9 in norms[9] and
            (n-shifts(c,d,7))%7 in norms[7]
            for c in range(12) for d in range(12))
for n,c,d,a,b in [(8,0,1,1,1),(49,1,0,3,6)]:
 assert n==3**c+5**d+a*a+b*b and (n-pow(5,d,9))%9==3
 assert all((n-shifts(c,d,m))%m in norms[m] for m in norms)
 for gap in (12,24):
  e=d+gap
  X=3**c+5**e+(a+1008*5**e)**2+b*b-1
  assert (X+1)%1008==n and 5**(2*e)<=X<=5**(3*e)
assert 12104-1-5==2*23*263 and 12104==1+5**3+23**2+107**2
p=20771
assert p%4==3 and all(p%v for v in range(2,isqrt(p)+1))
assert pow(5,p-1,p**2)==1 and pow(5,p-1,p**3)!=1
assert pow(3,p-1,p**2)==347394976
assert (p+2-shifts(0,0,p**2))%p**2==p
print('1008 exact classes, cofinal examples and frozen-depth countercontrol checked')

~~~
