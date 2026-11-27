# Eight uniform centers using separate protected orders on the two axes

**Eight centers are uniformly available among thirteen offsets.** For every integer \(n\), every gap \(h=8\cdot2^a\) with \(a\ge0\), and every finite panel of ordinary inert primes above \(23\), one can choose a common \(C,D\) and eight indices \(I\subseteq\{0,\ldots,12\}\) so that all centers \((C,D+ih)\) pass the small-head tests and have valuation \(0\) or \(2\) at every retained row. Every repeated class at an ordinary tie prime is a unit. A genuine common-Wieferich reader can hit at most one center, so seven such readers cannot cover the menu.

### Choosing and protecting the eight centers

First choose \(C,D\bmod8\) to pass \(2,3\). The exact \(7,19\) table in the replay then permits eight indices using at most four residues modulo \(5\). The table varies \(C,D\bmod18\) with the chosen parities and discards the least populated residue class modulo \(5\). Its maximum is \(8\) when \(n\equiv0\bmod7\) and the parities differ, and \(11\) otherwise. For example, \(n\equiv7\bmod84\) forces opposite parities, so eight is sharp for this particular head screen.

Two indices can tie at an inert prime \(q\) only if \(\operatorname{ord}_q(5)\mid(i-j)h\). The possible odd parts of \(i-j\) are \(1,3,5,7,9,11\), and an inert prime has \(v_2(q-1)=1\). Thus every tie prime divides one of \(5^k-1\) for \(k=2,6,10,14,18,22\). The exact factorizations give the following complete list above \(23\).

| Tie prime | \(\operatorname{ord}_q(3)\) | \(\operatorname{ord}_q(5)\) |
|---:|---:|---:|
| 31 | 30 | 3 |
| 67 | 22 | 22 |
| 71 | 35 | 5 |
| 5167 | 738 | 18 |
| 19531 | 6510 | 7 |
| 12207031 | 369910 | 11 |

Each listed prime occurs to exponent one in every relevant factorization. A base-\(5\) Wieferich reader retains its order modulo \(q^2\), so a repeated hit would require a square factor in one of those same integers. This excludes repeated hits even for singly base-\(5\) Wieferich readers, including zero observations.

Here is how to make every repeated class a unit before doing ordinary repairs.

- At \(31\), vary \(C\) in steps of \(72\). The five choices exclude at most three repeated classes. Then vary \(D\) in steps of \(72\) to pass \(11\). The five choices face at most four exclusions, and the change preserves the \(31\) readings.
- Vary \(C\) in steps of \(360\) to handle \(23\) and \(67\) together. There are eleven choices, with at most eight exclusions at \(23\) and two repeated classes at \(67\).
- Starting with period \(K=3960\), steer \(71,19531,5167,12207031\) in that order. Vary \(C\) by multiples of \(K\) at the first three rows and \(71K\) at the last, updating \(K\) by the row’s \(3\)-order each time. The numbers of distinct choices are \(7,31,41,521\). Each row has at most four repeated classes.

For ordinary repair, protect the full orders of the two axes **separately**. Among inert primes above 23, the protected \(3\)-order lcm has precisely the divisors \(31\) and \(71\). The protected \(5\)-orders contain neither, and base \(5\) is fast at both, so use it there. At every other ordinary row either fast axis is available. There is at most one nonunit center. Its first digit is unique, and a top digit gives exact valuation two. The repair increment includes the earlier periods modulo \(p^3\) and the protected orders on its own axis.

### Same-target controls

Use \(h=8\), \(I=(0,1,2,4,5,7,10,11)\), initial \(C=D=2\), and
\[
n=185006445893301985331857161124823290755.
\]
On the full retained prefix through \(71\), the base-\(5\) repairs at \(31,71\) have first digits \(20,8\). They give remainders \(16\cdot31^2\bmod31^3\) and \(13\cdot71^2\bmod71^3\), respectively. The later tie readings stay units.

For the negative control, repair \(31\) on base \(3\) instead, with all the other order locks except the one at \(19531\). This gives exact valuation two at \(31\), but turns indices \(0,7\) at \(19531\) from units into remainders \(87\cdot19531\) and \(18818\cdot19531\bmod19531^2\). No common first digit can repair that frozen tie. This is why the fast-axis choice matters.

The result is finite-phase. The controls can be made positive by a common target lift preserving every checked residue. The construction gives no ordinary exponent-height bound for the input \(n\).

```python
from itertools import product
from math import gcd, isqrt, lcm, prod

def prime(p):
    return p > 1 and all(p%d for d in range(2,isqrt(p)+1))

assert 5**2-1 == 24
F = {6:(72,(7,31)), 10:(24,(11,71,521)),
     14:(24,(29,449,19531)), 18:(216,(7,19,31,829,5167)),
     22:(24,(23,67,5281,12207031))}
for k,(a,fs) in F.items():
    assert 5**k-1 == a*prod(fs)
    assert len(set(fs)) == len(fs) and all(map(prime,fs))

O = {31:(30,3),67:(22,22),71:(35,5),5167:(738,18),
     19531:(6510,7),12207031:(369910,11)}
assert set(O) == {p for a,fs in F.values() for p in fs if p>23 and p%4==3}
for p,uv in O.items():
    for b,k in zip((3,5),uv):
        assert (p-1)%k == 0 and pow(b,k,p) == 1
        assert all(pow(b,k//f,p)!=1 for f in range(2,k+1) if k%f==0 and prime(f))
        assert pow(b,p-1,p*p) != 1
K = 3960
for p,m,t in ((71,1,7),(19531,1,31),(5167,1,41),(12207031,71,521)):
    u = O[p][0]
    assert u//gcd(u,m*K) == t
    K = lcm(K,u)

def S(c,d,m):
    return (pow(3,c,m)+pow(5,d,m))%m

def good2(r):
    t = r & -r
    return bool(t and t<=8 and r//t%4==1)

def head(n,c,d):
    return good2((n-S(c,d,32))%32) and all((n-S(c,d,p))%p for p in (3,7,11,19,23))

A = {(c,d):(S(c,d,7),S(c,d,19)) for c,d in product(range(18),repeat=2)}
def score(u,v,c,d,h):
    f = [0]*5
    for i in range(13):
        x,y = A[c,(d+i*h)%18]
        if x!=u and y!=v:
            f[i%5] += 1
    return sum(f)-min(f)

for n,e in product(range(32),range(2)):
    assert any(good2((n-S(c,d,32))%32)
               for c,d in product(range(8),range(e,8,2)))
for u,v,a,b,h in product(range(7),range(19),range(2),range(2),(2,4,8,10,14,16)):
    best = max(score(u,v,c,d,h) for c,d in product(range(a,18,2),range(b,18,2)))
    assert best == (8 if u==0 and a!=b else 11)

I = (0,1,2,4,5,7,10,11)
n = 185006445893301985331857161124823290755
P = tuple(p for p in range(27,72,4) if prime(p))
d = 2
K5 = lcm(3960,*(v for u,v in O.values()))
trace = []
for p in P:
    B = lcm(K5,p-1)
    roots = [i for i in I if (n-S(2,d+8*i,p))%p==0]
    if roots:
        i, = roots
        R = (n-S(2,d+8*i,p*p))%(p*p)
        Q = (pow(5,B,p*p)-1)//p
        j = (R//p)*pow(Q*pow(5,d+8*i,p),-1,p)%p
        d += B*j
        trace.append((p,i,j,(n-S(2,d+8*i,p**3))%(p**3)//(p*p)))
    K5 = lcm(K5,p*p*(p-1))
assert trace == [(31,0,20,16),(71,4,8,13)]
for i in I:
    assert head(n,2,d+8*i)
    assert all((n-S(2,d+8*i,p))%p for p in O if p>71)
    for p in P:
        R = (n-S(2,d+8*i,p**3))%p**3
        assert R%p or (R and R%(p*p)==0)

B = lcm(3960,*(u for p,(u,v) in O.items() if p!=19531))
C = 2+30*B
assert (n-S(C,2,31**3))%31**3 == 8*31**2
p = 19531
assert [(n-S(2,2+8*i,p))%p for i in (0,7)] == [4171,4171]
assert [(n-S(C,2+8*i,p*p))%(p*p) for i in (0,7)] == [87*p,18818*p]
```
