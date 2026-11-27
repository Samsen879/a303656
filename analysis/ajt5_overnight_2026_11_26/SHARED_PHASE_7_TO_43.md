# Exact outer phase conflict at 7 and 43

Fix c≡1 and d≡5 mod 6, and two residuals F0=n−3^c−5^(d+5), F1=n−3^(c+1)−5^d. Requiring both to have finite even valuations at 7 and 43 on the **same** (c,d) fails exactly if n≡12 mod 49 and n is zero mod 43 but not 1376 mod 43².

Indeed at 7 both residuals are units unless n≡5 mod 7. If they contact, they must both be zero mod 49. Writing c=1+6u,d=5+6v, their exponent sums there are 26−7(3u+2v) and 47−7(2u+3v). The linear determinant is 5 mod 7, giving one pair of u,v mod 7 for each n mod 49 in contact. This pair fixes both exponents mod 42, the true order of 3 and 5 at 43. The second sum is three times the first modulo 43; both contact only when n≡0 and the first sum is zero. The small table below shows precisely a single double-contact phase among the locked pairs, c=13,d=35 mod 42, at n=12 mod 49.

At 43, the exact relation F1−3F0=−2n+9374·5^d fixes compatibility mod 43². In the double-contact phase it forces n≡1376 mod 43². Whenever compatible, the phase has one nontrivial common linear lift to depth two; for single contact there is also a nontrivial lift. In either case at the next digit there are at most two forbidden lines, so one can achieve valuation exactly 2 wherever needed. At 7 the invertible matrix similarly allows exact even depth two. The extra 7 and 43 digits are independent **only after** fixing the shared low phase; apply CRT. If 7 has no contact, choose a low phase with neither 43 hit (among the 49 pairs each side has at most 7 solutions, since the actual step-6 orbit at 43 has size 7). Thus the full parity classification follows. Keeping exponents modulo lcm(294,77658)=543606 preserves all the 0-or-2 choices for the viable cases.

```python
assert all(pow(b,42,1849)!=1 for b in (3,5))
```
Exact table replay:

```python
from itertools import product

P = list(product(range(1, 42, 6), range(5, 42, 6)))
def S(c, d, m):
    return ((pow(3,c,m) + pow(5,d+5,m)) % m,
            (pow(3,c+1,m) + pow(5,d,m)) % m)

A = [(S(c,d,49)[0], c, d) for c,d in P if len(set(S(c,d,49))) == 1]
assert sorted(r for r,_,_ in A) == list(range(5,49,7))
assert [(r,c,d) for r,c,d in A if S(c,d,43) == (0,0)] == [(12,13,35)]
T = {x for u,v in product(range(43), repeat=2)
     for x,y in [S(13+42*u,35+42*v,1849)] if x == y}
assert T == {1376}
```

The classification concerns joint local success for **two prescribed labels in one seed**. It is not nonexistence of an individual representation of n or a claim about all seeds. With fixed finite n the index-height restriction still requires its own check.
