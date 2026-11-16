# A303656 — Abstract Covering Problem (ACP) 研究报告

日期：2026-11-16　|　输入：`A303656_Triage_Audit_2026-11-14.zip`（C21 frozen proof、C22 referee 文档）
状态声明：本报告全部结论由 AI 推导并由 exact 程序复核，**没有人类数学家审阅，也没有 formalization**。Theorem R 还依赖 C21 `PROOF.md` 中同样只经 AI referee 的 lemmas（见 §3.3 的 CONDITIONAL 标注）。

Tag 约定：PROVED | PROVED NEGATIVE STRUCTURAL THEOREM | CONDITIONAL | FINITE COMPUTATION | HEURISTIC | UNRESOLVED。FINITE COMPUTATION 只证明它穷举过的那个有限命题。

---

## 0. 结论速览

| # | 结论 | Tag |
|---|---|---|
| 1 | 没有找到任何 covering。在 pretend model 里，任何 parity class 的 covering 至少需要 **147 个 fibres**，并且至少用到一个 `H_p ≥ 16384` 的 prime（即 `p ≥ 32771`）。 | PROVED + FINITE COMPUTATION（Theorem A、Theorem R 的 `Q = ∅` 情形） |
| 2 | 真实模型：`f_q(a) = 0` 至少需要 **147 个** distinct joint-nonregular primes（C22 是 23）。只用 Haar union bound、不用 LP measure 的简单版本给出 30。 | CONDITIONAL（C21 的 rigidity 与 regular averaging lemma）+ FINITE COMPUTATION |
| 3 | `M = t` frontier 不是真正的障碍：fresh `M`-fibre 被 `M` 条 exponential curves 精确 tiling **当且仅当** 它们是同一类型的 `M` 条平行直线；`z ≠ 0` 的 curve 至多 `M−1` 个点。C22 在 `M = t = 23` 处卡住，原因是 catalogue 只到 19-smooth、active weight 只用了 `1/M`；用 complete catalogue 后，23 个最大的 active weights 之和只有 `0.0952`。 | PROVED（Lemma L4、Theorem F）+ FINITE COMPUTATION |
| 4 | 任何 measure / union-bound / LP-dual 方法都有一个可证明的上限：对 `T = {inert primes 7 ≤ p ≤ 473899}`，fractional covering 存在，因此不存在任何 measure certificate。要证明 (N) 必须用到 integrality（每个 prime 只能选一个 residue）。 | PROVED NEGATIVE STRUCTURAL THEOREM（Proposition H） |
| 5 | 一维限制不是障碍：固定 `α` 的一条 `β`-line 可以被 18 个 inert primes 的 residue classes 精确覆盖（`N = 315`，显式给出）；而 `h3 | 315` 的 `α`-line 不能。障碍是二维的。 | FINITE COMPUTATION |
| 6 | Dichotomy：**undecided**，证据偏向 (N)。 | UNRESOLVED / HEURISTIC |

---

## 1. Phase 1 — Formalization

### 1.1 记号

- inert prime：`p ≡ 3 (mod 4)`，`p > 3`。`h3(p) = oddpart(ord_p 3)`，`h5(p) = oddpart(ord_p 5)`，`H_p = max(h3, h5)`，`L_p = lcm(ord_p 3, ord_p 5)`，`supp(p)` = 整除 `h3·h5` 的 odd primes。因为 `v_2(p−1) = 1`，`ord_p b ∈ {h, 2h}`。
- parity class `c = (c1, c2) ∈ {0,1}²`：`α = c1 + 2a`，`β = c2 + 2b`，`(a, b) ∈ Ẑ²`。odd primes 的事件只依赖 `(a, b)` 的 odd-primary 坐标 `E_odd = ∏_{ℓ odd} Z_ℓ²`。
- fibre：`F_p^c(z) = {(a, b) ∈ Z/h3 × Z/h5 : 3^{c1}·9^a + 5^{c2}·25^b ≡ z (mod p)}`。对固定的 `p`，`z` 跑遍 `F_p` 时 fibres 是 class `c` 的一个 partition。
- weight：`w_p^c = max_z #F_p^c(z) / (h3·h5) ≤ 1/H_p`。

### 1.2 Lemma L1（lift lemma；回答 Phase 1 第 2 问）— PROVED

设 `p` 是 inert prime，`w3 = v_p(3^{p−1} − 1) ≥ 2`，`w5 = v_p(5^{p−1} − 1) ≥ 2`，`w = min(w3, w5)`，`ω` 为 Teichmüller lift。

(a) 条件于 tame class `(i, j) = (α mod ord_p 3, β mod ord_p 5)`，`s(e)_p` 在 `τ + p^w Z_p` 上是 Haar，`τ = ω(3)^i + ω(5)^j`。
*证明。* `3 = ω(3)·u`，`u ∈ 1 + p^{w3}Z_p` 且 `u ∉ 1 + p^{w3+1}Z_p`。`α_p ↦ u^{α_p}` 是 `Z_p → 1 + p^{w3}Z_p` 的拓扑群同构，把 Haar 推到 Haar；`α_p` 与 `α mod (p−1)` 独立。`5` 同理，两个独立 Haar coset 之和是较大 ball 上的 Haar。∎

(b) 该 class 上 `β_{p^k}(a − s(e))` 恒为零 ⟺ `v_p(a − τ)` 为奇数且 `< min(k, w)`。其余 class 上条件期望为正。
*证明。* 若 `v_p(a − τ) < w`，则 `v_p(a − s) = v_p(a − τ)` 在 class 上为常数。若 `≥ w`，`a − s` 在 `p^w Z_p` 上 Haar，`v ∈ {w, w+1}` 都有正概率，其中必有偶数或 `≥ k`。∎

(c) 因此 `p` 处的 bad set 总是包含在 `F_p(a mod p)` 中；并且对每个 `z` 存在 lift `a ≡ z (mod p)`（mod `p²`），使整个 fibre 都是 bad（取 `k = 2`）。
*证明。* fibre 中至多 `ord_p 3 ≤ p − 1` 个 tame classes，每个 class 的 `τ mod p²` 只排除 `z` 的一个 lift，而 lift 共 `p` 个（pigeonhole）。∎

**结论。** 对固定的 `(q, a)`，真正的 zero condition 严格强于 “unit-avoidance 处处失败”：`s ≡ a (mod p²)` 的 class 是 good；深度 `≥ w` 处不再 rigid，bad 部分依赖 `p`-primary 坐标。但作为**存在性**命题两者等价：bad sets ⊆ fibres（⇒），而任何 fibre covering 都能通过选 lift 变成真正的 zero（⇐）。regular prime `q` 的 bad set `{v_q(a − s) 奇且 < k}` 同样 ⊆ `F_q(a mod q)`。所以在 pretend model 里可以把所有 inert primes 都放进 `T`，搜索时用 fibre 是 exact 的。

### 1.3 Lemma L2（2-adic 与 prime 3）— PROVED，并经 brute force 验证

- 2-adic：class `c` 上 `s` 在 `r_c + 8Z_2` 上 Haar，`r_{(0,0)} = 2`，`r_{(1,0)} = 4`，`r_{(0,1)} = 6`，`r_{(1,1)} = 0`（`9` 与 `25` 各自生成 `1 + 8Z_2`）。class `c` 被 2-norm 完全杀死 ⟺ `(a − r_c) mod 8 ∈ {3, 6, 7}`（`k ≥ 3`）。于是 `a` 为奇数时杀死一个 `α`-parity（两个 classes），`a` 为偶数时恰好杀死一个 class。未被完全杀死的 class 保留一个与 odd 坐标独立的正测度 2-primary cylinder。
- prime 3：`s ≡ 5^β (mod 3^k)`。`3 | a` 时无 zero；否则 bad set = `{β ≡ b0 (mod 2), v_3(β − b0) 为偶数且 ≤ k − 2}`，只依赖 `β` 的 parity 与 3-primary 坐标，在该 `β`-parity 内测度 `< 3/4`。

**Proposition P1 — PROVED。** `f_q(a) = 0` ⟹ 存在一个 parity class `c`，它不受 2 和 3 的影响，并被 inert primes `> 3` 的 fibres 完全覆盖。（`a` 奇：剩两个 class，3 至多影响其中一个 `β`-parity；`a` 偶：剩三个。）反向的充分条件：fibres 覆盖同一 `α`-parity 的两个 classes，就可取 `a` 为奇数、`3 | a` 得到 pretend zero。

### 1.4 ACP 的有限组合陈述

> **ACP_c(T, z)。** 给定 parity class `c`、有限集 `T`（distinct inert primes `> 3`）和 residues `z_p ∈ F_p`。令 `N3 = lcm h3(p)`，`N5 = lcm h5(p)`。问：`⋃_{p∈T} π_p^{-1}(F_p^c(z_p)) = Z/N3 × Z/N5`？
> **(N)** ⟺ 对所有 `c, T, z` 答案为否。任何 zero 都给出某个 `c` 的 yes-instance（P1 + L1）。

regular-prime norm conditions、artificial targets 都是 fibre 的子集或 fibre 本身；2-adic 与 prime 3 只决定哪个 class 必须被覆盖。

### 1.5 Reference decision procedure 与 validation

`src/acp.py::coverage(c, targets)`：在 quotient `Z/N3 × Z/N5` 上逐点计数，返回未覆盖点数（exact，不抽样）。`src/model.py`：直接按定义计算 `F_q(a) = f_q(a)/π`（Fraction）。

`src/validate.py` 共 24 项，全部 PASS（FINITE COMPUTATION）：

| 检查 | 内容 |
|---|---|
| V0 | `β_{p^k}(y) = 0` 的规则对 20 个 prime powers 与 brute force 一致；`β_8 = (1,2,2,0,1,2,0,0)` |
| V1 | 复现 A2 audit：`q = 120` 时 `min F = 7/15`，恰在 `50, 70, 80, 100`；`E F = 1`，`E F² = 107/96` |
| V2, V3 | Lemma L2 的 2-adic 规则（`k = 3..8`，全部 `a`）与 prime 3 规则（`k = 1..5`） |
| V4 | `q ∈ {7², 7³, 11², 19², 23²}` 时 `F_q(a) > 0` 对所有 `a` |
| V5 | joint-nonregular toy（bases `31, 19`，`p = 7`，depths `2, 3`）：Lemma L1(b) 对 `k = 2, 3, 4`、所有 `a`、36 个 tame classes 成立；L1(c) 的 pigeonhole 成立 |
| V6 | **positive control**：bases `(B, B)`，`B = 2·1463² − 1`，`q = 1463²`，定义级引擎给出 `F_q(a) = 0`，`coverage()` 报告同一个 covering；去掉 prime 19 则不是 zero |
| V7 | `coverage()` 与朴素 `pow()` 枚举在 40 组随机 targets 上一致 |
| V8 | 从独立构造的 catalogue 复现 C21：19-smooth、`H < 512` 恰为 46 个 primes，orders 与 frozen `certificate.json` 相同；29 个 budgets 全部复现（最坏 `875703733/878169600`）；C22 的 33 个 budgets（最坏 `4238011529/4390848000`） |
| V9 | one-parameter toy：Erdős covering `{3,5,7,13,17,241}` 被识别为 covering，去掉 `241` 则不是 |

---

## 2. 结构性 lemmas

### Lemma L3（richness）— PROVED

设 `T` 是 class `c` 的 minimal covering，`ℓ` 是 odd prime，`T_ℓ = {p ∈ T : ℓ | h3·h5}` 非空。则 `|T_ℓ| ≥ ℓ`。

*证明。* `T ∖ T_ℓ` 的事件不依赖 `ℓ`-primary 坐标，由 minimality 它们留下正测度的未覆盖集 `U`。对 `x ∈ U`，`ℓ`-fibre `Z_ℓ²` 必须被 `T_ℓ` 的 traces 覆盖。若 `ℓ^j ‖ h3`（`j ≥ 1`），固定 `b` 后 `9^a` 随 `a_ℓ mod ℓ^j` 取 `ℓ^j` 个不同值，至多一个满足方程，所以 trace 测度 `≤ ℓ^{−j} ≤ 1/ℓ`；`ℓ | h5` 同理。少于 `ℓ` 个 trace 盖不住。∎

注意这对**每个** `ℓ` 成立，不只是最大的 `M`（C21 只对 top prime 用，是因为 regular norm primes 的存在）。

### Lemma L4（no full exponential curve）— PROVED

设 `M` 是 odd prime，`p ≡ 1 (mod M)`，`μ_M ⊂ F_p^×` 是 `M` 次单位根，`A = uμ_M`，`B = u'μ_M`，`N(z) = #{(x, y) ∈ A × B : x + y = z}`。

1. `z = 0`：`N ∈ {0, M}`（非空时是一条完整的直线 `X − vY = const`）。
2. `z ≠ 0`：`N ≤ M − 1`；若 `A ≠ B` 则 `N ≤ (M−1)/2`；若 `A = B` 且 `M ≥ 5` 则 `N ≤ M − 2`。

*证明。* 解对应 `T^M = B^M` 与 `(z − T)^M = A^M` 的公共根。因 `M` 为奇数，`D(T) = (z−T)^M + T^M − A^M − B^M` 的次数是 `M − 1`，首项系数 `Mz ≠ 0`（`p > M`），公共根都是 `D` 的根，故 `N ≤ M − 1`。`D(z − T) = D(T)`，所以解集 `S ⊂ B` 与 `z − S ⊂ A` 都是 `D` 的根；`A ≠ B` 时两者不交，`2N ≤ M − 1`。`A = B`、`N = M − 1` 时 `D = Mz(T^M − c)/(T − t0)`，比较 `T^{M−1}` 与 `T^{M−2}` 系数得 `z³M(M−1)(M+1)/12 = 0`，与 `p ∤ z(M−1)M(M+1)`、`p > 3` 矛盾。∎

数值验证（FINITE COMPUTATION，`src/frontier.py`）：`M ∈ {3,5,7,11,13,17,19,23}`，所有 `p < 20000`、`p ≡ 1 (mod M)`，所有 cosets 与所有 `z`。实测最大值：same coset `2, 3, 3, 6, 6, 6, 6, 12`；different cosets `1, 2, 3, 5, 4, 4, 4, 11`（`(M−1)/2` 在 `M = 3, 5, 7, 11, 23` 处取到，所以这个界是 sharp 的）。

**GAP：** same-coset 的界 `M − 2` 很可能远非最优（实测 `≤ (M+1)/2`），但我没有对所有 `p` 一致成立的证明。

### Theorem F（exact tiling ⟹ parallel lines）— PROVED

在一个 fresh `M`-fibre 上，`M` 个 active primes 的 traces 覆盖 `Z_M²` ⟺ 每个 trace 测度恰为 `1/M` 且两两不交。此时：
- 每个 active prime 的 `M`-指数型 `(v_M(h3), v_M(h5))` 属于 `{(1,0), (0,1), (1,1)}`，且 `(1,1)` 型必须 `z_p = 0`；
- 每个 trace 是 `AG(2, M)` 中的一条直线：type V（`X = c`）、type H（`Y = c`）或 type S（`z = 0`，`X − vY = c`）；
- `M` 条两两不交的直线必属同一 parallel class，所以 `M` 个 primes 同型（全 V、全 H，或全 S 且斜率相同）。

*证明。* trace `≤ ℓ^{−max(j, j')}`（L3 的证明）强制指数型；`(1,1)` 型且测度 `1/M` 意味着每个 `X` 都有解，即 `z − uμ_M = u'μ_M`，由 L4 得 `z = 0`。仿射平面中不交的直线平行。∎

**Corollary F'（C22 框架下 `M = t` 永不 critical 的原因）— PROVED。** 若 lower system 的 good set `U` 满足 `μ(U) > 1/3`，则 `t = M ≥ 13` 个 actives 不能盖住 `U` 上的所有 fresh fibres。理由：tiling 只在 `x ∈ ⋂_p G_p` 上存在，`G_p` 是 `F_p` 在 non-`M` 坐标上的投影；type V 时 `μ(G_p) ≤ 1/m_p`，`m_p = h3(p)/M`。`m_p ≥ 3` 则 `μ(G_p) ≤ 1/3`；全部 `m_p = 1` 则 `M` 个 `≥ 2M+1` 的 distinct primes 都整除 `9^M − 1`，而 `(2M+1)^M > 9^M`。type H 用 `25^M − 1`（需 `2M + 1 > 25`），type S 用 `gcd(9^M − 1, 25^M − 1)`。∎

---

## 3. Phase 2A — Catalogue search 与 certificates

### 3.1 Complete catalogue — FINITE COMPUTATION

`p | 3^{2h} − 1` 对某个 odd `h < B` ⟺ `h3(p) < B`（inert 时 2-部分自动满足）。所以所有 `H_p < B` 的 inert primes 都整除
`G = gcd(∏_{h odd < B}(3^{2h} − 1), ∏_{h odd < B}(5^{2h} − 1))`，把 `G` 完全分解即得 complete catalogue `Cat_B`。

| `B` | `G` 的 prime factors | inert primes，`H_p < B` | 最大 inert `p` |
|---|---|---|---|
| 512 | 141 | 108（C21 的 19-smooth 子集：46） | — |
| 16384 | 3028 | 2216 | 103859419 |
| 32768 | 5709 | 4161 | 2094938071 |

独立复核（`src/verify_catalogue.py`，不共享构造代码）：(i) 每个 prime 用完整 trial division 认证，orders 由 `b^o = 1`、`b^{o/q} ≠ 1` 重新确认；(ii) `G = ∏ p^e`；(iii) brute force 扫描所有 inert `p < 1.1·10^8`，恰有 4160 个满足 `H < 32768`，全部在表中（第 4161 个是 `2094938071`）；(iv) cutoff `2048` 的 modular completeness check（另一条路线）。

每个 prime、每个 class 的 `max_z N_z`、`N_0`、nonempty fibres 数都 exact 计算（`src/compute_weights.py`）；12 个巨大 primes 只保留 trivial bound `w ≤ 1/H`，后续只用到上界。`src/verify_weights.py` 用 `pow()` + `Counter` 重算了 90 个小 primes 的全部四个 classes，并用另一种方法重算了 40 个随机抽取的较大 primes。

Haar union bound 之和（`Σ w_p^c`，全 catalogue）：`B = 512`：`0.93 / 1.33 / 1.34 / 1.18`（classes `00 / 01 / 10 / 11`）；`B = 32768`：`1.17 / 1.71 / 1.75 / 1.58`。所以单纯的 union bound 早已失效，需要下面的工具。

### 3.2 Theorem A — PROVED + FINITE COMPUTATION

> 对每个 parity class `c`，不存在只使用 `H_p < 16384` 的 primes 的 covering。因此任何 covering（以及任何真实的 zero）都涉及至少一个 `max(h3, h5) ≥ 16384` 的 inert prime，特别地 `p ≥ 32771`。

*证明结构。*
1. 由 L3，minimal covering `T ⊆ Cat_16384` 包含在 rich core `S` 中（反复删去 “`ℓ`-active primes 少于 `ℓ` 个” 的 `ℓ`）。`|S| = 257`，order primes 只剩 `ℓ ∈ {3,5,7,11,13,17,19,23,29}`，`max S = 2085319`。
2. 取 `μ = ν0 ⊗ Haar`，`ν0` 是 `(Z/45)²` 上的 probability measure（整数表，`certs/nu_B16384_N45_c*.json`）。covering 要求对**任何** `μ` 都有 `μ(⋃ F_p) = 1`。
3. `A = {supp ⊆ {3,5}}`，`D = {supp ∩ {3,5} = ∅}`，`C` = 其余。`A` 与 `D` 的事件在 `μ` 下独立，故
   `μ(⋃) ≤ 1 − (1 − V_A)(1 − W_D) + V_C`，`V_X = Σ_{p∈X} max_z μ(F_p(z))`，`W_D` = `D` 的 Haar 和。
4. `src/verify_lp_cert.py` 对每个 prime 枚举 `Z/h3 × Z/h5` 的**全部**点、对**全部** `z` 取最大值（整数运算，不信任 LP 输出）：

| class | `V_A` | `V_C` | `W_D` | bound |
|---|---|---|---|---|
| 00 | 0.3980 | 0.2002 | 0.1410 | **0.6830** |
| 01 | 0.3800 | 0.2262 | 0.2696 | **0.7733** |
| 10 | 0.3746 | 0.2452 | 0.2008 | **0.7454** |
| 11 | 0.4183 | 0.2458 | 0.2119 | **0.7874** |

全部 `< 1`。∎（exact 有理数见 `out/theoremA_c*.json`。）`ν0` 的效果：例如 class `10` 中 prime `7` 的 mass 从 Haar 的 `1/3` 降到 `≈ 1/7`，`19` 从 `1/9` 降到 `1/19`。

### 3.3 Theorem R（K-target theorem，`K = 146`）

> **Theorem R(K)。** 设 `Q`、`T` 是不相交的有限 inert prime 集，`Q` 中每个 prime 至少对一个 base regular 并带任意 norm 数据，`T` 带任意 unit targets，`|T| ≤ K`，再加任意 2-adic 与 prime-3 norm 条件。则存在正 Haar 测度的 clopen exponent set 同时满足全部条件。
> **`K = 146` 成立。** 因此 `f_q(a) = 0` 至少需要 147 个 distinct joint-nonregular primes；在 pure fibre model（`Q = ∅`）中，任何 covering 至少需要 147 个 fibres。

Tag：`Q = ∅` 情形 **PROVED + FINITE COMPUTATION**。一般情形 **CONDITIONAL + FINITE COMPUTATION**，假设是 C21 `PROOF.md` §1–§2 原文陈述的两点：(H1) zero 的 root 必为 `p² | q` 的 joint-nonregular inert prime，unit-avoidance 蕴含该处 norm factor 为正；(H2) regular averaging lemma：`q` 是最大的 regular norm prime、其余约束不依赖该 regular base 的 `q`-primary 坐标时，`∫ W·β_{q^k} ≥ (1/q)∫ W`。

*证明（对 `M(T) = max_{p∈T} P^+(L_p)` 归纳，`K` 固定）。* 先固定 class `c` 与一个允许的 2-primary cylinder（L2；`c` 可能被对手强制，所以四个 classes 都要验证）。
- 用 (H2) 按递增顺序恢复 `q > M` 的 norm factors，故可设 `Q ⊆ [7, M]`。
- **Fresh fibre step（`t < M`，`t` = active targets 数）：** 删去 actives；若 `M ∈ Q`，把它换成 artificial unit target。新系统 target 数 `≤ K`，`M` 严格下降，由归纳得到不依赖 `M`-primary 坐标的正测度集；每个 active 在 fresh fibre 上的 trace `≤ 1/M`，剩余比例 `≥ 1 − t/M > 0`。
- **Direct budget（`t ≥ M`，以及 base `M ≤ 7`）：** 把 `Q` 的 norm 条件全部加强为 unit 条件，此时所有 bad events 都是 fibres。取 `μ = ν0^c ⊗ Haar ≪ Haar`，只需
  `C_M + A_M(t) + I_M(K − t) < 1`，
  其中 `C_M = Σ_{inert 7 ≤ q ≤ M} m_q`，`A_M(t)` = `{p > M, P^+(L_p) = M}` 中最大的 `t` 个 mass 之和，`I_M(k)` = `{p > M, P^+(L_p) < M}` 中最大的 `k` 个之和。catalogue 之外的 primes 有 `H_p ≥ B`，其 mass `≤ ρ_max/B =: τ`（`ρ_max` 是 `dμ/dHaar` 的上确界），以无穷多个 placeholder `τ` 计入。critical cases 只有 primes `7 < M ≤ K`、`M ≤ t ≤ K`。∎

*验证（`src/verify_root_budget.py`，整数运算，masses 向上取整到 `10^{-15}`）。* `B = 32768`，`K = 146`，每个 class 2301 个 budgets：

| class | 最坏 budget | 位置 `(M, t)` | `τ` |
|---|---|---|---|
| 00 | 0.808940 | (83, 83) | 4.15e-4 |
| 01 | 0.986416 | (83, 83) | 4.25e-4 |
| 10 | 0.922261 | (61, 61) | 4.95e-4 |
| 11 | **0.998929** | (83, 83) | 5.40e-4 |

`K = 147` 在 class `11` 失败（`1.000565`）。`m_p` 的来源：`supp ∩ {3,5} = ∅` 用 exact Haar weight；`h3·h5 ≤ 4·10^6` 用 exact `μ`-mass；其余用 `ρ(g3, g5)·w_p`（`ρ` 是 `ν0` 的 marginal density ratio，是合法上界）。小 primes 的 `μ`-mass 另用纯 Python 整数重算核对。

**Haar-only 版本（不需要任何 LP measure）：** 同一验证器取 `ν0` = uniform，`K = 29` 通过（最坏 `0.995116`，class `10`，`(13,13)`），`K = 30` 失败（`1.002911`，`(17,17)`）。即仅凭 complete catalogue + exact per-class weights 就有 **30 roots**。

说明：`K = 146` 不是方法的极限。`ν0` 是为 Theorem A 的目标优化的，没有针对 budgets 调整；更大的 `B`、对 `ρ_max` 加 cap、利用 pure-`ℓ` blocks 的独立性，都能继续抬高 `K`。但 Proposition H 说明这条路线有上限。

### 3.4 Proposition H（measure 方法的 horizon）— PROVED NEGATIVE STRUCTURAL THEOREM

> 对任何 probability measure `μ` 与任何 inert prime 集 `T`：`Σ_{p∈T} max_z μ(F_p^c(z)) ≥ Σ_{p∈T} 1/n_p ≥ Σ_{p∈T} 1/p`（`n_p ≤ p` 是 nonempty fibres 数）。
> 而 `Σ_{7 ≤ p ≤ 473899, p ≡ 3 (4)} 1/p ≥ 1`（19789 个 primes；去掉最后一个则 `< 1`；`src/horizon.py`，整数运算）。

*证明。* `p` 的 fibres 是 partition，`Σ_z μ(F_p(z)) = 1`，最大者 `≥ 1/n_p`。等价地，`y_{p,z} = 1/n_p` 是一个 fractional covering。∎

含义：对 `T ⊇ {inert primes ≤ 473899}`，C21/C22 的 union bound、本报告的 Theorem A / R、以及任何 LP dual 都**不可能**给出 certificate。(N) 的证明必须利用 “每个 prime 只选一个 residue” 的 integrality（L3、L4、Theorem F 属于这一类）。同时也说明：在 fractional 意义下 covering “存在”，所以 (N) 若成立，不是因为 budget 不够。

### 3.5 One-parameter controls — FINITE COMPUTATION（`src/toy_1d.py`，CP-SAT，解用 `pow()` 独立复核）

- (a0) base 2、所有 odd primes、`N = 24`：solver 自己**找到**了 covering `{3,5,7,13,17,241}`。搜索引擎在 covering 存在时会返回 Y。
- (b) 真实问题的 line restriction。把 class `c` 的 covering 限制到一条线上，得到 “每个 inert prime 至多贡献一个 residue class mod `h(p)`” 的一维 covering system，且任何这样的系统都能在单条线上实现。
  - `β`-line，`N = 315`：**COVERING 存在**，18 个 primes：`(p, h5, r)` = `(7,3,0) (11,5,3) (19,9,7) (31,3,2) (43,21,7) (71,5,1) (127,21,4) (211,35,22) (379,21,19) (631,35,15) (883,63,31) (1171,45,34) (5167,9,1) (7603,21,16) (19531,7,6) (23311,315,274) (34651,315,314) (169831,45,20)`。`N = 3465` 也存在（25 个 primes）。
  - `α`-line，`h3 | 315`：**INFEASIBLE**（14 个 primes，`Σ 1/h3 = 1.06 ≥ 1`，union bound 无法判定，exact solver 判定为否）。`h3 | 3465`（28 个 primes，`Σ 1/h3 = 1.41`）：CP-SAT 在 1200 s 内 UNKNOWN。
  - (a) base 2、只用 inert primes、`N = 630, 6930`：time limit 内 UNKNOWN。

结论：单条 `β`-line 可以被覆盖，所以一维 restriction 不构成障碍；二维 covering 要求所有 lines 用**同一组** `z_p` 同时被覆盖。

---

## 4. Phase 2B — `M = t` frontier

### 4.1 为什么 C22 在 `M = t = 23` 卡住，而它其实不 critical — FINITE COMPUTATION

C22 的 catalogue 限于 19-smooth orders，对 `M ≥ 23` 的 actives 只有 `1/M` 这个界，于是 `t/M = 1`。complete catalogue（`H < 32768`）给出：

| `M` | active inert primes | type V | type H | type B（both） | 最大的 `M` 个 `1/H_p` 之和 | type-B curve 在 fresh fibre 上的最大点数（`p ≤ 70000`） |
|---|---|---|---|---|---|---|
| 23 | 201 | 13 | 12 | 176 | **0.0952** | 12 / 23 |
| 29 | 155 | 3 | 12 | 140 | 0.0531 | 15 / 29 |
| 31 | 138 | 10 | 6 | 122 | 0.0264 | 6 / 31 |
| 37 | 118 | 9 | 5 | 104 | 0.0337 | 9 / 37 |
| 41 | 118 | 9 | 8 | 101 | 0.0459 | 21 / 41 |
| 43 | 96 | 6 | 3 | 87 | 0.0211 | 8 / 43 |
| 47 | 92 | 6 | 5 | 81 | 0.0210 | 15 / 47 |

`H_p` 最小的 23-active primes：`H = 23`（`p = 47`）、`69`、`111`、`115`、`299`、…。所以 `(M, t) = (23, 23)` 的 direct budget 远小于 1，Theorem R 的 budgets 已经把所有 `M ≤ 146` 的 frontier cases 一并处理。

### 4.2 Exact tiling 的算术结构 — PROVED（Theorem F）+ FINITE COMPUTATION

- **局部 tiling 存在。** 取前 23 个 type-V primes（`23 ‖ h3`，`23 ∤ h5`）：`5107, 8419, 15319, 31051, 45403, 45863, …, 345139`，class `10`。令 `a_i ≡ a* (mod lcm m_p)`、`a_i ≡ i (mod 23)`，`z_i = 3·9^{a_i} + 25^{b*} mod p_i`。则 lower point `(a*, b*)` 上的 fresh 23-fibre 被 23 条 vertical lines `X = i` **精确 partition**（`src/frontier.py` 逐点验证）。所以障碍不是 fibre 内部的局部算术。
- **全局不能延续。** tiling 只在 `⋂ G_p` 上存在，`μ(G_p) ≤ 1/m_p`，这里 `m_p = h3/23` 从 `3` 到 `7401`，故 `μ(⋂ G_p) ≤ 1/7401`。其余 `≥ 1 − 1/7401` 的 lower points 必须由 lower system 覆盖，问题原样递归到更小的 order primes，而它们各自又需要 `≥ ℓ` 个 actives（L3）。
- **`t = M` 的精确 partition 用 curves 不可能**（L4）：`z ≠ 0` 的 curve 至多 `M − 1` 点（不同 coset 时 `≤ (M−1)/2`）。

### 4.3 “lower fibres 能否处理” 的回答

在 C22 归纳框架内：能，且是定量的（Corollary F'，以及 Theorem R 的 budgets）。在 pure ACP 里：`t = M` 时 covering 被化归为 “lower system 覆盖 `E ∖ ⋂G_p`”，这与原问题同型，没有得到矛盾。**UNRESOLVED**：是否存在把这个递归变成 infinite descent 的论证。

---

## 5. Phase 3 — 结论

### 5.1 搜索范围（精确陈述）

1. 所有 `H_p < 32768` 的 inert primes（4161 个，complete）及其四个 classes 的 exact fibre statistics。
2. 对 `H_p < 16384` 的全部 2216 个 primes：不存在 covering（Theorem A；经 L3 化归到 257 个 primes，再用 exact measure certificate）。
3. 对任意 primes（包括 catalogue 之外）：`≤ 146` 个 fibres 不存在 covering（Theorem R，`Q = ∅`）。
4. 一维 line restrictions：见 §3.5。

没有做的事：没有在 `N²` 级别的 quotient 上对 “union bound `≥ 1`” 的大 prime 集做 ILP/SAT。原因是 Proposition H 之外的区域里，`Σ w ≥ 1` 且通过 L3 的 prime 集对应的 quotient 远超可枚举范围（rich core 在 `B = 32768` 已有 593 个 primes，order primes 到 47）。

### 5.2 Dichotomy verdict：undecided

- **支持 (N) 的证据。** (i) 147-fibre 下界与 `H ≥ 16384` 下界。(ii) L3 + Theorem F：每个 order prime `ℓ` 需要 `≥ ℓ` 个 actives，恰为 `ℓ` 时必须是同型平行直线，其 `G_p` 的交极小。(iii) class `(0,0)` 中 `z = 0` 的 fibre 全为空（`−1 ∉ ⟨9⟩⟨25⟩^{-1}`），只剩非线性 curves；纯 `z = 0` 系统在任何 class 都盖不住点 `(c1, c2)`（`3^{c1} + 5^{c2} ∈ {2, 4, 6, 8}` 没有 `> 3` 的 inert prime factor）— PROVED。(iv) HEURISTIC：非 coset 的 fibres 表现为伪随机 partition，随机模型下 covering 的期望个数在 quotient 增大时超指数趋于 0。
- **不能下结论的原因。** (i) Proposition H：fractional covering 存在，measure 方法无法证明 (N)。(ii) 一维类比（§3.5 的 `β`-line、Erdős covering）中 covering 确实存在，随机模型在一维是错的，所以 (iv) 只是 heuristic。(iii) 这个问题与 “是否存在 `Z` 使 `Z − 3^α − 5^β` 恒被有限个 primes 之一整除” 同型，是 two-parameter covering 问题；我不知道已有定理能判定它，也没有检索文献来确认其 open 状态（未引用任何外部定理）。
- **(Y-finite) / (Y-infinite)：** 没有任何 covering 可供分类。

### 5.3 证据所支持的最强一般性 lemma

Theorem F + Lemma L4（已证）：*fresh `M`-fibre 被 `M` 条 exponential curves `{3^α + 5^β ≡ z (mod p)}` 精确 tiling 是不可能的，除非它们是同型的 `M` 条平行直线；原因是 `(z−T)^M + T^M − A^M − B^M` 的次数为 `M − 1`、首项系数 `Mz`。*

猜想（UNRESOLVED，证据：§4.1 的 census 与 L4 的数值表）：type-B curve 在 fresh fibre 上至多 `(M+1)/2` 个点。若成立，则 `t < 2M − O(1)` 时 fresh fibre 上的 covering 必须含 `≥ M − (t − M) − 1` 条直线。

### 5.4 已知 GAP 与风险

- GAP-1：Theorem R 的一般情形依赖 (H1)(H2)，本报告没有重新证明它们。
- GAP-2：L4 的 same-coset 界非最优（见上）。
- GAP-3：`ν0` 由浮点 LP（scipy/HiGHS）找到；certificate 的正确性只依赖 exact 验证器，不依赖 LP。验证器与搜索代码共享 `core_tools.py` 中的 mass 计算函数，另有纯 Python 的独立核对只覆盖 `h3·h5 ≤ 40000` 的 primes。
- GAP-4：Theorem A 只在 `B = 16384` 验证；`B = 32768` 的 catalogue 已完成，但对应的 rich core（593 primes）没有做 certificate。
- 风险：class `11` 在 `K = 146` 的 margin 只有 `1.07·10^{-3}`。它是整数运算的结果，但对 catalogue 中任何一个 weight 的错误都敏感；Haar-only 的 `K = 29` 版本独立于 LP，可作为保守引用。

---

## 6. Replay

```
./run_all.sh            # quick：验证全部已存 certificates（本机实测约 22 分钟，2 cores）
./run_all.sh full       # 另外从零重建 catalogue 与 fibre statistics 并与存档比较（再加约 20 分钟；full 模式的各步骤单独跑过，但没有作为一条命令整体重放）
./run_all.sh full lp    # 再重跑产生 nu0 的 LP 搜索
AUDIT=<解压后的 audit 目录> ./run_all.sh    # 额外与 frozen C21 certificate.json 比对
```
依赖：python3、numpy、gmpy2、ortools（仅 `toy_1d.py`）、scipy（仅 `lp`）。

| 文件 | 作用 |
|---|---|
| `src/arith.py` | trial division、Pratt certificate、orders |
| `src/build_catalogue.py`、`src/verify_catalogue.py` | complete catalogue 及其独立复核 |
| `src/acp.py` | fibres、`coverage()`（reference decision procedure）、exact counts |
| `src/model.py`、`src/validate.py` | 定义级 `F_q(a)` 引擎与 24 项 validation |
| `src/compute_weights.py`、`src/verify_weights.py` | exact fibre statistics 及独立重算 |
| `src/core_tools.py`、`src/search_lp.py`、`src/verify_lp_cert.py` | rich core、LP 搜索、Theorem A 验证器 |
| `src/masses_under_nu.py`、`src/root_budget.py`、`src/verify_root_budget.py` | Theorem R |
| `src/horizon.py` | Proposition H |
| `src/frontier.py` | L4 brute force、census、local tiling |
| `src/toy_1d.py` | one-parameter controls |
| `certs/` | catalogue、weights、四个 `ν0`、各验证器输出 |

---

=== RESULT CARD ===
Headline (one sentence): 没有找到 covering；在 pretend model 中任何 covering 至少需要 147 个 fibres 且必含 `H_p ≥ 16384` 的 prime，`M = t` frontier 被 polynomial lemma 化解，但 (N) 仍未证明，而且可以证明 measure 方法本身证不了它。

ACP formalization (one paragraph, exact): 固定 parity class `c = (c1, c2)`（`α = c1 + 2a`，`β = c2 + 2b`）。对 inert prime `p > 3`，`F_p^c(z) = {(a, b) ∈ Z/h3(p) × Z/h5(p) : 3^{c1}9^a + 5^{c2}25^b ≡ z (mod p)}`。ACP_c(T, z)：有限个 distinct inert primes 的 fibres 是否覆盖 `Z/lcm h3 × Z/lcm h5`。Joint-nonregular（或 pretend）prime 的 bad set ⊆ fibre，且选 lift `a mod p²` 可使其等于整个 fibre（pigeonhole，fibre 至多 `p − 1` 个 tame classes）；regular prime 的 bad set 也 ⊆ fibre；2-adic 条件恰好杀死一个 class（`a` 偶）或一个 `α`-parity（`a` 奇），prime 3 只部分影响一个 `β`-parity。所以 zero ⟹ 某个 class 被 fibres 覆盖；(N) ⟺ 没有任何 class 可被覆盖。对固定 `(q, a)`，真实 zero condition 严格强于 unit-avoidance 失败，但存在性上两者等价。

Strongest claim + tag: Theorem R(146)——任意 `≤ 146` 个 unit targets 加任意 regular norm 条件都留下正测度，故 `f_q(a) = 0` 需要 `≥ 147` 个 joint-nonregular primes：CONDITIONAL（C21 的 rigidity 与 regular averaging lemma）+ FINITE COMPUTATION；其 `Q = ∅` 特例（任何 covering `≥ 147` fibres）与 Theorem A（必含 `H_p ≥ 16384`）：PROVED + FINITE COMPUTATION。结构性最强结论：Theorem F / Lemma L4（exact tiling ⟹ 同型平行直线）：PROVED；Proposition H（measure 方法在 `X0 = 473899` 处失效）：PROVED NEGATIVE STRUCTURAL THEOREM。

Dichotomy verdict: (N) / (Y-finite) / (Y-infinite) / undecided — reason in one sentence: **undecided**——所有证据指向 (N)，但 fractional covering 存在（Proposition H）且一维类比中 covering 真实存在，现有工具无法排除巨大 prime 集上的 integral covering。

Search space covered and certificates produced: complete catalogue `H_p < 32768`（4161 个 inert primes，gcd 构造 + brute-force 扫描到 `1.1·10^8` + modular route 复核）；四个 classes 的 exact fibre statistics；Theorem A 的四个 measure certificates（bounds `0.683 / 0.773 / 0.745 / 0.787`）；Theorem R 的 `4 × 2301` 个 exact budgets（`K = 146`）与 Haar-only 的 `K = 29`；L4 对 `M ≤ 23`、`p < 20000` 的 brute force；`M = 23..47` 的 active-prime census 与一个显式的 local tiling；一维 controls（含一个显式的 18-prime `β`-line covering）；24 项 Phase-1 validation（含 C21 的 29 个与 C22 的 33 个 budgets 的复现）。

What a verifier should check first (3 items): (1) Theorem R 证明中 direct budget 的完备性——critical cases 是否确为 `7 < M ≤ K`、`M ≤ t ≤ K` 加 base，placeholder `τ = ρ_max/B` 对 catalogue 外的 primes 是否合法，以及 (H1)(H2) 的原文假设是否被准确使用；(2) catalogue 的 completeness 论证（`p | G ⟺ h3, h5 < B`）与 `verify_catalogue.py` 的三条独立路线；(3) Lemma L4 的多项式论证（次数 `M − 1`、对合 `T ↦ z − T`、same-coset 的系数比较）与 Theorem F 中 “不交直线必平行” 的使用。

Suggested next step: 放弃继续抬高 `K`（Proposition H 已说明这条路有上限），转向 integrality：尝试把 Theorem F 的递归（`U ⊆ ⋂ G_p`，lower system 必须覆盖 `E ∖ ⋂ G_p`）做成对 order primes 的 descent，并先证明或否定 “type-B curve 至多 `(M+1)/2` 点” 这一猜想；同时请人类数学家审阅 (H1)(H2) 与 Theorem R 的归纳。
=== END CARD ===
