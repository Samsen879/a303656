# A303656 C=1 FIRST ESSENTIAL NONLINEAR CORE RECURSION — TARGETED PHASE C

## Executive verdict

```text
RECURSIVE CLOSURE:
NO GENERAL CLOSURE, BUT NEW OBSTRUCTION FOUND
```

本轮没有证明 universal finite-certificate no-go，也没有证明一个新的非平凡 arithmetic subclass 的 recursive closure。没有构造 actual complete certificate。

本轮真正越过“complete ⇒ E_L”的内容是：

**固定单一 anchor、原始状态及 U，在不作人工 lower-cylinder refinement 的 exact #13 表示中，证明 macro 的 lower guard 由其完整原始 support 的 logarithm guards 决定。进一步，每个最小 simultaneous slice-cover witness 的每个 rigid parent 都有一个 private original provider：该行提供此 parent 的精确 p-cylinder，且不在任何其他 parent 的 support 中。**

由此得到：

- shared-origin overlap 的 least-common-ancestor 深度约束；
- 每个 k-parent merge、沿任一 parent 路径，至少增加 k−1 个完整原始 row tokens；
- 一个不依赖“坐标数减少”的严格下降 support-profile potential；
- all-shared support triangle 等 hypergraph 模式不可能成为这种最小 simultaneous frontier；
- 但 nested 3×5×7 ABSTRACT partition 把这一 branching charge 逐步取等，最后仍到 TRUE。因此这不是 contradiction-producing potential。

必须区分 `M = 全部 original rows（含 regular helpers）` 与 `N = original rigid/nonregular seed origins`。上述 private providers 可以是 regular helpers；没有得到把它们再次单射回 N 个 rigid seeds 的定理。这是剩余缺口，而不是缺少一个形式上的严格下降函数。

推荐执行环境：网页端 research/reference laboratory。本轮实际执行数学推导、反例构造及 standalone exact computation；未使用大型 scan、Codex Ultra 或 repository-native integration。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Bound main SHA: 71b8d428b32724c37e593bcfd9d5f06a42e72d21
Bound main tree: 5609e47eed0c058c190ef59c61644e2fd4b8fad6
```

GitHub live branch metadata、closed PR metadata 和固定 SHA 的 STATUS.md 已读取。PR #17、#20、#18、#19 均为 merged，时间分别为 2026-09-06 14:12:30、14:15:57、14:18:58、14:21:38 UTC。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

本报告的源依据是 `SOURCE_READING.md` 中逐项列出的核心 mathematical reports、definitions 和 proofs，涵盖请求的七个目录及辅助 #18/#19 文件。不是整个 repository、各目录全部 generated catalogs/source code、历史 CI 的逐文件审计。未取得本地完整 checkout，未运行 repository 原有 test suite。本轮数值结论来自本包新写的 `reference.py`，不 import repository implementation。

## 2. E_L RECONSTRUCTION

### 2.1 Imported arithmetic definitions

沿用 [S7]，每个 original odd row 是不同的 actual prime q≡3 mod4，参数为 K_q≥2、两 anchors 共享的 r_q mod q^K_q、非空 positive odd accepted set E_q⊂[1,K_q−1]。

\[
V_{q,c}(d)=r_q-3^c-5^d,
\quad w_q=\operatorname{ord}_q(5),
\quad s_q=v_q(5^{w_q}-1),
\]
\[
a_q=\max(0,K_q-s_q),\quad
U=\operatorname{lcm}(t_2,\{w_q\}),\quad
L=\operatorname{lcm}(t_2,\{w_qq^{a_q}\}).
\]

Local zero mod q^K_q 是 unresolved，不 fatal。Coarse fatal 的量词是该 coarse class 的所有 full lifts 被同一原始行接受。固定 anchor 后，非空 original event 是 rigid cylinder 或 dynamic shell bundle。每行在该 anchor 至多有一个 logarithm class modulo w_q。

Dynamic q-row 的 lower guard 是该 log class；自己的 q-coordinate 是一组 parity-admissible shells，遗漏 unresolved center。Rigid row 的 whole event 就是 log cylinder；它需要 s_q≥2。Order 的所有奇素因子严格小于 q。

### 2.2 What E_L actually contains

[S7, MASTER_THEOREM §9] 的 E_L 是局部 obstruction record，不是 complete certificate 的改名。它记录 frozen arithmetic ledger、boundary-selected anchor c_*、dynamic-3-inactive parity b、初始 rigid-seed budget N≥7、兼容 single-origin linear lineages、某个精确 lower point y、rank-p 的 inclusion-minimal nonsimple centered frontier、lower/simple-pair absence，以及原始 blocker options/Hall deficiency。Hall-deficient subset 不保证与 local frontier support 相同。

`N≥7` 是 imported necessary bound，不是本轮用来证明新 recursion 的前提。下面的 abstract minimality、shadow/provenance 定理均不引用 seven-prime contradiction。

定义额外的 provenance-enhanced class：

\[
E_{\mathrm{complete\text{-}derived}}
=(E_L,\ \text{full frozen input},\ \text{complete-preserving extraction history},
\ \text{whole current residual}).
\]

只有该增强对象允许使用“本次 residual 仍 complete”。Bare E_L 只保证记录的局部 fiber 覆盖，不能据此启动全局 recursion。

进入 nonlinear 阶段后，下一核心应称 E_N 或 generalized provenance core。它不能继续使用 E_L 中的 `one seed = one original rigid origin` 条款。

## 3. NONLINEAR MACRO SEMANTICS

### 3.1 Exact rule and required record

固定 c=c_*、parity b、最终 U 和 original state vector。考虑最高剩余奇坐标 p：

\[
E_i=G_i\times A_i,\qquad X_p=\mathbb Z/p^{\beta_p}\mathbb Z.
\]

保留 whole dynamic bundle，不将其 side components 计成多个原始资源。令

\[
\mathcal C_p=\{I:\ \cup_{i\in I}A_i=X_p,
\ I\text{ inclusion-minimal}\}.
\]

Exact contraction 是 [S3] 的

\[
\operatorname{Sat}_p=\bigvee_{I\in\mathcal C_p}\ \bigwedge_{i\in I}G_i.
\]

一个输出 macro 至少记录：

```text
Macro = (
  eliminated coordinate p and retained ambient depths,
  exact minimal slice-cover witness I,
  parent event IDs and slices,
  full original-row support S,
  original rigid-seed support R contained in S,
  one globally frozen state token for every q in S,
  exact stripped CRT intersection G,
  anchor / guaranteed demand type,
  parent provenance DAG and witness receipt
)
```

S 包含 regular/dynamic helpers，R 只包含 initial rigid origins，二者不能互换。空 CRT intersections 丢弃。Lower events 原样保留。OR alternatives 不被当成同时新增资源。

### 3.2 Canonical positive-guard representation

下面的定理使用未作人工 disjoint refinement 的 #13 positive-cover-clause representation。除固定 parity / safe two-adic boundary 外，没有把某个任意 lower point 预先写进每个宏的定义。

若实现为展示或遍历而细分 named guards，必须保留原 cover clause 的几何内容；refinement 添加的深度不是新算术 precision。不能对人工细分后的 cell 直接使用下面的 exact-provider 结论。

对非空 original row q，写 H_{q,c} 为其 logarithm guard modulo w_q。Rigid row 的整个 event 是 H；dynamic row 的 H 不包含它自己的 shell slice。

### Theorem T1 — support determines the canonical cylinder

设 J 是已经完全消去的坐标集，M 是当前 canonical cylindrical macro，S(M) 为完整原始 support。则

\[
\boxed{G_M=\bigcap_{q\in S(M)} H_{q,c}|_{\Lambda\setminus J}.}\tag{T1}
\]

其中 restriction 表示删去已经消去的 primary congruence factors，保留其余 exact residues。

**证明。** Original rigid cylinder 满足此式。一个 original dynamic q-row 只有在自己的 q-coordinate 消去后才进入 cylindrical macro；它的 shell 覆盖事实由该次 exact witness 认证，残余仅为 H_q。每次 merge 对 parents 的 lower guards 取交，并令 support 为 parents 的并。CRT-coordinate stripping 与这些 congruence intersections 可逐坐标交换。因此归纳得到此式。不同 parents 引用同一个 q 时重复相同 H_q，交集幂等；不同 state 被禁止。□

**Corollaries.** 固定 anchor、state、J 后，两个有效 cylindrical macros 若 S 相同，G 必相同。若 S⊂T，则 G_T⊂G_S。所以可以选择同 support 的一个 canonical valid witness，并吸收有现成 smaller-support cylinder 的 larger-support cylinder。该操作保留每个 enabled-origin subset 下的 truth，而不仅保留 full ledger 的 truth。

**Reachability proviso.** T1 只说有效、可达宏的 guard 由 support 决定；不说任意 subset S 的 log-guard intersection 都可插入 residual。每个宏仍须保留真实 minimal-cover parent witness。

[S4] 已经建立 state-token idempotent algebra、support antichains 与 exact original-state relation；本轮不将这些基本机制重报为新发现。T1 是把这种 bookkeeping 明确落实到 actual logarithm-guard 几何的推导。

## 4. ORIGIN-REUSE AUDIT

### 4.1 Four different multiplicities

Branch-local reuse：q 出现在不同 OR clauses，合法，但 state 必须相同。

Simultaneous reuse：q 同时出现在某个 cover witness 的多个 parent supports，也可能合法。它不是每次消耗一份容量。

Duplicate geometric leaves：不同 provenance clauses 可以有同一 guard。仅做 geometry 去重可以保留 full-state truth，却可能删掉其他 enabled-original-subset 的合法证明。

Duplicate arithmetic capacity：将同一 q 的重复出现计成新 prime 或任意重选 state，不合法。

### Theorem T2 — private exact providers

取一个 nonempty lower intersection 的 inclusion-minimal slice-cover witness I。对每个 cylindrical/rigid parent i，其 proper p-cylinder A_i 都存在一个 q_i∈S_i，满足

\[
\boxed{Q_{q_i,p}=A_i,\qquad
q_i\notin\bigcup_{j\in I,\,j\ne i}S_j.}\tag{T2}
\]

这里 Q_{q,p} 是 H_{q,c} 的 p-primary projection；若 A_i=C_d(a)，则

\[
\nu_p(w_{q_i})=d,\qquad
H_{q_i,c}\text{ has the exact same residue }a\pmod{p^d}.
\]

**证明。** T1 把 A_i 表为有限个 p-cylinders 的非空交。p-adic cylinders 相交则嵌套，故该交等于其中某个最深因子，选其 original row q_i。最小 slice cover 中两个 rigid cylinders 不可能相交，否则较深者冗余，所以各 A_i 两两不相交。若 q_i 也属于另一个 cylindrical parent j，则 T1 给出 A_j⊂Q_{q_i,p}=A_i，矛盾。唯一可能的 dynamic parent 是未消去的 original p-row，support={p}；q_i>p，因为 p|w_{q_i}|q_i−1，所以 q_i 也不在该 dynamic support。□

Dynamic parent 自己的 token p 同样 private：它不能在任何先前生成的 macro 中出现，因为 p 尚未消去。

**重要加强：**这不只是“可给 leaves 匹配不同 providers”。每个 provider 在这个 simultaneous witness 中都是其 parent 的 private original row。它仍可以出现在其他 OR alternatives 的 witness 中。

### Theorem T3 — shared origins obey a prefix-LCA bound

若同一个 q 出现在若干不同 rigid parents 的共同 support 中，则这些 parents 的 p-cylinders 均包含于 Q_{q,p}。令 a 为包含所有这些 cylinders 的最小 p-adic ancestor 的深度，则

\[
\boxed{\nu_p(w_q)\le a.}\tag{T3}
\]

特别地，它们若横跨不同 first branches，则 a=0，因而 p∤w_q。这个共享 origin 在当前 p-coordinate 上没有位置区分能力，不能被反复计为提供多个 leaves 的资源。

T2/T3 是同一个 fixed anchor / fixed state 的结论。不能把两个 anchors 的不同 logarithm shadows 不加标签地合并应用。

### Precise hypergraph obstruction

Parents 的 support hypergraph 必须具有 private elements。三条支持

\[
\{a,b\},\quad\{b,c\},\quad\{a,c\}
\]

没有任何 private element，故不可能成为 T2 范围内的三-parent minimal simultaneous frontier。不论原始 rows 是否能算术实现，只要保持 canonical frozen-shadow semantics，这个模式就已被排除。

这不排除上述三条支持作为互相替代的 OR clauses 存在；被排除的是把它们同时当作最小、不同 leaf 的 full-cover parents。

## 5. CANDIDATE POTENTIALS

| Candidate | Precise test / outcome |
|---|---|
| Remaining-coordinate rank / rank multiset | 下降，但只是源文件已知的 termination；不排除 TRUE。 |
| Full original row count M、fixed original order ledger | Frozen，不下降；不能通过删宏冒充删行。 |
| Original rigid count N | First nonlinear 后不等于 leaves/macros；没有一般下降证明。 |
| Minimum complete original-support size | Full exact history 下恒定；nested examples 中全部原始行始终 indispensable。 |
| Maximum parent support size | Nested 3×5: 1→5→7，增加，否定该方向的非增性。 |
| Raw macro count / number of support alternatives | Duplicate p-frontier: 2p→2^p，p=3,5,7 均增加。 |
| Sum of normalized macro masses | 同一例 2→2^p；不是 Kraft conservation。 |
| Total original-token occurrence load | 每个 original 的出现次数 1→2^(p−1)，增加。任何非零非负固定 row weights 的这种 occurrence sum 都增加。 |
| Uniform-branch entropy log(number of clauses) | 同一例 log(2p)→p log2，增加；没有固有概率分布可赋予更强含义。 |
| Provenance width / maximum lineage size | OR antichain 可以增大；single lineage support size 是增加而非减小。 |
| Hypergraph unit-capacity packing | 把合法共享 origin 当成 consumed slot，sunflower 产生 false rejection。 |
| Hypergraph transversal / packing number | Sunflower 的 current supports: singleton family→three shared-core edges→one edge；packing/transversal 在末步可保持 1，不严格下降。 |
| Fixed blocker Hall deficiency | 仍是原始 ledger 图上的量，full exact contraction 不改变它。不能认作 current macro 的资源差额。 |
| Coverage-measure submodularity | Universal saturation 不保留 submodularity；duplicate alternatives 也破坏 supermodularity。见 §6。 |
| Original-state / enabled-origin semantic relation | Exact whole-state invariant，有用但 conserved；不是 strict descent。 |
| Lexicographic small-support profile | 本轮证明严格下降；见 T4。仍不排除 TRUE。 |
| Private-provider branching charge | 每个 k-parent merge 至少增加 k−1 个原始 tokens；可被 ABSTRACT nested complete partitions 逐步取等。 |

这里没有宣称所有 conceivable arithmetic potentials 都失败。已排除的是上述明确的量及以 conserved profile 为唯一输入的函数。

## 6. COUNTEREXAMPLES TO FAILED POTENTIALS

### A. Duplicate p-frontier — ABSTRACT

对每个 p∈{3,5,7}，在 X_p 中每个 digit 给两条不同 original tokens 的同几何 singleton events；全部 lower guards 为 whole，states frozen。

每个 minimal cover 必须在每个 digit 的两条供应中选一条，故有 2^p 个 witness supports。

| p | original rows | resulting minimal support clauses | raw mass before→after | occurrence of each origin |
|---:|---:|---:|---:|---:|
| 3 | 6 | 8 | 2→8 | 1→4 |
| 5 | 10 | 32 | 2→32 | 1→16 |
| 7 | 14 | 128 | 2→128 | 1→64 |

所有输出 guards 都是 TRUE；geometry-only 去重会留下一个，但全部 original-subledger proof alternatives 不能因此视作同一个资源。Source [S4] 已有 binary clause/mass amplification；本表是奇素数模型中的参数化复算与本轮 strict potential 的压力测试。

### B. Seven-row shared-core sunflower — ABSTRACT

在 X_3×X_5，坐标为 x,z，取

\[
A_i=\{z=i\},\quad i=1,2,3,4;
\qquad B_j=\{z=0,x=j\},\quad j=0,1,2.
\]

这是 7 个非空、两两不交、全覆盖的 product cylinders。每行 indispensable。

消去 5 得到

\[
M_j=\{x=j\},\qquad
S(M_j)=\{A_1,A_2,A_3,A_4,B_j\}.
\]

消去 3 得到 TRUE，support 是全部 7 行。于是

```text
current event counts: 7 -> 3 -> 1
maximum support size: 1 -> 5 -> 7
minimum complete original-support size: 7 -> 7 -> 7
```

公共 A-core 可合法出现在最后一次同时使用的全部三个 parents。Private providers 是各自的 B_j。把 A_i 容量设为 1，再要求三个 M_j 各消费它一次，会错误地拒绝真实的 abstract cover。

精确地说，这三个 support hyperedges 的 integral/fractional disjoint packing optimum 都是 1：选一条 edge 达到 1；任意一个共享 A_i 上的单位约束给出上界 1。但三个几何 leaves 确实共同覆盖 X_3。这里的 packing 不是正确的覆盖 primal。

**最小性范围。** 在 beta-one、rigid-only、3×5、连续两个 essential nonlinear steps 且消去 5 后没有 TRUE macro 的 grammar 中，7 行最少。若总行数 n≤6，top rows t≥5。所有 top witnesses 必须从 5 个 first branches 各取一条，t≤6 时最多 t−4 个 witnesses；保留 k=n−t 个 lower rows 后至多 n−4≤2 个 proper 3-cylinders，不能 cover。该证明只用 elementary counting，不引用 seven-prime arithmetic theorem。

这个例子不是 actual E_L：其四个 3-free depth-one 5-branches 违反 [S7, Lemma 7.1] 对 pre-nonlinear actual linear lineages 的“至多两个固定 branches”限制。因此它否定结构性再抽取/支持减少论证，不否定 actual arithmetic recursive closure。

### C. Nested 3×5×7 — ABSTRACT, sharp branching charge

先用 6 条 z_7≠0 的单-digit strips；在 z_7=0 中用 4 条 z_5≠0 strips；剩余 z_7=z_5=0 用 3 条 z_3 singleton cells。

这是 13-row exact partition，经过

\[
13\longrightarrow7\longrightarrow3\longrightarrow1\ (=\mathrm{TRUE}).
\]

最深路径的 support sizes 是 1→7→11→13，新增 tokens 分别为 6、4、2，恰好等于各次 arity−1。全部 13 个 original rows 在每一 exact stage 的 enabled-subledger profile 中均 indispensable。

一般的 nested construction 使用 1+Σ_i(p_i−1) 行，并把每一步 private branching charge 取等。故“有限原始 ledger + 每步付出 fresh support + well-founded descent”仍与 complete TRUE root 相容。

### D. Pairwise-disjoint supports and tree provenance — ABSTRACT

把 3×5 的全部 15 个 cells 各赋一个 original row。消去 5 后三条 x-singleton macros 的 supports 两两不交，每条大小为 5；再消去 3 得 TRUE。

因此 bounded witness width（这里最大 5）、tree-like provenance、simultaneous disjoint supports、单一 fixed anchor 本身不排除成功终点。没有构造满足这些附加条件的 actual admitted complete system。

### E. Universal projection destroys submodularity — ABSTRACT

p 条 disjoint strips 的 enabled-origin covered measure 为

\[
f_{\rm before}(A)=|A|/p,
\]

是 modular。消去该坐标后

\[
f_{\rm after}(A)=\mathbf1_{A=P}.
\]

取不同 a,b，令 A=P\{a}、B=P\{b}，则

\[
f(A)+f(B)=0<1=f(A\cup B)+f(A\cap B),
\]

故不 submodular。

再用 duplicated frontier 的两套互不相交完整选择 A,B，得到 2>1，违反 supermodularity。因而不能把这个 coverage functional 当作 contraction-closed matroid rank 或统一的 submodular capacity。

[S9] 的固定 bipartite Hall deficit δ(S)=|S|−C(N(S)) 是 supermodular；这与上述反例不冲突，因为它是不同函数。

### F. State reselection negative control — ABSTRACT

一条 original q 有三种状态，每个 frozen state 仅供应 X_3 中一个 digit。任何 single global state 都不 full。若把三种状态分别赋给三个分支，会伪造 full cover。

正确 token algebra 是同 state 幂等、不同 state 冲突为 FALSE。合法的 sunflower repetition 不发生 state reselection，不能与此错误模型混同。

## 7. BEST SURVIVING INVARIANT

### Theorem T4 — strict support-growth and support-profile descent

在 T1 的 canonical fixed-anchor setting 中，一个非空最小 k-parent cover macro M 满足，对每个 parent i，

\[
\boxed{|S(M)\setminus S_i|\ge k-1.}\tag{T4a}
\]

**证明。** T2 给每个 rigid parent 一个 private provider；若含 dynamic parent，其原始 token 也是 private。除 parent i 以外的 k−1 个 private tokens 不属于 S_i，却都属于 S(M)。□

所以每个 parent support 都严格包含于 child support。沿一条 original-to-descendant path，

\[
\boxed{\sum_{v\ \text{on path}}(k_v-1)\le M-1.}\tag{T4b}
\]

这是真正的 original-token amortization，不是“某个坐标没了”。但 M 计全部 original rows，包括 regular helpers。

令 n_s(Σ) 是当前非空 events 中 full support size 为 s 的数量，未消去的 original dynamic row 计一个 singleton support。定义

\[
\mathcal I_{\rm lex}(\Sigma)=(n_1,n_2,\ldots,n_M)
\]

按小 support size 优先的 lexicographic order 比较。

**每次移除至少一个 proper top event 的 exact contraction 都严格降低该向量。** 设被移除 parents 的最小 support size 是 s。所有新宏的 support size 均大于其每一个 parent，因此大于等于 s+1。小于 s 的计数不增加，size-s 至少减少一条；pruning 只会进一步减少计数。有限维非负整数向量的此 lex order well-founded。□

若需要单个整数，先作 T1 的 support-aware normalization。当前 cylindrical events 至多 2^M−1 个，original dynamics 至多 M 个。取

\[
B=2^M+M+1,
\qquad
\boxed{I(\Sigma)=\sum_{e\in\Sigma}B^{M-|S(e)|}.}\tag{T4c}
\]

每个 support-size digit 小于 B，故 lexicographic strict decrease 等价于该整数 strict decrease。Inert-coordinate pass-through 不必严格下降；每个 essential nonlinear step 都严格下降。

因此固定 M、固定 primitive shadows 的非平凡 exact contraction 不可能产生保留 support-size profile 的 cycle，连同 original labels 的 isomorphic renaming 也不行。这是 T4 的推论，不是发现了 arithmetic impossibility。

**边界。** I 是 provenance-sensitive、arithmetically compatible 的 complexity，不是 arithmetic capacity/Kraft mass。它没有证明 terminal TRUE 不可能。Nested partition 精确展示其到达 I=1 的 TRUE root。若计入整个历史 DAG 而非 current event frontier，历史节点会积累，不能声称 DAG memory 也下降。

### Theorem T5 — enabled-origin completeness is conserved, not a potential

固定当前完整 residual Σ。对每个 A⊂P，只启用 support⊂A 的 events，定义 χ_Σ(A) 为其是否 complete。

Full #13 contraction 对每个 A 都 exact：一个 enabled slice family full，当且仅当它包含一个 enabled minimal slice-cover clause。因此

\[
\boxed{\chi_\Sigma(A)=\chi_{\operatorname{Contr}\Sigma}(A)
\quad\text{for all }A.}\tag{T5}
\]

T1 的 support-aware absorption 保留此式。故任何仅依赖 frozen ledger 及整个 χ-profile 的 statistic 都不能作为 strict descent。最小 complete support、其 weighted minimum、complete-support antichain 的不变量均属此类。

该 exact provenance/state-relation 机制已在 [S4] 中出现。本轮贡献是将其作为潜能函数的明确障碍，并与 T1/T2/T4 及反例结合，而不是声称首次发现此 invariant。

**Pruning caveat.** #17 允许只保留一个仍 complete 的 linear sub-residual。这可能丢失其他 original-subledger 的覆盖证明。因此 T5 若从 E_L 的当前 residual 开始，保留的是该 proof-relative χ。只有全程保留 full exact contraction，才可自动与原始系统所有 subledgers 的 χ 等同。

## 8. RECURSIVE CORE THEOREM CANDIDATE

正确可证明的版本是：从 E_complete-derived 的完整当前系统出发，可以在同一 frozen ledger 和 U 上继续 exact、support-normalized contraction；每个非平凡步骤降低 T4 的 I；每个新 minimal witness 满足 T2/T3。

但其结论是“得到有限 exact residual sequence”，终点可能 TRUE。它不是用户要求的 terminal-impossible recursive survivor theorem。

对候选“再抽出更小 essential core”的逐项回答：

| Question | Answer |
|---|---|
| 原始 ledger 是否相同？ | 可以且应当相同；S 是 current proof support，不是新 prime ledger。 |
| 是否可以删除 origins？ | 只可删除经 whole-residual exact proof 确认不必要的 origins；不保证存在。Nested example 全部 indispensable。 |
| U 是否 frozen？ | 必须保持。Mute events 不触发 U 重算。 |
| lower guards 如何继承？ | exact stripped CRT intersections；T1 给出 original-log-shadow 表示。 |
| 多个 witnesses 必须全保留？ | 不必保留完全相同 support 的每份 DAG；可 canonical 化及 sound absorption。但不能无条件只挑一个局部 witness 替代全局 OR。 |
| new E_L 是否更小？ | 一般不是 E_L，而是多-origin E_N；support budget 可以更大，rigid-origin count 未获下降。 |
| 是否一定还有下一 essential nonlinear core？ | 没有证明；最小 ABSTRACT X_3 的三条 singleton 已可直接 TRUE，nested examples 给两级/三级完整过程。 |

尤其在 distinguished parity 上，若 critical coordinate 已是 3，消去它后没有更低 odd coordinate。此处若要排除 TRUE，必须排除 actual reachable terminal frontier，不能再借“寻找下一个小核心”延长证明。

## 9. PROOF OR FAILURE

### Proven in this report

T1：canonical support-to-log-guard identity。

T2：minimal simultaneous frontier 的 private exact-provider condition。

T3：shared-origin LCA/order-depth constraint。

T4：arity-sensitive support growth、path charge 与 strict support-profile potential。

T5：在明确 exact-history scope 中的 enabled-origin profile conservation，并据此排除依赖该 profile 的 strict potentials。

### What is not proved

未证明 private providers 必须是 nonregular rigid origins；未证明 regular helper provider 可以 injectively charged to a new original rigid seed；未证明完整 arithmetic ledger 的 terminal private-provider demand 超过 available capacity。

没有把 structural abstract counterexample 升格为 actual recursive-closure counterexample。没有用 seven-prime theorem 循环证明上述结论。没有通过 finite termination 宣称 no-go。

### Prefix-depth consequence

在一个 rigid-only full p-frontier 中，若最深 leaf 深度为 D，则至少有 1+(p−1)D 个 leaves [S2]。T2 将这些 leaves 注入不同、且相对该 witness 私有的 original provider rows。因此这个计数在 arbitrary nonlinear descendants 上仍有一个可靠的 **all-original-row** 解释。

但这不是 raw nonregular-prime tax。Providers 可能是已经消去的 regular dynamic helpers；同一个全局 provider 可在另一次 OR witness 中再次出现。Mixed dynamic frontiers 必须按未被 dynamic 覆盖的 side subtrees 分别计算，不能原样套用 rigid-only 的 depth bound。

## 10. EXACT COMPUTATION

### 10.1 Complexity gate and implementation

Reference 用整数 bitsets、Fraction、有限集合。一个 n-top-event step 通过 subset-union DP 枚举至多 2^n−1 个集合，并用删一元素测试 inclusion-minimality。Hard gate n≤18；本轮 named fixtures 的原始行数最大 15，实际 top subsets 不超过该 gate。

每个 m-row small model 另枚举全部 2^m enabled-origin subsets，把直接 pointwise universal projection 与 cover-clause contraction 对照。随机样本不是普遍证明；它们是 deterministic seeded regressions。初始 p=3 duplicate case 先 benchmark，再运行整个 bounded suite。具体计时记录在 `run_metrics.json`，不参与任何 coverage 判断。

### 10.2 Results

```text
Named ABSTRACT fixtures: 8
Seeded ABSTRACT fixtures: 112, seed 20260906
Complete seeded fixtures: 15
Enabled-subledger / state checks: 182944
Pointwise enabled-subledger projection checks: 120176
All-shared support-triangle assignments: 2989
Fixed-prime primality/order/lifting checks: 14
Actual row-anchor-exponent normal-form checks: 2741640
Assertion failures: 0
```

Triangle enumeration：p=3,beta=1 有 4^3=64 组 primitive shadows；p=3,beta=2 有 13^3=2197；p=5,beta=1 有 6^3=216；p=7,beta=1 有 8^3=512。三条 supports 为 ab、bc、ac 的 minimal proper-slice full frontier 数均为 0。

每个 nonempty cover 检查 exact guard identity、strict support growth、private providers、distinct providers、shared-origin LCA bound、arity charge、lex/integer potential、全 enabled-subledger truth/projection。

深度回归另包括 ternary seven-leaf frontier 及 beta-two dynamic nonsimple center refinement。它们是源文件已有 geometry 的回归，不是本轮新 arithmetic examples。

### 10.3 Actual arithmetic motifs

三组 K=2,E={1},U=L=228470 的共有 residues，全 period、两 anchors、两原始行均由直接 modular powers 对 normal form 验证。

| Motif | (r_67,r_20771) | Sat_67,0 mod3410 | Sat_67,1 mod3410 | safe counts at anchors |
|---|---|---|---|---|
| ALIGNED | (4,20775) | empty | {0} | 218219, 218218 |
| SPLIT | (2,20775) | empty | {1705} | 218219, 218218 |
| PAIRED | (2,13471) | {2728} | {1639} | 218218, 218218 |

SPLIT 在 y=0 的 pooled slices 是 66+1，各 anchor 自己都不 full。Local zero 保持 nonfatal。三个模型均不是 complete certificate。单个 20771 rigid origin 不能构成 source sparse lemma 所要求的 first essential nonlinear multi-origin frontier；这些例子检验 state/guard/type，不提供真实 nonlinear pathology。

复核

\[
\operatorname{ord}_{1645333507}(5)=2\cdot3^3\cdot30469139,
\quad s=2,
\]
\[
\operatorname{ord}_{30469139}(5)=1429\cdot1523,
\quad \operatorname{ord}_{1523}(5)=2\cdot761.
\]

1429、761 都是 1 mod4 prime labels。这里只认证原始 primes/orders/lifting 和 dependency edges；没有枚举巨大 full period，没有声称该 motif 产生 first nonlinear recurrence，也不把尚未加入 ledger 的 relay 当 actual original row。

程序没有 import repository code；直接 bitmask verifier 与 contraction routine 是不同组织方式，但来自同一作者/运行环境，不能称为 independent authors 或完全独立软件栈。

## 11. RELATION TO P4 / TERMINAL HALL

[S8] 的 typed demand grammar 必须保留：A0、A1、EITHER、BOTH 不同。Pooled EITHER root 不能当作两条 fixed-anchor roots。实际 SPLIT 已允许 EITHER 合法变成 TRUE。

本轮 T1–T4 选择 #17 的 fixed anchor/parity，避免把 pooled type 混入证明。若处理 mixed-anchor macro，至少需要按 (q,c) 保存 primitive shadows，并另外保持 q 的 shared state；不可不加修正地使用本报告“每个 q 只有一个固定 p-shadow”的论证。

Hypothetical complete input 必须失败于任何已证明足以构造 escape 的全局 criterion，包括在其适用 boundary/state 上的 allocated full-depth blocker 和 transitive/primed terminal Hall。这些是 whole frozen input 的必要过滤，不能说每个 bare local E_L 或每个 local nonlinear hyperedge 都单独 Hall-deficient。

[S9] 的 terminal Hall 是 sufficient escape criterion，不是完整 guard-forest/coalescing feasibility 的必要条件；匹配失败本身不等于 arithmetic cover 可实现。

T2 的 private-provider matching 与 terminal blocker matching 不是同一个二部图。前者为 actual reached frontier 的几何解释，后者为 original-system escape construction。若要联合，需要证明 frontier provider obligations 确实对应同一组 terminal demands；本轮未证明该 bridge。

## 12. DOES THIS MOVE TOWARD UNIVERSAL FINITE-CERTIFICATE NO-GO?

**推进了 nonlinear accounting，但没有接近到可以宣称 arithmetic closure。**

原来的危险说法是“macro 多了，因此 original resources 多了”。现在可替换为一个可验证的 statement：

> 每次 minimal simultaneous cover 中，各 rigid parent 有一个 private original exact-shadow provider；shared origins 的位置能力被 prefix LCA 严格限制。

这能排除 all-shared cyclic support patterns，并给 arbitrarily nonlinear descendants 的合法 provider tax。与此同时，nested complete partitions 证明该 tax、strict support-profile descent、无状态重选、甚至 disjoint supports/tree provenance 仍可以一起结束于 TRUE。

因此下一步不应继续寻找纯粹的“宏数量下降”或“有限树最后必须矛盾”。应把 regular helper providers 的供给，重新与有限 original rigid origins 的实际 finance/activation 关系相接。是否能做到仍不确定。

## 13. NEXT SINGLE TARGET

**PRIVATE-PROVIDER TO RIGID-ORIGIN CHARGING AT THE FIRST POST-NONLINEAR TERMINAL 3-FRONTIER.**

固定 E_complete-derived 的 first nonlinear output，研究一个实际可达的 rigid-only terminal 3-frontier。对 T2 提供的每个 private original provider q，若 q 是 regular dynamic helper，则沿它被激活并收缩的 exact DAG 向上追溯：能否给这些 private providers 分配彼此不同、或具有明确可证有限负载的 original rigid seed origins？

这个任务必须保留全部 OR alternatives 的同一原始状态、helper activation witnesses 和 lower guards。所需输出是一个真正的 charging theorem，或一个从 actual rows/actual lineages 出发的 provider-financing collision；只有 abstract all-shared triangles或 raw macro count 不再足够。

理由：T2 已经给出前沿上“谁必须私有”，缺的是“这些私有 regular helpers 是否真的需要新 rigid-origin capacity”。这比再次要求一个未定义的 global arithmetic potential 更可检验。

## 14. FINAL REPORT STATUS

```text
RECURSIVE CLOSURE:
NO GENERAL CLOSURE, BUT NEW OBSTRUCTION FOUND

PROVED:
CANONICAL LOG-GUARD SUPPORT IDENTITY
PRIVATE-PROVIDER / PREFIX-LCA OBSTRUCTION
STRICT SUPPORT-PROFILE DESCENT
ARITY-SENSITIVE ORIGINAL-TOKEN PATH CHARGE

NOT PROVED:
ARITHMETIC TERMINAL-TRUE EXCLUSION
PRIVATE-PROVIDER TO DISTINCT RIGID-ORIGIN CHARGING
GENERAL OR NEW NONTRIVIAL-SUBCLASS RECURSIVE CLOSURE
UNIVERSAL FINITE-CERTIFICATE NO-GO

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

“PROVED” 表示本报告给出了上述数学证明和 exact reference checks；不是声称经过独立数学作者审稿、proof assistant 形式化或外部文献优先权审查。
