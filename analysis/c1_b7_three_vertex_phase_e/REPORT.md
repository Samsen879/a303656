# A303656 C=1 B7 Three-Vertex Cyclotomic Square-Hit Closure — Phase E

## 0. Verdict

**新增七个严格排除阶，累计12/48；r=43 family 缩到903与1806，但未完全关闭。没有找到 actual nonregular terminal，没有证明 three-vertex B7 为空，没有证明 B7 为空，没有升级 N>=8。**

本轮新增完整 squarefree cyclotomic factorization：

    254, 301, 379, 381, 602, 758, 762.

Phase D 的43、86、127、129、258也由本轮独立 verifier 重证。

另有两个可用于 arbitrary branching B7 的低阶推论：

\[
q\in B7\Longrightarrow w_q\ge889;
\qquad q\in B7,\ |D(q)|\ge4\Longrightarrow w_q\ge2287.
\]

这是根的 exact-order 下界，不是 basin 顶点数下界，不是 nonregular 根数下界。本报告所有无限参数推论均给出数学论证；有限程序只证明明确的算术输入。

执行环境：网页端研究及本地容器 standalone reference laboratory。没有交给 Codex，没有 GitHub 写入。证明与代码来自同一研究会话，尚无独立作者审稿或 proof-assistant formalization。

## 1. LIVE AUTHORITY

```
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: fd59aad038a09f2fc6df7039111408fa231c27dd
main tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
PRECONDITION: PASS
```

开始与结束均读取 live main，SHA/tree未改变；固定SHA的STATUS仍为PAUSED/NONE/UNRESOLVED。以下PR均逐项确认merged，而非只从包的PR正文推断：

|PR|内容|merge SHA|
|---:|---|---|
|26|private-provider charging|`07a6f5fb2059b1dfc6be7cc6d1325cd65b49ae41`|
|27|two-nonregular global state|`a8e72c805c6a36d3e215507a4fcaad271147ce7e`|
|28|B7 pure-3|`8dcb744641a46b41597681b4eaddfd7b427d7280`|
|29|seven-head chain realizability|`fd59aad038a09f2fc6df7039111408fa231c27dd`|

完整来源映射见SOURCES.md与SOURCE_BINDING.json。[S1–S11]

**阅读与复现边界：** 已读取五组核心数学报告以及相关完整主证明/审计；没有逐文件完整阅读五个目录的全部辅助文件和生成数据，因此没有完全达到“整个目录逐文件完整阅读”的要求。没有完整repository checkout，没有repository-native tests/CI replay，也没有2e9 inventory重跑。本文的算术证书检查是新写的standalone replay，不能冒充这些未执行的工作。

## 2. PHASE D B7 RECONSTRUCTION

### 2.1 Intrinsic basal B7，不是 edge-only B7

对admitted prime x≡3(mod4)，记
\[
w_x=\operatorname{ord}_x(5),\quad s_x=v_x(5^{w_x}-1),\quad
O(x)=\{p:p\text{ odd prime},p\mid w_x\}.
\]
对全部odd order factors展开数值严格下降的绝对DAG；终端为3或1(mod4) primes。D(q)包含root及全部admitted descendants>3，但不含terminal3；T(q)是全部终端，不能只取一条路径。

采用Phase D明确支持的basal定义：q为admitted nonregular prime；T(q)={3}；所有proper admitted descendants regular；
\[
\Gamma(q)=\{x\in D(q):O(x)=\{3\}\}=\{7\};
\]
且整个basin中每个w_x的3-depth≤1、其余odd prime depths≤1。admission给v2(w_x)≤1，故全部w_x squarefree。[S1,S5]

这不要求只有7的order被3整除。例如w43=42允许43直接指向3，又指向7；其basal gateway仍只有7。把较强edge-only子类的空性用于全部B7是错误的缩窄。

### 2.2 First-relay gate 的重证

r=min(D(q)\{7})的odd order factors只能来自{3,7}，必须包含7，否则r本身是另一个basal gateway。因此w_r∈{7,14,21,42}。四个完整产品为
\[
\Phi_7(5)=19531,\quad\Phi_{14}(5)=29\cdot449,
\]
\[
\Phi_{21}(5)=379\cdot519499,\quad
\Phi_{42}(5)=7\cdot43\cdot127\cdot7603.
\]
本包独立认证所有因子。7在Φ42中imprimitive，其order为6。过滤admission与exact order得到
\[
A_7=\{43,127,379,7603,19531,519499\}.
\]
它们分别有order42、42、21、42、7、21，全部s=1。故r不是nonregular root，所有B7已经满足|D|≥3。[S1；本包check_gates]

### 2.3 Three-vertex gate；以及本轮补出的充要方向

若D(q)={7,r,q}，r必须直接整除w_q，其余odd support只能为3、7。所以
\[
I(r)=r\{1,2,3,6,7,14,21,42\}.
\]
六组互不重合，总计48阶。这是Phase D的D4，不是本轮重新发明的候选定理。[S1]

**Theorem E1（固定48域中的充要平方条件）。** 对r∈A7、n∈I(r)，若q为已证明的prime、q≡3(mod4)、ord_q(5)=n，且q²|Φ_n(5)，则q是实际B7成员，D(q)={7,r,q}。

证明：r|n使r为直接descendant；w_r包含7，故7也在closure中。n的其余odd factors只有3和7，r的odd support是{7}或{3,7}，7仅指向3，所以完整D恰为这三个顶点，T={3}。7、r已认证regular；q因exact primitive square-hit为nonregular。全部orders squarefree，r与q都不是basal，Γ={7}。反向是D4和s_q=v_qΦ_n(5)。证毕。

因此“单个square-hit未必B7”在一般问题中必须保留；在本轮固定48阶中，只要素性、admission、exact order与平方条件全部认证，其他B7条件可以严格补齐。不能将此充要方向外推到任意阶。

### 2.4 Arbitrary-branching filling theorem 接口复核

给定实际q∈B7，R=D(q)\{q}。取一个共同a，使a≡4(mod6)、a≡0(modp)对全部p∈R；所有odd rows用K=2,E={1}，设置
\[
r_p\equiv3+5^a\pmod{p^2},\qquad
r_q\equiv3+5^a+q\pmod{q^2}.
\]
对于d≡4(mod6)，若存在regular p使d≠a(modp)，取数值最小者。其全部lower order factors已匹配；squarefree orders给w_p|d−a而p∤d−a，所以该row valuation恰为1。若所有regular coordinates匹配，则w_q|d−a，nonregular lifting给5^d≡5^a(modq²)，root row valuation恰为1。

这里一个a、每row一个residue，最后prime-square CRT合成一个global state。每个proper relay出现在某个parent order中，K=2时所需own digits有真实support。证明不假设线性路径，也不把local zero接受为fatal。[S1,D5]

因此literal prime-order chain仅是充分子类；排除48个三顶点阶仍不能排除具有更多vertices或branching的B7。[S5,S8] Pooled/Kraft中的raw rigid资源界不能逐层套到derived macros，也不能把EITHER与固定anchor/full certificate混同。[S9,S10]

## 3. THREE-VERTEX ORDER TABLE

D=Phase D已排除、本轮重证；E=本轮新增排除；未标记的阶仍OPEN。

|relay r|八个candidate exact orders|已关闭|partial factorization|未提取factor|
|---:|---|---:|---:|---:|
|43|43(D), 86(D), 129(D), 258(D), 301(E), 602(E), 903, 1806|6|2|0|
|127|127(D), 254(E), 381(E), 762(E), 889, 1778, 2667, 5334|4|3|1|
|379|379(E), 758(E), 1137, 2274, 2653, 5306, 7959, 15918|2|4|2|
|7603|7603, 15206, 22809, 45618, 53221, 106442, 159663, 319326|0|4|4|
|19531|19531, 39062, 58593, 117186, 136717, 273434, 410151, 820302|0|5|3|
|519499|519499, 1038998, 1558497, 3116994, 3636493, 7272986, 10909479, 21818958|0|3|5|

累计12/48 closed，36 open；其中21个partial、15个尚无提取因子。36个remainder分为14个PROVEN_COMPOSITE和22个UNKNOWN_NOT_PRP_TESTED_SYMBOLIC。UNKNOWN不表示PRP，更不表示prime或squarefree。每个open remainder仍可能包含admitted square prime divisor。

完整48行的known products、exact cofactor expressions、十进制位数、exceptional gcd在order_table.json及THREE_VERTEX_ORDER_TABLE.md；每个已提取prime的exact-order drop residues、q mod4、valuation、s、模q²值在arithmetic_records.json。

## 4. R=43：四个优先阶

|n|Φ_n(5)位数|已认证分解/剩余|结论|
|---:|---:|---|---|
|301|177|四个不同、已证明的prime；乘积完整|EXCLUDED，本轮新增|
|602|177|六个不同、已证明的prime；乘积完整|EXCLUDED，本轮新增|
|903|353|149930509 ×1562986310551 ×C903；C903有333位|OPEN；C903已证明composite|
|1806|353|43 ×246201060546547 ×C1806；C1806有337位|OPEN；C1806已证明composite|

### 4.1 301与602的完整素因子

下面列出每一个因子，均已证明prime，不是沿用Phase D的P/PRP标签。[S3只用于discovery]

#### n=301

```text
Phi_301(5) =
66221
* 3595452428681
* 453098474981964966729037498128705243871
* 1024695328986282069992499825233134533904997483977104628437112381314174950866343474485790683881553166943169107370165052251
```

|prime factor（完整数值见上式）|q mod4|exact order|v_q(Φ)|s_q|
|---|---:|---:|---:|---:|
|66221|1|301|1|1|
|3595452428681|1|301|1|1|
|第3因子，39位|3|301|1|1|
|第4因子，121位|3|301|1|1|

#### n=602

```text
Phi_602(5) =
14449
* 42743
* 176989
* 26041733579107
* 71398356223351054354479829866663025664388644310993593530081301
* 815848665960876101737817318523947330508259341603714676894206499333984664006434088162821
```

|prime factor（完整数值见上式）|q mod4|exact order|v_q(Φ)|s_q|
|---|---:|---:|---:|---:|
|14449|1|602|1|1|
|42743|3|602|1|1|
|176989|1|602|1|1|
|26041733579107|3|602|1|1|
|第5因子，62位|1|602|1|1|
|第6因子，87位|1|602|1|1|

所有相关admitted factors重数1；实际上所有因素均重数1，所以得到了比“只排除admitted square factors”更强的整数squarefreeness。因而
\[
q\in B7,\quad D(q)=\{7,43,q\}
\Longrightarrow w_q\in\{903,1806\}.
\]

### 4.2 903、1806的精确缺口

C903与C1806的完整十进制值分别存于cofactors/C_903.txt、C_1806.txt。四个Φ值全文位于cyclotomic_values/。它们满足
\[
C_{903}=\frac{\Phi_{903}(5)}{149930509\cdot1562986310551},
\qquad
C_{1806}=\frac{\Phi_{1806}(5)}{43\cdot246201060546547}.
\]
两个商的整除性由两条Φ计算路径重新检查；base2 strong-Miller–Rabin失败是确定性的compositeness witness。这里使用的是“失败证明composite”，不是“通过证明prime”。

903的两个已提取primes都有exact order903，分别为1、3(mod4)，s=1。13位因子1562986310551由定向ECM提取，然后另行认证。1806中246201060546547为admitted prime，exact order1806，s=1；43则只有order42，是imprimitive factor，v43Φ1806=1。二者cofactor均与所有已提取factors互素。

尚未完成两个cofactor的full factorization或squarefreeness proof。复合不等于有平方，有限ECM未命中也不等于squarefree。存在隐藏admitted square divisor仍未排除。

## 5. OTHER FIVE RELAY FAMILIES

新增关闭r127中的254、381、762，以及r379中的379、758。下表逐项列出其余open integers；F为已经证明且各出现一次的known prime product，C=Φ_n(5)/F。C表示PROVEN_COMPOSITE，U表示UNKNOWN_NOT_PRP_TESTED_SYMBOLIC。

|r|n|F|C位数|状态|
|---:|---:|---|---:|---|
|127|889|1|529|C|
|127|1778|4283203|522|C|
|127|2667|133351|1052|C|
|127|5334|127|1055|C|
|379|1137|1|529|C|
|379|2274|6823|525|C|
|379|2653|1|1586|C|
|379|5306|2642389|1579|C|
|379|7959|379 × 7401871|3162|C|
|379|15918|111427|3166|C|
|7603|7603|760301 × 1262099|5302|C|
|7603|15206|1|5314|C|
|7603|22809|1|10628|U|
|7603|45618|1|10628|U|
|7603|53221|1|31882|U|
|7603|106442|319327|31876|U|
|7603|159663|1596631 × 72806329|63749|U|
|7603|319326|7603 × 188721667|63751|U|
|19531|19531|3326871479|13642|U|
|19531|39062|11835787|13644|U|
|19531|58593|1|27302|U|
|19531|117186|42304147|27295|U|
|19531|136717|19531 × 546869|81896|U|
|19531|273434|1|81906|U|
|19531|410151|1|163811|U|
|19531|820302|3281209|163805|U|
|519499|519499|1|363114|U|
|519499|1038998|1|363114|U|
|519499|1558497|1|726227|U|
|519499|3116994|1|726228|U|
|519499|3636493|36364931|2178674|U|
|519499|7272986|1|2178682|U|
|519499|10909479|519499 × 327284371|4357349|U|
|519499|21818958|45536165347|4357352|U|

各family最小未决remainder：r127为C1778（522位）；r379为C2274（525位）；r7603为C7603（5302位）；r19531为C19531（13642位）；r519499为C519499（363114位，与C1038998同位数）。全局最小仍是r43的C903（333位）。这里的“最小”按当前剩余整数的十进制位数排序，不宣称对应prime factor最小。

对于22个symbolic objects，没有为报告强行物化最高4357352位的cofactor，也没有声称已经对它们做了PRP或squarefreeness测试。表达式精确且known factors已认证；位数通过有理log区间严格认证，不是浮点近似。每个整除关系可由prime exact-order/exceptional LTE定理验证，不依赖生成整个大整数。

全48阶还做了固定q=k*n+1、1≤k≤10000的divisor probe，不是一般nonregular prime scan。探测发现的每个保留factor均重新认证；探测无命中不用于任何全局排除。

## 6. SQUARE-HIT / DERIVATIVE / RESULTANT THEOREMS

### 6.1 Primitive valuation 与 exceptional factor

当n=ord_q(5)时q∤n，且q不整除任何proper-divisor cyclotomic factor，所以
\[
s_q=v_q(5^n-1)=v_q(\Phi_n(5)).
\]
因此primitive nonregularity当且仅当q²|Φ_n(5)。[S1,S5,S10；本轮逐factor复核]

若奇primeℓ|n且n squarefree，写n=ℓm。利用
\[
\Phi_{\ell m}(X)=\Phi_m(X^\ell)/\Phi_m(X)\quad(\ell\nmid m)
\]
和modℓ约化，可知ℓ|Φ_n(5)当且仅当ord_ℓ(5)=m；此时LTE给vℓΦ_n(5)=1。2与5不整除本轮这些Φ值。因此48阶的全部imprimitive factors恰为下面六个。

|r|w_r|唯一exceptional n=r*w_r|v_rΦ_n(5)|s_r|
|---:|---:|---:|---:|---:|
|43|42|1806|1|1|
|127|42|5334|1|1|
|379|21|7959|1|1|
|7603|42|319326|1|1|
|19531|7|136717|1|1|
|519499|21|10909479|1|1|

这里还特别验证：5^1806≡1(mod43²)，但5^42不≡1(mod43²)，而ord43(5)=42。仅检查5^n−1的平方整除会把regular imprimitive factor误当作nonregular终端。

### 6.2 Theorem E2：48阶的 exact derivative gcd

\[
\boxed{\gcd(\Phi_n(5),\Phi'_n(5))=
\begin{cases}
r,&n=r w_r,\\
1,&\text{其他42阶}.
\end{cases}}
\]

证明：若q|Φ_n(5)、q∤n，X^n−1在characteristic q中separable，因而Φ'_n(5)不被q整除。不论v_qΦ_n(5)是1还是≥2，此结论都成立。

对六个exceptional factors r，modr有Φ_{rm}(X)=Φ_m(X)^{r−1}。5是Φ_m的simple root，且r≥43，故它在Φ_{rm}中为重根，r整除derivative。但v_rΦ_{rm}(5)=1，所以gcd中r只出现一次。上节已经排除其他index-prime factors。证毕。

程序直接重算四个优先阶的gcd为1、1、1、43；其余44阶采用上面有限exception分类与separability证明，而不是冒称全部巨大polynomials均已构造并求导。

**这不是squarefree theorem。** Primitive square divisor从来不出现在这个gcd里，所以gcd=1完全不能排除q²|Φ_n(5)。Cyclotomic discriminant/resultant控制polynomial roots碰撞；它不提供本轮固定整数lift的squarefree认证。没有找到一个真正更小、可分解且能普遍截住剩余primitive square divisors的固定arithmetical invariant。

### 6.3 Theorem E3：48个 cyclotomic values 两两互素

若prime同时整除两个不同Φ值且都primitive，它将拥有两个不同exact orders，矛盾。若某处imprimitive，则它是上表的r；其actual order w_r≤42，而48个indices均≥43，不可能在另一处primitive。作为imprimitive又只能出现在唯一n=r*w_r中。故48个值两两互素。

这阻止在不同indices之间重复计算同一prime，但不能推出任一单独Φ值squarefree。

### 6.4 Hensel/lifting 的精确表述与失败范围

对primitive q，f=Φ_n，f'(5) modq可逆。令u=f(5)/q modq，则唯一Hensel lift写成5+tq，满足
\[
t\equiv-u\,f'(5)^{-1}\pmod q.
\]
固定整数5本身已经是modq² root，当且仅当t=0，当且仅当u=0。这重述了square-hit，而不是由simple root推出其不可能。

LTE同时给
\[
\operatorname{ord}_{q^k}(5)=nq^{\max(0,k-s_q)}.
\]
因而s≥2时order到q²不增长，s=1时增长为nq。

q≡3(mod4)只给已有quadratic-residue必要条件：n odd时q≡11或19(mod20)，n even时q≡3或7(mod20)。它们不排除Hensel correction为0。[S10]

实际control q=20771≡3(mod4)，order10385=5*31*67 squarefree，s=2。本包证明其prime/order/q²与q³关系，说明“admission + squarefree order ⇒ regular”本身为假。它不是B7成员，因为order含free terminal5，不能冒作本轮成功terminal。B7更强的递归odd support能否排除所有square-hits，仍未解决。

## 7. 低阶扩展：不只适用于三个vertices

### Lemma E4 — Small regular basin inventory

定义regular B7-compatible prime p：以p为顶端的完整admitted closure全部regular，全部orders squarefree，T(p)={3}、Γ(p)={7}。对p≤2287，这些primes恰为
\[
\{7,43,127,379,2287\}.
\]

认证方法：完整trial division得到7≤p≤2287的173个admitted primes；producer以factor-removal求order，另写verifier以逐次乘5首次回到1求order，并显式遍历每个prime的完整closure/terminals/basal gateways。173个结果逐项一致。2287为prime，order254，s=1，故它是继A7小节点之后出现的下一regular-compatible vertex。完整数据是small_relay_inventory.json。

### Theorem E5 — Low-order B7 gate

设q∈B7且w_q<2287。任何proper descendant都不大于某个direct order factor，因此均<2287，且本身为regular B7-compatible。它们只能在{7,43,127,379}中。

43、127、379的orders仅含3、7，所以这些三个relays互相不可达。若其中至少两个出现在D(q)，它们都必须直接整除w_q，从而
\[
w_q\ge43\cdot127=5461>2287,
\]
矛盾。另一方面first-relay gate已经保证至少两个proper vertices。因此|D(q)|=3。

48阶中小于2287且未被本轮排除的恰为
\[
\boxed{889,903,1137,1778,1806,2274.}
\]
因此
\[
\boxed{q\in B7,\ w_q<2287\Rightarrow
|D(q)|=3\text{ and }w_q\in\{889,903,1137,1778,1806,2274\}.}
\]
立即得到w_q≥889，以及|D(q)|≥4⇒w_q≥2287。这里并未证明有w=2287的nonregular root，也没有排除深basin；只是一个经过有限relay gate支持的无条件必要限制。

## 8. FACTORIZATION CERTIFICATES

### 8.1 Final proof DAG

primality_certificates.json包含341个已证明primes（含ancestry，不是341个新relay）：101个bounded trial leaves、104个partial n−1 Pocklington节点、136个elliptic-curve节点。75个factor records全部由这个proof DAG支持。

Pocklington节点给出已认证prime powers乘积F|(N−1)，F²>N，并对每个prime ℓ|F给a：a^(N−1)=1 modN，gcd(a^((N−1)/ℓ)−1,N)=1。递归素性由较小primes支持。

EC节点不要求相信CM discovery、floating point class polynomials或任何PRP结果。给出曲线y²=x³+Ax+B modN、affine point M、较小已证明prime Q，逐项检查：gcd(N,6)=1；discriminant与N互素；M在曲线上；每个affine加法分母是modN的unit；Q*M=O；
\[
Q>(\lfloor N^{1/4}\rfloor+2)^2>(N^{1/4}+1)^2.
\]
若N composite，取prime p≤sqrtN。M modp非零，且Q为prime、QM=O，所以其order恰为Q。但Hasse界给#E(F_p)≤(sqrtp+1)²≤(N^(1/4)+1)²<Q，矛盾。由较小prime递归即可证明N prime。

这种certificate与PRP的区别及可独立重放的设计原则亦见primary ECPP作者说明[X3]；本包并未调用该作者的软件，而是自写发现器与验证器。

### 8.2 Discovery/verification independence 与边界

Discovery用SymPy、mpmath、Cunningham primary table[X1]，以及定向ECM。外部P标签只作hint。本轮301/602补全了Phase D尚未完成的素性证明；379/758的大因子也取得完整证书，而非直接信任table标签。

最终verifier只用Python标准库，不import SymPy、mpmath、repository implementation或CM数据。EC discovery使用右向左标量乘法，verifier另写左向右版本；cyclotomic products由Möbius公式与divisor-recursion两路构造；小relay order另用直接乘法重证。

这是同一研究会话内的不同计算核心，不是独立团队审稿，也不是完全独立硬件/语言软件栈。无限参数定理仍需要独立作者数学审阅。

### 8.3 Actual replay receipts

```
python -B verify.py --suite core --self-test --output verification_core.json
python -B verify.py --suite cofactors-a --output verification_cofactors_a.json
python -B verify.py --suite cofactors-b --output verification_cofactors_b.json
```

三项已实际执行并PASS。core验证341个prime nodes、75个factor records、48个metadata rows、12个完整squarefree产品、4个first-relay产品、6个relay gate、4个derivative gcd、173个small-relay primes与15项mutations。cofactor suites合计验证14个完整decimal cofactors、两路精确乘积与compositeness witnesses。

故障注入包括错误素性witness、singular EC curve、EC child/threshold错误、wrong exact order、imprimitive当primitive、s=1升级s=2、遗失factor、未证squarefree升级、错误exclusion flag，全部拒绝。

## 9. ALL COMPLETE FACTORIZATIONS

这里给出12个完整产品的全部已认证prime factors。所有因子各出现一次，且这些12阶没有imprimitive因子。所有因子的exact order均为本section标签n；逐项q mod4与s见ARITHMETIC_RECORDS.md。

### n=43 (D_REVERIFIED)

```text
1644512641
* 172827552198815888791
```

### n=86 (D_REVERIFIED)

```text
1549
* 9547
* 7866608083
* 1628744948329
```

### n=127 (D_REVERIFIED)

```text
14693679385278593849609206715278070972733319459651094018859396328480215743184089660644531
```

### n=129 (D_REVERIFIED)

```text
18471511
* 43955934961951833386625799
* 51349797354047205216257689
```

### n=254 (E_NEW)

```text
509
* 2287
* 2735581
* 3076137716865400512817630590222174947182195052472086065321936995866231846027
```

### n=258 (D_REVERIFIED)

```text
327845761
* 558801427
* 1420986601
* 236419892853700126919767791480523
```

### n=301 (E_NEW)

```text
66221
* 3595452428681
* 453098474981964966729037498128705243871
* 1024695328986282069992499825233134533904997483977104628437112381314174950866343474485790683881553166943169107370165052251
```

### n=379 (E_NEW)

```text
15919
* 19709
* 154593500445308877590595293456916511
* 41860079499485222307790780950329804339254636245435997529042203803559017464055721228065828012877736510442196227999749027441133636793780515165996915707368994923112234114211497494818757357039023864566980225773307642997757251
```

### n=381 (E_NEW)

```text
17365824770202511
* 2146271536375625882474712607488854837881
* 12882995722731844746940951540119250212241259630747509
* 232071850047734595810657641340191685995462669499867768115441253013859
```

### n=602 (E_NEW)

```text
14449
* 42743
* 176989
* 26041733579107
* 71398356223351054354479829866663025664388644310993593530081301
* 815848665960876101737817318523947330508259341603714676894206499333984664006434088162821
```

### n=758 (E_NEW)

```text
4549
* 37850067509
* 1343210014472411202426336065918923
* 5852667834365265642377407987102078112780734782396261068400422031577661759789757267376446582248467291768158865972429662727624006457139348054081628782862674240955984786641570754883282726024586372368002670342607737181047
```

### n=762 (E_NEW)

```text
23623
* 88128349
* 2906725201
* 967413475393459207
* 560679020564216733169
* 50116497076043011292644300325792931605363741164567945635824747420212771457187363742792084016298108729590292265691341
```

## 10. FINAL REQUIRED FLAGS

```
ACTUAL NONREGULAR TERMINAL FOUND?
NO

ALL 48 CLOSED?
NO — 12 closed, 36 open

THREE-VERTEX B7 EMPTY?
NO — NOT PROVED, not a claim that it is nonempty

B7 EMPTY?
NO — NOT PROVED, not a claim that it is nonempty

N>=8?
NO — not established
```

## 11. STRONGEST NEW ARITHMETIC CONCLUSION

\[
q\in B7,\ D(q)=\{7,43,q\}\Rightarrow w_q\in\{903,1806\},
\]
其中对应候选square-hit分别被压到一个明确333位composite cofactor和一个337位composite cofactor。所有48阶累计严格排除12个；并有全B7的w_q≥889与四顶点及以上的w_q≥2287。

没有从额外regular relays推断N>=8，没有把12个已关闭阶外推到全部48，没有把three-vertex class等同于arbitrary-branching B7。

## 12. NEXT SINGLE TARGET

**证明333位C903没有admitted square prime divisor，或提取并认证一个。**
\[
C_{903}=\Phi_{903}(5)/(149930509\cdot1562986310551).
\]
full squarefreeness足以关闭该阶，但不是必须：只要排除q≡3(mod4)的square factors也足够。若找到这样的q，必须先证明prime、exact order903、s≥2，再应用E1完整验证D={7,43,q}与B7 gateway；不将未认证square-hit当作成功。

```
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
