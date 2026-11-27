# The original exceptional set has a natural density

Let \(\mathcal E\) be the integers \(n>1\) with no representation \(n=a^2+b^2+3^c+5^d\) with nonnegative exponents. Let \(\mathcal B_{\rm all}\subset\widehat{\mathbb Z}\) be the set of \(n\) for which some finite modulus certifies that **every** nonnegative exponent pair \(c,d\) has residual \(n-3^c-5^d\) outside the square-sum residues. Then
\[
 d(\mathcal E)=\mu_{\rm Haar}(\mathcal B_{\rm all}).
\]
In particular the representable integers have density one if and only if there is no such congruence obstruction, because \(\mathcal B_{\rm all}\) is a union of open residue classes. This does not decide whether any obstruction exists. It also does not exclude a zero-density exceptional set in the absence of such obstructions.

## Exact finite obstruction law for a fixed axis

Fix \(C\ge0\) and \(d=j+Lu,\ 0\le j<L\) as in the [truncated single-axis count](SINGLE_WITNESS_FIXED_AXIS_TRUNCATION.md). There \(w_X>0\) exactly at an actual square-sum hit, its diagonal is \(o(1)\), and its normalized average \(Z_X\) has finite-center mixed moments and converges by iterated \(L^2\) approximation to the profinite \(F\).

At odd \(p\ne5\), \(o_p=\operatorname{ord}_p(5^L)\), and the exact order at depth \(a\) is
\[
 o_p p^{\max(0,a-v_p(L)-v_p(5^{p-1}-1))}.
\]
At 2 it is \(2^{\max(0,a-2-v_2(L))}\). At 3 the frozen term is the actual \(3^C\); at 5 the growing 5-power vanishes at each fixed depth, but this prime is split and never vetoes. For a finite panel take \(R\) the lcm of the unit orders modulo its primes. On fixing \(u\bmod R\), at each \(p\ne5\) the shift is constant modulo \(p^{k_p}\), \(k_p=v_p(5^{LR}-1)\), and remaining \(p\)-primary moves fill its whole shifted ball. Those moves are independent for the entire finite panel. So a phase passes precisely when the balls contain local norms, each on a positive-measure subcylinder: inert primes require an even valuation below depth or the zero class; 2 requires odd part \(1\bmod4\) when determined, or a potentially acceptable lift if not. No phase passing gives a finite congruence certificate. This excludes all actual \(u\ge0\), including exponents below the growth window, because the only nonunit term of that window is at the split prime 5.

For completeness the conditional argument from the [two-axis finite-obstruction law](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md) applies to this one-axis center as follows. With complete head observations at \(p\le z\), put \(H_z=\mathbb E(F\mid n_{p\le z})\). On \(H_z>0\), the head densities reweight only \(z\)-smooth primary coordinates of the phase \(u\), by the exact orders above. In a tail panel prime \(q>z\), condition on the smooth components of two phases, and the first full phase; the second phase still has an independent Haar part on larger primary coordinates. Its collision probability at \(q\) is at most \((\operatorname{ord}_q(5^L))_{>z}^{-1}\). Once \(z\) exceeds the prime factors of \(L\), this nonsmooth part equals that of \(\operatorname{ord}_q(5)\). Consequently the same small-order and large-smooth-part exceptions and Jensen estimate from the two-axis proof give the uniform conditional bound \(\mathbb E(F^2\mid n_{p\le z})\le D H_z^2\). There is no need for independence of collision indicators across tail primes. The conditional chance \(F>0\) is at least \(1/D\) whenever \(H_z>0\). Its martingale limit is the indicator of \(F>0\), so \(F=0\) agrees almost surely with the union of finite head blockers.

The upper dyadic limit of the fixed-window miss rate comes from \(L^2\) approximation and weak convergence; the reverse lower limit from the congruence certificates themselves. Both hold after restriction to any fixed residue class. For finitely many windows, including the two-growth-axis box, their joint miss rate tends to the measure of the intersection of the blockers. To see this without any cross-window correlation formula, approximate each blocker from below by its finite heads. The joint miss rate above the common certified classes is bounded by a sum of individual miss rates above their certified classes. Each difference tends to zero as its head increases. The opposite bound is immediate from the common certified classes.

## Closing the unbounded exponent ranges

Let \(\mathcal B_{\rm box}\) be the two-growth-axis blocker and \(\mathcal B_C\) the step-one blocker for fixed \(c=C\) (so all \(d\ge0\) are allowed in the certificate). Then exactly
\[
 \mathcal B_{\rm all}=\mathcal B_{\rm box}\cap\bigcap_{C\ge0}\mathcal B_C.
\]
An all-exponent obstruction restricts to every window, since all eventual phases at any fixed modulus are limits of actual growing exponents. Conversely choose one finite box certificate on the right. If its 3-depth is \(A\) (zero if absent), it already certifies absence for all actual \(c\ge A\), at *every* \(d\ge0\), by [fixed-axis escape](SINGLE_WITNESS_FIXED_AXIS_ESCAPE.md). Take one fixed-axis certificate for each \(C<A\). The lcm of these finitely many moduli with the box certificate gives a single all-exponent obstruction.

Now for each fixed \(T\), \(\mathcal E\) misses the growing box and all the windows \(C=0,\dots,T\), so the joint miss law bounds its upper dyadic density by the measure of their blocker intersection. Let \(T\to\infty\) by continuity from above. The reverse lower bound follows from taking finite unions of all-exponent certifying classes. Thus the dyadic density exists and equals \(\mu(\mathcal B_{\rm all})\); decomposing \([1,X]\) dyadically gives the same natural density. No window grows in number inside an analytic limit.

## A small joint-window replay (not an all-exponent obstruction)

Two particular step-84 windows separately block six of seven refinements of one CRT class, but their common blocker at this panel has measure \(5/7\) within the class. Although both windows miss 440, a third exponent represents it. The full-unrestricted claim above uses step-one fixed-axis windows, not selected progression slices.

~~~python
from math import gcd
M,Q=1008,7056
C=0; L=84
def normsets(*mods):
 return {m:{(x*x+y*y)%m for x in range(m) for y in range(m)} for m in mods}
tests=normsets(16,9,49)
classes=[440+M*u for u in range(7)]
good=[]
for j in (1,13):
 assert pow(5,L,Q)==1
 good.append({n for n in classes if all((n-1-pow(5,j,m))%m in R for m,R in tests.items())})
assert good==[{2456},{3464}]
assert len(set(classes)-set.union(*good))==5
assert (1+5+35**2+35**2)%Q==2456
assert (1+5**13+35**2+35**2)%Q==3464
assert 440==1+5**3+5**2+17**2 and 440 not in set.union(*good)

def order(a,m):
 assert gcd(a,m)==1
 t=a%m;k=1
 while t!=1:t=t*a%m;k+=1
 return k
# 7 divides L: the order stays 1 through depth two and then lifts.
assert [order(5**84,7**k) for k in (1,2,3,4)]==[1,1,7,49]
assert [order(5**84,2**k) for k in (4,5,6)]==[1,2,4]

~~~
