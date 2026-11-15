# E2 primitive unit-noise support theorem：独立交叉审查

## 裁决与适用范围

**独立复核后未发现 gap。** 在已经审查通过的 smooth-order harmonic tail lemma 前提下，A2 的 uniform relative conditional \(L^2\) 方法确实适用于下列 primitive unit-noise。对 E2 固定 canonical scheme，可把 quantitative target 精确归约为所有有限 canonical selector fractions 的 positivity：

\[
\boxed{\quad
\lim_{Y\to\infty}\Delta_Y
=H\!\left(\bigcup_{Y\ge5}\{a_Y=0\}\right).
\quad}
\tag{T}
\]

特别地，

\[
\boxed{\quad
\Delta_Y\longrightarrow0
\quad\Longleftrightarrow\quad
\text{每个有限 }Y\ge5\text{、每个 canonical residue }r
\text{ 都满足 }a_Y(r)>0.
\quad}
\tag{P}
\]

这没有证明右边的 arithmetic positivity，也没有把它与原 norm LP 等同。它与此前已证 \( \Delta_Y\to0\Rightarrow\mathrm{LP}\) 相容。本结论只针对固定 scales \(1,2,18\) 和固定按 \(x\bmod24\) 选择 scale 的 canonical rule；不能直接套给任意随 \(Y\) 改变的 branch scheme。

## 1. 噪声、joint shift law 与正确 normalization

令

\[
\tau=
H_{1+4\mathbb Z_2}
\otimes
\bigotimes_{p\ {\rm odd}}H_{\mathbb Z_p^\times},
\qquad
\rho_\lambda=\mu*(\lambda_*\tau),
\quad \lambda\in\{1,2,18\}.
\]

这里各 \(H_A\) 都是集合 \(A\) 上 normalized Haar；无限 product 是 probability measure，虽不必相对于整个 Haar 有 density。Joint \(\mu=(T_3+T_5)_*H^2\) 与 A2 完全相同，保留所有跨 prime correlations，own-base coordinates 保持 eventual value 0。

设 \(\mathcal F_P\) 为 output 中所有 \(p\le P\) 的完整 \(p\)-adic coordinates。取 \(P\ge5\)，并写

\[
V_P=\prod_{\substack{p\le P\\p\ {\rm odd}}}(1-1/p).
\]

有限-prefix noise 的 density 为

\[
K_{\lambda,P}(r)
=\frac{4\lambda}{V_P}
\mathbf1\!\left\{
r\in\lambda(1+4\widehat{\mathbb Z}),\
r/\lambda\in\mathbb Z_p^\times
\ \text{对所有 odd }p\le P
\right\}.
\tag{1}
\]

原因是第一条条件的 Haar mass 为 \(1/(4\lambda)\)，除法后的 odd unit conditions 再贡献 \(V_P\)。所有 \(\lambda\) 的 prime divisors 都已在 \(P\ge5\) 的 prefix 内。也可逐 prime 核对：在 odd \(p\mid\lambda\) 的 factor 为 \(p^{v_p(\lambda)}/(1-1/p)\)；在 2 的 factor 为 \(2^{v_2(\lambda)+2}\)。

因此有限-prefix output density 精确为

\[
G_{\lambda,P}(x)
=\int K_{\lambda,P}(x-s(e))\,de
=\frac{4\lambda}{V_P}\,a_{\lambda,P}(x).
\tag{2}
\]

该函数在 modulus \(4\lambda q_P\) 上 locally constant，其中 \(q_P\) 是 odd primorial。这一点直接来自 noise kernel，不需要重新证明 A2 对 norm-noise 所用的 local-constancy bridge。

## 2. 条件 tail Fourier estimate

固定全部 lower-primary exponent coordinates

\[
\theta=(\alpha_\ell,\beta_\ell)_{\ell\le P}.
\]

对于 \(p\le P\)，\(s_p(e)\) 完全由 \(\theta\) 确定：base 不等于 \(p\) 时，torsion order 整除 \(p-1\)，其 prime divisors 都不超过 \(P\)，principal-unit 部分只用 \(\ell=p\) 的 exponent coordinate；base 等于 \(p\) 时，eventual coordinate 是 0。特别地，own-base 3、5 不给 tail conditioning 添加边界项。

对于 \(p>P\)，\(\lambda\) 为 \(p\)-adic unit，所以 \(\lambda_*H_{\mathbb Z_p^\times}=H_{\mathbb Z_p^\times}\)。Unit noise 在 primitive conductor \(p^k\) 上的 Fourier coefficient 为

\[
\widehat\tau_p(a/p^k)=
\begin{cases}
-1/(p-1),&k=1,\\
0,&k\ge2,
\end{cases}
\qquad (a,p)=1.
\]

因此只有 odd squarefree \(P\)-rough conductors \(q\) 有非零 contribution，且 primitive coefficient 的模平方为 \(\phi(q)^{-2}\)。

令 \(t=\operatorname{ord}_q5\)，\(r_P(t)\) 为删除 \(t\) 中全部 \(\ell\le P\) prime powers 后的整数。给定 \(\theta\)，\(\beta\bmod t\) 的低 primary components 固定，余下 components Haar，因此 \(5^\beta\bmod q\) 在大小恰为 \(r_P(t)\) 的 multiplicative coset 上均匀。完整 Parseval 给出

\[
\sum_{a\bmod q}
|\widehat{\sigma}_{5,P,\theta}(a/q)|^2
=\frac{q}{r_P(\operatorname{ord}_q5)}.
\tag{3}
\]

条件下 \(\alpha,\beta\) 的剩余 coordinates 仍独立；丢去 base 3 coefficient 的模平方（至多 1），并把 primitive numerators 放大为所有 numerators，得到

\[
\|g_{\lambda,P,\theta}\|_2^2
\le
\sum_{\substack{q\ {\rm squarefree}\\(q,Q_P)=1}}
\frac{q}{\phi(q)^2\,r_P(\operatorname{ord}_q5)}.
\tag{4}
\]

包括 \(q=1\) 的常数项。下面说明该 bound 独立于 \(P,\theta,\lambda\)。

## 3. Modified rough-conductor Romanoff series

设

\[
A_P(T)=
\sum_{\substack{q\ {\rm squarefree},\ (q,Q_P)=1\\
r_P(\operatorname{ord}_q5)\le T}}
\frac{q}{\phi(q)^2},
\qquad Y=\max(P,T).
\]

每个被计入的 \(q\) 都使 \(\operatorname{ord}_q5\) 为 \(Y\)-smooth；故每个 \(p\mid q\) 都满足 \(\operatorname{ord}_p5\) 为 \(Y\)-smooth。因此

\[
A_P(T)
\le
\prod_{\substack{p>P\\P^+(\operatorname{ord}_p5)\le Y}}
\left(1+\frac{p}{(p-1)^2}\right).
\]

独立代数复算为

\[
1+\frac{p}{(p-1)^2}
=
(1-1/p)^{-1}
\left(1+\frac1{p(p-1)}\right).
\tag{5}
\]

第二个因子的全 prime product 绝对收敛，给出 uniform 常数。第一个 product 正是 A2 已审查的 rough-order Euler majorant：\(p>Y\) 的部分由
\(\sum_{p>Y,\ P^+(\operatorname{ord}_p5)\le Y}1/p\ll1\)
控制，\(P<p\le Y\) 的部分由 Mertens ratio 控制。于是

\[
A_P(T)\ll \max\left(1,\frac{\log T}{\log P}\right),
\]

从而 Tonelli 给出

\[
\sum_{\substack{q\ {\rm squarefree}\\(q,Q_P)=1}}
\frac{q}{\phi(q)^2\,r_P(\operatorname{ord}_q5)}
=\int_1^\infty\frac{A_P(T)}{T^2}\,dT
\ll1+\frac1{P\log P}\le C_0.
\tag{6}
\]

这里 \(C_0\) 不依赖 \(P,\theta,\lambda\)。从 finite quotients 取 \(L^2\) limit，即可得到所需 jointly measurable conditional tail densities；也可直接由 square-summable Fourier coefficients 构造后用 Fourier uniqueness 识别相应 measures。

## 4. Relative conditional \(L^2\) 与 finite extinction

Past likelihood 是

\[
k_{\lambda,P,\theta}(x_{\le P})
=\prod_{p\le P}
K_{\lambda,p}(x_p-s_p(\theta)).
\]

它非负、bounded、locally constant，且只依赖 \(\theta\)。给定 \(\theta\) 后，过去 noise 与未来 noise 独立。使用 (6) 的 uniform bound，对 exact likelihood mixture 作 weighted Cauchy–Schwarz，得到

\[
E_H[G_\lambda^2\mid\mathcal F_P]
\le C_0\,G_{\lambda,P}^2,
\qquad
G_{\lambda,P}=E_H[G_\lambda\mid\mathcal F_P].
\tag{7}
\]

这里 \(\rho_\lambda=G_\lambda H\) 且 \(G_\lambda\in L^2(H)\)。Existence 可先固定 \(P=5\)：过去 likelihood 有有限上界，(6) 控制未来 \(L^2\)，积分后即得全局 \(L^2\)；随后对全部 \(P\) 使用同一混合论证。

令 \(Z_\lambda=\{G_\lambda=0\}\)。在 \(G_{\lambda,P}>0\) 的位置，conditional Cauchy–Schwarz 给出

\[
H(G_\lambda>0\mid\mathcal F_P)\ge C_0^{-1}.
\]

而 \(E[1_{Z_\lambda}\mid\mathcal F_P]\to1_{Z_\lambda}\) a.e.。故在 \(Z_\lambda\) 上，不可能全部 \(G_{\lambda,P}\) 都正；反向由 conditional expectation 的非负性立即成立。因此

\[
\{G_\lambda=0\}
=\bigcup_{P\ge5}\{G_{\lambda,P}=0\}
=\bigcup_{P\ge5}\{a_{\lambda,P}=0\}
\quad\text{Haar-a.e.}
\tag{8}
\]

这一步没有把普通 nonnegative martingale convergence 当作 positivity theorem；统一的 relative bound (7) 是排除额外 infinite extinction 的必要输入。

## 5. Canonical patch 与 \(\Delta_Y\) 的极限

E2 的 canonical rule \(\lambda(x)\) 只依赖 \(x\bmod24\)，所以在所有 \(\mathcal F_P\), \(P\ge5\), 上可测。定义

\[
H_P(x)=G_{\lambda(x),P}(x),
\qquad
H_\infty(x)=G_{\lambda(x)}(x).
\]

这是同一 filtration 上的 nonnegative \(L^2\) martingale：
\(H_P=E[H_\infty\mid\mathcal F_P]\)。它不必 mean 1，但不影响论证。(7) 逐 canonical region 适用，故

\[
\{H_\infty=0\}
=\bigcup_{P\ge5}\{a_P=0\}
\quad\text{a.e.}
\tag{9}
\]

Equation (2) 给出

\[
a_Y(x)<Y^{-1/4}
\quad\Longleftrightarrow\quad
H_Y(x)<\frac{4\lambda(x)}{V_Y}Y^{-1/4}.
\tag{10}
\]

Mertens bound \(V_Y^{-1}\ll\log Y\) 与固定 \(\lambda\le18\) 说明右边 threshold 趋于 0。在 \(H_\infty>0\) 上，martingale convergence 使 (10) 最终不成立；在 \(H_\infty=0\) 上，(9) 给出某个 finite prefix 已经 exact zero。由于 selector events 随 \(Y\) 增加而递减，该零值之后一直保留，所以 (10) 最终成立。

Bounded convergence 证明 (T)。每个 \(a_Y\) 是 modulus \(72q_Y\) 上的非负 locally constant function；存在一个 zero residue 即有正 Haar mass。因此 union 的 Haar measure 为 0 当且仅当所有有限 canonical fractions 都 positive，证明 (P)。

## 6. 必须保留的 dependency 与边界

1. 这个 extension 依赖 A2 smooth-order harmonic tail 的已审查证明，不依赖 LP 或 POS。
2. 它把 E2 quantitative abundance 改写成新的 finite **primitive unit** positivity 问题；这是 finite norm LP 的充分条件，但两者尚未证明等价。
3. 先前 generic countermodel 不与本 theorem 矛盾：其 unit model 在 finite prime \(7\) 已有 zero cylinder，正好属于 (8) 的 finite extinction。
4. 结论不涉及整数 unweighted \(L^2\) transfer；没有证明 W6 的 SM。
5. E2 analytic engine 仍可给 actual almost-all，但其 arithmetic gate 现在可准确写成“所有 finite canonical unit selectors positive”；这项 gate 仍 OPEN。
6. 原背景的 A303656 每个整数可表示命题仍 UNRESOLVED；任何 eventual model 的 positivity 或 almost-all 都不是全整数结论。
