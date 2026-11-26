# Classification of quadratic height for a finite choice of child labels

Fix a parent label with shift A, and a finite nonempty list of child labels with residuals S_j=5(m−A)+K_j. Fix the progression m≡A mod p, where the variable p is an inert prime not dividing the nonzero K_j. The finite menu has a uniform O(p²) bound for a strictly positive true bridge for all sufficiently large p **if and only if** some K_j is zero or a positive sum of two squares.

Proof: Any positive parent norm ≤Cp² must be Tp² with T a positive integral sum of two squares and T≤C. For a fixed such T let a=5T. If K_j=0 then a x² is always a norm. If aK_j is a positive square, a=D u² and K_j=D v² with the same squarefree D, a norm itself; then a x²+K_j=D((u x)²+v²) is always a norm. A positive shift K_j admits such a T precisely when K_j is a norm; one may use the squarefree part of 5K_j. These choices give the upper bound with m=A+Tp².

For any remaining pair (T,j), choose an auxiliary inert q not dividing 2aK_j where aK_j is a quadratic nonresidue. Such q exist plentifully by the biquadratic splitting criterion for Q(sqrt(aK_j)) and Q(i), or by quadratic reciprocity and Dirichlet. If the squareclass of aK_j is −1 the two fields are equal and both nonresidue conditions already coincide. At q, −K_j/a is a nonzero square, giving a simple root of a x²+K_j. Choose a lift of that root modulo q² with valuation exactly one. Choose the auxiliary q distinct over every (T,j) in the finite range T≤C. CRT with p≡3 mod 4 gives a reduced class for p, so by Dirichlet it contains infinitely many primes. This forces every candidate in the fixed range to fail. Nevertheless at p itself each child passes at the same m=A+p², since p² is a square and 5p²+K_j is a unit. For the no-exception direction all K_j are nonzero.

Actual control: take (d,c)=(0,0), e=1, r=1. Child exponents f=1,2 give K=3,−3, and can have simultaneous finite obstruction. At p=11,T=1, their residuals hit 19 and 7 respectively to valuation one. At p=19 and T=1 both residuals are actual norms, illustrating that the obstruction is along chosen prime classes, not every prime. Restoring f=0 in the **same** child column gives K=5 and a permanent bridge:
```python
for K,q in [(3,19),(-3,7)]:
    assert (5*11**2+K) % q**2 in range(q,q*q,q)
assert 5*19**2+3 == 28**2+32**2
assert 5*19**2-3 == 11**2+41**2
for p in [3,7,11,19]:
    assert 5*p*p+5 == (2*p-1)**2+(p+2)**2
```
The finite-menu analysis does not classify a genuine entire child column with unbounded f or resolve A303656. No novelty claim is made.
