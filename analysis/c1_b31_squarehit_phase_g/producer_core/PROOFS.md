# Phase G — 证明、路线边界与反例

本文件与两个任务报告共用。G1–G5 是本轮整理的可审阅推导，不主张文献优先权；不是 proof-assistant formalization。标为“继承/特化”的内容不计作新排除。有限程序只核验实例，不证明全参数定理。

记 r₁=878851，r₂=625552508473588471，M={1,3,31,93}。

## G0. 来源定理及八指标的准确归一化（继承/特化）

对奇素数 ℓ≠5，令 f=ord_ℓ(5)，s=v_ℓ(5^f−1)。Phase E 的完整 valuation theorem 为

    v_ℓ(Φ_n(5)) = s  if n=f;
                    1  if n=fℓ^j, j≥1;
                    0  otherwise.

证明可由 LTE 与 5^N−1=∏_{d|N}Φ_d(5) 的 divisor-sum inversion 给出。特别地，imprimitive prime 永远只出现一次，不限于 squarefree n。

Phase F 已证明 r₁、r₂ 均为 regular，orders 分别为93、31；31 的 order 为3、regular。F3 因而给出

    q prime, q≡3 mod4, q² | Φ_(mr)(5)
    iff q 是 proper admitted closure 恰为 {31,r} 的三顶点 B31^odd member，且 order=mr。

这里逆向不依赖某个未知 shared state；它是 intrinsic arithmetic iff。与全局七盆地证书的 iff 不是同一个命题。

### G0.1 四指标恒等式

令 F_m(X)=Φ_(mr)(X)。因 r∤93：

    F_1(X)  = (X^r−1)/(X−1),
    F_3(X)  = (X^(3r)−1)(X−1)/[(X^r−1)(X^3−1)],
    F_31(X) = (X^(31r)−1)(X−1)/[(X^r−1)(X^31−1)],
    F_93(X) = (X^(93r)−1)(X^3−1)(X^31−1)(X^r−1)
              /[(X^(3r)−1)(X^(31r)−1)(X^93−1)(X−1)].

这些是 Q(X) 中的恒等式，商约去后在 Z[X] 中。不得直接在分母为0的有限域点作除法。

更紧凑地，对 d|93：

    H_d(X):=Φ_r(X^d)=∏_{m|d}F_m(X).

可由根的 exact order 证明：α^d 的阶为 r，当且仅当 α 的阶为 rm，其中 m|d；因 gcd(r,d)=1，全部根恰分入这些互异分圆因子。

所以四因子聚合为

    W_r = ∏_{m|93} Φ_(mr)(5)
        = Φ_r(5^93)
        = (5^(93r)−1)/(5^93−1).

唯一 imprimitive factor 是 r，且出现于 m=w_r：r₁ 对应 m=93，r₂ 对应 m=31。3 的 base-5 order 为2，不可能在本轮奇指标中产生 imprimitive 因子；31 的 order 为3，其 imprimitive 指标3·31^j不含r。其余可能的 index prime 只有r，应用 valuation theorem 即得上述结论。

故精确 normalized critical integer 为

    Z_r = W_r/r = (5^(93r)−1)/[r(5^93−1)].

八个未归一化 Φ-values 实际亦两两互素。若不同指标有共同素数ℓ，valuation theorem 迫使指标之比为ℓ的幂。同一relay内只可能ℓ=3或31，已被其orders排除；不同relay之间两个指标互不整除，因为每个都含自己的大素数r而不含另一个。由此没有跨因子“一次×一次”拼成平方的问题。

四指标状态关闭 iff Z_r 没有3 mod4素数平方因子。完整八指标关闭 iff Z_(r₁)Z_(r₂)没有这种平方因子。写出这些式子并不是平方自由证书。

## G1. 四倍乘数的二阶条件只有一个独立提升条件

### 定理 G1

令 r 是不整除93的素数，q>93是素数，q∤a，且

    ord_q(a)=mr,  m|93.

记 s=v_q(Φ_(mr)(a))。对每个 d|93：

    v_q(Φ_r(a^d)) = s  if m|d;
                    0  if m∤d.

在本任务应用中 q>mr≥r>93，所以相关 characteristic/index 例外均不存在。

### 证明

由 G0.1：Φ_r(a^d)=∏_{e|d}Φ_(er)(a)。所有er与q互素。一个因子被q整除，当且仅当 ord_q(a)=er；因此只有e=m可能被整除。它出现在乘积中 iff m|d，且其余因子均为q-adic units。乘积的valuation恰为s或0。证毕。

在各自 exact-order stratum 内的依赖表为：

| m \ d | 1 | 3 | 31 | 93 |
|---:|---:|---:|---:|---:|
|1|s|s|s|s|
|3|0|s|0|s|
|31|0|0|s|s|
|93|0|0|0|s|

这里不能把同一行中多个s解释成多个独立的square-hit事件。不同的行对应不同exact orders，不是在同一个q上同时发生的四个条件。

### G1.1 Fermat quotient 版本

定义 Q_q(a)=(a^(q−1)−1)/q modq。二项式展开立即给出

    Q_q(a^d)=dQ_q(a) modq.

本轮d|93，q>93，故d非零。这些quotients的同时消失与单一Q_q(a)=0完全等价。

同样，若 n=ord_q(a)，h=(q−1)/n，则

    Q_q(a)=h[(a^n−1)/q] modq,

h是unit。将一个幂商改写成另一个幂商不会产生第二个独立障碍。

更准确的局部形式是：在一个固定 exact-order-mr 模q根 a₀ 的 lifts a₀+qt 上，每个活跃 H_d 的唯一成功 digit 相同。因为 H_d=F_m·U_d 且 U_d(a₀)为unit，模q²条件 H_d(a₀+qt)=0 与 F_m(a₀+qt)=0相同。这是上述乘积恒等式的后果，而不是“零点简单所以不能平方”的错误论证。

### G1.2 严格范围

此定理排除的是：仅靠 a→a³、a³¹、a⁹³ 和上述分圆商，声称得到独立double-Wieferich条件。它不排除引入与a的幂乘法独立的新单位、非平凡加法关系、或其他确切算术输入。

对其他整数base b，Q_q(b)=0并不从Q_q(a)=0一般推出。例如实际base5的q=20771有Q_q(5)=0，但Q_q(31)=4907、Q_q(67)=3395，均非零。本例不属于目标pure3类；它只反驳不加目标额外条件的泛化。

## G2. 5-adic irreducibility：整族标准多项式分裂路线关闭

### 定理 G2（一般形式）

设 ℓ 为素数，ℓ∤n，c∈Q×，v_ℓ(c)=a，d≥2且gcd(a,d)=1。则

    Φ_n(cT^d) 在 Q[T] 中不可约。

### 证明

取本原n次单位根ζ，K=Q(ζ)。ℓ∤n保证K在ℓ处unramified。亦可从 X^n−1 moduloℓ的separability看出：Φ_n的discriminant在ℓ处为unit，field discriminant整除该order discriminant，故没有ℓ-ramification。

取任一P|ℓ，使用v_P(ℓ)=1的离散valuation。ζ是unit，所以v_P(ζ/c)=−a。

取α满足 cα^d=ζ，并令L=K(α)。在P上方的一处延伸中，v(α)=−a/d。因为gcd(a,d)=1，该valuation的分母为d，故该局部扩张的ramification index至少为d，因而[L:K]≥d。另一方面α满足一个d次二项式，所以[L:K]≤d。因此[L:K]=d。

又ζ=cα^d属于Q(α)，故K⊂Q(α)，且

    [Q(α):Q]=d[K:Q]=dφ(n).

这正是Φ_n(cT^d)的次数；α的最小多项式已经达到总次数，因此Φ_n(cT^d)不可约。证毕。

### G2.1 八指标应用

八个n均与5互素。取ℓ=5,c=5,a=1,d=2，得到

    Φ_n(5T²) 对全部八个n都在Q[T]不可约。

同样，对m∈{1,3,31,93}，因m为奇数，Φ_r(5^m T²)不可约。

对于一个relay，结合G0.1还有更强的准确表述：

    Φ_r((5T²)^93)=∏_{m|93}Φ_(mr)(5T²)

右侧四个因子已经是完整的有理不可约分解（忽略非零有理常数）。所以将四个指标包装到这个共同多项式之后，不存在第五个非平凡的有理多项式分裂步骤。

注意Φ_r(5^m T²)与Φ_r((5T²)^m)=Φ_r(5^m T^(2m))不同；后者本来有G0.1给出的分圆分解，不能混淆。

### G2.2 与 Aurifeuillean / norm 路线的关系

Brent记录的Gauss与Aurifeuillean恒等式给出平方差/平方和形式。某个平方差只有在相应radical可在所选参数域中处理时，才给出有理多项式分裂。G2严格排除了本轮 c=5T² 代换所希望得到的那种进一步Q[T]分裂；同时覆盖这种代换下的Cunningham或Sophie-Germain-type非平凡Q[T]因式分解，无论名称如何。

这不排除所有norm方法，不排除数域中分解，不排除不同参数化，不排除整数5代入后的偶然数值因子。

一个相关事实是√5∉Q(ζ_n)：左边的二次域在5处ramified，右边unramified。因此仅以Q(√5)作为二次子域来裂开这些Φ_n也不成立。但任何更大数域或其他norm方法并未由此全部排除。

### G2.3 两个必须保留的反例边界

当5|n时，定理的前提失效；n=5有实际分解

    Φ_5(5T²)
      =(25T⁴−25T³+15T²−5T+1)
       (25T⁴+25T³+15T²+5T+1).

这是正对照，不是对G2的反例。

更重要的是，G2绝不蕴含整数值squarefree。取n=3、c=30、ℓ=5、d=2，G2证明Φ_3(30T²)不可约；但T=1时

    Φ_3(30)=931=7²·19,
    ord_7(30)=3,
    Φ'_3(30)=61≠0 mod7.

所以“unramified + 不可约 + prime index + admitted q”仍完全允许平方命中。底数30不是5。这个例子同时阻止把本轮路线排除升级成目标算术关闭。

## G3. Reciprocity、trace与norm能提供什么

### G3.1 直接edge符号没有冲突

所有目标n的素因子ℓ都满足ℓ≡3 mod4。若q≡3 mod4且n|q−1，则q≡1 modℓ。Quadratic reciprocity给

    (ℓ/q)=−(q/ℓ)=−1.

令t=ω(n)，D=(−1)^((n−1)/2)n=(−1)^t n，则

    (D/q)=(−1/q)^t ∏_(ℓ|n)(ℓ/q)=(−1)^t(−1)^t=+1.

因此Gauss二次子域正好是split，不是inert。利用inert prime对二元norm的整除性质制造矛盾，在这里连前提都不满足。

与此同时，odd ord_q(5)给(5/q)=1，即q≡11或19 mod20。这与全部edge符号相容。对m不含31或3的情况，不得无证明地把该数当作q的直接order parent。

### G3.2 更高幂剩余的准确边界

q≡3 mod4时，|F_q×|只有一个2因子。因而对每个j≥1，2^j次幂的像与平方的像相同。普通“5还是四次/八次幂剩余”不是比(5/q)=1更严格的筛选。这里不否认在扩域中有更精细的reciprocity，但必须另给定义及输入。

对ℓ|n（n squarefree），写q−1=nh。一个exact order n元素是ℓ次幂 iff ℓ|h。证明：取生成元g，a=g^(hu)，gcd(u,n)=1；它是ℓ次幂 iff ℓ|hu iff ℓ|h。因此这件事仅编码q−1中ℓ的指数，并不从q²-lifting产生新约束。

### G3.3 降阶trace是准确等价，但不是新障碍

对n>2，令h=φ(n)/2。存在Ψ_n∈Z[Y]，使

    Φ_n(X)=X^h Ψ_n(X+X^−1).

在base5处，primitive q给

    v_q(Φ_n(5))=v_q(Ψ_n(26/5)),

右侧按Z_(q)理解，因为q≠5。p=878851时Ψ的次数降至439425。但是变量变换的导数1−5^(−2)=24/25在primitive q处为unit：q不能是2、3、5。因此同一个一阶lifting参数只是经过可逆坐标变换，没有获得第二个独立消失条件。

### G3.4 Cyclotomic ideal与深定理的适用义务

Phase E已证明：q≡1 modn且5具有exact order n时，K=Q(ζ_n)内q完全分裂，恰有一个P=(q,ζ_n−5)整除5−ζ_n，并且

    v_q Φ_n(5)=v_P(5−ζ_n).

P²|(5−ζ_n)不表示其他conjugate primes也整除同一个元素，不表示ramification，也不表示整个principal ideal是平方或r次幂。

Stickelberger、Jacobi sums、Kummer/cyclotomic-unit方法在本轮没有给出一个适用且额外限制q的定理。不能从单个局部valuation≥2直接补出全局ideal-power、unit或class-group假设。这是输入缺口的记录，不是“这些深方法全都不可能”的定理。

## G4. 四个exact-target换底数反例证书（Phase E E8的特化）

此处不是发现base5成员，而是对拟议base-uniform局部证明作对抗检查。

选已在Phase F出现的regular素数q₀=490398859；其base5 exact order为93r₁，且q₀−1=6·93r₁。本轮不搜索q₀。

设

    L=4·3²·5²·31²·r₁²,
    ω_m=5^((93/m)q₀) mod q₀²,
    A_m≡5 modL,
    A_m≡ω_m modq₀².

CRT可解且唯一模Lq₀²。ω_m是5^(93/m)的Teichmüller lift moduloq₀²，因此ord_(q₀)(A_m)=mr₁且A_m^(mr₁)=1 modq₀²。下层31、r₁的orders和regularity因模平方同余保持。额外加入5²模数保证v₅(A_m)=1；所以G2的irreducibility条件也保持。

程序给出最小非负解：

|m|A_m|
|---:|---:|
|1|70602295045730533920731272137800405|
|3|3328861110890542104637883579835605|
|31|106502391624211553419360119810724505|
|93|101668995081320798945080086074262905|

四个root的s均精确为2；proper admitted closure恰为{31,r₁}；31、r₁仍是all-odd regular。用Möbius乘积在modq₀³计算Φ_(mr₁)(A_m)，没有物化这些巨大整数。

这给出四个实际换底数类比成员，包含prime index r₁本身；它们不是base5 B31^odd成员。这一构造继承Phase E E8的CRT机制，本轮新增的是本任务参数上的完整可重放实例，不重新计为一个新的普遍CRT定理。

q₀处还有

    Q_(q₀)(3)=21026881,
    Q_(q₀)(31)=182795056,
    Q_(q₀)(r₁)=279869015.

均非零。所以下层edge的reciprocity、orders、regularity及top square hit，不会base-uniform地自动强迫这些独立整数base也Wieferich。

固定整数base5的额外全局性质没有被反例抹去。任何利用“底数恰等于5”的证明仍可能成功。

## G5. 可核验的文献有界gate

Dorais–Klyve，JIS14(2011), Article11.9.2，第7页§4.1，报告对base3、5、7完整搜索到（含端点）

    B=(2·3·5·7·11·13·17·19·23·29)·150000
     =970453984500000.

没有新增base5解。论文标题的6.7×10^15是base2范围，不可移用于base5。期刊页记载2011-10-16发表。OEIS A123692列出六个奇解；本轮对它们另给素性和exact-order/valuation证书：

|q|ord_q(5)|q mod4|s|
|---:|---:|---:|---:|
|20771|10385|3|2|
|40487|40486|3|2|
|53471161|13367790|1|2|
|1645333507|1645333506|3|2|
|6692367337|6692367336|1|2|
|188748146801|11796759175|1|2|

均不是八指标。2不admitted，也不在目标exact-order类。因此，**采用已发表搜索的穷尽性结论**，目标q必须>B。本轮没有重新运行该大搜索，也不宣称已审计其软件、所有原始输出或当前全球最高cutoff。

对n=r₁，结合源中已有q=1+2kn、k odd、q≡11/19 mod20，得到

    k≥552115199.

对应边界候选1+2kr₁=970453989512699仅是首个通过这些同余的整数；不宣称它是素数、Φ的因子或square hit。此式不是继续扫描的授权。

这是 BOUNDED EVIDENCE / INHERITED COMPUTATIONAL GATE ONLY。它不证明任一目标Φ无平方因子。对第二个relay，q>2r₂已超过B，故该历史bound不再带来额外截断价值。

## G6. 最终逻辑审计

G1是无界的条件依赖定理，G2是无界的特定参数化不可约定理；二者关闭的是明确方法，不是整数平方因子问题。G3中部分符号结构是源定理特化，部分是坐标/群结构分析；均未产生更严格terminal q类。G4是Phase E机制的任务特化反例；G5是文献有界证据。

没有新排除任何一个八指标。没有得到actual base5 member。没有证明三顶点空、一般B31^odd空、exactly-seven不可能、N≥8或A303656解决。两项任务的结果等级均为严格限定的D，不是A/B/C；不是声称所有固定阶数论路线失败。
