# Frozen exact computation specification

Authority: Samsen879/a303656, repository ID 1333945235.
Bound main: 44e522dd6e88504e2b9829f0b27359e6c45a76ff.
Bound tree: 6a30565826c8f988bfbb85e4098b78b2992d290c.
All remote access is read-only. No repository implementation is imported.

## A. Arithmetic dependency closure (frozen before execution)
- Seeds: 1645333507; controls 20771 and 40487.
- For a seed and every recursively reached admitted label p, compute primality,
  the complete factorization of p-1, exact ord_p(5), and s_p.
- Recurse only through odd prime factors of ord_p(5) congruent to 3 mod 4.
  Record every other odd prime factor as an unadmitted terminal coordinate.
- Domain is this finite, strictly descending dependency closure, not a prime scan.
- Algorithm: deterministic trial division; modular exponentiation; exact integer
  divisions. Order certificate: 5^w = 1 mod p and 5^(w/l) != 1 mod p for
  every prime l dividing w. Valuation certificate: powers modulo p^s and p^(s+1).
- Output: results/arithmetic_closure.json, containing input seeds, per-prime
  certificates, admitted support edges, terminal factors, minimal panel and U.
- Stop: the finite worklist is empty. No q_max extension and no full-period
  enumeration. Abort rather than silently change domain if arithmetic fails.

## B. Finite capacitated Hall audit (frozen before execution)
- Graphs: labelled left sizes 1 through 5; right coordinates 3,5,7; each of
  the 2^(3n) incidence graphs, including isolated left and right vertices.
- Capacities: paired (1,2,3) and single-anchor (2,4,6).
- Objective: independently compare subset-Hall deficiency with a slot-expanded
  augmenting-path maximum matching; test all stated minimal-core identities.
- Output: results/hall_audit.json, exact case counts and mismatch counts.
- Stop: exhaust the stated finite domain; stop at first mismatch with witness.

## C. Later targeted computations
Any additional nontrivial domain must be written here before running it.
No claim of replaying upstream catalogs, CI, or entire upstream test suite.

## C1. Actual paired-digit audit (frozen before execution)
- Sole nonregular row: q=20771, w=10385, K=2, E={1}.
- Enumerate its w distinct powers modulo q once (a single-row logarithm table,
  not an exponent-product or complete-system period).
- For every r mod q having both anchor logarithms, record whether their first
  digits coincide at lambda=5,31,67. Count all such r exactly and save one
  least-r witness of each observed case.
- Choose the first high digit h in 0,1,2 avoiding both local-zero residues;
  certify both witnesses have exact valuation one modulo q^2.
- Output: results/paired_digits.json. Stop after the w table entries and all
  their difference-two lookups. No prime scan and no boundary full period.

## C2. Routed capacity and min-cut audit (frozen before execution)
- Abstract DAG: row labels 3,7,11,23,31,67 with edges
  3->empty, 7->3, 11->5, 23->11, 31->3, 67->11.
  These are actual odd order supports; row regularity is not promoted.
- Every subset P of these six labels and every mandatory-target subset T of P.
- Capacities paired and single. Compare terminal-slot matching to direct
  enumeration of all A subset P using |T\A|+capacity(odd_factors(A)\A).
- Check capacity contraction and route-forest loads for every passing case.
- Label T as arbitrary mandatory guard targets, NOT as actual nonregular rows.
- Output: results/route_audit.json. Stop after the finite domain is exhausted.

## C3. Absolute-terminal circuit signatures (frozen before execution)
- Core sizes m=1,...,100. Potential terminal primes are primes lambda<=m with
  lambda=1 mod4. Enumerate distinct terminal sets with sum(lambda-1)=m-1.
- This is a combinatorial list of possible signatures, NOT an inventory of
  actual nonregular primes or a proof of arithmetic realizability.
- Output: results/terminal_signatures.json. Stop after size 100.

## C4. One actual boundary escape, without period enumeration (frozen)
- P={3,1523,30469139,1645333507}, all K=2 and E={1}; no two-adic row.
- Shared residues: r_3=r_1523=r_30469139=2, r_q=q+2.
- CRT exponent constraints: d=0 mod 2,27,1523; d=1 mod 761,1429,30469139.
- Objective: certify both rigid classes of q, all actual rows' two-anchor
  valuations at one CRT exponent, exact U=L, and one compatible global residue.
- Output: results/boundary_escape.json. Stop after this single CRT solution
  and its eight modular row evaluations. No iteration through U or L.

## C5. Boundary-primed coordinate-3 theorem (frozen before execution)
- For K_2=2,...,9, all r_2 modulo 2^K_2 and r_3 modulo 3, construct
  an anchor and exponent boundary that is two-square-safe and NOT divisible
  by 3 at that anchor. Compare against directly enumerated sums of two
  square residues (not the odd-part criterion used in the proof).
- 3*(4+8+...+512)=3060 boundary cases. No other row parameters are scanned.
- On every subset P of {3,7,11,23,31,67} and every T subset P\{3},
  repeat the single-anchor terminal matching/min-cut/route audit treating
  3 as a pre-inactivated row, hence a terminal of capacity 2.
- Output: results/primed_three.json. Stop at first mismatch or exhaustion.

## C6. Boundary-primed absolute terminal signatures (frozen before execution)
- m=1,...,100. Candidate terminals are 3 and primes lambda=1 mod4, lambda<=m.
- Enumerate nonempty distinct terminal sets with sum(lambda-1)=m-1.
- Recompute seed terminal frontiers, stopping at 3 rather than discarding it.
- These signatures classify necessary capacity profiles, not realized
  nonregular-prime families. Output: results/primed_terminal_signatures.json.

## C7. Six-nonregular-row universal obstruction (frozen before execution)
- Certify the complete shallow gateway inventories:
  ord in {3,6,9,18} from Phi_3, Phi_6, Phi_9, Phi_18 at 5;
  ord in {5,10} from Phi_5, Phi_10 at 5.
- Compute exact polynomial values, complete trial-division factorizations,
  admitted filters, exact orders and regularity. No prime scan.
- Enumerate (a,b,k) of nonnegative integers with a+b+k<=6, where a roots
  have absolute terminal set {3}, b have {5}, k have {3,5}.
- Verify an allocation x of mixed roots to 3 and k-x to 5 makes both
  exact guard-union upper bounds strictly less than 1. Other roots choose
  a terminal >=13. Internal/admitted missing-terminal primes are >=7.
- Output: results/six_row_obstruction.json, including all 84 integer cases.
- Stop after these six cyclotomic identities and 84 allocations.
