# Full-prefix phase width and exact removal of ordinary rows

Use the pre-lift test in [the fixed-panel interface](FIXED_PANEL_EVEN_VALUATION_CONSTRUCTION.md): for inert primes \(p>3\), write \(o_{b,p}=\operatorname{ord}_p b\), \(s_{b,p}=v_p(b^{o_{b,p}}-1)\), \(L_3=\operatorname{lcm}(2,(o_{3,p})_p)\), \(L_5=\operatorname{lcm}(18,(o_{5,p})_p)\), and \(t_p=\min_b(s_{b,p}+v_p(L_b))\). Test the residual modulo \(p^{t_p}\), accepting zero and nonzero even valuation. Distinguish the **effective** row graph, joining CRT coordinates on which a row's truth value actually depends, from a graph defined solely by modular order divisibility.

For arbitrarily large \(k\), there are real \(3,5\) full inert prefixes, targets, and compatible parity/3-adic seeds whose effective row graph contains \(K_k\), even after omitting all \(t_p=1\) rows and even after identifying the two axes' coordinates at each prime. Conversely, for feasibility of the full finite panel, one can discard all rows outside the order-ancestor closure of its double Wieferich primes. This is a fixed-phase feasibility result with free coordinates and subsequent LTE lifting. It does not preserve every frozen assignment, control the least eligible representative in a short height window, or certify the absence of outside blockers.

## The full graph has no uniform width

For each inert prime \(p>3\) and \(a\ge1\), both cyclotomic quotients
\[
 (3^{p^a}+1)/(3^{p^{a-1}}+1),\qquad (5^{p^a}-1)/(5^{p^{a-1}}-1)
\]
are \(3\bmod4\). The first is an alternating geometric sum with every summand \(1\bmod4\); the second is an ordinary geometric sum with the same property. Any common prime factor with the corresponding denominator must divide \(p\), by substituting \(-1\) or \(1\) into the quotient polynomial. Neither quotient is divisible by \(p\), since its value modulo \(p\) is \(1\) (use \(3^{p^j}\equiv3,\ 5^{p^j}\equiv5\bmod p\)). Thus each has an inert divisor other than \(p\) and 3, with the order of the corresponding base exactly \(2p^a\) and \(p^a\), respectively. A full prefix including these divisors gives \(t_p\ge a+1\).

Now let \(m\) be the product of \(k\) distinct primes other than \(2,3,5\). Put \(K=\mathbb Q(\zeta_m)\), \(E=K(3^{1/m})\). Since 3 is unramified in \(K\), the polynomial is Eisenstein at a prime above 3. Thus \(E/K\) is cyclic of degree \(m\), and \(E/\mathbb Q\) is Galois. The field \(K\) is unramified at 2 and does not contain \(i\); \([E:K]\) is odd, so \(E\) cannot contain \(i\) either. In \(E(i)/\mathbb Q\), choose an automorphism trivial on \(K\), a generator on \(E/K\), and nontrivial on \(i\). [Chebotarev, Theorem 28.9](https://math.mit.edu/classes/18.785/2025/LectureNotes28.pdf#page=6) realizes its conjugacy class at infinitely many rational primes \(p\). Every such \(p\) is inert, is \(1\bmod m\), and has \(3\) not an \(\ell\)-th power modulo \(p\) for all \(\ell\mid m\): the Frobenius is nontrivial on \(K(3^{1/\ell})\), even though \(p\) splits in \(K\). Since the multiplicative group modulo \(p\) is cyclic, \(m\mid o_{3,p}\).

Select a full prefix with \(t_p\ge2\) and a target with \(n\equiv82+p\bmod p^2,\ n\equiv3\bmod24\). At \((c,d)=(4,0)\), the residual has exact \(v_p=1\), and the parity and 3-adic seeds are compatible. Let \(c\) change by \(L_3/\ell^{v_\ell(L_3)}\) at any \(\ell\mid m\), keeping everything else fixed. This changes only the chosen CRT coordinate and changes \(3^c\bmod p\), so the residual becomes a unit. All \(k\) coordinates are effective in one row. An actual target with an independent true representation can be chosen as \(n=A^2+B^2+3^6+1\): choose \(A\equiv1, B\equiv4\bmod24\), solve \(A^2+B^2\equiv p-648\bmod p^2\) by surjectivity of the finite-field norm and a linear lift of a nonzero coordinate, and combine by CRT. Adding multiples of \(24p^2\) to \(A\) makes the finitely many chosen phase representatives strictly active without changing their row tests.

## Exact ordinary-row removal

Let \(D\) be the actual panel primes with both \(s_{3,p},s_{5,p}\ge2\). In the panel make an arrow \(q\to p\) if \(p\mid o_{3,q}o_{5,q}\), necessarily \(p<q\), and let \(A\) contain \(D\) and its reachable vertices. Keep the original \(L_b,t_p\) and remove the rows outside \(A\). Starting from an assignment that passes the retained rows, restore removed rows in ascending order. For a removed \(p\), choose a base with \(s_{b,p}=1\). No retained larger row can read the \(p\)-coordinate, by the definition of \(A\), and no smaller row can read it, by the order formula and \(p\) being larger. The fixed seed does not read it either. If the row is rejected, vary just the \(p\)-coordinate on that base by multiples of \(L_b/p^{v_p(L_b)}\). LTE gives all principal changes modulo \(p^{t_p}\) because \(t_p\le1+v_p(L_b)\); thus the residue can be made zero. An accepted row needs no change. The lift in the linked interface then gives finite-panel even valuations. This argument does not require recomputing a smaller period or protecting values at deleted coordinates that were prescribed externally.

For a panel with cutoff \(y\), let \(B_0=\sum_{q\in D}\log_2 q\). Expand each \(q\in D\) into a tree by putting the distinct odd prime factors of \(r-1\) below each vertex \(r\). All odd coordinate primes read by retained rows occur in these trees. At each vertex, its \(\log_2 r\) minus the sum of its children's logs is greater than one, since their product is at most \((r-1)/2\). Summing over the trees telescopes, bounding the number of vertex occurrences by \(B_0\). The retained rows therefore read at most \(2B_0\) odd coordinates. Their relevant prime-power sizes are at most \(y\) (order factors are at most \(q-1\), and \(p^{t_p-s_{b,p}}\le p^{v_p(L_b)}\le y\) for a retained \(p>3\)); including compatible seed choices adds at most the factor 36. After projecting onto the retained rows, the product of relevant domain sizes has logarithm at most \(\log_2 36+2B_0\log_2 y\). This bound uses actual exceptional roots, not a hypothetical count of all ordinary rows.

## Independent finite replay

At \(p=211\) and \(y=2111\), the first actual full prefix activating that row has \(t_{211}=2\). The integer \(979755=223^2+964^2+3^6+1\) gives a rejecting cell at \((4,0)\) and one-variable flips on seven coordinates. Removing 2111 first and 211 next is legal: both are ordinary on the two bases and the only prefix row with an order divisible by 211 is 2111. The checks below use only the Python standard library.

```python
from math import isqrt, lcm

def is_prime(n):
    return all(n % d for d in range(2, isqrt(n) + 1))

def order(b, p):
    return next(j for j in range(1, p) if pow(b, j, p) == 1)

def prime_part(n, p):
    q = 1
    while n % p == 0:
        n //= p
        q *= p
    return q

p, y = 211, 2111
panel = [q for q in range(7, y + 1, 4) if is_prime(q)]
assert p in panel and y in panel and len(panel) == 163
bases = (3, 5)
O = [{q: order(b, q) for q in panel} for b in bases]
assert [o[p] for o in O] == [210, 35]
assert [o[y] for o in O] == [211, 1055]
assert all([q for q in panel if o[q] % p == 0] == [y] for o in O)
assert all(pow(b, o[q], q*q) != 1 for b,o in zip(bases,O) for q in (p,y))
L = [lcm(seed, *o.values()) for seed,o in zip((2,18),O)]
assert [prime_part(l,p) for l in L] == [p,p]
n = 979755
assert n == 223**2 + 964**2 + 3**6 + 1 and n % 24 == 3
R = lambda c,d: (n - pow(3,c,p*p) - pow(5,d,p*p)) % (p*p)
assert R(4,0) == p
cases = [(0,3,1,12029), (0,5,1,31888), (0,7,1,31474), (0,p,153,0),
         (1,5,1,30963), (1,7,1,40787), (1,p,161,0)]
for axis,ell,t,v in cases:
    c,d = [4 + (axis == 0)*t*(L[0]//prime_part(L[0],ell)),
           0 + (axis == 1)*t*(L[1]//prime_part(L[1],ell))]
    assert c % 2 == 0 and d % 18 == 0
    assert R(c,d) == v and (v == 0 or v % p)
```
