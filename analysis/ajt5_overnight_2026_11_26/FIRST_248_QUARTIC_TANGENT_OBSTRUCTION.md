# The direct integer tangent test fails for the actual first-root quartic

Let $F(t)$ be the precise first-root quartic in FIRST_248_TWO_DIRECTION_TRIPLE.md. Its coefficient valuations, constant first, are $(1,6,6,9,10)$ at the prime 2. The replay below verifies the coefficients modulo $2^{16}$ without expanding the huge powers of 5.

For integer $u,t$, put $D_u(t)=(F(t)-F(u)-F'(u)(t-u))/(t-u)^2$, evaluated as a polynomial also at $t=u$. If the coefficients of $F$ are $a_i$, then
$$
 D_u(t)=a_2+a_3(t+2u)+a_4(t^2+2ut+3u^2).
$$
Thus $v_2(D_u(t))=6$, $v_2(F(u))=1$, and $v_2(F'(u))=6$, all for every integer argument. It follows that the auxiliary integer $4 F(u)D_u(t)-F'(u)^2$ has valuation exactly 9 and can never be a square. This rules out the direct choice $R=F,\ Q(t)=t$ in [Grechuk–Agbanwa, Proposition 2.2](https://arxiv.org/abs/2607.06627). It does not show that the quartic itself never represents a square sum, or rule out other parametrizations or a nontrivial choice of composition.

Append this to the replay in FIRST_248_TWO_DIRECTION_TRIPLE.md:

```python
mod=2**16
u0=U(0,mod)
g=a*a+b*b
D1=-K*(J(d,mod)-g+2*(a*B[0]+b*B[1]))
D2=-K*K*g
uv=[u0,(-b*D1,a*D1),(-b*D2,a*D2)]
coeff=[pow(5,E+1,mod)-239,0,0,0,0]
for i in range(3):
    for j in range(3):
        coeff[i+j]+=20*(uv[i][0]*uv[j][0]+uv[i][1]*uv[j][1])
assert [x%mod for x in coeff]==[45514,3008,62528,26112,13312]
assert [((x%mod)&-(x%mod)).bit_length()-1 for x in coeff]==[1,6,6,9,10]
```
