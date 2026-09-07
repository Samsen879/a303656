# A303656 C=1 — Hybrid allocated–transitive release theorem

## Research verdict

**HYBRID THEOREM: PROVED**, as the explicitly quantified sufficient theorem H below. It applies to a frozen finite admitted original-row system, arbitrary precision, full-depth projections, mixed anchors, and coalescing actual-row dependencies. It does **not** assert that a successful allocation/release plan always exists.

**STRICT SUBSUMPTION: PARTIAL.** P4 and the G1 escape mechanism (hence G3 and its boundary-primed specialization) are literal sufficient specializations of H. An actual arithmetic plan using both occupied-live allocation and regular-relay release is exhibited. However, that ledger also has alternative successful P4 and G3 plans. No actual ledger has been established here which fails *every* old plan but passes H. Exact local unions and temporal rigid blocking already occur in #17, and are not claimed as new by themselves.

新增结果是一个可直接审计的 **anchor-tagged global guard-release certificate**，把 full-depth allocation 与 optional regular/nonregular guard release 放入同一证明；另外给出一个 **actual regular-guard local feasibility family 不满足 matroid exchange** 的反例。没有新提高 seven-prime lower bound，没有新排除一个已具名、未被 Phase B 排除的完整证书算术族。

“PROVED”表示本文给出数学证明，不表示独立作者审稿或 proof-assistant formalization。以下以 [R1]–[R6] 表示固定 main 的 repository sources，以 [N] 表示本轮推导/计算。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Current main SHA: 71b8d428b32724c37e593bcfd9d5f06a42e72d21
Current main tree: 5609e47eed0c058c190ef59c61644e2fd4b8fad6
PRECONDITION: PASS
```

Live PR metadata 与 first-parent commit metadata 共同确认：

| PR | Merge commit | Main chain |
|---|---|---|
| #17 UNIFIED ENDGAME | 5b96db5bbe4634364df00dad5e9e0eeedb76ad09 | oldest of these four |
| #20 SEVEN-PRIME AUDIT | 64d4d498cbc2962923d4e5e0f830187d407773e6 | first parent is #17 merge |
| #18 POOLED LOWER COVER | 25a748662623f95ef5095ff4d8287c46982db100 | first parent is #20 merge |
| #19 BLOCKER-DEFICIENT CORE | 71b8d428b32724c37e593bcfd9d5f06a42e72d21 | first parent is #18 merge |

收尾再次读取 `refs/heads/main`，仍为上述 SHA。STATUS 保持 PAUSED / NONE / UNRESOLVED。

阅读了 STATUS、THEOREM_INDEX、ROUTE_MAP，以及六个指定目录的主报告和相关完整定义/证明正文；精确清单见 `SOURCE_BINDING.json`。没有只依据 README。**没有做六个目录每个生成数据文件/每段历史代码的逐文件重放，也没有运行仓库 CI 或 repository-native tests。** 容器未取得完整 checkout；source basis 是 GitHub connector 的 pinned reads，reference programs 为本轮独立写出的 standalone scripts。没有任何 GitHub 写入。

## 2. RECONSTRUCTED P4

[R5] 的 admitted ledger 由不同的实际 primes q≡3 mod4 索引。每行固定 K_q≥2、两 anchors 共用 r_q mod q^K，以及非空正奇数 accepted set E_q⊂[1,K_q−1]。

\[
V_{q,c}(d)=r_q-3^c-5^d,\quad
w_q=\operatorname{ord}_q(5),\quad s_q=v_q(5^{w_q}-1),
\]
\[
a_q=\max(0,K_q-s_q),\quad
U=\operatorname{lcm}(t_2,\{w_q\}),\quad
L=\operatorname{lcm}(t_2,\{w_qq^{a_q}\}),\quad \beta_p=v_p(U).
\]

Coarse fatal 指同一个 original row 接受该 coarse class 的**全部 full lifts**。Local zero mod q^K 不 accepted；本文所谓 safe 仅指未被 admitted local test 接受，不是已经找到 sum-of-two-squares representation。

P4 对每个具有 rigid-fatal component 的 original row q 选择一个奇素数 b(q)|w_q。把其 rigid-anchor logarithms 投影成 depth v_p(w_q) cylinders，并取真实 union B_p。即使 p 自己是 occupied dynamic row，只要

\[
D_p+\mu(B_p)<1
\]

在每个 odd coordinate 成立，就可在每个固定 two-adic boundary 上构造共同 odd coarse escape，再用 joint reverse CRT 得到共同 full escape。D_p 是原始 p-row 在任意 shared lower assignment 的 pooled dynamic mass 上界。

P4 没有把 blocker 解释为原始 rank-p rigid resource；它只是必要同余条件的投影。其公开算术实例是

\[
20771\mapsto5,\quad40487\mapsto653,\quad1645333507\mapsto3,
\]
\[
D_3+\mu(B_3)<\frac34+\frac2{27}=\frac{89}{108}<1.
\]

因此所有 nonregular rows 仅来自上述三素数的系统，已经被 P4.1 全部排除，其他 regular rows 可任意多、任意大，precision 与 shared residues 不受额外限制。[R5]

## 3. RECONSTRUCTED TRANSITIVE RELEASE

[R6] G1 选择 actual targeted rows T，包含全部 nonregular rows，并允许加入 regular relays。每行选择一个更小的 odd order factor。收到 incoming blockers 的 actual row 必须自己已被更小坐标阻断，或在 boundary 已不活跃；否则它的 own dynamic obligation 不能忽略。

这里阻断的是 **positive-divisibility guard**，不是只删除一个已命名的 rigid event。对两 anchors 处理所有存在的 guard，或对 boundary-selected 单 anchor 处理对应 guard。G1 直接在 full L 的 prime-power coordinates 上递增构造指数。

G2 证明容量收缩。对 t_p=(p−1)/k，k=1 或2，

\[
C(O(p))\le\frac{p-3}{2k}<t_p,
\quad O(p)=\{\ell\text{ odd prime}:\ell\mid w_p\}.
\]

G3 把 terminal-slot matching 转换成有效 guard forest。Paths coalesce 后，每个 actual relay 只保留一次自己的 outgoing guard obligation；并不继续传递每个 root 的一个守恒单位。

G4 的 min-cut 是 **conserved-flow 子模型**的 exact min-max，不是所有 release plans 的 min-max。Actual regular targets {11,23,67} 的 forest 11→5、23→11、67→11 成功，但三个 mandatory targets 无法匹配到 paired terminal5 的两个 slots。这不把它们说成 nonregular roots。

Primed G3 先选择一个 two-adically safe anchor/boundary，使 row3 的 positive guard 为假，再把坐标3作为 released terminal；并未删除原始 row3、U 或 L。其两-anchor common-safe 结论不能随意推广到 odd r2。[R6]

## 4. HYBRID STATE DEFINITION

### 4.1 Frozen ledger and tags

冻结全部 original parameters、U/L、anchor-specific exact normal forms。选择非空 anchor set C⊆{0,1} 和一个固定 two-adic exponent coordinate θ。

一个 tag 是 g=(q,c)，始终保留 q 的原始身份和唯一 shared residue。若 r_q−3^c modq∈⟨5⟩，定义唯一 logarithm b_g mod w_q：

\[
q\mid V_{q,c}(d)\iff d\equiv b_g\pmod{w_q}.\tag{4.1}
\]

没有 logarithm 的 tag 没有 positive-divisibility guard。两锚点 logarithms 若都存在，则不相等 modulo w_q；但它们在某个 p^e projection 上可能重合。

记 Z 为 guard 不存在、或已由 θ 的已固定因子证明 guard 不成立的 tags。Z 的定义是实际 congruence receipt，而不是未来阻断意图。

### 4.2 Tagged hybrid plan

选一组 targeted tags H，满足：每个不在 Z 中的 original coarse rigid-fatal tag 都属于 H。H 还可包含任意 actual row 的 positive-divisibility guard，包括 regular dynamic tags、nonregular dynamic tags，甚至不产生 coarse fatal event 的 guard。

对每个 g=(q,c)∈H，选择一个 receiver f(g)=p，满足

\[
p\text{ odd prime},\quad p\mid w_q,\quad p<q.
\]

要求 g 的 logarithm 存在。允许把同一 q 的两个 anchors 分配到不同 coordinates；这不改变其 r_q，也不把它们视为两个 primes。每个 tag 只选一个必要同余条件用于本 certificate；额外冗余限制不是新资源。

Receiver p 若在 original P 中，是 actual row coordinate；若不在 P 中，是 free coordinate，不能凭空再为它增加 row parameters 或 outgoing relay guard。特别地，5 可以作为 exponent coordinate，但不存在 admitted row5，也不存在 ord_5(5)。

定义 e_g=v_p(w_q) 和 exact cylinder

\[
C_g=\{z\in X_p:z\equiv b_g\pmod{p^{e_g}}\},
\quad X_p=\mathbb Z/p^{\beta_p}\mathbb Z,
\]
\[
B_p=\bigcup_{g\in H:f(g)=p} C_g.\tag{4.2}
\]

e_g≤β_p，因为 w_q|U。不同 tags 的重合或嵌套只在几何 union 中去重，provenance table 仍保留每个原始 q,c。

### 4.3 Dynamic shells and live status

若 tag (p,c) 的正常形为 dynamic，记其固定 zero center 为 ζ_(p,c)，m_p=min(a_p,β_p)，

\[
S_{p,c}=\bigcup_{\substack{0\le j<m_p\\s_p+j\in E_p}}
\{z:v_p(z-\zeta_{p,c})=j\}.\tag{4.3}
\]

实际 dynamic event 还需 lower guard d=b_(p,c) mod w_p 成立。因为 w_p|p−1，该 guard 只依赖比 p 小的 coordinates。

处理到 p 的 prefix y 时，定义

\[
\mathcal D_p^{\mathrm{live}}(y)
=\bigcup_{\substack{c\in C:\ (p,c)\text{ dynamic}\\
\text{guard compatible with the actual prefix }y}} S_{p,c}.
\]

每个 targeted own tag (p,c)∈H 已有 f(p,c)<p，因此在遵守 plan 的 prefix 中必已被阻断。其他 tags 也可能 incidentally 被已选 lower coordinates 阻断。Difference-2 保证在共同 prefix 上至多一个 dynamic anchor active。

### 4.4 Explicit temporal record

状态可写为

\[
\mathcal A=(\mathscr L,C,\theta,y,H,f,\{B_p\},\mathrm{status},\mathrm{receipts}),
\]

其中 y 保存**已经选定的完整 prime-power coordinate values**，不是独立挑选的局部最优状态。每个 tag 区分：ABSENT_GUARD / BOUNDARY_BLOCKED / TARGET_PENDING / GUARD_BLOCKED / DYNAMIC_LIVE / COARSE_FATAL_AVOIDED。

GUARD_BLOCKED 表示一个必要 congruence 已经失败，因而正整除永久不可能。COARSE_FATAL_AVOIDED 仅表示当前 coarse point 有非 fatal lift，不能谎称每个 full lift 已 safe。Original row 的 regular/nonregular 属性永不随状态改变。

## 5. MAIN THEOREM CANDIDATE — THEOREM H [N]

### Static exact full-depth tagged hybrid release theorem

在 §4 的冻结系统和合法 plan 中，令 J_p 是 original p-row 中不属于 H∪Z 的 dynamic anchor tags；p 不在 P 时令 J_p=∅。定义

\[
\boxed{\kappa_p=
\max\left(\{\mu(B_p)\}\cup
\{\mu(B_p\cup S_{p,c}):(p,c)\in J_p\}\right).}\tag{H}
\]

若所有 odd coordinates 满足 κ_p<1，则存在**同一个** x modU，使所选 C 中所有 anchors 的全部 original odd rows coarse-safe；并有**同一个** full lift d modL 在这些 anchors 全部 odd-safe。该结论对固定 θ 保持不变。

C={0,1} 时结论是 common odd-safe exponent。C={c} 且 θ 在该 anchor two-adically safe 时，结论足以否定 simultaneous completeness。它不主张两个 anchors 总能同时 two-adically safe。

一个保守的 sufficient inequality 是

\[
\overline D_p+\mu(B_p)<1,
\quad\overline D_p=\max(\{0\}\cup\{\mu(S_{p,c}):(p,c)\in J_p\}).\tag{H-mass}
\]

也可进一步将 μ(B_p) 上界为各不同投影的质量和，但没有必要这么做。为 uniform-in-residues corollary，可用 finite parity envelope 的上界；一旦只想验证冻结系统，应保留 exact union。

注意 (H) 不要求 μ(B_p∪S_(p,0)∪S_(p,1))<1。那将错误地把不可能同时 active 的两个 dynamic guards 一起收费。

## 6. PROOF / COUNTEREXAMPLE

### 6.1 Increasing-coordinate proof

先固定 θ，按 odd primes 递增处理 X_p。假设 lower coordinates 已按 plan 选定。

**已释放 own tags。** 若 (p,c)∈H，其 receiver f(p,c)<p 已处理。那一步选值避开了该 tag 的 cylinder，所以必要 congruence (4.1) 的一个因子已失败。不能再收取这个 tag 的 dynamic shell。

**仍活跃 own tags。** 其他 original dynamic p-tags 的完整 w_p guards 此时已经确定。同一 shared r_p 的两 anchors 不可能都正整除，因为两局部值之差为2，而 p 是奇素数。因此当前 live hazard 是空集，或 J_p 中一个固定 shell bundle。

由 (H)，

\[
\mu\bigl(B_p\cup\mathcal D_p^{\mathrm{live}}(y)\bigr)\le\kappa_p<1.
\]

有限 X_p 中可选择一个值同时避开它们。这个选择实际阻断所有 incoming targeted guards，并避开当前 live dynamic coarse event。

每个 targeted rigid event 在其 receiver 处永久失效；每个未 targeted dynamic event 在 own coordinate 处避开。所有 odd coordinates 完成后，每个所选 anchor 的每个 original coarse event 都不 fatal，得到同一个 x modU。非存在的 own coordinate（β_p=0）没有 dynamic coarse shell；其 full private digits 在下一步处理。

**重要量词：**同一个冻结 ledger、同一个 plan、同一个递增 prefix。不是“对每个 p 存在某个好 lower state”便自行拼接。静态最大值 (H) 对每个仍可能 active 的 own bundle 都保留余量，因此不需要提前猜测之后的 lower branches。

### 6.2 Joint reverse CRT

固定 x modU 后，对每个 actual q，5^d modq 在所有 compatible full lifts 中固定。至多一个 selected anchor 可正整除 q；其他 selected anchors 恒 valuation0。

Coarse safety 意味着该 row 有至少一个不 accepted 的 full local lift。它所需的额外 exponent freedom 仅在 q-primary digits 高于 β_q 的部分。对另一 row t≠q，所有 order factor q-adic precision 已包含在 U；因此这些 private q-digits不改变其他行。

分别选择每个 q 的 safe local extension，与 x 和 θ 联合 CRT，得到一个 d modL。可以取 local zero，但只以 LOCAL_ZERO_UNRESOLVED 记录，绝不接受它。于是 d 对所选 anchors 的全部 odd rows safe。证毕。

### 6.3 Equivalent full-L local formulation

令 γ_p=v_p(L)，把 B_p 拉回 Z/p^γ_pZ，dynamic shell 使用 j<a_p 的完整列表。因为 B_p 的深度≤β_p，B 在每个 coarse p-fiber 上是常值。Coarse dynamic 的定义又恰为整个对应 full fiber 被该 tag 接受。因此

\[
B_p\cup S^U_{p,c}\ne X^U_p
\iff
B_p\cup S^L_{p,c}\ne X^L_p.
\]

也可直接在 L 的 prime-power coordinates 递增执行证明；这时在 own step 就选择所有 private digits。两种版本的 union **数值质量不必相等**，但非满与否一致。该观察也避免把 later private same-prime digits 误当“无论怎样选都不影响安全”。

### 6.4 Quantitative survival

令 δ_p=1−κ_p>0。在每个合法 lower prefix，至少 δ_p 比例的 p-coordinate choices 可继续。因此 common coarse escape measure 至少 ∏_pδ_p。Full escape 至少有一个，保守 full-density bound 为 (U/L)∏_pδ_p。这里的乘积属于已通过计划条件的原始系统，不是任意 derived macro family 的 conserved potential。

### 6.5 History-sensitive extension and its limitation

静态 H 可以放宽为逐 prefix 使用真实已认证的 releases，并检查

\[
\mu(B_p(y)\cup\mathcal D_p^{live}(y))<1.
\]

但 B_p(y) 的删减只能依据已失败的必要 guard，不能根据未来愿望；所有步必须属于同一个 compatible history。若要求一个 policy 对其每个 reachable prefix 都保留余量，上述归纳仍成立。只给各坐标互不兼容的局部 witnesses 不够。

本文不把“存在一个成功完整 history”单独包装成新数学进展。可直接核验、不依赖未来猜测的主要充分条件是 (H)。

## 7. TEMPORAL SEMANTICS AUDIT

| Rule / risk | Correct conclusion |
|---|---|
| A: p-row 已在更小坐标阻断 | 对**已有 receipt 的 anchor tag**，D_live=0；若全部 selected tags 已阻断，才是 whole selected-row release。 |
| B: p-row 尚未释放 | 活跃 guard 对应的真实 dynamic shell 必须收费；不能在同一 local union 中同时视为 free 和 live。 |
| C: P4 kill 后能否继续作 relay | 算术 edge relation 仍存在；p-coordinate仍可供更大 rows 使用。已 killed 的是 p 的某个事件，不是指数坐标。另一 anchor hazard 是否消失须另查。 |
| D: higher prime coordinate | 不会修改较低完整 prime-power values，故不会恢复失败的 guard 或已避开的 coarse shell。 |
| D: private same-prime high digits | 任意坏选择可能使某一 full lift fatal；这不是 coarse event 重新活跃。joint reverse CRT 选择 safe lift，或直接 full-L induction 一次选全。 |
| Future intention | TARGET_PENDING 不是 GUARD_BLOCKED。只有 chosen residue≠required projection 才有 release receipt。 |
| Mixed state | r_q、K_q、E_q、b_(q,c)、ζ_(q,c) 从不随 branch 或 anchor 重新优化。 |

**Actual false row-wide release rule.** q=20771,K=4,E={1,3}，

\[
r=1+5^{6528}\pmod{q^4}=82423279840775796.
\]

anchor0 dynamic logarithm 6528；anchor1 rigid logarithm2。只将 rigid anchor1 分配到5，避开 digit2。取

\[
d=6528+10385\cdot20771=215713363,
\quad d\bmod5=3.
\]

其两侧 valuations 恰为 (3,0)。所以 rigid anchor1 确实已被阻断，但 dynamic anchor0 仍 fatal。LTE 给 v_q(5^(w_qq)−1)=s_q+1=3，证明不依赖抽样。反例推翻的是 row-wide 删除规则，不是声称这一个系统没有 escape。

## 8. COALESCENCE AUDIT

若 q1,…,qm 都进入 actual coordinate p，则每个 targeted anchor tag 产生自己的必要 cylinder，最多每个原始 q 两片；exact geometric union 可以重合或嵌套。Incoming costs 不能凭 paths 同终点就自动变成一片。

另一方面，p 自己的某一个 guard 只需被阻断一次。两个 roots 经 p 下降，不意味着要创建两个 p-row state 或重复支付两次同一个 outgoing guard。图中保留所有 incoming original identities；p 的 outgoing tag 用幂等语义复用。

本轮实际八行 witness 包含 23→11、67→11、11→5。23、67 的两侧 projected logs 在11上均为0，几何 B11只有一片；11→5 的 own guard 只一次。另一个 root20771→5也落在同一几何 digit0。数据保留四个 incoming tags at11 和两个 different rows at5，没有把几何去重等同于删去 original identity。

不能只沿路径传递最初 root 的 logarithm：q→p→r 中，在 r 避开的是 **p 自己**的冻结 logarithm；在 p 避开的是 q 的 logarithm。终端避开 p-guard并不会自动让 q-guard为假，必须再执行 p-coordinate step。

## 9. FULL-DEPTH BLOCKER AUDIT

Cylinders 的深度一律为 v_p(w_q)，并使用 normalized counting measure。两个相交 p-adic cylinders 嵌套，删除重复项与被 ancestor 包含的项后，最浅剩余 antichain 的质量和就是 exact union。

Dynamic shell v_p(z−ζ)=j 可展开为 p−1 个 depth j+1 的 side cylinders；因此同一个 prefix procedure 适用于 B∪D。

回归例（abstract geometry，机制在 #17 已出现）：p=3，D=S0(0)，B=C1(1)∪C1(2)。质量和4/3，但 exact union仅2/3。另一例 B=C2(0) 给 exact union7/9，若错误降为 first-digit C1(0)，则看起来全覆盖。两者仅说明更精确的 certificate geometry，不冒充新的 actual nonregular inventory。

实际大素数 q 的 p=3 projection depth为3，不是把它的 customary rigid rank从30469139改成3。2/27预算不会与 original rank3 resource-zero theorems 冲突。

## 10. MIXED-ANCHOR AUDIT

Difference-2 只在同一个完整 lower assignment、同一实际 row 上保证最多一侧 positive divisibility；它不允许先在两个 anchors 分别挑最好的 lower assignment。

同一 q 的两侧 type 可为 dynamic/rigid。本 theorem 只删除 H 或 Z 中的对应 tag，另一侧如果动态且 active 仍属于 D_live。Rigid incoming blocker也可以来自另一 anchor；必须检查它与当前 dynamic shell 的 union，不是各自安全便当作共同安全。

[R2,R5] 的实际 67/20771 SPLIT 在 lower0 mod3410 上给 D67,0=X67\{0}、opposite-anchor rigid cylinder={0}。Hybrid exact union正确判为 full，不能提前删除 current blocker后选0。该 source example 不是 complete certificate。

同一 q 的两 anchor full guards 不相交，但 projections可能重合。例如本轮 q40487 的两 logs0、20243在653上都投影为0。B653只收费1/653，provenance仍记录两个 anchor tags。

## 11. RELATION TO P4 AND G3

**P4 specialization.** H 只包含 rigid-fatal tags，且同一 q 的两个 rigid anchors 使用同一 receiver；不额外 target dynamic guards。P4 的 D_p 上界支配 J_p 中每个 shell，故 P4 inequality⇒(H)。其每一个 admitted instance 都被包含。

**G1 specialization.** 取 H 为 G1 targeted actual rows 在所选 anchors 的全部存在的 positive guards。收到 assignments 的 actual receiver 已 targeted 或 boundary-inactive，因此 J_p为空；条件只剩 μ(B_p)<1。没有 incoming 的 untargeted regular row有 proper dynamic shell。G1 因而是 H 的 specialization。

**G3 specialization.** G3 的 terminal matching 首先产生上述 G1 plan，再应用 H。严格说，G3 的 Hall 条件是构造某个 specialization plan 的 sufficient criterion，不是 H 的必要条件。Primed G3 取单 anchor并把 row3 的 boundary-inactive tags 放入 Z。

H 的 plan grammar 允许 G1 禁止的“incoming at live dynamic coordinate”，也允许 P4 未使用的 optional regular guard release。实际八行 witness同时使用这两项。但因存在其他旧 plan，该 witness不证明旧两个**可行系统集合之并**被严格扩大。

```text
LITERAL CONTAINMENT OF P4 AND G1/G3 SUFFICIENT INSTANCES: YES
ACTUAL PLAN USING BOTH MECHANISMS: YES
ACTUAL WHOLE-LEDGER STRICT SEPARATION FROM ALL OLD PLANS: NOT ESTABLISHED
STRICT SUBSUMPTION: PARTIAL
```

## 12. HYBRID DEFICIENT CORE AND SUBMODULAR OBSTRUCTION [N]

### 12.1 What is frozen in a core

固定 ledger、U/L、boundary、selected anchors、全部动态形状与 original guard options。不因从需求中删去一个 q 就删除其 support 或重算 U。

Left objects 是必须被阻断的 **original rigid row bundles**（每个 bundle保留其实际 anchor tags），不是路径条数、宏条数或 projected leaves。Plan 可选择额外 guard tags 进行 relay release。

对一个 mandatory subset S，记 Feas(S) 表示存在合法 H/f，覆盖 S 的全部 required tags，并通过 (H)。这里 S 之外的原始 rows仍在 ledger 中；删去的是 certificate obligation，不代表完整系统的事件消失。Feas 对减少 S 单调。若整体失败，可取一个 inclusion-minimal非空S，使 Feas(S)=false而每个单行 deletion可行。

这是 **minimal hybrid-unassignable core for the stated static certificate family**。它不是最小 actual complete certificate；也不证明原始系统没有其他 history-sensitive 或 selected-anchor escape。

### 12.2 Exact endogenous residual capacities

先固定 H。令 A⊆H 为收到 p 的 tags，且其 edges都合法。对每个可能 live bundle S_(p,c) 定义

\[
f_{p,c}(A)=\mu\left(\left(\bigcup_{g\in A}C_{g,p}\right)\setminus S_{p,c}\right).
\]

则 exact condition等价于

\[
f_{p,c}(A)<1-\mu(S_{p,c}),
\]

还包括空 dynamic bundle 的版本。右侧在 **H 和候选动态 tag 已冻结后**才是固定容量。改变 H 会释放 own tags、改变剩余动态列表；尚不能把它视为整个优化问题的固定 node capacity。

f_(p,c) 是 monotone submodular：向 A 加入 g 的边际成本是

\[
\mu\left(C_{g,p}\setminus\left(S_{p,c}\cup\bigcup_{h\in A}C_{h,p}\right)\right),
\]

随 A 增大而不增加。证明是集合包含关系。**一组 submodular constraints** 正确表达静态局部条件；不要未经证明说“对 c 取 max 仍 submodular”。

### 12.3 Actual arithmetic nonmatroid example

Original panel P={7,31,43,103}，selected anchor0，K=2,E={1}。它没有 actual row3，所以坐标3 free。取

| q | w_q | s_q | r_q | b_(q,0) | projection mod3 |
|---|---|---|---|---|---|
| 7 | 6 | 1 | 2 | 0 | 0 |
| 31 | 3 | 1 | 6 | 1 | 1 |
| 43 | 42 | 1 | 26 | 2 | 2 |
| 103 | 102 | 1 | 26 | 2 | 2 |

这些是真实 regular positive-divisibility guards，不是假造的 nonregular rigid leaves。所有深度v3(w_q)=1。

把一个 incoming set称为 feasible，当其 projected union不是全部X3。则

\[
I=\{7,31\},\quad J=\{7,43,103\}
\]

都 feasible，|I|<|J|；但向I加入J\I中的43或103，union都变成{0,1,2}。Matroid exchange失败。普通统一slot容量也不能同时允许J的三行、又禁止某些三行集合。

这排除**直接的**普通slot/matroid解释；并不证明不存在更复杂的扩展网络、整数规划或专门min-max theorem。

### 12.4 A valid configuration-weight obstruction

固定 H。令 I_p 为所有 local-feasible incoming subsets，包括所有候选 dynamic tags 的 exact constraints。若 H 能分配为 A_p∈I_p 的 partition，则对任意非负 tag weights t_g，必有

\[
\sum_{g\in H}t_g\le\sum_p\max_{A\in I_p}\sum_{g\in A}t_g.\tag{12.1}
\]

证明：对实际 partition求和，并在每个p上取最大值上界。违反式(12.1)认证该**固定H**无法分配；要排除整个 hybrid core，仍需处理所有合法 release choices。

事实上它们完整刻画**固定 H 的 fractional configuration relaxation**，但不刻画 integral assignment。证明如下。令 P_p 为 I_p 中各集合 incidence vector 的凸包，K=Σ_p P_p。各 I_p 向下封闭，所以 K 是非负正交域中的向下封闭紧凸集。Fractional cover存在当且仅当全1向量属于K；若存在更大的覆盖向量，向下封闭性允许减去重复归属。若全1不属于K，凸分离给一个权向量；将负分量置零不会减少对全1的分离强度，因为K向下封闭而其support function在这种替换下不变。故存在非负t使(12.1)失败。反向由实际凸分解求和直接成立。这个证明不声称构造全部I_p有效率，也不把fractional/integral gap伪称为actual prime gap。

因此得到的是 **fixed-release-pattern fractional configuration dual**；release pattern H 本身仍为外层离散选择。它不是整个 hybrid 问题的ordinary max-flow/min-cut。

## 13. BOUNDARY APPLICATIONS AND EXACT COMPUTATION [N]

### 13.1 Re-certified arithmetic

\[
w_{20771}=5\cdot31\cdot67,\quad s=2;
\qquad w_{40487}=2\cdot31\cdot653,\quad s=2;
\]
\[
w_{1645333507}=2\cdot3^3\cdot30469139,\quad s=2;
\]
\[
w_{30469139}=1429\cdot1523,\quad s=1.
\]

1429是prime≡1mod4，不能成为 admitted dynamic row。完整依赖认证还检查1523→761；但在下述实际八行 ledger中1523不是original row，不能当actual relay使用。`arithmetic_closure` 的 admitted 字段仅指允许的素数同余类别；真正row存在性由 `rows` ledger决定。

### 13.2 Actual hybrid ledger

没有 two-adic row。原始P为

\[
\{3,11,23,67,20771,40487,30469139,1645333507\}.
\]

| q | K | E | shared residue r |
|---|---|---|---|
| 3 | 6 | {1,3,5} | 507 |
| 11,23,67 | 2 | {1} | 2 |
| 20771 | 2 | {1} | 20773 |
| 40487 | 2 | {1} | 40489 |
| 30469139 | 2 | {1} | 6 |
| 1645333507 | 2 | {1} | 1645333513 |

大素数两侧真实 rigid logs为

\[
b_0=1,\quad b_1=85648253;
\qquad (b_0,b_1)\bmod27=(1,14).
\]

它们来自同一个 r=q+6，两个 log classes 的实际valuation都为1。relay30469139 的positive logs为1、882946，在1429上投影为1、1253。

采用plan：

\[
(q,0)\to3,\quad(q,1)\to30469139;
\quad(30469139,0/1)\to1429,
\]

以及20771→5、40487→653、23/67→11、11→5。

| receiver | exact B | live own hazard / exact union |
|---|---|---|
| 3 | {1 mod27} | D=S0(14)∪S2(14), μ(D)=20/27；B⊂D，union仍20/27 |
| 5 | {0 mod5} | free；union1/5 |
| 11 | {0 mod11} | own guard已在5阻断；union1/11 |
| 653 | {0 mod653} | free；union1/653 |
| 1429 | {1,1253 mod1429} | free；union2/1429 |
| 30469139 | {24709975 mod30469139} | own两侧guard已在1429阻断；union1/30469139 |

这是一个实际使用 **live occupied blocker + released regular relay + coalescence** 的plan。所有12个tag assignments都有合法 full-depth projection和状态收据。

### 13.3 ONE exponent, not separate local choices

最终 ambient periods由全部八行计算：

\[
U=267115101204182941669410,
\quad L=55292825949265868925567870=207U.
\]

构造的coarse point为

\[
x=106179260570583344376431\pmod U.
\]

Full CRT取

\[
\begin{array}{c|rrrrrrrrrrr}
\text{modulus}&2&243&5&11&23&31&67&653&1429&1523&30469139\\
\text{residue}&1&230&1&1&0&0&0&1&0&1&0
\end{array}
\]

得到

\[
\boxed{d=29221725291826523986342121\pmod L.}
\]

直接计算16个 row/anchor cells：row3/anchor0为LOCAL_ZERO_UNRESOLVED，剩下15个valuation均为0。因此同一d是共同odd-safe exponent，不是各坐标分别存在一点。

改动private3 digits，保留x modU及所有其他prime coordinates，可得

\[
d_{bad}=10790783308737901011152831\pmod L.
\]

它在row3/anchor0上的valuation恰为5∈E3；其余rows不变。这是“coarse escape不保证任意full lift安全”的真实回归。

### 13.4 Direct3 versus relay chain

Direct3不需要任何relay release，uniform bound89/108即足够；它在3端可能与live dynamic shell竞争，但深度3很便宜。经30469139→1429则免收30469139的own dynamic hazard，在该大坐标只留下至多2/30469139，同时把relay两guard的成本放到1429。

没有脱离其他incoming assignments就成立的全局优劣关系。比较必须看所有receiver的实际residual unions。本文mixed plan让direct blocker落在D3内，边际成本0，并把另一anchor的blocker转到released relay。

但当前ledger仍有P4替代plan：两侧q→3，此时实际coarse exact union21/27，scalar bound22/27；也有G3替代plan：两侧q→30469139→1429。因此不是actual whole-system strict-separation witness。

### 13.5 Actual scopes and counts

| Computation | Executed scope | Result |
|---|---|---|
| Arithmetic signatures | specified seeds and descending supports, plus four regular guard labels | exact trial-division primality / orders / lifting |
| Paired q state | bounded r_low target2..64, stopped at6; exact BSGS and modular verification | logs1,85648253; both rigid valuation1 |
| Full hybrid CRT | 8rows×2anchors | one common d verified |
| Bad private lift | same16cells, one differentprivate3choice | exactly row3/anchor0 becomes valuation5 |
| Actual mixed20771 | explicitd and logarithm/valuation identities | rigid side blocked, dynamic side fatal |
| Row3 coarse/full normal form | 27coarseclasses,243compatible full local cells | all match |
| Exact prefix unions | 4096cylinder subsets×27centers×5parity bundles=552,960 | 0 mismatches |
| Strict mass implication | 229,284 applicable union checks | 0 failures |
| Exact-union improvement instances | 133,650 cases: sum≥1 but exact union<1 | geometry only |
| One-root abstract hybrid | 25,200 systems;2,646,000 directgridcells | 18,165 staticpasses;0 unsound passes |
| Two-root abstract coalescence | 13,500 systems;1,417,500 directgridcells | 10,125 staticpasses;0 unsound passes |
| Actual local nonmatroid family | 4regular rows; all256ordered subsetpairs | exchangefails;submodularityholds |
| Bad plan mutations | 6 specific mutations | allrejected |

所有普遍结论来自证明，非来自有限枚举。Abstract tests中的synthetic rank5 relay不是actual admitted row5；它只测试三角normal-form逻辑。数据中7,015个单root systems通过真实escape但未通过静态condition，明确证明该condition不是必要条件（这些是abstract systems）。

没有扩大prime cutoff，没有枚举巨大L，没有把同一Python实验环境称为独立作者/独立机构复现。Code审阅时发现初版辅助函数未拒绝base5模5的order调用；已修复，并增加明确拒绝测试。自由coordinate5不携带该order，最终数学结果不使用错误值。

## 14. ADVERSARIAL COUNTEREXAMPLES — TEN RISKS

1. **Released row仍有另一anchor hazard：**实际mixed20771的(3,0) valuations反驳whole-row deletion。
2. **Two paths share relay：**原始relaytag只一次；实际23/67→11与所有相应tag收据验证。
3. **Blocker completely inside dynamic shell：**实际q→3的{1 mod27}⊂S0(14)，边际成本0。
4. **Mass>1 but exact union<1：**abstract4/3 versus2/3例；完整552,960次union审计。
5. **每个坐标分别好，但state不兼容：**一个shared stateσ=0要求x=0,y=1，σ=1要求x=1,y=0。分别可取x=0,y=0，却不存在同一σ兼容这个组合。H冻结state且使用同一prefix，不作这种拼接。这是错误推理的abstract反例，不是完整arithmetic no-go的反例。
6. **Mixed dynamic/rigid：**type按(q,c)记录；另一anchorincoming blocker仍与D_live联合检查。
7. **Local zero wrongly accepted：**row3/anchor0的actual full value0以unresolved记录；坏lift得到5而不是伪造valuationK。
8. **Later step changes lower guard：**完整primarycoordinate一次固定，laterdifferentprime不修改；privatebits用jointCRT处理。
9. **Nonexistent actual relay：**validator拒绝1429充当outgoing source；允许它作为free receiver。
10. **Macro becomes new row：**validator拒绝macro source、非orderedge、错误projection、重复tag资源化；原始ledger只包含八行。

## 15. NEW SURVIVOR CLASS

定义 frozen-state class E_H：原始参数满足Phase B的必要条件，并且对每个可用的two-adically safe选定anchor/boundary，mandatory original rigid demands没有通过(H)的合法hybridplan。

任何完整simultaneous admitted certificate都属于E_H，因一份成功单anchorplan就会给出反例exponent。它还必须通过原有≥7nonregular total、primed-terminalHall deficiency等necessary filters。这里的失败是staticcertificate-familyfailure，不是ordinaryflowcut，也不是原始系统无escape的等价判定。

该class保留：originalrowbundles、全深度cylinders、释放选择、被释放后的真实dynamicresidual、sharedstate、固定U/L，以及所有lowercompatibility。它比“某个masssum≥1”更具体，但本文没有认证一个actualmember证明其对Phase B剩余**实际系统集合**的缩小严格。

## 16. DOES IT STRICTLY IMPROVE PHASE B?

数学接口上有所推进：给出单一、可核验的global tagged sufficient theorem，允许incoming atlivecoordinate，同时允许regularguardrelease与coalescence，并把exactfull-depthunion和sharedstate放在同一量词框架。

但exactlocalunion、temporalrigidblocking、G1guardrelease、P4occupiedallocation本来分别已存在，不能各自再列为本轮首创。实际plan混合两机制不是实际class严格增强的证明。

**结论：formal synthesis proved；strict actual exclusion improvement NOT ESTABLISHED。**

## 17. CAN IT ELIMINATE ANY NEW ACTUAL ARITHMETIC CLASS?

没有认证一个此前P4/G3都无法排除的、已具名的完整证书算术族。三大nonregular边界和本轮八行ledger都已经在旧P4.1以及≤6nonregular no-go的范围中。

新actualnegative结果是localguardfamily非matroid，排除一种自然的建模捷径，不应被称为排除了新的完整certificateclass。没有提高seven-prime界，没有发现completeactualoddpooledcover，也没有解决A303656。

## 18. NEXT SINGLE TARGET

**Frozen seven-root hybrid-unassignable core 的 release-pattern exchange / exact local obstruction theorem。**

固定一个通过旧必要过滤的候选七rootledger及同一sharedstate，研究所有可合法release的guardtags；证明一个静态失败的最小core能否通过一次regular-guardrelease把至少一个exactunion从full变为proper，而不在其他坐标制造fullunion。目标是一个真正的exchange theorem或一个actualcounterexample，不是盲目扩大prime scan。仅靠刚刚被反驳的matroidexchange不足，必须使用actualorderdepths与submodular marginal costs。

```text
HYBRID THEOREM:
PROVED

UNIVERSAL SUCCESSFUL ASSIGNMENT:
NOT PROVED

STRICT SUBSUMPTION:
PARTIAL

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

## Source key

All repository sources fixed at main SHA 71b8d428b32724c37e593bcfd9d5f06a42e72d21; exact paths and known Git blobs in SOURCE_BINDING.json.

- [R1] analysis/c1_two_root_provenance_phase_a/REPORT.md and PROOF_AUDIT.md: original ledger, free blockers, joint reverse CRT, provenance.
- [R2] analysis/c1_two_anchor_sync_phase_a/REPORT.md: S1/SPLIT/two-adic boundary and exact arithmetic counterexample scopes.
- [R3] analysis/c1_kraft_hall_phase_a/REPORT.md: actual-prime resources, prefix unions, shared configurations, fractional limitations.
- [R4] analysis/c1_unified_endgame_phase_b/{REPORT,MASTER_THEOREM,DEFINITIONS,COUNTEREXAMPLES}.md: existing hybrid local criterion, temporal semantics, exact unions, seven-prime theorem.
- [R5] analysis/c1_pooled_lower_cover_phase_b/{REPORT,DEFINITIONS}.md: P4, mixed row normal form,89/108,conditional seed scope.
- [R6] analysis/c1_blocker_deficient_core_phase_b/{REPORT,DEFINITIONS,THEOREM_AUDIT}.md: G1–G4,primedHall,coalescence,K2.
- [N] This report's theorem H, static release certificate, eight-row mixed plan, actual nonmatroid guard example and standalone reference calculations. No literature-priority claim.
