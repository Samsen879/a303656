# A303656 C=1 GENERAL B7 BRANCHING — TARGETED PHASE E

## 0. 结论与证据等级

**本轮得到 C 的精确有限参数版本，以及 D 的实际 regular 算术反例；没有得到 A 或 B。**

新的主结果不是把一条 literal chain 换个名称，而是：用完整 regular dependency-closed state R 及其唯一 maximal-generator antichain A(R)，精确刻画可以在 R 上终止的 root orders，并把同一 state 的全部选择合并成单一 primitive-only critical integer。由此得到按真实 basin 顶点数递归的有限 family，并完整分类四顶点的 fork / serial 两种情况。

四顶点 fork 的 **120 个整数 indices 已全部输出**。四顶点 serial 的完整有限表达式也已证明，但它使用 Task 1 的 48 个分圆值的 regular primitive factors 作参数；这些因子集合没有全部分解、认证和数值展开。不得把“完整有限公式”写成“完整数字清单已经算完”。

另外认证了实际 regular diamond `6717031 -> {43,127} -> 7`，以及实际 transitive-edge 例子 `42743 -> {7,43}`。它们否定适用于所有 compatible regular basins 的 naïve tree / branch-deletion / fixed-eight-multiplier 引理，**不冒充 actual nonregular B7 反例**。

完整证明见 `THEOREMS.md` E1–E8；此处为中文研究报告。所有新定理均为本轮提出并自审的证明，不表示独立作者审阅、形式化证明或 repository promotion。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
main tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
PR26: MERGED — 07a6f5fb2059b1dfc6be7cc6d1325cd65b49ae41
PR27: MERGED — a8e72c805c6a36d3e215507a4fcaad271147ce7e
PR28: MERGED — 8dcb744641a46b41597681b4eaddfd7b427d7280
PR29: MERGED — fd59aad038a09f2fc6df7039111408fa231c27dd
End-of-research live main recheck: UNCHANGED
PRECONDITION: PASS
```

通过 GitHub connector 的 live branch、各 PR 的 merged 字段、连续 base/merge chain 及固定 SHA 文件核对；没有用历史包中的研究 SHA 冒充 current main。STATUS 保留 PAUSED / NONE / UNRESOLVED。[S1]

实际完整阅读了五个指定目录的核心数学报告，以及相关 DEFINITIONS、THEOREMS、THEOREM_AUDIT、B7 PROOF_AUDIT；逐文件清单见 `SOURCE_BINDING.json`。**没有逐一读完五个目录中的全部生成数据、辅助源码、历史记录和 integration 文件，因此不声称目录级“所有文件全读”。** 没有完整本地 checkout，没有重跑 repository-native tests/CI 或 2e9 inventory。下面的计算是本轮 standalone reference。

推荐执行环境：网页端数学研究与 reference laboratory。本轮未分派 Codex、未启动大型生产计算。

## 2. B7 BASIN DEFINITIONS

全篇固定边方向为：**较大 admitted prime -> 它的 exact order 的 odd prime factor**。

令

    w_p=ord_p(5), s_p=v_p(5^w_p-1),
    O(p)={odd primes dividing w_p}, H(p)=O(p)\{3}.

Regular 是 s=1；nonregular 是 s>=2。Absolute DAG 展开全部 admitted labels >3，包括 panel 原本未列出的算术标签；到 3 或 1 mod4 prime 停止。T(q) 为终端集合；D(q) 含 q 和全部 admitted descendants >3，不含 terminal 3。Gamma(q)={v in D(q):O(v)={3}}。[S2,S8]

B7 要求：q 是 admitted nonregular；T(q)={3}；proper descendants 全 regular；Gamma(q)={7}；D(q) 中每个 exact order 都 squarefree。最后一条限制的是 w_p，不是 p-1。它不禁止 43->3 这样的额外 direct edge。[S2,S3]

完整证书另需 actual active helpers、固定中心、全局共享状态及跨 root 的 basin disjointness；不能由一个 intrinsic B7 整数自动声称已有完整证书。[S2,S4]

## 3. MINIMAL B7 BASIN

**E1：固定 q 后，inclusion-minimality 是自动的。**

任何包含 q、且包含每个已保留顶点全部 admitted order factors 的集合，沿路径归纳都必须包含 D(q)。因此 D(q) 本身就是唯一最小 support-closed 集。删除任意 proper vertex 后，在从 q 出发的一条路径上取第一个被删顶点，其上一个保留顶点立刻缺少 required support。

这个性质适用于树，也适用于 diamond；它不能强制一个 regular vertex 只有一个用途。若某 direct edge 对 reachability 冗余，也不能相应删掉 exact order 中的因子。

尤其：B7 的每个 proper descendant 都 regular，所以不能从同一 basin 内截取一个更小的 nonregular B7 root。真正的 arithmetic compression 必须在 basin 外找到另一个 actual nonregular prime，并证明它的 square hit 和 closure。

## 4. FIRST-RELAY IMPORT

直接使用 Phase D 的已证 base case：

    A7={43,127,379,7603,19531,519499},
    min(D(q)\{7}) in A7,
    |D(q)|>=3.

六个 relays 全 regular；最小层 orders 为 7,14,21,42。[S2]

本轮只对该层四个完整分圆乘积做 replay，不把它们再列作新的主要定理。

## 5. BRANCHING STRUCTURE：正确的 critical structure

定义 good regular state R：有限 actual regular admitted primes，包含 7，orders squarefree，H(v) subset R；v!=7 时 H(v) 非空。下降性迫使所有节点最后都到 7。

关键不是选一条路径，而是定义

    A(R)=R \ union_(v in R) H(v).

A(R) 是没有 R 内上游顶点的 maximal-generator antichain。对任意 S subset R，E2 给出

    union_(p in S) D(p)=R  <=>  A(R) subset S.

证明：极大顶点不能从其他顶点到达，因此必须直接列入 S；反过来，每个顶点沿 incoming edges 向较大标签追溯，最终到达某个极大顶点。

**E3：完整 terminal family 为**

    J(R)={delta*product(S): delta in {1,2,3,6}, A(R) subset S subset R},
    |J(R)|=4*2^(|R|-|A(R)|).

设 SqPrim(n)={q prime=3 mod4:q does not divide n, q^2|Phi_n(5)}，则有准确等式

    {q in B7:D(q)\{q}=R}=union_(n in J(R)) SqPrim(n).

这是必要充分的 square-hit gate，不是只覆盖部分 chains 的 sufficient construction。

前向：squarefree root order 恰为 delta*product(H(q))；生成全部 R 强制包含 A(R)。反向：primitive square divisor 的 exact order 是 n，且 q>n>=max R；其全部 proper closure 就是 R，故满足完整 intrinsic B7 定义。

另有 **E3.1：每个固定 R 可进一步合并为单一 primitive-only critical integer**。令

    a_R=product A(R), b_R=6*product(R\A(R)), p=max R,
    W_R=Phi_(a_R)(5^b_R)=product_(n in J(R)) Phi_n(5),
    Z_R=W_R/p  if |A(R)|=1; otherwise Z_R=W_R.

则 Z_R 是整数，所有 prime factors 都大于 max R，并且

    {q in B7:D(q)\{q}=R}={q prime=3 mod4:q^2|Z_R}.

剔除因子的依据不是假设各分圆值互素：若小素数 l<=max R 整除某 Phi_n(5)，squarefree index 条件迫使 n=l*ord_l(5)。因 n 含 max R，只能 l=max R；多极大顶点时这又与其他极大顶点不被它依赖相矛盾。单极大顶点时，仅 n=p*w_p 产生一个 valuation-one 的 imprimitive p。因此恰好除掉上述一个 p，其他 prime divisors 都是真正 terminal candidates。

三组精确核对的例子是

    Z_{7}=Phi_7(5^6)/7,
    Z_{7,43}=Phi_43(5^42)/43,
    Z_{7,43,127}=Phi_5461(5^42).

这里合并的是同一固定 state 的有限 order family，不是将 q 的 base-5 order 降成 a_R；也没有宣称 Z_R 已完全分解或没有 admitted square factors。

正确 basin cost 是

    c(n)=1+|union_(p|n,p>3) D(p)|,

不是 1+sum|D(p)|。Shared relay 必须只计算一次。

## 6. CRITICAL SPINE ATTEMPT

最大 admitted order-factor 的下降链可以确定性选出，但反向一步 `w_child=parent*m` 的 m 记录其他分支；它不是可以忽略的附加标签。

固定 numerical predecessor p 确有很大的有限 overfamily

    m divides 6*product_(7<=r<p,r prime=3 mod4) r.

这只是随 p 增大的局部有限集合，不是统一 multiplier alphabet，也不限制总深度。固定八个 multipliers 的 regular-basin 引理则被下一节的实际 diamond 否定。

因此本轮将 spine 替换成 `(closed state, maximal generators, closure-union cost)`；没有证明 uniformly bounded branching 或 uniformly bounded spine depth。

## 7. COUNTEREXAMPLES

### 7.1 Actual regular diamond

认证的实际 prime 为 t=6717031：

    w_t=5461=43*127,
    5^127 mod t=6238090,
    5^43 mod t=3428912,
    5^5461 mod t^2=5828690216189=1+867748*t.

所以 s_t=1。素性同时通过至 sqrt(t) 的完整 trial division，以及 base 3 的 complete-(t-1) Lucas certificate；t-1=2*3*5*41*43*127。记录在 `results.json` 和 `ACTUAL_REGULAR_CERTIFICATES.json`。

真实边是 t->43、t->127、43->7、127->7，另有 43/127/7 到 3 的真实边。两条 incomparable branches 都是 exact order 所必需。其 admitted closure 不是树。

从 43 到 t 的反向步需要 multiplier 127；从 127 到 t 需要 multiplier 43。二者都不在 {1,2,3,6,7,14,21,42}。最大-factor spine 经 127，不经过整个 basin 的最小 proper relay 43。

**边界：这是 actual regular partial basin，不是 B7 member；没有认证一个 nonregular root 在它上方。** 因而它否定 general regular-basin 局部引理，却不是“actual B7 都有某条好 spine”这一更窄断言的实际反例。

### 7.2 Actual transitive-edge example

u=42743 是 actual regular prime，w_u=602=2*7*43，s_u=1。它同时直接依赖 7 和 43，而 43 又依赖 7。

删掉 u->7 不改变 reachability，但把 order 压成 86 是错的：程序精确核对 `42743 does not divide Phi_86(5)`。Graph transitive reduction 不等于 arithmetic order compression。

### 7.3 Formal nonregular root

在 actual regular state {7,43,127} 上画一个 formal nonregular Q，order label 5461，得到四顶点、inclusion-minimal 的 support fork。缺少的恰是实际 prime Q 与 Q^2|Phi_5461(5)。它只是 coloured/order-structural 模型，不是 arithmetic counterexample，不决定真实 minimal B7 的大小。

## 8. EXPLICIT FAMILY / RECURSION

### 8.1 Canonical size recursion

令 F1={{7}}。从 R in F_k 出发，对非空 S subset R、delta in {1,2,3,6}，令 n=delta*product(S)。将每个大于 max R 的 admitted regular primitive factor p of Phi_n(5) 加入，得到 R union {p} in F_(k+1)。相同 states 去重。

E4 证明：F_k **恰好**是 k 顶点 good regular states；每层有限、有效可生成。证明方法是按 prime 大小排序，所有 dependencies 都落在此前 prefix，因此每个 actual state 有确定的 numerical insertion history。

注意 intermediate transition 不要求 S 包含旧 A(R)，否则会错误删除 forks。更新公式是

    A(R union {p})=(A(R)\S) union {p}.

对任何固定 M，

    C_(<=M)=union_(1<=k<=M-1) union_(R in F_k) J(R)

有限，并且精确刻画全部 basin-size<=M 的 B7 square hits。这里“可计算”是严格有限 factorization 意义，不是承诺计算便宜，更不是声称已生成所有层。

### 8.2 完整四顶点 fork / serial 分类

设 D(q)={7,r,s,q}，7<r<s<q。r in A7。若 r 不整除 w_s，s 必为 A7 的另一 first relay；否则 w_s in I(r)。没有第三种情况。

**Fork：**

    C4_fork={k*r*s:r<s in A7,k in K},
    K={1,2,3,6,7,14,21,42}.

15 个 unordered pairs，每对 8 个 indices，共 120 个，全部输出，无重复。{43,127} 对应

    5461,10922,16383,32766,38227,76454,114681,229362.

**Serial：**

    S_r=union_(k in K) RegPrim(k*r),
    RegPrim(n)={s prime=3 mod4:s does not divide n,
               s|Phi_n(5),s^2 does not divide Phi_n(5)}.

每个 s in S_r 有 D(s)={7,r,s}，因此

    C4_serial=union_(r in A7,s in S_r)
              {delta*7^e*r^f*s:delta in {1,2,3,6},e,f in {0,1}}.

每个 (r,s) 恰好 16 个 indices，且与 fork family 不交：

    |C4|=120+16*sum_(r in A7)|S_r|.

这对全部 actual primes 无 cutoff。**120 fork 清单已展开；六个 S_r 未全部展开。** 已独立认证的 S43 示例包括 9547,42743,18471511,558801427,7866608083，不能将它们冒充完整 S43。

### 8.3 与 Phase D 的区别

Phase D 已有按 height 聚合的 R_j 与第二层 508-index overfamily。本轮不将它们重命名为新成果。新增的是 exact-size closed states、mandatory maximal antichain、shared-relay union cost、终端必要充分 gate，以及完整四顶点 fork/serial 分解。

## 9. CYCLOTOMIC COMPOSITION

当 prime l 不整除 m，

    Phi_(m*l)(5)=Phi_m(5^l)/Phi_m(5).

若 q 的 exact order 是 m*l，则 q 不整除 denominator；square hit 落在 base 5^l 的 numerator，不自动变成 base 5 的较小-index square hit。对任意 proper divisor d of ord_q(5)，q 不整除 5^d-1。

因此需要的是一个“产生另一个 actual nonregular prime”的算术定理，而不是 polynomial factorization identity 本身。[S2,S11]

## 10. INTERFACE WITH PROVIDER CHARGING

Provider confinement 只把 helpers 限制到具体 root basins；其有限 bound 依赖真实 root labels，不能变成仅依赖 N 的常数。[S6,S7]

Exactly-seven 的 disjointness 是不同 roots 的 basins 两两不交，不是单一 basin 内不同 branches 不可共享。一个 basin 的所有非平凡 fixed 3-shadows 可完全重合，所以 kappa=1 与很多 regular vertices/branches 并不冲突。7 个 obligations=7 capacity，仍没有 deficit。[S4,S6]

本轮 actual regular fork mask 使用 R={7,43,127}，K=2,E={1}，a=152908，residues 为 33 mod49、1428 mod1849、11159 mod16129。在 full L=229362 的 d=4 mod6 branch 中，38227 个 exponents 有 38226 个被覆盖，只剩 a 一个 hole。114681 次 direct row / shell comparisons 全一致。

这是 source arbitrary-branching filling 的实际 regular 部分验证，没有添加不存在的 q。此 partial system 的 U=42，**不是 U=L**。只有满足相应 order support 的实际 nonregular root 被添加后，才能使用完整 filling theorem 的结论。

## 11. MINIMAL-MEMBER THREE-VERTEX?

```text
NO — NOT PROVED.
NOT CLAIMED FALSE FOR ACTUAL B7 MEMBERS.
```

对于固定 q，minimality 不能删 support；proper descendants 又全 regular。实际 regular diamond 只说明图论局部引理不足，没有提供 actual B7 counterexample。

## 12. FINITE CRITICAL ORDER FAMILY?

```text
GLOBAL UNIFORM FINITE FAMILY: NO — NOT PROVED.
FIXED BASIN SIZE <= M: YES — EXACT FINITE RECURSION.
M=4: YES — COMPLETE FINITE FACTOR-PARAMETRIZED CLASSIFICATION.
M=4 FORK: YES — ALL 120 NUMERIC INDICES MATERIALIZED.
M=4 SERIAL: COMPLETE FORMULA, NOT A COMPLETE MATERIALIZED FACTOR INVENTORY.
```

还有一个反直觉但严格的 E8：**若 B7 为空，则 good regular states 反而必有任意大 cardinality。** 对任意 R 取 p=max R，Phi_p(5)=3 mod4 且 =1 modp，必有更大的 admitted exact-order-p prime z；若 z nonregular 就是 B7，故在 emptiness 假设下只能 regular，可以继续扩张。

因此不能等待 regular closure 递归在有限层自动耗尽，然后宣称 B7 为空。这个结论不排除其他形式的 global finite-critical-family 定理，只排除这种 finite-fixed-point 想法。

## 13. INTERFACE WITH TASK-1 THREE-VERTEX CLOSURE

Task 1 处理原 48 个 indices 的 SqPrim。即使所有这些 sets 都为空，regular sets RegPrim 仍然可能非空；本包已给多个实际例子。它们继续生成 serial 四顶点及更大 basins。

因此 Task 1 成功后可严格推出 `B7 member => |D(q)|>=4`，而不能单独推出 B7 empty。四顶点下一层分成 fork120 和上述 serial family。新的 family 是一个可审阅的算术接口，不是已经关闭的 square-hit ledger。

## 14. COMPUTATION / INDEPENDENCE

`reference.py` 只使用 Python standard library，不 import repository 实现，不联网。素性用完整 trial division；diamond 另有 full-(p-1) Lucas 方法。模幂和逐次乘法两种组织方式核对小指数；support invariant 用 direct reachability 和 antichain 条件比较。

| 工作 | 已执行范围 |
|---|---:|
| 实际 regular prime/order/lifting certificates | 13 |
| First-relay 完整乘积 replay | 4 |
| 完整数值 fork family | 120 indices |
| Fixed-state critical-integer identities / exact imprimitive cleanup | 3 states |
| 抽象 DAG root-support comparisons，formal 总顶点数 2–7 | 625300 |
| 同域 accepted support DAG counts | 1,2,10,122,3346,196082 |
| Actual fork direct row comparisons | 114681 |
| 负向 regression tests | 14 |

DAG 数不是 arithmetic prime inventory。没有实际 B7 member，没有一个新 fork index 被宣称全部 squarefree。第二种验证组织不等于 independent author 或 fully independent software stack。

Discovery 阶段只在 theorem-selected n=5461、10922 上测试 q=1+k*n，1<=k<=40000 且 q=3 mod4 的 divisibility，共 30000 次 modular tests，找到 t=6717031。该记录单列 `DISCOVERY_ONLY.json`；其 absence 不作排除证据，正式 replay 不运行这个 probe。没有 blind q scan，没有扩展 nonregular prime inventory。

## 15. DOES GENERAL B7 REDUCE TO FINITE ARITHMETIC?

```text
NO — NOT TO ONE GLOBAL FINITE FAMILY.
YES — FOR EVERY PRESPECIFIED FINITE BASIN-SIZE CAP.
```

无界 general B7 只得到精确的逐层有限递归 family；不能将它说成一个已知有限终止的 emptiness algorithm。

## 16. DOES THIS ENABLE B7 EMPTY?

```text
NO.
B7 EMPTY: NOT PROVED.
ACTUAL B7 MEMBER: NOT FOUND.
N>=8: NOT PROVED.
```

## 17. NEXT SINGLE TARGET

**Square-hit-preserving basin-cost descent (SQD)。**

证明或证伪以下完整算术断言：对 good state R、|R|>=3、n in J(R)，若 SqPrim(n) 非空，则存在 good R'、|R'|<|R|、n' in J(R')，使 SqPrim(n') 非空。

它要求产生真正的新 nonregular prime，而不是缩短原 DAG。若证明 SQD，则取 basin-size 最小的 B7 member，立即归约到三顶点；随后 Task 1 的完整 48-case closure 才能严格推出 B7 empty。当前没有证明 SQD，regular 反例也不直接否定它的 nonregular hypothesis。

这是本轮精确定位的缺失桥梁，不授权未经进一步 gate 的大规模 factorization。

## 18. FINAL STATUS

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
