# Correlated deep arithmetic for two exponent coordinates

At an odd prime not dividing 15, fix coarse classes c≡c0 mod H3, d≡d0 mod H5 with the respective multiplicative orders dividing H3 and H5. By LTE, as the two exponent parameters vary, U=(3^c−3^c0)/p^s3 and V=(5^d−5^d0)/p^s5 cover all pairs of p-adic residue classes, with s_b=v_p(b^H_b−1). Thus every shifted actual residual is one affine form in the **same** two primitive coordinates. First remove common powers from its coefficient pair; the actual valuations retain those scale offsets and the constant term. If the constant has smaller valuation than the coefficient content the label is already frozen.

Labels with proportional primitive coefficient pairs live on one linear coordinate and its joint one-dimensional root tree. For two nonproportional directions use a unimodular change of coordinates to write their coordinates as T and S=aT+delta W, where k=v_p(delta). At k=0 their local Haar distributions are independent. At k>0, first enforce **S≡aT mod p^k**. Only after fixing that coarse coordinate do the residual higher digits in each direction become independent; this follows directly from the linear map and the independent digits of W. Single-prime affine labels should therefore not be assigned separately adjustable depth bits.

There are actual, strictly active examples already at 7. In the two-row example each can attain even alone but not together. In the three-row example every pair can attain even together, but all three cannot. Independent replay:

```python
from itertools import product, combinations

p = 7
n = 100 + 343*5**40
pair = [(0,0),(0,6)]
triple = [(0,0),(1,3),(4,1)]

def zeros(rows):
    return {
        tuple(i for i,(a,b) in enumerate(rows)
              if ((n-3**a-5**b)//7-3**a*u-5**b*v) % 7 == 0)
        for u,v in product(range(7), repeat=2)
    }

def val(r):
    assert r > 0
    k = 0
    while r % 7 == 0:
        r //= 7
        k += 1
    return k

def actual(rows,c,d):
    return tuple(val(n-3**(c+a)-5**(d+b)) for a,b in rows)

assert (0,1) not in zeros(pair)
assert actual(pair,0,0) == (2,1)
assert actual(pair,18,18) == (1,2)
assert set(combinations(range(3),2)) <= zeros(triple)
assert (0,1,2) not in zeros(triple)
assert [actual(triple,c,d) for c,d in [(6,36),(12,30),(30,24)]] == [
    (2,2,1), (2,1,2), (1,2,2)]
```

A second obstruction to testing rank before scaling occurs at 11: H3=H5=5 yields depths (2,1). For n=123+1331*5^35 and labels (0,0),(4,4), the unscaled directional determinant 625−81 is a unit. After scaling and removing one factor of 11, the determinant has valuation 1; the reduced mod-11 forms require V≡0 and V≡10 respectively to reach depth two. The same point cannot lift both to even. These are fixed-phase local statements, not a claim about a growing outer-phase menu or global norm representations.
