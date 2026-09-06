# A303656 C=1 Unified Endgame — Phase B

## 本轮结论

本轮得到一个**无 prime-size cutoff、无 precision cutoff 的必要临界类归约**，以及其直接推论：

> **任何 complete finite admitted simultaneous C=1 certificate，至少含有 7 个不同的 original nonregular primes。**

更强的结构结论是：完整证书可以先归约到一个适当选择的 anchor 和 exponent parity，然后在保持原始来源唯一性的 linear provenance contraction 中严格降秩，直到遇到一个 **essential nonlinear descended-resource core**。该核心的局部 rigid witness 来自不同原始 nonregular primes，而不是把 derived macros 重新解释为 primes。

但是，**没有证明这个 exceptional class 为空，也没有得到 universal finite-certificate no-go。** 非线性合并之后的通用 arithmetic resource recursion 尚未闭合。

按任务给出的 gate 口径，本轮达到的是 **Gate B：明确的必要临界类归约**；不主张 Gate A、C 或 D。这里的 Gate B 指下文定义的单来源下降临界类，不是“所有量词均已消除”或者“只剩一个数值待算”。精确的证明、适用域和未闭合位置见 `MASTER_THEOREM.md`。

这些是本轮相对于已读取 current-main theorem stack 的推导；未声称完成文献优先权检索、proof-assistant formalization 或独立作者复核。

---

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 44e522dd6e88504e2b9829f0b27359e6c45a76ff
main tree: 6a30565826c8f988bfbb85e4098b78b2992d290c
```

| PR | live 状态 | merge commit |
|---|---|---|
| #14 | closed / merged | 44e522dd6e88504e2b9829f0b27359e6c45a76ff |
| #15 | closed / merged | 76e7b4d447ea2ba9674b2787990dd37551d6844a |
| #16 | closed / merged | 25086bb932bbae00692ddf06cce0474aedf1cd7a |

固定 SHA 的 STATUS 保留 PAUSED / NONE / UNRESOLVED。完成主要研究后再次读取 `refs/heads/main`，仍为上述 SHA。**PRECONDITION: PASS。**

Sources 是 GitHub connector 的 pinned reads；本地没有取得完整 repository checkout，没有执行 repository-native tests，也没有修改任何 GitHub 对象。读取范围和 Git blob identities 见 `SOURCES.md`、`results/source_binding.json`。本研究包的程序是 standalone reference implementation。

## 2. COMPLETE CURRENT THEOREM LADDER

现有结论与本轮新增内容必须分开。

| 层 | 来源结论 | 不能跨越的边界 |
|---|---|---|
| 原始 formal class | positive odd accepted valuations；local zero 不 fatal；coarse/full reverse CRT [S1] | 不能把零余数接受为“最高 valuation” |
| #11 | same-lower dynamic anchor exclusion；共同 full fiber 至少一个 rigid-only anchor [S2] | 不保证存在共同 full fiber |
| #12 | one-anchor prefix-frontier arithmetic realization；原始 prime leaf inventory 与 final ambient gate [S3] | 不保证 shared-residue/global realization |
| #13 | exact cover-clause contraction；hereditary provenance-cylinder grammar [S4] | 宏不是新 prime；替代 witness 可复用来源 |
| #14 | free-coordinate blocker；joint odd reverse CRT；必要 blocker deficiency [S5] | free matching 不是自动存在 |
| #15 | S1 common-top/pooled-lower alternative；S3 strict deficits；common two-adic criterion；actual SPLIT [S6] | pooled cover 不是 individual complete cover |
| #16 | active Kraft；ancestor-aware Hall；configuration accounting；原始 coordinate-3 资源零；resultant [S7] | 81/21 界只适用于其原始 arithmetic resource 域 |

本轮新增链条为：

```text
hypothetical complete simultaneous certificate
    -> parity-flexible boundary-selected anchor c_*
    -> choose parity b disabling dynamic row 3
    -> complete odd-row subsystem at (c_*,b)
    -> free blocker assignment exists? YES: contradiction
    -> otherwise retain a Hall-deficient original resource subset
    -> completeness-preserving linear provenance descent
    -> essential nonlinear descended-resource core E_L
    -> <=6 original nonregular primes: contradiction
    -> >=7: explicit exceptional class; nonlinear closure not proved
```

这条链没有把 S1 的 pooled 分支错误地改写为两个 individually complete lower systems，而是通过新的 boundary-selected one-anchor reduction 避开这一不合法同步要求。

## 3. UNIFIED STATE SPACE

同一 original ledger 保存 `(q,K,r,E,w,s,U)` 和完整 paired state。两种工作状态各有明确语义。

Ascending escape state 保存已选择的 lower CRT prefix、仍可能逃逸的 anchors、已认证的 rigid exclusions、当前/未来 blocker options。Descending obstruction state 保存未消去的坐标、原始 dynamic rows、单来源 rigid seeds、helper lineages 和 exact residual predicate。

这两种状态**不是同一个方向的 prefix**。Ascending 中某 row 因某个已选 digit 被排除，不意味着它可从一个尚未限制该 digit 的 descending whole-fiber budget 中删除。

在 linear descent 阶段，每个 geometric rigid seed 保持唯一原始 nonregular-prime 来源，最多生成一个 child。多个 seeds 可以引用同一 helper dynamic row，但必须是同一个冻结的 row state。具体 grammar 见 `DEFINITIONS.md` 和主定理第 4 节。

## 4. HYBRID LOCAL ESCAPE THEOREM

任务提出的不等式，在正确的时间语义下成立：

\[
\frac{|F_\ell|}{\ell}+\max(D_{\ell,0},D_{\ell,1})
+R^{\rm rem}_{\ell,0}+R^{\rm rem}_{\ell,1}<1.
\]

证明是 exact normalized measure 上的 union bound，加上同一 lower prefix 上原始 dynamic row 至多在一个 anchor active。

结论是存在一个完整 coordinate residue modulo `ell^beta`，同时避开 blocker cylinders 与剩余 fatal sets；不是“某个第一 digit 的所有高位都安全”。

目前被分配到 `ell` 的行，只有在实际选择了避开其 forbidden digits 的 residue 后才成为 preblocked。可在联合集合 `B_F union remaining events` 中条件性省掉包含于 `B_F` 的当前 rigid cylinder，但不能无条件把它从 whole-fiber Kraft demand 中扣除。

更重要的是，本轮给出 exact centered forbidden-set criterion：若没有任何 rigid/blocker cylinder 包含 dynamic center，则必有 hole；否则只需逐一检查最浅 centered cylinder 之前的所有 unaccepted side subtrees 是否被精确覆盖。它严格强于 scalar mass 检查，并保留 ancestor 覆盖。

## 5. GLOBAL BLOCKER OPTIMIZATION

每个 nonregular q 的选项是一个真实 odd order factor，或保持 alive。以二进制变量记录 assignment，以 OR 变量记录 distinct forbidden positions，可以建立 finite integer program。其成本必须按不同 digits 计，而非机械地按每行两个 slots 计。

完整优化还须包含 lower-guard activity、实际 digit choice、preblocked/current/future 状态与 whole paired row configuration。当前未证明一般情形具有普通 flow 或 matroid min-max 结构。

本轮实际实验仅对 `20771 -> alive / 5 / 31 / 67` 四种静态选项做完整枚举，各使用一个确定的 ascending greedy policy。在指定实际系统中，5 和 31 成功；alive 和 67 的该 policy 失败。**这种失败不是 exact primal infeasibility。** 另有不依赖该 greedy 限制的 exact alive-anchor backtracking。

Free-coordinate uniform 子问题保留 ordinary capacitated Hall 判定。对选定单 anchor，每个 free coordinate 提供 `ell-1` 个最坏情形 slots；完整证书因而必须存在一个 Hall-deficient original-seed subset。没有证明它恰好等于 nonlinear frontier 的来源集合。

## 6. PRIMAL–DUAL FORMULATION

正确 primal 是

\[
\exists c\in\{0,1\}\;\exists d:\quad\text{all rows are safe at }(c,d).
\]

不是要求同一个 d 在两个 anchors 都安全。只需要一个 anchor 的逃逸，就足以否定 simultaneous completeness。

Ascending game 的状态保存 alive set `S`。选 digit 后，从 S 中删除已被 fatal event 命中的 anchors；只要末端 S 非空就找到 escape。SPLIT 因而不会被自动误判为失败。

它的 exact dual 是覆盖所有 digit choices 的 losing tree。配置型 Hall/Kraft 权重给出该 dual 的必要不等式，但未证明这些权重足以判定 integral feasibility。四个 demands、两个 row configurations 的 fractional/integral gap 已被精确复算。

## 7. CRITICAL COORDINATE EXTRACTION

本轮没有从 `hybrid cost >=1` 直接宣告出现 core。那只是一个 sufficient bound 失效，可能完全由重叠造成。

真正的 core 来自 **complete parent + incomplete linear sub-residual**。在后者的一个 canonical lower escape y 上，前者必有 exact full top fiber，但没有 active simple pair。删除 redundant slices 得到 irredundant witness。

关键局部定理是：一个 admissible parity-shell dynamic bundle，加上少于 p 个 proper p-cylinders，能够覆盖全坐标，当且仅当存在 `dynamic + centered depth-one cylinder` 的 simple pair。若 `j=0` 不被接受，每个 first branch 都需要 rigid；若 `j=0` 接受而没有该 centered first branch，`j=1` 因 parity 不被接受，又需要至少 p 个 deeper cylinders。

因此首个 essential nonlinear witness 的 rigid-origin 数 r 满足

\[
p\le r\le N,\qquad r\equiv1\pmod{p-1},
\]

其中 N 是原始 rigid-seed 数，而不是 generated macro 数。严格下降会终止：一个全程 linear 的 terminal seed 必须经过最小 helper 3，但我们已经选了使 dynamic 3 inactive 的 parity。

## 8. KRAFT TRADEOFF

没有找到可用于任意非线性递归的 telescoping potential。实际两行例子 `(31,20771)` 已反驳一种自然但过粗的

\[
\Phi=\text{current safe measure}+\text{future raw rigid deficit}
\]

非增猜想：blocker 完全落在原先的 dynamic forbidden set 内，当前安全量不减，而未来 unconditioned inventory deficit 增加 `1/67`。这只反驳这一定义的 potential，不反驳所有条件化权重。

本轮有效的资源结算发生在**第一次非线性分叉之前**：single-origin injection 保持，不把宏当 prime；Kraft tree 的 leaf-depth tax 可以用于几何 frontier；算术 head inventory 对这些几何叶片给出真实位置限制。

## 9. POOLED-BRANCH RECURSION

S1 的 `A_0 union A_1=Y` 被原样保留为 anchor-tagged demand。Exact alive-anchor game 可以继续处理它，但其有限终止不等于 arithmetic contradiction。

主定理走另一条有效归约：对每个 two-adic residue，总有同一个 anchor 在两种 exponent parities 上分别拥有 safe boundary。因 odd rows 的指数 2-part 至多是 parity，完整证书迫使该 anchor 的 odd subsystem 在每种 parity 都 complete。随后选择 dynamic 3 inactive 的那个 parity。

这给出真正的单-anchor complete object，不是把 pooled cover 强行转换成 complete object。完整推导与 mod4 选择表见主定理第 2 节。

## 10. RESULTANT INTERFACE

继承 [S7] 的准确范围：original paired rigid resource、固定原始 rank 与 depth `h=ell^d`、固定 ordinary integer lower representative Y，满足

\[
q\mid\mathfrak D_h(Y)
=\operatorname{Res}(T^h-5^{Yh},(T-2)^h-5^{Yh}),
\]

且 odd h 的 resultant 非零。

本轮以 Sylvester/Bareiss determinant 精确计算 `h=3,5,7`、`Y=0,1,2` 的九个整数，并与封闭多项式表达交叉核对。非零 Y 的结果没有宣称完成 prime factorization，因此没有推出 arbitrary-Y 的资源零结论。

对 actual `q=20771`，完整 155 个 lower classes 的 coset-edge enumeration 与 polynomial-gcd degree 完全一致；总计 33 条 same-lower edges。Y=0 为空，但 Y=7 等非零 classes 确有 paired edges。

尚未证明 criticality 必然集中要求足够多 paired resources 于同一个原始 `(h,Y)`，也没有把 resultant 的原始 row 参数换成 descended macro 的当前 coordinate。这仍是 endgame closure 的约束，而不是已完成的矛盾。

## 11. COORDINATE-3 TERMINAL ANALYSIS

[S7] 的原始资源界仍为：depth 1,2,3 无原始 rigid prime；rigid-only full fiber 至少 81 个 active primes；允许 dynamic 的单-anchor full fiber 至少 21 个。它们不直接适用于 descendants。

本轮的 helper-aware 新结论是：linearly descended rank-3 seeds 中，深度不超过 2 的所有事件，必须包含于下列固定 helper guards 的并集：

```text
depth 1 heads: 7,31
depth 2 heads: 19,5167
```

这是完整的 order classification，而不是 prime scan。总覆盖量至多

\[
2/3+2/9=8/9.
\]

因此没有 dynamic 3 时，完整 descended 3-frontier 必须有 depth 至少 3 的叶子；完整 ternary frontier 至少有 `1+2*3=7` 个 rigid leaves，即 7 个不同 seed origins。

另一方面，“order DAG 足够长就必到 3”本身是假的。对任意 admitted p，`Phi_p(5)=3 mod4` 保证一个更大的 admitted q 满足 `ord_q(5)=p`。从 11 开始可以任意延长，底端是 coordinate 5。这里给出的是实际 order 算术反例，不是完整证书反例。

## 12. COUNTEREXAMPLES

反例按作用域分开记录在 `COUNTEREXAMPLES.md`：actual odd-r two-adic boundary 反驳错误 primal；actual 67/20771 SPLIT 反驳“共同 greedy 停止即 individually full”；同例检测 current-blocker 提前删除；centered geometry 反驳 `mass>=1 => coverage`；actual 31/20771 反驳指定 naive potential；abstract configurations 反驳 weighted Hall 的 integral sufficiency；actual arbitrarily long order chain 反驳单靠 DAG 长度强制 coordinate 3。

**没有构造 genuine actual complete certificate。** 七叶 ternary frontier 只是抽象几何，不能作为 seven-prime arithmetic sharpness example。

## 13. EXACT COMPUTATION

全部程序使用 Python standard library、整数、exact fractions、modular powers 与 exact determinant。运行没有扩大 prime scan，也没有启动大型计算。

| 检查 | 实际范围 | 结果 |
|---|---:|---|
| 稀疏 local-cover lemma | 100,189 cases | 0 mismatches |
| exact centered forbidden-set criterion | 129,183 cases | 0 mismatches |
| strict hybrid implication | 95,723 applicable cases | 0 failures |
| parity-flexible boundary | K=2..9；1,020 residues；2,040 parity witnesses | 全通过 |
| abstract triangular systems，rigid count 0/1/2 | 1,343,965 systems | 无 complete system；仅限所列 grammar |
| actual 67/20771 full-period anchor predicates | 456,940 comparisons | 0 mismatches |
| actual paired coset / polynomial gcd | 155 lower classes | 0 mismatches |
| exact resultants | 9 fixed `(h,Y)` cases | 两种组织方式一致 |
| <=6-leaf 5-frontier witness multiplicities | 714 abstract multisets | 上界全通过 |
| named regression tests | 15 tests | PASS |

前两项的 center=0 枚举利用 translation-equivariance；tests 另检查若干全 center translations。Abstract triangular model 使用实际 dynamic order signatures，但 rigid seeds 是 abstract cylinders，不能称为 actual-prime exhaustive search。

七-prime 普遍界依赖主定理的解析证明；这些表不是“枚举所有 finite certificates”。重放可输出到外部目录，reference JSON 的数学内容可逐项复核。仅 `seconds` 字段与测试日志中的运行时间不作为 mathematical equality 标准。

## 14. STRONGEST MASTER THEOREM

最强结构定理和数值推论分别是：

\[
\boxed{\text{Complete}_{0,1}\Rightarrow
\text{canonical first essential nonlinear descended-resource core }\mathcal E_L.}
\]

\[
\boxed{\text{Complete}_{0,1}\Rightarrow
\#\{q\in P:s_q\ge2\}\ge7.}
\]

七-prime 界的最后一步不是把 81 误套到宏上。假设 N<=6，由 core rank bound，首个 nonlinear p 只能是 3 或 5。

p=3 已由 `8/9` helper-capacity 和七叶 tax 排除。p=5 没有 dynamic；不超过六行的 irredundant full 5-frontier 只能是五个 first-level cylinders。若 top seeds 数为 n，minimal witnesses 至多 `n-4`；加回 lower seeds 后，完整 exact contraction 留下至多 `N-4<=2` 个 lower cylinders。

这些 lower cylinders 不可能是常量：否则构成它的五个 top cylinders 都必须 3-free，但 3-free depth-one 5-descendants 的 least helper 只能是 11 或 71，只能提供至多两个固定 first digits。这里使用完整分解 `Phi_5(5)=11*71`、`Phi_10(5)=521`，且前两者 regular，后者不 admitted。

因此 residual 至多有两个 proper 3-cylinders，而 dynamic 3 inactive，不可能覆盖。矛盾。所有步骤的详细证明见主定理第 6—8 节。

## 15. CANONICAL MINIMAL SURVIVOR CLASS

`E_L` 是局部 obstruction record：冻结实际 original ledger、boundary-selected anchor/parity、至少七个 initial rigid-seed budget、合法单来源 helper lineages、rank p 和 lower point y、无 active simple pair 的 inclusion-minimal full frontier，以及一个 free-blocker Hall deficiency。

它不要求候选 ledger 已经 globally complete 才能检查其局部条件，因此不是把完整证书换一个名字。对由完整证书提取的记录，另有 completeness-preserving history 与 fixed-U minimal subcover receipts。

“Canonical”基于指定的有限排序；“minimal”是 inclusion-minimal。没有声称最少总 prime 数的 complete certificate 已被找出，或所有 core 都有七片 local leaves；p=5 的 local witness 仍可能只有五片而需要额外 lower resources。

## 16. DOES THE RECURSION CLOSE?

**Linear phase 闭合到一个明确的 nonlinear exceptional core；general nonlinear phase 不闭合。**

如果只把所有坐标逐个消去，当然得到 finite decision procedure；那不是任务所要求的 arithmetic strict-descent endgame。第一次非线性之后，同一个来源可能出现在多个 lower alternatives 中。目前没有证明保持真实 prime accounting 的单调 potential，也没有证明每个 E_L 都能变成更小的 arithmetic critical class。

因此不主张 Gate C。

## 17. DOES THIS PROVE C=1 FINITE-CERTIFICATE NO-GO?

**没有证明 universal no-go。**

已经证明的无界子类是：original nonregular prime 总数至多六的任意 finite admitted system，不论 regular rows、precision、accepted sets 和 shared residues 如何选择，都不可能 complete simultaneous。

这不是 “q<=某个 cutoff” 的重新包装。它限制 nonregular resource cardinality，不限制 q 的大小。但 resource cardinality >=7 的系统没有被本轮普遍排除。

## 18. DOES THIS PROVE A303656?

**没有。**

研究对象仍是 finite fail-closed local certificate formalism。所读 repository 状态没有给出“C=1 obstruction 存在 iff complete finite admitted certificate 存在”的一般完备性定理。即使未来 universal finite-certificate no-go 成立，也不能跳过这一 formalism-to-original-problem bridge。

本轮更没有证明所有 `n>1` 的 universal representability，亦未构造 certified counterexample。

## 19. REMAINING SINGLE MATHEMATICAL GAP

对本轮 endgame 路线，剩下的核心缺口可以准确表述为：

> **对 E_L 中 state-compatible、single-origin descended frontiers，在第一次 nonlinear merge 及其后继 lower-demand alternatives 上，证明一个不把 branch reuse 误算成新 prime 的 arithmetic demand–capacity / well-founded descent theorem。**

Raw original Kraft inventory、局部 resultant 和 ordinary Hall 都未自动提供这个定理。需要把 helper-induced positions、真实 shared row states、重叠 cover witnesses 和剩余 anchor-tagged demands 同时计入。

这不是说原始 A303656 问题只剩该一个缺口；第 18 节的 formalism completeness bridge 是另一个层次。也不是说这个缺口已经被压缩成一个可直接交给大扫描的有限整数。

## 20. RECOMMENDED NEXT ACTION

推荐下一步先做一次 **theorem-first 独立审阅**，对象只冻结为 `MASTER_THEOREM.md` 的 parity-flexible boundary、single-origin descent、least-helper inventory 和 seven-prime proof，尤其审查 p=5 的 `N-4` residual-count argument。数学审阅通过后再由普通 Codex 做 repository-native integration 与独立复现；本轮没有授权或实施 integration，不建议先扩大 prime scan 或启动 Ultra。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
