# Elementary and effective refinements of the fixed-label height obstruction

Use the same real AJT edge R=m−2, S=5R+3 as in SUPERQUADRATIC_FIXED_LABEL_OBSTRUCTION.md. For an inert prime p>3, every positive bridge in m≡2 mod p has R=Tp² with T a positive integral sum of two squares. Hence a bound O(p²) is equivalent to one finite menu of such T working for every sufficiently large p.

**Elementary auxiliary primes.** If 3|T then 9|T, and S has valuation 1 at 3. Otherwise choose an even s coprime to 3 and divisible by each non-3 prime already used. The integer 5Ts²+3 is 3 mod 4, not divisible by 3, and coprime to all the already used non-3 primes. Thus some fresh inert q divides it to odd valuation. Its residue s is nonzero mod q and gives a simple root of 5T x²+3. Choose a lift modulo q² of exact valuation 1. This replaces the splitting-prime theorem for auxiliary q; Dirichlet's theorem is still needed to take p prime in the combined reduced class. It also allows any previously fixed reduced AP for p compatible with p≡3 mod 4 to be retained.

**Quantitative refinement.** For an integer B≥2 consider only positive norms T≤B with 3 not dividing T. Choose a prime ℓ in (5B,10B). Let D_T be the product of distinct odd split primes dividing 5T. For each T impose q_T≡7 mod 24, q_T≡1 mod D_T, and q_T≡B+T mod ℓ. These form a reduced class of modulus O(B²), and give mutually distinct q_T>B. By quadratic reciprocity, (5T/q_T)=1: split prime factors have symbol 1, odd inert prime factors have even exponents, and the symbol of 2 is 1. Also (−3/q_T)=1. Thus every chosen q_T has a nonzero simple root for the auxiliary polynomial. Linnik's theorem gives choices q_T=B^O(1). Apply the theorem a second time to the reduced combined class, including p≡7 mod 12, to obtain p_B>3 with log p_B=O(B sqrt(log B)); here the classical two-square counting bound O(B/sqrt(log B)) bounds the number of menu items. The chosen p_B cannot repeat indefinitely: each fixed prime has a true positive bridge, by taking u²+v²≡3 mod p with primitive lift (u odd, v even, and 5∤2u+v) and solving (2u+v)a+(2v−u)b=(3−u²−v²)/(2p). The parent (pa,pb) and child (2pa−pb+u,pa+2pb+v) are valid coordinates. A primitive lift exists by fixing a nonzero odd u in its mod-p class and avoiding a zero residue of v at every prime divisor of u other than 5 and p; the latter primes already have the required restrictions. Thus along an unbounded subsequence the true minimum satisfies H(p_B) ≫ p_B² log(p_B)/sqrt(log log(p_B)). This still asserts no fixed power gain.

```python
from math import isqrt
def two(n):
    return any(isqrt(n-a*a)**2 == n-a*a for a in range(isqrt(n//2)+1))
p = 743671
assert p % 4 == 3 and all(p%d for d in range(2,isqrt(p)+1))
for a,q in [(1,19),(2,11),(9,3)]:
    assert (5*a*p*p+3) % (q*q) in range(q,q*q,q)
assert all(not two(a) or not two(5*a*23**2+3) for a in range(1,13))
assert 6879-2 == 46**2+69**2 and 5*6879-7 == 52**2+178**2
```

Scope: a single fixed label; neither unrelated candidate labels nor entire menus are excluded. No priority claim is made.
