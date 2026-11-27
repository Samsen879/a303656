# Exact parity separation at the first root 248

Use the fixed class and period $P$ of FIRST_248_PRIMITIVE_SIEVE_SEED.md, with $m\equiv2\bmod4$, $x=5m+4$, $n=x-248$ and $d=4+kP$. The target adjacent column requires $n$ and $n-H_d$ to be sums of two squares, where $H_d=5^{d+1}-239$. This is the specific parent/child type studied in FIRST_248_UNWEIGHTED_RELATIVE_GROWTH.md.

There is **no** such integer with a true column from both the even and odd $k$ families. Indeed $P\equiv2\bmod4$, so $H_d\equiv6\bmod16$ for even $k$, and $14\bmod16$ for odd $k$. Since $n\equiv2\bmod4$, an actual norm $n$ must be $2$ or $10\bmod16$. In either case the second norm is $4\bmod8$ and so must be precisely $4\bmod16$. Thus an even-family true column requires $m\equiv6\bmod16$, while an odd-family true column requires $m\equiv14\bmod16$. These conditions cannot hold simultaneously. This uses only the residues and two actual norm conditions; the fixed modulus supplies the separate certificate that 248 is the first norm root.

Each family is nevertheless realized by unbounded true points. Let $V_0,S_0$ be the seed in the linked note, $\Delta=S_0-V_0$ primitive, choose an integer vector $B$ with $\Delta\cdot B=1$, and put $\eta=(-\Delta_2,\Delta_1)$. For any fixed $k\ge0$, the vectors
$$
 V=V_0+\frac{5^{d+1}-5^5}{2}B+50M t\,\eta,\qquad S=V+\Delta\quad(t\in\mathbb Z)
$$
preserve the seed's coordinate congruences modulo $50M$, since $5^{d+1}\equiv5^5\bmod100M$. Their norm difference is exactly $H_d$. Take $x=248+\|S\|^2=5m+4$; the congruences make $m$ an integer in the fixed class, the earlier-root obstructions persist, and $t$ unbounded assures positivity and eventual activation. Thus the cross-family zero is a genuine same-integer obstruction, not a failure of either family to have examples. It does not rule out simultaneously rich compatible subfamilies or decide the complete A303656 menu.

```python
P = 6794538543090173141159605868485890378482780024489277462090887580403986045899337581148450
assert P % 4 == 2
sums = {(a*a+b*b)%16 for a in range(16) for b in range(16)}
assert [pow(5,5+k*P,16)-239 for k in range(2)] == [-234,-226]
for k,target in [(0,[6]),(1,[14])]:
    h=(pow(5,5+k*P,16)-239)%16
    assert [m for m in range(2,16,4)
            if (5*m-244)%16 in sums and (5*m-244-h)%16 in sums] == target
```
