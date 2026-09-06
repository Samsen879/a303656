# A303656 C=1 pooled-lower-cover inverse theorem — Endgame Phase B

## 结论

**本轮没有普遍消去 S1 的 pooled-lower 分支。** 得到的是一套保留 anchor 与 original-state provenance 的 exact inverse/contraction formalism、一个超出 #14 的算术 no-go subclass、一个新的无 prime cutoff 的资源零，以及一个精确的条件性反向构造。

最主要的新增结论是 **full-depth allocated-blocker theorem**：rigid row 不必分配到没有 dynamic row 的坐标；只要它在某个 order prime-power 坐标上的投影，与该坐标的 dynamic shell 合计仍有严格余量，就能同时避开两个 anchors。由此，任意系统只要其全部 nonregular rows 属于

\[
\{20771,40487,1645333507\},
\]

就不可能成为 complete C=1 certificate，其余 regular rows 的大小、数量、precision、accepted sets 均不受额外限制。关键新预算为

\[
\frac34+\frac2{27}=\frac{89}{108}<1.
\]

本轮还以完整因数分解和递归素性证书证明

\[
\mathcal R_{3,4}=\varnothing.
\]

结合 #16 的 depths 1–3，任何 original pooled full 3-fiber 至少需要 **122** 个不同 rigid primes；允许 dynamic 3-row 时仍至少需要 **31** 个。这里不是把 one-anchor 的 81/21 直接套到 pooled cover。

另一方面，本文证明一个 **squarefree order-closed seed construction**：若存在满足明确递归 order-support 条件的 actual nonregular prime，则可直接构造完整 odd pooled cover，但仍有一个 anchor escape，因而不是 full certificate。本文没有找到满足该 seed 条件的实际 prime。这把尚存的 arithmetic question 定位得比一般 Boolean cover 更精确。

“新增”仅指相对于本文实际读取的绑定 main 数学记录的推导，不主张文献优先权。证明与 reference checks 来自同一研究环境，不代替独立作者的审稿或 proof-assistant formalization。

---

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Bound current main SHA: 44e522dd6e88504e2b9829f0b27359e6c45a76ff
Bound current main tree: 6a30565826c8f988bfbb85e4098b78b2992d290c
```

已读取 live branch、repository metadata、三个 PR 的 merged 状态，以及固定 SHA 下的 STATUS.md、THEOREM_INDEX.md、ROUTE_MAP.md。合并顺序不是 PR 编号顺序：

| PR | Merge commit | Main first-parent 关系 |
|---|---|---|
| #15 | 76e7b4d447ea2ba9674b2787990dd37551d6844a | #16 的第一 parent |
| #16 | 25086bb932bbae00692ddf06cce0474aedf1cd7a | #14 的第一 parent |
| #14 | 44e522dd6e88504e2b9829f0b27359e6c45a76ff | 本轮绑定 main |

```text
PRECONDITION: PASS
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

数学 source map 见 `SOURCE_BINDING.json`。读取范围是九个指定目录内列明的定义、逆分类、证明审计及主报告；没有执行九个目录所有生成数据、所有历史代码及整个仓库 archive 的逐文件重放。`SOURCE_BINDING.json` 明确记录这一边界，不把目录存在等同于每个辅助文件都已读过。本轮本地程序不 import repository implementation。

本包仅为研究 artifact，不是已合并的 repository theorem record。没有创建 branch、commit、issue 或 PR。

## 2. POOLED DEMAND DEFINITIONS

### 2.1 原始行、coarse 与 full

沿用 [S1]：每个不同 actual prime q 满足 q≡3 mod4，q≠5；K_q≥2；r_q mod q^K 在 c=0,1 两侧共用；E_q 是非空的 positive odd valuation set。令

\[
V_{q,c}(d)=r_q-3^c-5^d,
\quad w_q=\operatorname{ord}_q(5),\quad s_q=v_q(5^{w_q}-1),
\]
\[
a_q=\max(0,K_q-s_q),\quad
U=\operatorname{lcm}(t_2,\{w_q\}),\quad
L=\operatorname{lcm}(t_2,\{w_qq^{a_q}\}).
\]

local zero modulo q^K 永不 accepted。`F_(q,c)^full` 是 accepted full exponents；`F_(q,c)^coarse` 是其**全部 full lifts 均被同一个 row 接受**的 coarse classes。以下未特别注明时 F 是 coarse event，H_q=F_q0∪F_q1。

Difference-2 给 F_q0∩F_q1=∅。#14 的 joint reverse CRT [S7] 进一步给出：共同 odd-row coarse escape 存在，当且仅当共同 full odd-row escape 存在。因此完整 odd pooled cover 的 coarse/full 表述等价。这一结论不能随意扩成两个 anchors 同时 two-adically safe。

### 2.2 六个 demand types

令 C⊆{0,1} 表示一个 exponent 已经被覆盖的 anchor 集合。正确的状态是一个 upward-closed Boolean demand，而不只是一个固定“待覆盖集合”：

| Demand | 满足条件 | Minimal satisfying anchor sets |
|---|---|---|
| FALSE | 不可能满足 | 空族 |
| BOTH | 0、1 均在 C | {{0,1}} |
| A0 | 0 在 C | {{0}} |
| A1 | 1 在 C | {{1}} |
| EITHER | C 非空 | {{0},{1}} |
| TRUE | 无剩余义务 | {∅} |

初始 simultaneous completeness demand 是 BOTH。S1 的第二分支只给 EITHER，不是 BOTH，也不是某个固定 A0/A1。

### 2.3 S1 的精确剩余义务

在 maximal original odd rank p，写 lower coverage 为 A_c(y)，top coverage 为 B_c(y,z)，并令 S_c(y)=∀z B_c(y,z)。[S8] 的 S1 是

\[
\mathrm{Complete}_{0,1}\Rightarrow
S_0\cap S_1\ne\varnothing\quad\text{or}\quad A_0\cup A_1=Y.
\]

进入 pooled 分支后，真正的双锚点要求仍为

\[
\forall y\;(A_0(y)\vee S_0(y))\wedge(A_1(y)\vee S_1(y)).\tag{2.1}
\]

所以 A0-only cell 仍要求 S1，A1-only cell 仍要求 S0；A0∩A1 中才没有 top demand。不能把 ∀y(A0∨A1) 当作式 (2.1)。

### 2.4 Two-adic boundary 不能隐藏

S1 的 A_c 包含 two-adic predicate。若 r2 为奇数，一个 anchor 恒为 3 mod4，故 boundary-inclusive pooled cover 可以自动成立。[S8] 的 common-safe boundary 恰为无 two-adic row，或 r2 为偶数。

实际 S1-shaped 反例：P={3,7}，K=2，E={1}，r3=2，r7=0；two-adic K2=2，r2=1。此时 U=6、L=42，有非空 original rank-3 dynamic event，lower domain Y=Z/2Z，而 A0=Y、A1=∅。它是 complete pooled lower cover，但两个 anchors 的 full coverage counts 为 42、20，并非 complete certificate。

因此“任何 admitted system 都不可能 complete pooled lower cover”的**不限定 boundary 的 Theorem A 是假的**。下面的非平凡 odd pooled inverse theorem 在一个固定 common-safe two-adic assignment 上工作；在没有 common-safe boundary 的情形，必须保留某一 safe anchor 的固定需求，不能把它悄悄换成 EITHER。

## 3. ROW-LEVEL POOLED GEOMETRY

### 3.1 每个 anchor 的完整分类

固定 q，取 t_c=r_q−3^c mod q^K。若 t_c mod q 不在 ⟨5⟩ 中，该侧 inactive。否则存在唯一 b_c mod w_q 使 5^b_c≡t_c mod q。令 h_c 为 t_c−5^b_c 的 clipped valuation。

若 h_c<min(s_q,K_q)，则整条 logarithm guard d≡b_c mod w_q 上 valuation 恒为 h_c；它在 h_c∈E_q 时是 rigid fatal cylinder，否则不是 fatal event。

若 K_q≤s_q 且 h_c=K_q，该 guard 全是 local zero，不 fatal。

剩余情况 K_q>s_q、h_c≥s_q。因为 5^w_q 生成 precision K_q 下从 q^s_q 开始的 principal subgroup，存在唯一 full exponent center d_c* mod w_qq^a_q 满足 5^d_c*≡t_c mod q^K。写 β_q=v_q(U)、m=min(a_q,β_q)、ζ_c=d_c* mod q^a_q，则 exact coarse event 为

\[
d\equiv b_c\pmod{w_q},\qquad
v_q(d-\zeta_c)=j<m,\quad s_q+j\in E_q.\tag{3.1}
\]

中心 cylinder C_m(ζ_c) 被排除；β<a 时它包含可达 local zero，而不是宣称其中每个 full lift 都已经为零。该分类也覆盖空 dynamic bundle。

### 3.2 Pooled shape 的正确陈述

如果两侧均有 active logarithm，则 b0≠b1 mod w，否则同一 exponent 的两个局部值均被 q 整除，与差 2 矛盾。因此两个完整 logarithm guards 总是不相交。

同一 original row **不能整体只标记一次 dynamic 或 rigid**：它可以一侧 dynamic、另一侧 rigid。本轮实际检查 q=20771，K=4，E={1,3}，

\[
r=1+5^{6528}\pmod{q^4}.
\]

anchor0 在 b0=6528 mod10385 上 dynamic；anchor1 在 b1=2 mod10385 上为 valuation-one rigid。原因是

\[
v_q(5^{6528}-5^2-2)=1<s_q=2.
\]

完整 row 的 H_q 是至多两个**带 guard、带 anchor 的正常形组件**之并。它未必是同一个 p-adic 坐标中的两个 cylinders：dynamic 组件是 shell bundle，混合 dynamic/rigid 的两个组件还可能有不同 assigned ranks。

固定一个 original rank-p fiber 后，至多一个 dynamic p-bundle 活跃；其他实际 rigid q 每侧最多贡献一个 depth e=v_p(w_q) cylinder。两侧均在同一 lower fiber 活跃时，它们是两个不同、等深、互不相交的 cylinders。

### 3.3 共同 residue 不等于固定 additive log displacement

令 w_q=u p^e。两个 rigid classes 必须分别通过 lower guards，并满足

\[
5^{b_0}-5^{b_1}=2\pmod q.
\]

对指定 h0,h1<s_q 的更高 valuation，令 ν=min(v_q(5^b0−5^b1−2),K)。可同时实现这两个精确 valuations，当且仅当 {ν,h0,h1} 的最小值至少出现两次 [S5]。共同 residue 和 local-zero exclusions 仍须保留。

指数差 b0−b1 不是一个与位置无关的固定常数。正确对象是固定 lower coset 的 paired-position graph；它的每个顶点入度、出度至多一，且没有有向环 [S9]。若 lower representative 为 Y、h=p^e，则双边资源必须满足

\[
q\mid\operatorname{Res}_T(T^h-5^{Yh},(T-2)^h-5^{Yh}).\tag{3.2}
\]

该整数在 odd h 下非零，但 Y 在所有整数中变化后不能据此获得统一有限 prime pool。

实际 q=40487、K=2、E={1}、r=25919 的两 rigid classes 为 3968、14260，lower 均为 0 mod62，top-653 positions 为 50、547。这否定“一个 pooled row 在 fixed lower 上至多一个 cylinder”，不构成 complete cover。

## 4. EXACT RECURSIVE FORMULA

### Theorem P1 — typed universal elimination

固定 top word T(z)⊆{0,1} 与 lower coverage C。对任一六态 demand D，定义

\[
(\mathcal R_pD)(C)=\bigwedge_{z\in X_p}D(C\cup T(z)).\tag{4.1}
\]

它仍是六态之一，因为 finite AND、以及 C↦C∪T(z)，保持 monotonicity。

若 S_c=∀z T_c(z)，S_or=∀z(T0(z)∨T1(z))，则

\[
\mathcal R_p(\mathrm{EITHER})=(C_0\vee C_1)\vee S_{or},
\]
\[
\mathcal R_p(\mathrm{BOTH})=(C_0\vee S_0)\wedge(C_1\vee S_1).\tag{4.2}
\]

证明直接使用 lower bit 对 z 不变，以及 ∀ 分别与 AND 分配。不能用 S_or 替换 S0 或 S1。

### Theorem P2 — anchor-tagged cover-clause contraction

把 rank-p 的 exact original/macro events 分解为

\[
E_i=G_i(y)\times C_i(z),
\]

记录 `(original row, global state, anchor/demand tag, slice, guard, provenance)`。对 EITHER 取所有两侧 slices；对 A_c 仅取有该 anchor 保证的 slices。令 C_p 为 inclusion-minimal exact slice covers I：∪_{i∈I}C_i=X_p。则

\[
\operatorname{Sat}^{\lor}_p(y)
=\bigvee_{I\in C_p}\bigwedge_{i\in I}G_i(y),\tag{4.3}
\]

只保留 original-state 选择一致的 clauses；所有 lower-rank events 原样保留，不将其中的 dynamic bundle 冒充 CRT cylinder。若参数正在搜索，状态 tokens 满足

\[
z_{q,s}z_{q,t}=0\ (s\ne t),\qquad z_{q,s}^2=z_{q,s}.
\]

证明：真实覆盖的活跃 slices 含一个 minimal subcover；反向，由 guard conjunction 使该 exact cover 的所有 slices 同时活跃。不同 state tokens 的相乘不能发生在同一实际系统；相同 token 的重复只是重用。相交 lower CRT guards 给空集或一个 CRT cylinder。宏必须记录相应 I，不能任意插入 lower point predicate。

### Theorem P3 — coloured-prefix inverse form

将 dynamic shell S_j 展开成 p−1 个 depth j+1 side cylinders，保留同一个 original dynamic row ID；将 rigid components 保持为一个带颜色的 cylinder。p-adic cylinders 两两不交或嵌套。从任一 pooled full fiber 的 primitive cover 中删除被 ancestor 包含的 cylinders，并在重复 geometry 中选择一个带原始 provenance 的供应项，即得 complete prefix antichain。

因此，一个 actual pooled fiber 覆盖，当且仅当它有一个 **由真实活跃组件供应的 coloured complete prefix frontier**。每个原始 rigid q 在此 fiber 最多供应两片原始叶，一片/anchor；两片必须来自一个全局 paired configuration。dynamic row 可以供应许多 side leaves，但始终只是一行。

这不是“任意给两色前沿都可算术实现”的 converse。它是对冻结 actual configurations 的精确 inverse criterion。对 derived macros 也有几何版，但 actual-prime 数量界只适用于 original leaves。

在 whole lower domain 的 EITHER cover 中，从 common-safe two-adic point 按坐标递增选共同逃逸 digit。若每一步均有逃逸，就得到 whole-system common odd escape，矛盾。因此必有一个**actual original pooled full fiber**，可应用上述 inverse form。这是合法的 pooled-to-resource bridge，不需要 H1。

## 5. SPLIT TRANSITION

重放 [S8] 的实际系统：

```text
p=67, q=20771, Kp=Kq=2, Ep=Eq={1}
r67=2, r20771=20775
U=L=228470, lower y=0 mod3410, z=d mod67
```

| Original row | Anchor0 fatal slice | Anchor1 fatal slice |
|---|---|---|
| 67 | X67\{0} | ∅ |
| 20771 | ∅ | {0} |

故 E0={0}、E1=X67\{0}。这是完整 pooled fiber，却没有任何单-anchor full fiber。其两色 contraction clause 的 stripped guards 为 0 mod22 与 0 mod155，intersection 为 0 mod3410，**类型仅为 EITHER**。

沿两个 anchor 的逃逸继续时，anchor0 分支带 z=0；anchor1 分支带 z≠0，可以精确分成 66 个 residue cylinders。它们携带同一组 r67、r20771，而不是复制后重新选择 residues。没有“之后必合流”的定理。

对该 top word，EITHER 的 residual demand 为 TRUE；BOTH 的 residual demand 仍为 BOTH。这给任何“仅凭 unresolved-demand 数值总保持正值”的候选反证；SPLIT 本身是实际合法 transition。

在 genuine original rank-p fiber 上，一行不可能 pooled-full：dynamic 行至多一侧活跃且漏 center；rigid 行最多两片、总质量≤2/p<1。因此该两行 SPLIT 是 **按 original row 数最小的 actual pooled full-fiber motif**。它不是按 prime 大小的全局最小性声明。

完整周期实际结果：Sat0=∅，Sat1={1705 mod3410}；anchor safe counts 为 218219、218218；共同 odd-safe exponents 为 207968 个。该系统不是 whole-domain complete pooled cover，更不是 full certificate。

## 6. MIXED-ANCHOR HALL/KRAFT

### 6.1 Configuration inequality

固定 residual EITHER demand set D、非负权 f，以及每个 actual q 的完整 paired-state family S_q。每行选择一个全局 state。完整 pooled cover 必须满足

\[
\int_D f\,d\mu
\le\sum_q\max_{s\in S_q}\int_{D\cap(F_{q,0}(s)\cup F_{q,1}(s))}f\,d\mu.\tag{6.1}
\]

证明是对覆盖指示函数积分，然后逐行上界为其一个 configuration 的最大值。EITHER 的一个点只收取一次 demand；不能在左侧写两个 anchors 的总点数。若 demand 是 BOTH，则需还原两层 tagged vertices，使用对应的 two-layer inequality。

对 prescribed frontier，整型约束必须同时选择一行的完整 pair，而非两侧分别 matching。式 (6.1) 只是必要条件：本文保留了 #16 的 fractional-feasible / integral-infeasible abstract regression，不将其声称为 actual prime counterexample。

### 6.2 Fixed original fiber 的 pooled Kraft bridge

在 fixed lower y、coordinate p，令 C=Σ_q p^{-e_q}，C_pair=Σ_q ε_q(y)p^{-e_q}，其中 ε 表示该 actual resource 的 paired graph 非空。令 D_max 为唯一可能 dynamic bundle 的允许最大质量。则 pooled full fiber 必须满足

\[
1\le D_{max}+C+C_{pair}.\tag{6.2}
\]

冻结 residues 后可用真实 cylinder union 进一步收紧。与 #16 的 joint bound 不同，这里的右侧目标是 1，不是 2；也没有一般的独立条件 C≥1。

对 cylinder B 或 branch antichain，必须使用 μ(B∩H_q)，保留 ancestor coverage；不能仅统计“严格落在 B 内”的 leaves。改变 lower branch 不会把 q 变成另一个 prime。

### 6.3 New cutoff-free depth-four resource zero

当 P⁺(w_q)=3 且 v3(w_q)=4，q≡3 mod4 强迫 w_q=81 或 162。nonregularity 要求 q²|Φ_{w_q}(5)。本轮证明以下完整分解：

\[
\Phi_{81}(5)=5^{54}+5^{27}+1
=4861\cdot11419697846380955982026777206637491,
\]
\[
\Phi_{162}(5)=5^{54}-5^{27}+1
=3\cdot1783\cdot5023\cdot2066067271380136212224701233463.
\]

六个因子均为不同 primes。`primality_certificates.json` 的 44-node recursive Lucas certificates 由 standard-library checker 验证；乘积与每个因子的 valuation 也独立检查。完整 factorization 而非有界 prime scan 给

\[
\boxed{\mathcal R_{3,4}=\varnothing.}
\]

结合 #16 已证明的 depths1–3，original rigid 3-cylinder 必有 depth≥5。每个 actual q 对 pooled fiber 最多贡献 2/243；故 rigid-only full fiber 需要 N≥ceil(243/2)=122。允许 dynamic3 时，其 finite mass 严格小于 3/4，因而

\[
1<\frac34+\frac{2N}{243},\qquad N>\frac{243}{8},
\]

得到 N≥31。作为 one-anchor corollaries，分别为 243 与 61。β3≤4 时不存在 original pooled full 3-fiber。这些 bounds 不主张 sharpness，也不证明供应这些 primes 的 arithmetic pool 非空。

## 7. ARITHMETIC CONSTRAINTS

本轮将 arithmetic constraints 放在不同但兼容的层级，而不混成一个未经证明的 scarcity 假设。

Difference-2 用于完整 logarithm guards 的不相交，进而把每个坐标两侧 dynamic hazard 压到一个 bundle。Order triangularity 使这些 guards 在选择该坐标前已经确定。Rigid common-residue valuation criterion、paired graph 和 resultant 用于过滤每行的 paired configurations；它们不能被只保留两个独立 marginals 的 CSP 替代。

Prefix inventory 的 depth restrictions 用于实际 original full fiber。本轮将 coordinate3 的 resource-zero gate 从 depth3 推至 depth4。它不限制 assigned rank 不为3、但 order 包含3的 rigid prime；例如 1645333507 的最大 order factor 为30469139，所以它与 R3,1–4 的空性不矛盾。

新的 blocker theorem 恰好在另一层使用该 prime：把它的 rigid congruences **投影到 order 中的 3³ coordinate**，而不是说它在 rank3 供应一片原始 rigid leaf。这个 distinction 是 2/27 预算合法的关键。

### Finite dynamic envelope

若 original p-row 在某侧 dynamic，则同一 lower point 至多一侧活跃，且

\[
D_p\le\sum_{j\in J_p}(p-1)p^{-j-1}
<\begin{cases}p/(p+1),&s_p\text{ odd},\\1/(p+1),&s_p\text{ even}.\end{cases}\tag{7.1}
\]

没有 original dynamic event 时 D_p=0。这是所有允许 parity shells 的几何级数上界；有限 precision 使不等式严格。特别地 D3<3/4，不是错误的无限 shell 全部已覆盖假设。

## 8. COUNTEREXAMPLES

| 对象 | 证据等级 | 排除的错误推理 | 未证明的东西 |
|---|---|---|---|
| §2 的 {3,7}+two-adic 系统 | ACTUAL SHARED-RESIDUE，COMPLETE BOUNDARY-INCLUSIVE POOLED LOWER COVER | 不限定 boundary 的 Theorem A | 非 complete C=1 certificate |
| §5 的 67/20771 SPLIT | ACTUAL SHARED-RESIDUE LOCAL FULL POOLED FIBER | pooled ⇒ 一个 anchor full；路径必合流 | 非 whole lower-domain pooled cover |
| q40487 的两个 same-lower rigid cylinders | ACTUAL SHARED-RESIDUE ROW | 一行 pooled 至多一片 rigid cylinder | 非 full fiber |
| q20771 的 dynamic/rigid paired state | ACTUAL SHARED-RESIDUE ROW | 一个 prime 在两 anchors 的类型必须相同 | 非全周期枚举或 complete cover |
| 三行 binary macro-mass regression | ABSTRACT | 原始质量3/2与两个宏质量2必须守恒 | 不否定所有 arithmetic potentials |
| 两行 paired-option matching regression | ABSTRACT | weighted/fractional configuration feasibility ⇒ 整型 cover | 不声称 actual primes 实现该 option family |

此外，actual regular-row skeleton P={3,7,31}、K=2、E={1}、r=2 有 U=6、L=1302。全周期 1302 个 exponents 中 pooled 覆盖1300个，共同 escapes 恰为 {0,651}。这既不是 complete cover，也不能把 full period L 自动写成 coarse U。它为 §10 的 conditional seed construction 提供一个实际、精确的 regular skeleton。

## 9. EXACT COMPUTATION

先冻结 `COMPUTATION_SPEC.md`；条件构造新增 skeleton target 在运行前写入 `COMPUTATION_SPEC_ADDENDUM.md`。对 U/L 的后续解释记录在 `COMPUTATION_NOTES.md`，未悄悄修改冻结规格。

| Audit | 本轮真实范围 | 结果 |
|---|---|---|
| 六态 demand elimination | 340 top words，8160 truth evaluations | 0 mismatches |
| Actual small row geometry | q=3,7,11；K=2,3；另 q3,K4；全部 residues 和非空 odd accepted sets，共2123 systems | 1,856,944 full anchor-cells、2,064,494 coarse anchor-cells，0 mismatches |
| Actual SPLIT | U=L=228470，全部 exponents、两 anchors、两 actual rows | 与 exact slice formula 一致 |
| Actual paired rigid masks | q20771、40487，指定 shared residues，各自完整 w-period | 正确保留两个 logarithms 与 shared lower constraints |
| Mixed q20771 row | K4，6个 offsets/anchor，加 symbolic LTE proof | 非 full-period enumeration，样点与公式一致 |
| Prefix geometry | 3² 的4096 cylinder subsets，三个 dynamic cases，共12288 | 0 mismatches；{1} shell case明确标为 abstract geometry |
| Stateful contraction | 360 abstract systems，2880 global assignments，8640 root comparisons | 0 mismatches，439 pooled covers |
| Occupied-coordinate blocker | 35154 abstract triangular models，2,214,702 direct cells | 0 mismatches |
| Depth-four factors | 2 complete products，6 factor primes，44 recursive primality nodes | 全部 PASS |
| Sparse subclass signatures | 3,67,20771,40487,1645333507 | trial-division primality、exact orders、lifting valuations 全部 PASS |
| Adversarial unit tests | 17项，包括损坏 certificate、state conflict、BOTH-positive fixture | 全部 PASS |

Stateful random models每行有两种 one-sided configurations，允许另一侧为空；不是所有 actual paired rows 的穷举。Both-covered positive fixture另由 unit test检查。Actual paired-nonempty rows由独立 arithmetic cases检查。

没有增加 prime cutoff，没有声称枚举巨大 q=1645333507 的 full period，没有把两百万同源循环称为 independent software stacks。Symbolic new theorems 的量词不依赖 bounded samples；有限 certificates 只负责明确的 arithmetic identities。`tools/reproduce.py` 全部使用 Python standard library，输出到包外目录以防污染冻结结果。

## 10. STRONGEST THEOREM

### Theorem P4 — full-depth allocated-blocker common escape

固定一个 admitted original system 及其 shared states。令 Q_R 为至少一侧有 original coarse rigid fatal event 的 primes。对每个 q∈Q_R 选择一个奇素数 b(q)|w_q；**允许 b(q) 的 original dynamic row 存在**。

若 q 的 rigid logarithm 为 b_{q,c} mod w_q，令 e_{q,p}=v_p(w_q)。把分配给 p 的全部 rigid classes 投影，定义

\[
\mathcal B_p=\bigcup_{q:b(q)=p}\bigcup_{c:\,q\text{ rigid-fatal at }c}
\{z:z\equiv b_{q,c}\pmod{p^{e_{q,p}}}\}\subseteq X_p.
\]

这里不检查其他 lower guards，故 B_p 是安全的 over-exclusion。设 D_p 是 original p-row 在任一 shared lower assignment 上的 pooled dynamic mass 上界。若

\[
\boxed{D_p+\mu(\mathcal B_p)<1\quad\text{for every odd coordinate }p,}\tag{10.1}
\]

则对每个固定 two-adic exponent assignment，存在同一个 coarse exponent，避开全部 original odd events 的两个 anchors；且有同一个 full odd-safe lift。

#### Proof

按实际 prime coordinates 递增选值。到 p 时，original p-row 的 w_p 所有因子均小于p，故两个 dynamic guards 已确定。Difference-2 使至多一个 active bundle。它的质量≤D_p；预先固定的 B_p 质量为 μ(B_p)。式 (10.1) 保证可以选择 z_p 同时避开二者。

每个 assigned rigid event 都被违反了自己一个必要的 prime-power congruence，因此之后无论选择其他坐标，都不能重新活跃。每个 dynamic event 在自己的 prime coordinate 处已被避开；later coordinates 也不能修改它，因为其全部 dependence 已固定。

有限坐标完成后，全部 odd events 在两 anchors 都被避开。按 [S7] 的 joint reverse CRT，在每一 row 的 private higher p-digits 上只可能有一个 anchor 可有正 p-divisibility，因而可选择同时 safe 的 local lift；不同 p 的 private digits 独立，CRT 合并为一个 full exponent。QED。

一个可直接计算的 sufficient inequality 是

\[
D_p+\sum_{q:b(q)=p}t_{q,p}p^{-v_p(w_q)}<1,\tag{10.2}
\]

其中 t_{q,p}≤2 是两 rigid logarithms 在该 projection 上不同 residue classes 的实际个数。对所有 shared residues 的 uniform theorem，可将 t 替换为2。精确 union 版本 (10.1) 不会因跨行重叠而重复收费。

#### Quantitative survival and potential

令 δ_p=1−D_p−μ(B_p)>0。相同构造给 common coarse odd-safe set 的 normalized measure 至少 ∏_p δ_p。这个正下界属于通过分配条件的原始系统，不属于任意宏 family 的 raw mass。

任何 whole-predicate exact contraction 对相应 escape set 取投影。非空集合的投影仍非空，因此上述 witness 在两侧各自的 whole residual predicate（或正确聚合的 branch frontier）中都有存活的 projection，不必让路径合流。这里不声称任意挑选的 child cylinder 都包含这个 witness。

一般系统的 active-coordinate rank 严格下降只证明 termination；original escape-set projection 保持非空只在已建立初始非空时有用。本轮没有声称找到使所有 pooled transitions 都产生 contradiction 的 universal arithmetic potential。

### Corollary P4.1 — #14 boundary resource 被消去

若所有 nonregular original rows 属于 {20771,40487,1645333507}，使用

\[
20771\mapsto5,\qquad40487\mapsto653,\qquad1645333507\mapsto3.
\]

精确 orders 为 5·31·67、2·31·653、2·3³·30469139，均 s=2。坐标5与653不可能有 admitted dynamic row，负荷分别≤2/5、2/653；坐标3的负荷满足

\[
D_3+\mu(B_3)<3/4+2/27=89/108<1.
\]

故有共同 odd escape。对任意 sound two-adic row，选一个 two-adically safe anchor 和一个 safe exponent class，再固定该 two-adic coordinate，应用 theorem；所得 full exponent 在至少一个 anchor 对所有 rows safe。因此不存在 complete simultaneous certificate。

这不是“所有 primes≤1645333507”的结论；未审计该区间的 nonregular inventory。Regular rows 可任意大，因而又不是只检查三个固定低 precision examples。

### Corollary P4.2 — single-nonregular surviving signature

若只含一个 nonregular original row q，则只要 w_q 有一个没有 original dynamic row 的奇因子，旧 blocker 已足够；只要存在 p²|w_q，新 theorem 也足够，因为

\[
\frac{p}{p+1}+\frac2{p^2}<1\qquad(p\ge3).
\]

因此任何仍可能 complete odd pooled 的 single-nonregular system，必须使 w_q 的 odd part **squarefree**，且每个奇因子都在原始系统中拥有 dynamic-capable admitted row。实际某个 row 是否 active，仍由 shared state 决定。

### Theorem P5 — squarefree order-closed seed construction

令 q 为 actual admitted nonregular prime。假设存在有限集合 T，满足：

- 每个 p∈T 均为实际 regular admitted prime，p<q；
- U=lcm(w_q,{w_p:p∈T}) 的奇素因子恰为 T；
- U 的 odd part M 为 squarefree，即 U=2^ε M，ε∈{0,1}、M=∏_{p∈T}p。

这等价于一个明确的递归 order-support gate：从 w_q 的 odd factors 开始，加入所需的 regular admitted row primes及其 order factors；不得引入5、1 mod4坐标、其他 nonregular support row或重复 odd prime-power depth。这里是充分条件，未宣称是所有 one-q systems 的必要条件。

取 P=T∪{q}，不加 two-adic row，所有 K=2、E={1}，并取共享 residues

\[
r_p=2\ (p\in T),\qquad r_q=q+2.
\]

则 U=L，且

\[
\forall d\pmod U\quad \exists c\in\{0,1\},\exists p\in P:
V_{p,c}(d)\text{ has valuation }1.
\]

亦即构成完整 **odd pooled cover**。但 (c,d)=(1,0) 始终是 full-certificate escape。

#### Proof

由于 p∈T regular，ℓ_p=w_pp；squarefree order-closure 使 w_pp|U。q nonregular 使 ℓ_q=w_q|U，所以 L=U。

对给定 d，若某个 p∈T 满足 p∤d，取最小这样的 p。w_p 的全部 odd prime factors 比 p 小且在 T 中，所以它们均整除d。

若 w_p 为奇数，或 d 为偶数，则 w_p|d，取 c=0，局部值为1−5^d。因 s_p=1 且 p∤d，LTE 给 valuation1。

若 w_p 为偶数而 d 为奇数，则 d 是 w_p/2 的奇数倍，故 5^d≡−1 modp。取 c=1，局部值为−1−5^d。应用 5^{2d}−1=(5^d−1)(5^d+1) 及 LTE；第一个因子不被p整除，第二个的 valuation 为 s_p+v_p(d)=1。

若所有 p∈T 都整除d，则 M|d。因为 ord_(q²)(5)=w_q，5^d modulo q² 为1，或在 w_q 偶、d奇时为−1。分别选 c=0 或 c=1，q-row 的局部值都恰为 q modulo q²，valuation1。

这证明 pooled completeness。另一方面，d=0,c=1 时，每个 regular p-row 的局部值为−2；q-row 为q−2，全部 odd-safe，故不是 complete simultaneous certificate。QED。

若 w_q 为偶数，则还可取 d=M，证明 anchor0 全部 odd-safe：regular rows在适当一侧是local zero，另一侧为±2；q-row在anchor0为q+2。因此两 anchors 均非 individually complete，而 pooled union complete，确为 genuinely mixed construction。

**Existence scope：本轮没有提供满足这些 seed hypotheses 的实际 q。** 已验证的三个 nonregular primes分别在free coordinate5、free coordinate653、depth3 at coordinate3处失败。该条件定理不跨级成为已找到 complete actual odd pooled cover。实际 skeleton {3,7,31} 的两个 full escapes只展示regular部分，并未补入一个虚构seed。

## 11. MINIMAL SURVIVING POOLED CLASS

### 11.1 Exact survivor grammar

完整语法在 `DEFINITIONS.md`。其基本对象是 actual arithmetic paired-state atoms与带类型的 provenance cylinders。唯一允许的生成操作是：继承参数的 CRT restriction、真实 slice-cover/frontier witness 的 guard intersection、保留 alternatives 的 OR、consistent state-token conjunction、以及 exact typed maximal-coordinate elimination。

对冻结有限原始系统，这个语法的 EITHER root 为真，当且仅当该系统 pooled complete；BOTH root 为真，当且仅当两个 anchor roots 在同一 global state assignment 下都为真。没有另行引入任意 lower predicate的规则。这是精确 grammar，不是有限 prime-size classification。

### 11.2 Arithmetic survivor filters

在 common-safe boundary 下，任何未被本轮消去的 actual pooled cover 都必须同时满足：

1. **Allocated-blocker failure**：对全部 original rigid rows，不存在使每个 D_p+μ(B_p)<1 的合法 order-factor assignment。
2. **Original pooled frontier witness**：ascending first-stop 在某个真实 odd coordinate 给出满足 P3 的两色前沿；不是拿 derived macro充当 prime。
3. **Configuration consistency**：一个 shared state同时通过所有被使用 fibers 的 guards、valuation compatibility、resultants及positions；不能逐fiber单独选 residue。
4. **Capacity/position gates**：满足式(6.1)，在 coordinate3满足 depth≥5及122/31成本；其他坐标通过相应 exact inventory，不把未知库存视为自动充足。
5. **Recursive typed root**：由 grammar得到 TRUE 的 EITHER root；用于完整证书时，另须满足式(2.1)的反侧 top obligations。

任何 blocker-assignment failure 可在**保留 U 与 dynamic budgets不变**的前提下，抽出 inclusion-minimal failing rigid-resource subset，称为本轮的 minimal blocker-deficient core。此 minimality 仅是明确约束系统中的 inclusion-minimality，不是已找到最小 actual certificate，也不等于删除这些 prime 后 U 不变。

只有一个 nonregular row的最小计数候选类进一步被压到 P4.2：squarefree odd order、所有 odd factors拥有原始 dynamic-capable rows、exact shared residue与global typed contraction保留。P5 给其中order-closed regular-support子类一个条件性正构造，尚未证明存在其 seed。

### 11.3 Requested special-case gates

| Gate | 本轮结果 | Induction 边界 |
|---|---|---|
| 一个 lower odd coordinate | 完整 coloured-prefix criterion；coordinate3且β≤4普遍不可能 | β≥5或其他coordinate仍需实际库存；不能自动induct |
| 所有 β=1 | dynamic active时漏一个digit；rigid row最多给两点；paired configurations exact | P5揭示conditional mixed-cover construction，不能普遍no-go |
| 一个 dynamic + arbitrary rigid | P3给exact frontier grammar，式(6.2)给必要成本 | 下层macro非actualprime，不能复用raw inventory |
| rigid-only pooled | 原始两色prefix frontier + configuration selection；coordinate3至少122个prime | 各row的pair必须全局一致，mass不是充分条件 |
| blocker-deficient core | 从first-digit/free-coordinate升级到full-depth/occupied-coordinate；明确消去1645333507旧边界 | 仍有squarefree、fully-supported或多row weighted-unassignable cores |

## 12. INTERFACE WITH #14

P4 使用 #14 的 original-resource viewpoint、difference-2、joint reverse CRT与escape projection；不是把原 theorem重命名。它新增两个自由度：可以投影到完整 p^e 而非仅 first digit；可以选择已有 dynamic row 的 blocker coordinate，只要 finite shell仍留余量。

因此 #14 明确记录的 q=1645333507 free-coordinate boundary 不再是这个增强 theorem 的边界，即使 prime3与30469139 rows同时存在。其 s=2、order中的3³给出了低负荷投影。

没有修改 #14 既有 record，也没有声称所有 nonregular primes都具有这样一个factor。新 unresolved core变为 weighted/full-depth-unassignable而不只是free-coordinate-unassignable。

## 13. INTERFACE WITH #16

本轮没有直接套 one-anchor Kraft theorem。先由 actual pooled first-stop取得真实两色frontier，再按一个 prime的**完整paired configuration**收费。于是一个 rigid q可支付两片，但每片带anchor与共享state，pooled RHS为1。

新的 R3,4=∅ 是对 #16 六个旧cyclotomic certificates以外的一项补充。它把 applicable pooled rigidity depth推到5，并给122/31 bounds；将 #16 的one-anchor量词保留后也得到243/61。所有结论只对original actual-row fibers有效。

Paired resultant在fixed y,h下过滤double-use资源；它不能使所有 lower assignments共享一个有限prime列表。更高coordinate的macro若投影到3，不会被R3,1–4=∅自动删除。

## 14. DOES THIS ELIMINATE S1 SECOND BRANCH?

```text
Can the pooled-lower branch be eliminated universally? NO.
```

准确含义分三层：

- 未限制two-adic boundary的“任何pooled lower cover都不可能”命题，有本文actual反例，故为假。
- 非平凡 common-safe-boundary / odd pooled class，本轮没有证明普遍不存在，也没有找到一个完整actual odd pooled cover。
- 在全部complete C=1 systems中排除S1第二分支，仍未完成；本轮更没有产生完整双锚点证书。

已经普遍消去的是 P4 满足其明确假设的 subclass，其中包括 nonregular pool contained in {20771,40487,1645333507}。P5的conditional construction还表明：试图证明一个 blanket odd-pooled no-go，需要真正排除相应actual order-closed seed，而不能只用Boolean/两色树的逻辑。

## 15. REMAINING GAP

缺口不是“如何消去一个universal quantifier”：P1/P2已给exact公式。也不是“是否允许local mixed SPLIT”：actual两行样本已允许。更不是“能否把每个macro当成一个新Wieferich资源”：那是错误记账。

剩余具体问题是：一个有限、actual、global shared-state system是否能在每个可用order-factor坐标都阻止 P4 的严格余量分配，同时让其真实两色前沿按上述grammar覆盖整个common-safe lower domain。

在single-nonregular子类，P4.2已排除free-factor与重复odd-order-depth情况。squarefree、fully dynamic-supported的paired core仍在；P5仅在更强regular order-closure假设下给条件性正构造，seed存在性尚未建立。多nonregular情形还需要处理weighted assignment failure与全局configuration integrality，不能由单点resultant或分别one-anchor realization替代。

即使得到complete pooled lower cover，还必须在A0-only/A1-only cells补上式(2.1)的反侧top obligations。这是通向full certificate的另一明确条件；本文没有把它删掉。

## 16. NEXT SINGLE TARGET

**SINGLE-NONREGULAR SQUAREFREE-ORDER POOLED-COVER CLASSIFICATION。**

推荐执行环境：网页端 Pro，负责 theorem/referee 与中等规模 exact reference computation；未到需要普通 Codex integration 或 Ultra 大规模计算的 gate。

冻结一个actual nonregular q及其递归multiplicative-order support DAG，保留全局shared residues与原始dynamic rows，分类regular系统的共同escape在d mod w_q上的投影，问它何时能被该q的一至两个真正rigid logarithm classes全部覆盖。

目标是一个对这个single-q core的必要充分criterion：应包括 P5 的order-closed正构造，并解释不满足其closure条件的fully-supported cases能否被排除。成功输出应是可验证的actual seed/complete odd pooled cover，或覆盖该精确core的无条件no-go；不以扩大prime cutoff替代这个问题。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

### Source key

所有 [S#] 的文件与 Git blob IDs 见 `SOURCE_BINDING.json`，统一绑定 §1 main。

- [S1] Entangled-coordinate formal class与theorem audit。
- [S2] Contraction-tree definitions与theorem audit。
- [S3] Minimal saturated-coordinate definitions、abstract classification、realizability audit。
- [S4] Two-anchor common-residue Phase A report。
- [S5] Prefix-frontier arithmetic realizability Phase A report。
- [S6] Hereditary-shell Phase A report。
- [S7] Two-root provenance Phase A report（#14）。
- [S8] Two-anchor synchronization Phase A report（#15）。
- [S9] Kraft–Hall Phase A report（#16）。
