# Thin-order closure rules out all-exponent blocking on a panel

Apply the [base-5 order-path rule](ALL_EXPONENT_BASE5_ORDER_PATHS.md) to a finite panel. Suppose every inert base-5 Wieferich row and all its inert source successors can choose edges \(p\to r\), with \(r>2\) prime dividing \(o_p=\operatorname{ord}_p(5)\), such that \(o_p/r\le3\), except for edges in the three specified paths
\[
20771\to67\to11\to5,\quad40487\to653,\quad
1645333507\to30469139\to1429.
\]
Then for every \(n\) the panel has a fixed-axis phase at the small \(c=C_*(n)\) from the order-path rule. Such a panel is not an all-exponent certificate.

Choose the parity to pass 2 and avoid the root at 3; this leaves its odd-primary coordinate free. Routes descend, ending at that prime or a split prime. At each destination the sum of forbidden-ball measures must be \(<1\), since that permits simultaneous CRT selection on the free digits. All protected inert rows have unit residuals, and all other ordinary rows can be repaired in ascending order on their unread own digits.

For \(r>3\), thin incoming orders can only be \(r,2r,3r\). Distinct source primes divide the product
\[
 B_r=\Phi_r(5)\Phi_{2r}(5)\Phi_{3r}(5)
     =\frac{(5^{2r}-1)(5^{2r}+5^r+1)}{24\cdot31}<5^{4r}.
\]
An inert source is \(1\bmod r\) and \(3\bmod4\), so \(k\) such sources have product at least \(\prod_{j=1}^k((4j-2)r+1)\ge (4rk/e)^k\), by integrating \(\log(4rx)\) below its midpoint sum. For \(r\ge23\), \(k=r\) would exceed \(B_r\) since \(4r^2/e>625\); for \(r\ge67\) even \(k=r-1\) exceeds \(B_r\), using \(4r(r-1)/3>1250\) and \(625^{r/(r-1)}<1250\). Each edge costs at most \(1/r\); thus at \(r\ge67\) one extra prescribed edge still fits. All nonthin edges in the three listed paths end at distinct primes at least 67. For \(r=11,13,17,19\), the finite lower product of the first \(r\) **prime** candidates is greater than \(B_r\), verified in the replay. At 5 and 7 there are at most two and three thin edges respectively, checked by factoring \(B_r\). At 3 the only inert sources with the permitted orders \(3,6,9\) are \(31,7,19\), with combined weight \(1/3+1/3+1/9\).

For an arbitrary fixed cofactor bound \(M\) and at most \(E\) nonthin extras per destination, the same method leaves just finitely many capacity checks. Put \(S=\sum_{m\le M}\varphi(m)\). For \(r>\max(M,2E+3,6^{2S})\) the product of relevant cyclotomic values is at most \(6^{(r-1)S}\) (bound each factor by distance from a unit root); \(k=r-E\ge r/2\) thin incoming primes would give \((4rk/e)^k\ge r^{r/2}>6^{rS}\). At the remaining finitely many destinations, compare actual order candidates dividing the corresponding cyclotomic factors. This does not show that every finite exceptional panel has a bounded-thin routing with the necessary small-destination capacity.

The final test repeats the released phase for the same actual integer as in [the shallow-pin chain](FIXED_AXIS_SHALLOW_PINNING_CHAIN.md). The displayed long \(d\) is a local phase and the true representation uses \(c=2,d=0\).

~~~python
from math import prod,isqrt
def prime(p):
    return p>1 and all(p%i for i in range(2,isqrt(p)+1))
def B(r):
    x=5**r
    return (x*x-1)*(x*x+x+1)//744
for r,P,want in [(5,(11,71,181,521,1741),2),
                  (7,(29,379,449,19531,519499),3)]:
    assert all(prime(p) for p in P) and prod(P)==B(r)
    assert sum(p%4==3 for p in P)==want
for r in (11,13,17,19):
    P=[]; j=1
    while len(P)<r:
        p=(4*j-2)*r+1
        if prime(p): P.append(p)
        j+=1
    assert prod(P)>B(r)
assert 5**18-1==24*31*3*7*19*829*3*5167
# The exponent-18 factor 5167 has exact order 18 and is not an order-9 source.
assert pow(5,9,5167)!=1
N,d=301491668318363121843280379,93097841
assert [d%p for p in (5,11,67)]==[1,1,1]
for m,want in ((4,1),(3,2),(11,7),(67,38),(31**3,31**2),(20771,2622)):
    assert (N-1-pow(5,d,m))%m==want
assert (N-pow(5,d,27))%27==18
assert N==10+53636783280**2+17363432593063**2
~~~
