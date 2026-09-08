#!/usr/bin/env python3
from pathlib import Path
import json
R=Path(__file__).resolve().parent
D=json.loads((R/'evidence.json').read_text())
A=D['authority']
prs=[(21,'1f4928d6a26fe98d28d576c56cd0f1dfecb13459','2026-09-07T09:44:28Z'),(22,'509bd064f849ff465e40e9edd7205c89b45a08c7','2026-09-07T09:49:22Z'),(23,'57d19d4d67f18ad38566ac5dafd7c4bf62f8b23c','2026-09-07T09:53:38Z'),(24,'cc15e53761f0669aefe8d5421c190d0584ebef78','2026-09-07T09:57:50Z'),(25,A['main_sha'],'2026-09-07T12:39:49Z')]
(R/'AUTHORITY.json').write_text(json.dumps({**A,'read_method':'live GitHub GET tools; pinned file reads; PR merged/base/merge metadata','live_main_rechecked_at_end':True,'merged_prs':[{'number':n,'merged':True,'merge_sha':s,'merged_at':t} for n,s,t in prs], 'repository_native_replay_performed':False,'local_research_only':True},indent=2)+'\n')
source='''# Sources and read scope

All source-derived statements are pinned to the main SHA in AUTHORITY.json.
These are read-only content/metadata observations, NOT a fresh repository-native
integration replay. A full local checkout/archive was not available; no claim
of fresh repository checksums, CI, or protected-file replay is made.

The task's four package directories were reviewed through their actual source
file contents in the complete PR file diffs (#20, #21, #22, #24), not merely their
PR bodies. The governing theorem, seven-prime report, shared-state proof excerpt,
and STATUS were fetched again by immutable current-main SHA. PR metadata was
separately refreshed to check the serialized merge chain #21--#25. #25 modifies
two Hybrid integration/test metadata files; it does not modify mathematical payload.

[S1] analysis/c1_order_dag_phase_c/THEOREMS.md, especially §§7,12,13.
Current Git blob: 0c86de426dc932a13a4d7cccb198e4ef3bd7c811.
[S2] analysis/c1_global_shared_state_phase_c/PROOF_DETAILS.md, especially C2/C3
(single shared state) and C9 (odd pooled scope, not simultaneous C=1).
Current Git blob: 5c6d4ebddcf7fb3ead3c21b130a2120ec7325211.
[S3] analysis/c1_hybrid_allocated_transitive_phase_c/; general tagged release
and coalescence in an escape policy do not override exactly-seven basin disjointness.
[S4] analysis/c1_seven_prime_audit_phase_b/REPORT.md and its actual arithmetic
certificates/proof/source files. Current REPORT blob:
50a9c03fed03a3471eab22b0527a8a789c19d2a7.
[S5] STATUS.md, current Git blob 2ba295c0ada0d19b4e7f7d7871312d0696a785d2.
[S6] Primary Cunningham Project table pmain126.txt, base 5 minus, exponent 191
and exponent 271 entries. Used as factor/cofactor hints only. Its P121/P171 labels
are not substituted for locally replayed primality certificates.

Pinned source locations:
```
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_order_dag_phase_c/THEOREMS.md
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_global_shared_state_phase_c/PROOF_DETAILS.md
https://github.com/Samsen879/a303656/tree/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_hybrid_allocated_transitive_phase_c
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/analysis/c1_seven_prime_audit_phase_b/REPORT.md
https://github.com/Samsen879/a303656/blob/3fb4b4b4f71018017c7ea014ae7a1380f27b6b94/STATUS.md
https://homes.cerias.purdue.edu/~ssw/cun/pmain126.txt
```

All Phase-D numerical assertions in REPORT.md are generated here and checked by
verify.py, except the exhaustive q<=2e9 inventory, whose exhaustiveness is imported
from [S4]. The four named inventory primes' primality/orders/valuations, including
the nonadmitted negative control, ARE independently recertified here.
No claim of literature novelty is made for newly explored factors.
'''
(R/'SOURCES.md').write_text(source)
headtable='| h | exact order | depth | lower log ell | CRT d_h | r_h mod h² |\n|---:|---:|---:|---:|---:|---:|\n'
for z in D['conditional_fixture']['rows']:
 depth=1 if z['h'] in [7,31] else 2 if z['h'] in [19,5167] else 3
 headtable+=f"| {z['h']} | {z['w']} | {depth} | {z['ell']} | {z['center_mod_wh']} | {z['r_mod_h2']} |\n"
roles={'literal_head':'literal head','alternative_depth3_head':'alternative depth-3 head','two_anchor_fixture_row3':'row 3','chain_factor':'admitted regular relay','nonadmitted_rejected_edge':'rejected nonadmitted edge','imported_inventory_independently_recertified':'inventory / control, not a chain node'}
nodetable='| q | exact ord_q(5) | s_q | admitted? | regular? | role |\n|---:|---:|---:|:---:|:---:|---|\n'
for q,z in D['nodes'].items():nodetable+=f"| {q} | {z['order']} | {z['s']} | {'YES' if z['admitted'] else 'NO'} | {'YES' if z['regular'] else 'NO'} | {roles[z['role']]} |\n"
facttable='| prime exponent p | proved prime factors of Phi_p(5), all multiplicity 1 | remaining cofactor | status |\n|---:|---|---|---|\n'
for z in D['families']:
 fs=' × '.join(z['proven_prime_factors']) or 'none extracted'
 rem=str(z['cofactor_digits'])+' decimal digits' if 'cofactor_digits' in z else z['cofactor_expression']
 if z['complete']:rem='1'
 status='COMPLETE' if z['complete'] else 'OPEN'
 facttable+=f"| {z['exponent']} | {fs} | {rem} | {status} |\n"
boundtable='| head h | every terminal q_h is strictly greater than | head-chain status |\n|---:|---:|:---:|\n'
for h in D['literal_head_order']:boundtable+=f"| {h} | {D['terminal_lower_bounds'][str(h)]['strictly_greater_than']} | OPEN |\n"
prtable='| PR | merged at (UTC) | merge SHA |\n|---:|---|---|\n'
for n,s,t in prs:prtable+=f'| #{n} | {t} | `{s}` |\n'
report=r'''# A303656 C=1 Seven-head conditional completion-chain realizability — Phase D

## 0. Verdict / 成果等级

**Level C，附 Level D 数据。没有实例化七个 nonregular terminals，没有排除 exactly-seven。**

本轮的严格成果是：三个 heads 的第一层 preimages 完整分类；13 个 admitted regular relay 节点的认证与实际部分链；七个 heads 的有限 terminal 排除下界；对 Theorem 12.1 的 shared-residue / ambient / parity 接口重建；以及一个明确标为条件性的 depth-3 head 替换推论。

必须区分：已证存在任意长 admitted prime-order chains；本轮实际找到的有限 prefixes；以及尚未证明存在的 nonregular terminal。前两者均不能替代第三者。

## 1. LIVE AUTHORITY

```text
REPOSITORY: Samsen879/a303656
REPOSITORY ID: 1333945235
MAIN SHA: MAIN_SHA_TOKEN
MAIN TREE: MAIN_TREE_TOKEN
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```

结束前重新 GET live main，SHA 仍相同。Phase C 与 #25 的 merge 状态逐项核对如下；这些是 live metadata，不是从旧报告抄录的 authority。[S5]

PR_TABLE_TOKEN

四个必读包的内容审阅范围、固定 blob 和 primary 外部资料见 SOURCES.md。本轮未执行 repository-native integration replay，也未将源 PR 的 PASS 收据称作本轮测试。新 reference laboratory 和 standalone arithmetic verifier 位于本包。

## 2. THEOREM 12.1 RECONSTRUCTION

对 literal H0 中每个 h，需要有限实际链

    h=p_0<p_1<...<p_k=q_h,  k>=1,
    ord_{p_i}(5)=p_{i-1}  (1<=i<=k),
    p_i ≡ 3 (mod 4), all p_i prime,
    s_{p_i}=1 for i<k, s_{q_h}>=2.

这里 s_p=v_p(5^{ord_p(5)}-1)。**原 Theorem 12.1 不允许把 exact order 擅自换成 2p 或一般 composite order。** 所有 statements about prime-order chains in this report have exactly this scope。[S1, §12]

### 2.1 Odd rows and telescoping cover

全体 odd rows 使用 K=2, E={1}，local zero modulo p² 不接受。
在 c=1 上，每个严格位于 head 之上的 regular relay p_i 设置 r=4；terminal q 设置 r=q+4 mod q²。

若 p regular、ord_p(5)=n，则 5^n=1+ap mod p²，其中 a!=0 mod p。对 n|d 写 d=nt，二项式展开给出

    1-5^d = -apt mod p².

因为 p 不整除 n，r=4 的 row 恰在 n|d 且 p∤d 时具有 valuation 1。若 q 是 terminal 且 s_q>=2，r=q+4 的 row 恰在 n|d 时具有 valuation 1。s_q>2 也完全允许；不需要强行 s=2。

沿链向下归纳，head 以上 rows 的 union **包含**整个 d=0 mod h 条件。注意是包含，不是宣称其全局 union 恰等于这一 guard；高层 rows 还可能覆盖其他 exponents。这个区别避免把 partial saturation 误当作新的 exact prime macro。

### 2.2 Exact heads, logarithms and residues

HEAD_TABLE_TOKEN

这七个 heads 全部是 admitted primes 且 s=1。本轮从 CRT 重新得到表中的 d_h 和 r_h，而不是把来源表格作为免检输入：

    d_h=ell mod w_h, d_h=0 mod h,
    r_h=3+5^{d_h} mod h².

head row 在 lower guard 内覆盖 h-coordinate 非零的部分；完整上游链补齐 h-coordinate 零点，因而覆盖整个 lower guard。所有这些 residues 对同一 row 的 c=0,1 固定，不按 fiber 或 anchor 重选。[S1, §12; S2, C2/C3]

### 2.3 Two parities and two anchors

even d 上的七个 guards 是完整三进 frontier：

    C1(0), C1(1), C2(2), C2(5), C3(8), C3(17), C3(26).

另加 row 3：K=2,E={1},r_3=2 mod 9。它在 c=1 恰覆盖 odd d 且 3∤d。剩余 odd d、3|d 由 head 31 及其链覆盖。

two-adic row 采用 K_2=2,r_2=1 mod4。c=0 时 local value=3 mod4，始终被 sums-of-two-squares obstruction 排除；c=1 时 local class=1 mod4，odd-row system 负责覆盖。因此不是把 odd pooled EITHER 误作 simultaneous C=1，而是逐 anchor 给出独立成立的 rejection。[S1, §12; S2]

### 2.4 One global CRT residue; conditional U and L

设 R 为完整构造中所有大于 3 的 regular row primes，包括 heads 与所有 regular relays。完整七链成立时，各 regular prime 都出现在其上一级 row 的 order 中，故

    U = L = 54 * product_{p in R} p.

每条 root row 的 induced period 为其前驱，因为 K=2<=s_q；每个 regular row 的 period 为 w_p*p。所有奇 row moduli 是相异 prime squares，另有 modulus 4，故可以同时解出一个全局 residue

    r mod M,  M=4 * product_{odd rows p} p².

**本轮的 prefixes 不具备这个完整构造。不能把 U=L 公式直接套到未终止 prefixes：最上端 regular relay 的 own coordinate 尚无更高实际 row 填充。** 本轮没有数值化最终 M,r,U,L，也没有把 hypothetical upstream seeds 作为实际 rows 输出。

## 3. EXACT SEVEN HEADS AND ALTERNATIVES

原 Theorem 12.1 固定

    H0={31,7,19,5167,271,4159,31051}.

其中 depth 1 是 31,7；depth 2 是 19,5167；depth 3 是 271,4159,31051。

但一般 exactly-seven 的 Theorem 7.1 必要形只固定前四个；depth-3 三个 heads 是

    G3={163,271,487,4159,31051,16018507}

中的任意三个不同成员。[S1, §7] 因此“4159 的这一种 chain 构造失败”不是“每个 exactly-seven 构造都失败”。

### 本轮新推论 D-ALT：20 种条件性 head-set 替换

保持 heads 31,7,19,5167 与前述 residues 规则。任取 G3 中三个不同 primes，分别分配给 a=8,17,26 mod27 的三个末层槽位。order=27 时取 ell=a；order=54 时取满足 ell=a mod27 的唯一 even lift（分别是 8,44,26）。再按同一 CRT 定义每个 head residue。

这些候选 heads 的 primality、exact order 和 s=1 已由本包认证。even d 上的 frontier 不变；odd d 仍由 row3 与 head31 覆盖。因此，只要相应七条 literal prime-order chains 存在，同一个完成证明成立。

共有 C(6,3)=20 个无序 head sets、120 个槽位分配；本轮另核验 120*54=6480 个 collapsed parity cases。这个结果是对源构造的条件性推论，**不证明各 head 的 chain-existence 互相等价，也不声称原文 Theorem 12.1 已把 H0 改写成任意集合。**

## 4. PREIMAGE DAG DEFINITIONS AND STOP-CONDITION AUDIT

对于每个已证明的 admitted prime p，定义

    Gamma(p)={q prime : q ≡3 mod4, ord_q(5)=p}.

因为 p 是奇素数，Phi_p(5)=(5^p-1)/4。其每个 prime factor q 都有 exact order p：order 只能是 1 或 p，而 q 若 order=1 则 q|4，不可能。p 自身也不整除 Phi_p(5)。所以本轮 prime-index preimage 枚举没有 order-loss exceptional factor。

必要候选形为 q=2pk+1；admitted 等价于 k odd。因为 exact order p 为 odd，5 在 q 下是 quadratic residue，故 q mod5 必为 1 或4。这是有证明的候选过滤，不是经验 sieve。

### 每个 admitted node 都有 admitted child

    Phi_p(5) = 1+5+...+5^{p-1} = p =3 mod4,
    Phi_p(5)=1 modp.

因此必有 q≡3 mod4 的 prime factor，且 exact order 为 p、q>p。这是源 §12 已有的存在引理，本轮重新检查其 stop-condition 含义。[S1]

所以 regular admitted node 的完整 first-preimage decomposition **不可能**全部 nonadmitted，也不可能真的没有 admitted child。有限搜索无命中只能是 OPEN。任意长 admitted chains 存在，并不迫使链遇到 q²|Phi_p(5)。

### 遇到中途 nonregular 时

在第一处 s>=2 截断，原 regular prefix 加上此节点立即成为该 head 的成功链。继续把此点当作 regular relay 不符合原假设，但没有理由丢弃已经成功的 prefix。未完成素性/分解的 cofactor 保持 OPEN；明确 nonadmitted factor 对该 edge 为 REJECTED，但不使其父节点或 head 整体死亡。

## 5. TARGETED FACTORIZATION AND COMPUTATIONAL GATE

仅处理源 theorem-linked prime indices。没有扩大一般 q<=B Wieferich inventory。

初始优先级：7 的强制首子节点；19 的小型分支；31 的强制首层分类；随后 271、4159、5167、31051。首次圆分数位数分别为 5、13、22、189、2907、3611、21704。

31 的强制 regular child P=625552508473588471，其 Phi_P(5) 约 4.3724e17 decimal digits，不予展开。改用固定指数的 q=2Pk+1 divisibility search。实际找到了

    Q=268987578643643042531=430P+1,
    ord_Q(5)=P, s_Q=1.

这说明“不能物化整个 Phi”不等于“不能寻找、验证它的 prime factors”。

### 两个独立算术核心

A：C++ uint64 progression + uint128 modular multiplication；枚举全部 k，并记录 nonadmitted factors。
B：C++/GMP arbitrary-precision progression + GMP modular powers；只枚举 odd k 的 admitted candidates。
14 个共同 domain 的 admitted hit streams 完全相同。各 domain 的 K、确切 factor hits 与执行收据保留在 search/、replay_search/ 和 evidence.json。

此外，巨大 31 分支的关键 K=1,000,000 域以及下一 relay 的必要 prefix，用 Python arbitrary-precision pow 重新遍历。它不是复用 GMP 的核心，也没有物化 5^P。

使用新写、只作 factor discovery 的 Montgomery/Suyama stage-1 ECM 进行小规模补充：Phi_5167 的 B1=2000、20 curves；Phi_4159 余因子的 B1=2000、12 curves；Phi_31051 的 B1=500、1 curve。未得到 factor。全部是 NO_FACTOR_FOUND_NOT_EXHAUSTIVE，不是 no-child 或 squarefree 证明。没有将它称作成熟 GMP-ECM 软件的完整 stage-2 run。

## 6. PER-HEAD CHAIN STATUS

以下 arrows 全部是 exact prime-order relation，不是只知道 predecessor divides q-1：

```text
31 -> 625552508473588471 -> 268987578643643042531 -> OPEN

7 -> 19531 -> 3326871479 -> 6653742959 -> OPEN
                         \-> 5109083184043259 -> OPEN

19 -> 191 -> 112691 -> OPEN
          \-> 60426671 -> OPEN
   -> 6271 -> OPEN
   -> 3981071 -> OPEN

271 -> 64993931 -> OPEN
    -> 12987902099 -> OPEN

4159  -> admitted first child OPEN
5167  -> admitted first child OPEN
31051 -> admitted first child OPEN
```

全部 displayed chain nodes 都是已证明的 admitted regular primes。没有实际 nonregular chain endpoint。4159 的已提取 factor 38678701 是 nonadmitted，不在上述链中。

## 7. FINITE PREIMAGE CLASSIFICATIONS AND EXACT COFACTORS

三个完整第一层分解为

    Phi_7(5)  =19531,
    Phi_19(5) =191*6271*3981071=4768371582031,
    Phi_31(5) =1861*625552508473588471=1164153218269348144531.

1861≡1 mod4，其 edge 排除；剩余 admitted factors 全部 regular。

完整的 19 个已展开 exponent families 如下。所有 listed factors 均有递归素性证明、exact-order certificate 和 s=1；没有把未分解 remainder 写成“无其他 factors”。

FACTOR_TABLE_TOKEN

Phi_191 的 121 位余因子与 Phi_271 的 171 位余因子，在 Cunningham primary table 中分别标为 P121、P171。[S6] 本轮有确切十进制值、精确整除关系，且它们通过 discovery-stage probable-prime screening；**本包没有这两个数的独立素性证书，因此没有将它们计入 certified prime DAG。**

所有 exponent<=40000 的剩余 cofactor 全值保存在 cofactors/Phi_<p>_remaining.txt。更大 exponent 的 cofactor 用不可歧义的精确整数表达式 (5^p-1)/(4*F) 保存；每个已除 prime 的 exact order 和 multiplicity 独立验证，因此整除性不是浮点推测。

## 8. PER-NODE PRIME / ORDER / s / REGULARITY / ADMISSIBILITY

下表包含全部 33 条 arithmetic records；其中 inventory/control 不属于这七条 chain 的新发现。原始 q² 与 q^(s+1) 模幂结果、order-factor exclusion residues、children 与展开状态均见 evidence.json。

NODE_TABLE_TOKEN

素性使用 recursive full-(N-1) Lucas certificates，66 个 proof DAG primes。对每个 N，完整分解 N-1，给出 witness a，验证 a^(N-1)=1 modN，且对每个 prime r|N-1 有 gcd(a^((N-1)/r)-1,N)=1。递归底为 2。最终 verifier 不调用 SymPy 或 probabilistic primality。

例如 Q=268987578643643042531 的 N-1=2*5*43*625552508473588471，Lucas witness a=2；它的前驱 P 使用 witness a=3。完整递归子证书随包给出，不依赖“看起来像素数”。

## 9. BOUNDED TERMINAL EXCLUSION THEOREM

**适用域仅为 Theorem 12.1 的 literal exact-prime-order chains；不是一般 B7 或所有 exactly-seven order basins 的 terminal 下界。**

对一个 head h 与上界 B，沿所有可能的 admitted children<=B 递归。若当前节点 regular，其 complete factorization 或有界 progression 枚举包含全部这些 children；将仍<=B 的实际 children 继续检查。若有限展开闭合且全是 regular，就证明该 head 的任意 terminal 必须>B。

这是对所有可能路径的有限排除，不只是验证一条选定链。它也不是 unbounded no-terminal theorem。exclusion 的 breadth-first independent verifier 逐个检查相应 k-domain 的覆盖以及所有分支。

BOUND_TABLE_TOKEN

### 31 分支的下界证明展开

Phi_31 的唯一 admitted child 是 P=625552508473588471，regular。令

    B=2*P*1,000,000+1=1251105016947176942000001.

在所有 admitted q<=B 中，ord_q(5)=P 的唯一解是 Q=430P+1，且 Q regular。GMP 与独立 Python 遍历一致。

若从 Q 向上一步仍不超过 B，则 q'=2Qk+1 必有 k<=2325。独立 Python 检查全部 odd k<=2325，连 composite divisor hit 都没有。其余 P-children 若存在都已超过 B，后续严格递增，不可能回到 B 以下。因此所有可能终止链的 terminal q_31>B。

不能把这里的“唯一解”外推为 Q 是 P 的全体 admitted preimages 中的唯一成员；唯一性仅在明确上界 B 内。

## 10. BASIN DISJOINTNESS AND GLOBAL STATE

literal prime-order chain 的 admitted predecessor 是唯一的：如果一个 prime x 被两条 chain 共享，则向下不断取 ord_x(5) 会得到相同前驱，直到相同 head，或迫使一个 head 出现在另一条 head 的上方。H0 的 head orders 为 3,6,9,18,27，没有一个等于另一 head，后一种情形不可能。

因此不同 chains 在大于3的 admitted rows 上自动不相交；terminal 也互异；only absolute terminal 3 可共用。链中不能共享 regular relay。这个结论既符合 §12 构造，也符合一般 exactly-seven §7.2 的必要 basin-disjointness。[S1]

Hybrid escape theorem 的路径 coalescence 是另一种 statement，不能据此允许这里共享 relay。[S3] 同样，某 prime 的 q-1 含 5 或其他 nonadmitted factor 不自动破坏 basin；被约束的是 exact multiplicative order 的因子。例如 6271-1 含 5 与11，但 ord_6271(5)=19，仍是合法 pure-3 relay。[S1, §7.2]

全部 actual prefixes 通过此不相交检查；若最终七链都成立，无须另加未经来源支持的强 disjointness 条件。CRT state 由不同 prime-square residues 合成一个全局 r，不逐 fiber 重选。

## 11. TERMINAL NONREGULAR CANDIDATES / 2e9 INVENTORY

源 Phase B 的完整 q<=2e9 admitted inventory 为 20771、40487、1645333507。[S4] 本轮不重跑其全局穷举，但独立证明了这三者的 primality、exact order、q² divisibility 和 q³ nondivisibility：

    20771:      w=10385=5*31*67,          s=2;
    40487:      w=40486=2*31*653,         s=2;
    1645333507: w=1645333506=2*3^3*30469139,s=2.

它们的 exact order 全是 composite，因此均不可能是 literal prime-order chain 的 terminal。没有出现第四个 <=2e9 admitted terminal；辅助 control 53471161 虽 s=2，但 q≡1 mod4，非 admitted。

本轮所有 certified chain factors 的 s 都为1，因此没有一个成功 terminal。测试从未用 Fermat-Wieferich 条件代替 exact-order proof：两种模幂同时记录，exact order 还经所有 prime-divisor exclusions 证明。

## 12. CONDITIONAL CERTIFICATE REPLAY — WHAT PASSED AND WHAT DID NOT

PASS：recursive primality certificates 66；arithmetic node records 33；三个 complete first-preimage factorizations；16 个 partial factor families；14 个 independently executed A/B progression domains；huge-31 Python replay；七个 finite terminal lower-bound proofs。

PASS：七个 actual regular heads 的 1,051,299 个 full-period cases，加上 row3 的6个 cases，总计 **1,051,305**；literal construction 的54个 collapsed classes；新 conditional alternative-head 推论的6480个 classes。

PASS：六个 fail-closed mutation tests：错误素性 witness、错误 exact order、nonadmitted prime 被标作 admitted、错误 CRT residue、擅自扩大下界适用域、虚构 full-certificate flag，全部拒绝。

**NOT DONE / NOT CLAIMED**：七个实际 terminal chains；最终 actual all-row ledger；数值化最终 global r,M,U,L；逐 d modL 的完整 actual certificate 检查；repository-native tests / CI replay；独立作者审稿；proof-assistant formal verification。

source 的头部 conditional fixture 和本轮重算都保留 hypothetical-upstream 标签。不能把其 54-cell PASS 写成 CERTIFIED FINITE COMPLETE C=1 CERTIFICATE。

## 13. DOES THIS KILL EXACTLY-SEVEN? NO

必须纠正任务判据中的一个逻辑风险：

    no literal prime-order terminal chain for one H0 head
    DOES NOT BY ITSELF IMPLY exactly-seven impossible.

第一，三个固定 depth-3 heads 不是一般 §7 的全部允许选择。第二，即使针对必需的 head 7、31、19 或5167 排除了纯 prime-order chains，§7 的一般 pure-3 basin 仍允许不是单一 prime-order path 的 actual order-DAG。§12 是充分构造，不是对所有 exactly-seven systems 的充要分类。

源 §13 的 B7 emptiness 才会直接攻击一般 seven-root survivor 的必要来源；仅对某些 prime-order paths 的未命中或否定不能替代 B7=empty。[S1, §13]

本轮甚至没有证明某一 literal head 的所有终止链都不存在；全体七项都还是 OPEN。

## 14. LOGICAL INTERFACE TO A303656

即使未来实例化本 conditional construction，直接所得也只是 stated formal class 的 finite complete C=1 certificate，即覆盖 c=0,1 的 exponent problem。原 A303656 问题的 c 无此上界。

因此它会击穿对应 formal class 的 universal finite-C1-certificate no-go，却不自动给出整个 a²+b²+3^c+5^d 问题的反例。仍须核对把不受限 c 的原问题连接到这个 C=1 certificate 的独立 reduction，或者对特定 n 排除全部相关 c,d。本轮没有完成或声称该接口。项目主状态保持不变。[S1; S5]

## 15. NEXT SINGLE ARITHMETIC TARGET

**Phi_5167(5)=(5^5167-1)/4 的 admitted first-child extraction 与 square-divisor test。**

这是一份确切的 3611 位输入，完整十进制值已随包保存。5167 是一般 seven-root normal form 的必需 depth-2 head，不像某个可替换的 depth-3 head。本轮独立穷尽表明其任何 admitted child 必须大于 1033400000001；模4引理保证至少一个 admitted child 存在。

下一个冻结目标只作用于这个整数：提取一个 prime q≡3 mod4 的 factor，给出可重放的素性证明，验证 ord_q(5)=5167，立即计算 q²/q³ lifting。若 s>=2，该 head 成功；若 s=1，则得到实际 regular relay 而不是宣称该 branch dead。这里不安排一般 nonregular prime scan，也不要求对这个3611位整数伪造 complete factorization。

## 16. FINAL REQUIRED FLAGS

```text
ALL SEVEN CHAINS EXIST? OPEN
CONDITIONAL CERTIFICATE INSTANTIATED? NO
FULL CERTIFICATE INDEPENDENTLY VERIFIED? NO
DOES THIS KILL EXACTLY-SEVEN? NO

SUCCESS LEVEL: C, with D partial-chain/cofactor data
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
'''
report=report.replace('MAIN_SHA_TOKEN',A['main_sha']).replace('MAIN_TREE_TOKEN',A['main_tree']).replace('PR_TABLE_TOKEN',prtable).replace('HEAD_TABLE_TOKEN',headtable).replace('FACTOR_TABLE_TOKEN',facttable).replace('NODE_TABLE_TOKEN',nodetable).replace('BOUND_TABLE_TOKEN',boundtable)
(R/'REPORT.md').write_text(report)
readme='''# A303656 seven-head completion-chain Phase D — read-only evidence bundle

Start with REPORT.md. Outcome: Level C with D partial data; all seven terminal
chain-existence questions remain OPEN. No complete actual C=1 certificate is present.

## Offline mathematical replay

```bash
python3 verify.py
python3 regression_tests.py
```

The default verifier uses Python standard library only. It independently checks
recursive full-(N-1) Lucas certificates, exact orders and valuations, exact factor
identities, actual head-row coverage, conditional compressed covers, recorded
search streams and the huge-31 Python replay. No network/repository code imports.

## Rerun both complete bounded factor-search implementations

Requires g++ and GMP development headers/libraries already installed:

```bash
python3 verify.py --replay-search
```

This compiles in a temporary directory and reruns the 14 matching uint128/GMP
search domains. The underlying methods are fixed-index cyclotomic preimage
searches, not a generic scan for nonregular primes. Recorded stdout is deterministic;
execution wall times are not. All integers in the uint128 implementation satisfy
its explicit uint64 candidate bound. The GMP implementation supports larger primes.

## Rebuild discovery outputs (not needed to verify)

```bash
python3 build_evidence.py
python3 write_report.py
```

Discovery additionally uses SymPy. Its probable-prime screening of the 121- and
171-digit cofactors is NOT an independent primality certificate. No terminal
hypothesis is filled from those values. The report and evidence retain OPEN.

## Main files

REPORT.md: mathematical report and all requested final flags.
SOURCES.md / AUTHORITY.json: source provenance and frozen live-main metadata.
evidence.json: 33 arithmetic nodes, 66 primality proof nodes, exact-order/lifting
witnesses, 19 factor families, conditional rows and seven terminal exclusion proofs.
verify.py / verification.json: independent checker and actual execution result.
regression_tests.py / regression_results.json: six fail-closed mutation checks.
search/ and replay_search/: exact candidate-domain logs from both native cores.
large31_independent_replay.json: Python arbitrary-precision third-core check.
cofactors/: exact remaining integers for moderate exponent targets.
ecm/: bounded stage-1 exploratory receipts, never absence proofs.
SHA256SUMS.txt: payload integrity; not a replacement for mathematical verification.

No binary, executable build product, nested archive, author email, or local Git
checkout is bundled. Source-repository CI/test receipts are not claimed as freshly
reproduced. No GitHub writes were performed.
'''
(R/'README.md').write_text(readme)
print('REPORT chars',len(report))
