# Frozen targeted computation specification

Authority: main 3fb4b4b4f71018017c7ea014ae7a1380f27b6b94; tree 5ee6ab9e51f3e6d471991b7407de193d12777882.
No GitHub writes, no prime scan.

1. Verify primality, exact base-5 orders and lifting exponents of the named primes
   3, 7, 11, 19, 31, 67, 20771, 40487.
2. On actual roots 20771 and 40487 (K=2,E={1}), construct two exponent fibers
   over the shared regular relay 31, with original row 3 safe; test all 961
   shared residues of row 31. Each fiber is to have exactly one active rigid
   root cylinder, at distinct 31-centers. Confirm individual feasibility and
   global incompatibility by direct modular evaluations, not independent
   anchor choices.
3. Test the regular shared-center congruence theorem for small primes and
   both anchor roles, including unequal precision requirements.
4. Compute exact multi-use resultants for fixed h,Y cases, with particular
   focus on the existing actual q=20771 paired lower classes Y=7,8,162 at h=67.
   Benchmark h=3,5,7 before any h=67 calculation. Compute actual integer gcds
   if the benchmark supports it. Do not use a derived macro rank as original h.
5. Validate exact two-root trace / separator criteria on small finite arithmetic
   fixtures. Label conditional or abstract fixtures explicitly. Do not invent
   actual nonregular primes, or claim a complete cover from partial fibers.
6. Preserve the actual Phase C fractional gap as a regression; optionally embed
   it in an exactly-two-nonregular family with frozen nonregular zero masks.

Theorems are analytic deductions. Finite checks do not establish unbounded
prime inventory, independent proof review, or repository-native replay.
