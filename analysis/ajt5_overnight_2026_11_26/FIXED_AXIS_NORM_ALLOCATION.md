# Exact norm-shell allocation for one fixed exponent axis

Fix \(c=C_*(n)\) as in the [base-5 order-path test](ALL_EXPONENT_BASE5_ORDER_PATHS.md), and first fix a parity of \(d\). The 2-adic condition can be met with either parity by a higher 2-primary choice, and odd-prime orders at inert primes never read more than that parity. We may therefore treat the remaining phase as its odd-primary coordinates. The split prime 5 imposes no norm veto.

At inert \(p\), a collision modulo \(p\) in the selected parity has at most one exponent class \(e_p\bmod o_p\), where \(o_p=\operatorname{ord}_p(5)\). If there is no collision, ignore the row. Set \(w_p=v_p(5^{o_p}-1)\); within the colliding class the residual is fixed modulo \(p^{w_p}\). A nonzero even valuation below \(w_p\), or valuation zero, means that row always passes; an odd valuation below \(w_p\) requires avoiding the collision. Avoidance can be assigned to any odd \(r\mid o_p\), which forbids one ball \(e_p\bmod r^{v_r(o_p)}\) on that coordinate. A mismatched parity had already avoided it. If the residual is zero at depth \(w_p\), either assign an avoidance coordinate or assign a repair at \(p\) itself. Within the colliding class the lift is a ball parametrization, with residual valuation \(w_p+v_p(d_p-\alpha_p)\) at its unique lifted root \(\alpha_p\). For the repair, require the corresponding union \(S_p\) of even-valuation shells. Imposing the repair on phases that might turn out not to collide is harmless, because any such phase passes anyway.

For each assignment take the union \(B_r\) of forbidden balls on each coordinate, and take \(S_r=\mathbb Z_r\) if there is no self-repair there. The panel is feasible if and only if some assignment has \(\mu_r(S_r\setminus B_r)>0\) on every coordinate. Sufficiency follows from primary-coordinate CRT. For necessity read the assignment from a feasible phase: a noncolliding row picks a differing digit, a colliding row in the zero ball can choose self-repair. If the latter phase hits the exact lifted root, avoiding finitely many forbidden balls leaves a whole neighborhood of it, containing a positive-measure even-valuation shell. Thus exact roots do not obstruct the strict positive-measure test. To calculate the loads, delete redundant contained forbidden balls. Within a ball at depth \(a\) containing a repair root, the acceptable Haar fraction is \(r/(r+1)\) when \(w_r+a\) is even and \(1/(r+1)\) when it is odd; on other balls the constant valuation decides it. This uses full norm tests, not just first-residue unit avoidance.

## A necessary synchronization with a growth-box obstruction

Suppose \(q>5\) first blocks the [two-growth-axis box](SINGLE_WITNESS_FINITE_OBSTRUCTIONS.md) at the same \(n\), but the fixed \(C_*\) phase \(d\) passes through \(q\). In any compatible assignment for its old head, temporarily omit the 3-condition and call the resulting forbidden union on coordinate 3 \(B_3\). For the existing parity, let \(S_3^{\mathrm{grow}}\) be the allowed set for \(n-5^d\) at 3, and put \(a=v_3(\operatorname{ord}_q(5))\). Necessarily
\[
 S_3^{\mathrm{grow}}\cap(d_3+3^a\mathbb Z_3)\ \subseteq B_3
\]
when allowed sets are taken as finite-good valuation shells. Otherwise vary only the 3-primary digit inside that slice, allow the normalized 3-condition, and retain all old assigned tests and the condition at \(q\) (lifting the order at \(q\) adds only \(q\)-powers). At all other non-split primes keep the finite periods of \(c=C_*\), then let \(c\) grow in those periods. This gives a surviving growth phase and is a contradiction.

When \(3\nmid\operatorname{ord}_q(5)\) and the selected parity collides at 3, the normalized allowed set has measure \(1/4\) on the 3-primary coordinate. In the absence of a depth-one forbidden ball covering its root class, covering it requires balls in all three depth-two sub-balls: the two non-root sub-balls contain exact valuation-two phases, and the root sub-ball contains deeper even shells. The condition alone does not rule out such coverage.

## Exact controls

At \(n=11\), fixed \(C=0\) and growing \(3^c\) require opposite parities for a unit at 3, yet \(d=41\) on the same odd branch gives exact valuation two both for the growing 3-test and the fixed 7-test. For the larger same-\(n\) example, seven ordinary rows cover all unit escapes on the even branch, but one controlled prime-square lift passes all seven. That \(d\) is larger than the target's ordinary height, while the displayed different exponent pair gives a true witness. Neither example is an all-exponent blocker.

~~~python
assert (11-pow(5,41,27))%27==18
assert (11-1-pow(5,41,343))%343==294
N=2900803570375724211
P=(7,31,19,5167,271,4159,31051)
assert all(pow(5,54,p)==1 for p in P)
assert all(any((N-1-pow(5,d,p))%p==0 for p in P)
           for d in range(0,54,2))
assert (N-1-pow(5,162,343))%343==98
assert all((N-1-pow(5,162,p))%p for p in P[1:])
assert N==3**2+5**0+1051047365**2+1340187676**2
~~~
