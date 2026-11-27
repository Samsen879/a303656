# A monomial pullback boundary for the native signed mixed shells

The exact criterion below concerns a rational-function norm over \(\mathbb Q(\sqrt{-3})\), not whether a numerical specialization happens to be a norm. The distinction is witnessed twice: the \(d=85\) exceptional plus shell has an integer norm witness but the constituent 5 fails its minus shell; at \(d=119\) there is no formal monomial norm identity even though its native plus specialization is a norm. This complements [the native 17-tower saturation](https://github.com/Samsen879/a303656/commit/c49156f35c4bb0c0eeef9f7085d5b722f53d88a9).

In the ramification argument, a totally ramified local extension at odd residue characteristic has no unramified quadratic subextension. The unique place above each prime over 3 also excludes a nontrivial quadratic subfield that would split locally there. The square-root inclusion test uses the cyclotomic quadratic character of conductor 5; the negative character of \(-5\) requires ramification at 2. For a pullback of odd degree, the extension of rational function fields remains linearly disjoint from the constant quadratic extension; commuting the two norm maps makes an odd power a norm, and dividing out an even power proves the stated obstruction. The Aurifeuillian comparison is prior literature; no priority claim is made.

### Exact norm-identity boundary

Let \(K=\mathbb Q(\sqrt{-3})\), let \(d>1\) be odd with \(3\nmid d\), and define
\[
P_{d,m}^{\pm}(T)=\Phi_d(5T^m,\mp3),\qquad m\ge1,
\]
using the homogeneous cyclotomic polynomial. The plus sign gives the shell from \(5^d+3^d\) at \(T=1\). Then \(P_{d,m}^{\pm}\) is a norm from \(K(T)\) to \(\mathbb Q(T)\) **exactly when the sign is plus, \(m\) is even, and \(5\mid d\)**. Homogenizing gives the same criterion for \(\Phi_d(5X^m,\mp3Y^m)\), which includes the actual odd-exponent square classes at \(m=2\).

For the proof, put \(L=\mathbb Q(\zeta_d)\) and take a root \(\alpha\) with \(\alpha^m=\mp(3/5)\zeta_d\). The binomial is Eisenstein at each prime of \(L\) above \(3\), since \(L/\mathbb Q\) is unramified there. Also \(L\subset\mathbb Q(\alpha)=E\), so \(P_{d,m}^{\pm}\) is irreducible over \(\mathbb Q\) and \(E/L\) is totally ramified above \(3\).

There is at most one quadratic subextension of \(E/L\). Two distinct ones would both be ramified above \(3\), so their radicands would both have odd valuation. The product radicand would give a third quadratic subextension unramified or split there, contradicting total ramification. When \(m\) is even the unique quadratic subextension is \(L(\sqrt{\mp15})\), obtained from \(\alpha^{m/2}\) since \(\zeta_d\) is a square in \(L\). It equals \(L(\sqrt{-3})\) precisely when \(5\) is a square in \(L\) for the plus sign, or \(-5\) is a square for the minus sign. The first holds exactly when \(5\mid d\). The second is impossible because \(\mathbb Q(\sqrt{-5})\) ramifies at \(2\), while \(L\) does not.

If \(K\subset E\), the polynomial splits into two conjugate factors over \(K\), and its leading coefficient \(5^{\varphi(d)}\) is a square. Otherwise it remains irreducible over \(K\), so its multiplicity in a rational-function norm would have to be even. This also gives an obstruction for **any odd-degree rational pullback** of \(P_{d,1}^{\pm}\). Taking the field norm down from the pullback would make an odd power of \(P_{d,1}^{\pm}\) a norm, which forces the polynomial itself to be one.

The exceptional plus case is constructive. For \(5\mid d\), the roots
\[
\frac{\sqrt{-15}}5\left(\frac a5\right)\zeta_d^a,
\qquad a\in(\mathbb Z/d\mathbb Z)^\times ,
\]
form one orbit over \(K\). The polynomial with these roots and leading coefficient \(5^{\varphi(d)/2}\), multiplied by its conjugate, gives \(P_{d,2}^+\). At the mixed index \(85=17\cdot5\) this yields the actual integer witness
\[
\Phi_{170}(5,3)
=15897485586118478569079^2
 +3\cdot13563623532951514253140^2.
\]
The constituent \(5\) still fails in its minus shell, which is \(11\cdot131\). The identity therefore supplies a mixed-shell norm without supplying a compatible generator. [Brent on Aurifeuillian identities](https://arxiv.org/abs/1004.5466)

### Primitive arithmetic test and same-input control

Let \(d>1\) be odd and \(3\nmid d\). Either of these conditions gives an inert prime \(p\) with \(\operatorname{ord}_p(25/9)\mid d\).

| Condition on \(d\) | Test |
|---|---|
| \(d\equiv2\bmod3\) | \(p=2d+1\) is prime |
| \(d\equiv1\bmod3\) | \(p=4d+1\) is prime and \((15/p)=1\) |

The first follows because \(25/9\) is a square. The second follows from Euler’s criterion applied to \(5/3\). In either case an odd \(v_p(5^{p-1}-3^{p-1})\) blocks \(d\). **If all proper divisors of \(d\) are admissible, the order is automatically exactly \(d\)**. Otherwise the same odd valuation would block a proper divisor by LTE. In particular, for an admissible prime \(b\equiv1\bmod3\), primality of \(34b+1\) and its odd valuation suffice to force a primitive obstruction at \(17b\), without factoring either mixed shell. This criterion makes no assumption about the distribution of such prime pairs.

At the same native input \((5,3)\), both constituents \(7\) and \(17\) pass. At \(119=17\cdot7\), the **plus** shell also passes, with exact coordinates below, while the **minus** shell has \(v_{239}=1\) and exact order \(119\). Thus the rational-function obstruction and arithmetic specialization have different scopes even at one fixed index.

```python
def N(x, y):
    return x*x + 3*y*y

def mix(a, b, s):
    return ((5**(a*b) + s*3**(a*b))*(5 + s*3)
            // ((5**a + s*3**a)*(5**b + s*3**b)))

for q, s, x, y in [
    (7,-1,137,80), (7,1,74,39),
    (17,-1,512959,198560), (17,1,225833,121632),
]:
    assert (5+s*3)*N(x,y) == 5**q+s*3**q

assert mix(17,7,1) == N(3224497952188665649525917753489953,
                        1755391293872065118753503753143368)
p = 239
assert all(p%i for i in range(2,16)) and p%3 == 2
z = 25*pow(9,-1,p)%p
assert pow(z,119,p) == 1 and pow(z,7,p) != 1 and pow(z,17,p) != 1
assert mix(17,7,-1)%p == 0 and mix(17,7,-1)%(p*p) != 0
assert mix(17,5,1) == N(15897485586118478569079,13563623532951514253140)
```

