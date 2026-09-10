# A303656 C=1 — GENERAL B31^odd BRANCHING OBSTRUCTION
## Targeted Phase G：全图互反律、提升不可辨识性与认证反模型

## 0. 结论

**本轮得到 E 级路线剪枝；没有证明 B31^odd 空，没有找到 actual base-5 member，没有得到全局有限 critical family，也没有显著缩小 fixed-base-5 terminal family。**

主要成果是把“全 all-odd DAG 的互反律，也许能与 nonregular square hit 产生矛盾”拆成有明确边界的数学断言，并严格证明其中几种断言不能成立：

- mandatory maximal-generator 的二次符号乘积，两侧均为 `(-1)^|A(R)|`，不是相反符号；两种 antichain parity 都保留。
- 模 q^h 的所有 prime-to-q 幂剩余测试只取决于模 q；它们不能区分 regular 和 nonregular lifts。q-primary 测试能区分，但恰好读出原来的 Fermat quotient / square-hit 条件，并未给第二个矛盾。
- 允许改变底数时，任何满足基本闭包要求的有限 rooted DAG、QR-compatible pair signs 和 root nonregular/proper regular 标记，都能由实际 prime labels 与某些 **素数底数** 同时实现；可以锚定实际 base-5 proper state。
- 给出五个完整认证的 variable-base square-hit countermodels，覆盖 maximal-generator 数目1、2、3，包含保留所有 vertex 的 base-5 一阶数据、保留实际 base-5 proper fork、以及 transitive-edge 三种针对性检验。
- 固定 base5 的 critical integer 有额外分支特征：单极大生成元时为5 mod8，多极大时为1 mod8。但该同余对移除一个 odd prime square 不变，因此不是 C 级 terminal 压缩。

完整陈述与证明在 `THEOREMS.md` G1–G5；确切整数、素性证书、完整 closures 和 negative tests 在 `evidence.json`、`COUNTERMODELS.md`、`verify.py`。

**新颖性边界：** Phase E Cyclotomic §13/E8 已有 lower-state CRT variable-base 反例。此轮不是重新发现 CRT 或 Hensel；推进在于整个 all-odd class、任意有限 branching/antichain 和互反律符号的可实现性，以及 tame/q-primary 区分的精确 no-go 范围。没有主张文献优先权。

## 1. Live authority 与阅读范围

```text
Repository: Samsen879/a303656
Pinned main SHA: c6ca0dc061783ab993be6fa077c8f66cd730e28c
Pinned main tree: 57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06
Pinned head: Merge PR #37 — Phase F four-vertex B7 fork-serial arithmetic
Head commit time: 2026-09-09T07:59:42Z
```

通过连接的 GitHub GET 读取 live main，并把后续来源读取固定在上述 SHA，而非使用历史研究包内自己的旧 main。

完整阅读并交叉核对了四份指定目录的核心 `REPORT.md`、B7 Branching 的 `THEOREMS.md`，以及四份 `INTEGRATION.md`。重点核对了 F2、F4 与 Seven-Basin 的 O31 接口。**没有逐文件读完四个目录的所有生成数据、历史 source bindings、辅助脚本、tests 和 manifests，因此用户要求的目录级全量阅读未完全完成，不能记为 FULL PASS。** 没有本地完整 checkout，没有重跑仓库原生 integration tests、CI 或全量 prime inventory；本包独立重认证了所使用的六个 inherited base-5 regular vertices，而不是信任 probable-prime flags。

Phase F 原始报告记载当时缺少 Phase E source；现有 `INTEGRATION.md` 明确记录后续 O31 source reconciliation PASS，dependency 已绑定 merged repository。本轮使用已对接的接口，不把历史缺口误报为当前缺口，也不把仓库报告的 replay PASS 当成本轮已经重跑的结果。

固定 STATUS 仍为：

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
LARGE-SCALE COMPUTATION: NOT AUTHORIZED
A303656: UNRESOLVED
```

结束前的 live-main recheck 与具体 read receipts 见 `SOURCE_BINDING.json`。源文件 blob SHA 来自 GitHub connector metadata；本轮没有获得可独立重算所有 source-byte hashes 的完整源码副本。包内 `SHA256SUMS.txt` 只认证本轮本地交付文件。

执行环境为网页端数学研究与中等规模 reference laboratory；没有启用 Codex CLI、Codex Ultra 或大规模分解。

## 2. F2/F4 的核心保护

这里使用来源的整个 intrinsic B31^odd 类：root 为 admitted nonregular prime，proper admitted descendants 全部 regular，T(q)={3}，basal gateway={31}，每个 x∈D(q) 的 ord_x(5) 都为奇数平方自由。

**terminal3 不在 D(q) 内。** ord_3(5)=2 不是空类证明；它是停止展开的 terminal，不受 whole-basin all-odd quantifier 约束。

F4 对任意 finite good regular state R 给精确判据

\[
q\in\mathcal B_{31}^{\rm odd},\quad D(q)\setminus\{q\}=R
\iff q\equiv3\pmod4,\quad q^2\mid Z_{31}(R).
\]

其中 terminal order 必含全部 maximal generators A(R)，不能只选择某条好路径或某个方便的 support subset。

F2 说明 B31^odd 若空，regular prime-order extension chain 反而可无限延伸。本轮没有把有限分支当成有限深度，也没有等待 regular recursion 耗尽；所研究的是终端 lifting 所缺失的信息。

## 3. 全图互反律没有产生相反符号

若 admitted edge x→p，两端皆3 mod4，p|ord_x(5) 给 x≡1 modp，因此

\[
\left(\frac{x}{p}\right)=1,\qquad
\left(\frac{p}{x}\right)=-1.
\]

对整个有限图相乘，只得到每条边贡献一个−1。acyclic 并不使这些负号消失。实际 base5 regular 子图

\[
490398859\longrightarrow\{31,878851\},\qquad878851\longrightarrow31
\]

的三个 admitted edges 的符号乘积就是−1。exact orders 分别为81733143=3·31·878851与93=3·31，全部 lifting=1，本轮以完整 Lucas certificates 与 exact-order tests 重认证。

对于 root q，F4 的 maximal-generator condition 迫使所有 a∈A(R) 都直接整除 ord_q(5)，所以

\[
\boxed{\prod_{a\in A(R)}\left(\frac{a}{q}\right)=(-1)^{|A(R)|}.}
\]

从 DAG 一侧和从 q≡1 moda 的另一侧推导，结果相同。若想得到 contradiction，必须提供一个真正独立、且要求相反符号的新算术定理，不能把同一批 reciprocity identities 计算两次。

G4 进一步给出任意有限允许图与 pairwise signs 的 variable-base realizability，而不仅是几个抽象 DAG 恰好没找到矛盾。但这仍不是 fixed-base5 所有图都可实现的断言。

## 4. Square-hit upgrade：缺失信息准确位于哪里

设 q 是奇素数，h>=1，gcd(m,q)=1。G2 证明

\[
u\text{ 在模 }q^h\text{ 是 }m\text{ 次幂}
\iff u\bmod q\text{ 在 }\mathbb F_q^\times\text{ 是 }m\text{ 次幂}.
\]

原因是 reduction kernel 为 q-group，m-th powering 在该 kernel 上可逆。

对于 q≡3 mod4，所有2^j-th-power residue tests 都与 quadratic test 相同。因此在这些 rational local power-residue tests 内，从二次升到四次、八次，或者把模数从q提高到q²，并没有获得 nonregular 信息。

相反，

\[
u\text{ 在模 }q^2\text{ 是 }q\text{ 次幂}
\iff u^{q-1}\equiv1\pmod{q^2}.
\]

它能识别 lifting，却恰好等于需要解决的 square-hit condition。Teichmüller/Hensel/这个 q-primary 判据是同一缺失系数的不同表述。

**范围不能越界：** 本轮并未证明所有 higher reciprocity、cyclotomic units 或 ramified-symbol 方法都无效。它排除的是明确的 prime-to-q 有限 local power-residuacity 升级，以及不引入 fixed-base5 新算术信息的图/符号组合。

## 5. 最直接的认证反模型：保留 base5 一阶资料，改变第二阶

取

\[
q=878851,\quad R=\{31\},\quad n=93,
\]
\[
\boxed{b=679350864025912037.}
\]

**b 本身已由 complete-(b−1) recursive Lucas certificate 认证为素数。** 它不是5，但满足

\[
b\equiv5\pmod{8\cdot9\cdot31^2},\qquad b\equiv5\pmod q.
\]

因此 proper31 的 exact order、regularity、小模数数据，以及 root 的 modq order 全部与 base5 相同：

| vertex | exact order at base5 | exact order at base b | s at base5 | s at base b |
|---|---:|---:|---:|---:|
|31|3|3|1|1|
|878851|93|93|1|2|

终端模 q³ 的明确检查为

\[
b^{93}\equiv1+258873\,q^2\pmod{q^3}.
\]

258873≠0 modq，故 s_q(b) **恰为2**。因为 exact order为93、q∤93，得到 q²|Φ93(b)，其 proper absolute closure恰为31→3。所有 basin vertices admitted、all-odd、squarefree，proper31 regular，root nonregular。

maximal generator只有31，且 `(31/q)=-1`；这个负号与 nonregular terminal 完全兼容。其 regular comparator 使用同样全部下游资料及 root 的模q资料，只有 q-adic lifting 不同，所有 prime-to-q power tests相同。

**这不是 base-5 B31odd member。** 在 base5 下，q仍然 regular；没有推翻 F1 的 two-vertex exclusion。该模型反驳的是不依赖底数恰为5的更弱 universal lemma。

## 6. 不只一个链：完整 branching 与任意 antichain 宽度

第二类反模型保留实际 base5 proper fork

\[
R=\{31,878851,625552508473588471\}
\]

在全部 proper p² 下的资料，并使用认证终端

\[
q=269386049336015633650142291,
\quad\operatorname{ord}_q(b)=878851\cdot625552508473588471.
\]

本轮得到 common integer base b，使所有 proper vertices 的 s=1、root 的 s=2、A(R) 有两个元素，符号乘积+1。这里 root 的 base5 residue 并未保留；事实上所给 n 不是该 q 的 base5 order，不能把这个模型当作 base5 regular terminal，更不能当 base5 square hit。巨大底数、完整 CRT equations 和每个 modular check都存于证据文件。

另一个完整 fixture 有 proper generators311、2791、3659，它们在选定 variable base下的 exact orders均为31，root603442975211的exact order为三者乘积，s=2。因此 |A|=3、符号乘积−1也可出现。这些 relays不是 base5 first-relay inventory中的新成员。

全部五个反模型包括两个 certified prime-base 两顶点模型、保留 actual base5 proper fork 的四顶点模型、三极大生成元模型和保留所有一阶 base5 数据的 transitive-edge 模型。详见 `COUNTERMODELS.md`。

无限域 G4 的证明分两步：先用 CRT 与 Dirichlet 在每个 direct child 上要求新prime为1，并在 non-edge primes上自由选择 QR-compatible residue；然后在每个 prime处独立选择 exact-order finite-field element 与指定 lifting digit，最后再用 CRT 与 Dirichlet得到一份共同素数底数。这能实现任意有限允许 DAG，而不仅是扫描到的几种小形状。

成功的 fixed-base5 障碍因而必须在上述可保持资料之外使用“这个整数确实等于5”的算术。这个结论不替它规定唯一可能的工具，也不声称所有整族方法已经失败。

## 7. 固定 base5 的 critical mod8 特征与失败的平方推论

令

\[
\alpha=\prod_{a\in A(R)}a,\qquad
\beta=3\prod_{r\in R\setminus A(R)}r.
\]

将 B7 Branching E3.1 的聚合公式适配 all-odd family，有

\[
Z_{31}(R)=
\begin{cases}
\Phi_p(5^\beta)/p,&A(R)=\{p\},\\
\Phi_\alpha(5^\beta),&|A(R)|\ge2.
\end{cases}
\]

唯一可能的 imprimitive index prime 是 singleton case 的p，出现一次；multi-max case不能有这种小因子。完整证明不要求分解这些巨大整数。

由于 βodd、5^β≡5mod8，可进一步得

\[
Z_{31}(R)\equiv5\pmod8\quad(|A|=1),
\qquad Z_{31}(R)\equiv1\pmod8\quad(|A|\ge2).
\]

单极大情形由几何和展开得到；多极大情形用 Φα(1)=1 与 `2Φα'(1)=φ(α)`、4|φ(α)。本轮对六个认证 base5 vertices产生的15个 actual closed substates逐一作独立组织的 Möbius-unit mod8检验，并做280个单纯代数 congruence regressions；后者不冒充actualgoodstates。

但 odd q²≡1mod8，所以 Z/q² 与 Z 有相同 residue。由“不为完全平方”推“无平方因子”是错误的。因此这一新 signature不关闭任何 terminal index，不给新的 candidate count bound，也不计成功等级C。

## 8. Reference computation 与安全范围

`verify.py` 完全离线，只用 Python标准库，关键检查在 `python -O` 下仍保留。素性使用递归完整 p−1 Lucas criterion，不信任 generator中的 probable-prime筛选。

认证/检查范围：45个递归素性证书；27条 exact-order/lifting rowrecords；五个完整 variable-base closures；46个代表性 tame lift测试及对应 q-primary正反测试；15个actualbase5closedsubstates；280个代数mod8回归；admittedvertex数2到6的小型 abstract root-closed admitted-subgraph 穷举（不计 optional direct3 edges 的选择）；12种损坏输入必须拒绝。

抽象DAG计数为1、2、10、122、3346，是有限组合回归，不是 prime inventory，不是证明G4无限量词的依据。与先前B7出现相同计数并不是一项新的算术成果。

另做过一个明确的有限 countermodel-discovery probe：固定 actual properfork，对四个 F4必需indices和odd k<=100000，测试 q=1+2kn、q≡11/19mod20，共80000个模幂候选，无survivor。此结果仅在 `discovery_only.json` 记录，**不用作任何无界index排除、squarefree证书或成员不存在结论**。复现脚本把k上限硬限制在原gate内；不授权扩大搜索或大规模分解。

完整运行记录及普通/优化/fresh-extraction replay比较在 `REPLAY_RECEIPT.json`。同一会话产生证明、generator和verifier，不是 independent-author review或fullyindependentsoftwarestack。不同计算组织仅用于发现实现错误，不替代数学证明。

## 9. 精确 scope audit

| 可能误推 | 本轮实际结论 |
|---|---|
|所有 all-odd trees 必须终止|不成立；继续保留F2的无限regular chain|
|acyclic edge product必为+1|被actualbase5regulartriangle反驳|
|A(R)某种奇偶性被互反律排除|没有；两侧符号相同|
|所有 higher reciprocity都无用|没有证明；只覆盖指定tame rational localtests|
|CRT反模型是base5member|不是；literalbase5仍未解决|
|底数要求prime可拯救base-uniformlemma|不行；G3/G4允许primebases，两个fixture已认证prime|
|properstate regular必排除highernonregular|base-uniform版本被反例否定；fixedbase5版本未否定|
|Z不是平方数所以没有squarehit|错误；mod8signature对除q²不变|
|获得globalfinitecriticalfamily|没有|
|exactly-seven/N>=8推进已闭合|没有|

从本轮没有新增 empty-class定理，不能触发 O31→exactly-seven impossible→N>=8 的链条。Seven-Basin的条件性globalstate构造也未被这些反模型实例化为base5七根证书。

## 10. 最终状态

```text
SUCCESS LEVEL:
E — narrowly scoped graph/reciprocity/tame-lifting route pruning

B31^odd EMPTY:
NOT PROVED

ACTUAL BASE-5 B31^odd MEMBER:
NONE CERTIFIED

GLOBAL FINITE CRITICAL FAMILY:
NOT PROVED

NEW BASE-5 TERMINAL/INDEX EXCLUSIONS:
NONE

EXACTLY-SEVEN:
NOT KILLED

N>=8:
NOT PROVED

A303656:
UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
