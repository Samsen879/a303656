# A303656 C=1 CLOSED-STATE SQD — TARGETED PHASE F

## 0. Executive verdict

本轮证明一个 exact-state **no-migration theorem**，并给出一个正确的、但一般不严格的 canonicalization theorem。它们不是 general B7 → three-vertex 的证明。

核心结果，在下文明确独立定义的 basal-B7 regular closed-state 类中，是

\[
 R\ne T\quad\Longrightarrow\quad \gcd(Z_R,Z_T)=1.
\]

因此，若实际有 \(q^2\mid Z_R\)，同一个 q 在任何不同 exact closed state 上连一次整除都不能保留。这个结论不依赖 R、T 的大小，不依赖某个 prime cutoff，也不依赖大整数整体分解。

另一方面，令 \(P_B=\prod_{p\in B}p\)，则有精确恒等式

\[
 \frac{5^{6P_B}-1}{(5^6-1)P_B}
 =\prod_{\substack{\varnothing\ne T\subseteq B\\T\text{ good closed}}}Z_T,
\]

右侧因子两两互素。一个 ambient square hit 可以唯一投影到其 canonical support state，但该 state 完全可能就是 B 本身。不能把此 non-strict projection 偷换成 strict cost descent。

**没有证明 SQD-root 或 SQD-cost；没有找到 actual base-5 B7 root；没有得到 actual base-5 反例；没有把 minimal B7 member 压到 three-vertex。**

## 1. LIVE AUTHORITY / SOURCE BOUNDARY

```text
Repository: Samsen879/a303656
main SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
main tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
HEAD: Merge PR #29 — seven-head chain realizability, Phase D
HEAD time: 2026-09-08T03:37:01Z
GITHUB WRITES: NONE
```

通过 GitHub connector 实际读取 pinned main 的 B7 Phase D 报告、Provider Phase D 相关段落、STATUS、目录和 branch metadata。STATUS 是 PAUSED / NONE / UNRESOLVED。

**关键缺口：本轮运行目录仅实际收到 `分工规则.txt`、`项目简介.txt`。所要求的三个 Phase E ZIP 没有挂载；本轮没有取得 Phase E Branching 的原始 source payload。**

所以：下文不是“已逐符号核对 Phase E 的 source reconstruction”。它是从已读取的 Phase D basal-B7 定义出发，独立给出的 exact-closure reconstruction，并附完整证明。其数学结论在此明确类中成立；将同名符号对接 Phase E 原包，还必须核对定义、normalizer、scope 与 provenance。本轮不使用跨会话摘要充当源文件，不把任务中的 shorthand 当作已验证定理。

没有取得完整本地 checkout；没有重跑 repository tests、历史大型 prime inventories 或全部 Phase D/C 辅助文件。独立 raw-byte 下载尝试遭 DNS 失败，未用于任何 source-hash 验证。代码为本会话新写的 Python reference，不宣称跨作者或独立软件栈复现。

### Source-derived baseline

Phase D 使用

\[
 w_x=\operatorname{ord}_x(5),\qquad
 s_x=v_x(5^{w_x}-1),\qquad
 O(x)=\{p:p\text{ odd prime},\ p\mid w_x\}.
\]

Regular 是 \(s_x=1\)，nonregular 是 \(s_x\ge2\)。admitted vertices 是 \(x>3\)、\(x\equiv3\pmod4\) 的 primes。沿全部 odd order factors 递归展开；terminal 3 不计入 D(q)，而 1 mod 4 primes 是其他 terminals。

Basal gateway 是

\[
 \Gamma(q)=\{x\in D(q):O(x)=\{3\}\}.
\]

B7 要求 root nonregular、所有 proper admitted descendants regular、\(T(q)=\{3\}\)、\(\Gamma(q)=\{7\}\)，并要求全部 exact orders squarefree。它**没有**要求除 7 外不能直接有指向 3 的边。例如 \(w_{43}=42\) 合法。

Phase D 已给出 six first relays

\[
 \{43,127,379,7603,19531,519499\},
\]

three-vertex 的 48-index gate，以及 \(|D(q)|\ge3\)。本轮重验了第一层小整数；没有冒称复核 Phase E 对 301、602 等进一步关闭的 certificates。

## 2. CLOSED-STATE THEORY RECONSTRUCTION

本节的 J、W、Z、SqPrim 是本轮独立明确化的符号；不是假称已读取同名 Phase E 定义。

### 2.1 Good regular state and closure

称非空有限集合 R 是 good regular closed state，当且仅当：

- 每个 p∈R 是 admitted regular prime，且 w_p squarefree；
- 沿 odd order factors 的完整递归只有 terminal 3；
- R 对 admitted descendants 封闭；
- 它的 basal-gateway 集合恰为 {7}。

对位于一个 good state 内的 seed set S，定义 Cl(S) 为 S 及其全部 admitted descendants >3 的并集。特别地 Cl(∅)=∅。所有非空 good states 含 7；其中每个顶点均下降到 7。

令偏序 p≼v 表示 p∈Cl({v})。定义 A(R) 为 R 在这个偏序下的 maximal elements，而不是数值最大的单个元素。

### Theorem F1 — Unique minimal generating antichain

\[
 \operatorname{Cl}(S)=R
 \iff A(R)\subseteq S\subseteq R.
\]

证明：每个非 maximal 顶点位于某个 maximal 顶点的 descendant closure 中，故 Cl(A(R))=R。反之，若一个 maximal a 不在 S 中，则没有 R 中的另一顶点能向下生成 a，故 a 不在 Cl(S)。因此 A(R) 是唯一的 inclusion-minimal generating set，也是 antichain。证毕。

### 2.2 Exact indices and integer strata

写

\[
 P_R=\prod_{p\in R}p,\quad
 a_R=\prod_{p\in A(R)}p,\quad
 b_R=6\prod_{p\in R\setminus A(R)}p.
\]

定义

\[
 J(R)=\left\{n\mid 6P_R:
 \operatorname{Cl}(\{p>3:p\mid n\})=R\right\}.
\]

由 F1，等价于

\[
 J(R)=\left\{\delta\prod_{p\in S}p:
 \delta\in\{1,2,3,6\},\ A(R)\subseteq S\subseteq R\right\}.
\]

所有 n squarefree，且 \(|J(R)|=4\cdot2^{|R|-|A(R)|}\)。定义

\[
 W_R=\prod_{n\in J(R)}\Phi_n(5)
     =\Phi_{a_R}(5^{b_R}).
\]

最后一个等号是精确等号：因为 gcd(a_R,b_R)=1，且两数 squarefree，\(\Phi_{a_R}(X^{b_R})=\prod_{d\mid b_R}\Phi_{a_Rd}(X)\)。

定义

\[
 \epsilon_R=\begin{cases}p,&A(R)=\{p\},\\1,&|A(R)|\ge2,\end{cases}
 \qquad Z_R=W_R/\epsilon_R.
\]

后文证明这个 quotient 整数恰好删除全部 imprimitive contribution，而不删除任何 primitive contribution。

为避免 SqPrim 的不同输入约定，本报告显式使用

\[
 \operatorname{SqPrim}_5(n)=\{q\text{ prime}:q\nmid 5n,\ q^2\mid\Phi_n(5)\},
\]

以及 admitted hit set

\[
 \mathcal H(R)=\{q:q\equiv3\pmod4,\ q\in\operatorname{SqPrim}_5(n)
                  \text{ for some }n\in J(R)\}.
\]

## 3. UNIQUE-INDEX LOCALIZATION AND PRIMITIVE NORMALIZATION

### Lemma F2 — Squarefree-index cyclotomic valuation

对于 odd prime ℓ≠5 和本报告的 squarefree n>2：

- ℓ∤n 且 ℓ∣Φ_n(5)，当且仅当 ord_ℓ(5)=n。
- ℓ∣n 且 ℓ∣Φ_n(5)，当且仅当 n=ℓ·ord_ℓ(5)；此时 v_ℓ(Φ_n(5))=1。

第一条由 characteristic ℓ 下 X^n−1 的 separability 得到。第二条可写 n=ℓm，使用

\[
 \Phi_{\ell m}(X)=\frac{\Phi_m(X^\ell)}{\Phi_m(X)},\qquad \ell\nmid m,
\]

以及模 ℓ 的 \(\Phi_{\ell m}(X)\equiv\Phi_m(X)^{\ell-1}\)，先得 ord_ℓ(5)=m，再用 LTE 得 valuation 增量恰为 1。等价地，从 \(v_\ell(5^{dk}-1)=s_\ell+v_\ell(k)\)，d=ord_ℓ(5)，在 cyclotomic factorization 中取 valuation 即可。

这些 J(R) indices 都有 >3 的 odd support。2 仅能在相应 2-power indices 产生问题，3 仅能在 2 或 2·3^j 处出现，5 不整除这里的 cyclotomic values，故三者均不会留在 W_R 中。

### Theorem F3 — The only imprimitive contribution

若 ℓ 是 W_R 的 imprimitive divisor，则存在 n∈J(R)，满足

\[
 n=\ell w_\ell.
\]

n 的 >3 support 是 {ℓ} 加上 ℓ 的 direct admitted order factors。它的 closure 因而就是 Cl({ℓ})。由 n∈J(R)，得到 R=Cl({ℓ})，所以 A(R)={ℓ}。

反过来，若 A(R)={p}，则 R=Cl({p})；n=pw_p 确实属于 J(R)，且 p 在 Φ_n(5) 中恰出现一次。没有第二个 imprimitive index，因为 w_p 唯一。

因此 W_R 的完整 imprimitive contribution 正是 ε_R。每个 Z_R 的 prime divisor q 都有唯一 index

\[
 n=w_q\in J(R),\qquad q>n\ge\max R.
\]

特别地

\[
 q^2\mid Z_R\iff q^2\mid\Phi_{w_q}(5),\quad w_q\in J(R).
\]

这排除了“q 在两个不同 cyclotomic values 中各出现一次，从而拼出 q²”的可能。

### Theorem F4 — Exact root iff, including its scope

对 good regular closed R 和 prime q，

\[
 \boxed{q\in\mathcal B_7\ \&\ D(q)\setminus\{q\}=R
 \iff q\equiv3\pmod4\ \&\ q^2\mid Z_R.}
\]

证明：左向令 n=w_q。它 squarefree，且其 >3 support S 的 closure 正是 R，所以 n∈J(R)。q∤n，故 nonregularity 恰为 q²∣Φ_n(5)，也即 q²∣Z_R。

右向由 F3 得唯一 n=w_q∈J(R)，且 q>max R。于是 q 的全部 proper admitted descendants 恰是 R；R 的 regularity、squarefree orders、terminal 与 basal-gateway 条件都被继承。q 本身的 order 含 >3 support，不是新增的 basal gateway，并且 q nonregular。故 q∈B7。证毕。

**这里是“proper descendant set 恰好等于 R”，不是“包含在 R 中”或“q 出现在某个覆盖 R 的 ambient state 中”。**

### Theorem F5 — Disjoint exact index strata

若 R≠T，则 J(R)∩J(T)=∅。因为任何 n 的 support closure 都唯一，不可能同时等于两个不同 state。

### Theorem F6 — Pairwise coprimality across every distinct state

\[
 \boxed{R\ne T\ \Longrightarrow\ \gcd(Z_R,Z_T)=1.}
\]

证明：共同 prime q 将由 F3 给出同一个唯一 index w_q，因而 w_q∈J(R)∩J(T)，与 F5 矛盾。证毕。

这个定理不只适用于 nested substates。

固定 R 内，甚至未归一化的不同 Φ_n(5)、n∈J(R)，也两两互素。一个共同 divisor 若在两处都 primitive，会有两个不同 exact orders；若在一处 imprimitive，则 A(R)={q}，另一处 primitive index w_q 不含 q，因此不属于 J(R)；两处均 imprimitive 时 index 同为 qw_q。三种可能都不能给出两个不同 indices。

## 4. Z_R VS Z_R' FACTORIZATION

### 4.1 Proper deletion loses all exact-state indices

对于 proper good T⊊R，

\[
 J(T)\cap J(R)=\varnothing,\qquad \gcd(Z_R,Z_T)=1.
\]

所以 J(T) 不是 J(R) 的非空 subset。把 Z_T 当作 Z_R 删除若干 cyclotomic factors 后的余积是错误的。

更精细地，未归一化的 W 满足

\[
 \gcd(W_R,W_T)=
 \begin{cases}
 p,&A(R)=\{p\},\ T=R\setminus\{p\},\\
 1,&\text{otherwise}.
 \end{cases}
\]

理由：共同 divisor 只能是 R 的 singleton normalizer p；它在较低 state 中的 primitive order 为 w_p，其 support closure 必须是 R\{p}。p regular，所以在较低层也只出现一次。除去 normalizer 后这一重叠消失。

例子：R={7,43}，T={7}。此时

\[
 W_T=\Phi_7(5^6),\qquad W_R=\Phi_{43}(5^{42}),
\]

\[
 \gcd(W_R,W_T)=43,\qquad \gcd(W_R/43,W_T/7)=1.
\]

这个 43 不是可保留的 nonregular resource。

### 4.2 The correct cumulative factorization

定义 ambient integer

\[
 V_B=\frac{5^{6P_B}-1}{(5^6-1)P_B}.
\]

### Theorem F7 — Canonical stratum factorization

\[
 \boxed{V_B=\prod_{\varnothing\ne T\subseteq B,\ T\text{ good closed}} Z_T.}
\]

证明：6P_B 的 divisors 中不整除 6 的那些，恰是 δ∏_{p∈S}p，其中 S 是 B 的非空 subset。按唯一 Cl(S)=T 分组，得到

\[
 \frac{5^{6P_B}-1}{5^6-1}=\prod_T W_T.
\]

每个 p∈B 恰好对应一个 principal closed state Cl({p})，其唯一 generator 是 p。因此 ∏_T ε_T=P_B。除去这些 normalizers即得公式。F6 证明右侧两两互素。证毕。

所以 T⊆B 时 V_T∣V_B，且

\[
 V_B/V_T=\prod_{U\subseteq B,\ U\not\subseteq T,\ U\text{ good closed}}Z_U.
\]

对于不同 good B,C，还可得 gcd(V_B,V_C)=V_{B∩C}。

**V 的包含单调性与 Z 的分层互素性可以同时成立；不能混用。**

### Corollary F7.1 — Valid non-strict square-hit canonicalization

若 admitted q²∣V_B，则存在唯一 good T⊆B，使 q²∣Z_T。该 T 是 ord_q(5) 的 >3 support closure；保留的是同一个 actual q 和同一个 actual square hit。

但 T=B 完全没有被排除。若已知 q²∣Z_B，则 F6 更说明，对每个 proper good T⊊B 都有 gcd(q,V_T)=1。即：到达 exact state 后，nonstrict canonicalization 已无可继续的同根下降。

## 5. SQD-STRONG / SQD-ROOT / SQD-COST / SQD-CRITICAL

取 basin cost c(R)=|R|；root basin 的 admitted vertex count 为 1+c(R)。

### 5.1 First repair the stopping rule

若将 SQD-root 或 SQD-cost 按字面要求用于**每个** hit state，而不指定 terminal class，则在 B7 非空时，选择最小 cost hit state 就立刻矛盾。因此无 terminal 的全称 strict descent 已经蕴含 B7 为空，不是一个可以无条件反复运行的算法。

有效的 three-vertex 目标应只要求 |R|>2 时下降，在 |R|≤2 停止。由于 Z_{ {7} } squarefree，真实 stop 实际只能是 |R|=2。

### SQD-STRONG

修正版：若 |R|>2 且 q∈H(R)，则存在 proper good T⊊R，使同一个 q∈H(T)。

**反向定理已证明：** 对每个实际前提 witness，所有不同 T 都有 q∤Z_T。故这样的转移绝无可能。

逻辑精度：本轮没有 actual base-5 high-cost hit，因此不能声称已经给出反驳这个全称蕴含式的 actual base-5 counterexample。这个全称命题有可能仅因所有 high-cost antecedents 为空而为真。事实上，修正版 SQD-strong 等价于“所有 B7 roots 都是 three-vertex”，比“存在一个最小 three-vertex root”强得多。

无 stopping rule 的 literal SQD-strong 则等价于 B7 为空。

### SQD-ROOT

修正版：若 |R|>2 且 H(R)非空，则存在 proper good T⊊R，使 H(T)非空，允许更换 root。

尚未证明，也未给出 actual base-5 反例。F6 不反驳更换 prime 的存在性，但说明较小 state 的 hit 必须来自完全不同的 primitive prime stratum。

此修正版等价于：**每个 hit state 内都包含一个 hit-bearing two-vertex closed substate**。正向用有限 descending chain；反向直接选该 two-vertex substate。它不是 closure antichain 的自动推论。

### SQD-COST

修正版：若 |R|>2 且 H(R)非空，则某个 good T（不必 T⊂R）满足 |T|<|R|、H(T)非空。

它等价于

\[
 \mathcal B_7\ne\varnothing
 \Longrightarrow \exists q\in\mathcal B_7:\ |D(q)|=3.
\]

正向选择最小 cost hit；反向让那个 cost-two hit 为所有更大 states 提供较小目标。因此此 global version 实质上是目标 reduction 的重述，不能当作免费 lemma 使用。

### SQD-CRITICAL

同一个 q 的 smaller-index square hit 被 exact-order uniqueness 禁止。对于不同 q'，一般 cyclotomic identities 不给出存在性。

此外 m<n、甚至 m∣n 且 m<n，也不保证 basin cost 下降。如果只删除 δ 中的 2 或 3，或删除 direct support S\A(R) 中的一个 nonmaximal vertex，support closure 可以仍等于 R。

一个真正可用于目标的版本至少还须要求

\[
 T=\operatorname{Cl}(\{p>3:p\mid m\})\subsetneq R,
\]

或另行认证 |T|<|R|，并要求 T 为 good regular state、q' 为实际 admitted primitive square divisor。此 strengthened version 未证明。

## 6. MAXIMAL-GENERATOR ANALYSIS

若 |R|>1，R\{v} 仍为 good closed state，当且仅当 v∈A(R)。因为 non-generator 顶点由剩余 maximal generators 强制生成；而删除 maximal vertex 不会破坏任何其他顶点的 descendant closure。

所以“删除一个 non-generator vertex 但保留所有 maxima”不是合法 closed-state 删除。删除 generator 又会删除所有 J(R) indices，因为每个 exact-state index 都包含该 generator。

对于 square-hit support S，定义本身已给 Cl(S)=R。这不是需要额外证伪的偶发障碍，而是 exact stratum 的必然性质。

即使将来能证明 square hit 强迫 S=A(R)，依然 Cl(A(R))=R，不能由此得到较小 state。若要更换 root，所需的是独立的跨 stratum square-hit existence theorem，而不是再缩短同一个 generating antichain。

## 7. CYCLOTOMIC DESCENT

经典 identities 是

\[
 \Phi_{mp}(X)=\Phi_m(X^p)/\Phi_m(X)\quad(p\nmid m),
\]

及 \(\Phi_{mp}(X)=\Phi_m(X^p)\)（p∣m）。它们在整数代入后并不把 numerator 的 primitive square divisor 传给 denominator。

### Small exact general counterexample

\[
 \Phi_6(19)=19^2-19+1=7^3,\qquad \operatorname{ord}_7(19)=6.
\]

而 proper divisor indices 给

\[
 \Phi_1(19)=18=2\cdot3^2,\quad
 \Phi_2(19)=20=2^2\cdot5,\quad
 \Phi_3(19)=381=3\cdot127.
\]

没有一个 proper-divisor value 有 admitted prime q'>3、q'≡3(4) 的平方。这里 q=7 是实际 primitive square divisor，但任意不同 admitted root 的 proper-divisor square descent 也失败。

n=6 是最小 squarefree composite index；对 n=6，程序穷尽检查 2≤a<19，确认 19 是产生此类 admitted primitive square hit 的最小 base。**该最小性只指上述明确定义的 toy domain。**

这是一般 cyclotomic SQD-critical 的 exact counterexample，**不是 base-5 B7 state，也不反驳带 B7-specific 额外假设的版本**。

## 8. COUNTEREXAMPLE SEARCH / EXACT REFERENCE

### 8.1 Base-5 bounded domain

范围：全部 admitted regular vertices p≤1,000,000；枚举此 vertex universe 中全部非空 good closed states，|R|≤4。root/primitive factor 搜索另限制 q≤1,000,000。

| quantity | exact result |
|---|---:|
| good regular vertices | 25 |
| vertices whose own closure has size ≤4 | 23 |
| size-one states | 1 |
| size-two states | 6 |
| size-three states | 24 |
| size-four states | 79 |
| total states | 110 |
| distinct exact indices | 1532 |
| cross-state index collisions | 0 |
| fully instantiated integer states | 8 |
| numerical pairwise Z gcd checks | 28 |
| numerical raw W deletion-gcd checks | 11 |
| cumulative V partition checks | 8 |
| admitted primitive square hits q≤10^6 in these states | 0 |

所有 state 的 A、J、所有 proper good substates、bounded primitive factorization 与完整性状态记录在 `results/states.json`。

只有 R={7} 在本轮获得 Z_R 的完整分解。其余材料是 partial factorization 或 symbolic exact representation；绝不把空的 bounded square-hit 列表解释成 squarefree certificate。|R|≤4 不是对无界 vertex labels 的穷尽。

R={7} 的完整结果是

\[
 Z_{\{7\}}=29\cdot43\cdot127\cdot379\cdot449\cdot7603\cdot19531\cdot519499
 =2078978087221418143138393.
\]

八个因子都是不同 primes。因此 base-5 B7 的 proper regular state 至少两个顶点；这是 lower bound，不是 upper bound。

例子：

- {7,43}：A={43}，J={43,86,129,258,301,602,903,1806}。
- {7,43,127}：A={43,127}，J={5461,10922,16383,32766,38227,76454,114681,229362}。
- {7,43,9547}：A={9547}，|J|=16；这是实际 chain state，不是抽象标签。
- {7,43,127,379}：A={43,127,379}，|J|=8；数据是 symbolic/partial，不宣称整体分解。

q≤10^6 的两个 admitted base-5 nonregular primes 是 20771 和 40487，其 orders 分别是 5·31·67 与 2·31·653。前者有 forbidden terminal 5，后者有 forbidden terminal 653；31 也是错误 basal gateway。两者均不提供本任务的 B7 square-hit。

### 8.2 Actual arithmetic toy above the terminal threshold

将 base 5 改为 a=3589，保留相同 admission、squarefree-order、regular descendants 与 basal-gateway 条件，有实际 root q=863：

| p | ord_p(3589) | 3589^order mod p² |
|---:|---:|---:|
|7|6|22|
|43|42|173|
|431|86|116802|
|863|862|1|

所有 p 是 primes；前三者 regular，root nonregular。

\[
 R=\{7,43,431\},\qquad A(R)=\{431\},\qquad
 863^2\mid\Phi_{862}(3589).
\]

n=862 的 prime order-drop checks 是 3589^431≡862 mod863、3589²≡646 mod863，均非 1。所有 proper good substates 恰是 {7}、{7,43}。同一个 q 在这两者都没有 primitive hit。因此这是**真实换底数算术中的 SQD-strong 反例，且 |R|=3 高于 cost-two stop**。

它不是 actual base-5 反例；也没有证明其较小 states 不含其他 q' 的 square hit，故不冒充 SQD-root 的反例。未声称它是跨所有 bases、所有 roots 的绝对最小例子。

### 8.3 Abstract marked-index test

实际 base-5 regular skeleton R={7,43,127}、A={43,127} 上，给 n=5461 一个 abstract square-hit mark，其余 indices 不标记。所有 closure、antichain、unique-index 性质都保持，但较小 states 没有 mark。

没有给任何 actual prime q 赋值，没有证明 5 的任何新 Wieferich congruence。这个实验只说明纯 closure/mark 组合论不自动提供更换 root 的 square-hit；它不是 actual arithmetic counterexample，也不是对完整数论理论的 formal independence proof。

## 9. MINIMAL B7 ROOT ARGUMENT

假设 B7 非空，选择 c(R)=|R| 最小的 root。R={7} 已排除，所以 |R|≥2。

若 |R|>2，确实存在 removable maximal vertex；但 F6 证明原 q 在删后的 state 必定消失。没有另一个 q' 的存在定理，极小性无法产生矛盾。

所以当前只能得到 |D(q)|≥3，不能得到 minimal |D(q)|=3。选 lexicographic (|R|,max R,bit length Z_R) 也不会改变这一缺口：exact-order localization 不生成另一个 prime。

## 10. CERTIFICATE-SPECIFIC SQD / PROVIDER / O31

### 10.1 What the verified Provider source actually supplies

Phase D 给的是 actual dynamic-helper ancestry、basin support confinement、fixed-shadow width capacity。exactly-seven 正常形是 seven obligations 对 seven unit-capacity basins，deficit=0。它没有给出每个 basin 的 vertex-count upper bound，也没有给出 replacement root 的 nonregularity。

原 q 固定时，其 arithmetic order factors 和完整 descendant closure 也固定。删除某个 guard occurrence 或 ambient 不使用的 regular row，不等于删去 D(q) 中一个实际强制 descendant。

### 10.2 Disjointness alone gives no new banned B7 branch

若 R 为 good B7 regular state，而另一个 admitted descendant-closed basin C 不含 7，则 R∩C=∅ 自动成立。否则共同顶点 v 会迫使 C 包含 v 的 descendant 7。

因此仅靠“其他 basins 已经不能使用 7”，不能再推出 R 中某个特定 branching relay 不可用。额外排除必须来自确切的 shared residue/logarithm/guard constraints，而不是重复使用 disjointness。

### 10.3 Descent must preserve its own domain

证书专属下降还有第二个常被遗漏的 gate：若只对 certificate-derived B7 states 证明“存在一个更小的 arbitrary B7 hit”，这个更小 hit 未必仍是 certificate-derived，因而无法再次应用该专属定理。

要用 minimal-certificate argument，必须证明下列之一：

1. actual replacement root 与其 helpers 能嵌入一个新的完整 exactly-seven shared-state certificate，且 cost 严格下降；或
2. 从原 certificate 一次直接得到 cost-two actual B7 hit；或
3. 下降定理也适用于所有后续非 certificate-specific successors。

本轮没有证明上述任一项。

### 10.4 O31 boundary

任务给出的 “full-state iff O31” 在本轮不是已读取的原始 theorem。由于 Phase E Seven-Basin package 未提供，本轮没有替它增添额外约束，也没有假称复核其 scope。F6 对同一个 root 的 no-migration 依然适用于任何 certificate-derived exact state，因为它是整数本身的性质。

## 11. FINAL REPORT / VERDICT

```text
SQD PROVED?
RESTRICTED — non-strict ambient-to-canonical square-hit localization only.
No strict SQD-root, SQD-cost, or certificate-specific descent proved.

NAIVE SQD FALSE?
ACTUAL BASE-5 UNIVERSAL STATEMENT: NOT DETERMINED.
SAME-q TRANSITION ON ANY EXACT-STATE WITNESS: IMPOSSIBLE, proved.
ACTUAL DIFFERENT-BASE SQD-STRONG COUNTEREXAMPLE: YES.
GENERAL CYCLOTOMIC SQD-CRITICAL COUNTEREXAMPLE: YES.

MINIMAL B7 MEMBER THREE-VERTEX?
NO — not proved; this is not a proof that such a minimal member cannot exist.

DOES GENERAL B7 REDUCE TO THREE-VERTEX?
NO — no such reduction established.

ACTUAL BASE-5 B7 COUNTEREXAMPLE FOUND?
NO.

PHASE-E SOURCE RECONSTRUCTION FULLY VERIFIED?
NO — required source ZIP unavailable in this session.
```

`NAIVE SQD FALSE?` 不能在这里诚实地压缩成无 scope 的 YES/NO：若 B7 为空，该全称蕴含可能 vacuously true；no-migration theorem 本身不构造一个 base-5 B7 root。

### NEXT SINGLE TARGET

**CERTIFICATE-CLASS-PRESERVING ROOT REPLACEMENT，必须更换 actual prime。**

在取得并核对 Phase E Branching/Seven-Basin 原始 payload 后，只研究：一个 minimal exactly-seven complete shared-state certificate 的 B7 basin 若 |R|>2，能否构造一个 cost 更小、仍具完整 shared-state certificate 的 actual replacement root。不能以同一个 q、仅移除一个 vertex、抽象重新标记 square hits 或 pooled capacity 代替此结论。

本轮没有给这一目标通过 promotion gate；尤其没有为继续大规模分解或无界枚举提供新 gate。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
