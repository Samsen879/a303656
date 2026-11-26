# A true shallow-pin chain and bounded-cofactor capacity

In the [fixed-axis shell model](FIXED_AXIS_SHELL_HALL_TRANSPORT.md), a source with odd initial lifting depth can force its first exponent digit on a colliding branch. Several such forced digits can cascade even when the intermediate inert coordinates were not frozen at the start. This is real for bases 3 and 5, but does not by itself obstruct the unrestricted problem.

For \(o_p=\operatorname{ord}_p(5)\), the exponent \(w_p=v_p(5^{o_p}-1)\) is exactly the exponent of \(p\) in the cyclotomic value \(\Phi_{o_p}(5)\), since none of the proper divisor powers in the cyclotomic product is 1 modulo \(p\). A hard row therefore contributes at least \(p^2\). When a coordinate is pinned to one first digit by its **own repair shell**, the initial depth is odd; a Wieferich coordinate pinned that way contributes at least \(p^3\).

For a fixed odd source \(r>3\), take all shallow readers of order \(o_p=rm\) with \(m\le M\) and \((m,r)=1\). Since \(p\equiv1\bmod r\) is odd it is at least \(2r+1\). If there are \(h\) hard and \(b\) other rows, their product contribution gives
\[
 (2r+1)^{2h+b}\le
 \prod_{\substack{m\le M\\(m,r)=1}}\Phi_{rm}(5).
\]
The usual cyclotomic product gives
\(\log\Phi_s(5)\le\varphi(s)\log5+5/16\), using
\(\sum_{d\ge1}|\log(1-5^{-d})|\le(5/4)\sum_{d\ge1}5^{-d}=5/16\).
Thus for fixed \(M\) the joint incoming budget is \(O_M(r/\log r)\). In particular, a *free* sufficiently large coordinate has spare first digits in such a bounded-cofactor system. If hard readers alone require \(r\) possible first digits, the range of their cofactor \(M\) must be \(\Omega(\sqrt{\log r})\), by \(\sum_{m\le M}\varphi(m)\ll M^2\). This is not enough to free an already pinned coordinate, where a single aligned shallow reader may block. Strictly descending order paths only bound chain length in terms of the starting prime, not uniformly.

## Same integer: a frozen chain, a released chain, and an actual representation

The replay below constructs a concrete countercontrol. Fix \(c=0\) at the unit primes, choose odd \(d\), and use normalized \(n-5^d\) at 3. All seven normalized 3-classes require \(d=5\bmod6\). If the split coordinate is frozen at \(d=0\bmod5\), the row at 11 collides, forcing \(d=5\bmod11\) so that it can lift to an even norm. That combines with the parity to collide at 67, forcing \(d=5\bmod67\). Independently the normalized 3-condition triggers 31, forcing \(d=5\bmod31\). The three local force steps follow from the shown exact values modulo the cubes: changing the first digit would give odd valuation one. Then at 20771 the locked order residue is \(d=5\bmod(5\cdot31\cdot67)\) and gives valuation one at this base-5 Wieferich row. Base 3 is ordinary there, so it is not an example of a common terminal.

Releasing just the split coordinate at 5 lets each of the seven classes pass, on shared non-3 coordinates, by changing \(d\) to 1 at 5 as checked below. Independently, every active exponent \(0\le d\le37\) at \(c=0\) is genuinely excluded at this integer: the given coprime divisor block \(u=3\bmod4\) ensures a prime \(3\bmod4\) occurs to odd exponent. Yet the displayed true witness has \(c=2,d=0\). This separates a frozen local failure, an actual finite-window failure, and the unrestricted claim.

~~~python
from math import gcd

N = 301491668318363121843280379
q = 20771
assert N == 10 + 53636783280**2 + 17363432593063**2
assert N % 972 == 11 and 5**37 < N-1 < 5**38
for r, o in ((11,5), (31,3), (67,22)):
    assert pow(5,o,r) == 1 and pow(5,o,r*r) != 1
    assert (N-1-pow(5,5,r**3)) % r**3 == r*r
assert pow(5,5*31*67,q*q) == 1
assert (N-1-pow(5,5,q*q)) % (q*q) == q

U = (11,43,3,7,3,20771,169858687,503,3,7,3,31,19,433859,3,11,3,31,
     1476199,23,3,7,3,31,707828591,11,3,7,3,31,11,21499,3,7,3,11,859,131)
for d, u in enumerate(U):
    R = N-1-5**d
    assert u % 4 == 3 and R % u == 0 and gcd(u,R//u) == 1

from math import prod
m=[2,81,5,11**2,31**2,67**2]
M=prod(m)
def crt(vals):
    return sum(v*(M//p)*pow(M//p,-1,p) for p,v in zip(m,vals))%M
seen=set()
for x in range(81):
    d=crt((1,x,1,5,5,5))
    a=(N-pow(5,d,243))%243
    if not (a in (81,162) or a%9==0 and a%27!=0): continue
    seen.add(x%27)
    assert d%6==5
    assert (N-1-pow(5,d,11))%11
    assert all((N-1-pow(5,d,r**3))%r**3==r*r for r in (31,67))
    assert (N-1-pow(5,d,q))%q
assert len(seen)==7

~~~
