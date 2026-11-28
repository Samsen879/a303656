# Finite dual mixed-edge mesh at L=128, K=11520

This focused certificate uses the original [#93](https://github.com/Samsen879/a303656/pull/93) anchor. It covers more than 2^97 **distinct generated targets**, with 65,536 primitive critical seeds on each of two mixed edges. A separate frozen 17th-layer extension has actual loading solutions within ordinary height, but no specified critical rotation on any such signed solution. Neither claim represents an externally prescribed target, and the negative result is limited to the frozen factor packet.

## Reproduce

From this directory, on Python 3.9+ with assertions enabled, run:

```sh
python3 -I -B verify/independent_34root_phase130.py data
python3 -I -B verify/literal_65536_independent.py data/released_phase_65536.json
python3 -I -B verify/independent_r17_phase10_mitm.py data
python3 -I -B verify/verify_r17_global_negative.py data
python3 -I -B verify/verify_r17_native_negative.py data
```

The first command includes the recursive Lucas primality certificates, complete trial division through 2^24, local counting and uniform rational angle check. The second verifies all 131,072 actual chords of one retained target. The remaining commands verify the global layer-17 signed CRT extrema and the least-positive ordinary-height native countercontrol. The scripts print computed outputs and some save local result JSON files beside the checker.

## Proof and exact quantifiers

## 1. 固定目标和精确量词

对任意整数 \(L\ge1\)，设

\[
\begin{aligned}
A&=9^L,&B&=25^L,&H&=3A+25B,\\
D&=12B-3A,&E&=A+10B,&h&=D-5,\\
J_0&=B-2A,&\Delta&=h^2+20E.
\end{aligned}
\]

合法整数参数恰可取 \(10\mid y\)。令

\[
t(y)=\frac{5y^2-hy+5+3h-E}{10},\qquad
P=(h-3t,t),
\]

\[
Q_1=P+(1,3),\qquad Q_2=P+(3-y,-1-3y),
\qquad S=N(P),\quad n=S+H.
\]

直接展开给出

\[
N(Q_1)=S+2D=n-9A-B,\qquad
N(Q_2)=S+2E=n-A-5B.
\]

三个真实标签分别为

\[
(2L+1,2L+2),\quad(2L+2,2L),\quad(2L,2L+1).
\]

这里标签 \((c,d)\) 意味着补上 \(3^c+5^d\)。高斯坐标取绝对值即可得到要求的非负平方变量。两条边都从同一个 \(P\)、同一个 \(n\) 出发，且各改变两个指数。

对高斯整数 \(G=m-ib\mid Q_e\)，令

\[
R=(Q_e/G)\overline G,\quad (x,z)=R-P,\quad
q=(x^2+z^2)/2.
\]

要求 \(N(G)\) 为奇数且与 \(10DE\) 互素。则弦坐标为奇数，且

\[
2qS=(D_e-q)^2+(xP_2-zP_1)^2,
\qquad (D_1,D_2)=(D,E).
\]

行列式为偶数。所谓本原临界种子，额外要求

\[
\gcd(x,z)=1,\qquad
64K^2q<S<64K(K+1)q,
\quad K=\lfloor\log_2 S\rfloor.
\]

角度的精确理想量为 \(2b^2/N(G)=2\sin^2\theta\)，其中
\(\theta=\arg(m+ib)\)。统一误差为

\[
\left|q/S-2b^2/N(G)\right|
\le D_e/S+|Q_e-P|/\sqrt S.
\tag{1}
\]

本轮使用

\[
Y=2^{K/4},\qquad 13Y/16\le y<7Y/8.
\tag{2}
\]

窗口长度是 **\(Y/16\)**，不是 \(Y\)。在主证书的整个窗口内，精确有理数界证明 \(2^K\le S<2^{K+1}\)、普通高度和误差小于 \(8/Y\)。\(t(y)\)、\(S(y)\)、\(n(y)\) 在此严格递增，因而参数数目就是不同目标数目。

另有一个有用的范围标记：\(h\equiv4\pmod8\)，合法参数下 \(t\) 为奇数，\(P_1\equiv P_2\pmod8\)，所以 \(S\equiv2\pmod{16}\)，\(H\equiv12\pmod{16}\)，从而 \(n\equiv14\pmod{16}\)。

## 4. 对所有复合子集共同控制本原性

### 4.1 两个精确 gcd 恒等式

在实际整除及 \(\gcd(N(G),10DE)=1\) 下，

\[
\boxed{\gcd(R_1-P)=\gcd(m-(2t+3)b,D),}
\tag{7}
\]

\[
\boxed{\gcd(R_2-P)=\gcd(5m+(5y-h)b,E).}
\tag{8}
\]

这里左端是弦两个整数坐标的正 gcd。任一共同奇素因子必整除对应 gap；乘以 \(G\) 在模 gap 上可逆。对第一边，若 \(G(R_1-P)=(u,v)\)，则 \(u=m-(2t+3)b\)、\(v-3u=2Db\)。对第二边，令 \(c_0=5m+(5y-h)b\)，则 \(v-3u=-2c_0\)、\(5u=(3-y)c_0+Eb\)。这证明完整 gcd 等式，而不只是必要条件。

因此，针对 \(p\mid D\) 的一个复合子集，坏相位由

\[
5m-b(5y^2+5y+5-E)=0\pmod p
\]

给出，至多两类。若 \(b=0\pmod p\)，则常数 \(5m\) 非零，没有坏类。对 \(p\mid E\)，(8) 至多排一类。这里的“一个因子”指**完整的 carrier 乘子集积**，不能只检验基本卫星。


### 4.3 小子群与释放相位

主证书的两个 carrier 为

\[
5083154-39i,\qquad5083136-39i.
\]

每个卫星为 \(m_j-i\)，且 \(39\mid m_j\)。因此模 3、13 时 carrier 的旋转为 \(+1\)，卫星旋转为 \(-1\)，任意子集都留在 \(\{\pm1\}\)。

精确坏相位进一步简化：模 3 的第一边对**所有** \(y\) 都安全；模 13 的第二边仅 \(y\equiv10\pmod {13}\) 对旋转 \(-1\) 失败。故只需保留

\[
y\equiv a\pmod {130},\qquad
a\in\{0,20,30,40,50,60,70,80,90,100,110,120\}.
\tag{9}
\]

无需固定 \(y\pmod {DE}\)，甚至无需固定模 3 的参数。

## 5. 主定理的精确构造与计数

### 5.1 冻结 34 个基本因子

`released_phase_65536.json` 给出两边各一个 carrier 加 16 个卫星，及其精确整除根。SHA256：

`9f9ecea648200594a8ce716c8a1402b2bbaeeb8588523d087e993a2e7c1e6d30`

34 个范数两两互素且与 \(10DE\) 互素；完整递归 Lucas 证书证明它们全部是素数，每条二次整除式有恰好两个不同根。故有 \(2^{34}\) 个互不相交的根选择，结合 (9) 为 \(12\cdot2^{34}\) 个参数类。

同一份 JSON 保留一个明确的实际目标：把其中存储根与 \(y\equiv0\pmod{390}\) 作 CRT，取 (2) 的第一个代表。这个代表的全部 **131,072** 次字面高斯除法、范数、弦 gcd、奇偶、恒等式、临界不等式与数值去重，已由未读取搜索核心的另一实现完整重放。

### 5.2 同一个内部角区间上的 dyadic 网

设

\[
W=\frac1{128K^2}=\frac1{16986931200},\quad
\delta=\frac W{65536}=\frac1{1113255523123200}.
\]

两边第 \(j\) 个卫星的角接近 \(W2^{-j}\)。证书逐边验证单侧总误差

\[
\sum_{j=1}^{16}\left[
W2^{-j}-\frac{b_j}{m_j}+\frac13\left(\frac{b_j}{m_j}\right)^3
\right]<\delta/100.
\tag{10}
\]

证书还逐项验证 \(0<b_j/m_j<W2^{-j}\)。结合 \(x-x^3/3<\arctan x<x\)，(10) 才得到所需的单侧误差门。它允许保留旧卫星后增加层数，避免错误地要求所有旧因子满足新的统一单项容差。

所以每边的子集角均形如 \(\theta_e+k\delta+e_k\)，\(0\le k<65536\)、\(-\delta/100<e_k\le0\)。所有相邻角隙在 \([0.99\delta,1.01\delta]\) 内。两 carrier 的角差小于 \(W/2\)，故共同覆盖一个长度大于

\[
W/3=1/50960793600
\]

的**内部**角区间。没有声称覆盖整个临界带。

跨边相位差除以 \(\delta\) 的整数部为 30,245，其小数部分被精确有理 Taylor 界夹在 0.932160477663768 与 0.9321604776756071 之间。扣除两边总误差后，跨边角分离仍大于 \(\delta/16\)。在这里 \(2\sin^2\theta\) 的导数大于 \(1/(8K)\)，这给出理想比例分离；它远大于 (1) 的统一误差。因此全部实际 \(q\) 在整个窗口中都临界且互异。

### 5.3 不完全分解 \(DE\) 的多数参数证明

完整试除所有不超过 \(2^{24}\) 的素数，得到

\[
D=3\cdot573737\cdot D_*,\qquad E=13\cdot E_*,
\]

各显示小素因子仅一次。余因子 \(D_*,E_*\) 分别为 578、595 bits，其所有素因子大于 \(2^{24}\)，故各最多 24 个不同素因子。这个结论不依赖余因子的完全分解。

对第一边的全部 65,536 个复合子集，模 573737 有 63,294 个不同的 \(m/b\) 值，没有 \(b=0\) 的情形。逐 \(y\) 枚举和独立判别式计数分别得到：坏参数类恰为 **63,550** 个。独立判别式方法的 0、1、2 根纤维数为

\[
(31519,0,31775),\qquad 2\cdot31775=63550.
\]

对任意一个根选择及任意一个 (9) 的安全相位，令

\[
T=130\prod_{\nu=1}^{34}p_\nu,
\quad N_0=\left\lfloor\frac{Y/16}{T}\right\rfloor
=2168307913068703036.
\]

该类在窗口内有 \(N_0\) 或 \(N_0+1\) 个候选。由于步长与每个余 gap 素数互素，一个素数的 \(b\) 个坏类最多损失 \(b(\lfloor N/p\rfloor+1)\) 个候选。用 (7)、(8) 的二次/一次次数差，余因子总损失不超过

\[
72\cdot65536\left(\left\lfloor N/2^{24}\right\rfloor+1\right).
\]

故每类的好点下界为

\[
N-63550\left(\left\lfloor N/573737\right\rfloor+1\right)
-4718592\left(\left\lfloor N/2^{24}\right\rfloor+1\right).
\tag{11}
\]

在两种可能的 \(N\) 上，(11) 分别为

\[
1318298606421300420,\qquad1318298606421300421.
\]

乘以互不相交的 \(12\cdot2^{34}\) 类，并利用 \(n(y)\) 单调，得到开头的精确下界。

不采用 63,550 的精细统计、只对 573737 用每个第一边子集至多两根的保守界，独立计算仍得

\[
219170044033061157232365797376>2^{97}.
\]

所以主结论的 \(2^{97}\) 门不依赖该精细计数的单点正确性。


### 6.1 第 17 层：所有合法相位下的真正角度—高度失配

继续保留前 34 个基本因子，只增加两条第 17 级卫星：

| 边 | \(m\)（因子为 \(m-i\)） | 范数 |
|---|---:|---:|
| 1 | 2226511046257290 | 4957351439105732170116878144101 |
| 2 | 2226511046247696 | 4957351439063009876161385308417 |

冻结数据是 `released_phase_r17_boundary.json`，SHA256：

`77d913c4ea3dd0dd69ee136d801f846efd492d2b67bbe43172ad50c209380638`

36 个范数的完整 Lucas 证书和各式两个不同根均通过。此次只施加最弱合法参数条件 \(10\mid y\)，不再附加模 3、13、\(DE\) 的相位。周期有 3016 bits，共有

\[
2^{36}=68719476736
\]

个互异的根选择。两个独立方法——逐半集合取补区间的 meet-in-the-middle，以及排序后单调双指针寻找模边界——精确求得：

- 最小非负共同根为 2977 bits；
- 最近的负共同根绝对值为 2980 bits；
- 所以每一个合法的、有符号的共同加载参数都满足 \(|y|\ge2^{2976}\)。

这是覆盖全部根类的压缩精确计数与极值证明，**没有逐条循环 687 亿次**。两个极值见证又被直接代回 36 条原始高斯整除式。

在此参数尺度，精确有理界给出

\[
t>.49y^2,\qquad h<t/100,\qquad
S>(1+2.99^2)(.49)^2y^4>y^4.
\]

因此真正的 \(K_{\rm actual}=\lfloor\log_2S\rfloor\ge11904\)。但冻结因子的所有 carrier/子集角都为正、总角小于 .01，理想比例至少为两个 carrier 理想比例的较小值。实际误差至多

\[
5/|y|\le5\cdot2^{-2976},
\]

而精确证书验证

\[
\min_e\frac{2\cdot39^2}{N(G_{e,0})}
-5\cdot2^{-2976}
>\frac1{64\cdot11521^2}
\ge\frac1{64K_{\rm actual}^2}.
\]

故这些冻结旋转的每一个实际 \(q/S\) 都超过当前高度的临界带上界。结论是：

> **固定 \(L=128\)、这 36 个有向基本因子及其 carrier/子集规则后，对任何合法整数 \(y\)，只要全部因子能够加载，全部这些旋转都不是临界种子。**

这已经超出了“某个选定窗口为空”的结论。更换根分支、取消额外相位、把目标移到另一个窗口都不能挽救这套冻结扩展。必须改变因子或角设计。它仍然不排除其他 17 层构造、其他目标参数化，也不排除 Sun 表示。

还有一个直接回代的、非空集式的原生反控：取最小正共同根，实际 \(K_y=11906\)，目标 \(n\) 仍在原普通高度内。36 个因子全部整除，两个 carrier 的实际旋转都为整数，两条奇坐标弦的完整 gcd 都为 1，标签和恒等式也全部通过；但两边都满足精确界

\[
1.068<64K_y^2q/S<1.069,
\]

所以严格非临界。完整 3585 位目标整数和两个 \(q\) 保存在 `r17_native_negative.json`，短脚本直接回代。不能把上面的结论误写成“整个普通高度都没有加载目标”；真实失败是角度与实际高度不匹配。

