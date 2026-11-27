# A primitive compatible seed for the first root 248 and a one-sided sieve density

The exact arithmetic below certifies an actual first root $248$ and an adjacent true column at $d=4$ in the same old 17-prime congruence class. It also gives a primitive difference vector, the input for a geometric counting argument. This note does not assert an asymptotic lower bound for the number of columns.

Use $L(a,b)=(2a+b,a-2b)$, so $L^2=5I$ and $\|L U\|^2=5\|U\|^2$. The seed has $V=L(U)$, $m=626+\|U\|^2$, $x=5m+4$, and $x=3134+\|V\|^2=248+\|S\|^2$. Each possible numerical root below 248 has a named inert prime at exact valuation one; these assignments persist through modulus $M$. The resulting 20 obstructions imply 248 is the least true root for this $x$.

The variables $\Delta=S-V$ and $w=S+V$ satisfy $\Delta\cdot w=2886$, and $\Delta$ is primitive. In the same vector classes modulo $100M$, replace the right hand side by $H=5^{d+1}-239$ with $d=4+kP$. The displayed modular powers give $H\equiv2886\bmod100M$. Any integer solution $(\Delta,w)$ in those classes recovers $V=(w-\Delta)/2$, $S=(w+\Delta)/2$ and $U=L(V)/5$, with all coordinates integer, $m=5^d+1+\|U\|^2$, and both norm identities at the same $x$. The checks on residues suffice because shifts of $\Delta,w$ by $100M$ shift $V,S$ by $50M$.

There is also a simple exact local sieve ratio. For an odd split prime $p\equiv1\bmod4$ away from the fixed modulus, allow all $\Delta\ne0$ modulo $p$ and $2\Delta\cdot V=H-\|\Delta\|^2$. There are $p(p^2-1)$ solutions. Remove the parent vector $V$ on one isotropic line $L_p$ (equivalently, remove one Gaussian factor direction). If $\Delta\notin L_p=L_p^\perp$, there is exactly one $V$ on that line; this supplies $p^2-p$ deletions. If $\Delta\in L_p\setminus\{0\}$, the condition vanishes on the line precisely when $p\mid H$, which adds $p(p-1)$ deletions. The combined deletion ratio is $(1+1_{p\mid H})/(p+1)$. This calculation gives local data for an orientation sieve, without assuming that the two norm conditions are independent.

Replay (Python standard library):

```python
from math import gcd, isqrt, prod

M = 9347826066398882709188429669140410838620697995580440275819854118709839842706586206254981282837544384679264569603
P = 6794538543090173141159605868485890378482780024489277462090887580403986045899337581148450
x0 = 25750794589

U = (
    157353088100171132182977391956579959133519787047402755449234815876452680282328738327502504456403250986332077088964414197832780927989754340212074049917465933706436574857849522486810632839806005017808524748491584143744763635238051441722,
    471994533302592483714840661799687141258567589836218070593555801950335984904223403538341555874721816763280305502350502150156590809237455991596528791942935729386425077400068689475444247940932773675875565440635036551937485383344378730336,
)
V = (
    786700709502934748080795445712847059525607163931023581492025433703241345468880880193346564787528318735944459680279330545822152665216964672020676891777867596799298227115767734449065513620544783711492614937618204839427012653820481613780,
    -786635978505013835246703931642794323383615392625033385737876788024219289526118068749180607293040382540228533915736590102480400690485157642980983533968405525066413579942287856464077863042059542333942606132778488960130207131450706018950,
)
S = (
    786700709502934748080795445712847059525607163931023581492025433703241345468880880193346564787528318735944459680279339893682160404538580106882881401986564074184275565998626816649191920838779343708861655771723462604138459238084707939381,
    -786635978505013835246703931642794323383615392625033385737876788024219289526118068749180607293040382540228533915736580753851172723179650783303727460554559380989153094837668253225977409013550425739630551638021302884925552388925671239425,
)

def norm(z):
    return sum(t*t for t in z)

m = 626 + norm(U)
x = 5*m + 4
delta_seed = tuple(s-v for s, v in zip(S, V))
w_seed = tuple(s+v for s, v in zip(S, V))
ell0 = 100*M

assert V == (2*U[0]+U[1], U[0]-2*U[1])
assert x == 3134 + norm(V) == 248 + norm(S)
assert gcd(*delta_seed) == 1
assert m % 4 == 2 and x % M == x0 % M
assert m.bit_length() == 1553 and m % 10**18 == 315129758168998806
assert tuple(t % 50 for t in V) == (30, 0)
assert tuple(t % 50 for t in S) == (31, 25)
assert norm(V) % 125 == 25
assert pow(5, P, M) == 1
assert pow(5, 5+P, ell0) == pow(5, 5+2*P, ell0) == 3125

# Each listed root has exact valuation 1 at its assigned prime.
blockers = {
    7: (2, 86, 128), 11: (14,), 31: (6,), 19: (26,),
    43: (134,), 59: (34, 152), 71: (52,), 131: (8,),
    139: (4,), 191: (206,), 251: (32,), 1847: (10,),
    11551: (126,), 13259: (106,), 66571: (82,),
    1716719623: (244,), 8583598187: (28,),
}
assert M == prod(p**(3 if p in (7, 11, 31) else 2) for p in blockers)
assert {t for roots in blockers.values() for t in roots} == {
    5**e + 3**f for e in range(4) for f in range(6) if 5**e + 3**f < 248
}
for p, roots in blockers.items():
    assert p > 3 and p % 4 == 3
    assert all(p % q for q in range(2, isqrt(p)+1))
    for t in roots:
        assert (x0-t) % p == 0 and (x0-t) % (p*p) != 0
```
