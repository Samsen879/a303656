# E2 canonical selector 与 LP / POS 的准确依赖

## 裁决

**E2 的 canonical \(\Delta_Y\to0\) 蕴含 LP。因此不能把它列为绕开 LP 的独立逻辑目标。** 它是更强、带 quantitative unit-avoidance 条件的充分入口。现有 A2 support theorem、LP / POS equivalence 或 W6 zero-set bridge 都未证明反向 implication；“LP ⇒ canonical \(\Delta_Y\to0\)” 对实际 \((3,5)\) family 仍未解决。这里只辨认 dependency，不另审 E2 全部 analytic engine。

**后续交叉审查更新：** A2 的方法可独立扩展到 primitive unit-noise，进一步证明 \(\Delta_Y\to0\) 等价于“所有有限 canonical \(a_Y(r)>0\)”。完整证明在同目录 e2_unit_noise_support_audit.md。此新归约没有把 unit positivity 与原 norm LP 等同，以下所有关于二者界限的结论仍保留。

依据是 E2 report 第五节和 §5.1（本地 e2_report.txt 的 282–353 行），canonical scales 为 \(\lambda=1,2,18\)，odd primorial 为 \(q_Y\)，共同 modulus 为 \(72q_Y\)。已同时阅读相关 analytic appendix；selector 的准确定义和本节结论以报告第五节为准。

## 1. 同一个 joint eventual measure 下的精确定义

令 \(e=(\alpha,\beta)\) 服从 \(\widehat{\mathbb Z}^2\) 上 Haar，\(s(e)=T_3(\alpha)+T_5(\beta)\)，其 pushforward 为共享背景中的 \(\mu\)。对 output \(x\in\widehat{\mathbb Z}\)，取 E2 指定的 canonical \(\lambda(x)\in\{1,2,18\}\)。定义

\[
A_{Y,x}=
\left\{e:
x-s(e)\in\lambda(x)(1+4\widehat{\mathbb Z}),\
z(e,x):=\frac{x-s(e)}{\lambda(x)}\in\mathbb Z_p^\times
\quad\hbox{对所有 odd }p\le Y
\right\},
\]

\[
a_Y(x)=H^2(A_{Y,x}).
\]

除法没有歧义：乘以非零整数 \(\lambda\) 在 \(\widehat{\mathbb Z}=\prod_p\mathbb Z_p\) 上是 injective；第一条件已保证可除。\(\lambda(1+4\widehat{\mathbb Z})\) 就是整数 congruence \(s\equiv x-\lambda\pmod{4\lambda}\)。第二条件正是整数商与 \(q_Y\) coprime 的条件。两者只依赖 \(s,x\pmod{4\lambda q_Y}\)，所以确实产生 E2 的有限-period rational fraction。

这里没有另换 exponent distribution。整数 \(c,d\) 的 growing rectangles 中，删除任何固定数目的 initial rows 后，其这些有限 congruences 的极限就是上述 joint eventual pushforward。Own-base 3 与 5 的坐标在 \(\mu\) 中本来分别按 eventual value 0 处理；不会出现额外 independent-prime 或 transient-row 假设。

## 2. Selector ⇒ finite norm support，包含任意 prime-power precision

固定 \(q\ge1\)，取 \(Y\ge P^+(q)\)。如果 \(e\in A_{Y,x}\)，则 \(r=x-s(e)=\lambda z\) 在每个 \(p\mid q\) 都是 \(\mathbb Z_p\) 中的 two-squares norm：

- \(p\equiv3\pmod4\)：\(z\) 为 unit；又因 \(\lambda\in S_2\)，\(v_p(\lambda)\) 为偶数。因此 \(v_p(r)=v_p(\lambda)\) 是偶数，且任意 unit 都是未分歧 quadratic norm。
- \(p=2\)：\(z\equiv1\pmod4\)，是 \(\mathbb Z_2[i]\) 的 norm；\(\lambda\in S_2\) 也是 norm，乘法封闭给出 \(r\) 是 norm。
- \(p\equiv1\pmod4\)：任意 \(r\in\mathbb Z_p\) 都是 two-squares norm。

因此对每一个 \(k\ge1\) 都有 \(\beta_{p^k}(r)>0\)，CRT 给出 \(\beta_q(r)>0\)。这是 exact valuation 论证，所以不要求 E2 的共同 branch modulus 含有 \(q\) 的全部 prime powers。

令

\[
m_q=\min\{\beta_q(t):t\in\mathbb Z/q\mathbb Z,\ \beta_q(t)>0\}>0.
\]

在同一个 \(\mu\) 下，逐点有

\[
f_q(x)=\pi\int\beta_q(x-s(e))\,de
\ge \pi m_q\,a_Y(x).
\tag{1}
\]

从而

\[
\{f_q=0\}\subseteq\{a_Y=0\}
\subseteq\{a_Y<Y^{-1/4}\}.
\tag{2}
\]

取 Haar measure 得

\[
\Delta_Y\ge H\{f_q=0\}\qquad(Y\ge P^+(q)).
\tag{3}
\]

若存在一个 finite zero \(f_q(a)=0\)，则 \(H\{f_q=0\}\ge1/q\)。故 canonical \(\Delta_Y\to0\) 排除每个 finite zero，即推出 LP。一般有限 branch abundance 版本亦如此：若正 fraction 的 selected branches 覆盖 Haar density 趋于 1，则 (1) 逐 branch 适用，也必排除所有 finite zero cylinders。

## 3. 为什么当前成果不能反向推出 E2 abundance

Finite norm positivity 允许 inert residual 的 positive even valuation；primitive selector 则要求除去固定 \(\lambda\) 后，在全部 \(p\le Y\) 都是 unit，还对 split primes 也施加 unit avoidance。两者的支持条件不同，且 E2 还要求具体 \(Y^{-1/4}\) 下界。

可以给出一个完全明确的 **generic measure countermodel**，说明反向 inference 不是 A2 / W6 所涉及的抽象 measure theory 后果。此模型不声称是实际 \(3^\alpha+5^\beta\) 的 \(\mu\)，也不是 A303656 counterexample。

取 inert prime \(p=7\)。令 shift law 在 \(p\)-component 为 \(p\mathbb Z_p\) 上的 normalized Haar，在其他 prime components 为完整 Haar。Two-squares convolution density 在其他 coordinates 为 1，在 \(p\)-coordinate 为

\[
F(x_p)=
\begin{cases}
1/p,&x_p\in p\mathbb Z_p,\\
1+1/p,&x_p\notin p\mathbb Z_p.
\end{cases}
\]

这个计算来自 \(B_p=(1+1/p)\mathbf1_{\{v_p\ {\rm even}\}}\)：在 \(p\mathbb Z_p\) 内，偶 valuation 的条件概率为 \(1/(p+1)\)。所以 \(F\) 有全局正下界，所有 finite norm densities positive，POS 成立，finite-zero support identification 也成立。

但 canonical \(\lambda=1,2,18\) 均与 \(p=7\) coprime。在 cylinder \(x_p\in p\mathbb Z_p\) 内，每个 shift 都使 \((x-s)/\lambda\) 被 \(p\) 整除。故 \(a_Y=0\) 对所有 \(Y\ge7\) 成立，\(\Delta_Y\ge1/7\)。这里 finite \(a_Y=0\) 与所有 finite norm \(f_q>0\) 明确共存。

**对实际 \((3,5)\) family：** E2 已检查的 \(Y=5,7,11,13\) 没有 zero selector branches，但全部 \(\Delta_Y=1\)；这些有限结果既不证明更大 \(Y\) 无零支，也不否定 asymptotic lower tail。当前材料没有提供实际 canonical zero-branch certificate，也没有证明 LP ⇒ canonical abundance。不能把上述 generic countermodel 误报为实际 exponent family 的反例。

W6 bridge 识别的是保留全部 admissible inert even valuations 的 norm-survivor zero set；它没有把 norm indicator 换成 unit indicator，因此不会填平这一步。

## 4. 对 triage 依赖图的修正

\[
\text{E2 canonical }\Delta_Y\to0
\ \Longrightarrow\ \mathrm{LP}
\ \overset{\mathrm{A2}}{\Longleftrightarrow}\ \mathrm{POS}
\ \overset{\mathrm{V}}{\Longrightarrow}\ \text{actual almost-all}.
\]

E2 自身的 analytic engine 另给 \(\Delta_Y\to0\Rightarrow\) actual almost-all；这是不同证明路径，但 arithmetic hypothesis 不是弱于 LP 的旁路。若保留 E2 为研究候选，应说明其目标为更强的 unit-selector lower tail，并把“证明实际 LP ⇒ abundance”或“构造 actual canonical zero-branch certificate”标为尚需实质新论证的界面，而不是已证的模型等价。
