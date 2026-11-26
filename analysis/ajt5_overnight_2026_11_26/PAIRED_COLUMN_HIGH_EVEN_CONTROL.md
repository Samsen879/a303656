# Exact even tails for two adjacent child columns

Fix d, m, r, set x=5m+r, and inspect the two residuals x−5^d−3^f and x−5^(d+1)−3^f in the **same** phase f≡a mod P. For a finite panel of inert p>3, put C=lcm(P,{ord_p(3)}) and λ_p=v_p(3^ord_p(3)−1)+v_p(C). For each coarse f_0 mod C consistent with the input phase, a valuation below λ_p is frozen; if the residual is zero mod p^λ_p, the next two independent p-adic digits of the parameter in f=f_0+Ct suffice to realize a finite even valuation. Indeed the LTE principal-unit slope is primitive, so one can choose valuation λ_p if it is even and λ_p+1 otherwise. At the same prime the two residuals differ by 4*5^d, a unit, so at most one requires adjustment. The adjustments are compatible across primes by CRT. Thus a coarse class admits both residuals with finite even valuations iff no already frozen valuation is odd. A positive result is for local exponent parity; at fixed m it may lie beyond activation.

Restricting the even valuations to 0 or 2 is genuinely different. For d=0, r=4, m=8468456693985 the actual short side f=1 has valuation exactly 4 at 19 and both the parent and short-side child are real square sums. On the entire phase f≡1 mod 32490 this short-side residual remains zero modulo 19³, so the 0-or-2 search fails even though the true f=1 bridge exists.

```python
m = 8468456693985
x = 5*m+4
assert m == 4+1848634**2+2247445**2
assert x == 5+3+3520111**2+5472760**2
S = x-5-3
assert S % 19**4 == 0 and S % 19**5
assert pow(3,32490,19**3) == 1
```

This is a statement about the specified finite two-column menu, not about a global covering or the conjecture.
