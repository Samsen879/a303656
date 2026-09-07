# A303656 C=1 GLOBAL SHARED-STATE REALIZABILITY
## TYPED POOLED EITHER RECURSION — TARGETED PHASE C

## 本轮结论

本轮没有普遍消去 pooled 分支，但取得三个可精确定义的进展。

**第一，Gate A 得到必要充分判据。** 对恰有一个 nonregular prime 的实际有限 ledger，固定全部 precisions 与 accepted sets，只允许各行的 shared residue 在完整 residue ring 中变化，完整 odd pooled cover 的存在性，等价于一个递归 squarefree regular order-closure 条件，加上明确的 accepted-valuation 条件。这个判据包含 P5，而不是排除 P5。

**第二，构造了 actual arithmetic 的整型／分数 gap。** 五个实际素数给出的真实 coarse domain 上，5,859 个全局整型状态全部失败，最佳覆盖只有 1,300/1,302；同一配置模型却存在对每个 cell 都提供 830/651 覆盖容量的分数解。自然 incidence matrix 也有 determinant -2 的 actual minor。

**第三，得到原始 rigid row 的 multi-fiber order/resultant 判据。** 同一 row 的跨 fiber 复用，首先要求 lower order 整除各 ordinary lower representatives 的差值 gcd。通过这一检验后，同一 original depth 的多个 resultants 模 q 重复；不能把它们当作独立限制。结合 cyclotomic square-divisibility，可以得到一个作用域明确的有限算术筛选。

这些是本轮新推导和 reference computation，不是已获独立作者审阅或 proof-assistant 形式化的 repository theorem record。未主张文献优先权，未写入 GitHub。更展开的证明记录见 PROOF_DETAILS.md；本文件包含结论、关键证明与全部要求的报告栏目。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 71b8d428b32724c37e593bcfd9d5f06a42e72d21
main tree: 5609e47eed0c058c190ef59c61644e2fd4b8fad6
Phase B: #17 / #20 / #18 / #19 均 merged
结束前复读 main: 未变化
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

已通过固定 SHA 的 connector reads 通读六个指定目录的主 REPORT.md，并阅读 pooled DEFINITIONS.md 与 THEOREM_AUDIT.md。没有把这说成逐一阅读或重放目录内全部 generated catalogs、历史代码与辅助文件。具体 source paths、Git blob identities、merged 状态和阅读边界见 SOURCE_BINDING.json。

本地没有 repository checkout；没有执行 repository-native tests。这里的程序是独立新写的 standalone reference implementation。

现有 seven-nonregular theorem 已经排除至多六个 nonregular primes 的 simultaneous BOTH certificate；本轮不将其对一行／两行的推论重命名为新结果。本轮 Gate A 分类的是更弱但真实存在量词问题的 whole odd EITHER cover。[S6]

## 2. GLOBAL QUANTIFIER MODEL

实际 odd row 由不同的 q=3 mod4 指定，q!=5。每行选定 K_q>=2、非空 positive odd accepted set E_q⊂[1,K_q-1]，以及两个 anchors 共用的 r_q mod q^K_q。记

\[
V_{q,c}(d)=r_q-3^c-5^d,\quad
w_q=\operatorname{ord}_q(5),\quad
s_q=v_q(5^{w_q}-1),
\]
\[
a_q=\max(0,K_q-s_q),\quad
U=\operatorname{lcm}(t_2,\{w_q\}),\quad
L=\operatorname{lcm}(t_2,\{w_qq^{a_q}\}).
\]

local zero 永不 accepted。有限 state-family 搜索可在支持全部候选 full periods 的共同有限域 Ω 上进行；使用 coarse U 时，必须确认它由保留的 actual rows 合法诱导。

正确问题是

\[
\boxed{\exists s\in\prod_q\mathcal S_q\quad\forall d\in\Omega:
D_d(F_0(d;s),F_1(d;s))=1.}
\]

不是 forall d exists s_d。坐标消元、分支展开与 provenance reuse 都不得重新选择 r_q。

若 K、E 仍在无界变化，不能未经证明就声称已有一个有限 ILP。有限整型模型需要 frozen finite families，或已证明充分的 finite incidence quotient；后面的无界定理使用解析证明，不依赖枚举全部 primes 或 precisions。

## 3. SIX-STATE AUDIT

| Demand | 对 coverage bits C0,C1 的要求 |
|---|---|
| FALSE | 永假 |
| A0 | C0 |
| A1 | C1 |
| EITHER | C0 OR C1 |
| BOTH | C0 AND C1 |
| TRUE | 永真 |

固定全局状态后，top word 为 T(z)。令 S_c=∀z T_c(z)，S_or=∀z(T0(z)∨T1(z))。P1 的精确公式仍是

\[
(\mathcal RD)(C)=\bigwedge_zD(C\cup T(z)),
\]
\[
\mathcal R(\mathrm{EITHER})=C_0\vee C_1\vee S_{or},
\qquad
\mathcal R(\mathrm{BOTH})=(C_0\vee S_0)\wedge(C_1\vee S_1).
\]

SPLIT 给 S_or=true、S0=S1=false。因此 EITHER 可成为 TRUE，BOTH 仍是 BOTH。P2 的不同 cover clauses 保留为 OR；P3 的原始 colored frontier 保留 actual row/state tags。[S5,S7]

本轮检查了长度 1..4 的全部 340 个非空 top words，以及 8,160 个 demand/lower-bit truth cells；六态闭合与 EITHER/BOTH 公式均无违例。actual 67/20771 SPLIT 保留，没有被当成错误而删除，也没有被升级为 whole-domain completeness。

## 4. ROW STATE FAMILY

每个 state 至少保存

```text
(q,K,E,r mod q^K,w,s,
 anchor0 normal form, anchor1 normal form,
 original ranks/depths, full logarithms,
 paired positions, lower guards, local-zero information)
```

这些 normal-form fields 由 (q,K,E,r) 推导，不是可以独立拼接的参数。

对 t_c=r-3^c，若 t_c modq 不在 <5> 中，该侧 inactive；否则有唯一 b_c modw。小于 min(s,K) 的 valuation 在整个 b_c guard 上恒定，只有 accepted h<s 才给 rigid fatal component。K>s 的 lifted subgroup 分支给 dynamic center 和 parity shells。一个 q 可以一侧 dynamic、另一侧 rigid。[S5]

\[
V_{q,0}(d)-V_{q,1}(d)=2
\]

保证同一 lower prefix 上至多一个 anchor 对该 q 正整除。regular row 的 s=1，没有 rigid fatal component，且 active 时总有 safe center lift。

对 q=20771、40487，在 K=2,E={1} 下，本轮按 mod-q base 和至多两个 exceptional lifts 分组，完整描述了所有 q² 个 shared residues 的 fatal-anchor profile。分别 accounting 431,434,441 与 1,639,197,169 个 states；这是结构化全分类，不是逐个循环 q² residues。

## 5. INTEGER CONFIGURATION FORMULATION

对 fixed actual ledger 和 finite legal families，置

\[
x_{q,s}\in\{0,1\},\qquad\sum_{s\in\mathcal S_q}x_{q,s}=1.
\]

令 h_{q,s,c}(d) 为 actual incidence。A_c demand 对应

\[
\sum_{q,s}h_{q,s,c}(d)x_{q,s}\ge1.
\]

EITHER 对 pooled incidence max(h0,h1) 使用一个不等式；BOTH 使用两个分开的 anchor 不等式；TRUE 无约束；FALSE 不可行。对全部 cells 同时施加，得到 exact integer feasibility，而不是逐 fiber 的 state choice。

Macro witness variables 必须受全部 source-state tokens 与 lower guards 约束。同一 q,s 的重复是幂等 reuse；同一 q 的不同 states 不能 conjunction。不同合法 cover witnesses 是 OR alternatives，不能全部 AND。选取 subcover 也不等于压制 selected state 自带的其他 events。[S7]

### C1 — actual fractional/integer gap

取实际 ledger

\[
P=\{3,7,31,43,1303\},\qquad K_q=2,\quad E_q=\{1\}.
\]

对应 exact orders 是 2,6,3,42,62，全部 s=1。故

\[
U=1302=2\cdot3\cdot7\cdot31,
\qquad L=72\,949\,758=1302\cdot43\cdot1303.
\]

43、1303 是真实 regular support rows，其 orders 分别补入 7、31。它们自己的 coordinate depth 为零，coarse fatal masks 为空；固定 r43=r1303=2。不能删掉这两行后仍把 1302 称为 coarse U：仅有 {3,7,31} 时，U=6，full L=1302。

采用下列全局 shared-residue families：

\[
\mathcal S_3=\{2+3k:0\le k<3\},
\]
\[
\mathcal S_7=\{a+7k:a\in\{2,5,6\},0\le k<7\},
\]
\[
\mathcal S_{31}=\{a+31k:a\in\{2,6,26\},0\le k<31\}.
\]

每个 family 内等权分数选择。在每一个 coarse cell，三个 rows 的 fractional pooled incidences 分别是

\[
\frac23,\quad\frac6{21}=\frac27,\quad\frac{30}{93}=\frac{10}{31},
\]

总和恒为

\[
\boxed{\frac{830}{651}>1.}
\]

这些是固定的全局分布，不是每个 cell 单独优化。7-row 的三个 base residues 覆盖三对互补 logarithm guards；31-row 的三个 base residues 对应其三个 anchor-0 logs。在 active base 下，q 个 lifts 中恰一个 local zero，其余有 valuation 1。

然而任何 integral state 都失败。原因是全部 rows regular，可以逐坐标选择 safe centers。精确枚举全部 3*21*93=5,859 个状态，得到：

| common coarse escapes | state vectors |
|---:|---:|
| 2 | 217 |
| 14 | 434 |
| 38 | 868 |
| 62 | 434 |
| 218 | 868 |
| 224 | 868 |
| 248 | 868 |
| 434 | 1302 |

最佳仅覆盖 1,300/1,302。全体 residues=2 时，逃逸为 {0,651}。对每一个状态，另外把最小 coarse escape a 提升为

\[
d\equiv a\pmod{1302},\qquad d\equiv0\pmod{43\cdot1303},
\]

并直接检查五个实际 rows、两个 anchors 的 modular valuations，5,859 个 full escape witnesses 全部通过。没有枚举 72,949,758 个 full cells。

因此，即使该 EITHER 问题对应的所有非负 weighted row-configuration Hall inequalities 都成立，也不保证 integral feasibility：fractional cover 已经保证

\[
\sum_df(d)\le\sum_q\sum_sx_{q,s}\sum_df(d)H_{q,s}(d)
\le\sum_q\max_s\sum_df(d)H_{q,s}(d).
\]

这不是 source 的纯 abstract 两资源例子，而是 actual prime / legal shared residues / genuinely supported U 的反例。它不声称任意加强后的 LP 或 extended formulation 都无用。

### actual non-TU minor

取 q=3 的 r=2,5,8 三列及 d=0,2,4 三行，得到

\[
\begin{pmatrix}0&1&1\\1&1&0\\1&0&1\end{pmatrix},\qquad\det=-2.
\]

自然 original-state incidence matrix 因而并非 totally unimodular。此结论不排除某个更受限 subclass 的特殊 integral formulation。

## 6. CROSS-FIBER COLLISION THEOREM / COUNTEREXAMPLE

### C2 — original rigid multi-use compatibility

固定 actual q，w=u h，h=p^e，p=P+(w)。一个 global state 在每个 anchor 至多有一个 rigid logarithm b_c。因此同一 anchor 在多个原始 fibers 的使用，必须对应相同 b_c modw；要求的 rigid valuations 也必须一致。不能让 q 在一个 fiber 使用 b，再在另一个 fiber 改用 b'。

尤其，同一 q 若须在 ordinary lower representatives Y1,...,Ym 同时供应双边 rigid leaves，必要地

\[
\boxed{Y_i\equiv b_0\equiv b_1\pmod u\quad\forall i.}
\]

通过这个检验后，同一 state 的跨 ambient-fiber reuse 合法，不消耗新 prime。

两个 anchors 的剩余 residue compatibility 仍须通过 source 的 valuation minimum criterion：对指定 rigid h0,h1<s，

\[
\min\{v_q(5^{b_0}-5^{b_1}-2),h_0,h_1\}
\]

至少出现两次，附上合法 clipping 与 zero exclusion。[S2]

### 实际冲突

q=20771，w=10385，h=67，u=155，K=2,E={1}：

| Y | b0 | b1 | r modq² | top positions |
|---:|---:|---:|---:|---|
| 7 | 2177 | 9772 | 16 | (33,57) |
| 8 | 1558 | 10238 | 17555 | (17,54) |

两组都是真实 paired states，两个 valuations 都恰为 1。但没有一个 state 能同时服务这两个 lower classes，因为 7!=8 mod155。

完整 catalog 中 q20771 有 28 个非空 lower classes、33 条 same-lower edges；不同非空 classes 两两不能由这个 q 的一个双边状态同时供应，共 378 对。q40487 有 62 个非空 classes、652 条 edges，对应 1,891 对这类冲突。

这证明了真正的量词 gap；没有证明任意 complete cover 必须把指定的两个 fibers 都分配给该 q。

### 实际合法复用

同一 q20771 的 r=16,b0=2177,b1=9772 同时服务 Y=7 与 Y=162，因为差值为155。加入 actual 67-row 后，ambient lower modulus 是3410，这两个 y 确实不同，但 q 所见的 projection 相同。故“跨 fiber 复用必冲突”或“每次复用支付新 prime”都错误。

### C3 — 多个 exact valuation constraints

对 a_i=3^{c_i}+5^{d_i} modq^K 和 0<h_i<K，置 H=max h_i，选 h_*=H 的 a_*。存在一个 r 同时满足 v_q(r-a_i)=h_i，当且仅当：h_i<H 时 v_q(a_i-a_*)=h_i；h_i=H 时 a_i≡a_* modq^H；这些最高层 constraints 的 forbidden digits

\[
(a_i-a_*)/q^H\pmod q
\]

没有穷尽全部 q 个 digits。

证明：写 r=a_*+q^H t，较低 valuations 被中心差固定，最高层只要求 t 避开各 forbidden digits；更高位任意。

Pairwise compatibility 一般不充分。实际 q=3,K=2,E={1} 在 anchor0 的 d=0,2,4 对应 centers 2,8,5 mod9；每两个需求都有 legal shared residue，三个同时却排除了 r=2 mod3 的全部三个 lifts。这里是一个 original fiber 内的三个 exponent cells，不冒充三个不同 lower guards。

原始 rigid uses 的 h<s 会使相同 anchor／相同 logarithm 的中心在 q^(h+1) 下重合。因此不能靠重复同一个 rigid class 人为制造任意多独立的 forbidden next digits。

## 7. MULTI-FIBER RESULTANT ANALYSIS

保留 source 的原始定义

\[
R_h(Y)=\operatorname{Res}_T(T^h-5^{Yh},(T-2)^h-5^{Yh}),
\]

其中 h=p^e 是 original arithmetic depth，Y 是非负 ordinary integer。odd h 时该整数非零，双边 original rigid use 必须使 q|R_h(Y)。[S4]

### C4 — 先检验 support，再谈 resultant gcd

若同一 q/state 被真实要求同时供应全部 Y_i，则

\[
u\mid G:=\gcd(Y_2-Y_1,\ldots,Y_m-Y_1),
\qquad q\mid\gcd_iR_h(Y_i).
\]

对通过 u|G 的固定 q，w=u h 整除 h(Y_i-Y_1)，所以

\[
5^{Y_ih}\equiv5^{Y_1h}\pmod q.
\]

对应 polynomial pairs 模q相同，resultants 模q也相同。多个 divisibility 条件此时不是新的独立限制。

反过来，q20771 确实整除 R67(7) 与 R67(8)，上表实际 powers 给出 common roots；但两次 paired use 不可能共用一个 state。因此 gcd 可通过，而全局状态仍失败。

### C5 — exact finite-support paired-resource criterion

假设指定的 ordinary Y_i 不全相同，故取绝对 gcd 后 G>0。令 M 为 G 中只含小于 p 的 prime factors 的最大 divisor。若 ambient lower modulus M0 已冻结，先将 G 替换为 gcd(G,M0)，以保持对 supported candidates 的 representative-invariance。

定义

\[
V_{p,e}(M)=\frac{5^{Mp^e}-1}{5^{Mp^{e-1}}-1}
=\prod_{u\mid M}\Phi_{up^e}(5).
\]

对 actual q>p,q=3 mod4，在允许自由选 paired positions、K=2,E={1} 的 potential-resource 层面，存在一个 shared state 同时在全部 Y_i 双边 rigid-active，当且仅当

\[
\boxed{q^2\mid V_{p,e}(M),\qquad q\mid R_{p^e}(Y_1).}
\]

必要性：global state 给 u|M；exact order 与 nonregularity 给 cyclotomic quotient 的 q² divisibility；paired use 给 resultant divisibility。

充分性：q²|V 迫使 w_q=u p^e、u|M、s_q>=2。因 h|w_q|q-1，相关 polynomials 在 F_q 中分裂为 simple roots。q|R 因而给出 a0,a1∈5^Y1<5^u> 且 a0-a1=2。取其 b0,b1，选择共同 r modq² 避开至多两个 zero lifts。所有 Y_i 同余 modu，所以这个状态同时有效。

若 colored top positions 已预先指定，还必须通过 C2 的相同 b_c 检验；上述条件不能代替位置约束。没有证明任意 complete certificate 都强迫某个 q 承担这些指定 uses；OR alternatives 不能全部 conjunction。

### exact checks

| h | gcd(R_h(0),R_h(1),R_h(2)) |
|---:|---:|
| 3 | 56=2³·7 |
| 5 | 3872=2⁵·11² |
| 7 | 3712=2⁷·29 |

九个 resultants 的 Bareiss determinant 与 rational polynomial Euclid 结果完全一致。这里 G=M=1，对应 Phi3(5)=31、Phi5(5)=11·71、Phi7(5)=19531，全部 squarefree，所以这些特定 simultaneous demands 没有 nonregular supplier。

同时验证 q20771 在 Y=7,162 的合法复用及 q²|V_(67,1)(155)，避免错误地把全部多 fiber 使用排除。

这些过滤只作用于 original rows、original h、合法 ordinary representatives。Derived macro 的 current rank 不能代入 R 或 V。

## 8. P5 ADVERSARIAL CHECK

P5 的 hypothesis 是一个 actual nonregular q，加上有限 regular admitted set T，使

\[
U_*=\operatorname{lcm}(w_q,\{w_p:p\in T\})=2^\epsilon M,
\qquad M=\prod_{p\in T}p.
\]

源构造固定 K=2,E={1}，r_p=2、r_q=q+2，得到 whole odd pooled cover；没有给出符合 hypothesis 的实际 q，而且 (c,d)=(1,0) 是 certificate escape。[S5]

它没有逐 fiber 换状态。变化的是“由哪个已经固定的 row/anchor 覆盖 d”。Regular rows 覆盖最小的非零 support coordinate，q 处理 terminal trace M|d；该 trace 恰能压入至多两个 rigid logarithms。

本轮下一节证明其 converse，并推广 accepted-valuation 条件。P5 因此不是新定理的反例，而是充分性方向的标准构造。

## 9. OPPOSITE-ANCHOR OBLIGATIONS

Simultaneous completeness 始终保留

\[
\boxed{\forall y\;(A_0(y)\vee S_0(y))\wedge(A_1(y)\vee S_1(y)).}
\]

A0-only cell 要求 S1；A1-only cell 要求 S0。EITHER 下层覆盖不会删除这些 obligations。[S3,S5]

Typed obligation graph 的资源节点应为 actual state literals，需求节点应为 anchor-tagged unmet cells。只允许 actual incidence 或 type-correct provenance clause 支持需求。若状态二值化且每条 clause 至多两个支持 literals，可用 ¬l1→l2、¬l2→l1；矛盾要求一个 literal 与其 negation 落入同一个 strongly connected component。仅仅看到 alternating anchor colors 不够；一般 clauses 仍需 integer/SAT hypergraph。

P5 在 d=0 留下明确 A1 obligation：regular rows 的 local value 都是-2，q-row 是q-2。重复 SPLIT 不能把这一点变成 TRUE。现有 seven-nonregular theorem 进一步说明，仅增加 regular rows 或重选 one-nonregular ledger 的 states，不能完成 BOTH；任何假设的成功扩充最终都须至少七个 original nonregular primes。[S6]

## 10. SINGLE-NONREGULAR CLASSIFICATION

以下是本轮最主要的无界推导，研究 odd pooled EITHER，不借用 favorable two-adic coverage。

### C6 — 每个 regular-safe prefix 都能延伸

固定全局 regular states。在支持 full row periods 的 CRT 域内，先固定 parity，再递增处理 odd prime coordinates。regular p 的 guards 只依赖较小坐标；至多一个 anchor active。Inactive 时任选；active 时选择 safe center。由此任何已避开先前 regular rows 的 prefix 都能延伸为全体 regular rows 的共同逃逸。高位 regular rows 不能事后删除合法低位 prefix。

### C7 — two-point projection rigidity

令 S 为 fixed regular system 的 full common escape set，W 为 supporting period 的 divisor。若

\[
|\pi_W(S)|\le2,
\]

则每个 odd p|W 都必须满足：p 是系统中的实际 regular admitted row；1∈E_p；v_p(W)=1；并且

\[
|\pi_{w_p}(S)|\le2.
\]

证明如下。如果 p 缺席、在某个 safe prefix inactive，或不接受 valuation1，则全部 p 个 first digits 都有 safe lifts。C6 将它们分别延伸为 S 中的点，产生至少 p>=3 个 W-projections，矛盾。

若 p²|W，active center 第一位之上的 p-1 个非中心 second digits 给 local valuation2，因其为偶数而 safe；中心 second digit 也有 safe center lift。因此至少 p 个不同 p²-projections 可延伸。K=2 时这些 centered first-digit lifts 全部保留 local zero，结论相同。

故所有 earlier-safe prefixes 都必须使 p active；其投影只能落在固定的至多两个 logarithm guards b_p,0、b_p,1，得到最后的 two-point 条件。证明没有使用 fractional Hall 或密度近似。

### C8 — frozen-state terminal-trace criterion

以下先在 full exponent domain 陈述；仓库的 joint reverse CRT 将 whole odd full pooled cover 与 odd coarse pooled cover 对应起来。这里不包含 simultaneous two-adic safety 的额外主张。[S5]

q 为唯一 nonregular row；R_<q 为小于 q 的 regular rows。定义

\[
M_q=\operatorname{lcm}(w_q,\{w_pp^{K_p-1}:p\in R_{<q}\}),
\]
\[
D_q=\pi_{w_q}\{d\bmod M_q:\ R_{<q}\text{ 在两个 anchors 都 safe}\}.
\]

令 B_q 为 q 的 actual rigid fatal components 的 logarithm 集合，至多两个。不能把 dynamic guard 算入 B_q。

则对冻结 states 及任意更大的 regular rows，

\[
\boxed{\mathrm{CompleteOddEITHER}\iff D_q\subseteq B_q.}
\]

若包含关系成立，没有被 lower regular 覆盖的每个 d 都落在 q 的恒定 rigid fatal class 中。

若不成立，选一个 lower regular escape，其 w_q-log 不在 B_q。M_q 的全部 prime coordinates 小于 q；补齐其他低位后，在 q-coordinate 选择 safe dynamic center，或使用已经 nonfatal 的 rigid/inactive 分支。差值2保证此 log 不会同时激活另一 anchor。再用 C6 延伸通过所有更高 regular rows，得到 full common escape。证毕。

### 定义：hereditary regular order closure

从 w_q 的 odd prime factors 出发，递归加入每个已需 p 的 w_p 的 odd prime factors，得到最小集合 T(q)。如果 w_q 及所有这些 w_p 的 odd parts 均 squarefree，而且每个所需 p 都是 actual regular admitted prime，则称 closure gate 通过。

所有 dependencies 都严格下降，所以对一个固定 q，此定义有限且 well founded。也可递归定义 H：p∈H 当且仅当 p regular/admitted、w_p 的 odd part squarefree、且其中每个 odd prime factor 都在 H。

### C9 — 固定 K、E，只搜索 shared residues 的必要充分定理

固定实际 ledger P=R∪{q}，R 全 regular，q 唯一 nonregular；固定全部 K_p 和 E_p。允许各 r_p 在其完整 residue ring 中自由选择。

存在 ONE global shared-residue vector，使全域 odd pooled cover 完整，当且仅当

\[
\boxed{\begin{array}{l}
\text{regular squarefree closure gate 通过，且 }T(q)\subseteq R;\\
1\in E_p\quad\forall p\in T(q);\\
E_q\cap\{h:0<h<s_q,\ h\text{ odd}\}\ne\varnothing.
\end{array}}
\]

**必要性。** C8 使 regular escape trace modulo w_q 至多两点。对 W=w_q 使用 C7，再对每个被迫出现的 w_p 递归使用，得到完整 closure、squarefreeness 与 support rows 的 valuation1 条件。由 C6，trace 非空，故 B_q 非空；q 必须接受某个 rigid odd h<s_q。

**充分性。** 取 T=T(q)、M=∏_{p∈T}p，任选 h∈E_q 且 h<s_q，固定

\[
r_p=2\pmod{p^{K_p}}\quad(p\in T),\qquad
r_q=q^h+2\pmod{q^{K_q}}.
\]

其他 regular rows 的合法 residues 任意，因为添加覆盖不能破坏已有覆盖。对任意非负整数 d：

若存在 p∈T 不整除 d，取最小的 p。w_p 的所有 odd factors 都小于 p、属于 T，因而整除 d。Squarefreeness 使其 odd part 整除 d。若 w_p odd 或 d even，则 w_p|d，regular LTE 给 v_p(1-5^d)=1，于 anchor0 fatal；若 w_p even 且 d odd，则 plus-LTE 给 v_p(1+5^d)=1，于 anchor1 fatal。两者都被 E_p 接受。

若全部 p∈T 都整除 d，则 M|d。因为 h<s_q，ord_(q^(h+1))(5)=w_q；5^d 在相应 parity 上为1或-1 modulo q^(h+1)。于是 anchor0 或 anchor1 的 local value 为 q^h modulo q^(h+1)，具有 exact accepted valuation h。所有 d 都被固定的 row-state 覆盖。证毕。

K=2,h=1 时正是 P5。一般固定 K 下不保证 U=L；证明对所有整数 d 直接成立，没有重命名 period。

### 明确的新 hereditary 排除类

11、19、67 是 regular admitted primes，orders 分别为5、9、22。11 遇到不 admitted 的5；19 遇到 repeated odd depth 3²；67 经11再遇到5。因此三者不在 H。

所以，唯一 nonregular q 的 w_q 一旦被11、19或67整除，就不能只靠任意 additional regular rows 做成 whole odd pooled cover，即使 direct odd order factors 已 squarefree、且已经全部直接获得 dynamic support。

这严格加强了只检查 direct support 的 P4.2。另一方面，3、7、31、43、127、1303 通过 hereditary regular gate；这只是 exact examples，不是新 prime scan，也不是 H 的完整列表。

如果 state families 额外限制可选 residues，C9 的充分性不能直接套用；应回到 C8 和 integral configuration problem。本轮没有给出一个通过 arithmetic closure gate 的 actual nonregular q。

## 11. GATE B / GATE C

### Gate B：two nonregular rows

冻结 regular states，移除已满足的 typed demands。对 residual vertex v，记 C_i(v) 为 q_i 可正确覆盖它的 states。精确可行 state-pair graph 是

\[
\mathcal E=(\mathcal S_{q_1}\times\mathcal S_{q_2})\setminus
\bigcup_v[(\mathcal S_{q_1}\setminus C_1(v))\times(\mathcal S_{q_2}\setminus C_2(v))].
\]

全局可行当且仅当该图非空。BOTH 使用两个 tagged vertices；EITHER 使用一个 pooled vertex；opposite-anchor obligations 保留其标签。这是 forbidden-rectangle CSP，不是两个独立 matching。

C2-C5 可以删除不可兼容 state pairs 或被强迫的 original suppliers。本轮没有得到全体 two-nonregular odd pooled systems 的一般算术分类；simultaneous BOTH 的 two-nonregular 不可能性仍引用已有 seven-prime theorem。

### Gate C：one-nonregular 两行最小 motif 不可延伸

任何仅由一个 regular p 和一个 nonregular q 构成的 two-row ledger，都不可能 whole odd pooled complete。

由 C9，非空 T(q) 必须包含于 {p}。w_p 不能有任何 odd factor，否则需要另一个更小 support prime，故 p=3。Closure squarefree 随即把 w_q 限制为3或6；Phi3(5)=31、Phi6(5)=3·7 的实际 order candidates 都 regular，矛盾。

这解释了为什么两行可以构造 actual original full-fiber SPLIT，却不能仅凭两行延伸到整个 domain。它没有分类所有含多个 nonregular origins 的 minimal frontiers。

## 12. EXACT COMPUTATION

所有代码仅用 Python standard library、整数、modular powers、Fractions 与 exact determinants。每次补充计算前均记录 scope。程序没有扩大 prime scan。

| 检查 | 执行范围 | 结果 |
|---|---|---|
| Integer configuration | 5,859 global states；全部1,302 coarse cells | 0 complete；最多覆盖1,300 |
| Fractional witness | 全部1,302 cells | 每点830/651 |
| Direct full CRT escapes | 每个状态一个，共5,859个 | 五行、两 anchors 全部 safe |
| Six demands | 340 words；8,160 truth cells | 0 violations |
| Paired catalogs | q20771、40487 的完整 w-period | 33／652 same-lower edges |
| Structured q² families | 全部modq bases及exceptional lifts | 全部q² states accounting |
| Exact resultants | h=3,5,7；Y=0,1,2 | Bareiss=Euclid |
| Valuation constraints | 129个mod9 constraint families | 全部与直接求解一致 |
| Regular width | 1,880 states；1,830,700 anchor cells | 2,040 projection checks通过 |
| Accepted-set sensitivity | q3,K4/5；972 states；262,440 anchor cells | 1,296 projection checks通过 |
| Named unit tests | 13 tests | PASS |

另外故意使用不合法 E={1,2} 的负向控制，显示接受 even valuation2 会破坏 width lemma；该控制没有被当作 admitted system。

results.json 是 deterministic exact output。Bareiss/Euclid、两种 paired enumeration 是同一环境中的不同组织方式，不是两个 fully independent software stacks。C6-C9 的无界结论依据解析证明，不依据这些有限枚举。

未实施：逐个 q²-state loop、72-million full-period enumeration、一般 nonregular prime scan、repository-native replay。

## 13. STRONGEST NEW NECESSARY CONDITION

对 one-nonregular pooled survivor，direct squarefree support 不够；其整个递归 odd order closure 必须落在 actual regular admitted rows 中，每个 support row 必须接受 valuation1，终端 q 必须接受 rigid h<s_q。在 residues 不额外受限时，这也是充分条件。

对一般 typed recursion，任何真正被强迫的多次 original paired use，都须先通过共同 lower-order／position constraints；在 G>0 的合法 ordinary representatives 下，再通过 C5 的 finite-support square-divisor 与 paired-resultant conditions。

Actual configuration gap 则证明，即使 primes 与 U 全部真实，也不能以 weighted rowwise Hall 代替 global integral state feasibility。

## 14. CAN THE POOLED BRANCH NOW BE UNIVERSALLY ELIMINATED?

**NO。**

本轮没有证明 universal odd pooled no-go，没有构造 actual complete odd pooled cover，没有构造 simultaneous C=1 certificate，也没有解决 A303656。

若提供一个通过 C9 arithmetic closure gate 的 actual q，显示的固定 residues 就给 whole odd EITHER cover。本轮没有证明这种 q 存在或不存在。多 nonregular systems 仍需进一步 global-state 分析；即使得到完整 EITHER，还须单独完成 BOTH obligations。

## 15. NEXT SINGLE TARGET

**TWO-NONREGULAR TERMINAL-TRACE CLASSIFICATION。**

对 q1<q2，始终冻结 q1 的完整 paired state，分类 lower escapes 在 w_q2 上的 trace，研究它何时能落入 q2 的至多两个 rigid logarithms。目标是从 forbidden-rectangle CSP 提炼结构性 state-collision 定理；不得按 trace cell 重新选择 q1，也不先扩大 prime scan。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

## Sources

全部 paths 固定在第一节 main SHA，blob identities 见 SOURCE_BINDING.json。

[S1] analysis/c1_two_anchor_common_residue_phase_a/REPORT.md

[S2] analysis/c1_prefix_frontier_realizability_phase_a/REPORT.md

[S3] analysis/c1_two_anchor_sync_phase_a/REPORT.md

[S4] analysis/c1_kraft_hall_phase_a/REPORT.md

[S5] analysis/c1_pooled_lower_cover_phase_b/REPORT.md；THEOREM_AUDIT.md

[S6] analysis/c1_unified_endgame_phase_b/REPORT.md

[S7] analysis/c1_pooled_lower_cover_phase_b/DEFINITIONS.md
