# Two real shallow guards with a free ordinary lift

**Yes. Two genuine base-\(5\) exceptional rows can share one shallow digit and leave the other axis unread for an ordinary lift.** At \(20771\) and \(40487\), on the same integer \(N\), the forbidden \(d_{31}\) digits are respectively \(5\) and \(6\). Taking \(d_{31}=0\) protects both rows for every \(c_{31}\). The free \(c_{31}\) then repairs the residue at \(31\) from valuation \(1\) to valuation \(2\).

### A portable two-row bound

In the shared shallow setting of commit `63f090d`, let \(H\subset\mathbb F_p^\times\) have odd prime order \(r\). Suppose the actual orders of both bases read exactly one \(r\)-digit, and freeze their cofactors so the two power sets are \(AH\) and \(BH\). The forbidden \(d_r\) digits correspond bijectively to \(BH\cap(t-AH)\), where \(t=N\bmod p\). [Shared shallow baseline](https://github.com/Samsen879/a303656/commit/63f090d84443397d49c74b7d1c454f2d4efa6d5c)

For \(t\ne0\), put \(\alpha=(-A)^r,\ \beta=B^r\), and form
\[
P(X)=\alpha X^{r+1}-\beta(X-t)^{r+1}-\alpha\beta t.
\]
Every common point is a double root of \(P\). Conversely, \(P=P'=0\) forces \(X^r=\beta\) and \((X-t)^r=\alpha\). At these points \(P''\ne0\), since it is proportional to \(1/X-1/(X-t)\). Thus:

- If \(\alpha=\beta\), then \(\deg P=r\) and there are at most \((r-1)/2\) forbidden digits.
- Otherwise there are at most \((r+1)/2\). Equality requires \(P/(\alpha-\beta)\) to be the square of a polynomial splitting into distinct linear factors over \(\mathbb F_p\). A single nonsquare evaluation rules out equality.

In particular, **two rows with the stronger half-bound leave at least one digit**, provided all \(r\) digits are available. For any number of rows and a prelocked available set \(D\), the portable sufficient inequality is \(\sum_p |B_p\cap D|<|D|\), where \(B_p\) is the forbidden set in the *common* \(d_r\) coordinate. The exact row count before restriction to \(D\) is \(\deg\gcd(X^r-\beta,(X-t)^r-\alpha)\). The union can also be smaller than the sum.

### Two genuine rows on the same integer

Take
\[
N=10+7469418541821370391905589976840289^2
     +8187539692710415393868954311484136^2.
\]
With \(r=31\), the verified data are:

| Prime \(p\) | \(o_3(p)\) | \(o_5(p)\) | Hard exponent at \(c=0\) | Forbidden \(d_{31}\) |
|---|---:|---:|---:|---:|
| \(20771\) | \(335r\) | \(335r\) | \(5\) | \(\{5\}\) |
| \(40487\) | \(653r\) | \(1306r\) | \(10453\) | \(\{6\}\) |

For each listed hard exponent \(e\), \(N-1-5^e\equiv p\bmod p^2\), and \(5^{o_5(p)}\equiv1\bmod p^2\). These are actual odd-valuation rows under the fixed \(c=0\) phase. Both primes are ordinary to base \(3\). The nonsquare tests \(P(t)/(\alpha-\beta)\) give \(13073\) and \(7537\) respectively, so the two-row capacity bound alone certifies \(15+15<31\). The exact union leaves 29 choices.

The **complete prelocks before assigning \(d_{31}\)** are
\[
c\equiv0\pmod{2\cdot3\cdot5\cdot11^2\cdot67^2\cdot653},\qquad
d\equiv5\pmod{2\cdot3^4\cdot5\cdot11^2\cdot67^2\cdot653}.
\]
These include both guard cofactors, the parity and \(3\)-adic conditions, the ordinary \(11,67\) shells, and \(c\bmod30\) for the lift at \(31\). Neither prelock reads \(31\). After setting \(d\equiv0\bmod31^2\), the \(d\)-axis reads \(31\) but the \(c\)-axis remains free there. One exact local phase is
\[
(c,d)=(5001119933700,\ 140201609034965).
\]
The residues modulo \(4,27,11^3,31^3,67^3,20771,40487\) are respectively
\[
1,\ 18,\ 121,\ 961,\ 4489,\ 19407,\ 30848.
\]
At the same \(d\), keeping \(c=0\) gives \(22\cdot31\bmod31^2\). Thus the ordinary \(31\)-lift genuinely uses the unread axis. The large phase is a local witness; \(N\)'s actual square representation uses \(c=2,d=0\).

**Separate zero-target control.** At the same genuine exceptional prime \(40487\), take target \(t=0\), \(c\equiv0\bmod653\), and \(d\equiv653\bmod1306\). The cosets are \(H\) and \(-H\), so all 31 digits allow a collision and this unit-protection scheme fails. The integer \(40487=10+101^2+174^2\) itself has a true representation. This zero case does not enter the nonzero-target bound.

```python
from math import isqrt
N=10+7469418541821370391905589976840289**2+8187539692710415393868954311484136**2
r=31
c,d=5001119933700,140201609034965
for p,m,k,e,bad,non in [(20771,335,335,5,5,13073),(40487,653,1306,10453,6,7537)]:
    assert p%4==3 and all(p%j for j in range(2,isqrt(p)+1))
    assert [next(i for i in range(1,p) if pow(b,i,p)==1) for b in (3,5)]==[m*r,k*r]
    assert pow(5,k*r,p*p)==1 and pow(3,m*r,p*p)!=1
    assert (N-1-pow(5,e,p*p))%(p*p)==p
    assert c%m==0 and d%k==5 and d%r==0
    H={pow(3,m*j,p) for j in range(r)}
    assert {(5+k*j)%r for j in range(r) if (N-pow(5,5+k*j,p))%p in H}=={bad}
    t=N%p; alpha=-1; beta=pow(5,5*r,p)
    val=((alpha*pow(t,r+1,p)-alpha*beta*t)*pow(alpha-beta,-1,p))%p
    assert val==non and pow(val,(p-1)//2,p)==p-1
assert c%(2*3*5*11**2*67**2*653)==0
assert d%(2*3**4*5*11**2*67**2*653)==5
assert (N-1-pow(5,d,31**2))%31**2==22*31
for m,z in ((4,1),(27,18),(11**3,121),(31**3,961),(67**3,4489),(20771,19407),(40487,30848)):
    assert (N-pow(3,c,m)-pow(5,d,m))%m==z
assert 40487==10+101**2+174**2
H={pow(3,653*j,40487) for j in range(r)}
assert {pow(5,653+1306*j,40487) for j in range(r)}=={-x%40487 for x in H}
print('OK')
```

This gives joint transport for a real two-row panel, not arbitrary exceptional panels.
