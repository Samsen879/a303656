# A303656 C=1 EXACTLY-SEVEN BASIN GLOBAL SHARED-STATE REALIZABILITY
## Targeted Phase E — 统一状态构造、奇偶持久性与 31-basin gate

## 0. 结论与证明层级

**没有排除 exactly-seven，没有推出 N>=8。** 本轮的主结果是构造性兼容，而不是七根的算术实例化。

在来源的 exactly-seven normal form 内，本报告给出以下新推导：

- **E1 / arbitrary-basin filling：** 任意一个满足该 normal form 的实际有限 regular closure，可在一份固定实际行状态下填满自己的整个指定叶纤维；不要求是链。
- **E2 / seven-basin gluing：** 七个不交盆地的 E1 状态可由 CRT 合为 ONE global residue，同时实现全部七个 mandatory rank-3 roles。
- **E3 / parity-deletion lemma：** 固定选定 anchor，从 row3-inactive parity 翻转时，一个 single-origin basin 的 whole-private-fiber profile 保持原叶，当且仅当该盆地所有原始行的 multiplicative orders 均为奇数；否则 profile 为空。
- **E4 / opposite-parity necessity：** 完整 exactly-seven 必须使 31-headed basin 全部为奇数阶。并且 row3 必须接受 valuation 1，其动态中心的第一位必须位于 31 的叶。
- **E5 / full two-anchor compatibility：** 给定满足 normal form 算术条件的七个实际有限盆地，只要 E4 的 all-odd 31 条件成立，就可显式构造完整 simultaneous C=1 state。所有 odd rows 可取 K=2,E={1}。

因此，针对这些实际有限算术输入，状态存在性已压缩为一个明确条件：

    prescribed seven-basin arithmetic normal form admits a complete C=1 state
       iff O31: every x in the 31-basin has odd ord_x(5).

这里的“算术 normal form”在 §2、§4 精确定义，不是任意七个抽象图。上述存在性允许选择合法 K,E，充分性统一取 K=2,E={1}；它不是对任意预冻结 K,E 的无条件 iff。必要性使用来源的 exactly-seven normal-form theorem；充分性由本报告直接构造。**并没有证明这样的七个实际 nonregular roots 存在，也没有证明 O31 的算术族非空。**

E1–E5 是本轮给出的可审阅数学证明，不是已在仓库 promoted 的定理，也未经过另一作者或 proof assistant 的独立确认。来源中的 literal-chain compatibility 本来已经成立；本轮不把它重新标成新发现。

推荐执行环境：网页端数学研究与 standalone reference laboratory。本轮已完成中等规模 exact checks，没有使用 Codex CLI、Ultra、大型 scan 或 repository-native 执行。

## 1. LIVE AUTHORITY

```text
REPOSITORY: Samsen879/a303656
REPOSITORY ID: 1333945235
MAIN SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
MAIN TREE: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
HEAD: Merge PR #29
HEAD COMMIT TIME: 2026-09-08T03:37:01Z
FINAL LIVE-MAIN RECHECK: UNCHANGED
```

已通过连接的 GitHub GET 核对这些已合并 PR：

| 来源 | PR | merged at (UTC) |
|---|---:|---|
| Global Shared State Phase C | 22 | 2026-09-07T09:49:22Z |
| Order-DAG Phase C | 24 | 2026-09-07T09:57:50Z |
| Provider Charging Phase D | 26 | 2026-09-08T03:28:13Z |
| Two-Nonregular Phase D | 27 | 2026-09-08T03:31:05Z |
| B7 Phase D | 28 | 2026-09-08T03:33:50Z |
| Seven-head Chain Phase D | 29 | 2026-09-08T03:37:02Z |

六个指定包的阅读通过固定 SHA 文件及引入它们的完整 PR diff 完成。这里没有把源报告内部较早的 authority SHA 当成 current main。`SOURCES.md` 和 `AUTHORITY.json` 记录来源绑定。

执行边界：未取得本地完整 repository checkout，未重新运行仓库 integration tests、producer runners、CI 或 q<=2e9 inventory scan。`reference.py` 是本轮新写、仅用 Python 标准库的独立小型实现；源包 PASS 与本轮 PASS 分开记录。没有把未实例化 terminal 的 conditional profile 当作 actual arithmetic ledger。

## 2. EXACTLY-SEVEN NORMAL FORM

以下使用 [S1, Theorems 7.1–7.2] 的必要 normal form，而不是重新假定结论。

选择 two-adic boundary anchor c*，再选择 row3 在此 anchor 不动态覆盖的 parity b。来源先由七个 original rigid seeds 限制 first essential nonlinear rank <=7，再排除 rank5、rank7，留下 rank3。浅层实际 heads 仅有两枚 depth1 和两枚 depth2，其最大质量为

    2/3 + 2/9 = 8/9 < 1.

因此必须到达 depth3。完整三叉前沿若到达深度 m，至少需要 2m+1 个叶；七叶给 m<=3。七叶又恰有三个 internal vertices，存在 depth3 便强制这三个 internal vertices 排成一条内部路径：根的两个孩子直接为叶；第三个孩子的两个孩子直接为叶；最后一个孩子有三个叶。

故不是仅有数字 (2,2,3)，而是完整前缀树

    two depth-1 sibling branches;
    two depth-2 sibling branches inside the remaining depth-1 branch;
    three depth-3 sibling branches inside the remaining depth-2 branch.

depth1 heads 必为 31、7；depth2 heads 必为 19、5167；depth3 为

    G3={163,271,487,4159,31051,16018507}

中三个互异成员。三个在 order27，三个在 order54。它们的素性、exact orders 和 regularity 均在本轮小型 reference 中重新检查。

对 root q，D(q) 包括 q 及全部 admitted descendants >3；terminal 3 不放进 D(q)。normal form 给出：所有 proper descendants 是 actual regular helpers；七个 D(q) 两两不交；所有 odd order factors >3 都在自己的 closure；若最终叶深度为 e，则所有 x in D(q) 满足

    v3(w_x)<=e;
    vp(w_x)<=1 for every odd p>3;
    w_x=ord_x(5).

每个 proper helper 接受 valuation 1，实际 linear incoming cylinder 位于其 fixed dynamic center。约束是关于 ord_x(5)，不是关于 x-1 的全部因子。admission x=3 mod4 自动给 v2(w_x)<=1。[S1]

Charging Phase D 的结论为每盆地 shadow capacity=1，七叶总需求=7；不是进入下一层必然产生新欠账。[S4]

## 3. SEVEN BASIN ROLES

这里列出的 positions 是本轮自由选 state 时采用的一个共同布局。一般 frozen input 的真实叶位置可以不同；没有宣称能在不改变其 states 时任意重排。

记 C_e(a)={d:d=a mod3^e}。选择 c=1、b=0：

| role | mandatory head | e | 指定 3-adic 叶 | 该 head 的 lower log |
|---|---:|---:|---|---|
| B1 | 31 | 1 | C1(0) | 0 mod3 |
| B2 | 7 | 1 | C1(1) | 4 mod6 |
| B3 | 19 | 2 | C2(2) | 2 mod9 |
| B4 | 5167 | 2 | C2(5) | 14 mod18 |
| B5 | g1 in G3 | 3 | C3(8) | 8 mod27 或 8 mod54 |
| B6 | g2 in G3 | 3 | C3(17) | 17 mod27 或 44 mod54 |
| B7-role | g3 in G3 | 3 | C3(26) | 26 mod27 或 26 mod54 |

最后一行的 role label 不是“以 7 为 basal gateway 的 B7 arithmetic class”；后者是第二行的盆地，避免名称混淆。

在 even parity 的 27 个 3-adic cells 上，逐盆地累计覆盖数为

    9,18,21,24,25,26,27.

一般必须区分 mandatory basin roles 与 literal H0。H0 选 g1,g2,g3=271,4159,31051；一般有 C(6,3)=20 个 head sets、120 个有序分配，不是仅一个 set，也不是仅120个 DAG。[S1,S6]

## 4. GLOBAL STATE VARIABLES AND CENTRAL QUANTIFIER

固定一个实际有限 ledger 时，每行只有一份

    s_p=(r_p modp^Kp, Kp, Ep),
    V_(p,c)(d)=r_p-3^c-5^d.

同一 r_p 同时决定两个 anchors 的行为。local zero modulo p^Kp 使用截断 sentinel Kp，绝不计作 fatal；非零时只接受 Ep 中满足 0<h<Kp 的 odd h。原始

    U=lcm(t2,{w_p}),
    L=lcm(t2,{w_p*p^max(0,Kp-sp)}),
    sp=vp(5^w_p-1)

在分析中保持，不通过删除行擅自重算。[S2,S3]

真正的有限状态问题是

    exists ONE s, for EVERY exponent vector x representing d modL:
        all required typed demands hold.

指数向量是 universal test variable，不是要求一个 d 同时属于七个互斥叶。七个 basin duties 是

    for every i, for every d in its designated parity/leaf:
        some actual row in D_i is fatal at the designated anchor.

若固定 K,E，有限 SAT 可给每个实际 r_p 一个 one-hot state；log、center、guard、valuation 都由这个 state 的实际模幂导出。若 K,E、prime inventory 尚未固定，问题是一族有限 CSP，不能把未知 q 当作已经存在的 SAT row。

### Exact CRT separation

对七盆地 core，任何共享 odd primary coordinate >3 都会是两盆地共享的实际 admitted descendant，违背 full closure disjointness。所以 core 仅在 2、3-primary coordinates 上共享指数变量。

把原 L 精确分解为

    Z = (d mod 2^beta, d mod 3^gamma),
    X_i = all full private primary coordinates of basin i,
    X_out = retained ambient coordinates outside the core.

私有坐标包括 higher own-coordinate powers，以及 Kq>sq 时的 root own-coordinate powers；不能只保留 row labels。固定状态后的 core 函数 F_i,c(Z,X_i) 不依赖 X_j (j!=i)。

**重要范围：** 任意额外 regular row 可能同时读取几个盆地的坐标。完整 arbitrary typed CSP 必须把它保留成额外 factor，不能无条件宣称全 ledger 都是七块独立系统。对于本报告的正向构造，core 已经覆盖，额外正覆盖无害；对于 c* 的必要性，闭包之外全是 regular rows，可在 core escape 上按素数递增选择 safe centers。因此它们不能修补一个 boundary core escape，且不需要删除原 U/L。[S2 safe extension; S4 support confinement]

### Theorem E1 — arbitrary-basin canonical filling

给定一个实际 finite basin D=R union {q}，满足 §2 的 arithmetic closure、regularity、depth e 和 squarefree-private-order 条件，q nonregular。固定 anchor c、parity b、leaf lambda mod3^e。CRT 选一个非负整数 a：

    a=b mod2,
    a=lambda mod3^e,
    a=0 modp for every p in R.

为这些 actual rows 一次性设置

    Kp=2, Ep={1};
    r_p=3^c+5^a modp^2                       (p in R),
    r_q=3^c+5^a+q modq^2.

则整个 {d=b mod2, d=lambda mod3^e} 在 anchor c 被该盆地覆盖。

**证明。** 若存在 p in R 使 d!=a modp，取数值最小者。w_p 的所有 odd factors >3 都是 R 中更小的素数，故对应坐标与 a 一致；2、3-primary factors 由指定 parity/leaf 匹配。所有 private order depths 为1，所以 w_p | d-a，同时 p不整除d-a。regularity sp=1 给 vp(5^d-5^a)=1，p 行 fatal。

若所有 R 的 own digits 都与 a 一致，同理 w_q | d-a。sq>=2 给 5^d=5^a modq^2，因此 q-row 的 local value=q modq^2，valuation恰为1。local zero 从未被计作覆盖。证毕。

这个证明允许 arbitrary branching、盆地内部多个 parents 引用同一 helper、额外 3-edges，以及 depth2/3 的非平方自由 3-primary factors。它只要求 >3 的 order factors 平方自由。

保留 odd-row 原 K,E 的版本也成立：regular rows 需1 in Ep；root 取某个 h in Eq with h<sq，令 r_q=3^c+5^a+q^h modq^Kq，其他 rows 用同一公式 modulo p^Kp。以上最小失配仍给 valuation1，全中心分支给 valuation h。这里是重新选择允许的 r，而不是保证任意已经冻结的 residues 都成功。

E1 是来源 B7 D5 的逐坐标推广；原 D5 只需 e=1、head7。[S5]

### Theorem E2 — one global state for all seven roles

给每个 basin 一次性选择上述 a_i。D_i 不交，故每个 original row 被赋值一次。所有 prime-power residue equations 可由 CRT 合成 ONE integer R_global。

a_i 可以不同，但它们是构造各行 residues 的常数，不是分别选七个输入指数，也不是为同一 row 选七份状态。此后对所有 d 都使用同一个 R_global。E1 在每个叶上同时适用，七叶并成整个选定 parity。

所以七个 mandatory rank-3 roles 的 shared-state CSP，在满足条件的实际算术输入上，确有显式共同 witness。这不依赖 pairwise compatibility 推断 global compatibility。

## 5. PAIRWISE COMPATIBILITY MATRIX

下面的 1 表示：在 actual arithmetic basins 存在并满足 §2 条件的假设下，两项**指定 parity/anchor 的 whole-leaf duties**可以由一份共同 CRT state 同时满足。没有声称 terminal primes 已经找到。

|  | 31 | 7 | 19 | 5167 | g1 | g2 | g3 |
|---|---:|---:|---:|---:|---:|---:|---:|
| 31 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 7 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 19 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| 5167 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| g1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| g2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |
| g3 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |

全部 pair 共享的 separator 是 3-primary 投影和可能的 parity；共享 actual prime >3、共享 free odd coordinate >3、跨盆地同一 relay-state 约束均被完整 normal form 排除。盆地内部复用 helper 时，E1 的共同 a_i 把其所有 center 要求同时对齐。

这张矩阵不是完整 two-anchor 结论。后者还有 row3 的 opposite-parity constraints，见 §8。也没有发现一个对全部 admissible exactly-seven 输入都 universally incompatible 的 mandatory pair。

## 6. TWO-ROOT TRACE APPLICATION

来源 D1 的 last-root criterion 是

    exists ONE lower state tau: J_q(D(tau)).

D 是 lower system 的全部共同 escapes 在原始 w_q 上的投影。若 H=Eq intersect {h:0<h<sq, h odd}，则 empty trace 无条件允许；singleton 要 H非空；两个不同 logs 还要 5^a-5^b=±2 modq^min(H)；三个或以上 logs 不可能由一个 actual root rigid-cover。[S3]

它推广到七根时，选择**全体 roots 中最大的 q**，把另外六 roots 和所有 proper regular helpers 都放在同一 lower vector tau；不能把六个 pairwise witnesses 的 tau 拼凑。

在 E5 的完整 canonical construction 中，固定一次这样的 tau。删去 q-row 后，任意 remaining A1 escape 必须同时满足：它属于 q 的指定叶（若 q 为31盆地，也包括另一 parity 的同一3-leaf）；该盆地所有 regular own digits 都是中心。否则其他六盆地、row3，或 E1 的最小失配 helper 已经覆盖。

因此在 q 的**原始 order**上

    D_A1(tau) subset {a_q modw_q}.

odd pooled EITHER trace 只是该集合的子集。故 J_q 必通过，且不必用两点的 ±2 条件：r_q=3+5^a_q+q 已经提供 A1 的真实 valuation1。即使31盆地用于两个 parities，O31 保证原始 w_q 为奇数，仍是同一个 log，而非两点需求。

这证明“前六盆地必迫使最后一根 trace失败”不是这个 conditional arithmetic domain 的普遍定理。若没有 O31，只能先对 selected parity 得到 singleton；不能擅自把它升级到全域。

## 7. HIGHER-ORDER CSP AND ELIMINATION

固定 ONE whole state s_i，定义每个 separator cell 上的实际两锚 mask profile

    A_i(z;s_i) = { (F_i,0,F_i,1)(z,x_i) : x_i ranges over its full private block }.

它是 {0,A0,A1,BOTH} 的非空子集，只有15种单-cell可能值。两个独立 private blocks 的 exact join 为

    A odot B = {a bitwise-OR b : a in A, b in B}.

对每个 z，把七盆地、row3、two-adic row 的 profiles 作 join，再检查该 cell 的 typed demand 对所得每一个 mask 都成立。这保留了“forall private exponents”的量词。

**whole-profile consistency：** 存在量词选择的是一个实际 s_i 产生的整个 z->A_i(z) 函数，不是逐 z 自由挑选15种 masks。DP 的 S_k 保存可实现 whole profiles、原始 state/backpointer 及共享变量一致性；用 odot 更新。canonical K2 构造仅需 z=d mod54，不枚举巨大 product of regular primes。一般 K 情况可以用3-adic prefix signatures压缩，但本报告不声称 profile个数有普遍多项式上界。

### Actual-row Helly failure

取 actual row3，K=2,E={1}，anchor c=0，状态 r3 in {2,5,8}。三个指数 d=0,2,4 的 A0 fatal state sets 是

    {5,8}, {2,5}, {2,8}.

两两相交，三者交为空。这是 actual modular row constraints，不是虚构 Boolean tokens。本轮直接模幂复算了全部集合与交。

本轮还有与 opposite parity 直接相连的版本：anchor c=1，d=3,1,5，得到相同三个允许集合。它们分别代表 odd parity 的 C1(0)、C1(1)、C2(5) 三个 missing cylinders。在 K2 下状态集合对整个相应 cylinder 都适用。

若31盆地存在偶阶节点，则 §8 证明这三个 holes 同时必须交给 row3，于是出现一个**三项 row3 demand 的 minimal unsatisfiable core**。删去任一需求，另两个可由一个实际 row3 state 同时满足。这个 obstruction 条件化于 parity-defective31，不能宣称它对所有 seven-basin arithmetic inputs 都存在。

### Replayed actual 31-row collision

来源 actual fixture 用 P={3,31,20771,40487}，K2,E1，r3=2,r20771=20773,r40487=40493。U=L=40688430，M=1312530。在 d=0 modM 与 d=437511 modM 两个31-fibers中，其余三行分别只覆盖 digit0与digit1，要求 r31 分别在 {2,4} 与 {684,686}，无交。[S3]

本轮重新检查全部961 states、62 actual cells，覆盖 histogram 为

    2 cells:899 states; 60 cells:58 states; 61 cells:4 states.

这说明真实状态冲突并非虚构，但该例让两根共用31，违反 exactly-seven 的 basin disjointness；其 roots 的绝对 closures 也不是所需 pure3族。不能把它直接升格成 N>=8。

## 8. TWO-ANCHOR TYPED DEMANDS AND PARITY PERSISTENCE

类型的语义始终为

    A0=m0; A1=m1; EITHER=m0 OR m1;
    BOTH=m0 AND m1; TRUE=true; FALSE=false.

特别地，profile {A0,A1} 通过 EITHER，不通过 BOTH。one-anchor、pooled OR、simultaneous C=1 三者不能互换。[S2,S3]

### Theorem E3 — parity-deletion / private-fiber persistence

冻结完整输入的 c* 和 row3-inactive parity b。每个盆地在所有 >3 private coordinates 饱和后留下它的一个实际3-leaf L_i。翻转到 b'=1-b，并用 CRT 识别两 parity 上相同的 odd-primary coordinates。

如果 D_i 的所有 w_x 都为奇数，所有这些行的完整 periods 都为奇数，逐点函数不变，其 saturated profile 仍为 L_i。

如果有某个 x in D_i 的 w_x 为偶数，则该行在 c* 的唯一 modulo-x logarithm guard只允许 b，故在 b' 全部失活。此时整个盆地没有任何 whole-private-fiber coverage，profile为空。

**第二项的直接证明。** 若失活行就是 root，则只剩 regular rows；按素数递增选各自 safe center 即得到 escape。若它是 proper helper p0，从它沿实际 order edges 反向选一条路径

    p0 < p1 < ... < pt=q,   pj divides w_(p(j+1)).

p0 已失活，故其 own coordinate可自由选；令它不等于 p1 的固定 lower-log p0-digit，便使 p1 在 c* 失活。现在 p1 的 own coordinate也可自由选，使 p2 失活，直至 root 的 lower guard被破坏。所有 off-path regular rows 按素数递增选 safe centers；higher own coordinates 不改变已经安排好的 lower-log mismatch。实际 prime labels严格递增，CRT variables私有，所以过程终止且所有行同时安全。这个构造可在任何固定3-primary z上执行。因此不是“覆盖少一些”，而是没有一个完整 private fiber 能再由该盆地覆盖。证毕。

盆地之外的 regular rows同样可在该 core escape 上递增 safe-extension，故不能修复这个 boundary defect。必要性始终保留原始 U/L。[S2,S4]

### Theorem E4 — 必需的全奇阶 31-basin

在实际 frontiers 中，把31、7的两个 depth1叶分别记 A、B，剩余首层分支记 C。5167 的 depth2叶位于 C 内。由 w7=6、w5167=18 与 E3，翻转 parity 后，7盆地和5167盆地的 saturated profiles 都为空。

不同盆地的 private coordinates 不交。固定一个 separator z 时，若每个盆地都存在 private escape，就能通过 CRT 同时选择这些 escapes。所以在失去的 B 以及 C 内的5167二级叶上，只有 row3 能提供 complete private-fiber cover。其他盆地不能通过各自不完整的覆盖拼出一个全 private-product 覆盖。

regular row3 在 active parity 上具有唯一3-adic动态中心 alpha，其截断 valuation为

    min(K3, 1+v3(d-alpha)),

其中 local-zero sentinel K3仍不接受。

要覆盖整个首层叶 B，必须1 in E3，且 alpha mod3不在B。要覆盖 C 内整个指定二级叶，alpha mod3也不能在C：若首位在C，该二级叶不是包含安全中心，就是具有偶数 valuation2（截断时仍安全），不可能整体 fatal。K3=2时整个中心首层叶已是local-zero，结论相同。

因此

    1 in E3,
    alpha mod3 = A = the 31 leaf.

在该安全中心的3-adic投影上，row3不覆盖，其他六盆地的 profiles 均不在A。two-adic boundary lemma保证在 b'仍有安全2-adic prefix，与该3-adic选择可CRT拼接。故31盆地必须在 b'有whole-private-fiber coverage。E3给出必要条件

    O31: 2 does not divide ord_x(5) for EVERY x in D(q_31).

注意约束包括 root 及全部 proper descendants，不是只检查 head31，也不是只检查 root 的 order。[S1 boundary and normal form]

等价地，若31盆地有任何偶阶节点，row3必须同时覆盖A、B和C内的5167叶，正是 §7 的三项 incompatible demand（任意 K 的证明见上）。这是被排除的一个明确子类，不是排除了所有 exactly-seven。

### Theorem E5 — arbitrary branching 下的完整 simultaneous C=1

现在给定七个满足 §2 算术条件的实际 finite basins，并假设 O31。对 §3 的共同布局，在 c1、even parity 上使用 E1。所有 odd rows取K2,E1。

31盆地所有orders为奇数，所以它对整个 d=0 mod3 的覆盖同时适用于两个parities。另设置

    r3=2 mod9,
    r2=1 mod4, K2=2.

在 c1：even d由七盆地覆盖；odd d且3不整除d由row3覆盖；odd d且3整除d由31盆地覆盖。故 odd rows alone 在 anchor1 覆盖每一个d。

在 c0：5^d=1 mod4，所以 local value为1-1-1=3 mod4，two-adic sums-of-two-squares obstruction始终成立。于是两个anchors逐一都被排除，是 BOTH，不是 EITHER。

所有row moduli相异，取同一个CRT residue

    R_global mod M,
    M=4*9*product_(p in union_i D_i) p^2.

所有proper regular p>3都出现在上游order中，且depth3 heads提供3^3，head7/5167提供parity。因此该canonical完整core的真实induced ambient为

    U=L=54*product_(p in union_i R_i) p.

这是actual-input条件构造的公式；当前未给出数值M、R_global、U或L，因为七个nonregular endpoints尚未实例化。对于已冻结而包含额外rows的ledger保留其原U/L，构造在更大的共同period上仍覆盖；不把删行后的period冒充原period。

## 9. RESULTANT CONSTRAINTS

保留来源的 original row、原始 order、original quotient坐标。若同一actual q 被同时要求完成多个 paired rigid positions，来源条件为

    w_q=u*h,
    u divides gcd_j(Y_j-Y_1),
    q divides gcd_j R_h(Y_j),
    R_h(Y)=Res_T(T^h-5^(Yh),(T-2)^h-5^(Yh)).

不得把 contracted 3-adic macro 的 depth当作original h，也不能把互斥OR branches全部做gcd。[S2,S3]

来源 h=67、Y=7,8 的两次原始位置约束给出

    gcd(Phi_67(5), source-resultant-gcd)=432821=269*1609,

剩余素数均1 mod4，不是admitted suppliers。本轮重新做了给定源factorization后的整数gcd与两个因子的素性核验；**没有重新计算那两个巨大的 resultants**。

在E1–E5中，每个root承担自己的一个A1 original log。七个roles不共用q；31跨两个parities时原始w_q为奇数，仍是同一log。盆地内部的branching也由同一个a_i对齐center。因此没有推导出同时mandatory的不同Y1,Y2来触发新的gcd obstruction。额外A0事件即使存在，也不是构造需要满足的新paired义务。

## 10. LITERAL-HEAD MODEL

来源 Order-DAG Theorem12.1 已经证明 literal H0 chains存在时有一个共同CRT state；Phase D明确重建了two-parity、two-anchor与U/L接口。[S1,S6]

H0及其states为

| h | w_h | r_h modh² |
|---:|---:|---:|
|31|3|4|
|7|6|33|
|19|9|237|
|5167|18|26482920|
|271|27|54317|
|4159|27|5094267|
|31051|27|508857581|

每条 literal chain 满足 ord_(p_i)(5)=p_(i-1)，不是2p或一般composite order。31链从head的order3开始，其余orders均为奇prime，所以自动满足O31。故本轮E5覆盖literal模型，也覆盖全部20个depth3 head sets的120个assignments。

本轮小型reference重新核验120*54=6480个conditional separator exponent cases，以及全部表中actualhead residue值。它没有把条件上游chains作为实际rows加入计算。来源目前只有actualregular prefixes，没有七个nonregularterminals；这一状态未改变。

## 11. GENERAL B7 MODEL

源B7以basal gateway {7}定义，不禁止非basal节点有额外直接3-edge。比如regular43有order42，不能因此被排除。B7中所有orders平方自由，properdescendantsregular。[S5]

E1允许这类任意branching，E5还允许其他六盆地也branching；只要31盆地满足O31，即可globalglue。故不是仅允许“任意B7替换一条7链，其余六条仍必须是链”。后者原来已有B7 D5；本轮明确推广了其余六个盆地。

本轮actualregular skeleton参考：

| R | a | L | 指定guard cells | regular覆盖 | 剩余hole |
|---|---:|---:|---:|---:|---:|
|{7,43}|1204|1806|301|300|1204|
|{7,43,127}|152908|229362|38227|38226|152908|

第二项有实际branching，即43与127同时在7之上；两者exactorder42。其states为r7=33、r43=1428、r127=11159。它们仅验证了regular部分的least-mismatchmechanism；**没有提供覆盖最后hole的actualnonregularq**，不应列为完整certificate。

另外，actualregular skeleton {31,1303}，orders3与62，在r31=r1303=4下，选定even C1(0)只留1个中心hole；oppositeodd C1(0)留1303个holes。它说明“head31的order是奇数”不足以保证整个盆地跨parity持久。此例也没有虚构nonregularterminal。

## 12. EXACT REFERENCE RESULTS AND AUDIT

`python3 reference.py --output RESULTS.json` 使用Python标准库，八组checks全部PASS：

1. 16个actualprimes的complete trial-division素性、exactorder与lifting exponent；10个heads及3、43、127、1303、20771、40487。
2. 七叶前沿、120个headassignments、6480个conditionalexponentcases、literalheadstates。
3. 两个B7regularskeleton以及31even-relayskeleton。
4. actual31sharedstatecollision的961states*62cells。
5. actualrow3三项MUS，含c1opposite-parity版本。
6. K3=2..5的row3必要条件穷举，分别检验6、18、162、486个state/E组合；通过者均接受1、中心首位为31branch。
7. 3375个typedprofilejoin结合律cases，以及54个canonicalBOTHseparatorcells。后者用保证覆盖的A1投影/lower-envelope masks做充分性检查，不宣称已经计算未知roots的全部actualtwo-anchorprofiles；额外A0覆盖仅被忽略，并未被强行suppression。
8. 源resultantfactorization后的integergcdgate。

这些checks支持公式、典型状态与边界语义；任意branching、任意有限K的结论来自证明，不是把有限测试外推。未执行repository-native replay，未宣称fullyindependent复算过全部sourcecertificates。

主要adversarial检查：

- 只允许ONE actualrowstate；center/log不能独立选择。
- 分清a_i constructionconstants与universalexponentd。
- 全部oddordersupport>3必须真实、封闭、私有；freecoordinates不得丢失。
- E1保留3^2、3^3，不把所有orders误当平方自由。
- E3包括even-orderroot和even-orderproperhelper两种失活情形。
- E4在K3=2与higherK下都保留local-zero安全点。
- 外部regularrows不能修补closedboundaryescape，但任意typedCSP中不能无条件删掉它们。
- 原始roottrace用w_q，不用contractedleafmodulus。
- 正面conditionaltheorem不等于actualterminalexistence，更不等于unboundedc的A303656结论。

## 13. VERDICTS

```text
GLOBAL STATE INCOMPATIBILITY?
  NOT PROVED universally for exactly-seven.
  PROVED for the parity-defective 31-basin subclass (within source normal form).

GLOBAL STATE AUTOMATIC COMPATIBILITY?
  PROVED for all seven mandatory selected-parity rank-3 roles.
  PROVED for full simultaneous C=1 under O31.
  No assertion that arbitrary frozen states work.
  No unqualified use of vertex-disjointness alone for arbitrary typed ledgers.

LITERAL-HEAD MODEL?
  CONDITIONALLY COMPATIBLE whenever its actual terminal chains exist.
  This was already supported by source Theorem12.1; independently reconstructed here.

GENERAL B7 MODEL?
  Arbitrary branching admitted by E1/E5;
  six other basins may also branch, with O31 required for full C=1.

ACTUAL SEVEN-ROOT LEDGER FOUND?
  NO.

EXACTLY-SEVEN KILLED?
  NO.

N>=8?
  NO.
```

成功层级：确认C；给出normal-form/O31作用域内的D型推广，以及一个新的opposite-parity必要条件。不宣称A或无条件B。

## 14. NEXT SINGLE TARGET

**研究 all-odd 31-basin 的算术空性/存在性，而不是扩大七根globalstateSAT。**

定义候选 B31^odd：qnonregular、T(q)={3}、basal gateway={31}、所有properdescendantsactualregular；每个x inD(q)满足

    ord_x(5)=3^epsilon * product_(p in S_x) p,
    epsilon in {0,1}, S_x subset of smaller actual regular descendants >3.

不允许factor2或任何平方orderfactor。E4表明每个completeexactly-seven都必须暴露这样一根。最小高于31的actualdescendant，其order只能从{31,93}开始；这给一个theorem-gated有限入口，而不是按q<=B泛扫。

若能证明 B31^odd为空，才可结合E4推出N>=8。若得到actualmember，则与其他六盆地的兼容性已有E5处理，剩下的是那些actualbasins的算术存在性，而不是重新逐fiber选state。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
