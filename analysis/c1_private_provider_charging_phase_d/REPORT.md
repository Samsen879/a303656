# A303656 C=1 PRIVATE-PROVIDER → NONREGULAR-RIGID-ORIGIN CHARGING
## TARGETED PHASE D — 研究与精确 reference 报告

## 0. 本轮结论

**取得 scoped bounded-capacity charging theorem；未取得 arithmetic terminal closure。**

相对读取的 Phase C 栈，本报告给出三个新的推导：

1. **Center-provider ancestry：**每个进入有效 canonical macro 的 original dynamic helper，都有一条由实际中心填补 witnesses 认证的严格递增素数链，终止于该 macro support 内的 original nonregular rigid origin。
2. **Support confinement：**macro 的全部原始 support 限制在其 rigid origins 的实际 dynamic order basins 中；盆地外任意增加 regular 行，不能增加该 macro 的原始 support 供给。
3. **Frozen-shadow width charging：**一个固定状态、固定坐标、共同 lower point 的 minimal simultaneous frontier 中，同一 origin 的 charge 次数至多是其 basin 所有固定 exact shadows 的不交宽度。

但 exactly-seven 的审计结果是：**七个 basin 各有容量 1，恰好对应七个 leaves，欠账为 0。** 首次 essential nonlinear step 已在 3，消去它便可进入 TRUE，不存在必须再付费的下一层 odd recursion。

成果属于 **B 的明确受限版本，并给出 C 类建模障碍**，不属于 A；没有新的 actual 多-provider 完整算术族，也没有推出 N>=8。

完整证明见 `THEOREMS.md`，精确输出见 `results.json`。本文的“证明”指给出可审阅数学推导，不表示独立作者复审、proof assistant 验证或 repository theorem promotion。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 3fb4b4b4f71018017c7ea014ae7a1380f27b6b94
main tree: 5ee6ab9e51f3e6d471991b7407de193d12777882
Head: Merge PR #25 — cumulative-main Hybrid replay repair
Commit time: 2026-09-07T12:39:49Z
End-of-source-reading main recheck: UNCHANGED
```

通过固定 SHA 的 connector reads 确认 nonlinear Phase C、unified Phase B、order-DAG Phase C 均在 current main。六个指定目录的核心数学 reports/definitions/theorems 已读取，另读取 global shared-state Phase C 的相关结果；具体文件与可取得的 Git blob 标识在 `SOURCE_BINDING.json`。

**阅读边界：不是六个目录所有 generated catalogs、每份源码与辅助文件的逐文件全量阅读或重放。** 没有取得本地完整 checkout，没有运行 repository-native tests 或 CI。本文未将历史包内 authority SHA 当成当前 main；所有数学来源均用本轮固定 SHA 读取。计算为本地新写 standalone reference，不导入仓库实现。

推荐执行环境：网页端数学研究与 reference laboratory。本轮未请求 Codex CLI、Codex Ultra 或大型 scan。

## 2. PRIVATE PROVIDER DEFINITIONS

固定 source 的 c*、dynamic-3-inactive parity b、原始 ledger、全部 shared states、U 及其 depths，使用未人工 lower-cell refinement 的 canonical positive cover clauses。[S1–S4]

记 original rigid origins 为 R_0，全部 original nonregular primes 为 Q；一般只有 R_0 subset Q，不把 nonregular dynamic 行算作初始 rigid seed。

一个 parent M 的 private exact provider v 必须是 **original prime row**，并满足

    v in S(M),
    Q_(v,p) = A_M,
    v not in the other simultaneous parents' full supports.

“original regular row / derived macro support member / dynamic helper”不是互斥分类。一条 regular 原始行可以先作为 dynamic helper 进入宏的 support，再以其留下的 logarithm guard 充当 lower exact provider。macro 本身始终不是 provider prime。

还须补上用户四类表中没有单独列出的情形：**original nonregular dynamic row**。它虽然 s>=2，却不是当前 anchor 的 rigid endpoint，追溯不能在这里擅自停止。

Regular provider 的 precision 来自 H_v modulo w_v 的 p-primary 因子，不来自不存在的 regular rigid fatal component。若 Q_(v,p)=C_d(a)，则 v_p(w_v)=d；coarse shell geometry 和当前精度始终从原始合法状态导出。[S1,S2]

## 3. PROVIDER GENEALOGY

对每次 provider occurrence 记录

```text
(parent ID, current coordinate, exact original provider,
 introduction witness for each dynamic token,
 unique parent covering that token's omitted center,
 next exact original provider, endpoint rigid origin,
 all original state tokens and CRT guards)
```

这比 unlabelled order path 或“两个宏共同包含某 root”更强。只靠 co-support 不能伪造 ancestry edge。

从动态 v 的 own-coordinate introduction 出发，中心不能由它自己覆盖。沿唯一 covering rigid parent 的 exact original provider 向上追；在 arithmetic order DAG 的通常方向上，这是把链反向读取。

## 4. REGULAR-PROVIDER ANCESTRY THEOREM

**定理 D1。** 每个有效 nonempty canonical macro 中的 original dynamic token h，都有一条

    h=v_0 < v_1 < ... < v_t=o,
    v_j divides ord_(v_(j+1))(5),

其中全部 tokens 属于该 macro support，终点 o 是 original rigid row，故 s_o>=2。

**证明。** 找到 h 原始 dynamic event 首次进入该 occurrence provenance 的消去节点。其 bundle 遗漏中心；若遗漏的是一个 center cylinder，先固定其中一点。minimal full witness 有一个包含该点的 rigid parent；各 rigid slices 不交，所以该 parent 唯一。这不宣称一个 parent 覆盖整个遗漏 center cylinder。T2 为它提供 exact original row v_1。因为 h divides w_(v_1) divides v_1-1，得到 v_1>h。若 v_1 rigid，则结束；若 dynamic，则在更早的 parent provenance 中重复。素数标签严格递增、原始 ledger 有限，所以必停在 rigid atom。每次都沿 support 内部的真实 witness 前进。证毕。

此定理不需要全局 completeness，但需要可达的 canonical witness，不适用于未经算术认证的裸几何图。它证明 ancestry 存在，**没有证明 ancestry 唯一、没有证明 endpoint 私有，也没有证明 endpoint 尚未被其他义务使用。**

## 5. CHARGING MAP

按固定 row-ID/witness 顺序，在 D1 的候选中心 providers 中作确定选择，可定义

    charge(i) = endpoint of a certified ancestry path for a private provider of i.

若 private provider 自身就是 original rigid row，链长为 0。否则沿动态 introduction 追溯。

“well-defined enough”在这里意味着：对已冻结的 proof receipt 与指定 tie-breaking，输出确定；不意味着存在脱离 proof witness 的天然唯一 root。

后面的容量定理对**任何这样的 certified choice**都成立，不依赖挑到一个最幸运的 matching。

## 6. SIMULTANEOUS VS OR-BRANCH REUSE

本轮的 charge 左侧只计一个相同 p、相同 lower point y、相同 frozen state 的 minimal slice-cover witness 中的 proper rigid parents。

不同 OR witnesses 不累加。不同 lower fibers 即便都需覆盖，也不能直接套用同一单-fiber 容量。不同 anchors 必须保留标签；BOTH 的两个需求不等于 EITHER 的两个替代分支。ancestor 与 descendant obligations 也不是自动需要两份新资源。[S1,S2,S7]

ABSTRACT duplicate ternary 模型有 6 个 original tokens、8 个 TRUE alternatives；每个 token 出现 4 次。正确解释是 8 个可替代证明，而不是 8 份同时消耗。

## 7. NONREGULAR ORIGIN CAPACITY

### 7.1 支持封闭定理

对 original rigid origin o，定义 B(o)：从 o 沿 odd order factors 向下，只加入**当前 anchor/parity 中实际存在且 dynamic 的 original rows**，再递归展开。因为边严格降素数，这是一个有限 active dynamic basin。

**D2：**

    S(M) subset union_(o in R(M)) B(o).

证明是对每个 dynamic support token 应用 D1 再反向读链；rigid token 属于自己的 basin。

令 M_eff 为全部初始 rigid origins 的 B(o) 并集大小。它由实际 root primes 的有限 order closures 控制，不会因盆地外 arbitrarily many regular rows 而增加。在完整固定边界系统中，可 mute 这些外部 dynamic events 而保持 completeness 真值，条件是保留原始 ledger/U/depths：任何 terminal TRUE witness 的 support 本来就不使用它们。

这是 completeness-level pruning，不是 intermediate residual equality，也不是删掉原始行后重新计算 U。结合 Phase C T4，得到每条 provenance path 的

    sum(arity-1) <= M_eff-1.

它比直接使用所有原始行数 M 更集中，但 M_eff 不是仅由 N 决定的常数，仍不能排除 TRUE。

### 7.2 可计算的单-origin 容量

冻结 p 与状态，令

    F_(o,p) = {distinct proper Q_(v,p): v in B(o), p divides w_v}.
    kappa_(o,p) = maximum number of pairwise-disjoint members of F_(o,p).

如果最大 listed depth 为 D，则

    kappa_(o,p) <= min(|F_(o,p)|, p^D) <= |B(o)|.

由于 p-adic cylinders 相交即嵌套，kappa 正好等于 F 内**inclusion-minimal distinct cylinders 的个数**。这是 family 中最细的 cylinders；不能误用计算 union measure 时保留的最浅 cylinders，也不能人工加入 refinement。

**D3：**对一个 minimal simultaneous witness，

    number of parents charged to o <= kappa_(o,p).

证明：T2 使这些 parents 的 exact slices 正好属于 F_(o,p)，且在当前 witness 中两两不交。

另有位置敏感的必要式：分配给 o 的 leaf masses 之和不超过 union F_(o,p) 的精确质量。这不是把每个 helper 的质量简单相加。

## 8. HALL/HYPERGRAPH FORMULATION

左侧是上述一个 witness 的 rigid obligations。边 i→o 要有 exact private original provider 和实际 center-ancestry path；仅有一般 order reachability 不够。

写 Gamma(i) 为所有合法 endpoints，D1 保证非空；D3 推出每个 J subset I 满足

    |J| <= sum_(o in Gamma(J)) kappa_(o,p).

因此一个存在的实际 witness 必然具有这一 capacitated Hall matching。可以保留 (parent,provider,origin,path,state) 超边；provider 在这个 witness 内只能承担一条 private role。

反方向不成立：matching 成功没有恢复精确位置、其他 CRT factors、dynamic-center cover、state compatibility 或宏的实际可达性。来自不同 frozen states/互斥 histories 的 edges 不能合并后冒充一个可实现 witness。[S6,S7]

## 9. EXACTLY-SEVEN CHARGING AUDIT

这里最重要的不是找到“下一轮欠费”，而是先检查下一轮是否存在。

Order-DAG Theorems 7.1–7.2 已给出：exactly seven complete input 在所选边界的 first essential nonlinear step 就是 rank 3；七个 roots 全部保留，frontier 为 (2,2,3)，basins 两两不交，所有 proper admitted descendants 是实际 regular helpers。[S5]

每个 basin 的非平凡固定 3-shadows 都包含它对应的 final leaf，因此彼此嵌套。每个 basin 又有一个 proper head shadow，故

    kappa_(o,3)=1, for all seven o.

每个 private provider 落在唯一 basin，因此确有强的 bijective charging。然而

    obligations = 7,
    total capacity = 7,
    deficit = 0.

几何质量也恰好取等：2/3+2/9+3/27=1。消去完整 3-coordinate 后，没有更低 odd coordinate；固定 parity 的 odd terminal 可以直接 TRUE。**“下一次 nonlinear recursion 必须再要 private provider”在这里没有前提。**

所以本轮没有推出 N>=8。若要排除此情形，须另证 actual basins/state realization 不能实现这个 equality case；charging 本身目前没有给出这个算术矛盾。

## 10. ORDER-DAG INTERFACE

D1 的 ancestry 正是 arithmetic DAG 的反向链；D2 将 descendant geometry 的支持限制到实际动态盆地。一般 basins 可以相交，一般 origin 的不同 helpers 可以引入不同的 lower shadows，所以不默认 injective。

Exactly-seven 的 basin disjointness 确实使每个 provider 的 origin 唯一，但它只给“七对七”，不迫使“八对七”。[S5]

尤其不能把 pure-3 terminal closure 误写成 root 的原始 order 必须是 3^e 或 2*3^e。原始 root 可以先经更大 admitted regular primes 下降。

Order-DAG Theorem 12.1 的七条 prime-order chains 若都能在 nonregular root 终止，就有一份 exactly-seven complete certificate 的条件构造；它与本轮 charging 取等完全兼容。那些 endpoints 仍未实例化，不能把本轮 regular-head 实验称作 actual complete certificate。

## 11. HYBRID RELEASE INTERFACE

若一个 provider tag 的 lower guard 已被同一 compatible ascending prefix 实际破坏，那么含有该 original H_v 的 macro 在对应区域确实失效；这由 T1 直接给出。

但三个命题不同：

    individually releasable provider;
    jointly compatible releases of a family;
    a complete Hybrid escape plan for the whole frozen input.

只有最后一种、并满足 Phase C H 的全部本地 exact-union 条件，才能否定 complete input。不能因某 helper 局部可 release，便把它从所有 simultaneous witness 的 capacity table 删除；也不能把 complete-derived histories 的全局 Hybrid failure 自动赋予 bare E_L。[S2,S6]

本轮没有证明所有 private providers 都属于一个可独立定义的 locally hybrid-unreleasable set。正确必要条件仍是：完整原始系统没有成功的合法全局 Hybrid plan。

## 12. GLOBAL STATE INTERFACE

容量 F_(o,p) 使用一个 fixed state vector，而不是汇总每个 original row 的所有可能 residues。[S7]

同一 root 经不同 helpers 供给角色时，几何来自各 helper 自己的 H_v。它不等同于要求 root 的同一 original rigid log 在多个指定 original fibers 上重复命中。因此 Global Phase C C2–C5 的 ordinary-lower/order/resultant constraints 只能在确实出现相应 original-row demands 时接入，不能给 derived macro 随意代入 original depth。

本轮复核 actual q=20771 的两个 source states：

    r=16:    (b0,b1)=(2177,9772), lower class 7 mod155;
    r=17555: (b0,b1)=(1558,10238), lower class 8 mod155.

四个 local valuations 都为1。第一 state 可合法同时用于 ordinary representatives7与162，因为相差155；不能用同一个 state 同时满足 lower7和8 的这两组强制 paired demands。跨 fiber 不必冲突，但逐 fiber 换状态确实违法。[S7]

## 13. COUNTEREXAMPLES

### 13.1 ABSTRACT：同一 root 支持两个同步 private regular providers

坐标 (x,y,z) in X3×X7×X31。所有状态一次冻结。取

    R: y=0,z=0;
    A_j: x=0,y=0,z=j, j=1,...,30;
    B_i: x=1,y=i,z=0, i=1,...,6;
    C: x=2;
    dynamic7: x=0,y!=0;
    dynamic31: x=1,z!=0.

前38条 rigid atoms 全是 synthetic，不是已认证 nonregular primes；因此整个例子标为 ABSTRACT，不能称为 actual E_L。

31处：R 与30个 A_j 全覆盖，给 x0,y0；dynamic31 分别与 R/B_i 配对，给七条 x1,y=i。7处：dynamic7 配前者给 M0=x0；后面七条 rigid slices 全覆盖给 M1=x1；C=x2 原样保留。

最终3处的 M0,M1,C 是同一个真正 simultaneous minimal frontier。M0 的 private exact provider 可选7，M1 可选31，并且二者均有实际模型中的 center-ancestry path 到 R：7→R 与31→R。此例的 kappa_(R,3)=2。

R 自己的 3-shadow 是 whole，因此 T3 的 LCA 条件并未被违反；区别几何由其两个 helpers 引入。这推翻“任意 ancestry charging 自动容量1”，**不推翻存在另一种 unit-capacity matching**，因为还有其他 roots 可重新分配。

### 13.2 ABSTRACT：global minimal frontier 的单位-root Hall 失败

在 X3×X5×X7，取13个 distinct synthetic rigid atoms：

    C_k: z=k, k=2,...,6;
    A_i: z=0,x=i, i=0,1,2;
    B_j: z=1,y=j, j=0,...,4.

它们形成原始 product 的 exact partition。消去7后得到15个 pairwise-disjoint、全都 indispensable 的宏

    M_ij: x=i,y=j,
    S(M_ij)={A_i,B_j,C_2,...,C_6}.

对整个当前 lower-domain minimal cover，15 obligations 只能连接13 roots，单位-capacity Hall deficit为2。它们不是15个 equivalent TRUE OR alternatives，而是15个不同、全都需要的 product cells。

但是固定 x=i 时，p5 的同一 fiber 只有5个 simultaneous obligations，所以这不是 D3 的反例。精确历史为13→15→3→1(TRUE)。该例直接排除将单-fiber charging 无证明升级成全局 cut 单位注入。

### 13.3 ACTUAL：regular helper 引入 root 自己没有的坐标

P={11,31,67,20771}，c=1，全部 K=2,E={1}，regular residues=4，r20771=20775。精确 orders：

    w11=5, w31=3, w67=22, w20771=10385=5*31*67.

相应 s 为1,1,1,2，U=L=685410。先消去67，再31。在后续11处，support={20771,67,31} 的 parent 以 regular67 为唯一 exact provider，且 center ancestry 为67→20771。

但11不整除 w20771；root 的11-shadow为whole，helper67的11-shadow为C1(0)。这实际认证了“ancestry 不等于 shadow inheritance”。

继续11处线性收缩得到 full exponent guard d=0 mod30，随后在free5处失去覆盖。它不是 complete certificate，没有在单一实际 simultaneous frontier 中造出 one-root multi-role collision。

### 13.4 已明确区分的其他负向控制

ABSTRACT OR duplicates 验证8个 alternatives不收费8次；ABSTRACT one-row three-state模型中每个 fixed state容量1，非法 union-of-states才会变成3。Source actual paired states另用于检验同一 residue 的合法/非法 cross-fiber reuse。没有找到 actual arithmetic 的“一个 regular helper 在同一个 minimal same-fiber witness 内私有服务两个不同 rigid parents”；T2本身排除这种说法。

## 14. EXACT COMPUTATION

程序 `reference.py` 只用 Python standard library、整数、集合、bitsets与 modular powers，不 import repository code，不用浮点作 coverage decisions。beta-one canonical engine 逐 witness 检查 exact coverage/minimality、T1/T2、center ancestry、support confinement、capacity、T4；另一组织方式的直接点集 universal projection 作对照。

| 检查 | 实际范围/结果 |
|---|---|
| Same-origin fork | 40 events；40→10→3→1；两条 private-provider paths 均到R；capacity2 |
| Cartesian minimal cut | 13→15→3→1；global unit-Hall deficit2 |
| Enabled-original subsets | Cartesian例全部8192个 subsets，projection一致 |
| Shadow-width identity | 4096个3-adic depth<=2 families，加32个5-adic depth1 families；最细成员计数=独立packing DP |
| Seeded triangular models | 500个，seed20260907；23个complete；全部检查通过 |
| Basin muting | 同500例，保留ambient和atom metadata，mute外部动态事件；terminal truth全部一致 |
| Actual four-row normal form | 全部685410 exponents×4 rows=2741640 cells，全部一致 |
| Actual paired-state checks | 4个指定 local valuations，均恰为1 |
| Seven regular heads与row3 | 1051305 full-period row checks，全部一致 |
| Conditional seven-root collapse | 54个parity/3^3 classes，全部条件覆盖；未实例化nonregular endpoints |
| Assertion failures | 0 |

最后一项 regular full-period计数包含七个heads的1051299次，再加row3的6次。它不枚举不存在的conditional roots。

所有 seeded dynamic5、synthetic prime labels、abstract geometries 都明确标 ABSTRACT。Reference checks 不是普遍定理证明，也不是独立作者或不同软件栈复现。没有扩大nonregular prime scan，没有重放2e9 inventory，没有执行仓库CI。

## 15. DOES EXACTLY-SEVEN DIE?

```text
NO
```

七个 private roles 可分别落在七个不交 basin，容量恰好取等。first nonlinear rank3之后没有必须出现的下一odd step。没有N>=8结论。

## 16. GENERAL CHARGING THEOREM?

```text
YES — CENTER ANCESTRY + ROOT-BASIN CONFINEMENT
      + FIXED-STATE SINGLE-FRONTIER SHADOW-WIDTH CAPACITY

NO — N-ONLY EXHAUSTION, GLOBAL-CUT UNIT CAPACITY,
     OR TERMINAL-TRUE EXCLUSION
```

这比 Phase C 的 all-original-token accounting 多出了真正的 original rigid-origin endpoint 和可计算 basin capacity，但尚未把这种capacity转为 complete arithmetic input 的矛盾。

## 17. NEXT SINGLE TARGET

**ACTUAL SINGLE-FIBER CENTER-ANCESTRY UNIT-HALL THEOREM / COUNTEREXAMPLE。**

固定一个从actual original ledger和single frozen state可达的、first nonlinear之后的terminal3 minimal witness。让 Gamma(i) 是该private role通过所有合法exact-provider/center-ancestry选择可到达的rigid roots。研究是否必有

    |J| <= |Gamma(J)| for every subset J.

即：虽然任意 charging 可以碰撞，是否总能通过合法改配得到单位容量注入？要求是actual reachable same-fiber witness，不是把global cut、不同states或其他OR alternatives拼接起来。

本轮fork没有否定这个existential statement；13→15反例也不是same-fiber反例。证明它可把“固定basin宽度”进一步压到“可改配的root单位容量”；actual counterexample则会定位真正的state-compatible nonlinear recycling机制。即使证明成功，它也不会单独排除exactly-seven的7=7 equality case。

## 18. FINAL STATUS

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

## Source keys

[S1] Nonlinear Phase C `REPORT.md`, especially T1–T5 and counterexample scopes.
[S2] Unified Phase B `MASTER_THEOREM.md`, `DEFINITIONS.md`.
[S3] Hereditary Phase A `REPORT.md`.
[S4] Contraction-tree Phase A `REPORT.md`, `DEFINITIONS.md`, `THEOREM_AUDIT.md`.
[S5] Order-DAG Phase C `THEOREMS.md`, especially 7.1–7.2 and12.1.
[S6] Hybrid Phase C `REPORT.md`, especially H, temporal records, and global-failure scope.
[S7] Global shared-state Phase C `REPORT.md`, especially C2–C5 and typed demand/state semantics.
[S8] Pinned `STATUS.md` and live main branch metadata.
