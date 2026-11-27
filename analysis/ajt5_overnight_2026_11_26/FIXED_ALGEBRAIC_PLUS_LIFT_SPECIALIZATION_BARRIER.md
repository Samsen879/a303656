# An algebraic specialization barrier for fixed plus lifts

**A fixed finite-degree algebraic lift cannot produce infinitely many seed heights in the required field.** The obstruction holds even if the specialized lifts in \(L_+\) are allowed denominators. It applies to arbitrary infinite subsequences, not only to lifts that succeed at every point of a progression.

### Specialization obstruction

Write \(r=\sqrt{-15}\), \(K=\mathbb Q(r)\), and \(L=K(\sqrt5)\). Let \(\sigma\) be the nontrivial automorphism of \(L/K\). Fix an affine index \(n=n_0+hm\), with \(h>0\), and set \(X=5^m,\ Y=3^m\). For any fixed nonzero polynomial \(P(X,Y,Z)\) with algebraic coefficients, **only finitely many \(m\)** can admit a \(\beta_m\in L\) satisfying both
\[
P(5^m,3^m,\beta_m)=0,\qquad
N_{L/K}(\beta_m)=\alpha_+(2n+1).
\]
Allowing a larger fixed coefficient field does not change the statement. Taking the product of the conjugates of \(P\) over \(L\) gives a nonzero relation over \(L\), while the required specialized values still lie in \(L\).

**Reduction to a rational function.** Suppose there are infinitely many such samples. Keep an irreducible factor of \(P\) that contains infinitely many of them, clear denominators, and multiply \(\beta_m\) by the specialized leading coefficient. The resulting values solve a monic equation over a fixed ring of \(S\)-integers. They are therefore \(S\)-integral, even if the original \(\beta_m\) were not. Dividing by a sufficiently large power of \(X\) keeps the equation monic and makes every monomial in its nonleading coefficients have negative weight for \((\log5,\log3)\).

The normalized equation has nonzero discriminant. Add the exponent differences from its highest-weight discriminant monomial to the finite list of negative-weight vectors. Two adjacent continued-fraction convergents bracketing \(\log3/\log5\) give a unimodular change of monomials to \(U,V\) in which all those vectors have nonnegative coordinates. For an upper convergent \(p/q\) and its adjacent lower convergent \(p'/q'\), take exponent vectors \((-p,q)\) and \((p',-q')\). Both weights are negative and their determinant is ±1. Their cone tends to the entire negative half-plane, so sufficiently late convergents contain the finite list. Both \(U,V\) tend to zero exponentially along the samples. The equation now has polynomial coefficients, and its discriminant is a monomial times a unit near \((0,0)\).

On a small product of punctured disks, the roots are distinct and have finite monodromy. If the degree is \(d\), the substitutions \(U=u^{d!}, V=v^{d!}\) kill both monodromies. The roots are bounded because the equation is monic, so they extend to convergent power series at the origin. Their coefficients are algebraic: an automorphism of \(\mathbb C\) fixing \(\overline{\mathbb Q}\) permutes the finitely many formal roots, whereas a transcendental coefficient would have infinite orbit.

Now fix a residue of \(m\bmod d!\) and a branch that supplies infinitely many of the actual samples. The fractional powers then become algebraic constants times powers of two multiplicatively independent **rational** bases. Absorb the constants into the series. The inputs are \(S\)-units tending exponentially to zero, the outputs lie in \(L\) and are \(S\)-integral, and the monic root-height bound gives logarithmic height \(O(m)\). Corvaja–Zannier’s analytic \(S\)-unit theorem makes the series polynomial over \(L\) on a coset containing infinitely many inputs. Those inputs are Zariski dense in the two-dimensional torus by multiplicative independence, so this is a polynomial on the full torus. Undoing the scaling gives a fixed rational function over \(L\) for infinitely many of the original lifts on the refined progression. [Corvaja–Zannier, Theorem 1](https://www.numdam.org/article/ASENS_2005_4_38_1_76_0.pdf)

**Why the rational function cannot exist.** After fixing the parity of \(n\), the target is \(aX^h+bY^h\), with \(b/a=(3/5)^{n_0}r/5\). Exponential independence turns the norm equality into a rational-function identity. Specializing at \(Y=1\) is legitimate because the order along \(Y-1\) doubles under the norm and is zero on the target. This would give
\[
f(X)\sigma(f)(X)=aX^h+b.
\]
At the prime of \(L\) over \(3\), \(v(b/a)=2n_0+1\) is odd. Every irreducible factor of the binomial has degree divisible by \(h/\gcd(h,2n_0+1)\), by the valuation of the product of its roots. The binomial is squarefree, so a factor fixed by \(\sigma\) cannot occur in a norm. The remaining factors would pair off in equal degrees, forcing the total degree to be divisible by \(2h/\gcd(h,2n_0+1)\). This contradicts total degree \(h\).

### Same-index and conjugate controls

At \(t=7\), put \(v=\sqrt5\), \(u=\sqrt{-3}\), \(r=uv\). The degree-two branch with fixed \(y=\tfrac12-\tfrac25r\) and \(x=\sqrt{\alpha_+(t)+5y^2}\) specializes to \(x=\tfrac{17}2+r\). Thus \(x+vy=(17-4u+v+2r)/2\) is an integral lift of \(68+19r\).

At that **same admissible index**, the branch \(x=\sqrt{\alpha_+(7)},\,y=0\) fails field membership. The norm of \(\alpha_+(7)\) is the prime \(10039\), so an unramified prime above \(10039\) in \(L\) has valuation one on \(\alpha_+(7)\). It cannot be a square in \(L\). Conjugating the successful lift by \(v\mapsto-v\) keeps its Eisenstein norm and lands on the opposite signed target.

```python
from fractions import Fraction as Q
from math import isqrt

def sq(z):
    a,b = z
    return a*a-15*b*b, 2*a*b

def nk(a,b,c,d):  # beta = (a+b*u+c*v+d*r)/2
    return Q(a*a+3*b*b-5*c*c-15*d*d,4), Q(a*d-b*c,2)

def ne(a,b,c,d):
    return Q(a*a-3*b*b-5*c*c+15*d*d,4), Q(a*b-5*c*d,2)

x,y = (Q(17,2),1), (Q(1,2),Q(-2,5))
assert tuple(a-5*b for a,b in zip(sq(x),sq(y))) == (68,19)
good, wrong = (17,-4,1,2), (17,-4,-1,-2)
assert nk(*good) == (68,19) and nk(*wrong) == (68,-19)
assert ne(*good) == ne(*wrong) == (74,-39)
p = (5**7+3**7)//8
assert p == 68**2+15*19**2 == 10039
assert all(p % j for j in range(2,isqrt(p)+1))
assert 23816**2 + 3*42940**2 == 25**7-9**7
```

The result closes the route through a fixed algebraic relation in the two exponential bases. It gives no finiteness or density conclusion for admissible heights obtained from varying relations or from constructions outside that model.

The analytic S-unit theorem is used with exact S-unit inputs, exponential decay in both monomial coordinates, S-integral normalized outputs, and logarithmic root heights linear in the progression index. Independent BigInt checked the successful same-index specialization, its conjugate target, and the alternative square branch's prime-norm obstruction. The conclusion applies only to a fixed polynomial relation and required values in the fixed field.
