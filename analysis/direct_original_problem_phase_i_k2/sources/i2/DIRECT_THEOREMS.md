# Direct additive reset: precise theorem statements and proofs

Date: 2026-09-10. Scope: the literal shift language S={3^c+5^d:c,d>=0}.
All assertions below are proved here, except items explicitly marked as targets or inherited background. No C=1 certificate, order-DAG, B7 or B31 hypothesis is used. These elementary route exclusions and the local calculation are not claimed to be new to the mathematical literature. They do not prove the original conjecture or an inverse theorem for its exceptional set.

## Definitions and boundary convention

Let b(m)=1 for a nonnegative integer m that is a sum of two integer squares, and b(m)=0 otherwise. In particular b(0)=1. The positive-integer two-squares criterion is used only for m>0. Define

    R(n)=sum_{c,d>=0; 3^c+5^d<=n} b(n-3^c-5^d).

The conjecture is R(n)>0 for every integer n>1. Equal numerical shifts from different exponent pairs are counted separately. All scope statements about the conjecture retain the boundary <=, not <.

## I2-D1. Uniform near-shift covering bound

For integers X>=2 and 1<=H<=X/2, let

    U(X,H)=#{n in Z : X<=n<=2X and 0<=n-s<=H for some s in S}.

Then

    U(X,H) <= 4(2H+1)
              +2(H+1)(floor(log_3(2X/H))+floor(log_5(2X/H))+2).

In particular U(X,H)=O((H+1)(1+log(X/H))) with an absolute constant. No square condition is imposed on n-s in this statement.

### Proof

If n is counted, s=3^c+5^d lies in [X-H,2X], hence in [X/2,2X]. At least one summand A is in [X/4,2X]. This interval has ratio 8. It contains at most two powers of 3, because three such powers span a ratio at least 9, and at most two powers of 5. We may therefore cover all possibilities using at most two anchors A of each base.

Fix an anchor A and write B for the summand from the other base. If B<=H, every covered n lies in [A,A+2H], giving at most 2H+1 integers, regardless of the number of small powers B.

If B>H, there are at most floor(log_b(2X/H))+1 powers B of its base b up to 2X. Each produces an interval [A+B,A+B+H] containing H+1 integers. Sum this bound over the at most two anchors of each base. Overlap and duplicate shifts only decrease the union. This proves the displayed bound. QED.

### Corollary: sublinear residual strategies have density zero

Let h(n)>=0 satisfy h(n)=o(n). Then

    #{n<=X : exists c,d>=0 with 0<=n-3^c-5^d<=h(n)} = o(X).

Consequently, representations that additionally require the residual to be a sum of two squares still cover only density zero.

To see this on [X,2X], use H=max(1,ceil(sup_{X<=n<=2X}h(n))). Then H=o(X), and the theorem gives

    U(X,H)/X = O((H+1)/X * (1+log(X/H))) = o(1).

The standard dyadic decomposition gives the global conclusion. The case of eventually bounded H is included.

**Scope:** this rules out the whole explicit strategy class “first force n-3^c-5^d=o(n), then solve a small norm problem.” It does not rule out residuals comparable to n, and it does not say that the original representable set has density zero.

## I2-D2. A macroscopic shift-free interval on every dyadic scale

Every real interval [X,2X], X>0, contains an open subinterval with no element of S and length at least 97X/1700 > X/20.

### Proof

Any shift in [X,2X] has a summand A>=X/2. There are at most two possible powers of 3 for this summand and at most one possible power of 5: the interval [X/2,2X] has ratio 4.

Put epsilon=1/100. For each of these at most three anchors, all shifts with the other summand B<epsilon X lie in an interval [A,A+epsilon X]. These three closed clusters have total length at most 3X/100.

For the remaining shifts, B lies in [X/100,2X]. There are at most four powers of 5 in this interval (ratio 200<5^4) and at most five powers of 3 (200<3^5). The two 3-anchors therefore contribute at most 8 remaining points, and the one 5-anchor at most 5, for a total of 13 points.

Removing at most three intervals and 13 points leaves at most 17 components of total length at least 97X/100. One component has length at least 97X/1700 and contains no shift. Endpoints need not belong to S. QED.

For every sufficiently large X, choose an integer n just to the left of the right endpoint of this gap. Every s<=n in S then satisfies

    n-s >= X/20-2 >= n/40-2.

Thus arbitrarily large n require a linear-sized residual in every possible original representation. This is a statement about shift geometry, not a claim that such n are unrepresentable.

## I2-D3. Small-coordinate and greedy-square exclusions

For X>=2 and Y>=0, the number of n<=X admitting an original representation with min(a,b)<=Y is at most

    (floor(Y)+1)(floor(sqrt(X))+1)
      (floor(log_3 X)+1)(floor(log_5 X)+1).

### Proof

Relabel the two square variables so that the smaller one is first. There are at most floor(Y)+1 choices for it, floor(sqrt(X))+1 for the other, and the displayed exponent bounds. Counting all quadruples is an upper bound on the number of distinct n. QED.

It follows that any requirement Y=o(sqrt(X)/(log X)^2) covers only o(X) integers. This includes one square identically zero, a bounded/polylogarithmic square coordinate, or a coordinate bounded by X^(1/2-epsilon) for fixed epsilon>0.

For the strict greedy method, each candidate residual m is tested only with a=floor(sqrt(m)). If successful, the other coordinate satisfies

    b^2=m-a^2<2sqrt(m)+1<=2sqrt(X)+1.

Its support therefore has cardinality O(X^(3/4)(log X)^2)=o(X).

More generally, testing the K nearest descending choices for the larger square gives b^2<=2K sqrt(X) (up to harmless boundary constants), and hence support

    O(sqrt(K+1) X^(3/4)(log X)^2).

This is o(X) when K=o(sqrt(X)/(log X)^4). This excludes the stated restricted algorithm, not every argument one might call a nearest-square method.

## I2-P1. Literal-base joint 2-adic/3-adic local count

For m>0 define

    L2(m)=1{m/2^v2(m) == 1 mod 4},
    L3(m)=1{v3(m) is even}.

These are necessary local norm conditions; they are not sufficient for a global sum of two squares.

Let L=log n and, for n sufficiently large, put

    C=floor(log_3(n/4)), D=floor(log_5(n/4)),
    T23(n)=sum_{0<=c<=C; 0<=d<=D} L2(n-3^c-5^d)L3(n-3^c-5^d).

Every residual here is at least n/2, so it is positive. Uniformly in the integer n,

    T23(n)=lambda(n mod 24)(C+1)(D+1)+O((log n)^(5/3)),

where the implied constant is absolute and

| n condition | lambda |
|---|---:|
| 3 divides n | 1/2 |
| n odd and 3 does not divide n | 5/16 |
| n mod 24 in {2,4,8,22} | 7/32 |
| n mod 24 in {10,14,16,20} | 13/32 |

In particular the two local conditions together retain asymptotically at least 7/32 of the bulk exponent rectangle, for every n. This does not assert any positive proportion survive all other bad primes.

### Step 1: the 2-adic calculation

Conditional on c parity, 3^c is uniform in its coset 1 or 3 modulo 8 in the 2-adic limit: 9 generates 1+8 Z_2. Conditional on d parity, 5^d is uniform in its coset 1 or 5 modulo 8: 25 generates 1+8 Z_2. These facts follow as well from

    v2(9^(2^j)-1)=j+3, v2(25^(2^j)-1)=j+3.

For uniform m in a fixed class r mod 8, the local norm proportions are respectively

    r=0,1,2,3,4,5,6,7:
      1/2,1,1,0,1/2,1,0,0.

For r=0 this uses sum_{e>=0}2^(-e-2)=1/2; the value m=0 has Haar measure zero. For r=4 the odd part is uniform modulo 4.

If n is odd, averaging over c parity gives probability 1/2 for either fixed parity of d.

If n is even, one d parity gives probability 3/4 and the other 1/4. The favored parity is

    d odd  when n == 0 or 2 mod 8;
    d even when n == 4 or 6 mod 8.

### Step 2: the 3-adic calculation and shared parity

Discard temporarily c<k3 and work modulo 3^k3. Then 3^c vanishes modulo that modulus. Conditional on d parity, 5^d is uniform in its unit coset modulo 3, since 25 generates 1+3 Z_3; explicitly ord_{3^k}(5)=2*3^(k-1).

If 3|n, all residuals are units at 3 and pass L3. Otherwise one d parity matches n modulo 3, and the other does not. For the matching parity the residual is uniform in 3 Z_3 and

    Prob(v3(m) positive and even | 3|m)
      =sum_{j>=1} 2/3^(2j)=1/4.

For the nonmatching parity the probability is 1. The matching parity is even for n==1 mod 3 and odd for n==2 mod 3.

Conditional on the shared d parity, the remaining 2-power and 3-power exponent components are independent by the ordinary finite CRT. Thus if n is odd and 3 does not divide n, the joint factor is (1/2)*(1+1/4)/2=5/16.

For even n coprime to 3 it is

    (1/2)((3/4)(1/4)+(1/4)*1)=7/32

when the matching parity is favored at 2, and

    (1/2)((1/4)(1/4)+(3/4)*1)=13/32

otherwise. Enumerating the classes modulo 24 gives the table. Notice that multiplying unconditional 2-adic and 3-adic densities would give the wrong answer in these classes.

### Step 3: uniform finite-height error

Choose q2=2^k2 and q3=3^k3, both within fixed multiplicative constants of L^(1/3), with k2>=3. A pair of finite lower/upper local indicators can be determined from the residual modulo q2 and q3. At 2 the ambiguous classes are divisible by 2^(k2-1), not merely 2^k2: the odd part modulo 4 needs one extra bit. At 3 the ambiguous class is zero modulo q3.

On a complete exponent torus the proportion of ambiguous points is

    O(1/q2+1/q3),

uniformly in n. For example, for each c the 2-adic ambiguity has probability at most 8/q2; the 3-adic ambiguity has probability at most 3/(2q3) if n is a unit, and zero otherwise. Lower and upper torus densities therefore differ from the limiting lambda by at most this quantity.

After removing c<k3, the indicators have periods

    Tc=2^(k2-2),
    Td=lcm(2^(k2-2),2*3^(k3-1))=2^(k2-2)3^(k3-1).

Counting complete rectangles and their boundary strips incurs

    O(Tc(D+1)+Td(C+1)+Tc Td)=O(L^(5/3)).

The ambiguous residues contribute O(L^2/q2+L^2/q3)=O(L^(5/3)). The discarded c values contribute O(k3(D+1))=O(L log L), which is smaller. Replacing the shortened rectangle by (C+1)(D+1) has the same smaller cost. The upper and lower estimates give the theorem. QED.

### Adversarial checks and limitations

The program enumerates lower/upper local densities at (k2,k3)=(5,2),(7,4),(8,5), for all 24 basic classes and 24 nontrivial lifts. Every exact rational bracket contains the stated lambda. This finite check is an audit, not the proof of the uniform asymptotic.

The O(L^(5/3)) error can be larger than the main term at the modest numerical ranges scanned here. The table is not claimed to be a high-precision predictor at n<=10^7. It is not the full singular series, does not eliminate primes 7,11,19,..., and is not an inverse theorem for the original exceptional set.

## I2-L1. The correct size-completion lemma (background, not claimed as new)

Suppose m>0, L2(m)=1, and vp(m) is even for every prime p==3 mod4 with p<=sqrt(m). Then m is a sum of two squares.

Indeed, the product of the distinct bad primes with odd valuations is 1 modulo 4, because the odd part of m is 1 modulo 4. A nonempty such set therefore has even cardinality. If all its primes exceed sqrt(m), it has at least two distinct primes whose product exceeds m, an impossibility. The set must be empty.

At a lower cutoff m^(1/3), two primes larger than the cutoff can still occur with product at most m. A statement that merely bounds the number of remaining primes is not a completion proof. The repository already studied square-root-cutoff methods; this lemma is not promoted as a new result.

## I2-L2. No arithmetic progression alone certifies a norm (background)

For any M>=1 and residue r, choose a prime q==3 mod4 not dividing M. The CRT system

    m==r mod M, m==q mod q^2

has infinitely many positive solutions. Each has vq(m)=1 and is not a sum of two squares. Hence no nonempty arithmetic progression, even with an arbitrarily large lower size bound, consists entirely of norms. A modulus-based positive construction needs an additional non-congruence ingredient.

## What remains unproved

No lower bound R(n)>=1 for every sufficiently large n was obtained. No effective finite threshold for the original conjecture was obtained. No new structural theorem about E(X)={n<=X:R(n)=0} was obtained. The exact local theorem and the scoped route exclusions constitute a Level D direct reset, not Level C/B/A.
