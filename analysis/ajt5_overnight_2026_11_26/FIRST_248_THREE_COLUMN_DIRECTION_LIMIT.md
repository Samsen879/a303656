# A common-direction obstruction and height cost for three actual columns

Keep the first-root-248 class and period $P$. For three specified same-parity indices $d_1<d_2<E$, consider a linear model for the normalized parent coordinates: a common affine motion, with three fixed intercepts, whose squared norms differ by the required constants. Equal linear terms in each norm difference force the intercept differences perpendicular to the common nonzero direction. Write them as $s_iG$ for primitive integral $G$, signed nonzero integers $s_i$, and set $g=\|G\|^2$, $q=G\cdot U$. Then necessarily
$$
 D_i=(5^E-5^{d_i})/4=s_i(2q+gs_i),\qquad i=1,2.
$$
The true parent residuals normalized by $4$ are odd, so all three vectors have opposite coordinate parities. If $g$ is odd, each $s_i$ must therefore be even. This gives $D_i/4=r_i(q+gr_i)$ with $s_i=2r_i$.

For the actual labels $(d_1,d_2,E)=(4,4+2P,4+4P)$, the normalized differences $(D_1/4,D_2/4)$ are $(2,3)\bmod4$, as the replay checks. If $g$ is odd, the second product being odd makes $r_2$ odd and $q$ even. The first product being even then forces $r_1$ even, so that product is $0\bmod4$, a contradiction. Thus no common affine direction with odd transverse norm works for this actual triple, even though every pair of these labels can coexist by FIRST_248_COMPATIBLE_COLUMN_PAIRS.md. This does not exclude even transverse norms or nonlinear constructions.

There is also a height cost without any parity restriction. Fix the first two labels $d<e$, put $\Delta=(5^e-5^d)/4$, and let the largest $E$ grow with $T=(5^E-5^e)/4$. With the middle slot as origin, the first projection $q_e$ obeys $\Delta=s(2q_e+gs)$, so $|s|\le\Delta$ and $|q_e|\le g\Delta$. The required decrease to the last slot forces a squared projection $q_e^2-gT\ge0$. Thus $g\ge T/\Delta^2$. A single line with that primitive step has at most $1+\sqrt{X/g}$ integer parameters with $m\le X$, since its parent norm is at most $X/4$. The estimate concerns one affine line and already holds before testing the first-root norm; it imposes no such restriction on a union of many directions.

```python
P=6794538543090173141159605868485890378482780024489277462090887580403986045899337581148450
a,b,c=(pow(5,4+k*P,64) for k in (0,2,4))
assert (a,b,c)==(49,33,17)
assert ((c-a)%64//16,(c-b)%64//16)==(2,3)
assert all(not ({(r*(q+g*r))%4 for r in range(4)} >= {2,3})
           for q in range(4) for g in (1,3))
```
