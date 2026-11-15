# E1 MP-LT 与 fixed primitive-noise positivity：第二独立审查

## 裁决

**ACCEPT。** 对 E1 实际定义的 corrected \(C32\) profiles，新审查通过的 unit-noise extension 给出

\[
\boxed{
\mathrm{MP\!-\!LT}
\ \Longleftrightarrow\
\bigl[\forall Q\ge2,\ \forall a\bmod32W_Q,\ P_Q(a)>0\bigr]
\ \Longleftrightarrow\
P_\infty>0\quad\text{Haar-a.e.}
}
\tag{E1}
\]

这里的 finite positivity 是 E1 的 **primitive profile** positivity，不能替换为原 norm LP。这个结论仍未证明三者中的任一个成立，也没有审查替代 E1 的 integer analytic reduction。

本次独立逐式读了 proofs/05_hybrid_covariance.md §7–9A、proofs/09_romanoff_tail.md、proofs/11_primitive_profile_scope.md，以及 REPORT_zh.md 的 profile 和 MP-LT 定义。

## 1. Profile 的模型身份

令

\[
W_Q=\prod_{\substack{p\le Q\\p\equiv3\ (4)}}p,\qquad
V_Q=\prod_{p\mid W_Q}(1-1/p),
\]

并令 \(\psi=\mathbf1_{C32}\)，其中 \(C32\) 是报告固定的 15 个 mod-32 classes。实际 finite profile 是

\[
P_Q(x)=
\int_E\psi(x-s(e))\!
\prod_{p\mid W_Q}
\frac{\mathbf1_{p\nmid x-s(e)}}{1-1/p}\,de,
\tag{1}
\]

其中 \(s(e)=T_3(\alpha)+T_5(\beta)\)，\(e\) 为完整 joint exponent Haar。这与报告中的 stable-period limiting fraction 完全一致。

特别是：

- 分母是全部 exponent pairs 的 \(J\)，不是通过 \(C32\) selector 后的 pair count，所以没有把 prior 改成另一个 conditioned exponent law。
- Signed \(v_X\)、small/large sieve weights、\(\eta\)、\(X\)-dependent cutoffs 都属于 integer proxy；它们不出现在固定 \(Q\) 的最终 profile (1) 中。
- \(W_Q\) 是 nested prime-prefix product，**不是**“只保留 denominator \(d\le Q\)”的 Fourier truncation。所有 \(d\mid W_Q\) 的 coefficients 都存在，哪怕 \(d>Q\)。
- Own-base 3 的 finite preperiod 在 growing exponent rectangles 中所占比例趋零；这正是同一个 eventual \(\mu\)，没有额外 transient-row 修改。

定义 finite positive measure

\[
\kappa=
(\psi\,dH_2)
\otimes\!\!\bigotimes_{p\equiv3(4)} H_{\mathbb Z_p^\times}
\otimes\!\!\bigotimes_{p\equiv1(4)} H_{\mathbb Z_p}.
\]

它的总质量是
\[
m=\int\psi\,dH_2=15/32.
\]
则 (1) 是 \(\mu*\kappa\) 的有限-prefix density。归一化 \(G_Q=P_Q/m\) 后得到 probability-noise model。

## 2. Unit-noise support theorem 适用

使用与 A2 相同的完整 lower-primary exponent conditioning：
\((\alpha_\ell,\beta_\ell)_{\ell\le P}\)，包括 split \(\ell\) 的 exponent coordinates，不能只固定 inert coordinates。Split output noise 为 Haar 不等于可以删除这些 exponent correlations。

过去 likelihood 的 2-adic factor 为固定 bounded locally constant function \(\psi/m\)，inert factors 为 normalized unit indicators；split output factors为 1。所有过去 output shifts 都由这些完整 lower coordinates 决定。

尾部 Fourier support 是已审 unit-noise extension 的一个子集：只有 squarefree inert conductors 非零，primitive coefficient 的模平方为 \(\phi(q)^{-2}\)。所以完全相同的 conditional Parseval 与 rough-order bound 给出

\[
E[G_\infty^2\mid\mathcal F_P]
\le C_0\,G_P^2,
\tag{2}
\]

其中 \(C_0\) 与 \(P\) 和 conditioning 无关。这里 \(\mathcal F_P\) 可取所有 \(p\le P\) 的完整 output coordinates。因为 noise kernel 本身在 \(32W_P\) 上 locally constant，\(G_P\) 就是报告的 \((32/15)P_P\)；不需要另有 prime-power approximation。

因此 \(P_Q\to P_\infty\) in \(L^2\) 和 a.e.，并有

\[
\{P_\infty=0\}
=\bigcup_{Q\ge5}\{P_Q=0\}
\quad\text{Haar-a.e.}
\tag{3}
\]

每个 finite zero 是正测度 cylinder，且之后吸收。故 finite primitive positivity 与 primitive POS 等价。\(Q<5\) 的 profiles 是较高 prefix 的 conditional expectations，所以不会改变这个等价。

## 3. Primitive POS ⇒ MP-LT

报告定义

\[
b_Q(t)=H\{P_Q<t\},\qquad
\mathcal T(Q)=
\sum_{\substack{q>Q\\(q,5)=1}}
\frac{(q/\phi(q))^2}{q\,\operatorname{ord}_q5}.
\]

已证 \(\mathcal T(Q)\to0\)，且每个 finite \(Q\) 都有 \(\mathcal T(Q)>0\)。对任意固定 \(C>0\)，MP-LT 是

\[
\inf_{Q\ge2,\ t>0}
\{b_Q(t)+C\mathcal T(Q)/t^2\}=0.
\]

若 \(P_\infty>0\) a.e.，给定 \(\varepsilon>0\)，先取固定小 \(t>0\) 使
\(H(P_\infty\le2t)<\varepsilon\)。由

\[
\{P_Q<t\}\subset
\{P_\infty\le2t\}\cup\{|P_Q-P_\infty|>t\},
\]

再令 \(Q\) 充分大，\(L^2\) convergence 和 \(\mathcal T(Q)\to0\) 使后者测度与 \(C\mathcal T(Q)/t^2\) 都小于 \(\varepsilon\)。因此 MP-LT 成立。

这里不需要 explicit minimum，不需要 quantitative negative-log bound，也不需要 \(\mathcal T(Q)\) 的 stretched-exponential rate。参数顺序为：先固定 \(t\)，再让 \(Q\to\infty\)，最后允许 \(t\downarrow0\)。

## 4. MP-LT ⇒ finite primitive positivity

所有 profiles 的 mean 都是固定 \(m=15/32\)，所以 Markov 给

\[
b_Q(t)\ge1-\frac{m}{t}.
\tag{4}
\]

若一列 \(Q_j,t_j\) 使 MP-LT expression 趋于零，则由 (4)，最终 \(t_j<2m\)。于是

\[
\frac{C\mathcal T(Q_j)}{t_j^2}
\ge\frac{C\mathcal T(Q_j)}{4m^2}.
\]

每个 finite \(Q\) 的 tail 都严格正，因此必有 \(Q_j\to\infty\)。

若某个 finite \(Q_0\) 的 profile 在一个 residue 上为零，记其完整 zero-cylinder set 的 Haar mass 为 \(\alpha>0\)。Selector events 随 prime prefix 增大而递减，所以对全部 \(Q\ge Q_0\)，这个 cylinder 仍为 zero。于是任意 \(t>0\) 都有

\[
b_Q(t)\ge\alpha,
\]

与上述趋零 sequence 矛盾。故 MP-LT 排除每个 finite zero，完成 (E1)。

## 5. 合并后的准确状态

E1 原稿把 MP-LT 留作 stronger lower-tail hypothesis 的谨慎表述，在尚无 relative conditional \(L^2\) 输入时是合理的；新的 arithmetic unit-noise support theorem 补上了这个特定模型的缺口，因此可把其未解 gate 精确改写为：

> 对所有 finite \(Q\) 与所有 \(a\bmod32W_Q\)，corrected \(C32\) primitive profile \(P_Q(a)\) 严格为正。

这是一个 finite primitive covering 问题。找到 exact zero certificate 会否定该 E1 primitive gate；它不自动否定原 norm LP 或 A303656，因为 norm residual 允许 positive even inert valuations，而 primitive residual 把全部 divisible cells 排除。

若证明上述 finite positivity，则结合本 note 的 (E1) 和 E1 原来的 integer inequality (17)，可得到 actual almost-all；integer inequality 的 analytic proof仍是该最后一步的独立依赖。这里没有把 signed proxy 当成 nonnegative model，也没有证明 W6 的 unweighted SM。
