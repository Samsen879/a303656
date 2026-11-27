# A stopping rule for isolated ordinary relays

This conditional result concerns the tail with its starting threshold fixed, doubly ordinary inert rows of precision at least two, and a frozen starting phase with the parent remainder divisible by its prime. All other rows must continue to pass on the variations used. It does not assert that a minimal obstruction has such an isolated path.

**An isolated one-reader obstruction passes a full torsion family to its successor.** If that successor is ordinary to both bases and the target has valuation one there, it cannot pass the obstruction on to just one more reader. In the verified chain \(7\to43\to98299\), this stops the relay at \(98299\).

### Order and precision restriction

Work in the tail \(c\ge v_3(M)\), with the threshold held fixed. At an inert prime \(p>3\) ordinary to both bases, open both \(p\)-primary exponent coordinates through their full periods. Fix the other primary coordinates and require all rows except \(p\) and a single higher reader \(R\) to pass throughout this variation.

If \(R\) blocks every repair at \(p\), it must read exactly one \(p\)-digit on each axis, have \(n\equiv0\pmod R\), and have matching order-\(p\) characters along the first repair line. A deeper reader cannot exhaust the lifts at a first repair point. At precision at least four, the parent passes on the lifts of valuation two, which occupy \(1-1/p\) of that fibre. A deeper reader can veto at most \(1/p\). The shallow assertion is the single-reader cut. [Activated cut](https://github.com/Samsen879/a303656/commit/2af5c06473546891fec7b13988110a5f39f32eca) · [Depth-four baseline](https://github.com/Samsen879/a303656/commit/758d227b3425027e872e1dc71cd2a97aa9a66b97)

Each of the \(p\) first repair points lifts to a pass at the **full** precision of \(p\). These lifts do not alter \(R\), which reads only the first digit. The matching characters agree modulo \(R^{e_R}\), since their order is prime to \(R\). So the repaired family gives powers
\[
(UT,VT),\qquad T\in\mu_p
\]
at \(R^{e_R}\), with the same \(R\)-primary exponent coordinates in the full periods. If \(R\) is doubly ordinary, opening its coordinates gives first repair lines with right-hand side
\[
(n/R)T^{-1}-(U+V)/R\pmod R.
\]
When \(v_R(n)=1\), these are \(p\) distinct parallel lines. A single further reader that can cover a whole line has a fixed \(R\)-primary collision line across this family. It can cover at most one. This stopping rule assumes the other rows pass on the resulting family and its opened coordinates. Additional active readers are a separate case.

For nonzero \(n\), if \(m\) successive ordinary rows \(R_1<\cdots<R_m\) receive such a family and each relays to a single reader, then \(\prod_iR_i^2\mid n\). Each succeeding prime is at least \(2R_i+1\), because its order reads the \(R_i\)-digit. Hence
\[
|n|\ge R_1^{2m}2^{m(m-1)}.
\]
In particular, squarefree \(n\) permits no two consecutive isolated relays through a doubly ordinary intermediate row.

There is a separate precision constraint. If \(p^e\) is essential in a divisor-minimal tail modulus, lowering to \(p^{e-1}\) gives a witness with residual of odd valuation \(e-1\). On either ordinary axis, moving just the \((e-1)\)-st primary exponent digit can make that residual zero while holding all readers of at most \(e-2\) digits fixed. Some reader of depth at least \(e-1\) must then actually veto. At depth four this requires a **third-digit reader on each axis**, beyond the shallow reader of the original cut. The published depth-four block therefore cannot supply a precision-essential fourth power on a path with just that one structural reader. [Exact precision closure](https://github.com/Samsen879/a303656/commit/fac27d29f366a0aed19e2ce917577d8084e9166e)

### Replay at the next row

For the original target, \(v_{98299}(n)=1\). The replay takes all 43 first points of the repair line at 43, lifts each to zero modulo \(43^4\), and verifies that they give 43 distinct repair lines at 98299. It then opens the 98299 digits and lifts every one of those phases to zero at all three prime powers, preserving both predecessors.

```python
from math import lcm

q,R = 43,98299
n,d0 = 487145982612429033,33697459974838
L = lcm(42,(R-1)*R//q)
J = lcm(42*q**3,R-1)

def r(c,d,m):
    return (n-pow(3,c,m)-pow(5,d,m))%m

T = pow(3,L,R*R)
assert T==pow(5,41*L,R*R) and pow(T,q,R*R)==1 and T%R!=1
assert n%(R*R)==R and (3+pow(5,d0,R*R))%(R*R)==0
assert all(pow(a,J,m)==1 for a in (3,5) for m in (49,q**4))
B = pow(5,d0,R)*((pow(5,J,R*R)-1)//R)%R
lines=set()
for t in range(q):
    c,d=1+L*t,d0+L*(41*t%q)
    for h in (2,3):
        z,step=q**h,q**(h-1)*L
        delta=r(c,d,z*q)
        assert delta%z==0
        slope=pow(5,d,q)*((pow(5,step,z*q)-1)//z)
        d+=step*(delta//z*pow(slope,-1,q)%q)
    assert r(c,d,49)==r(c,d,q**4)==0 and r(c,d,R*R)==R
    rhs=pow(pow(T,t,R),-1,R)
    lines.add(rhs)
    d+=J*(rhs*pow(B,-1,R)%R)
    assert all(r(c,d,m)==0 for m in (49,q**4,R*R))
assert len(lines)==43
print("PASS")
```

The bound applies to an isolated, fully opened relay. A general minimal tail obstruction has yet to be shown to have that structure. The global closure still requires a common exceptional terminal in a minimal tail modulus, while this argument identifies where an ordinary one-reader path must stop or branch. Moving \(c\) below the tail threshold still requires checking the ternary row separately.

For the second relay, the fixed-line remark follows by projecting the ratio of the two powers at the higher reader onto its \(R\)-primary roots of unity. The upstream torsion factors have \(p\)-power order, with \(p\ne R\), so their projection is trivial and they cannot translate the \(R\)-primary line. They can prevent the collision from activating. At least \(1-1/R\) of second-digit lifts at a repair point pass at precision four or higher by having exact valuation two; at precisions two and three all lifts of the first repair point pass. Thus the size comparison against a deeper reader is strict for these inert primes.
