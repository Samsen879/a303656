# A303656 C=1 B7 pure-3 basin arithmetic classification — Phase D

## 0. 结论与证据级别

**本轮结果：完整的第一层算术分类、严格的有限候选表示缩减，以及一个适用于 branching B7 basin 的条件性填充定理。没有证明 B7 为空，没有找到实际 nonregular B7 成员，没有把总根数界提高到八。**

最重要的无 cutoff 结论为：采用下文由 exactly-seven 证明支持的 basal-gateway 定义，任意 B7 root 的完整 admitted closure 中，除 7 以外数值最小的顶点，必为

\[
A_7=\{43,127,379,7603,19531,519499\}.
\]

这六个顶点全部 regular，因而都不是该 nonregular root。任何 B7 basin 至少有两个 proper regular admitted relays，且 root 不能直接接在只有 7 的 regular basin 上。

如果整个 admitted basin 恰有三个顶点 \(D(q)=\{7,r,q\}\)，则 \(r\in A_7\)，并且 root 的 exact order 必在明确的 48 个整数中。本轮无条件排除其中五个：
\[
43,\ 86,\ 127,\ 129,\ 258.
\]
剩余 43 个有限 order cases，不等于已经有 43 个实际 nonregular primes。

本报告中的新数学推导和程序均由同一研究会话完成；不是独立作者审稿或 proof-assistant formalization。`verify.py` 的有限计算不能代替无限参数定理的证明。所有结论仅在源仓库 admitted original-row C=1 formal class 中使用。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: 3fb4b4b4f71018017c7ea014ae7a1380f27b6b94
main tree: 5ee6ab9e51f3e6d471991b7407de193d12777882
PRECONDITION: PASS
```

通过 live branch、fixed-SHA STATUS 和各 PR 的 merged 字段、main base/merge ancestry 确認：

| PR | 内容 | Merge commit |
|---|---|---|
|21|Hybrid|1f4928d6a26fe98d28d576c56cd0f1dfecb13459|
|22|Global Shared State|509bd064f849ff465e40e9edd7205c89b45a08c7|
|23|Nonlinear Core|57d19d4d67f18ad38566ac5dafd7c4bf62f8b23c|
|24|Order-DAG|cc15e53761f0669aefe8d5421c190d0584ebef78|
|25|Hybrid scope repair|3fb4b4b4f71018017c7ea014ae7a1380f27b6b94|

#25 是累计 main 的 integration scope replay 修复，不改变数学 source payload。没有用各源报告自己的历史研究 SHA 替代当前 authority。

**实际阅读范围：** 五个指定目录中的核心定义、主证明、相关报告和证明审计，逐项列于 `SOURCE_BINDING.json`。没有逐一阅读五个目录全部辅助文件、生成数据和历史代码，因此不声称完成了“每个目录全部文件”的逐文件阅读。没有完成本地 checkout；只读 clone 尝试因 DNS 失败。没有重跑 repository-native tests，也没有重跑 \(2\times10^9\) prime inventory。以下 standalone 验证与这些未执行的工作明确区分。

## 2. PRECISE B7 DEFINITION

### 2.1 继承的 arithmetic notation

对 admitted prime \(x\equiv3\pmod4\)，定义
\[
w_x=\operatorname{ord}_x(5),\qquad s_x=v_x(5^{w_x}-1),
\qquad O(x)=\{p:p\text{ odd prime},\ p\mid w_x\}.
\]
Regular 指 \(s_x=1\)，nonregular 指 \(s_x\ge2\)。

Absolute order DAG 对每个 admitted \(x>3\) 展开全部 \(O(x)\)，包括原 panel 没有列出的 arithmetic labels。边严格下降。终端为 3 或 \(1\bmod4\) primes，终端集合为 \(T(x)\)。\(D(q)\) 包括 \(q\) 和全部 admitted descendants \(>3\)，不包含 terminal 3。

### 2.2 必须显式处理的 “last gateway” 歧义

Phase C §13 使用了 informal “only last gateway into 3 is 7”，但未另给集合公式。Phase B DEFINITIONS §9 区分了任意路径的最后 row 与最大-factor 路径的 pure-order gateway。Phase C 的 shallow-head inventory 和 disjointness 证明实际支持的是 **basal gateway**：
\[
\Gamma(q)=\{x\in D(q):O(x)=\{3\}\}.
\]

本轮研究 exactly-seven 所必需的完整算术类，形式化为
\[
\boxed{
\begin{aligned}
\mathcal B_7=\{q:\;&q\text{ prime},\ q\equiv3(4),\ s_q\ge2;\\
&T(q)=\{3\};\\
&s_x=1\quad(x\in D(q)\setminus\{q\});\\
&\Gamma(q)=\{7\};\\
&v_3(w_x)\le1,\ v_p(w_x)\le1
\quad(x\in D(q),\ p>3\text{ odd})\}.
\end{aligned}}
\]
这是本轮的 precise necessary B7 definition，不是把 prompt 中的候选文字直接用作定义。

由于 admitted \(x\) 自动满足 \(v_2(w_x)\le1\)，此类的 **每个 exact order \(w_x\) 实际上全部 squarefree**。这不是要求 \(x-1\) squarefree。

更强的定义
\[
\mathcal B_7^{edge}=\{q\in\mathcal B_7:
 \{x\in D(q):3\mid w_x\}=\{7\}\}
\]
禁止其他节点有直接指向 3 的边。它只是额外限制；源 exactly-seven 证明没有证明这一更强必要性。本报告没有静默把二者等同。

实际 regular example 是 \(w_{43}=42=2\cdot3\cdot7\)，\(w_7=6\)。它的 basal gateway 只有 7，却有 \(43\to3\) 和 \(7\to3\) 两条直接边。§10 给出的真实共享 residue skeleton 也证明这种附加 3-guard 与同一个头部 branch 的中心配置并不冲突。

若维护者坚持把源 shorthand 解释为 \(\mathcal B_7^{edge}\)，必须单独修补 “exactly-seven implies this stronger class” 的证明。仅证明较强子类为空，不足以自动推出总界八。本轮采用较大的、已被证明为必要的 basal 类，避免这种缩窄漏洞。

### 2.3 Intrinsic root conditions 与 certificate conditions

上述定义只谈单个 root 的算术 closure。完整七根证书还要求：proper descendants 是 panel 中实际 active helpers；每个 helper 接受 valuation 1；incoming cylinders 位于它的固定中心；lower guards 可兼容；七个 basins 不共享 admitted row。不能把这些 whole-ledger 条件定义成孤立整数 q 的“已完成证书”。

Prime-order chain、intermediate logarithms 全取 0、特定的三枚 depth-three heads，均是 source 条件构造的简化，不是全部 B7 必要条件。

## 3. EXACTLY-SEVEN DEPENDENCY RECONSTRUCTION

源资料的逻辑链如下；不是从 finite inventory 或 Hall circuit 大小直接推断。

**Boundary。** 选择同一 \(c_*\)：\(r_2\equiv0,1(4)\) 时取 1，\(r_2\equiv2,3(4)\) 时取 0。该 anchor 的每种 exponent parity 分别有 sound two-adic safe lift。再选使 row 3 inactive 的 parity。Complete certificate 因而迫使此 fixed-anchor/fixed-parity odd subsystem complete。

**Original resources。** 每个 nonempty original rigid event 给至多一个 seed，并来自 \(s_q\ge2\) 的 original prime。Dynamic row 的 parity-shell bundle 排除中心。Macro 不是新 prime；固定 U 不因 muting 或 contraction 重算。

**Sparse exact elimination。** 在 \(r<p\) 个 proper p-cylinders 下，dynamic bundle 加这些 cylinders 能 full-cover，当且仅当有 accepted shell 0 和 centered depth-one seed。每个 seed 只有一个 child，继承实际 helper 的完整 lower order guard；CRT intersection 的 modulus 是 LCM，不能减掉未消去的 order factor。

**六根不可能。** 独立 seven-prime proof 在 \(N\le6\) 时精确消去所有 \(p\ge7\)。剩余 rank 3 的 shallow helpers 只给 \(2/3+2/9=8/9\)；更深 ternary leaf 要至少七叶。Rank 5 的所有 nonlinear alternatives 加 lower seeds 至多给两个 proper 3-cylinders，仍不完整。Blocker Phase B K2 另给 guard-routing 证明。这个界是 total \(N\ge7\)，不是每个最小 Hall-deficient subset 都有七根。

**\(N=7\) 的其他首 rank。** Phase C cross-strip lemma 使用同一组实际 helpers 7/31 与 11/71 的 fixed guards。Rank 5 全部 alternatives 的上界为 1、2、4，residual 最多 3、3、4 个 proper ternary cylinders，无法填补 outside-A3 branch。Rank 7 必须用尽七个来源；计入可能 simple-pair clause 后，residual 仍最多两个 proper lower cylinders，不能 complete。

**唯一前沿。** 首次 essential nonlinear rank 为 3。浅层质量迫使 depth ≥3，七叶 tree tax 迫使 depth ≤3。故 profile 为
\[
(2,2,3).
\]
Depth-one heads 必为 7、31；depth-two 必为 19、5167；depth-three 从
\[
\{163,271,487,4159,31051,16018507\}
\]
选三个不同 heads。仅后者有 20 种组合，绝不是只有一个固定 H0。

**整个 DAG。** 七个来源全都 surviving rigid，所以 proper helper 不能再是其中任何 nonregular root。Guard inheritance 强制所有 proper descendants regular、实际存在；order 在 3 以上 squarefree，3-depth 不超过对应 leaf depth。共享 descendant 会共享 basal gateway 的 fixed ternary cylinder，与 irredundant shallow frontier 冲突。因此七个 \(D(q)\) 两两不交。

**导出 B7。** 取 7-headed depth-one leaf 的来源 q。全部 basal gateways 的 3-depth ≤1，完整分解仅允许 7 或 31。31 是另一片已占据的 first leaf，其 fixed guard 不能包含当前 disjoint leaf，故不在本 basin。至少有 head 7，因此 \(\Gamma(q)=\{7\}\)，得到 q∈B7。

## 4. ORDER-PREIMAGE TREE OF 7

### Theorem D1 — Exact-order prime preimages

对固定 \(n\ge1\)，所有 exact-order preimages 满足
\[
\operatorname{ord}_p(5)=n\Longrightarrow p\mid\Phi_n(5),\quad p\nmid n.
\]
反过来，\(p\mid\Phi_n(5)\) 且 \(p\nmid n\) 时，\(\operatorname{ord}_p(5)=n\)。

前向：p 只可能出现在 \(5^n-1\) 中的第 n 个分圆因子，否则有更小 order。反向：在 characteristic p 且 p∤n 时，\(X^n-1\) separable，不同 cyclotomic factors 的 roots 不相交。可用检查 \(5^n=1\) 和 \(5^{n/\ell}\ne1\)（每个 prime \(\ell\mid n\)）独立认证。

因此每个 exact-order 层是某个明确整数的有限 prime-divisor set。有限分支不等于有限总深度。

特别地
\[
\Phi_7(5)=19531
\]
为 prime，所以 strict prime-order chain 第一条延伸强制
\[
7\longrightarrow19531,\qquad w_{19531}=7,\quad s_{19531}=1.
\]
进一步的 strict chain endpoint 必须是 \(\Phi_{19531}(5)\) 的 admitted primitive prime factor；nonregular endpoint 要求其平方整除该数。本轮未完成此 13,651 位整数的整体分解或 square-factor 判定。

### Theorem D2 — 完整 first-basin-extension 分类

设 q∈B7，并令 \(r=\min(D(q)\setminus\{7\})\)。因为每个 >3 admitted 节点都有 basal descendant，而唯一 basal 是 7，故 7 是 D(q) 的最小节点。

r 的任何 odd order factor >3 必须为 7。其 odd support 不可能只有 3，否则 r 是另一个 basal gateway。再用 squarefree orders，得到
\[
w_r\in\{7,14,21,42\}.
\]
四个完整因式分解：
\[
\begin{array}{c|l}
n&\Phi_n(5)\\\hline
7&19531\\
14&29\cdot449\\
21&379\cdot519499\\
42&7\cdot43\cdot127\cdot7603
\end{array}
\]
所有所列因子均为经证明的不同 primes。过滤 admission 和 exact order：
\[
\begin{array}{c|l}
w_r&\text{admitted primitive }r\\\hline
7&19531\\
14&\varnothing\\
21&379,\ 519499\\
42&43,\ 127,\ 7603.
\end{array}
\]
其中 7 虽整除 \(\Phi_{42}(5)\)，却只有 order 6，必须剔除。

故 \(r\in A_7\)。这些 factors 在相应 \(\Phi_n(5)\) 中均只出现一次，故 r regular。q nonregular，所以 r≠q。于是
\[
\boxed{|D(q)|\ge3,\quad |D(q)\setminus\{q\}|\ge2.}
\]
这是对任意 prime 大小、任意 basin 深度和 branching 的定理，不是 bounded prime enumeration。

### Corollary D2.1 — conditional total odd-row count

Exactly-seven 正常形的七个 disjoint basins 各至少包含一个 proper regular head；7-headed basin 现在至少还需要 A7 中的一个额外 proper regular row。因此至少有八个 regular rows >3。源 Theorem7.2 还强制实际 row3 存在；它 regular。加上七个 nonregular roots，得到
\[
\boxed{N=7\ \&\ \text{complete}\ \Longrightarrow
\text{至少16条 original odd rows，其中至少9条 regular}.}
\]
这是在 total nonregular count 恰好七的条件下的 total-row lower bound，**不是**把 nonregular 下界提高到八。

## 5. CYCLOTOMIC SQUARE-FACTOR ANALYSIS

### Theorem D3 — nonregularity 的准确平方条件

令 \(n=\operatorname{ord}_q(5)\)。q∤n，且 q 不整除任何 \(\Phi_d(5)\), d|n,d<n。因此
\[
s_q=v_q(\Phi_n(5)),\qquad s_q\ge2\iff q^2\mid\Phi_n(5).
\]

对于本轮的 squarefree \(n>2\)，若 odd prime \(\ell\mid n\) 整除 \(\Phi_n(5)\)，则它是 imprimitive 因子。写 \(n=\ell m\)，\(\ell\nmid m\)。LTE 给
\[
v_\ell(5^{\ell m}-1)-v_\ell(5^m-1)=1
\]
在 \(\ell\mid5^m-1\) 时成立；若该 divisibility 不成立则差为 0。因所有新 cyclotomic valuations 非负，总增量至多 1，故任一这种 imprimitive factor 在 \(\Phi_n(5)\) 中只出现一次。平方因子不会由这种 index prime 产生。2、5 也不产生这里的 admitted square resource。

### 不能使用的 derivative shortcut

对 primitive q∣Φ_n(5)、q∤n，恰有
\[
\Phi'_n(5)\not\equiv0\pmod q.
\]
这和 \(q^2\mid\Phi_n(5)\) **完全可以同时成立**：前者说模 q 的 polynomial root 是 simple；后者说整数 5 的固定 lift 恰好落在 mod q² 的 root 上。不能通过
\(\gcd(\Phi_n(5),\Phi'_n(5))\) 没有 q，推出整数 Φ_n(5) 没有 q²。Resultant/discriminant 只处理 root collision，不自动证明这些 integer values squarefree。

同样，primitive-divisor 存在性不产生 primitive **square** divisor。对 admitted prime p，Φ_p(5)≡3 mod4、Φ_p(5)≡1 modp，确保一个更大的 admitted exact-order preimage，但不确保其 nonregularity。任何无穷 squarefreeness 假设在本报告中均未被使用。

## 6. REGULARITY OF INTERMEDIATE RELAYS

除完整 factorization 证明外，逐项独立计算
\[
5^{w_p}\bmod p^2=1+k_pp,\qquad 0<k_p<p.
\]

| p | \(w_p\) | \(k_p\) | \(s_p\) |
|---:|---:|---:|---:|
|7|6|6|1|
|43|42|42|1|
|127|42|122|1|
|379|21|50|1|
|7603|42|2581|1|
|19531|7|4|1|
|519499|21|443642|1|

每个 exact order 再检查所有 prime divisors 的 order-drop tests。六个 A7 primes 的素性另用 trial division 检查，不借助 discovery factorization；全部因子的素性均有 recursive Lucas certificates。

注意 \(519499-1\) 含 \(7^2\)，但 \(w_{519499}=21\) squarefree。限制 order 的 multiplicities，不允许偷换为限制 prime-minus-one 的全部 multiplicities。

## 7. STRICT FINITE/ARITHMETIC SURVIVOR GATE

### Theorem D4 — 恰好三个 admitted vertices 的完整阶列表

若 q∈B7 且 \(D(q)=\{7,r,q\}\)，D2 给 \(r\in A_7\)。r 必直接整除 w_q，否则不可能从 q 到达 r；其余 odd factors 只能为 3、7。故
\[
\boxed{w_q\in I(r)=\{r,2r,3r,6r,7r,14r,21r,42r\}.}
\]
六个 r 的这 48 个整数互不相同。只需检查这些 Φ 值的 admitted primitive square divisors，不需要遍历 q≤某个界。

本轮的五个完整新分解为
\[
\begin{aligned}
\Phi_{43}(5)&=1644512641\cdot172827552198815888791,\\
\Phi_{86}(5)&=1549\cdot9547\cdot7866608083\cdot1628744948329,\\
\Phi_{127}(5)&=(5^{127}-1)/4=P_{89},\\
\Phi_{129}(5)&=18471511\cdot43955934961951833386625799\\
&\qquad\cdot51349797354047205216257689,\\
\Phi_{258}(5)&=327845761\cdot558801427\cdot1420986601\\
&\qquad\cdot236419892853700126919767791480523 .
\end{aligned}
\]
所有因子均经本地递归素性证书证明，且每个只出现一次。故这五个 exact orders 对所有 q 都不能给出 nonregular terminal。

特别地，\(D(q)=\{7,43,q\}\) 被严格压到
\[
\boxed{w_q\in\{301,602,903,1806\},\quad q^2\mid\Phi_{w_q}(5).}
\]

### B7* 的精确范围与“strict”的含义

令 F={7,14,21,42,43,86,127,129,258}。本轮所有 exactly-seven certificate 所需的 q 必满足：

- q∈B7；
- \(\min(D(q)\setminus\{7\})\in A_7\) 且这个最小节点是 proper regular relay；
- \(w_q\notin F\)；
- \(|D(q)|=3\) 时，\(w_q\) 落在 D4 的剩余 43-index list；r=43 时进一步落在四个上述 indices。

称带这些已认证 filters 的候选表示为 **B7***。Strictness 是在尚待检验的 order-DAG/root-order **候选表示域** 上：例如模板“regular 7、regular 43、待检验 nonregular q，w_q=43”此前满足结构限制，现在被无条件排除；而未判定的 w_q=301 模板保留。

不能错误宣称已经证明一个严格真包含的 actual-prime 集合 \(B7^*\subsetneq B7\) 同时又证明每个 B7 member 都在 B7*。作为真实整数集合，过滤后的集合与原集合相等，即 \(B7\cap\{\text{filters}\}=B7\)。研究上的严格进展是非空候选模板被删除，不是逻辑矛盾式的 actual-set properness 宣称。

### Depth 与 vertex count 不可混用

\(|D(q)|=3\) 的 48-index gate 不是全部 height-two B7。Height two 可以同时使用 A7 的多个 relays。令 \(R_0=\{7\}\)，由所有
\[
n=2^\epsilon3^a\prod_{p\in S}p,\quad
\epsilon,a\in\{0,1\},\quad\varnothing\ne S\subseteq R_j
\]
的 admitted primitive regular factors 递归扩充 \(R_{j+1}\)。每个阶段有限；以 admitted >3 edges 定义的有限高度 basin 均被其有限迭代捕捉。

第一层 \(R_1=\{7\}\cup A_7\)，共七个 regular vertices。全部下一层 orders 有 \(4(2^7-1)=508\) 种，包括已排除的四个 first-extension indices。48-index family 仅限制到两个 proper admitted vertices。没有为 508 个巨大整数的整体分解授权大型计算。

## 8. ORDER-CHAIN RIGIDITY AUDIT

如果 \(w_q=p\) 为 odd prime，admission 给
\[
q=1+2mp,\qquad m\text{ odd}.
\]
Odd order 要求 \((5/q)=1\)，因而 \(q\equiv11,19\pmod{20}\)；even order 则 \(q\equiv3,7\pmod{20}\)。这些是源 Kraft–Hall 中已有的约束，不冒充本轮新定理。

它们与实际 regular preimages 相容，不能仅靠排列 congruences 形成 impossibility。\(q^2\mid5^p-1\) 的必要补充是 lifting coefficient 真正为零，而不是把 q−1 中未出现在 order 的因子强制排除。

对唯一 strict prime-chain index p=19531，本轮另做一个有限 **divisor probe**：只测试
\[
q=1+2m\cdot19531,\quad 1\le m\le10000,\quad m\equiv5,9\pmod{10}.
\]
2000 个候选整数均不满足 \(5^{19531}\equiv1\pmod q\)。这一阴性结果只适用于该明确局部 divisor probe；不排除更大的 exact-order preimages，不证明 Φ19531 squarefree，不作为主要数学成果。

在 stronger edge-only 类中，第一 proper relay 确实只能是 19531。但这不能代替 basal B7 的六 relay 分类。

## 9. BASIN DISJOINTNESS AUDIT

B7 的 basal gateway 为 7。任意共享 admitted descendant x 也有 basal descendant 7；因此与它共享 x 的另一 root 必把 7 包含在自己的 closure 中。Exactly-seven 正常形已禁止这种情况，但没有额外算术定理迫使它发生。

不能把“所有 T(q) 都包含终端 3”误写成“basins 共享 actual relay row”。D(q) 特意排除了 terminal 3。共同终端是允许的。

31、19、5167 是强制 heads；271、4159、31051 只是 Theorem 12.1 选用的一个 depth-three triple，而不是全部七根证书唯一可选的另外三头。攻击固定 H0 的失败并不排除其他 19 个 triples。

更强的正面审计见下一节：任何 actual basal-B7 member 都可在 source 的 conditional construction 中替代 7-headed prime-order chain；与其余六条 CHAIN basins 的 disjointness 自动成立，因为它们的 basal gateway 各为另一个 h。故不能仅凭 branching 或额外 3-edges 判定 B7 无法与那六类 conditional basins 共存。

这不证明七个 nonregular roots 确实存在。结论只是：目前没有得到 coexistence impossibility。

## 10. 条件性 B7 BASIN FILLING：不限 prime-order chains

### Theorem D5 — arbitrary branching B7 fills one selected head guard

假设有 actual \(q\in B7\)，令 \(R=D(q)\setminus\{q\}\)。所有 R 中 primes regular，7∈R。CRT 选
\[
a\equiv4\pmod6,\qquad a\equiv0\pmod p\quad(p\in R).
\]
取所有 odd rows \(K=2,E=\{1\}\)，在 shared state 中设
\[
r_p=3+5^a\pmod{p^2}\quad(p\in R),\qquad
r_q=3+5^a+q\pmod{q^2}.
\]

**断言：** 这些 actual rows 在 anchor c=1 覆盖整个 \(d\equiv4\pmod6\) branch。

证明：对该 branch 中 d，若 R 中有 p 使 d≠a modp，取数值最小者。w_p 的每个 odd >3 factor 是 R 中更小的节点，故其坐标均等于 a；3 与 2 也已匹配。Squarefree order 给 w_p∣d−a，而 p∤d−a。Regularity/LTE 给 p-row valuation exactly 1。

若 R 的所有 own coordinates 均匹配，则 w_q∣d−a。Nonregularity 给 \(\operatorname{ord}_{q^2}(5)=w_q\)，所以 q-row 局部值为 q modq²，valuation exactly 1。证毕。

每个 proper relay p 都出现在某个上游 order 中，因此 induced U 包含它的 own p-digit。w7=6 提供 parity 和 3；K=2 下 U=L。各行 residue 通过 pairwise-coprime prime squares 的 CRT 合为一个 global residue；不存在每个 fiber 独立选 state 的偷换。

**源 Thm12.1 的替代版：** 若其余六个 heads \(31,19,5167,271,4159,31051\) 满足源 CHAIN，而 7-head 只要求一个 actual q∈B7，则上面的 branch filling 可以替代其 7-chain。其余 even branches、odd d 的 row3/head31 coverage、c=0 的 two-adic rejection 沿源证明保持成立。不同 basins 的 basal gateways 不同，因此不共享 admitted vertex。

这是新的条件性扩展，不是实际 complete certificate，也不是 B7 存在性证明。

### 实际 regular skeleton regression

实际 rows {7,43}，K=2,E={1}，a=1204，r7=33 mod49、r43=1428 mod1849。在 full period 1806 的 branch d=4 mod6 中，共有301个 exponents，300个被覆盖，唯一 hole 为1204。直接局部 modular masks 与 shell formulas 的3612次 row comparisons完全一致。

这个 skeleton 没有 nonregular root；不能把缺失的 root 当成已经存在。但它准确展示了为何 \(43\to3\) 的额外边不与 same-head guard alignment 冲突。

## 11. POSITIVE DIRECTION：实际 regular extension，不是 B7 member

本轮认证的 89 位素数为
\[
P_{89}=(5^{127}-1)/4
=14693679385278593849609206715278070972733319459651094018859396328480215743184089660644531.
\]
其 exact order 为 127，且
\[
5^{127}=1+4P_{89}<P_{89}^2,
\]
故 \(s_{P_{89}}=1\)。

完整 admitted DAG 为
\[
P_{89}\to127,\qquad127\to7,\quad127\to3,\qquad7\to3.
\]
Orders 为127、42、6，三个 s-values 全部1；T={3}，basal gateway 为7，所有 orders squarefree。它是实际、认证的 B7-compatible regular partial basin，**不属于 B7，因为顶端仍 regular**。

它也不是 \(7\to127\) 的 prime-order chain：127的order是42而不是7。较严格的 prime-order chain 已认证的 first step 仍是7→19531；更高 nonregular hit 未找到。

## 12. TARGETED EXACT COMPUTATION / INDEPENDENCE

`verify.py` 只用 Python standard library，不导入 SymPy、仓库实现或联网代码。

| 项目 | 本轮已执行 |
|---|---:|
|完整 cyclotomic products|11|
|recursive complete-(n−1) Lucas prime certificates|108|
|factor / exact-order / lifting records|26|
|first relay gate 的独立 trial-division primality|6|
|actual regular skeleton 的 direct row comparisons|3612|
|回归测试|14，全通过|
|strict-index19531局部 divisor probe|2000个候选整数|

Discovery 使用 SymPy 和 Cunningham 的 primary table；verification 使用另写的 integer product、divisor-recursion/Möbius 两种 Φ-value construction、recursive Lucas primality、exact-order drop tests、直接 modp²、重复乘法的独立 modular core。108 包括 certificate ancestry nodes，不是108个新的 B7 relays。26包括不同 Φ 值中的重复因子 occurrence，不是26个 distinct nonregular primes。

对Φ301、Φ602还读取了 primary table 给出的 factor/cofactor并验证整数乘积。但部分大因子的递归素性认证未完成，故只放入 `discovery_only_301_602.json`，**未**把301、602计入已排除 indices。外部 P 标签或本地 probable-prime 测试不替代本包要求的 certificate path。

同一研究者的两条验证路径不等于独立作者或独立研究团队。主验证不调用 discovery factorization function。

复现：
```bash
python verify.py --self-test
python verify.py --output fresh_results.json
```

## 13. ACTUAL B7 MEMBER FOUND?

```text
ACTUAL B7 MEMBER FOUND?
NO
```

已找到并认证的是 regular relays 和 regular partial basin；没有 actual nonregular terminal。没有将 formal root、conditional seed 或 prime-order compatible template冒充 actual prime。

## 14. B7 EMPTY? / DOES >=7 IMPROVE TO >=8?

```text
B7 EMPTY?
NOT PROVED

DOES >=7 IMPROVE TO >=8?
NO
```

如果以后证明本报告完整 necessary basal-B7 类为空，或证明其无法与任何允许的其他六个 basins 共存，则 exactly N=7 不可能。结合源 total N≥7，即得 total N≥8。

不需要额外证明 N>7 时不能出现局部七来源 witness；总数恰好七被排除就足够。但本轮只排除了有限结构/阶层，既未排除所有B7，也未证明一般共存不可能，所以没有这个升级。

B7 的全局未判定不来自简单“扫描范围不够”：缺口是 unbounded regular order closure 上是否会出现满足 exact square divisibility 的首个 nonregular root。任意长 admitted chains 的存在不解决 square hit 问题；有限 branching 也不给统一高度界。

## 15. STRONGEST NEW ARITHMETIC NECESSARY CONDITION

任何 exactly-seven complete certificate 必须含某 q，使：

\[
q\in B7,\quad r=\min(D(q)\setminus\{7\})\in
\{43,127,379,7603,19531,519499\},
\]
\[
r\ne q,\quad s_r=1,\quad |D(q)|\ge3,\quad
w_q\notin\{7,14,21,42,43,86,127,129,258\}.
\]

如果 \(|D(q)|=3\)，则 root order 在附带 JSON 的43个剩余 indices 中；r=43 时只能是301、602、903、1806，且 q²必须整除相应 Φ-value。

这是 derived arithmetic filter，不声称上述 remaining orders 中实际存在 nonregular root，不声称所有更大 basins 已有限枚举。

## 16. NEXT SINGLE TARGET

**完整判定最小分支 \(D(q)=\{7,43,q\}\) 的四个残余 cyclotomic square-factor cases：**
\[
\Phi_{301}(5),\quad\Phi_{602}(5),\quad
\Phi_{903}(5),\quad\Phi_{1806}(5).
\]

先完成301、602现有 factor/cofactor 的递归素性或可独立重放的证书，再处理903、1806；每个因子必须精确区分 primitive、admitted和s-value。成功将关闭或实例化一个完整三顶点 arithmetic subclass；即使该分支全部关闭，也不能宣布全部 B7 空。

此 target 是48-index theorem中的一个完整分支，不是盲目扩大q_max。没有启动全部508-index family，也没有授权大型生产计算。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
