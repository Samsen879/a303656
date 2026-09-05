# A303656 C=1 TWO-ROOT PROVENANCE OBSTRUCTION — TARGETED PHASE A

## 结论摘要

**本轮证明了一个 genuine arithmetic subclass 的 two-root no-go，而不是所有 finite admitted systems 的 universal no-go。**

核心新结果是 **free-coordinate rigid-blocker theorem**：把每个 original rigid row 分配给其 order 中一个没有 original dynamic row 的奇素数坐标；若每个这样的坐标仍有未被两 anchor 禁止的 digit，就能构造同一个 coarse exponent，避开两个 anchors 的全部 odd-row fatal events。该逃逸点可以沿任意 exact provenance contraction 投影，故两棵树不可能同时到达 covered root。论证不要求共同的 saturation coordinate、lower cylinder 或 contraction tree，因而在该 subclass 中绕过 H1。

特别地，若系统中所有 base-5 nonregular primes 都属于 `{20771,40487}`，则分别用坐标 `5` 和 `653` 排除其 rigid events。其余 regular prime rows 的数量、大小、precision 与 accepted odd valuation sets 均不受额外限制。结合本轮独立重放的既有 `q <= 10^7` inventory，得到：**所有 original odd row primes 不超过 `10^7` 的 finite admitted C=1 certificates 均不可能 complete；precision 不需要有界。** 这不是 A303656 的 representability theorem。

另外完成：三个 original rows 的最小 abstract same-lower-bridge counterexample；state-sensitive provenance / exact CSP；original-resource cardinality–charge obstruction；实际 `(67,20771)` paired-mask quotient 和 full-period replay。

```text
PHASE VERDICT: B. NONTRIVIAL TWO-ROOT INVARIANT PROVED
ADDITIONAL OUTCOMES: C. IMPORTANT NATURAL INVARIANT DISPROVED
                     D. USEFUL FINITE CSP REDUCTION
PROMOTION GATE B: A SUBSTANTIAL FORMAL SUBCLASS TWO-ROOT NO-GO
GATE A / UNIVERSAL FINITE-ADMITTED TWO-ROOT NO-GO: NOT PROVED
```

以上是本阶段的数学分类，不是 repository route promotion。本目录的集成不修改 authority state。

---

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Bound main SHA: 0200beede923c56e0284d9555c1dabaf91fa1755
Bound main tree: 23f10c12181c5caa394f7a3fb1acb6e79cc02fe6
```

Live metadata 和 first-parent ancestry 已核对：

| PR | 已 merge | Merge commit |
|---|---|---|
| #11 | 是 | e9b537f70fb0196b30f5b476b634299b012c369e |
| #12 | 是 | 7786a0b356a790623eb0662b64e84b9c6240edde |
| #13 | 是 | 0200beede923c56e0284d9555c1dabaf91fa1755 |

三者构成 `#11 -> #12 -> #13` 的 main first-parent chain，不是仅检查 PR 的 merged flag。固定 SHA 下的 `STATUS.md` 仍为：

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

### Source-reading 与独立性边界

已通过 GitHub connector 阅读 `STATUS.md`、`docs/THEOREM_INDEX.md`、`docs/ROUTE_MAP.md`，以及六个指定 analysis directories 中用于本轮论证的 original definitions、theorem/proof documents、realizability audit 和三个新 PR 的完整 REPORT。具体文件与已读取的 Git blob IDs 见 `SOURCE_BINDING.json`。旧文件中关于 hereditary closure 尚未解决的历史描述，按 #13 的明确 provenance-cylinder theorem 作时间顺序解释；没有将旧报告悄悄改写。

没有执行整个 repository 的逐文件 archive audit、全部历史 tests 或所有历史 computation。容器未取得完整 Git checkout；GitHub 内容来自 connector 的固定-SHA读取。研究包全部程序是本轮 standalone implementation，不 import repository code。独立性指不同 exact formulations / implementations 的 cross-check，不声称来自不同作者或不同语言软件栈。

---

## 2. FORMAL PAIRED-STATE MODEL

### 2.1 Original arithmetic rows

按 [S1–S5]，`P` 为有限个互异 primes，满足 `p == 3 (mod 4), p != 5`。每个 row 给定 `K_p >= 2`、非空 positive odd valuation set `E_p subset {1,...,K_p-1}`，以及两 anchors 共享的 `r_p mod p^K_p`。

\[
V_{p,c}(d)=r_p-3^c-5^d,\qquad c\in\{0,1\}.
\]

仅当 clipped valuation 是 `E_p` 中的正奇数才 fatal。`V == 0 mod p^K` 是 **local zero**，不 accepted。

\[
w_p=\operatorname{ord}_p(5),\quad s_p=v_p(5^{w_p}-1),\quad
 a_p=\max(0,K_p-s_p),\quad \ell_p=w_pp^{a_p},
\]
\[
U=\operatorname{lcm}(t_2,\{w_p\}),\quad
L=\operatorname{lcm}(t_2,\{\ell_p\}),\quad \beta_p=v_p(U).
\]

可选 sound two-adic row 的 period 是 `t_2=1`（`K_2=2`），否则 `2^(K_2-2)`。没有该 row 时取 `t_2=1`。Coarse fatal 意味着该 `x mod U` 的**全部** full lifts 都被同一 original row 接受。

### 2.2 Triangular events 与两棵树

CRT domain `X(U)=product_l X_l` 的坐标按 prime label 递增。Dynamic row `p` 的最大坐标为 `p`；rigid row `q` 的 customary rank 为 `P^+(w_q)`。因为 `w_q | q-1`，它们是 triangular events。

在 maximal coordinate `p`，写 top events 为 `G_i(y) x A_i(z)`。`G_i` 是 lower CRT guard；`A_i` 是 exact shell bundle 或 rigid cylinder slice。Minimal cover witness 是一个 inclusion-minimal row/macro index set `I`，使 `union_(i in I) A_i=X_p`。

Derived provenance-cylinder macro 记录其 lower cylinder、eliminated coordinate、parents 和 exact covering witness。其几何 slice 可以是 rigid cylinder；它不是 actual prime，不获得新 residue，也不获得额外 capacity。

`Sigma_0` 与 `Sigma_1` 共享 original parameters，但允许不同 eliminated coordinate sets、guards、witnesses、macros 和 descendants。**Branch-local reuse** 是同一已固定 row 在多个证明分支再次被引用，不是重新选一次 residue。

---

## 3. EXISTING FIXED-ANCHOR RESULTS RECONSTRUCTED

[S3, S6] 给出：
\[
\operatorname{Sat}_{p,c}(y)
=\bigvee_{I:\,\cup_{i\in I}A_{i,c}=X_p\;\mathrm{minimal}}
  \bigwedge_{i\in I}G_{i,c}(y).
\]

并且
\[
\forall z\,[\mathrm{Lower}_c(y)\vee\mathrm{Top}_c(y,z)]
=\mathrm{Lower}_c(y)\vee\operatorname{Sat}_{p,c}(y).
\]

这在明确的 provenance-cylinder grammar 内 hereditary exact。它不等于 literal actual-row-only closure。其 consequence 是 fixed-anchor root truth 与 original coverage 等价，而不是 two-root impossibility。

[S4] 的 centered prefix-frontier inverse theorem 只对 exact fiber covers 分类；[S5] 要求每个 original rigid leaf 来自不同实际 nonregular prime，且先选 resource/support rows、诱导最终 `U`，再固定 lower fiber。[S6] 的宏不能被重新套入这份 prime inventory。

[S7] 已证明 odd-row pointwise exclusion：
\[
V_{p,0}(d)-V_{p,1}(d)=2,
\qquad F_{p,0}\cap F_{p,1}=\varnothing.
\]

同一 shared lower assignment 上，original dynamic `p`-row 至多在一个 anchor active。该事实不要求两棵树相同。

旧的 Hall-type demand-capacity inequality 和宏数量可能指数增长也已经在 sources 中出现。本轮不把它们当作新成果。

---

## 4. CANDIDATE INVARIANTS

| 方向 | 本轮判断 |
|---|---|
| A. Paired coverage deficit | Semantic escape-set projection 是有效 invariant，但若不能证明初始 escape 存在，就只是 coverage 的重述。Blocker theorem 提供了一个非空初始 escape construction。 |
| B. Signed anchor imbalance | 单纯正负 row count 不足；state-dependent cardinality–charge 条件可作严格 necessary obstruction。 |
| C. Common-guard intersection | 不应要求两树有共同 proper residual；三行反例排除这种 abstract bridge。 |
| D. Provenance overlap | row ID overlap 不是 conflict。搜索 residues 时必须保留 `(original row, exact paired state)`，而不只保存 ID。 |
| E. Kraft/entropy potential | Raw macro mass 不 conserved；容量应继续计在 original resources 上。 |
| F. Demand-capacity / Hall | 既有容量条件继续有效；新 free-coordinate blocker assignment 是在 original rigid resources 与无 dynamic 的坐标之间作 capacitated assignment。 |

---

## 5. PROVED PAIRED INVARIANTS

### Theorem 1 — free-coordinate paired rigid-blocker escape

固定一个 genuine admitted system 和其 shared residues。令 `R_c` 为 anchor `c` 的 original coarse rigid-fatal rows。为每个 `q in R_0 union R_1` 分配一个奇素数 `b(q)`，满足：

\[
b(q)\mid w_q,\qquad b(q)\notin P.
\]

即 `b(q)` 是真实 exponent coordinate，但没有 prime row 能在这个坐标提供 original dynamic event。若 rigid row `q` 在 anchor `c` 的 fatal class 是 `d == a_(q,c) mod w_q`，定义

\[
B_\lambda=\{a_{q,c}\bmod\lambda:
 b(q)=\lambda,\;q\in R_c,\;c\in\{0,1\}\}.
\]

假设每个已使用的 blocker coordinate 都满足
\[
|B_\lambda|<\lambda.\tag{B}
\]

则对每个预先固定的 coordinate-two assignment，都存在一个 coarse class `x mod U`，使两个 anchors 的**所有 odd rows 均非 coarse fatal**。没有 coordinate two 时省略该参数。

#### Proof

按实际 prime coordinate 递增构造 `x`。

在 blocker coordinate `lambda`，选择第一 digit 不在 `B_lambda` 内。其余高位任意。这样，每个分配给它的 original rigid congruence 在相关 anchor 都不可能成立；这是一个永久 exclusion，不依赖尚未选择的更高坐标。因为 `lambda notin P`，该坐标没有 original dynamic event 与这个选择竞争。

在其他坐标 `p in P`，之前已选定所有 `w_p` 的 prime factors，因此两个 anchor 的 dynamic activity guards 均已确定。共享 residue 的 difference-2 identity 使至多一个 anchor active。若没有 active fatal bundle，任取 digit；若有，只需选在该 bundle 外。这样的 digit 存在：exact dynamic shell bundle 始终遗漏其 unresolved center cylinder。`beta_p=0` 或 empty fatal bundle 时无额外约束。

其他非 row-prime 坐标任取。最后，所有 original rigid events 都已由其 blocker 排除，所有 original dynamic events 都在自己的坐标被避开。Earlier choices 不被 later coordinates 改变，因为 original dynamic dependence triangular，而 rigid exclusion 已违反其必要的一条 congruence。两个 anchors 均 odd-row coarse safe。QED.

#### Paired invariant 的具体内容

在任一 ascending prefix 后：

1. 已经过其 row-prime coordinate 的 original dynamic events，在两个 anchors 都被避开；
2. 已经过其 assigned blocker coordinate 的 original rigid events，在两个 anchors 都被排除；
3. 所有这些 exclusions 对 higher-coordinate extension 稳定。

这是原始行信息的 invariant，不把 derived macro 当新的行。

### Theorem 2 — joint odd-row reverse CRT

若同一 coarse class `x mod U` 在两个 anchors 对每一 odd row 都不是 coarse fatal，则它有同一个 full lift `d mod L`，对两个 anchors 的全部 odd rows 都 safe。

#### Proof

固定 row `p`。因为 `w_p | U`，在全部 `x`-lifts 上，`5^d mod p` 固定。故在这些 lifts 中至多一个 anchor 能有 positive p-divisibility；另一个 anchor 恒非 fatal。Coarse safety 因而提供一个 local lift，同时避开该 row 的两个 anchor events。

Row `p` 的剩余自由指数信息仅在高于 `beta_p` 的 `p`-power digits 中。对于任何别的 row `q != p`，其 `w_q` 所含 `p`-power 已包含在 `U`，所以这些额外 digits 不影响别的 row。不同 original primes 的 private digits 可以由 CRT 合并，且保留 `x mod U`，包括已固定的 two-adic coordinate。所得 full exponent 同时 odd-safe。逆向显然：一个 full safe lift 阻止相应 coarse class 成为任何 row 的 fatal class。QED.

这比仅逐 anchor 使用已有 reverse CRT 多保留了 joint odd safety；证据为 `joint_reverse_crt_checks.json`，证明不依赖有限测试。

### Corollary 2.1 — arbitrary two-adic precision 下的 two-root no-go

在 Theorem 1 的条件下，没有 complete simultaneous C=1 certificate。无 two-adic row 时，Theorem 2 甚至给出两个 anchors 共享的 full odd-safe exponent。

有 sound two-adic row 时，按 [S1–S3] 的 exact two-adic lemma 选择至少一个 safe anchor 与一个 safe exponent class；`K_2=2` 按 constant boundary 处理。将该 class 固定为初始 coordinate-two assignment，再用 Theorems 1–2。最终至少一个 anchor 对全部 local rows safe，因此不可能两个 roots 都 covered。

这里没有声称两个 anchors 必须同时 two-adically safe。

### Theorem 3 — uniform resource-assignment subclass

令 `Q={q in P:s_q>=2}`。这是所有**可能**产生 positive rigid fatal events 的 original row pool；给定参数下部分成员可以 dynamic 或 inert，不妨仍将它们纳入 pool。

若有函数 `b:Q -> {odd primes lambda | U : lambda notin P}`，满足 `b(q)|w_q`，并且
\[
2\,\#\{q:b(q)=\lambda\}<\lambda\qquad\text{for every }\lambda,\tag{U}
\]

则对**全部** precisions、accepted sets 和 shared residues，complete simultaneous certificate 均不可能。

Proof：每个 original row 在每个 anchor 最多提供一个 rigid logarithm class，因此对 `B_lambda` 最多贡献两个 digits。条件 (U) 保证 (B)，然后用 Corollary 2.1。对所有参数的量词顺序是 `for every original parameter assignment, there exists an escape`，不是一个 exponent 必须适用于所有 residues。

这是 capacitated assignment condition：每个 blocker coordinate 提供 `floor((lambda-1)/2)` 个 worst-case paired-row slots，original nonregular row 只能分配给整除其 order 的 blocker。它不消耗或创造宏资源。

单-anchor 变体只需 `#assigned rows < lambda`，可以用于选定的 two-adically safe anchor，得到一个更宽的 sufficient no-go subclass；本轮主要记录更强的 paired-escape conclusion。

### Corollary 3.1 — `{20771,40487}` nonregular pool

本轮以 exact computation 验证：
\[
w_{20771}=5\cdot31\cdot67,\quad s_{20771}=2,
\]
\[
w_{40487}=2\cdot31\cdot653,\quad s_{40487}=2.
\]

选择 `b(20771)=5`、`b(40487)=653`。坐标 `5` 不是 admitted dynamic prime，`653 == 1 mod 4` 也不可能有 admitted dynamic row。两个 blockers 各只分配一个 original row：
\[
|B_5|\le2<5,\qquad |B_{653}|\le2<653.
\]

所以 **任何 finite admitted system，只要其全部 nonregular rows 属于 `{20771,40487}`，两根就不可能同时 covered**。Regular rows 可以任意多、任意大，并可以产生任意深的 ambient support。提升 ambient depth 不会取消上述第一 digit exclusions。

### Corollary 3.2 — 既有 `10^7` panel 的 precision-unbounded no-go

本轮重新完整筛出 `q<=10^7, q prime, q==3 mod4` 的 `332398` 个 candidates，并用
\[
5^{q-1}\equiv1\pmod{q^2}
\]

检测 nonregularity。因 `w_q|q-1` 且 `q` 不整除 `(q-1)/w_q`，该 test 与 `q^2 | 5^w_q-1` 等价。只对 hits 再 exact-reduce order。方法与 source 对每个 prime 都 factor/reduce order 的实现不同。

唯一 hits 正是 `20771,40487`，与 [S5] 一致。因此所有 odd row primes <=`10^7` 的 admitted systems，无论 `K_p` 多大、`E_p` 如何选择、shared residues 如何优化，都不可能构成 complete C=1 local certificate。

有限部分只有 prime inventory；**arbitrary precision / arbitrary shared residues 的结论来自定理，而非枚举**。没有把有限范围内 absence 推广到所有 primes。

### How the escape survives divergent contractions

在整个 original product 上取上述共同 odd-safe 点。对任意 anchor 的 exact contraction，如果其 lower projection 落入 covered residual，则该 lower fiber 的每个 extension 都 covered，与这个点仍是 safe 矛盾。因此 safe point 的 projection 继续为 residual escape。两棵树可以消去不同坐标；分别投影同一个 original witness 即可，不必将 trees 逐 node identify。

加入 two-adic event 后，对选定 safe anchor 继续该 argument 即足以排除 double covered roots。

### Theorem 4 — original-resource cardinality–charge obstruction

这是补充的 finite-state filter，不是上面 blocker theorem 的假设。固定 unmet demand set `D`（two-adic 已覆盖的 demands 可以先删除），exact row states `S_q`，每个 state 的 demand set `F_q(s)`，以及一个 finite abelian group `G` 中的 charge `omega:D -> G`。

定义
\[
C_q=\{(|F_q(s)|,\sum_{u\in F_q(s)}\omega(u)):s\in S_q\},
\quad C=C_1+\cdots+C_r.
\]

若 cover 存在，则 `C` 中必有一个 `(m,g)`，满足
\[
m\ge|D|,\qquad g-\sum_{u\in D}\omega(u)
\in \underbrace{\Omega+\cdots+\Omega}_{m-|D|\ \mathrm{terms}},
\quad\Omega=\{\omega(u):u\in D\}.\tag{C}
\]

零个 terms 的 sumset 为 `{0}`。

Proof：若 incidence multiplicity 为 `n(u)>=1`，则 `m-|D|=sum_u(n(u)-1)`，而 charge difference 为 `sum_u(n(u)-1)omega(u)`，恰有这么多 excess incidence terms。QED.

特别当 `sum_q max_s |F_q(s)|=|D|` 时，每个 selected row 必须达到 maximum capacity，且 selected sets 必须 partition `D`，故 total charge 必须恰好等于 demand charge。

非平凡例子：`D={0,1} x Z/n`，`n` rows，每行选择 `a_i`，覆盖 `(0,a_i)` 与 `(1,a_i+delta_i)`，`delta_i !=0`。两层都覆盖迫使两组 positions 都为 permutations，从而
\[
\sum_i\delta_i=0\pmod n.
\]

`n=3, delta=(1,1,2)` 因 charge 非零而 impossible；两个 anchors 各自均可 covered。将 domain 复制为 `2 x 3` 可得到要求中的 triangular small-domain example。

条件 (C) 是必要而非充分。独立反例关系 `R1={(0,1),(0,2)}`, `R2={(0,1),(1,0)}`, `R3={(0,1),(2,0)}` 各 anchor 有两种 complete assignments，charge filter passes，但 joint cover 不存在。数据见 `cardinality_charge_filter.json`。

---

## 6. FAILED INVARIANTS + COUNTEREXAMPLES

### 6.1 I2 / I3 / I4：三行、`2 x 2` 的 exact abstract counterexample

令 `X={0,1} x {0,1}`，第一 coordinate 为 `x`，第二为 `y`：

| Original row | Anchor 0 fatal event | Anchor 1 fatal event |
|---|---|---|
| L | `x=0` | `x=1` |
| U | `(x,y)=(1,0)` | `(x,y)=(0,0)` |
| V | `(x,y)=(1,1)` | `(x,y)=(0,1)` |

每个 row 的两个 events 都不相交，且其 rank 不随 anchor 改变。两个 anchors 都是 exact partition。两个 roots 的唯一 minimal original-row support 都是 `{L,U,V}`，所以 **provenance overlap 并不自动产生 conflict**。

但 original top-rank saturation 是
\[
\operatorname{Sat}_{y,0}=\{1\},\qquad
\operatorname{Sat}_{y,1}=\{0\}.
\]

它们无共同 lower assignment。Original rank-`x` family 在每个 anchor 都只有 `L` 的一半 domain，也不 full。因此不存在 same-lower original-rank full fiber。最后一步两个 roots 都 true，不会补回一个共同的 proper nonterminal residual。

这里反驳的 I3 是有意义的 **rank-specific original-row bridge**。若把 lower rows 一起算入每个 fiber，则 whole-product coverage 本来就使每个 fiber full；那不是 H1。

#### Minimality scope

枚举的 grammar 是：`2 x 2` 上所有 proper product cylinders（每个 coordinate 为 singleton 或 whole），可为空；每对 row events pointwise disjoint；允许不同 original rows 有相同 geometry。按 row permutation 去重枚举。

| Grammar | Paired row catalog | 2-row systems / double roots | 3-row systems / double roots | 3-row double roots without a common original-rank fiber |
|---|---:|---:|---:|---:|
| Anchor ranks 可变 | 48 | 1176 / 2 | 19600 / 384 | 112 |
| 每 row 的 nonempty rank 固定 | 40 | 820 / 2 | 11480 / 188 | 20 |

两行不足的解析理由也很短：每个 proper rectangle 至多有两个 cells，两个 rows 要 complete 必须是互补 parallel strips。Pointwise exclusion 再迫使另一个 anchor 使用同一 strip partition 但交换 rows。因此必有共同 original saturation rank/fiber。三行达到上述反例。

**这只是该明确 abstract grammar 的 minimality，不是 actual prime realization，更不是 genuine arithmetic H1 的反例。**

### 6.2 I1 的语义限制

强制两棵树都消去相同 ambient coordinates 时，“都出现同一个 coordinate label”是语法事实，不能被反例推翻。若 I1 指“两个 anchors 的 original row systems 必须在某个相同 rank saturation”，则三行 variable-rank example 已反驳：

`A: x=0 / (x,y)=(1,0)`；`B: x=1 / (x,y)=(0,0)`；`C: empty / y=1`。

Anchor 0 仅 original rank `x` saturated，anchor 1 仅 original rank `y` saturated。其 descendants 可以再次出现共同 coordinate，不能声称反驳所有可能的 I1 表述。

### 6.3 I5：macro count 不是 original resource count

在 binary top fiber 上给两个 distinct original rows slice `{0}`，三个 rows slice `{1}`，lower guards 都为 whole。产生 `2*3=6` 个 minimal cover witnesses，来自仅五个 original rows。两 anchors 对调 digits 还可满足 rowwise exclusion。

Geometry 去重后可仅剩一个 full lower cylinder；provenance 则有六种不同 witness alternatives。五行是该 binary singleton one-step grammar 中 `number of minimal cover clauses > number of rows` 的最小 covered example，因为 `floor(r^2/4)<=r` 对 `r<=4` 成立。更一般的 exponential bound 已属 [S6]，本例是 bookkeeping regression。

### 6.4 I6：naive Kraft mass 不守恒

两个 `{0}` rows 加一个 `{1}` row，给出 covered binary fiber。每 anchor 原始 mass sum 为 `3/2`；两个 provenance macros 的 sum 为 `2`；按 geometry 去重后 mass 为 `1`。因此三种计数不能被当成同一个 conserved quantity。两行 complementary partition 的 covered case 守恒，三行是此 binary covered grammar 的最小非平凡失败。

更小的 incomplete 单行 `1/2 -> 0` 当然已使无条件 mass preservation 失败；不能隐藏这个平凡更小反例。

---

## 7. BOOLEAN/CSP FORMULATION

### 7.1 Exact arithmetic allowed states

冻结 actual primes、precisions、accepted sets、ambient periods。定义
\[
r\sim_q r'\iff(F_{q,0}(r),F_{q,1}(r))=(F_{q,0}(r'),F_{q,1}(r')).
\]

`S_q` 是所有 residues 的 paired-mask equivalence classes，每类保存一个实际 representative 和精确 multiplicity。不能把两个 anchor 的 masks 独立选择；它们共同来自一个 state。改变 residue 不改变 `U,L`，因此该 quotient 不暗中修改 ambient support。

令 `z_(q,s)` 表示 original row `q` 选择 state `s`，每行 exactly one。对 demand `(c,x)`：
\[
P_{c,x}=\bigvee_{q,s:\,x\in F_{q,c}(s)}z_{q,s}.
\]

两根同时 covered 等价于
\[
\exists(s_q)_q\in\prod_q S_q:\quad
\bigwedge_x P_{0,x}\ \wedge\ \bigwedge_x P_{1,x}=1.
\]

可选 two-adic event 以正确的 fixed predicate 加入 demands；若其参数也需搜索，独立建立 exact two-adic state selector。程序中的 generic CSP experiments 不含 two-adic row；上述数学 formulation 可以包含它。

### 7.2 State-sensitive provenance algebra

Monomial 为 partial assignment token set `{(q,s),...}`。OR 合并 alternatives 并删除含冗余 superset 的 terms；AND 取 compatible union。同一 row 不同 states 相乘为零：
\[
z_{q,s}z_{q,t}=0\quad(s\ne t),\qquad z_{q,s}^2=z_{q,s}.
\]

这允许相同 state 在不同 branches 重复使用，同时禁止 residue 随 branch 改变。

实现保留的是 inclusion-minimal **consistent derivation monomials**。它不声称仅靠 subset absorption 就找到了 one-hot 约束下全部语义 prime implicants；例如 `OR_(s in S_q) z_(q,s)` 在 complete assignments 上为 true，但实现未必化简成空 monomial。此限制只影响压缩程度，不影响 exact truth。

### 7.3 不假定共同树的 exact relation invariant

这里 `F_c` 表示所有 original events（及适用的 two-adic event）的 OR，即总 coverage predicate。对已消去坐标集 `J_c` 定义
\[
\Phi_{c,J_c}(y;s)=\bigwedge_{z\in X_{J_c}}F_c(y,z;s).
\]

任意 exact contraction 只是继续执行这些 universal products。保留所有剩余 coordinate quantifiers 后，可行的 original-state relation
\[
\mathcal J=\{s:\forall y\,\Phi_{0,J_0}(y;s)=1,
                     \forall y'\,\Phi_{1,J_1}(y';s)=1\}
\]

不变，即使 `J_0 != J_1`。这一 invariant 对 whole residual predicate / correctly aggregated branch frontier 成立，不声称任取一个 child cylinder 都单独保持 whole-root feasibility。

Blocker theorem 对其 subclass 证明 `J=empty`；一般情况下，这个 exact formulation 本身不证明 unsatisfiability。

### 7.4 Geometry-only 与 provenance-preserving 的正确比较

在 original states 已 frozen 时，两种 exact implementations 的 root truth **必须一致**；没有正确的“geometry 说 covered、provenance 说 uncovered”的差异。

真正危险的 relaxation 是把 `R_q` 换成独立 marginals，或仅保留 `F_(q,0) intersect F_(q,1)=empty`。`delta=(1,1,2)` 的 exact translation relations 有 `3^3=27` assignments，joint cover 为零；替换成全部 off-diagonal pairs 后有 `6^3=216` assignments，joint covers 为 `12`。两者仍满足 pointwise exclusion，但后者允许了新的 paired states。

---

## 8. INDEPENDENT EXACT COMPUTATION

所有 mathematical operations 使用 integers、bitsets、sets 或 exact fractions；不使用 floating point。

| Audit | 范围 | 结果 |
|---|---|---|
| Frozen-row root checks | 六个指定 domains；各250 unrestricted与250 pointwise-exclusive systems，共3000 paired systems、6000 roots | Direct enabled-row truth tables 与 recursive provenance minimal supports 完全一致；geometry truth 一致 |
| Enabled-row assignments | 上述 samples 中全部 `2^r` subfamilies，两 anchors 合计124704 | 0 mismatches |
| Minimality enumeration | `2 x 2`，两种明确 grammars，全部0–3 row multisets | 三行最小 counterexample，具体 counts 见第6节 |
| State-sensitive CSP | 300 stateful systems，7146 complete state assignments | Direct original-system enumeration 与 symbolic roots 一致 |
| Charge filter | 600 stateful systems | 0 unsound rejections；也明确保存 filter passes 但 CSP UNSAT 的例子 |
| Constructive blocker | `3 x 5 x 7` abstract normal form，1190 paired rigid states、124950 whole-product cells | 构造的共同 odd-safe 点均通过独立 direct enumeration |
| Joint reverse CRT | 240 actual small-prime residue/valuation systems；3120 coarse classes，183600 full-period cells | 0 mismatches |
| Actual pair | 两个 shared-residue witnesses，每个228470 exponents、两个 anchors | Guard/slice formulas、direct valuations、recursive roots 一致 |
| Frozen inventory replay | 全部332398 admitted primes <=10^7 | 仅20771与40487 nonregular |
| Unit tests | 见 tests/test_reference.py | 全部通过；覆盖 local zero、state conflict、branch reuse、deeper odd shells |

`direct_check.py` 不调用 contraction 的 slice-cover routine，直接枚举 original event sets 和 enabled-row subsets。Stateful direct CSP 也不调用 symbolic provenance operations。二者由本轮同一实验环境实现，故不称为 independent authors/software stacks。

Minimality 枚举中所有系统先作 direct coverage 检查，joint-covered 系统再运行完整 contraction/subfamily checks；没有声称对该枚举中每一个 noncover 也重复运行 contraction。六-domain sample suite 则对每一个 sampled system 都 cross-check。

---

## 9. ACTUAL-ARITHMETIC REPLAY

### 9.1 原 `(67,20771)` witnesses

`K_67=K_20771=2, E={1}`，`U=L=228470`，lower period `3410`。Source [S7] 的两个例子独立复算为：

| `r_67,r_20771` | `Sat_67,0` | `Sat_67,1` | 每 anchor safe exponents | Minimum joint fiber holes |
|---|---:|---:|---:|---:|
| `2,13471` | `{2728}` | `{1639}` | 218218 | 67 |
| `0,4494` | `{2431}` | `{106}` | 218218 | 66 |

每个 selected fiber 都是 exact `66+1` partition，dynamic center 是本行 local zero，仅由 rigid row 覆盖。两例 root 均 uncovered。

Independent hash join 与 nested join 同时重现 `603` shared dynamic center states、`5192` rigid class pairs、`693` 双 anchor pointwise alignment combinations、`692` distinct ordered lower pairs，same-lower count 为零。`693*20769=14392917` 是 pointwise 双 fiber 的 full residue systems 数量，不是 complete certificates 数量。

### 9.2 Exact residue quotient：按 p-adic center trie 消去无关 residue freedom

固定 row 的 local period `ell`，把所有 targets
\[
T_{c,d}=3^c+5^d\pmod{p^K}
\]

放入 low-digit-first p-adic trie。在深度 `h` 的 node，未出现的 next digits 都使剩余 targets 恰好有 valuation `h`，因此形成一个带精确 multiplicity 的等价 bucket；出现的 digits 递归。到 depth `K` 的 matching targets 是 local zeros，保持 nonaccepted。最后合并相同 paired masks。

若 distinct targets 数量为 `C`，trie nodes 和 pre-merge emitted buckets 均不超过 `1+K*C`，且 `C<=2*ell`。这是 output-sensitive finite reduction，不是对 `log p,K` 的 polynomial-time 宣称；`ell` 本身可以很大。

| Original row | Raw residues | Exact paired states | Inclusion-maximal states |
|---|---:|---:|---:|
| `67, K=2` | 4489 | 2346 | 2345 |
| `20771, K=2` | 431434441 | 25963 | 15578 |

完整 paired-state catalogs 保存代表 residue、两个 event signatures 和该 class 的 exact residue count。对 `67` 逐个枚举全部4489 residues 作独立检查；对 `20771` 用全部20771 low digits 及每个 low digit 至多两个 exceptional zero lifts 作另一种 exact partition。每个 state 的 mask 和 multiplicity 均一致。

Raw pair space 为 `1936709205649`；exact quotient product 为 `60909198`；positive-cover dominance pruning 后为 `36530410`。**这些是 state-space cardinalities，不是已经穷举的完整 systems 数量。** Blocker theorem 已直接排除该 pair 的全部参数，不需要执行这三千多万 state combinations。

Dominance pruning 只适用于纯 positive coverage existence：若同一 actual row 的一个 realizable paired state 在两个 anchors 都包含另一个，则可替换而不会减少 coverage。附加 prescribed role/absence constraints 后不能不加检查地使用。

---

## 10. INTERFACE WITH RESOURCE THEOREM

| 本轮对象 | 类型 | 允许的使用 |
|---|---|---|
| `q=20771` 或 `40487`，带 order 与 shared state | ORIGINAL PRIME RESOURCE | 分配到整除其 order 的 free coordinate，至多贡献两个 forbidden first digits |
| 某 `Sat_p` 的 CRT conjunction | DERIVED MACRO | 只表示 exact residual coverage；不得创造新的 forbidden-digit/prime capacity |
| `{(q,s),...}` 与其 parent witnesses | MIXED PROVENANCE CLAUSE | 检查 original state consistency；不按 monomial 次数重复计资源 |

[S5] 的 distinct rigid-prime inventory 仍是关于 original rows 的结论。本轮 blocker theorem 正是直接作用于这个层面。其 regular-support robustness 解释了为何加入更多 regular rows 或增加 `beta`，不能修复上述被 free coordinates 排除的 rigid pool。

---

## 11. STRONGEST DERIVED COROLLARY

> 对任何有限 admitted prime set `P`，若每个 nonregular original row 都可按 Theorem 3 分配给足够有余量的 odd coordinate，而该 coordinate 没有 original dynamic row，则不存在 complete C=1 shared-residue certificate。允许 arbitrary precision、accepted positive odd valuations、regular support rows 及 sound two-adic row。

明确实例是 nonregular pool contained in `{20771,40487}`，以及其 consequence：所有 odd row primes <=`10^7` 的 finite panels。该结论不只是“若干选定 residues 的 solver UNSAT”，也不是扩大 prime scan 的经验判断。

它只排除这一 formal local-certificate class。**不证明所有 `n>1` 都有目标表示，不证明不存在真实 counterexample，也不改变 A303656 的 UNRESOLVED 状态。**

---

## 12. DOES THIS BYPASS H1?

**在 blocker subclass 内：是。** 证明直接构造 original-system escape，并沿两条各自的 exact contractions 保留其 projection。既不推出也不使用 same-lower simultaneous saturated fiber。

**对全部 genuine finite admitted systems：尚未。** Abstract 三行例子只说明不能从 pointwise exclusion 与粗糙 provenance 推出 H1；它不反驳真正 arithmetic class 内尚未建立的 H1。Exact CSP 在 formulation 层面也不依赖 H1，但一般仍需证明其 feasible state relation 为空。

---

## 13. REMAINING GAP

Blocker availability 不是 universal arithmetic fact。Repository 已记录的更大 nonregular prime
\[
q=1645333507,\qquad w_q=1645333506=2\cdot3^3\cdot30469139
\]

在本轮再次验证 primality、exact order 和 `s_q=2`。它没有 universally non-admitted 的 odd order factor：`3` 和 `30469139` 都是 admitted prime labels。若 panel 包含这两个 dynamic row primes，不能用本轮的结构性 free-coordinate assignment 直接排除它；若 panel 缺其中一个，则仍可能使用 panel-relative blocker。

这不是 complete certificate，也不是 theorem 的反例；它明确表明不能把 `10^7` corollary 推广到所有 primes。

此外，一般的 state-sensitive polynomial 可以指数膨胀，cardinality–charge filter 不是充分条件，partial-assignment antichain 不等于全部 one-hot semantic prime implicants，actual inverse-frontier resource class 也未被本轮完整分类。

本轮没有另行构造更大的 complete actual-prime system，没有枚举任意 many-row residue panels，没有进行整个 repository archive/CI audit。

---

## 14. RECOMMENDED NEXT PHASE

推荐执行环境：网页端 Pro 做 theorem/referee 与独立 reference computation；通过一个明确的 nontrivial arithmetic gate 后，再由普通 Codex CLI 做 repository-native integration/reproduction。无依据启用大规模 Ultra scan。

下一个单一目标应是 **blocker-deficient core theorem**：把没有 free-coordinate assignment 的 original nonregular rows 抽出，保留 exact shared-state relation，证明这些核心是否仍产生 state-sensitive charge/Hall obstruction。先用现有 `1645333507` resource 的 order-support graph 作 theorem-level boundary case，不枚举其巨大 full period。只有一个 panel 确实未被 blocker theorem、旧的 scalar deficit 或 elementary global mass 排除时，才值得生成其 compressed arithmetic CSP。

若需要 repository integration，应单独审阅本包中 Theorems 1–3 的 quantifiers、joint reverse CRT proof、bounded inventory implication 与 numerical catalogs；本轮未执行 integration。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

---

## Source key

所有引用绑定到第1节的 main SHA；精确路径及 blob IDs 见 `SOURCE_BINDING.json`。

- [S1] `c1_entangled_coordinate_deficit/FORMAL_CLASS.md` 和 `THEOREM_AUDIT.md`。
- [S2] `c1_contraction_tree_phase_a/DEFINITIONS.md`。
- [S3] `c1_contraction_tree_phase_a/THEOREM_AUDIT.md`。
- [S4] `c1_minimal_saturated_coordinate_inverse/.../DEFINITIONS.md`, `ABSTRACT_CLASSIFICATION.md`, `REALIZABILITY_AUDIT.md`。
- [S5] `c1_prefix_frontier_realizability_phase_a/REPORT.md`。
- [S6] `c1_hereditary_shell_phase_a/REPORT.md`。
- [S7] `c1_two_anchor_common_residue_phase_a/REPORT.md`。

Theorems 1–4、上述 blocker corollaries、state quotient implementation 与新的 small-model counterexamples 是本轮的推导/计算，不是声称从 sources 逐字摘出的既有成果。未作整个数学文献的 novelty claim。
