# C21 / C22 的 typed target invariant：为何不能直接 joint-filter catalogue

## 结论

冻结的 46 行 inventory 内没有 joint-nonregular prime，只说明 critical state 中仍然保留的 **original joint targets** 若落在该 smooth-order 范围内，必须有 \(H_p\ge512\)。它不允许删除 regular catalogue targets，因为归纳会从外部 regular norm conditions 生成新的 unit targets。

C22 的有效改进来自 \(7,11\) core events 的独立性；与 joint-filter 无关。下面的结构 invariant 对 C21 和 C22 均适用。

## 精确 largest-order chain

记

\[
F(p)=P^+\!\left(\operatorname{lcm}(\operatorname{ord}_p3,
\operatorname{ord}_p5)\right).
\]

在 pivot \(M\) 处，每个 active target \(p\) 实际满足 \(F(p)=M\)，不仅是 \(M\mid L_p\)：因为 \(M\) 已是全部当前 target orders 的最大 prime factor。

给每个初始 joint target \(r\in T_0\) 一个 root label。归纳中可保持如下 invariant：

1. 当前 targets 分成 original joint targets 与 artificial regular targets。
2. 每个当前 target 带一个非空 root-label set；不同当前 targets 的 labels 彼此不交。
3. Original target \(r\) 带自己的 singleton label。
4. 若 pivot \(M\) 是 remaining regular norm prime，则新 artificial target \(M\) 带全部被删除 active targets 的 label union；每个带来的 root 都沿 \(F\) 的迭代链到达 \(M\)。
5. 若 pivot \(M\) 不在 norm set，则该组 active labels 被丢弃。整个过程从不增加 root-label 数。

Artificial target 的各个中间 prime 都是 regular inert primes，并必须是被替换掉的外部 norm primes。最大 pivot 严格下降；所以在 critical state \(M\) 中，所有 artificial targets 的 prime 值都大于 \(M\)，其 orders 的 prime factors却都不超过 \(M\)。因此它们正好可以进入冻结 catalogue 的 outside-target slots。

## 为什么 ancestry 本身不额外增加 root 成本

对给定 cutoff \(M\)，考虑 regular inert terminal \(p>M\) 且 \(F(p)\le M\)。称它 reachable，如果存在一个 joint-nonregular root \(r\)，使 \(F\) 的迭代从 \(r\) 到达 \(p\)，途中除 \(r\) 外的所有 vertices 都是大于 \(M\) 的 regular inert primes。

若若干不同 terminals 各自 reachable，则可为它们各选一个 root，令外部 norm set 包含这些 finite paths 的所有 regular vertices。不同 terminals 的路径在 cutoff 以上不能合并：一旦合并，确定性的 \(F\)-iteration 会给出相同 terminal。因此所选 roots 不同，各条路径在 \(>M\) 部分不相交。

按 descending pivots 执行归纳时，每个这样的 path pivot 只有一个 active target，故 \(t=1<M_{\rm pivot}\)，可以逐步把每个 root 变成对应 terminal。到 cutoff 时，所有这些 terminals 可以同时出现，每枚只耗一个初始 root。

所以：

- 不能无条件声称每一个 catalogue subset 都真实 reachable；这需要实际 joint roots 的 arithmetic existence / ancestry。
- 但若各 terminal individually reachable，则不存在额外的 combinatorial root-cost penalty 阻止其同时出现。
- 冻结 46-row inventory 只覆盖 \(19\)-smooth orders 且 \(H<512\)。它没有排除来自 inventory 外、沿 \(F\) 到达例如 71 或 271 的 joint root。

## 可验证的下一步 lemma

若要通过 typing 改善 direct budget，必须增加可检验的 arithmetic 输入，例如证明某个 heavy regular terminal 的上述 basin 不含 joint-nonregular root，从而合法删去相应 artificial row。仅检查该 terminal 本身 regular 不够。

另一种可验证目标是改变 restoration lemma，保留真正的 regular norm condition，而不把它加强为 unit avoidance；此时必须重新证明它与 fresh active targets 的联合 positive-mass bound，不能继续套未经 conditioning 修正的 marginal union bounds。

目前没有上述 basin exclusion，也没有新的 non-unit restoration theorem。故简单 joint-filter 必须 REJECT；冻结 universal-target budget 应保留所有 regular rows。这个结论不否定已独立通过的 C22 independence-block 改进。
