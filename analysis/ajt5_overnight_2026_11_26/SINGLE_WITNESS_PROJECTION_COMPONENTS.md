# Terminal projections: descent and independent components

Use the [terminal projection test](SINGLE_WITNESS_TERMINAL_PROJECTION.md): for each inert \(q\), \(U_q\) is the set of modulo-\(q\) shifts over all survivors of the earlier local tests for the same \(n\). The conclusion here is that **a first common Wieferich inert prime cannot be the first blocker**. A later common Wieferich inert prime is not excluded.

## Descent in the absence of a connected earlier exceptional prime

Build the retained digit constraint graph from the descending enumeration for \(q\). One may group the retained digits of each axis at each prime into one variable; each retained test is adjacent to the variables that compute its truncated residual, including its own primary coordinate when read. The modulo-\(q\) sum is an output, not a constraint vertex. Let \(R\) be the largest prime dividing either of the two modulo-\(q\) orders, and choose an \(R\)-primary variable read by the output. If its component contains no earlier retained test at \(p>R\), the following cases give two output values:
- For split \(R\), no \(R\)-test needs to be respected, and smaller primes never read the chosen variable.
- For inert \(R\) with \(|U_R|\ge2\), choose a phase passing the primes below \(R\) and with shift different from \(n_R\bmod R\). It then passes \(R\) as a unit. Changing the chosen \(R\)-digit preserves all these conditions because it does not affect the shift modulo \(R\) or at earlier primes. Pick two settings distinguished by the output on the chosen axis. Restrict both phases to the component and fill other components from any survivor of the full old head. All tests in this component are at most \(R\), and lossless retained enumeration makes this gluing valid.

If there is a retained test \(p>R\) in the component, either it is common Wieferich or an ordinary axis at \(p\) has a positive retained depth. In the ordinary case the test reads the first \(p\)-primary digit of that axis. That digit was retained by a later test that reads it, since the terminal orders do not involve \(p>R\). Follow such edges upward; a finite increasing chain must reach a common Wieferich test above \(R\) in the same component. Thus a singleton \(U_q\), if its chosen component has no such path, forces inert \(R\) and singleton \(U_R\). This is strict descent. It cannot end at \(3\), since both parities of \(d\) are possible at 2 for every observation there, giving \(U_3=\{1,-1\}\). For inert \(q>3\) the largest order factor cannot be 2: then the order of 3 divides 2, since \(v_2(q-1)=1\), which would require \(q\mid8\).

In particular, no singleton projection arises before or at the first common Wieferich inert prime. For the actual first blocking prime, there can be earlier common Wieferich tests which themselves pass; the proof does not dispose of their dependency paths.

## The full product of component tables

Fix one old survivor and call its two output powers \(A,B\in\mathbb F_q^\times\). For each component let \(P_C\) be its full table of possible relative multipliers \((u,v)\) on the two powers. Feasible combinations across components are independent because every old test is internal to a component, so
\[
 U_q=\{A\prod_C u_C+B\prod_C v_C:\ (u_C,v_C)\in P_C\}.
\]
For a singleton, every row must satisfy \(A(u-1)+B(v-1)=0\). In particular any variation on just one axis, or a rank-two span of the differences \((u-1,v-1)\), excludes a singleton. If two components vary, compare individually and jointly changing a nontrivial row in each. Subtraction gives \(A(u_1-1)(u_2-1)+B(v_1-1)(v_2-1)=0\). Using the individual equalities gives \(A+B=0\), since both nontrivial rows change both axes. Every component then has \(u=v\), and the two effective orders (lcm of orders of realized output-power ratios) coincide. In particular if the axes have different largest effective order primes, a singleton requires one varying component that contains both active sources, with its *full* table on a line giving a nonzero sum. A selected line of local solutions cannot substitute for the full table.

### Replay

For \(n=216315\) and terminal \(31\), independent active sources of orders 5 and 3 can yield equal output on a diagonal, but the two other corners of the same feasible rectangle give different outputs. The whole earlier-head output has 27 values. At 2 the first exponent is even, at 3 the residual is a unit, and the remaining inert primes below 31 can repair via ordinary lifts with their own primary digits unread by the output. This is a real order countercontrol to assuming that differing source primes imply pairwise distinct outputs.

~~~python
from itertools import product

n, q = 216315, 31
old = (3, 7, 11, 19, 23)

def order(a, p):
    return next(k for k in range(1, p) if pow(a, k, p) == 1)

def shift(c, d, p):
    return ((0 if p == 3 else pow(3, c, p)) + pow(5, d, p)) % p

assert (order(3, q), order(5, q)) == (30, 3)
assert order(pow(3, 6, q), q) == 5 and order(5, q) == 3
for c, d in product((2, 8), (1, 2)):
    assert (n - shift(c, d, 4)) % 4 == 1
    assert all((n - shift(c, d, p)) % p for p in old)
assert [shift(c, d, q) for c, d in product((2, 8), (1, 2))] == [14, 3, 25, 14]

assert n % 3 == 0 and n % 4 == 3
assert all(any(pow(a, p-1, p*p) != 1 for a in (3, 5))
           for p in old if p > 5)
U = {shift(c, d, q) for c in range(0, 30, 2) for d in range(3)}
assert len(U) == 27 and set(range(q)) - U == {0, 16, 18, 28}

~~~
