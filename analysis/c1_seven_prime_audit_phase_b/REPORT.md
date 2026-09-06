# A303656：扩展 prime scan 与七-prime 证明审阅

## 结论

第一项完成：从旧 q≤10^7 panel 扩展到 **q≤2×10^9**，上界扩大200倍。两种不同整数算法分别完整检查49,112,626个q≡3(mod4)的素数，得到相同inventory：

    20771, 40487, 1645333507.

第二项完成：七个original nonregular primes必要界通过本轮重新推导与对抗检查，判定 **ACCEPT IN THE STATED FORMAL CLASS**。新重证在N≤6下直接消去所有p≥7，避免依赖一般critical-core提取。没有发现需要撤回七-prime命题的致命缺口。

这仍不是独立作者/不同模型的审稿，也不是形式化验证。新代码不import原reference，source replay和新的检查分开报告。

## 1. Authority及输入

Live main与source所绑定版本一致：

    main 44e522dd6e88504e2b9829f0b27359e6c45a76ff
    tree 6a30565826c8f988bfbb85e4098b78b2992d290c
    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED

本轮用户请求授权的是有界scan扩展及审阅；没有进行repository promotion或写入GitHub。source ZIP和内部payload完整性通过，详情见REVIEW.md。

## 2. 扫描规约与完整性

精确谓词为5^(q-1)≡1(modq²)，等价于s_q≥2。Implementation A使用all-integer segmented sieve与128-bit乘法的模q²二进制幂；B使用另写的odd-only sieve与base-q两位乘法，且采用不同的幂运算方向。B还逐prime检查Fermat residue的低位为1。

2e9以内所有中间整数均在已证明的机器整数界内：A乘法用128位；B最高的两位乘法和不超过2q²-3q<2^64。没有浮点决定。

逐10^7整数区间记录候选数、prime sum、residue-stream fingerprint及hits，外加最后一个包含2e9端点的空候选区间，共201条记录。A/B记录逐项一致。Fingerprint仅作为回归对照，不代替完整筛法与整数算法的正确性论证。

Python arbitrary-precision pow独立复算旧≤10^7基线：332,398个候选，命中20771和40487。新旧全部hits另作确定性trial-division primality、完整q-1分解、order因子排除和精确s_q认证。

所有扫描raw区间记录、程序、baseline及证书均在本包；没有用外部list跳过任何候选。

## 3. 结果

| q | ord_q(5) | order分解 | s_q | 永远不可能有admitted dynamic row的odd factor坐标 |
|---:|---:|---|---:|---|
| 20771 | 10385 | 5·31·67 | 2 | 5 |
| 40487 | 40486 | 2·31·653 | 2 | 653 |
| 1645333507 | 1645333506 | 2·3³·30469139 | 2 | 无 |

新增的是完整扫描panel中的1645333507，不是文献新发现。它已在源仓库作为boundary resource出现；本轮将其连同所有≤2e9候选一起穷举认证。OEIS A123692与A305332也记录该素数和order，外部资料仅用于来源/已知性对照。

补充扫描所有odd primes q≠5到10^8：5,761,453个候选，命中20771、40487、53471161。第三个满足q≡1(mod4)，不属于admitted original-row resource，不能误算为第四个资源。

本轮完整scan界就是2e9，不外推到更高。更高精度和任意r/E的no-go量词来自数学定理，而不是本轮scan枚举。

## 4. 七-prime审阅的主线

详见SEVEN_PRIME_INDEPENDENT_PROOF.md与REVIEW.md。核心是：

    假设完整证书且nonregular资源≤6
      -> 固定同一个可兼容两种parity的anchor
      -> 选dynamic3 inactive的parity
      -> 每个p≥7因seed数<p，只可能simple-pair覆盖
      -> full exact收缩保持来源单射及seed数≤6
      -> 剩余仅3、5
      -> rank3浅层helper容量≤8/9，full frontier至少七叶
      -> rank5 full收缩最多留下两个proper3-cylinders
      -> 两种可能均矛盾。

rank5步骤明确区分n≤4与n=5或6，并计入全部minimal witnesses。非空constant residual被实际11/71 helper位置约束排除，而不是凭直觉宣称macro不能覆盖全域。

## 5. 新的独立检验

| 检查 | 明确有限范围/比较数 | 结果 |
|---|---|---|
| Actual row normal forms | 565,710 full-event comparisons | 0 mismatches |
| Coarse forall-lifts predicate | 730,180 comparisons | 0 mismatches |
| Fixed-anchor two-adic boundary | K2=2,...,12；8,188 residues、16,376 parity witnesses | PASS |
| Sparse local-cover lemma | 2,504,523配置；具体p/β见JSON | 0 mismatches |
| Shallow rank3 fixed-head placements | 729个placement；max union8/9 | PASS |
| Complete ternary frontiers | 所有≤7叶树形，共17个含root-only | 深度3至少七叶 |
| Rank5五/六行cylinder多重集 | 1,901,416组，允许不同来源重复几何 | witness至多1/2 |
| Compatible/incompatible CRT交 | 1,600对 | 0 mismatches |
| Abstract sparse exact contraction | 1,200 states、18,000 fiber comparisons | 0 mismatches |
| 本轮named regression tests | 15项 | PASS |

原source重放另为25个payload checksums、10个mathematical JSON、15项tests全部PASS。它与上述新实现分开，不声称复用原代码就是独立证据。

## 6. 扩展面板对应的数学结论

七-prime必要界与本轮inventory联合给出：所有nonregular original primes都来自上述三个素数的finite admitted systems不可能complete simultaneous；因此尤其排除全部odd-row primes≤2e9的证书。Regular helpers/support rows、precision和residues仍可任意。

还记录一个**不依赖七-prime界**的第二证明：选定anchor及关闭dynamic3的parity后，将三个潜在rigid rows分别阻断于5、653、3。每个坐标只需避开一个first digit；前两者永无admitted dynamic，第三者在当前boundary上inactive。随后greedy避开其余dynamic centers，再reverse CRT。见EXPANDED_PANEL_BLOCKER_PROOF.md。

此第二证明让扩展panel no-go不依赖七-prime定理的未来审稿结果；但它没有推广到任意nonregular pool。

## 7. 输出与不变的边界

- REPORT.md：两项工作的总报告。
- REVIEW.md：逐环节审阅裁决及误用风险。
- SEVEN_PRIME_INDEPENDENT_PROOF.md：不依赖general critical-core提取的重证。
- EXPANDED_PANEL_BLOCKER_PROOF.md：独立的three-resource-pool no-go。
- tools/、tests/、results/：scan、核验及全部有限结果。
- evidence/：原包和authority/source custody。

未证明七资源足够、universal finite-certificate no-go或A303656 universal representability。未对整个Phase B报告全部命题进行独立背书。

    PROJECT: PAUSED
    ACTIVE PROMOTED ROUTE: NONE
    A303656: UNRESOLVED
    GITHUB WRITES PERFORMED: NONE
