# Two-axis protected closure and cross-axis acyclic routing

**Two-axis repair can shrink the protected closure, and an acyclic assignment can charge every row that remains, including ordinary ancestors.** The resulting growing-prefix criterion needs a bounded-cofactor condition on the assigned orders. At the actual terminal \(71\), the \(5\)-axis keeps \(7\) out of the closure, although the \(3\)-axis reads it.

### Two-axis closure and assignment

Fix exponent strides \(A_3,A_5\) and initial conditions at \(2,3\). An axis \(g\in\{3,5\}\) is eligible to repair an inert \(p>3\) if \(g\) is ordinary at \(p\), \(p\nmid A_g\), and its first \(p\)-primary digit is available. Start the protected set with the terminals and the rows with no eligible axis. Then add an earlier row \(p\) precisely when **each** of its eligible axes is read by some protected row. On axis \(g\), a protected row \(t\) reads \(p\) when \(p\mid\operatorname{ord}_t(g)\).

At the fixed point, each remaining row has an eligible axis unread by the protected set. Repair those rows in increasing prime order. A repair can give exact valuation two at its own prime and preserves both the protected rows and the already repaired rows. The latter have no exponent-period factor as large as the new repair prime. [Finite-obstruction and ordinary-primary repair framework](https://raw.githubusercontent.com/Samsen879/a303656/d11b5bd3209a45b0485c7200e30567e1349aa32e/analysis/ajt5_overnight_2026_11_26/SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md)

To obtain units at the protected rows, assign each row to one active primary coordinate \((g,\ell)\) that it reads. Draw an arrow from every active **opposite-axis** coordinate it reads to its assigned coordinate. Require this graph to be acyclic and the load at each coordinate to be less than one, with row cost
\[
\ell^{-v_\ell(\operatorname{ord}_p(g^{A_g}))}.
\]
Choose the coordinates in topological order. When a row’s assigned coordinate is reached, the opposite-axis term is settled modulo \(p\). A collision then forbids at most one projected primary residue. Other coordinates on the assigned axis can be chosen later, since they cannot undo exclusion by that projection. This is why the ordering condition only uses cross-axis arrows.

### A growing-prefix condition that charges the ancestors

Apply the following hypothesis to **every** row of the resulting closure. On its assigned axis \(g\), require
\[
\operatorname{ord}_p(g)=u\ell^e,
\qquad 1\le u\le B,\quad 1\le e\le K_\ell .
\]
For fixed strides and sufficiently large \(\ell>B\), put \(C_g=\log(g+1)\sum_{u\le B}\varphi(u)\). At coordinate \((g,\ell)\),
\[
\sum_{p\text{ assigned here}}\nu_{p,g}\ell^{-e}
\ \le\ \frac{C_g H_{K_\ell}}{\log\ell},
\qquad
\nu_{p,g}=
\begin{cases}
2&g\text{ nonordinary at }p,\\
1&g\text{ ordinary at }p .
\end{cases}
\]
For each \(u,e\), the primes contribute \(p^{\nu_{p,g}}\) to \(\Phi_{u\ell^e}(g)\). Use \(\log p\ge e\log\ell\) and \(\log\Phi_{u\ell^e}(g)\le\varphi(u\ell^e)\log(g+1)\), then sum over the layers. The bound includes ordinary ancestors at their full cost.

In particular, \(K_\ell\le\ell^\delta\) with \(\delta<1/\max(C_3,C_5)\) makes every sufficiently large coordinate safe. The small coordinates can be checked once: their assigned orders lie in a finite set, so their possible rows lie among prime divisors of finitely many \(g^{u\ell^e}-1\). This gives a sufficient condition for growing prefixes without a separate assumption on the load of an unbounded ancestor core. The remaining hypothesis is substantive: each closure row needs an assignment of the stated shape in an acyclic order. I have not established that for a cofinal family of actual prefixes.

### Actual \(3,5\) CRT control

At \(q=71\), the two orders are \(35\) and \(5\). Thus \(7\) is read on the \(3\)-axis and unread on the \(5\)-axis, where it is ordinary. Row \(11\) is nonordinary on base \(3\), but is ordinary on base \(5\) and unread by \(71\) there. All other earlier inert unit rows have an eligible \(3\)-axis. With both strides equal to \(8\), the protected core is just \(\{71\}\), and it can use the \(5\)-primary coordinate on the \(3\)-axis. This gives local phases through \(71\) for every target after choosing the initial \(2,3\) anchor.

At the pinned target below, with the other coordinates fixed, **every** \(3\)-axis repair of \(7\) makes \(71\) a nonunit. The \(5\)-axis repair has exact valuation two at \(7\), preserves the terminal residue modulo \(71^2\), and passes the whole earlier panel.

```python
from math import isqrt

q = 71
P = tuple(p for p in range(7,q+1,4)
          if all(p % k for k in range(2,isqrt(p)+1)))
def order(g,p):
    return next(k for k in range(1,p) if pow(g,k,p) == 1)
assert (order(3,q),order(5,q)) == (35,5)
assert [p for p in P[:-1] if pow(3,p-1,p*p)==1] == [11]
assert all(pow(5,p-1,p*p)!=1 for p in (7,11))

def two(z):
    return z%4==1 or z%8==2 or z%16==4 or z%32==8
assert all(any((n-5**d)%3 and two(n-5**d-3**c)
               for d in (2,3) for c in range(8)) for n in range(96))

n = 23785997169091798839
L, E = 9189152280, 7501348800
assert (n%4,n%3,n%343,n%(q*q)) == (3,0,107,3358)
assert all(n%p==0 for p in P if p not in (7,q))

def rem(m,c,d):
    return (n-pow(3,c,m)-pow(5,d,m)) % m

# The first 7-primary digit is the whole relevant 3-axis dependence.
assert pow(3,7*E,49)==pow(3,7*E,q)==1
assert [t for t in range(7) if rem(49,L+t*E,L)==0] == [1]
assert [t for t in range(7) if rem(q,L+t*E,L)==0] == [1]
assert rem(343,L+E,L)==49 and rem(q*q,L+E,L)==q

# The other axis repairs 7 and preserves the terminal.
c,d = L,L+E
assert rem(343,c,d)==196
assert rem(q*q,c,d)==rem(q*q,L,L)!=0
assert rem(4,c,d)==1 and rem(3,c,d)!=0
assert all(rem(p,c,d)!=0 for p in P if p!=7)
```

The pinned calculation concerns congruence phases. A sufficiently large positive lift of \(n\) preserving the displayed CRT residues makes those particular exponents active. The theorem gives no ordinary-height bound at a prescribed target, and passage through a finite prime panel gives no two-square certificate.

Independent BigInt replay checked both exact order profiles, the unique wrong-axis first digit and valuation-one terminal hit, and the true right-axis repair preserving the complete earlier panel. The growing-layer theorem is conditional on actual acyclic assignments for the whole closure.
