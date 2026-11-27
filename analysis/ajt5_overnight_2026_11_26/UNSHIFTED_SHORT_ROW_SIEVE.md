# A short unshifted row through a logarithmic inert-prime sieve

For 2^y≤n<2^(y+1), put A=floor(sqrt(y)), J=1+floor(log_2 y). Condition on n≡1 mod 9 and n≡9 mod p for every prime 7≤p≤A with p≡3 mod 4. As y tends to infinity, all but relative proportion y^(-1/2+o(1)) of the integers in this conditioned class have some residual n−9−5^(2i+1), 0≤i<J, that is coprime to every prime p≤y with p≡3 mod 4. For large y the candidates are in the actual unshifted box, 9 and 5^(2i+1) both at most n/4.

The seeded primes cannot hit these rows: an odd exponent makes the residual a 3-adic unit, and the other seeded primes see a nonzero power of 5. For A<p≤y, two row residues collide only if p divides the product of 25^h−1 over 1≤h<J. Its logarithm is O(J²), so there are O(J²/log A) such primes; a union bound costs at most O(J³/(A log A)). Every other prime hits at most one row and has probability J/p to hit any. These hit indicators are independent **across primes** under the conditional full CRT period, not across rows. To cover all rows without any collision-prime hit needs at least J hits. The exponential moment with base 2 bounds this probability by exp(−J(log 2−sum 1/p)), where the sum is over A<p≤y, p≡3 mod 4. By the prime number theorem for arithmetic progressions and partial summation, that sum is (log 2)/2+o(1), and the full period is exp((1/2+o(1))y), against block length exp((log 2)y). On the fixed residue class the discrepancy is bounded by the full period divided by the block length, up to an absolute constant. This gives the stated combined bound.

There is no pointwise assertion for this short row. For any fixed 0<gamma<(log 2)/2 choose K=floor(gamma*y/log y) distinct inert primes q_i in (A,y]. Impose n≡9+5^(2i+1)+q_i mod q_i² for 0≤i<K in addition to the seeded classes. The combined modulus is at most exp((2*gamma+o(1))y)<2^y, so the same dyadic block contains an integer where the first K rows all have a genuine odd valuation. The primes needed exist by the same prime distribution theorem. The following concrete check includes a raw surviving row and an independent out-of-sieve obstruction.

```python
from math import isqrt
n = 340282366953781138240569012879100594507
assert n.bit_length()-1 == 128 and (n%9,n%7,n%11) == (1,2,9)
def residue(n,d): return n-9-5**d
for i,p in enumerate((19,23,31,43,47,59,67,71)):
    assert residue(n,2*i+1) % (p*p) in range(p,p*p,p)
for p in range(3,129,4):
    if all(p%k for k in range(2,isqrt(p)+1)):
        assert residue(n,21)%p
assert 4*5**21 <= n
m = 1220536
assert residue(m,3)%47**2 in range(47,47**2,47)
assert residue(m,5) == 221**2 + 1081**2
```

The exceptional proportion is conditional on a prescribed class that changes with y. This argument does not show unconditional density one for all integers, a full box pointwise guarantee, or a true representation when some inert prime above y still obstructs every candidate. No novelty claim is made.
