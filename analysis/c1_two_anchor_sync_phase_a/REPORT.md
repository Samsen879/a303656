# A303656 C=1 TWO-ANCHOR SYNCHRONIZATION BRIDGE — TARGETED PHASE A

## 结论摘要

**PHASE VERDICT: C. WEAKER USEFUL BRIDGE FOUND。**

另有 **D. STRUCTURAL NEGATIVE RESULT**，严格限于明确定义的 abstract finite triangular paired model。

本轮的主要结果不是“actual H1 已反驳”，而是以下三件事：

1. 证明 **maximal-original-coordinate survivor dichotomy**：complete simultaneous system 在最高原始事件坐标上，必须出现共同 full fiber，或者两 anchors 的 lower events 合并后已经覆盖全部 lower domain。
2. 将该 alternative 与 #11 的 dynamic exclusion / rigid-frontier tax 组合，得到一个可以用 exact rational inequalities 检查的 **pooled-lower-deficit / top-rigid-deficit no-go class**。
3. 构造 complete abstract systems，证明 H1、H2 和一种精确定义的 minimal-provenance witness collision，不能仅从 triangularity、shared row identities、rowwise anchor exclusion、finite completeness 推出。另构造 actual arithmetic **local split**，表明 first common greedy divergence 不必是任何一个 anchor 的 full fiber。

所有“新”均指相对于本轮读取的 current-main theorem ladder 的推导；没有声称完成外部文献的新颖性检索，也没有声称经 proof assistant 形式化。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

---

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Frozen current main SHA: 0200beede923c56e0284d9555c1dabaf91fa1755
Frozen current main tree: 23f10c12181c5caa394f7a3fb1acb6e79cc02fe6
```

本轮重新读取了 branch metadata、三个 PR 的 live metadata、固定 SHA 下的 `STATUS.md`。三者均为 `closed / merged:true / draft:false`。

| PR | merge commit | merge 时间，UTC |
|---|---|---|
| #11 | `e9b537f70fb0196b30f5b476b634299b012c369e` | 2026-09-05 05:57:18 |
| #12 | `7786a0b356a790623eb0662b64e84b9c6240edde` | 2026-09-05 06:00:36 |
| #13 | `0200beede923c56e0284d9555c1dabaf91fa1755` | 2026-09-05 06:04:06 |

Git parent metadata 确认 ancestry：

```text
0200beed... -> 7786a0b3... -> e9b537f7...
    #13           #12           #11
```

`STATUS.md` 的 paused/unresolved 状态没有变化。这里的 Phase verdict 不是 repository route promotion。

### 阅读和计算边界

已读取 `STATUS.md`、`docs/THEOREM_INDEX.md`、`docs/ROUTE_MAP.md`，以及六个指定 analysis directories 中的核心原始 definitions、theorem proofs、realizability proofs 和三个新 PR 的数学报告。精确 paths、blob identifiers、读取范围见 `results/source_binding.json`。

没有宣称逐项检查全部大型 generated catalogs，也没有运行 repository implementation。本轮 numerical claims 来自新写的 `tools/reference.py`；本次 integration 另行运行 repository verification。源代码、结果、原仓库数据之间的区别必须保留。

---

## 2. RECONSTRUCTED THEOREM LADDER

### 2.1 Actual admitted arithmetic rows

原始 odd row 由一个不同于其他 rows 的实际 prime q 指定，满足 q ≡ 3 (mod 4)。数据为

\[
K_q\ge2,\qquad r_q\pmod {q^{K_q}},\qquad
\varnothing\ne E_q\subset\{1,3,5,\ldots\}\cap[1,K_q-1].
\]

两 anchors c=0,1 使用同一个 residue r_q。定义

\[
V_{q,c}(d)=r_q-3^c-5^d.
\]

只有正的 accepted odd valuation 才 fatal。`V ≡ 0 (mod q^K)` 是 unresolved local zero，不能当作 valuation K 或 accepted event。

\[
w_q=\operatorname{ord}_q(5),\quad
s_q=v_q(5^{w_q}-1),\quad
a_q=\max(0,K_q-s_q),\quad
\ell_q=w_q q^{a_q}.
\]

若有 sound two-adic row，令 t₂=1（K₂=2），否则 t₂=2^(K₂−2)。没有该 row 时也取 t₂=1。于是

\[
U=\operatorname{lcm}(t_2,\{w_q\}),\qquad
L=\operatorname{lcm}(t_2,\{\ell_q\}),\qquad
\beta_p=v_p(U).
\]

**coarse fatal** 的量词是：该 coarse class 的每个 full lift 都被同一个 row 接受。原仓库 reverse CRT 定理给出 fixed-anchor coarse escape 与 full-period escape 的等价。

### 2.2 Triangular rank 与 exact slices

因 w_q | q−1，每个 l | w_q 都满足 l<q。

Dynamic row q 的 rank 是 q；其 lower guard 是 logarithm class modulo w_q。在自己的 coordinate 上，设

\[
m=\min(a_q,\beta_q),\qquad
J=\{0\le j<m:s_q+j\in E_q\}.
\]

fatal slice 是固定 center ζ 周围的 shell union

\[
\bigcup_{j\in J}\{z:v_q(z-\zeta)=j\}.
\]

center cylinder z ≡ ζ (mod q^m) 不 fatal。其 exact mass 为

\[
\rho_{q,c}=\sum_{j\in J}\frac{q-1}{q^{j+1}}.
\]

Rigid fatal row q 只有在 accepted h<s_q 时出现，因而需要 s_q≥2。它是一个 class modulo w_q，rank 为 p=P⁺(w_q)。固定全部 lower coordinates 后，其 slice 是一个 depth-e cylinder，e=v_p(w_q)，mass p^(−e)。

同一个 actual row 在不同 anchors 的分类可能不同；本报告中的 rank、D、R 都按实际 anchor-specific event 分类，不把一边的分类无条件复制到另一边。

### 2.3 原有结论与边界

原仓库已经证明：

- Fixed-anchor coordinate strict deficit 给出 greedy escape。
- Complete simultaneous certificate 对 two-adic lemma 所选的 anchor，强迫至少一个 **original-row actual odd full fiber**。
- Irredundant full fiber 有 centered prefix-frontier classification。
- #11：同一个 odd row 在同一个 exponent 上不能对两 anchors 同时正整除；所以共同 lower assignment 下，dynamic p-row 至多在一个 anchor active。
- #11：共同 full p-fiber 必有一个 rigid-only anchor；该 anchor 至少需要 p 个 distinct actual rigid rows，并须满足完整 prefix-frontier coverage。
- #12：one-anchor fiberwise arithmetic realization 必须通过 dynamic parity、distinct nonregular-prime leaf inventory、final induced ambient-depth 三道条件。
- #13：`Sat_p = union_I intersection_(i in I) G_i`，其中 I 是 exact minimal slice-cover witness；它给出 hereditary provenance-cylinder contraction。

必须始终区分：

```text
rational mass saturation
!= original-row actual full fiber
!= one-anchor arithmetic realization
!= same-lower two-anchor realization
!= separate anchor-tagged provenance contraction
!= complete simultaneous certificate.
```

Derived macro 可以在下一步表现为 geometric rigid cylinder，但不是 actual prime row。

---

## 3. CANDIDATE BRIDGES TESTED

以下 H1/H2 的 Sat 仅使用原始 rank events，不把 already-covered lower event 当作当前坐标 saturation。令 S_{p,c} 为 anchor c 的 original rank-p saturation set。

### H1

\[
\forall\mathcal S,\quad
\operatorname{Complete}_0(\mathcal S)\land\operatorname{Complete}_1(\mathcal S)
\Longrightarrow
\exists p\text{ odd}\ \exists y:\ y\in S_{p,0}\cap S_{p,1}.
\]

**Abstract paired triangular class: DISPROVED ABSTRACTLY。**

**Actual admitted arithmetic class: OPEN AFTER TARGETED SEARCH。**

### H2

\[
\operatorname{Complete}_{0,1}(\mathcal S)
\Longrightarrow
\exists p\text{ odd}:\ S_{p,0}\ne\varnothing\land S_{p,1}\ne\varnothing.
\]

结论同上。独立 fixed-anchor greedy theorem 只给出两个 existential coordinates；没有理由令它们相等。Counterexample R 给出完整反例，不是把原有 incomplete pair example 误用为反例。

### H3：非平凡 common-prefix 版本

一个可检验的版本必须事先指定非平凡 quotient π_M:Y→Z/MZ，要求

\[
\exists p, y_0\in S_{p,0},y_1\in S_{p,1}:\quad
\pi_M(y_0)=\pi_M(y_1),\quad M>1.
\]

不能把 M=1、整个 lower domain 或事后不受限制选出的 cylinder 当作 substantive synchronization。

对固定的非平凡 modulus，下面的 nested family 可令两个 singleton saturation sets 的差不为 0 mod M。更强地，选择 a−b 与 lower modulus m 互素，则对任何非平凡 divisor M|m 都不可能同余。因此该非平凡 quotient 版本 **DISPROVED ABSTRACTLY**。Actual class **OPEN AFTER TARGETED SEARCH**。

### H4：预先约束的 separation

在固定 lower cyclic domain Z/mZ 中，预先指定 proper subset D，要求某对 saturation witnesses 满足 y₀−y₁∈D。

Nested family 实现 Z/mZ 的每一种差值，因而不存在独立于系统的 proper allowed-difference set。该版本 **DISPROVED ABSTRACTLY**。

“存在某个依赖系统而任意选择的 coset 包含差值”没有限制力，因为 singleton coset 总是可以事后选择。对未明确 complexity 参数的“low-complexity relation”不作含糊真假判断。Actual nontrivial variants **OPEN AFTER TARGETED SEARCH**。

### H5：nontrivial minimal witness collision

精确定义为：对每个 complete system，存在分别属于两个 anchors 的 #13 类型 maximal-coordinate、inclusion-minimal slice-cover provenance trees，并存在两个非平凡 nodes，其 original-row cover-witness supports 相同。这里限定的是该 tree grammar，不是允许任意 redundant padding 的 proof encoding。

Counterexample R 的两边唯一 minimal global covers 分别是 A-family 和 B-family；maximal-coordinate provenance contraction 也只产生各自不同的非平凡 witness。故该版本 **DISPROVED ABSTRACTLY**。

若允许把无关 rows 任意加进 witness，或者把 entire original row list、covered root 当作“shared witness”，则相同标签可以人为制造，不能用于 rigid-resource obstruction。

Actual admitted class 的 substantive H5 **OPEN AFTER TARGETED SEARCH**。

---

## 4. PROVED RESULTS

### Theorem S1 — maximal-original-coordinate survivor dichotomy

考虑两 anchors 上的有限 triangular **original** event system。令 p 为所有非空 original odd events 中的最大 rank。若 ambient U 含有更高但对这些 events inert 的 coordinates，忽略这些 inert coordinates，不改变 coverage。

令 Y 为全部低于 p 的 coordinates，X_p=Z/p^βZ。定义

\[
A_c(y)=\text{“某个 rank 小于 p 的 original event 已覆盖 y”},
\]

其中 A_c 包含 two-adic predicate；定义

\[
B_c(y,z)=\text{“某个 original rank-p event 覆盖 }(y,z)\text{”},
\]

\[
S_c=\{y:\forall z\in X_p,\ B_c(y,z)\},\qquad
C_p=Y\setminus(A_0\cup A_1).
\]

这里 A_c 也表示其 truth set。

**若系统 complete at both anchors，则**

\[
Y\setminus A_c\subseteq S_c\quad(c=0,1),\qquad
\boxed{C_p\subseteq S_0\cap S_1.}
\]

特别地，

\[
\boxed{\operatorname{Complete}_{0,1}
\Longrightarrow
[S_0\cap S_1\ne\varnothing]\ \lor\ [A_0\cup A_1=Y].}
\]

#### 证明

p 是最高 original event rank，所以固定 y 后，anchor c 的每个 cell 只能由 A_c 或 B_c 覆盖。Completeness 等价于

\[
\forall y\ \forall z:\ A_c(y)\lor B_c(y,z).
\]

A_c 与 z 无关，因此等价于

\[
\forall y:\ A_c(y)\lor[y\in S_c].
\]

若 y 避开 A₀ 和 A₁，就同时属于 S₀、S₁。若 S₀∩S₁ 为空，则没有共同 lower survivor，故 A₀∪A₁=Y。证毕。

**范围：**这是一个 unconditional alternative，不是“completeness 自动产生 common lower survivor”。第二分支是真正可能的 abstract 完整模型现象，不能删掉。反方向 `pooled lower cover ⇒ complete simultaneous cover` 不成立。

### Theorem S2 — genuine paired greedy first-stop trichotomy

从一个 common-safe boundary 开始。在共同 lower prefix y 处，令

\[
E_c(y)=X_p\setminus\{z:B_c(y,z)\}.
\]

只要 E₀∩E₁ 非空，就选择其中一个共同 digit。第一次无法继续时恰为：

| 类型 | 条件 |
|---|---|
| JOINT_FULL | E₀=E₁=∅ |
| SINGLE_FULL | 恰有一个 E_c=∅ |
| SPLIT | 两者非空，但 E₀∩E₁=∅ |

若原系统 complete，则该过程不可能到达 common escape，因此必在有限坐标内停下。

这不是 pigeonhole 的近似结论，而是两个 finite escape sets 的穷尽分类。只有第一类直接允许应用 #11 的共同 full-fiber tax。SPLIT 只给出 B₀∪B₁=X_p，不能交换成 B₀=B₁=X_p。

允许在 SPLIT 后选不同 digits，只会产生两条各自合法的 greedy paths；没有新的共同 lower invariant。下面的 actual 67/20771 construction 证明 SPLIT 并不被原始局部算术排除。

### Theorem S3 — pooled-lower-deficit / top-rigid-deficit no-go

仍使用 original events 和 S1 的最大 odd rank p。按仓库定义令 D_{l,c} 是 dynamic l-row 的完整 conditional shell mass（没有该事件时为 0），R_{l,c} 是所有 original rigid fatal rows assigned to l 的 cylinder masses 之和。

假设：

**Boundary gate.** 存在一个 two-adic coordinate value，使两 anchors 的 two-adic predicates 同时 safe；无 two-adic row 时自动成立。

**Pooled lower gate.** 对每个 odd l<p，

\[
\boxed{\max(D_{l,0},D_{l,1})+R_{l,0}+R_{l,1}<1.}\tag{PL}
\]

**Top rigid gate.**

\[
\boxed{R_{p,0}<1,\qquad R_{p,1}<1.}\tag{TR}
\]

则该系统不可能是 complete simultaneous certificate。

#### 证明

先选择 common-safe two-adic digit。按 increasing odd coordinates 选择共同 lower digits。

在 l 的共同 lower prefix 上，#11 保证原始 dynamic l-row 在两 anchors 至多一边 active。因此两边 dynamic union 的 mass 不超过 max(D_{l,0},D_{l,1})，不是二者之和。Rigid union 的 mass 不超过 R_{l,0}+R_{l,1}。由 (PL)，该 pooled union 不覆盖整个 l-coordinate，可以继续选共同 escape digit。

最终得到 y∈C_p。若 complete，S1 迫使两边 rank-p fiber 都 full。可是 dynamic p-row 在该 y 至多一边 active，另一 anchor 必须只靠 original rigid rows。它们的 union mass 由 (TR) 严格小于 1，矛盾。

因此至少一个 anchor 有 coarse escape，再由仓库 reverse CRT 得到 full-period escape。证毕。

#### 重要区别

- (PL) 是**附加的可检查假设**，不是从 completeness 自动推出。
- 结论不要求 D_{p,c}+R_{p,c}<1。在顶层两边的 one-anchor budgets 可以都达到或超过 1。
- 更精确的版本可直接证明 C_p 非空，无须通过 (PL)；也可用 #12 的不可实现 rigid frontier 排除顶层，而不局限于 mass<1。
- 若共有 N_p<p 个可能在顶层提供 rigid fatal event 的 distinct actual primes，则 R_{p,c}≤N_p/p<1，这是 (TR) 的方便 sufficient condition。
- (TR) 比 N_p<p 更灵活：即使有较多但很深的 cylinders，其 Kraft mass 仍可能小于 1。
- 不能在 contraction 后把 derived macros 作为 actual primes 代入 R。本证明只在最高 **original** event rank 接合 arithmetic tax。

### Theorem S4 — common two-adic safety criterion

对原仓库的 sound sum-of-two-squares test modulo 2^K，K≥2，两 anchors 有同一个 safe exponent，当且仅当 shared residue r₂ 为偶数。

#### 证明

5^d≡1 mod4。若 r₂ 为奇数，两 local values 都是奇数，相差 2；恰有一个恒为 3 mod4，不能是 two-square residue。因此不存在共同 safe exponent。

若 r₂≡0 mod4，选

\[
5^d\equiv r_2-3\pmod {2^K}.
\]

两 local values 分别是 2、0。

若 r₂≡2 mod4，选

\[
5^d\equiv r_2-5\pmod {2^K}.
\]

两 local values 分别是 4、2。

右端都为 1 mod4，而 5 生成 modulo 2^K 的整个 1+4Z subgroup：归纳使用 v₂(5^(2^t)−1)=t+2，得到 exact order 2^(K−2)，恰等于该 subgroup 的大小。故所需 d 存在；2、0、4 都是 sound two-square residues。K=2 按 modulo 4 解读 4=0。证毕。

因此 S3 的 boundary gate 在此 arithmetic class 中可直接写成：**没有 two-adic row，或 r₂ even**。原有 selected-anchor lemma 本身不足以证明这一 common-safe property。

---

## 5. DISPROVED RESULTS

### Counterexample R — complete systems with disjoint saturated coordinates

Domain 是 X=(Z/3Z)×(Z/5Z)，coordinates 为 x、z，依次排序。使用 8 个 shared row identities。下表列出完整 fatal events；所有 lower guards 都是 universal。

| row | anchor 0 | anchor 1 |
|---|---|---|
| A₀ | x=0 | x=1 |
| A₁ | x=1 | x=0 |
| A₂ | x=2 | x=0 |
| B₀ | z=1 | z=0 |
| B₁ | z=0 | z=1 |
| B₂ | z=0 | z=2 |
| B₃ | z=0 | z=3 |
| B₄ | z=0 | z=4 |

每个 row 在两边都非空，每个 row 的两 anchor events 都不相交。所有 slices 都是 proper rigid singleton cylinders，rank 不随 anchor 改变。整个 simultaneous system 也 row-irredundant：任何 A-row 的删除都会破坏 anchor 0 completeness，任何 B-row 的删除都会破坏 anchor 1 completeness，因此不能把反例归咎于无用的额外 rows。

Anchor 0 的 A-rows 覆盖全部 x，因此覆盖全部 15 cells；anchor 1 的 B-rows 覆盖全部 z，也覆盖全部 15 cells。

但 original saturation ranks 是

\[
\{p:S_{p,0}\ne\varnothing\}=\{3\},\qquad
\{p:S_{p,1}\ne\varnothing\}=\{5\}.
\]

H2 为假，所以 H1 也为假。这里不是“某几个 fibers pointwise 可实现”，而是两个完整的 15-cell anchor domains 都覆盖。

此外，anchor 0 的 unique inclusion-minimal global row cover 是 {A₀,A₁,A₂}；anchor 1 的是 {B₀,…,B₄}。例如 anchor 0 缺少任一 A_i 时，z=2 的相应 x-cell 无法由 B补上；anchor 1 缺少任一 B_j 时，x=2 的相应 z-cell 无法由 A补上。

Maximal-coordinate contraction 在 anchor 0 不产生 B-witness；在 anchor 1 的 B-cover 直接收缩为 covered constant，A-family 不能单独覆盖 lower coordinate。故 nontrivial minimal provenance witnesses 完全错开。

#### 无限 family 与计数边界

把 3、5 换成任意 m,n≥3，取无 fixed points 且非 surjective 的 f:[m]→[m]、g:[n]→[n]，令 A_i 的两边为 x=i、x=f(i)，B_j 的两边为 z=g(j)、z=j，即有同样结论。

在这个 **unguarded singleton rectangular template** 中，需要 m 个 A-rows 和 n 个 B-rows，m+n 的数量是该 template 内的最小值。没有声称它是所有允许 dynamic rows、guards、不同 rank assignments 的 abstract models 的全局最小值。

### Counterexample N — same coordinate, arbitrarily separated lower witnesses

令 lower coordinate 为 Z/mZ，m≥3，top coordinate 为 Z/nZ，n≥2。任取 a,b∈Z/mZ。

选择一个无 fixed points 的 bijection

\[
f:(Z/mZ)\setminus\{a\}\longrightarrow(Z/mZ)\setminus\{b\}.
\]

a≠b 时可从含有 a→b 的 m-cycle 限制得到；a=b 时固定 a，循环其余 m−1 个元素即可。

m−1 个 lower rows 在 anchor 0 覆盖 x≠a，在 anchor 1 覆盖 x≠b，并按 f 配对。n 个 top rows R_j 定义为

\[
F_{R_j,0}=\{x=a,z=j\},\qquad
F_{R_j,1}=\{x=b,z=j+1\pmod n\}.
\]

每个 row 的两事件 disjoint。两 anchors 都 complete，而唯一 original saturation coordinate 是 top，且

\[
S_{\mathrm{top},0}=\{a\},\qquad S_{\mathrm{top},1}=\{b\}.
\]

所以 H2 成立，H1 当且仅当 a=b。差 a−b 可以是 lower group 的任意元素。这个 family 还表明：即使 exact top witness row family 完全相同，也只会收缩成不同 lower guards，不会自动产生同一个 residual cylinder。

m=2 时，a≠b 的版本也成立；本轮的 2×3、2×3×2 模型使用这一版本。重复 prime-sized factors 只是 toy product coordinates，不冒充一个 genuine prime-power CRT decomposition。

---

## 6. INDEPENDENT COMPUTATION

### 6.1 实现与独立性

`tools/reference.py` 只使用 Python standard library，未 import repository implementation。数据结构记录 shared row identity、anchor、rank、CRT guard、exact bitmask、local-zero mask、provenance support。

实现包含：

- 原始 coverage 与 Sat_p 的逐 cell exact enumeration；
- non-coprime CRT guard intersection；
- inclusion-minimal slice-cover family enumeration；
- canonical provenance contraction，每一层与直接 forall projection 对照；
- paired greedy first-stop classification；
- actual modular-power / clipped-valuation replay；
- local-zero corruption rejection。

这是一个独立写出的 software stack；其中不同组织方式的 cross-check 不是“两个完全独立实现”。

### 6.2 Template enumeration

| product | nested complete models | nested H1 false | rectangular complete H2 false |
|---|---:|---:|---:|
| 2×3 | 4 | 4 | 0 |
| 2×3×2 | 4 | 4 | 0 |
| 3×3 | 18 | 12 | 36 |
| 3×5 | 36 | 24 | 5,880 |

合计 5,978 个 template-generated complete systems。枚举范围是上述明确 templates 的参数，不是所有 finite triangular models 的全量分类。表中的 0 也不能被解释为相应 grid 上不存在其他类型反例。

### 6.3 Additional exact audits

| audit | 范围 / 结果 |
|---|---|
| last-coordinate truth identity | 4,416 cases，0 mismatches |
| rigid-only first-branch tax | 951 cases，0 mismatches |
| seeded recursive contraction | 1,000 paired systems；53 complete；635 derived clauses；0 mismatches |
| seed | 20260905 |
| named regression tests | 10/10 PASS，见 test_reference.py 与 unit_tests.log |
| local-zero corruption | 将 dynamic center 并入 fatal mask 后，被明确拒绝 |
| common two-adic safety | K=2,…,8 的每个 residue；direct square-sum sets；与 even-r criterion 完全一致 |
| actual arithmetic full periods | 三个 67/20771 shared systems，各 U=L=228,470，两个 anchors |

随机生成只用于 deterministic regression evidence；普遍的 contraction 和 no-go assertions 依据上面的证明，不依据随机成功率。

### 6.4 Shared-residue surrogate 的精确边界

为避免仅仅给两套无耦合 masks，程序还为每个 abstract row 分配不同 surrogate primes q≡3 mod4，K=2、r=0、E={1}，并构造一个 arbitrary periodic table g_i(d)。令

\[
\widetilde V_{i,c}(d)=-3^c-g_i(d)\pmod{q_i^2}.
\]

它满足同一个 shared residue 和 difference identity `V₀−V₁=2`，精确实现所列 paired fatal/zero masks。

例如 anchor-0 fatal cell 取 g=−1−q；anchor-1 fatal cell 取 g=−3−q；对应 local-zero cell 取 g=−1 或 −3；两边都不 fatal 的 cell 取 g=1。所有 table values 均为 units modulo q²，程序逐项验证。

**g_i(d) 不等于 5^d。** 因而这个 surrogate 不满足 actual multiplicative-order、lifting、nonregular-resource 条件，不是 admitted arithmetic realization。它只隔离：rowwise residue coupling 与 difference identity 本身仍不足以推出 synchronization。

---

## 7. COUNTEREXAMPLES：ACTUAL ARITHMETIC CHECKS

### 7.1 New actual local first-split witness

选择实际 primes

\[
p=67,\quad q=20771,\quad K_p=K_q=2,\quad E_p=E_q=\{1\},
\]

并在两个 anchors 共用

\[
\boxed{r_{67}=2,\qquad r_{20771}=20775.}
\]

Exact order data 为

\[
w_{67}=22,\ s_{67}=1;\qquad
w_{20771}=10385=155\cdot67,\ s_{20771}=2.
\]

故 U=L=228470，lower modulus 为 3410。固定 y=0 mod3410，用 z=d mod67 作为 top digit。

| actual row | anchor 0 fatal digits | anchor 1 fatal digits |
|---|---|---|
| 67 | z≠0，共66个 | 空 |
| 20771 | 空 | z=0，共1个 |

因此

\[
B_0=X_{67}\setminus\{0\},\qquad B_1=\{0\},
\]

\[
E_0=\{0\},\qquad E_1=X_{67}\setminus\{0\}.
\]

两 escape sets 非空且不相交，是 **SPLIT**，不是 JOINT_FULL，甚至不是 SINGLE_FULL。

#### 直接算术验证

对 67-row，anchor 0 的 local value 为 1−5^d；当 d≡0 mod3410 时，22|d，LTE 给出非中心 digits 上 valuation1，z=0 时为 local zero。Anchor 1 的 local value mod67 为 −2，因此 inactive。

对 q-row，anchor 1 的 local value 为 q+1−5^d，在 d≡0 mod10385 时 exact valuation1。与 y=0 的交给出 z=0。Anchor 0 要求 5^d≡3 modq；但在这个 lower fiber 中 5^d 属于 order67 subgroup，而

\[
3^{67}\equiv7380\not\equiv1\pmod{20771},
\]

所以不可能。

### 7.2 这不是 actual complete counterexample

完整 period 的结果是：

| shared residues (r67,r20771) | Sat₀ | Sat₁ | 两 anchor safe cell counts |
|---|---|---|---|
| (2,13471)，原仓库例 | {2728} | {1639} | 218218，218218 |
| (0,4494)，#11 sharp例 | {2431} | {106} | 218218，218218 |
| (2,20775)，本轮split例 | 空 | {1705} | 218219，218218 |

每一行的共同 Sat intersection 都为空；每一行都远非 complete。新例只证明 actual local constraints 允许 first split，不能用来否定“每个 actual complete certificate 都满足 H1”。

### 7.3 3×5 abstract countermodel 的 unchanged-U nonrealizability

若要求 actual arithmetic realization 保持 U=15，则每个 row 的 w_q |15，因而 q |5^15−1。Exact factorization 为

\[
5^{15}-1=30517578124
=2^2\cdot11\cdot31\cdot71\cdot181\cdot1741.
\]

符合 q≡3 mod4 的全部候选只有 11、31、71。其 (w_q,s_q) 分别为 (5,1)、(3,1)、(5,1)。全部 regular，不能提供 positive rigid fatal valuation；自己的 q-coordinate 又不在 U 中，dynamic coarse event 也不能出现。

所以 Counterexample R 不可在 **unchanged U=15** 中由 actual admitted rows 实现。这是对 finite divisor set 的完整证明，不是“扫到某个 cutoff 未找到”。

允许添加 resources 后改变 U 的更大系统，不由这一 factorization 排除；本轮没有解决该 enlarged-system 问题。

---

## 8. INTERFACE WITH #11 / #12 / #13

### #11

S3 使用的是原始 dynamic exclusion 与 rigid-only frontier necessity。在 top step 得到的是共同 lower survivor 经 completeness 强迫的 full fibers，没有将 separate witnesses 换成一个共同 witness。

#11 已有 period-level Hall-type capacity condition，本轮不把它重命名为新成果。

### #12

R_{p,c}<1 及 N_p<p 都是对 actual original rigid resources 的 sufficient shortages。更强的版本可以检查各 depth inventory 是否能实现 rigid-only complete prefix frontier。

但 #12 的 one-anchor construction 不能证明 abstract Counterexamples R/N 同时在两个 anchors 由 actual shared residues 实现。没有进行这个跳跃。

### #13

Counterexamples 的 contractions 保留 named original-row provenance，并由直接 finite coverage 校验。它们展示了 separate exact roots 不会自动给共同中间 witness。

S1 也适用于一般 semantic triangular decomposition 的最后一步，但 S3 的 **arithmetic resource interpretation 只用 original events**。将它递归应用到任意 macro residual 后，必须重新证明对应 resource accounting，不能原样沿用 actual-prime inventory。

---

## 9. STRONGEST NEW COROLLARY

在 actual admitted class 中，设 p 是最大非空 original odd event rank。若

\[
R_{p,0}<1,\qquad R_{p,1}<1,
\]

那么 #11 排除任何共同 top full fiber。因此 S1 给出如下必要条件：

\[
\boxed{\operatorname{Complete}_{0,1}\Longrightarrow A_0\cup A_1=Y.}
\]

也就是说，**两个 anchors 的 original lower events 必须组成一个 complete pooled lower cover**。

再加 common-safe two-adic boundary 及所有 lower coordinates 的 (PL) 时，这个 pooled lower cover 被 exact greedy construction 排除，故无 complete simultaneous certificate。

这就是本轮的 weaker useful bridge：不是无条件强迫 H1，而是证明一个 alternative，并在一个明确 no-go class 中排除其逃避分支。

对于三组已 replay 的 67/20771 systems，lower fatal events 为空，top rigid mass 在两边都是 1/67，故该 corollary 适用。它们的 top one-anchor budgets 可以为 66/67+1/67=1，说明新 criterion 不要求原 main 的全坐标 strict deficit。不过这些具体两-row systems 也能被更简单的 total mass 估计排除，因此不声称第一次排除了它们；它们用来验证接口与条件。

---

## 10. WHAT DOES NOT FOLLOW

本轮没有证明：

- actual admitted H1、H2、H3、H4、H5 的普遍否定或普遍肯定；
- 存在 actual complete simultaneous certificate；
- pooled lower cover 足以推出 complete simultaneous coverage；
- every common greedy split 后必再次合流；
- two separate anchor-tagged provenance trees 必有有用的共同非平凡 witness；
- nonregular prime resources 在全体 primes 中存在 universal 数量上界；
- derived provenance macros 可以作为 actual primes 计数；
- arbitrary actual resource selection 保持外部 frozen U 不变；
- 有限 local-mask escape 直接给出 sum-of-two-squares representation；
- universal C=1 no-go、A303656 的证明或 certified counterexample。

Abstract counterexamples 有充分完整的 finite coverage，但缺 actual powers-of-five structure；actual split 则有真实算术，但缺 completeness。这两个缺口不能互相抵消。

---

## 11. REMAINING GAP

现在可将下一步 gap 写得更具体：

> 在 top rigid-resource deficit 下，是否存在满足全部 actual shared-residue、order、lifting、two-adic 和 local-zero constraints 的 complete pooled lower cover，能与更高坐标的 anchor-specific obligations 同时组装成 complete simultaneous system？

如果 pooled lower cover 使用一个 active dynamic shell 与另一 anchor 的 rigid center 拼合，SPLIT 会出现；本轮 actual example 说明这不能仅凭 local arithmetic 消掉。

如果要从 top alternative 继续向下递归，需要追踪 **mixed-anchor original demands**，或者建立对 derived provenance 的可靠 original-prime accounting。原 #13 只保证 sound exact contraction，没有提供这种跨 anchor 的 resource conservation theorem。

Actual H1/H2 是否成立仍未决定；继续把“两个 finite trees 总会撞上”当作默认引理已经没有依据。

---

## 12. RECOMMENDED NEXT TARGET

下一项建议只选一个：

**ARITHMETIC POOLED-LOWER-COVER INVERSE THEOREM WITH ANCHOR-TAGGED DEMANDS。**

推荐执行环境仍为网页端 research/reference laboratory。目标是：在原始 actual rows 上，分类由 S1/S3 强迫的 pooled lower covers，尤其分析 dynamic shell 与 opposite-anchor rigid center 的 mixed cover 如何向下一层传播；证明一种不能由 arbitrary paired masks 满足、但 actual multiplicative-order / common-residue data 必须满足的 invariant。

先 theorem 与小型 exact CSP，不增加 prime-scan cutoff。只有得到新的、可审计的 arithmetic gate，才考虑 repository-native integration 或更大规模计算。

---

## 13. PHASE VERDICT

```text
PRIMARY:
C. WEAKER USEFUL BRIDGE FOUND

SECONDARY:
D. STRUCTURAL NEGATIVE RESULT
   (complete abstract paired triangular systems only)

ACTUAL H1:
OPEN AFTER TARGETED SEARCH

ACTUAL H2:
OPEN AFTER TARGETED SEARCH

UNIVERSAL C=1 NO-GO:
NOT PROVED

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

---

## Source map

所有 repository URLs 均固定在本轮 bound SHA；精确 metadata 另见 `results/source_binding.json`。

- [Formal class](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_entangled_coordinate_deficit/FORMAL_CLASS.md)
- [Coordinate-deficit audit](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_entangled_coordinate_deficit/THEOREM_AUDIT.md)
- [Contraction definitions](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_contraction_tree_phase_a/DEFINITIONS.md)
- [Contraction theorem audit](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_contraction_tree_phase_a/THEOREM_AUDIT.md)
- [Prefix inverse classification](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_minimal_saturated_coordinate_inverse/source/A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A/ABSTRACT_CLASSIFICATION.md)
- [Two-anchor common-residue obstruction](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_two_anchor_common_residue_phase_a/REPORT.md)
- [Arithmetic realizability](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_prefix_frontier_realizability_phase_a/REPORT.md)
- [Hereditary provenance-cylinder contraction](https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/analysis/c1_hereditary_shell_phase_a/REPORT.md)
