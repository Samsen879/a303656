# A shorter uniform primitive menu for the dyadic displacement problem

For every fixed \(\varepsilon>0\) the \(O(k)\)-entry primitive menu can be taken with maximum displacement \(O_\varepsilon(Q^{139/372+\varepsilon})\), uniformly even when the real adjacent labels vary with \(k\). Here \(Q=27\cdot2^k\), \(c\ge1,d\ge0,k\ge5\), and a menu serves the locally liftable common classes. The separate explicit exponent is \(299/800\). The improvement is over [#97](https://github.com/Samsen879/a303656/pull/97). It proves existence of true common targets on corresponding integral lines, not representation of an arbitrary prescribed target. The proof below spells out the fixed-parameter result, the dyadic kernel and large-square tail, then optimizes the completion ledger. Exact finite controls are at the end.

## A. Epsilon-family theorem

## Exact statement

For every epsilon>0 there is a constant C_epsilon such that, for every
power of two `m=2^h>=8`, every `a=2 mod8`, and every `(r,s) mod27` with at
least one coordinate a unit modulo 3, there are positive integers u,v
satisfying

    gcd(u,v)=1, (u,v)=(r,s) mod27, u^2+v^2=a modm,
    max(u,v) <= C_epsilon*m^(139/186+epsilon).                (T-eps)

The constant depends only on epsilon. The order of quantifiers permits
the right side and the mod-27 address to change arbitrarily with h.

At the #96 interface, after renaming epsilon, the same O(k)-size menu has
maximum displacement

    O_epsilon(Q^(139/372+epsilon)).

The exponent `139/372=0.373655913978...` is strictly below 3/8. The exact
endpoint without epsilon is not asserted. A convenient explicit bound
with an absolute constant is the already checked

    O(Q^(299/800)) = O(Q^.37375).

Indeed `299/400-139/186=7/37200>0`, so the explicit point also lies inside
the parameterized family.

## 1. Parameter choices

It suffices to prove the result for `0<e<=1/1000`; larger requested
epsilons follow by using the result at 1/1000. Set

    r0=139/186, r=r0+e, R=m^r,
    gamma=e/10, G=m^gamma,
    xi=e/100,       M=N*m^xi,
    sigma=e/100,    the epsilon in polynomial Weyl,
    eta=e/100,      the exponent in the elementary divisor bound,
    J=ceil(1/xi)+2.

For every short common divisor g<=G, the scaled box has

    m^(r0+9e/10) <= S=R/g <= m^(r0+e).

This lies inside `[m^.74,m^.75]`. The estimate reused here is the symbolic
completion bound (CE). The earlier numerical (SC2) window is not assumed;
when e is very small the present S can be below m^.7474. The proof of
(CE) applies throughout this wider interval: `N=27m/S`, every retained
Kloosterman modulus is at least `m/(2M)` and therefore tends to infinity,
and no earlier `q>=m^.99` or minimum-frequency restriction is used.

The smooth frequency tail is bounded by

    O_e(m^(1-xi*(J-1)))=O_e(m^(-xi)),

so all aliases outside the retained square are harmless. The derivative
order J is fixed once e is fixed; it need not be uniform as e tends to
zero. This is consistent with the quantifier `C_epsilon`.

## 2. The completion estimate with explicit e margins

The unchanged length-dependent prefix bound is

    L^(1+sigma) * [q^(-1/96)+q^(1/96)L^(-1/16)
                                     +q^(1/16)L^(-5/16)].

Its validity for short prefixes is essential: after splitting by
`2^(ceil(n/6)+2)`, Weyl's three resulting powers of the progression
length are positive. They can all be bounded at the full interval
length; if the full interval is shorter than the splitting modulus,
the second term is already at least a constant times the trivial bound.

Keeping the interval and common-factor dependencies gives exactly

    O_sigma(M^sigma * [
        m^(47/96)*(M/N)^2
        +m^(49/96)*M^(31/16)/N^2
        +m^(9/16)*M^(27/16)/N^2 ]).                          (CE)

The sums over the common dyadic factor have exponents
`-143/96,-139/96,-5/4`, so all converge. The dyadic interval sums are
geometric as well. The affine mod-27 phase stays in the real linear
coefficient of Weyl's polynomial.

At `S<=m^r`, the three raw m exponents, before the truncation and Weyl
epsilon costs, are bounded by

    E1=47/96,
    E2=43/96+r/16,
    E3=1/4+5r/16.

At r=r0 one has

    E2=2r0-1=46/93,
    E2-E1=5/992,
    E2-E3=11/992.

For `0<e<=.001`, the second term remains the largest, since its difference
from E1 increases, and its difference from E3 only decreases by e/4.

The truncation costs are respectively `2xi,31xi/16,27xi/16`, each at most
`e/50`. In the present S interval, `M<=27m^.26`, so `M^sigma` costs at
most `.26e/100=13e/5000` in the exponent, up to a fixed factor. Their sum
is at most `113e/5000<e/20`. There is also room within e/20 to absorb any
retained logarithms. Consequently

    W(S;m,a;r,s)
      =2I^2*S^2/(729m)+O_e(m^(E2+e/20))                     (SC-eps)

uniformly for every scaled box in the short Möbius sum, every right side,
and every admissible mod-27 address.

## 3. Primitive Möbius inversion

The primitive main term is

    kappa*m^M0,    M0=2r-1,
    kappa=2I^2/(81*pi^2)>0.

The key identity is exact:

    M0-E2 = (31/16)*e.

Summing the error in (SC-eps) over g<=G costs at most another e/10 in the
exponent. Thus this error is below the main exponent by

    (31/16-1/20-1/10)*e = (143/80)*e > 0.

Completing the Euler product costs `O(m^(M0-e/10))`.

For the absolute large-common-divisor tail, use the unchanged positive
tail lemma with

    X=R^2=m^(2r), q=m/2, b=a/2.

The exponent 2r lies strictly between 1.49 and 1.51 throughout the stated
e interval. The factor of 2 between m and q is absorbed once m is
sufficiently large. In particular, its hypotheses do not impose any
bound on the ordinary label difference.

Multiplying the tail count by `r_2(2ell)<<_eta X^eta` gives the following
three bounds. Since `2r<3/2`, their exponents are at most

    M0-e/10+3e/200 = M0-17e/200,
    49/100+3e/200,                with a logarithm,
    M0-1/50+3e/200.

The first is strictly below M0. For the second, the gap is at least

    46/93-49/100+(2-3/200)e
      =43/9300+(397/200)e > 0.

For the third, the gap is at least `1/50-3/200000>0`, because e<=1/1000.
Thus every error is of smaller order than the positive primitive main
term, uniformly in a and the mod-27 class.

The weighted primitive count is eventually positive. The same elementary
finite-modulus CRT construction as in the explicit-exponent proof covers
the remaining finitely many m, with a constant depending only on e.
This proves (T-eps).

## 4. What the endpoint does and does not mean

The number `139/186` is where this completion ledger's dominant raw error
meets the primitive main term:

    2r-1 = 43/96+r/16.

At the exact endpoint the displayed estimates no longer give a positive
power margin, and the chosen positive sieve and truncation parameters
cannot be set to zero. Therefore no epsilon-free endpoint is claimed.
This is a boundary of the present argument, not a construction-independent
lower bound or an assertion that a better method is impossible.

The theorem continues to distinguish three quantifier regimes. It applies
to every k for globally fixed labels, and uniformly to labels that change
with k, after the local orientation conditions are met. It does not state
that one fixed polynomial pair realizes all these points. It also does
not turn a local class into a representation of an arbitrary prescribed N.
An ordinary-height application must separately check the actual label heights and the minimum of the affine line.

## B. Completion with full prefix lengths

## Statement

There is an absolute constant C such that, for every `m=2^h>=8`, every
`a=2 mod8`, and every `(r,s) mod27` with at least one coordinate a unit
modulo 3, there are positive integers u,v with

    gcd(u,v)=1, (u,v)=(r,s) mod27, u^2+v^2=a modm,
    max(u,v) <= C*m^(299/400).

Thus the exponent is `.7475=3/4-1/400`. At the #96 interface, where every
circle modulus is at most a constant times `sqrt(Q)`, the displacement
bound is

    O(Q^(299/800)) = O(Q^(3/8-1/800)).

The quantifiers are uniform in a and in the mod-27 class. They allow
labels to depend on k, but do not provide a fixed polynomial formula or
a representation at every prescribed target integer. The earlier proof's
orientation extends the local menu to both parities of c>=1; ordinary
label height remains a separate condition.

## 1. The exact phase input retained from the earlier proof

For `q=2^n`, odd A,B, the complete Kloosterman sum vanishes unless AB is
1 modulo 8, once n is large enough. On an admissible branch let
`lambda^2=AB`, `y=lambda/A`, and `C0=A/y`. For even n=2j>=6,

    K_q(A,B)=2^j * [(1+i^C0)e_q(2lambda)
                         +(1+i^(-C0))e_q(-2lambda)].

For odd n=2j+1>=9,

    K_q(A,B)=2^(j+1) * [e_8(C0)e_q(2lambda)
                              +e_8(-C0)e_q(-2lambda)].

These follow by splitting the summation variable at the middle binary
digits and retaining the quadratic correction at the two critical
points. The earlier note gives the explicit derivation, and its exact
checker verifies the identities in integer cyclotomic bases.

For the circle kernel the phase has

    lambda(x)^2=C*(x^2+b^2)/2,

with C,b,x odd. On a progression `x=x0+2^s*t`, take
`s=ceil(n/6)+2`. Its square-root Taylor series has all degrees at least
six zero modulo q. The coefficient of degree five in `2lambda` has
exact valuation `5s-7`, because

    lambda^(5)(x)=-15*C^5*b^2*x*(4*x^2-3*b^2)/(32*lambda(x)^9).

The reduced leading phase denominator is

    q5=2^(n-5s+7) comparable to q^(1/6).

Also `C0=lambda mod8` and lambda is fixed modulo 8 on each progression,
so the complete-sum amplitude is constant there. Every nonconstant
Taylor coefficient is 2-adically integral; reducing its residue modulo
q gives an ordinary real polynomial phase after division by q.

## 2. A length-dependent bound valid for every prefix

Let an x interval have length at most L, with L>=1. The relevant phase
can include an arbitrary real linear term. For a branch of the phase
above, with bounded amplitudes that are constant on the progressions,
every prefix satisfies

    |sum phase| <<_epsilon L^(1+epsilon) *
       [q^(-1/96) + q^(1/96)*L^(-1/16)
                         + q^(1/16)*L^(-5/16)].                (LP)

Here q is sufficiently large, and the implied constant is uniform in
C,b, the interval position, the analytic branch choices, and the extra
linear coefficient. Bad square classes contribute zero.

To prove this, put `P=2^s`, so `P` and `q5` are each comparable to
`q^(1/6)`, by fixed absolute constants. On one residue class modulo P,
classical degree-five Weyl gives, for a progression of T terms,

    O_epsilon( T^(1+epsilon)*q5^(-1/16)
             +T^(15/16+epsilon)
             +q5^(1/16)*T^(11/16+epsilon) ).                  (W5)

Every power of T displayed here is positive. Therefore, for any prefix
of the original interval, each progression can be bounded by substituting
the full interval's upper length `O(L/P)` whenever `L>=P`. Summing over
at most P progressions gives

    O_epsilon( L^(1+epsilon)*q^(-1/96)
             +L^(15/16+epsilon)*q^(1/96)
             +L^(11/16+epsilon)*q^(1/16) ),

which is (LP). Short prefixes are included in this argument: empty
progressions contribute zero; a progression of one or a few terms is
bounded by the same increasing expression at the full upper length.

If `L<P`, the second term in (LP) is at least a fixed positive constant
times L, because `P` is at most a fixed constant times `q^(1/6)`. Thus
the trivial O(L) estimate proves (LP) in this case too. There is no
unrecorded lower-length assumption. This also explains why the earlier
discarding of very short prefixes is unnecessary.

The standard Weyl inequality permits arbitrary lower real coefficients.
Its use here is exactly the one stated in Wooley's ICM 2014 report,
Theorem 7.1 / equation (7.1), and already used in the frozen proof.

## 3. Completion with the full A,d dependence

Fix the same nonnegative, nonzero smooth weight w supported inside (0,1),
and put `I=integral w`. It is enough to count at scales

    m^.7474 <= S <= m^.7475.

Write `N=27m/S`, `xi=1/10000`, and `M=N*m^xi`. With
`omega=27^(-1) modm` and `t=(27*omega-1)/m`, the exact Poisson expression is

    W = S^2/(729m^2) * sum_{alpha,beta in Z}
        hat(w)(alpha/N)hat(w)(beta/N)
        e_27(-t*(r*alpha+s*beta))
        C_m(omega*alpha,omega*beta;a).                         (P)

This contains every Poisson alias. The zero frequency is the main term
`2I^2 S^2/(729m)`. The sum outside `|alpha|,|beta|<=M` is `O(m^.4)`;
in fact the same `J=10000` Schwartz estimate gives `O(m^.0001)`.
Indeed its absolute bound is `O_J(m*(M/N)^(1-J))` using `|C_m|<=2m`.

For large m, M is much smaller than m. Frequencies with exactly one
coordinate zero vanish by the exact marginal count. The remaining
nonzero kernel requires

    alpha=2d*x, beta=2d*b, with x,b odd and d a power of two.

Exactly one multiplier stratum survives in the Gauss-sum expansion:

    C_m(alpha,beta;a)
      =4d*K_{m/(2d)}(m/(8d)-a/2, -(x^2+b^2)/2).              (CK)

Multiplication of both frequencies by omega changes the second
coefficient by its odd square, and therefore only changes the odd
constant C in the square-root phase. Its amplitude is `O(sqrt(m*d))`.
The residual factor in (P) is a genuine real linear phase; it is retained
in (LP). It need not have a power-of-two denominator.

Since `d<=M`, every Kloosterman modulus here tends to infinity with m:
`q=m/(2d) >= m/(2M)`. Thus (LP) and the exact complete-sum formulas apply
uniformly to all retained frequencies after one finite starting modulus.
No restriction `d<=m^.01` or `|alpha|>=m^.23` is needed.

Divide alpha into positive and negative dyadic intervals of size A, and
fix beta and d. The x interval has length comparable to `A/d`. In the normalized formula
(P), the supremum plus total variation of the smooth Fourier factor is
O(1); both factors S/27 have already been extracted into the prefactor.
Thus partial summation uses the all-prefix bound (LP). There are `O(M/d)`
possible beta frequencies in the corresponding stratum. Up to absolute
constants and a factor `M^epsilon`, the three resulting contributions
for this A,d are respectively

    m^(47/96) * A*M/N^2        * d^(-143/96),
    m^(49/96) * A^(15/16)*M/N^2 * d^(-139/96),
    m^(9/16)  * A^(11/16)*M/N^2 * d^(-5/4).                  (E)

For example, before expanding (LP), the factor is

    sqrt(m)*A*M/N^2*d^(-3/2),

and the three relative factors are

    m^(-1/96)*d^(1/96),
    m^(1/96)*A^(-1/16)*d^(5/96),
    m^(1/16)*A^(-5/16)*d^(1/4).

This verifies every exponent in (E). Each dyadic d series converges.
The A sums have positive exponents 1,15/16,11/16 and are dominated by
their largest interval. Consequently the total nonzero Fourier error is

    O_epsilon(M^epsilon * [
        m^(47/96)*(M/N)^2
        +m^(49/96)*M^(31/16)/N^2
        +m^(9/16)*M^(27/16)/N^2 ]).                          (CE)

Negative frequencies and a truncated last dyadic interval are covered by
the same all-prefix estimate. The sums can be bounded geometrically;
retaining an extra logarithm would also fit in the margin below.

## 4. Explicit smoothed-count margin

Here `N>=27m^.2525` and `M<=27m^.2527`. Inserting
`M=N*m^.0001` in (CE), before the tiny Weyl epsilon, gives exponent
bounds

    47/96 + .0002                         = .489783333333...,
    49/96 - .2525/16 + 31*.0001/16        = .494829166666...,
    9/16 - 5*.2525/16 + 27*.0001/16       = .4837625.

Fix the Weyl epsilon as `1/1000000`. Its extra factor costs at most
`.2527/1000000` in the exponent, plus a fixed constant. The largest
displayed exponent is below `.49485` by exactly `1/48000` before this
tiny cost. Thus, with room for any retained logarithms,

    W(S;m,a;r,s)
      =2I^2*S^2/(729m)+O(m^.49485)                          (SC2)

uniformly throughout the stated S interval and for all a,r,s.

## 5. Ordinary primitivity

Use

    R=m^.7475, G=m^.0001, eta=1/100000.

For `g<=G`, with `gcd(g,6)=1`, division of both coordinates by g puts
`S=R/g` in the interval for (SC2), preserves `a=2 mod8`, and preserves
the admissible mod-27 class. Short Möbius inversion gives the positive
main term

    kappa*R^2/m = kappa*m^.495,
    kappa=2I^2/(81*pi^2)>0,

because the Euler product over integers coprime to 6 is `9/pi^2`.
The error from (SC2) is

    O(G*m^.49485)=O(m^.49495),

and completing the Euler product costs `O(m^.4949)`.

For clarity, the unchanged positive tail lemma is

    #{g>G odd, ell>=1: g^2*ell<=X, g^2*ell=b modq}
       << X/(qG)+q^.49*log(2q)+X/q^1.02,                   (ST)

uniformly for a power of two q, odd b, and `q^1.49<=X<=q^1.51`.
Its proof splits g at `q^.49,q^.51`. Small g use direct counting;
large g use at most four roots per ell and `g<q`; the middle uses the
exact cubic Taylor expansion of inverse-square phases, classical Weyl,
and Erdős--Turán with cutoff `q^.03`. Complete dyadic blocks cover the
two endpoints. Section C gives the unchanged positive tail proof.

For the Möbius tail take exactly `X=R^2=m^1.495`, `q=m/2`, `b=a/2`.
The X range in (ST) holds for all sufficiently large m; for example
`m>=2^101` is enough for its upper inequality. For each (g,ell), the
number of coordinate pairs is at most `r_2(2ell)<<_eta X^eta`.
The three tail exponents are therefore

    .4949 + .00001495 = .49491495,
    .49   + .00001495 = .49001495  (with a logarithm),
    .475  + .00001495 = .47501495.

Every error is strictly below the main exponent `.495`. The weighted
primitive count is asymptotic to its positive main term, uniformly in a
and in the prescribed mod-27 class. Hence a primitive point exists for
every sufficiently large m.

For the finitely many smaller moduli, take the odd u in [1,53] with the
desired mod-27 class, choose a root of `a-u^2 modm`, and impose by CRT
the desired v class modulo 27 and `v=1 modp` for every prime p!=3 dividing
u. If 3 divides u then the prescribed v class is a unit modulo 3. This
gives a positive primitive point. Increasing one absolute C covers the
finite initial set and proves the theorem.


## C. Exact phase and large-square-tail derivation

## 1. Polynomial Weyl inequality used

For a real polynomial P of degree d>=2 whose leading coefficient is exactly
b/q in lowest terms, an interval of T integers satisfies

    |sum e(P(t))| <<_{d,epsilon}
       T^(1+epsilon)*(q^(-1)+T^(-1)+q/T^d)^(1/2^(d-1)).            (W)

Other coefficients, including an arbitrary real linear coefficient, are
unrestricted. This is the standard Weyl differencing inequality. All uses
below keep d=3 or 5 fixed. One can choose its epsilon as small as needed;
the resulting implied constants remain absolute because all numerical
parameters in this note are fixed.

## 2. Exact dyadic Kloosterman phases

Let q=2^n, A,B odd, and K_q(A,B)=sum_{x odd (q)} e_q(Ax+B/x).
For n sufficiently large this vanishes unless AB=1 modulo 8. If AB=1
modulo 8 choose lambda^2=AB in Z_2 and y=lambda/A. Put C0=B/y^3=A/y in
Z_2; only C0 modulo 4 or 8 will be used. Since C0/lambda=y^(-2)=1 modulo 8,
these amplitudes depend only on lambda modulo 8. For n=2j>=6,

    K_q(A,B)=2^j * [(1+i^C0)e_q(2lambda)
                         +(1+i^(-C0))e_q(-2lambda)].              (K-even)

For n=2j+1>=9,

    K_q(A,B)=2^(j+1) * [e_8(C0)e_q(2lambda)
                                +e_8(-C0)e_q(-2lambda)].          (K-odd)

Proof: for even n split x=z+2^j*t and for odd n split x=z+2^(j+1)*t.
The inner sum forces A*z^2=B modulo 2^j. Group the surviving z around the
two genuine critical points +/-y. The remaining nearby points are
y+e*2^(j-1), with e=0,1 in the even case and e=0,1,2,3 in the odd case.
The phase difference is C0*e^2*2^(2j-2). Cubic and higher terms vanish
modulo q in the indicated ranges. This gives respectively 1+i^C0 and
sum_{e=0}^3 e_8(C0*e^2)=2e_8(C0). The negative critical point gives the
conjugate amplitude. This also proves the vanishing assertion by the
stationarity condition modulo 8.

## 3. A short square-root phase estimate

The needed phase is a branch of

    lambda(x)^2 = C*(x^2+b^2)/2,

where C,b,x are odd and the right side is a square in Z_2. On any residue
class x=x0 modulo 2^s with s>=4, choose one analytic branch lambda(x).
Since v2(lambda'(x))=-1, the branch changes by a multiple of 2^(s-1), so
its residue modulo 8, and its Kloosterman amplitude in (K-even)/(K-odd),
are fixed on that class. The fifth derivative has exact valuation -5:

    lambda^(5)(x) = -15*C^5*b^2*x*(4*x^2-3*b^2)/(32*lambda(x)^9).

All factors in its numerator are odd. Thus the coefficient of t^5 in
2lambda(x0+2^s*t) has exact valuation 5s-7.

Set s=ceil(n/6)+2. Expanding

    lambda(x0+2^s*t)
      =lambda(x0)*(1+z1*t+z2*t^2)^(1/2),
    v2(z1)=s, v2(z2)=2s-1,

shows that a coefficient of degree j has valuation at least j(s-2)+1.
Therefore all degrees j>=6 vanish modulo 2^n. The phase 2lambda, plus
any real linear phase, becomes a degree-five polynomial modulo 2^n with
leading denominator

    q5=2^(n-5s+7),       q5 is comparable to (2^n)^(1/6).          (5-den)

Here 'comparable' uses fixed absolute factors only.
To use (W), take each integral 2-adic Taylor coefficient modulo 2^n and
divide its integer representative by 2^n. This produces a genuine real
polynomial with exactly the stated reduced leading denominator; no real
interpretation of a 2-adic coefficient is assumed.

We use this uniformly with an ambient m tending to infinity, modulus
q=2^n between m^.99/4 and m, and x intervals obtained by dividing a
frequency interval of length m^.23<=A<=m^.27 by 2d, where 1<=d<=m^.01. Prefix
sums are bounded by

    O((A/d)*m^(-1/400)).                                         (S5)

To check prefixes rigorously, those shorter than (A/d)*m^(-1/400) are
bounded trivially. In every longer prefix, after splitting into the
classes modulo 2^s, each progression has length

    T >> m^(.23-.01-.0025-1/6) = m^(61/1200).

Also q5 >> m^(.99/6), q5 << m^(1/6). Consequently the three terms in (W)
are bounded by powers with exponents at most

    -0.165,  -61/1200,  1/6-5*(61/1200)=-7/80.

After the degree-five exponent 1/16, the weakest saving is 61/19200,
which exceeds 1/400. Choose the epsilon in (W) sufficiently small to
retain the latter. Summing over the O(2^s) progressions preserves the
relative saving. The finitely many short progressions and endpoints are
absorbed since T is a positive power of m. This proves (S5), uniformly
in C,b, all branches, and every additional real linear coefficient.

## 4. Smoothed circle count with a power saving

Fix once and for all a nonnegative, nonzero C-infinity function w supported
inside (0,1), bounded by 1. Write I=integral w. For

    m^.74 <= S <= m^.75,

let

    W(S;m,a;r,s) = sum w(u/S)w(v/S),

over u^2+v^2=a modulo m, u=r modulo 27 and v=s modulo 27. Then

    W(S;m,a;r,s) = 2I^2*S^2/(729m) + O(m^.4978).                  (SC)

There is no gcd restriction in (SC). All constants are uniform in a,r,s.

Here are the completion details and error accounting. Write u=r+27x,
v=s+27y and complete x,y modulo m. Poisson summation for the two smooth
weights gives coefficients bounded by

    O_J(S*(1+|alpha|/N)^(-J)),       N=27m/S,

up to fixed factors of 27. The exact coefficient also has a linear phase;
the transformed circle kernel is C_m(27^(-1)alpha,27^(-1)beta;a), with
another linear phase. All these phases are harmless in (S5), including
the possible residual denominator 27. The zero frequency is 2m and gives
the displayed main term. Choose xi=1/10000 and truncate at M=N*m^xi.
By taking, for example, J=10000, the discarded Fourier tail is O(m^.4),
using the trivial complete-kernel bound 2m. Any fixed bounded factors in
N or M have no effect.

In the surviving frequencies |alpha|,|beta|<=M, frequencies with one
coordinate zero vanish, since the circle has exactly four roots in the
other coordinate for every odd coordinate. Low frequencies are much
smaller than m/2. The nonzero frequencies can contribute only when

    alpha=2d*x, beta=2d*b,   x,b odd, d a power of 2.

For them the additive Gauss-sum calculation in the older note has exactly
one surviving valuation stratum, and gives

    C_m(alpha,beta;a)
      =4d*K_{m/(2d)}(m/(8d)-a/2, -(x^2+b^2)/2).                 (C-K)

After multiplication of both frequencies by 27^(-1), the second
coefficient receives its odd square; this just replaces the odd constant
C in the square-root phase. The kernel has amplitude O(sqrt(md)).

There are three error ranges.

1. Common dyadic factors d>m^.01: bound absolutely. The total is

       O(sqrt(m)*(M/N)^2*sum_{d>m^.01, dyadic} d^(-3/2))
          =O(m^(.5+.0002-.015))=O(m^.4852).

2. |alpha|<m^.23: bound absolutely, summing the common dyadic factors.
   The total is

       O(sqrt(m)*m^.23*M/N^2)=O(m^.4801),

   because N is at least a fixed multiple of m^.25.

3. d<=m^.01 and |alpha|>=m^.23: divide alpha into dyadic intervals.
   For each fixed beta and each d use (K-even)/(K-odd) and (S5). On every
   2-adic branch the amplitude is constant. Partial summation accommodates
   the smooth Fourier coefficient; its supremum plus total variation on
   any dyadic interval is O(S). Summing the beta frequencies and dyadic
   alpha intervals gives

       O(sqrt(m)*m^(-1/400)*(M/N)^2)
          =O(m^.4977).

The logarithm from dyadic intervals, if retained rather than summed
geometrically, is absorbed by the difference between .4977 and .4978.
Negative frequency intervals obey the same derivative valuation and
Weyl argument. This proves (SC).

## 5. Saved large-square-factor tail

Let q be a power of 2, b odd, and q^1.49 <= X <= q^1.51. As in the older
note define

    T(X,q,b;G)=#{g>G odd,l>=1: g^2*l<=X, g^2*l=b modulo q}.

Uniformly in b,G,

    T(X,q,b;G) << X/(qG) + q^.49*log(2q) + X/q^1.02.            (ST)

For g<=q^.49 use the one l-progression, at total cost
O(X/(qG)+q^.49). For g>q^.51 exchange the order of counting: l<=X/q^1.02.
For each l, g^2=b/l modulo q has at most four roots; g<=sqrt(X)<q, so at
most four positive g occur. This gives the last term of (ST).

For q^.49<g<=q^.51, cover this positive set by complete dyadic intervals
U<g<=2U, with q^.49/2<=U<=q^.51. Extending the two endpoint intervals is
permitted for an upper bound. Thus no arbitrarily short endpoint interval
is subjected to the lower-length assumption in Weyl's inequality. Use the
fixed fractional-part interval of length sigma=X/(qU^2) from the older note.
This length is less than 1. Apply Erdős--Turán with H=floor(q^.03).
For each 1<=h<=H, consider

    sum_{g in the interval, odd} e_q(h*b*g^(-2)).

Remove 2^v=gcd(h,q), giving modulus q0=q/2^v>=q^.97 and odd coefficient.
On a progression g=g0+2^s*t with s=ceil(log2(q0)/4), the inverse-square
Taylor series has degree at most three modulo q0. Its cubic coefficient
has valuation 3s+2, so its reduced denominator is comparable to q0^(.25).
The progression length is at least a fixed multiple of q^.24. Thus the
degree-three Weyl bracket has its three terms bounded by

    O(q^(-.2425)),  O(q^(-.24)),  O(q^(-.47)),

respectively. After its exponent 1/4 and a small Weyl epsilon, we obtain
the uniform bound O(U*q^(-.055)). Summation over progressions preserves
the relative saving. Erdős--Turán now gives

    count << U*sigma + U*q^(-.03) + U*q^(-.055)*log q.

Since U<=q^.51 the two error exponents are .48 and .455, both below .49.
Summing O(log q) blocks proves (ST). No Möbius cancellation is used.

## 6. Primitive Möbius inversion with explicit margins

Take R=m^(.75-.001), G=m^.0001 and use the fixed weight w. The contribution
from common divisors g<=G, gcd(g,6)=1 is evaluated by (SC), with S=R/g in
its permitted interval. Its main term is

    2I^2 R^2/(729m) * sum_{g<=G, gcd(g,6)=1} mu(g)/g^2,

and its total error is O(G*m^.4978)=O(m^.4979). The complete Euler product
is 9/pi^2, so the target main term is

    kappa*R^2/m,  kappa=2I^2/(81*pi^2)>0,
    R^2/m=m^.498.

Completing the Euler product costs O(R^2/(mG))=O(m^.4979). For the absolute
large-g Möbius tail put X=R^2 and q=m/2. Each g,l is weighted by at most
r_2(2l) <<_eta X^eta. Choose eta=1/100000. Since X is comparable to
q^1.498, (ST) applies, and the tail is

    << X^eta*[X/(mG)+m^.49*log m+X/m^1.02].

The three exponents in m are at most

    .4979+.000015=.497915,
    .49+.000015=.490015 (times log m),
    .478+.000015=.478015.

All are strictly less than .498. Therefore the weighted primitive count
is asymptotic to kappa*m^.498 and is positive for sufficiently large m.
For the finitely many smaller m, choose the odd u in [1,53] congruent to r
modulo 27. The number a-u^2 is 1 modulo 8, so it has a square root v0 modulo
m. By CRT choose v=v0 modulo m, v=s modulo 27, and v=1 modulo every prime
p!=3 dividing u. These moduli are pairwise coprime after repeated prime
factors are removed. If 3 divides u, the admissibility assumption gives
3 not dividing s. Hence gcd(u,v)=1, and a positive v always exists.
Increasing the absolute constant covers these finitely many m. This proves
(T).

## 7. Label orientation and exact quantifier scope

Write the original two labels as

    L0=3^c+5^d, U0=3^(c+1)+5^(d+1), D0=U0-L0,

with c>=1 and d>=0. If c is even use L_eff=L0,D_eff=D0. If c is odd use
L_eff=U0,D_eff=-D0. In both cases D_eff=6 modulo 8 and 3 does not divide
D_eff. These are the local conditions used by the [#96 dyadic menu](https://github.com/Samsen879/a303656/pull/96). Its
local argument therefore extends to both parities after this orientation.
The primitive circle theorem supplies O(Q^(749/2000)) displacements for
the same O(k) local layer/type/class requirements.

The affine line has u*x+v*y=H, with H=(D_eff+A)/2 and A=u^2+v^2. Its
minimum total value is

    mu=L_eff+H^2/A.

A negative D_eff is harmless: mu-L_eff=H^2/A>=0 and

    mu-(L_eff+D_eff)=(A-D_eff)^2/(4A)>=0.

Thus a point on this line with total value N>mu has both original
residuals positive. The ordinary-height quantity mu must still be checked
in each application; a uniform short modular displacement alone does not
bound it when actual labels grow.

Theorem (T) has the order of quantifiers

    exists absolute C; for every h,a,r,s in the stated local classes,
    there exist u,v depending on h,a,r,s with the stated properties.

Consequently it applies both to globally fixed labels and to any chosen
sequence of labels depending on k. It makes no assertion that one fixed
polynomial pair u(t),v(t) supplies these points, and it does not assert
representation at every prescribed integer N. The effective constants in
the proof are not numerically optimized; the replay script audits exact
finite identities and exponent margins, not a universal numerical cutoff.

## 8. Native 3/5 positive and negative controls

Take c=2,d=4, so L=634, U=3152 and D=2518. Put k=20,
Q=27*2^20=28311552. The basic zero-layer prescription is H=0 modulo 1024,
so its circle modulus is m=2048. The possible positive norms begin with
1578,3626,5674. The first has no sum-of-two-squares representation; the
second has exactly the positive representations (35,49),(49,35), both
of gcd 7. In particular (35,49) has the admissible mod-27 class (8,22),
with both coordinates 3-adic units. Yet H=(D+3626)/2=3072 is not divisible
by 7. The dot-product equation 35*x+49*y=3072 has no integer solution at
all. Thus imposing a mod-27 unit coordinate does not remove the need to
prove ordinary primitivity. The first primitive norm is 5674=7^2+75^2.

For an actual same-target positive control in the original label windows,
use the primitive displacement s=(103,107), A=22058, H=12288. Then

    18875002 = 634 + 3072^2 + 3072^2
             = 3152 + 3175^2 + 2965^2.

Its signed line point is z=(-3072,3072), with z-s=(-3175,2965).
The lower residual is 18*2^20, hence 0 modulo 2^20 and 18 modulo 27.
With X=10^7, the target lies strictly between X and 2X, and both label
pairs (2,4),(3,5) satisfy the original bounds

    3^(4c)<=X<=3^(8c),  5^(2d)<=X<=5^(3d).

These are exact controls, not evidence for an asymptotic exponent.

## D. Independent derivation of the surviving circle stratum

# 附录 D. 根审查者独立重建的圆核

The following derivation verifies the complete kernel used by the improved frequency sum. It explains why allowing every common binary
factor up to the Fourier cutoff introduces no new multiplier strata.

Let m=2^h, a=2 modulo 8, and

\[
C_m(\alpha,\beta;a)=\sum_{u^2+v^2=a\ (m)}e_m(\alpha u+\beta v).
\]

Consider nonzero frequency coordinates with v₂(gcd(α,β))
less than h−4. This includes every nonzero low-frequency pair in the
proof once its cutoff M is less than m/16. Multiplying both frequencies
by an odd unit, in particular the inverse of 27, preserves this condition.

Expand the circle indicator by an additive multiplier t. The t=0 term
vanishes at every retained frequency except (0,0), by additive
orthogonality. At a nonzero
multiplier stratum δ=gcd(t,m), write q=m/δ and t=δT with T odd. The two
Gauss sums vanish unless δ divides both frequencies. For q≥4 they vanish
unless α/δ and β/δ are even. In the latter case square completion and
the exact quadratic Gauss-square identity give

\[
\begin{aligned}
G_q(T,b)&=e_q\bigl(-(b/2)^2/T\bigr)G_q(T,0),\\
G_q(T,0)^2&=2q i^T.
\end{aligned}
\]

Thus this stratum contributes

\[
2\delta\,K_q\left(q/4-a,
-\frac{(\alpha/\delta)^2+(\beta/\delta)^2}{4}\right).
\tag{1}
\]

All contributing q are larger than 16 in the range under consideration.
The first Kloosterman coefficient in (1) therefore has valuation exactly
one. The second must have valuation one as well, for the following
elementary cancellation reason. If its valuation is zero, translating
the odd summation variable by q/2 changes every phase by a half-integer.
If its valuation is at least two, translating by q/4 changes the phase
by a half-integer: the linear derivative has valuation one and the
quadratic and higher corrections vanish modulo q. Each is a bijective
translation, so the sum equals its negative and is zero.

More explicitly, for f(x)=Ax+B/x with v₂(A)=1, the increments are

\[
f(x+q/2)-f(x)\equiv(q/2)(A-B/x^2)\pmod q,
\]

and, when 4 divides B,

\[
f(x+q/4)-f(x)\equiv(q/4)(A-B/x^2)\pmod q.
\]

The first coefficient in parentheses is odd when B is odd; the second
has valuation one when 4 divides B. This proves the cancellations without
an asymptotic stationary-phase assumption.

If v₂(α) and v₂(β) differ, the valuation of the second coefficient in
(1) is even, so every stratum vanishes. If they agree and

\[
\alpha=2d x,\quad\beta=2d b,\quad x,b\text{ odd},
\]

then δ≤d and the second coefficient has valuation
`2v₂(d/δ)+1`. Exactly δ=d survives. Removing the common factor two from
both Kloosterman coefficients uses
`K_q(2A,2B)=2K_(q/2)(A,B)`. Consequently

\[
\boxed{C_m(\alpha,\beta;a)
=4d\,K_{m/(2d)}\left(m/(8d)-a/2,-(x^2+b^2)/2\right).}
\]

Odd coordinate frequencies vanish directly from translation of the
corresponding circle coordinate by m/2. Frequencies with exactly one
zero coordinate vanish in the retained range because each odd coordinate
has exactly four partners, and the Fourier sum over odd residues is zero
away from 0 and m/2. The zero-zero kernel has 2m points.

Finally, multiplying α,β by the odd inverse ω of 27 multiplies the second
coefficient by ω². The square-root phase remains
`λ(x)²=C(x²+b²)/2` with an odd constant C. Its fifth-derivative valuation
is unchanged. Therefore the stronger proof's sum over all d up to M is
covered by the same exact kernel identity; it does not require d≤m^.01.


## Exact arithmetic replay

This script checks the exponent comparisons and a native positive/negative pair. The analytic bounds follow from the proof and the explicit Weyl input, not from finite testing.

```python
from fractions import Fraction as F
from math import gcd,isqrt
r0=F(139,186)
assert 2*r0-1==F(43,96)+r0/16==F(46,93)
assert F(299,400)-r0==F(7,37200)
assert all(x>0 for x in [F(143,80),F(17,200),F(43,9300),F(1,50)-F(3,200000)])
for e in (F(1,1000),F(1,10**7)):
 r=r0+e;M=2*r-1
 E=[F(47,96),F(43,96)+r/16,F(1,4)+5*r/16]
 assert E[1]==max(E) and M-E[1]==F(31,16)*e
 assert F(149,100)<2*r<F(151,100)
 assert E[1]+e/20+e/10<M
 assert max(M-F(17,200)*e,F(49,100)+F(3,200)*e,M-F(1,50)+F(3,200)*e)<M
L,U=3**2+5**4,3**3+5**5
pairs=lambda A: [(u,v) for u in range(1,isqrt(A)+1) for v in [isqrt(A-u*u)] if v>0 and u*u+v*v==A]
assert not pairs(1578) and pairs(3626)==[(35,49),(49,35)] and gcd(7,75)==1 and 7*7+75*75==5674
assert ((U-L+3626)//2)%7!=0
x,y=-3072,3072;u,v=103,107
N=L+x*x+y*y
assert N==U+(x-u)**2+(y-v)**2==18875002 and gcd(u,v)==1
assert (N-L)%(2**20)==0 and (N-L)%27==18
X=10**7
assert X<N<2*X and all(3**(4*c)<=X<=3**(8*c) and 5**(2*d)<=X<=5**(3*d) for c,d in [(2,4),(3,5)])
print("PASS exponent ledger and native exact controls")
```

Primary bound: [Trevor Wooley, *Translation invariance, exponential sums, and Waring’s problem*](https://www.math.purdue.edu/~twooley/publ/2014icm.pdf), equation (7.1).
