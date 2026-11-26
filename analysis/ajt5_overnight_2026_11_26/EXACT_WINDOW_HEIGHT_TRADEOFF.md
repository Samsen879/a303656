# Short exponents versus activation height in the sparse construction

This is a quantitative supplement to SPARSE_SHARED_EXPONENT_PROTECTION.md. For a finite panel of K selected primes, fix m≡2 mod 11 and c=0. Choose d_0∈{0,5,…,600} with v_11(m−1−5^d_0)=2, as given by the finite check in the main note. Put d=d_0+605t, preserving that valuation.

For q_k of orbit length o_k, there are at most b_k=2(k+7)^2 prohibited classes of t mod o_k, counting both new endpoints and the available offset factors. In H consecutive integers they hit at most H b_k/o_k+b_k times. Thus, writing B=sum b_k and rho=sum b_k/o_k, any H=floor(B/(1−rho))+1 consecutive integers contain a survivor. In particular rho≤1/2, so taking the interval starting at zero yields
```
d ≤ 600 + 2420 sum_{k=1}^K (k+7)^2 .
```
This witness avoids every q-contact without requiring independence or computing their common period. The proof does not bound the least positive integer m having all these rows activated.

Indeed, with U,W the two maximal offsets, strict activation of the whole old window requires m>3^(U+c)+5^(W+d+10). Even if synchronization is implemented with actual orders instead of q_k−1, its positive offset w added at stage K is a multiple of 605 and satisfies 5^w≡1 mod every q_k through stage K. Hence 605·lcm(o_1,…,o_K) divides w. In particular
```
log_5 m > W+10 ≥ 2420·2^K·(K+7)^2 + 10 .
```
This lower bound applies to this particular synchronization recipe, not to arbitrary shared-exponent sieves. It exposes why small starting exponents or positive Haar mass leave the original short, unshifted exponent box unaddressed.
