# Ordinary-window antichains and common-sum obstructions

In the checked P2 model, write A=3^a, B=5^b, d=2(A+75B), e=20A+25B. After fixing rounded depths, a short factor is v=v0 times a subset product of k ambiguous primes. Feasible subsets in the ordinary interval (4 sqrt(A), (21/2)sqrt(A)) form an antichain, because proper inclusion changes the product by at least 7. If at most r primes can be selected by size, the LYM inequality bounds this by binomial(k,min(r,floor(k/2))). The same reasoning applies to z in its narrower interval.

Under the pinned H assumption, the baseline v0/H already contains each ambiguous prime; a selected set of size m contributes each chosen prime a second time. Consequently k! m! < (21/2)sqrt(A)/H. If H is of order A^mu, Stirling and binomial(k,m)<=phi^(k+m), phi=(1+sqrt(5))/2, give the cap exp(((1/2−mu)log(phi)+o(1)) log(A)/loglog(A)) for ordinary d-assignments. This uses the size-limited antichain, not independence of prime allocations.

For even a,b, gcd(d,e)=1: the only possible common prime outside 2,3,5 is 59, but A/B=-16 modulo 59 is impossible for squares. Let G_e be the gcd of the possible gcd(z,e/z) over the rounded e-allocations. Every common edge sum is divisible by G_e, so v²+d=0 modulo G_e. As v0 is a unit modulo G_e, (v/v0)² belongs to one residue class. Its interval has length 377A/(4v0²), giving at most ceil(377A/(4v0²G_e)) possibilities. In the short branch each sum fixes at most one z.

For the actual modular phase replay, the exact depth-three split at 331 on d would make the common sum zero modulo 331, but then the e-remainder is 100*59*B, a nonsquare. The exact depth-three split at 126736826507 on e instead excludes the fourth label by its nonsquare test. These are obstructions to allocating the named primes on both sides, not actual multi-assignable collisions inside both ordinary windows. Even a surviving edge match must be completed by a square n−K for prescribed n. No global density or source bound changes.

```python
from math import isqrt, lcm

g, N, P = 468741, 623894271, 23894400218362914240
p, q, p0 = 331, 126736826507, 10485619
assert all(all(r % i for i in range(2, isqrt(r)+1)) for r in (p,q))
h = 15988466940877055464693432539214677187145141377654439147300423991157063451
k = 19848674835359031706
T = lcm(P, p0*(p0-1), (q-1)*q**3)
assert pow(3,N*T,p*p) == 1+55*p
h += 11504622*T
period = T*p**3                 # Keep h,k in these classes modulo period.
assert period % ((p-1)*p**3) == period % ((q-1)*q**3) == 0
a,b = N*h+1,N*k-2

A,B = pow(3,a,p**4),pow(5,b,p**4)
assert 2*(A+75*B)%p**4 == 64*p**3
assert 6*(pow(3,11*g*h,p**4)+pow(5,11*g*k,p**4))%p**4 == 6*p**3
assert min(242*g,2662*g,2662*3939,2662*1717) > p-1
assert (pow(-3,165,p),pow(-5,165,p),pow(59,165,p)) == (1,p-1,p-1)

A,B = pow(3,a,q**4),pow(5,b,q**4)
assert (20*A+25*B)%q**4 == 40579912650*q**3
assert pow(-4*(2*A+150*B),(q-1)//2,q) == 1
assert pow(-4*(182*A-6*B),(q-1)//2,q) == q-1

assert a%2==b%2==0
assert pow(-16,29,59)==58
# Independent numerical length of the squared-factor interval.
from fractions import Fraction
assert Fraction(21,2)**2-4**2==Fraction(377,4)
print("Independent parity, edge-coprimality constant, and interval width checks passed")
```
