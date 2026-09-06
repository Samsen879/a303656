# Exact definitions and complete survivor grammar

本文件为 REPORT.md 的 operational companion。所有 arithmetic symbols沿用绑定repository formal class；这里新增的是 demand typing、pooled provenance与full-depth blocker对象。

## 1. Frozen universe and row states

一个输入实例固定有限actual admitted prime set P、所有K_q、允许的非空odd accepted sets、optional two-adic data，以及由保留的原始行确定的U与L。若r/E仍在搜索，对每行枚举一个finite exact family S_q；每个state包含完整paired masks，不允许分别列出anchor marginals后自由拼接。

一个原始行状态记录：

```text
OriginalState = (
  actual_prime q,
  precision K,
  shared_residue r mod q^K,
  accepted_valuations E,
  exact_order w,
  lifting_valuation s,
  anchor0_normal_form,
  anchor1_normal_form
)
```

不同q的CRT residues可以独立选择，但同一q的state必须在整个exponent domain、所有anchors、全部contraction branches中保持一致。正确存在性量词是

```text
exists one global state vector s
  such that for every original exponent x, the requested demand holds.
```

不是`for every x, exists a state vector s_x`。

冻结U以后抽取某个fiber subcover，不改变U；删除一个证明中的event，不表示从全局P删除其prime。加入新的资源而改变U，需要显式重建support与所有lower assignments。

## 2. Fatal semantics

`val_q,K(a)`在a=0 modq^K时返回K作为clipped sentinel，否则返回0..K−1。`Fatal(q,c,d)`要求该值属于E_q且严格小于K。

Full fatal mask按d mod w_qq^a_q定义。Coarse fatal mask要求固定d modU的每个compatible full lift都被同一行accepted。动态center处可能有某些safe lifts，已经足以让coarse event不fatal；不要求所有lifts都safe。

一侧rigid event必须由0<h<s_q的accepted valuation产生。s_q=1的regular row没有rigid fatal event。实际nonregular q必有一个odd factor整除w_q：若w_q=1，q|4不admitted；若w_q=2，唯一admitted可能为q=3，而s3=1。

## 3. Boolean demand lattice

覆盖集合C以bit mask编码：0=∅，1={0}，2={1}，3={0,1}。单调demand用其四个truth values编码：

```text
FALSE  = 0
BOTH   = 8
A0     = 10
A1     = 12
EITHER = 14
TRUE   = 15
```

EITHER的minimal satisfying antichain是{{0},{1}}；BOTH是{{0,1}}。不能把两者共同写成一个untyped“{0,1} demand”。

给定top coverage word T(z)，residual demand定义为

```text
R(D)(C) = AND_z D(C union T(z)).
```

三条关键消元式：

```text
R(Ac)     = Lower_c OR Sat_c
R(EITHER) = Lower_0 OR Lower_1 OR Sat_OR
R(BOTH)   = (Lower_0 OR Sat_0) AND (Lower_1 OR Sat_1)
```

这里Sat_OR不等于Sat_0 OR Sat_1。对SPLIT，它为TRUE而两个Sat_c均FALSE。

`D(C) => R(D)(C)`给一个局部demand弱化序。它不是universal no-go potential，因为EITHER可沿actual SPLIT合法变为TRUE。active-coordinate rank严格下降只保证termination。

## 4. Guarded events and typed macros

一个rank-p原始event记录：

```text
GuardedAtom = (
  original_row q,
  global_state s_q,
  anchor c,
  rank p,
  lower_CRT_guard G,
  exact_top_slice C,
  source_arithmetic_identity
)
```

原始dynamic slice是一个accepted shell bundle；rigid slice是一个positive-depth cylinder。rank-p宏记录：

```text
TypedMacro = (
  guaranteed_demand A0 | A1 | EITHER,
  lower_CRT_cylinder,
  eliminated_coordinate p,
  exact_slice_cover_witness I,
  compatible_original_state_tokens,
  parent_provenance_DAG
)
```

BOTH通过两个fixed-anchor保障的consistent conjunction表达，也可保存为显式AND节点。宏的几何形状可能为rigid cylinder，但它的类型永远不是actual prime row。

Pooled宏只能支持EITHER demand；不能向A0/A1 root注入。原始A_c event也能支持EITHER（一个anchor足够），但反向转换无效。

## 5. Coloured original prefix frontier

在X_p=Z/p^βZ上，primitive leaf是

```text
(depth e, position a mod p^e,
 anchor c, actual row q, global state s_q,
 source-component identifier)
```

dynamic shell S_j(ζ)展开为p−1个depth j+1的side cylinders，它们是同一bundle的OR组件，保留同一行ID，不生成p−1个primes。

固定lower point后，取活跃原始组件的primitive cylinders，删除strict-descendant redundancy并解决相同geometry的重复供应。Pooled full coverage等价于能够选出一个覆盖root的prefix antichain；每片leaf保留颜色和真实供应关系。

对original rigid q，同一fixed fiber最多有两个不同原始cylinders，至多一片/anchor；这两片必须来自同一state。只选择其中一片作为subcover是允许的，但并不抑制那个state本来存在的其他fatal events。

“primitive leaf集合最小”和“整条row bundle最小”不是同一概念。若需row-minimality，另对完整row events删除冗余，不能靠删除bundle内的一片叶冒充删除一行。

## 6. Complete grammar G_pool

以下是全部允许的生成规则。输入必须是已通过arithmetic normal-form validation的actual paired-state families。

### G0 — Materialize only original atoms

从固定original state的精确normal form生成anchor-tagged原子，或保留给定sound two-adic predicate。允许常量∅与whole domain。不得创造一个没有actual source的rigid prime。

### G1 — Restrict by named CRT data

对已有domain/cylinder按已有row orders、center moduli或已推导guards作exact non-coprime CRT intersection。冲突得到空集。不得无来源地插入一个有利lower subset。

### G2 — Expose primitive slices

仅将原始shell bundle按其公式展开为side cylinders，将CRT macro按当前maximal prime factor成lower guard×top cylinder。Bundle parent、anchor与state tags不丢弃。

### G3 — Produce a typed cover clause

在maximal coordinate p，选一个精确cover I，验证其top slices的union确为X_p。对A_c只使用有该anchor保证的events；对EITHER使用pooled guarantees。

检查所有state tokens一致，取stripped lower guards的CRT intersection，将该intersection与cover I及parent provenance一起保存为相应typed macro。Rank<p的原始events原样保留。

Top slices有full cylinder的lower-event singleton，仅为pass-through，不将一个原始lower dynamic event重命名为新CRT宏。代码的全slice实现使用这个等价规则。

### G4 — Conjoin compatible provenance

同一q同一state重复出现为idempotent reuse；同一q不同states的conjunction为FALSE。其他行state tokens作集合并。AND的geometry按G1处理。

### G5 — Keep alternatives as OR

不同有效clauses以OR保留。只允许经过exact geometry/token equality证明的去重，或经过实际implication证明的absorption。不把同一q在OR各支出现视为额外prime库存。

若需要disjoint children，按**已经存在的named guards**的common finite CRT modulus精细化，并给每个child保留一个原cover witness。不能为了完成覆盖额外创建没有parent的child。

### G6 — Eliminate maximally with its type

应用第3节的typed universal identity，移除p的全部dependence；macro moduli必须真正成为p-free。每个child剩余coordinate数减少1，因此整个过程有限。

对BOTH可分别构造A0、A1的roots，但最后必须在同一个global state assignment下取AND。不得用一个EITHER-covered root代替两个anchor roots。

### G7 — Check terminal arithmetic boundary

所有odd coordinates消去后，检查剩余实际two-adic domain及constant demands。无two-adic row时仍保留orders带来的coordinate2 support；若U为odd，最终domain为singleton。

一个frozen system的root为TRUE，当且仅当原始finite domain满足该root的typed coverage statement。这个等价性通过G3的双向cover-clause证明与G6的逐层归纳获得。

这是一套完整、可验证的有限instance grammar；它不声称arbitrary finite abstract grammar的每个leaf都能由某个未知prime实现，也不构成对所有primes的有限字面清单。

## 7. Original-resource accounting

| Multiplicity | 对象 | 正确规则 |
|---|---|---|
| branch-local reuse | 同一个q出现在不同lower cylinders | 允许，但s_q不变 |
| simultaneous leaf multiplicity | 一个fixed原始fiber的两色frontier | rigid q至多两片，至多一片/anchor；dynamic所有side leaves仍为一行 |
| provenance multiplicity | proof DAG中重复引用q | token集合幂等；不增加库存 |
| actual prime multiplicity | 原始P中不同q的个数 | 每个prime恰为一个资源，不能由宏展开增加 |

在多个branch上做加权估计时，先回到原始domain计算每个q的union incidence，再对其一个完整configuration取max。不能先对各branch独立max后宣称这些best states可同时实现。

## 8. Assigned full-depth blockers

Q_R为具有某个原始rigid fatal component的actual rows。一个allocation选择b(q)|w_q为odd prime。定义

```text
B_p = union of all projected rigid classes b_(q,c) mod p^v_p(w_q)
      for rows assigned to p.
```

与top-rank leaf不同，该projection可以落在P⁺(w_q)以下的坐标。它表示主动禁止一个必要congruence，不声称q是在这个坐标的actual original rigid supplier。

D_p为原始p-row的pooled conditional dynamic mass上界；at most one active anchor确保取一个bundle即可。若每个D_p+mu(B_p)<1，则可构造共同odd-safe point。

Global state固定后，所有projection可直接算出。若对全部residues作uniform theorem，可用至多两片、每片p^{-v_p(w_q)}的上界。

## 9. Minimal survivor class

冻结U、全部dynamic budgets及global row-state约束。对rigid-resource subsets运行明确的allocation feasibility问题：是否存在assignment使所有strict budgets成立？若完整集合失败，取inclusion-minimal失败子集。该对象叫minimal blocker-deficient core。

这个词不宣称已知最小actual complete pooled cover，更不宣称删除prime后ambient不变。实际candidate必须另外通过arithmetic state validation、coloured-frontier coverage与G_pool的typed TRUE root。

Single-nonregular q candidate若有free odd factor或p²|w_q立即被排除。剩余最小计数signature为squarefree odd order且所有其odd factors拥有原始dynamic-capable rows；具体whole-system feasibility仍保留完整grammar。
