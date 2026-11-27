# Six deep phases versus the seventh shallow phase at one target

**Six shallow and three deep readers erase six phases. A seventh shallow reader is strictly stronger in the same quarter-height box.** At one actual target with the same \(3,5\) strides, the three-deep panel erases columns \(4,53,102,151,200,249\). Replacing its third deep reader with a seventh shallow reader also erases column \(298\). The deep panel’s first vertical escape there is \((298,2013)\). Both panels preserve \((5,45)\).

## Exact incidence bound

Keep the equal-step \(3,7\) native chart and count at most nine higher readers of orders \(49\) and \(343\), outside the fixed \(3571\) stripes. Every fully erased column requires six distinct shallow phases. Each missing nonroot phase modulo \(49\) costs seven deep readers, since all seven children modulo \(343\) contain native-even lifts. With \(s\le5\) shallow readers, this would cost at least \(s+7(6-s)\ge12\) readers.

All erased columns therefore lie in a single class modulo \(49\). Two erased columns in different classes would share at least \(12-s\ge3\) of their six chosen shallow readers. The certified order-\(49\) swap lemma allows at most one: a shared row must swap the horizontal and vertical phases, fixing its vertical phase in the first column. The replay reruns that lemma’s 686 resultants; the exact inputs were also independently checked by multiplication determinants and complete factorization. [SymPy polynomial reference](https://docs.sympy.org/latest/modules/polys/reference.html)

Within the allowable horizontal class, six shallow phases leave one vertical class modulo \(49\). It must contain the native root \(r(u)\bmod343\) defined by \(7^4\mid R(u,r(u))\). The matching first lifting coefficients give \(r(u+49j)\equiv r(u)-49j\bmod343\), so \(T=u+r(u)\) is constant there. A deep reader’s collision at the root solves
\[
(g^u)^2-(n\bmod q)g^u+g^T=0\pmod q.
\]
Consequently, each deep reader supplies at most one orbit of \(u\mapsto T-u\). When the swap preserves the horizontal class, its seven phases split into three pairs and one fixed point. Three deep readers attain six precisely by taking the three pairs. They cannot cover the fixed point as well. When the swap leaves the class, each deep reader supplies at most one phase. This argument at order \(343\) uses only the quadratic and native-root motion.

A seventh shallow reader at exact valuation one fills the missing vertical class for the entire horizontal class. In the control below, the swap has \(T=253\bmod343\), with pairs \(\{4,249\},\{53,200\},\{102,151\}\) and fixed point \(298\). The nine-reader panels share six shallow and two deep rows. Their ninth rows are \(15689507\) at order \(343\) and \(202567\) at order \(49\), respectively.

## Same-target replay

The common target has quarter-height horizontal maximum \(298\) and vertical maximum at least \(2601\). In the deep panel, any escape at column \(298\) must have \(v\equiv298\bmod343\) and \(v\equiv0\bmod3\). The first candidate \(984\) has exact valuation five at \(3\). The next, \(2013\), passes every deep-panel test and has exact valuation one at the extra shallow reader.

```python
from functools import cache
from math import isqrt, lcm, prod
from sympy import symbols, resultant, factorint

def prime(p):
    return p >= 2 and all(p%d for d in range(2,isqrt(p)+1))

X = symbols("X")
Phi = sum(X**(7*i) for i in range(7))

@cache
def factors(N):
    f = factorint(N)
    assert prod(int(p)**k for p,k in f.items()) == N
    assert all(prime(p) for p in f)
    return f

for e,count in ((1,25),(7,3)):
    zeros, candidates = [], set()
    for a in range(49):
        for b in range((a-e)%7,49,7):
            N = abs(int(resultant(Phi,1+X**a-X**e-X**b,X)))
            if N:
                candidates.update(int(p) for p in factors(N) if p%196 == 99)
            else:
                zeros.append((a,b))
    assert zeros == [(e,0)] and len(candidates) == count
    for p in candidates:
        s = p-1
        while s%7 == 0:
            s //= 7
        g,h = pow(3,s,p),pow(5,s,p)
        assert g != h or pow(g,49,p) != 1 or pow(g,7,p) == 1

Q, extra = 3571, 202567
sh = list(zip((6763,119659,190807,430907,434827,472067),
              (11,18,25,32,39,46)))
dp = [(9145067,4,249),(11802631,53,200),(15689507,102,151)]
rows = ([(Q,7,0,1),(extra,49,4,4)]
        + [(p,49,4,b) for p,b in sh] + [(p,343,a,b) for p,a,b in dp])
B = lcm(18,*(p*((p-1)//m) for p,m,a,b in rows))
A = 4117*B
C = lcm(*(p*(p-1) for p,m,a,b in rows))

def S(u,v,m):
    return (pow(3,C+A*u,m) + pow(5,B*v,m)) % m

for p,m,a,b in rows:
    g = pow(3,A,p*p)
    assert prime(p) and p%4 == 3 and pow(3,C,p*p) == 1
    assert g == pow(5,B,p*p) and pow(g,m,p*p) == 1 != pow(g,m//7,p)
assert pow(3,A,49) == pow(5,B,49) != 1
assert pow(5,B,27) == 1 != pow(5,B,81) and pow(5,9*B,243) == 1

eq = [(4,3),(243,82),(7**5,S(4,1278,7**5)+7**4)]
eq += [(p*p,S(a,b,p*p)+p) for p,m,a,b in rows]
M = prod(m for m,_ in eq)
n0 = sum(t*(M//m)*pow(M//m,-1,m) for m,t in eq) % M

def R(u,v,m):
    return (n0-S(u,v,m)) % m

def val(u,v,p):
    return next(k for k in range(6) if R(u,v,p**(k+1)))

for i,v in enumerate((1278,2601,837,2160,396,1719,2013)):
    u = 4+49*i
    assert (u+v)%343 == 253
    assert [val(u,v,p) for p in (3,7,extra)] == [4,4,1]
    assert R(u,v,Q) and all(R(u,v,p) for p,b in sh)
    assert all(R(u,b,p*p) == p for p,b in sh)
    assert [val(u,v,p) for p,a,b in dp] == [
        int(i in (j,5-j)) for j in range(3)
    ]

assert val(298,984,3) == 5
for u in range(5,298,49):
    assert [val(u,45,p) for p in (3,7)] == [4,2]
    assert all(R(u,45,p) for p,_,_,_ in rows)

E = C+298*A
delta = (n0-4*pow(3,E,M)) % M
assert E > M.bit_length() and 298*4117 >= 2*2601
print(E, delta)  # The common target is 4*3**E + delta.
```

The six shallow rows cover all nonroot vertical phases in the erased columns. In the remaining phase, the native \(7\)-valuation is three away from the root class modulo \(343\). The assigned deep row covers that entire root class at exact valuation one. The extra shallow row covers the remaining phase directly, giving the strict full-fibre comparison. All displayed remainders are positive. The escapes certify local survival, and their full two-square status remains open here.
