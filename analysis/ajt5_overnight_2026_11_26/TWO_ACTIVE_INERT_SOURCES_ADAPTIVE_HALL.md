# Adaptive routing for two active inert sources

**Two active inert sources can be handled by reducing the lower source first and routing the upper source only after that reduction.** This gives a deterministic exclusion on the full \(3,5\) panel before \(q=1471\). For every positive old head in that panel, the terminal read retains at least \(4/5\) of its phase mass. The proof works with the terminal’s own prime-primary coordinate frozen.

### Adaptive source reduction and Hall condition

Vary primary digits at distinct odd primes in the **same** exponent of \(g\in\{3,5\}\). A digit at depth \(a-1\) at \(r\) must satisfy \(r^a\mid\operatorname{ord}_q(g)\). Work on a grid with all other exponent coordinates fixed.

Process the source primes in increasing order. A source \(p\) can read only smaller selected primes in its first-residue test, since their powers must divide \(\operatorname{ord}_p(g)\mid p-1\).

- **When all lower digits read by \(p\) are fixed**, apply the exact native norm test to its own digit. At native depth \(h=a-1+v_p(g^{p-1}-1)\), distinct digit choices first separate at depth \(h+1\). A nonempty native set has at least \(p-1\) choices for even \(h\). For odd \(h\), a matching reading can leave just one. Substitute any such pin before processing the next source.
- **When \(p\) still reads free lower digits**, its first-residue collision specifies at most one tuple of those digits. Treat this tuple as forbidden. Avoiding it gives a unit remainder at \(p\), so all its native choices remain available.

An old nonsource row likewise forbids at most one tuple on the digits it reads. To see this, equality of two powers would require their exponent difference to be divisible by the order. A changed digit on any read primary factor prevents that divisibility. An exact unary restriction can therefore be applied before processing a source that reads the affected digit. [Earlier private-order elimination](https://github.com/Samsen879/a303656/commit/15d8441dd555d8e5ddd517bfc790b435b00c8280)

After these reductions, let \(w_i\) be the remaining digit widths and \(D_p\) the free read set of each unresolved forbidden tuple. To retain two choices in a digit \(j\), use capacities \(c_i=w_i-1-\mathbf1_{i=j}\). The exact cut condition for assigning each tuple to one of its read digits is
\[
\#\{p:D_p\subseteq U\}\le\sum_{i\in U}c_i
\qquad\text{for every subset \(U\) of the free digits}.
\]
This is capacitated Hall, with \(c_i\) copies of digit \(i\). Forbid the assigned value on each receiving digit. The resulting rectangle contains at least two phases with distinct shifts mod \(q\), so one has a unit terminal remainder. The cut is exact for this assignment test. Other survival patterns may also pass the local tests. If the test succeeds on every positive old grid, the terminal head stays positive. [Earlier direction-bundle Hall test](https://github.com/Samsen879/a303656/commit/49c29dfc3410b9faf98abdd5fa2277e532743c07)

### Full chronological panel before \(1471\)

A useful two-source case avoids counting the lower-only readers altogether. Let \(r<s\), let the upper source \(s\) read the lower digit, and assume the upper native depth is even. First apply the lower source and **all other old rows that leave the upper digit free**, except for the source at \(s\). This gives \(I\times[s]\) on each grid. Let \(T\) count the remaining nonsource rows that read the upper digit.

If \(|I|\ge2\), discard at most one lower choice to make the source at \(s\) a unit. On a remaining lower choice, the \(T\) readers leave at least \(s-T\) upper choices. If \(|I|=1\), substitute that pin and apply the upper native test. On an old-positive grid, even depth leaves at least \(s-1\) upper choices before the \(T\) readers. Hence **\(T\le s-3\) excludes a terminal zero**, with at least \(s-1-T\) old survivors per contributing grid.

For \(g=5\), use
\[
(r,s,q)=(3,7,1471),\qquad (r^a,s^b)=(3,49).
\]
The order of 5 at \(q\) is \(735\), and its order at 7 is 6, so 7 reads the lower digit. The upper native depth is 2. The **only** nonsource inert prime before \(q\) whose order of 5 contains 49 is 491, with order 245. Thus \(T=1\), at least five old phases survive per contributing grid, and the terminal ratio is at least \(4/5\).

### Same-target replay

The replay passed. At one CRT target, the lower row pins its digit and the upper row reads that pin. The deeper upper digit leaves five old cells and four terminal survivors. At the same target, the shallow upper digit leaves one old cell, which fails the terminal test at exact valuation one. The upper source is a unit on the two *rejected* lower choices, so those safe readings cannot be combined with the lower pin.

```python
from math import lcm, prod, isqrt

def prime(p): return p > 1 and all(p%d for d in range(2,isqrt(p)+1))
def order(p): return next(k for k in range(1,p) if pow(5,k,p)==1)
def val(t,p):
    assert t
    a=0
    while t%p==0: a,t=a+1,t//p
    return a

q=1471
assert prime(q) and q%4==3 and order(q)==735 and order(7)==6
assert pow(5,6,49)!=1 and pow(5,q-1,q*q)!=1
P=[p for p in range(11,q,4) if prime(p)]
assert [p for p in P if (p-1)%49==0 and order(p)%49==0]==[491]

L=lcm(18,6*7**3,*(p*(p-1) for p in P+[q]))
U,V=L//3**val(L,3),L//7**val(L,7)
def f(i,j,m,k=7): return (729+pow(5,2+U*i+k*V*j,m))%m

data=[(4,3),(27,f(0,0,27)+9),(7**4,f(0,6,7**4)+343),
      (491**2,f(0,5,491**2)+491),(q*q,f(0,0,q*q)+q)]
data += [(p,f(0,0,p)+1) for p in P if p!=491]
M=prod(m for m,_ in data)
n=sum(t*(M//m)*pow(M//m,-1,m) for m,t in data)%M

def v(i,j,p,e,k):
    m=p**e
    return val((n-f(i,j,m,k))%m,p)

assert n%4==3 and f(0,0,4)==2
assert [v(i,1,7,4,1) for i in range(3)]==[1,0,0]
for k,old,new in [(7,list(range(5)),list(range(1,5))), (1,[0],[])]:
    assert all(v(i,j,3,3,k)==[2,1,1][i]
               for i in range(3) for j in range(7))
    live=[j for j in range(7) if v(0,j,7,4,k)%2==v(0,j,491,2,k)%2==0]
    assert live==old
    assert all((n-f(0,j,p,k))%p for j in live for p in P if p!=491)
    assert [j for j in live if v(0,j,q,2,k)%2==0]==new
```

The shallow failure keeps the terminal’s primary coordinate frozen. The actual terminal is ordinary, so releasing that coordinate offers a separate repair. These are deterministic local support results. The existence of a positive two-square remainder is a separate question.

Independent BigInt replay checked the exact native pins, the sole upper reader, and the 5-to-4 versus 1-to-0 outcomes on the same CRT target. The Hall condition certifies an assigned-constraint rectangle and is not necessary for genuine local survival.
