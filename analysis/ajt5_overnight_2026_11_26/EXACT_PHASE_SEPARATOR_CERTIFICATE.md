# Exact phase separators and an actual lock requiring two coordinates

Use the [fixed-phase lifting interface](FIXED_PANEL_EVEN_VALUATION_CONSTRUCTION.md). Treat the parity and 3-adic seed first and use positive actual exponents when reporting a witness. For remaining inert primes \(p\), let \(L_b,o_{b,p},s_{b,p},t_p\) be as in that interface. The pre-lift test at \(p\) rejects exactly when the residue modulo \(p^{t_p}\) is nonzero of odd valuation. The test reads the exponent of base \(b\) modulo
\[
 m_{b,p}=o_{b,p}p^{\max(0,t_p-s_{b,p})}.
\]
This is the exact order of \(b\) modulo \(p^{t_p}\) by LTE. In particular rows with \(t_p=1\) never reject a pre-lift phase: a zero residue there must still be lifted later.

Split the two exponent residues into prime-power coordinates by CRT, retaining fixed seed digits as restrictions. Form a graph on these coordinates, joining those appearing in the same row test. A tree decomposition with each row assigned to a bag containing its coordinates gives an exact feasibility algorithm. For each bag, enumerate its assignments and send its parent the set of separator assignments having an extension satisfying all assigned and descendant tests. This is exact by induction: below a separator, different descendant subtrees share no unrecorded coordinate. An empty root table certifies failure for that seed, without asserting failure for other seeds. Conversely accepted assignments are passed to the ordinary simultaneous lift; their height must still be checked. If every bag domain has product at most \(D\), each bag visits at most \(D\) assignments, with local tests and child lookups counted at that scale. There is no general bound here on the necessary \(D\) or on the height of a usable lift.

For a single free exponent coordinate at \(\ell\), with all other coordinates fixed, a different-prime row \(p\ne\ell\) has at most one forbidden congruence cylinder: modulo \(p\), injectivity on the available \(\ell\)-part of the order gives at most one exponent class causing a collision, and on that class the value modulo \(p^{t_p}\) is constant. This is because the order growth from \(p\) to \(p^{t_p}\) is a power of \(p\), not \(\ell\). Such cylinders can be counted by containment and disjointness rather than enumerating the full coordinate. The row at \(p=\ell\) can depend on finer digits and is not covered by this simplification.

## An exact two-coordinate lock

Take \(Q=\{7,43,431\}\). The two orders at these primes are respectively \((6,6),(42,42),(43,215)\), and all six initial lift depths are one. Thus \(L_3=1806,\ L_5=27090\) and the pre-lift depths are \(2,2,1\). Define
\[
 a=169150261+234294186\cdot3^{1806},\quad n=3^{1432}+5^{3655}+a^2 .
\]
Fix \(d=3655\), and let \(c\) range over the least representatives with \(c\equiv4+6u\bmod42,\ c\equiv z\bmod43,\ 0\le u<7,\ 0\le z<43\). All 301 rows are active. The depth-two test at 7 passes exactly when \(u=0\); the one at 43 passes exactly when \(u\ne0\) or \(z=13\). Direct powering modulo \(7^2,43^2\) verifies both statements. Thus from \((1,0)\) neither a change of \(u\) alone nor a change of \(z\) alone can pass. At frozen \(z=0\), deleting either of the two tests restores a feasible point. Jointly there is a unique passing cell \((0,13)\), with \(c=1432\), whose true remainder is \(a^2\). The 43 row has extension counts \((1,43,43,43,43,43,43)\) after eliminating \(z\); its separator message alone is full, even though freezing the other coordinate creates a lock.
