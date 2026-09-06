# Theorem audit and claim register

## 1. Verdict register

| ID | Statement | Classification | Essential limitation |
|---|---|---|---|
| P1 | 六态monotone demand在exact top elimination下封闭 | PROVED | TRUE的EITHER root不代表BOTH |
| P2 | Anchor/state-tagged minimal slice cover clauses给exact residual | PROVED | 保留one-hot global states与typed guarantees |
| P3 | Actual pooled full fiber给coloured original prefix frontier | PROVED | arbitrary coloured frontier的arithmetic realization未由此证明 |
| P4 | Full-depth allocated blockers + dynamic slack给common odd escape | PROVED | 每个坐标须有strict budget；不是所有系统都通过 |
| P4.1 | nonregular pool⊆{20771,40487,1645333507}不存在complete C=1 certificate | PROVED UNIFORM SUBCLASS | 不是整个prime interval inventory；regular rows可任意大 |
| P4.2 | single-nonregular survivor必须squarefree odd order且fully dynamically supported | PROVED NECESSARY CONDITION | 非充分条件、非已找到actual survivor |
| P5 | Squarefree regular order-closed actual seed给complete odd pooled cover | CONDITIONAL CONSTRUCTION THEOREM | seed hypotheses尚未实例化；构造本身无two-adic row且非full certificate |
| K4 | R_(3,4)=empty | PROVED WITH FINITE CERTIFICATES | 不推广到d≥5 |
| K4 cor. | pooled full3-fiber rigid N≥122，dynamic allowed N≥31 | PROVED NECESSARY BOUNDS | only original rows；不主张sharpness |
| A-literal | 任意admitted系统都不存在boundary-inclusive pooled lower cover | FALSE | 实际{3,7}+two-adic例，不是full certificate |
| A-normalized | 无common-safe-boundary actual odd pooled cover | NOT ESTABLISHED | 未提供actual complete odd pooled cover，也未普遍排除 |
| C1-universal | 不存在任何complete finite C=1 certificate | NOT ESTABLISHED | P4只处理明确subclass |
| A303656 | 目标整数表示问题已解决 | NOT CLAIMED | Local-mask escape不等于表示定理 |

## 2. P1/P2 quantifier audit

正确式子是`forall z[(L0 or T0) and (L1 or T1)]`分别变成
`(L0 or forall z T0) and (L1 or forall z T1)`。

不是`L0 or L1 or forall z(T0 or T1)`；后者仅对应EITHER。

若候选row states未冻结，state symbols不是每个fiber重新选择的局部常量。所有cover clauses必须保留它们；最后是`exists s forall x`。代码通过独立direct truth枚举每个完整s，再对比symbolic roots，避免把`forall x exists s_x`当成答案。

`minimal_slice_covers`的minimality在slice incidence variables层面成立。加入one-hot state constraints后，它们不一定是全部semantic prime implicants；本文不作这个更强的错误声明。

在lower事件独立于top时，minimal cover中的该事件只会作为singleton pass-through出现。这样其原始dynamic bundle可原样保留，不必假称lower guard是一个新CRT cylinder。

## 3. Row normal-form audit

三处常见漏洞均显式关闭：

- `h>=s`仅在K>s时进入principal-subgroup dynamic lifting；K<=s且完全匹配是local-zero guard，不fatal。
- coarse m=min(a,beta)，不能把beta之外的未固定higher digits当作已accepted shells。
- 一个actual q可anchor0 dynamic、anchor1 rigid；assigned rank必须附在组件上，不能只附在row ID上。

Difference2保证完整b0,b1 modw不同；不保证投影到某个lower factor后不同。Full-depth blocker中允许两侧projection重合，并按union收费。

同lower、同original rigid rank-p时，两side cylinders等深。它们若top位置相同，连同共同lower guard将迫使b0=b1 modw，故不可能。因此这个特定情形的两片确实不相交。

## 4. P3 minimality and resource audit

把dynamic shell展开为side cylinders只用于p-adic几何证明，它们仍是同一原始bundle的多个OR组件。将其计为p−1个不同primes会直接破坏P3的resource结论。

Irredundant primitive-cylinder subcover可由laminarity提取prefix antichain；row-minimality另需按整条row验证。本文不把primitive deletion混同row deletion。

一个original rigid q至多供应两片，只在一个fixed lower fiber成立。不同fibers允许同一q重复出现，不能对整棵树实行global token consumption。相反，在一个fiber中不能把重复macro references当成更多actual q。

Derived macro前沿的几何递归正确，但其leaf不是R_(p,e)中的新成员。K4和122/31界仅在首次original pooled full-fiber witness或明确original fiber上使用。

## 5. P4 proof obligations

P4的关键不是scarcity heuristic，而是以下五个确定性步骤：

1. 每个original rigid fatal event是一个完整logarithm congruence。违反其中一个order prime-power因子就永久禁用该event。
2. 对它作全domain投影，可能禁用过多exponents，但不会漏掉该rigid event；所以over-exclusion只让sufficient test更保守。
3. 选择坐标p时，w_p的prime factors均小于p，dynamic activity由已固定prefix决定。
4. Difference2限制active dynamic bundle至多一个，确保预算用D_p而非错误的两侧之和。
5. 严格的union bound逐坐标构造同一个coarse exponent；joint reverse CRT保留固定two-adic coordinate并给同一个full odd-safe exponent。

这些步骤不依赖clauses是否合流，也不依赖macro数量。每个positive δ_p给实际剩余概率，下界乘积对有限系统严格为正。

任何不满足strict inequality的系统只是不被P4判定；不能从test failure推出存在pooled cover。

### Occupied-coordinate improvement is genuine

旧#14只能在没有original dynamic row的free coordinate上放至多两个first digits。
新P4对q=1645333507使用3^3上的两个depth-three cylinders，总质量2/27。
即使3-row存在并允许任意precision与odd shell集合，D3<3/4，合计<89/108。
若错用first digits，3/4+2/3>1；新结论不能由这项旧预算直接得到。

这里q的original rigid assigned rank是30469139，不是3。投影到3仅用于主动阻断，故不与R3,1–4=empty冲突。

### Uniform corollary scope

三种nonregular rows各至多出现一次，因为原始primes不同。每个最多两侧rigid classes，故2/5、2/653、2/27是所有shared residues的有效upper bounds。

其余rows被假定regular，因而没有任何rigid fatal event，只增加proper dynamic hazards与ambient support。不能把未检查的更大nonregular row归入“regular”以套用结论。

## 6. K4 factor/primality proof audit

若R_(3,4)有q，则w_q∈{81,162}。q>3且q不整除w_q，exact multiplicative order使q只出现在对应primitive cyclotomic factor；nonregularity使其中q-valuation至少2。

两项完整factorizations均由大整数乘法复原。因子素性不是依据factor discovery软件宣称：certificate checker递归验证每个n−1的完整prime factorization，并检查某a满足

```text
a^(n-1) == 1 mod n
for every prime r | n-1:
    a^((n-1)/r) != 1 mod n.
```

第一式使a为unit；第二组与完整factorization使ord_n(a)=n−1。于是n−1|phi(n)，而phi(n)<=n−1，合数时严格小于n−1，矛盾。因此n为prime。所有递归leaf终止于2。

该full-order判据不需要借用partial-factor Pocklington版本的额外gcd条件；它使用的是n−1的完整已认证分解。Unit test故意把4861的base改成1，verifier必须拒绝。

旧depths1–3从绑定#16继承。本包没有声称重新认证#16每一项旧resultant或重新扫描其10^7 inventory。

## 7. P5 construction audit

P5不是“假设存在pooled cover则有pooled cover”。它的hypotheses仅为实际prime/order/lifting/support条件，并用明确residues r_p=2、r_q=q+2构造覆盖。

平方自由条件作用于LCM U的odd prime-power depth，而不是禁止不同orders共享同一个prime factor。所有regular support primes属于T并且都在U中出现，故w_pp|U。终端q的s>=2确保ord_(q²)(5)=w_q，所以U=L。

Least nonzero-coordinate proof依赖这些精确条件；没有它们，不能把一个dynamic row的guard当作自动active。相应±1分支也依赖v2(w_p)<=1；这是q≡3 mod4给出的实际限制。

构造明确不加入two-adic row。d=0,c=1时所有局部值−2或q−2均odd-safe，所以构造本身不是complete certificate。没有声称添加任意额外event后仍保留这个特定escape。

Even w_q时d=M还使anchor0全部odd-safe，故conditional construction确实可以是genuinely mixed而不是one-anchor complete。

已知三个nonregular rows均未通过seed gates。regular skeleton的actual U是6、actual L是1302；把1302提升为coarse U需要尚未提供的actual support seed。这一点不能通过把full period重命名为coarse period来绕过。

## 8. Computation-to-theorem boundary

| Evidence | What it proves | What it does not prove |
|---|---|---|
| Exact row enumeration | 列明参数下direct full/coarse masks一致 | 全部many-row arithmetic systems的穷举 |
| Synthetic stateful models | 测试typed/provenance实现；可发现逻辑反例 | Synthetic row labels是actual prime |
| Blocker finite models | 代码实现与constructive argument的边界检查 | Universal P4由有限模型归纳成立 |
| Lucas certificates + products | 两个具体cyclotomic整数完整squarefree | 所有higher-depth cyclotomics squarefree |
| Actual SPLIT full replay | 一个完整指定period的精确mask与escape | 完整lower-domain pooled cover |
| Conditional seed proof | 每个符合hypotheses的actual seed都有构造 | 已存在/已找到这样的actual seed |

Universal P4与P5依据本文数学证明；finite checks是adversarial corroboration。新的K4同时依赖完整有限arithmetic certificates与general order argument。

## 9. Endgame audit

本轮没有把下列缺口互相抵消：actual SPLIT缺whole-domain completeness；完整abstract covers缺actual powers-of-five realization；conditional seed construction缺一个已认证seed；完整pooled cover即使取得，仍缺反侧anchor top obligations。

因此最终NO的含义是本轮没有普遍消去S1第二分支，而不是证明了完整C=1 certificate存在。原项目三条authority state均保持不变。
