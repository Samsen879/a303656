# Squarefree overlap for any fixed family of rationally rotated sectors

Use the shifts, dyadic interval, and subcritical width \(X^{-1/2+\epsilon}\le w=o((\log X)^{-2})\) in [the two-sector note](THIN_SECTOR_ROTATION_CORRELATION.md). Consider finitely many distinct Gaussian rational unit rotations of a reference thin sector, with the identity included. Rotate within disjoint thin sectors (the reference orientation can be changed when analyzing a subset). Let \(B\asymp Xw(\log X)^2\) denote the common one-sector coordinate-count main term. For each rotation write \(\rho_j=\alpha_j/\beta_j\) reduced over \(\mathbb Z[i]\), and let \(\beta\) be a Gaussian lcm of the denominators. The number of actual integers hit by all sectors, each with some squarefree norm residual, is
\[
  (f(N\beta)+o(1))B,\qquad
  f(D)=\begin{cases}\prod_{p\mid D}(p+2)^{-1},&D\text{ squarefree},\\
  0,&\text{otherwise}.\end{cases}
\]

At a fixed shift, a single reference coordinate \(z\) gives an exactly rotated tuple iff \(z\) lies in the intersection of denominator lattices, equal to \(\beta\mathbb Z[i]\). This is the Gaussian case of [Baake and Grimm's multiple coincidence construction](https://oro.open.ac.uk/5815/1/multico.pdf). Now condition on squarefreeness: if the denominator norm has a rational square factor no tuple in the lattice has squarefree norm. Otherwise the same finite CRT count and squarefree tail bound as in the two-sector proof give the factor \(1/(p+2)\) for each distinct forced Gaussian prime above \(p\). To pass from coordinates to actual integers, any integer hit in all sectors but not by a common rotated tuple must have a nonmatching pair between the reference and at least one other sector. A finite union of the two-sector estimates costs only \(o(B)\); repeated reference witnesses cost \(o(B)\) also. Nothing here treats a family whose size grows with \(X\).

For a split prime \(p=\pi\bar\pi\), write \(e_j=v_\pi(\rho_j)\); then \(v_{\bar\pi}(\rho_j)=-e_j\). The exponent of \(p\) in \(N\beta\) is \(\max_j e_j-\min_j e_j\), since the identity has exponent zero. The corresponding exponent in the norm of the reduced denominator of \(\rho_j/\rho_k\) is \(|e_j-e_k|\). Thus nonzero joint leading term is equivalent to squarefree denominator norm for **every** pairwise relative rotation. Nevertheless the joint coefficient does not multiply pairwise coefficients: a shared prime counts once. Applying the formula to subsets and inclusion–exclusion counts actual exact membership patterns with at least one required sector, up to \(o(B)\). It does not answer the small fixed critical-width distinct-shift question.

## Exact four-sector witness and incompatibility control

At \(X=2^{19}\), \(w=1/32\), and shift 32, the integer 539077 has residual \(539045=5\cdot13\cdot8293\). Its four rotated coordinates correspond to \(1,(4+3i)/5,(12+5i)/13,(33+56i)/65\). The four-way coefficient is \(1/(7\cdot15)=1/105\). In contrast both \((4+3i)/5\) and \((3+4i)/5\) separately have coefficient \(1/7\) against the axis, but the relative rotation is \((24-7i)/25\), of reduced Gaussian denominator norm 25, so those three together have zero leading term.

```python
from math import isqrt
n=539077
assert n-(3**3+5)==5*13*8293
assert all(8293%d for d in range(2,isqrt(8293)+1))
for u,v,D,a,b in [(1,0,1,734,17),(4,3,5,577,454),
                  (12,5,13,671,298),(33,56,65,358,641)]:
    assert a*a+b*b==n-32
    assert (D*a,D*b)==(734*u-17*v,734*v+17*u)
    assert 0<=32*(u*b-v*a)<u*a+v*b
for p,u,v in [(5,2,1),(13,3,2)]:
    all_good=joint=0
    for a in range(p*p):
        for b in range(p*p):
            if (a*a+b*b)%(p*p):
                all_good+=1
                joint+=(u*a+v*b)%p==0
    assert (all_good,joint)==({5:(560,80),13:(28080,1872)}[p])
```
