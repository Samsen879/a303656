# A303656 — B31^odd / n=878851，Targeted Phase G

## 0. 结论

**n=878851 未关闭，最小状态未关闭，没有发现 actual base-5 B31^odd member。**

本轮可提交的是 **LEVEL D：严格限定的无界路线排除**，附文献有界gate。不是LEVEL A/B/C；没有获得一个比“指定exact order + base5 Wieferich”明显更小的新terminal-prime类。

主要结果：对n=878851证明Φ_n(5T²)在Q[T]不可约；证明power-base/composition产生的二阶条件不独立；给出保留下层actual regular state的exact-target换底数反例。不可约定理是本轮证明与应用，不主张文献优先权。CRT反例机制继承Phase E，实例化不是base5成员。

推荐执行环境：网页端研究与标准库reference laboratory。本轮未交给Codex，没有扩大q或k扫描。

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
main SHA: c6ca0dc061783ab993be6fa077c8f66cd730e28c
tree: 57ecf1ce3dc7760c6622bb79aca60d1bf2ba0b06
PR #30–#37: closed, merged=true
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

通过live GitHub connector读取，而非相信题面SHA。`AUTHORITY.json`记录merge times；`SOURCE_BINDING.json`记录逐个核心source路径及读取边界。

**来源完整性边界：** 已读取四个相关包的核心REPORT及INTEGRATION范围说明，核对F3、F4、primitive valuation和O31；未逐文件阅读每个目录全部辅助代码、生成数据、manifest和日志，因此“所有必读目录逐文件完整阅读”要求未全部完成。未取得原始字节checkout，未独立重放源hash、源runner或repository tests。数学结果另给完整证明，不把这些未执行事项记为PASS。

Phase F producer REPORT里的“当时缺失Phase E”是历史记录；当前merged INTEGRATION已明确对齐O31并绑定merged依赖。不能把历史缺口当成当前不存在Phase E。

## 2. SOURCE THEOREM RECONSTRUCTION

沿用merged定义：admitted x>3、x≡3 mod4；w_x=ord_x(5)，s_x=v_x(5^w_x−1)。D(q)含root与全部admitted descendants>3，**不含停止展开的terminal3**。B31^odd要求root nonregular，所有proper descendants regular，纯terminal3，basal gateway={31}，所有w_x odd squarefree。

F1已完整认证两个first relays：878851（order93）和625552508473588471（order31）；两者regular。因此two-vertex class已由源排除。

F3给出exact三顶点条件：q∈B31^odd且proper closure={31,r} iff root exact order属于{r,3r,31r,93r}且admitted primitive square hit。反向由imprimitive valuation-one保证。

F4对good regular closed R定义maximal-generator antichain A(R)与J31(R)，然后用归一化critical integer Z31(R)给exact-state iff。不是“proper closure包含于R”的弱条件。

O31是全31-basin（不含terminal3）的odd-order条件。Seven-Basin iff只适用于给定actual exactly-seven arithmetic normal form，允许选择合法K/E；没有提供七个actual nonregular roots，也不适用于任意冻结state。

## 3. EXACT TARGET

```text
R={31,878851}
J31(R)={878851,2636553,27244381,81733143}
本任务第一目标 n=878851（prime）。
```

要求排除或认证

    q prime, q≡3 mod4, ord_q(5)=878851,
    q² | Φ_878851(5).

已知同余为q=1+2kn、k odd、q≡11或19 mod20。这些来自源，不算新结果。n为prime时，q∤n；且q不能整除5−1，因此q²|Φ_n(5)与5^n=1 modq²等价。

即使这个n被关闭，R仍有三个terminal indices；本轮没有混淆单指标与状态关闭。

## 4. NEW LEMMAS

完整文字证明在`PROOFS.md`。

**G2（不可约路线排除）**：若ℓ∤n、c∈Q×、gcd(v_ℓ(c),d)=1，则Φ_n(cT^d)不可约。取ℓ=5,c=5,d=2，即Φ_878851(5T²)不可约。它排除该自然Aurifeuillean平方代换下的Q[T]分裂，不排除数值平方因子。

**G1（幂倍乘条件依赖）**：对ord_q(a)=mr，d|93，v_qΦ_r(a^d)仅为原valuation s（m|d）或0；活跃的多个二阶条件是同一个条件。Q_q(a^d)=dQ_q(a)也不能产生独立double-Wieferich。

**G3（符号/trace审计）**：q3 mod4时二次、四次、八次等普通幂剩余像相同；edge符号与Gauss二次子域split符号相容。降至real trace多项式的变量变化在目标q处étale，减少次数却不增加独立消失条件。

G3的部分基础结构、primitive valuation及唯一prime-ideal解释已在Phase E/F；本轮只给精确特化，未重复计为新增排除。

## 5. PROOFS

G2的关键是分歧指数，而不是简单导数。令K=Q(ζ_n)。5∤n使K在5处unramified；对cα^d=ζ_n，延伸valuation给v(α)=−v₅(c)/d。既约分母d迫使[K(α):K]≥d，二项式又给≤d。因ζ_n=cα^d属于Q(α)，总次数为dφ(n)，等于Φ_n(cT^d)的次数，故不可约。

G1来自Φ_r(X^d)=∏_{e|d}Φ_(er)(X)；在固定exact-order-mr处只有e=m可能被q整除，其他因子是units。没有第二个独立square-hit条件。

其余证明与完整量词、例外、反例见`PROOFS.md` G0–G6。证明为本会话可审阅推导，未做独立作者审稿或形式化认证。

## 6. COUNTEREXAMPLE ATTACKS

最小可读边界例：Φ_3(30)=931=7²·19，ord_7(30)=3，Φ'_3(30)=61≠0 mod7；同时G2证明Φ_3(30T²)不可约。因此不可约、simple root、unramified不等于整数值squarefree。

更贴近本题的反例取源中actual regular q₀=490398859。CRT构造

    A=70602295045730533920731272137800405

满足A≡5 mod(4·3²·5²·31²·878851²)，并在q₀²处为5^93的Teichmüller lift。本轮认证

    ord_(q₀)(A)=878851,
    v_(q₀)(Φ_878851(A))=2,
    proper admitted closure={31,878851},
    下层两顶点仍regular、all-odd，v₅(A)=1。

这是**换底数A**的actual arithmetic countermodel，不是base5成员。它将Phase E E8在本任务的prime index上完整实例化；证明只依赖这些局部数据的base-uniform排除不成立，不排除真正利用整数5本身的定理。

已被Phase E否定的simple-root/derivative/resultant/Hensel快捷证明不继续作为新路线；本包只作回归边界。

## 7. COMPUTATION, IF ANY

`python3 reference.py --self-test --output fresh.json`仅用标准库，验证57个recursive full n−1 Lucas certificates、两项first-relay完整乘积、源regular rows、六个文献odd Wieferich解的exact orders与s=2、四个换底数反例及相关模q³身份、小多项式恒等式与归一化残数。证书构造脚本的SymPy只提议有限factorizations；最终验证不信任probable-prime判断。

未重跑k≤10^6；未扩大general q scan；未物化Φ_878851(5)或更大目标。最大aggregate-modulus只有394 bits。多项式回归最高次数558；不是构造目标次数多项式。

### 已发表搜索的准确范围

Dorais–Klyve 2011论文第7页§4.1明确覆盖base5到（含端点）

    B=970453984500000.

论文标题6.7×10^15不可移作base5范围。期刊记载2011-10-16发表。本轮逐个认证六个已知odd解的阶，均非八指标。采用该论文的搜索穷尽性，目标q>B；对n=878851结合旧同余给k≥552115199。

**BOUNDED EVIDENCE ONLY / NO CLOSURE。** 未重跑历史大搜索、未认证其原始全部日志、未声称这是当今全球最高搜索界。第二relay本身大于该界，所以此文献界主要作用在第一个relay family。

## 8. WHAT IS ACTUALLY CLOSED

关闭的是明确方法：Φ_n(5T²)的进一步有理多项式分裂；以及仅由5的幂倍乘/分圆商得到第二个独立lifting条件的论证。取得D级路线结果，不是无界terminal exclusion。

新增关闭的目标indices：**0**。

## 9. WHAT REMAINS OPEN

n=878851是否存在admitted square hit仍未判定。最小R的四指标全部保留。另一个relay、larger closed states、B31^odd空性、exactly-seven以及A303656均未解决。

没有获得一个新且明显更稀疏的terminal-prime类。Stickelberger/Jacobi-sum/cyclotomic-unit方向未得到适用的新排除定理；这不是宣布这些方向原则上不可能。

## 10. NEXT SINGLE TARGET

**为Φ_878851(5)的admitted square part设计可独立重放的证书接口**：冻结“证明不存在q≡3 mod4且q²整除该整数”所需的充分条件，先在小指数上证明soundness并验证正负对照。只有产生这种证书的明确数学机制及资源benchmark后，才考虑任何大计算。不是继续k扫描，也不预设必须完整分解。

```text
n=878851 CLOSED: NO
MINIMAL STATE R={31,878851} CLOSED: NO
ACTUAL B31^odd MEMBER: NO
B31^odd EMPTY: NO — not proved, not a nonemptiness assertion
EXACTLY-SEVEN KILLED: NO
N>=8: NO
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

来源与文献URL、读取边界见`SOURCE_BINDING.json`；完整证明见`PROOFS.md`；有限证据见`evidence.json`与`certificates.json`。
