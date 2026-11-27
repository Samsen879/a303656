# Fixed polynomial menus: an exact fresh-prime obstruction

This is a project lemma assembled from standard norm factorization, Chebotarev, and CRT. No originality or priority claim is made. It is about a **fixed finite menu**, not the entire growing A303656 exponent range.

## Statement

Fix an arithmetic progression of positive integers and finitely many labels. Each label requires every polynomial in a finite list of nonzero polynomials in ℤ[t], eventually positive, to be a sum of two integer squares at the same t. Factor each polynomial over ℚ into its leading scalar and monic irreducibles.

* Drop any label having a row with no irreducible factor of odd multiplicity that remains irreducible over ℚ(i), but with a leading scalar that is not a norm from ℚ(i). That row never gives a nonzero norm.
* For each remaining label form the set of monic factors that remain irreducible over ℚ(i) and occur to odd multiplicity in at least one of its rows. If there is an empty set, that label succeeds at every sufficiently large t.
* Otherwise some subprogression of every starting progression blocks the entire menu, and the success set of the fixed menu has density zero in the starting progression. The minimum number of **fresh inert primes outside the finite excluded set below** needed to block these remaining labels at a common t by odd valuations is exactly the minimum number of factors meeting all their sets.

## Proof

An irreducible monic polynomial over ℚ that splits over ℚ(i) splits into two conjugate factors, hence is a Gaussian rational polynomial norm. Even powers also are norms. This gives the scalar and empty-set cases, using the usual sum-of-two-squares criterion to pass from a rational norm that is a positive integer to an integer norm.

Exclude 2, the prime divisors of the initial modulus, the numerators and denominators of scalars, and primes of bad reduction for the factors, their discriminants, and their pairwise resultants. Let f be a listed factor and temporarily work in a Galois field containing its roots and i. As f remains irreducible over ℚ(i), a root field does not contain i. Its root stabilizer therefore contains an element acting nontrivially on i. Chebotarev yields a positive density of inert primes where f has a simple root. For each factor in a hitting set choose a distinct such prime. Lift the root to a class modulo p² other than the unique lift giving divisibility by p². Resultants ensure no other factor vanishes there. CRT imposes all these classes at once and preserves the original progression. Every hit label now has an odd inert valuation in one row. Conversely, each allowed prime can hit at most one distinct factor at a common t, so blocking all labels must hit all the factor sets.

For density zero, fix any one listed factor in a label. On the positively dense eligible primes just described, at least (p−1)/p² of the classes modulo p² have valuation exactly one at this factor. The corresponding local exclusions for any finite collection multiply by CRT, relative to the initial progression. Their excluded fractions have divergent sum by Chebotarev and partial summation, so the products of surviving fractions tend to zero. A finite union over labels still has density zero. This does not produce an asymptotic for menus whose labels vary with t.

## Exact controls

1. Take the three single-row labels (t²+3)(t²+1), (t²+3)(t²+2), and t²+2. The factor sets require both t²+3 and t²+2. At t≡2060 mod 5929 = 7²·11², their valuations at 7 and 11 respectively are exactly one. In contrast, the row (t²+3)² is always a norm and cannot be removed by this test.
2. In the quartic A303656 family, take b=4663+372438k, s=5b+2, T=(s²+3081)/10; put g=T²+2, m=5g+2, n=5m+4. The parent and child residuals are rational norm multiples of H(s)=(s²+3081)²+K with K=20(12−3^c−5^d) and K=4(64−3^f−5^e), respectively. A monic Gaussian factor of H can be taken as s²+ias+q+ir with a,q,r rational; comparing the linear coefficient forces ar=0. Comparing the other coefficients gives precisely: K is a nonnegative integer square, or q²=3081²+K and 2(3081−q) is an integer square for some integer q. Exhausting the possible 107 parent pairs and 138 child pairs leaves only parent (c,d)=(1,4) and children (f,e)=(1,2),(3,0) as polynomial norms. None are adjacent under e=d or d+1. The affine change from k to s is invertible over ℚ, so the fixed-menu result applies to any starting k progression. The grandparent-column 0 and child-column 2 retain the identity n=(5T)²+6²+3+25. **Thus a fixed one-layer menu can be blocked while the two-layer witness survives, but other one-layer labels can still survive at the same integer.**

Primary reference for the Chebotarev input: [Serre, Quelques applications du théorème de densité de Chebotarev](https://numdam.org/articles/10.1007/BF02698692/).
