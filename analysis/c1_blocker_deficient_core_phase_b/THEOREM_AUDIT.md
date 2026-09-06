# Theorem audit — Phase B

本文件给出本轮新推导的自包含证明与 scope guards。`PROVED` 表示下面给出数学证明，
不是声称经过 proof assistant 或另一个独立作者审核。程序是 regression / arithmetic
certificate checks，不是普遍定理的归纳替代。没有做整个数学文献的新颖性宣称。

## H1. Finite capacitated Hall / min-max

左侧 Q，右侧 Lambda，所有 capacities t_lambda 为正整数。把每个右点复制成
相应数量的 slots，得到普通二部图。最大 matching 数为

    nu = min_{S⊂Q} (|Q\S| + C(N(S))), C(A)=sum_{lambda∈A}t_lambda.

必要性：S 至多匹配到 C(N(S)) 个 slots，其他行至多 |Q\S| 个。
充分性：取最大 matching，从未匹配的左点沿 alternating paths 出发。无 augmenting
path 时，所有可达右 slots 已匹配，且其 owner 左点也可达。设可达左点集 S；
其 matching deficit 恰好给出上式的 tight cut。等价地，可用整数最大流。

Primal / dual：

    max sum z_(q,lambda)
    sum_lambda z_(q,lambda)≤1; sum_q z_(q,lambda)≤t_lambda; z≥0.

    min sum_q alpha_q + sum_lambda t_lambda gamma_lambda
    alpha_q+gamma_lambda≥1 on every edge; alpha,gamma≥0.

Slot graph 的 integral matching/min-cut 给出 integral optimum；对一个 Hall cut S，
取 alpha_q=1_{q∉S}、gamma_lambda=1_{lambda∈N(S)} 得到对应的整数 dual。

函数 delta(S)=|S|−C(N(S)) 是 supermodular：邻域容量是 submodular。
因此最大 deficit 的所有 maximizers 在 union/intersection 下封闭；它们的交和并
给出 canonical smallest/largest maximum-deficit sets。不能把它们和某个任意
inclusion-minimal deficient core 混为一谈。

## H2. Minimal deficient-core structure

设 S inclusion-minimal deficient，m=|S|，N=N(S)。则：

1. C(N)=m−1。
2. 每次删去一行 q，N(S\{q})=N，且剩余 m−1 行能匹配并占满全部 slots。
3. 每个右点满足 deg_S(lambda)≥t_lambda+1。
4. 对 nonempty proper R⊂S，
   C(N(S)\N(S\R))≤|R|−1。
5. m>1 时所有左邻域非空，诱导二部图连通；m=1 当且仅当该行邻域为空。

证明：若 m>1，minimality 给 m−1≤C(N(S\{q}))≤C(N)<m，均为整数，
因此全都等于 m−1。正 capacities 强迫两个邻域相等。所有 proper subsets
满足 Hall，因此 deletion matching 存在并饱和右侧。m=1 直接成立。

取 R=N^{-1}(lambda)∩S；S\R 不邻接 lambda。Hall 给
m−|R|≤C(N)−t_lambda=m−1−t_lambda，故 degree bound。
同样，对任意 R，m−|R|≤C(N(S\R))，移项即得第4项。
若 m>1 且图有多个 components，每个 component 是 proper left subset，
各自 deficit≤0，求和不可能等于1。空邻域行本身已 deficient，故不能处于更大的最小核心。

Paired capacities 给 lambda≤2m−1；single capacities 给 lambda≤m。
这些结论是 finite matching geometry，不保证相关行真的为 nonregular primes。

## G1. Guard forest escape theorem

固定实际 admitted P、K、r、E，选一个 anchor，或同时选择两个 anchors。
令 T⊂P 包含全部 nonregular Q。每条 targeted row p 选择 odd divisor b(p)|w_p。
若 b(p) 是实际 row label，它必须也在 T，或已经在 boundary 处证明不活跃。
因 b(p)<p，所有 edges 严格下降。

在每个接收坐标 lambda 上，把所有 assigned original rows 在所选 anchors 的
positive-divisibility logarithm classes 投影到 lambda-primary coordinate。
假设这些 forbidden cylinders 的 union 不是整个坐标。
则可选择 full exponent，避开所有 odd fatal rows；若所选 anchor 的 two-adic
boundary 也 safe，完整 simultaneous certificate 不可能。

### 直接在 L 上的证明

依次固定 L 的 rational-prime CRT coordinates，从 coordinate 2 开始。
考虑 odd lambda：

- 若接收 assigned guards，且 lambda 在 P 中，其自身行已经被更低 b(lambda)
  阻断，或已预先不活跃。因此可自由选一个不在 forbidden union 的 lambda-coordinate。
- 若 lambda 不在 P 中，没有自身动态行，选择同样自由。
- 若没有 incoming assignments，且自身行 targeted，它已被更低坐标阻断。
- 剩余情形只有 untargeted regular row lambda。其 positive-divisibility guard
  modulo w_lambda 只依赖较小坐标。如果 guard 不成立，该行安全。如果成立，
  因 s_lambda=1，5 生成的 subgroup modulo lambda^K 正好是 <5 mod lambda>
  的全逆像；因此可选自己 lambda-primary exponent coordinate，使本地值为零
  modulo lambda^K。L 包含 lambda^(K−1)，所以这一零值选择确实存在。
  Local zero 是 unresolved，不能 fatal。

同时处理两个 anchors 时，同一 regular row 的两个 lower guards 不可能同时成立，
否则 lambda|2。因此只需为其中至多一个 anchor 选择 zero，另一边不正整除。
所有较高坐标不会改变已完成的条件。有限 CRT 完成所需 full exponent。

这里用到的 regular lifting fact 可由 LTE 证明：
ord_(p^K)(5)=w_p p^(K−1) 当 s_p=1；其 subgroup 大小和 mod-p subgroup
全逆像大小相等。全程不把 zero 当成 accepted valuation，也不消费 macro。

### Worst-case sufficient quotas

每个 original row / anchor 最多贡献一个 first digit。
因此 single load≤lambda−1，或 paired load≤(lambda−1)/2，均足够。
使用完整 primary cylinders 时，严格质量上界

    sum_assigned lambda^(−v_lambda(w_p)) < 1

也足够；它只用于证明 union 非满，不是假设饱和质量等价于覆盖。
若 cylinder 位置已知，可改用 exact prefix-tree union criterion。

## G2. Arithmetic capacity contraction

令 t_lambda=(lambda−1)/k，k=1 或2。对 admitted p，O(p) 是 w_p 的不同奇素因子。
因为 p≡3 mod4，v2(p−1)=1，且 w_p|p−1，

    product_{lambda∈O(p)} lambda ≤ (p−1)/2.

对任意整数 factors a_i≥2，sum(a_i−1)≤product(a_i)−1；可由两个 factors
的 (a−1)(b−1)≥0 归纳，空乘积也成立。因此

    C(O(p))≤(p−3)/(2k)<(p−1)/k=t_p.

若 O(p) 中一个 admitted factor 用其更低 frontier 替换，总容量不增加。
所以 C(F_P(p))≤C(O(p))<t_p。

## G3. Transitive terminal Hall escape

若 Q 能匹配到 F_P(q) 的 t_lambda slots，则存在 G1 的 guard forest。

证明：对每个匹配对选一条下降路径。匹配 slots 全部不同。若一条路径通过内部 p，
其 terminal 属于 F_P(p)，故通过 p 的路径数至多 C(F_P(p))<t_p。
不同 incoming row edges 对应不同的入 p 路径事件，所以 incoming load 也不超过此数。
每个 free terminal 的 load 不超过其匹配 slots 数。

对所有路径的 union，每个 actual relay row 只保留一个已出现的 outgoing edge。
下降性保证不会出现环，closure 仍在 union 内，删除 edges 不会增加任何 forbidden union。
于是所有配额均满足，G1 给出 escape。

这证明 terminal Hall 是一个足够的 no-go criterion，不是所有 guard forests 的必要条件。
路径可以合并，只有一次 relay guard 要被阻断；conserved flow 不捕捉全部这种收益。

## G4. Exact conserved-flow min-cut

构造网络：source→q_out 容量1，q∈Q；每个 actual relay p 有 p_in→p_out
容量 t_p；每个 odd order edge p_out→lambda_in 容量 INF；free terminal
lambda_in→sink 容量 t_lambda。source injection 在 q 的 gate 之后。
取 INF 大于全部有限容量之和。

有限 cut 的 source-side out-nodes 集 A⊂P 给出成本

    |Q\A| + C(O(A)\A).

若 boundary 中有 admitted p∉A，把 p 加到 A 至少移除 t_p，最多加入
C(O(p))<t_p，并且不会增加 source-edge 成本。因此最优 cut 可取对 admitted
下降边闭合。由 G3 的 paths 和 integral flow，得到 exact identity

    max conserved routed flow
    = min_{A⊂P} (|Q\A|+C(O(A)\A))
    = min_{S⊂Q} (|Q\S|+C(F_P(S))).

这是这个明确定义的 flow 的 min-max，不是完整 certificate CSP 的 min-max。

### Coalescing converse 的实际 order-labelled 反例

P=T={11,23,67}，全部实际 regular rows。odd supports 分别是 {5},{11},{11}。
Paired terminal5 只有2 slots，三个 mandatory targets 的 conserved matching 不满。
但 forest 11→5，23→11，67→11 的 loads 是1和2，分别≤2和5，完全有效。
这里的 mandatory T 不是 nonregular Q；反例只否定“terminal Hall 对所有释放森林必要”。

## B1. Boundary-primed row 3 lemma

对任何 admitted system，总可以选一个 anchor c 和 two-adic exponent boundary，
使 two-adic row safe，并且 actual row 3（若存在）不正整除。

没有 two-adic row 时，可选任意 d，再利用 V_(3,0)−V_(3,1)=2 选不整除的 anchor。

有 two-adic row、r2 even 时，5 生成 modulo 2^K 的所有1 mod4 units。
若 r2≡0 mod4，选 5^d=r2−3：两个值为2和0。
若 r2≡2 mod4，选 5^d=r2−5：两个值为4和2。
因此两 anchors 同时 two-square-safe；再从中选择 row3 不正整除的那个。
K=2 时将4按0解读；需要时显式固定 d 的奇偶性。

r2 odd 时：r2≡3 mod4 选 c=0，r2≡1 mod4 选 c=1。
该 anchor 的 two-adic local value 对每个 d 都是1 mod4 的奇数，因而 safe。
对 fixed c，row3 的 positive guard 至多占据一个 exponent parity，因为 w3=2。
选择另一个 parity 即可。

奇数1 mod4 的 residue 可表为两个平方：K≥3 时，1 mod8 为平方；5 mod8
减4后为平方。1 mod8 units 的平方 lifting 用通常的逐位归纳得到。
5 的 exact order 2^(K−2) 由 v2(5^(2^j)−1)=j+2 得到。

因此 row3 的 higher precision、accepted E3 不影响该引理：这里已排除正整除。
这不是假定两 anchors 在所有 r2 下都有 common-safe exponent。

## B2. Primed terminal Hall and arithmetic exceptional circuits

预先应用 B1，然后在 G1–G4 中把3作为 free terminal，容量 h3=2，其他容量
h_lambda=lambda−1。实际 row3 没有被删除，只是其 guard 已为假。
得到 panel-relative F^3_P(q) 的 Hall criterion。

进一步定义 absolute T(3)={3}，T(p) 递归到3或1 mod4 prime。
对 p>3，w_p 的 odd support 非空：w=1 没有 admitted odd prime，w=2 仅可能
p=3。因此 T(p) 非空，且下降终止。

从 F^3_P(S) 开始，将所有缺失的 admitted terminal p>3 按其 odd order factors
展开。G2 保证每次容量不增加；最后得到 T(S)。所以

    C(T(S))≤C(F^3_P(S)).

于是

    [for all S⊂Q, |S|≤sum_{lambda∈T(S)}(lambda−1)]
    => no complete simultaneous certificate.

其逆否命题是新必要条件，不是把不存在的 descendants 当 actual rows。

对最小违反该条件的 S，H2 给

    |S|=1+sum_{lambda∈T(S)}(lambda−1),
    degree_S(lambda)≥lambda.

所有 T(q) 非空，所以不能 singleton，也不能两行。
所有 capacities 偶数，所以最小 circuit 大小是奇数。
若3不在 frontier，则 |S|≡1 mod4；若3在，则 |S|≡3 mod4。
大小3只可能 T(S)={3}，大小5只可能 {5}，大小7只可能 {3,5}。
大小9、11不可能；13为{13}；15为{3,13}。
这些是 capacity signatures，不是实际 nonregular primes 已存在的证明。

## K1. Exact shallow gateway inventories

Pure-3 terminal paths 可选择每步最大的 odd order factor。其最后 gateway g 满足
w_g=3^e 或2·3^e。以下 identities 完全分解后检查 primality 和 exact order：

    Phi_3(5)=31;           Phi_6(5)=3·7;
    Phi_9(5)=19·829;      Phi_18(5)=3·5167;
    Phi_5(5)=11·71;      Phi_10(5)=521.

因此 pure-3 depth1 admitted gateways 只有7、31，depth2只有19、5167。
Pure-5 depth1 gateways 只有11、71。521≡1 mod4；Phi 值中的3不是相应 order 的资源。
完整性来自有限 order classification 与这些整数的全部因子，不是 q_max。
这些浅层 gateways 都 regular，但它们可以作为被阻断的 actual relay rows。

对 at most a≤6 条 pure-3 paths，distinct terminal gateways 的 guard union mass
上界 F3(a)，以及 at most b≤6 条 pure-5 paths 的上界 F5(b) 为：

| n | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| 27 F3(n) | 0 | 9 | 18 | 21 | 24 | 25 | 26 |
| 25 F5(n) | 0 | 5 | 10 | 11 | 12 | 13 | 14 |

F3 来自至多两个1/3、两个1/9，其余≤1/27。
F5 来自至多两个1/5，其余≤1/25。
即使若干 paths 合并到同一 gateway，也只算这条 original row 一次，所以上界仍正确。

## K2. Six-root guard-routing no-go — 本轮最强 unbounded-prime 结论

**定理。** 任意 finite admitted system，若 |Q|≤6，就不可能是 complete
simultaneous C=1 certificate。Regular rows 可以任意多、任意大；所有 K、E、r
任意；允许 sound two-adic row。没有 prime cutoff。

### 证明

首先用 B1 选定安全 anchor/boundary，使 row3 不活跃。
对每个 q∈Q 沿 absolute order DAG 选择一个 terminal：

- 若 T(q) 含 prime≥13，选其中一个；
- 其余分成 a 个 T(q)={3}，b 个 T(q)={5}，k 个 T(q)={3,5}。

当然 a+b+k≤6。Pure-3 和 pure-5 roots 使用 largest-factor paths。
Mixed roots 分配 x 个走向3，其余 k−x 走向5，沿任一对应下降路径。

取 M3(a)=2−min(a,2)，M5(b)=4−min(b,2)。因为

    M3(a)+M5(b)=6−min(a,2)−min(b,2)≥6−a−b≥k,

可选 x≤M3(a)、k−x≤M5(b)。K1 的表给出

    F3(a)+x/3 < 1,
    F5(b)+(k−x)/5 < 1.

这两条不等式也可直接逐 a,b 表格检查：F3(a)<1；a=0,1,2 的剩余配额
分别为2,1,0；F5(b) 在 b≥2、b≤6 时≤14/25<3/5，所以还能容纳2个1/5。
程序核对全部84个 (a,b,k) triples，但证明不依赖未知 prime inventory。

实际 panel 缺失某条 admitted path row 时，就在该 free coordinate 停止。
它至少为7，所以至多6条 paths 的 first digits 仍不能覆盖整个坐标。
没有截断的 actual internal row primes 也至少为7，其 incoming distinct guard
edges 至多6，故同样留有一个 digit。Terminal≥13 的容量更足够。
Terminal3 和5 则分别由上述严格 Kraft-type mass bounds 留出空 cylinder。

现在取 paths 的 union，每个 actual relay 只保留一个 outgoing edge。
所有 incoming loads / forbidden unions 只会减少。每条 targeted actual row
都在更小坐标被阻断；G1 给出安全 full exponent，矛盾。证毕。

### 必须保留的 scope

- 6 是 nonregular **roots 的总数量**，不是所有 actual rows 数量。
- 各路径可以包含任意多个 regular relays；每个坐标的 indegree 仍≤6，
  因为一条严格下降 path 只能进入该坐标一次。
- 不把 generic relay guard 当成 nonregular rigid leaf；K1 的 regular gateways
  只是用来阻断其 divisibility，从而释放它们的 own coordinates。
- 不能仅拿某个三行 deficient subcore 套用 K2，忽略 panel 内其他 nonregular rows。
- `|Q|≥7` 是必要条件，不是七行存在完整证书，也不宣称下界 sharp。

## E1. Explicit surviving arithmetic class

定义 E 为所有 admitted finite panels，满足 |Q|≥7 且 primed panel-relative terminal
Hall 失败，即存在 nonempty S⊂Q，

    |S|>sum_{lambda∈F^3_P(S)}(lambda−1).

每个 hypothetical complete certificate 的 panel 必在 E，来自 B2 和 K2。
因为 N_P(S)⊂F^3_P(S)，且 single capacities 不小于 paired capacities，
E 确实包含在原来的 direct paired-Hall-deficient panel class 内。
已知边界 singleton 不在 E；任何至多六行 nonregular pool 也不在 E，故缩小严格。

另外 C(T(S))≤C(F^3_P(S))，所以 E 中每个 panel 的 absolute T 图也有 deficient
subset，可以再取一个最小 circuit 并应用 B2 的 terminal-signature 分类。
这个 absolute minimal circuit 不必等于 panel graph 的 minimal circuit。
单独 absolute-Hall 失败是较弱条件，不能把那个较大的类误称为原始类的严格子集。
E 的实际 nonregular inventory 与 shared-residue complete coverage 尚未判定。

因此用户的 literal Theorem A 为假，完整 arithmetic Theorem B 未获得；
这里获得的是 Theorem D / Gate C 的明确 exception reduction，加 K2 的 universal
cardinality obstruction。不是 universal C=1 no-go。

## Counterexample / overclaim audit

**Literal A false, actual singleton:** q=1645333507，P 含3和30469139，则 N_P(q)=empty。
q prime、s_q=2 已独立认证。它是实际 original direct-Hall core，不是 complete certificate。

**Order-compatible 不等于 nonregular:** P={7,31} 的两条实际 order supports 都只有3；
paired cap3=1，形成两行 minimal deficient graph，没有 internal support edge。
但两行均 regular，所以它不回答“actual nonregular core 每行都必须有 internal edge吗”。
这一额外 arithmetic assertion 本轮仍未证明。

**No all-common factor:** abstract minimal graph neighborhoods {3},{3,5},{5},{5}，
paired caps1,2，缺额1且全部 deletion matchable，没有所有左点共同的 neighbor。

**Coalescence:** G4 的 regular-row example 否定把 conserved-flow failure 当作最终 no-go
策略穷尽。E 故意只是 necessary residual class，不能称作全部不可释放核心的精确分类。

**Digit collision 不是默认 invariant:** actual q20771 的5192个 shared low residues，
在 coordinate5 有1038个相同投影、4154个不同投影。具体 witnesses 见 results。
这是同一 actual row 两 anchors 的现象；没有把它复制成多个 distinct primes。

**Kraft 接口边界:** K2 用原始 relay guards 的 union 上界，不是从一般 blocker Hall
缺额推导某个 shared-lower rigid full fiber。#15 的 H1 缺口仍未被证明；#16 的
81-row /21-row rigid-3-fiber bounds 不能无条件应用到 derived macros 或所有 panels。

## Final audit verdict

    H1–H2: PROVED, finite capacitated matching structure.
    G1–G4: PROVED, explicitly scoped guard/flow theorems.
    B1–B2: PROVED, boundary priming and transitive arithmetic Hall.
    K1–K2: PROVED, finite identities + universal six-root obstruction.
    E1: PROVED, necessary exceptional-class reduction.
    Literal universal deficient-core nonexistence: FALSE.
    Complete classification of actual nonregular cores: NOT PROVED.
    UNIVERSAL C=1 NO-GO: NOT PROVED.

    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED
    GITHUB WRITES PERFORMED: NONE
