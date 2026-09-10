# B31^odd Branching Phase G — 形式陈述与证明

## 0. 证明地位、来源与边界

以下是本轮提出并自审的数学推导，不是 proof-assistant formalization、独立作者审稿或 repository promotion。程序只认证明确的有限证据。出处编号见 `SOURCES.md`，固定仓库绑定见 `SOURCE_BINDING.json`。

本包的成功等级是 **E：指定路线的严格剪枝**。G5 给出一个额外固定底数同余，但没有显著缩小 terminal candidate class，故不计 C。没有证明 B31^odd 空，没有认证 base-5 member，没有全局有限临界族，也没有 N>=8。

G1 的单边互反律、F4 的 closed-state criterion、Hensel 唯一提升，以及 lower-state CRT 可改变终端 lifting 的基本思想均已有来源。特别地，[S3, §13/E8] 已有 variable-base CRT 反例。本轮不将这些基础重新标成首创；新增工作是全图/任意 antichain 的精确定理、prime-to-q 幂剩余的适用边界、保留实际 all-odd 全闭包的认证反模型，以及 G5 的 mod8 分支特征。无文献优先权主张。

## 1. 固定 base 5 的定义

对 admitted prime x>3，即 x≡3 (mod4)，令

    w_x = ord_x(5),   s_x = v_x(5^{w_x}-1),
    O(x) = {odd prime p : p | w_x}.

absolute order DAG 必须展开全部 admitted odd order factors；到 3 或 1 mod4 素数停止。D(q) 含 q 及全部 admitted descendants >3；T(q) 为 terminal set。**3 不属于 D(q)，不属于 all-odd quantifier。**

来源 [S1] 的 B31^odd 要求：q nonregular，T(q)={3}，proper descendants 全 regular，唯一 basal gateway 为31，且每个 x∈D(q) 的 w_x 都为奇数、平方自由。这里 regular 指 s_x=1，nonregular 指 s_x>=2。

Good regular state R 是有限的 actual admitted regular prime set，包含31、不包含3，各 w_x odd squarefree，所有 order factors 属于 R∪{3}，且终端闭包为{3}。不要求 R 是链或由一个顶点生成。

A(R) 为 R 内没有上游顶点的 maximal-generator antichain。来源 [S1, F4] 给

\[
J_{31}(R)=\left\{3^\epsilon\prod_{p\in S}p:
 \epsilon\in\{0,1\},\quad A(R)\subseteq S\subseteq R\right\},
\]
\[
C_n=\frac{\Phi_n(5)}{\gcd(n,\Phi_n(5))},\qquad
Z_{31}(R)=\prod_{n\in J_{31}(R)}C_n,
\]
\[
q\in\mathcal B_{31}^{\rm odd},\ D(q)\setminus\{q\}=R
\iff q\equiv3\pmod4,\quad q^2\mid Z_{31}(R).
\]

不同 C_n 两两互素，平方来自唯一 primitive exact-order index，而不是跨分圆值的碰撞。上述判据是继承结果，不是本轮新证明。

来源 [S1, F2] 同时说明：B31^odd 若空，则存在任意长甚至无限的 regular all-odd prime-order chain。下文不使用 regular-state 有限终止假设。

## G1. 全图二次符号的一致性；没有 antichain 奇偶矛盾

### G1.1 单边与全边乘积

设 x,p 是不同的 3 mod4 素数，p|ord_x(5)。则 x≡1 modp，故

\[
\left(\frac{x}{p}\right)=1,
\qquad
\left(\frac{p}{x}\right)=-1.
\]

第二式是二次互反律 [P1]。于是任何有限边集 E，及任意非负整数权重 e_{xp}，都满足

\[
\prod_{(x,p)\in E}\left(\frac{p}{x}\right)^{e_{xp}}
 =(-1)^{\sum_Ee_{xp}},
\qquad
\prod_{(x,p)\in E}\left(\frac{x}{p}\right)^{e_{xp}}=1.
\]

逐边应用互反律得到的乘积关系恰是这两个等式，不是它们的相反式。无环性没有把第一个乘积改成+1。边的数目、入度、出度或 reachability 不提供额外符号公理。

实际 base-5 regular 例子：令 a=878851、t=490398859。来源的 exact orders，经本轮重认证，为

\[
w_{31}=3,\quad w_a=3\cdot31,\quad w_t=3\cdot31\cdot a.
\]

admitted 子图有 a→31、t→31、t→a 三条边，沿所有三条边的 lower-over-upper Legendre 乘积是−1。它是有向无环图，却不是“边乘积必为+1”的例子。它仅有 regular vertices，不是 base-5 nonregular member。

### G1.2 Mandatory maxima 乘积

若 q 是任何 admitted exact-order terminal candidate，n=w_q∈J31(R)，则每个 a∈A(R) 直接整除 n，故 q≡1 moda。由上式

\[
\boxed{\prod_{a\in A(R)}\left(\frac{a}{q}\right)
       =(-1)^{|A(R)|}.}
\]

从“DAG 的直接 order edges”推导和从“q≡1 moda 加互反律”推导所得的符号完全相同。没有任何一个 antichain 奇偶性在这一计算中被排除。

这不是说任意固定底数状态都存在 terminal，也不是说所有以互反律为工具的论证都无效。精确否定的是：仅把这些同一批 edge congruences 乘起来，就能从两侧得到相反符号。

## G2. Prime-to-q 幂剩余看不到 lifting；q-primary 测试看见的正是原 square hit

### G2.1 有限精度定理

设 q 是奇素数，h>=1，m>=1 且 gcd(m,q)=1。对任意 unit u modulo q^h，

\[
\boxed{u\in((\mathbb Z/q^h\mathbb Z)^\times)^m
\iff \bar u\in(\mathbb F_q^\times)^m.}
\]

**证明。** 向右显然。令 K 为 reduction map 的 kernel，它是阶 q^{h-1} 的有限阿贝尔群。因为 m 与 q 互素，k↦k^m 是 K 的自同构：取 m 在模 q^{h-1} 下的逆元作为逆映射指数即可。若 \bar v^m=\bar u，任取 unit lift v，则 uv^{-m}∈K。取 z∈K 满足 z^m=uv^{-m}，得到 (vz)^m=u。h=1 时直接成立。证毕。

因此同一个非零 modq residue 的全部整数 lifts，在所有这样的 m-th-power 测试中完全相同，即使某个 lift regular、另一个 nonregular。这是全 h、全 prime-to-q m 的定理，而不是只测几个小指数的经验结论。

### G2.2 2-power 层级不会比 quadratic 更强

若 q≡3 mod4，则 q−1 恰含一个2因子。有限域的 cyclic group 中，对于任意 j>=1，2^j-th powers 与 squares 是同一子群。结合 G2.1，模 q^h 的单位群中也一样。

对 B31odd 的 odd-order residue 5，quadratic、quartic、octic 等 **rational prime-power modulus 下的幂剩余存在性测试** 全部通过；这不区分 s_q=1 与 s_q>=2。

### G2.3 不能删除 gcd(m,q)=1

在模 q² 的 unit group 中，

\[
\boxed{u\text{ 是 }q\text{ 次幂}
\iff u^{q-1}\equiv1\pmod{q^2}.}
\]

若 u=z^q，则 Euler 定理给 u^{q-1}=1。反之若 u^{q-1}=1，则 u^q=u，所以 u 自己便是所需 q 次幂的一个根。

若 n=ord_q(u)，写 u^n=1+qκ modulo q²，则

\[
u^{q-1}\equiv1+q\frac{q-1}{n}\kappa\pmod{q^2}.
\]

(q−1)/n 在模q下可逆，故这恰好等价于 κ=0，亦即 primitive square-hit condition。q-primary 测试的确能区别 lifting，但所得条件只是原问题本身，不自动给出矛盾。

**范围。** 本定理并未否定所有 higher reciprocity：ramified number-field symbols、含固定整数5的全球单位关系、或额外 q-adic 算术均不属于上述有限 prime-to-q 幂剩余测试的范围。

## G3. 固定实际 all-odd state 与一阶 base-5 数据时，终端 lifting 可独立切换

设 R 是 actual base-5 good state，q>maxR 是 admitted prime，且 ord_q(5)=n∈J31(R)。本节 q 可以 regular 或 nonregular；不预设所求 base-5 root 存在。令

\[
M=8\cdot9\prod_{p\in R}p^2,
\qquad b_t=5+Mq t.
\]

则 M 与5q互素，所有 b_t 保持：

- 每个 proper p 的 base-5 residue modulo p²，因而保持其 exact order、regularity 与全部下游闭包；
- root q 的 base-5 residue modulo q，因而保持 exact order n；
- b_t≡5 modulo8和9，因而保留指定的小模数数据、terminal3 的 regularity；
- 所有 numeric prime labels、edge reciprocity、maximal-generator set，以及 G2 的全部 tame root power tests。

定义

\[
\kappa=\frac{5^n-1}{q}\pmod q.
\]

Taylor 展开给

\[
\frac{b_t^n-1}{q}\equiv
\kappa+Mt\,n5^{n-1}
\equiv\kappa+Mt\,n5^{-1}\pmod q.
\]

其斜率是 unit。因此恰好一个 t moduloq 满足

\[
\boxed{t_*\equiv-5\kappa(Mn)^{-1}\pmod q.}
\]

t=t* 的 residue class 使 terminal nonregular，其余 q−1 个 classes 使它 regular。随后在

\[
b=b_{t_*}+Mq^2j
\]

中改变 j moduloq，可使 (b^n−1)/q² 的系数遍历 F_q；除唯一一个 j 外均得到 **exact s_q(b)=2**。这给出同时保留 proper s=1 的完整 variable-base B31odd analogue。

**Prime-base 加强。** 每个选定的 exact-lifting residue class modulo Mq³ 都是 unit；故 Dirichlet 定理 [P2] 给出无穷多个素数底数 b，满足同一整套约束。regular 版本亦然。不能把原因归咎于“允许了 composite base”。若另加任意与q互素的有限 lower/auxiliary congruences，CRT 切换仍可做；prime-base 断言另外要求整个最终 progression 是 unit，不能在例如 b≡5 mod5 时无条件套用 Dirichlet。

**继承与新范围。** 这里的 CRT/Hensel 核心是 [S3,E8] 已有机制。本节明确了固定 base-5 actual R、保留 root first-order data、所有 tame tests、exact s=2 与 prime-base 的同时保持，并为其提供全 all-odd fixtures。

**重要逻辑边界。** 结论是一个关于变化底数 b 的定理，不是说 literal integer 5 可以自由改变，也不是信息论上无法由给定 q 计算 5 modq²。它否定的是对底数一致适用、且只依赖上述保持量的“proper regularity 强制 terminal regularity”命题。固定 base 5 的更强算术定理仍可能成立。

## G4. 任意有限允许 DAG、互反律符号与指定 lifting 标记可由某些素数底数实现

### G4.1 精确量词与允许输入

取任意有限 DAG，包含一个 terminal3 和至少两个 admitted vertices。其中指定 head 标签31，只指向3；每个其他 admitted vertex 至少有一个 admitted lower child；所有 admitted vertices 沿路径到达31；指定唯一 root 可到达全图。可有任意 branching、shared descendants、transitive edges，以及额外 direct3 edges。边按某个 topological order 指向较早节点。

对每个尚未赋 numeric label 的 admitted vertex，任意指定其 residue class 为11或19 modulo20。可再任意指定各 admitted label pair 的 Legendre symbols，但必须满足：两方向互为负号；edge 的 lower-over-upper 为−1、upper-over-lower 为+1。

给所有 proper admitted vertices 标记 s=1；给 root 标记任意指定整数 s>=2。更一般可指定各 vertex 的正整数 lifting valuation，但以下 B31 analogue 使用上述 proper/root 标记。head31 保持 s=1。

可选的 anchored 版本：先固定一个 actual base-5 good state R0 的全部 numeric labels、orders、modp² base data 与 pair symbols；它在图中必须 downward closed，并且与输入图兼容。所有新标签选在 maxR0 以上。没有 anchored 版本也至少固定 head31 的 base residue5 modulo31²。

### G4.2 结论

存在 numeric prime labels 与无穷多个 **素数底数 b≡5 mod8、b≡5 mod9**，使得：

1. 每个 vertex 的 exact order ord_x(b) 恰为其全部 outgoing labels 的乘积，而不是仅仅整除这个乘积；
2. 所有 orders 为奇数、平方自由；全部 prime labels admitted，且在指定的11/19 mod20 classes；
3. 全部指定 pairwise quadratic symbols 成立；
4. proper lifting 为1，root lifting 为所指定的 s；
5. absolute closure、terminal3 与 basal gateway31 全部恰为给定图，不产生隐藏的 free branch；
6. anchored base-5 proper data 原样保留。

因此，任意有限 maximal-generator width 都有 actual variable-base square-hit model；单纯 antichain parity 或 base-uniform 全图符号约束不可能排除全部这样的 marked DAGs。

### G4.3 证明：先选 numeric primes

按 topological order 逐点选标签 x。对每个已选 direct child p 施加 x≡1 modp；对每个已选 non-child p，按所需符号选择一个非零 residue c_p modulo p，使 (c_p/p) 等于所需 (x/p)。有限域中二次剩余和非剩余都存在。

这些不同 p 的条件，与 x≡11或19 mod20，模数两两互素，CRT 有一个 unit residue class。若有 direct3 edge，也加 x≡1 mod3；否则可不加3条件。Dirichlet 定理给这个 progression 中任意大的素数 x，所以可使 x 大于所有已选标签。

每条 edge 因 x≡1 modp 成立，且每对 admitted labels 都是3mod4，互反律保证其另一方向恰为所指定的符号。non-edge 的 x−1 可以仍被某个 lower label 整除；这不构成多余 order edge，因为我们下一步指定的是 exact order，不是 x−1 的全部因子。

令 n_x 为 x 的 outgoing labels 的乘积。它是奇数平方自由，且 n_x|x−1。故 F_x^× 中有 exact order n_x 的元素 u_x。head31 用 u=5，其 order 为3；anchored vertices 用5。

### G4.4 证明：再选 common base 的所有 lifting

对于未锚定 vertex x，要实现 valuation s_x，先把 u_x 提升成 X^{n_x}−1 的 root ω_x modulo x^{s_x+1}。这是 elementary simple-root lifting：每一步的下一位由

    f(u+x^j t) = f(u)+x^j t f'(u) mod x^{j+1}

唯一确定，因为 f'(u)=n_x u^{n_x−1} 是 unit。此处只用标准 Hensel 的 simple-root 情形 [P3]，也给出了有限递归理由。

施加

\[
b\equiv\omega_x+x^{s_x}\pmod{x^{s_x+1}}.
\]

Taylor 给

\[
b^{n_x}-1\equiv
x^{s_x}n_x\omega_x^{n_x-1}\not\equiv0\pmod{x^{s_x+1}},
\]

同时它被 x^{s_x} 整除，所以 exact valuation 为 s_x。modx residue 保持 u_x，故 exact order仍为 n_x。

对 head31 与其他 anchored proper vertices，直接施加 b≡5 modx²，保留 s=1。加上 b≡5 mod72，所有模数互素且 residues 为 unit；CRT 给单一 unit arithmetic progression。再由 Dirichlet 定理，这个 progression 有无穷多个素数 b。

这些 exact orders 的全部素因子就是指定 outgoing labels。由图的有限下降与 reachability，entire absolute closure 恰为图，终点只有3，唯一 basal gateway是31。由各点的 exact valuations，proper vertices regular、root nonregular。证毕。

### G4.5 精确排除与未排除

被否定：对所有底数成立、仅靠上述全图 closure／admission／order-squarefreeness／pairwise reciprocity 与 tame power-residue 结构，便能推出“nonregular terminal 不存在”的命题。其允许数据全都可与实际 square hit 共存，且底数可要求为素数。

未被否定：literal base=5 的空性；某个 additional fixed-base-5 global identity；unramified/tame 以外的数域 reciprocity 论证；需要一份更强全球算术关系而不仅是这些图/符号数据的 theorem。也没有说明每个固定 base-5 R 都有合适的 base-5 primitive divisor。

## G5. 固定 base 5 的聚合整数与 mod8 分支特征

设 R good，A=A(R)，p=maxR，

\[
\alpha=\prod_{a\in A}a,\qquad
\beta=3\prod_{r\in R\setminus A}r.
\]

α、β 为互素奇数平方自由整数。定义 d=p 当 A={p}；当 |A|>=2 时 d=1。

### G5.1 精确聚合（从 B7 的 E3.1 适配）

\[
\boxed{Z_{31}(R)=\frac{\Phi_\alpha(5^\beta)}d.}
\]

**证明。** 对 coprime α,β，比较根的 exact order 得

\[
\Phi_\alpha(X^\beta)=\prod_{e\mid\beta}\Phi_{\alpha e}(X).
\]

这些 indices 恰为 J31(R)。若 ℓ<=p 整除其中的某 Φ_n(5)，则 ℓ=2、5 不可能。若 ℓ∤n，则 ord_ℓ(5)=n>=p>=ℓ，矛盾。于是 ℓ|n；由于 n squarefree，cyclotomic valuation identity [S3,E1] 强制 n=ℓ ord_ℓ(5)，且该 imprimitive occurrence 的 valuation恰为1。

若 ℓ<p，p|n/ℓ=ord_ℓ(5) 又矛盾，故 ℓ=p。若 A 还有另一个成员 a，则 a|n/p=ord_p(5)，使 a 在 R 内有上游 p，违背 a∈A。因此 multi-max case没有 imprimitive factors。

当 A={p} 时，w_p|β，n=pw_p 是 J31(R) 的唯一 imprimitive index，恰贡献一个 p。剩余各素因子都大于 p，exact order 唯一，故没有跨 primitive parts 的重复。于是除掉 d 恰为来源 F4 的 Z31(R)。证毕。

这里把 B7 公式中的 6 改为3，适配 all-odd family；不是将 base-5 exact order 从 αe“压缩成α”，也不是已经分解这个巨大整数。

### G5.2 Mod8 signature

\[
\boxed{Z_{31}(R)\equiv
\begin{cases}
5\pmod8,&|A(R)|=1,\\
1\pmod8,&|A(R)|\ge2.
\end{cases}}
\]

**Singleton 证明。** β奇，所以 X=5^β≡5≡1+4 mod8。Φ_p(X)=Σ_{j=0}^{p−1}X^j，故

\[
\Phi_p(X)\equiv p+4\frac{p(p-1)}2
=p(2p-1)\pmod8.
\]

G5.1 给 Φ_p(X)=pZ，p 为odd unit，因此 Z≡2p−1≡5 mod8，因为 p≡3mod4。

**Multi-max 证明。** α 含至少两个不同奇素数，所以 Φ_α(1)=1。这一标准值也可由 X^α−1 的 Möbius product 在 X→1 取极限得到。分圆多项式为 reciprocal，degree φ(α)，故在1处求导得

\[
2\Phi'_\alpha(1)=\varphi(\alpha)\Phi_\alpha(1)=\varphi(\alpha).
\]

α 有两个以上奇素因子，φ(α) 被4整除，所以 Φ'_α(1) 为偶数。整系数 Taylor 展开给

\[
\Phi_\alpha(1+4)\equiv
\Phi_\alpha(1)+4\Phi'_\alpha(1)\equiv1\pmod8.
\]

此时没有 d 除数。证毕。

### G5.3 这不是 square-hit obstruction

每个 odd q 都满足 q²≡1 mod8。若 q²|Z，则

\[
Z/q^2\equiv Z\pmod8.
\]

故 G5.2 对含不含平方因子没有区分力。single-max Z 不是 perfect square，但“不是平方数”绝不等于“没有平方因子”。multi-max 的 residue1也不说明它是平方或平方自由。

原始 Φ 的其他因子不自动是 panel 的 actual rows；不能把给出整个整数同余的 companion factor 加收为一个 mandatory nonregular origin。G5.2 不给 N>=8，不给 state-size bound，亦不满足本任务 C 所要求的显著压缩。

## 2. Success-level 与 scope audit

A: B31^odd empty — NOT PROVED.
B: one globally finite critical family — NOT PROVED.
C: significant new restriction on arbitrary base-5 square-hit roots — NOT PROVED.
D: actual base-5 B31^odd member — NONE CERTIFIED.
E: specified base-uniform graph/QR/tame-lifting obstruction routes — PRUNED by G1–G4.

No use of finite branching => finite depth occurs. No change to original proper-regular, whole-closure, exact-order, all-odd, squarefree, terminal3 or gateway quantifiers is made.

GITHUB WRITES PERFORMED: NONE.
