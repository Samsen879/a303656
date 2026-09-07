# Phase C targeted reference computation — frozen before execution

Repository basis: Samsen879/a303656 main 71b8d428b32724c37e593bcfd9d5f06a42e72d21,
tree 5609e47eed0c058c190ef59c61644e2fd4b8fad6. GitHub read-only.

Theorem gate: with at most 12 original nonregular roots, an absolute terminal
at least 13 admits a descending path confined to coordinates at least 13.
The small-coordinate problem is therefore concentrated on terminal set {3,5}.
An inclusion-minimal terminal Hall circuit has m=1+sum(lambda-1), deg(lambda)>=lambda.
These statements will be proved in the report, not inferred from enumerations.

Exact finite targets:
1. Enumerate absolute terminal signatures with circuit size at most 19.
2. Enumerate terminal-type counts a,b,k with total at most 12 and the exact rational
   six-root gateway budget; distinguish success of a sufficient bound from true escape.
3. Verify selected cyclotomic values at n=3,6,9,18,27,54,81,162,5,10,25,50,7,14,11,22.
   The n=81,162 large factors are source-supplied candidates; verify product, exact orders,
   nonregularity and recursive full n-1 Lucas primality certificates. No PRP-only conclusion.
4. Verify the three source-supplied nonregular primes and their entire absolute order-DAG
   closures. No new prime-range scan, no claim to rerun the q<=2e9 inventory.
5. Enumerate complete p-ary frontier profiles with at most 12 leaves for p=3,5,7,11.
6. Test exact small Hall circuits by subset enumeration, including circuits properly inside Q.
7. Verify any explicit local countermodel or gateway-position witness introduced in the report.

Discovery factorization may use SymPy, but the final arithmetic verifier uses integer
identities, recursively certified primes, modular powers, and exact rational arithmetic.
No floating-point decision. No repository code imported. No GitHub writes.

A finite result is evidence only in the listed domain. The full arithmetic seven-root
existence/nonexistence question is not made finite by this specification.

Theorem-gated extension before its execution: in a seven-seed rank-5 nonlinear
step every minimal 5-frontier has five depth-one leaves. If the rank-3 residual
covers with at most four clauses, its irredundant frontier has three depth-one
leaves. A mixed least-helper relevant at joint depths (1,1) must have order 15
or 30. Add exactly n=15,30 to the factorization targets.

Second extension before execution: to test whether the new depth-(1,1) cross-strip
obstruction extends to 8--12 roots, the first new mixed rectangle can have ternary
depth 2 and quinary depth 1. Its least-helper exact order is 45 or 90. Add only
n=45,90; these tests do not imply that all possible indices have been bounded.
