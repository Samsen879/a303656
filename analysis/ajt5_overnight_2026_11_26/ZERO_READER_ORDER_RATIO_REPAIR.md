# Zero-reader order ratios and ordinary-axis repair

## Scope

This is a finite-panel escape criterion for inert primes whose target residue is zero, with conditional addition of ordinary rows. It does not control exponent height or unlisted primes, does not account for nonzero rigid observations, and changes neither the unconditional density bound nor the minimum-source bound.

## Homogeneous slope obstruction

Let q > 5 be inert with q dividing n, and let an odd prime ell divide q-1. Projecting a collision 3^c = -5^d modulo q to the ell-Sylow subgroup removes the sign. If the two base orders there are ell^a and ell^b, write c = ell^u C and d = ell^v D with C and D units. A collision needs equal residual depths (a-u)_+ and (b-v)_+. At common depth j > 0, taking discrete logs gives one class of slopes D/C modulo ell^j; both reduced logs are units in the cyclic group of order ell^j. At equal depth zero, this coordinate imposes no restriction. Thus in strata without any unrestricted row at this coordinate, the sum of 1/phi(ell^j) over active rows must be at least one to cover the slopes. For a,b positive and primitive strata with min(u,v)=0, a row can contribute to only the difference v-u=b-a. Avoiding a collision by this test works without assuming an ordinary lift. If q is common Wieferich and q divides n exactly once, every collision modulo q also gives exact valuation one: both powers and the sign lie in the order-(q-1) subgroup modulo q², on which reduction is injective.

## Appending ordinary rows

Assume n = 9 modulo 24. Reserve compatible odd prime-power coordinates that separate the two projections at every zero reader, and impose c odd, c >= 1. If each added ordinary row p > 5 has a base g with g^(p-1) not congruent to 1 modulo p² and an unrestricted exponent at its own p-coordinate, repair these rows in increasing order. On that exponent move by L t, with L a multiple of p-1 and of all period or reservation moduli that must be held fixed. Earlier cube-order periods have prime factors below p, and the hypothesis excludes a reservation on this exponent at p, so p does not divide L. If the remainder is a unit at p, take t=0. Otherwise the two successive base-p digits of t select the unique residue p² modulo p³, by the unit first derivative. Later repairs preserve it. The remainder is 1 modulo 4 and a unit at 3, so these rows are also safe. This proves a panel statement after arbitrary period shifts, regardless of whether the admissible exponents fit below a prescribed target.

## Replay

At the existing pinned target, c=1,d=0 already passes the seven listed rows. Only two of the 54 unit slopes modulo 81 remain candidates for a zero collision; the independent explicit repair loop below completes the other 52 slopes at the same target. All four actual zero readers are ordinary as primes; none is being claimed to be a common Wieferich prime. The final separate positive target is a genuine two-square witness for an 11-to-1783 one-axis repair.

```python
from math import gcd, isqrt, lcm, prod

Q = 11419697846380955982026777206637491
zero = (1783, 5023, Q, 163)
ordinary = (19, 271, 4159)
chain = (1838773, 871578403, 1770336106919153, 584210915283320491,
         143715885159696840787, Q)
for p in (11, 19, 163, 271, 1783, 4159, 5023, chain[0]):
    assert all(p % d for d in range(2, isqrt(p) + 1))
for p, t in zip(chain, chain[1:]):
    assert p*p > t and (t-1) % p == 0 and pow(2, t-1, t) == 1
    assert gcd(pow(2, (t-1)//p, t)-1, t) == 1

def primary(base, p, ell):
    m = p-1
    while m % ell == 0:
        m //= ell
    z = pow(base, m, p)
    j = 0
    while pow(z, ell**j, p) != 1:
        j += 1
    return z, j

assert [(primary(3,p,3)[1], primary(5,p,3)[1]) for p in zero] == [
    (3,4), (4,4), (4,4), (4,3)]
assert [t for t in range(81) if t%3 and any(
    primary(3,p,3)[0] == pow(primary(5,p,3)[0],t,p)
    for p in zero)] == [41,46]
assert all(pow(g,p-1,p*p) != 1 for p in zero+ordinary for g in (3,5))

P = prod(zero[:-1]+ordinary)
c = 27*lcm(11,31,70491962014697259148313439547145)*P
A, k = 18*P, 163
S = 56*k*c
pairs = [(9,24),(pow(3,c,19**2),19**2)] + [(p,p*p) for p in zero[:-1]]
pairs += [(pow(3,c,p*p)+pow(5,A*i,p*p)+p,p*p)
          for i,p in enumerate((271,4159),1)]
pairs += [(pow(3,c+S,k*k)+1+k,k*k)]
M = prod(m for _,m in pairs)
n = sum(z*(M//m)*pow(M//m,-1,m) for z,m in pairs) % M
assert n > 4 and all((n-4)%p for p in zero+ordinary)


# Complete all 52 usable slopes on the same original pinned target.
for slope in range(81):
    if slope%3 == 0 or slope in (41,46):
        continue
    C,D,L = 1,slope,162
    for p in sorted(ordinary):
        L=lcm(L,p-1)
        assert L%p
        m=p**3
        E=pow(5,D,m)
        r=(n-pow(3,C,m)-E)%m
        if r%p == 0:
            h=pow(5,L,m)
            k=(E*(h-1)//p)%p
            t=(r//p)*pow(k,-1,p)%p
            r=(r-E*(pow(h,t,m)-1))%m
            assert r%(p*p)==0
            t+=p*((r//(p*p)-1)*pow(k,-1,p)%p)
            D+=L*t
        L=lcm(L,(p-1)*p*p)
    assert D%81==slope
    assert all((n-pow(3,C,p)-pow(5,D,p))%p for p in zero)
    for p in ordinary:
        r=(n-pow(3,C,p**3)-pow(5,D,p**3))%p**3
        assert r%p or r==p*p
print("All 52 explicit completions independently replayed")

p, q = 11, 1783
assert [primary(g,q,p)[1] for g in (3,5)] == [1,0]
assert [pow(g,p-1,p*p) for g in (3,5)] == [1,78]
offset = 3 + 5**1070
n = offset + 67202650537**2 + 93090084098**2
assert n%24 == 9 and n%q**2 == 0
assert (n-4)%p**3 == p and (n-offset)%p**3 == p*p
assert (n-offset)%q != 0
print("52 safe slopes, pinned low anchor, exact one-axis norm repair")
```
