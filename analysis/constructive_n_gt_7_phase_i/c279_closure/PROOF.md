# Certified arithmetic and architecture-specific closure

## 1. Two exact evaluations

For 279=3²·31, the closed formula is

    Phi_279(5) = (5^279-1)(5^3-1)/((5^93-1)(5^9-1)).

All divisions are exact. Independently, the primary checker recursively divides
5^d-1 by all previously computed Phi_e(5), e proper divisors of d, for every
d|279. The second checker evaluates the Möbius product by squarefree subsets
of {3,31}. Thus evaluation does not merely hash the supplied integer.

Both methods give C=

    647310534648447373054716179652933499827507406084233396665155828948791617392664703265092784874951801626592881977085113283203001

This is 126 digits, 418 bits. Decimal-plus-LF SHA256 is
`2754f9618901c35bbf9c9ba15f9f29c7c7f3c72facff3a1aab13ab03f97c36f2`.

## 2. Complete factor identity

    q1 = 247114592858611
    q2 = 2619475147786243221682441564765834085031894176855868169779152514905083781606453302669371739151283560390355875491

Exact multiplication gives C=q1*q2, with distinct q1,q2>1 and residual cofactor1.
Both primes are certified by the following self-contained rule, applied to
`PRIMALITY_CERTIFICATE.json`. No P112/PRP label is used.

## 3. Primality rule and complete dependency coverage

Let F>1 divide n-1 and have fully recursively certified prime factors. For each
prime p|F require a witness 1<a<n such that a^(n-1)=1 mod n and
gcd(a^((n-1)/p)-1,n)=1. For any prime ell|n these imply a has order dividing
n-1 modulo ell, but not dividing (n-1)/p. Hence the full p-primary part of
n-1 divides ell-1. In particular F|(ell-1), and every prime divisor ell>=F+1.
If F²>n this excludes compositeness, including repeated prime factors.

One recursive node uses the elementary cubic refinement: F³>n excludes three
prime factors counted with multiplicity. A composite n must therefore be
(aF+1)(bF+1) with positive integers a,b. If a+b>=F, then ab>=a+b-1>=F-1,
and n=abF²+(a+b)F+1>=F³+1, a contradiction. Thus a+b<F. Writing
(n-1)/F=sF+r, 0<=r<F, forces s=ab, r=a+b, so r²-4s=(a-b)².
A negative or nonsquare discriminant excludes the remaining composite case.
This is a fully proved Pocklington-style exclusion rule, not reliance on an
unidentified BLS/library extension or a newly invented project theorem.

The sole cubic node is

    T = 102890956671710346286076658204017777664223384154447947346031589165926965891317454792249
    F = 2^3 * 7 * 202325874913307 * 2056008495713304274609
      = 23295088192565643551027432342194029928
    s = 189604433124
    r = 12252126975341220670094228051570019619

Its F³>T and nonsquare r²-4s are verified with integer arithmetic/isqrt. All
other eight-node certificate dependencies use F²>n. Leaves terminate in full
trial division through integer sqrt, with leaf bound10^9. Each exponent,
divisibility, witness, gcd, bound and recursive dependency is checked.

The primary implementation is iterative/topological with built-in pow/gcd;
the second is recursive with its own repeated-squaring and Euclidean routines
and a separate trial-division loop. Neither imports producer functions or PASS
fields. Both rigorously certify q1 and q2; no probabilistic leaf exists.

## 4. Admission and exact orders

Both q_i are 3 mod4 and do not divide279. For each, 5^279=1 mod q_i,
5^93!=1 and 5^9!=1. Since the only prime divisors of279 are3 and31,
these prove ord_q_i(5)=279. Exact residues are in closure_result.json.

## 5. Valuations and squarefreeness

The complete distinct-prime product implies both valuations are exactly1.
Each checker also defensively checks division and nondivision by q_i²; the
second computes full valuations by repeated exact division. Each verifies
5^279!=1 mod q_i². There are no further prime divisors. Hence C is squarefree.

## 6. Exact Sq(279)

Merged INSTANTIATION_GATES.md defines Sq(t) as primes q with q≡3 mod4, q∤t,
ord_q(5)=t and q²|Phi_t(5). Both q_i fail the last condition, despite satisfying
the other four. Complete factorization excludes any other prime divisor.
Therefore Sq(279)=empty and its exact cardinality is0.

## 7. Frozen I7 corollary and non-implications

The existing I7 iff is an instantiation conjunction for this frozen (1,5,3)
architecture only. It necessarily requires |Sq(279)|>=3, and six other order
gates. Since0<3, that conjunction is false: the frozen I7 cannot instantiate.
No additional factorization or inherited exhaustive lower bound is needed.

This does NOT imply all N=9 architectures are impossible, nor general N>7 or
the C=1 formalism is impossible. It does not prove A303656 or supply an original
additive counterexample. It gives no conclusion about Sq(t) for the six other
orders. Those were not evaluated. No new architecture or route is promoted.
Overall PROJECT remains PAUSED; ACTIVE PROMOTED ROUTE NONE; A303656 UNRESOLVED.

Authority classification: candidate split is EXTERNAL FACTOR PROVENANCE plus
EXACT CERTIFICATION; both primalities are CERTIFIED ARITHMETIC FACTS;
squarefreeness and Sq279 emptiness are NEW CERTIFIED ARITHMETIC AUTHORITY;
frozen I7 closure is a NEW ARCHITECTURE-CLOSURE COROLLARY. General N=9/N>7
impossibility is NOT PROVED. Historical bounded OPEN remains historically true.
