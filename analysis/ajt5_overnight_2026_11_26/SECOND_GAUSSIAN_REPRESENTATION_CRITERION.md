# A prime criterion for a second Gaussian representation

Let \(C\) be a positive power of \(5\) and \(h\equiv2\bmod4\) with \(5\nmid h\). Write \(N=C^2+h^2\). Allowing signed \(L,k\), the conditions
\[
 N=L^2+25k^2,\qquad L\equiv C\bmod16,\qquad k\equiv2\bmod4
\]
hold for some \(L,k\) if and only if \(N\) has a prime divisor \(13\) or \(17\bmod20\). This criterion applies to an auxiliary Gaussian representation when one true square has been fixed in the shared-height analysis. It does not force the other squares.

By primitivity, every prime factor of \(N\) is \(1\bmod4\), and \(5\nmid N\). For necessity write \((L+5ki)/(C+hi)=(u+iv)/w\) in lowest common denominator, \(w>0\). Then \(w\mid N\), \(u,w\) are odd and \(v\) even; indeed the real numerator is odd and the imaginary numerator even before reduction. A rational unit circle parametrization in primitive Pythagorean form shows \(u+2v\) is a square modulo \(5\): \(s^2-t^2+4st=(s+2t)^2\bmod5\), and sign changes preserve the conclusion. This square is nonzero, since its product with \(u-2v\) is \(w^2\bmod5\). Evaluation of the rotation at \(i=2\) also gives \(L/(2h)=\pm1/2\bmod5\), a nonsquare. Hence \(w\) has a nonsquare prime factor modulo \(5\).

For sufficiency choose a Gaussian prime \(\pi\) of norm \(\ell\equiv13,17\bmod20\) dividing \(C+hi\), with odd real part and even imaginary part. Multiplication by \(\bar\pi/\pi\) gives integral coordinates. The rotation is \(1\bmod2\) and is nonsquare at \(i=2\bmod5\), since the product of its numerator and denominator there is \(\ell\bmod5\). The new coordinates have squared norm \(h^2\bmod5\), so exactly one coordinate is zero modulo \(5\). If that coordinate were the real one, the rotation at \(i=2\) would be \(\pm1\), impossible. Thus the new imaginary coordinate is \(5k\). The real coordinate is odd, and \(N\equiv5\bmod8\) implies \(k\equiv2\bmod4\). Both \(h^2\) and \((5k)^2\) are \(4\bmod32\); hence \(L^2\equiv C^2\bmod32\), so one sign of \(L\) satisfies \(L\equiv C\bmod16\).

In any fixed nonempty modular class of allowed \(h\)'s satisfying the stated hypotheses, sampled over an interval of growing length, the proportion without a second representation tends to zero, uniformly in powers \(C\). For each admissible prime not dividing the fixed class modulus, exactly two classes modulo that prime give \(\ell\mid N\). Retain any fixed finite subset of these primes, apply CRT, and then enlarge the subset: the product of \(1-2/\ell\) tends to zero by divergence of reciprocal primes in the two progressions. This statement does not control the size of \(k\), nor a density conditioned on any further exact square.

Controls: \(234^2+125^2=70381\) is prime and \(1\bmod20\), so fails the criterion. Conversely \(126^2+125^2=(-51)^2+25\cdot34^2\), with \(-51\equiv125\bmod16\), satisfies the stated conditions.
