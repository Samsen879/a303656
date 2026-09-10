# A303656 C=1 — Certificate-specific different-prime replacement, Phase G

## 0. 判决

**成功等级 C，严格限定为下文显式定义的 structural/order/provenance/typed-mask reduct。**

找到一个带七个形式 original nonregular origins、真实 regular 骨架、固定共同状态、完整 BOTH 覆盖语义的有限反模型。它有 cost 4 的 B7 exact state，却没有另一个可供替换的 original B7 origin。因而，**不能只从本轮核对的现有组合、祖源、容量、共享状态约束推出 different-prime SQD**。

还证明一个比抽象反模型更直接的条件性结论：在任何实际 exactly-seven complete certificate 中，B7 original origin 恰有一个。另一个原根在任何 good B7 exact state 上都不可能有 square hit；不限于 cheaper states。这是从已合并 normal form 与 exact-state iff 推出的定理，不以找到实际七根证书为前提。

**没有找到实际七根算术证书，没有找到实际 B7 square hit，没有反驳允许从证书外产生新实际素数的算术 SQD。** 七个形式端点没有被验证为素数，更没有验证它们的 base-5 lifting congruences。

```text
THEOREM: NOT PROVED                 # requested strict different-prime SQD
ABSTRACT COUNTERMODEL: FOUND        # the explicit structural reduct only
ACTUAL ARITHMETIC COUNTEREXAMPLE: NOT FOUND
ROUTE STATUS: DEAD AT CURRENT AUTHORITY
GITHUB WRITES PERFORMED: NONE
```

这里 DEAD 只指“继续用同一套结构/状态机制推出新根存在性”这一路线，不指所有 arithmetic replacement theorem。

## 1. Live authority 与阅读边界

```text
Repository: Samsen879/a303656
main SHA: c6ca0dc061783ab993be6fa077c8f66cd730e28c
main tree: 57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06
Head: Merge PR #37, four-vertex B7 Phase F
PR #26, #30, #32, #35: merged=true, individually checked
Final live-main recheck: UNCHANGED
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

逐段读取本结论依赖的 Order-DAG、Branching、Provider 完整 THEOREMS，以及 Closed-State SQD、Seven-Basin 的数学证明；核对 F 的 `DEPENDENCY_BINDING.json`，不把 F producer 当时缺失 E 源码的旧记录误当作当前 integration 仍未对接。来源见 `SOURCE_BINDING.json`、`SOURCES.md`。

**未完成五个目录所有辅助代码、历史材料和生成数据的逐文件通读；没有完整本地 checkout，没有重放 repository-native tests、所有历史大整数证书或 2e9 inventory。** 这是任务执行的明确未完成项，不声称“所有目录全量读完/全量复现”。本包只对明确列出的新有限模型与实际 regular 算术证据作 standalone replay。Git blob 标识来自 connector metadata，未伪称从本地完整源文件重新算出。

## 2. 先修正量词和 stopping rule

固定

\[
 c(R)=|R|,\qquad |D(q)|=1+c(R).
\]

本包检验有内容的 three-vertex reduction 版本：当 `c(R)>2` 时，要求存在 cheaper B7 square hit。反模型使用 `c(R)=4`，不是一个恰好位于 cost-two stop 的无效例子。

若“非最小”被定义成“并非现有 B7 hit 的最小成本”，那么存在更便宜 hit 只是定义重述，不能说明最小成本为 2。若完全不设停止类，对每个 hit 都要求 strict descent，则任何非空 well-founded hit 集合都立即矛盾。这些版本不能混称为一个可迭代算法。

题目的候选来源必须进一步区分：

- **In-certificate:** q' 是同一证书的另外六个 original nonregular primes 中之一，或其原始支持内可追溯的 actual nonregular row。
- **External arithmetic:** q' 是证书外另一个实际 nonregular prime，必须另有存在性证明，并在替换后重新验证 complete certificate。

第一个版本的来源集合被 G1 完全排除。第二个版本不是本轮被反驳的算术命题。其他类型 basin 可以有更少的顶点，但因为它们不是 B7，不能作为 `q'²|Z_T` 中 good B7 state T 的候选。

## 3. G1：唯一 B7 original origin

设 C 是 hypothetical actual exactly-seven complete certificate，原根集合为 Q(C)。令其 7-headed B7 root 为 q，exact state 为 R。

已合并 Order-DAG Theorem 7.2 给出不同原根的完整 admitted descendant basins 两两不交，proper descendants 全 regular。[S2] 已合并 E3.1/F4 给出

\[
 q'\equiv3\pmod4,\quad q'^2\mid Z_T
 \iff q'\in\mathcal B_7,\ D(q')\setminus\{q'\}=T.
\]

若 `q' in Q(C)\{q}` 满足左侧，则 7 同时属于 D(q') 和 D(q)，与 disjointness 矛盾。若 q'=q，则 distinct-state coprimality 排除一切 T≠R。[S3,S4]

因此

\[
\boxed{\{(q',T):q'\in Q(C),\ T\text{ good B7},\ q'^2\mid Z_T\}
       =\{(q,R)\}.}
\]

这不仅是“没有更便宜的另外一个原根”，而是“另外六个原根根本不在任何 B7 exact stratum”。同一盆地的后继也不能补位，因为它们全 regular。Derived macro 不是 original prime。Provider ancestry 的作用是返回已有 origin，不是生成第八个素数。[S5]

**逻辑限定：** 此条件性排除定理没有给出实际高成本 C；故不把原算术蕴含式宣称为已有实际反例。它可能因高成本 antecedent 不存在而 vacuously true。

## 4. 有限反模型

### 4.1 实际 regular 骨架与形式端点

| basin ID | head | depth | leaf λ mod 3^e | 实际 regular 集 R_i | 形式 root order |
|---|---:|---:|---:|---|---:|
| O31 | 31 | 1 | 0 | 31, 878851, 625552508473588471 | 878851 × 625552508473588471 |
| B7 | 7 | 1 | 1 | 7, 43, 127, 6717031 | 6717031 |
| H19 | 19 | 2 | 2 | 19, 191, 6271 | 191 × 6271 |
| H5167 | 5167 | 2 | 5 | 5167 | 5167 |
| H271 | 271 | 3 | 8 | 271 | 271 |
| H4159 | 4159 | 3 | 17 | 4159 | 4159 |
| H31051 | 31051 | 3 | 26 | 31051 | 31051 |

所有表中 regular 数字的素性、base-5 exact order 和 s=1 均由本包实际验证；共 14 条 regular core rows。七个 Q_i 则是 **FORMAL_ORIGINAL_NONREGULAR_ORIGIN**，没有实际素数值。它们只在抽象模型中具有非正则颜色、唯一 order 标签和 rigid-atom 行为。

尤其 B7 骨架是真实 regular diamond：

\[
6717031\to\{43,127\},\quad43\to\{7,3\},\quad127\to\{7,3\},\quad7\to3.
\]

`ord_6717031(5)=43*127=5461`；6717031 本身不是 nonregular root。[S3] 形式 Q_B7 位于其上，声明 order=6717031。

\[
R=\{7,43,127,6717031\},\quad A(R)=\{6717031\},\quad c(R)=4,\quad|J(R)|=32.
\]

`Z_R` 的表达式为

\[
Z_R=\Phi_{6717031}(5^{229362})/6717031.
\]

**本包没有计算或分解此巨大整数，也没有证明 Q_B7² 整除它。** 抽象关系使用 `Hit_hat(Q_B7,R)`；不能删掉 hat 后称为数论事实。

O31 骨架 orders 分别为 3、93、31，其形式 root order 也为奇数，所以它保留 all-odd 31 条件。选择实际 first relays 而不是直接在 31 上方伪装一个已知被 first-relay 定理排除的 nonregular terminal。[S7]

### 4.2 一份状态，不是逐叶挑选状态

各 basin 一次选定 a_i：

\[
a_i\equiv0\pmod2,\quad a_i\equiv\lambda_i\pmod{3^{e_i}},\quad
 a_i\equiv0\pmod p\ (p\in R_i).
\]

所有实际 regular rows 使用 `K=2,E={1}` 和

\[
r_p=3+5^{a_i}\pmod{p^2}.
\]

形式端点固定同一个表达式 `r_Q=Q+4 mod Q²`；其选定 anchor 的 formal rigid guard 为 `d=0 mod w_Q`。没有同一 row 的多个 local state。若端点的 actual prime/order/lifting gate 成立，这个 formal guard 恰是该固定 residue 的实际 guard；本轮没有验证该 antecedent。

实际 row3 固定 `r3=2 mod9`，two-adic row 固定 `r2=1 mod4`。实际 regular subledger 的单个 CRT residue 在 model.json 中数值给出；加入七个 Q_i 后的 full CRT residue **仍是未实例化的符号式**。

完整模型保持同一个 exponent period

\[
L=U=54\prod_{p\in\bigcup_i R_i}p
\]

及同一状态，逐一检验 54 个 separator cells。每个 private p-digit 的 `0 / 非0` quotient 是精确的，因为所有 own centers 和 >3 的 lower log digits 都是 0，且相关 orders 在 >3 上 squarefree。该压缩不是随机采样 p-digits。

在 A1：偶数 parity 由七叶完整划分覆盖，奇数且 3∤d 由 row3 覆盖，奇数且 3|d 由 O31 basin 覆盖。在 A0：two-adic row 对所有 d 给 local class 3 mod4。因此检验的是 **BOTH**，不是 pooled EITHER。

未知 Q_i 的额外 A0 fatal behavior 不需要、也没有被任意选成 false；报告使用已保证的 A0 two-adic lower bound。这与源 E5 的构造量词一致。[S6]

### 4.3 Ancestry、confinement 与 simultaneous capacity

程序按降序消去每个 basin 的 regular coordinates。每一步记录唯一当前 linear rigid parent、真实原始行 exact provider、omitted center、完整原始 support、固定 lower guard 和 center-ancestry path。它不是由 co-support 猜出来的裸路径。

例如 B7 的一个合法 receipt 为

```text
eliminate 6717031: provider Q_B7
eliminate 127:     provider p6717031
eliminate 43:      provider p6717031
eliminate 7:      provider p43  (fixed tie-breaking)
final 3-provider: p7
```

这里 p6717031 在不同消去阶段出现，不按同一 frontier 的两份消费计费。最终七个 3-leaf parents 的 supports 完全不交，各自 private head provider 追溯到自己的唯一 original origin。

每个 basin 所有非平凡固定 3-shadows 嵌套，故 κ=1。七个 mandatory leaves 在同一状态下得到真实的抽象 full cover，但

\[
7\text{ obligations}=7\text{ capacities},\quad\mathrm{deficit}=0.
\]

这不是凭空假设 Hall matching 足够；已额外给出完整 linear receipt 与全局 cover 检验。[S5]

### 4.4 Exact-state 与 coprimality guard

有限 registry 使用八个已认证 B7-compatible regular labels：

```text
7, 43, 127, 379, 7603, 19531, 519499, 6717031.
```

其全部 good closed substates 有 80 个；J-strata 共 1020 个互不碰撞的 exact indices；其中 22 个 state 比 cost 4 更便宜。这里只是该有限 label registry 的穷尽，不是无界实际 low-cost states 的穷尽。

所有表示出来的 primitive prime atoms 只能归属其唯一 exact-order closure；实际 regular atoms 的 valuation 为 1，唯一 formal B7 atom 的 valuation 标记为 2。不同 state 不共享同一 prime atom，包括一次整除层面。故没有 same-q migration，也不利用 normalizer 制造 spurious square hit。

“不存在更便宜的证书内原根”并不依赖这个有限 registry 的搜索上界：另外六个原根的完整 closure 都不含 7，G1 的集合论证明排除它们在任何 B7 state 上成为候选。

## 5. Minimality 不会自动救活下降

本模型的 21 条 core original rows（14 regular + 7 formal origins）全部是 fixed-state deletion-indispensable。删除任一行后，程序给出共同 exponent d mod **原始** L，使 A1 所有其余行安全。没有删除行后重算 period。

因此它甚至满足“没有冗余 regular helper”。所有 maximal generators 都必不可少；每条 private helper ancestry 的终点也唯一。这些较弱 structural minimality 条件依然允许 cost 4，不提供新的 cost upper bound。

这不是 global minimum over actual complete certificates 的算术证明。它只排除把 inclusion/deletion minimality 偷换成 three-vertex bound 的办法。

## 6. G3：外部实际根的移植，以及真正缺失的量词

另外得到一个条件性 interface lemma：固定一个实际 exactly-seven certificate 的另外六个 arithmetic basins；若**独立获得**任何 actual B7 root q*，则其整个 basin 自动与那六个 basins 不交。因为它的每个顶点都下降到 7；任何交点都会迫使另一个 basin 包含 7，矛盾。

O31 basin 不变，所以源 E5 可为替换后的七个实际 basins 重新构造 **ONE** global state，选 `K=2,E={1}` 得到完整 certificate。[S6] 这解决“有外部实际根以后能否继续留在 certificate-derived domain”的接口，但不保留原 frozen residue vector，也不产生 q*。

在真实非空 certificate 集合上最小化 total regular helper count 是 well-founded 的；若已有 cheaper actual B7 q*，上述移植会严格减少此数。故一个 minimum-helper complete certificate 的 B7 cost 等于 actual B7 类的全局最小 cost。然而不能从这里推出该 minimum 是 2。

所以本轮清楚拆开了两件事：

\[
\text{new actual square-hit existence}\quad\neq\quad
\text{conditional global certificate gluing}.
\]

后一件已有条件性解法；前一件仍没有证明。继续以 ancestry/7=7/CRT 代替前一件，应停止。

## 7. Replay 与审计结果

| 检验 | 结果 |
|---|---:|
| 递归 full-(n−1) Lucas 素性证书节点 | 33 |
| actual base-5 exact-order / regularity certificates | 21 |
| actual regular modular row comparisons | 6480 |
| formal endpoint 的 congruence-guard comparisons | 2160 |
| 精确 private quotient cases | 2160 |
| ONE-state separator cells，通过 BOTH | 54 |
| fixed-state core row deletion witnesses | 21 |
| 负向语义/数据篡改 controls，全部拒绝 | 12 |
| actual nonregular endpoint prime/lifting checks | **0** |

Verifier 仅使用 Python 标准库，不联网、不导入仓库代码、不运行 factor search。新输入构建阶段仅对固定 regular labels 作小型 exact arithmetic；没有大 computation。生成、证明、自审与验证来自同一会话，不宣称 independent author 或 fully independent software stacks。

## 8. 交付与 nonclaims

`MODEL.md` 冻结精确形式语言和被省略的 arithmetic-realization 公理；`PROOFS.md` 给出 G1、反模型和 G3 的完整论证；`model.json`、`arithmetic_certificates.json` 是输入；`finite_model_data.json`、`results.json` 是可重算输出。

```text
DIFFERENT-PRIME SQD (actual arithmetic): UNRESOLVED
B7 EMPTY: NO
EXACTLY-SEVEN: NOT KILLED
N>=8: NOT PROVED
A303656: UNRESOLVED
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
GITHUB WRITES PERFORMED: NONE
```

**路线裁剪结果：DEAD AT CURRENT AUTHORITY，只针对本轮显式检验的结构性推出方式。** 本包不应被集成为 arithmetic counterexample、一般 B7 emptiness theorem 或 N>=8 theorem。
