# Conditional coverage for a small unshifted exponent grid

Let y=floor(log2 n), A=floor(sqrt(y)), and J=1+floor(log2 y). In the block [2^y,2^(y+1)), condition on n≡2 mod 9 and n≡0 mod each inert prime 7≤p≤A. Take c=2,4 and d=0,2,…,2J−2. All these residuals are units at the seeded primes: at 3 by parity of d, and at the other seeded primes because a sum of two nonzero squares cannot vanish. They are in the actual unshifted box for large y.

The same estimates apply to one row, or to R=max(2,floor(J/50)) rows: use half-exponents i=1,2 plus i=2J+2,…,2J+R−1, with c=2i. Put L=RJ, ν=sum 1/p over the inert primes A<p≤y, and b_y=1−exp(−ν). The conditional proportion on which every selected point is blocked by some odd valuation at a screened prime is (1+o(1))*b_y^L.

Proof: The L integral shifts 9^i+25^j are distinct (the first two rows differ by 72, not a difference of two powers of 25; the other rows are separated by more than 25^(J−1)). The product of all pairwise differences has log size O(L²J), giving O(L²J/log A) collision primes above A. Also ord_p(25)>log(p)/log(25), so any given residue class of a tail prime hits at most 11R grid points for all sufficiently large y, by counting j in each row.

For each noncollision prime p sample independent Poisson variables of mean t_p=−log(1−L/p)/L on the L labels and keep one uniformly selected mark if present. This gives exactly the CRT hit law: no mark with probability 1−L/p, or one given label with probability 1/p. The primes are independent under the CRT measure. Before keeping one mark, labels are independent, each hit with probability b=1−exp(−sum t_p). Conditional on every label hit, the probability of any prime having multiple marks is O(L² sum_{p>A} p^−2)=o(1): for the same label use the Poisson second factorial moment divided by b, and for distinct labels use two first moments divided by b². Thus ordinary primes alone cover all labels with probability (1+o(1))*b^L. Including the collision primes multiplies the upper bound by at most product over those primes of [1+(L/p)(b^(−11R)−1)]=1+o(1), by conditioning on their independently selected residues and bounding the missing labels with the pre-thinning Poisson law. Here b>1/4 eventually and 4^(11R)≤y^(0.44+o(1)). By partial summation of the prime number theorem in progressions, ν→(log 2)/2, and L*|sum t_p−ν|=o(1), so b^L=(1+o(1))*b_y^L.

The full first-power CRT modulus D is exp((1/2+o(1))*y), so interval discrepancy is negligible even relative to b_y^L. For each ordinarily covered residue class modulo D, select one hit prime per label. At most 1/p+O(D/2^y) of the actual integer lifts give an extra p factor for that selected hit. Summing over labels is o(1), so the lower bound also holds for true odd valuations. No assumption of independent grid points is used at an individual prime.

A concrete two-row counterexample to any pointwise claim in this subgrid has y=100, nine true odd-hit primes, and no possible eight-prime support even in the first-power relaxation. Replay:

```python
from math import isqrt

P = [p for p in range(11,101,4)
     if all(p % k for k in range(2,isqrt(p)+1))]
S = [3**c + 25**j for c in (2,4) for j in range(7)]
Q = [(31,41),(19,15),(11,7),(23,2),(43,33),
     (71,11),(47,1),(59,12),(67,29)]

a,M = 2,9
for q,r in [(7,0)] + [(p*p,r) for p,r in Q]:
    a += M*((r-a)*pow(M,-1,q) % q)
    M *= q
n = a + M*((2**100-a+M-1)//M)
assert n.bit_length()-1 == 100
assert 4*max(3**4,25**6) <= n
assert all(any((n-s)%p == 0 and (n-s)%(p*p) != 0
               for p,_ in Q) for s in S)
assert all((n-3**c-5**16)%p for c in (2,4) for p in [3,7]+P)

best = {0:0}
for p in P:
    masks = {sum(1<<i for i,s in enumerate(S) if s%p == r)
             for r in range(p)} - {0}
    nxt = best.copy()
    for u,k in best.items():
        for v in masks:
            nxt[u|v] = min(nxt.get(u|v,99), k+1)
    best = nxt
assert best[(1<<len(S))-1] == 9
print(n)
```

The conditioned class has vanishing relative size in the full block. Neither this asymptotic nor its counterexample decides the full exponent box or deals with primes above the screening threshold. No novelty claim is made.
