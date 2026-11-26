# Short exponent prefixes without enumerating full periods

In an anchored rectangle c=c_0+S_c x, d=d_0+S_d y, first consider readers fixed on the d-axis. A nonconstant such reader excludes at most one x-class modulo its step order. Always-rejecting constant rows must have been excluded separately. After x is chosen, a reader moving on the d-axis excludes at most one y-class, by solving for 5^(S_d y) in its actual cyclic subgroup. A zero-reader primitive slope class likewise excludes at most one residue class at a fixed eligible column.

In a prefix of length L, a class of period T removes at most ceil(L/T) cells. Thus if the sum of these ceilings is strictly below L, the prefix contains a survivor. When the periods are powers of three, remove nested contained classes; the remaining classes are disjoint. The exact surviving count is L minus sum_i floor((L+T_i-1-a_i)/T_i), with least representative a_i. Once a prefix rectangle is certified, compare its largest offset to n using integer arithmetic to guarantee positivity.

At the earlier fixed target, the two c-only readers have step order three, and the moving orders for remaining eligible rows are 3,9,9,27 after trivial unit rows are omitted. A 3-by-6 prefix suffices, not the entire joint period. On its first column the only forbidden classes are y=3 mod 9 at 271 and y=0 mod 27 at 5023; the earliest positive survivor is (31,1240).

The same target also has two subprogressions with the same modular survivor count (five out of nine) and the same first surviving index (two) but different actual heights. One first survivor is active; the other is above n, and both earlier active points have exact odd valuations. This shows why counts on a period alone are insufficient. This conditional panel result has no two-square certificate or general density consequence.

```python
from math import prod

Z = (1783,5023,11419697846380955982026777206637491,163)
P = (19,127,199,271,4159)
f = [3**(1+2310*j) + 5**(82+2310*j) for j in range(9)]
pairs = [(9,24)] + [(0,q) for q in Z]
pairs += [(f[j]+p,p*p) for p,j in zip(P,(0,1,2,2,5))]
M = prod(m for _,m in pairs)
u = sum(a*(M//m)*pow(M//m,-1,m) for a,m in pairs) % M
n = f[-1]+1+(u-f[-1]-1) % M

def R(y,m):
    return (n-pow(3,31,m)-pow(5,778+462*y,m)) % m

for q in (Z[0],Z[2],Z[3]):
    e = (q-1)//3
    assert n%q == 0 and (q-1)%3 == 0 and e%2 == 0
    assert pow(3,e,q) != pow(5,e,q)  # excludes c,d == 1 mod 3
for p,t,hits in zip(P,(3,1,1,9,9),(set(),set(),set(),{3},set())):
    assert pow(5,462*t,p) == 1
    assert t == 1 or pow(5,462*(t//3),p) != 1
    assert {y for y in range(t) if R(y,p)==0} == hits
for p in (127,199):
    assert pow(3,6930,p) == 1 and pow(3,2310,p) != 1
q = 5023
assert R(0,q) == 0 and pow(5,462*27,q) == 1 and pow(5,462*9,q) != 1

assert 3**4651 + 5**3088 < n
assert all(R(1,p) for p in Z+P)
assert 3**31 + 5**16024 < n < 3**31 + 5**24340
assert R(3,271**2) == 49*271 and R(30,271**2) == 132*271
assert R(27,5023**2) == 2964*5023
for a,b,want in ((27,3,{2,3,5,6,8}),(3,24,{2,4,5,7,8})):
    assert {j for j in range(9) if all(R(a+b*j,p) for p in Z+P)} == want
print("Short prefix and same-target height obstruction verified")

# Prefix check independent of cycle size.
bounds=[(3,9),(0,27)]
for L in range(1,80):
    formula=L-sum((L+T-1-a)//T for a,T in bounds)
    assert formula==sum(y%9!=3 and y%27!=0 for y in range(L))
assert min(y for y in range(6) if all(R(y,p) for p in Z+P))==1
print("Exact prefix counts independently checked")
```
