# C22：第二独立 referee 的证明审查

## 裁决

**ACCEPT。** 在冻结 C21 的完整 \(19\)-smooth、\(H<512\) inventory 及其未知-tail bound 基础上，core primes \(7,11\) 的真实独立性把 universal target budget 从 21 提高到 22。于是 finite eventual-power norm zero 至少需要 **23 个不同 joint-nonregular inert squared factors**。

这项强化不使用“catalogue 中没有 joint-nonregular prime”筛选，不改变 cutoff，不扩大 prime inventory。仍然保留全部 regular artificial targets。这里详细审查新的 independence block、完整归纳接口和 restoration；另外独立复算了 46 行 exact orders、三个 refined weights 以及全部 33 个新 rational budgets。

## 1. 新 core bound 及其 conditioning

在原 C21 proof 的准备步骤中，prime 3 的条件只使用 \(\beta\) parity：可使 residual mod 3 为 unit。任意 finite 2-norm condition 与任一 \(\beta\) parity 相容，所以可再固定一个允许的 positive-measure 2-primary cylinder。这个 conditioning 只作用于 \((\alpha_2,\beta_2)\)，没有对任何 odd-primary exponent coordinates 条件化。

令 \(E_p=\{3^\alpha+5^\beta=z_p\pmod p\}\)。Exact orders 为

\[
\operatorname{ord}_7(3)=\operatorname{ord}_7(5)=6,\qquad
\operatorname{ord}_{11}(3)=\operatorname{ord}_{11}(5)=5.
\]

固定 2-primary coordinates 后，\(E_7\) 只依赖 \((\alpha_3,\beta_3)\)，\(E_{11}\) 只依赖 \((\alpha_5,\beta_5)\)。这些 odd coordinate pairs 是独立 Haar。因此这两个 events 确实独立，且对任意固定 targets

\[
u=H(E_7)\le\frac13,\qquad v=H(E_{11})\le\frac3{25}.
\]

函数 \(u+v-uv\) 在单位正方形上分别递增，所以

\[
H(E_7\cup E_{11})
=u+v-uv
\le\frac13+\frac3{25}-\frac1{25}
=\frac{31}{75}.
\tag{1}
\]

旧 core contribution 为 \(34/75\)，故所有 \(M\ge11\) 的 direct budget 可统一减少 \(1/25\)。

这不是在“已经避开 \(E_7,E_{11}\)”后的 posterior 中应用原 marginal bounds。证明始终在保留全部 odd Haar coordinates 的空间中使用

\[
H(E_7\cup E_{11}\cup\text{其余 bad events})
\le H(E_7\cup E_{11})+\sum_{\rm 其余}H(E_p).
\]

其余 events 可以与 \(E_7,E_{11}\) 任意相关。

### 缺失 core 条件

若 prime 7 或 11 不在真实条件中，可添加任意该 prime 的 dummy unit-avoidance condition。这样只加强所需结论，而 (1) 对任何 target residue 一致成立。若 core prime 原本属于 regular norm set，强制 residual 为 unit 是合法的充分条件；若它属于 target set，则使用其已有 residue。因 \(Q,T\) 不交，每个 prime 至多有一个真实条件。所有 core primes 原本已在 \(C_M\) 中预算，dummy 条件不占 outside-target slots。

## 2. Budget 22 的完整归纳

保留原证明的对象：不交 finite odd inert sets \(Q,T\)，\(Q\setminus\{3\}\) 的每个 prime 至少对一个 base regular；每个 \(Q\)-prime 有任意 finite norm precision / residue，另有任意 finite 2-norm condition；\(T\)-primes 有任意 unit-avoidance residues。现在假设 \(|T|\le22\)。

设 \(M=\max_{p\in T}P^+(L_p)\)，\(t\) 为 active targets 数。

- 先按原 regular averaging 删除所有 \(q>M\) 的 norm factors。
- 当 \(t<M\) 时，删去 active targets；若 \(M\) 是 remaining regular norm prime，删去此 norm factor 并加入 prime \(M\) 的 unit target。新的 target 数为 \(|T|-t+\delta\le22\)，最大 order prime 严格下降。
- 应用归纳后，所有 lower constraints 都不依赖 fresh \(M\)-primary coordinates。每个 active target 的 fibre bad probability 至多 \(1/M\)，因此总和 \(t/M<1\)，保留 positive mass。
- 新 prime \(M\) 的 unit condition保证恢复其任意 precision norm factor；它本身不依赖 \(M\)-primary coordinates，所以 fresh-fibre 选择不会破坏它。

当 \(M\ge23\) 时，\(t\le22<M\)，全部由这个步骤处理。因此新的 critical cases 仍只有

\[
M\in\{11,13,17,19\},\qquad M\le t\le22,
\]

合计 32 个，加上 \(M\le7\) base case 为 33 个。没有引入 \(M=23\) 的 inventory requirement。

## 3. 全部 finite budgets 独立复算

采用冻结 catalogue 的完整 eligible rows，重新用直接 modular iteration 算 exact orders，再用 exact addition counts 算 \(11,71,271\) 的 refined weights。对未列出 primes 仍保留无限 \(1/512\) placeholders。Top-\(k\) 时放入 \(k\) 个 placeholders 足够，未删除任何 regular row。

Base case 为

\[
C_7+\operatorname{Top}_{22}\{p>7,\ P^+(L_p)\le7\}
=\frac{155932663}{190512000}<1.
\]

每个 critical case 使用

\[
C_M-\frac1{25}+I_M(22-t)+A_M(t).
\tag{2}
\]

独立复算 maxima：

| \(M\) | 最坏 \(t\) | 最大 budget |
|---:|---:|---:|
| 7 | base | \(155932663/190512000\) |
| 11 | 11 | \(4238011529/4390848000\) |
| 13 | 13 | \(110693503/115315200\) |
| 17 | 17 | \(2645398583/2940537600\) |
| 19 | 19 | \(41918323/50265600\) |

所有 33 个 inequalities 都严格小于 1，全局最小剩余质量为

\[
\frac{152836471}{4390848000}>0.
\]

逐项结果保存在同目录 c22_independent_budgets.json。

另作直接 \(225\)-cell 检查：对每个 fixed parity pair，取 \(\alpha,\beta\bmod30\) 中相应的 \(15\times15\) cells，joint \((s\bmod7,s\bmod11)\) counts 精确满足 product factorization。四个 parity pairs 的最大 union probabilities 分别为

\[
71/225,\quad31/75,\quad31/75,\quad71/225.
\]

这是对 independence 公式的有限复核；无限 proof 使用的是上述 disjoint primary-coordinate argument。

## 4. Regular restoration 没有新依赖

Core budgets 在完全未对 odd constraints 条件化的 Haar 空间中一次性给出 positive-measure admissible set。删除的 \(q>M\) regular norm factors 可按升序恢复：此时所有已经存在的 norm factors 的 prime 都小于 \(q\)，所有 targets 的 order prime factors 都不超过 \(M<q\)，因此它们均不依赖 \(q\)-primary exponent components。

对 chosen regular base 的 \(q\)-primary coordinate 积分，原 C21 的局部平均下界 \(1/q\) 保证每次恢复保留 positive mass。恢复过程中不需要 \(E_7,E_{11}\) 在其他 constraints 下继续独立；独立性只在先前的 unconditioned direct budget 中使用一次。

全部约束仍由 finite exponent quotients 决定，得到 positive-measure clopen exponent set。这完成 universal 22-target statement。

## 5. 23-root corollary 的适用空间

若某个 finite eventual-power density \(f_q(a)=0\)，先删除处处 positive 的 split factors 与仅一次幂的 inert factors。余下 joint-nonregular inert primes 作 \(T\)，其余 regular inert primes 作 \(Q\)，prime 3 由 base 5 regularity / parity 处理。若 \(|T|\le22\)，新 theorem 给 positive exponent Haar mass，使每个 \(T\)-residual 为 unit、所有 \(Q\)-norm factors positive、2-norm factor positive，矛盾。

故至少有 23 个不同 inert primes \(p>3\) 满足

\[
p^2\mid q,\qquad
v_p(3^{\operatorname{ord}_p3}-1)\ge2,\qquad
v_p(5^{\operatorname{ord}_p5}-1)\ge2.
\]

这是 finite **eventual-power norm obstruction** 的必要条件。它没有给出 LP，也没有修改 ordinary exponent-row certificates，更不是全整数 counterexample 或原猜想的证明。
