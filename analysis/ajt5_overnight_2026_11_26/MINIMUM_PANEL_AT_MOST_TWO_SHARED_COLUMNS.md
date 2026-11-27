# At most two shared columns for the minimum mixed equal-step panel

**The same seven readers cannot erase adjacent columns outside the fixed \(3571\) stripes.** In the equal-step \(3,5\) model, all columns erased by a minimum-budget panel lie in one residue class modulo \(49\). For the mixed budget of six order-\(49\) readers and one order-\(343\) reader, at most two classes modulo \(343\) can be erased. The same seven actual primes attain two classes, \(4\) and \(53\bmod343\), at one target with active escapes in columns \(5,54,102\).

## The sharing restriction

Keep the native \(3,7\) chart with \(v\equiv1-u\bmod7\), \(n\equiv82\bmod243\), and \(v_3(B)=2\). Assume \(7\nmid B\), \(A=\lambda B\) with \(\lambda\equiv1\bmod49\), and \(3^C\equiv1\bmod q\) at the higher readers. At each order-\(49\) reader, the actual steps \(3^A,5^B\) coincide in an element \(g\) of order \(49\).

Suppose this reader collides at \((u,v)\) and \((u+\delta,v')\), where \(\delta\not\equiv0\bmod49\). Write \(\delta\equiv et\bmod49\), with \(e=1\) or \(7\) and \(t\) a unit. Dividing the equal offsets by \(g^u\) and using \(X=g^t\) gives
\[
1+X^a-X^e-X^b=0,\qquad b\equiv a-e\bmod7.
\]
Here \(a=(v-u)/t\) and \(b=(v'-u)/t\bmod49\). The last congruence comes from the native line. Thus \(q\) divides the resultant of this polynomial with \(\Phi_{49}\), unless the integer resultant vanishes.

The exact check below covers 343 resultants for each \(e\). The only zero is \((a,b)=(e,0)\). The nonzero resultants leave 25 candidate inert primes for \(e=1\) and three for \(e=7\). None admits the required actual \(3,5\) steps. Indeed, if \(s\) is the prime-to-\(7\) part of \(q-1\), then \(3^s,5^s\) must themselves have exact order \(49\). Raising the common-step equality to \(s\), using \(7\nmid B\) and \(\lambda\equiv1\bmod49\), forces \(3^s=5^s\). The check excludes this at every candidate. The 686 resultant magnitudes can be independently reproduced using integer multiplication determinants in \(\mathbb Z[X]/(\Phi_{49})\). The inline replay uses SymPy and checks every prime factor by trial division. [SymPy’s polynomial arithmetic documentation](https://docs.sympy.org/latest/modules/polys/internals.html)

Consequently a reader shared across two different horizontal phases modulo \(49\) must swap the exponent phases:
\[
(v,v')\equiv(u+\delta,u)\pmod{49}.
\]
A minimum seven-reader erasure needs six order-\(49\) readers on distinct vertical classes. At most one of them can make that swap. At any other \(Q\)-unit column, at most one shallow reader and the possible order-\(343\) reader can collide. Six lifts spaced by \(21\), beginning below \(21\), then give an escape with \(v\le125\). The exact native tests remove at most two lifts at \(3\) and one at \(7\), and the two higher readers remove at most one each.

## Why the mixed panel can share exactly two classes

Let \(r(u)\bmod343\) be the native root defined by \(7^4\mid R(u,r(u))\). For a shift \(\delta\equiv0\bmod49\) the root moves by
\[
r(u+\delta)\equiv r(u)-\delta\pmod{343}.
\]
Both first lifting coefficients at \(7\) agree in this chart. Writing \(\delta=49j\), the two shift multipliers modulo \(7^4\) are \(1+343cj\) and \(1-343cj\), so their changes cancel.

The six shallow readers leave one \(v\bmod49\) class. At a fully erased column this must be the class of \(r(u)\). Within it, the lifts outside \(r(u)\bmod343\) have native valuation three, while the root class contains even lifts that require the deep reader. Hence the order-\(343\) reader must hit \((u,r(u))\). If its two steps coincide, the product \(g^{u+r(u)}\) is constant on the single allowable \(u\bmod49\) class. The prescribed sum and that product give one quadratic, so there are at most two erased \(u\bmod343\) classes.

The replay makes the two roots \(4,53\). The six shallow readers delete the six \(v\bmod49\) classes other than \(4\) on the native line at both columns. The deep reader deletes \(v\equiv53\bmod343\) at \(u=4\) and the swapped class \(v\equiv4\bmod343\) at \(u=53\), in both cases at exact valuation one. This covers the full native fibres. The root phases at the two erased columns have exact native valuations \(4,4\) at the displayed witnesses.

## Exact replay

The target is \(n=4\cdot3^E+\texttt{offset}\) from the code. Its quarter-height horizontal maximum is \(102\), and its vertical maximum is at least \(3042\). Both erased columns and all three escapes are active with positive remainders.

```python
from functools import cache
from math import isqrt, lcm, prod
from sympy import symbols, resultant, factorint

X = symbols("X")
F = sum(X**(7*i) for i in range(7))

def prime(p):
    return p >= 2 and all(p%d for d in range(2,isqrt(p)+1))

@cache
def factors(n):
    f = factorint(n)
    assert prod(int(p)**j for p,j in f.items()) == n
    assert all(prime(p) for p in f)
    return [int(p) for p in f]

for e,count in ((1,25),(7,3)):
    zero, candidates = [], set()
    for a in range(49):
        for b in range((a-e)%7,49,7):
            n = abs(int(resultant(F,1+X**a-X**e-X**b,X)))
            if n:
                candidates.update(q for q in factors(n) if q%196 == 99)
            else:
                zero.append((a,b))
    assert zero == [(e,0)] and len(candidates) == count
    for q in candidates:
        s = q-1
        while s%7 == 0:
            s //= 7
        g,h = pow(3,s,q),pow(5,s,q)
        assert g != h or pow(g,49,q) != 1 or pow(g,7,q) == 1

Q = 3571
rows = [(6763,49,11),(119659,49,18),(190807,49,25),
        (430907,49,32),(434827,49,39),(472067,49,46),(9145067,343,53)]
panel = [(Q,7,1),*rows]
C = lcm(*(q*(q-1) for q,m,b in panel))
B = lcm(18,*(q*((q-1)//m) for q,m,b in panel))
A = 4117*B

def S(u,v,m):
    return (pow(3,C+A*u,m)+pow(5,B*v,m)) % m

for q,m,b in panel:
    assert prime(q) and q%4 == 3
    g = pow(3,A,q*q)
    assert g == pow(5,B,q*q) and pow(3,C,q*q) == 1
    assert pow(g,m,q*q) == 1 != pow(g,m//7,q)
assert pow(3,A,49) == pow(5,B,49) != 1
assert pow(5,B,27) == 1 != pow(5,B,81)

eq = [(4,3),(243,82),(7**5,S(4,396,7**5)+7**4),
      (Q*Q,S(0,1,Q*Q)+Q)]
eq += [(q*q,S(4,b,q*q)+q) for q,m,b in rows]
M = prod(m for m,_ in eq)
n0 = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq) % M

def val(u,v,p):
    return next(k for k in range(6) if (n0-S(u,v,p**(k+1)))%p**(k+1))

for u,v in ((4,396),(53,1719)):
    assert [val(u,v,p) for p in (3,7,9145067)] == [4,4,1]
    assert all(val(u,b,q) == 1 for q,m,b in rows[:-1])
for u,v,k in ((5,45,2),(54,45,2),(102,3042,4)):
    assert [val(u,v,p) for p in (3,7)] == [4,k]
    assert all(val(u,v,q) == 0 for q,m,b in panel)

E = C+102*A
offset = (n0-4*pow(3,E,M)) % M
assert E > M.bit_length() and 102*4117 >= 2*3042
print(E, offset)
```

The spacing theorem uses the actual equal-step and anchor conditions above. The fixed \(3571\) row still erases its own adjacent pair. The new restriction governs sharing the seven-reader budget on columns where that row is a unit. The three escapes certify local survival, with full two-square status undetermined.
