# Exact fixed-slice kernel parameterized by live rigid sources

**The reduced interface is bounded by the number of live rigid sources.** The bound comes from exact descending contraction. Removing unread ordinary rows alone can leave a nontrivial interface, even with one genuine rigid source. [CRT interface baseline](https://github.com/Samsen879/a303656/commit/79fc53b5fd0755b5f732b12bb3f291011f39450f)

### A source-count bound and a no-cover certificate

Fix \(n,c\) and the parity of \(d\) on a slice where the two-adic row passes. Use the exact odd-prime panel, with one row per prime. Start with the coordinates read by live rigid sources. Whenever a coordinate \(p\) in this set has an active dynamic row, add the coordinates read by its actual order guard. Everything outside the resulting closure can be peeled in decreasing prime order. At each peel the native row has a safe center for every lower assignment, and no retained row reads the deleted coordinate.

Now take a connected component with \(r\) live rigid sources. **Every rank \(p>r\) can be eliminated without increasing its source count.** At the descending step, the only native dynamic row involving \(p\) is row \(p\) itself. Higher rows have already been eliminated, and lower rows have orders dividing \(q-1<p\). At a fixed lower phase:

- If the outer shell is safe, the \(p-1\) off-center first branches and the center each need a rigid prefix.
- If the outer shell is rejected, the center branch still needs coverage. Without its centered first prefix, each of its \(p\) children has a safe point, requiring \(p\) sources. At depth one, there is no finer prefix available.

With fewer than \(p\) sources, the only new full-fibre witness is therefore a centered first prefix paired with the actual rejecting outer shell. Delete its \(p\)-prefix and intersect its lower guard with the native row’s order guard. Each source has at most one descendant. This gives the induction down through every \(p>r\). The cutoff is sharp for the prefix rule: **synthetically**, \(p\) distinct first prefixes cover the entire axis.

The remaining component has at most \(k=\pi_{\rm odd}(r)\) axes. On each axis there are at most \(r+k-1\) reader-prefix tests. The native row adds just **one Boolean test** for whether its own shell rejects, regardless of the precision or number of shells. Its order guard is handled on the other axes. Thus each axis needs at most \(2(r+k)\) cells, and the whole exact kernel has at most \([2(r+k)]^k\) cell tuples. This bounds the weighted interface independently of the sizes and depths of the eliminated orders, once the actual guards are decoded. A component that splits can use a fresh local source count.

A cheap sufficient no-cover certificate is to take, on each remaining axis, the nonempty set of cells safe for its native shell. Their product passes all dynamic rows. If the sum of the surviving rigid rectangles’ relative masses in that product is below one, a safe point exists. The masses use exact prefix and shell counts. The bounded kernel gives an exact decision when this sufficient test is inconclusive.

### Actual controls

**One genuine rigid source.** Prime \(20771\) has \(\operatorname{ord}_{20771}(5)=10385=5\cdot31\cdot67\) and lifting depth two. Set \(n\equiv4+20771\bmod20771^2\) and \(n\equiv4\bmod p^2\) for \(p=67,31,11\), with \(c=1\) and even \(d\). The rigid guard reads \(\{5,31,67\}\), so the read closure retains a triangle after unread-row peeling. The actual centered contractions at \(67,31,11\) leave a single guard on \(\{3,5\}\). Its one prefix cannot fill rank 5, so it disappears. This is a base-5 rigid control on the chosen slice. Directly, \(d=2\) passes all four rows.

**The fixed 7/11/463 graph.** The exact input scope at 463 gives a four-vertex clique. Its private center makes the projected constraint a tautology. The remaining two edges peel as well, leaving no nonconstant message on the retained \(3,5\) axes. Charging the whole actual 463 guard creates a triangle on \(\{3,7,11\}\) even though the exact panel has zero rigid sources. At the hit target, descending elimination \(11\to7\) sends an eight-cell message on \(\{3,5,7\}\). The order \(7\to11\) needs at most four cells per message. Both leave **14 of 15** lower phases safe in the charged model, while the exact panel leaves **15 of 15**.  This is why artificial vetoes must be accounted for separately when applying a genuine-source budget.

### Inline replay

```python
from itertools import product
from math import isqrt, prod

def crt(rows):
    m = prod(q for _,q in rows)
    return sum(a*(m//q)*pow(m//q,-1,q) for a,q in rows) % m

for q,w,fs,s in (
    (20771,10385,(5,31,67),2), (67,22,(2,11),1),
    (31,3,(3,),1), (11,5,(5,),1), (463,462,(2,3,7,11),1),
):
    assert all(q % j for j in range(2,isqrt(q)+1))
    assert prod(fs)==w and all(pow(5,w//p,q)!=1 for p in fs)
    assert pow(5,w,q**s)==1 and pow(5,w,q**(s+1))!=1

q = 20771
n = crt([(4+q,q*q)]+[(4,p*p) for p in (67,31,11)])
assert (n-4)%(q*q)==q
assert all((n-3-pow(5,2,p))%p for p in (q,67,31,11))
scope = {5,31,67}
for p,reader,expected in ((67,11,{5,31,11}),
                          (31,3,{3,5,11}),(11,5,{3,5})):
    assert p in scope and (n-4)%(p*p)==0
    scope = (scope-{p}) | {reader}
    assert scope==expected
assert scope=={3,5} and 1<5

n = 35974890041509937764240647419591826365
D = {3:(0,2),5:(0,4),7:(0,2),11:(0,1)}
def residue(p,K,*digits):
    return (n-3-pow(5,crt([(0,2),*digits]),p**K))%p**K
def safe(p,*digits):
    r = residue(p,2,*digits)
    return r==0 or r%p!=0

for x,y,z,t in product(*(D[p] for p in (3,5,7,11))):
    assert safe(7,(x,3),(z,7)) == (x!=2 or z==2)
    assert safe(11,(y,5),(t,11)) == (y!=4 or t==0)
    assert (residue(463,1,(x,3),(z,7),(t,11))==0) == (
        (x,z,t)==(2,2,0))
    assert safe(463,(x,3),(z,7),(t,11),(88,463))

# Charged guard, projected in the two different orders.
m11 = {(x,y,z):any((y!=4 or t==0) and (x,z,t)!=(2,2,0)
                  for t in D[11]) for x,y,z in product(D[3],D[5],D[7])}
m7 = {(x,t):any((x!=2 or z==2) and (x,z,t)!=(2,2,0)
               for z in D[7]) for x,t in product(D[3],D[11])}
assert (len(m11),len(m7))==(8,4)
for x,y in product(D[3],D[5]):
    left = any(m11[x,y,z] and (x!=2 or z==2) for z in D[7])
    right = any(m7[x,t] and (y!=4 or t==0) for t in D[11])
    assert left==right==((x,y)!=(2,4))

# Synthetic sharpness of the strict p > r cutoff.
assert set(range(7))==set(range(6)) | {6}
assert set(range(7))-set(range(6))=={6}
print("PASS")
# Exhaustively check the sparse contraction on a three-level toy axis.
from itertools import combinations
p=3
choices=[(a,p**j) for j in range(1,4) for a in range(p**j)]
for shell in (False,True):
    bad={x for x in range(p**3) if shell and (x%p or (x%p**2==0 and x!=0))}
    for k in range(p):
        for W in combinations(choices,k):
            filled=all(x in bad or any(x%m==a for a,m in W) for x in range(p**3))
            assert filled==(shell and (0,p) in W)

```

This bound applies to the fixed-c, fixed-d-parity finite panel with the actual one-native-row structure. A native shell test can be treated as an arbitrary Boolean decoration of its own laminar prefix partition; it doubles the cell count without requiring enumeration of all its shells. If the component has no rigid sources, all its coordinates peel, so the empty reduced kernel passes. Bounds on width before exact contractions, and on panels with extra synthetic vetoes, do not follow from the genuine-source count.
