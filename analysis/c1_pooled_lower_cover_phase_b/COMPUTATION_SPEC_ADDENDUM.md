# Pre-run addendum: conditional order-closed seed construction

This addendum does not alter COMPUTATION_SPEC.md or its original scope.
It is frozen before running the added tests below.

Theorem target: a single nonregular terminal prime q whose recursively required
odd order-coordinate set T consists entirely of regular admitted primes, with
squarefree odd part of U=lcm(w_q,{w_p:p in T}), yields a complete odd pooled
cover at K=2,E={1} by r_p=2 (p in T), r_q=2+q. No existence of such q is
asserted. A full two-anchor certificate is not obtained: (c,d)=(1,0) escapes.

Frozen arithmetic skeleton for checking the regular part of this conditional
construction: T={3,7,31}, externally prescribed U=1302=2*3*7*31, r_p=2.
These actual rows alone induce U=6, not 1302; hence the experiment is explicitly
an externally supported arithmetic skeleton, not a complete admitted system.
The terminal nonregular q is NOT supplied and NOT simulated as an actual prime.
Test every exponent modulo 1302 and the exact common escape set.

Classify the existing three nonregular primes against the seed conditions;
do not enlarge a prime cutoff or search for new terminal primes.
