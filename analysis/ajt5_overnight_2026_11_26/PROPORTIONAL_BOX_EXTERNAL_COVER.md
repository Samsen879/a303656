# Near-total odd-valuation coverage outside a fixed panel

Fix any finite set P of primes congruent to 3 mod 4. For every sufficiently large real X there is an integer n in [X,2X) with n = 2 + u² + v² and n ≡ 0 mod p² for all p in P. In the common active rectangle
\[
 0\le c\le \lfloor\log_3(X/4)\rfloor,\qquad
 0\le d\le \lfloor\log_5(X/4)\rfloor,
\]
a fraction at least \(1-O((\log\log X)^{-1/2})\) of cells have \(v_q(n-3^c-5^d)=1\) at an inert prime \(5<q\le\sqrt{\log X}\) outside P. Thus they fail the genuine integer two-square test. At least \(1/4-O((\log\log X)^{-1/2})\) of all cells both fail this way and pass all the fixed-panel and 2-adic norm tests. The same assertion about near-total coverage holds simultaneously in all continuous subrectangles whose sides are each bounded below by a fixed positive multiple of \(\log X\), with a constant depending on that multiple. The choice of n is common to the whole rectangle.

## Proof

Set \(\delta=3^c+5^d-2\). Choose residues for u and v independently and uniformly modulo \(q^2\) for each auxiliary prime q. If \(q\nmid\delta\), the nonzero norm fiber over \(\mathbb F_q\) has \(q+1\) points by the surjectivity of the finite-field norm and the order \(q+1\) of its kernel. At each point the gradient of \(u^2+v^2-\delta\) is nonzero, so exactly q of its \(q^2\) lifts remain zero modulo \(q^2\). The probability of exact valuation one is \(a_q=(q+1)(q^2-q)/q^4=1/q-1/q^3\). When \(q\mid\delta\) we use only the lower bound zero. Write \(V=\prod_q(1-a_q)\) and \(b_q=a_q/(1-a_q)\). The probability a cell escapes is at most \(V\prod_{q\mid\delta}(1+b_q)\), by independence across primes; no independence across cells is used.

If there are J columns, the fraction of cells with \(q\mid\delta\) is at most \(1/\operatorname{ord}_q(5)+1/J\): on every row the admissible columns are empty or in one class modulo that order. To average the product, expand it into subsets and, for a nonempty subset, apply this bound at its largest prime q. The sum of its weights and those of the other subsets with largest q is \(b_q\prod_{t<q}(1+b_t)\), where t runs over the auxiliary list. The contribution from all \(1/J\) errors is at most \(1/J\) after multiplication by V. Since \(q\le 5^{\operatorname{ord}_q(5)}-1\), the order contribution before multiplication by V is at most a constant times \(\sum_q 1/(q\sqrt{\log q})<\infty\), by the prime-counting upper bound and partial summation. Here \(\prod_{t<q}(1+b_t)=O(\sqrt{\log q})\) by Mertens in progressions; the ratio between the products with factors \(1-a_q\) and \(1-1/q\) is bounded above and below. Thus some single choice of residues leaves at most \(O(V+1/J)\) of the cells uncovered. For the stated cutoff, [Williams's Mertens theorem in progressions](https://doi.org/10.1016/0022-314X(74)90032-8) gives \(V\asymp (\log\log X)^{-1/2}\).

For each fixed panel prime choose a pair whose norm is -2 modulo \(p^2\), using the nonzero norm fiber and the same lifting argument. Impose \(u\equiv1,\ v\equiv0\pmod8\) and combine by CRT. The resulting common modulus M satisfies \(\log M=O(\sqrt{\log X}\log\log X)=o(\log X)\), using even the trivial count of primes. Taking the smallest admissible \(u\ge\sqrt X\) and \(0\le v<M\) realizes n in the height band. On even-even cells \(3^c+5^d\equiv2\bmod8\) and n is 3 modulo 8, giving a 2-adic square. Also \(3^c+5^d\) is a unit at every panel prime: at 3 this follows separately for \(c=0\) and positive even c, and at every other inert prime both powers are nonzero squares and their sum cannot vanish. Restriction to any proportional subrectangle can lose at most the total number of uncovered cells in the whole rectangle. The origin has a genuine two-square witness by construction.

## Exact finite control

This supplies reproducible counts for a single point in \([2^{239},2^{240})\), using a separate finite \(150\times103\) activity rectangle (every residual is positive, as checked).

~~~python
u = 939906129562517635027009607335484817
v = 730661942054553584
n = 2 + u*u + v*v
P, Q = (3, 43, 79, 223), (7, 11, 19)
assert 2**239 <= n < 2**240
assert all(n % (p*p) == 0 for p in P)
hit = even = clear = 0
def strip(x, p):
    k = 0
    while x % p == 0:
        x //= p
        k += 1
    return k, x
for c in range(150):
    for d in range(103):
        x = n - 3**c - 5**d
        assert x > 0
        if any(x % q == 0 and x % (q*q) != 0 for q in Q):
            hit += 1
            even += (c % 2 == d % 2 == 0)
            clear += (strip(x, 2)[1] % 4 == 1 and
                      all(strip(x, p)[0] % 2 == 0 for p in P))
assert (hit, even, clear) == (4375, 643, 2140)
~~~

The 643 even-even hits are a distinguished subset of the 2140 hits which pass all fixed local tests. The theorem is existential in n within each height band. It does not certify every cell, furnish a counterexample to the original conjecture, or give a uniform positive statement for arbitrary n.
