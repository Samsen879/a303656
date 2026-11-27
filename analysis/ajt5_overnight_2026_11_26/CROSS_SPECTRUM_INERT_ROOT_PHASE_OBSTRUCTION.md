# Exact inert-root phase obstruction to a cross-spectrum mean product

Use the two opposite-sign spectra of [the mod-65 phase gate](OPPOSITE_FACTOR_SPECTRA_PHASE_GATE.md), restrict \(n\equiv527\bmod672,\ n\equiv35\bmod65\), and keep the original separated \(3,5\) exponent box. On the two sides take respectively the fixed subphases \((c_+,d_+)\equiv(26,50)\bmod120,\ (c_-,d_-)\equiv(50,50)\bmod120\). Both sets retain a positive fraction of the original number of labels. Every shift is \(34\bmod65\), giving both residuals the same tag 1. However their shifts are \(4,2\bmod11\), respectively. All constructed residuals use only split primes, so \(n\equiv4\bmod11\) makes the plus hit count zero, and \(n\equiv2\bmod11\) makes the minus hit count zero.

Write \(Z_\pm(n)\) for actual hit counts (not a product of local indicators) and \(\mu_\pm\) for their means over the coarse target class. Fix \(y\) first, then \(X\to\infty\). The weighted Mertens and fixed-modulus PNT argument of the linked note gives \(\mu_\pm\asymp_y K_\pm/\sqrt{\log X}\), where \(K_\pm\) counts actual retained labels. In a mod-11 class other than its forbidden one, the conditional first moment on either side is \((11/10+o_y(1))\mu_\pm\): the final large prime enters a specified unit class at 11, changing its probability by \(1/10\) and the number of target points by \(1/11\). In the forbidden class the mean is exactly zero.

Therefore a prediction of mixed mass in every finer target class using the *coarse* product \(\mu_+\mu_-\) is false at the main scale \(XK_+K_-/\log X\): two of the eleven classes have no mixed hits at all but the proposed coarse product is positive. The average of the product of the two conditional means has factor \(99/100=(9/11)(11/10)^2\) relative to the coarse product. This is a first-moment local correction, not a theorem that the true mixed moment equals that product.

For an allowed class, even the primary final-prime progressions are outside the previous one-prime Bombieri–Vinogradov argument. If \(D_+,D_-\) are the fixed marked products before the last primes, a genuine pair must solve \(D_+b_+-D_-b_-=s_--s_+\) at the same \(n\). The plus product has size at least \(X^{13/120+22/64}\), and the minus product at least \(X^{13/120+3/8}\). For a plus final prime, the modulus includes the minus product while its prime scale is \(\ll X^{1-13/120-22/64}\); and symmetrically on the other side. Both moduli exceed the corresponding square-root scales. Thus the previous range cannot be reused as a reason for positive mixed mass. A mixed lower bound for the allowed residue classes remains unproved.

```python
from fractions import Fraction
for c,d,s11 in ((26,50,4),(50,50,2)):
    assert (pow(3,c,65)+pow(5,d,65))%65==34
    assert (pow(3,c,11)+pow(5,d,11))%11==s11
    assert pow(3,120,65)==pow(3,120,11)==pow(5,120,11)==1
    assert pow(5,d+120,65)==pow(5,d,65)
assert Fraction(9,11)*Fraction(11,10)**2==Fraction(99,100)
assert Fraction(13,120)+Fraction(3,8)>(1-Fraction(13,120)-Fraction(22,64))/2
assert Fraction(13,120)+Fraction(22,64)>(1-Fraction(13,120)-Fraction(3,8))/2
```
