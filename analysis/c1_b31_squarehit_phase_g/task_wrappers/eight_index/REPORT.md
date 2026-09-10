# A303656 — B31^odd 八指标共同结构，Targeted Phase G

## 0. 结论

**八个indices均未关闭，两个完整four-index relay families均未关闭。**

本轮结果等级：**D，严格限定的整族方法排除**。无界结果不是“八指标无square hit”，而是：四倍乘数的二阶条件没有新增独立性；一个自然的整族Aurifeuillean包装已经完成全部Q[T]不可约分解，不存在所希望的进一步标准分裂。本轮未得到A/B/C所要求的算术关闭或新的共同更稀疏terminal class。

以下区分源定理特化、新路线审计、换底数对照和文献bounded gate，不把重述计作新排除。推荐执行环境：网页端研究及标准库reference laboratory；无Codex、无大型scan。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656 (ID 1333945235)
main: c6ca0dc061783ab993be6fa077c8f66cd730e28c
tree: 57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06
PR #30–#37: merged=true
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

已重新live读取main与STATUS，而非采用交接SHA作未经核验authority。四个相关包核心REPORT和INTEGRATION范围均已读取。未逐文件读完全部辅助代码、manifest、生成数据和日志，故不能标为“所有required directories完整逐文件审计PASS”。未取得源字节checkout、未复跑源runner/旧scan/repository tests；具体边界见`SOURCE_BINDING.json`。

## 2. SOURCE THEOREM RECONSTRUCTION

Phase F F1证明first-relay全集恰为r₁=878851与r₂=625552508473588471，均regular，orders分别93、31。F3的三顶点iff使用全部actual proper closure，而非挑选一条有利路径；任何admitted平方命中自动primitive，因为imprimitive valuation恰为1。

F4以maximal-generator antichain定义exact family J31(R)，normalized C_n两两互素，给exact-state root iff。SQD Phase F的no-migration说明不能把一个实际square-hit q转移到另一个exact state。这里并没有证明different-prime replacement不可能。

O31的whole-basin条件包括root与全部admitted descendants>3，不包括terminal3。Seven-Basin的状态存在性iff有actual七盆地normal-form及允许选择合法K/E的范围；本轮不以未知七个roots作已经存在的算术输入。

## 3. EXACT FAMILY

|m|r₁=878851|r₂=625552508473588471|
|---:|---:|---:|
|1|878851|625552508473588471|
|3|2636553|1876657525420765413|
|31|27244381|19392127762681242601|
|93|81733143|58176383288043727803|

对任一n=mr，prime q≡3 mod4且q²|Φ_n(5)，当且仅当它给出proper closure={31,r}且exact order=n的actual三顶点member。

本轮研究整个矩形family；没有把八次独立blind factorizations当作共同结构研究。

## 4. NEW LEMMAS / SHARED FORMULAS

### 4.1 共同多项式与归一化（继承特化）

令F_m(X)=Φ_(mr)(X)，H_d(X)=Φ_r(X^d)，则d|93时

    H_d(X)=∏_{m|d}F_m(X).

于是

    Z_r=∏_(m|93) C_(mr)
       =Φ_r(5^93)/r
       =(5^(93r)−1)/[r(5^93−1)].

唯一normalizer r₁在m=93，r₂在m=31。八个raw Φ-values事实上也两两互素，故不存在cross-factor拼平方。此段是Phase E/F机制在B31八指标的精确特化，不是新squarefree证明。

### 4.2 G1：倍乘不能提供独立double-Wieferich

对固定exact order mr，v_q(H_d(5))仅在m|d时等于同一个s，否则为0。

|m\d|1|3|31|93|
|---:|---:|---:|---:|---:|
|1|s|s|s|s|
|3|0|s|0|s|
|31|0|0|s|s|
|93|0|0|0|s|

活跃条件s≥2完全相同。Q_q(5^d)=dQ_q(5) modq也仅是同一条件的unit倍数。这里没有对不同q之间的随机独立性作统计断言。

### 4.3 G2：整个自然参数化的完整不可约分解

八个n均不被5整除。通用valuation-degree论证给

    Φ_n(5T²)在Q[T]不可约。

从而对两个relay分别有完整有理不可约分解

    Φ_r((5T²)^93)=∏_(m|93)Φ_(mr)(5T²).

原来的四个分圆因素就是全部，不存在进一步非平凡Q[T]分裂。Aurifeuillean、Cunningham或Sophie-Germain型身份只要想在这个参数化下再分裂，都受到这一结论约束。

范围必须限定为这个参数化和有理多项式分裂；不是“所有norm路线无用”，更不是数值squarefree。

### 4.4 G3：quadratic/higher residue审计

目标n的每个素因子ℓ均3 mod4，q≡1 modℓ给(ℓ/q)=−1；但D=(−1)^((n−1)/2)n满足(D/q)=+1，Gauss quadratic norm处于split情形。q3 mod4时普通四次、八次等2-primary power-residue像与平方相同。没有得到同余矛盾。

## 5. PROOFS

全部公式及证明见`PROOFS.md` G0–G3。

G1由唯一exact-order因子与unit补因子直接推出，保留所有分母合法性。G2的证明使用K=Q(ζ_n)在5处unramified，以及α²=ζ_n/5的valuation分母2，强制[K(α):K]=2；总次数2φ(n)保证不可约。更一般的gcd(v_ℓ(c),d)=1版本同理。

平方代换后的整族分解是G0.1的多项式身份与G2的逐因子不可约性组合，不由有界试分解外推。两个r的大小对证明无影响。

“simple root⇒数值squarefree”在Phase E已被否定。本轮没有用它，也不把重新发现这一错误计作新结果。

## 6. COUNTEREXAMPLE ATTACKS

**准确hypothesis对照：** n=5违反5∤n，Φ_5(5T²)确实分成两个四次因子；完整系数在证明与程序中。n=3,c=30满足不可约定理却有Φ_3(30)=7²·19，排除不可约⇒squarefree的误读。

**exact-target variable-base对照：** 以源regular q₀=490398859，分别对m=1,3,31,93构造A_m，保持A_m≡5 mod(4·3²·5²·31²·r₁²)，在q₀²选取order mr₁的Teichmüller lift。四个实际A_m完整列于`PROOFS.md`及`evidence.json`。

每例认证：q₀prime、3 mod4、exact root order mr₁、root s=2、proper closure恰{31,r₁}、下层all-odd且regular，v₅(A_m)=1。四列composition valuations与G1完全一致。由此可直接反驳相应base-uniform局部排除，但不能反驳真正使用整数5全局特征的定理。

这些不是base5 B31成员。CRT机制继承Phase E E8；新内容是四指标上的可重放特化，而非一个新泛化CRT定理。

## 7. COMPUTATION AND LITERATURE

标准库reference验证57个recursive Lucas prime certificates、两个first-relay完整乘积、四个目标参数换底数模型、四个小指标regular模型、八个小多项式composition身份、两个normalized aggregate modr²恒等式、符号关系和六个已知odd base5 Wieferich解。

aggregate modr²对两r均用精确模乘幂及可认证整除计算，最大模数394 bits；没有构造聚合巨数。该残数关系约束完整因子分解，不约束某个指定terminal q，不计为新稀疏gate。

文献复核：Dorais–Klyve第7页§4.1确为base5提供到B=970453984500000的历史穷尽搜索。六个奇解的exact orders全部不是八指标。采用该已发表结果可排除目标q≤B；本轮只重算六个实例，未复跑历史搜索，不声称当前最高界。

未重复k≤10^6；未扩大general q scan；未物化八个Φ-values。文献结果是BOUNDED EVIDENCE ONLY，不是family closure。

## 8. WHAT IS ACTUALLY CLOSED

整族方法层面：

- 四倍乘幂/分圆商本身提供第二个独立lifting条件的说法被精确依赖定理排除。
- Φ_r((5T²)^93)包装下的进一步Q[T]分裂路线被完整不可约分解排除。

算术层面：新关闭indices为0/8，新关闭完整relay families为0/2，没有actual base5三顶点member，也没有新共同更稀疏terminal q类。

这里的D不是“所有共同algebraic obstruction都不可能”；其他精确定义的方法仍未排除。

## 9. WHAT REMAINS OPEN

两个Z_r是否含admitted prime square均未判定。三顶点空性未证；更大closed states也未约束为有限深度。单个minimal state即使关闭也不会自动推出一般B31^odd空。

primitive lifting、Teichmüller、唯一degree-one prime ideal和trace变换都没有产生额外条件。没有一个适用的Stickelberger/Jacobi-sum/cyclotomic-unit theorem被落实到目标；这只是本轮未取得结果，不是全部文献或未来方法的不可能性声明。

## 10. NEXT SINGLE TARGET

**回到n=878851，设计无需预设完整分解的admitted-square-part可重放证书接口。** 先证明soundness并给小指数正负样例，明确缺少的数学输入，再决定有无可授权的大计算。不要再将四个powered-base quotients视为独立，也不要继续机械延长k扫描。

```text
B31^odd THREE-VERTEX EMPTY: NO — not proved
MINIMAL STATE R={31,878851} CLOSED: NO
SECOND RELAY FOUR-INDEX FAMILY CLOSED: NO
ACTUAL BASE-5 B31^odd MEMBER: NO
B31^odd EMPTY: NO — not proved
EXACTLY-SEVEN: NOT KILLED
N>=8: NOT PROVED
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

证明、来源边界、证据与replay文件均在包内。没有GitHub write，没有authority/status变更。
