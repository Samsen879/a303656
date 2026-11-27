# Joint native vetoes in a rank-step certificate

This is an exact local cover test and a sharp countercontrol at the represented target from AXIS_CONDITIONED_RANK_ELEVEN_PACKING.md. It does not assert that synthetic center supports are produced by common Wieferich primes or change the global bounds.

Fix all conditioning coordinates. On the remaining prime-power prefix tree put every native veto and justified prior projection into one union N, keeping original support labels with each justified projection. At a prefix C, close it if N covers it or a live prefix contains it. Otherwise recurse through precisely the children meeting C outside N. At maximum read depth, one surviving cell gives an escape. This procedure is exact: all live prefixes overlapping C and not containing it are strict descendants in a single child. Thus when j children still have holes and each source supplies only one prefix, at least j eligible sources are needed. For multi-piece sources, combine child witnesses using union of original labels, not addition of label counts. An order guard is not a projected veto until its own fiber has been closed. The union of native shells can be queried without enumerating the full prime-power box by reversing digits and treating each shell as an interval difference.

In the fixed c=1, even-d chart with d=2 mod 5 and d=1 mod 7, put x=d mod 9. Actual ordinary row 43 vetoes x=1 mod 3 away from its 43-center 22; row 19 vetoes x=0 mod 9 away from its 19-center 0. Supply independent synthetic center prefixes at those two coordinates. Their resulting projections cover {1,4,7} and {0}, respectively. Add synthetic ternary prefixes {2,5,8}, {3}, {6}. Removing either center support leaves exactly the corresponding uncovered set, whereas keeping both closes the fiber. A single extra prefix covering the entire 0 mod 3 branch makes row 19 redundant. To keep both projections essential, at least two extra prefixes are therefore needed for 3 and 6, plus one in the 2 mod 3 branch. The three-prefix minimum is unique at this resolution. All five support deletions are checked against raw powers in the replay.

```python
from itertools import product
from math import prod

def crt(rows):
    M = prod(m for _,m in rows)
    return sum(a*(M//m)*pow(M//m,-1,m) for a,m in rows) % M

def cover(a,e,rows):
    children = {}
    for b,f,label in rows:
        if (a-b)%3**min(e,f):
            continue
        if f<=e:
            return {label}
        children.setdefault(b%3**(e+1),[]).append((b,f,label))
    if len(children)!=3:
        return None
    result = set()
    for b,part in children.items():
        child = cover(b,e+1,part)
        if child is None:
            return None
        result |= child
    return result

u = 1749240030127890765912351734436595992951490159
v = 1808434766219862061671534508108331483094094788
n = 28+u*u+v*v
for q,w,fs,e in ((19,9,(3,),0),(43,42,(2,3,7),22)):
    assert pow(5,w,q)==1 and pow(5,w,q*q)!=1
    assert all(pow(5,w//p,q)!=1 for p in fs)
    assert (n-3-pow(5,e,q*q))%(q*q)==0

def veto(q,d):
    r = (n-3-pow(5,d,q*q))%(q*q)
    return r!=0 and r%q==0

# Five synthetic origin labels, including the two center supports.
rows = [(1,1,"A43"),(0,2,"A19"),(2,1,"R2"),(3,2,"R3"),(6,2,"R6")]
expected = {None:set(),"A43":{1,4,7},"A19":{0},
            "R2":{2,5,8},"R3":{3},"R6":{6}}
raw = {k:set() for k in expected}

for x,t,s in product(range(9),range(19),range(43)):
    d = crt([(0,2),(2,5),(1,7),(x,9),(t,19),(s,43)])
    f = veto(19,d) or veto(43,d)
    assert veto(19,d)==(x==0 and t!=0)
    assert veto(43,d)==(x%3==1 and s!=22)
    labels = {"A19":t==0,"A43":s==22,"R2":x%3==2,"R3":x==3,"R6":x==6}
    for k in raw:
        if not (f or any(on for label,on in labels.items() if label!=k)):
            raw[k].add(x)

assert raw==expected
for k,holes in raw.items():
    kept = [r for r in rows if r[2]!=k]
    assert {x for x in range(9) if cover(x,2,kept) is None}==holes
    assert (cover(0,0,kept) is None)==bool(holes)
print("PASS")

# Independent exhaustive minimum at the actual 9-cell resolution.
from itertools import combinations
X=set(range(9))
N43={1,4,7}
N19={0}
family=[X]+[{i for i in X if i%3==j} for j in range(3)]+[{i} for i in range(9)]
winners=[]
for count in range(4):
    for F in combinations(family,count):
        U=set().union(*F)
        if U|N43|N19==X and U|N43!=X and U|N19!=X:
            winners.append((count,F))
assert winners==[(3,({2,5,8},{3},{6}))]
print("Unique three-prefix minimum independently checked")
```
