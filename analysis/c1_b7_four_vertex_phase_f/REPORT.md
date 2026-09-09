# A303656 C=1 FOUR-VERTEX B7 FORK–SERIAL CYCLOTOMIC CLOSURE — PHASE F

## 0. 结果与证据等级

**本轮达到 Level D：从已合并 Phase D 定义独立重建四顶点分类，证明 exact-state primitive critical-integer 公式与去重定理，给出完整 fork 表和部分已认证 serial 表。没有关闭任何完整四顶点状态。**

已得到 15 个 fork proper-states、120 个互异 fork terminal indices；认证 28 个 regular serial relays，得到 28 个 serial proper-states、448 个互异 serial terminal indices。本包合计 43 个已明确认证的 proper-states、568 个互异 terminal indices。**这不是全部 serial states 的完整总数。**

完整六个 S_r 的数值枚举没有完成。完整 square-part certificate 没有完成。没有实际 nonregular B7 member。没有提高 basin-size 下界。

数学推导、程序设计与审计均来自同一研究会话；不声称独立作者证明、proof-assistant formalization 或 repository-native tests。验证程序是标准库实现，不用 probable-prime oracle 决定素性。

## 1. LIVE AUTHORITY 与缺失来源

```text
Repository: Samsen879/a303656
main SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
main tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
Tip: Merge pull request #29, Phase D seven-head chain realizability
main checked twice in this session: unchanged
Phase E branch search: no phase-e branches returned
Phase E ZIP physically available in this session: NO
GitHub writes: NONE
```

实际附件只有项目规则与项目简介两个文本文件，没有 prompt 中列出的三个 Phase E ZIP。GitHub 的 analysis 目录仍是 Phase D 及更早内容。因此本报告**不声称读取、校验或复现了缺失的 Phase E Branching 包**。

本轮从固定 SHA 的 `analysis/c1_b7_pure3_phase_d/REPORT.md` 的 precise basal-gateway definition、D1–D4 及相关讨论出发。额外读取了其 `arithmetic_certificates.json` 的选定范围，以及 `discovery_only_301_602.json`。来自旧文件的因子只作为输入线索；本包采用新的递归 Pocklington 证书和 exact-order / lifting 检查重新认证。

以下 `S_r` 是本轮基于这些定义重建的 regular-preimage set。以下 `\widehat Z_R` 是本轮明确规范化的闭状态整数；**没有将它冒称为缺失 Phase E 文件原符号 Z_R 的逐字复现**。完整来源记录见 `SOURCE_BINDING.json`。

## 2. FOUR-VERTEX CLASSIFICATION RECONSTRUCTION

### 2.1 采用的 B7 类

对 admitted prime x≡3 mod4，令

\[
w_x=\operatorname{ord}_x(5),\qquad s_x=v_x(5^{w_x}-1),
\qquad O(x)=\{p\text{ odd prime}:p\mid w_x\}.
\]

边方向为 **x→p，当 p 是 w_x 的 odd prime factor**。它严格数值下降；3 是终端，且不计入 D(q)。使用绝对算术闭包，不仅是某个 panel 中已列的 rows。

B7 要求 q admitted、s_q≥2；T(q)={3}；所有 proper admitted descendants regular；basal gateway

\[
\Gamma(q)=\{x\in D(q):O(x)=\{3\}\}=\{7\};
\]

以及 basin 中每个 exact order squarefree。这是 basal 类，**不是**禁止所有额外 3-edges 的更强 edge-only 类。

设 D(q)={7,r,s,q}，并按数值取 r<s。r 的 admitted proper support 只能是 {7}，因此 w_r∈{7,14,21,42}。四个完整分解为

\[
\Phi_7(5)=19531,\quad \Phi_{14}(5)=29\cdot449,
\]
\[
\Phi_{21}(5)=379\cdot519499,\quad
\Phi_{42}(5)=7\cdot43\cdot127\cdot7603.
\]

过滤 admission 和 order loss，得到

\[
A_7=\{43,127,379,7603,19531,519499\}.
\]

其 orders 依次为 42,42,21,42,7,21，且全部 regular。7 的 order 为 6。素性、所有 order-drop tests、mod p² regularity 在本包重新验证。

### 2.2 为什么只有 fork 与 serial

s 的 admitted odd support 只能来自 {7,r}，且不能为空，否则 s 会成为另一个 basal gateway。

* 若 r∤w_s，则 s 的 admitted proper support 是 {7}，所以 s∈A7。这是 fork。q 必须直接含 r 和 s；若漏掉其中一个，无法从另一个到达它。
* 若 r∣w_s，则 s 经 r 到达 7。这是 serial；7∣w_s 可以成立，也可以不成立。q 必须直接含 s，但 r∣w_q、7∣w_q 都可选。

额外直接到 3 的边、serial 中到 7 或 r 的 transitive edges 均保留，没有被示意图误删。

令

\[
K=\operatorname{Div}(42)=\{1,2,3,6,7,14,21,42\}.
\]

Fork 的完整 terminal-order family 是

\[
\boxed{I^F_{r,s}=\{krs:k\in K\}.}
\]

Serial 的 regular preimage set 是

\[
\boxed{S_r=\{s\text{ prime}:s\equiv3(4),\ s_s=1,
\ w_s\in\{kr:k\in K\}\}.}
\]

对 s∈S_r，完整 terminal-order family 是

\[
\boxed{I^S_{r,s}=\{ks,\ krs:k\in K\}
=\{ds:d\mid42r\}.}
\]

因此分别是 8 与 16，不是依赖 summary 的计数猜测。

## 3. PRIMITIVITY、ORDER LOSS 与 admitted parity

### Lemma 1 — squarefree index 的精确 imprimitive 修正

若 n>2 squarefree、p odd、p∤5，则：p∤n 且 p∣Φ_n(5) 时 exact order 就是 n。若 p∣n，则

\[
p\mid\Phi_n(5)\iff n=p\,w_p,
\qquad v_p(\Phi_n(5))=1.
\]

证明：写 n=pm、p∤m。用 Φ_pm(X)=Φ_m(X^p)/Φ_m(X)。模 p 下 ord_p(5^p)=ord_p(5)，而 p∤m 时 Φ_m 的根对应 exact order m。因此只有 m=w_p 可能贡献 p；该情形 LTE 给新增 valuation 恰为 1。n>2 的本轮 squarefree Φ 值不含 2；也不含 5。

对 fork，r 与 s 的 orders 都整除 42，均不含另一 relay。因此所有 120 个 fork indices 的 Φ 值均**没有 imprimitive prime divisor**。

对 serial，唯一可能的 imprimitive prime 是 s，唯一相关 index 是

\[
\boxed{n=s\,w_s,\qquad v_s(\Phi_{s w_s}(5))=1.}
\]

28 个已认证 serial states 各有且仅有一个这样的 index。其余 15 个 indices 没有 order loss。

若 admitted q 的 exact order n 为奇数，则 q≡11 或19 mod20；若 n 为偶数，则 q≡3 或7 mod20。理由是 v2(q−1)=1，使 order parity 等价于 (5/q) 的符号，再用二次互反律。**两种 parity 都被允许，没有删除一整半 indices。**

## 4. AGGREGATE CRITICAL INTEGER THEOREM

记 H=5^42。

### Theorem F1 — fork exact-state aggregate

对两个不同 r,s∈A7，定义

\[
\boxed{F_{r,s}=\prod_{k\mid42}\Phi_{krs}(5)
=\frac{(H^{rs}-1)(H-1)}{(H^r-1)(H^s-1)}.}
\]

即

\[
F_{r,s}=\frac{(5^{42rs}-1)(5^{42}-1)}
{(5^{42r}-1)(5^{42s}-1)}.
\]

这是 Φ_rs(H)，所以是整数。由 cyclotomic factorization，右侧恰选出 index 中同时含 r、s 的因子，不选出仅含一个 relay 的 lower-state factors。

\[
\boxed{
\exists q\in B7:\ D(q)=\{7,r,s,q\}\text{ 且为 fork}
\iff
\exists q\text{ prime},\ q\equiv3(4),\ q^2\mid F_{r,s}.
}
\]

### Theorem F2 — serial exact-state aggregate

对 r∈A7、s∈S_r，定义

\[
\boxed{S_{r,s}=\frac1s\prod_{d\mid42r}\Phi_{ds}(5)
=\frac{5^{42rs}-1}{s(5^{42r}-1)}.}
\]

乘积前的 1/s **不可遗漏**：s 的唯一 imprimitive contribution 必须去掉。LTE 给

\[
v_s\!\left(\frac{5^{42rs}-1}{5^{42r}-1}\right)=1,
\]

所以除以 s 后是整数，且所有 prime factors 都是相应 terminal index 的 primitive factors。

\[
\boxed{
\exists q\in B7:\ D(q)=\{7,r,s,q\}\text{ 且为 serial}
\iff
\exists q\text{ prime},\ q\equiv3(4),\ q^2\mid S_{r,s}.
}
\]

**两定理的 iff 证明。** 必要方向：root 的 exact order 落在相应 index family，且 nonregularity 等价于 q²∣Φ_n(5)。充分方向：规范化后所有 factors primitive，故一个 admitted square prime q 有唯一 exact order n 属于该 family；v_qΦ_n(5)=s_q≥2。Fork 的 n 同时含 r、s，serial 的 n 含 s，而 s 的已认证 closure 含 r 与7。因此 proper closure 恰为 {7,r,s}，没有 extra admitted descendants。每个 proper vertex regular，所有 orders squarefree，basal gateway 唯一为7。q>n≥s，也不会与 proper state 重合。

这个证明不把 integer squarefreeness 与 polynomial separability 混淆，也不使用 derivative/resultant shortcut。

## 5. GOOD CLOSED STATE 与 EXACT STATE 不能混同

对本轮任一 good regular proper-state R={7,r,s}，令 M=6∏_{p∈R}p=42rs，并定义本轮的规范化闭状态整数

\[
\boxed{\widehat Z_R=\frac{5^M-1}{2M^2}.}
\]

这是整数：对于每个 p∈R，w_p∣M、p∣M、s_p=1，LTE 给 v_p(5^M−1)=2；对3也为2；对2为3。分母恰将所有 index primes 完全除去。

它的 admitted square divisor 对应的是

\[
\exists q\in B7:\ D(q)\setminus\{q\}\subseteq R,
\]

**不是自动对应 equality**。若 q²∣\widehat Z_R，q∤M 且 w_q∣M，故 closure contained in R；n∣6 的小 pure-basal cases 没有外部 admitted square factor，所以 gateway 条件也正确。反方向由 LTE/primitive valuation 立即成立。

令

\[
Z_7=\frac{5^{42}-1}{2\cdot42^2}
=29\cdot31\cdot449\cdot43\cdot127\cdot379\cdot7603\cdot19531\cdot519499,
\]

它 squarefree。再定义每个 first-relay 的三顶点 primitive aggregate

\[
\boxed{C_r=\frac{5^{42r}-1}{r(5^{42}-1)}.}
\]

这个 C_r 是本报告局部记号，不是其他任务中的 C903 或 C1806。其 admitted prime divisors 正好是 8 个三顶点 exact-order preimages。因而有另一种完整、但未完成数值分解的 S_r 定义：

\[
\boxed{S_r=\{s\text{ prime}:s\equiv3(4),\ v_s(C_r)=1\}.}
\]

准确分解为

\[
\boxed{\widehat Z_{\{7,r,s\}}=
\frac{Z_7}{rs}\,C_rC_sF_{r,s}\quad\text{(fork)},}
\]

\[
\boxed{\widehat Z_{\{7,r,s\}}=
\frac{Z_7}{r}\,\frac{C_r}{s}\,S_{r,s}\quad\text{(serial)}.}
\]

这些乘法分量两两互素；Z7 相应部分 squarefree；serial 中 v_s(C_r)=1。因此：fork 的未过滤闭状态 square hit 还可能来自 C_r 或 C_s；serial 的还可能来自 C_r。除非另行关闭低阶 families，否则不能从闭状态定理直接得出用户希望的 exact-four-vertex iff。F1/F2 正好补上这个逻辑缺口。

## 6. DUPLICATE STATE / INDEX ANALYSIS

六个 S_r 两两不交，且都与 A7 不交。因为 s∈S_r 时 w_s 的 >7 prime support 恰有 r，唯一确定 r；而 A7 的 orders 只含2、3、7。

Fork indices 的 >7 prime factors 是两个 A7 元素，唯一恢复 unordered pair。Serial indices 恰含一个不在 A7 的 prime s，再由 w_s 唯一恢复 r。由唯一分解定理：

\[
\#I_F=120,\quad
\#I_S=16\sum_{r\in A7}|S_r|,
\]

且 raw counts 均等于 distinct counts；fork/serial 交集为空；二者与 48 个三顶点 indices {kr:r∈A7,k∣42} 的交集也为空。

**没有同一 actual prime-labelled R 同时具有 fork 和 serial 两种 edge realization。** Exact multiplicative orders 决定全部边，不能在固定 prime labels 下自由重选 DAG。一个 set R 即足以确定算术图，但在使用闭状态 square-hit 定理时仍须区分 contained closure 与 exact closure。

所有规范化 terminal cyclotomic values 的 prime supports 也两两不交：一个 primitive prime 的 exact order 唯一。因此所有不同状态的 F 与 S 彼此互素。聚合不会把不同因子各出现一次的同一 prime 伪造成 square hit。

可以进一步按 first relay 定义

\[
G_r=\prod_{t\in A7,\ t>r}F_{r,t}\;
\prod_{s\in S_r}S_{r,s}.
\]

六个 G_r 两两互素，全部四顶点 closure 等价于它们全无 admitted square divisor。**这是有限集合上的形式性压缩；完整 S_r 尚未枚举，因此本轮没有将六个 G_r 全部实例化或分解。** 聚合减少查询数量，但总位数不会神奇消失。

## 7. FORK: 完整状态与大小表

下表 15 个状态均是 certified regular proper-states；每行 8 indices，全部 closure_status=OPEN。位数用有严格余项界的有理数 logarithm intervals 认证；前三个整数也实际构造并记录 big-endian SHA256。

|r|s|rs：乘以 K 得全部 indices|F 的十进制位数|closure|
|---:|---:|---:|---:|---|
|43|127|5461|155,356|OPEN|
|43|379|16297|466,068|OPEN|
|127|379|48133|1,398,203|OPEN|
|43|7603|326929|9,373,138|OPEN|
|43|19531|839833|24,080,160|OPEN|
|127|7603|965581|28,119,413|OPEN|
|127|19531|2480437|72,240,480|OPEN|
|379|7603|2881537|84,358,237|OPEN|
|379|19531|7402249|216,721,438|OPEN|
|43|519499|22338457|640,532,249|OPEN|
|127|519499|65976373|1,921,596,745|OPEN|
|7603|19531|148494193|4,358,508,907|OPEN|
|379|519499|196890121|5,764,790,233|OPEN|
|7603|519499|3949750897|115,936,336,901|OPEN|
|19531|519499|10146334969|297,847,495,352|OPEN|

特别地，最小状态的 8 indices 为

\[
5461,10922,16383,32766,38227,76454,114681,229362.
\]

完整 120 行见 `indices.csv` 中 shape=fork。它们没有 imprimitive index prime。与三顶点 exclusion indices 的 overlap 为0。由于缺失 Phase E 原包，因此不声称已审计那个包全部其他 exclusion records。

## 8. SERIAL: 六张已认证表与未完成的完整 census

以下每张表列出的都是已认证 S_r 子集，**不是完整 S_r**。每个 s 均 fresh-prime-certified、admitted、regular，exact order 及 lifting coefficient

\[
5^{w_s}\bmod s^2=1+k_s s,\quad 0<k_s<s
\]

均精确验证。s≤10^10 的部分来自完整定向 AP 枚举；再加入5个从固定 SHA 因子线索重新认证的大素数。

### r=43: |S_r|≥9，完整 |S_r| 未知

|s|exact order|lifting coefficient k_s|regularity|
|---:|---:|---:|---|
|9547|86|6869|s_s=1|
|42743|602|28799|s_s=1|
|18471511|129|10935302|s_s=1|
|558801427|258|228381906|s_s=1|
|7866608083|86|6979768417|s_s=1|
|26041733579107|602|21236513736748|s_s=1|
|172827552198815888791|43|6578050564|s_s=1|
|43955934961951833386625799|129|13814757969496504861156109|s_s=1|
|236419892853700126919767791480523|258|174873425047096123598364461127972|s_s=1|
### r=127: |S_r|≥5，完整 |S_r| 未知

|s|exact order|lifting coefficient k_s|regularity|
|---:|---:|---:|---|
|2287|254|1957|s_s=1|
|23623|762|17966|s_s=1|
|133351|2667|30698|s_s=1|
|4283203|1778|753470|s_s=1|
|14693679385278593849609206715278070972733319459651094018859396328480215743184089660644531|127|4|s_s=1|
### r=379: |S_r|≥4，完整 |S_r| 未知

|s|exact order|lifting coefficient k_s|regularity|
|---:|---:|---:|---|
|6823|2274|4971|s_s=1|
|15919|379|9109|s_s=1|
|111427|15918|90535|s_s=1|
|7401871|7959|2780067|s_s=1|
### r=7603: |S_r|≥5，完整 |S_r| 未知

|s|exact order|lifting coefficient k_s|regularity|
|---:|---:|---:|---|
|319327|106442|27600|s_s=1|
|1262099|7603|317632|s_s=1|
|1596631|159663|1434954|s_s=1|
|188721667|319326|126997831|s_s=1|
|648003691|22809|317869461|s_s=1|
### r=19531: |S_r|≥3，完整 |S_r| 未知

|s|exact order|lifting coefficient k_s|regularity|
|---:|---:|---:|---|
|11835787|39062|1131360|s_s=1|
|42304147|117186|27063347|s_s=1|
|3326871479|19531|2262705296|s_s=1|
### r=519499: |S_r|≥2，完整 |S_r| 未知

|s|exact order|lifting coefficient k_s|regularity|
|---:|---:|---:|---|
|36364931|3636493|32264000|s_s=1|
|327284371|10909479|27660845|s_s=1|

完整有界计数 |S_r∩[1,10^10]| 按 r=43,127,379,7603,19531,519499 的顺序为 5,4,4,5,3,2，总计23。加5个大素数后，已认证计数变成9,5,4,5,3,2，总计28。

因此已明确生成的 serial raw count=distinct count=448；与 fork 的交集0，与三顶点 family 的交集0。本包总 indices=568。完整 serial 总数仍是 16Σ|S_r|，不是448。

全局最小的三个 serial aggregates 是：

|r|s|w_s|aggregate decimal digits|
|---:|---:|---:|---:|
|127|2287|254|8,522,905|
|43|9547|86|12,050,293|
|43|42743|602|53,954,925|

这一最小性不仅来自大范围搜索输出：标准库验证器另对 W=r(s−1)≤43(42743−1) 做独立短枚举。r≥43 且 s≤W/43+1；42W log10(5)−log10(s) 的增长保证 W 更大不会排到第三名之前。所有遗漏的 s>10^10 更不可能进入前三。

例如最小 serial 状态的完整 16 indices 是 {2287d:d∣5334}，唯一 imprimitive index 为2287·254=580898；其因子2287恰除去一次。

## 9. FACTORIZATION / SQUARE-PART RESULTS

### 9.1 状态定向、而非 general-B7 prime scan

每个 fork state 只测试其必要 AP

\[
q=1+2rs(2j+1),\quad q\le10^{12}.
\]

每个 serial state 只测试

\[
q=1+2s(2j+1),\quad q\le10^{12}.
\]

用 e=gcd(42rs,q−1) 先测试 5^e≡1 modq，再过滤 prime、exact order、mandatory support，最后用 mod q² 检验 lifting。Relay enumeration 相应使用 s=1+2r(2j+1)、s≤10^10、e=gcd(42r,s−1)。这些 AP 完整覆盖**所声明的有界范围**，不覆盖任意大 prime。

15 个 fork states 找到28个 admitted primitive prime factors；23个 bounded-relay serial states 找到62个。新增5个大 relays 都大于10^12，本身即使其 terminal q>10^12，因此无需另跑该小 terminal bound。90个 terminal prime factors 全部 valuation1，无 square hit。

发现程序为 C++ exact unsigned-128 modular arithmetic；输出 primes、orders、lifting 和 aggregate residues 由标准库 Python 独立验证。215个递归 prime certificate nodes 全部通过。完整区间扫描的 fresh replay 使用同一 C++ implementation，**不称作 independently implemented coverage verification**。小规模 priority enumeration 和所有输出证书检查另有 Python 实现。

前三个 fork states 的已找到 admitted factors如下；它们都不是 nonregular root：

|r,s|q|exact order|valuation in F|
|---|---:|---:|---:|
|43,127|6717031|5461|1|
|43,127|5518679083|229362|1|
|43,127|11078413963|76454|1|
|43,379|2053423|684474|1|
|43,379|393572551|342237|1|
|43,379|474796799|16297|1|
|43,379|968652448591|48891|1|
|127,379|208223359|48133|1|
|127,379|23557541659|336931|1|
|127,379|26303433043|288798|1|
|127,379|46951334851|1010793|1|
|127,379|203924792303|673862|1|

### 9.2 少量 selected p−1 分解

在完成 state construction、去重与大小排序后，另对6个小 index 做 B1=10000、bases2和3的 GMP Pollard p−1。发现的 gcd 被进一步拆成素因子，再做精确素性证书与乘积验证；没有把 gcd 自动当 prime。

\[
\begin{aligned}
\Phi_{4574}(5)&=119527769\cdot128712361\cdot C_{4574},\\
\Phi_{5461}(5)&=6717031\cdot C_{5461},\\
\Phi_{6861}(5)&=69316463449\cdot C_{6861},\\
\Phi_{10922}(5)&=3211069\cdot C_{10922}.
\end{aligned}
\]

这里 C_n 只是本节残余 cofactor 的局部记号。每个展示的 prime 因子 valuation1；除6717031外它们全为1 mod4，不是 admitted root。全部 cofactor 仍未获得完整 square-part certificate。对2287、16383没有找到新的 p−1 因子，这不构成排除证据。各 cofactor 的 bit length 与 canonical hash 见 `pminus1_results.json`。

**没有执行 ECM；没有完整分解任何四顶点 state aggregate；没有证明任何一个 aggregate 无 admitted square divisor。** 有理数位数计算、整数实际构造、没有找到 square factor，都不替代 square-part proof。

## 10. COMPUTATIONAL AUDIT 与可复现性

`verify.py --replay-probes --replay-pminus1` 全部通过，记录于 `validation.json`。包括：215个递归素性证书；first-relay 完整分解；28个 regular serial relays；568个不同 indices；每个 order-loss 位置；43个 aggregate 位数；前三个 fork 的完整数值哈希；90个 terminal factors 的 exact order、admission、lifting 和直接 aggregate mod q²；selected p−1 residual hashes；所有 bounded probe 的 fresh replay。

Pocklington 证书检查是自包含的：证书给 n−1 的已证明素因子乘积 F，要求 F²>n，并对每个 p∣F 提供 a，使 a^(n−1)=1 modn 且 gcd(a^((n−1)/p)−1,n)=1。任何素因子 ℓ∣n 因而满足 F∣ℓ−1，从而 ℓ>√n，排除 n composite。证书递归下降，以小于10000的 trial division 为基例。

位数认证采用 log x=2Σ z^(2j+1)/(2j+1)、z=(x−1)/(x+1)，几何尾界为2z^(2N+1)/((2N+1)(1−z²))。先计算 log2 与 log(5/4)，再得 log5/log10；大 s 先除以2的幂。Aggregates 的指数小项给出统一误差 <8·5^(−42)。上下有理数界的 floors 完全一致，才接受十进制位数；前三个 materialized fork 还独立验证10^(d−1)≤F<10^d。

原始 Phase E ZIP 仍未读取；本包不包含、也不伪造它的 original checksum 或 manifest。没有 repository-native checkout/test/PR 操作。

## 11. COMBINED WITH THREE-VERTEX

本轮仍只能继承已认证的 |D(q)|≥3。没有排除全部三顶点，也没有排除全部四顶点。

仅在四顶点全部关闭时，结论是 |D(q)|≠4，不是 |D(q)|≥5。只有全部三顶点与全部四顶点同时为空，才能推出至少五顶点。关闭 r=43 的三顶点 subfamily 仍不等于关闭其他五个 first-relay subfamilies。

Prompt 所述903/1806残留没有在本轮重审；Phase E 原文件缺失时，不将该阶段的新结论追加为本轮已重放的 authority。无论其最后结果如何，三顶点 index family 与本轮四顶点 family 都没有数值重叠。

## 12. NEXT SINGLE TARGET

固定最小 fork state {7,43,127}：

\[
\boxed{F_{43,127}=\frac{(5^{229362}-1)(5^{42}-1)}
{(5^{1806}-1)(5^{5334}-1)}.}
\]

唯一 closure gate：证明这个155,356位整数没有 q≡3 mod4 的 prime square divisor，或输出一个完整认证的 positive q。对应8个 indices已经冻结；不要用继续扩展 q cutoff 代替此 gate。对该 aggregate 的 square-part audit 与三顶点903/1806逻辑独立。

## 13. FINAL STATUS

```text
ACTUAL B7 MEMBER FOUND? NO
ALL FORK CLOSED? NO
ALL SERIAL CLOSED? NO
ALL FOUR-VERTEX CLOSED? NO
FULL NUMERICAL S_r ENUMERATION COMPLETE? NO
GENUINE COMPLETE FOUR-VERTEX STATE EXCLUSIONS: 0
SUCCESS LEVEL: D — independent aggregate theorem / certified partial tables

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
