# A303656 C=1 BLOCKER-DEFICIENT NONREGULAR CORE CLASSIFICATION — ENDGAME PHASE B

## 0. 推荐执行环境

推荐执行环境：

```text
网页端 GPT-5.6 Pro

```

你的角色：

- ALGEBRAIC NUMBER THEORIST
- MULTIPLICATIVE ORDER / WIEFERICH PRIME SPECIALIST
- CAPACITATED HALL / MATCHING THEORIST
- ORDER-SUPPORT DAG SPECIALIST
- ADVERSARIAL PROOF REFEREE
- EXACT FINITE COMPUTATION LABORATORY

本轮是 **endgame-level theorem research**。

不是扩大 prime scan。

优先级：

```text
universal theorem
>
structural classification
>
minimal surviving arithmetic class
>
targeted exact computation
>
bounded evidence

```

不得用“又搜到一些 primes”作为主要成果。

---

# 1. ABSOLUTE GITHUB RULE

严格只读。

不得：

```text
merge
comment
review
push
create branch
create issue
edit repository
modify STATUS.md
modify authority state

```

最终必须写：

```text
GITHUB WRITES PERFORMED:
NONE

```

---

# 2. LIVE AUTHORITY — FAIL CLOSED

Repository：

```text
Samsen879/a303656
Repository ID: 1333945235

```

必须从 live GitHub 自己确认 current：

```text
main SHA
main tree
STATUS.md

```

并确认以下三个 PR 已全部进入 current main：

```text
#14 — C=1 two-root provenance blocker theorem
#15 — C=1 two-anchor synchronization bridge
#16 — arithmetic Kraft–Hall resource obstruction

```

对应 directories 至少必须存在：

```text
analysis/c1_two_root_provenance_phase_a/
analysis/c1_two_anchor_sync_phase_a/
analysis/c1_kraft_hall_phase_a/

```

如果任何一个未 merge：

```text
PRECONDITION FAIL

```

停止正式 Phase B。

项目状态必须保持：

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

```

---

# 3. REQUIRED READING

至少完整阅读：

```text
STATUS.md
docs/THEOREM_INDEX.md
docs/ROUTE_MAP.md

analysis/c1_entangled_coordinate_deficit/
analysis/c1_contraction_tree_phase_a/
analysis/c1_minimal_saturated_coordinate_inverse/

analysis/c1_two_anchor_common_residue_phase_a/
analysis/c1_prefix_frontier_realizability_phase_a/
analysis/c1_hereditary_shell_phase_a/

analysis/c1_two_root_provenance_phase_a/
analysis/c1_two_anchor_sync_phase_a/
analysis/c1_kraft_hall_phase_a/

```

必须从原始 definitions 重建：

```text
w_q
s_q
dynamic row
rigid row
coarse fatal
local zero
U
L
beta_p
actual full fiber
provenance macro
blocker coordinate
original prime resource
paired forbidden digit
Kraft frontier
paired resource

```

---

# 4. STARTING THEOREM — DO NOT REPROVE AS FINAL RESULT

\#14 已给出：

令

```text
Q = {original nonregular rows q : s_q >= 2}.

```

对每个 `q` 的 panel-relative eligible free blocker：

```text
N(q)
=
{ odd prime lambda :
  lambda | w_q
  and
  lambda not in P }.

```

一个 blocker coordinate `lambda` 的 worst-case paired capacity：

```math
c_lambda = floor((lambda-1)/2).
```

若存在 capacitated assignment：

```text
each q -> one lambda in N(q)

```

且每个 `lambda` 接收的 rows 数不超过 `c_lambda`，

则 complete simultaneous certificate impossible。

因此 hypothetical complete certificate 必须违反 capacitated Hall。

也就是说存在非空：

```text
S subseteq Q

```

满足：

```math
|S| > sum_{lambda in N(S)} floor((lambda-1)/2).
```

本轮把这样的 `S` 称为：

```text
BLOCKER-DEFICIENT NONREGULAR CORE

```

---

# 5. PRIMARY OBJECTIVE

研究：

> **blocker-deficient nonregular core 到底被 arithmetic order structure 强迫成什么样？**

最终优先尝试证明：

```text
THEOREM A:
no finite admitted blocker-deficient core exists

```

如果这个过强，则依次降级到：

```text
THEOREM B:
every minimal blocker-deficient core belongs to an explicitly classified
arithmetic family.

THEOREM C:
every minimal blocker-deficient core forces a new contradiction with
multiplicative-order / Wieferich / capacity constraints.

THEOREM D:
all blocker-deficient cores reduce to a strictly smaller explicit
exceptional class E.

```

如果只能得到 D，必须精确定义 `E`。

不接受：

```text
“似乎 rare”
“扫描中没找到”
“可能需要更多 primes”

```

作为主要结论。

---

# 6. MINIMAL DEFICIENT CORE — EXACT STRUCTURE

取 inclusion-minimal deficient `S`。

研究它必须满足哪些 Hall-tight properties。

至少推导：

```text
for every proper T subset S:
|T| <= capacity(N(T))

but

|S| > capacity(N(S)).

```

研究是否因此迫使：

- blocker coordinates 全部接近 capacity saturation；
- 每个 q 的 eligible free factors高度重合；
- 某些 coordinates 必须被大量 rows共同使用；
- 每个 removable row都会恢复 matching；
- 是否存在 canonical deficiency `1` reduction；
- 是否可以通过 Hall dual / min-cut 得到 canonical weighted certificate。

请把问题写成真正的 finite capacitated bipartite matching theorem，而不是文字 intuition。

---

# 7. EXPLOIT THE ORDER DAG

若：

```text
lambda | w_q

```

则：

```text
lambda < q.

```

如果 `lambda in P`，它不是 free blocker，而是系统中的 actual dynamic row prime。

因此 blocker deficiency意味着：

> 很多 `w_q` 的 odd factors 要么已经在 `P` 中，要么 free factors 的 capacity 被其他 nonregular rows挤满。

定义 directed support graph：

```text
q -> lambda
iff
lambda is an odd prime divisor of w_q
and
lambda in P.

```

所有 edges strictly descend：

```text
lambda < q.

```

这是 DAG。

必须研究：

### Question A

minimal blocker deficiency 是否迫使每个 `q` 至少有一个 descending support edge？

### Question B

反复沿：

```text
q -> lambda

```

下降，最终必须终止。

终点 prime row 的 order factors 如何满足 deficiency？

### Question C

能否由 well-founded descent + Hall deficiency 推出 contradiction？

### Question D

如果终点是：

```text
3
5
or prime == 1 mod4

```

这些并不都是 admitted dynamic rows。

这是否自动产生 free blocker？

必须严格处理 `5` 不是 admitted row 的特殊性。

---

# 8. SATURATED FREE COORDINATES

Blocker deficiency不要求：

```text
N(q)=empty

```

也可能是：

```text
free coordinates exist
but their capacities are collectively exhausted.

```

因此必须区分：

```text
TYPE I:
factor-closed q
(all odd factors of w_q are dynamic row primes)

TYPE II:
capacity-deficient q-family
(free factors exist but are Hall-overloaded)

TYPE III:
mixed core

```

尝试证明 minimal core 的 classification。

尤其：

> capacity overload 能否被 arithmetic congruence compatibility进一步削弱？

Worst-case capacity：

```math
floor((lambda-1)/2)
```

来自每 row 最多两个 forbidden digits。

但 actual shared-residue relation 可能使多个 rows 的 forbidden digits碰撞。

如果能证明：

```text
distinct forbidden digits << 2 * row count

```

或反之必须很分散，

可能显著改变 Hall capacity。

研究 exact digit structure，不要仅保留 worst-case bound。

---

# 9. THE BOUNDARY RESOURCE 1645333507

必须独立重算：

```text
q = 1645333507
w_q = 2 * 3^3 * 30469139
s_q = 2

```

并确认：

```text
3
30469139

```

都是 admitted dynamic labels。

这个 row 在 panel 同时包含这两个 primes 时：

```text
N(q)=empty

```

所以 singleton `{q}` 可以成为最简单的 factor-closed blocker-deficient object。

不要停止于此。

研究：

### 9.1

如果 `3` 和 `30469139` 被迫进入 P，它们各自在 global certificate 中引入什么新的 dynamic obligations？

### 9.2

`30469139` 的：

```text
w
s
odd order factors

```

是什么？

是否继续迫使更小 admitted dynamic rows？

### 9.3

沿 order DAG 完整展开这一 boundary resource 的 dependency closure。

目标不是 full-period enumeration，而是 structural dependency analysis。

### 9.4

这个 closure 是否：

- 自动产生 free blocker；
- 自动触发 coordinate-3 Kraft tax；
- 产生 impossible resource multiplicity；
- 或形成一个真正的新 surviving core？

---

# 10. INTERFACE WITH #16 KRAFT–HALL

Blocker-deficient row `q` 仍然是 actual nonregular prime resource。

它可能在：

```text
ell = P+(w_q)

```

处供应 rigid leaf。

而 blocker factors 是：

```text
lambda | w_q

```

二者通常不同。

研究 Hall deficiency是否迫使大量 q：

```text
share same P+(w_q)

```

或集中到少数 coordinates。

如果是，则应用：

```text
actual Kraft capacity
prefix-frontier resource demand
coordinate-3 exclusions
resultant paired-resource restrictions

```

尝试把：

```text
blocker Hall overload

```

转化成：

```text
rigid-resource Kraft overload.

```

如果存在一个 min-max / duality theorem，这是本轮最高价值方向之一。

---

# 11. PRIMAL–DUAL FORMULATION

主动尝试建立一个优化问题。

对每个 nonregular row `q`，可能的“处理方式”：

```text
A. kill q using a free blocker factor;
B. leave q alive as potential rigid resource;
C. kill q later by another coordinate's common greedy choice.

```

把 blocker assignment 写成 primal flow。

寻找 dual weights：

```text
alpha_q
gamma_lambda

```

解释 Hall deficiency。

然后问：

> dual certificate能否与 Kraft demand、order-DAG inequalities、shared-residue constraints组合成 contradiction？

如果可以，给出 exact theorem。

---

# 12. COMPUTATION POLICY

```text
THEOREM FIRST.
COMPUTATION SECOND.

```

不得首先扩大：

```text
q_max

```

不得以 `10^8 / 10^9` prime scan 作为主任务。

允许：

- factor/order exact computation；
- blocker graph construction；
- finite matching / max-flow；
- small exact CSP；
- minimal deficient-core enumeration；
- boundary-resource dependency closure；
- exact modular computations；
- rational/integer Hall duals。

所有计算必须：

```text
exact integer arithmetic
deterministic
reproducible

```

不得 floating-point 判断 congruence、valuation 或 exact capacity。

在运行非平凡 computation 前冻结：

```text
domain
objective
output schema
stop condition

```

---

# 13. ADVERSARIAL COUNTEREXAMPLE SEARCH

不要只证明。

还要尝试构造：

```text
abstract blocker-deficient cores
actual order-compatible blocker-deficient cores
shared-residue-compatible cores

```

如果 universal theorem false，尽量找到 **minimal actual arithmetic survivor**。

必须区分：

```text
abstract graph survivor
order-realizable survivor
actual nonregular-prime survivor
potential complete-certificate survivor

```

不能混淆。

---

# 14. PROMOTION GATES

按顺序判断：

```text
GATE A:
universal blocker-deficient core impossibility proved

GATE B:
all minimal deficient cores structurally classified

GATE C:
boundary family reduced to explicit finite/arithmetic exceptional class

GATE D:
only computational evidence / examples

```

若 A 成立：

这是重大 endgame advance。

若 B/C 成立：

也应完整输出。

若只有 D：

明确：

```text
NO ENDGAME THEOREM OBTAINED

```

---

# 15. REQUIRED FINAL REPORT

最终至少包括：

```text
1. LIVE AUTHORITY
2. FORMAL BLOCKER GRAPH
3. CAPACITATED HALL THEOREM
4. MINIMAL DEFICIENT CORE STRUCTURE
5. ORDER-DAG ANALYSIS
6. BOUNDARY RESOURCE 1645333507
7. PRIMAL-DUAL FORMULATION
8. INTERFACE WITH KRAFT–HALL
9. EXACT COMPUTATION
10. COUNTEREXAMPLES
11. STRONGEST PROVED THEOREM
12. MINIMAL SURVIVING CLASS
13. DOES THIS CLOSE THE BLOCKER-DEFICIENT BRANCH?
14. REMAINING GAP
15. NEXT SINGLE TARGET

```

必须明确：

```text
UNIVERSAL C=1 NO-GO:
PROVED / NOT PROVED

```

只有真的完成完整 logical chain 才能写 `PROVED`。

---

# 16. ARTIFACT PACKAGE

如环境允许，生成一个 self-contained source bundle：

```text
A303656_BLOCKER_DEFICIENT_CORE_PHASE_B.zip

```

至少包含：

```text
REPORT.md
DEFINITIONS.md
THEOREM_AUDIT.md
COMPUTATION_SPEC.md
tools/
tests/
results/
SHA256SUMS.txt

```

standalone scripts 不依赖 repository implementation。

---

# 17. FINAL STATE

最后必须写：

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

```

除非你真的证明 A303656；仅排除 finite certificate formalism 绝不能改变最后一行。

以及：

```text
GITHUB WRITES PERFORMED:
NONE

```