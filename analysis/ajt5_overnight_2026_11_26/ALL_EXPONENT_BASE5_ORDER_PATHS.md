# Base-5 order paths for all-exponent obstructions

An all-exponent finite congruence obstruction in the sense of [the exact density theorem](EXACT_DENSITY_ALL_EXPONENTS.md) must contain at least seven inert base-5 Wieferich primes outside \(\{20771,40487,1645333507\}\). This is a necessary condition, not a proof that that many primes exist or can obstruct. A related fixed-axis criterion applies to any finite panel.

Fix \(n\) locally. Use \(C=0\) if \(n=2,3\bmod4\) and \(C=1\) if \(n=0,1\bmod4\). For odd \(n\), \(n-3^C-5^d=1\bmod4\). For even \(n\), it is \(0\bmod4\); fixing either parity of \(d\) leaves \(5^d\) free in its principal-unit ball at depth three, which permits choosing a higher acceptable valuation and odd part. Select the parity of \(d\) for a unit at 3; this leaves the 3-primary exponent component free.

## Route a protected prime to an order coordinate

To protect an inert \(p>3\), choose an odd prime \(r\mid\operatorname{ord}_p(5)\); such a prime exists because \(p\) otherwise divides \(5^2-1=24\). The root equation can exclude at most one class of the \(r\)-primary exponent coordinate at depth \(v_r(\operatorname{ord}_p(5))\). Avoiding that class suffices to give a unit at \(p\). If \(r\) itself is inert and greater than 3, also give it an outgoing protection edge; its target index is smaller. Select independently at each resulting coordinate by the union bound on the excluded classes, and combine the finite choices by CRT. A nonprotected inert prime is ordinary in base 5, and its own coordinate has not been reserved by any protected prime: any inert reserved prime greater than 3 would itself have been protected. Such primes can be repaired in increasing order by using their own digits, making a collision have valuation two, preserving all protected and earlier ordinary tests. The test at 5 is automatic. This produces a fixed \(c=C\) window that passes the entire panel whenever the edge loads are all strictly less than one.

## Six extra exceptional primes fit

Protect the three named exceptional primes with routes
\[
 20771\to67\to11\to5,\qquad 40487\to653,\qquad
 1645333507\to30469139\to1429.
\]
These paths are disjoint and end at split primes. Give each of at most six extra exceptional starting primes a path choosing the largest odd order factor, following an already prescribed successor if reached. Each new edge counts once. At \(r\ge11\) at most seven edges arrive (at most one from the named routes), and at \(r=7\) at most six. Those loads are \(<1\).

At \(r=3\), only \(7,31\) can supply first-depth edges in the default routes and only \(19,5167\) can supply second-depth edges, by the exact cyclotomic factors in the replay. Thus at most six arrivals have total load at most \(2/3+2/9+2/27<1\). At \(r=5\), at most seven arrive. If at most four are shallow, the load is at most \(4/5+3/25<1\). Otherwise reroute the excess shallow edges to 3. Their old orders divide \(2\cdot 5\cdot3^a\) with exact 5-depth one. Only 11 and 71 can have \(a=0\), and no inert prime can have \(a=1\), from the listed exact cyclotomic factors. Thus excess edges can be chosen with \(a\ge2\). If \(k\) distinct new edges initially went into 5, at least \(k\) of the at most six new starting paths ended there, so at most \(6-k\) new edges entered 3. At most \(k-3\) moves are required (one old 5-edge was prescribed). After moves at most three reach 3 and one is at least second-depth, for load at most \(2/3+1/9\). This proves the criterion for the stated exceptional budget.

The same proof also supplies a good double-growth phase for such a panel, by retaking the parity at 3 using the growth limit \(3^c=0\) instead of the fixed \(3^C\), and retaining the parity and finite unit-base periods for \(c\) elsewhere. These are two separate constructions; they need not choose the same \(d\) parity. In fact on \(n=0\bmod3\), any actual whole-box blocker would already block all nonnegative exponents, because its limit test at 3 never vetoes and changes at 5 never veto. No actual such blocker is produced.

## Replay

The last example has seven ordinary inert primes covering all even exponents by first roots at one integer, while every prime still allows ordinary higher-digit repair. It shows why a proof insisting on unit residuals at *all* earlier ordinary primes is too strong.

~~~python
from math import isqrt
from fractions import Fraction as F
def isprime(p):
 return p>1 and all(p%i for i in range(2,isqrt(p)+1))
def factors(x):
 d=2; out=set()
 while d*d<=x:
  if x%d==0:
   out.add(d)
   while x%d==0: x//=d
  d+=1
 if x>1:out.add(x)
 return out
paths=[[(20771,10385,67),(67,22,11),(11,5,5)],
       [(40487,40486,653)],[(1645333507,1645333506,30469139),(30469139,2176367,1429)]]
assert len({p for path in paths for p,_,_ in path})==6
for path in paths:
 for p,o,r in path:
  assert isprime(p) and isprime(r)
  assert p%4==3 and o%r==0 and pow(5,o,p)==1
  assert all(pow(5,o//s,p)!=1 for s in factors(o))
 assert path[-1][-1]%4==1
 p=path[0][0]
 assert pow(5,p-1,p*p)==1 and pow(3,p-1,p*p)!=1
spec={3:(31,),6:(3,7),9:(19,829),18:(3,5167),5:(11,71),10:(521,),15:(181,1741),30:(61,7621)}
cycl={}
for m in range(1,31):
 v=5**m-1
 for d in range(1,m):
  if m%d==0:v//=cycl[d]
 cycl[m]=v
for m,ps in spec.items():
 z=cycl[m]
 for p in ps:
  assert isprime(p) and z%p==0
  z//=p
 assert z==1
assert F(2,3)+F(2,9)+F(2,27)==F(26,27)
assert F(4,5)+F(3,25)<1 and F(2,3)+F(1,9)<1
n=2900803570375724211
P=(7,31,19,5167,271,4159,31051)
assert n%12==3 and all(pow(5,54,p)==1 and pow(5,p-1,p*p)!=1 for p in P)
assert all(any((n-1-pow(5,d,p))%p==0 for p in P) for d in range(0,54,2))

~~~
