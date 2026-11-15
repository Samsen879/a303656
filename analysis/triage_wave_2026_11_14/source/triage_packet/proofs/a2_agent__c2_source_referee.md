# C2：Moree density 与 proper-antichain / g6 接口的第二审查

## 窄范围裁决

**ACCEPT：** (i) Moree fixed-divisibility densities 经 finite inclusion–exclusion 推出 B7 relative prime density 0；(ii) proper admitted antichain product theorem；(iii) distinct-frontier expansion 与已认证 \(g_6\) 的全局 growth 推论。

本次独立阅读 primary Moree source 与 C2 proof text。按 root 的任务边界，不重复运行已由 root / C21 referee 完整 replay 的 \(g_6\) inventory；这里只重审 finite certificate 如何推出 global minimum，以及 maximum-label recurrence 接口。没有把 density 0 写为 emptiness，也没有把 repo seven-root bound 与新的 eventual norm 23-root bound混同。

## 1. Moree 的精确 source scope

Primary source：
Pieter Moree, *On primes p for which d divides ord_p(g)*,
arXiv:math/0407421，<https://arxiv.org/pdf/math/0407421>。

原文 Corollary 1 给 fixed \(d,g\) 的 natural prime density，且无 GRH 假设。Theorem 2 中，当 \(d\) 为 odd 时 \(\epsilon_1=1\)，所以

\[
\delta_g(d)=
\frac1{d(h,d^\infty)}
\prod_{\ell\mid d}\frac{\ell^2}{\ell^2-1}.
\]

取 \(g=5\)，最大 perfect-power exponent \(h=1\)。对 squarefree odd \(d\)，

\[
\delta_5(d)=\prod_{\ell\mid d}\frac{\ell}{\ell^2-1}.
\tag{1}
\]

没有附加 \((d,5)=1\) 要求；\(\ell=5\) 可出现在 finite set 中。原文 Theorem 3 才是 GRH 下更强 error term，C2 的应用不使用它。

给定有限 \(\Lambda\subset\{\ell:\ell\text{ prime},\ell\equiv1\pmod4\}\)，令 \(m=\prod_{\ell\in\Lambda}\ell\)。整数恒等式

\[
\mathbf1_{\{\forall\ell\in\Lambda:\ell\nmid\operatorname{ord}_q5\}}
=\sum_{d\mid m}\mu(d)\mathbf1_{\{d\mid\operatorname{ord}_q5\}}
\]

是有限求和。因此先固定 \(\Lambda\) 再令 \(X\to\infty\)，由 (1) 得到 exact limiting proportion

\[
\prod_{\ell\in\Lambda}
\left(1-\frac{\ell}{\ell^2-1}\right).
\tag{2}
\]

B7 的 terminal set 为 \(\{3\}\)，故 root order 不能有任何 \(\ell\equiv1\pmod4\) 的 factor，否则它直接成为错误 terminal。B7 因而包含于上述每一个 avoidance set。

又 \(\sum_{\ell\equiv1(4)}1/\ell=\infty\)，而 \(\ell/(\ell^2-1)>1/\ell\)，故有限 products (2) 可任意小。严格量词是：给定 \(\varepsilon>0\)，先选 finite \(\Lambda\) 使 product 小于 \(\varepsilon\)，再对这个固定 \(\Lambda\) 令 \(X\to\infty\)，最后令 \(\varepsilon\downarrow0\)。没有移动 modulus、没有交换未经证明的无限和与极限。

因此

\[
\#\{q\le X:q\in B7\}=o(\pi(X)).
\]

Admitted primes 是 \(q\equiv3\pmod4\)，其计数渐近为 \(\pi(X)/2\)，故 B7 在 admitted primes 中的 relative natural density 也为 0。这个结论不证明 B7 finite、empty，或没有具体 member。

## 2. Proper-antichain theorem

对 actual admitted prime \(x>3\)，设

\[
H(x)=\{p>3:p\equiv3\pmod4,\ p\mid\operatorname{ord}_x5\},
\qquad P(x)=\prod_{p\in H(x)}p.
\]

由于 \(x\equiv3\pmod4\)、\(\operatorname{ord}_x5\mid x-1\)，

\[
P(x)\le\operatorname{oddpart}(\operatorname{ord}_x5)
\le(x-1)/2<x.
\tag{3}
\]

先证明 closed closure 的辅助命题：任何 reachability antichain \(A\subseteq D_{\rm ord}(x)\) 都有 \(\prod A\le x\)，等号仅当 \(A=\{x\}\)。若 \(x\notin A\)，给每个 \(a\in A\) 选择一条路径并按第一条 admitted child 分组；shared descendant 只分配一次。每组仍是相应 child closure 的 antichain，强归纳和 (3) 给出严格上界。

对 proper antichain 即得

\[
\prod_{a\in A}a\le P(q).
\]

“Proper”不可删除：\(A=\{q\}\) 是 closed antichain，但 \(q>P(q)\)。Antichain 条件也不可删除，深层相互可达 labels 的 product 不受同一界控制。

令 \(M(q)\) 为 direct support \(H(q)\) 中不被另一 direct child reach 的 maximal elements。每个 proper descendant 都位于某个 \(m\in M(q)\) 的 closure。再次按 \(m\) 分组，并利用辅助命题的严格等号条件，得到

\[
\max_{A\ {\rm proper\ antichain}}\prod A
=\prod_{m\in M(q)}m=P^*(q),
\]

且 maximizer 唯一为 \(M(q)\)。Shared descendants 不会产生重复乘积；这不是 tree 假设。

在 B7 中，root order squarefree 且没有 split odd prime factors，所以

\[
P(q)=
\frac{\operatorname{ord}_q5}
{2^{v_2(\operatorname{ord}_q5)}
3^{v_3(\operatorname{ord}_q5)}}.
\]

一般深层 antichain product 只保证不超过此量，不保证整除 root order。

## 3. Expanded frontier 不必是 antichain，但 recurrence 不依赖它

从 \(F=M(q)\) 开始，取当前数值最大的 label \(x\)，令

\[
F'=(F\setminus\{x\})\cup H(x),\qquad
U(F)=\bigcup_{p\in F}D_{\rm ord}(p).
\]

边严格降值，故 \(x\) 也是 \(U(F)\) 的最大 label，不能由另一个 frontier label reach。于是
\(U(F')=U(F)\setminus\{x\}\)：每步恰少一个 vertex。

设 \(Z=\prod(F\setminus\{x\})\)。因为 frontier 是 distinct prime labels 的集合，

\[
\prod F'
=\frac{ZP(x)}{\gcd(Z,P(x))}\le ZP(x).
\]

用 (3) 得

\[
\prod F=xZ\ge(2P(x)+1)Z\ge2\prod F'+1.
\tag{4}
\]

\(F'\) 可以有可比较的 labels。证明没有对 \(F'\) 误用 proper-antichain inequality；它只用了 local bound (3)、集合去重和 (4)。\(g_j\) 的定义允许任意 finite nonempty distinct actual-prime frontier，因此停止时仍可调用 \(g_j\)。

B7 的 no-dead-end lemma 保证每个 proper subtree 都包含 7，因此 expansion 不会提前变空，并可在任意要求的剩余 closure size 精确停止。

## 4. g6 certificate 的全局含义

已认证 witness \(\{43,82339\}\) 的 product 为 \(3540577\)，closure union 有 6 个 vertices。任何 product 更小的 frontier，其每个 prime label 都小于此 witness bound。因此该界内的完整 compatible-prime inventory 与 product-bounded subset enumeration 足以证明全局 minimum；它不是把 bounded prime scan 外推到任意 root。

手工 minimization 接口也成立：最优 frontier 可删去冗余 7；budget 内唯一 three-label possibility \(\{43,127,379\}\) 只有 4 个 closure vertices；singletons 由完整 inventory 排除。Pairs 的两个 closure 都含 7，若 union 至少为 6，则 sizes \(u\le v\) 满足 \(u+v\ge7\)，所以使用旧 \(g_2,g_3,g_4,g_5\) 即得 product 至少 \(43\cdot82339\)。Unique prime factorization 给出 optimizer 的唯一性。

从 \(k-1\) 个 proper vertices 停到 6 个恰用 \(k-7\) 步。迭代 (4) 的 shifted form
\(W_{\rm old}+1\ge2(W_{\rm new}+1)\)，得到

\[
P^*(q)\ge3540578\cdot2^{k-7}-1
\qquad(k\ge7).
\]

这允许 branching 与 shared descendants，不对 root \(q\) 加大小 cutoff。它是 necessary order lower bound，不提供 root-order upper bound，也不产生 B7 member 或 emptiness。Repo 的 ordinary admitted \(C=1\) seven-root statement 不因此升级；本轮 C22 推出的 23 roots 属于另一个 finite eventual-power norm obstruction 空间。
