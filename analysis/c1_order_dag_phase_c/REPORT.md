# A303656 C=1 EXTREMAL ORDER-DAG — TARGETED PHASE C

## 结论

本轮未证明总 nonregular root 数可以由 7 提高到 8。新的主要结果是：

**恰有七根的完整证书，必须具有 pure-3、七个互不共享 admitted relay 的 regular 子 DAG，以及首次非线性合并的 (2,2,3) ternary frontier。**

另一个新增定理处理 small core + extras：当总根数 N≤12 时，令

    H={q∈Q:T(q)⊆{3,5}}。

完整性迫使 |H|≥7；等号时这七根必须全部 T(q)={3}，并满足上述正常形。
结合仓库已有的 q≤2e9 完整 inventory，可推出：

    完整证书至少需要七个 q>2e9 的 original nonregular primes。

这是新的结构推论，不是 prime-density 外推。另给出一个严格的条件性七根完整证书构造，条件是七个指定 regular heads 上方出现相应 prime-order chains 的 nonregular 顶点；本轮没有实例化这些顶点。

以下新增证明为本轮研究推导，完整英文证明见 THEOREMS.md；尚未经过独立作者审阅或 proof-assistant formalization。

## 1. LIVE AUTHORITY

    Repository: Samsen879/a303656
    Repository ID: 1333945235
    main SHA: 71b8d428b32724c37e593bcfd9d5f06a42e72d21
    main tree: 5609e47eed0c058c190ef59c61644e2fd4b8fad6

PR #17/#20/#18/#19 均确认 merged。结束前重读 main，SHA/tree 未变。实际 merge commits、读取范围和来源见 source_binding.json、SOURCES.md。

五个要求的研究目录通过对应合并 PR 的完整 diff 阅读；关键 current-main 文件又单独按固定 SHA 读取。没有取得完整本地 checkout，没有重跑 repository-native tests，也没有重跑整个 2e9 scan。全部 GitHub 操作只读。

## 2. ORDER-DAG DEFINITIONS

原始 admitted row 的 prime q≡3 mod4，w_q=ord_q(5)，s_q=v_q(5^{w_q}−1)。Q 是原始 s_q≥2 的 distinct primes，不包括 derived macros 或 regular helpers。

对每个 odd p|w_q，定义 q→p。由于 w_q|q−1，所以 p<q。绝对下降展开全部 admitted labels>3，停止于 3 或 λ≡1 mod4（包括5）；终端集合记 T(q)。Panel-primed frontier 则还会在首个未列入 panel 的 admitted row 停止。

用已有 boundary lemma 固定同一个 c_*，再选使 dynamic 3 inactive 的 parity b。完整证书在此固定 (c_*,b) 必须 odd-complete。这不是要求两个 anchors 同时逃逸，也不把 pooled EITHER 改成 BOTH。

## 3. RECONSTRUCTED TERMINAL-HALL CONDITION

在固定 anchor 下每个终端 λ 有 λ−1 slots。已有 transitive guard theorem 通过实际 row coalescing 构造 release forest；不是每条 origin path 都新增一个 relay row。

如果全部 subsets S 都满足 |S|≤Σ_{λ∈T(S)}(λ−1)，则存在充分的 release assignment，从而逃逸。完整证书必须违反这个 Hall 条件；反向不成立。

对于 inclusion-minimal deficient S，令 m=|S|、C=Σ(λ−1)。删除任意 q 后有

    m−1≤C(T(S\{q}))≤C(T(S))<m，

因此 m=C+1。若终端 λ 有 d<m 个邻根，删去这 d 个根后，以剩余 terminal capacity 上界得到 d≥λ；d=m 时同样由 m≥λ 得到结论。因此

    |S|=1+Σ_{λ∈T(S)}(λ−1)，deg_S(λ)≥λ。

最小签名：3根 {3}；5根 {5}；7根 {3,5}；13根 {13}；15根 {3,13}；17根 {5,13} 或 {17}；19根 {3,5,13} 或 {3,17}。9、11 不对应这种最小 absolute-terminal circuit。

七个 pure-3 roots 中任意三根已经是 minimal deficient circuit，共35个。因此绝不能把七根总规模当成 minimal S 的规模。

## 4. P4-FAILURE CONDITION

冻结全体实际 row states、ambient U 和 dynamic components。把每个 rigid root 分配到一个 p|w_q，取完整 p^{v_p(w_q)} logarithm projection 的精确并集 B_p。若所有坐标满足

    D_p+μ(B_p)<1，

则 P4 构造 escape。完整性只意味着每个 allocation 至少一个坐标失败；失败不是 exact coverage。

本轮多根扩展：若 S 是 inclusion-minimal P4-nonallocatable rigid set，删除 q 后某成功 allocation 的 slack 为 δ_p=1−D_p−μ(B_p)，那么 q 的每个 option 都满足

    δ_p≤μ(C_{q,p}\B_p)≤t_{q,p}/p^{v_p(w_q)}，t_{q,p}≤2。

否则可把 q 加回该坐标并继续成功。这替代了错误的“每个深度≥2的根都可单独处理，所以全体也可处理”。一般 multi-root failure 不迫使所有 odd orders squarefree。

选择实际 release rows R，令 F_p 为其正 divisibility guards 的精确 projection 并集，其他 rigid events 分配为 B_p，则

    1_{p∉R}D_p+μ(F_p∪B_p)<1（每个p）

是新的联合充分策略：r∈R 在 b(r)<r 处已真正被禁用，才可省掉自己坐标的 dynamic hazard。该模型覆盖 selected-anchor P4 与 transitive release，但不声称一般 exact flow/min-cut 对偶。只有明确选定 depth/component upper bounds 的 slot relaxation 才具有普通 capacitated Hall 判据。

## 5. EXACTLY-SEVEN-ROOT CLASSIFICATION

### 新引理：cross-strip

一个 linearly descended seed 剩余只依赖3、5，且3-depth≤1、5-depth=1。令 A3 为 helpers7、31的固定 first3-cylinders 并集，A5 为11、71的固定 first5-cylinders 并集。则该 seed 包含于

    (A3×X5)∪(X3×A5)。

取最小实际 helper，它的 order odd part 只能是3、5、15。前两类给上述 pure heads；而

    Φ15(5)=181·1741，Φ30(5)=61·7621，

四个素因子全部1 mod4，没有 admitted mixed head。注意结论是两组固定 strips 的并集，不是“所有 mixed seeds 不存在”。

### 排除 p=5

设 top seeds n、lower seeds k，n+k≤7。五进满前沿在此规模只能是五个 first-level cylinders。n=5/6/7 时全部 minimal cover alternatives 数量最多1/2/4；加入 k 后，full exact residual 最多3/3/4个 proper3-cylinders。

这些 residual 都不能为常量，否则五个 constituents 全部3-free，只能落在11、71的两个固定5-branches，不可能覆盖五个 branches。

≤4个 proper3-cylinders 的完整并集必须包含全部三个 first3-branches。选 A3 之外的 branch B。它既不能由 retained lower seed 直接给出，也不能由 macro 给出：后一种情形要求五个 constituents 的 lower guards 都是 unrestricted 或 B，cross-strip 随即把它们全部限制在 A5 的两个5-branches。矛盾。

### 排除 p=7

首个 nonlinear witness 必须用尽全部七个 seeds。设 G 为全部 lower guards 的交。所有 nonlinear clauses 的 guard 都是 G 或 G∩H7。若无 simple pair，exact residual 至多一个 proper clause；其不能为常量，因为 pure7-depth1唯一 admitted regular gateway 是19531，只给一个固定 first7-branch。

若有 simple pair，essential nonlinear witness 必须在 dynamic7 inactive 时发生，所以七个 rigid cylinders 自己覆盖全7-fiber，必为七个不同 first branches，centered first cylinder 唯一。完整 residual 包含于该 simple-pair clause 与 G 两个 proper lower CRT cylinders，每个测度≤1/3；lower dynamic3 inactive、没有dynamic5，因此不完整。这里没有遗漏其他 nonlinear alternatives。

### 剩下的唯一首个 nonlinear rank

只能 p=3。已有浅 gateway 容量2/3+2/9=8/9迫使某叶 depth≥3；七叶 ternary depth tax 又迫使 depth≤3，因而唯一 profile 为 (2,2,3)。

    depth1：7、31，两者都必须出现；
    depth2：19、5167，两者都必须出现；
    depth3：{163,271,487,4159,31051,16018507} 中三个不同 heads。

这只给20种 deepest-head combinations，不是20种全部 arithmetic DAG。

## 6. STRONGEST NEW NECESSARY CONDITION

七根完整证书除上述前沿，还必须满足：

- 每个 q 的 T(q)={3}；全部 proper admitted descendants 都是 panel 中实际 active dynamic helpers。
- 这些 helpers 全部 regular；七个 admitted basins 在终端3之外两两不交，Q 为 order-reachability antichain。
- 叶深 d=1,1,2,2,3,3,3 的 basin 内所有实际 x 满足 v3(w_x)≤d，且每个 odd p>3 有 v_p(w_x)≤1。每个 helper 必须接受 valuation1；每步 incoming cylinder 必须位于该 helper 固定 dynamic center。
- 实际 row3 必须存在，并在 c_* 的另一个 parity 有非空 dynamic component。

关键论证：linear lineage 会继承所有 order factors，不能只追踪一条方便路径。要把任何 p>3 消去，必须经过实际 centered depth-one helper。全部七个 nonregular rows 已在 c_* rigid，不能再充当 dynamic helpers。若两个 roots 共享 admitted descendant，就共享某个最终3-gateway；其固定3-cylinder 必包含两片互不相交的七叶前沿，与上述完整 shallow gateway inventory 冲突。

这些是对 ord_x(5) 的限制，不是对 x−1 全部分解的限制。T(q)={3} 不意味着 w_q=3^e 或2·3^e，甚至不意味着3直接整除 w_q。

## 7. SMALL DEFICIENT CORE + EXTRA ROOT ANALYSIS

当 N≤12，所有 p≥13 都大于当前 seed 数。因此 sparse lemma 保证这些坐标的 exact saturation 恰好等于 linear saturation。下降消去它们，保持 completeness、来源唯一性与 frozen U。

每个 E=Q\H 的 root 都有绝对 terminal λ≥13。任何保留下来的 lineage 都必须继承这条路径；到 free λ 时没有 dynamic row可供 linear contraction，所以该来源必在13以上消失。缺失或inactive relay只会让它更早消失。

因此13以下最多剩 |H| 个来源。已有六来源障碍排除 |H|≤6；若 |H|=7，上述 p5/p7 排除与七叶正常形迫使全部 pure3。

这给出了真正的 small-core-plus-easy-extras 定理：例如3根 {3} deficient circuit 加若干全都可到达≥13终端的 roots，若总根数≤12，仍然无法 complete。不是把“准备 release”直接记作已删除。

## 8. TERMINAL SIGNATURE ARITHMETIC REALIZABILITY

本轮复核三个实际 nonregular roots 的完整 terminal closures：

| q | w_q | T(q) |
|---|---|---|
|20771|5·31·67|{3,5}|
|40487|2·31·653|{3,653}|
|1645333507|2·3³·30469139|{3,761,1429}|

后者经过 ord_30469139(5)=1429·1523、ord_1523(5)=2·761。所有实际中间 admitted relays 的素性、order 和 regularity 均复算。

所以 {3,5} 对单个 nonregular root 的算术可实现性早已为真；它不等于七根 complete panel 可实现性。新的七根正常形没有被这三个实例实现。

## 9. SHALLOW GATEWAY ANALYSIS

全部 gateway 采用完整 cyclotomic products 加素性、exact order 和 lifting 认证，而非范围扫描。固定 head 只有一个 frozen logarithm guard，多个 origins 不能各自重新选择它的位置。

R_(3,1..4)=empty 被定向复核：Φ3、Φ6、Φ9、Φ18、Φ27、Φ54、Φ81、Φ162 在相关 primitive factors 上均无 nonregular square factor。

它只排除原始 rank3 rigid resources 的这些 depths。若一个原始 rank3 nonregular leaf 被 essential 地用于 rigid-only ternary frontier，则其 depth≥5，几何 depth tax 给至少11个 leaves；这不是向任意重复引用的 nonlinear macro 收11个新 primes。

混合 shallow 排除也有明确边界：Φ45(5)=1171·169831·297315901，其中1171、169831 是实际 admitted regular order45 gateways。因而没有理由从15/30的空集合推广到全部 mixed depths。

## 10. CYCLOTOMIC / NONREGULAR ATTACK

对 actual q，w=ord_q(5) 与q互素，q只出现在5^w−1的 primitive factor Φ_w(5)中。因此

    v_q(Φ_w(5))=s_q，nonregular ⇔ q²|Φ_w(5)。

本轮把若干 shallow 首次非线性方案转成了可闭合的有限 w-family：3/6、9/18、27/54、5/10、7/14、15/30 等，完成了所需分解与认证。

但是 pure3 terminal basin 可以任意高；其 root order 可以包含比3大得多的 admitted factors。没有证明所有候选 w 都落入某个有限列表，也没有证明这些 Φ_w(5) 全部无平方因子。

## 11. 条件性七根 complete construction

固定 heads {31,7,19,5167,271,4159,31051}。假设每个 h 都存在实际 admitted chain

    h=p0<p1<...<pk=q_h，ord_{p_i}(5)=p_{i−1}，
    中间 p_i regular，末端 q_h nonregular。

则可以构造 exactly-seven-root complete C=1 certificate，而不仅是 pooled cover。

所有 odd rows K=2、E={1}。在 c=1，中间 rows取 r_p=4，顶端取 r_q=q+4 modq²。链逐层覆盖 d=0 modh。用每个 head 的一次固定 residue把自己的中心设为0，并把 lower guards设为：

    31:0 mod3；7:4 mod6；19:2 mod9；5167:14 mod18；
    271:8 mod27；4159:17 mod27；31051:26 mod27。

偶数 d 被 (2,2,3) 前沿覆盖。奇数 d 中，row3取 r3=2 mod9，覆盖所有 d不整除3 的奇数；其余奇数由31-chain覆盖。最后 two-adic r2=1 mod4 使 c=0 对所有 d 都 fatal。所有 row residues 用 CRT 合成同一个 global state；全部 regular own-coordinate digits 都由父 order 支持，因此 U=L。

**这是一条以实际 chain 存在为前提的定理；本轮没有找到七个末端 q_h，没有构造实际完整证书。** 实验只检验实际 regular heads 与明确标记为 conditional 的上游覆盖。

Φ_p(5)≡3 mod4、Φ_p(5)≡1 modp 确保从任何 admitted p 都能往上找到 exact order p 的 admitted prime，故实际 order chains 可以任意长；这完全不保证途中出现 q²|Φ_p(5)。primitive divisor 与 primitive square divisor 是不同条件。

## 12. TARGETED EXACT COMPUTATION

| 检查 | 实际范围/结果 |
|---|---|
| recursive full n−1 Lucas primality certificates | 93，PASS |
| selected cyclotomic values | 20，精确乘法/order/lifting 检查 PASS |
| 三个已知 nonregular roots 的完整 absolute DAG | PASS |
| 七根 terminal 图，每根取 {3}/{5}/{3,5} | 3^7=2187，minimal circuits 检查 PASS |
| p-ary depth profiles / five-branch witness counts | ≤12 leaves，PASS |
| conditional construction 的实际 regular rows | 1,051,299 full-period comparisons，0 mismatches |
| conditional collapsed parity×3³ classes | 54，全部覆盖；非实例化 actual roots |
| regression tests | 10，PASS |

Discovery 使用 SymPy，最终素性不依赖 probable-prime 宣称；reference.py 标准库实现逐层认证完整 n−1 factorization 和 Lucas orders，并拒绝故意破坏的证书。未扩大 prime scan。

## 13. CAN >=7 BE IMPROVED? / NEW LOWER BOUND

**NO：本轮没有证明总根数下界提高到8，也没有证明7是 sharp。**

尝试8至12时，p5的 alternative cover 数在8来源时已经可达8，残余可出现七叶深3前沿；9来源允许五进 depth2 frontier；11来源又容许 p11 首次非线性。以下只列尚未排除的必要 witness sizes，不表示实例存在：

| N | p=3 的r | p=5 的r | p=7 的r | p=11 的r |
|---|---|---|---|---|
|7|7|已排除|已排除|—|
|8|7|5|7|—|
|9–10|7,9|5,9|7|—|
|11–12|7,9,11|5,9|7|11|

每个 N≤12 都还必须满足第7节的 H dichotomy。没有据此宣称≥8/9/10/11/12/13。

## 14. IMPLICATION WITH 2e9 INVENTORY

有新的无条件结构加 bounded-inventory 推论：至少七个 original nonregular primes 必须 >2e9。

证明：若 N≥13，已有 inventory直接给N−3≥10。若N≤12，H至少7。H=7时全部pure3，不可能是已知三根；H≥8时已知三根至多20771属于H，故至少7个H根在界外。

总根数下界仍7；若panel包含已知三根中的κ根，则N≥7+κ。包含三根全体时至少10，但这不是对全部panels的无条件≥10。

## 15. NEXT SINGLE TARGET

定义 B7 为：T(q)={3} 的 actual nonregular root，全部 proper admitted descendant closure regular，唯一最终3-gateway为7，整个 basin 的 order 在3以上 squarefree、3-depth至多1。

**证明 B7 为空，或给出一个完整认证的实际成员。**

七根完整证书必包含 B7 成员。若证明空，则总下界升到8；找到成员则实现一个必需 arithmetic basin，但仍不是完整证书。只检查从7出发的 prime-order chains 不足以排除完整 B7，因为它还允许 branching orders。

    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED

    GITHUB WRITES PERFORMED:
    NONE
