# More edge-disjoint matchings at the weighted cube-root threshold

**#107 的 \((\log X)^{1/4}\) 轮可以提高。** 令 \(L=\log X\)，保留原来的实际 \(3,5\) 指数窗、每个指定目标同余类、\(J=H/Q\ge C X^{1/3}\) 和 \(H\le X\)。在该类的正比例目标上，任删至多 \(\rho L\) 个指数顶点后，仍有以下保证。每轮匹配含 \(\gg L\) 条边，各轮边不交。 [#107 的阈值](https://github.com/Samsen879/a303656/pull/107/files) · [#105 的矩估计](https://github.com/Samsen879/a303656/pull/105/files)

| 使用的上矩 | 剩余不同真边 | 匹配轮数 |
|---|---:|---:|
| 原文列出的 \(9/8\) 阶及二阶矩 | \(\gg L^{2-\alpha}\) | \(\gg L^{1-\alpha}\) |
| 同一 Henriot 上筛，对 \(1\le s\le2\) 一致 | \(\gg L^{2-\log 2}e^{-C_1\sqrt{\log L}}\) | \(\gg L^{1-\log 2}e^{-C_1\sqrt{\log L}}\) |

这里 \(\alpha=8(2^{1/8}-1)\)，故 \(1-\alpha=0.275938\ldots\)，\(1-\log 2=0.306853\ldots\)。第一行的幂次是所列不等式能推出的最优幂次。第二行的幂次和 \(\sqrt{\log L}\) 损失的尺度也在下述抽象模型中达到。对任何 \(1\le m\le cL\)，还可把保证写成 \(\gg L^2/(Um)\) 轮、每轮恰 \(m\) 条边，其中 \(U\) 是下文的权重截点。

### 删点与轮数

记一条标签的权为 \(w_e(n)=r_2(u_e(n))/4\)，总权为 \(W(n)\)，顶点能量为 \(\mathcal E(n)=\sum_v(\sum_{e\ni v}w_e(n))^2\)。原矩估计给出
\[
\sum_n W(n)\gg JL^2,\quad
\sum_n W(n)^2\ll JL^4,\quad
\sum_n\mathcal E(n)\ll JL^3,\quad
\sum_{n,e}w_e(n)^{1+h}\ll JL^{2+a(h)},\qquad a(h)=2^h-1.
\]
舍去 \(w_e>U\) 损失至多 \(O(JL^{2+a(h)}/U^h)\)。取 \(U=(A L^{a(h)})^{1/h}\)，固定充分大的 \(A\)，即可保留定比例首矩。Cauchy–Schwarz 和 Markov 于是给出 \(\gg J\) 个目标，其保留权至少 \(c_0L^2\)，且 \(\mathcal E\le C_0L^3\)。

在每个这样的目标上，删去任意 \(\rho L\) 个顶点损失至多 \(\sqrt{\rho L\mathcal E}\)。取 \(\rho\) 充分小，再删掉任意至多 \(c_0L^2/(4U)\) 条边，仍有 \(\gg L^2\) 权重。极大匹配的两端覆盖余边，所以其大小 \(M\) 满足 \(W_{\rm rem}^2\le 2M\mathcal E\)，从而 \(M\gg L\)。每轮取其中 \(m\) 条，给出上表的轮数和边数。删点集合可以在看到目标和图之后选定。

取 \(h=1/8\) 得第一行。第二行所需的一致性来自 \(w\) 对应的乘法函数 \(R=r_2/4\)。对所有 \(1\le s\le2\)，\(R^s\) 共用 Henriot 类中的参数，因为 \(R(p^\nu)^s\le(\nu+1)^2\) 且 \(R(u)^s\le\tau(u)^2\)。多项式、区间和高度参数固定。单线性因子的 Euler 因子在分裂素数上的一阶项为 \((2^s-1)/p\)，惰性素数上为 \(-1/p\)，二阶余项对 \(s\) 一致。故单标签上界 \(O(JL^{2^{s-1}-1})\) 一致成立。取 \(h=(\log L)^{-1/2}\)，得到
\[
\log U=(\log 2)\log L+O(\sqrt{\log L}).
\]
[Henriot 勘误中的 New Theorem 5](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/B0BD208D979495FE06B8192209E710EA/S0305004114000280a.pdf/nair-tenenbaum-uniform-with-respect-to-the-discriminant-erratum.pdf)

### 逐标签对也成立的尖锐性权阵

取素数 \(p\)，令每轴有 \(L=pd\) 个顶点，分成 \(d\) 个 \(\mathbb F_p\) 块。每个抽象目标在每侧每块独立选一个仿射置换 \(x\mapsto ax+b\)。两顶点的输出颜色相等时给边权 \(p\)，否则为零。遍历全部置换选择。

- 每个目标的支撑恰为 \(p\) 个不交的 \(K_{d,d}\)。每点加权度为 \(L\)，总权为 \(L^2\)，顶点能量为 \(2L^3\)。每个标签的平均首矩为 \(1\)，平均 \(1+h\) 阶矩为 \(p^h\)。
- 任意两个不同标签的平均权乘积至多 \(p/(p-1)\)。若某侧分属不同块，两色独立，联合命中概率为 \(1/p^2\)。若两侧各自在同一块，置换保持相等或不等，联合概率为 \(0\) 或 \(1/[p(p-1)]\)。这也检查了共享顶点的标签对。
- 总边数为 \(Ld=L^2/p\)，所以大小 \(\gg L\) 的轮数至多 \(O(L/p)\)。循环移位恰给出 \(d\) 个满匹配。任删 \(\rho L\) 个顶点，每个匹配仍保留至少 \((1-\rho)L\) 条边。

选 \(p\asymp L^\alpha\) 即达到第一行的边数和轮数。对一致矩界，令 \(\beta=\log 2\)，选 \(p\asymp L^\beta\exp(c\sqrt{\log L})\)，其中 \(c>0\) 固定。由 \(2^h-1\ge \beta h+\beta^2h^2/2\)，
\[
h\log p-(2^h-1)\log L\le \frac{c^2}{2\beta^2}+O(1)
\]
对 \(0\le h\le1\) 一致成立。两种标度都可先对名义长度选相邻尺度的素数，再取 \(d\) 使 \(pd\) 渐近于该长度。整个权阵周期只有 \([p(p-1)]^{2d}=\exp(o(L))\) 个目标，可重复填满立方根尺度的 \(J\)。

这确定了缺少的分析输入。若想去掉第二行的指数损失，一个足够条件是在 \(w\le A L^{\log 2}\) 的真标签上证明总权 \(\gg JL^2\)。现有上矩允许权集中在更高的尺度。#104 的 \(\sqrt L\) 轮来自直接的平方自由真边首矩及无权能量，证明使用 \(J\ge X^{1/2+\varepsilon}\)。它没有提供立方根窗内的对应首矩。上述权阵只说明矩不等式的极限，未声称能由实际 \(3,5\) 标签实现。 [#104 的无权首矩及能量](https://github.com/Samsen879/a303656/pull/104/files)

### 整数重放

下面穷尽 \(p=3,d=2\) 的 1,296 个抽象目标，核对单标签、共享或不共享顶点的标签对，以及任删两点的匹配控制。

```python
from collections import Counter
from itertools import combinations, product

p, d = 3, 2
L = p*d
forms = list(product(range(1,p), range(p)))
single, pair, J = Counter(), Counter(), 0
def colors(F):
    return [(a*x+b)%p for a,b in F for x in range(p)]

for F in product(forms, repeat=2*d):
    u, v = colors(F[:d]), colors(F[d:])
    E = [(i,j) for i,j in product(range(L), repeat=2) if u[i]==v[j]]
    assert len(E)==L*d
    assert set(Counter(i for i,j in E).values())=={d}
    assert set(Counter(j for i,j in E).values())=={d}
    single.update(E)
    pair.update(combinations(E,2))
    J += 1

assert len(single)==L*L and set(single.values())=={J//p}
assert set(pair.values())=={J//p**2, J//(p*(p-1))}
assert len(pair)<L*L*(L*L-1)//2
M = [{(i, ((i//p+k)%d)*p+i%p) for i in range(L)} for k in range(d)]
assert len(set.union(*M))==d*L
for deleted in combinations(range(2*L),2):
    assert all(sum(i not in deleted and L+j not in deleted for i,j in m)
               >=L-2 for m in M)
assert sum(i>=2 for i,j in set.union(*M))==d*(L-2)
print(J, L, L*d, 2*L**3, d, L-2)
```

实跑输出 `1296 6 12 432 2 4`。
