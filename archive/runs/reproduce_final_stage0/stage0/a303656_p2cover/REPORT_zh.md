# A303656：finite \(p^2\)-cover 路线的严格审计与计算结果

## 最终结论：B

对明确的完整素数族

\[
\mathcal F_{5000}=\left\{p:\ p\equiv3\pmod4,\ p\nmid15,\ 
\max(\operatorname{ord}_p(3),\operatorname{ord}_p(5))\le5000\right\}
\]

得到了 **certified UNSAT**：无论怎样选取 \(P\subseteq\mathcal F_{5000}\) 及 \(t_p\bmod p^2\)，都不可能形成 finite \(p^2\)-cover。

这不是 SAT solver 的无证明 UNSAT；它来自一个严格的局部容量不等式，并由独立 GMP verifier 用精确整数/有理数运算核验。没有找到全局 finite \(p^2\)-cover certificate，因此没有 \(t_p\)、CRT 模数或 \(n_0\) 可输出。

---

## 1. Reduction 审计

设 \(P\) 是有限个满足 \(p\equiv3\pmod4\)、\(p\nmid15\) 的素数。假设对每个 \(p\in P\) 给定 \(t_p\bmod p^2\)，且对每个 \(c,d\ge0\)，至少存在一个 \(p\in P\) 使

\[
t_p-3^c-5^d\equiv p w\pmod{p^2},\qquad p\nmid w.
\]

因为不同 \(p^2\) 两两互素，CRT 给出唯一剩余类

\[
n\equiv t_p\pmod{p^2}\quad(p\in P)
\]

模 \(M=\prod_{p\in P}p^2\)。对任意落在该剩余类中的整数 \(n\)，以及任意 \(c,d\ge0\)，令

\[
m=n-3^c-5^d.
\]

由假设，某个 \(p\in P\) 满足 \(p\mid m\) 而 \(p^2\nmid m\)，故 \(v_p(m)=1\)。于是：

* 若 \(m>0\)，它不可能是两个整数平方之和，因为一个 \(3\pmod4\) 素数以奇指数出现；
* 若 \(m=0\)，则 \(m\equiv0\pmod{p^2}\)，与 \(v_p(m)=1\) 矛盾；
* 若 \(m<0\)，它显然不可能等于 \(a^2+b^2\)。

因此该 CRT 剩余类中的每个 \(n>1\) 都是反例，且这样的正整数有无穷多个。

### 审计结论

**PROVED**：remainder \(=0\) 没有遗漏；负 remainder 与非负 remainder 均处理正确；CRT 条件兼容；reduction 无错误。

由于 \(p\nmid15\)，3 与 5 都是模 \(p^2\) 的单位，故从指数 0 开始纯周期：

\[
3^{c+\operatorname{ord}_{p^2}(3)}\equiv3^c\pmod{p^2},\qquad
5^{d+\operatorname{ord}_{p^2}(5)}\equiv5^d\pmod{p^2}.
\]

所以完整指数空间确切地缩减为

\[
\mathbb Z/L_3\mathbb Z\times\mathbb Z/L_5\mathbb Z,
\quad
L_3=\operatorname{lcm}_{p\in P}\operatorname{ord}_{p^2}(3),
\quad
L_5=\operatorname{lcm}_{p\in P}\operatorname{ord}_{p^2}(5).
\]

---

## 2. 必要条件与严格 pruning

令

\[
r_p=\operatorname{ord}_p(3),\qquad s_p=\operatorname{ord}_p(5).
\]

对固定 \(p\) 和 \(t\bmod p\)，定义

\[
A_p(t)=\{(u,v)\in\mathbb Z/r_p\times\mathbb Z/s_p:
3^u+5^v\equiv t\pmod p\}.
\]

固定 \(u\) 后，\(5^v\) 在一个周期内互异，所以至多有一个 \(v\)；故 \(|A_p(t)|\le r_p\)。交换两变量又有 \(|A_p(t)|\le s_p\)。因此

\[
\frac{|A_p(t)|}{r_ps_p}\le\frac1{\max(r_p,s_p)}.
\]

把各局部周期提升到

\[
R=\operatorname{lcm}_{p\in P}r_p,
\qquad S=\operatorname{lcm}_{p\in P}s_p,
\]

每个局部点恰有 \((R/r_p)(S/s_p)\) 个提升。因此若

\[
\sum_{p\in P}\frac1{\max(r_p,s_p)}<1,
\]

则模 \(p\) 可整除集合的并集严格小于整个 \(R\times S\) torus，存在一个 \((c,d)\) 对所有 \(p\in P\) 都不满足

\[
p\mid t_p-3^c-5^d.
\]

而 \(p^2\)-cover 必须先满足模 \(p\) 可整除，因此不可能成立。

**PROVED**：这是严格 union-bound pruning，不是 density heuristic。

### 更强的精确局部容量

计算

\[
\beta_p=rac1{r_ps_p}\max_{t\bmod p}|A_p(t)|.
\]

同一证明给出更强必要条件

\[
\sum_{p\in P}\beta_p\ge1.
\]

这仍然只使用模 \(p\) 的整除 cover，所以对任何 \(p^2\)-cover 都是严格必要条件。

---

## 3. 完整枚举 \(\mathcal F_{5000}\) 与 certified pruning

定义

\[
A_B=\prod_{k=1}^{B}(3^k-1),\qquad
C_B=\prod_{k=1}^{B}(5^k-1),\qquad
G_B=\gcd(A_B,C_B).
\]

对任意 \(p\nmid15\)，

\[
p\mid G_B
\iff \operatorname{ord}_p(3)\le B\ \text{且}\ \operatorname{ord}_p(5)\le B.
\]

因此完整因子分解 \(G_{5000}\) 后筛出 \(p\equiv3\pmod4\)，就得到完整的 \(\mathcal F_{5000}\)，没有素数大小上界。

独立 verifier 完成了以下检查：

1. 重新用 GMP 构造 \(A_{5000},C_{5000}\) 和 \(G_{5000}\)；
2. 检查证书中 1224 个不同素因子均为素数；
3. 检查其带重数乘积精确等于 \(G_{5000}\)；
4. 筛出 527 个合格素数；
5. 对每个素数重新计算 \(r_p,s_p,\operatorname{ord}_{p^2}(3),\operatorname{ord}_{p^2}(5)\)；
6. 枚举 \(r_ps_p\) 个局部指数对，精确计算 \(\beta_p\)；
7. 用 GMP 有理数而非浮点数比较所有不等式。

核验输出：

```text
VERIFIED
B=5000
eligible_prime_count=527
sum_loose_decimal=1.2665065873636761
top65_loose_decimal=0.99943786675097401
top66_loose_decimal=1.0016165159884467
sum_exact_alpha_decimal=0.97307606772937005
alpha_above_1_over_5001_count=388
alpha_above_1_over_5001_sum_decimal=0.95810404892019441
upper_capacity_597_primes_decimal=0.99989569059186001
upper_capacity_598_primes_decimal=1.0000956505998584
minimum_primes_with_max_order_above_B=135
cardinality_lower_bound=598
```

由此得到：

* **PROVED / CERTIFIED BY VERIFIER**：任何只使用 \(\mathcal F_{5000}\) 中素数的集合都不能 cover，因为所有 527 个素数的精确容量总和仍小于 1。
* **PROVED / CERTIFIED BY VERIFIER**：题目指定的 \(1/\max(r_p,s_p)\) lemma 单独给出全局 \(|P|\ge66\)：全体候选中最大的 65 个权重之和仍小于 1。
* **PROVED / CERTIFIED BY VERIFIER**：精确容量把全局必要下界提高到
  \[
  |P|\ge598.
  \]
* **PROVED / CERTIFIED BY VERIFIER**：任何 cover 至少要含 135 个满足 \(\max(r_p,s_p)>5000\) 的素数。

### 按 \(\max(r_p,s_p)\) 排序的表格节选

| p | ord_p(3) | ord_p(5) | ord_{p²}(3) | ord_{p²}(5) | 1/max | maxfiber | β_p |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 11 | 5 | 5 | 5 | 55 | 1/5 | 3 | 3/25 |
| 7 | 6 | 6 | 42 | 42 | 1/6 | 6 | 1/6 |
| 19 | 18 | 9 | 342 | 171 | 1/18 | 9 | 1/18 |
| 23 | 11 | 22 | 253 | 506 | 1/22 | 11 | 1/22 |
| 67 | 22 | 22 | 1474 | 1474 | 1/22 | 22 | 1/22 |
| 59 | 29 | 29 | 1711 | 1711 | 1/29 | 15 | 15/841 |
| 31 | 30 | 3 | 930 | 93 | 1/30 | 3 | 1/30 |
| 271 | 30 | 27 | 8130 | 7317 | 1/30 | 7 | 7/810 |
| 71 | 35 | 5 | 2485 | 355 | 1/35 | 4 | 4/175 |
| 43 | 42 | 42 | 1806 | 1806 | 1/42 | 42 | 1/42 |
| 47 | 23 | 46 | 1081 | 2162 | 1/46 | 23 | 1/46 |
| 131 | 65 | 65 | 8515 | 8515 | 1/65 | 33 | 33/4225 |
| 151 | 50 | 75 | 7550 | 11325 | 1/75 | 29 | 29/3750 |
| 79 | 78 | 39 | 6162 | 3081 | 1/78 | 39 | 1/78 |
| 83 | 41 | 82 | 3403 | 6806 | 1/82 | 41 | 1/82 |
| 179 | 89 | 89 | 15931 | 15931 | 1/89 | 45 | 45/7921 |
| 191 | 95 | 19 | 18145 | 3629 | 1/95 | 14 | 14/1805 |
| 2851 | 38 | 95 | 108338 | 270845 | 1/95 | 19 | 1/190 |
| 103 | 34 | 102 | 3502 | 10506 | 1/102 | 34 | 1/102 |
| 107 | 53 | 106 | 5671 | 11342 | 1/106 | 53 | 1/106 |

完整 527 行见 `output/primes_B5000_verified_by_order.csv`。

---

## 4. Method A：显式 bitset

实现：`src/method_a_bitset.py`。

对给定 \(P\)，精确构造

\[
C(p,t)=\{(u,v)\in\mathbb Z/L_3\times\mathbb Z/L_5:
(t-3^u-5^v)\bmod p^2\in p\mathbb Z\setminus p^2\mathbb Z\}.
\]

每个集合用 packed bitset 表示；DFS 选择每个 \(p\) 的一个 \(t\)，并用剩余集合的乐观并集作安全剪枝。

### 实际运行：\(P=\{7,11\}\)

```text
L3 = 210
L5 = 2310
|U| = 485100
cover_found = false
best_t = (0,2)
best_covered = 114660
uncovered_at_best = 370440
```

该实例的 bitset 搜索完整结束。加入 \(p=19\) 后，

```text
L3 = 11970
L5 = 131670
|U| = 1576089900
```

程序按设定阈值拒绝物化，展示了显式 torus 的扩张问题。

**COMPUTATIONAL OBSERVATION**：bitset 结果本身未生成 DRAT/LRAT 类证明文件，因此不把 solver 输出单独称为 certified UNSAT；该小实例同时已被 \(1/\max\) lemma 严格排除。

---

## 5. Method B：lazy constraint generation

实现：`src/method_b_lazy.py`。

### Candidate CSP

写

\[
t_p=q_p+p h_p,
\qquad 0\le q_p,h_p<p.
\]

对于固定指数对，令

\[
3^c+5^d\equiv q+p h\pmod{p^2}.
\]

则 \(p\) 覆盖该点当且仅当

\[
q_p=q,\qquad h_p\ne h.
\]

所以每个 adversarial pair 加入一个精确约束

\[
\bigvee_{p\in P}(q_p=q_{p,c,d}\land h_p\ne h_{p,c,d}).
\]

### Exact adversarial oracle

oracle 不物化 \(L_3L_5\)。对每个 \(p\) 引入局部状态

\[
c_p\bmod r_{p,2},\qquad d_p\bmod s_{p,2},
\]

其中 \(r_{p,2}=\operatorname{ord}_{p^2}(3)\)、\(s_{p,2}=\operatorname{ord}_{p^2}(5)\)。对任意两个素数加入

\[
c_p\equiv c_q\pmod{\gcd(r_{p,2},r_{q,2})},
\qquad
d_p\equiv d_q\pmod{\gcd(s_{p,2},s_{q,2})}.
\]

广义 CRT 表明这些两两相容条件是存在全局 \(c,d\) 的充要条件。

为避免长度 \(p r_p\) 的幂表，使用精确提升公式。若

\[
3^{r_p}\equiv1+pA_p\pmod{p^2},
\qquad c_p=u+r_pk,
\]

则

\[
3^{c_p}\equiv3^u(1+pA_pk)\pmod{p^2}.
\]

5 的处理相同。因为 \(\operatorname{ord}_{p^2}(3)/r_p\in\{1,p\}\)，该表示覆盖全部局部状态。

因此 exact oracle 是一个有限 modular CSP，其状态规模由各局部周期和 gcd 兼容关系给出，而不是 \(L_3\times L_5\) 的笛卡尔积。SMT 返回 SAT 时，代码用广义 CRT 重建全局 \((c,d)\)，再以 Python 精确模幂独立检查它确实未被任何 \(p\) 覆盖。

### 实际运行

1. \(P=\{7,11,19\}\)，强制调用 exact CRT oracle：

```text
torus cardinality = 1576089900
oracle = SAT
(c,d) = (11634,84482)
```

该 witness 被直接模 \(p^2\) 运算复核。

2. \(P=\{7,11\}\)，绕过预先 pruning 以测试 lazy loop：candidate solver 在 3 个已加入约束后返回 UNSAT；没有正式 SAT proof，所以只记为 **COMPUTATIONAL OBSERVATION**。数学上的不可能性由 lemma 独立保证。

3. 前 10 个小-order 素数：全 torus 大小为 39 位数；lazy loop 生成 28 个精确反例约束后 candidate solver 超时并返回 UNKNOWN。

**UNRESOLVED**：该 timeout 不构成任何数学结论。

4. 按 \(1/\max\) 排名前 66 个素数：松弛容量和为 \(1.0016165>1\)，所以通过题目指定的初级 pruning；但精确容量和仅为 \(0.7871147<1\)，因此被更强的严格 pruning 排除。其 torus cardinality 有 379 位数；lazy loop 的 5 次测试均立即找到精确未覆盖点。

---

## 6. 证书与 verifier 状态

### 已有正式证书

`cert/gcd_factor_B5000.txt` 是 \(G_{5000}\) 的完整因子分解证书。

`src/verify_pruning.cpp` 不依赖 Z3、SAT solver 或浮点数；它使用 GMP 精确重算并验证：

* 完整素数族枚举；
* 所有 order；
* 所有局部最大 fiber；
* 容量总和；
* \(\mathcal F_{5000}\) 的 UNSAT；
* \(|P|\ge598\) 与至少 135 个高-order 素数的必要条件。

### 没有 finite \(p^2\)-cover certificate

因此以下项目不存在，不能输出：

* prime set \(P\) 与全部 \(t_p\)；
* CRT 解 \(n_0\bmod M\)；
* 独立 cover verifier 的成功记录。

没有声称任何整数是 counterexample。

---

## 7. 实验纪律标签

| 标签 | 本次结果 |
|---|---|
| **PROVED** | reduction；周期性；\(1/\max\) lemma；精确容量 lemma；gcd 枚举等价性。 |
| **CERTIFIED BY VERIFIER** | \(\mathcal F_{5000}\) 完整枚举与 UNSAT；\(|P|\ge598\)；至少 135 个高-order 素数。 |
| **COMPUTATIONAL OBSERVATION** | Method A 的 \(\{7,11\}\) 搜索统计；lazy solver 的小实例 UNSAT/UNKNOWN 行为。 |
| **HEURISTIC** | lazy oracle 的 grid/random 快速找 witness 阶段；每个返回的 witness 都会精确检查，但搜索失败本身不作结论。 |
| **UNRESOLVED** | 是否存在使用大量 \(\max(r_p,s_p)>5000\) 素数的 finite \(p^2\)-cover。 |

---

## 8. 复现

依赖：Python 3、NumPy、SymPy、z3-solver、C++17、GMP。

```bash
cd a303656_p2cover
python -m pip install -r requirements.txt
./run_reproduce.sh
```

从头重建 gcd 因子分解证书：

```bash
REGENERATE_CERT=1 ./run_reproduce.sh
```
