# A303656 C=1 Cyclotomic Wieferich Terminal Family Obstruction — Phase E

## 0. Verdict / 推荐执行环境

推荐执行环境：网页端 GPT-5.6 Pro。任务为数学推导、反例审计与小模数 exact reference computation；不需要大型 prime scan 或 Codex Ultra。

**本轮没有新增排除任何 B7 root-order，没有证明某个六-relay 完整子族为空，没有建立 fixed-base-5 的 nonregular descent。** 得到的是：一个完整的局部等价定理、48 个分圆值的互素性与精确 index-prime 分类、六组统一的模 r² 因子平衡条件，以及对一种 base-uniform descent 的具体反例。

不能把这些结果评为目标 A 或 B。模 r² 条件作用于完整因子分解，不是指定 terminal q 的单独条件，尚不满足目标 C 的“显著缩小 terminal candidate family”。本轮否定了若干明确的局部推理，并不证明目标 D 中“所有整族策略不可能、只能逐 n factor”的更强断言。

所有新推导均为本会话提出的研究证明；有限算术由随包标准库程序重算。未进行独立作者审稿或 proof-assistant formalization。继承的 theorem 与本轮推导分别标注，不主张文献优先权。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Bound main SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
Bound main tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
main commit time: 2026-09-08T03:37:01Z
```

只读 GitHub connector 确认：

| PR | merged | merge commit |
|---:|:---:|---|
|26|true|07a6f5fb2059b1dfc6be7cc6d1325cd65b49ae41|
|27|true|a8e72c805c6a36d3e215507a4fcaad271147ce7e|
|28|true|8dcb744641a46b41597681b4eaddfd7b427d7280|
|29|true|fd59aad038a09f2fc6df7039111408fa231c27dd|

#27、#28、#29 的 base/merge metadata 顺次连接；#29 为当前 main；结束前重新 GET live main，SHA/tree 未变。固定 SHA 的 STATUS.md 仍为 PAUSED / NONE / UNRESOLVED。[S0]

**阅读范围限制。** 已读取并交叉对照五个指定目录的核心报告、Order-DAG 的 THEOREMS.md、B7 的 PROOF_AUDIT.md、相关 live PR metadata 与 STATUS。没有完成五个目录所有辅助代码、生成数据、日志的逐文件阅读，因此用户要求的“全部目录逐文件完整阅读”未完全达到，不能记录为 FULL PASS。没有本地完整 checkout，没有重跑 repository-native tests、CI 或 2×10⁹ inventory。源文件取自固定 SHA；未把旧报告自己的历史 SHA 当作当前 authority。具体路径和边界见 SOURCE_BINDING.json。[S1–S6]

## 2. DEFINITION OF W_5(n)

对 n≥1 定义

\[
W_5(n)=\{q\ne5:q\text{ prime},\ \operatorname{ord}_q(5)=n,
\ q^2\mid\Phi_n(5)\}.
\]

与 admitted 类分开定义

\[
W_5^{\rm adm}(n)=W_5(n)\cap\{q:q\equiv3\pmod4\}.
\]

不能用只排除 admitted factors 的结论，冒充整个 W_5(n) 为空。Exact order 已自动给出 n|q−1，因此 q∤n。后文 q-adic 主定理使用奇素数 q≠5；q=2 的例外另列。

## 3. EXACT-ORDER / CYCLOTOMIC EQUIVALENCE

### E1. 全部 index-prime 例外的 valuation 公式

令 ℓ 为奇素数，ℓ≠5，f=ord_ℓ(5)，s=v_ℓ(5^f−1)。则对所有正整数 n，

\[
v_\ell(\Phi_n(5))=
\begin{cases}
s,&n=f,\\
1,&n=f\ell^j,\quad j\ge1,\\
0,&\text{otherwise}.
\end{cases}\tag{E1}
\]

**证明。** LTE 给

\[
v_\ell(5^N-1)=
\begin{cases}s+v_\ell(N/f),&f\mid N,\\0,&f\nmid N.\end{cases}
\]

设右侧为 A(N)。从 5^N−1=∏_{d|N}Φ_d(5) 得 A(N)=∑_{d|N}v_ℓΦ_d(5)。E1 所列值的 divisor sum 在 f∤N 时为 0，在 f|N 时恰为 s+v_ℓ(N/f)，故由 divisor-sum inversion 的唯一性得到 E1。这里 f|ℓ−1，故 ℓ∤f。证毕。

由此 **imprimitive index prime 即使在 n 不 squarefree 时，也只以一次幂出现**；其平方不会产生本任务所需的 nonregular resource。源 Phase D 对 squarefree n 的讨论是该公式的子情形。[S1]

对 2 和 5，精确例外为

\[
v_2\Phi_1(5)=2,\qquad
v_2\Phi_{2^j}(5)=1\ (j\ge1),\qquad
v_2\Phi_n(5)=0\text{ otherwise};
\]

\[
v_5\Phi_n(5)=0\quad(n\ge1).
\]

前者由 5^N−1 的二进 valuation 和 divisor sums 得出；后者由 Φ_n(5) 的常数项模 5 得出。特别地 W_5(1)={2}，不是 admitted resource；W_5(2)=∅。

若奇素数 q 的 exact order 为 n，则

\[
\boxed{v_q\Phi_n(5)=v_q(5^n-1)=v_q(5^{q-1}-1)=s_q.}\tag{E2}
\]

因 (q−1)/n 不被 q 整除，最后一个等式也是 LTE。因此 primitive setting 下的四种说法：nonregular、q²|5^n−1、q²|Φ_n(5)、base-5 Wieferich，严格等价。

## 4. B7 n-FAMILY：从源重建，不采用 stronger edge-only 类

沿用 Phase D 的必要 basal 定义：

\[
O(x)=\{p\text{ odd prime}:p\mid w_x\},\quad
\Gamma(q)=\{x\in D(q):O(x)=\{3\}\}.
\]

B7 要求 q admitted/nonregular、T(q)={3}、所有 proper admitted descendants regular、Γ(q)={7}，且 basin 内所有 exact orders squarefree。D(q) 包含 q 与 admitted descendants >3，排除 terminal 3。[S1]

**不允许偷换为只有 7 能直接指向 3。** 43 的 order 为 42，故 43→3 与 43→7→3 同时存在，仍合法。也不能把 exact-order squarefree 换成 prime-minus-one squarefree。[S1,S6]

最小 proper extension r 的 odd order support 必须包含 7，且只能再包含 3，故 w_r∈{7,14,21,42}。四个完整分解为

\[
\Phi_7(5)=19531,\quad \Phi_{14}(5)=29\cdot449,
\]
\[
\Phi_{21}(5)=379\cdot519499,
\quad\Phi_{42}(5)=7\cdot43\cdot127\cdot7603.
\]

删除 nonadmitted factors，以及 Φ42 中 order 仅为 6 的 imprimitive factor 7，恢复

\[
R=\{43,127,379,7603,19531,519499\}.
\]

本包独立 trial-division / modular-power 复算得到

|r|w_r|s_r|(5^{w_r}−1)/r mod r|
|---:|---:|---:|---:|
|43|42|1|42|
|127|42|1|122|
|379|21|1|50|
|7603|42|1|2581|
|19531|7|1|4|
|519499|21|1|443642|

若 D(q)={7,r,q}，r 必整除 w_q，其他 odd factors 只能是 3、7，所以

\[
\boxed{n=w_q=rd,\quad r\in R,\quad d\mid42.}\tag{F1}
\]

这里 d 的确切集合为 {1,2,3,6,7,14,21,42}，共 48 个不同 indices。

### E3. intrinsic three-vertex 类的反向成立

对任何 r∈R、d|42，若 q∈W_5^adm(rd)，则 q>rd≥r，order support 仅为 r 及可能的 3、7。r 的完整 admitted proper closure 为 {7}，7 和 r 均 regular，且其 orders squarefree、basal gateway 为 7。因此 q 满足 B7 的全部 intrinsic conditions，且 D(q)={7,r,q}。

故不只是必要性，实际上

\[
\boxed{\{q\in B7:|D(q)|=3\}
=\bigsqcup_{r\in R}\ \bigsqcup_{d\mid42}W_5^{\rm adm}(rd).}\tag{F2}
\]

这是 **单个整数的 intrinsic arithmetic 等价**，不是完整七根 shared-state certificate 的等价。

Phase D 已认证排除 n∈{43,86,127,129,258}；本轮没有重新证明那些大数素性证书，也不将它们计作新增成果。43 个 order cases 仍保留；r=43 的未决部分仍为 {301,602,903,1806}。[S1]

一般 B7 不受 |D|=3 限制；height two 也可以同时使用多个 r，源第一阶段对应 508 个 potential next indices。不能把 F1 或 F2 外推到 arbitrary branching / unbounded-height B7。[S1]

## 5. BASIC CONGRUENCE STRUCTURE

对 admitted q，q−1 恰含一个 2 因子。因此 n 必有 v₂(n)≤1。写 q−1=nh，则

\[
n\text{ odd}\Longrightarrow h\equiv2\pmod4,
\]
\[
n\text{ even}\Longrightarrow v_2(n)=1,\ h\text{ odd}.
\]

Euler criterion 给 odd n 时 (5/q)=1，even n 时 (5/q)=−1。再由 quadratic reciprocity，

\[
\begin{array}{c|c}
n\text{ odd}&q\equiv11,19\pmod{20}\\
n\text{ even}&q\equiv3,7\pmod{20}.
\end{array}\tag{C1}
\]

这在 Kraft–Hall 源中已经存在，不是本轮的新排除。[S4] 48 个 indices 全与之兼容。不得追加没有证明的 q−1 squarefree、q≢1 mod r²，或某一个 q mod8 类不可能等限制。

## 6. FERMAT QUOTIENT FORMULATION

固定奇素数 q≠5，n=ord_q(5)，h=(q−1)/n，定义

\[
A_q=\frac{5^n-1}{q}\pmod q,\qquad
Q_q(5)=\frac{5^{q-1}-1}{q}\pmod q.
\]

从 (1+qA_q)^h 展开，

\[
Q_q(5)\equiv hA_q\pmod q.\tag{Q1}
\]

h 在 F_q 中可逆，故 Q_q(5)=0 与 A_q=0 等价。写 F=Φ_n、G=(X^n−1)/F，则

\[
A_q\equiv G(5)\frac{F(5)}q\pmod q.
\]

下一节将进一步得到不含不必要 n-dependent unit 的正规化公式。

## 7. CYCLOTOMIC DERIVATIVE ATTACK：准确恒等式，而非 collision

因为 q∤n，X^n−1 在 F_q 上 separable。5 是 F 的 simple root，其他分圆因子在 5 处非零。对 X^n−1=FG 求导并代入，

\[
F'(5)G(5)\equiv n5^{n-1}\not\equiv0\pmod q.\tag{D1}
\]

所以 primitive q **必然**满足 q∤Φ'_n(5)，无论 s_q=1 还是 s_q≥2。q²|Φ_n(5) 不是 q|Φ'_n(5)。

设 B=F(5)/q mod q。利用 h≡−n⁻¹ mod q、5^n≡1 mod q，Q1 与 D1 给

\[
\boxed{Q_q(5)\equiv-\frac{B}{5F'(5)}\pmod q.}\tag{D2}
\]

这里所有逆元均已证明存在。直接把 Φ'_n(5)/Φ_n(5) 当作模 q 数是不合法的，因为分母为 0；正规化必须先除去已知的一次 q，并保留 unit factors。

对固定整数 lift 5+qt，Taylor expansion 给

\[
F(5+qt)\equiv F(5)+qtF'(5)\pmod{q^2}.
\]

因此唯一成功 digit 为

\[
\boxed{t\equiv-\frac{B}{F'(5)}\equiv5Q_q(5)\pmod q.}\tag{D3}
\]

结论不是 derivative route 永远无用，而是 **“simple derivative / discriminant 无 q 因子 ⇒ 固定值没有 q²”这一具体推理错误**。D2–D3 本身没有提供独立于 Q_q(5)=0 的第二个障碍。

## 8. ALGEBRAIC NUMBER FIELD FORMULATION

令 K=Q(ζ_n)，O_K=Z[ζ_n]。由 q≡1 mod n、q∤n，q 在 K 中 unramified 且完全分裂。因 5 mod q 是 primitive n-th root，恰有一个 prime ideal

\[
\mathfrak p=(q,\zeta_n-5)
\]

整除 5−ζ_n；其他 degree-one primes 对应不同的 primitive roots，不整除这个固定元素。

由于

\[
N_{K/\mathbb Q}(5-\zeta_n)=\Phi_n(5),
\]

且这唯一的局部 residue degree 为 1，

\[
v_q\Phi_n(5)=v_{\mathfrak p}(5-\zeta_n)=s_q.\tag{N1}
\]

故 square hit 是

\[
\mathfrak p^2\mid(5-\zeta_n),
\]

**不是**“两个不同 split primes 同时整除 5−ζ_n”，更不是 ramification。完全分裂与同一 prime ideal 的 valuation≥2 完全兼容。

在 K_𝔭≅Q_q 的嵌入下，ζ_n 映到与 5 mod q 对应的 root of unity，N1 即变成下一节的 Hensel 条件。这里没有新出现一个迫使更小 order prime nonregular 的 norm-divisibility 结论。

## 9. TEICHMÜLLER / HENSEL FORMULATION

记 ω=ω_q(5)∈Z_q^× 为 5 mod q 的 Teichmüller lift。它的 exact order 为 n，并满足

\[
\omega\equiv5^q\equiv5+5qQ_q(5)\pmod{q^2}.\tag{H1}
\]

第一同余可直接验证：5^q mod q² 与 5 模 q 相同，且其 (q−1)-次幂为 1 mod q²；唯一性来自 Hensel。

于是

\[
\boxed{q\in W_5(n)\iff5\equiv\omega_q(5)\pmod{q^2}.}\tag{H2}
\]

不能写成整数 5 在 Z_q 中**精确等于** ω；5 不是非平凡 root of unity。这里只是精度 q² 的一致。

更一般地，若 s=s_q，则

\[
\operatorname{ord}_{q^k}(5)=nq^{\max(0,k-s)}.\tag{H3}
\]

证明为对 5^n 的 LTE，结合 reduction modulo q 的 exact order n。

采用 log_q(ω)=0 的标准 q-adic logarithm normalization，写 5=ω⟨5⟩，则

\[
v_q(\log_q5)=s_q,\qquad
\frac{\log_q5}{q}\equiv-Q_q(5)\pmod q.
\]

这也是同一提升系数的表述，不是第二个独立 rare event。Hensel 保证每个 simple root 都有唯一提升；它不保证整数代表 5 的 digit 0 不是那个提升。

## 10. RESULTANT/GCD RESULTS

### E4. 一般的 common-value gcd 不含平方

若不同 n,m 的 Φ_n(5)、Φ_m(5) 有共同奇素因子 ℓ，E1 迫使它们的 indices 均为 fℓ^a，且至少一个 a>0。在那个值中 ℓ 的 valuation 恰为 1。2 的例外公式也给相同结论。因此

\[
\gcd(\Phi_n(5),\Phi_m(5))\text{ 不含任何 prime square}.\tag{G1}
\]

实际上 gcd 是 1 或一个素数：共同 ℓ 迫使较大 index 与较小 index 之比为 ℓ 的正幂，不可能同时对应两个不同素数。

这与 Apostol–Diederichsen 的 cyclotomic resultant formula 一致；Louboutin 的短证明给出 m>n>1 时，resultant 在 m/n 为素数 ℓ 的正幂时为 ℓ^{φ(n)}，其余为 1。[P1]

特别地，各 W_5(n) 互不相交。仅凭 exact-order 唯一性也能得到这点。**这不证明一般 B7 basins 不共享 proper admitted relays**；root 唯一与 ancestor-sharing 是不同问题。

### E5. 本任务 48 个 Φ 值实际上两两互素

不同 r,s∈R 的 rd、se 互不整除：r,s>7，且 d,e 仅含 2、3、7。因此不可能有 prime-power ratio。

同一 r 的两个 indices 之比若为 prime power，只能来自 2、3、7。共同素数 3 或 7 的 index 形状分别只能为 2·3^a 或 6·7^a，不含 r>7；2 只出现在 power-of-two indices，也不可能。故

\[
\boxed{\gcd(\Phi_{rd}(5),\Phi_{se}(5))=1
\quad((r,d)\ne(s,e)).}\tag{G2}
\]

这是关于全部因子的 theorem，不需要将 48 个整数分别分解。程序进行 1128 次精确 index-pair 检查；它们不是 1128 次巨大整数 gcd 的实际计算。

### E6. 唯一 imprimitive factor 与六个聚合整数

设 f_r=w_r，则 E1 进一步给

\[
\epsilon_{r,d}=\mathbf1_{d=f_r},\qquad
C_{r,d}=\frac{\Phi_{rd}(5)}{r^{\epsilon_{r,d}}}.\tag{G3}
\]

C 的所有素因子都 primitive，故每个 p|C 满足 p≡1 mod rd。六个 imprimitive occurrences 的 indices 是

\[
1806,\ 5334,\ 7959,\ 319326,\ 136717,\ 10909479,
\]

分别只去掉一个 r。

由 r∤42，

\[
\prod_{d\mid42}\Phi_{rd}(5)
=\frac{5^{42r}-1}{5^{42}-1}=\Phi_r(5^{42}),
\]

\[
\boxed{B_r:=\prod_{d\mid42}C_{r,d}
=\frac{5^{42r}-1}{r(5^{42}-1)}.}\tag{G4}
\]

G4 是源 Kraft–Hall KH-4 的 (ℓ=r, depth=1, M=42) **特化**，不是本轮首创的 finite-support invariant。[S4]

由 G2–G3，

\[
\forall d\mid42,\ W_5(rd)=\varnothing
\iff B_r\text{ squarefree}.
\]

相应地，r 对应的 intrinsic three-vertex B7 子族为空，当且仅当 B_r 没有 admitted prime-square divisor。两种条件不可混同。

这将任务统一成六个 explicit integers 的 square-part 问题，但没有自动证明它们 squarefree；物化更大的聚合数也未必比处理其互素 components 更高效。

## 11. 新的整族模 r² 因子平衡：证明与精确证据

### E7. 全部 48 个 normalized values 的非零一阶系数

本轮得到

\[
C_{r,d}\equiv1+r\kappa_{r,d}\pmod{r^2},
\qquad \kappa_{r,d}\ne0\pmod r.\tag{B1}
\]

在 d≠f_r 时，Φ_{rd}(X)=Φ_d(X^r)/Φ_d(X) 给

\[
\boxed{\kappa_{r,d}
\equiv5Q_r(5)\frac{\Phi'_d(5)}{\Phi_d(5)}\pmod r.}\tag{B2}
\]

**证明。** 用 5^r≡5+5rQ_r(5) mod r² 对 Φ_d 在 5 处展开，然后除以 r-adic unit Φ_d(5)。每个 r regular，故 Q_r(5)≠0。对 d|42 的小多项式，精确 derivative 值为

|d|Φ_d(5)|Φ'_d(5)|
|---:|---:|---:|
|1|4|1|
|2|6|1|
|3|31|11|
|6|21|9|
|7|19531|22461|
|14|13021|16059|
|21|196890121|481424574|
|42|290639881|689236926|

这八个 derivative 值均不被 R 的任一成员整除。因此 B2 同时证明 42 个 nonexceptional coefficients 非零。

六个 exceptional d=f_r 不能除以 Φ_d(5) mod r。它们用两种不同的 exact organization 验证：一是先算 Φ_d(5^r) modulo Φ_d(5)·r³，再做严格整数除法；二是对 ∏_{a|rd}(5^a−1)^{μ(rd/a)} 分离每个 factor 的 r-adic valuation 与 unit，计算 unit product mod r²。两路均不物化巨大分圆值，结果逐项相同。

全表如下；列顺序固定为 d=1,2,3,6,7,14,21,42。

|r|1|2|3|6|7|14|21|42|
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
|43|31|35|1|4|6|34|16|24|
|127|13|51|84|113|77|103|113|20|
|379|367|371|93|196|374|152|278|14|
|7603|421|2815|6729|2894|3194|4141|2316|2810|
|19531|13950|9300|269|18334|5579|10229|19258|1193|
|519499|109652|419434|105361|262189|258050|432861|344114|222192|

**程序的一般精确除法公式：** 令 den=Φ_d(5)·r^ε，先计算 Φ_d(5^r) mod den·r²，结果必被 den 整除；商即 C mod r²。对六个例外 ε=1，此 modulus 就是 Φ_d(5)·r³。只涉及 d≤42 的小多项式与 modular exponentiation。

### E7.1 因子平衡推论

写 C_{r,d}=∏_{p|C}p^{e_p}。由 p≡1 mod r，在模 r² 展开乘积得到

\[
\boxed{\sum_{p\mid C_{r,d}}e_p\frac{p-1}{r}
\equiv\kappa_{r,d}\not\equiv0\pmod r.}\tag{B3}
\]

因此每一个 C_{r,d} 至少有一个 primitive prime factor p，满足

\[
v_r(p-1)=1,\qquad r\nmid e_p.
\]

特别地这些 C 都不是整数的 r 次幂。

**限制至关重要：** p 不一定是拟寻找的 nonregular terminal q；regular companion 可以独自使 B3 的总和非零。Φ_n(5) 的所有因子也不必作为 actual panel rows 出现。因此 B3 不能用于向整个 C=1 ledger 收取另一个 mandatory root，也不允许将 v_r(q−1)=1 强加给每个 q∈W_5(n)。

就单独模 r² 而言，任意 1+rκ 都是平方：它等于 (1+rκ/2)² mod r²。因此这些非零 coefficients 本身不排除平方因子。

### E7.2 六个聚合校验

令 A=5^42，H_r=(A−1)/r mod r。各 H 非零，且 binomial expansion 给

\[
B_r=\frac{(1+rH)^r-1}{r^2H}
\equiv1-\frac{rH_r}{2}\pmod{r^2}.\tag{B4}
\]

这里 H 先取准确整数 (A−1)/r；r>3 使三次及以上相关项在所需精度消失。因此

\[
\sum_{d\mid42}\kappa_{r,d}\equiv-\frac{H_r}{2}\pmod r.
\]

六组 (H_r,−H_r/2 mod r) 依 R 的顺序为

\[
(42,22),(122,66),(100,329),(2581,2511),(24,19519),(367785,75857).
\]

这为整族 computations 提供第二层一致性检查；不是 B_r squarefree 的证明。

## 12. KNOWN NONREGULAR SANITY CHECK

本轮没有重跑 q≤2×10⁹ 的 inventory。只针对强制指定的三个 q，使用 complete trial division 证明素性，分解 q−1、验证 exact-order drops，并重算 q²/q³ lifting。

|q|ord_q(5)|s_q|(5^n−1)/q² mod q|T(q)|
|---:|---|---:|---:|---|
|20771|10385=5·31·67|2|10626|{3,5}|
|40487|40486=2·31·653|2|12312|{3,653}|
|1645333507|1645333506=2·3³·30469139|2|1624266569|{3,761,1429}|

三者均满足 Q_q(5)=0、Φ'_n(5)≠0 mod q、5≡ω mod q²。derivative/Hensel formula 对它们没有误排。

每个例子违反的是 B7 的 **额外 closure 假设**：20771 引入 free terminal 5；40487 引入 653≡1 mod4；1645333507 除引入 761、1429 外，3-depth 还为 3，不符合 B7 的 depth≤1。[S1–S3；数值本轮复算]

proper admitted descendants 及其 exact orders / lifting coefficients 为

\[
31: (w,k)=(3,4),\quad67:(22,29),\quad11:(5,9),
\]

\[
30469139:(2176367,26663658),\quad1523:(1522,93).
\]

全部 s=1。3 本身也 regular：w₃=2、k₃=2。由此，以下 **不加 pure-3 前提的具体 descent 命题为假**：

> 每个 nonregular q 都必须有一个 nonregular proper admitted order-descendant。

这并不反驳尚未建立的 B7-specific descent，也不反驳某种另有精确定义的“exceptional smaller object”。后者需要提出对象、证明继承性质、证明严格下降和底层不可能，不能以“可能存在某种 descent”替代这些义务。

## 13. E8：base-uniform 局部 descent 的 CRT 反例

设 S 是有限个不含 q 的素数。对每个 p∈S 固定 A≡5 mod p²；对 q 固定 A≡ω_q(5) mod q²。CRT 同时可解。它保留所有 S 中的 base-5 orders 及 regularity，同时使 q 对 base A 满足 Wieferich condition。因此，仅使用这些较小素数处局部资料的 **base-uniform** 论证，不能推出 q 必 regular。

小型、完整可重放的例子为

\[
A=2882381\ne5,
\]

\[
A\equiv5\pmod{4\cdot3^2\cdot7^2},\qquad
A\equiv1639=5^{43}\pmod{43^2}.
\]

实际算术：

|p|ord_p(A)|s_p(A)|
|---:|---:|---:|
|3|2|1|
|7|6|1|
|43|42|2|

且 A^42 mod 43³=1+27·43²。于是 base A 的 analogue 具有 pure-3、squarefree-order、proper regular basin 与 nonregular root 43，所有相关 prime ideal / derivative / Hensel 条件正常成立。

**这是 variable-base 反例，不是 W_5(42) 的成员，不是 base-5 B7 member，更不是 A303656 counterexample。** 它准确指出：成功的 fixed-base-5 证明必须利用上述 base-uniform local data 以外的算术输入。

## 14. UNCONDITIONAL THEOREMS：本轮能保留什么

E1/E2 给完整 valuation 与 exact-order equivalence；D2/D3/H1–H3 给正规化 quotient/derivative/lift 定理；N1 给唯一 degree-one prime ideal 的准确解释；E3 给 intrinsic three-vertex 反向；E4–E6 给 value-gcd、48-value coprimality 和 imprimitive classification；E7 给统一模 r² factor balance；E8 否定指定的 base-uniform 局部 descent。

G4 的有限支持聚合继承 KH-4。五个旧 index exclusions 与第一层 regular relay 分类继承 Phase D，并对后者的小数值重新验证。不能把相同结论换记号后再计作新增 family death。

没有证明任何新 W_5(rd) 或 W_5^adm(rd) 为空；没有证明 general B7 的统一高度界；没有实际新 terminal。

## 15. CONDITIONAL THEOREMS：abc / height

Silverman 型结论以及 Ding 的算术级数加强，在 abc 前提下给的是 **non-Wieferich primes 的数量下界**。Ding Theorem 1.1 对 fixed a,k≥2 给 p≡1 mod k、a^{p−1}≢1 mod p² 的素数数量 ≫log X。它既不指定 ord_p(a)=n，也不是 Wieferich primes 的零上界。[P2]

下面给一个直接从 rational abc 推导、确实适用于当前 fixed base 的条件性估计。写

\[
M=5^n-1=UD,
\]

其中 U 是所有 exponent 恰为 1 的 prime factors 之积，D 是所有 exponent≥2 的完整 prime powers 之积。于是

\[
\operatorname{rad}(M)\le U\sqrt D=\frac M{\sqrt D}.
\]

对 1+M=5^n 应用 abc，任取 ε>0，得到

\[
M\ll_\epsilon\left(5M/\sqrt D\right)^{1+\epsilon},
\]

因此

\[
\boxed{D\ll_\epsilon M^{2\epsilon/(1+\epsilon)}.}\tag{A1}
\]

等价地，任意 η>0 都有 D≪_η5^{ηn}。若 q∈W_5(n)，q²≤D，故任意 δ>0 都有

\[
q\ll_\delta5^{\delta n}.
\]

这是 powerful part 的 conditional subexponential bound，而不是 powerful part=1。它与 n|q−1 给出的线性下界 q≥n+1 完全相容，也没有为 48 个固定 n 提供明确数值常数。因此不能用于本项目 unconditional closure。

primitive-divisor existence 也不够。源对每个 admitted prime p 的 Φ_p(5)≡3 mod4 的论证已保证存在更大的 admitted exact-order child；它只保证一次整除，不保证平方整除，也不保证所有子节点 regular。[S2,S3]

## 16. HEURISTICS

固定 q 和一个模 q 的 exact-order-n root，q 个模 q² 的 lifts 中，恰好一个保持 n-th-root 条件。这是 Hensel 的精确有限计数。

将“固定 q、变化 base lift”的比例 1/q 转为“固定 base 5、变化 q”的概率模型，则需要随机性假设。Katz 对 Crandall–Dilcher–Pomerance model 的讨论给出 Fermat quotient 随 q 类似随机、全素数范围 Wieferich 数量约 log log X 的 heuristic。[P3]

该模型没有证明 B7 order-closure 筛选后的独立性；没有证明八个 indices 或不同 relays 的事件概率按某种独立乘积相乘；也不能把 expected count 小于 1 变成 actual count 等于 0。

因此本包无任何 heuristic 被提升为 project theorem。

## 17. Reference computation 与复现

运行：

```bash
python verify.py --self-test --output fresh_evidence.json
```

Python 3.10+，标准库，无网络，无仓库 import。程序即使在 `python -O` 下也保留关键检查；错误输入通过显式 CheckFailure 拒绝。

本轮执行并通过：四个 first-layer complete products、六个 relays 的素性/order/regularity、48 个 normalized residue 的两条 algebraically different computation routes、1128 个结构性 index-pair tests、三个指定 nonregular primes 的素性/order/q²/q³ 与 admitted closure、11 组 derivative/Fermat/Hensel identities、q=7/43 的 50 个 lift digits、60 个小 indices 上的 480 次 valuation regressions、6 个错误声明拒绝测试。

两路 normalization 都在同一 Python 会话/整数环境中执行；不是两个完全独立软件栈或独立团队。small-index regressions 不能代替 E1 的全参数证明。两个 q 的 lift 枚举不能代替 Hensel theorem。

程序不声称认证 Phase D 五个大分解，不重放 2×10⁹ prime inventory，不输出 complete certificate。所有这些 nonclaims 同时写入 evidence.json。

## 18. FINAL DECISION / NEXT SINGLE TARGET

```text
DOES ANY COMPLETE B7 FAMILY DIE IN THIS PHASE E?
NO

DOES THIS ADVANCE B7 EMPTY BY A NEW TERMINAL/ORDER EXCLUSION?
NO

NEW EXCLUDED INDICES:
NONE

REMAINING THREE-VERTEX INDICES:
43 (inheriting Phase D's five exclusions)
```

路线层面的收获是消除了 derivative collision、split-prime norm 和一般 descent 的具体错误论证，并将现有有限 family 的 square-part 问题正规化。没有理由因这些局部论证失败，就宣布其他 family-wide methods 不可能。

**NEXT SINGLE TARGET：** 定义

\[
\operatorname{Sq}_{3(4)}(N)=
\prod_{p\equiv3(4)}p^{\lfloor v_p(N)/2\rfloor}.
\]

对 r=43 的四个残余 indices，判定唯一的聚合 square-part 命题

\[
\boxed{\operatorname{Sq}_{3(4)}\!\left(
\Phi_{301}(5)\Phi_{602}(5)\Phi_{903}(5)
\frac{\Phi_{1806}(5)}{43}\right)=1.}
\]

由于 G2，任何平方不会由不同 factors 的一次整除拼成；因为 G3，43 已被精确去除。该命题为真就关闭完整 r=43 three-vertex 子族；为假并认证对应 admitted prime 则得到该子族的 actual B7 member。接受任意可独立重放的 square-part certificate，**不宣称只能靠逐 n 完全分解**。本轮没有执行这个尚未通过的新 closure gate，也未授权扩大一般 q scan。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```

## References

[S0] Fixed-SHA STATUS、live main branch/tree、PR #26–#29 metadata。

[S1] `analysis/c1_b7_pure3_phase_d/REPORT.md`，尤其 §§2,4–8,10,12–16。

[S2] `analysis/c1_seven_head_chain_realizability_phase_d/REPORT.md`。

[S3] `analysis/c1_order_dag_phase_c/REPORT.md` 与 `THEOREMS.md`，尤其 Theorems 7.1,7.2,12.1。

[S4] `analysis/c1_kraft_hall_phase_a/REPORT.md`，尤其 KH-4、§5.2、§11.2。

[S5] `analysis/c1_pooled_lower_cover_phase_b/REPORT.md`，尤其 P4/P5、exact-order 与 pooled/BOTH scope。

[S6] `analysis/c1_b7_pure3_phase_d/PROOF_AUDIT.md`。

[P1] Stéphane Louboutin, *Resultants of cyclotomic polynomials*, Publ. Math. Debrecen 50/1–2 (1997), 75–77, DOI 10.5486/PMD.1997.1721。

[P2] Yuchen Ding, *Non-Wieferich primes under the abc conjecture*, C. R. Acad. Sci. Paris, Ser. I 357 (2019), 483–486, DOI 10.1016/j.crma.2019.05.007，Theorem 1.1。

[P3] Nicholas M. Katz, *Wieferich Past and Future*, §2：Fermat quotient 与 Crandall–Dilcher–Pomerance model。历史 inventory 不是当前 exhaustiveness authority。

机器可读路径、固定 SHA URL 与访问边界见 SOURCE_BINDING.json；外部资料访问地址见 SOURCES.md。
