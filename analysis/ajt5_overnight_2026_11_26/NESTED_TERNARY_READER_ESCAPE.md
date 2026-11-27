# Nested ternary-order escape on an anchored slope

Take c_j=c_0+Sj, d_j=d_0+lambda Sj, with c_0 and lambda units modulo 3, d_0=lambda c_0 modulo 3, and v_3(S)=k>=1. For each reader p>5, include the prime-to-3 part of p-1 in S and require the target residue nonzero modulo p. Write T=3^r>1 for the joint order of the step powers. Then each reader hits at most one of the three lifts of every j modulo T/3.

Indeed, the top-digit multipliers u,v are cube roots and at least one is nontrivial. If exactly one is nontrivial, the three values are distinct. If u=v, the three values are distinct except for an identically zero triple, which cannot hit a nonzero target. Otherwise v=u^(-1); a repeat after one step would force 3^c/5^d=-(v-1)/(u-1)=u^(-1). But both bases then have ternary order depth a=k+r>=2. Taking the primary component of 5 as generator, let sigma be the primary logarithm of 3. The top multipliers being unequal means sigma differs from lambda modulo 3. The primary component of the alleged ratio has exponent sigma c-d, a unit modulo 3 by the anchored primitive slope. Its order is 3^a, a contradiction. Every repeat in a triple can be rotated to an adjacent repeat.

If m_r<=2 readers have order 3^r at every depth r<=R, every complete window of 3^R consecutive phases has at least product_r(3-m_r) survivors. On the residue tree each surviving parent has three children; each reader introduced at that level deletes at most one. Also, the ordered differences ±T/3 cannot occur between hits. The previous distinct-difference lemma therefore sharpens to h(h-1)<=T-3. If B is the actual number of surviving parents and s_r is the largest h satisfying this inequality, the next number is at least max(0,3B-m_r min(B,s_r)).

The replay builds one target with nine positive remainders and all four preceding zero readers avoided. Three ordinary nonzero readers of order three cover the entire ray modulo nine by exact valuation one. At the very same target a panel with orders 3,3,9,9 leaves one phase, even though the sum of the independent hit bounds exceeds the window. The omitted reader at 199 certifies that this surviving remainder is not a sum of two squares. The constructed target is above the last offset by design; no general prescribed-target height control or global bound changes.

```python
from math import isqrt, prod

Z = (1783, 5023, 11419697846380955982026777206637491, 163)
P = (19, 127, 199, 271, 4159)
depth = (1, 1, 1, 2, 2)
assigned = (0, 1, 2, 2, 5)
S = 2310
cells = [(1+S*j, 82+S*j) for j in range(9)]
F = [3**c + 5**d for c,d in cells]
assert all(c%6 == 1 and d%6 == 4 and (d-c)%81 == 0 for c,d in cells)

pairs = [(9,24)] + [(0,q) for q in Z]
for p,r,j in zip(P,depth,assigned):
    assert p%4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
    assert all(pow(g,p-1,p*p) != 1 for g in (3,5))
    assert all(pow(g,S*3**r,p) == 1 for g in (3,5))
    assert any(pow(g,S*3**(r-1),p) != 1 for g in (3,5))
    pairs.append((F[j]+p,p*p))

M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = F[-1]+1+(u-F[-1]-1) % M
R = [n-f for f in F]
assert F[-1] < n <= F[-1]+M and n.bit_length() == 43100
assert all(x > 0 and all(x%q for q in Z) for x in R)
assert all(n%p and R[j]%(p*p) == p for p,j in zip(P,assigned))

hits = [{j for j,x in enumerate(R) if x%p == 0} for p in P]
assert hits == [{0,3,6}, {1,4,7}, {2,5,8}, {2}, {5}]
for j,x in enumerate(R):
    p = P[j%3]
    assert x%p == 0 and x%(p*p) != 0
assert set(range(9)) - (hits[0] | hits[1] | hits[3] | hits[4]) == {8}
assert R[8] % 199**2 == 88*199
print("Exact three-reader cover and positive nested-panel survivor verified")

# Verify the leaf constraint on raw sums at every parent, including all windows.
for i,p in enumerate(P):
    t=3**depth[i]
    for j in range(t//3):
        vals=[F[j+b*t//3]%p for b in range(3)]
        assert len(set(vals))==3 or vals==[0,0,0]
for start in range(9):
    ray=[(start+j)%9 for j in range(9)]
    assert sum(j not in hits[0]|hits[1]|hits[3]|hits[4] for j in ray)==1
print("Nested branch uniqueness independently verified")
```
