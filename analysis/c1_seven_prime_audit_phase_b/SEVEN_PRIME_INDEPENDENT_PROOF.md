# 七个 nonregular primes 必要界：不依赖一般 critical-core 提取的重证

## 0. 命题及审阅范围

在 `Samsen879/a303656` 的 fixed-SHA admitted original-row formal class 中，任何 complete simultaneous C=1 finite certificate 至少含七个不同的 original primes q，满足

    q = 3 (mod 4),  s_q = v_q(5^ord_q(5)-1) >= 2.

不限 q 的大小、K_q、非空 accepted odd valuation sets、shared residues 或 regular helper/support rows 的数量。本证明不声称七个资源足够，不给出完整证书，更不证明 A303656 的普遍可表示性。

这是对源包 `MASTER_THEOREM.md` §1–8 的重新推导。与原文不同，以下在 N<=6 的反证假设下直接精确消去所有 p>=7，因此无需依赖一般 exceptional-core 提取、canonical pruning、free-blocker matching、pooled synchronization 或 resultant 定理。

## 1. 原始事件的形式与 reverse CRT

原始 row q 有 K_q>=2、共享 r_q 和 E_q⊂{1,3,...}∩[1,K_q-1]。在 anchor c 上考察

    V_(q,c)(d)=r_q-3^c-5^d.

模 q^K 的零不接受。令 w_q=ord_q(5)、s_q=v_q(5^w_q-1)、a_q=max(0,K_q-s_q)，并冻结最终 ambient U 和全周期 L。所有 w_q|q-1，因此 v_2(w_q)<=1，odd-row 全周期 w_q q^a_q 的 2-adic 部分也至多为 2。

固定 anchor，原始 coarse event 是以下之一：空集；一个 rigid logarithm class modulo w_q；或一个 dynamic row q，等于固定 lower logarithm guard H_q 乘以 q-coordinate 上的 shell union D_q。后一情形 accepted shells 的 indices 全有相同 parity，中心柱永不 fatal。一种正的 rigid event 必须有 accepted valuation h<s_q，故 s_q>=2。

该分类可直接从唯一的 logarithm modulo w_q 和 LTE 得出：若 t=r_q-3^c 的 mod-q 值不在 <5> 中则 inert；否则先固定唯一 logarithm a mod w_q。若 h=v_q(t-5^a)<min(s_q,K_q)，同一 w_q class 上的 valuation 恒为 h；否则在可提升的情形存在唯一 exponent center d_* modulo w_q q^a_q，非中心处 valuation 为 s_q+v_q(d-d_*)。局部零仍排除。

还需保留 coarse 的 forall-lifts 定义。若一个 coarse x 对每一 odd row 都不是 coarse fatal，则各 row 的一个 safe lift 可以同时选取：row q 的未固定自由度只在 q-coordinate 超过 v_q(U) 的 private digits 中；其他 rows 的 w-orders 对该坐标的依赖已包括在 U。将不同 q 的 private digits 用 CRT 合并，得到共同 full odd-safe lift。这里使用的是每个原始 prime 的独立 private digits，不是错误地把任意 union-of-rows 的 forall 与 exists 交换。

## 2. 固定一个 anchor，并关闭 dynamic 3

若无 two-adic row，取 c_*=0。若有 shared two-adic residue r_2，取

    c_*=1,  r_2≡0或1 (mod4);
    c_*=0,  r_2≡2或3 (mod4).

r_2 偶数时取目标 local values T=0,4；奇数时取 T=1,5。这些 T 均为两平方和；r_2-3^c_*-T 均≡1 (mod4)，且两个目标 unit 相差4。5生成 modulo2^K 的所有1 mod4 units，mod8 的1/5类别决定 exponent parity。因此同一个 c_* 在两种 exponent parities 上分别都有 two-adically safe exponent。K=2 时直接按 modulo4处理，两种实际 parity 均可选。

因为 odd-row predicates 只依赖 exponent 的 parity 而不依赖更高的2-bits，若 fixed c_* 的 odd subsystem 在任一 parity 上存在 safe exponent，则可在保留该 parity 的同时，经 CRT 换成 two-adically safe 的高位，构成全证书的 escape。

所以 hypothetical simultaneous completeness 强迫 fixed c_* 的 odd subsystem 在两种 parity 上分别完整。

w_3=2，且 s_3=1；在 fixed c_* 上，row3 的 mod3 divisibility 最多在一种 parity 活跃。取另一种 parity b。若 row3 不存在或 inert，任选其 inactive parity。于是我们得到一个仍然完整的 fixed-anchor, fixed-parity odd system，但 dynamic3 已 inactive。

此步不要求两个 anchors 同时 two-adically safe，也没有把 pooled lower cover 当成某个 anchor 的 full cover。U 为奇数时，parity 可作为不改变 odd-row masks 的辅助标签；并不生成虚构的 two-adic hazard。

## 3. 少于 p 个 proper cylinders 的局部覆盖

令 X=Z/p^β，β>=1，D 为一个 admitted parity-shell bundle（允许为空），C_i 为 r<p 个 proper p-cylinders。

断言：D∪⋃C_i=X 当且仅当 D 接受 shell0，且某个 C_i 恰为 centered first-level cylinder C_1(ζ)。

证明：D不接受shell0时，p-1个非中心first branches都需要rigid cylinder；中心点也需要另一支，故至少p个。D接受shell0时，shell1必不接受。没有 C_1(ζ)，则其p个second-level branches分别需要rigid cylinder，其中中心branch至少要覆盖中心点，仍需p个。β=1直接成立。反向显然。

这里 parity、properness、local-zero exclusion 都不可删除。例如 p=3,β=2,J={0,1} 与一个深度2中心 singleton 可以覆盖全域，但这个 J 不满足 admitted parity 条件。

## 4. N<=6 时，所有 p>=7 的收缩都精确且不增殖

反设原始 nonregular prime 总数<=6。固定(c_*,b)后，每个非空 original rigid event设为一个seed，保留原始来源；其数量 N<=6。原始 dynamic events另存。所有ambient坐标及深度始终保持，不因删除事件重算U。

在最大剩余 odd coordinate p>=7，top rigid seeds的数量≤6<p。由§3，对每一个 lower point y，top fiber full 当且仅当一个simple pair活跃，即 actual dynamic p-row 与一个 centered depth-one seed 同时活跃。

因此 full exact saturation residual 正好是这些 simple pairs 的 lower guard intersections 之并。每个seed最多产生一个child：其top cylinder的位置已固定，dynamic p-row的guard和center也唯一且已冻结。没有第二个child可任意重选。lower seeds保留，所以总seed数不增加，每个原始来源仍至多出现一次。

依次精确消去全部p>=7，若原系统完整，剩余系统也完整。所有生成seed仍是具有唯一原始rigid来源的CRT cylinder，并有一条实际dynamic helper lineage。剩余odd坐标最多为3、5；没有active dynamic3，也没有admitted dynamic5。

这一步是本重证的核心简化：在N<=6的反证域内，linear residual不只是subset，而是每个p>=7处的完整exact residual。

## 5. Least-helper invariant：不能抹去尚未消去的 order factor

seed最初是一个coset modulo原始w_q。simple-pair收缩在p处先删除恰好深度1的p因子，再与helper的logarithm guard modulo w_p相交。兼容非空CRT交的modulus是LCM。因此，对任何尚未消去的odd prime ℓ，来源order或某个已使用helper order中的ℓ-power都必须保留在当前guard中；交集只能增加精度或变空，不能抹掉该因子。

可写为：若h已在线age中且ℓ未消去，则

    v_ℓ(M_current) >= v_ℓ(w_h).

取最小helper h。w_h 的odd factors都<h；若某个这种因子大于当前rank，它只能由lineage内更小的helper消去，矛盾。所以这些order factors都必须仍出现在当前guard中。

特别地，seed不能变成非空constant。无helper时，constant意味着原始w_q无odd factor，故w_q=1或2；order1不提供admitted odd prime，order2只有q=3且regular。存在helper时，constant迫使最小helper的w_h=1或2，故h=3；但我们的helper收缩只在p>=7进行，且dynamic3已关闭。矛盾。

这是actual order provenance约束，不能由仅有triangular几何的模型替代。

## 6. 坐标3：浅层helper最多覆盖8/9

若一个linearly descended rank3 seed的深度≤2，无helper时它需要一个original rank3 rigid resource，其order为3、6、9或18之一。以下完整因式分解全部squarefree：

    Φ3(5)=31,       Φ6(5)=3·7,
    Φ9(5)=19·829,   Φ18(5)=3·5167.

所以没有这种original nonregular resource。

有helper时，取最小h。§5迫使w_h=3^e或2·3^e，1≤e≤2。完整order检查与admitted congruence过滤后只有

    depth1: h=7,31;
    depth2: h=19,5167.

每个helper在fixed anchor上仅有一个已经冻结的logarithm guard；同一个helper被多个seed引用不产生多个自由位置。所有浅层seed的union因此包含在两个depth1与两个depth2 fixed cylinders的union中，总measure≤2/3+2/9=8/9。

任何rigid-only full rank3 cover，删去冗余后是complete ternary prefix frontier。浅层不够，必有一个深度D≥3的leaf。沿其路径每层另有p-1个非空兄弟子树，故leaf数≥1+(p-1)D；这里至少7。独立seed来源不重复，故≤6个linearly descended seeds不可能覆盖rank3。

注意：这是descended-helper的七来源界，不是把原始资源的81-row界套到macros。

## 7. 坐标5：精确处理全部 nonlinear alternatives

先证明一个位置约束。rank5、top depth1且3-free的linearly descended seed，无helper时需要original order5或10的nonregular prime，但

    Φ5(5)=11·71,  Φ10(5)=521;

11、71均regular，521≡1 mod4不admitted。有helper时取最小h；§5与3-free条件迫使w_h=5或10，故h只有11或71。每个helper仅有一个fixed mod5 logarithm。因此所有这种3-free seeds只能位于最多两个fixed first branches。

现在设剩余rank5 seeds有n个，lower rank3 seeds有k个，n+k≤6。

**n≤4。** 没有dynamic5，也没有五个first branches所需的rigid资源，故所有rank5 saturation为空。完整性将迫使其余k≤6个rank3 linearly descended seeds完整，违反§6。

**n=5或6。** 任一irredundant full5-frontier最多六叶，必恰为五个depth1 leaves：完整5-ary tree叶数≡1 mod4，而深度≥2会需要至少9叶。因此所有minimal slice-cover witnesses都从每个first branch选一个depth1 seed。五行至多一个witness；六行至多一个branch有两个选择，至多两个witness。形式上数量≤n-4。

进行完整exact contraction，而不是只保留某一个witness。所有cover macros加保留lower seeds的数量≤(n-4)+k≤2。

每个非空macro都必须带proper3-guard。若它是constant，则五个构成seed的lower guards都必须3-free；但上述位置约束只允许至多两个first5 branches，不可能构成五分支覆盖。CRT非空交不能将某个proper3-guard变成whole domain。保留lower seeds也不能是constant，见§5。

因此full exact residual只含至多两个proper3-cylinders，且无dynamic3，不能完整。若ambient根本没有3-coordinate，所谓proper3-guard不能存在；这些macros必须为空，结论相同。

## 8. 结论

全部情形矛盾。故complete simultaneous finite admitted certificate要求N≥7，从而原始nonregular primes总数至少七。

来源数只在线性阶段保持单射；§7的非线性macros明确按全部geometric clauses计数，没有把它们当成新prime。该证明不假设一般非线性阶段的source计数守恒。

## 9. 本轮检验与边界

独立代码 `tools/audit_independent.py` 不导入源包或repository reference。它复核row normal forms、coarse forall projection、two-adic boundary、稀疏局部覆盖、helper inventory、8/9位置界、全部五/六行depth≤2五进柱多重集、guard intersections与稀疏精确收缩。具体有限域及计数见 `results/audit_*.json`。

无限prime范围及任意precision的结论依赖上述解析证明，不依赖这些有限枚举。重证与程序由同一会话完成，不等于另一位作者/另一模型的独立审稿，也未进行proof-assistant形式化。
