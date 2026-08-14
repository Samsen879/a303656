# OEIS A303656：Bounded Self-Consistent Counterexample Search

## 0. 最终结论与分级

本轮没有找到 certified counterexample。

本轮允许的最终结论类型中，结论属于 **B**：

> 对下面逐项写明的有限整数区间，两个独立实现进行了 exact exhaustive computation，均得到 counterexample candidate set 为空。

最强连续结果是

\[
240000000001\le n\le241600000000,
\]

即从已知验证上界之后连续检查了

\[
1,600,000,000
\]

个整数。两套程序都直接枚举原表示

\[
n=a^2+b^2+3^c+5^d
\]

而不只搜索某个有限 obstruction-prime family；因此这个有限区间的空结果比“固定 prime pool 下没有 valuation-one certificate”更强。

再加上 21 个远端窗口、3 个对数尺度窗口以及两个跨 exponent-activation 边界的窗口，两个独立实现共同精确检查了

\[
1,853,000,000
\]

个互不重叠的整数，candidate count 均为 0。两个实现逐窗口匹配的无序平方对总数为

\[
108,943,945,529.
\]

机器可读总审计：`output/formal_results_audit.json`。

严格标签如下。

| 事项 | 标签 |
|---|---|
| valuation-one certificate criterion | **PROVED** |
| 上一阶段 527 / 598 / 135 baseline | **REPRODUCED FROM SOURCE / CERTIFIED BY VERIFIER** |
| 明确列出的双实现有限区间原问题搜索 | **INDEPENDENTLY REPRODUCIBLE EXACT EXHAUSTIVE FINITE COMPUTATION** |
| 全部 \(p\equiv3\pmod4\) 的 exact-one、\(\{1,3\}\)、任意奇 valuation 有限搜索 | 按下文分别标为双实现或单实现的 **EXACT EXHAUSTIVE FINITE COMPUTATION** |
| Direct SMT / CEGIS timeout 或无 proof-object UNSAT | **UNKNOWN** 或 **SMT UNSAT WITHOUT PROOF OBJECT** |
| 是否存在任意大小的 counterexample | **UNRESOLVED** |

这些计算不证明原猜想在无限范围内成立，也不应解释为“支持猜想为真”。

---

## 1. valuation-one certificate criterion 的严格审计

令

\[
s(c,d)=3^c+5^d,
\qquad r=n-s(c,d).
\]

假设 \(n>1\)，并且存在有限素数集

\[
P\subset\{p:p\text{ prime},\ p\equiv3\pmod4\}
\]

使得每个满足 \(s(c,d)\le n\) 的非负整数对 \((c,d)\) 都有某个 \(p\in P\) 满足

\[
p\mid r,\qquad p^2\nmid r.
\]

这等价于 \(v_p(r)=1\)。则 \(n\) 不可表示为

\[
n=a^2+b^2+3^c+5^d
\]

其中 \(a,b,c,d\ge0\)。

### 1.1 情形 \(r>0\)

若存在表示，则

\[
r=a^2+b^2>0.
\]

Fermat 两平方定理适用于正整数：一个正整数能写成两个整数平方之和，当且仅当它的素因子分解中每个
\(q\equiv3\pmod4\) 的指数均为偶数。certificate 却给出某个 \(p\equiv3\pmod4\) 满足
\(v_p(r)=1\)，矛盾。

### 1.2 情形 \(r=0\)

此时只能有 \(a=b=0\)。但对任意素数 \(p\)，都有

\[
p^2\mid0.
\]

所以条件

\[
0\equiv0\pmod p,
\qquad
0\not\equiv0\pmod{p^2}
\]

永远不成立。两个 theorem verifier 都显式要求 `remainder > 0`，并用 \(n=2,s=2\) 的故意错误输入验证了拒绝路径。

### 1.3 情形 \(r<0\)

若 \(s(c,d)>n\)，则

\[
r=n-s(c,d)<0,
\]

而 \(a^2+b^2\ge0\)。因此这些 pair 不可能参与表示，不需要 certificate 覆盖。反过来，任何真实表示对应的 pair 自动满足 \(s(c,d)\le n\)。

### 1.4 Fermat 两平方定理的适用条件

定理只在上述 \(r>0\) 分支使用；\(r=0\) 和 \(r<0\) 已分别单独处理。因此没有把零的 valuation 当作有限整数，也没有把定理错误地应用到负数。

### 1.5 \(p=3\) 完全合法

\(3\) 是素数且

\[
3\equiv3\pmod4.
\]

obstruction 检查作用于 remainder \(n-3^c-5^d\)，并不要求底数 3 或 5 在模 \(p^2\) 下可逆。上一阶段 global periodic-cover 排除 \(p\mid15\) 是另一个问题的单位性要求；本轮 fixed-\(n\) bounded search 没有该限制。全部 prime pools 都保留了 \(p=3\)。

### 1.6 exponent enumeration 完整

Python verifier 从 1 开始反复乘 3，生成全部且仅全部满足 \(3^c\le n\) 的幂；对 5 同理。随后枚举笛卡尔积并只保留

\[
3^c+5^d\le n.
\]

若某 pair 满足这个不等式，则两个正项分别不超过 \(n\)，所以一定已出现在两个幂表中。过程只用 exact integer multiplication、comparison 和 modular arithmetic，不使用 floating-point logarithm。

不同 exponent pairs 可能给出同一 shift。例如

\[
3^1+5^2=28=3^3+5^0.
\]

搜索器可以对相同 shift 共享一个条件，但 theorem verifier 始终逐 exponent pair 输出 obstruction row，不会丢失 duplicate pair。

**审计结论：PROVED。** reduction 没有错误，可以合法地进行 bounded search。

---

## 2. Stage 0：上一阶段 artifact baseline

上传归档复制为：

`baseline/a303656_p2cover_bundle.zip`

SHA256：

```text
4dadb8ce07cd0ccf56575ef0882d6bb02284a02c61e05cd1424e070d83b22ff3
```

执行了以下步骤：

1. 检查上传 ZIP 的 SHA256；
2. 解压后对归档内 `SHA256SUMS` 的全部条目执行校验，全部为 `OK`；
3. 不信任归档内预编译 binary，从 `src/verify_pruning.cpp` clean rebuild；
4. 运行 clean verifier，并把重新生成的 527 行 prime CSV 与归档版本逐字节比较；
5. 在当前独立 Python 环境中运行上一阶段自己的 `run_reproduce.sh`。

最终 clean run 的核心输出为：

```text
eligible_prime_count=527
sum_exact_alpha_decimal=0.97307606772937005
upper_capacity_597_primes_decimal=0.99989569059186001
upper_capacity_598_primes_decimal=1.0000956505998584
minimum_primes_with_max_order_above_B=135
cardinality_lower_bound=598
```

当前最终复现中 clean verifier 用时 19.31 秒，并输出 `VERIFIED`。完整记录：

- `logs/final_audit/run_reproduce_stage0_current.log`
- `reproduce_stage0_current/logs/stage0_internal_sha256.log`
- `reproduce_stage0_current/logs/stage0_verify_pruning.log`
- `reproduce_stage0_current/logs/stage0_bundle_run_reproduce.log`
- `reproduce_stage0_current/logs/stage0_bundle_run_reproduce.trace`

本轮没有扩大 \(B\)，没有重新进行 global torus-cover 搜索。

---

## 3. 两个独立 theorem verifiers

### 3.1 Python exact verifier

文件：`src/verifier.py`

它使用 Python arbitrary-precision integers，并且：

- exact 枚举所有 powers 和全部 admissible exponent pairs；
- 检查 `remainder > 0`；
- 检查 `r % p == 0` 且 `r % (p*p) != 0`；
- exact 计算并输出 valuation；
- 验证每个 pool 元素确为素数且 \(p\equiv3\pmod4\)；
- 若给出 assignment CSV，则要求它恰好覆盖全部 admissible pairs，既不能缺 pair，也不能加入非 admissible pair；
- 输出 pair count、distinct shift count、每个 pair 的 obstruction、uncovered pairs 和 PASS/FAIL；
- PASS 时可生成 `cert/counterexample.json` 和 `cert/obstructions.csv`；
- 不导入 Z3、CP-SAT、MILP 或搜索器。

### 3.2 C++/GMP exact verifier

文件：`src/verifier_gmp.cpp`

这是独立实现：

- `mpz_class` 表示 \(n\)、powers、shift 和 remainder；
- 独立 power/pair enumeration；
- 独立 prime-pool parser 和 primality check；
- 可读取 Python 生成的 assignment CSV；
- 显式检查 missing/extra assignment rows；
- 不依赖 Z3 或任何搜索器。

### 3.3 fault injection 与 toy tests

已完成：

- \(n=2\)：出现 remainder 0；Python 与 C++/GMP 均 FAIL；
- \(n=5,P=\{3\}\)：shift 2 的 remainder 3 被 \(p=3\) exact-one 阻挡，但完整域还含 shift 4，其 remainder 1 未覆盖；两个 verifier 均 FAIL；
- 人工遗漏一个 admissible pair 的 assignment CSV 被拒绝；
- unit-test-only 的 restricted synthetic core 对 `n=5, shift=2, p=3` 返回 PASS，验证正分支；生产 theorem verifier 对同一 \(n\) 仍因完整域而拒绝。

这里不能制造一个“完整 theorem verifier 接受的小范围 toy n”，因为那本身就会是原问题的真实 counterexample。故正分支使用明确标注的 synthetic restricted core，而生产 verifier 的完整域绝不放宽。

由于没有找到 candidate，`cert/` 中没有伪造的 `counterexample.json` 或 `obstructions.csv`；`cert/NO_COUNTEREXAMPLE_CERTIFICATE.txt` 明确记录这一点。

---

## 4. 有限 exponent domain

所有正式程序都在运行时检查

\[
N_{\rm high}<3^{C+1}+1,
\qquad
N_{\rm high}<5^{D+1}+1.
\]

例如连续主区间使用

\[
C=23,\qquad D=16,
\]

并检查

\[
241600000000<3^{24}+1=282429536482,
\]

\[
241600000000<5^{17}+1=762939453126.
\]

因此所有 admissible pairs 自动满足 \(0\le c\le23,0\le d\le16\)。在该主区间的最高端共有 407 个 exponent pairs、406 个 distinct shifts，唯一 duplicate shift 是 28。

程序不是静态地假设这些 bounds；跨越激活边界时会提高 \(C\) 或 \(D\)：

- 跨 \(3^{24}+1=282429536482\) 的窗口使用 \(C=24,D=16\)；
- 跨 \(5^{17}+1=762939453126\) 的窗口使用 \(C=24,D=17\)；
- \(10^{12},10^{13},10^{14}\) 附近窗口分别使用 \((C,D)=(25,17),(27,18),(29,20)\)。

---

## 5. 用户要求的 Method A、B、C

### 5.1 Method A：Direct Z3 Int

文件：`src/search_z3_direct.py`

对整数变量 \(n\)，每个 relevant pair 的 clause 是

\[
3^c+5^d\le n\Longrightarrow
\bigvee_{p\in P}
\left(
 n\equiv3^c+5^d\pmod p
 \land
 n\not\equiv3^c+5^d\pmod{p^2}
\right).
\]

powers 在 solver 外用 exact Python integers 预计算；脚本不用 `Optimize`，支持 interval splitting，并在 SAT 时立即调用独立 Python verifier。

结果：

- toy `[2,50]`, \(P=\{3,7,11,19\}\)：Z3 `unsat`；无 proof object，只记 SMT observation；Method C 对同一区间给出 exact empty；
- 正式 `[240000000001,240000000100]`，ranked 16-prime pool：`UNKNOWN(timeout)`；
- 同一区间 ranked 32-prime pool：`UNKNOWN(timeout)`。

UNKNOWN 不构成数学结论。

### 5.2 Method B：CEGIS

文件：`src/search_z3_cegis.py`

每轮：

1. candidate solver 仅含当前积累的 pair clauses；
2. 得到 candidate \(n\)；
3. exact adversary 按当前 \(n\) 从头枚举全部 \(3^c+5^d\le n\) 的 pairs；
4. 找到第一个 uncovered pair 后加入精确 modular clause；
5. adversary 无反例时才调用独立 theorem verifier。

JSONL 每轮记录 candidate、active pair count、新 pair、pool size、solver time、verifier time 和 termination reason。

正式 100-number pilot：

- ranked 16-prime pool：若干 candidate 被 adversary 反驳，随后 Z3 返回 UNSAT；无 proof object，标签 `SMT_UNSAT_WITHOUT_PROOF_OBJECT`；
- ranked 32-prime pool：`UNKNOWN`。

### 5.3 Method C：exact finite interval scan

文件：

- `src/search_bitset.cpp`；
- independent clean-room `src/search_exhaustive_clean.cpp`；
- 第三个较慢实现 `src/search_exhaustive_python.py`。

它们 exact 检查 fixed prime pool 下每个 active shift 的 valuation-one predicate。正式结果：

\[
[240000000001,240010000000]
\]

使用 `output/primes_ranked_256.txt` 的 256 个素数，两个独立 C++ 实现逐个检查全部 10,000,000 个整数，candidate count 为 0。

标签：

> **INDEPENDENTLY REPRODUCIBLE EXACT EXHAUSTIVE FINITE COMPUTATION FOR THIS FIXED 256-PRIME EXACT-ONE FAMILY**

它只排除该固定 pool 的 certificate family，不推出该区间没有原问题 counterexample。后面的 direct two-square search 才给出原问题本身的更强有限结论。

---

## 6. bounded prime-pool 策略

文件：

- `src/prime_analysis.py`
- `src/prime_solver_impact.py`
- `output/formal_prime_metrics.csv`
- `output/formal_prime_metrics.json`

从前 512 个 \(p\equiv3\pmod4\) 素数开始，保留 \(p=3\)，并对正式 bounded shift family 计算：

- exact marginal incidence count 和有理数比例；
- shift residue buckets；
- 最大 pair bucket；
- duplicate/overlap pair count；
- conflict pair count；
- bounded compatibility heuristic；
- cumulative solver branching impact pilot。

这不是上一阶段 global \(\beta_p\) 排名，也不只是按 \(1/p\)。ranked top 16 为：

```text
3,7,11,19,23,31,67,71,43,47,59,83,103,79,107,127
```

正式 base family 有 407 pairs、406 distinct shifts。前几项的 bounded 指标为：

| rank | p | max pair bucket | overlap pairs | exact marginal incidence fraction |
|---:|---:|---:|---:|---:|
| 1 | 3 | 206 | 39671 | 0.22222223366093366 |
| 2 | 7 | 67 | 11681 | 0.122448983783783785 |
| 3 | 11 | 55 | 8494 | 0.082644637592137596 |
| 4 | 19 | 25 | 4199 | 0.049861497788697785 |
| 5 | 23 | 22 | 3468 | 0.041587902948402949 |
| 6 | 31 | 17 | 2672 | 0.031217484275184275 |

pool sizes 16、32、64、128、256、512 均有显式文本文件。完整 ranking 与 prime-by-prime metrics 在 `output/` 中。

---

## 7. all-prime exact valuation search 与 higher odd valuation

有限 prime pool 没有找到 candidate 后，实现了两个独立 segmented factor-sieve：

- `src/search_factor_sieve.cpp`；
- `src/search_factor_sieve_clean.cpp`。

对每个正 remainder，它们用全部不超过当前 factor-range 平方根的素数做 exact segmented division。移除这些素因子后，任何 residual \(>1\) 必为 exponent 1 的素数；所以没有遗漏大素因子。所有平方根均为 integer sqrt。

模式：

- `max_odd=1`：允许 \(v_p=1\)；
- `max_odd=3`：允许 \(v_p\in\{1,3\}\)；
- `max_odd=-1`：允许任意奇 valuation。

双实现 exact 结果：

| interval | valuation family | candidates |
|---|---|---:|
| `[240000000001,240100000000]` | all \(p\equiv3\pmod4\), \(v_p=1\) | 0 |
| 同上 | all \(p\equiv3\pmod4\), \(v_p\in\{1,3\}\) | 0 |
| 同上 | all \(p\equiv3\pmod4\), arbitrary odd \(v_p\) | 0 |
| `[282300000001,282400000000]` | all \(p\equiv3\pmod4\), \(v_p=1\) | 0 |

另有 primary implementation 单独完成：

- exact-one `[240000000001,241000000000]`：0 candidates；
- exact-one `[250000000001,250100000000]`：0 candidates；
- exact-one `[270000000001,270100000000]`：0 candidates。

这些单实现结果只标为 **EXACT EXHAUSTIVE FINITE COMPUTATION BY THE STATED IMPLEMENTATION**，不称 independently certified。

arbitrary-odd 模式根据 Fermat 两平方定理等价于直接判断 remainder 是否不是两个平方之和；下节用完全不同的直接平方对枚举对原问题进行了更大范围的双实现交叉检查。

---

## 8. 更强的独立路线：直接枚举原表示

为避免把 factorization 或 obstruction-prime 实现变成单点故障，增加了两套互不共享核心枚举逻辑的程序：

1. `src/search_twosquares_bitset.cpp`
   - x-outer；
   - bitwise integer square root；
   - exact `uint64_t/__uint128_t`；
   - 不使用 floating point 或 factorization。

2. `src/search_twosquares_clean.cpp`
   - y-outer；
   - binary-search integer square root；
   - 独立的 annulus-boundary 更新；
   - exact `uint64_t/__uint128_t`。

### 8.1 为什么这个 finite computation 是 exact

固定区间 \([L,U]\) 和通过严格不等式认证的 \(C,D\)。程序 exact 生成全部 distinct shifts

\[
s=3^c+5^d\le U.
\]

对每个 shift，相关 remainder interval 是

\[
\max(0,L-s)\le r\le U-s.
\]

程序枚举全部且仅全部无序对

\[
0\le a\le b,
\qquad
a^2+b^2=r
\]

并清除对应的

\[
n=s+a^2+b^2.
\]

任意有序非负 pair \((a,b)\) 都对应唯一无序 pair；符号不影响平方。因此清除后留下的 bit 恰好是该区间内没有任何表示的整数。remainder 0 由 \((a,b)=(0,0)\) 明确枚举。

同一 shift 的 duplicate exponent pairs 可以合并，因为对固定 \(n\) 它们给出完全相同的 remainder；程序仍记录 pair count、distinct shift count 和 duplicate count。

两个实现对每个 chunk 的以下字段逐项相同：

- interval；
- \(C,D\)；
- 两个严格 domain inequalities；
- pair / distinct shift / duplicate counts；
- shifts processed before termination；
- unordered square-pair count；
- candidate count 和 candidate list。

独立 Python brute force 在小区间、remainder-zero case、包含 surviving candidate 的 \(n=1\) case 以及多个边界 case 上与两套 C++ 完全一致。

### 8.2 连续正式区间

\[
240000000001\le n\le241600000000.
\]

- integer count：1,600,000,000；
- 160 个无缝、无重叠的 10,000,000-size chunks；
- \(C=23,D=16\)；
- candidate count：0 / 0；
- 两实现匹配的 unordered square pairs：93,835,687,931；
- aggregate SHA256：
  `33fc50fd1323c8d9b8b6f69e22599de9ec392a3d55f8c7c12f4cc5f4cca67319`。

原始 chunk JSON、空 candidate sidecars 和 aggregate：

`output/direct/formal_1p6b_final/`

### 8.3 21 个远端 10M windows

全部由两套实现独立检查，candidate count 均为 0：

```text
[242000000001,242010000000]
[244000000001,244010000000]
[246730000000,246739999999]
[248000000001,248010000000]
[250000000001,250010000000]
[252000000001,252010000000]
[254000000001,254010000000]
[256000000001,256010000000]
[258000000001,258010000000]
[260000000001,260010000000]
[262000000001,262010000000]
[264000000001,264010000000]
[266000000001,266010000000]
[268000000001,268010000000]
[270000000001,270010000000]
[272000000001,272010000000]
[274000000001,274010000000]
[276000000001,276010000000]
[278000000001,278010000000]
[280000000001,280010000000]
[282400000001,282410000000]
```

总计 210,000,000 个整数；aggregate SHA256：

`09c1248d0f736906e78dd001059782d7ce865514d1c5ae025ee0538839775cfa`。

### 8.4 logarithmic windows

| interval | C,D | pair / distinct shift count | candidates |
|---|---:|---:|---:|
| `[1000000000001,1000001000000]` | 25,17 | 466 / 465 | 0 |
| `[10000000000001,10000001000000]` | 27,18 | 531 / 530 | 0 |
| `[100000000000001,100000001000000]` | 29,20 | 627 / 626 | 0 |

总计 3,000,000 个整数；aggregate SHA256：

`40c663199356537a9b84aca02aca544d113c1fffb998ae50149fe9696f4b19ae`。

### 8.5 exponent-activation boundary windows

跨 \(3^{24}+1\)：

\[
[282420000001,282440000000],
\qquad C=24,D=16.
\]

candidate count 0；aggregate SHA256：

`4168065ed62a949c90fe0144c73958f6b12de0ed1768def452b89570e5f45eca`。

跨 \(5^{17}+1\)：

\[
[762930000001,762950000000],
\qquad C=24,D=17.
\]

candidate count 0；aggregate SHA256：

`8f831b92f14f564ee053c75519bbe927661d0c8ef17843d8b17f5ab6c99d1601`。

### 8.6 独立审计

`src/verify_direct_outputs.py` 重新打开每个 raw chunk，检查：

- x/y interval manifests 完全相同；
- 每个 dataset 无 gap、无 overlap；
- `integers_tested = high-low+1`；
- exact \(C,D\) inequalities；
- candidate sidecars 与 JSON 一致；
- 两实现全部数学字段一致；
- 所有声称互不重叠的 datasets 确实 disjoint。

最终输出：

```text
DIRECT_OUTPUT_AUDIT_PASS
continuous_integer_count=1600000000
far_window_integer_count=210000000
logarithmic_window_integer_count=3000000
C_boundary_integer_count=20000000
D_boundary_integer_count=20000000
total_distinct_integer_count=1853000000
matched_unordered_square_pairs=108943945529
```

`src/audit_formal_results.py` 还对 factor-sieve、fixed-pool Method C、SMT/CEGIS 状态和 raw chunk SHA256 做总审计，输出：

```text
FORMAL_RESULTS_AUDIT_PASS
direct_distinct_integer_count=1853000000
direct_candidate_count=0
factor_dual_dataset_count=4
factor_single_dataset_count=3
```

最终日志：

- `logs/final_audit/verify_direct_outputs_packaging.log`
- `logs/final_audit/audit_formal_results_packaging.log`
- `logs/final_audit/run_reproduce_packaging_quick.log`
- 较早的同结果审计仍保留在 `logs/current_validation/` 与 `logs/final_audit/` 中。

---

## 9. failure profile 与 structural observations

这些只属于 **COMPUTATIONAL OBSERVATION**。

固定 ranked-256 exact-one scan 的前几个 first-failure shifts 为：

| shift | first-failure count in 10M interval |
|---:|---:|
| 2 | 3,706,838 |
| 4 | 2,489,717 |
| 6 | 1,593,767 |
| 8 | 899,978 |
| 10 | 565,968 |
| 14 | 318,740 |
| 26 | 147,172 |
| 28 | 111,567 |

这说明有限-pool 模型的实际兼容性瓶颈首先集中在最小 shifts，而不是高 exponent tail。

在连续 1.6B direct search 的 160 个 chunks 中，所有 survivors 都在处理 125 到 188 个 distinct shifts 后清零；平均 149.34，中位数 150。最难的 chunk 是

```text
[240620000001,240630000000]
```

它在第 188 个 shift 后清零。这个现象不能外推为无限范围定理。

下一步最强建议不是继续线性扩大一个有限 prime pool，而是：

- 以最早失败 shifts 为 seed，建立 residue-choice SAT / exact CRT lifting；
- 把 `n mod p` 的 residue choice 与 `n mod p^2` 的 forbidden lifts 分层编码；
- 对任何 SAT residue assignment 用 exact self-consistency loop 重新激活全部 shifts；
- 同时保留 direct two-square chunk search 作为完全不同的 adversarial verifier；
- 若继续 finite-range 推进，优先并行扩展连续区间，并让两套 direct implementations 对每个 chunk逐项交叉。

本轮曾探索 residue-cover/CRT 与宽 prime sieve；它们没有产生通过 theorem verifier 的 candidate，因此只保留为 heuristic/engineering observations，不纳入严格结论。

---

## 10. 运行时间、内存与环境

环境记录：`logs/final_audit/environment.txt`。

```text
Python 3.13.5
g++ 14.2.0
GMP 6.3.0
z3-solver 4.16.0
NumPy 2.5.1
SymPy 1.14.0
Linux x86_64
reported RAM: 4.0 GiB
nproc: 56
```

连续 1.6B aggregate 中，raw chunk elapsed-time sums 为：

```text
x-outer implementation: 1194.32954 s
y-outer implementation:  807.55126 s
```

这是各 chunk elapsed 的总和；部分 chunks 并行运行，因此不能当作单次 wall-clock。最后新增的 90M clean rerun 在 `JOBS=5` 下：

```text
x-outer wall: 11.13 s, orchestrator max RSS 42,704 KiB
y-outer wall: 11.45 s, orchestrator max RSS 39,704 KiB
```

最终 quick clean-build reproduction（跳过 Stage 0，但包含 toy、双 factor、双 direct 和 stored-output audit）：

```text
wall: 29.70 s
max RSS: 183,796 KiB
exit status: 0
```

Stage 0 最终独立复现 exit status 0。完整 formal search 是由多个保留 raw logs 的前台 runs 组成；没有把被 timeout 中断或缺少完整 chunk/exit-status 的尝试计入任何 exact result。最终封装时又做了一次冗余 `ONLY_STAGE0` 尝试；它在 clean verifier 已再次得到 527 / 598 / 135 后被外部中断于旧 bundle 的内部复现脚本，因此不作为新的完成记录。该中断原样记入 `logs/INTERRUPTED_RUNS.txt`，完整 Stage 0 结论仍只依赖先前 exit-status 0 的复现。

---

## 11. 明确未完成与禁止外推

1. 没有找到 certified counterexample；
2. 因而没有 `counterexample.json` 或 `obstructions.csv`；
3. 没有声称任何 n 是最小 counterexample；
4. SMT SAT 从未被直接当作 certificate；
5. SMT UNSAT 无 proof object 未称 certified；
6. timeout 未称 negative result；
7. fixed prime pool 的空结果未外推到所有 primes；
8. exact-one family 的空结果未外推为不存在 counterexample；
9. direct exact finite result只覆盖明确列出的有限 intervals；
10. 没有根据有限空结果声称原猜想正确。

最终数学状态仍是：**UNRESOLVED**。

---

## 12. 文件布局与一键复现

```text
REPORT_zh.md
README.md
baseline/a303656_p2cover_bundle.zip
src/
tests/
cert/
output/
logs/
run_reproduce.sh
requirements.txt
SHA256SUMS.txt
```

重要入口：

- `src/verifier.py`
- `src/verifier_gmp.cpp`
- `src/search_z3_direct.py`
- `src/search_z3_cegis.py`
- `src/search_bitset.cpp`
- `src/search_exhaustive_clean.cpp`
- `src/search_factor_sieve.cpp`
- `src/search_factor_sieve_clean.cpp`
- `src/search_twosquares_bitset.cpp`
- `src/search_twosquares_clean.cpp`
- `src/audit_formal_results.py`
- `src/verify_direct_outputs.py`
- `output/formal_results_audit.json`
- `output/final_packaging_audit.json`
- `output/direct/formal_1p6b_final/summary.json`

默认快速复现：

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
./run_reproduce.sh
```

只重做 Stage 0：

```bash
ONLY_STAGE0=1 ./run_reproduce.sh
```

重做全部保留的 1.6B 连续区间、远端窗口、logarithmic windows、两个 activation-boundary windows，以及相应 factor checks：

```bash
LEVEL=full1p6b JOBS=5 ./run_reproduce.sh
```

`LEVEL=full1p6b` 计算量显著大于默认 quick mode。所有模式都从源码 clean build；不信任归档或 bundle 中的预编译 binaries。
