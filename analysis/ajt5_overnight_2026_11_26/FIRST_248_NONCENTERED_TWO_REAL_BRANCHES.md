# A noncentered four-column track with a two-real-branch obstruction

On the original first-248 seed \(s=S=5409768750\) and base columns \(4,8,12\), use seed norm coordinates \((3/5,4/5)\) instead of \((1,0)\) for the normalized gates \(248\) and \(16\). This gives an actual infinite integer four-column family. On this specific track, any **fixed** algebraic curve on which the fifth residual is identically a sum of two rational-function squares can produce only finitely many integer \(m\). This does not exclude the union of varying representations over the whole original track.

Use \(g,m(s),h_{248},h_{16},h_{20}\) as in [the two-stage construction](FIRST_248_CENTERED_TWO_STAGE_PELL.md), with \(h_{248}=h_0\). Put \(\lambda_j=(S^2+h_j)^{-1}\), \(k=S^2(\lambda_{16}-\lambda_{248})\), \(\theta=3/5\), and
\[
 L_{248}(s)=\theta+\frac{\theta-k/\theta}{2S}(s-S),\qquad
 L_{16}(s)=\theta+\frac{\theta+k/\theta}{2S}(s-S).
\]
The expressions \(Q(s)=\lambda_j(s^2+h_j)-L_j(s)^2\) are identical for the two values of \(j\), by direct expansion. Write \(Q(S+\delta)=a\delta^2+b\delta+16/25\), where \(a,b>0\) and \(a\bmod7=5\) with unit denominator. Choose an integer \(W>0\) with \(A=aW^2\) integral, and \(e=b/(2a)\). Given an integer unit \(U+V\sqrt A\) of norm one, take
\[
 s=S+e(U-1)+(4/5)WV,\qquad y=(4/5)U+(Ae/W)V .
\]
Completing the square in \(\delta\) verifies \(y^2=Q(s)\). Multiply the two original Gaussian witnesses by \((L_j(s)+iy)/(3/5+4i/5)\). Their norms have the exact new scales, while the three base coordinates remain affine in \(s\). As in the linked proof, taking a positive unit power returning to \((1,0)\) modulo all coefficient denominators times the old preservation modulus makes every coordinate integral and preserves all twenty earlier-root obstructions. Its iteration grows \(s\) and gives unbounded integer \(m\).

## Finiteness on each fixed cover

Exact rational arithmetic gives \(Q(0)<0,\ Q(\pm9S/10)>0\), and \((9S/10)^2<-h_{20}<S^2\); these can be checked by substitution into the displayed \(L_{248}\). Thus the two components of \(y^2=Q(s)\) over the reals both contain open intervals where the fifth residual \((s^2+h_{20})/g\) is negative. The two poles of \(s\) on the projective conic are real and conjugate over the nonsquare coefficient field \(\mathbb Q(\sqrt a)\).

Let a smooth geometrically integral curve over \(\mathbb Q\) map nontrivially to this conic, and suppose its pullback fifth residual is a sum of two rational-function squares. For a genus-zero domain with a rational point, both source and target are real projective lines. If the pulled-back \(s\) has just two geometric poles, each target pole must have a single preimage, and each preimage is real by conjugation. Taking both pole pairs as 0 and infinity makes the map a real monomial up to nonzero scalar, as it has no other zeros or poles. Such a map covers at least one whole real affine component, including values with negative fifth residual, a contradiction away from the finitely many poles of the purported squares. The preimage counts over the conjugate target poles are equal; hence a genus-zero cover with a rational point and the norm identity has at least four geometric poles of \(s\). A genus-zero curve without rational points supplies no witnesses.

Now integer \(m\) forces \(s^2=g(m-5^{12}-1)-q_{12}^2\in\mathbb Z\), and rational \(s\) with integral square is integral. The [function-valued form of Siegel's theorem](https://arxiv.org/pdf/1910.11663#page=1) then gives finiteness for each fixed cover: in positive genus \(s\) is nonconstant, while in genus zero it has at least four poles. The simplest positive seed control is the cover \(z^2=(s^2+h_{20})/(S^2+h_{20})\), which contains \((s,y,z)=(S,4/5,1)\). It has genus one: over the algebraic closure the radicand has four simple zeros (two above each root \(s^2=-h_{20}\)), and its two poles have even order. It therefore supplies a genuine five-column seed but does not evade fixed-cover finiteness.
