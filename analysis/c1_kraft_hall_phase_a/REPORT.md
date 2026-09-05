# A303656 C=1 Arithmetic Kraft–Hall Resource Obstruction — Targeted Phase A

## 0. 结论与范围

**PHASE VERDICT：A. NEW UNIVERSAL RESOURCE OBSTRUCTION，限于本文明确给出的 arithmetic classes。** 同时得到 C 类的非平凡 Hall/Kraft formulation。这里的“new”指相对于本轮核对的 main 中所读 mathematical records 的新增推论，不主张文献优先权。

本轮最主要的无条件结果不是扩展 prime scan，而是：

\[
\boxed{\mathcal R_{3,1}=\mathcal R_{3,2}=\mathcal R_{3,3}=\varnothing}
\]

这一结论没有 prime-size cutoff。于是任意深度的 original actual-prime rigid-only full 3-fiber 至少需要 **81** 个不同 active rigid primes；same-lower simultaneous full 3-fiber 也至少要在一个 anchor 支付这项资源成本。允许 dynamic 3-row 时，一个 anchor 的 full 3-fiber 仍至少需要 **21** 个不同 active rigid primes。

第二个结果是 shared-lower paired-resource 的 exact resultant invariant。它把固定整数 lower representative 和固定 depth 下的“双边可用 primes”限制在一个明确的非零整数的 prime divisors 中。由完整 resultant factorization，得到全零 lower assignment 上

\[
\boxed{\mathcal R^{\mathrm{double}}_{5,1}(0)
=\mathcal R^{\mathrm{double}}_{7,1}(0)=\varnothing.}
\]

这是对所有 primes 的结论，不是对扫描区间的结论。它分别给出 beta-one common full fibers 的 **10-row** 和 **8-row** joint lower bounds。

没有证明对所有 \(\ell\) 都有 global raw Kraft capacity 小于 1；没有证明任意完整 certificate 必然产生 same-lower joint witness；没有把 provenance macros 当作新 actual primes。A303656 未解决。

## 1. LIVE AUTHORITY

本轮通过 GitHub connector 只读核对的 snapshot：

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 0200beede923c56e0284d9555c1dabaf91fa1755
main tree: 23f10c12181c5caa394f7a3fb1acb6e79cc02fe6
```

PR #11、#12、#13 均为 merged，merge chain 为：

```text
#11 e9b537f70fb0196b30f5b476b634299b012c369e
#12 7786a0b356a790623eb0662b64e84b9c6240edde
#13 0200beede923c56e0284d9555c1dabaf91fa1755
```

#12 的 base 是 #11 merge；#13 的 base/当前 main 的第一 parent 是 #12 merge。读取了绑定 SHA 上的 STATUS.md、THEOREM_INDEX.md 和 ROUTE_MAP.md。它们保留：

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

Source basis 与实际 reading/replay 范围在 `SOURCE_READING.md` 中逐项列出。原始研究通过 connector 读取 mathematical texts；本次 integration 已在绑定 main 的独立 worktree 中执行 repository verification、privacy scan 与完整逐文件 checksum。后文 reference programs 是独立新写的 standalone 程序，不导入 repository implementation。

## 2. RESOURCE DEFINITIONS

### 2.1 沿用 main 的 formal class

实际 odd rows 由不同 primes \(q\equiv3\pmod4,\ q\ne5\) 索引。每行选定 \(K_q\ge2\)、两个 anchors \(c=0,1\) 共用的 \(r_q\bmod q^{K_q}\)，及非空 positive odd accepted valuation set \(E_q\subset\{1,\ldots,K_q-1\}\)。局部值为零 modulo \(q^{K_q}\) 时 unresolved，不能作为 accepted event。

令

\[
w_q=\operatorname{ord}_q(5),\quad s_q=v_q(5^{w_q}-1),\quad
U=\operatorname{lcm}(t_2,\{w_q\}),\quad \beta_\ell=v_\ell(U).
\]

在固定 lower CRT assignment 后，assigned coordinate 为 \(\ell=P^+(w_q)\) 的 original rigid event 是空集或一个 cylinder

\[
C_d(t)=\{x\in X:x\equiv t\pmod{\ell^d}\},\quad
X=\mathbb Z/\ell^\beta\mathbb Z,\quad d=v_\ell(w_q).
\]

采用 normalized counting measure \(\mu(C_d)=\ell^{-d}\)。唯一可能的 dynamic row 是 prime \(\ell\) 本身；它只能接受 \(s_\ell+j\) 为奇数的 shells，并排除自己的 unresolved center。

### 2.2 三种不同的 pool

**Raw potential resource pool** 是

\[
\mathcal R_{\ell,d}=\{q\text{ prime}:q\equiv3(4),q\ne5,
 s_q\ge2,P^+(w_q)=\ell,v_\ell(w_q)=d\}.
\]

它表示有可能用来建造一个 rigid leaf 的 actual prime，不表示该 prime 在某个已固定 residue system 中活跃。

**Support pool** 是

\[
\mathcal S_{\ell,\beta}=\{q\text{ admitted}:v_\ell(w_q)=\beta\}.
\]

这里不要求 nonregular，也不要求 \(P^+(w_q)=\ell\)。Regular support row 能增大 ambient depth，却不能被计作 active rigid leaf。

**Active pool** 必须包含 frozen system 参数。固定 \(\mathscr A=(P,K,r,E,U)\)、anchor \(c\)、lower assignment \(y\)。写 \(w_q=u_q\ell^d\)。定义

\[
\mathcal R^{\mathrm{act}}_{\ell,d}(\mathscr A;y,c)
\]

为 \(P\cap\mathcal R_{\ell,d}\) 中满足以下条件的 primes：该行在 anchor \(c\) 确有 original rigid fatal class \(b_{q,c}\bmod w_q\)，对应 accepted odd valuation \(h\in E_q\) 且 \(h<s_q\)，并且 \(b_{q,c}\equiv y\pmod{u_q}\)。其 top cylinder 为 \(C_d(b_{q,c}\bmod\ell^d)\)。不存在 logarithm、lower guard 不匹配、valuation 不在 E 中或 local zero，都不能计为 active。

对 externally frozen U 的候选资源，还必须要求 \(w_q\mid U\)。否则它是可能扩充 ambient system 的资源，而不是原坐标系中随时可用的资源。

### 2.3 量词与 main 的边界

PR #12 的 one-anchor construction 允许先选 actual resources/support，让它们诱导最终 U，再固定/兼容扩展 lower point，并选择各行 residue。它不保证 arbitrary resources 保持一个外部冻结的 U 不变。

PR #13 的 derived provenance macro 即使在下一层表现为 rigid cylinder，也不是新 actual prime。以下 actual-prime resource 结论只适用于 original rows。对其他 lower fibers 的 branch-local row reuse 不消耗一个全局不可复用 token。

## 3. KRAFT THEOREM

### KH-1 — Active Kraft necessity

**Classification: UNCONDITIONAL THEOREM.**

若 fixed \((\mathscr A,y,c,\ell,\beta)\) 的 original rigid events 覆盖 X，则

\[
\boxed{\sum_{d=1}^{\beta}
\frac{|\mathcal R^{\mathrm{act}}_{\ell,d}(\mathscr A;y,c)|}{\ell^d}\ge1.}
\]

**Proof.** 从有限覆盖中删去 redundant events，得到 irredundant subcover。两个相交的 ell-adic cylinders 必然嵌套，因此 irredundancy 使这些 cylinders 两两不相交。覆盖 X 意味着它们构成 complete prefix frontier，其 depth profile 满足

\[
\sum_{d=1}^{\beta}n_d\ell^{-d}=1.
\]

一个 actual row 在 fixed anchor/lower point 至多给出一个 cylinder，故 frontier leaves 分 depth 单射到 active primes：\(n_d\le|\mathcal R^{act}_{\ell,d}|\)。相加得证。这里删除的是 fixed ambient fiber 中的 subcover event，不声称删除 prime 后 U 不变。□

KH-1 本身是对 source Kraft equality 和 per-depth resource injection 的系统化，而非本轮最主要 arithmetic novelty。

### KH-2 — 必须修正的 branchwise inequality

**Classification: UNCONDITIONAL THEOREM；不含 ancestor proviso 的 inside-only 公式作为一般 prefix-tree 命题是 FAILED CONJECTURE。以下 abstract counterexample 不被升级为 actual rigid-prime counterexample。**

对任意 cylinder B，普遍有效的是

\[
\boxed{\mu(B)\le\sum_{q\in\mathcal R^{act}}\mu(B\cap C_q).}\tag{3.1}
\]

Proof 是对 B 上的覆盖指示函数积分。

只有在没有可用的 strict ancestor cylinder 覆盖 B 时，才能直接写成

\[
\sum_{q:C_q\subseteq B}\ell^{-d(q)}\ge\mu(B).
\]

反例：\(\ell=3,\beta=2\)，用三个 depth-one cylinders 覆盖 X。取一个 depth-two cylinder B。没有 selected leaf 落在 B 内，但 B 被自己的 depth-one ancestor 覆盖。这个反例属于 abstract geometry；它不声称三个 actual depth-one resources 在 coordinate 3 存在。

对任意 antichain \(\{B_i\}\)，令 \(D=\bigsqcup_i B_i\)，同样有 \(\mu(D)\le\sum_q\mu(D\cap C_q)\)。允许一行选多个可能位置时，必须对一行的 options 取 **max**，不能把所有 options 的质量相加。

### KH-3 — Fixed-position exact tree criterion

**Classification: UNCONDITIONAL THEOREM.**

对固定 actual cylinders，自 tree root 递归：如果 node v 本身就是一个 active cylinder，则 \(V(v)=\mu(v)\)；否则 \(V(v)=\sum_{w\text{ child of }v}V(w)\)，未覆盖 terminal 的值为 0。遇到已选 ancestor 时不再递归计其 descendants。由对子树的归纳，V(v) 正是该子树中 union 的 measure。因此 full coverage 等价于 \(V(root)=1\)。这个 criterion 保留 position；global mass 超过 1 不能让质量跨越一个空 branch。

## 4. HALL/MATCHING FORMULATION

### 4.1 一个 anchor 的 prescribed frontier

左侧为给定 frontier 的确切 leaves；右侧为不同 actual primes。边表示该 q 在所有已固定的 lower/residue/ambient 约束下，可以实现那个 **exact cylinder**。若各行的允许选择独立，则该 frontier 的 row assignment 存在，当且仅当

\[
|N(A)|\ge|A|\quad\text{for every leaf subset }A.
\]

这是 ordinary Hall theorem。必要性来自 injection；充分性可由 maximal matching 的 alternating-path argument 证明：若有 unmatched left vertex，搜寻所有 alternating reachable vertices；没有 augmenting path 时，这些 left vertices 的邻居数严格小于其个数，违背 Hall。

Depth-only inventory graph 把同 depth 的所有位置视为相邻；position-sensitive graph 不作这种忘却；shared-residue two-anchor realization 一般不再是这个普通 graph。

### 4.2 一个不应反驳的正确 converse

**Classification: UNCONDITIONAL THEOREM，受 one-anchor free-residue / compatible final-ambient scope 限定。**

固定有限 beta，令 \(N_d\) 为可自由分配位置的不同资源数。假定 main 的 ambient-support gate 已通过。在 one-anchor 自由选择 residues 的量词下，

\[
\sum_{d=1}^{\beta}N_d\ell^{-d}\ge1
\]

不仅必要，而且足以实现**某个** rigid-only complete frontier。

**Proof.** 令 \(h_0=1\)，递归选择

\[
a_d=\min(N_d,\ell h_{d-1}),\qquad h_d=\ell h_{d-1}-a_d.
\]

在 depth d 的 pending nodes 中选 a_d 个作为 leaves，其余向下展开。若最终 \(h_\beta>0\)，则此前没有任何一步清空 pending nodes，所以每步 \(a_d=N_d\)，从而总 capacity 为 \(1-h_\beta/\ell^\beta<1\)，矛盾。故得到 exact Kraft profile。再对每个 leaf 采用 PR #12 的 CRT/residue construction。□

因此不能笼统宣称“raw capacity sufficient”总是错误。它对有限深度、某个 frontier、自由 one-anchor positions 是真的；对 prescribed frontier、frozen positions、shared residues 则不是这个 theorem。无限 depth 也须另论：每层 \(N_d=\ell-1\) 的无限 Kraft sum 为 1，但没有 finite subfrontier 达到 1。

### 4.3 两 anchors 必须使用 configurations

每个 q 具有一个 exact finite configuration family \(\mathcal F_q(y)\)。成员是由同一 residue/precision/valuation choice 产生的完整 pair \((C_{q,0},C_{q,1})\)，允许一侧或两侧空，但不允许把两侧自由拼接。若行参数已经冻结，这个 family 只有一个实际 configuration。

对 prescribed leaves，可写 integer configuration feasibility：每个 q 最多选择一个 configuration；每个要求的 leaf 由正确 cylinder 覆盖；one q 在同一 anchor 不能供应两个不同 leaves。若目标要求 exact event family 而不只是某个 subcover，configuration 还必须保存所有额外 events 与 one-sided suppression constraints。

对 residual demands \(D_c\) 和非负权函数 \(f_c\)，必要条件为

\[
\boxed{
\sum_c\int_{D_c}f_c\,d\mu
\le\sum_q\max_{(C_0,C_1)\in\mathcal F_q(y)}
\sum_c\int_{D_c\cap C_c}f_c\,d\mu.}\tag{4.1}
\]

先删除已经由 dynamic event 覆盖的 demands，再应用式 (4.1)。任取一个实际可行选择，对其覆盖指示函数积分并逐 q 上界为 max，便得证明。Antichain / branch demands 是 f 取相应 indicator 的特例。

这是一组 necessary inequalities，不等于 integral hypergraph sufficiency。抽象反例：Q1 允许 pairs (a,u),(b,v)，Q2 允许 (a,v),(b,u)。每侧各自有 perfect matching，但从每个 Q 选一条 pair 不可能覆盖 a,b,u,v；每条 option 赋 1/2 的 fractional solution 却完全覆盖。这个 counterexample 不是 actual-prime construction，不能据此宣布存在 arithmetic obstruction。

## 5. ARITHMETIC RESTRICTIONS

以下都是由 formal class 直接推导的 **UNCONDITIONAL THEOREMS**。

### 5.1 Order、congruence 和 Wieferich

若 \(q\in\mathcal R_{\ell,d}\)，则

\[
v_2(q-1)=1,\quad v_2(w_q)\le1,\quad
w_q=u_q\ell^d\mid q-1,\quad P^+(u_q)<\ell,
\]

\[
q\equiv1+2\ell^d\pmod{4\ell^d},\qquad q\ge2\ell^d+1.
\]

因为 \((q-1)/\ell^d\equiv2\pmod4\)，得到该 congruence。

令 \(k=(q-1)/w_q\)，则 \(q\nmid k\)。LTE 给出

\[
v_q(5^{q-1}-1)=v_q(5^{w_q}-1)=s_q.
\]

所以 nonregularity 等价于 base-5 Wieferich condition。由于 q 不整除 w_q，q 作为 primitive order factor 只出现在 \(\Phi_{w_q}(5)\) 中，且

\[
v_q\Phi_{w_q}(5)=s_q\ge2.
\]

### 5.2 Quadratic / higher-residue constraints

因为 \(q-1\) 只有一个 2-factor，w_q 为奇数当且仅当 \((5/q)=1\)。由 quadratic reciprocity，结合 q≡3 mod4：

\[
\begin{array}{c|c}
w_q\text{ odd}&q\equiv11,19\pmod{20}\\
w_q\text{ even}&q\equiv3,7\pmod{20}.
\end{array}
\]

对 \(r^t\Vert q-1\)，设 \(a=v_r(w_q)\)。在 cyclic group \(\mathbb F_q^\times\) 中，5 是 \(r^j\)-th power 当且仅当 \(a\le t-j\)，其中 \(0\le j\le t\)。特别地，r>ell 时 5 的 order 不含 r；r=ell 时，其 r-primary order 精确为 ell^d。

不能把 \(v_\ell(w_q)=d\) 偷换成 \(v_\ell(q-1)=d\)，所以不能无证明地排除 q≡1 modulo ell^(d+1)。上述条件只给 q mod8∈{3,7}；本轮 actual nonregular panel 中 20771 与 40487 分别落在两个 classes，故不能全局删去其一。

不同 (ell,d) 的 raw rigid-resource sets 两两不交，但同一个 q 的 order 可以给多个其他 coordinates 提供 support；同一个 row 在不同 lower branches 也可复用。

### KH-4 — Finite-support cyclotomic invariant

固定正整数 M，所有 prime factors 都小于 ell。限制 lower order part \(u_q\mid M\)。定义

\[
V_{\ell,d}(M)
=\frac{5^{M\ell^d}-1}{5^{M\ell^{d-1}}-1}
=\prod_{u\mid M}\Phi_{\ell^d u}(5).
\]

则有 exact identity

\[
\boxed{\mathcal R_{\ell,d}^{[M]}
=\{q>\ell:q\text{ prime},q\equiv3(4),q\ne5,
q^2\mid V_{\ell,d}(M)\}.}\tag{5.1}
\]

**Proof.** 令 A=5^(M ell^(d−1))。若 q>ell 且 q|V，则 A 不能为 1 modulo q，否则 V≡ell≠0。由 A^ell≡1，得到 5 的 order 整除 M ell^d 而不整除 M ell^(d−1)，即 exact ell-depth 为 d，lower part 整除 M。又 q 不整除 M ell^d，LTE 显示 numerator 的 q-valuation 正好是 s_q，denominator 的 q-valuation 为 0。因此 v_q(V)=s_q。反向相同。□

式 (5.1) 是固定 support 的 finite exact invariant。若 V 在所有 admitted prime factors 处没有 square factor，则没有 rigid resource。不需要 q_max，但 factoring V 可能很难；此 theorem 不暗示所有不受 support 限制的 raw pools 都有限。

### 5.3 一个较弱但无条件的 counting bound

设 k 为小于 ell 的 odd primes 个数，固定 ell,d。Possible orders m≤X 至多为

\[
2\prod_{3\le p<\ell\atop p\text{ prime}}
\left(1+\left\lfloor\frac{\log X}{\log p}\right\rfloor\right).
\]

对一个 exact order m，所有不同 nonregular q 的 q² 之积整除 5^m−1，而每个 q≥m+1；同时 q≡1 modm。因此该 order 的 q≤X 资源数至多

\[
\min\left(\frac{m\log5}{2\log(m+1)},\frac{X-1}{m}\right)
\le\sqrt X\quad(m\ge3).
\]

相加得到

\[
\#\{q\le X:q\in\mathcal R_{\ell,d}\}
=O_{\ell,d}\bigl(\sqrt X(\log X)^k\bigr).
\]

Partial summation 还给出该 fixed class 的 \(\sum_q1/q\) 收敛。但这不控制其 Kraft capacity：该 class 中每个 q 消耗的是固定质量 ell^(-d)，不是 1/q。即使上述 reciprocal sum 收敛，prime 个数仍可能无限。这是 density 与 resource count 不能互换的具体例子。

## 6. UNCONDITIONAL RESULTS：coordinate 3 的 arithmetic zero

### KH-5 — 无 q 上界的三个 depth exclusions

对于 q≡3 mod4，v2(w_q)≤1。因此 \(P^+(w_q)=3\)、\(v_3(w_q)=d\) 强制

\[
w_q=3^d\quad\text{or}\quad w_q=2\cdot3^d.
\]

以下六个完整 factor identities 已做 exact product、trial-division primality、exact order 和 lifting verification：

| m | Phi_m(5) 的完整分解 |
|---:|---|
| 3 | 31 |
| 6 | 3·7 |
| 9 | 19·829 |
| 18 | 3·5167 |
| 27 | 109·271·4159·31051 |
| 54 | 3·163·487·16018507 |

它们都是 squarefree。任何对应 actual rigid q 都必须 q²|Phi_w(5)，所以

\[
\mathcal R_{3,d}=\varnothing\qquad(d=1,2,3).
\]

注意 factor 3 出现在若干值中，却只有 order 2，不是 coordinate-3 resource。完整 admitted order-signature primes 是

```text
d=1: 7, 31
d=2: 19, 5167
d=3: 163, 271, 487, 4159, 31051, 16018507
```

全部 regular。最后一个 prime 大于旧 scan 的 10^7，故本结论不能被描述成“再次在旧范围找不到”。Completeness 来自 finite order classification，不来自 prime-size exhaustion。

### Corollary 5.1 — 81-row rigid frontier tax

任意 beta 下，每个 original active rigid 3-cylinder 的 depth≥4，mass≤1/81。因此 rigid-only full 3-fiber 至少需要 81 个不同 active actual primes。若 N≤80，则

\[
\mathrm{Cap}^{act}_{3,c}(y)\le N/81\le80/81<1.
\]

由 source #11，同一个 lower assignment 上两个 anchors 的 full 3-fibers 至少有一个 rigid-only anchor。所以，少于 81 个可供该 anchor 使用的不同 actual primes 时，这种 simultaneous witness 不可能存在。这对 arbitrary beta、prime sizes、row precisions 都成立。

### Corollary 5.2 — Dynamic allowed 时至少 21 个 rigid primes

s3=v3(5²−1)=1，dynamic 3-row 只可接受 even j。其有限 shell mass 严格小于

\[
\sum_{j\ge0\atop j\text{ even}}\frac2{3^{j+1}}=\frac34.
\]

若有 N 个 active rigid primes，full coverage 必须满足

\[
1<\frac34+\frac N{81},
\]

故 N>81/4，亦即 N≥21。这里严格不等式来自 finite precision，未把 infinite shell tail 计作已覆盖。

当 beta≤3 时根本没有 original rigid resource；dynamic row 自己排除中心，故连一个 anchor 的 full original rank-3 fiber 都不可能存在。

这些是 necessary row-count bounds，不声称有 21 或 81 个 arithmetic resources 可实现 sharp examples。

## 7. SHARED-RESIDUE ARITHMETIC：paired graph 与 resultant

### KH-6 — Paired-position graph

**Classification: UNCONDITIONAL THEOREM.**

令 q∈R_(ell,d)，h=ell^d，u=w_q/h。固定 shared lower assignment \(b\equiv Y\pmod u\)。在 F_q 中令

\[
H_q=\langle5^u\rangle,\qquad |H_q|=h,
\qquad A_q(Y)=5^YH_q.
\]

该 lower fiber 的所有 5-powers 正好是 A_q(Y)。两个 rigid anchors 可共同活跃，必须有

\[
a_0-a_1=2,\qquad a_0,a_1\in A_q(Y).
\]

反过来，若此式成立，K=2、E={1} 时，r modulo q 的值被确定，在 q 个 modulo q² lifts 中避开至多两个 local-zero lifts 即可同时取得两个 valuation-one rigid events。因此对于可选择 residues 的 potential resource model，这个 condition 是必要充分的。

将 vertices 以 b modh 标记，edge 为 (x0,x1)。每个 vertex 出度和入度均≤1，没有 loop。将两个 projections 同一标记识别后，图还是 directed path forest：一条 t-cycle 会强制 2t≡0 modq，但 t≤h<q，不可能。它不是自由的 Cartesian product。

Exact edge count 为

\[
\deg\gcd_{\mathbb F_q[T]}
(T^h-5^{Yh},(T-2)^h-5^{Yh}).\tag{7.1}
\]

因为这两个 polynomials 的 roots 都是在 F_q 中分裂的 corresponding cosets，且 q不整除h，roots simple。

### KH-7 — Nonzero resultant invariant

定义整数

\[
\mathfrak D_h(Y)=\operatorname{Res}_T
(T^h-5^{Yh},(T-2)^h-5^{Yh}),\quad Y\ge0.
\]

对每个 odd h，\(\mathfrak D_h(Y)\ne0\)，且

\[
\boxed{q\text{ can be rigid-active at both anchors at lower }Y
\ \Longrightarrow\ q\mid\mathfrak D_h(Y).}\tag{7.2}
\]

**Proof of nonvanishing.** 若有 common complex root z，则 |z|=|z−2|=5^Y，故 Re z=1，z−2=−conjugate(z)。因为 h 为奇数，

\[
(z-2)^h=-\overline{z^h}=-5^{Yh},
\]

与另一个 equation 要求 +5^(Yh) 矛盾。Resultant divisibility 则来自 common root modulo q。□

因此，对固定的 ordinary integer Y 和固定 h，所有 double-usable primes 都在一个明确有限 divisor set 中，即使不限制 lower part u 的大小。该结论并不声称 raw R_(ell,d) 有限，也不声称把 Y 在所有 integers 中变化后仍只有有限个 primes。

对 fixed finite ambient lower point y，可取一个 common ordinary representative Y，并只允许其 supported resources。若一开始只有不含全部候选 lower prime powers 的 partial assignment，就必须先解决兼容扩展；不能把它当作对全部 q 已定义的 y。

### KH-8 — 全零 lower 的 universal forbidden position

令 Y=0。任何 odd-order H_q 都不含 −1。如果 anchor-0 rigid cylinder 包含 top point x=0，则 b0≡0 modulo w_q，a0=1，因此 a1=−1 不可能属于 H_q。

所以：**在全零 lower 上，一个覆盖 anchor-0 top-zero 的 original rigid prime，不能在另一个 anchor 的同一个 lower fiber 中供应任何 rigid cylinder。** 这是对所有 odd coordinates 和 depths 的 position-sensitive zero，不是统计结论。

由此，如果两个 anchors 都 rigid-only，并且所有 active rigid depths≥D，那么至少需要 ell^D+1 个不同 primes：选一个覆盖 anchor-0 zero 的 q，它对 anchor1 完全不可用；anchor1 自己还需要至少 ell^D 个其他 primes。特别地，coordinate3、zero lower、RR case 给出 **82-row** lower bound。

### KH-9 — ell=5,7 的 double-resource zero

计算 Y=0 的四个 resultants，完整分解如下（仅写绝对值）：

| h | abs(D_h(0)) |
|---:|---|
| 3 | 2^3·7·13 |
| 5 | 2^5·11^3·31·41 |
| 7 | 2^7·29·71·113·127·239·1093 |
| 9 | 2^9·7·13·19^4·37^2·73·163·199·307·757 |

Initial exact discovery 后，以 polynomial Euclidean resultant 和独立 Sylvester/Bareiss determinant 复算；每个 prime factor 都由 trial division 认证。对于 h=5，所有 admitted q>h divisors 为 11、31；对于 h=7，为 71、127、239。它们全部是 base-5 regular primes。故

\[
\mathcal R^{double}_{5,1}(0)=\mathcal R^{double}_{7,1}(0)=\varnothing.
\]

对 exact order signatures 再过滤当然仍为空。Resultant factor 的 multiplicity 不是 s_q：例如 11³|D5(0)，但 s11=1，不能混淆这两个 valuation。

## 8. INTERFACE WITH TWO-ANCHOR OBSTRUCTION

### KH-10 — Joint Kraft capacity

令 Q 为与 fixed ambient/lower setup 兼容的有限 actual prime pool，d_q 为其 depth。令 epsilon_q(y) 在该 q 的 paired-position graph 非空时取 1，否则取 0。定义

\[
C=\sum_{q\in Q}\ell^{-d_q},\qquad
C_{pair}(y)=\sum_{q\in Q}\epsilon_q(y)\ell^{-d_q}.
\]

令 D_max 为该 finite beta 中允许的最大 dynamic shell mass；没有 admitted dynamic row 时 D_max=0。若同一 lower y 的两个 rank-ell fibers 都 full，则必要地

\[
\boxed{C\ge1,\qquad C+C_{pair}(y)+D_{max}\ge2.}\tag{8.1}
\]

第一式来自至少一个 rigid-only anchor。第二式中每个 q 最多贡献 (1+epsilon_q)ell^(-d_q) 的双层总质量，而 source anchor-exclusion 使 dynamic mass 只能在一侧出现。若 residues/E 已冻结，可用实际 configurations 进一步收紧；使用 potential configurations 只会放宽 capacity，不会误排可行系统。

### Corollary 10.1 — 两个 joint row bounds

在 beta=1、全零 lower fiber：

- ell=5：dynamic row 不 admitted，D_max=0，且 C_pair=0。故 2≤N/5，即 **N≥10**。
- ell=7：dynamic 两侧总质量至多 6/7，且 C_pair=0。故 2≤6/7+N/7，即 **N≥8**。若两侧都没有 dynamic，则进一步 N≥14。

这些 bounds 允许 arbitrary prime sizes 和 arbitrary lower order parts。它们是 universal within the specified class，不是 q≤某值的结果。

### 与 complete certificate 的接口

上述所有 joint obstructions 都需要真实 same-lower / same-coordinate witness。Main 尚未证明 completeness 强制这样的 witness。Lower-ranked events 如果已覆盖某 anchor 的整个 fiber，就不是此处的双层 rank-ell demand；higher-ranked events 和 derived macros 也不能偷偷加入 original resource count。

因此，本轮为 future synchronization theorem 提供了 stronger exact arithmetic obstruction，但没有代替 synchronization theorem。

## 9. INDEPENDENT COMPUTATION

### 9.1 冻结目标与 benchmark

`COMPUTATION_SPEC.md` 在对应 runs 前固定了 targets。唯一 q scan 是**复算已有的 q≤10^7 panel**，先做 q≤10^5 benchmark；没有扩大 q_max。Theorem-driven supplement 固定 Y=0、h∈{3,5,7,9}，先测试 h=3，再执行其余固定 cases。

Frozen original timing 仅用于记录本环境的 benchmark，不是性能承诺：

| task | elapsed seconds |
|---|---:|
| q≤100000 benchmark | 见 results/benchmark_panel.json |
| q≤10000000 panel | 约 2.94 |
| q=20771 paired catalog | 约 0.198 |
| q=40487 paired catalog | 约 0.247 |
| existing two-row replay | 约 0.337 |

所有数学判断使用 integer / Fraction / exact modular arithmetic。Final bundle 的程序只需 Python standard library。Initial factor discovery 后，sealed factor identities 又由不依赖第三方 symbolic package 的生成器与 verifier 检查。

### 9.2 Existing main panel 的 independent reproduction

332398 admitted primes，nonregular hits 恰为

| q | w_q | factorization | s_q |
|---:|---:|---|---:|
| 20771 | 10385 | 5·31·67 | 2 |
| 40487 | 40486 | 2·31·653 | 2 |

Counts (support / order signature / active nonregular)：

| ell | d | counts |
|---:|---:|---|
| 3 | 1 | 83226 / 2 / 0 |
| 3 | 2 | 27727 / 2 / 0 |
| 3 | 3 | 9249 / 5 / 0 |
| 67 | 1 | 4873 / 645 / 1 |
| 67 | 2 | 72 / 35 / 0 |
| 67 | 3 | 1 / 1 / 0 |

本表所有 absence 都仅限 q≤10^7。不能用来证明 R67 高层 universally empty。

### 9.3 Position-sensitive inventories

独立使用 full log table 与逐 lower coset 的 residue enumeration 两种组织方式，完全一致：

| q | (ell,h,u) | all pairs | same-lower pairs | nonempty lower classes |
|---:|---|---:|---:|---:|
| 20771 | (67,67,155) | 5192 | 33 | 28 / 155 |
| 40487 | (653,653,62) | 40485 | 652 | 62 / 62 |

20771 的 per-lower edge-count histogram 为：0 edges 有127类，1 edge 有24类，2 edges 有3类，3 edges 有1类。Y=0 没有 pair。

40487 的 Y=0 有5个 pairs；完整 graph 数据在 `paired_positions.json`。每个 actual pair 都检查了 modq difference、两端 positions、lower equality、以及存在避开 local zeros 的 common q² residue。

### 9.4 旧 (67,20771) 系统复算

重新算出：dynamic pairs603、rigid pairs5192、pointwise joins693、distinct lower pairs692、same-lower joins0。

直接枚举 228470 个 exponent classes：

```text
r67=2, r20771=13471:
  Sat0={2728}, Sat1={1639}, min joint holes=67.

r67=0, r20771=4494:
  Sat0={2431}, Sat1={106}, min joint holes=66.
```

这些是 main 已有结果的 independent reproduction，不列为本轮新 theorem。

### 9.5 Finite verification

独立 verifier 检查：6 个完整 cyclotomic identities、4 个 resultants 的 Bareiss determinant、28 个不同 factor primes 的 deterministic primality；ell=3,beta=2 的所有4096个 cylinder subsets；1000个有限 depth-inventory profiles。其结果包括729个 full covers、8748次正确 branch inequality checks，以及2916个 inside-only 错误版本在 full covers 上的失败 instances。

这些程序是 independently organized reference checks，运行在同一 Python 环境；不是两个独立机构或完全独立 software stacks 的证明审查。

## 10. COUNTEREXAMPLES

**C1 — FAILED CONJECTURE：无 ancestor proviso 的一般 prefix-tree inside-only 公式。** 见 §3 的 abstract depth-one cover / depth-two branch。

**C2 — FAILED CONJECTURE：frozen actual positions 的 mass≥1 保证 coverage。** 独立构造已知机制：c=0，lower=0 mod3410，K=2、E={1}，r67=2，r20771=53298436。Dynamic 覆盖66个 digits；rigid full class b=2480 给出 top digit1，已在 dynamic cover 中。总 mass=1，union=66/67，遗漏 zero digit。不能把这个例子误当成 rigid-only actual counterexample，也不能称其机制是本轮首创。

**C3 — FAILED CONJECTURE：one-anchor Hall + weighted configuration capacities 足以保证 joint integral matching。** §4 的两-resource coloured hypergraph 是 abstract counterexample，不宣称实际 primes 已实现该 configuration family。

**C4 — FAILED CONJECTURE：全零 lower 使每个 actual q 都只能单边 active。** q=40487、w=40486、ell=653、u=62、K=2、E={1}、r=25919。Classes b0=3968、b1=14260 都是0 modulo62，top positions 为50、547。两侧精确 valuation 都为1。这是实际 arithmetic counterexample，表明 KH-9 的 ell=5,7 不能扩成所有 ell。

**不是反例的正确命题：** finite-beta/free-one-anchor/some-frontier 的 raw Kraft sufficiency 在 §4.2 已证明。其量词不能删去。

## 11. CONDITIONAL RESULTS 与外部文献

### 11.1 Conditional synchronization interface

**Classification: CONDITIONAL THEOREM / ACCEPTED IMPLICATION，未证明 hypothesis。**

设某个 certificate class 满足 H1：每个 complete simultaneous certificate 都产生一个 original-row same-lower full rank-ell fiber witness，且该 witness 必须落入以下某个已证明 deficit class，例如 ell=3、对应 rigid-only anchor 的可用 primes≤80；或者 zero-lower beta-one ell=5 且总rigid primes≤9；或者 ell=7 且总rigid primes≤7。

则这个 class 中没有 complete simultaneous certificate。Proof：H1 给 witness，KH-5/KH-10 排除 witness。H1 是独立尚未证明的 synchronization / coordinate-forcing hypothesis，不由本轮结果自动成立。

### 11.2 Primary literature 的实际含义

查阅 Yuchen Ding, *Non-Wieferich primes under the abc conjecture*, C. R. Acad. Sci. Paris, Ser. I 357 (2019), 483–486, DOI 10.1016/j.crma.2019.05.007，Theorem 1.1。它在 abc 假设下，对 fixed a,k≥2 给出 p≡1 modk 的 **non-Wieferich primes 的下界** ≫log x。

也核对 Graves–Weiss 2025 preprint arXiv:2503.19144v1 的相关 number-field conditional statements。二者都不提供本文需要的 fixed smooth-order Wieferich resource count 上界。不能将“有很多 non-Wieferich primes”倒置成“Wieferich resources 的 Kraft mass<1”。

Evidence grading：Ding 是 published primary theorem；Graves–Weiss 是 primary preprint；本轮不以 survey、OEIS comment 或 blog heuristic 充当 arithmetic theorem 的 premise。对全局 Wieferich resource scarcity，本轮没有从标准 conjecture 推出更强结论。

## 12. BOUNDED EVIDENCE 与 statement register

| Statement | Classification | Scope |
|---|---|---|
| Active Kraft、corrected branch inequality、fixed-cylinder tree recurrence | UNCONDITIONAL THEOREM | Fixed original-row fiber |
| One-anchor finite-capacity converse | UNCONDITIONAL THEOREM | Free residues / some frontier / ambient gate |
| Finite-support cyclotomic invariant | UNCONDITIONAL THEOREM | Fixed M, no q cutoff |
| R3,d empty for d=1,2,3 | UNCONDITIONAL THEOREM with exact finite certificates | All q |
| 81-row / 21-row bounds | UNCONDITIONAL THEOREM | Original rank3 fibers, arbitrary beta |
| Paired resultant finite divisor invariant | UNCONDITIONAL THEOREM | Fixed ordinary Y and h |
| Zero-lower forbidden anchor-0 zero projection | UNCONDITIONAL THEOREM | Every odd coordinate/depth |
| Double-resource zeros at (5,1),(7,1),Y=0 | UNCONDITIONAL THEOREM with exact finite certificates | All q, arbitrary lower order parts |
| Joint 10/8-row bounds | UNCONDITIONAL THEOREM | Zero-lower beta-one classes |
| 10^7 panel and selected paired catalogs | EXACT FINITE RESULT | Explicit finite domains |
| Ancestor-free omission / blanket zero-lower one-sidedness | FAILED CONJECTURE | Counterexamples above |
| H1 plus a proved deficit class excludes complete certificates | CONDITIONAL THEOREM | H1 remains unproved |
| Universal raw Kraft deficit for every ell | OPEN | Not established |
| Wieferich scarcity suggests fewer resources | HEURISTIC only | Not used in proofs |

## 13. STRONGEST NEW COROLLARY

对于任意有限 admitted original-row system，任意 beta、任意 allowed precisions、任意 shared residues，如果在 same-lower simultaneous full 3-fiber 所需的 rigid-only anchor 上最多有80个 active distinct primes，则

\[
\mathrm{Cap}^{act}_{3,c}(y)\le80/81<1,
\]

从而该 joint full fiber 不可能存在。

这个 implication 不含 q_max，也不假设 Wieferich primes 稀少或有限。它把六个完全可核验的 arithmetic factor identities 转化为对无限参数类有效的 exact obstruction。

此外，resultant theorem 把 fixed (Y,h) 的 double-usable resource pool 压到有限 prime divisors；这是区别于单边 raw scarcity 的 arithmetic mechanism。

## 14. WHAT REMAINS OPEN

R_(ell,d) 的一般分类，以及 R3,d 对所有 d≥4 的情况未解决。未证明 universal global Kraft capacity<1。未证明给出的 row-count bounds 可被 actual resources 达到。未完成所有 primes、所有 lower assignments 的 joint integral configuration problem。

Completeness 到 same-lower/same-coordinate original-row witness 的 H1 bridge 仍然缺失。Derived macros 的 provenance resource charging 也尚未建立，不能把本文的 actual-prime成本逐层强加到 contraction macros 上。

One-anchor 原始 theorem 的 full-fiber occurrence 不能强制 ell=3、5 或7，因此这些 coordinate-specific obstructions 不等于完整 C=1 no-go。Local-mask escape 也不等于 sums-of-two-squares representability。

## 15. NEXT RECOMMENDED GATE

建议进入一个独立的 **theorem integration audit**：优先复审 KH-5 的 completeness/factor certificates、KH-7 的 resultant quantifiers、KH-8 的 zero-position exclusion、KH-10 的 single-use joint capacities，并核对所有 original-row / macro scope guards。该 audit 通过后才适合整合为 theorem-only record；不是自动 promotion，也不需要先扩大 prime scan。

Gate assessment：A 的 formulation 部分已得到，但 T1 本身不是核心 novelty；B 由 coordinate3 无界-q exclusion 与81-row obstruction支持；C 由 resultant/zero-position/joint capacity 支持；E 由与 future synchronization theorem 的 exact interface 支持。D 中有实际 counterexample 与抽象 counterexample，但各自范围不可互换；本轮不声称已构造 actual rigid-only raw-capacity-sufficiency 的新反例。

```text
PHASE VERDICT:
A. NEW UNIVERSAL RESOURCE OBSTRUCTION
   WITH EXPLICIT COORDINATE / LOWER-FIBER SCOPE

Additional outcome:
C. NEW HALL/KRAFT FORMULATION WITH NONTRIVIAL CONSEQUENCE

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

REPOSITORY INTEGRATION:
DRAFT PR ONLY
```
