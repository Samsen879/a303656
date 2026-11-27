# Capacity matching with ordinary-prime repair shells

This strengthens the [mixed-order fixed-axis cut](FIXED_AXIS_MIXED_ORDER_CUT.md), in the problem of sharing non-3 exponent coordinates across several allowed 3-primary classes at the same \(n\). Choose an admissible 3-prefix per desired class, refined to all the 3-digits read by the panel. Fix the parity and fixed \(c=C_*(n)\). Include as avoidance tasks the hard collision rows active on any chosen prefix, and any repairable rows we voluntarily choose to avoid to free their own coordinate. A repairable row not voluntarily avoided can instead impose its own even-valuation shell \(S_r\). If it collides in multiple prefixes, the local collision class is the same class modulo the order of 5 and its repair root \(\alpha_r\) is the same.

A task \(p\) routed to a prime factor \(r>3\) of its order forbids a single ball on the \(r\)-coordinate. On a free coordinate there are \(r\) first-digit cells; the same is true for a repair shell with even initial depth, because the root cell can use deeper even shells. For an odd-depth repair shell the first digit is fixed to that of \(\alpha_r\), but all \(r\) second-digit children inside it are alive: the non-root children have odd distance valuation one and the root child has deeper odd-distance shells. If a forbidden ball on \(r\) is disjoint from \(S_r\), the task is already satisfied. Otherwise a ball hitting at most one alive child can be assigned there, allowing capacity \(r-1\) tasks at that coordinate. A shallow ball covering the entire odd-depth repair shell cannot be accepted as an edge. A successful capacitated matching keeps at least one live child at each coordinate. Choose exact good valuations within them and combine by primary-coordinate CRT. One may also free a blocked coordinate by routing its own repairable row somewhere else; all such edges lead to smaller primes.

For fixed prefixes and release choices the exact check is the positive measure of \(S_r\) after deleting the assigned forbidden balls, as in [norm-shell allocation](FIXED_AXIS_NORM_ALLOCATION.md). Matching is only a sufficient relaxation; repeated and nested balls can pass the exact test when matching fails. In particular, if the chosen prefixes do not admit any common non-3 repair by even this sufficient criterion, Hall produces an overloaded subset for the graph being used. With no voluntary releases, available sufficient edges include every split factor, every inert factor read to depth at least two, and every factor whose own row was already designated hard and satisfied by its outgoing avoidance task. An overloaded subset \(T\) has \(|T|>\sum_{r\in\Gamma(T)}(r-1)\). This constrains that matching obstruction, not arbitrary existence of a genuine blocker. A failure of all seven classes to share digits can still leave individual classes feasible.

The replay verifies the same \(n\) with a true short representation, two actual base-5 exceptional hard tests and an ordinary depth-two reader. The forced first digit at ordinary prime 31 avoids one hard row immediately but collides with the other under a freeze of its split factor 653; the latter is handled by releasing that split factor. The second 31-digit can separately avoid reader 17299 while preserving exact valuation two. All seven 3-classes have concrete witnesses to the resulting local panel with identical non-3 imposed coordinates. These are finite local phase facts, not a full-exponent obstruction.

~~~python
from math import prod
N=2087236010422886770972202007475102895968502778098555726208137252171
X=296221625772963004886731795278721
Y=1414032799777752478789910309433518
assert N==6+X*X+Y*Y and N%4==3
assert [d for d in range(2,93,3) if (N-1-pow(5,d,31**2))%31**2==0]==[32]
for p,o,ex,f in [(20771,5*31*67,3,(5,31,67)),(40487,2*31*653,63,(2,31,653))]:
 assert pow(5,o,p*p)==1 and all(pow(5,o//z,p)!=1 for z in f)
 assert (N-1-pow(5,ex,p*p))%(p*p)==p
assert pow(5,9*31**2,17299)==1
assert all(pow(5,9*31**2//x,17299)!=1 for x in (3,31))
assert pow(5,17298,17299**2)!=1
base=28322467133
assert (base%27,base%31**2,base%653)==(5,63,1)
m=(2,81,31**2,653,5,67); M=prod(m)
def crt(vals):
 return sum(v*(M//q)*pow(M//q,-1,q) for q,v in zip(m,vals))%M
chosen={}
for x in range(81):
 d=crt([1,x,63,1,base%5,base%67])
 t=(N-pow(5,d,243))%243
 if not (t in (81,162) or t%9==0 and t%27!=0):
  continue
 assert (N-1-pow(5,d,31**3))%31**3==9*31**2
 assert all((N-1-pow(5,d,p))%p for p in (20771,40487,17299))
 chosen[x%27]=d
assert len(chosen)==7

~~~
