# Nonzero reader: free scale versus frozen digits

## Distinct-difference test on a fixed slope

Fix unit anchors for c,d modulo 3^k, a compatible slope lambda = d/c modulo 3^H, and compatible prime-to-3 congruences. From any compatible pair vary the actual exponents along (c_j,d_j)=(c_0+Sj,d_0+lambda Sj), where S=3^k M with 3 not dividing M. Include the prime-to-3 exponent moduli and the prime-to-3 part of p-1 in M. This preserves both anchors and the slope.

At a reader p>5 with target t=n mod p nonzero, a collision is A X^j+B Y^j=t, where X=3^S and Y=5^(lambda S) modulo p, and A,B are nonzero. Let T be the joint order. If at least one base has ternary order depth above k, then T>=3. For a nonzero difference delta modulo T, a pair of collisions at j and j+delta gives a linear system in A X^j and B Y^j. If the two multipliers at delta differ, the system determines both quantities and hence j modulo T. If the multipliers coincide, the nonzero target forces that common multiplier to be 1, contradicting joint order. Consequently h collisions satisfy h(h-1)<=T-1, and three consecutive scales cannot all collide, because they would repeat the same ordered difference. This bypass is modulo p and does not assume an ordinary lift. It requires an available scale digit. It says nothing by itself about simultaneous survival at other readers or the height at a general prescribed n.

## Pinned controls

At the target of ZERO_READER_ORDER_RATIO_REPAIR.md, every one of the 52 retained primitive slopes has an explicit positive remainder coprime to the same seven-prime panel with c<=13 and d<=142. This is only a panel survivor, not a two-square certificate. The replay gives a genuine hit by zero reader 5023 and a separate exact-valuation-one hit by nonzero reader 19 on a zero-reader survivor. At the same n, freezing c=1,d=2 modulo 110 permits every slope by CRT but makes nonzero reader 11 reject all candidates in that phase. Releasing the 11-primary digit on the 5-axis preserves the ternary slope and repairs a specific phase to valuation two modulo 11³. This frozen congruence control is also only a local statement, with no global density or source-bound change.

```python
from math import lcm, prod

Q = 11419697846380955982026777206637491
Z, O = (1783, 5023, Q, 163), (19, 271, 4159)
P = prod(Z[:-1] + O)
C = 27*lcm(11,31,70491962014697259148313439547145)*P
A, k = 18*P, 163
pairs = [(9,24), (pow(3,C,361),361)] + [(q,q*q) for q in Z[:-1]]
pairs += [(pow(3,C,p*p)+pow(5,A*i,p*p)+p,p*p)
          for i,p in enumerate((271,4159),1)]
pairs += [(pow(3,C+56*k*C,k*k)+1+k,k*k)]
M = prod(m for _,m in pairs)
n = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M

def primary(g, p):
    m = p-1
    while m % 3 == 0:
        m //= 3
    return pow(g,m,p)

def R(c, d):
    return n-3**c-5**d

units = [t for t in range(81) if t%3]
bad = [t for t in units if any(
    primary(3,q) == pow(primary(5,q),t,q) for q in Z)]
assert bad == [41,46] and all(n%q == 0 for q in Z)
slopes = [t for t in units if t not in bad]

assert R(31,130)>0 and R(31,130)%5023**2 == 2510*5023
assert n%361 == 360 and R(7,16)>0 and R(7,16)%361 == 9*19
assert all(R(7,16)%q for q in Z)
assert all(pow(g,18,19)==1 and pow(g,6,19)!=1 for g in (3,5))

witnesses = {}
for t in slopes:
    cells = [(c,t*c%81) for c in (1,7,13)]
    cells = [(c,d+81*(d%2)) for c,d in cells]
    assert all(c%3==1 and d%3==t%3 for c,d in cells)
    assert sum(R(c,d)%19==0 for c,d in cells) <= 2
    witnesses[t] = next((c,d) for c,d in cells
                        if R(c,d)>0 and all(R(c,d)%p for p in Z+O))
assert len(witnesses) == 52
assert max(c for c,d in witnesses.values()) == 13
assert max(d for c,d in witnesses.values()) == 142

assert n%121==6 and R(1,2)>0 and R(1,2)%121==99
assert [pow(g,110,121) for g in (3,5)] == [1,1]
assert [pow(g,10,121) for g in (3,5)] == [1,78]
for t in slopes:
    d = 2+110*((t-2)*pow(110,-1,81)%81)
    assert d%81==t and (n-3-pow(5,d,121))%121==99
assert 93962%810==2
assert (n-3-pow(5,93962,11**3))%11**3==121
print("52 active slopes; exact zero and nonzero controls; frozen-11 obstruction")

# Verify the distinct-difference property on all nonzero cosets of reader 19,
# including all slopes modulo the actual ternary order.
from collections import Counter
for X in (pow(3,6,19),pow(5,6,19)):
    for Y in (1,pow(5,6,19),pow(5,12,19)):
        T=3
        assert pow(X,T,19)==pow(Y,T,19)==1 and X!=1
        for a in range(1,19):
            for b in range(1,19):
                fs=Counter((a*pow(X,j,19)+b*pow(Y,j,19))%19 for j in range(T))
                assert all(h<=2 for z,h in fs.items() if z)
print("Nonzero reader-19 orbit bound independently checked")
```
