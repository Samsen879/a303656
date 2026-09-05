# Frozen independent computation specification
Base: 0200beede923c56e0284d9555c1dabaf91fa1755; tree 23f10c12181c5caa394f7a3fb1acb6e79cc02fe6.
No GitHub writes. No repository program is imported or used as a computational kernel.

1. Complete order signatures at coordinate ell=3, exact depths d=1,2,3, with no bound on q. Factor Phi_(3^d)(5) and Phi_(2*3^d)(5) completely. Verify products and primality independently by trial division (factors expected small; otherwise produce certificates). Test multiplicative order and s for every admitted factor. Benchmark d=1 before remaining cases. Output exact factor identities and a completeness proof; this is not a prime-size scan.
2. Reproduce the existing q<=10^7 admitted-prime panel, not extend it. Benchmark q<=10^5 first. Independently sieve and reduce orders, compare counts for ell=3,67 depths1..3, and all nonregular hits. Store integer output plus timings. Do not infer universal absence from this panel.
3. Enumerate paired positions of q=20771 and 40487 by independent modular power tables. For each q, h=ell^d, u=w/h, retain only pairs b0=b1 mod u and 5^b0-5^b1=2 mod q. Output each lower class's exact directed pairs in the ordinary CRT coordinate b mod h, full-pair totals, diagonal exclusions, and matching properties. Cross-check pairs by direct modular evaluation.
4. Exhaustively check fixed-cylinder capacity recurrence and corrected branch inequalities for ell=3,beta=2, all 4096 subsets. Construct explicit abstract and actual-row counterexamples, keeping classifications separate.
5. Do not extend q_max or depths adaptively in this phase. New results are theorem-driven: cyclotomic finite signatures, finite support certificates, and position-sensitive resource bounds.

## Theorem-driven supplement, frozen before execution
For odd h, simultaneous lower-Y activation forces a prime divisor of the nonzero integer Res(T^h-5^(Y*h),(T-2)^h-5^(Y*h)). This follows from coset membership and the absence of two complex odd-order roots of unity with nonzero real difference. Freeze the exact additional domain Y=0 and h=3,5,7,9; benchmark h=3; factor the four resultants, certify all factors, and test the actual order and nonregularity. No extension to larger h is authorized in this phase.
