# A303656 C=1 TWO-NONREGULAR GLOBAL SHARED-STATE POOLED REALIZABILITY
## TARGETED PHASE D — 研究报告

## 本轮结论

本轮得到：一个消去较大 root residue 搜索的 **exact terminal-trace iff**；一个 **serial-root iff**；严格坐标分离时的 **C9 OR iff**；保留 shared states 的 separator-profile iff；共享 regular relay 的精确同余碰撞条件；以及一个真正算出大整数 gcd 的 original multi-use resultant 排除。

同时发现，任务中“两个 roots 分别通过 C9 仍不保证 pooled union”的前提，需要在本轮优先采用的量词下修正。**固定 K/E、允许完整 residue rings、目标仅为 whole odd EITHER 时，一个 root 通过 C9 就已经充分。** 两个 C9 构造的共享 regular rows 都取 r_p=2，不会发生该类冲突。真正剩下的是两个 C9 都失败后的 cooperation，或者额外指定了 mandatory roles / restricted states 的问题。

未得到消去全部 lower-state 量词的任意重叠 two-q order-signature 分类；未构造 actual whole odd pooled cover；未提高 seven-root 下界。以下定理是本轮给出证明的研究推导，未获独立作者审阅或 proof-assistant formalization。完整证明见 `THEOREMS.md`。

---

## 1. LIVE AUTHORITY

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Bound main SHA: 3fb4b4b4f71018017c7ea014ae7a1380f27b6b94
Bound main tree: 5ee6ab9e51f3e6d471991b7407de193d12777882
End-of-research live main recheck: unchanged
Global shared-state Phase C: PR #22, merged
Order-DAG Phase C: PR #24, merged
Hybrid scope repair: PR #25, merged
PRECONDITION: PASS
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

PR #22 的 merged time 为 2026-09-07 09:49:22 UTC；#25 为 2026-09-07 12:39:49 UTC。#25 修改的是 cumulative-main scope test，不是数学 source payload。

源依据包括五个指定目录的数学报告及 Global 的 PROOF_DETAILS/PROOF_AUDIT、Pooled 的 DEFINITIONS、Order-DAG 的 THEOREMS，并补读 Hybrid 主定理。精确读取范围和 recheck 见 `SOURCE_BINDING.json`。未把目录存在说成全部生成数据、历史实现均已逐文件审计；未取得完整本地 checkout，未执行 repository-native replay。新计算均为本地 standalone reference，未 import 仓库实现。

---

## 2. C9 SINGLE-NONREGULAR RECONSTRUCTION

记 C9_R(q) 为源 C9 的三个条件：

1. q 的 hereditary regular order closure 全部属于实际 regular support R，且 q 和该 closure 内所有 orders 的 odd parts 均 squarefree；
2. 每个所需 regular p 都接受 valuation 1；
3. q 接受某个 odd h，0<h<s_q。

这里 closure 不是 Order-DAG 的 absolute terminal set。后文用 C_i 表示 support/dependency closure，用 Term(q) 表示 terminal set，避免两种 T(q) 混用。

C9 的量词为：固定 P、全部 K、全部 E，只在完整 residue rings 中选一个 global shared-residue vector。其充分性直接取

    r_p=2 mod p^K_p，所有必需 regular support；
    r_q=q^h+2 mod q^K_q。

正因为如此，本轮有立即成立的推论：

    C9_R(q1) OR C9_R(q2)  ==>  two-root whole odd pooled cover exists.  (D0)

一个 root 已经覆盖整个 domain 后，新增行只能增加覆盖。两个构造若都适用，共享 regular rows 的 prescribed residues 也完全一致。因此“两个 rowwise C9 都成功却因共享 support 失败”不是这一 free-state EITHER 类中的反例方向。

源 C9 的必要性仍来自 C6 safe-prefix extension、C7 two-point projection rigidity、C8 frozen terminal trace，而不是分数 Hall 容量。

---

## 3. TWO-ROOT FORMAL CLASS

固定

    P=R union {q1,q2}, q1<q2,
    s_p=1 for p in R, s_q1,s_q2>=2,
    K_p>=2,
    empty != E_p subset {positive odd h<K_p}.

每行只有一个 shared r_p mod p^K_p，两个 anchors 均使用它。

    V_(p,c)(d)=r_p-3^c-5^d,
    w_p=ord_p(5), a_p=max(0,K_p-s_p),
    U=lcm(t2,{w_p}),
    L=lcm(t2,{w_p p^a_p}).

Local zero 不 accepted。本轮 odd pooled 目标不借用 two-adic row 的 favorable coverage。若把 odd r2 的恒定 fatal anchor 加进 pooled union，问题可能平凡化，不能冒充本轮结论。分析时可用支持 full periods 的 CRT refinement，但不把它重命名成 original U。

同一行可一边 dynamic、一边 rigid；same lower prefix 上至多一个 anchor 正整除。不同 primes 的 residues 可用 CRT 合成一个全局整数，真正的冲突在于同一 original row 被要求承担不相容的状态。

---

## 4. TWO-NONREGULAR NECESSARY/SUFFICIENT CRITERION：精确 last-root 消元

令

    A={q1} union {p in R:p<q2},
    N=lcm(w_q2,{ell_p:p in A}), ell_p=w_p p^max(0,K_p-s_p).

冻结 A 的 ONE state vector tau。定义 D2(tau) 为 A 的 full common escapes 在 w_q2 上的投影。N 的全部 prime factors 都小于 q2。

若 q2 的 actual rigid fatal logs 为 B2，则

    whole odd pooled cover  iff  D2(tau) subset B2.                 (4.1)

这里必须是 rigid FATAL logs，不能把 dynamic guard 填进去。若有 log 未被 B2 覆盖，就在 q2-coordinate 选 safe center，再穿过所有更大 regular rows，得到 full escape。

现在可以完整消去 r_q2。令

    H2=E_q2 intersect {h:0<h<s_q2},
    h2=min H2（仅在 H2 非空时定义）。

定义 J2(D)：

| D | 存在一个 q2 shared state，rigid-cover D 的条件 |
|---|---|
| empty | 总是可以，q2 无须承担义务 |
| {a} | H2 非空 |
| {a,b}, a!=b | H2 非空，且 5^a-5^b ≡ 2 或 -2 mod q2^h2 |
| 至少三个 logs | 不可能 |

因此得到

    two-root realizability  iff  exists ONE tau: J2(D2(tau)).       (D1)

两点条件的充分性不是独立选两个 anchors：把两 centers 对齐 modulo q2^h2 后，选择 r 的下一位避开至多两个 forbidden digits，保证两 valuation 均恰为 h2。

这是一个明确算术化的 terminal-trace iff，去掉了整个 q2^K 的 residue 搜索；**它仍保留 lower vector tau 的存在量词，因此不等于任意 overlap 的 order-only C9。**

---

## 5. CLOSURE GRAPH TYPES

从每个 w_qi 的 odd coordinates 出发，递归展开实际 regular support 的 odd order factors。Missing/nonadmitted coordinates 作为 free coordinate 保留，不能只记录 row labels 而忘掉共享自由坐标。

| 结构 | 本轮正确处理 |
|---|---|
| odd coordinate closures disjoint | §6 的 OR iff |
| regular closure contained / same support | §7 separator profiles；不是自动冲突 |
| partially overlapping | 对所有 shared states 只选一次，再做 exact profile join |
| 首个 shared relay p | p 的 lower closure 一并进入 separator；§8 检查状态角色 |
| 一个 root 在另一 root 的 order closure 中 | 属于 serial interaction，不满足独立 separator 假设；用 D1/D2 |

如果两个完整 hereditary REGULAR closures 的交恰好只有一个 prime p，且没有其他共享自由坐标，则 p 只能是 3。因为 w_p 的每个 odd factor 也必须出现在交集中，而这些因子严格小于 p；于是 w_p 无 odd factors，admitted 候选只剩 order2 的 p=3。所谓“共享一个 p>3 relay”通常是 first-merge 描述，不是完整 hereditary intersection 真的只有它。

---

## 6. DISJOINT-CLOSURE THEOREM

假设两个 roots 互不出现在对方的 dependency closure 中，且完整 odd coordinate closures（包括 free coordinates）不交。那么

    two-root whole odd pooled cover exists
      iff C9_R(q1) OR C9_R(q2).                                   (D4)

**证明要点。** C7–C9 的必要性在固定 parity 上仍成立。因此，一个 root 若不满足 C9，则任意 frozen states 在每个 parity 都留下 escape。两个 roots 都失败时，选同一 parity，各自取一个 private escape，由 CRT 合并，再选择 root safe centers 并延伸过外部 regular rows。

对应的 tensor 逻辑是

    forall(x1,x2) [C1(x1) OR C2(x2)]
      iff [forall x1 C1(x1)] OR [forall x2 C2(x2)]。

不是 AND。一个子系统单独全域覆盖已经足够；没有要求两边分别覆盖。

注意：Order-DAG 七个 basins “在 3 以上不交”，仍共享 3-adic coordinate，不能直接套这个严格 disjoint theorem。

---

## 7. ONE-SHARED-SUPPORT EXACT PROFILE CLASSIFICATION

以下要求 roots incomparable。令 R_i 为 root i 的实际 regular dependency rows，

    N_i=lcm(w_qi,{ell_p:p in R_i}), g=gcd(N1,N2)。

可在分析域中显式补 parity。固定 ONE compatible regular vector sigma，S_i 是相应 regular escape set。冻结 roots 时取它们的 FULL ACTUAL rigid log sets B_i，定义

    E_i=pi_g {d in S_i: d mod w_qi not in B_i}。

则

    whole odd pooled complete  iff  E1 intersect E2 = empty。       (D3)

交非空时，两个 escaping private exponents 在 mod g 上相同，非互素 CRT 将其拼起来；交空时不存在 joint escape。

对 free-state 存在性，可枚举各侧整个 private state vector 和由 §4 的算术条件允许的 root supply sets。每个 shared p 的 r_p 在两侧共用，只选一次。允许 supply set 忽略一个 state 的额外 fatal event，但不能宣称该事件被 suppression；necessity 使用 actual full B，sufficiency 利用额外覆盖无害。

对于 one-shared-support，这给出的 exact condition 是：**某个合法 shared r_p，使两侧各自的一份全局 private-state profile 不交。** 两份 private vectors 必须在所有 separator cells 上同时有效，不能逐 z 重新选。

这完成了精确 separator/integer 层的 iff；并未把 arbitrary private profiles 压成仅看 w_q1,w_q2 的简单数值条件。Mandatory simple-pair roles 则有下一节的封闭同余判据。

另有一个结构必要条件：在 incomparable 类中，若 W=gcd(w_q1,w_q2)，regular escape 的 W-projection 至多四点。于是任意 p>=5、p|W 都必须是 actual regular row、接受1、v_p(W)=1，且其整个 hereditary regular closure 通过 C9 support gate。证明先用“五个 digits 超过四点”，再对被迫 active 的 p 使用 C7 的 two-point recursion。共同 defect 5、11、19、67 因而不能由两根共同修复；共同 factor31 不被此条排除。这些示例也可由既有 Hybrid 机制解释，不冒称严格超越所有旧策略。

---

## 8. SHARED-SUPPORT COLLISION

设 regular p 必须承担某个角色：anchor c、lower log b mod w_p、center prefix z mod p^m。令

    t ≡ b mod w_p,
    t ≡ z mod p^m。

其 exact arithmetic condition 为

    r_p ≡ 3^c+5^t mod p^(m+1)。                                  (D6)

两个角色 alpha,beta 兼容，当且仅当对应 centers 在
p^(min(m_alpha,m_beta)+1) 下相同。多个此类角色满足全部这些 nested congruence compatibility 当且仅当有 shared r_p。这里是 center-prefix 等式；任意 exact valuation demands 仍需源 C3 的 forbidden-next-digit 检验。

在 K=2,E={1}，某个 mandatory fiber 的其他 rows 仅覆盖 digit z，而 p-row 必须覆盖剩下 p-1 个 digits 时，允许的 shared states 恰为

    {1+5^t, 3+5^t} mod p^2。

因此 three cases 的精确分类是：同一 induced state——相同 congruence；distinct compatible roles——congruences 一致但 role labels 不同；incompatible roles——这些 sets 的交为空。

### Actual two-root / shared-31 witness

全部 K=2,E={1}，取

    P={3,31,20771,40487},
    r3=2, r20771=20773, r40487=40493,
    U=L=40688430, M=U/31=1312530。

| 31-fiber | 三个 frozen rows 的覆盖 | 31-row 的全部可行 r mod961 |
|---|---|---|
| d=0 mod M | 仅 x=d mod31=0，来自 q20771 | {2,4} |
| d=437511 mod M | 仅 x=1，来自 q40487 | {684,686} |

两 fibers 的 31 lower log 都是 d=0 mod3。第二行中心指数为 t=63 mod93，且 5^63=683 mod961，所以得到后一对 residues。

枚举全部961个 r31，在这62个 actual cells 上：899 states 覆盖2格，58 states 覆盖60格，4 states 覆盖61格，无一覆盖62格。两 fiber 各自可实现，却不能共享一行状态。

这是真实 arithmetic collision，不是两个随意 Boolean masks。但是这两个 root values 的 unrestricted whole-cover no-go 已有 P4；本轮新增的是具体 global-state failure mechanism，不把它重命名为新 prime-class exclusion。

不同 anchor roles 也可相容：p7,r7=2 在 anchor0 的 center d=0 与 anchor1 的 center d=21 均投影到 z=0，因 1+5^0=3+5^21=2 mod49。

---

## 9. MULTI-USE RESULTANT

必须保留 original h 和 ordinary Y：

    R_h(Y)=Res_T(T^h-5^(Yh),(T-2)^h-5^(Yh))。

若同一个 original q，w_q=u h，被同时强制在全部 Y_j 上供应 paired rigid events，则

    u | gcd(Y_j-Y_1),
    q | gcd(R_h(Y_1),...,R_h(Y_m))。

先检查第一个条件。它通过后，这些 polynomial pairs modulo q 相同，所以多个 resultant divisibility 不能被当成新的独立概率惩罚。它未通过时，即使整数 gcd 含 q，仍不存在 global state。

### 本轮实际计算的大整数 gcd

取 source 已有 actual paired classes Y=7,8，original h=67。两个完整 resultants 的绝对值分别为72347、82614 bits。直接计算与半阶恒等式计算完全一致。

其正 gcd 的完整分解是

    2^67 ·269^15 ·1609^3 ·1877^4 ·3083 ·4289 ·4691
         ·5897 ·7639 ·20771 ·27337。

每个因子用 trial division 认证；乘积与两个完整整数的 Euclidean gcd 一致。完整 signed integers 以 `.hex` 文本保存。

q20771 的确在 gcd 中，也确有以下各自合法的 states：

| Y | b0 | b1 | r mod q² |
|---|---:|---:|---:|
| 7 | 2177 | 9772 | 16 |
| 8 | 1558 | 10238 | 17555 |

但 u=155 不整除1，故不能合并。相反，Y=7 与162 的差为155，可继续合法复用原来的 r16。

更强的 finite-support 排除是：对于任意可能同时服务 Y7、Y8 的 admitted supplier，u|1 强迫 w_q=67。令 V=(5^67-1)/4，精确得到

    gcd(V,gcd(R67(7),R67(8)))=432821=269·1609。

两个因子均为1 mod4，故这组 mandatory original paired demands **不存在任何 admitted supplier**；甚至不必再要求 nonregularity。没有使用 prime-size cutoff，也不需要对 V 做完整分解。

若这些 Y 是 OR alternatives，而不是同一 selected conjunction 中的 mandatory uses，上述 gcd 不能一起施加。这一 forcing 条件没有被本轮证明为任意 whole cover 的必要条件。

---

## 10. INTEGER GLOBAL CONFIGURATION

对 finite legal states 使用 one-hot variables

    x_(q,s) in {0,1}, sum_s x_(q,s)=1。

对每个 EITHER residual cell 施加 actual pooled incidence 的 covering inequality；A_c 用指定 anchor incidence；BOTH 使用两条带 anchor 标签的不等式；TRUE 无约束，FALSE 不可行。Original state tokens 跨所有 cells 与 macro branches 保持一致。

D1 去掉最后一个 root 的 residue 搜索，D3 把独立 private blocks 投影为 profiles，D6/D7 提供 exact arithmetic cuts。这些都是全局整型配置的消元，不是逐 fiber 最大化后再拼接。

源 C1 的 fractional gap 被完整复算：5859个 global states，U1302，没有 integral cover，uniform fractional capacity 为830/651。并构造了 honest exactly-two extension：增加

    q20771: r=344840143 modq²,
    q40487: r=477301244 modq²。

这两行在 K2,E1 下 full fatal masks 均为空：anchor0 target 非 unit，anchor1 为 local-zero power class。新的 actual U=284819010，L=15958124311290；coarse incidence 仍由1302-period kernel 描述。因此 LP/integer gap 在 exactly-two original-nonregular 类中仍存在。

**边界：两新增 roots 是故意 inert 的。** 这不是 interacting two-root positive example，更不满足 success level D。其价值仅为保护“LP 可行不能替代 integer realization”的接口。

---

## 11. ACTUAL ARITHMETIC EXAMPLES 与计算范围

| 项目 | 精确范围 | 结果 |
|---|---|---|
| Named arithmetic | 3,7,11,19,31,67,20771,40487 | trial primality、exact order、lifting PASS |
| Shared-31 collision | 961 states ×62 actual cells | 两 fiber individually feasible，合取无解 |
| Regular center roles | p3,K3；p7,K3；p11,K2 | 830 roles，232579 pair checks，全部吻合同余判据 |
| Root paired-state compression | q20771、40487 全部 w-period | 分别5192、40485 oriented legal pairs，全部构造 shared lifts |
| Whole-domain two-root CSP | 两实际 roots，3×3指定状态 | 9个配置均与 terminal-trace 判据一致；无 complete cover |
| Phase-C fractional regression | 5859 vectors；1302 cells | histogram 与830/651复现；5859 full CRT escapes |
| Exactly-two inert extension | symbolic period lift +两 root 全 w-period | U/L 合法，gap 保留 |
| Large resultants | h67,Y7/8 | direct=half-degree；gcd/factors/support gcd PASS |

共七个 reference audit groups PASS。没有进行 blind prime scan，没有遍历40-million或更大 full period，也没有把两种同环境组织方式称为 independently developed software stacks。

---

## 12. SERIAL-ROOT NECESSARY/SUFFICIENT CRITERION

这是本轮除 terminal-trace 外另一个明确 whole-domain iff。

如果

    q1 | w_q2，且 s_q1 not in E_q1，

那么

    two-root whole odd pooled exists  iff C9_R(q1)。               (D2)

证明：若 lower one-root system 已经 complete，结论来自 C9。否则挑一个 lower escape。q1 的 inactive/nonfatal rigid branch 容许全部 first digits；dynamic branch 的所有非中心 first digits 具有不被接受的 valuation s_q1，中心也有 safe lift。因而至少 q1 个 first-digit choices 能通过后来所有 regular rows，得到超过两个 w_q2-logs；q2 的两个 rigid logs 不可能全盖住。

沿 actual regular intermediate rows 的 q2→...→q1 order path，同样可用 two-point width 向下传递。因此 **K2,E1 starting class 沿上述实际 regular-relay paths 的 comparable-root cooperation 被化约为较小 root 的 C9**，不能借上方第二根修补失败的单根系统。

此处不能删掉 s_q1 not in E_q1：若存在一个实际 squarefree order-closed support，其中 q1 为唯一 nonregular relay、s_q1 为奇数且被接受，较大 q2 又接受 rigid h，则取全部 support r=2、q2 residue=q2^h+2，可用 P5 的 least-nonzero-coordinate argument 构造 whole odd pooled cover。选择 E_q1={s_q1} 时两个 single-q C9 都会失败。这是严格条件构造；本轮未实例化所需实际 prime family。

---

## 13. OPPOSITE-ANCHOR OBLIGATIONS

保留六态 FALSE/A0/A1/EITHER/BOTH/TRUE，特别是

    R(EITHER)=C0 OR C1 OR Sat_OR,
    R(BOTH)=(C0 OR Sat0) AND (C1 OR Sat1)。

Actual SPLIT 只能使 EITHER 成 TRUE，不能消除 BOTH。

Global simultaneous completeness 仍要求

    forall y: (A0(y) OR S0(y)) AND (A1(y) OR S1(y))。

A0-only cell 留下 A1 obligation，A1-only cell 反之。一个 pooled supply set 不得被自动当成指定 anchor 的保障。§8 的未定 anchor 两选项在 typed role 下必须选对应的一个；因此 typed constraints 可以使原本 pooled-compatible 的角色变得冲突。

恰好两个 nonregular roots 不能完成 simultaneous BOTH certificate，已由 source 的 at-least-seven theorem 给出。本轮不把这条旧推论重报为新的 lower bound。

---

## 14. RELATION TO EXACTLY-SEVEN BASINS

Phase-C Order-DAG 已证明：exactly-seven 的 admitted basins 在终端3之外互不共享 regular relay，且各 root 是 order-reachability antichain；首个 ternary frontier 的 leaf depths 为1,1,2,2,3,3,3。浅 heads 是7、31、19、5167，更深三叶来自 source 列出的六个 actual heads。

因此有两个不能跨越的接口边界。

第一，不能再以“七个 basins 必须共享一个 p>3”为前提做碰撞，因为 survivor normal form 已经排除了这种 overlap。真正共同的 separator 是 3-adic coordinate 与 parity。

第二，七叶中的任意两个 basins 只需供应各自 assigned leaves，不需单独覆盖 whole domain。故“该二根子系统不能 whole-EITHER-complete”不等于“这两片叶不能同时存在”。将 D2/D4 的全域 no-go 直接套给七根中的任意一对，是错误的量词升级。

合法接口是：把七叶 normal form 给出的 mandatory typed center roles 转成 D6 congruences，或转成 D3 的受限 domain demand profiles，然后检验同一状态下的合取。现阶段未得到一对 mandatory basins 的新普遍矛盾。Source Theorem12.1 的条件性七链构造仍未被推翻；上游 nonregular chains 未被实例化。

---

## 15. DOES THIS ELIMINATE A NEW SURVIVOR CLASS?

**NO——以“已经通过既有 P4/Hybrid 等障碍、此前尚存的 unrestricted two-root whole odd pooled 算术族”为标准，本轮没有认证一个严格新增的全域排除族。**

**YES——对明确同时强制的 original-role / multi-use 子问题，本轮给出了可审计的排除。** 具体包括 actual shared31 两-fiber状态合取无解，以及 h67、Y7/Y8 的全 admitted-prime simultaneous paired-use 空性。它们只有在 demand forcing 合法时才能用于全域证书。

本轮完成了 disjoint iff、serial subclass iff、一般 exact terminal-trace reduction，以及 shared-support 的 exact profile/role 条件；未完成 arbitrary overlap 的 order-signature-only two-q C9，未找到 actual cooperative whole cover。故不声称完整达到 success level A，也不把有限 profile CSP 本身冒充全面 arithmetic classification。

---

## 16. NEXT SINGLE TARGET

**K2/E1、两个 C9 都失败、roots incomparable、只共享 3-adic boundary 与 parity 的 cooperative profile classification。**

固定上述域后，以实际 regular heads 7、31、19、5167 的完整 paired states 为起点，研究两侧 ONE-global-state escape profiles 是否可能不交，保留 opposite-anchor obligations。目标是证明 profile 永远相交，或构造包含真实 nonregular roots 的不相交实例；不能把 upper roots 用未实例化的 formal seeds 冒充。

这一目标避开了已由 canonical C9、strict disjoint theorem、serial theorem 解决的分支，并直接对接 seven-basin 的实际公共 boundary。没有启动新的 prime scan。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
