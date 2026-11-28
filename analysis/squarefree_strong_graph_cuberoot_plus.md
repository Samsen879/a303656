# A squarefree strong graph above the cube-root scale

在 #104 的原 \(3,5\) 指数窗内，平方自由真标签图的阈值可从 \(J\ge X^{1/2+\varepsilon}\) 降到 **\(J\ge X^{1/3+\varepsilon}\)**。我从公开原始定理重建了 P4 所述路线。两个关键点是分裂素数必须固定一个禁用的高斯方向，以及大平方尾项必须在去重后交换计数变量。 [#104 原稿](https://github.com/Samsen879/a303656/pull/104/files)

**精确结论。** 固定 \(0<\varepsilon<2/3\)，令 \(X\) 充分大，\(X\le T\le2X\)，\(Q=27\cdot2^k,\ k\ge3\)，\(H\le X\)，且 \(J=H/Q\ge X^{1/3+\varepsilon}\)。在每个指定类 \(b\bmod Q\) 的 \((T,T+H]\) 内，有 \(\gg_\varepsilon J\) 个目标 \(n\)，其标签来自
\[
X^{1/8}\le3^c\le X^{1/4},\qquad X^{1/3}\le5^d\le X^{1/2}.
\]
按 #104 的相位取 \(D_0\in\{1,2,18\}\)。任删至多 \(\rho_\varepsilon\log X\) 个指数顶点后，每个这样的 \(n\) 仍有 \(\gg_\varepsilon(\log X)^{3/2}\) 条不同真边，核心 \((n-3^c-5^d)/D_0\) 为平方自由的分裂素数乘积，并有 \(\gg_\varepsilon\sqrt{\log X}\) 个两两边不交、大小各为 \(\gg_\varepsilon\log X\) 的匹配。结论覆盖每个目标**同余类**中的正比例目标。

### 逐标签下界

固定相位内的一条实际标签 \(\lambda=3^c+5^d\)。核心 \(u=(n-\lambda)/D_0\) 位于端点 \(\asymp X\)、长度 \(H/D_0=qJ\) 的半开区间，并满足 \(u\equiv a\bmod q,\ q=Q/D_0\)，其中 \(a\equiv1\bmod4,\ (a,3)=1\)。数高斯整数 \(Z\) 使 \(N(Z)=u\)。取
\[
R=X^{\varepsilon/8},\qquad z=X^{\varepsilon/32}.
\]
对 \(3<p<z\)，惰性 \(p\) 的禁项是 \(p\mid Z\)。此时 \(p\mid N(Z)\) 当且仅当 \(p\mid Z\)，因为 \(-1\) 在模 \(p\) 下非平方。对分裂 \(p=\pi\bar\pi\)，固定一个方向，禁项是 \(\pi\mid Z\) 或 \(\bar\pi^{\,2}\mid Z\)。用触发禁项的**有理素数乘积**作有限支撑筛标签。其局部密度为
\[
g(p)=
\begin{cases}
p^{-2},&p\equiv3\pmod4,\\
p^{-1}+p^{-2}-p^{-3},&p\equiv1\pmod4.
\end{cases}
\]

对平方自由筛除数 \(d\le R\)，展开每个分裂素数的并集。每项归约为 \(\delta\mid Z\)，其中 \(t=N(\delta)\le d^3\)，\(t\equiv1\bmod4\) 且 \((t,q)=1\)。代 \(Z=\delta W\)，Tolev 的输入是原两个端点各除以 \(t\)，**模数仍为 \(q\)**，新剩余类为 \(a t^{-1}\bmod q\)。两端一致有
\[
x_t\asymp X/t,\qquad
q\le X^{2/3-\varepsilon},\qquad
q/x_t^{2/3}\ll X^{-3\varepsilon/4}.
\]
所以 (10) 中的 gcd 因子为 \(1\)，两端总误差为 \(O(X^{1/3}(\log X)^8)\)，这里利用了 \(q=2^j3^i,\ j\ge2,\ 1\le i\le3\)。新剩余类仍为模 4 的 \(1\) 和模 3 的单位，故圆点数恒为 \(8q/3\)。该项的主项恰为 \((8\pi/3)J/t\)。合并后得到
\[
A_d=(8\pi/3)Jg(d)
 +O\!\left(3^{\omega(d)}X^{1/3}(\log X)^8\right).
\]
在平方自由 \(d\) 上 \(3^{\omega(d)}=\tau_3(d)\)，故绝对余项总和为 \(O(X^{1/3+\varepsilon/8}(\log X)^{10})=o(J/\sqrt{\log X})\)。 [Tolev，式 (2)、(3)、(10)](https://arxiv.org/pdf/1106.3474v2)

模 4 的 Mertens 公式给出筛维数 \(1/2\) 和 \(V(z)\asymp(\log z)^{-1/2}\)。有限支撑下筛可取 \(D=z^{1+\delta_0}\le R=z^4\)，其中 \(\delta_0>0\) 固定且充分小，直接使用 \(f_{1/2}(1+\delta_0)>0\)。定理误差和上述余项均可吸收，得到 \(\gg_\varepsilon J/\sqrt{\log X}\) 个高斯点。 [Kurlberg–Lester–Rosenzweig，定理 2.1 及式 (2.23) 后](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136)

**先去权，再删尾。** 对一个固定幸存范数，每枚小分裂素数只允许一种方向，且指数至多为 \(1\)。高斯分解给出的幸存坐标数至多
\[
4\prod_{\substack{p\ge z\\p\ {\rm split}}}(v_p(u)+1)
\le 4\cdot2^{\log(3X)/\log z}=O_\varepsilon(1).
\]
因而已经得到同阶的不同核心数。对 \(z\le p\le X^{1/3}\) 的平方因子，逐 \(p\) 用 \(J/p^2+O(1)\)。对 \(p>X^{1/3}\)，写 \(u=p^2m\)，先固定 \(m\ll X^{1/3}\)。这时 \(m\) 为模 \(q\) 的单位，\(p^2\equiv a/m\bmod q\) 至多八个根，且 \(p\) 的实区间长度为 \(O(qJ/\sqrt{Xm})\)。逐 \(m\) 求和得到 \(O(JX^{-1/3}+X^{1/3})\)。合计平方尾项
\[
O(J/z+X^{1/3})=o(J/\sqrt{\log X}).
\]
这里只减不同核心。把这一尾界直接从带坐标权的计数里扣除，或把逐 \(p\) 的 \(O(1)\) 一直加到 \(\sqrt X\)，都不能给出所需下界。

### 固定顶点的无权能量

令 \(L=\log X\)。单标签与双标签的上界只需筛惰性素数，仍可用 #104 的截点 \(J^{1/10}\) 和层级 \(J^{1/2}\)。对差 \(h=\lambda-\mu\ne0\)，两标签只在 \(p\mid h\) 时重合禁类。双标签误差为 \(O(\sqrt J\log J)\)，主项上界为 \(O((J/L)\prod_{p\mid h}(1+C/p))\)。

该差权在全盒以及每个固定顶点上平均有界。具体地，展开 \(p\le L^2\)、\(p\nmid30\) 的平方自由乘积。固定一条标签，再固定另一条的一轴，剩下的一轴在模 \(d\) 最多命中一个阶周期类，比例至多 \(1/\operatorname{ord}_d(B)+O(1/L)\)，其中 \(B\in\{9,25,5^{18}\}\)。固定顶点时选择另一轴。阶至多 \(U\) 的 \(d\) 都整除 \(\prod_{j\le U}(B^j-1)\)，其差权系数和为 \(O((\log(2U))^{O(1)})\)，故按阶作二进分组后收敛。边界误差由 Mertens 公式求和，\(p>L^2\) 的部分由 \(\log|h|=O(L)\) 控制。

于是边数 \(F(n)\) 的首矩为 \(\gg_\varepsilon JL^{3/2}\)，二阶矩为 \(O(JL^3)\)，而 \(\sum_n\sum_v d_v(n)^2=O(JL^2)\)。Cauchy–Schwarz 与 Markov 保留 \(\gg_\varepsilon J\) 个目标。每个目标删 \(\rho_\varepsilon L\) 个顶点至多损失 \(\sqrt{\rho_\varepsilon L\sum_v d_v^2}\) 条边。余图只要还保留 \(\gg_\varepsilon L^{3/2}\) 条边，极大匹配的端点覆盖所有边，故由同一能量界得到 \(\gg_\varepsilon L\) 条匹配边。每轮取固定小常数倍 \(L\) 条，边数预算给出 \(\gg_\varepsilon\sqrt L\) 轮。 [#104 的配对上筛与图提取](https://github.com/Samsen879/a303656/pull/104/files)

### 同目标整数复验

下例在真实指数窗内给出一条平方自由真边、一条通过小面板却须由大平方尾项删除的真范数，以及一个奇惰性赋值反控。有限面板取 \(p<10,\ p>3\)，供复验局部机制。

```python
from collections import Counter
from itertools import product
from math import isqrt

X, n, q = 10**10, 10019833945, 216
labels = [(5,5), (5,7), (3,5)]
assert X < n <= X + 10**8 and n % q == 25
for c,d in labels:
    a,b = 3**c,5**d
    assert a**8 >= X >= a**4 and b**3 >= X >= b**2
u,v,w = [n-3**c-5**d for c,d in labels]  # D0 = 1
assert all(a%4 == 1 and a%3 != 0 for a in (u,v,w))
assert u == 38036**2 + 92591**2
assert all(u % k for k in range(2,isqrt(u)+1))
assert v == 29**2*(3449**2+136**2) and v%5 and v%7 and v%29**3
assert w%7 == 0 and w%49 != 0

def divides(x,y,a,b):
    t = a*a+b*b
    return (x*a+y*b)%t == (y*a-x*b)%t == 0

P = list(product(range(25),repeat=2))
A = {xy for xy in P if divides(*xy,2,1)}
B = {xy for xy in P if divides(*xy,3,-4)}
assert (len(A),len(B),len(A&B)) == (125,25,5)
assert [(x,y) for x,y in product(range(7),repeat=2)
        if (x*x+y*y)%7 == 0] == [(0,0)]

eta = Counter((x*x+y*y)%q for x,y in product(range(q),repeat=2))
for a in (u,v,w):
    for t in (1,5,25,125,49,125*49):
        assert eta[a*pow(t,-1,q)%q] == 8*q//3
print(u,v,w,"verified")
```

实跑输出 `10019830577 10019755577 10019830793 verified`。本次证明使用固定正 \(\varepsilon\)，因此平方自由结论尚未推进到 #107 的无幂损失端点。
