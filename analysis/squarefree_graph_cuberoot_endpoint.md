# Squarefree matching at the cube-root endpoint

**平方自由真边可以做到 \(J\ge C X^{1/3}\)；完整的 \(\sqrt{\log X}\) 轮仍有缺口。** 新的一步是分三段扣除平方尾项。对小平方因子直接估计商的高斯权，对中段只用截断权与素数个数，对大平方因子交换计数次序。这样在立方根端点扣掉的是真实非平方自由核心，最终计数单位是不同的实际 \(3,5\) 标签。

### 结论与原强度的差别

保留 [#104 的相位和指数窗](https://github.com/Samsen879/a303656/pull/104/files)。令
\[
L=\log X,\qquad K=J/X^{1/3},\qquad
z=\min(K^{1/4},X^{1/1000}),\quad Z=\log z,\quad
\beta=\log 2,\quad \Delta=\beta-\tfrac12.
\]
存在绝对常数 \(C,C_1,\rho>0\)。若 \(K\ge C\)、\(H\le X\)，则每个指定类中有 \(\gg J\) 个目标，任删至多 \(\rho L\) 个指数顶点后，仍有至少 \(\gg L\,\mathcal M\) 条不同平方自由真边和 \(\gg\mathcal M\) 轮边不交匹配，每轮含 \(\gg L\) 条边，其中
\[
\boxed{\displaystyle
\mathcal M=\sqrt L\,(Z/L)^\Delta
   \exp\!\left[-C_1\sqrt{\log(eL/Z)}\right].}
\]

- **立方根端点 \(K=C\)** 给出 \(\gg L^{1-\log 2}\exp(-C_1\sqrt{\log L})\) 轮，核心均平方自由。
- **亚幂尺度 \(K=\exp(L/g)\)**，若 \(g\to\infty\) 且 \(K\ge C\)，给出 \(\gg \sqrt L\,g^{-\Delta}\exp(-O(\sqrt{\log(eg)}))\) 轮。
- **固定幂余量 \(K\ge X^\varepsilon\)** 恢复 #114 的 \(\gg_\varepsilon\sqrt L\) 轮。上述亚幂式保留了明确损失。

### 圆盘范围与去重

记 \(f_z(u)\) 为通过 [#114](https://github.com/Samsen879/a303656/pull/114) 的高斯方向筛的坐标数除以四。它是乘法函数。对 \(3<p<z\) 的惰性素数只许指数零，对小分裂素数只许一个方向且指数至多一。对 \(p\ge z\) 的分裂素数，\(f_z(p^a)=a+1\)。

取筛层级 \(D=z^{1+\delta}\)，其中 \(0<\delta\le1/2\) 固定且足够小。对每个展开项，除去的高斯因子范数 \(t\le D^3\)。在 #107 圆盘式中，平方半径 \(x_t\ge X/(2D_0t)\)，模数 \(q=Q/D_0\le X^{2/3}/(D_0K)\)。因此逐项都有
\[
q/x_t^{2/3}\le 2^{2/3}D_0^{-1/3}D^2/K\ll K^{-1/4}.
\]
新剩余类仍是模 \(4\) 的 \(1\) 和模 \(3\) 的单位。绝对余项总和至多 \(O(X^{1/3}D(\log(2D))^2)\)，可由足够大的绝对 \(C\) 吸收。半维下筛因此给出每标签 \(\sum f_z(u)\gg J/\sqrt Z\)。即使 \(K\) 固定，也可先固定足够大的最小 \(z\)，再选择 \(C\)。 [#107 的圆盘界](https://github.com/Samsen879/a303656/pull/107/files) · [半维下筛定理 2.1](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

最坏点态去重因子 \(4\cdot2^{\log(3X)/\log z}\) 在这里过大。改用一致的 Henriot 上矩。令 \(0\le h\le1\)，则
\[
\sum f_z(u)^{1+h}\ll \frac{J}{\sqrt Z}(L/Z)^{2^h-1}.
\]
所有 \(f_z^{1+h}\) 都受 \(\tau^2\) 控制，共用增长参数。Euler 乘积的一阶项在小分裂素数为零、大分裂素数为 \((2^{1+h}-1)/p\)、惰性素数为 \(-1/p\)，二阶余项一致。取 \(h=(\log(eL/Z))^{-1/2}\)，可舍去超过
\[
U=(L/Z)^\beta\exp\!\bigl(C_2\sqrt{\log(eL/Z)}\bigr)
\]
的权重而只损失任意预先固定的小比例首矩，取 \(C_2\) 充分大即可。 [Henriot 修正定理 5](https://doi.org/10.1017/S0305004114000280)

### 三段平方尾项

对 \(p\ge z\) 有精确逐点不等式
\[
f_z(p^2m)\le 3f_z(m).
\]
分裂时这是 \(a+3\le3(a+1)\)，惰性时两侧的指数奇偶相同。设 \(P=X^{1/12}\)，\(Y=X^{1/3}L^{1/8}\)。以下估计均为逐标签，核心所在实区间的两端 \(\asymp X\)。

| 平方因子范围 | 扣除的权重上界 |
|---|---:|
| \(z\le p\le P\) | \(O(J/(z\sqrt Z))\) |
| \(P<p\le Y\) | \(O(U(J/P+Y/\log Y))\) |
| \(p>Y\) | \(O((X/Y^2+J/Y)/\sqrt Z)\) |

第一段把 \(u=p^2m\) 换成模 \(q\) 的既约商进程。其长度 \(J/p^2\ge X^{1/6}\)，索引基点 \(\gg X^{1/6}\)，线性式高度 \(O(q)\)。Henriot 可取长度指数和高度指数各 \(1/8\)，因此商的首矩为 \(O(J/(p^2\sqrt Z))\)。第二段对每枚素数计 \(J/p^2+O(1)\)，再乘截断权 \(U\)，所以只有 \(O(Y/\log Y)\) 个单位误差。

第三段先固定 \(m\le M\ll X/Y^2\)。同余 \(p^2\equiv a/m\bmod q\) 至多有八根，实区间在每个根类内至多给 \(O(1+J/\sqrt{Xm})\) 个候选。用 \(f_z(p^2m)\le3f_z(m)\) 即可，甚至无需在这一步保留 \(p\) 的素性。对 \(m\ge X^{1/12}\) 用同一首矩上界作二进求和，对更小的 \(m\) 用 \(\tau(m)\)。得到
\[
\sum_{m\le M} f_z(m)(1+J/\sqrt{Xm})
\ll (M+J\sqrt{M/X})/\sqrt Z .
\]
第一段由最小 \(z\) 吸收。后两段为 \(o(J/\sqrt Z)\)，一致允许 \(K=C\)，因为 \(U\sqrt Z\le L^{\beta+o(1)}\)、\(\beta+1/8<1\)，且 \(X/Y^2=X^{1/3}L^{-1/4}\)。因此截断后每标签仍有 \(\gg J/\sqrt Z\) 的**平方自由**权重。

### 从权重到真匹配及剩余阻碍

同一 Euler 乘积给出不同标签的混合上矩
\[
\sum_n f_z(u_\lambda)f_z(u_\mu)\ll
  (J/Z)\prod_{p\mid\lambda-\mu}(1+C_3/p).
\]
两式在有限坏素数以外的一阶项是单式首矩的一阶项的两倍。坏素数按单位斜率估计，实际差权仍可用原来的周期平均。这给出总权二阶矩 \(O(JL^4/Z)\)、顶点能量总和 \(O(JL^3/Z)\)。选出 \(\gg J\) 个总权 \(\gg L^2/\sqrt Z\)、能量 \(O(L^3/Z)\) 的目标。Cauchy–Schwarz 控制任意删点和极大匹配的顶点覆盖。每轮取固定小常数倍 \(L\) 条边，至多花费 \(O(LU)\) 的权重，故有 \(\gg L/(\sqrt Z U)\) 轮。每条边只按一个标签计数。 [原差权平均与删点提取](https://github.com/Samsen879/a303656/pull/105/files)

这个层级与矩接口有两个明确的限制。在最坏模数 \(q\asymp X^{2/3}/K\) 下，#107 的逐项范围即使对范数 \(t=p\) 的单个分裂因子也要求 \(p\ll K^{3/2}\)。固定 \(K\) 时，该范围不能支持增长的方向面板。其次，现有矩允许支撑集中在权重 \((L/Z)^\beta e^{c\sqrt{\log(eL/Z)}}\) 的边上。将上一轮的有限域颜色权阵改成约 \(\sqrt Z\,U\) 种颜色、同色边权约 \(U\)，则单标签平均权为 \(\asymp Z^{-1/2}\)，不同标签对平均权乘积为 \(O(Z^{-1})\)，支撑每目标只有 \(O(L^2/(\sqrt Z U))\) 条边。二次不等式 \(2^h-1\ge\beta h+\beta^2h^2/2\) 验证其一致上矩。这是抽象的矩限制。要在端点得到 #104 的完整强度，一个足够的新输入是直接给出逐标签 \(\gg J/\sqrt L\) 的平方自由核心首矩，或在该尺度上证明相应的低权首矩。

### 精确重放

沿用上一轮的同目标标签，新增核对平方商的权重比恰为 \(3\)，以及换元后的八个根。

```python
from math import isqrt

X,n,q = 10**10,10019833945,216
labels = ((5,5),(5,7),(3,5))
assert X<n<=X+10**8 and n%q==25
for c,d in labels:
    a,b = 3**c,5**d
    assert a**8>=X>=a**4 and b**3>=X>=b**2
u,v,w = (n-3**c-5**d for c,d in labels)
m = 3449**2+136**2
prime = lambda p: p>=2 and all(p%j for j in range(2,isqrt(p)+1))
ps = (u,13,29,916469)
assert all(prime(p) and p%4==1 and p>=10 for p in ps)
assert u==38036**2+92591**2 and m==13*916469 and v==29**2*m
assert w%7==0 and w%49!=0
roots = [p for p in range(q) if p*p*m%q==v%q]
assert roots==[25,29,79,83,133,137,187,191]
print([2,3*2*2,0,2*2], roots)
```

实跑得到 \(f_{10}(u),f_{10}(v),f_{10}(w),f_{10}(m)=(2,12,0,4)\)。第二条是真范数，且必须从平方自由图中删除。
