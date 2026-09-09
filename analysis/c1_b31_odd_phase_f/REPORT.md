# A303656 C=1 — B31^odd arithmetic classification, Phase F

## 0. 结论与证据边界

本轮取得：

1. 从已合并 Phase C/D 基础独立重建 exactly-seven 的 O31 必要条件，并给出相应的固定状态判据与全局 CRT 充分构造。
2. 无 cutoff 的完整 first-relay 定理：
   \[
   A_{31}^{\rm odd}=\{878851,625552508473588471\}.
   \]
   两者均经素性证书与精确 lifting 认证为 regular。
3. 两顶点 basin 全部排除；三顶点 basin 精确归约到八个 cyclotomic square-hit indices，但这八个整数的平方因子问题没有全部关闭。
4. 对任意有限 good regular state 给出 maximal-generator antichain、精确 terminal-order family 及 primitive-part critical integer 的 iff 定理。一般类因此具有穷尽的有限分支递归表示，但没有得到全局有限状态界。
5. 认证七个 actual regular closed states，其中三个新增较深状态；没有找到 actual nonregular B31^odd member。
6. 条件性 original odd-row 总数界由 Phase D 的 16 提升为 17；这不是 nonregular-root 下界八。

成功等级：**E + 一般类的精确递归 closed-state reduction**。不是 A；不是 B 所要求的一个全局有限 critical family；不是 C；不是 D。

所有新无限域证明均为本会话提出的、可审阅的数学推导，不是独立作者审稿或 proof-assistant formalization。附带程序只验证明确列出的有限证据。

---

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
main tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
Head: Merge PR #29, Phase D seven-head chain realizability
```

通过 GitHub connector 只读读取 live main、固定 SHA 的 STATUS.md、analysis inventory、branches 与最近 PR 信息。PR #26–#29 已合并；本轮查询的 main 与分支列表没有 Phase E 集成。

**重要来源缺口：当前实际附件只有项目简介与分工规则。题面列出的三个 Phase E ZIP 均没有作为本轮可读文件提供，也没有从 live GitHub 找到。** 因而：

- 没有完成“完整阅读 Seven-Basin Phase E ZIP”的要求。
- 没有认证 Phase E ZIP 的 manifest、hash、定理编号或正式 O31 原文。
- 下文 O31 是依据已合并 Phase C/D 的独立重建，不冒称“已核对 Phase E 原文”，也不是已合并的 Phase F repository theorem。
- 没有通过记忆或题面猜测补写一个不存在的 source receipt。

实际关键来源：

- `STATUS.md`；
- `analysis/c1_order_dag_phase_c/THEOREMS.md`，重点 §§1–7、9、12；
- `analysis/c1_order_dag_phase_c/REPORT.md`；
- `analysis/c1_b7_pure3_phase_d/REPORT.md`，重点 §§2–10；
- `analysis/c1_private_provider_charging_phase_d/REPORT.md`，重点 center ancestry、support confinement 与 exactly-seven audit。

没有完整本地 checkout，没有重跑 repository-native tests、CI 或 2e9 inventory。附带验证器是本轮新写的独立代码路径，但数学推导、证书生成与验证器来自同一会话，不能称为独立作者复审。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

## 2. PHASE E O31 RECONSTRUCTION

### 2.1 从已合并基础重建 pure-3 (2,2,3) 正常形

继承源 formal class：distinct original row primes，固定 shared residue，K>=2，accepted positive odd valuations；local zero 不接受。选择源 boundary anchor c_*，再选择使 row3 dynamic inactive 的 exponent parity b。完整证书在同一个 (c_*,b) 上必须 odd-complete。

使用源中已经证明的 exact sparse-elimination lemma：少于 p 个 proper p-cylinders 与一个 regular dynamic bundle 满纤维覆盖，当且仅当通过接受 valuation 1 的 centered depth-one simple pair。每个 original rigid seed 至多有一个 linear child；lower order factors 的交不能凭空删除尚未消去的 prime，也不能降低其指数。

这里给出 normal-form 核心推导，而不是以有限 scan 替代无限域证明。

**首 nonlinear rank。** 七个原始 nonregular origins 只能在 p<=7 发生第一次 essential nonlinear step，因此候选为 3、5、7。

**排除 p=5。** 设 top seeds n、lower seeds k，n+k<=7，n>=5。此规模的 full 5-frontier 只能由五个不同 depth-one branches 构成。n=5,6,7 时 minimal alternatives 至多 1,2,4；加上 k 后 exact residual 至多有 3,3,4 个 proper ternary cylinders。

固定 A3 为实际 helpers 7、31 的 first 3-guards，并令 A5 为 11、71 的 first 5-guards。一个 linearly descended seed 若只剩 3-depth<=1 与 5-depth=1，其最小 helper 的 odd order 只能是 3、5、15。完整分解

\[
\Phi_{15}(5)=181\cdot1741,\qquad\Phi_{30}(5)=61\cdot7621
\]

没有 admitted mixed head。因此这种 seed 位于 `(A3 x X5) union (X3 x A5)`。

四个以内 proper ternary cylinders 要 full-cover，必须有每个 first branch 的 depth-one cylinder。取 A3 外的 first branch B。保留的 lower seed 不能提供 B。若某个 5-contraction macro 提供 B，则其五个 constituents 的 3-guards 都必须 unrestricted 或 B，cross-strip 迫使其 5-guards 全落在 A5 的两个 branches，不能覆盖五个 branches。矛盾。

**排除 p=7。** essential witness 必须使用全部七个 origins。所有 nonlinear alternatives 的 lower guard 都是全部七个 lower guards 的交 G，或 G 与 dynamic7 guard 的交。没有 simple pair 时至多一个 proper residual clause。它不能为常量：pure order 7/14 的唯一 admitted gateway 是 regular 19531，不能提供七个不同 first 7-branches。

若有 simple pair，essential nonlinear witness 必须在 dynamic7 inactive 时发生，七个 rigid cylinders 自己构成七个不同 first branches，centered branch 唯一。全部 residual 被 simple-pair clause 与 G 两个 proper lower cylinders 包含；每个测度至多 1/3，且没有可填补的 lower dynamic3/5。仍不完整。

**p=3 与 profile。** depth-one admitted heads 只有 7、31；depth-two 只有 19、5167。浅层质量至多 2/3+2/9=8/9，所以需要 depth>=3。一个含 depth-d leaf 的 full ternary prefix tree 至少有 1+2d 个 leaves；七个 leaves 迫使 d<=3。结合每个前两层至多两个 distinct heads，完整 profile 唯一为

\[
(2,2,3),\qquad 2/3+2/9+3/27=1.
\]

depth-three 的三个 distinct heads 从 `{163,271,487,4159,31051,16018507}` 选出。二十种 head triples 并不是全部 arithmetic DAG 的二十种分类。

**整个 arithmetic closure。** 每个 surviving origin 的未消去 support 必须通过实际 centered regular helper，故全部 proper admitted descendants 均实际存在。七个 nonregular rows 已是 rigid origins，不能同时作为这里的 dynamic helpers。每个被消去的 p>3 必为 depth one；retained 3-depth 不下降，所以某 depth-d leaf 对应 basin 的每个 x 都满足 v3(w_x)<=d、vp(w_x)<=1 (odd p>3)。free terminal 不可消去，故 T(q)={3}。

若两个 basins 共享 admitted descendant，则进一步下降共享一个 basal 3-gateway。其固定 3-cylinder 必须包含两个不交 frontier leaves；浅层完整 gateway inventory 与这些 leaves 的深度、互不包含关系排除此事。因此 basins 在 terminal3 之外两两不交。

row3 必须在相反 parity 有非空 dynamic event：否则同一个论证可在两种 parity 重复，二者都会要求 order6 的实际 row7 active，而 row7 的固定 guard 只能有一个 parity。

### 2.2 Selected-parity basin compatibility

对 regular helper p，在给定 anchor 上，若 r_p-3^{c_*} 属于模 p 的 5-generated subgroup，则它在模 p^K 的唯一 logarithm 可写为 a_p modulo w_p p^{K-1}。当 d=a_p modulo w_p 时，非零局部值满足

\[
v_p(r_p-3^{c_*}-5^d)=1+v_p(d-a_p).
\]

因此 incoming depth-one p-cylinder 必须是 `d=a_p mod p`，且该 helper 必须接受 valuation 1。每次 contraction 还必须继承 `d=a_p mod w_p`。共享的 lower prime coordinates、3-primary guards 与 parity 必须由同一个 exponent CRT 解同时满足，不能为每个 fiber 重新选择 a_p。

在一个已经成功 surviving 的 basin 中，这些 congruences 相容，其最后投影正是对应的固定 ternary leaf。较深 p-adic center digits 不能凭空替代一个不兼容的 first center digit。

### 2.3 Parity-switch lemma：all-odd 是整个 basin 的条件

固定所有实际 residues、K、E 与 ambient U，在 c_* 上把 b 换成 1-b。

对于在 b active 的 original event：

- w_x odd 时，其 entire event 在所有 odd coordinates 上保持不变；
- w_x even 时，其固定 logarithm guard 只允许 b，故在 1-b 失活。

这适用于 regular dynamic helpers，也适用于供给原 rigid seed 的 nonregular root；换 parity 不会把同一 root 的 rigid local type 重新选择为另一种 dynamic state。

在 exactly-seven 的 disjoint basins 中，任何 p>3 只有自己 basin 的一个 origin 可以提供相关 seed。盆地外 dynamic rows 不能无来源地救援：进入任何 full-cover witness 的 dynamic row，其 omitted center 必由更大的实际 order provider 填补；逆向追溯严格增大的 prime labels，最终到原 rigid origin。因此其 support 位于该 origin 的 absolute order closure。

所以在 p>3 的 exact elimination 中，没有跨盆地的第二个 origin 可以跳过一个 inactive 必需 helper。结论为：

> 一个 basin 在 opposite parity 的最终 ternary leaf 与 selected parity 完全相同，当且仅当其 D(q) 中全部 w_x 都为 odd；否则这个 origin 没有 surviving leaf。

这里没有把“q 的 order odd”偷换成“全部 proper relays 的 orders odd”。

### 2.4 Opposite-parity obstruction 与 O31 necessity

记 selected frontier 的 first-level branches 为 L31、L7、C。C 内的两片 depth-two leaves 为 L19、L5167；另一个 depth-two branch 再分成三片 depth-three leaves。

w7=6 与 w5167=18 均为 even，因此 opposite parity 必定丢失整个 L7 与整个 L5167。不只是原 row7/5167 单独失活：其所属 basin 的唯一 origin 也不能在最终 3-residual 提供该 leaf。

令 a3 为 opposite-parity dynamic row3 的固定 3-adic center。regular row3 满足 valuation `1+v3(d-a3)`，只能接受 positive odd valuations，并遗漏 center。

- 为覆盖整个失去的 first branch L7，a3 的 first digit 不得落在 L7，且必须接受 valuation 1。
- a3 的 first digit 也不能落在 C。若其 second digit 不在 L5167，L5167 上的 valuation 全为 2，不能接受；若其 second digit 落在 L5167，该 leaf 含遗漏的 center，仍不能由 row3 单独 full-cover。
- 因而 a3 的 first digit 必落在 L31。其他 basins 的 leaves 都在 L31 外；row3 自己遗漏 center，所以 L31-basin 必须在 opposite parity 保留。

由 parity-switch lemma，得到独立重建的 O31：

\[
\boxed{\forall x\in D(q_{31}),\quad \operatorname{ord}_x(5)\text{ is odd}.}
\]

更精确的 **fixed-state opposite-parity criterion** 是：在已满足 selected-parity 正常形及其真实 linear compatibility 的同一个 ledger 上，opposite parity complete 当且仅当

1. O31 成立；
2. row3 在该 parity dynamic，接受 valuation 1；
3. row3 的 center first digit 与 L31 相同。

必要性已证。充分性：row3 的 valuation-one shell 覆盖 L31 外的两个 first branches；保留的 all-odd 31-basin 覆盖整个 L31，包括 row3 center。其他 basins 在 opposite parity 是否存活，不再必需。

此证明没有假定 row3 只有 shell0。它明确处理了 center 与不被接受的 valuation2，避免以粗略“row3 质量 2/3”代替 exact coverage。

### 2.5 O31 sufficiency / complete-state construction

O31 单独不是“有一个完整 certificate”。需要七个 actual nonregular roots 及其 pairwise-disjoint proper regular basins、纯 terminal3 与对应 depths `1,1,2,2,3,3,3`；每个 basin 的所有 orders 在 3 以上 squarefree，3-depth 不超过对应 leaf depth，并存在对应 actual head。31-basin 额外满足 O31。

在这些 **actual arithmetic prerequisites** 下，可以构造同一个 complete state，而不要求其余六个 basins 是 literal prime-order chains。

选择 c=1 与 selected parity even。按

\[
L_{31}:0\bmod3,\quad L_7:1\bmod3,\quad
L_{19}:2\bmod9,\quad L_{5167}:5\bmod9,
\]

以及 `8,17,26 mod27` 指定其余三片。对于 leaf `alpha mod 3^d` 的 basin，令 R=D(q)\{q}。CRT 选择

\[
a\equiv\alpha\pmod{3^d},\qquad a\equiv0\pmod p\ (p\in R),
\]

并对需要的 even order 同时选 a even。取所有 odd rows 的 K=2、E={1}，设

\[
r_p=3+5^a\pmod{p^2}\ (p\in R),\qquad
r_q=3+5^a+q\pmod{q^2}.
\]

对目标 leaf 中任意 d，若某个 p∈R 的 own coordinate 不等于 a，取数值最小者。w_p 的全部 odd factors >3 是更小的 basin vertices，故均匹配；3-primary guard 与所需 parity 也匹配。因此 w_p|(d-a)、p∤(d-a)，p-row 的 valuation 恰为1。

若所有 R-own coordinates 均匹配，w_q|(d-a)。因 s_q>=2，ord_{q^2}(5)=w_q，q-row 的局部值是 q modq²，valuation 恰为1。

所以每个 basin 填满 selected leaf。对 all-odd 31-basin，证明完全不需要 parity，故它在两种 parity 都填满 `d=0 mod3`。

取 row3 的 K=2、E={1}、r3=2 mod9，在 c=1 时恰覆盖 odd d 且 d!=0 mod3。取 two-adic row K2=2、r2=1 mod4，则 c=0 对所有 d 的局部值为3 mod4，直接拒绝该 anchor。c=1 的两种 parity 已由上述 odd rows 完整覆盖。

所有 actual row residues 最后通过 pairwise-coprime prime-power CRT 合成一个 global residue。每个 proper relay 的 own prime 都出现在某个上游 order，故 induced U 包含全部所需 own digits；row3 的 digit 由 heads 提供。没有接受 local zero，也没有发明额外原始 primes。

**结论边界：**这是条件性充分构造；没有实例化七个 nonregular roots。缺失的 Phase E ZIP 仍待原文比对，本节不替它伪造 source authority。

## 3. PRECISE B31^odd DEFINITION

对 admitted prime x>3，即 x≡3 mod4，定义

\[
w_x=\operatorname{ord}_x(5),\qquad s_x=v_x(5^{w_x}-1),\qquad
O(x)=\{p:\ p\text{ odd prime},\ p\mid w_x\}.
\]

Absolute order DAG 沿全部 odd order factors 下降，停止于 3 或 1 mod4 的 primes。D(q) 是 q 与全部 admitted descendants >3；T(q) 是 absolute terminal set。定义 basal gateway

\[
\Gamma(q)=\{x\in D(q):O(x)=\{3\}\}.
\]

本轮 intrinsic class 定义为

\[
\mathcal B_{31}^{\rm odd}=\{q:\ q\text{ prime},\ q\equiv3(4),\ s_q\ge2;
\ T(q)=\{3\};\ s_x=1\ (x\in D(q)\setminus\{q\});
\ \Gamma(q)=\{31\};\ w_x\text{ odd and squarefree}\ (x\in D(q))\}.
\]

**terminal3 不属于 D(q)。** ord_3(5)=2；若把 terminal3 也纳入 all-odd quantifier，会产生一个错误的“空类证明”。O31 的 whole-basin quantifier 包括 root 与所有 admitted relays >3，不包括停止展开的 terminal3。

在这里，Gamma={31} 实际可以由其余条件推出：finite descending pure3 closure 必有 basal gateway，odd squarefree basal order只能为3，而 Phi3(5)=31。保留 Gamma 条件是为了对齐 source 的 basin terminology。

条件来源分层：

- pure3 terminal、proper regularity、depth-one basin 的 squarefree orders、与其他 basins 的 disjointness 来自已合并 Phase C/D 正常形；
- whole-basin odd 来自 §2 的本轮独立 O31 重建，不标为已核对的 Phase E source theorem；
- 本定义没有增加 literal chain、edge-only gateway 或特定 shared-residue choice；
- disjointness 是多个 basin 的 whole-ledger 条件，不是孤立 q 的额外自约束；
- 特定 K=2、E={1}、common a 是充分构造的选择，不是所有 actual certificate 状态的必要限定。

特别不要求 `{x∈D(q):3|w_x}={31}`。例如实际 relay 878851 的 order93=3*31，既直接指向3，也指向31；其 basal gateway 仍只有31。

## 4. FIRST-RELAY THEOREM

### Theorem F1 — complete unbounded first-relay classification

对任意 q∈B31^odd，令

\[
r=\min(D(q)\setminus\{31\}).
\]

不需要假定 q 是全类最小 root，也不需要 basin 是链。唯一 basal gateway 为31，故每个 admitted vertex 都可下降到31，31 为最小 vertex。r 的全部 odd order factors 只能在 `{3,31}`，且必须包含31，否则 r 又是 basal gateway。odd 与 squarefree 给出

\[
w_r\in\{31,93\}.
\]

本轮完整分解、递归 Lucas 素性认证与 exact-order tests 得到：

\[
\Phi_{31}(5)=1164153218269348144531
=1861\cdot625552508473588471,
\]

\[
\begin{aligned}
\Phi_{93}(5)&=699485272571293183230764923557158439390121\\
&=31\cdot148429\cdot878851\cdot172974812463239310024750410929.
\end{aligned}
\]

完整过滤为：

| index | factor | mod4 | exact order | disposition |
|---|---:|---:|---:|---|
|31|1861|1|31|free, non-admitted|
|31|625552508473588471|3|31|admitted, regular|
|93|31|3|3|imprimitive; not a relay of order93|
|93|148429|1|93|free, non-admitted|
|93|878851|3|93|admitted, regular|
|93|172974812463239310024750410929|1|93|free, non-admitted|

因此

\[
\boxed{r\in A_{31}^{\rm odd}=\{878851,625552508473588471\}.}
\]

两者在相应 primitive cyclotomic value 中的 multiplicity 都恰为1。另有独立 exact lifting checks：

| p | w_p | `(5^w mod p² - 1)/p` | s_p |
|---:|---:|---:|---:|
|31|3|4|1|
|878851|93|482192|1|
|625552508473588471|31|7444|1|

所以 r 不可能是 nonregular q，得到

\[
\boxed{|D(q)|\ge3.}
\]

这完整排除 two-vertex B31^odd，不排除 three-vertex 或一般 branching。

### Corollary F1.1 — conditional total original odd-row bound

Exactly-seven 正常形需要七个 disjoint regular heads。已合并 B7 first-relay theorem 强制7-basin另有一个 proper regular relay；F1 强制31-basin另有一个 proper regular relay；二者因 disjointness 是不同原始行。加上必须存在的 regular row3：

\[
\boxed{N=7\ \&\ \text{complete}\ \Longrightarrow
\text{至少17条 original odd rows，其中至少10条 regular}.}
\]

这里 N 仍是 original nonregular roots 的数量。此推论**没有**得到 N>=8。

## 5. ODD-ORDER PREIMAGE DAG

### 5.1 精确 congruence filters

对任何 prime x≡3 mod4，写 x-1=2m，m odd。则

\[
w_x\text{ odd}\iff w_x\mid m
\iff (5/x)=1
\iff x\equiv11,19\pmod{20}.
\]

前两步来自 cyclic group 的唯一 odd-order subgroup；最后一步由 `(5/x)=(x/5)` 与 mod4 条件合并得到。

若 exact order n odd，则

\[
x=1+2kn,\quad k\text{ odd},\quad kn\equiv5\text{ or }9\pmod{10}.
\]

这是 finite-index divisor probing 的完整 congruence gate；不能额外要求 k 或 x-1 squarefree。实际例子 `878851-1=2*3^4*5^2*7*31` 仍合法，因为其 order 只有93。

对于 basin edge x->p，p 与 x 都为3 mod4，x=1 modp，quadratic reciprocity 还给出 `(p/x)=-1`。因此所有直接 order-factor parents 在模 x 下都是 quadratic nonresidues，尽管5为 quadratic residue。这是一条必要关系，不单独产生矛盾。

### 5.2 受 theorem gate 控制的递归

从 R0={31} 开始。对 finite good regular state R，只考虑

\[
n=3^\epsilon\prod_{p\in S}p,
\qquad\epsilon\in\{0,1\},\quad\varnothing\ne S\subseteq R.
\]

每个 admitted exact-order preimage 来自 Phi_n(5)，过滤 odd order、mod4、exact order 与 lifting。regular preimage 可以加入状态；nonregular preimage 必须记录完整 predecessor closure，不能继续当成 proper regular helper。

按数值递增添加 vertices 可获得 canonical finite branching enumeration。任意 finite B31 basin 的 proper regular vertices 按升序排列，都可被该过程捕捉，因为每个 order factor 都小于其 vertex。

每层状态数有限，任意固定 vertex-count / height 的问题均有有限递归列表。没有证明总高度或总 vertices 有统一上界。

### 5.3 一个阻止错误“有限树证明”的定理

**Theorem F2。** 若 B31^odd 为空，则存在任意长、乃至无限的 regular all-odd prime-order chain，以31为 basal head。

证明。对于任意 admitted p>3，

\[
\Phi_p(5)\equiv3\pmod4,\qquad\Phi_p(5)\equiv1\pmod p.
\]

所以它至少有一个 admitted prime factor y!=p。其 exact order 为p，因而 y>p；在 p 的整个 closure regular 的条件下，y 的 proper closure 正是 D(p)。如果 y nonregular，它立即是 B31^odd member；若假设类为空，则每一步这样的 y 必 regular，可以一直延伸。证毕。

因此“all-odd preimage DAG 终究没后继”不是可用的空类机制。空类与无限 regular extension 完全相容；若能证明这个 regular extension tree 真正有限，反而会迫使此前出现一个 nonregular member。

### 5.4 实际 regular nodes 与 states

除31和两个 first relays 外，本轮认证：

| prime x | exact w_x | s_x | admitted parents >3 |
|---:|---:|---:|---|
|490398859|81733143=3*31*878851|1|31,878851|
|48486209671|2636553=3*878851|1|878851|
|268987578643643042531|625552508473588471|1|625552508473588471|

每行 prime 均有 full n-1 recursive Lucas certificate，order 均有所有 prime-factor order-drop tests，s=1 由模 x² 非1认证。

实际 good states 包括：

- `{31}`；
- `{31,878851}` 与 `{31,625552508473588471}`；
- 两个 first relays 同时加入31的 fork state；
- `{31,878851,490398859}`；
- `{31,878851,48486209671}`；
- `{31,625552508473588471,268987578643643042531}`。

所有这些 states 都只有 regular vertices。没有一个能被报告成 actual B31^odd member。

## 6. THREE-VERTEX CLASSIFICATION

### Theorem F3 — exact eight-index equivalence

若 D(q)={31,r,q} 且 q∈B31^odd，则 F1 给 r∈A31^odd。q 必须直接把 r 作为 order factor，否则不能到达 r。其余可能 factors 只有3、31，且全部 squarefree、odd。因此

\[
\boxed{w_q\in\{r,3r,31r,93r\}.}
\]

具体八个 indices：

| multiplier | r=878851 | r=625552508473588471 |
|---:|---:|---:|
|1|878851|625552508473588471|
|3|2636553|1876657525420765413|
|31|27244381|19392127762681242601|
|93|81733143|58176383288043727803|

反过来，对于任一上述 r 与 n，若 prime q≡3 mod4 且 q²|Phi_n(5)，则 q 是 actual three-vertex B31^odd member。

证明反向时必须排除 imprimitive squares：n 为 odd squarefree；若 ell|n，则 ell 在 Phi_n(5) 中的 multiplicity 至多1。于是 square divisor q 必有 q∤n，exact order 为 n。因为 n 含 r 且其他 factors 仅有3、31，proper admitted closure 恰为 `{31,r}`，这两者已经认证 regular；其余定义条件全部成立。

本轮没有证明八个 Phi-values 均不存在这样的 admitted square divisor，故没有推出 |D(q)|>=4。

### Height-two 与 four-vertex 分支的区别

若 admitted DAG 从31向上最多两条边到 root，proper relays 只能从两个 first relays 选取。因此除八个 chain indices 外，唯一 fork state 为

\[
R=\{31,a,b\},\quad a=878851,\quad b=625552508473588471,
\]

其 exact root-order family 为 `{ab,3ab,31ab,93ab}`。全部 height-two cases 共十二个 terminal indices；只有该 fork case 有四个 basin vertices。

任意四顶点 basin 还可能是三层 sequential extension：第二个 proper relay u 是某个 `{r,3r,31r,93r}` 的 regular admitted primitive preimage，随后 root 的 order family 由 §7 的状态定理给出。不能把四个 fork indices 冒称所有 four-vertex cases。

## 7. BRANCHING CLOSED-STATE FORMULATION

### 7.1 Good regular state

R 为有限 prime set，满足31∈R、3∉R；每个 p∈R admitted 且 regular，w_p odd squarefree；O(p)⊆R∪{3}，并且 absolute terminal closure 为 `{3}`。不要求 R 本身由单个最大 vertex 生成，也不要求它是链。

令 D_R(p) 为 p 在 R 内的 downward closure，包含 p。定义 maximal-generator antichain

\[
A(R)=\{a\in R:\ a\notin D_R(y)\text{ for every }y\in R\setminus\{a\}\}.
\]

有限 DAG 保证 `union_{a in A(R)} D_R(a)=R`。对于 S⊆R，

\[
\bigcup_{s\in S}D_R(s)=R\iff A(R)\subseteq S.
\]

必要性：若 a 是 maximal generator，它不能作为其他 R-vertex 的 proper descendant，只能自己属于 S。充分性由 maximal closures 覆盖 R。

### 7.2 精确 terminal order family

定义

\[
J_{31}(R)=\left\{3^\epsilon\prod_{p\in S}p:
\epsilon\in\{0,1\},\quad A(R)\subseteq S\subseteq R\right\}.
\]

则

\[
|J_{31}(R)|=2^{1+|R|-|A(R)|}.
\]

令 `q above R` **精确表示** `D(q)\{q}=R`，而不是“R 只是 q 的部分 descendants”。一个实际 terminal q 生成整个 R 当且仅当 w_q∈J31(R)。

这也是 arbitrary branching 中最关键的 support 条件：只要求 order factors 来自 R 不足够；必须直接包含全部 maximal generators。

### 7.3 Critical integer 与 iff

为防止多个 cyclotomic factors 的 imprimitive collisions 被错当成 square hit，定义

\[
C_n=\frac{\Phi_n(5)}{\gcd(n,\Phi_n(5))},\qquad
Z_{31}(R)=\prod_{n\in J_{31}(R)} C_n.
\]

n odd squarefree，gcd 恰去除所有 imprimitive index-prime factors，且这些因素只出现一次。每个 prime divisor of C_n 的 exact order 都是 n，因此 distinct C_n 两两 coprime。

**Theorem F4 — exact closed-state criterion。** 对 good regular state R 与 prime q，

\[
\boxed{q\in\mathcal B_{31}^{\rm odd}\ \&\ D(q)\setminus\{q\}=R
\iff q\equiv3\pmod4\ \&\ q^2\mid Z_{31}(R).}
\]

**证明。** 正向令 n=w_q。full proper closure=R 给 n∈J31(R)；q∤n，且 s_q=v_q(Phi_n(5))>=2，所以 q²|C_n。

反向，C_n 两两 coprime，故 q² 来自唯一 C_n。q primitive，w_q=n∈J31(R)。A(R)⊆support(n) 给 full proper admitted closure 恰为R；其中每个 vertex regular、all-odd、squarefree、terminal3。q 本身由 q²|Phi_n(5) nonregular，得到全套定义。

这里 q>max R 不必另加为假设：max R 属于 A(R)，因而整除 n；primitive q 的 n 整除 q-1，自动给 q>max R。

这是一个 exact arithmetic equivalence，不是 heuristic 或“存在某个方便 state”。但 **R 的全体仍是一个没有已知全局大小界的递归族**。符号上写出 Z31(R) 不表示已经展开、分解或认证其平方因子。

### 7.4 为什么 imprimitive factors 不能平方

对 n odd squarefree 与 odd ell|n，写 n=ell*m，ell∤m。若 ell|5^m-1，LTE 给

\[
v_\ell(5^{\ell m}-1)-v_\ell(5^m-1)=1.
\]

所有新 cyclotomic valuations 非负，所以 v_ell(Phi_n(5))<=1。若 ell∤5^m-1，新 quotient 模 ell 非零。2、5 也不产生本轮 admitted square divisors。

对于 q∤n 的 primitive factor，ord_q(5)=n，并有 s_q=v_q(Phi_n(5))。这是平方判据的来源，不是 polynomial derivative 判据。

## 8. CYCLOTOMIC SQUARE-HIT RESULTS

### 已经完整认证

- Phi31(5)、Phi93(5) 的完整分解及所有因子的 primality。
- 其中全部 admitted primitive factors regular；two-vertex class 空。
- 正常形使用的十二个 shallow cyclotomic products 已独立重算。
- 所列 deeper regular nodes 的 primality、exact orders、s=1。
- 三个 known nonregular sanity examples 的 exact s=2 与完整 terminal closures。

### 有界 divisor probe

只对 F3 已证明必要的八个 indices 做：

\[
q=1+2kn,\quad1\le k\le100000,\quad k\text{ odd},\quad q\equiv11,19\pmod{20}.
\]

每个 index 恰20000个候选，共160000个。先做 modular divisibility 与每个 prime-factor order-drop test；全部 surviving candidates 恰为 §5.4 的三个 prime，随后用 Lucas certificates 认证，全部 s=1。

这是该明确有限 k-domain 的穷尽结果，不是各 Phi_n(5) 的完整 factorization，不是任一八个 order-case 的无界排除。没有启动 general q-scan、大型整数分解或未经 gate 的 computation。

### 没有证明的命题

- 没有证明八个 three-vertex terminal indices 的 Phi-values squarefree。
- 没有证明所有 primitive admitted factors regular。
- 没有证明 arbitrary-branching class 有统一有限高度或 vertex bound。
- 没有以“derivative modq 非零”推断整数 Phi_n(5) 无平方因子。

`Phi'_n(5) != 0 modq` 与 `q²|Phi_n(5)` 可以同时成立：simple polynomial root 的某个固定整数 lift 恰好可能是 modq² root。Resultant/discriminant 只能控制相应 root collisions，不能省掉本轮的 integer square-hit 问题。

## 9. ARITHMETIC SANITY CHECK

| q | exact w_q | s_q | terminal set | why not B31^odd |
|---:|---|---:|---|---|
|20771|5*31*67=10385|2|{3,5}|有 free terminal5；且 proper relay67 的 order22为even|
|40487|2*31*653=40486|2|{3,653}|root order even；还有 free terminal653|
|1645333507|2*3^3*30469139|2|{3,761,1429}|root order even，3-depth=3非squarefree，另有free terminals|

尤其20771是“root order odd 不代表 whole basin all-odd”的实际反例：

\[
20771\to67\to11\to5,\qquad w_{67}=22.
\]

另一路20771->31->3不允许抹去上述坏分支。Absolute closure 必须展开全部 order factors，而不是选择一条有利路径。

## 10. ACTUAL MEMBER / EMPTINESS / N>=8 AUDIT

```text
ACTUAL B31^odd MEMBER?
NO — none found or certified in this session.

B31^odd EMPTY?
NO — emptiness has not been proved; this does not assert nonemptiness.

EXACTLY-SEVEN KILLED?
NO.

N>=8?
NO.
```

若将来证明本报告完整 intrinsic class B31^odd 为空，则 §2 的必要性给 exactly-seven complete certificate impossible；结合已合并 total N>=7 theorem，严格得到 N>=8。

这个 implication 必须使用整个必要类，不能只排除 literal chain、edge-only subclass、three-vertex states 或一个有界 divisor probe。

本轮实际得到的总数结论只有：`N=7 and complete => at least17 original odd rows`。不能把 regular helpers 加进 nonregular-root count。

## 11. STRONGEST NEW ARITHMETIC NECESSARY CONDITION

任何 hypothetical exactly-seven complete admitted certificate 的31-origin q 必须满足：

\[
\begin{gathered}
q\in\mathcal B_{31}^{\rm odd},\qquad |D(q)|\ge3,\\
\min(D(q)\setminus\{31\})\in\{878851,625552508473588471\},\\
R=D(q)\setminus\{q\}\text{ is a good regular state},\\
q\equiv11,19\pmod{20},\qquad
q^2\mid Z_{31}(R),\qquad w_q\in J_{31}(R).
\end{gathered}
\]

若 |D(q)|=3，J31(R) 就是 F3 的四个对应 indices；两个 first relays 合起来共八个 exact cases。一般 branching 则由 F4 保留全部 maximal generators，没有漏掉共享下游或多-parent orders。

## 12. NEXT SINGLE TARGET

**完整关闭最小实际 regular state R={31,878851} 的 terminal square-hit family**：

\[
J_{31}(R)=\{878851,2636553,27244381,81733143\}.
\]

目标是对这四个 indices 给出无界的 admitted primitive square-divisor 判定，首先处理最小 n=878851；不是继续扩大 general q-scan。任何实际大分解须先给出 complexity、压缩方案与小 benchmark；本报告没有授权这项大型计算。

仅完成该目标仍不等于 B31^odd 为空：另一个 first-relay family 和所有 larger closed states 仍必须保留。

## 13. REPLAY AND ADVERSARIAL AUDIT

运行：

```bash
python3 verify.py
```

标准库 verifier 不调用 SymPy，不信任 probable-prime declarations。它验证66个 recursive full n-1 Lucas certificates、37个 exact-order/lifting row records、两个 first-relay full products、十二个 shallow identities、七个 actual good regular states、maximal-generator 判据的有限独立枚举、normalized (2,2,3) frontier 与 opposite-parity center geometry，以及160000个候选的 full modular replay。

九个 corruption / malformed-state tests 全部被拒绝，包括：篡改 odd flag、lifting coefficient、Lucas witness、完整乘积、first relay list，以及把 terminal3、even-order7、non-squarefree-order19 或缺少31的集合冒充 good state。

`verification_log.json` 是实际运行结果。它不是 infinite theorem 的 formal proof，也不是仓库原生集成测试。

报告的关键防误推检查：

- terminal3 没有被错误纳入 all-odd quantifier；
- root odd 与 whole-basin odd 明确分开；
- basal gateway 不等于唯一直接3-edge；
- orders squarefree 不等于 x-1 squarefree；
- exact-order indexprime31已从 Phi93 的 proper-relay候选排除；
- whole R closure 要求所有 maximal generators，不能只用任意 support subset；
- critical product 去除 imprimitive factors，不能把跨因子的重复误判为terminal square；
- finite branching 不等于 finite total depth；
- actual regular skeleton 不等于 actual nonregular member 或 complete certificate；
- 17条 original odd rows 不等于 nonregular roots 至少8；
- 缺失 Phase E ZIP 没有被描述成已读取或已合并。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
