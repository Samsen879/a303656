# A303656 — Thread 3：有限递推与 representation lifting

**日期：2026-09-21。性质：本轮推导及精确重放材料，尚未经独立审稿；不是冻结权威的更新。**

## 0. 结论与 authority binding

仓库：`Samsen879/a303656`。

```text
main SHA: 8f17e88e517720f61f3c21d58d91c04cd6fa11b5
main tree: 811a274b1f671412305c8565fcd79e9d41c0189b
读取：STATUS.md, README.md, docs/THEOREM_INDEX.md,
      docs/ROUTE_MAP.md, docs/AUTHORITY_TREE.md, docs/ARTIFACT_LINEAGE.md
仓库操作：只读；本材料未提交到 main，未替换任何冻结文件。
原题：UNRESOLVED；本轮没有 universal proof，也没有反例。
```

公开索引已经收录 N-005、N-006、N-007：Gaussian 单分支稀疏性、仿射 S-unit 轴纤维分类、有限精确仿射 shift-language 系统的 entropy no-go。本报告不把这些结论重新命名为新发现；对于以下扩展，另给完整推导，而不是把索引当作其证明。

本轮主要产出：

1. **定理 M / M+：计数级有限线性系统的 no-go。** 不同整数伸缩 `1, F(x^{K_1}), ..., F(x^{K_s})` 在 `C(x)` 上线性无关。借助一个带完整证明的 Ore 消元引理，这还排除任何包含 F 的有限系统 `Y(x)=b(x)+sum A_K(x)Y(x^K)`，其中系数有理、K 属于有限整数集合且 K>=2。不是只排除单一底数。
2. **定理 Q*：有限有理 lifting 的全部可达集只有零密度。** 允许有限多个正定二元有理二次型、分数权重、指数任意重选和任意 guards；固定有限 K>=2、R，并对有理 charts 的次数统一设界。这样的系统从有限基例生成的原始整数只有 `O(sqrt(X) log^6(X) + log^(r+2)(X))` 个，r 为倍率中不同素因子数。另保留一个不要求源状态可达的一步入边定理 Q。
3. 三条**覆盖全部原始 residue classes 的正系数下降等式**：偶数、1 mod 4、3 mod 4 分别进入三个明确辅助状态。下降正确，但不能延伸成有限有理线性闭合系统。另有一个完全精确的正系数无限网格，其状态在 `C(x)` 上线性无关；同时给出一个四基本函数的非线性闭合系统，并展示其必须相减、卷积 fanout 无界的失败点。
4. 一个明确的 **Boolean window decoder restart gate**。它尚未证明；这只是剩余缺口的准确形式，不是已取得的正向定理。

“本轮推导”不等于“文献首次发现”，也不等于“已被独立审阅接受”。

## 1. 约定：计数与支持必须分开

令

\[
\theta(x)=\sum_{a\in\mathbb Z}x^{a^2},\qquad T(x)=\theta(x)^2,
\]
\[
L_b(x)=\sum_{j\ge0}x^{b^j},\qquad
F(x)=T(x)L_3(x)L_5(x)=\sum_{n\ge0}f(n)x^n.
\]

这里平方变量是有符号计数，指数从 0 开始；因此 `L_b` 的首项是 `x`，不是常数 1。将平方变量取绝对值可知：

\[
f(n)>0\quad\Longleftrightarrow\quad
n=a^2+b^2+3^c+5^d,\quad a,b,c,d\ge0.
\]

有 `f(0)=f(1)=0, f(2)=1`。同一个数值 shift 若由不同指数对产生，在计数时必须保留其重数。

全文 `G\succeq0` 表示逐项系数非负，而不是只指 `G(x)>=0` 在实区间成立。

## 2. A — 精确 identity catalogue

### 2.1 完整仿射系数约束

设 `z=(a,b)^t`，考虑

\[
\|Mz+t\|^2+3^{c+\delta}+5^{d+\varepsilon}
=K(\|z\|^2+3^c+5^d)+R.
\tag{A1}
\]

若此式在一个含独立无界参数的 residue cylinder 上成立，比较 `a,b` 的二次、一次项得

\[
M^tM=K I_2,\qquad M^tt=0.
\]

因 `K>0`，矩阵可逆，所以 `t=0`。剩余约束是

\[
(3^\delta-K)3^c+(5^\varepsilon-K)5^d=R.
\tag{A2}
\]

若 `c,d` 在该 cylinder 中分别独立无界，分别变化一个指数，得

\[
3^\delta=K=5^\varepsilon,
\]

从而 `K=1, delta=epsilon=0, R=0`。对仍有两个独立无界指数方向的有限同余或奇偶状态，此结论不变：相应尾部包含等差子网格。若一个指数固定，则会落到下面的轴纤维规则，而不是得到一个双自由指数规则。任意非同余的指数耦合条件不由本段单独排除。

有理矩阵也满足同样的系数约束。若平方输出是关于 `a,b` 的更高次数实多项式，最高次齐次部分的两个平方之和不能相互抵消，因此其次数仍只能至多为 1。

整数矩阵满足 `M^tM=KI_2` 当且仅当

\[
M=\begin{pmatrix}u&-\sigma v\\v&\sigma u\end{pmatrix},
\quad u^2+v^2=K,\quad \sigma\in\{\pm1\}.
\tag{A3}
\]

每个正 `K` 的矩阵数为 `2 r_2(K)`。精确枚举 `1<=K<=100` 已与此公式逐一比较。

| K | 矩阵数 | 代表 |
|---:|---:|---|
| 3 | 0 | 无整数 Gaussian similitude |
| 5 | 16 | `(a-2b,2a+b)` |
| 9 | 8 | `(3a,3b)`，加符号与交换 |
| 15 | 0 | 无整数 Gaussian similitude |
| 25 | 24 | `(5a,5b)` 或 `(3a-4b,4a+3b)` |

### 2.2 确实成立的单轴 lifting

若 `n=a^2+b^2+3^c+5^d`，则

\[
\boxed{5n-4\,3^c=(a-2b)^2+(2a+b)^2+3^c+5^{d+1}.}
\tag{A4}
\]
\[
\boxed{9n-8\,5^d=(3a)^2+(3b)^2+3^{c+2}+5^d.}
\tag{A5}
\]
\[
\boxed{25n-24\,3^c=(3a-4b)^2+(4a+3b)^2+3^c+5^{d+2}.}
\tag{A6}
\]

(A6) 中平方输出也可换成 `(5a,5b)`。所有输出平方变量均可取绝对值，指数始终非负。

关键限制是：这些式子的 additive carry 含 `3^c` 或 `5^d`。除非把相应指数固定为一个状态参数，否则它并不是有限集合中的常数 `R`。

更一般地，固定输入、输出 `c=c_0,c_1` 后，存在

\[
K=5^s,\quad R=3^{c_1}-5^s3^{c_0},\quad d'=d+s,
\]

并用 Gaussian 乘数 `(1+2i)^s` lift 平方部分。固定 `d=d_0,d_1` 后，存在

\[
K=3^{2t},\quad R=5^{d_1}-3^{2t}5^{d_0},\quad c'=c+2t,
\]

并把两个平方变量乘以 `3^t`。

### 2.3 真正的有理非线性恒等式：只能旋转 norm

对任意有理函数 `s=s(a,b)`，在分母有定义处，

\[
\left(\frac{(1-s^2)a-2sb}{1+s^2}\right)^2+
\left(\frac{2sa+(1-s^2)b}{1+s^2}\right)^2=a^2+b^2.
\tag{A7}
\]

这可与 (A3) 复合，产生非线性的有理 norm similitude。它没有产生 additive norm defect。还必须另外检查输出是否为整数；有理恒等式本身不提供整数性。

## 3. B — 精确正系数架构：无限网格与全 residue 收缩

### 3.1 非负余项

Gaussian 整数映射 `a+ib -> (1+2i)(a+ib)` 是单射，故

\[
D_5(x):=T(x)-T(x^5)\succeq0.
\]

整数格映射 `(a,b)->(3a,3b)` 是单射，故

\[
D_9(x):=T(x)-T(x^9)\succeq0.
\]

不能照抄为 `T(x)-T(x^3)\succeq0`：其 `x^3` 系数正好是 `-4`。

### 3.2 状态定义与两条递推

定义

\[
H_{u,v}(x)=T(x)L_3(x^{5^u})L_5(x^{9^v}),\quad u,v\ge0.
\tag{B1}
\]

原始状态为 `H_{0,0}=F`。精确恒等式为

\[
\boxed{H_{u+1,v}(x)=H_{u,v}(x^5)+E^{(5)}_{u,v}(x),}
\tag{B2}
\]

其中

\[
E^{(5)}_{u,v}=
 x^{9^v}T(x)L_3(x^{5^{u+1}})
 +D_5(x)L_3(x^{5^{u+1}})L_5(x^{5\cdot9^v})\succeq0.
\tag{B3}
\]

另一条为

\[
\boxed{H_{u,v+1}(x)=H_{u,v}(x^9)+E^{(9)}_{u,v}(x),}
\tag{B4}
\]

其中

\[
E^{(9)}_{u,v}=
 T(x)(x^{5^u}+x^{3\cdot5^u})L_5(x^{9^{v+1}})
 +D_9(x)L_3(x^{9\cdot5^u})L_5(x^{9^{v+1}})\succeq0.
\tag{B5}
\]

证明只需准确使用

\[
L_5(x^B)=x^B+L_5(x^{5B}),\quad
L_3(x^A)=x^A+x^{3A}+L_3(x^{9A}),
\]

再加减相应的 `T(x^5)` 或 `T(x^9)`。因此不是经验覆盖，也不依赖某个有限截断。

### 3.3 转移图

箭头表示 source coefficient at `m` 向 target coefficient at `K m` 的正向转移。

```text
H00=F ----5----> H10 ----5----> H20 ----5----> ...
  |               |               |
  9               9               9
  v               v               v
 H01 ----5---->  H11 ----5---->  H21 ----5----> ...
  |               |               |
  9               9               9
  v               v               v
 H02 ----5---->  H12 ----5---->  H22 ----5----> ...
  :               :               :
```

令 `h_{u,v}(n)=[x^n]H_{u,v}`。它确实给出

\[
h_{u+1,v}(5m)=0\Longrightarrow h_{u,v}(m)=0,
\tag{B6}
\]
\[
h_{u,v+1}(9m)=0\Longrightarrow h_{u,v}(m)=0.
\tag{B7}
\]

在这些反向边上，整数 index 严格下降，`u+v` 也严格下降。但原始零点 `h_{0,0}(n)=0` 没有这样的入边可供反向使用。若通过扩大状态来引入负 `u,v`，则出现分数权重或无界 denominator；它不再是这里的整数非负状态系统，更不自动拥有有限基例。

因此失败原因不是符号不正，也不是下降高度未检查，而是 **状态方向错误及状态无法闭合**。

### 3.4 状态不等价；同时存在非线性关系

下面定理 M 的证明还给出：

\[
\{H_{u,v}:u,v\ge0\}\quad\text{在 }\mathbb C(x)\text{ 上线性无关。}
\tag{B8}
\]

所以不能通过有限个有理系数线性组合，把该网格精确折叠成有限线性状态空间。

但它们**不是代数无关**。恰好有

\[
\boxed{H_{u,v}H_{u',v'}=H_{u,v'}H_{u',v}.}
\tag{B9}
\]

特别地 `H00 H11 = H10 H01`。这来自乘积的 rank-one 分离。它不能直接用于最小零系数下降：乘积系数是卷积，`f(n)=0` 并不使 `[x^{n+k}](F H)` 为零，其他较小 index 的正系数会继续贡献。若移项剥离这些贡献，则失去 positivity-preserving 性质。本报告没有排除更巧妙的非线性使用方式。

### 3.5 更好的原始入口：三个辅助状态覆盖全部 residue guards

定义

\[
U(x)=\sum_{u\in\mathbb Z}x^{u(u+1)}
=2\sum_{u\ge0}x^{u(u+1)}.
\]

注意 `U(0)=2`，因为 `u=0,-1` 都贡献常数项。令

\[
G_e(x)=T(x)\sum_{c,d\ge0}x^{(3^c+5^d)/2},
\tag{B10}
\]
\[
G_1(x)=\theta(x)U(x)\sum_{j,d\ge0}x^{(3\cdot9^j+5^d)/4},
\tag{B11}
\]
\[
G_3(x)=\theta(x)U(x)\sum_{j,d\ge0}x^{(9^j+5^d-2)/4}.
\tag{B12}
\]

所列指数全部是非负整数。各状态系数记作 `g_e,g_1,g_3`。有完全精确的正系数等式

\[
\boxed{f(2m)=g_e(m),\quad f(4m+1)=2g_1(m),\quad
f(4m+3)=2g_3(m).}
\tag{B13}
\]

等价地，

\[
F(x)=G_e(x^2)+2xG_1(x^4)+2x^3G_3(x^4).
\tag{B14}
\]

**证明。** 幂项和始终为偶数。偶数 norm 的表示具有同奇偶平方变量，变换

\[
(a,b)\mapsto((a+b)/2,(a-b)/2)
\]

是 `a^2+b^2=2t` 与 `u^2+v^2=t` 的整数表示双射，故 `r_2(2t)=r_2(t)`，得到偶数分支。

奇数 norm 必为 `1 mod 4`；两个坐标中恰有一个奇数。写成奇数坐标 `2u+1`、偶数坐标 `2v`，则

\[
(2u+1)^2+(2v)^2=1+4\{u(u+1)+v^2\}.
\]

两个坐标位置产生因子 2。`n=1 mod4` 迫使 c 为奇数，写 `c=2j+1`；`n=3 mod4` 迫使 c 为偶数，写 `c=2j`。代入即得另外两式。

**零点下降图：**

```text
                         F(n)=0
                       /    |     \
              n even / n=1 mod4   \ n=3 mod4
                    v        v       v
              Ge(n/2)=0  G1((n-1)/4)=0  G3((n-3)/4)=0
                    |        |       |
               辅助状态闭合尚缺失；不可把 state label 删除
```

这次 guards 确实穷尽所有整数；对于 n>=2，所达 index 严格变小。它是本轮最好的**原始入口**，不只是一次 residue covering。但原始最小反例假设只知道较小 index 的 `F` 非零，不知道 `G_e,G_1,G_3` 非零。因此仍没有得到矛盾。

下面的 M+ 排除把这些系数等式扩展成任何有限有理线性、有限整数倍率 K>=2 的闭合系统。定理 Q* 进一步涵盖用有界次数有理 witness maps 闭合这些二次型状态的尝试；并不是因为出现分数权重就自动逃出 no-go。

具体地，`G_e` 的权重为 A=B=1/2；对另外两个状态，把 `u(u+1)` 改写为 `(u+1/2)^2-1/4`：

```text
G1: q=(u+1/2)^2+v^2, A=3/4, B=1/4, C=-1/4, c even;
G3: q=(u+1/2)^2+v^2, A=1/4, B=1/4, C=-3/4, c even.
```

这些都是 Q* 的有限有理二次型状态。原始非负平方变量条件通过取绝对值恢复；系数公式使用有符号计数。

### 3.6 一个真正有限的非线性函数闭合系统，以及其精确失败点

令

\[
\Phi(x)=\theta(x),\qquad
\Psi(x)=\sum_{j\ge0}x^{j(j+1)/2}.
\]

只有四个基本系列就能给出闭合的函数系统：

\[
\boxed{\Phi(x)=\Phi(x^4)+2x\Psi(x^8),}
\tag{B15}
\]
\[
\boxed{\Psi(x)^2=\Phi(x)\Psi(x^2),}
\tag{B16}
\]
\[
L_3(x)=x+L_3(x^3),\qquad L_5(x)=x+L_5(x^5),
\qquad F(x)=\Phi(x)^2L_3(x)L_5(x).
\tag{B17}
\]

(B15) 是把平方变量分成偶数和奇数。(B16) 是经典 theta/triangular identity；这里可直接由双平方表示推导，不需要假设某个模形式定理：

\[
[x^n]\Psi(x)^2=\frac14r_2(8n+2),\qquad
[x^n]\Phi(x)\Psi(x^2)=\frac14r_2(4n+1).
\]

第一式用 `8*T_j+1=(2j+1)^2`，所有坐标必须为奇数，四种符号给出因子 4。第二式用 `4n+1=(2a)^2+(2j+1)^2`，奇数坐标的符号和两坐标的位置给出因子 4。再用已证明的 `r_2(2m)=r_2(m)` 即得 B16。

```text
Phi(x) ------> Phi(x^4), Psi(x^8)
Psi(x)^2 ----> Phi(x), Psi(x^2)
L3(x) -------> x, L3(x^3)
L5(x) -------> x, L5(x^5)

output: F = Phi^2 * L3 * L5
```

这个系统确实有限，不能因 M+ 就否认它。M+ 的假设是线性，而这里有平方/乘积。

但是，令 `p_n=[x^n]Phi, q_n=[x^n]Psi`，提取 B16 的第 n 个系数并隔离 q_n，必须写成

\[
\boxed{2q_n=\sum_{j=0}^{\lfloor n/2\rfloor}p_{n-2j}q_j
-\sum_{j=1}^{n-1}q_jq_{n-j}.}
\tag{B18}
\]

p_n 可先由 B15 的严格较小 index 计算，随后 B18 计算 q_n；基例 `p_0=q_0=1` 确实有限。因此这是有效的精确系数算法。然而它有两个不符合目标的性质：**必须相减**；而且系数递推的卷积项数随 n 增长，不是一个固定 fanout 的 finite-state transition。

最小的明确 cancellation 例子就是 n=2：右侧第一项为 1，被减去的卷积项也为 1，故 `2q_2=1-1=0`。两个函数方程都看起来使用正系数，并不能让隔离出的未知系数严格为正。

因此，本轮既没有把“函数闭合”误判为不可能，也没有把这个四函数闭合系统误判为一个 minimal-zero induction proof。它是 exact functional closure，不是需要的 positivity-preserving coefficient closure。

## 4. C — 定理 M：有限 mixed-dilation 线性递推不存在

### 4.1 精确声明

**定理 M。** 对任意有限组不同的正整数 `K_1,...,K_s`，

\[
1,F(x^{K_1}),\ldots,F(x^{K_s})
\]

在 `C(x)` 上线性无关。

即：若 `p_0,p_1,...,p_s` 为复系数多项式，且

\[
p_0(x)+\sum_{j=1}^s p_j(x)F(x^{K_j})=0,
\tag{M1}
\]

则所有 `p_j` 都是零多项式。有理系数的情况清分母即可。

因此，`F` 不满足任何整数底数 `k>=2` 的非平凡线性 Mahler 方程；这包括有限阶与有理非齐次项。不同的底数 `3,5,9,15,25,...` 混合，也不能形成上述有限 scalar equation。

本结论针对精确计数级数。它不推出支持指示序列不是 automatic，也不排除 Boolean transfer、非线性递推或另行构造的正 minorant。

### 4.2 引理：几何幂指数和的对数周期展开

取 `b>1, ell_b=log b, t=e^{-y}`，定义

\[
S_b(t)=\sum_{j\ge0}e^{-b^jt},\qquad
h_b(t)=\sum_{j\ge1}(1-e^{-t/b^j}).
\]

有 `0<=h_b(t)<=t/(b-1)`。定义

\[
P_b(y)=S_b(e^{-y})-h_b(e^{-y}).
\]

由

\[
S_b(bt)=S_b(t)-e^{-t},\qquad
h_b(bt)=h_b(t)+1-e^{-t}
\]

得到 `P_b(y)-P_b(y-ell_b)=1`，故

\[
P_b(y)=y/\ell_b+C_b+\Psi_b(y),
\tag{M2}
\]

其中 `Psi_b` 是周期 `ell_b`、均值零的光滑函数，并且

\[
S_b(e^{-y})=P_b(y)+O(e^{-y}).
\tag{M3}
\]

接下来计算全部非零 Fourier 系数。逐项求导得到绝对局部一致收敛的 periodization：

\[
P_b'(y)=\sum_{j\in\mathbb Z}e^{j\ell_b-y}
                    \exp(-e^{j\ell_b-y}).
\]

置 `omega_m=2 pi m/ell_b`。对一个周期积分并展开 periodization：

\[
\widehat{P_b'}(m)
=\frac1{\ell_b}\int_{\mathbb R}e^{-u}e^{-e^{-u}}e^{-i\omega_mu}\,du
=\frac{\Gamma(1+i\omega_m)}{\ell_b}.
\]

因此对 `m!=0`，

\[
\boxed{\widehat\Psi_b(m)=\frac{\Gamma(2\pi im/\ell_b)}{\ell_b}\ne0.}
\tag{M4}
\]

最后的不为零使用 Gamma 函数没有零点这一标准事实 [S2]。周期函数光滑，所以 Fourier 系数绝对可和。也可由 Gamma 的垂直方向衰减直接得到一致收敛。此展开属于 harmonic sums 的 Mellin/log-periodic 机制 [S3]，但以上给出了所需版本的独立推导。

### 4.3 Theta 前因子

由 theta 的模变换/Poisson summation [S1]，

\[
T(e^{-t})=\frac\pi t\left(1+O(e^{-\pi^2/t})\right),\qquad t\downarrow0.
\tag{M5}
\]

令 `Q(y)=P_3(y)P_5(y)`。因为 `P_b(y)=O(1+y)`，对固定 `K` 有

\[
F(e^{-Kt})=\frac\pi{Kt}
 \left(Q(y-\log K)+O(t(1+y))\right).
\tag{M6}
\]

这保留了微小但非零的周期振荡；若只保留 `log^2(1/t)/t` 的主量级，会丢掉证明所需的信息。

### 4.4 从有理系数关系抽取常系数 translate relation

先设 (M1) 中至少一个 `p_j, j>=1` 非零。令

\[
s=\min_{j\ge1,\ p_j\ne0}\operatorname{ord}_{x=1}p_j.
\]

写

\[
p_j(e^{-t})=a_jt^s+O(t^{s+1}),
\]

其中较高阶者 `a_j=0`，且不全为零。设 `alpha_j=a_j/K_j`。

若 `p_0` 的消失阶小于 `s-1`，其首项压倒其他项，立即矛盾。否则将关系除以 `pi t^{s-1}`，得到某个常数 `c`（可能为零）满足

\[
\sum_j\alpha_j Q(y-\log K_j)+c=o(1),\qquad y\to+\infty.
\tag{M7}
\]

误差可取 `O(e^{-y}(1+y)^2)`。

(M7) 左侧可写成

\[
A y^2+y B(y)+C(y),
\]

其中 `B,C` 都有绝对收敛的 Fourier 级数，其频率属于

\[
2\pi\left(\frac{\mathbb Z}{\log3}+\frac{\mathbb Z}{\log5}\right).
\]

除以 `y^2` 得 `A=0`；再除以 `y` 得 `B(y)->0`。一个绝对收敛的 almost-periodic Fourier 级数若趋于零，则其所有 Fourier 均值都为零，因此该函数恒为零。于是 `B=0`，随后 `C(y)->0`，同理 `C=0`。

这里不需要任何频率之间的统一间距下界。即使 mixed 频率稠密，绝对可和性仍允许在 Cesaro 平均中逐项交换极限。

### 4.5 Mixed Fourier modes 与两次 Vandermonde

对正整数 `m,n`，频率

\[
\omega_{m,n}=2\pi\left(\frac m{\log3}+\frac n{\log5}\right)
\]

不会等于任何纯 3 或纯 5 频率，并且对应的整数对唯一。原因是 `log3/log5` 无理，否则出现 `3^r=5^s`。

因此，在刚才恒为零的 `C(y)` 中，这个频率只可能来自 `Psi_3 Psi_5`。由 (M4) 其非零公共系数可约去，得到

\[
\sum_j\alpha_j A_j^m B_j^n=0\qquad(m,n\ge1),
\tag{M8}
\]

其中

\[
A_j=e^{-2\pi i\log K_j/\log3},\qquad
B_j=e^{-2\pi i\log K_j/\log5}.
\]

所有点 `(A_j,B_j)` 两两不同。如果两对相同，则

\[
K_j/K_l=3^r=5^s
\]

对某些整数 `r,s` 成立，所以 `K_j=K_l`。

把 `j` 按相同的 `A_j` 分组。固定 `n`，让 `m` 遍历从 1 到组数，用 Vandermonde 可逆性得到每组内部

\[
\sum_{j\text{ in group}}\alpha_j B_j^n=0.
\]

同组内的 `B_j` 两两不同，再令 `n` 遍历从 1 到组大小，第二次 Vandermonde 得全部 `alpha_j=0`。这与最小消失阶的选取矛盾，证明完成。

若开始时所有 `p_j,j>=1` 已为零，则显然 `p_0=0`。

### 4.6 对无限状态网格的推论

对

\[
H_{u,v}(e^{-t})
=\frac\pi t\{P_3(y-u\log5)P_5(y-v\log9)+O(t(1+y))\},
\]

完全同样的论证适用。对应的 phase pair 是

\[
\left(e^{-2\pi i u\log5/\log3},
      e^{-2\pi i v\log9/\log5}\right).
\]

它们对不同 `(u,v)` 两两不同，所以得到 (B8)。注意 (B9) 表明线性无关绝不等同于代数无关。

### 4.7 固定底数有限向量系统：无需可逆性假设

假设有限向量 Y 包含 F，并且

\[
Y(x)=A(x)Y(x^k)+b(x),\qquad A,b\text{ 为有理函数},\quad k\ge2.
\]

增加常数坐标 1 使系统齐次，令增广维数为 d。对 j=0,...,d，迭代系统把 `F(x^{k^j})` 都写成 `Y(x^{k^d})` 的有理系数行向量组合。d+1 个行向量在 d 维空间中线性相关，于是得到非平凡 scalar Mahler 关系，与 M 矛盾。这里从未要求 A 可逆。

### 4.8 定理 M+：有限个不同底数也不能救活闭合线性系统

**定理 M+。** 不存在有限维函数向量 Y，以 F 为一个坐标，满足

\[
\boxed{Y(x)=b(x)+\sum_{K\in\mathcal K}A_K(x)Y(x^K),}
\tag{M9}
\]

其中 `mathcal K` 是有限整数集合、每个 K>=2，且所有矩阵条目及 forcing b 均在 `C(x)` 中。若存在有限初始系数例外，它们只增加多项式 forcing，结论不变。系数是否非负对这个 no-go 没有影响。

**为什么有限向量系统可以消元？** 不能直接使用交换矩阵行列式，因为 dilation 与有理系数不交换。以下给出所需专门版本。

取所有倍率 K 中的素因子 `p_1,...,p_r`，并扩大系数域为

\[
E=\bigcup_{N\text{ supported on }\{p_1,\ldots,p_r\}}
\mathbb C(x^{1/N}).
\]

这些分数幂选取在正实轴附近取正值的分支。`sigma_i(f)(x)=f(x^{p_i})` 在 E 上是两两交换的自同构，其逆为 `x->x^{1/p_i}`。令

\[
\mathscr O=E[T_1,\ldots,T_r;\sigma_1,\ldots,\sigma_r],
\quad T_i a=\sigma_i(a)T_i,\quad T_iT_j=T_jT_i.
\]

这是一个无零因子的 skew polynomial ring。每个总 operator-degree <=N 的子空间，作为左 E 空间或右 E 空间，维数都是 `binom(N+r,r)`。

对非零 a,b，寻找 `u a=v b`。右乘 a,b 对左 E 空间是线性的；当 N 足够大，

\[
2\binom{N+r}{r}>\binom{N+d+r}{r},\qquad d=\max(\deg a,\deg b),
\]

所以线性映射 `(u,v)->u a-v b` 有非零核。无零因子保证 u,v 均非零，从而存在非零共同左倍数。用右 E 空间同理得到共同右倍数。因此可以构造左右 Ore 分式除环 D。这里自同构性是必要的；扩大到 E 正是为了不把非满射 endomorphism 当成自同构。[S6] 提供 Ore/skew-fraction 的标准背景；上述增长维数论证专门核实本次使用的条件。

写 (M9) 为 `M Y=b`，其中

\[
M=I-P,\qquad P=\sum_K A_K T^{v(K)}.
\]

P 的每个 monomial 都具有正 operator-degree。M 在 D 上可逆：否则有非零 `w in D^d` 满足 Mw=0。清除共同右分母得到非零 `u in mathscr O^d` 且 Mu=0。但 u 的最低 operator-degree 项不会被 Pu 取消，因为 Pu 的所有项至少高一次。这是矛盾。

取 M 的逆矩阵中对应 F 的行，清共同左分母，得非零算子 q 与算子行 B，使

\[
B M=q e_F^t.
\]

应用到 Y 上，得到

\[
q\cdot F=B\cdot b\in E.
\tag{M10}
\]

q 是有限多个不同整数 dilation 的 E 系数线性组合，而右侧仍在 E 中。

最后注意 M 的证明实际上只用了系数在 x=1 处的有限消失阶和 Taylor 余项。因此，它对**在 x=1 处 meromorphic 的系数**同样成立：先清共同极点即可。E 中每个元素在所选的 x=1 分支都 meromorphic，所以 (M10) 与 M 的同一证明矛盾。M+ 证毕。

**边界。** M+ 排除的是 (M9) 这种有限计数级 equality。它不排除 Boolean/support 系统、带非有理未闭合 forcing 的写法、非线性系统或不符合此 normal form 的其他机制。K=1 的同 index 项若可经有理矩阵求逆移到左边，则可化到 (M9)；奇异、无信息的隐式系统不被直接宣称已排除。

## 5. D — 定理 Q：有理 repair、任意 guards 与零密度入边

### 5.1 核心引理：非零常数 norm defect 不能被通用有理公式修复

**引理 Q1。** 设 `K>0, eta` 为有理数。若 `A,B` 属于 `Q(a,b)`，且作为有理函数恒等式

\[
A(a,b)^2+B(a,b)^2=K(a^2+b^2)+\eta,
\tag{Q1}
\]

则 `eta=0`。

**证明。** 假设 `eta!=0`。多项式

\[
q=a^2+b^2+\eta/K
\]

在 `Q(i)[a,b]` 中不可约。因为若分解为两个一次因子，其最高次部分必须是 `a+ib` 与 `a-ib` 的倍数；一次项同时消失会迫使两因子的常数项均为零，与非零常数项矛盾。等价地，它的三变量齐次化是秩 3 的二次型，不能分解为两个线性式。

复共轭固定这个不可约因子。令 `G=A+iB`，则

\[
v_q(G\bar G)=v_q(G)+v_q(\bar G)=2v_q(G)
\]

为偶数，而 `Kq` 的 `q`-valuation 为 1。矛盾。分母不会破坏论证，因为 valuation 在函数域中可以取负值。证毕。

此引理并不否认某些特殊整数 `(a,b)` 上存在 repair；它只否认通用有理恒等式。下面正是对这些特殊点计数。

### 5.2 规则类的精确定义

允许有限多个源状态

\[
m=a^2+b^2+A_s3^c+B_s5^d+C_s,
\quad A_s,B_s\in\mathbb Z_{>0},\quad C_s\in\mathbb Z.
\tag{Q2}
\]

每条最终输出原始状态的规则固定整数

\[
n=K_e m+R_e,\quad K_e\ge2.
\]

输出是

\[
n=a'^2+b'^2+3^u+5^v.
\]

允许 `c,d,u,v` 任意选择，也允许任意 guards，而不限于同余 guards。对每个固定的指数四元组，`a',b'` 必须由关于 `a,b` 的有理公式给出；公式张数具有与指数无关的统一有限上界 J，分子、分母的总次数有统一上界 `D`。这些公式的系数允许依赖四个指数；但不允许在指数固定后，再通过任意非有理的 `m`、`a` 或 `b` 查表来选择无限多张公式。所有分母必须有定义，所有成功输出必须是整数。

有限状态、有限条边、固定有理公式的通常架构是此规则类的特例。平方根、无界 floor 分支、无界 additive carries、非整数权重及多源表示的联合构造不在此声明内。

令 `L_R(X)` 为这些规则可作为**最后一步**输出的 `1<=n<=X` 的集合。不要求其源状态真的已经从基例生成；允许全部源表示只会扩大这个集合。

### 5.3 非零 defect 的精确数量级

固定一条边和四个指数，令

\[
\eta=K_e(A_s3^c+B_s5^d+C_s)+R_e-3^u-5^v.
\tag{Q3}
\]

若 `eta!=0`，由 Q1，输出公式的 norm 与 `K_e(a^2+b^2)+eta` 之差不是零有理函数。清分母，得到一个非零二元多项式，总次数至多 `4D+2`。

在 `0<=a,b<=L` 的整数网格上，一个总次数 `d` 的非零二元多项式有至多 `d(L+1)` 个零点。证明：令关于 b 的次数为 s，其首项系数是次数至多 d-s 的非零 a 多项式。至多 d-s 个 a 层可整层计入 L+1 个点；其余每层至多 s 个根，总数不超过 d(L+1)。这允许完整的竖直线分量。

因为 `n<=X`、所有权重为正，固定规则下有 `a,b=O(sqrt X)`，四个指数分别只有 `O(log X)` 种可能。因此所有非零 defect 的成功输出合计至多

\[
\boxed{O_{\mathcal R,D}(\sqrt X(\log X)^4).}
\tag{Q4}
\]

这一步不假设 guards 是 exhaustive，也不假设每条规则对所有表示有效。任意 guards 只会取上面集合的子集。

### 5.4 零 defect：S-unit 轴纤维与有限例外

`eta=0` 等价于

\[
3^u+5^v-K_eA_s3^c-K_eB_s5^d-(K_eC_s+R_e)=0.
\tag{Q5}
\]

把非零项分成最小 vanishing subsums。对每个最小子和，在除去一个项后，Evertse–Schlickewei–Schmidt 的有限秩单位方程定理 [S4] 给出有限种 projective ratio patterns。

包含非零常数项的 block 固定其中所有指数。包含 3 幂项和 5 幂项的 block 也固定它们，因为一个确定的 `3^r/5^s` 比值唯一决定 `(r,s)`。因此唯一可能留下自由指数的 block 是

\[
3^u=K_e A_s3^c
\quad\text{或}\quad
5^v=K_e B_s5^d.
\tag{Q6}
\]

第一种要求 `K_e A_s=3^r, u=c+r`；第二种要求 `K_e B_s=5^t, v=d+t`。由于 `K_e>=2` 且 `A_s,B_s` 为正整数，这两种自由 block 不可能同时出现。

故全部无限族都是单轴族，此外只有有限多个指数四元组。对原始权重 `A_s=B_s=1`，这正是已有 N-006 的机制；此处同时给出用于加权源状态的适配。

在 3 轴族中 `3|K_e` 且 `u>=1`，输出满足

\[
n=K_e(a^2+b^2)+3^u+5^v\equiv5^v\not\equiv0\pmod3.
\]

在 5 轴族中，同理 `n not=0 mod5`。所以所有无限轴族均不输出 15 的倍数。

剩下有限多个指数四元组。每个只产生

\[
n=K_e(a^2+b^2)+h
\]

这样的平移、伸缩两平方和集合。经典 Landau 计数界 [S5]

\[
\#\{j\le X:j=a^2+b^2\}=O(X/\sqrt{\log X})
\]

给出这些集合的有限并仍然为零密度。

### 5.5 结论

**定理 Q。** 对上述有限规则类，

\[
\boxed{
\#(\mathcal L_{\mathcal R}(X)\cap15\mathbb N)
=O_{\mathcal R,D}\!\left(
\frac{X}{\sqrt{\log X}}+\sqrt X(\log X)^4\right)=o(X).
}
\tag{Q7}
\]

因此，几乎所有 15 的倍数都没有这种规则的最终入边。任何只由此类规则与有限基例组成的归纳架构，都不能覆盖全部整数。

这里的“几乎所有”是关于**规则不可达性**，绝不是关于 A303656 的反例。它也不是 universal finite-induction no-go。

本结论不需要先检查状态图是否有环：即使允许所有源状态、所有 guards、所有路径，最后一步已经不能覆盖一个正密度整数集合。

### 5.6 可选的定量复杂度推论

ESS 的非退化解数上界只依赖变量数及群秩，而不依赖固定系数。对 (Q5) 的最小子和，变量数至多 4、群秩至多 4；项的分块也只有有限种。所以非轴孤立四元组数可用一个绝对常数控制。

由此，对次数统一有界、`|R_e|,|C_s|` 统一有界的规则目录，若允许目录随 `X` 改变并要求覆盖 `[1,X]` 内全部 15 的倍数，其规则/chart 数 `J(X)` 必须满足

\[
J(X)=\Omega(\sqrt{\log X}).
\tag{Q8}
\]

隐含常数经由一般 ESS 界极其糟糕；这只是渐近复杂度下界，不是实际规模预测，也不授权大规模枚举。

### 5.7 广义架构定理 Q*：有限基例的全部可达集合只有零密度

Q 是一个**一步入边**定理，允许任意源表示，即使源状态无法从任何基例到达。以下追踪完整路径，获得一个针对全部可达集合的结论，并把允许的状态范围扩大到任意有限正定二元有理二次型和正有理幂权重。Q 与 Q* 的量词不同：Q 不要求源表示可达，Q* 要求实际的 witness-propagating 路径，因此不把它们混称为一个无条件的包含关系。Q* 的证明不使用 ESS 或 Landau。

#### 5.7.1 规则类

有限个状态 i 的表示形式为

\[
n=q_i(z)+A_i3^c+B_i5^d+C_i,
\quad z\in\mathbb Z^2,\quad c,d\ge0,
\tag{Q*1}
\]

其中

\[
q_i(z)=(z+h_i)^tG_i(z+h_i),
\quad G_i\in M_2(\mathbb Q)\text{ 对称正定},\quad h_i\in\mathbb Q^2,
\]

`A_i,B_i>0` 为有理数，`C_i` 为有理数。只取 n 为整数并满足该状态 guards 的表示。原始状态是 `q=a^2+b^2, A=B=1, C=0`。任何正定有理二次多项式的常数最小值可并入 C，因此这个写法允许非齐次二次型。

有限条规则具有固定 `n'=K_e n+R_e`，其中整数 K_e>=2、R_e 任意。固定四个输入/输出指数 `(c,d,u,v)` 后，输出坐标 z' 由有理 charts `Phi_e(z) in Q(z_1,z_2)^2` 给出；chart 数目有与指数无关的统一有限上界 J，分子/分母总次数统一 <=D。系数可依赖这些指数，guards 任意；成功时所有输出坐标、指数和状态 index 必须合法。这个条件不允许指数固定后还有无限多张隐含查表 charts。

初始资料只有有限个 `(state,index)` 基例。正定性与正权重保证每个基例实际具有有限多组表示；在上界证明中允许它们全部作为 seeds。

**witness continuity 是实质假设：** 每条边使用上一条边实际得到的表示。不能在只保留 `(state,index)` 后，无代价调用一个 oracle 重新选择任意指数不同的表示；这会改变 norm，属于另一个未被本定理建模的 existence decoder。单纯固定 norm 的换坐标不破坏下面的计数；但改变幂项、从而改变 norm 的无限表示重选不能悄悄省略。对“从任意给定源表示都能 lift”的规则，本定理直接适用。若只保证存在一个特选源表示，必须另证这个选择能由已建立的状态性质推出。

#### 5.7.2 广义 norm-defect rigidity

设 q_i,q_j 为以上中心化的正定二次型。若有理函数 Phi 满足

\[
q_j(\Phi(z))=Kq_i(z)+\eta
\]

作为恒等式，则 eta=0。

证明与 Q1 相同，但在目标二次型的 splitting field 中进行。配方后 q_j 可写成

\[
\alpha\{\ell_1^2+\delta\ell_2^2\},\quad
\alpha,\delta>0\text{ 有理},
\]

其中 `ell_1,ell_2` 是可逆有理仿射坐标。故左侧是 `Q(sqrt(-delta))/Q` 中一个 norm 乘有理常数。若 eta!=0，右侧除去 K 后的二次多项式，其三变量齐次化具有秩 3：在中心化坐标中行列式为 `(eta/K) det(G_i)!=0`。所以它在 splitting field 上仍不可约，而且被共轭固定。norm 的该因子 valuation 必为偶数，而右侧 valuation 为 1，矛盾。

因此这一 rigidity 不限于 Gaussian 源/目标，也不依赖两种二次型具有相同的判别式。

#### 5.7.3 所有非零-defect 输出的计数

对一条成功边，设

\[
\eta=K_e(A_i3^c+B_i5^d+C_i)+R_e
      -(A_j3^u+B_j5^v+C_j).
\tag{Q*2}
\]

若 eta!=0，每张 chart 只能在一个非零二元多项式的零点集上成功，次数仍 <=4D+2。目标 index <=Y 时，源和目标的四个指数各有 `O(log Y)` 种可能，源坐标位于边长 `O(sqrt Y)` 的整数网格内。因此这种输出**表示**（进而其 norm 值）的总数有界为

\[
\boxed{\mathcal D(Y)=O_{\mathcal R}(
\sqrt Y(1+\log Y)^4).}
\tag{Q*3}
\]

这里统计全部可能源表示，无需知道它们实际可达。

#### 5.7.4 最后一次 defect 与乘法尾部

考虑从某个 seed 到原始状态的任意有限路径。若每一步 eta=0，沿途的二次型值只按固定 K 倍率相乘。因此最终 norm 是

\[
q_{\rm final}=S q_{\rm seed},\qquad
S\in\mathcal M=\langle K_e:e\text{ 为规则}\rangle_{\rm multiplicative}.
\]

否则，取路径上**最后一次 eta!=0 的步骤**。令它的输出 index 为 m、二次型值为 q_*；之后所有步骤 eta=0，所以

\[
q_{\rm final}=S q_*,\qquad S\in\mathcal M.
\tag{Q*4}
\]

零 norm 的情形单独处理：若 q_*=0，则最终仍为零 norm，原始整数只是 `3^c+5^d`，只有 `O(log^2 X)` 个。

各状态的 q 值具有统一有理分母，故非零 q>=epsilon>0。因此最终 index <=X 时 S<=X/epsilon。设所有倍率中的不同素因子共有 r 个，则

\[
\#(\mathcal M\cap[1,X/\epsilon])=O_{\mathcal R}((1+\log X)^r),
\tag{Q*5}
\]

并且更重要地

\[
\sum_{S\in\mathcal M}S^{-1/2}
\le\prod_{p\mid\prod_eK_e}(1-p^{-1/2})^{-1}<\infty.
\tag{Q*6}
\]

为何可以按 X/S 控制最后一次 defect 的大小？令最后这段尾部的倍率乘积为 S，`R_max=max |R_e|`。逐次代入 `n'=Kn+R` 得

\[
\left|m-\frac{n_{\rm final}}S\right|
\le R_{\max}\sum_{j\ge1}2^{-j}\le R_{\max}.
\tag{Q*7}
\]

若 m 不超过某个固定 B>2R_max+2，这些状态表示只有有限多组，可并入有限的 seed norm 集。否则 `m<=2X/S`。

对于每个 S，(Q*3) 因而给出至多

\[
O_{\mathcal R}(\sqrt{X/S}(1+\log X)^4)
\]

个可能的 q_*。每个最终 norm 搭配的原始指数对只有 `O(log^2 X)` 种。对 S 求和，并使用 (Q*6)，得到非零-defect 路径的总输出数

\[
O_{\mathcal R}(\sqrt X(1+\log X)^6).
\]

没有 defect 的路径、以及低 index 最后-defect 路径，由有限 norm 集及 (Q*5) 产生至多 `O((1+log X)^{r+2})` 个整数。

#### 5.7.5 定理与边界

**定理 Q*。** 在 (Q*1) 指定的有限二次型状态、有限固定 K>=2/R、统一有界次数有理 charts 和有限基例之下，原始状态的可达整数集合 Reach 满足

\[
\boxed{\#(\operatorname{Reach}\cap[1,X])
=O_{\mathcal R}\!\left(
\sqrt X(1+\log X)^6+(1+\log X)^{r+2}\right)=o(X).}
\tag{Q*8}
\]

所以该类架构不仅不能证明全部整数，甚至不能从有限基例生成正密度的原始整数集合。

这个结论允许任意 guards、任意指数重选、不同判别式的二元正定形式和有理 cosets。它也已包含 B13 的三个辅助状态。检查路径是否有环不是遗漏：证明计数所有有限路径；零 norm 尾部可能出现的重复也单独计入稀疏 shift 集。

**仍未被排除的东西：** 不由有界次数有理 charts 实现的 Boolean 或 algebraic-root 选择、联合调用多个源表示、无限规则或次数增长、非二元二次型状态、依赖平方坐标的 index maps 等。仅指数依赖的 carry 还有下一节的扩展，不能一概当成已逃出 no-go。不能把 Q* 的 Reach 补集称作原题反例集合。

### 5.8 扩展 Q†：仅仅允许指数依赖 carry 仍不够

甚至可以允许

\[
n'=K_e n+R_e(c,d,u,v),\qquad K_e\in\mathbb Z_{\ge1},
\]

其中 carry 在四个指数固定后是任意指定的有理数，不要求从有限数值集合取值；但所有成功步骤必须满足 **n'>n**。状态、次数、chart 数与 witness continuity 仍按 Q*。

这时仍有

\[
\boxed{\#(\operatorname{Reach}\cap[1,X])
=O_{\mathcal R}\!\left(\sqrt X(1+\log X)^{r+6}
+(1+\log X)^{r+2}\right)=o(X).}
\tag{Qdagger}
\]

证明保留广义 norm rigidity 和最后-defect 分解。正向 index 单调保证最后一次 defect 的 source/target index 都 <=X，所以 (Q*3) 直接给出 `O(sqrt X log^4 X)` 个可能的 repair norm。之后的不同 multiplier S 只有 `O(log^r X)` 种，每个 final norm 配 `O(log^2 X)` 个幂对即得上界。K=1 不增加乘法半群复杂度；零 norm 仍单独处理。

这也解释了为什么 A4/A5 的 `-4*3^c`、`-8*5^d` 并非自动的逃生口：它们本身是 norm 无 defect 的单调步骤，从有限 seeds 出发只会让 norm 落在固定倍率半群中。

真正未涵盖的 target carry 可以依赖平方坐标、使用无界不同倍率、或伴随并非如此单调的另一种状态高度；不能把这里的结论外推到那些机制。

## 6. 状态错误与数值反模型

### 6.1 narrowed zero 不能冒充 original zero

令

\[
\mathcal A_c(n):\quad n=a^2+b^2+3^c+5^d.
\]

固定 `c` 的确有

\[
n\equiv3^c\pmod5,\ n>3^c,
\quad \neg\mathcal A_c(n)
\Longrightarrow
\neg\mathcal A_c\!\left(\frac{n+4\cdot3^c}{5}\right).
\tag{D1}
\]

高度 `n-3^c` 恰好除以 5。但它只能下降到 `n-3^c` 不被 5 整除的**无限终止集合**，不是有限基例。

而且 `A_0(21)` 与 `A_0(5)` 都为假：减去 `1+5^d` 后余数总是 `3 mod4`。下降 `21 -> 5` 完全正确；原始问题却两点都可表示：

\[
5=0^2+1^2+3+1,\quad
21=1^2+4^2+3+1.
\]

因此终止时不能丢掉固定 `c` 的状态标签，再援引原始问题的小数值基例。

### 6.2 计数 domination 也不能凭支持直觉假设

精确系数给出：

| q | n | floor(n/q) | f(n) | f(floor(n/q)) |
|---:|---:|---:|---:|---:|
| 3 | 25 | 8 | 8 | 9 |
| 5 | 98 | 19 | 20 | 28 |
| 9 | 109 | 12 | 16 | 20 |
| 15 | 506 | 33 | 36 | 40 |
| 25 | 382 | 15 | 20 | 24 |

它们否定相应的简单 coefficient inequality `f(n)>=f(floor(n/q))`，不是原题反例，也不否定 Boolean implication。

### 6.3 计数 no-go 与支持 positivity 完全可以并存

令

\[
A(x)=\frac1{1-x}+F(x).
\]

A 的每个系数都至少为 1，所以其支持就是全部非负整数。然而定理 M 立即推出 A 也没有有限 rational-coefficient mixed-dilation 关系：否则减去对应的有理 forcing 就得到 F 的禁用关系。

这是一个无需假设 A303656 成立的明确反模型：**计数序列没有有限线性递推，不妨碍其支持已经是最简单的有限状态语言。** 因此 M/M+ 从不单独推出原题的任何反例，也不排除 Boolean 层面的完整归纳证明。

## 7. E — 一个明确的 restart lemma

**LEMMA R — Boolean five-window decoder（尚未证明）。**

对每个整数 `m>=2` 和 `r in {0,1,2,3,4}`，

\[
\boxed{
[x^{5m}]H_{1,0}(x)>0
\quad\Longrightarrow\quad
[x^{5m+r}]F(x)>0.
}
\tag{R}
\]

这里

\[
H_{1,0}(x)=T(x)L_3(x^5)L_5(x)
\]

是一个完全指定的状态，不是一个未定义的新对象。

**为什么它足够。** (B2) 给出 `h_{1,0}(5m)>=f(m)`。假定 `n>=10` 为最小原始反例，写成 `n=5m+r`，则 `m>=2` 且 `m<n`，所以 `f(m)>0`；因此 `h_{1,0}(5m)>0`，由 (R) 得 `f(n)>0`，矛盾。

真正的基例只有 `2<=n<=9`，可明确写成：

```text
2 = 0²+0²+1+1       3 = 1²+0²+1+1
4 = 1²+1²+1+1       5 = 1²+0²+3+1
6 = 2²+0²+1+1       7 = 2²+1²+1+1
8 = 2²+0²+3+1       9 = 2²+1²+3+1
```

**本轮没有证明 (R)。** 它加上这些基例等价于一个完整解决方案；不能把这个重述当作已跨越 pointwise bottleneck。它的作用是准确指认网格缺失的“解码并遗忘权重”步骤。

定理 M 不排除 (R)，因为 (R) 只比较支持、不比较计数。定理 Q 则说明，不能期待把 (R) 与 Gaussian injection 复合成有限张、有界次数、固定 affine target 的单源有理 witness formulas；这种复合会落回已排除的规则类。仍可能的实现必须真正使用非有理选择、无界 carry、另一种未覆盖的状态类型，或多表示之间的存在性关系。

有限数值检验 (R) 没有新的 theorem value：若目标 `f(n)>0` 已在该有限区间直接验证过，(R) 在同一区间成立只是重复已知事实。

## 8. 精确计算证书与可重放性

运行：

```bash
python verify_thread3.py --N 20000
```

依赖 Python 3.10+、NumPy、SymPy；不访问网络，不写入 GitHub，不进行大规模 original-n 扫描。

已执行的结果：

- 6 项符号 identity checks，包括 Gaussian lifting、有理旋转及网格的二次 rank-one identity。
- `1<=K<=100` 的全部整数 `2x2` norm similitude matrices，与闭式分类逐一匹配。
- (B2)、(B4) 在 `0<=u,v<=2` 的 18 个实例，每个逐系数检验到 `x^20000`，全部通过；余项逐项非负。
- (B13) 的三个完整 residue 分支逐系数核验：偶数分支 m<=10000，两个奇数分支 m<=4999；全部通过。
- (B15)、(B16) 的非线性 theta 系统逐系数核验到 20000；另外仅用闭合递推重建前 512 个系数，核对通过，并复现 `2q_2=1-1=0` 的 cancellation。
- 使用独立的 divisor-sum 公式重算全部 r_2(n)，与整数格枚举交叉核对；另以直接四变量枚举核验 f(0)..f(400)。
- 有理中心化二次型的三变量齐次化行列式，以符号运算验证为 eta*det(G)。
- 固定 `c=0` 的 `21 -> 5` 状态反模型精确检验。
- `K in {1,3,5,9,15,25}`、多项式次数 `<=12` 的 78 列关系搜索：提取了 78x78 整数系数子矩阵，在素数 `1000000007` 下的行列式为 **118956141 != 0**。选取的最大 coefficient index 为 **79**。

- 再增加次数 <=12 的多项式 forcing，共 91 列：满秩；选定子式模上述素数的行列式为 **398217515 != 0**，最大 coefficient index 为 **90**。

这两项都不是数值拟合：非零模素数行列式证明整数行列式非零，因此严格排除这些有限次数范围内的相应复系数多项式关系（78 列对应齐次关系；91 列另含 forcing）。它与定理 M 的无界证明是独立的有限交叉检查，不能取代后者。

`certificate.json` 保存矩阵目录、余项哈希、pivot rows、pivot values、模素数行列式与反模型。脚本另用 SymPy 的有限域矩阵行列式重算选定子式，与增量消元独立核对。

精确截断系数的 SHA256（逗号分隔十进制编码）：

```text
f(0),...,f(20000):
ba233c4ed7c44cc2de546be1111467fae1e33209fb75b3e65f41e006bdec89b2
```

## 9. 对抗性审查台账

| 检查项 | 结果与边界 |
|---|---|
| c=d=0 convention | `L_b` 首项 x；所有 boundary terms 均保留 |
| 整数性 | Gaussian / 3-scaling 自动；一般有理 rotation 必须额外 guard |
| 指数非负 | 所列正向规则不减少指数；反向只用于既有 forward image |
| well-founded height | B13 的三个入口全部严格降 index；但辅助状态未闭合。网格方向另有限制；固定 c 终止于无限集合 |
| exhaustive guards | B13 穷尽 even / 1 mod4 / 3 mod4；Q 与 Q* 允许任意 guards 后仍给出其 no-go |
| finite bases | 旧轴模型没有；R 若成立则只需 2..9 |
| cycles | 网格严格增加 u+v；有限剪裁无环，但这本身不证明覆盖 |
| unreachable residue | Q 的类中，15 的倍数除零密度外均无最终入边 |
| infinite states | 网格状态在 C(x) 上线性无关；M+ 排除有限有理线性闭合系统，含多个固定倍率 |
| novelty | 不声称文献首创；未把 N005–N007 重算为新发现 |
| count vs support | M 排除计数级线性递推，不排除 Boolean 递推 |
| linear vs nonlinear | 明确存在 H00 H11 = H10 H01，不声称代数无关 |
| bounded vs unbounded | 有理次数上界、有限 charts、有限 K/R 是 Q/Q* 的实质假设 |
| witness continuity | Q* 统计实际输出接下一输入的表示路径；不偷偷加入按 index 任意重选表示的 oracle；Q 的一步上界则允许全部源表示 |
| source-state scope | Q 仅正整数权重；Q* 容许任意有限正定二元有理二次型、正有理幂权重及有理平移，不容许多源联合 witness |
| existing project status | 本轮材料未修改 PAUSED / UNRESOLVED 的冻结权威 |

## 10. F — Verdict

```text
KILL:
  原始 F 的有限 rational-coefficient scalar Mahler / mixed-dilation equality。
  包含 F 的有限 rational linear system Y=b+sum A_K Y(x^K)，有限整数 K>=2。
  有限基例 + bounded-degree 单源有理 lifting + 固定 K>=2,R
  + 有限正定二元有理二次型 / 正有理幂权重状态。
  仅指数依赖 carry 的单调扩展，见 Q†。

CONDITIONAL:
  LEMMA R（Boolean window decoding）；本轮没有证明。

HEDGE:
  不受上述假设覆盖的 Boolean / 非有理选择 / 平方坐标依赖 carry / 多表示递推。

PROMOTE（仅供独立审阅，不是主证明路线晋级）:
  定理 M、M+、Q、Q*、Q† 的证明稿和精确重放包。
```

本轮研究上的价值是把“再多搜一些矩阵／再写一个 Mahler 方程”转化为计数级与 witness 级两组带准确量词与边界的否定定理，而不是得到 universal representation 的正向进展。

## 11. 外部数学输入与引用对应

完整 URL 与访问日期存于 `sources.json`。

- **[S1]** NIST Digital Library of Mathematical Functions, §20.7, equation 20.7.32：theta modular transformation。用于 (M5)。
- **[S2]** NIST DLMF, §5.2：Gamma 的解析延拓、无零点性质。用于 (M4)。
- **[S3]** P. Flajolet, X. Gourdon, P. Dumas, *Mellin transforms and asymptotics: Harmonic sums*, Theoretical Computer Science 144 (1995), 3–58，尤其 pp.23–24 的对数周期与 harmonic-sum Mellin 机制。报告所需特殊版本在 §4.2 自行推导。
- **[S4]** J.-H. Evertse, H. P. Schlickewei, W. M. Schmidt, *Linear equations in variables which lie in a multiplicative group*, Annals of Mathematics 155 (2002), 807–836；arXiv:math/0409604。使用非退化有限秩单位方程的有限性及只依赖维数和秩的数量界。
- **[S5]** 经典 Landau 两平方和计数定理；可核验的现代原始研究文献入口：E. Bank, L. Bary-Soroker, A. Fehm, *Sums of two squares in short intervals in polynomial rings over finite fields*, arXiv:1509.02013，其引言回顾整数版本。这里不使用该文有限域结果来替代整数定理。

- **[S6]** F. Chyzak, B. Salvy, *Non-commutative Elimination in Ore Algebras Proves Multivariate Identities*, Journal of Symbolic Computation 26 (1998), 187–227，§1.2、§1.5.5：skew polynomial/Ore fractions 背景。M+ 的共同倍数维数证明、最低次数矩阵论证与本题适配另行给出，不误用 polynomial Mahler algebra 的 Noetherian 性。

- **[S7]** NIST DLMF, §27.13, equation 27.13.7：Jacobi 的 `r_2(n)=4(delta_1(n)-delta_3(n))`。仅用于独立系数重算，不作为 M 或 Q* 的证明前提。

外部输入只用于上面注明的环节；定理 M 的 mixed-phase/Vandermonde 推导和定理 Q 的 bounded-degree rational repair 计数、M+ 的消元及 Q* 的最后-defect 路径计数是本报告给出的适配证明，不是声称这些文献已经写出了 A303656 的对应结论。
