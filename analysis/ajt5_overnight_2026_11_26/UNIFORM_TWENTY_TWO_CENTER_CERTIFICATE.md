# Uniform twenty-two centers by reserving one endpoint

**The same 37-offset menu now gives twenty-two centers uniformly.** The final ternary loss at \(379\) can be removed. The change is to reserve one missing endpoint at the earlier \(23,67,199\) stage. After that reservation, the joint \(271,379,4159\) step works for **every** allowed seven-phase choice.

### Reserve an endpoint before choosing the seven-phase coordinates

In the generic head, start with the 25 indices \(i\not\equiv1\bmod3\). Use the existing \(23,67\) steering, but send their joint forbidden class to **\(5\) or \(9\bmod11\)**. Each class costs exactly two indices. Class \(5\) removes index \(27\), and class \(9\) removes index \(9\).

At least one choice survives \(199\). Once \(C\) is fixed, let \(D_5,D_9\) be the two \(D\)-choices. Moving the forbidden head class from \(5\) to \(9\) gives
\[
D_9-D_5\equiv-8(9-5)\pmod{11}.
\]
At \(199\), the index period is \(33\), so every repeated representative is in \(\{0,1,2,3\}\). If both choices had a repeated hit there, their representatives would differ by \(4\bmod11\). No two representatives in that range do. When \(23,67\) are both units, cut class \(5\) and choose a \(D\)-phase avoiding \(199\).

For the exceptional head entry \((C,D)=(89,89)\) from the earlier proof, omit index \(9\) before trimming its 27 candidates to 25. The usual \(23,67,199\) step still leaves 23.

### Clear the three ternary rows together

Write \(L=6930\) and vary \(C,D\) by \(Lx,Ly\), respectively, for \(x,y\in\{0,1,2\}\). This preserves all earlier separate-axis readings.

- **\(379\) depends only on \(x\).** If all three \(x\)-choices hit repeated classes, three distinct \(5^{8r}\), \(0\le r\le15\), must form a translate of a scaled order-three subgroup. They must therefore satisfy \(3\sum z^2=(\sum z)^2\). The only triples passing that test modulo \(379\) are \((0,7,14)\) and \((1,8,15)\). Each uses a representative \(1\bmod3\), which the generic head omits. The exceptional head also lacks both triples.
- **\(271\) and \(4159\) each veto at most one \(y\) once \(x\) is fixed.** Their \(5\)-order is \(27\), and the repeated representatives are in \(0,\ldots,9\). A \(D\)-move by \(L\) preserves the hit representative modulo \(9\). The only collision in that range is \(0,9\), and the endpoint reservation prevents both from being repeated representatives.

Choose a safe \(x\) at \(379\), then a \(y\) outside the at most two vetoes. Lock both axes modulo \(20790\). The higher ternary digits, late steering, and ordinary repairs proceed unchanged. The seven-phase step costs at most one deletion, so at least **22** of the 23 candidates survive.

The non-reuse argument stays within this single selected menu. A two-hit common-Wieferich reader would have its square divide \(5^{2m}-1\) for an odd \(m\le35\), which the [existing squarefree certificate](https://github.com/Samsen879/a303656/blob/a00176489cff6c1882530aaac183d3ec12a0f720/analysis/ajt5_overnight_2026_11_26/UNIFORM_TWENTY_CENTER_CERTIFICATE.md) excludes. Thus a blocking finite panel requires at least 22 such readers.

### Same-target control

The replay uses \(C=22\), observations \(257,59,2728\) at \(271,379,4159\), and zero observations at \(23,67\).

| Earlier \(D\) | Cut modulo \(11\) | Ternary outcome |
|---:|---:|---|
| \(1\) | \(4\) | All nine phases fail under the frozen locks. The pair \((x,y)=(0,1)\), and it ties indices \(0,27\) at \(4159\). |
| \(631\) | \(5\) | \((x,y)=(0,2)\) leaves singleton hits at \(271,4159\) and clears \(379\). |

The change \(D\mapsto D+630\) preserves the seven-phase readings. On the same CRT target, the failed pair at \(4159\) has first readings \(3507,1656\), so a common first digit cannot repair it. The successful branch gives exact remainders \(226\cdot271^2\bmod271^3\) and \(3099\cdot4159^2\bmod4159^3\), preserving the full prefix through \(271\) and the \(379\) reading.

This is a **finite-phase result**. It does not bound the selected exponents in the ordinary height window for the input \(n\).

```python
from itertools import combinations, product
from math import isqrt, lcm, prod

def S(c,d,p):
    return (pow(3,c,p)+pow(5,d,p)) % p

def prime(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))

def order(b,p):
    return next(j for j in range(1,p) if pow(b,j,p)==1)

def repeats(I,m):
    return {i for i in range(37-m) if i in I and i+m in I}

L=6930
assert pow(5,L,379)==pow(3,L,271)==1
assert pow(3,L,379)!=1 and pow(3,3*L,379)==1
assert order(5,271)==order(5,4159)==27 and L%27==18
v=[pow(5,8*i,379) for i in range(16)]
triples=[J for J in combinations(range(16),3)
         if (3*sum(v[i]**2 for i in J)-sum(v[i] for i in J)**2)%379==0]
assert triples==[(0,7,14),(1,8,15)]

head=[i for i in range(37) if i%3!=1]
assert len(head)==25
for j in (5,9):
    J=[i for i in head if i%11!=j]
    assert len(J)==23 and not {0,9}<=repeats(J,27)
    assert all(not set(t)<=repeats(J,21) for t in triples)
rare=[i for i in range(37) if all(S(89,89+8*i,p)!=r
      for p,r in ((7,2),(19,0),(11,8),(31,27)))]
assert len(rare)==27 and 9 in rare
assert all(not set(t)<=repeats(rare,21) for t in triples)

locked=(7,11,19,23,31,67,199,43,71,127,211,631)
assert all(lcm(*(order(b,p) for p in locked))==L for b in (3,5))
assert all(pow(b,3*L,p)==1 for b in (3,5) for p in (271,379,4159))

c=22
def mask(d):
    return [i for i in head if all(S(c,d+8*i,p) for p in (23,67))]
A,B=mask(1),mask(631)
assert len(A)==len(B)==23
assert {i%11 for i in set(head)-set(A)}=={4}
assert {i%11 for i in set(head)-set(B)}=={5}
obs={271:257,379:59,4159:2728}
def hit(p,d,x,y,I):
    return [i for i in I if S(c+L*x,d+L*y+8*i,p)==obs[p]]
def phases(d,I):
    return [(x,y) for x,y in product(range(3),repeat=2)
            if all(len(hit(p,d,x,y,I))<=1 for p in obs)]
assert phases(1,A)==[] and phases(631,B)==[(0,2)]
assert hit(4159,1,0,1,A)==[0,27]
assert [hit(p,631,0,2,B) for p in obs]==[[18],[],[0]]

# The certified tie set and the unchanged 5-axis lock.
T={31,43,47,59,67,71,127,163,191,199,211,251,271,379,487,631,1303,4159,
   5167,5227,6271,7603,8971,19531,31051,35671,38923,519499,595123,3981071,
   5096867,9384251,12207031,16018507,190771747,28086211607,386478495679,
   6090817323763,42272797713043,625552508473588471}
P=tuple(p for p in range(27,272,4) if prime(p))+(379,4159)
V=lcm(3960,*range(2,71,4))
assert all(pow(5,V,p)==1 for p in T)
assert all(any(pow(b,p-1,p*p)!=1 for b in (3,5)) for p in P)

D0=631+2*L
D=D0
R=[(32,23),(3,1),(23,0),(67,0),(379,59)]
trace=[]
for p,i in ((271,18),(4159,0)):
    K=lcm(V,p-1,*(q*q*(q-1) for q in P if q<p))
    r=(S(c,D+8*i,p**3)+p)%p**3
    assert r%p==obs[p]
    R.append((p**3,r))
    j=pow(((pow(5,K,p*p)-1)//p)*pow(5,D+8*i,p),-1,p)
    D+=K*j
    if (r-S(c,D+8*i,p**3))%p**3==0:
        D+=K*p
    trace.append((p,j,(r-S(c,D+8*i,p**3))%(p**3)//p**2))
assert trace==[(271,125,226),(4159,1217,3099)]

for p in (T|set(P)|{7,11,19,31})-{23,67,271,379,4159}:
    U={S(c,D0+8*i,p) for i in B}
    if p in {7,11,19,31}:
        U|={S(c,1+8*i,p) for i in head}
    if p in {43,71,127,211,631,199}:
        U|={S(c,1+8*i,p) for i in A}
    R.append((p,next(r for r in range(p) if r not in U)))
M=prod(q for q,r in R)
n=sum(r*(M//q)*pow(M//q,-1,q) for q,r in R)%M
assert (n-S(c,D,32))%32==1
assert [(n-S(c,1+L+8*i,4159**2))%(4159**2)
        for i in (0,27)]==[3507*4159,1656*4159]
for i in B:
    assert all((n-S(c,D+8*i,p))%p for p in (3,7,11,19,23,31,67))
    for p in P:
        r=(n-S(c,D+8*i,p**3))%p**3
        assert r%p or (r and r%p**2==0)
```
