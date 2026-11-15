# PS02 → A2 Lemma 8 / Theorem 9 / Theorem 10：最小修正与独立审查

## 裁决和范围

**在本次逐式检查的链条中未发现逻辑缺口；应作 source / exposition corrections，不应 REJECT 主结论。** 下列文本给出正确的 source range、bounded-parameter 与 floor 修补，并把最容易隐藏统一性问题的计算写全。它只审查 smooth-order harmonic tail → uniform rough-conductor Romanoff bound → conditioned Parseval；不审查 A2 的其他附加命题，不证明 LP，也不代替整数 weighted transfer。

Primary source 为 Carl Pomerance–Igor E. Shparlinski, *Smooth Orders and Cryptographic Applications*, ANTS-V, LNCS 2369 (2002), 338–348：<https://math.dartmouth.edu/~carlp/PDF/paper128.pdf>。Theorem 3 在 printed p. 344；fixed integer base 扩展在 printed p. 346。原 PDF 已重读，并已用页面截图核对根号跨度。

## 一、可替换原引用的最小段落

固定整数 \(b\ge2\)，令

\[
 L_b(x,y)=\#\{p\le x:p\nmid b,\ P^+(\operatorname{ord}_p b)\le y\},
 \qquad u=\frac{\log x}{\log y}.
\]

Pomerance–Shparlinski Theorem 3（原文先写 \(b=2\)，printed p. 346 明确允许 fixed integer base）给出

\[
 L_b(x,y)\ll_b \frac{u\rho(u/2)}{\log(2u)}\pi(x),
 \qquad \exp\!\sqrt{\log x\,\log\log x}\le y\le x.
 \tag{PS}
\]

这里根号覆盖整个 \(\log x\,\log\log x\)。若本文仅在较窄的
\(y\ge\exp(\sqrt{\log x}\,\log\log x)\) 范围使用它，则这个使用仍然有效，但必须称为原定理的 corollary，不能把较窄范围误写成原文范围。所有 \(\ll_b\) 常数只依赖固定的 \(b\)。

固定 base 扩展的实质也可直接核对：若 \(\operatorname{ord}_p b=t\)，则这些不同 primes 的乘积整除 \(b^t-1\)，从而其个数为 \(O_b(t)\)。PS Theorem 3 proof 中唯一涉及 base 2 的 small-order counting 因此原样成立；其余使用的是 \(p-1\) 的 smooth divisor estimates。

## 二、源文 proof 的两处必要说明

### 2.1 Theorem 1 的 shell 截断

原 proof 定义 \(z_0=\exp((\log\log x)^2)\)，再用
\(\pi(x,y/e^i)-\pi(x,y/e^{i+1})\) 分段。所需上限是

\[
 i_0=\left\lfloor\log\frac{y}{z_0}\right\rfloor,
 \tag{F}
\]

不是 printed \(\lfloor\log z_0\rfloor\)。用 (F) 时每一段上端至少为 \(z_0\)，最后下端严格小于 \(z_0\)，故加上 \(\pi(x,z_0)\) 确实覆盖全部区间。积分上端随后可以放大到无穷，原估计不变。

求和转积分所用单调性只需在 \(u\ge2\) 证明。令 \(v=\log x/(\log y-t)\ge2\)，则

\[
 \frac{d}{dv}\{v^2\rho(v-1)\}
 =2v\rho(v-1)-\frac{v^2}{v-1}\rho(v-2)\le0,
\]

其中使用 \((v-1)\rho(v-1)\le\rho(v-2)\)。区间 \(1\le u\le2\) 直接用 \(\pi(x,y)\le\pi(x)\)；不把大参数 asymptotic 声称为 bounded \(u\) 的一致渐近式。

### 2.2 Theorem 3 的内部参数

先对 \(1\le u\le4\) 使用 trivial bound：连续正函数
\(u\rho(u/2)/\log(2u)\) 在此 compact interval 上有正下界。
在 \(u\ge4\)、\(y\) 充分大时，原文选择

\[
 w=\frac{\sqrt x}{\log y}
\]

满足 Theorem 2 的必要条件 \(y\le w\le x\)，因为
\(w/y=y^{u/2-1}/\log y\ge y/\log y>1\)。
写 \(L=\log y,r=u/2,\delta=\log L/L\)。原 range 给出
\(u\log(uL)\le L\)，故 \(u\le L\) 对充分大 \(y\) 成立。由 Dickman log-derivative 的标准一致上界，

\[
 \log\frac{\rho(r-\delta)}{\rho(r)}
 \ll\delta\log(r+1)
 \ll\frac{(\log L)^2}{L}=o(1).
\]

而 \(u\rho(u)\le\rho(u-1)\le\rho(u/2)\)，且 \(u/\log(2u)\ge1\)，故 Theorem 2 的附加项被主上界吸收。Small-order 项为
\(O_b(xL^{-2}\rho(u/2))\)，也被 (PS) 吸收。这里无需把源文的所有 \(\sim\) 符号逐字维持为 bounded-parameter asymptotics；所需 upper bound 在全部 stated range 成立。

## 三、uniform harmonic tail 的完整常数检查

目标为

\[
 M_b(y)=\sum_{\substack{p>y,\ p\nmid b\\P^+(\operatorname{ord}_p b)\le y}}\frac1p\ll_b1
 \qquad(y\ge2).
 \tag{H}
\]

### 3.1 Exact-order harmonic estimate

固定 \(t\ge2\)，把 order 恰为 \(t\) 的 primes 排为 \(p_1<\cdots<p_J\)。因为 \(p_j\equiv1\pmod t\)，所以 \(p_j\ge jt+1\)；又因 \(\prod_jp_j\mid b^t-1\)，所以
\(J\log(t+1)\le t\log b\)。因此

\[
 \sum_{\operatorname{ord}_p b=t}\frac1p
 \le\frac{1+\log(\max(1,J))}{t}
 \ll_b\frac{\log(2t)}t.
 \tag{E}
\]

\(t=1\) 只涉及 \(b-1\) 的有限 prime factors，可另吸收。

### 3.2 PS 的实际合法截断

对充分大的 \(y\)，令 \(L=\log y\) 和

\[
 X_0=y^{8\log\log y}=\exp(8L\log L).
\]

PS 的实际 range 在整个 \(y\le x\le X_0\) 成立，因为

\[
 \log X_0\log\log X_0
 =8L\log L\cdot\log(8L\log L)=o(L^2).
\]

因此 (PS)、\(\pi(x)\ll x/\log x\) 与 partial summation 给出

\[
 \sum_{\substack{y<p\le X_0\\P^+(\operatorname{ord}_p b)\le y}}\frac1p
 \ll_b1+\int_y^{X_0}\rho\!\left(\frac{\log t}{2L}\right)\frac{dt}{tL}
 \le O_b(1)+2\int_{1/2}^{\infty}\rho(v)\,dv
 \ll_b1.
\]

最后的积分有限，例如 \(n\rho(n)\le\rho(n-1)\) 递推给出 factorial decay。

### 3.3 \(p>X_0\) 的两段

若 \(\operatorname{ord}_p b=t\le\sqrt{X_0}\)，则 prime-product bound 给出这些 \(p>X_0\) 的个数至多 \(t\log b/\log X_0\)。不使用 smoothness 即得

\[
 \sum_{\substack{p>X_0\\\operatorname{ord}_p b\le\sqrt{X_0}}}\frac1p
 \le\frac{\log b}{X_0\log X_0}\sum_{t\le\sqrt{X_0}}t
 \ll_b\frac1{\log X_0}.
\]

其余使用 (E)，归结为

\[
 \sum_{\substack{t>\sqrt{X_0}\\P^+(t)\le y}}\frac{\log(2t)}t.
\]

取 \(\varepsilon=1/L,\sigma=1-\varepsilon\ge1/2\)，并令
\(Z_y(s)=\prod_{\ell\le y}(1-\ell^{-s})^{-1}\)。对 \(\sigma\le s\le1\)，

\[
 -\frac{d}{ds}\log Z_y(s)
 =\sum_{\ell\le y}\frac{\log\ell}{\ell^s-1}
 \ll\sum_{\ell\le y}\frac{\log\ell}{\ell}
 \ll L,
\]

因为 \(\ell^{1-s}\le e\) 且 \(1-\ell^{-s}\ge1-2^{-1/2}\)。用 \(Z_y(1)\ll L\)，在长度 \(1/L\) 的区间积分可得 \(Z_y(\sigma)\ll L\)，进而 \(-Z_y'(\sigma)\ll L^2\)。Rankin 因而给出

\[
 \sum_{\substack{t>\sqrt{X_0}\\P^+(t)\le y}}\frac{\log(2t)}t
 \le X_0^{-\varepsilon/2}
 \sum_{P^+(t)\le y}\frac{\log(2t)}{t^\sigma}
 \ll L^{-4}L^2=L^{-2}.
\]

这证明 (H) 对大 \(y\) 一致成立。Bounded \(y\) 只有有限多个 smooth-prime sets；各自有限 Euler product 在 \(s=1\) 的值和 derivative 均有限，再用 (E) 即可统一吸收。没有把 finite-range PS estimate 直接延伸至全部 \(p\)。

## 四、rough-conductor Romanoff bound：prime powers 与统一性

设 \(P\ge2\) 包含 \(b\) 的全部 prime factors，\(Q_P=\prod_{\ell\le P}\ell\)，\(r_P(t)\) 表示删去 \(t\) 中所有 \(\ell\le P\) 的 prime powers。定义

\[
 A_P(T)=\sum_{\substack{(d,Q_P)=1\\r_P(\operatorname{ord}_d b)\le T}}\frac1d,
 \qquad Y=\max(P,T).
\]

任何被计入的 \(d\) 都使 \(\operatorname{ord}_d b\) 为 \(Y\)-smooth；因 \(\operatorname{ord}_p b\mid\operatorname{ord}_d b\) 对每个 \(p\mid d\) 成立，

\[
 A_P(T)\le
 \prod_{\substack{p>P\\P^+(\operatorname{ord}_p b)\le Y}}(1-1/p)^{-1}
 \ll_b\max\left(1,\frac{\log T}{\log P}\right).
 \tag{R}
\]

解释：\(p>Y\) 的乘积由 (H) 一致有界；\(P<p\le Y\) 的乘积可放大到全部 primes，Mertens ratio 为 \(O(\log Y/\log P)\)。Euler product 允许每个 prime 的所有 powers，是合法的 majorant；它不要求这些 powers 的 orders 仍然合格，也没有忽略 squareful conductors。

由 Tonelli，包括 \(d=1,r_P(1)=1\) 在内，

\[
 \sum_{(d,Q_P)=1}\frac1{d\,r_P(\operatorname{ord}_d b)}
 =\int_1^{\infty}\frac{A_P(T)}{T^2}\,dT
 \ll_b1+\frac1{P\log P}.
\]

这里隐常数独立于 \(P,T\)。

## 五、接入 conditioned Parseval 时所需的精确 conditioning

取 \(P\ge5\)，固定 exponent Haar 的**全部** lower-primary coordinates
\(\theta=(\alpha_\ell,\beta_\ell)_{\ell\le P}\)，而非只固定有限 residues。对每个 \(P\)-rough conductor \(q\)，令 \(t=\operatorname{ord}_q5\)。条件下 \(\beta\bmod t\) 在固定 low-primary component 的 coset 中均匀，其 multiplicative orbit 大小恰为 \(r_P(t)\)。因此

\[
 \sum_{a\bmod q}|\widehat\sigma_{P,\theta}(a/q)|^2
 =\frac{q}{r_P(\operatorname{ord}_q5)}.
\]

对 primitive numerator 的 odd quadratic norm factor，Fourier coefficient 的模平方为 \(q^{-2}\)；丢去 base 3 factor 的模平方（至多 1），再把 primitive numerator sum 放大为 all numerators，得到

\[
 \|g_{P,\theta}\|_2^2
 \le\sum_{(q,Q_P)=1}\frac1{q\,r_P(\operatorname{ord}_q5)}
 \le C_0.
\]

\(C_0\) 与 \(P,\theta\) 无关。这正是 A2 后续 relative conditional \(L^2\) 所需的统一性。这里只核对 tail Fourier 段；从此到 finite-cylinder support identification 仍须另用已经审查的 exact likelihood mixing 和 local-constancy bridge，不能把这个 Parseval bound 单独称为 positivity proof。

## 审稿结论

最小必改项：正确书写 PS radical range；把 fixed-base extension 指向 printed p. 346；修正 Theorem 1 shell floor；对 bounded \(u\) 单独用 trivial bounds；补上 (X_0\) 合法性、Rankin derivative 与统一常数的短计算。修正后，**smooth-order harmonic tail → uniform rough-conductor Romanoff → conditioned Parseval** 这条链成立。此结论依赖已发表 PS theorem 的 sieve / smooth-number inputs，本次没有把这些深层经典 inputs 当作由有限实验证明。
