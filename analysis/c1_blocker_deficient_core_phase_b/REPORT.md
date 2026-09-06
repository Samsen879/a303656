# A303656 C=1 Blocker-Deficient Nonregular Core — Endgame Phase B

## 结论先行

**本轮得到 Theorem D / Promotion Gate C 层级的严格缩减，而不是仅有扫描证据。**
主要新结论是：

> **任何 complete admitted C=1 simultaneous certificate，至少必须包含七条不同的
> original nonregular prime rows。**

该定理不限制 prime 大小、regular support rows 的数量、precision 或 shared residues。
完整证明见 `THEOREM_AUDIT.md` 的 B1、K1、K2；并未证明七条就足够，也未证明下界 sharp。

另外建立了 order-DAG guard release、transitive capacitated Hall、conserved-flow
min-cut，以及 boundary-primed coordinate 3 机制。给定边界 q=1645333507 的直接
singleton Hall 缺额确实存在，但不再是本轮方法的存活障碍。

    UNIVERSAL C=1 NO-GO: NOT PROVED

数学证明由本轮独立写出并自我审计，尚未经过另一个独立研究者或 proof assistant 审核。
本包程序与仓库 implementation 独立；不同检查方法不冒称 independent authors。

## 1. LIVE AUTHORITY

推荐执行环境：网页端 research / reference laboratory。本轮在此环境完成数学推导、
只读 source audit、standalone integer computation；没有转交 repository 写入任务。

    Repository: Samsen879/a303656
    Repository ID: 1333945235
    main SHA: 44e522dd6e88504e2b9829f0b27359e6c45a76ff
    main tree: 6a30565826c8f988bfbb85e4098b78b2992d290c

PR15 merge `76e7b4d447ea2ba9674b2787990dd37551d6844a`，
PR16 merge `25086bb932bbae00692ddf06cce0474aedf1cd7a`，
PR14 merge 即当前 main。逐个 PR 的 merged flag 与 main 的 first-parent chain 均已核对。
要求的三个 directories 均存在。开始和收尾的 live main 读取相同。

STATUS.md、THEOREM_INDEX.md、ROUTE_MAP.md 和九个指定目录的核心数学文本已读取。
精确 reading 清单、blobs 与未覆盖范围见 `SOURCE_READING.md`。没有假称重放了整个仓库
的 tests、历史 prime catalogs 或 CI；container 的直接网络 clone 未成功，实际来源为
GitHub connector 的固定 SHA 读取。

    PRECONDITION: PASS
    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED

## 2. FORMAL BLOCKER GRAPH

沿用原始 admitted row class。令

    Q={q∈P:s_q≥2}, O(q)={odd primes lambda:lambda|ord_q(5)},
    N_P(q)=O(q)\P, c_lambda=(lambda−1)/2.

N_P 是 #14 的 original direct free-blocker graph。不是所有 order factors 都 free：
若 factor 本身在 P 中，尚有它自己的 row obligation。

新对象是沿 actual support DAG 递归到 free terminals 的 F_P(q)。之后利用 boundary
使 actual row3 不活跃，得到 F^3_P(q)：遇到3或缺失的 row label 即停止，其他 admitted
labels 继续下降。采用 selected-anchor capacities h_lambda=lambda−1。

另定义 panel-independent T(q)：T(3)={3}，其余递归至3或1 mod4 prime。
所有 nonregular q 的 T(q) 都非空。不得把这些未实际加入 P 的 descendants 当成新资源；
实际路径走到缺失的 row label 就可以停止。

`DEFINITIONS.md` 逐项重建 w、s、dynamic、rigid、coarse fatal、local zero、U、L、beta、
actual full fiber、provenance macro、original resource、paired forbidden digits 和 Kraft frontier。

## 3. CAPACITATED HALL THEOREM

任意 finite graph、positive integer capacities t 的 maximum matching rank 为

    nu=min_{S⊂Q} (|Q\S|+sum_{lambda∈N(S)}t_lambda).

#14 的原始 theorem 是 direct paired matching 成功就能排除 complete certificate。
本轮不把它重证后列作新主要成果。新增的是：可以先阻断 actual regular relay rows，
再使用它们的 own coordinates 处理更大的 nonregular rows。

因此 `direct matching fails` 只意味着 #14 的最简单分配不可用，不等于方法终止。
新 terminal matching 可成功，甚至 terminal matching 失败时，coalescing guard forest
仍可能成功。三个判据不可混为必要充分等价。

## 4. MINIMAL DEFICIENT CORE STRUCTURE

对 inclusion-minimal deficient S，m=|S|：

    C(N(S))=m−1;
    N(S\{q})=N(S) for every q;
    every deletion has a full matching saturating all right slots;
    deg_S(lambda)≥t_lambda+1.

此外，删除 nonempty proper R⊂S 后丢失的邻域容量至多 |R|−1。
当 m>1 时图连通，所有左邻域非空。这不是“接近饱和”，而是精确的 deletion saturation。
证明见 audit H2。

因此原问题的三类需要修正：factor-closed row 的最小核心只能是 singleton；
有 free factors 的非平凡核心是 collective capacity overload；若 mixed 指把空邻域行
和其他行放在一个最小核心中，则不可能。若 mixed 指同一行同时有 internal 和 free
factors，则并不受此禁止。

Hall 不强迫所有 rows 共有同一 factor。四行 abstract example
{3},{3,5},{5},{5} 已满足所有 minimality identities，却没有共同 neighbor。

## 5. ORDER-DAG ANALYSIS

lambda|w_q|q−1 给 lambda<q。下降图没有环，但“有限下降”本身不能推出 contradiction。
真正新增的两步是 capacity contraction 与 boundary priming。

### 5.1 Arithmetic capacity contraction

对 t_lambda=(lambda−1)/k，k=1或2，

    sum_{lambda∈O(p)}t_lambda
       ≤(p−3)/(2k)<t_p.

原因是不同 odd factors 的 product≤(p−1)/2，而 sum(lambda−1)≤product−1。
于是 matched root paths 穿越 internal row prime 时，不会使该 coordinate 超载。

### 5.2 先使 row3 不活跃

总可选择一个 two-adically safe 的 anchor/boundary，让 row3 在该 anchor 不正整除。
若 r2 even，可让两个 local two-adic values 为(2,0)或(4,2)，再选 row3 不整除的 anchor；
若 r2 odd，某一 anchor 对所有 d 都 two-adically safe，再选择避开 row3 guard 的 parity。
没有 two-adic row 更直接。

这释放了 coordinate3，但只用于选定 anchor，不伪称所有 residues 都有 common-safe
two-anchor boundary。5 则始终 unadmitted，本来就是可能的 free terminal。

### 5.3 对原来的四个问题的回答

A：Hall 和 order DAG 本身不强迫每行有 internal edge。实际 order-labelled {7,31}
有共同 free3 且 paired-deficient，却无 internal edge；不过两行 regular，故这不是
actual nonregular 版本的反例。那个额外 arithmetic assertion 本轮未证明。

B/C：终点可以是3，也可以是 unadmitted prime；3 可经上述 boundary 预先处理。
容量在 internal rows 的传播有严格证明，不再只靠“下降总会结束”的直觉。

D：5和1 mod4 primes 不会成为 admitted dynamic rows；3会，但可预先使其 guard 为假。
这三个情形必须分别处理。

## 6. BOUNDARY RESOURCE 1645333507

独立 deterministic trial-division primality、exact order、lifting 结果：

| actual row p | w_p | s_p | odd support |
|---:|---:|---:|---|
| 1645333507 | 1645333506 | 2 | 3,30469139 |
| 30469139 | 2176367=1429·1523 | 1 | 1429,1523 |
| 1523 | 1522=2·761 | 1 | 761 |
| 3 | 2 | 1 | empty |

所以 q 的 w=2·3^3·30469139，题设数据正确。3和30469139 均为 admitted labels。
但加入它们不等于它们在所有 lower branches 必然 active；residue、lower guard 和 local-zero
条件仍然存在。

更具体地，row3 的 lower guard 只取决于 d mod2，q 使 beta3≥3；row30469139 的
lower guard 是 d modulo1429·1523 的一个 class，q 使它的 own-coordinate beta≥1。
两行都 s=1，guard active 时产生本身的 accepted odd shells，并排除 center；
guard inactive 时没有该动态义务。加入1523又引入 modulo2·761 的 lower guard，
其 own coordinate 则由30469139的 order 支撑。这些 obligation 可以通过阻断 guard
处理，不需要假定其 residues 恰好使某条 branch active。

完整 admitted dependency closure 是

    q → 3
    q → 30469139 → 1523
                  → 1429 [unadmitted terminal]
    1523 → 761 [unadmitted terminal].

1429、761 均 prime≡1 mod4。最短有用 release path 为

    q → 30469139 → 1429.

先用1429使30469139-row不正整除，再用30469139坐标阻断q。若中途 row 不在 P 中，
更可直接把相应 coordinate 当 free terminal。

因此：q 的 original singleton N_P(q)=empty 是真实的，但它不是不可释放的最终障碍。
对只含这一条 nonregular row、任意多 regular support rows 的 panel，已经得到普遍 no-go。
更强地，K2 定理排除任何不超过六条 nonregular rows 的 panel。

一个 frozen actual shared-residue witness：P={3,1523,30469139,q}，K=2，E={1}，
前三行 r=2，r_q=q+2。U=L=2725026504850506222。

    d=1569734815146673626

在两个 anchors 都避开全部 odd fatal rows。row3/anchor0 的 local value 是 exact zero，
按原定义 unresolved；其余七个值不正整除。只计算了这一个 CRT 点，没有枚举 U。
详见 `results/boundary_escape.json`。

q 的 rigid rank 是30469139，不是3。含因子3不自动触发 #16 的 full-3-fiber 税，
也不能把这个 singleton 的1/30469139 rigid mass 叫作 Kraft overload。

## 7. PRIMAL–DUAL FORMULATION

Direct assignment LP 的 dual 为

    min sum alpha_q + sum t_lambda gamma_lambda,
    alpha_q+gamma_lambda≥1 on every allowed edge.

Hall cut 给 canonical binary weights。对 descending order network，加入 actual row
node gates，得到 exact conserved-flow objective

    min_{A⊂P} (|Q\A|+C(O(A)\A)).

容量收缩使 min-cut 可向 admitted descendants 闭合，等于 transitive terminal matching
rank。预先处理3后，对 P\{3} 应用同一公式。

但这不是完整策略 A/B/C 的总最优化：一个 relay guard 被阻断一次后，可服务多个 roots，
所以 coalescing forest 不守恒于 root units。例 P={11,23,67}，三条 mandatory regular
targets 的 paired conserved flow 只有2，但 forest 11→5、23→11、67→11 有效。

准确结论是：得到一个可审计的 min-max 与更强的 forest sufficient criterion；没有证明
Hall dual 与任意 Kraft demands / shared-residue CSP 的全局强对偶。

## 8. INTERFACE WITH KRAFT–HALL

本轮真正使用的桥梁是 **actual relay guard 的 depth-sensitive noncoverage**。
它与 original nonregular rigid-leaf demand 不同，不能交换计数。

沿 pure-{3} 最大因子路径，到3的末端 gateway 必满足 w=3^e或2·3^e。
完整 cyclotomic identities 强制 depth1 只有7、31；depth2只有19、5167。
Pure-{5} 路径同理，depth1只有11、71。因而六条 roots 的 terminal guard costs 有
下列严格上界：

| root 数 n | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 27·F3(n) | 0 | 9 | 18 | 21 | 24 | 25 | 26 |
| 25·F5(n) | 0 | 5 | 10 | 11 | 12 | 13 | 14 |

Mixed-{3,5} roots 每条至多加1/3或1/5，可以按 audit K2 的 allocation lemma 分配，
两端质量都严格小于1。Internal admitted coordinates 至少为7，因此至多六条 incoming
paths 也必留空 digit。这给出 unconditional |Q|≥7 necessary condition。

#16 的 R_(3,1..3)=empty、81个 rigid rows 和 dynamic-allowed 21个 rigid rows 结论仍是
有效依赖，但它们只适用于实际 original full rank3 fiber。本轮没有证明一般 complete
certificate 必有 same-lower joint fiber，也没有把 provenance macros 当新 primes。

## 9. EXACT COMPUTATION

全部非平凡 domain 在运行前写入 `COMPUTATION_SPEC.md`。没有 prime scan、没有 q_max
扩展、没有 boundary full-period enumeration。

| 审计 | frozen domain | 结果 |
|---|---|---|
| arithmetic closure | 固定q与20771、40487 control seeds | exact prime/order/lifting certificates |
| Hall | 左1..5、右3/5/7全部 incidence graphs；paired/single | 74,896 cases，0 mismatches |
| order-DAG | 六个固定 admitted labels、所有 P/T subsets | 1,458 cases，0 mismatches |
| primed3 routes | 同一固定 DAG，3 pre-inactive | 486 cases，全部 passing |
| two-adic/3 boundary | K2=2..9，所有r2和r3 mod3 | 3,060 cases，direct square-sum verification |
| shared digits | q20771单行10385个 powers | 5,192 paired low residues |
| gateway inventory | 六个完整 Phi identities | exact primality/order filters |
| six-root allocation | a+b+k≤6 | 84 cases，严格 rational deficits |
| named regression tests | tests/test_reference.py | 23/23 PASS |
| fresh replay | 九份 deterministic JSON | byte-for-byte identical |

Matching 的 subset-Hall formula 与 slot-augmenting algorithm 是不同算法组织；
它们仍由同一作者在同一 Python 环境实现。Fresh replay 也不是独立作者证明。

Actual digit structure 不能默认 collision savings：q20771 在coordinate5 的 paired
projections 有1038个相同、4154个不同。显式共有residue witnesses：

    r=20777 modq²: logs (1,2176), digits (1,1), both valuation1;
    r=20775 modq²: logs (2176,0), digits (1,0), both valuation1.

这只刻画一个 actual prime 的两个 anchors，不冒充多条互异资源的 collision theorem。

## 10. COUNTEREXAMPLES

本轮保留四个层级，而不是将它们拼成一个虚假的 complete counterexample：

**Abstract graph survivor：** 四行 {3},{3,5},{5},{5} 是 minimal paired deficit。

**Order-realizable survivor：** {7,31} 的真实 orders 支持两行对free3的 overload；
但两行 regular，不能归入 Q。

**Actual nonregular-prime survivor：** q1645333507 的 direct factor-closed singleton；
完整 shared-residue system 也可以构造。它存活原始图，却被 release theorem 排除为
complete-certificate obstruction。

**Potential complete-certificate survivor：** 仅得到必要类 E；没有构造其中满足全部
nonregular inventory / residue / full coverage 条件的实际完整系统。

另外 conserved-flow converse 有 regular-row coalescing 反例，故本包不宣称已穷尽所有
后续 greedy / merged-path strategies。

## 11. STRONGEST PROVED THEOREM

**Six-root guard-routing no-go：|Q|≤6 ⇒ 不存在 complete simultaneous certificate。**

证明不是搜索：B1 先释放3；每个 root 在 strictly descending arithmetic graph 中选择
terminal；pure3/5 的浅层 gateway inventory 提供严格 Kraft-type deficits；mixed roots
可分配；其余 terminals≥13，internal / missing admitted coordinates≥7；每个坐标
至多六条 path 入边。路径合并后使用 actual-row guard escape lemma，直接在 full L
上选择 CRT coordinates，regular rows 在必要时取 local zero。

这条完整链没有 H1 synchronization 假设，也不需要把 derived macro 重新解释为实际素数。

## 12. MINIMAL SURVIVING CLASS

最终采用较强、panel-relative 的必要类：

    E = {finite admitted P :
         |Q|≥7,
         exists nonempty S⊂Q with
         |S|>sum_{lambda∈F^3_P(S)}(lambda−1)}.

由于 N_P(S)⊂F^3_P(S)，E 确实是原 direct paired-deficient panel class 的子类。
已验证边界 singleton 被排除，所以缩减严格。

E 还强迫 absolute terminal graph T 中有某个 minimal circuit，其 m 满足

    m=1+sum_{lambda∈T(S)}(lambda−1), degree(lambda)≥lambda.

最小 signatures 是 m=3:{3}，m=5:{5}，m=7:{3,5}，m=13:{13}；9、11不存在。
这不是说 E 的每个 core 都至少七行：七行下界约束完整 panel 的 nonregular 总数。
Panel-relative minimal core 与 absolute minimal circuit 也未必是同一行集。

没有证明 E 为空、有限、或 arithmetic-realizable；也没有将“稀少”作为结论。

## 13. DOES THIS CLOSE THE BLOCKER-DEFICIENT BRANCH?

**没有全部关闭。**

已关闭：仅靠 q1645333507 factor closure 保留下来的 singleton 方向；所有至多六条
nonregular roots 的 candidate panels；所有通过 transitive boundary-primed Hall 的 panels。

仍未关闭：E 中至少七条 original nonregular rows 的多路径拥堵、可能的终端 prefix
coverage，以及与 shared residues / dynamic obligations 的联合实现。

用户的 literal THEOREM A（不存在任何 admitted deficient core）为假。
THEOREM B 的完整 arithmetic 分类未获得。获得的是 THEOREM D 与 Promotion GATE C，
外加一个新的 unbounded-prime cardinality theorem，而不是只有 GATE D 计算证据。

## 14. REMAINING GAP

需要进一步控制 coalescing guard forests、terminal full primary cylinders 与 actual
nonregular resource inventory。当前流对每个 root 消耗一个 terminal slot，真实 relay
可以合并，因此其 deficit 不是所有策略失败的证据。

另一方面，seven-root 时首次可能出现 admitted coordinate7 的 first-digit capacity
饱和；3端的粗 gateway bound 也可能不再严格小于1。这是本轮证明在7处停止的具体原因，
不是“大素数还没扫够”。不能把这些上界饱和当成存在 actual coverage。

没有证明所有 blocker overload 都迫使相同 P⁺(w_q)，也没有一般 Hall-to-rigid-Kraft
强对偶。Local-mask escape 只排除给定有限 formalism，不是 A303656 表示定理。

## 15. NEXT SINGLE TARGET

**SEVEN-ROOT ARITHMETIC GUARD-FOREST / GATEWAY CLASSIFICATION。**

唯一下一目标：对 |Q|=7，分类在 boundary-primed3之后仍无法改道的实际 guard forests，
同时保留 gateway 的 exact order、depth、original-row identity 和 shared residue。
重点是 coordinate7 的六位容量边界、3/5 terminal 的 exact prefix overlap，以及
合并路径能否系统性打破首次饱和。先证明或给出 actual arithmetic counterexample；
不扩大 prime scan，不把 arbitrary paired masks 作为 actual primes。

## Artifact / reproducibility

见 `README.md`。所有 scripts 仅依赖 Python standard library，固定结果包含九份
可逐字节重放的 JSON。`SHA256SUMS.txt` 保护本包所有其他文件；ZIP checksum 在外侧。
本轮没有创建 Issue、comment、review、branch、commit、PR，也没有 merge 或修改 STATUS。

    UNIVERSAL C=1 NO-GO: NOT PROVED
    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED
    GITHUB WRITES PERFORMED:
    NONE
