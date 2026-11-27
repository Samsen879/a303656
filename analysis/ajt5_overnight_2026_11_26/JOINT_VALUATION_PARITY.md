# Exact joint valuation parity on a finite root menu

Fix a prime p, an initial residue ball in Z_p, and a finite list of integer roots. Return each vector of finite even (E), finite odd (O), and exact equality (Z), with its conditional Haar mass. Coincident roots share a state; roots outside the initial ball have constant finite valuation throughout that ball. Each equality state is a single point of mass zero and must still be checked for pointwise assertions.

## Proof and construction

At a residue ball of depth d containing roots, split into its p child balls. If a child contains no root, every root still in the parent ball has valuation exactly d throughout that child, and the other coordinates already have fixed values. Aggregate all empty children as one contribution with relative weight (p minus the number of occupied children)/p. Recurse only on occupied children, each of weight 1/p. Equal roots can be stored once and expanded at the end.

Compress every run with the same root cluster. A unary run entered at depth d contributes (1−1/p)p^(−j) of its entry mass from exits at depth d+j; sum separately for the two parities. At a single-root leaf the run is infinite, so these two relative masses are p/(p+1) and 1/(p+1), for the parity of d and its opposite. Also emit the equality point. For a cluster with more than one distinct root the first split is determined by the minimum valuation of the differences with one chosen root. Thus no arbitrary precision cutoff is needed. Aggregate contributions that give the same full vector. Per distinct cluster, including its final split, all exits yield at most two vectors, as they differ only by the common parity on that cluster. With k distinct roots inside the initial ball the compressed tree has at most 2k−1 clusters for k>0, giving at most 4k−2 positive-mass states and k equality states. With k=0 there is just one constant state.

For finitely many different primes, a choice of positive-mass states has an integer witness: choose one open cylinder per state, then apply CRT. Product Haar measure gives the product of local masses, also the natural density of the combined finite condition. Indeed the local states can be approximated by clopen cylinders with error confined to finitely many arbitrarily small root neighborhoods. Exact equality is instead a specified integer to be checked against every other constraint. None of these statements makes shared exponent variables independent or supplies an integer meeting infinitely many growing conditions.

## Controls

* At p=11, 3125−705 has valuation 2. If t shares their class modulo 121, both distances are divisible by 121 and at least one has valuation exactly 2. If both valuations are odd, they must therefore be 1. The third root 20307 has the same residue modulo 121 and then also has valuation 1. An equality point cannot satisfy the two old odd conditions.
* At p=83, condition on a ball containing five roots in separate children. The 78 empty children give all O. Each occupied child gives its one E with conditional probability 83/84 and otherwise all O, apart from equality. The combined weights are 79/84 all O and 1/84 for each single E. The companion script uses five simple representatives of those five child classes. It does not replay the full 28-prime window or validate its reported relative density.
* For any depth D, the inputs r+p^D and r+p^(D+1) agree modulo p^D yet have opposite valuation parity at r. Truncated residues without a tail rule cannot decide all joint point states.

This is a finite valuation tool, not a proof of an AJT5 bridge or of the original conjecture. No novelty or priority claim is made.
