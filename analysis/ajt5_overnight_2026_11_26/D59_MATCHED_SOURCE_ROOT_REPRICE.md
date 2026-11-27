# Matched source-root repricing at D=59

**The finite \(D=59\) charge falls from 354 to 284 units of \(10^{-11}\) density.** The new exception-density upper bound is **\(0.0000653840846076457\ldots\%\)**. This uses the existing common-Wieferich cutoff and allows arbitrarily many common-Wieferich primes above it. [Finite-prime ledger](https://github.com/Samsen879/a303656/blob/c12d0e2/analysis/ajt5_overnight_2026_11_26/FINITE_PRIME_SOURCE_REPRICE.md) · [Current three-tail baseline](https://github.com/Samsen879/a303656/commit/3736b2b6519cf82991df4ace668e5ea839077a95)

### The matched first-blocker comparison

Fix an eligible terminal \(q\) assigned to \(D=59\) and the original mod-\(3960\) head. Let \(\mathcal D\) be the union of older \(59\)-readers on the two axes. Let \(J\) consist of the common-Wieferich rows among the retained rows. The existing cutoff gives \(B<p<q\) for every \(p\in J\).

Temporarily omit \(J\) as well as \(59\) and \(\mathcal D\). On the original first-blocker event, this reduced retained prefix has an anchor. Choose the anchor from its observations alone. Both source orders at \(59\) are \(29\), and the split prime \(29\) is free in the locked head. Change its digit on base \(3\). Every affected row in the reduced prefix has at least one ordinary axis. The affected rows have prime greater than 29; on an ordinary axis their own primary repairs preserve the root modulo \(59\) and the locked head modulo 3960. In increasing-prime order the repairs preserve all earlier rows, since their periods cannot contain the new prime, and can only affect later rows. At a collision, two free primary digits suffice to obtain valuation exactly two. This produces two distinct roots before reading \(J\), \(n_{59}\), the dropped readers, or the terminal. [Protected source-root construction](https://github.com/Samsen879/a303656/commit/29e0e8f6ef234eabfd795e993ce1e8709ec5d827)

Require both anchors to be units at every restored \(p\in J\). Conditional on the reduced retained observations, the two shifts are fixed. They exclude at most two residues at each \(p\), and these prime coordinates are independent. The exact probability of passing this unit screen is \(\prod_{p\in J}(1-m_p/p)\), where \(m_p\in\{1,2\}\) counts the distinct shifts. In particular,
\[
\Pr(\text{both anchors restored})
\;\ge\;\prod_{p\in J}(1-2/p)
\;>\;\frac{199}{1000}.
\]
For the last step use \(\log q<5\cdot59/4+\log2\) and the existing Brun–Titchmarsh reciprocal envelope in the single class \(3\bmod4\). With \(U=5\cdot59/4-\log2\) and \(V=\log B-\log4\), it gives \(\sum_{p\in J}1/p\le 1/U+\log(U/V)\). Multiplying this bound by \(2+4/(B-1)\) bounds the negative log of the product and gives less than \(807/500\). This estimates all possible restoration failures without a catalogue above \(B\). [Original maximal-order endpoint](https://github.com/Samsen879/a303656/blob/de217297c9441bf716939e22ede8de25696494e6/analysis/ajt5_overnight_2026_11_26/MAX_ORDER_RANKED_TERMINAL_DENSITY_BOUND.md) · [Montgomery–Vaughan, Theorem 2](https://www.cambridge.org/core/journals/mathematika/article/abs/large-sieve/2B0269C6D6662EED351C6C06AA8D62ED)

On screen success, the two-root comparison gives \(\beta_qG\), where \(G=(59S_{59})^{58}/58!\). On screen failure, restore the original single-anchor calculation, with zero first-blocker contribution if the full retained prefix has no survivor. The screen uses only retained observations. Thus \(n_{59}\), the dropped readers and the terminal still have their original conditional laws. The failure bound is uniform in the small-head observations, so it multiplies the existing parity-filtered depth charge before those observations are averaged. The separate robust-reader allowance is retained in full. [Same-condition two-root comparison](https://github.com/Samsen879/a303656/commit/e2860de8be846477817a763e9e12d4f17df7f59c)

With \(R\) the existing ranked reciprocal envelope and \(C\) the **unrounded** original \(D=59\) depth charge, the replacement is therefore
\[
C_{\rm new}\le \frac{801}{1000}C+RG .
\]
The certified rounding is \(354\to284\). The finite-prime subtotal is now **30,144**, the full finite subtotal is **56,392**, and all three infinite tails retain their previous values. The bound applies to growing-box misses and hence to all-exponent exceptions.

### Inline replay

The short replay takes the inherited ranked envelope as outward input. Rebuild it with `ranked(59)[2]` from the linked finite-prime ledger and compare it as a rational against `287195785/10**13`. The inline replay also checks an actual local restore at row 523.

```python
from fractions import Fraction as Q
from math import ceil, factorial, isqrt, lcm, prod

B, W, r = 9*10**14, 10**11, 59

def series(y):
    z = (y-1)/(y+1)
    a = 2*sum(z**(2*j+1)/(2*j+1) for j in range(12))
    return a, a+2*z**25/(25*(1-z*z))

l2, h2 = series(Q(2))

def logs(x):
    y, k = Q(x), 0
    while y >= 2:
        y /= 2
        k += 1
    a, b = series(y)
    return a+k*l2, b+k*h2

def lo(x): return logs(x)[0]
def hi(x): return logs(x)[1]

u = Q(5*r,4)
env = 1/(u-hi(2))+hi((u-lo(2))/(lo(B)-hi(4)))
z = Q(807,500)
assert (2+Q(4,B-1))*env < z
assert (sum(z**k/factorial(k) for k in range(21))
        + z**21/factorial(21)/(1-z/22)) < Q(1000,199)

R = Q(287195785,10**13)  # Outward bound on the inherited ranked R.
S = (Q(ceil(W*hi(r)),W)+Q(1,2))/(r-1)
K = (1+isqrt(4*r-3))//2
psi = min(prod(r*S/(r-(j+1)*K) for j in range(k))
          for k in range(1,7))
G = (r*S)**(r-1)/factorial(r-1)
C = R*(psi/r+(1-psi)*Q(19,48)*(1+(1+Q(1,119))*S)/r**2)
assert ceil(W*C) == 354
assert ceil(W*(Q(801,1000)*C+R*G)) == 284
assert Q(654540846076458,10**19)-Q(70,10**9) == Q(
    653840846076458,10**19)

# Ordinary arithmetic control for local restoration.
p, c, d = 523, 23, 8817
n = 259198168546788118777752775481721787383681
def shift(a,b,m): return (pow(3,a,m)+pow(5,b,m))%m
L = lcm(3960,p*p)
L *= pow(L,-1,29)
a, step = c+L, lcm(3960,58)
assert (n-shift(a,d,p*p))%(p*p) == p
assert (shift(c,d,59),shift(a,d,59)) == (50,22)
f = ((pow(3,step,p*p)-1)//p)*pow(3,a,p)%p
a += step*pow(f,-1,p)
if (n-shift(a,d,p**3))%p**3 == 0:
    a += step*p
assert (n-shift(a,d,p**3))%p**3 in range(p*p,p**3,p*p)
assert a%3960 == c%3960 and shift(a,d,59) == 22
```

Use the upper decimal **0.000065384085%** when stating the certified strict bound; the longer decimal is the approximate value of the upper-bound envelope. The gain is 70 whole units in the relevant existing ledger, with no change to the cutoff or tails.
