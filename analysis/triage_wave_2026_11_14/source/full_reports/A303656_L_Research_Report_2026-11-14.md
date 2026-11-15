# A303656 — Lane L：文献深查与输入审计

研究日期：2026-11-14。实质研究起点：13:23:41 UTC；本稿冻结：2026-11-14 14:23:44 UTC。本轮实际经过 60 分 3 秒；期间进行了原始文献核对、独立证明、反例测试与证书复算，不以并行会话时长相加，也未用空等计时。

## 结论先行

**UNRESOLVED.** 没有找到 A303656 的证明，也没有找到无条件 almost-all 定理。下文不把正密度、几乎所有 short intervals 含有许多可表示整数、或 finite-level positivity 误写成几乎每个整数可表示。

**PROVED.** 本次独立完成了给定 R1-b 的审计：对原题规定的 H_X、Z_X、μ_q、β_q、f_q，以及 q_j=j!，有 f_{q_j}→f∞ in L²(Ẑ) 及 a.e.，∫f∞=π；而且对每个固定 j，

\[
\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}|Z_X(n)-f_{q_j}(n\bmod q_j)|^2
=\|f_\infty\|_2^2-\|f_{q_j}\|_2^2.
\]

这是对已有候选 R1-b 的完整证明补齐，不是新提出的猜想，也不宣称首创。关键补充是所有实际非零 shift differences 的共同乘积控制 composite-divisor tail；完整证明附于本报告后。

**PROVED.** 最值得立即传给其他路线的文献更新是 Assing–Humphries 2026：其 arXiv v1 Thm. 1.3 给出 r₂ shifted correlation 在 1≤h≤X 的统一误差 Oε(X^{87/128+ε})。R1-b 仅用 Chamizo 2022 已有 Oε(X^{17/23+ε}) 即可闭合，所以审计不依赖这项最新改进。

**PROVED.** (POS) 可精确改写为 density martingale 的条件 Hellinger 累积量沿 Haar-a.e. 路径有限；这个等价不需要 independence。其 arithmetic convergence 仍未解决。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 本题 f_q 不按互素模数 tensorize：f₄(1)/π=1，f₅(1)/π=21/20，但 f₂₀(1)/π=4/5。因此独立 Euler-product positivity 定理不能直接用于这个 f∞。

## 1. 记号、原始问题与书目更正

**UNRESOLVED.** 原问题仍为：每个 n>1 是否都有 n=a²+b²+3^c+5^d，a,b,c,d≥0。全文保留用户指定的 S2、D(n)、R(n)：R(n) 只计 exponent pairs，不计平方表示的不同符号或次序。

**PROVED.** OEIS A303656 计 a≤b 的完整四元组；用户的 R(n) 恰对应 [A303429](https://oeis.org/A303429)。两者的正性等价，数值本身不相同。Sun 原始正式出处是：Zhi-Wei Sun, *Restricted sums of four squares*, International Journal of Number Theory 15(9) (2019), 1863–1893, DOI [10.1142/S1793042119501045](https://doi.org/10.1142/S1793042119501045)，[arXiv:1701.05868v10](https://arxiv.org/abs/1701.05868v10)，Conj. 4.1(i)，PDF p.24。原文 N 明确定义为非负整数。

**FINITE COMPUTATION.** [A303656 原始条目](https://oeis.org/A303656)记录 Jiao-Min Lin 已验证 1<n≤2.4×10¹¹（Sun，2022-07-30 注）。用户提供的“另有连续 1.6×10⁹ 个整数”未在本次找到可独立核验的原始计算说明，因此不把它升级为本次已核的文献事实。

**PROVED.** 题目提供的 Elsholtz–Luca–Planitzer 线索存在错配。*Romanoff’s theorem and sums of two squares* 是 Artyom Radomskii 的 arXiv:2504.09954 初版标题；v7 改名 *Variants of Romanoff’s theorem*，作者不是 D. Radomskii。Christian Elsholtz, Florian Luca, Stefan Planitzer 的实际论文是 *Romanov type problems*, Ramanujan Journal 47 (2018), 267–289, DOI [10.1007/s11139-017-9972-8](https://doi.org/10.1007/s11139-017-9972-8)，[正式全文](https://link.springer.com/article/10.1007/s11139-017-9972-8)。其 Thm. 1–2 分别证明 p+2^{2^k}+m!（k,m≥0）及 p+2^{2^k}+2^q（k≥0，p,q primes）的正 lower density，不是题述二平方论文。

**UNRESOLVED.** Sun 本人的 [2018 MathOverflow 原帖](https://mathoverflow.net/questions/300832/does-every-integer-n1-have-the-form-a2b23c5d-with-a-b-c-d-nonnegat)也提出 S2+2^c+3^d 覆盖所有 n>1，以及 S2+2^c+5·2^d 覆盖所有 n>5。本次未找到这些精确形式的无条件证明；搜索中的 restricted-squares 文献常研究另一猜想 S2+(2^a3^b)^2+(2^c5^d)^2，不能据题名判定为 A303656 的 partial result。

## 2. 优先文献表：exact usable statements

“全文”指取得完整原文并核对下列 theorem 与相关证明段；不代表替作者完成整篇 proof verification。只读摘要的版本明确标为 **abstract only**。定理均用等价数学表述转述，不长篇逐字摘录。

| ID / 完整引用及链接 | 标签与可直接使用的陈述（含 hypotheses） | 可投递路线；具体接口与限制 |
|---|---|---|
| L1. Artyom Radomskii, *Variants of Romanoff’s theorem*, [arXiv:2504.09954v7](https://arxiv.org/html/2504.09954v7), 27 Aug 2026。全文。 | **PROVED.** Cor. 1.1：固定 a≥2；f∈Z[t]，degree d≥1，正首项、所有系数 gcd=1，f(N)⊂N。d≥2 时 #{n≤x:n∈S2+a^{f(N)}}≍_{a,f}x/(log x)^{1/2−1/d}；d=1 时存在 c₁>0，使充分大 x 至少 c₁x 个 n 有至少 c₁√log x 个 (s,m) 表示。 | A/B/E/V：half-dimensional Romanoff 基线；d=2 已达正密度，未达 almost-all。主 Thm. 1.1 的一般 collision hypothesis 可用于双指数 shifts；见附录。 |
| L2. Hao Pan, Wei Zhang, *On the integers of the form p²+b²+2ⁿ and b₁²+b₂²+2^{n²}*, Mathematics of Computation 80 (2011), 1849–1864, DOI [10.1090/S0025-5718-2011-02445-2](https://doi.org/10.1090/S0025-5718-2011-02445-2), [作者全文 v4](https://arxiv.org/pdf/0812.1259v4)。 | **PROVED.** Thm. 1.4 及 Thm. 4.1 的 proof：{b₁²+b₂²+2^{n²}:b₁,b₂,n≥0} 有正 lower density；同时存在 odd-modulus arithmetic progression 完全不含此类数。 | A/C/E：同一模型可同时有正密度与正密度例外；其 exponent-square 漏剩余类机制不可套给 unrestricted c,d。 |
| L3. Fernando Chamizo, *The Additive Problem for the Number of Representations as a Sum of Two Squares*, Mediterranean Journal of Mathematics 19 (2022), Article 44, 17 pp., DOI [10.1007/s00009-021-01959-3](https://doi.org/10.1007/s00009-021-01959-3)。[正式全文](https://link.springer.com/article/10.1007/s00009-021-01959-3)。 | **PROVED.** 对每个 ε>0，1≤h≤T，Σ_{1≤t≤T}r₂(t)r₂(t+h)=C(h)T+Oε(T^{17/23+ε})，统一于 h,T。C(h)=8·abs(2^{v₂(h)+1}−3)·σ(oddpart(h))/h。此统一简式是 Cor. 1.5 四段的推论；h=0 不在范围。 | A/B/V：R1-b 的已发表、足够强的输入；必须保留 2-adic 因子，非零 shifts 在本题均 even。 |
| L4. Edgar Assing, Peter Humphries, *Spectral Fourth Moments of Hecke–Maaß Cusp Forms*, Quarterly Journal of Mathematics, haag043, online 14 Oct 2026, DOI [10.1093/qmath/haag043](https://doi.org/10.1093/qmath/haag043)；[arXiv:2607.13518v1](https://arxiv.org/html/2607.13518v1), 15 Jul 2026。arXiv 全文；期刊版 **abstract only**。 | **PROVED.** v1 Thm. 1.3，θ=7/64：若 1≤h≤T，则 h^{-ε}E(T,h)≪ε T^{2/3} 当 h^{69/64}≤T；否则 ≪ε h^{23/128}T^{1/2}。故统一 E≪εT^{87/128+ε}。所需 spectral 输入由 Thm. 1.2 在固定 level/discriminant 的 Heegner points 上证明。 | A/B/E/V：最新误差升级。不能声称一般点的 spectral conjecture 已解决；v1 附带 mean-square 行有排版疑点，本报告完全不用该行。 |
| L5. Andrew Granville, K. Soundararajan, *A binary additive problem of Erdős and the order of 2 mod p²*, Ramanujan Journal 2 (1998), 283–298, DOI [10.1023/A:1009786614584](https://doi.org/10.1023/A:1009786614584)；[作者全文](https://dms.umontreal.ca/~andrew/PDF/wieferich.pdf)。 | **CONDITIONAL (所列 Wieferich counting hypothesis).** Thm. 2：若每个 x≥3 的 base-2 Wieferich prime 数 ≤2log x/(loglog x)²，则除 O(x/log x) 个外的 odd n≤x 都是 positive squarefree integer 加 2 的幂。 | C/P/E：local covering 与 almost-all 的经典桥梁；squarefree 的 summable p^{-2} tail 是关键，不能换成 S2 的 p^{-1} tail。 |
| L6. Yu-Chen Sun, Lilu Zhao, *The optimal scale in Linnik’s microsquare problem for almost all integers*, [arXiv:2609.13894v1](https://arxiv.org/abs/2609.13894v1), 12 Sep 2026, 26 pp。全文。 | **PROVED.** Thm. 6.2：almost all odd integers 是 squarefree positive integer 加 2^k，当且仅当不存在由 distinct odd primes p_i 的单个 classes a_i mod ord_{p_i²}(2) 组成的 finite cover of Z。另 Thm. 1.2：任意 Ψ(n)→∞，除 o(X) 个 admissible n≤X（4∤n，n≠7 mod8）外，n=x²+y²+z² 且 0<z<√log n·Ψ(n)。 | B/E/P：covering-free iff 的直接近邻。本文给出 fixed-w、先 X 后 w 的独立证明修补；其 signed-Hooley correlation 只陈述于 polylogarithmic shifts，不能直接换成 H_X 的 O(X) 差。 |
| L7. Yu. M. Kabanov, R. Sh. Liptser, A. N. Shiryaev, *On the question of absolute continuity and singularity of probability measures*, Math. USSR-Sbornik 33(2) (1977), 203–221, DOI [10.1070/SM1977v033n02ABEH002421](https://doi.org/10.1070/SM1977v033n02ABEH002421)；[原始全文入口](https://www.mathnet.ru/eng/sm3876)。 | **PROVED.** Thm. 1 在 locally equivalent 情形的 discrete formulation：P,Q 在各 F_j 上局部等价，F=σ(∪F_j)，Z_j=dQ_j/dP_j，h_j=E_P[(√(Z_{j+1}/Z_j)−1)²∣F_j]；Q≪P iff Σh_j<∞ Q-a.s.。交换两测度给反向 absolute continuity criterion。 | P/B：本题需要 Haar≪ν 的方向；本报告另给无 UI 前提的 pathwise martingale 证明，避免误换 P-a.s./Q-a.s.。 |
| L8. Emmanuel Kowalski, *Averages of Euler products, distribution of singular series and the ubiquity of Poisson distribution*, Acta Arithmetica 148(2) (2011), 153–187, DOI [10.4064/aa148-2-4](https://doi.org/10.4064/aa148-2-4)；[作者全文](https://people.math.ethz.ch/~kowalski/singular-series-distribution.pdf)。 | **PROVED.** 固定 integer k>1；各 p 上取独立 uniform k-tuples，ρ_p 是 occupied classes 数。Z=∏_p(1−ρ_p/p)(1−1/p)^{-k} a.s. 绝对收敛；P(Z>0)=∏_{p≤k}P(ρ_p<p)（Cor. 4.2、Example 4.3），因此条件于有限 admissibility 后 positive a.e.。证明用 Σ_pE∣local factor−1∣<∞。 | P/V：真正的 arithmetic Euler-product positivity 范例；本题共享 exponent periods，f₂₀ 的精确反例否定直接 tensorization。 |
| L9. François G. Dorais, Dominic Klyve, *A Wieferich Prime Search up to 6.7×10¹⁵*, Journal of Integer Sequences 14 (2011), Article 11.9.2, 14 pp；[正式全文](https://cs.uwaterloo.ca/journals/JIS/VOL14/Klyve/klyve3.pdf)。 | **FINITE COMPUTATION.** §4.1、§5 的完整 base-3/5/7 搜索界是 B=6469693230·150000=970453984500000。base 3：11,1006003。base 5 的 odd solutions 共六个，见§5名单。标题 6.7×10¹⁵ 是 base-2 范围，不是 base-5。 | C/P/V：替换 repo 的有界 inventory cutoff；只可作有限计算输入，不能由稀少推断不存在更多。 |
| L10. David J. Platt, Timothy S. Trudgian, *On the sum of two squares and at most two powers of 2*, American Mathematical Monthly 124(8) (2017), 737–740, DOI [10.4169/amer.math.monthly.124.8.737](https://doi.org/10.4169/amer.math.monthly.124.8.737)；[作者全文](https://arxiv.org/pdf/1610.01672v2)。 | **FINITE COMPUTATION.** Thm. 1 的最小性部分：535903 是 n>1 中不能写为二平方加至多两个 nonnegative powers of 2 的最小值。**PROVED NEGATIVE STRUCTURAL THEOREM.** 每个 2^α·1151121374334，α≥0，也不可表示；证明由 finite certificate 和缩放 lemma 组成。 | C/E/V：严格 counterexample mechanism；seed 与最小反例不同。缩放 lemma 要求 seed≡0 mod18，不能直接移植到两种奇底数。 |
| L11. Xiangyu Wang, *A Short Proof of a Theorem of Pan and Zhang*, [arXiv:2609.37508v2](https://arxiv.org/pdf/2609.37508v2), 12 Oct 2026, 6 pp。全文。 | **PROVED.** Lemma 2.2：A(T)=Σ_{d odd, ord_d(2)≤T}1/d≪log T（T≥2）；故固定 0<ε<1 时 Σ_{d odd}1/[d·ord_d(2)^{1−ε}]<∞。Thm. 1.1 重新证明 S2+{2^{c²}} 正 lower density。 | A/B/V：elementary common-product 方法；本报告独立推广到固定 g=5 及任意固定 logarithmic moment。此论文没有在 bibliography 中引用 Radomskii，不能列为 forward citation。 |
| L12. Paul Erdős, Paul Turán, *Über die Vereinfachung eines Landauschen Satzes*, Mitteil. Forsch.-Inst. Math. Mech. Univ. Tomsk 1 (1935), 144–147；[原始全文](https://www.renyi.hu/~p_erdos/1935-11.pdf)。 | **PROVED.** p.144 的未编号主定理：固定 δ>0，Σ_{d≥1,(d,a)=1}1/[d·ord_d(a)^δ]≪δ loglog a（a→∞）；因而每个固定 integer a≥2 的级数收敛。小 a 的表述应写1+loglog a 或单独处理，不能写负上界。 | A/B/P/V：Romanoff composite-order series 的经典源头；本报告不将无 log 权的收敛误报为2026新定理。 |

## 3. Pointwise 输入：精确作用域

| 完整来源与版本 | 标签、定理与 hypotheses | 接口 / GAP |
|---|---|---|
| Yann Bugeaud, Pietro Corvaja, Umberto Zannier, *An upper bound for the G.C.D. of aⁿ−1 and bⁿ−1*, Mathematische Zeitschrift 243 (2003), 79–84, DOI [10.1007/s00209-002-0449-z](https://doi.org/10.1007/s00209-002-0449-z)；[作者全文 PS](https://irma.math.unistra.fr/~bugeaud/travaux/pgcd1.ps)。 | **PROVED.** 固定 multiplicatively independent integers a,b≥2；每个 ε>0，充分大 n 有 gcd(aⁿ−1,bⁿ−1)<exp(εn)。阈值 ineffective。 | P/C：控制两幂差的共同 prime factors；不给 bad prime 的 residue class、odd valuation 或 moving residual 的 pointwise coverage。 |
| Pietro Corvaja, Umberto Zannier, *A lower bound for the height of a rational function at S-unit points*, Monatshefte für Mathematik 144(3) (2005), 203–224, DOI [10.1007/s00605-004-0273-0](https://doi.org/10.1007/s00605-004-0273-0)；[arXiv:math/0311030v2](https://arxiv.org/pdf/math/0311030v2)。全文。 | **PROVED.** 固定 finitely generated Γ⊂G_m²(Qbar)；沿 multiplicatively independent (u,v)∈Γ，max{h(u),h(v)}→∞ 时，h((u−1)/(v−1))∼h(1:u:v)。对固定有限 prime set S 的 integral S-units，任意 ε>0，除有限多个 independent pairs 外 gcd(u−1,v−1)<max{abs(u),abs(v)}^ε。 | P/C：可以分别取 u=3^h,v=5^k，不能只引用同 exponent 的 BCZ 后自行改变指数；仍是 ineffective、固定 Γ 的结论。 |
| Cameron L. Stewart, *On prime factors of terms of binary recurrence sequences*, Acta Arithmetica 209 (2023), 173–189, DOI [10.4064/aa220601-7-3](https://doi.org/10.4064/aa220601-7-3)；[arXiv:2206.01275](https://arxiv.org/pdf/2206.01275)。全文。 | **PROVED.** 固定 integer binary recurrence u_d=aα^d+bβ^d，distinct roots，abαβ≠0，α/β 非 root of unity。Thm. 2：除 density-zero 的 d 外，P(u_d)>d exp(log d/(104loglog d))。Thm. 1 在 a/b、α/β multiplicatively dependent 时给每个充分大 d 的 effective 版本。 | P：每个固定 A≠0 的 A−5^d 属此类，但 A=n−3^c 随问题变化，d≤log₅A 是初始窗口；没有所需 uniformity。 |
| Yuri Bilu, Sanoli Gun, Haojie Hong, *Uniform explicit Stewart theorem on prime factors of linear recurrences*, Acta Arithmetica 206 (2022), 223–243, DOI [10.4064/aa211116-13-11](https://doi.org/10.4064/aa211116-13-11)；[作者全文 v5](https://arxiv.org/pdf/2108.09857v5)，preprint title 中 Stewart 带 apostrophe。期刊版 **abstract only**，作者版全文。 | **PROVED.** Thm. 1.2：γ∈Q*，γ≠±1，n≥exp(10⁶)，存在 prime p 满足 v_p(γⁿ−1)≥1 且 p≥n exp(0.0005log n/loglog n)。 | P/V：uniform in rational γ 不等于 uniform in arbitrary moving A−5^d；γ=5/A^{1/d} 通常不再 rational。 |
| Jean Bourgain, *New bounds on exponential sums related to the Diffie–Hellman distributions*, C. R. Math. 338 (2004), 825–830, DOI [10.1016/j.crma.2004.03.027](https://doi.org/10.1016/j.crma.2004.03.027)；[正式全文](https://www.numdam.org/item/10.1016/j.crma.2004.03.027.pdf)。 | **PROVED.** Thm. 2.1：固定 δ>0 存在 δ′>0；p prime，θ∈F_p*，ord_pθ=t，p^δ<t₁≤t，则 max_{a≠0}∣Σ_{s=1}^{t₁}e_p(aθ^s)∣<t₁p^{−δ′}。 | E/P：确实包括 incomplete progressions。若 p=n^η，实际 exponent length O(log n) 不满足 fixed p^δ 下界；不能偷偷令 δ=δ(p)。 |

**PROVED.** 现代 complete-subgroup 文献不全要求 fixed p^δ：I. D. Shkredov, *Some remarks on the asymmetric sum-product phenomenon*, Moscow Journal of Combinatorics and Number Theory 8 (2019), 15–41，[原始全文](https://arxiv.org/pdf/1705.09703)，Cor. 16 给 log₂∣Γ∣≥C log₂p/log₂log₂p（固定 C>2）时 Fourier cancellation。该阈值仍远大于任意 fixed power of log p；不能把 full subgroup 当成长度 O(log n) 的 orbit prefix。

## 4. 2024–2026 的 forward citations 与相关 covering 更新

**PROVED.** 以下两篇的完整 reference list 均实际列出 arXiv:2504.09954；这是本次核实的 forward citations，不宣称检索穷尽。

| 完整引用 | 标签、精确结果 | 接口与边界 |
|---|---|---|
| Artyom Radomskii, *A Romanoff-type theorem for a multiset of products of powers*, [arXiv:2609.38207v1](https://arxiv.org/pdf/2609.38207v1), 23 Sep 2026, 7 pp。全文。 | **PROVED.** Thm. 1.2：固定 b₁,…,b_d≥2，u_i≥1，逐 exponent tuple 计重；至少 c₂x 个 n≤x 有 ≥c₁(log x)^{d−1} 个 n=p+∏b_i^{u_i} 表示，或 ≥c₁(log x)^{d−1/2} 个 n=s+∏b_i^{u_i} 表示（s∈S2）。无需 bases multiplicatively independent 或 coprime。 | A/B/V：处理 multiplicity 的正式模型；是 product shifts，不是 3^c+5^d，不能仅改符号套用。 |
| Artyom Radomskii, *Additive complements to the primes and large gaps between Romanoff numbers*, [arXiv:2610.14127v3](https://arxiv.org/pdf/2610.14127v3), 1 Nov 2026, 32 pp。全文。 | **PROVED.** 存在绝对 c*,X*：任意 B⊂Z≥0，X≥X*，若 H=⌊c*log X·loglog X/(B(X)+1)⌋≥1，则 [X/2,X] 内有 H 个连续整数不在 primes+B。故 eventual additive complement 必须 B(X)≫log X loglog X。 | C/E：定理联结的 gap threshold；本题双指数 B(X)≍log²X 使显示的 H 最终为0，而且目标集不是 primes，不能声称产生 A303656 反例。 |

**PROVED.** Granville–Pappalardi, *Two dimensional covering systems and possible prime producing a^m−b^n*, [arXiv:2601.10296v2](https://arxiv.org/pdf/2601.10296v2), 11 Apr 2026（全文），Prop. 3：p∤ab 时 a^m≡b^n modp 的指数集合是一个 homogeneous cocyclic lattice。令 r=ord_pa，s=ord_pb，L=lcm(r,s)，可写 mv≡nu modL，u=L/s，gcd(v,L)=L/r。Cor. 1 将 finite prime divisibility covering 等价于这些 lattices 覆盖 Z²。可投递 C/P；原题 n−3^c−5^d 的 inhomogeneous masks 一般不是 subgroups。

**PROVED.** J. E. Cremona, P. Koymans, *Lattice coverings and homogeneous covering congruences*, [arXiv:2601.03212v3](https://arxiv.org/html/2601.03212v3), 12 Oct 2026（全文），Thm. B/6.8：有限个 finite-index sublattices 构成 Z² 的 irredundant cover，若其 indices 的 lcm=∏_{i=1}^t p_i^{e_i}，则 lattice 数≥1+t+Σ_i e_i(p_i−1)。可投递 C；不能把拆出的 residue classes 数当作 original nonregular rows 数。

**PROVED.** Xiangjun Dai, Huixi Li, Junfeng Li, Shaoyun Yi, *On the moduli of distinct covering systems*, [arXiv:2611.15110v1](https://arxiv.org/html/2611.15110v1), 11 Nov 2026（全文），Thm. 1.1–1.3：finite cover of Z by a_i mod d_i，所有 d_i>1 且 pairwise distinct；若全 odd，则 45∣lcm(d_i)，且 min d_i≤9；一般 distinct cover 有 min d_i<14000，全 squarefree 则 min d_i≤7。可投递 C；其一般 convex-comparison lemma 可保留 multiplicity weights，但这些数值结论本身要求 distinct moduli。C=1 valuation shell 拆分会重复 modulus，因此不能直接转移常数。

## 5. Wieferich inventory 与 C=1 条件推论

**FINITE COMPUTATION.** Dorais–Klyve 的 B 范围内 odd base-5 Wieferich primes 为

20771, 40487, 53471161, 1645333507, 6692367337, 188748146801。

其中 3 mod4 的只有 20771、40487、1645333507，均小于 2×10⁹。论文 §4.1 给总数六，Table 6 只列后四个较大值；完整名单与 Amir Akbary, Sahar Siavashi, *The Largest Known Wieferich Numbers*, INTEGERS 18 (2018), A3，[全文 Table 1](https://math.colgate.edu/~integers/s3/s3.pdf) 交叉核对。本次对六个值及两个 base-3 值独立做 primality、exact order、mod q²/q³ 检查，没有重新扫描到 B。

**PROVED.** 对 odd prime q≠5，t=ord_q(5)，因为 (q−1)/t prime-to-q，LTE 给

\[
v_q(5^t-1)=v_q(5^{q-1}-1).
\]

所以 repo 的 nonregular 条件 s_q≥2 与 usual base-5 Wieferich 完全一致。

**CONDITIONAL (接受 [pinned repo Cor. 9.1](https://github.com/Samsen879/a303656/blob/ba7f028bb7bad69885e34549969059c00487380b/analysis/c1_order_dag_phase_c/THEOREMS.md) 的 formal-class theorem，以及发表的完整有限 inventory).** 对 repo `ba7f028` 所界定的 complete finite admitted original-row C=1 certificates，至少七个 original nonregular primes q≡3 mod4 必须满足

\[
q>970453984500000.
\]

这只是把原 cutoff 2×10⁹ 用已发表 inventory 提升；不重证 repo 的 order-DAG theorem，不排除全部有限 certificates，不提高“至少七个”的个数。

**UNRESOLVED.** 截至本次检索，[Richard Fischer 的实时原表](https://www.fermatquotient.com/FermatQuotienten/FermQ_Sort.txt)在 base 3、5 项标为 >1.2×10¹⁵。存档显示该标记至少在2020年底已出现，但未找到其完整区间覆盖及算法日志。因此本报告将它列为目前可见的更新声明，不把它当作已独立审计的 exhaustive bound，也不把旧 B 冒充全球最新纪录。

## 6. (POS) 的精确剩余问题

**PROVED.** μ_q 的 compatible distributions 定义 μ on Ẑ。令 η 为两个 independent Haar variables 的平方和之 law，ν=μ*η。其 cylinder density 为 f_q/π。上述 L² 结果表明 ν=(f∞/π)·Haar；(POS) 正好要求反向 Haar≪ν。

**PROVED.** 若某 finite f_q 在一个 residue class 上为0，则 (POS) 立即失败。否则所有 f_{j!}>0。定义

\[
h_j(a)=2-\frac{2}{j+1}\sum_{t=0}^{j}
\sqrt{\frac{f_{(j+1)!}(a+t j!)}{f_{j!}(a)}}.
\]

则

\[
f_\infty(x)>0\ \text{Haar-a.e.}
\quad\Longleftrightarrow\quad
\sum_{j\ge1}h_j(x\bmod j!)<\infty\ \text{Haar-a.e.}
\]

**UNRESOLVED.** GAP：还没有证明 composite finite levels 全正，以及上述 Hellinger series 的 Haar-a.e. 收敛。L² boundedness 只给绝对连续性的一侧。不能用每级均值π或每个 prime-power marginal 都正替代这个问题。

**PROVED.** 单独 prime powers 甚至有 sharp uniform lower bound f_{p^k}/π≥4/5。特别

\[
f_{2^k}/\pi=1,\quad
f_{3^k}(a)/\pi=\begin{cases}4/3&3\mid a\\5/6&3\nmid a,\end{cases}\quad
f_{5^k}(a)/\pi=\begin{cases}4/5&5\mid a\\21/20&5\nmid a.\end{cases}
\]

**PROVED NEGATIVE STRUCTURAL THEOREM.** 模20的 eventual shifts 均匀分布于 {6,8,12,14}；β₄=(1,2,1,0)，β₅(0)=9/5，其余=4/5。直接卷积得 f₂₀(1)/π=4/5，而 (f₄(1)/π)(f₅(1)/π)=21/20。跨 prime 的 exponent-period compatibility 是实质问题。

**PROVED.** Base primes 的一整块也可完全控制：对 k≥3、u,v≥1，f_{2^k3^u5^v}(a)=f_{120}(a mod120)，并且≥(4/15)π。证明条件于 c mod4、d mod2，再用剩余 exponent-period components 的 CRT independence，见完整 stabilization 附录。这不是一般 composite tensorization。

**FINITE COMPUTATION.** Exact Fraction certificate 给 min_a f_{120}(a)/π=7/15，四个 minimizers 是50、70、80、100；七个选定模数的独立 norm-count / eventual-cycle 算法与公式逐项一致。

**PROVED.** 更精确的无条件 reduction 是

\[
\limsup_{X\to\infty}\frac{\#\{n\in[X,2X]:R(n)=0\}}X
\le \operatorname{Haar}\{f_\infty=0\}.
\]

证明：R(n)=0⇒Z_X(n)=0。固定 ε>0、j，按 f_{j!}<ε 与其补集分割；后者占比由 squared error/ε² 控制。先 X→∞，再 j→∞。用 Haar{f_{j!}<ε}≤Haar{f∞≤2ε}+Haar{|f_{j!}−f∞|≥ε} 消除 sublevel-set 边界问题，最后 ε↓0。整个证明只在整数上评价 fixed f_q；从不在 Haar-null 的整数集上评价 f∞ 的 a.e. 版本。

**CONDITIONAL ((POS)).** 上式立即给 #{n∈[X,2X]:R(n)=0}=o(X)。未断言 (POS) 是整数 almost-all 的必要条件。

## 7. 为什么 squarefree 的 covering-free 定理能做，而现有 S2 转移还不能做

**PROVED.** 对 F={x∈Ẑ:p²∤x 对所有 p}，任何 shift law μ，若每个 finite prime set T、每个 a mod ∏_{p∈T}p² 都有正 μ-mass 的 shifts 避开这些 p²，则 g(x)=∫1_F(x−s)dμ(s)>0 Haar-a.e.。固定 T、condition 到 class a 并把 good shifts 的 μ 归一化，剩余 tail 的 conditional mean 为 ρ_T=∏_{p∉T}(1−p^{-2})。由于 tail-survival∈[0,1]，其为0的概率≤1−ρ_T；对 classes 求和，再 T↑全部 primes，得到0。这不需要 μ 的 prime independence。

**UNRESOLVED.** 对 S2，odd valuation 的 local bad mass 是 1/(p+1)，p≡3 mod4；尾和发散，任一无限 tail 的生存 Haar mass 为0，上述证明失效。Sun–Zhao 的 equivalent finite-cover criterion 因而不能直接解决本题 (POS)。这里精确缺少的是 tail estimate，不是一个没有说明的“局部到整体原则”。

## 8. 有限核验与排除的误用

**PROVED NEGATIVE STRUCTURAL THEOREM.** 一个无需计算的单底数对照：每个 n≡15 mod441 都不在 S2+{3^c:c≥0}。c=0 时 n−1≡14 mod49，有 v₇=1；c=1 时 n−3≡3 mod9，有 v₃=1；c≥2 时 n−3^c≡6 mod9，仍有 v₃=1。负 residual 当然也不在 S2。此处只构造近邻模型的反例，不涉及原来的 3^c+5^d。

**FINITE COMPUTATION.** 精确 Fraction 计算核对了23个选定 moduli 的 f_q，全部均值为π，112个 divisor projections 一致；q≤720 的 norm counts 分别由直接枚举(u,v)及 prime-power公式+CRT得到一致结果。另一个独立脚本核对36个 moduli、4210个 h-residues 的 local kernel。代码没有把有限正性外推成 (POS)。

**FINITE COMPUTATION.** Platt–Trudgian 大 seed 的858个必要 residuals 均有明确 prime≡3mod4 的 odd-valuation certificate；Pan–Zhang 的 exponent cover、prime orders 与递归 primality certificates 也做了有限核对。这些用于检验文献 mechanism，不是新的 A303656 range search。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 单个 power 的 weighted L² 对照保留不可忽略的 diagonal：若 H_X^(2)={c≥0:2^c≤X/2}，Z_X^(2) 及 f_q^(2) 按相同方式定义，则

\[
\lim_{j\to\infty}\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}
|Z_X^{(2)}(n)-f_{j!}^{(2)}(n)|^2=4\log2.
\]

完整证明见附录：Borwein–Choi 的 Σ_{t≤X}r₂(t)²=4XlogX+O(X) 给 diagonal 常数；共同乘积 tail 控制 offdiagonal。它不否定两指数 R1-b，因为本题 |H_X|≍log²X，diagonal 恰好消失。结论限定为先固定 periodic predictor 再令 X→∞，不排除 modulus 与 X 共同增长。

**PROVED.** Google DeepMind formal-conjectures 中 A303656 issue 的“closed”表示 formal statement 已加入；当前 theorem 被标 research open，proof 为 `sorry`。它不是猜想已解决的证据。

**UNRESOLVED.** 未找到可直接给 moving A=n−3^c、d≤log₅A 的 Stewart-type uniform theorem；也未找到可以对原来的 logarithmic exponent windows、任意相关 p 自动给 fixed power saving 的已核 theorem。文献缺口陈述仅限本次搜索覆盖，不是“不存在这类定理”的证明。

## 9. 与已关闭路线的关系、推荐下一步

**PROVED.** 本报告没有逃过 N-001：weighted L² 仍不提供 adversarial L∞。也没有逃过 N-009：finite/profinite consistency 不选出一个固定 exponent pair。R1-b 审计使用 n-average correlation，未重提 N-010 已关闭的 pointwise minor-arc 路线；没有从 averaged theorem 推出每个 n 的 R(n)>0。

**UNRESOLVED.** 最值得下一会话首先审查的是：用附录的 exact norm identity 独立复核 R1-b；然后直接研究 Hellinger series 的 unweighted pathwise convergence，或给出 f∞ 的 arithmetic zero set。单 prime positivity、uniform positive moments、及假想 Euler product 均不能替代此目标。

## 附录索引

- 附录 A：R1-b 完整证明。
- 附录 B：Romanoff logarithmic-moment lemma。
- 附录 C：Shifted correlation 的原文与版本审计。
- 附录 D：Radomskii 一般定理的完整 hypotheses。
- 附录 E：Hellinger、prime powers、squarefree covering。
- 附录 F：Base-prime block 的精确 stabilization。
- 附录 G：Single-power negative comparator。
- 附录 H：Multiplicative chaos 与 Kesten–Stigum。
- 附录 I：Direct profinite literature screening。
- 附录 J：版本与 counterexample audit。

可重放脚本、有限核验输出和 certificates 另见配套 ZIP 中的 README。



---

# 附录 A：R1-b 完整证明

此稿审计给定 R1-b，不声称 A303656、POS 或 almost-all 已无条件解决。主文只需 Chamizo2022 的 uniform correlation；2026 Assing–Humphries 可升级误差，并非逻辑必要条件。

## 0. 记号与结论

**PROVED.** 固定

\[
H_X=\{(c,d)\in\mathbb Z_{\ge0}^2:3^c+5^d\le X/2\},\quad M_X=|H_X|,
\quad s_{(c,d)}=3^c+5^d,
\]

\[
Z_X(n)=M_X^{-1}\sum_{i\in H_X}r_2(n-s_i),\quad X\le n\le2X,
\]

其中r_2(t)=#{(a,b)∈Z²:a²+b²=t}。令μ_q为s_i modulo q的极限分布，β_q(a)=q^(−1)#{(u,v) modq:u²+v²≡a}，

\[
f_q(a)=\pi\sum_{b\bmod q}\mu_q(b)\beta_q(a-b),\qquad q_j=j!.
\]

则存在非负 f∞∈L²(Ẑ,Haar)，f_{q_j}→f∞ in L²及a.e.，且∫f∞dHaar=π。更精确地，对每个固定j，

\[
\boxed{\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}
|Z_X(n)-f_{q_j}(n\bmod q_j)|^2
=\|f_\infty\|_2^2-\|f_{q_j}\|_2^2.}
\]

因此给定R1-b的 double limit 等于0。下面分别证明每个环节。

**UNRESOLVED.** 本结论不包含Haar{f∞=0}=0。POS仍需另外证明；POS是通向almost-all的充分条件，此稿不声称必要性。有限模数上某f_q为0，也不自动说明整数问题有正密度反例：不进入极限exponent occupation measure的边界指数仍可能提供表示。

## 1. 三角域、极限shift分布与碰撞

**PROVED.** 设C=⌊log_3(X/2)⌋+1、D=⌊log_5(X/2)⌋+1。H_X包含3^c≤X/4、5^d≤X/4的内矩形，并包含于[0,C−1]×[0,D−1]。每个方向从X/2改为X/4仅删O(1)个指数，故

\[
M_X=CD+O(C+D)\asymp(\log X)^2.
\]

对固定q，3^c、5^d modulo q分别eventually periodic（先剥离与base不互素的prime-power部分，再用multiplicative order）。矩形的经验分布因此收敛，H_X与矩形O(logX)的差不改变极限。μ_q存在，且q|q′时μ_q是μ_q′的pushforward。由profinite projective compatibility得到Ẑ上的概率测度μ，其modq边缘为μ_q。

**PROVED.** 零差不能仅按i=j计数，但有不依赖S-unit theorem的初等上界。若非平凡

\[
3^c+5^d=3^{c'}+5^{d'},\qquad c<c',
\]

则d>d′。令h=c′−c、k=d−d′，有

\[
3^c(3^h-1)=5^{d'}(5^k-1).
\]

由LTE，

\[
c=v_3(5^k-1)\le1+\log_3D,\qquad
 d'=v_5(3^h-1)\le1+\log_5C.
\]

这里k odd时第一valuation为0，k even时为1+v_3(k)；4∤h时第二为0，4|h时为1+v_5(h)。选(c,c′,d′)后等式确定5^d，故d至多一个。因此非平凡ordered collisions为

\[
O(C(1+\log C)(1+\log D))
=O(\log X(\log\log X)^2)=o(M_X).
\]

所以K_X=#{(i,j)∈H_X²:s_i=s_j}=M_X+o(M_X)。该估计由pointwise子审查独立提出并交叉核验。

## 2. 共同乘积消除finite-X divisor remainder

**PROVED.** 对q≥1，令

\[
W_X(q)=M_X^{-2}\#\{(i,j)\in H_X^2:s_i\ne s_j,\ q\mid(s_i-s_j)\}.
\]

若(q,5)=1，固定c,c′,d后，5^{d′}≡5^d+3^c−3^{c′} modq 的d′∈[0,D−1]至多D/ord_q(5)+1个（target不在5生成的循环子群时无解）。因此

\[
W_X(q)\ll\frac1{\operatorname{ord}_q(5)}+\frac1D,
\]

常数与X,q无关；例如X≥16时内矩形粗界M_X≥CD/16可给常数256。计数上界允许把zero differences加回来；W_X及以下乘积本身均排除它们。

**PROVED.** 定义整数

\[
Q_X=\prod_{\substack{i,j\in H_X\\s_i\ne s_j}}|s_i-s_j|,
\]

空积取1。每个差绝对值≤X/2，故logQ_X≪M_X²logX≪(logX)^5。只要W_X(q)>0就有q|Q_X，因而

\[
\sum_{q:W_X(q)>0}\frac1q
\le\frac{\sigma(Q_X)}{Q_X}\ll\log\log X.
\]

由此对Y≥2，

\[
T_X^{(5)}(Y):=\sum_{\substack{q>Y\\(q,10)=1}}\frac{W_X(q)}q
\ll\sum_{\substack{q>Y\\(q,5)=1}}\frac1{q\operatorname{ord}_q(5)}
+\frac{\log\log X}{\log X}.
\]

此处关键是只对实际出现的divisors求和，不能粗换成所有q≤X；后一粗界给O(1)而不是o(1)。

**PROVED.** Romanoff log-moment审计稿已证明，对每个固定k≥1，Σ_{(q,5)=1}(logq)^k/[q ord_q(5)]<∞。所以

\[
T_X^{(5)}(Y)\ll_k(\log Y)^{-k}+\frac{\log\log X}{\log X}.
\]

只用Wang2026 Lemma2.2的无log权重收敛亦足够得到先X→∞再Y→∞的tail消失。取Y=0并单独加q=1，可得Σ_{(q,10)=1}W_X(q)/q≪1，对X一致。

**PROVED.** 任意odd divisor t=5^bq，(q,10)=1，且W_X(5^bq)≤W_X(q)。置B=⌊(logY)/(2log5)⌋。b≤B且t>Y时q>√Y；b>B时geometric sumΣ5^(−b)≪Y^(−1/2)。因此

\[
\boxed{F_X(Y):=\sum_{\substack{t>Y\\t\text{ odd}}}\frac{W_X(t)}t
\ll_k(\log Y)^{-k}+\frac{\log\log X}{\log X}+Y^{-1/2}.}
\]

这对X≥16,Y≥4统一成立。q含3的幂完全允许，因为5仍是mod3^a的unit；5的幂已用几何尾处理，整个证明不需切换另一base。

## 3. Exact finite local kernels

**PROVED.** 定义

\[
\Gamma_q(h)=\frac1q\sum_{a\bmod q}\beta_q(a)\beta_q(a+h).
\]

它对互素模数multiplicative。对odd prime p和a≥1，

\[
\Gamma_{p^a}(h)=1+\sum_{j=1}^a p^{-2j}c_{p^j}(h)
=(1-p^{-2})\sum_{j=0}^{a-1}p^{-j}\mathbf1_{p^j\mid h}
+p^{-a}\mathbf1_{p^a\mid h}.
\]

对2的幂，

\[
\Gamma_{2^a}(h)=1+\sum_{j=2}^a2^{2-2j}c_{2^j}(h),\quad 0\le\Gamma_{2^a}(h)\le2.
\]

此处c_q(h)为Ramanujan sum。证明：β_q的normalized Fourier coefficient为q^(−2)G_q(t)^2，其中G_q(t)=Σ_{x modq}e(tx²/q)；Parseval给Γ_q=Σ_t|q^(−2)G_q(t)^2|²e(th/q)。odd modulus时改变变量(x,y)→(x−y,x+y)证明primitive Gauss sum |G_{p^j}(t)|²=p^j。2-power时

\[
|G_{2^j}(t)|^2=2^j\sum_{h:\,2h\equiv0\bmod2^j}e(th^2/2^j)
\]

等于0(j=1,t odd)或2^(j+1)(j≥2,t odd)。按frequency的primitive denominator分组即得公式。

**PROVED.** 当a→∞时，2-adic kernel一致收敛至

\[
b_2(h)=\begin{cases}1,&v_2(h)=0,\\2-3\cdot2^{-v_2(h)},&1\le v_2(h)<\infty,\\2,&h=0\text{ in }\mathbb Z_2.\end{cases}
\]

并且1/2≤b_2≤2、|Γ_{2^a}−b_2|≤2^(1−a)。

## 4. L² martingale无需Chamizo

**PROVED.** 由μ的compatibility及β_{q′}按q的cosets平均等于β_q，q|q′时E_Haar(f_{q′}|modq)=f_q。因此f_{j!}是非负martingale，且∫f_q=π。

**PROVED.** 若U,V独立分布为μ，固定(r,5)=1。由§1的矩形极限，μ_r=ν_{3,r}*ν_{5,r}，其中ν_{3,r}是3^c的eventual-cycle分布，ν_{5,r}是在5生成的、长度ord_r(5)的循环子群上的均匀分布。取相互独立的A,A′∼ν_{3,r}、B,B′∼ν_{5,r}；给定A,A′,B后，A+B=A′+B′至多指定一个B′值。因此

\[
\Pr(U\equiv V\pmod r)\le\frac1{\operatorname{ord}_r(5)}.
\]

对r=1仍按ord_1=1理解。任意odd d=5^br，则P(d|U−V)≤P(r|U−V)。因此

\[
\mathbb E_{\mu\times\mu}\sum_{d\text{ odd}}\frac{\mathbf1_{d\mid(U-V)}}d
\le\frac54\sum_{(r,10)=1}\frac1{r\operatorname{ord}_r(5)}<\infty.
\]

**PROVED.** Exact norm identity是

\[
\|f_q\|_2^2=\pi^2\mathbb E_{\mu\times\mu}\Gamma_q(U-V).
\]

positive local expansion给Γ_q(h)≤2Σ_{d|q, d odd}1_{d|h}/d，故norms一致有界。L² martingale convergence theorem推出f_{j!}→f∞ in L²及a.e.，均值π。

**PROVED.** 还可以精确识别norm limit。将odd q-part的kernel写成

\[
\Gamma_{q_{\rm odd}}(h)=\sum_{\substack{d\mid q\\d\text{ odd}}}
\frac{w_q(d)}d\mathbf1_{d\mid h},\quad0\le w_q(d)\le1.
\]

这里w_q(d)是所有满足v_p(d)<v_p(q)的odd p|q的(1−p^(−2))之积。对固定odd d，q=j!足够大时d|q，且

\[
w_{j!}(d)\longrightarrow\prod_{p\text{ odd}}(1-p^{-2})=8/\pi^2.
\]

用前段可积majorant 2Σodd d^(−1)1_{d|h}，先对countable divisor sum再对μ×μ用dominated convergence，得

\[
\boxed{\|f_\infty\|_2^2=8\mathbb E_{\mu\times\mu}
\left[b_2(U-V)\sum_{d\text{ odd}}\frac{\mathbf1_{d\mid(U-V)}}d\right].}
\]

所有prime powers及d的极限均由显式可积majorant控制，不要求uniform in q的lattice-point estimate。

## 5. Chamizo correlation在本窗口适用

**PROVED.** 对h>0，Chamizo2022正式发表版Corollary1.5给

\[
\sum_{1\le t\le T}r_2(t)r_2(t+h)=C(h)T+O_\epsilon(T^{17/23+\epsilon})\quad(1\le h\le T),
\]

constant独立于h,T，且

\[
C(h)=8b_2(h)\sum_{\substack{d\mid h\\d\text{ odd}}}\frac1d.
\]

若u>v是H_X两个不同数值shift，h=u−v，A=ceilX−u−1，B=floor2X−u，则A−h=ceilX−2u+v−1≥1，A≥X/2−1，B≤2X。故两个端点均h≤T，得到

\[
\frac1X\sum_{X\le n\le2X}r_2(n-u)r_2(n-v)
=C(h)+O_\epsilon(X^{-6/23+\epsilon}),
\]

uniform in所有u,v。端点造成的主项改动为 O(C(h)/X)=O(loglog(3X)/X)，由 σ(m)/m 的标准上界吸收。原文若含t=0，其项在S(B,h)−S(A,h)中抵消。负位移由交换u,v处理。Assing–Humphries2026 arXiv v1 Thm1.3可将−6/23换成−41/128，但不需要此改进才能完成本证明。

**PROVED.** h=0单独使用Borwein–Choi2003 Theorem3.2/(3.14)的Σ_{n≤T}r_2(n)^2=O(TlogT)。由K_X=M_X+o(M_X)，全部zero差贡献

\[
O\left(\frac{K_X\log X}{M_X^2}\right)=O(1/\log X)=o(1).
\]

因此

\[
\frac1X\sum_{X\le n\le2X}Z_X(n)^2
=\frac1{M_X^2}\sum_{s_i\ne s_j}C(|s_i-s_j|)+o(1).
\]

## 6. Norm identification的每个limit

**PROVED.** 将右边C的odd divisor sum先截在Y；由§2，截尾误差至多16F_X(Y)，故lim_{Y→∞}limsup_{X→∞}误差=0。再将b_2按v_2(h)截在固定A，uniform errorO(2^(−A))乘上平均odd divisor sum O(1)，所以可在X极限后令A→∞。

固定Y,A后的表达式只取决于h modulo一个固定整数（例如2^(A+1)lcm{d≤Y:d odd}）。由§1 μ_q经验分布收敛，其平均收敛于μ×μ的相应平均。排除h=0的差别是至多固定常数×K_X/M_X²→0。最后由§4的integrable divisor majorant，令Y,A→∞，得到

\[
\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}Z_X(n)^2
=8\mathbb E_{\mu\times\mu}\left[b_2(U-V)\sum_{d\text{ odd}}\frac{\mathbf1_{d\mid(U-V)}}d\right]
=\|f_\infty\|_2^2.
\]

这里所有截断固定后才令X→∞；uniform tail保证最后去掉截断。

## 7. Fixed-q mixed moment

**PROVED.** 固定q。在任一annulus X/2≤u²+v²≤2X中，对每个modq lattice coset的格点计数为area/q²+O_q(√X)。对norm residue a的所有cosets求和，且对s_i≤X/2一致，有

\[
\sum_{\substack{X\le n\le2X\\n\equiv a\bmod q}}r_2(n-s_i)
=\frac{\pi X}{q}\beta_q(a-s_i)+O_q(\sqrt X+1).
\]

于是

\[
\frac1X\sum_{X\le n\le2X}Z_X(n)f_q(n)
\longrightarrow\frac1q\sum_{a\bmod q}f_q(a)^2=\|f_q\|_2^2.
\]

确切地说，先对i平均，再以μ_{q,X}→μ_q替换有限modq分布；误差O_q(X^(−1/2))。另固定周期函数f_q²的整数平均→Haar average。结合§6展开平方，就得到§0方框exact identity。

## 8. 原始文献与最近closed route

**PROVED.** Fernando Chamizo, *Mediterr.J.Math.*19(2022),44, DOI10.1007/s00009-021-01959-3，正式全文已核；Edgar Assing–Peter Humphries, arXiv2607.13518v1 Thm1.3，全文已核，QJM haag043正式版仅abstract；Borwein–Choi, *RamanujanJ.*7(2003),95–127, DOI10.1023/A:1026230709945，作者全文已核；Xiangyu Wang arXiv2609.37508v2 Lemma2.2，全文已核。具体statement及版本限制见独立literature audit。

**PROVED.** 最近的closed route是N-010 pointwise minor-arc no-go，以及N-001 random-CRT L²不能推出adversarialL∞。本稿只完成n-averaged weighted L²的识别，不声称任何pointwise n保证；所以既未重复其已否定结论，也未绕过它们。POS没有从L² convergence或finite-level positivity自动得到。



---

# 附录 B：Romanoff logarithmic-moment lemma

## 命题

**PROVED.** 固定整数g≥2，令ℓ_g(d)=ord_d(g)，限(d,g)=1；约定ℓ_g(1)=1。对每个固定非负整数k，有

\[
\sum_{\substack{d\ge1\\(d,g)=1}}\frac{(\log d)^k}{d\,\ell_g(d)}<\infty.
\]

k=0时令(log1)^0=1。因此对每个固定整数k≥1及Y≥2，

\[
\sum_{\substack{d>Y\\(d,g)=1}}\frac1{d\,\ell_g(d)}\ll_{g,k}(\log Y)^{-k}.
\]

这里k固定，未声称隐含常数对k一致。这个强化由下面独立推导得到；Wang2026 Lemma2.2提供的是无log权重的order分布思路，不能将全部加强误写成他文中原定理。

## 1. 一个全整数 divisor moment bound

**PROVED.** 对每个固定整数k≥0，存在C_k，使每个整数N≥1满足

\[
\sum_{d\mid N}\frac{(\log d)^k}{d}
\le C_k\,[\log\log(3N)]^{k+1},
\]

当k=0采用上述约定。为避开N极小时loglog(3N)<1的常数麻烦，也可将右边统一写C_k(1+loglog(3N))^(k+1)；两种写法仅差绝对常数。

**PROVED.** k=0是σ(N)/N≪loglog(3N)的经典上界。以下证明k≥1。将N=∏p^{a_p}，设随机divisor D满足

\[
\Pr(D=d)=\frac{d^{-1}}{\sum_{e\mid N}e^{-1}}\quad(d\mid N).
\]

乘法分解说明随机变量V_p=v_p(D)相互独立，并且

\[
\Pr(V_p=r)=\frac{p^{-r}}{\sum_{j=0}^{a_p}p^{-j}},\quad0\le r\le a_p.
\]

对于1≤r≤a_p，

\[
\Pr(V_p\ge r)=\frac{p^{-r}-p^{-a_p-1}}{1-p^{-a_p-1}}\le p^{-r}.
\]

故V_p被一个几何变量G_p（Pr(G_p≥r)=p^(−r)）stochastically dominated；可将所有p独立couple。因此

\[
\mathbb E[(\log D)^k]\le\mathbb E\left[\left(\sum_{p\mid N}(\log p)G_p\right)^k\right].
\]

对每个固定j≥1，

\[
\mathbb E[G_p^j]=(1-p^{-1})\sum_{r\ge1}r^jp^{-r}\le\frac{C_j}{p}
\]

对所有p≥2统一成立，例如取C_j=Σ_{r≥1}r^j2^(1−r)。

**PROVED.** 设L=logN，先假设L≥max(3,e^(k−1))；其余有限范围扩大C_k即可。对1≤j≤k，

\[
U_j(N):=\sum_{p\mid N}\frac{(\log p)^j}{p}\ll_j(\log L)^j.
\]

证明分两段。p≤L时，由Chebyshev θ(t)=Σ_{p≤t}logp≪t及partial summation，

\[
\sum_{p\le L}\frac{(\log p)^j}{p}
=\int_{2^-}^{L}\frac{(\log t)^{j-1}}t\,d\vartheta(t)
\ll_j(\log L)^j.
\]

p>L时，函数(logt)^(j−1)/t在t≥L下降，所以

\[
\sum_{\substack{p\mid N\\p>L}}\frac{(\log p)^j}{p}
\le\frac{(\log L)^{j-1}}L\sum_{p\mid N}\log p
\le(\log L)^{j-1}.
\]

注意这里使用Σ_{p|N}logp≤logN=L；小素数截点是**logN**，最后得到的是**loglogN**的幂，未混淆两层log。

**PROVED.** 展开第k次方。把有序k个prime indices按相同prime归组，每个set partition的块大小为j_1,...,j_r，Σj_i=k；不同prime的独立性及上述moment bound给该组总和

\[
\le\prod_{i=1}^r C_{j_i}U_{j_i}(N)
\ll_k(\log L)^k.
\]

去掉distinct-prime限制只增大非负和。k固定时set partitions仅有限个，故E[(logD)^k]≪k(loglogN)^k。乘回σ(N)/N≪loglog(3N)即完成divisor moment bound。

## 2. 小order的加权计数

**PROVED.** 对实数T≥1，令J=⌊T⌋、P_T=∏_{1≤j≤J}(g^j−1)。若ℓ_g(d)≤T，则d|P_T。因此

\[
A_{g,k}(T):=\sum_{\substack{(d,g)=1\\\ell_g(d)\le T}}\frac{(\log d)^k}{d}
\le\sum_{d\mid P_T}\frac{(\log d)^k}{d}
\ll_{g,k}(\log(2T))^{k+1},
\]

因为logP_T≤(logg)J(J+1)/2。g=2,T<2导致P_T=1的小例外被同样公式及常数覆盖。

## 3. Partial summation 与尾项

**PROVED.** 对任何U≥1，有限Stieltjes partial summation给

\[
\sum_{\substack{(d,g)=1\\\ell_g(d)\le U}}
\frac{(\log d)^k}{d\ell_g(d)}
=\frac{A_{g,k}(U)}U+\int_1^U\frac{A_{g,k}(t)}{t^2}\,dt.
\]

第一项→0，而∫_1^∞(log(2t))^(k+1)t^(−2)dt<∞。所有项非负，monotone convergence得全级数收敛。最后对d>Y有(logd)^k≥(logY)^k，故得到开头尾界。这里没有q,X之间的limit interchange。

## 4. Radomskii v7 (1.4) 对B={3^c+5^d}的直接应用

**PROVED.** 本节只核v7 Theorem1.1的hypothesis (1.4)，不假冒almost-all结论。B按指数对计重；令C=⌊log_3x⌋+1、D=⌊log_5x⌋+1，则B(x)≍CD，ρ_B(x)≤min(C,D)。

对p≠5，固定c,c′,d后，5^{d′}≡5^d+3^c−3^{c′} (modp)的d′在[0,D−1]至多D/ord_p5+1个。因此

\[
\sum_{j:b_j\le x}\lambda_B(x;j,p)
\le C^2D^2/\operatorname{ord}_p(5)+C^2D.
\]

从而对任意固定α∈(0,1)，

\[
\frac1{B(x)^2}\sum_{j:b_j\le x}
\sum_{p\le(\log x)^\alpha}\frac{\lambda_B(x;j,p)\log p}{p}
\ll\sum_{p\ne5}\frac{\log p}{p\operatorname{ord}_p(5)}
+\frac1D\sum_{p\le(\log x)^\alpha}\frac{\log p}{p}+1
\ll1.
\]

p=5的贡献用collision≤B(x)²吸收；第一项由k=1的composite-order series收敛；第二项≪loglogx/logx。这验证(1.4)，没有必须使用有限S-unit碰撞结论：若η(x)≍sqrt(logx)，则ρ_B(x)η(x)≪log^(3/2)x=o(B(x))已足够适用主定理的positive-density分母。

**PROVED.** 该核验本身只涉及Radomskii的小prime weighted collision condition及其positive-density用法。无穷级数收敛本身不能代替finite-X tail argument；后续独立审计已用共同乘积Q_X=∏_{s_i≠s_j}|s_i−s_j|补上：logQ_X≪log⁵X，Σ_{q|Q_X}1/q≪loglogX，故额外collision remainder≪loglogX/logX。完整证明见lane_l_r1b_full_audit.md §2。

**UNRESOLVED.** 这些结论仍不推出POS或每个n的R(n)>0。



---

# 附录 C：Shifted correlation 的原文与版本审计

## 1. 资料及版本范围

**PROVED.** Fernando Chamizo, “The Additive Problem for the Number of Representations as a Sum of Two Squares,” *Mediterranean Journal of Mathematics* **19** (2022), article 44, 17 pp., DOI [10.1007/s00009-021-01959-3](https://doi.org/10.1007/s00009-021-01959-3). 正式发表版全文已读：[HTML](https://link.springer.com/article/10.1007/s00009-021-01959-3)，[PDF](https://link.springer.com/content/pdf/10.1007/s00009-021-01959-3.pdf)。Theorem 1.1、Corollary 1.5、§4 Theorem 4.1/4.2 已核。

**PROVED.** Edgar Assing and Peter Humphries, “Spectral Fourth Moments of Hecke–Maaß Cusp Forms,” *Quarterly Journal of Mathematics*, advance article haag043 (online 14 October 2026), DOI [10.1093/qmath/haag043](https://doi.org/10.1093/qmath/haag043). [arXiv:2607.13518v1](https://arxiv.org/abs/2607.13518v1), submitted 15 July 2026; [arXiv PDF](https://arxiv.org/pdf/2607.13518v1), 26 pp. 当前 theorem 审计明确针对 arXiv v1。

**UNRESOLVED.** 正式期刊全文未取得，属于 **abstract only**；OUP 元数据列 revision received 18 September 2026，而 arXiv 仅 v1，不能断言两版逐字或 theorem 编号相同。OUP 正式发表信息已核。作者公开 errata 文件不含此篇。

## 2. 定义、主项及 parity

**PROVED.** 令 r_2(t)=#{(a,b)∈Z²:a²+b²=t}，对正整数 h 写

\[
S(x,h)=\sum_{1\le t\le x}r_2(t)r_2(t+h),\qquad E(x,h)=S(x,h)-C(h)x.
\]

原文若从 t=0 起计，只多 r_2(h)；下面两个端点相减时这一项精确抵消。写 h=2^k u、u odd，则

\[
C(h)=\frac8h\sum_{d\mid h}(-1)^{h+d}d
=8|2^{k+1}-3|\frac{\sigma(u)}h.
\]

因此 h odd 时 C(h)=8σ(h)/h；h even 时

\[
C(h)=8(2-3/2^k)\frac{\sigma(u)}u.
\]

特别 k=1,2,3 的前因子分别为4,10,13，不能将 h even 误套8σ(h)/h。所有 3^c+5^d 都为偶数，所以本问题非零位移均为偶数；必须保留此2-adic因子。

## 3. Chamizo 2022 无条件 uniformity

**PROVED.** Corollary 1.5 在1≤h≤x的四段为（每个 ε>0，常数仅依赖ε）

\[
h^{-\epsilon}E(x,h)\ll_\epsilon
\begin{cases}
x^{2/3},&h^{117/64}\le x,\\
h^{39/128}x^{1/2},&h^{89/64}\le x<h^{117/64},\\
h^{7/96}x^{2/3},&h^{161/160}\le x<h^{89/64},\\
x^{17/23},&h\le x<h^{161/160}.
\end{cases}
\]

从第二段 h≤x^(64/89) 得 exponent≤64/89；第三段 h≤x^(160/161) 得 exponent≤17/23。故统一得到

\[
E(x,h)\ll_\epsilon x^{17/23+\epsilon}\quad(1\le h\le x),
\]

隐含常数独立于 h 和 x。这里 m=0 不在 theorem 范围内。负位移也未由原文直接陈述，但交换 shift 顺序后可只用 h>0。

**CONDITIONAL (Chamizo §4 的 spectral fourth-moment estimate (4.1)).** Chamizo Theorem 4.1 对1≤h≤x²给出

\[
x^{-\epsilon}E(x,h)\ll_\epsilon x^{2/3}+x^{1/2}h^{(1+4\theta)/8}
+x^{1/3}h^{1/3}+\min\{x^{1/2}h^{1/4},x^{1/4}h^{(3+4\theta)/8}\}.
\]

其中 θ 是 Hecke eigenvalue Ramanujan 界 λ(h)≪εh^(θ+ε) 的许可指数。所需 (4.1) 是固定相关点 z0 的 dyadic fourth moment Σ_{T≤|t_j|<2T}|u_j(z0)|⁴≪εT^(2+ε)。2022 原文仍视其为未证。

## 4. 2026 年改进

**PROVED.** Assing–Humphries arXiv v1 Theorem 1.2：固定 q∈N，以及 Γ0(q)\H 上来自负 fundamental discriminant D 的 Heegner point z0；对所有T≥1及ε>0，固定q的正交 Hecke–Maaß cuspform basis 满足

\[
\sum_{\phi\in\mathcal B(q),\,T\le t_\phi\le2T}|\phi(z_0)|^4
\ll_{q,D,\epsilon}T^{2+\epsilon}.
\]

这里依赖 q,D 不可忽略；一般点的 conjecture 没有因此全解决。Correlation application 只需(q,z0)=(1,i)和(2,(-1+i)/2)，皆D=−4，所以 theorem 覆盖。

**PROVED.** 同文 Theorem 1.3（PDF p.4）使 Chamizo 的上述 pointwise 界无条件成立。其五段陈述为

\[
h^{-\epsilon}E(x,h)\ll_\epsilon
\begin{cases}
x^{2/3},&h^{3/4+3\theta}\le x,\\
h^{(1+4\theta)/8}x^{1/2},&h\le x<h^{3/4+3\theta},\\
h^{(3+4\theta)/8}x^{1/4},&h^{1/2+2\theta}\le x<h,\\
h^{1/4}x^{1/2},&h^{1/2}\le x<h^{1/2+2\theta},\\
h^{1/3}x^{1/3},&x<h^{1/2}.
\end{cases}
\]

取θ=7/64：3/4+3θ=69/64，(1+4θ)/8=23/128。因此

\[
\boxed{E(x,h)\ll_\epsilon x^{87/128+\epsilon}\quad(1\le h\le x).}
\]

第一段 exponent 2/3<87/128；第二段 h≤x给 x^(1/2+23/128)。此推论的ε常数与h,x无关。

**UNRESOLVED.** arXiv v1 Theorem 1.3 的附带 mean-square 行印为N^(4/2)M^(1/3)+M^4，且 proof 最后一行自指 Theorem1.3，明显需要版本/排版核对。本审计不使用 mean-square 行；使用的 pointwise 五段与 Chamizo Theorem4.1 的分段化相符。

## 5. 对 R1-b 的精确适用窗口

**PROVED.** 对任意 X≥8，取两个不同的数值 shift u=3^c+5^d、v=3^{c'}+5^{d'}，均≤X/2。不失一般性 u>v，置h=u−v≥1，

\[
A=\lceil X\rceil-u-1,\qquad B=\lfloor2X\rfloor-u.
\]

则 A≥X/2−1、B≤2X，并且

\[
A-h=\lceil X\rceil-2u+v-1\ge v-1\ge1.
\]

故 h≤A≤B，两个端点都落在 theorem 的 h≤x 范围。精确恒等式为

\[
\sum_{X\le n\le2X}r_2(n-u)r_2(n-v)=S(B,h)-S(A,h).
\]

由2026界及 B−A=X+O(1)，

\[
\frac1X\sum_{X\le n\le2X}r_2(n-u)r_2(n-v)
=C(h)+O_\epsilon(X^{-41/128+\epsilon}).
\]

在这里用C(h)≪εh^ε吸收端点O(C(h)/X)；这一界由σ(h)/h≪εh^ε直接得到。误差对H_X中所有不同数值 shifts统一，因此除以|H_X|²后对所有ordered pairs求平均不损失指数。只用2022版时同理误差Oε(X^(−6/23+ε))。没有 h≤X/2 的未覆盖区域。

## 6. 位移0及数值碰撞

**PROVED.** Jonathan M. Borwein and Kwok-Kwong Stephen Choi, “On Dirichlet Series for Sums of Squares,” *Ramanujan Journal*7(2003),95–127, DOI10.1023/A:1026230709945。作者全文https://www.sfu.ca/~schoia/paper/dirichlet.pdf，Theorem3.2与(3.14)：

\[
\sum_{n\ge1}\frac{r_2(n)^2}{n^s}
=\frac{16\zeta(s)^2L(s,\chi_{-4})^2}{(1+2^{-s})\zeta(2s)}\quad(\Re s>1),
\]

\[
\sum_{n\le x}r_2(n)^2=4x\log x+4\alpha x+O(x^{2/3}),
\]

其中α=2γ+(8/π)L'_{-4}(1)−(12/π²)ζ'(2)+(log2)/3−1。R1-b只需O(XlogX)。

**PROVED.** 数值shift相等的ordered pair数为|H_X|+O(logX(loglogX)²)，已由LTE初等证明：非平凡碰撞c<c′、d>d′时，c=v₃(5^(d−d′)−1)≪loglogX，d′=v₅(3^(c′−c)−1)≪loglogX；选(c,c′,d′)后d至多一个。故zero-shift归一化贡献O(logX/|H_X|)=O(1/logX)→0，无需假设S-unit有限碰撞。完整证明见lane_l_r1b_full_audit.md §1。仍不可把“指数对不同”直接当作“数值shift不同”。

## 7. 限制及路由

**UNRESOLVED.** 上述 input 验证的是 averaged r_2 correlation 所需的 x,h uniformity。它不独立证明 R1-b 的 composite-divisor tail、profinite martingale identification 或 POS。尤其它不推出R(n)>0对每个n；也不推出f∞>0 a.e.。最邻近已关闭 N-010 是 pointwise minor-arc 路线；这里使用 n-平均的二阶矩并改进其误差，未宣称绕过N-010。

**PROVED.** 本审计可投递给 lane A/B（R1-b 相关和与limit interchange），E（误差量级核验），V（版本及parity审计）。不应将它作为C/P的全n正性证明。



---

# 附录 D：Radomskii 一般定理的完整 hypotheses

**PROVED.** Artyom Radomskii, *Variants of Romanoff’s theorem*, [arXiv:2504.09954v7](https://arxiv.org/html/2504.09954v7), 27 August 2026, Theorem 1.1。以下是原定理的数学转述；原文中的自然数索引从1开始。

令 A=(a_i) 为严格递增的正整数序列，B=(b_j) 为允许重复的正整数序列，每个值 v 的 multiplicity ord_B(v) 有限。定义

\[
A(x)=\#\{i:a_i\le x\},\quad
A(x,r)=\#\{i:a_i\le x,\ a_i+r\in A\},\quad
B(x)=\#\{j:b_j\le x\},
\]

\[
\lambda_B(x;j,p)=\#\{k:b_k\le x,\ b_k\equiv b_j\pmod p\},
\quad \rho_B(x)=\max_{1\le v\le x}\operatorname{ord}_B(v).
\]

假设存在正函数 η(x)，且以下 estimates 对充分大 x 成立，隐含常数固定：

\[
A(x)\asymp\frac{x}{\eta(x)},\qquad A(x/2)\gg A(x),
\]

\[
A(x,r)\ll\frac{r}{\varphi(r)}\frac{x}{\eta(x)^2}
\quad\text{uniformly for every integer }r\ge1,
\qquad B(x/2)\gg B(x).
\]

还要求存在固定 α∈(0,1)，使

\[
\sum_{j:b_j\le x}\sum_{p\le(\log x)^\alpha}
\frac{\lambda_B(x;j,p)\log p}{p}\ll B(x)^2.
\]

若 r(n)=#{(i,j):a_i+b_j=n}，则存在 c₁,c₂>0，仅依赖 α 与这些 estimates 的常数，使充分大 x 有

\[
\#\left\{n\le x:r(n)\ge c_1\frac{B(x)}{\eta(x)}\right\}
\ge c_2x\frac{B(x)}{B(x)+\rho_B(x)\eta(x)}.
\]

**PROVED.** 在本题应用中，为避免将未引用的 S2 autocorrelation upper bound 当成假设已知，可以直接使用原文 Example 2 的 A=S′：所有仅由 p≡1 mod4 primes 组成的正整数。它是 S2 的子集，η(x)=√log x，且原文核实上述 A(x,r) bound。其 asymptotic 的 printed leading constant 需要按本报告 H5 修正，但上述 comparison estimates 不受影响。

**PROVED.** B 按 (c,d)∈Z≥0² 的 tuple multiplicity 列出 3^c+5^d。于是 B(x)≍log²x，B(x/2)≍B(x)，ρ_B(x)≤min(⌊log₃x⌋+1,⌊log₅x⌋+1)≪log x。Romanoff logarithmic-moment 附录 §4 已验证其 small-prime collision 条件。因此有常数 c₁,c₂>0，使充分大 x 至少 c₂x 个 n≤x 满足

\[
R(n)\ge c_1(\log x)^{3/2}.
\]

**PROVED.** 这提供本题的 positive-density / many-representations 基线；它不等于 almost-all，也不应作为超过 repo P-001 基线的新突破来报告。更强的 R1-b 审计采用不同的 weighted statistic Z_X。

**UNRESOLVED.** GAP：该定理分母只给固定正比例，不能由 B(x)≫ρ_B(x)η(x) 把 c₂ 提升到1；原文没有这样的 uniform-to-one conclusion。



---

# 附录 E：Hellinger、prime powers、squarefree covering

## H1. 无 independence、无 UI 前提的 Hellinger path criterion

**PROVED.** 设 (M_j,F_j,P)_{j≥0} 是严格正、有限值、mean-one martingale，M_0=1。令 r_j=M_{j+1}/M_j，w_j=√r_j−1，h_j=E(w_j²∣F_j)。则

\[
\{M_\infty>0\}=\left\{\sum_{j\ge0}h_j<\infty\right\}\quad\bmod P\text{-null}.
\]

**PROVED.** 非负 conditional expectation 给 E(r_j∣F_j)=1，故 r_j∈L¹、w_j∈L²。并有 E(w_j∣F_j)=−h_j/2，a_j:=E(√r_j∣F_j)=1−h_j/2∈(0,1]。置 A_n=∏_{j<n}a_j，Y_n=√M_n/A_n。逐步条件期望表明 Y_n 是 mean-one nonnegative martingale，所以收敛到有限值 a.s.。若 Σh_j=∞，则 log A_n≤−Σ_{j<n}h_j/2→−∞，于是 M∞=0。

**PROVED.** 反向不能假定 ΣEh_j<∞。固定整数 K≥1，取

\[
I_j^K=\mathbf1_{\sum_{i=0}^{j}h_i\le K},\qquad d_j=w_j+h_j/2.
\]

I_j^K 是 F_j-measurable，可作 j→j+1 步的 predictable multiplier；由于包含本步 h_j，ΣI_j^Kh_j≤K 没有 overshoot。E(d_j∣F_j)=0、E(d_j²∣F_j)=h_j−h_j²/4≤h_j，因此 S_n^K=Σ_{j<n}I_j^Kd_j 的 L² norm squared≤K，故 S_n^K a.s. 收敛。Tonelli 同时给 EΣI_j^Kw_j²≤K，因此该和 a.s. 有限。在 {Σh_j≤K} 上所有 I_j^K=1，故 Σw_j 收敛，Σw_j²<∞。最终 |w_j|≤1/2，log(1+w_j)=w_j+O(w_j²)，于是 log M_n=2Σ_{j<n}log(1+w_j) 收敛到有限实数。取可数 K 的并即得 M∞>0。

**PROVED.** 这个自含论证与 Kabanov–Liptser–Shiryaev 的 dependent Hellinger criterion 一致。用于 M_j=f_{j!}/π 时，F_j 的每个 class 分裂成 j+1 个等 Haar 权子类，所以 h_j 正是主报告§6的显式公式。若存在 finite-level zero，先直接判定 (POS) 失败，不在零值上定义比值。

**UNRESOLVED.** Arithmetic GAP 是沿 Haar paths 的 Σh_j 是否有限。L² boundedness 自动给 ΣE(ΔM_j)²<∞；它不控制 h_j 中的相对变化，尤其在 M_j 很小时不能除去分母。

## H2. 每个 prime-power marginal 的统一正性

**PROVED.** 对任意 prime p、k≥1、a mod p^k，本题 f_{p^k}(a)/π≥4/5；p=5 且 5∣a 时取等号。

**PROVED.** 若 p≡1 mod4，Z/p^kZ 中有 i²=−1，线性变量变换 u=x+iy、v=x−iy 可逆。对每个 unit u，uv=a 有唯一 v，因此 β_{p^k}(a)≥φ(p^k)/p^k=1−1/p≥4/5；对任意 shift law 的平均保留下界。若 a 为 unit，则 uv=a 强制 u,v 均为 units，故此时 β_{p^k}(a)=1−1/p。

**PROVED.** 若 p≡3 mod4，unit a 的 norm count 为 (p+1)p^{k−1}：mod p 有 p+1 个解，均 nonsingular，每层 Hensel lifting 增加 p 倍。因此 β_{p^k}(a)=1+1/p。p≠3 时，ord_p(3)≥5：3^t−1 在 1≤t≤4 的 odd prime factors 只有5与13，均为1 mod4。固定5的 cycle value，3的 cycle 对指定 shift mod p 至多命中一次，故 μ_p 的最大质量≤1/ord_p(3)≤1/5。至少4/5 shifts 使 a−s 为 unit，故 f_{p^k}(a)/π≥(4/5)(1+1/p)>4/5。p=3 用下段精确公式得到最小值5/6。

**PROVED.** p=2 时，对 k≥3，〈5〉恰为所有 1 mod4 units，〈3〉中 1、3 mod4 两类等频，所以 shifts 均匀覆盖 even residues。k=1,2 直接同样成立。所有 (u,v) mod 2^k 中恰好一半使 u²+v² 为指定 parity，因此 β_{2^k} 在任一 parity class 的平均为1，f_{2^k}≡π。

**PROVED.** 5 在各 3^k 上是 primitive root（ord_35=2、v₃(5²−1)=1）；3 在各 5^k 上是 primitive root（ord₅3=4、v₅(3⁴−1)=1）。故相应 μ 均匀覆盖 units。利用上一段 unit norm count 及 Σ_aβ_{p^k}(a)=p^k，得到主报告所列 f_{3^k}、f_{5^k} 常值公式。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 这些下界不 tensorize 成 composite 下界。模20的 explicit convolution 反例已经足以推翻 f_{20}/π=(f₄/π)(f₅/π) 的身份；这不是对任何修正后 Euler product 的普遍否定。

## H3. squarefree covering-free criterion：保持正确极限次序的证明

**PROVED.** 假设没有 finite cover of Z by a_i mod ord_{p_i²}(2)，其中 p_i 为 distinct odd primes。固定 w，W=∏_{3≤p≤w}p。对每个 c mod W²，禁止 2^k≡c mod p² 只排除空集或一个 class mod ord_{p²}(2)；没有 full cover 保证存在某 fixed k_c≥1，令 s_c=2^{k_c}，使 c−s_c 不被任何 p²、p≤w 整除。对奇 n≡c mod W²，n−s_c 为 odd。令 S_w=max_c s_c，先丢弃 n≤S_w 的 O_w(1) 个数；此后只数 S_w<n≤X，所有 residual 都在 [1,X] 中。

**PROVED.** 对固定 c、n≤X，若 residual 不 squarefree，就有 p>w、p²≤X 且 n≡s_c modp²。由 CRT，此类 n 的数量至多

\[
\frac{X}{2W^2}\sum_{p>w}\frac1{p^2}+O(\pi(\sqrt X)).
\]

把 W² 个 odd residue classes（mod 2W²）求和，加回 O_w(1) 个已丢弃的小整数。W 固定，误差 O(W²π(√X))+O_w(1)=o(X)。故 limsup_{X→∞}exception/X≤(1/2)Σ_{p>w}p^{-2}，再令 w→∞即为0。完全不需要令 w=w(X)，也不需要证明 ord_{W²}(2) 小于 log X。

**PROVED.** 反向若有 cover，CRT 取 odd n 同时满足 n≡2^{a_i} modp_i²；每个 k 都有某 p_i²∣n−2^k，所以该 positive-density arithmetic progression 没有 positive squarefree residual。此即 Sun–Zhao Thm. 6.2 的精确定性结论；修补了其 growing-w 论证中未交代的周期长度条件。

## H4. Erdős 1950 的 progression：排除 prime-equality 例外

**PROVED.** Paul Erdős, *On integers of the form 2^k+p and some related problems*, Summa Brasil. Math. 2 (1950), 113–123，[原始全文](https://www.renyi.hu/~p_erdos/1950-07.pdf)，Thm. 3。所有 n≡7629217 mod11184810 都不能写成 p+2^k（p prime，k≥0）。

**PROVED.** 令 M=11184810=2·3·5·7·13·17·241，r=7629217。r modulo (3,5,7,13,17,241) 为 (1,2,1,11,8,121)。与这些 primes 对应的 exponent classes 为 0 mod2、1 mod4、0 mod3、7 mod12、3 mod8、23 mod24；直接分 k mod24 核验其并为 Z，并且各自 2^k≡r modulo 对应 prime。因此若 n=p+2^k、k≥1，则 p 必须属于这六个覆盖 primes。

**PROVED.** p∈{7,13,241} 时 n−p≡0 mod3，不可能是2的幂；p∈{3,5,17} 时 n−p modulo7 分別为5、3、5，均不在 {1,2,4}。所以“residual 等于覆盖 prime”的例外全部排除。k=0 时 n=p+1 为 odd 只可能 p=2,n=3，而3不在该 progression。无须留下有限 exceptions。

## H5. 资料中的两个版本性细节

**PROVED.** Radomskii 2504.09954v7 Example 2 将仅由 p≡1 mod4 primes 组成的整数的 asymptotic constant 印成 reciprocal Euler-product exponent。其2026年 product-powers 文明确更正为

\[
\frac{1}{2\sqrt2}\prod_{p\equiv3\ (4)}(1-p^{-2})^{1/2}=\frac1{4K},
\]

其中 K 为 Landau–Ramanujan constant。可独立用 F(s)=∏_{p≡1(4)}(1−p^{-s})^{-1} 及 F(s)²=(1−2^{-s})ζ(s)L(s,χ₄)∏_{p≡3(4)}(1−p^{-2s}) 核对。所需 ≍ 及 Romanoff positive-density theorem 不受此常数排版影响。

**UNRESOLVED.** Assing–Humphries arXiv v1 的附带 mean-square 行写 N^{4/2}M^{1/3}+M⁴；原始 Chamizo1999 Cor. 4.2 写的是 N^{4/3}M^{1/3}+M⁴。本报告只使用分别核过的 pointwise-in-h error estimates，不自行改写尚未取得的期刊版 theorem。



---

# 附录 F：Base-prime block 的精确 stabilization

## 1. 精确陈述

**PROVED.** 使用题目规定的 μ_q、β_q、f_q。对每个 k≥3、u≥1、v≥1，令 q=2^k3^u5^v，则对所有 a modq 有

\[
\boxed{f_q(a)=f_{120}(a\bmod120).}
\]

更明确地，记 B(a)=f_{120}(a)/π，则

\[
\boxed{
B(a)=\frac18\sum_{r=0}^3\sum_{s=0}^1
\beta_8(a-3^r-5^s)\,
\beta_3(a-5^s)\,
\beta_5(a-3^r).
}
\]

各 β 按其下标模数计算参数。尤其 B(a)≥4/15；同一下界适用于所有上述 q，与 k,u,v 无关。

**UNRESOLVED.** 该结论只处理prime divisors全部在{2,3,5}中的一个block。加入其他primes后，其exponent orders可与本block相关；本文不声称一般CRT tensorization、所有composite finite levels正性或(POS)。

## 2. Eventual periods 与需要的 conditional independence

**PROVED.** 固定q。有限个 c<u 或 d<v 在 limiting exponent occupation measure 中质量为0；因此只看c≥u、d≥v，此时3^c=0 mod3^u、5^d=0 mod5^v。由LTE及primitive-root lifting，

\[
\operatorname{ord}_{2^k}(3)=2^{k-2},\quad
\operatorname{ord}_{2^k}(5)=2^{k-2},\quad
\operatorname{ord}_{5^v}(3)=4\cdot5^{v-1},\quad
\operatorname{ord}_{3^u}(5)=2\cdot3^{u-1}.
\]

前两式在k≥3成立，包括k=3。后两式分别用v₅(3⁴−1)=1、v₃(5²−1)=1。令A=max(k−2,2)、B₀=max(k−2,1)，则c、d的eventual periods分别为

\[
T_c=2^A5^{v-1},\qquad T_d=2^{B_0}3^{u-1}.
\]

固定模数的矩形exponent averages给c modT_c与d modT_d独立均匀。H_X与相应完整矩形仅差O(logX)个点，不改变此极限。

**PROVED.** 条件于r=c mod4和s=d mod2后，CRT给出以下真正成立的independence：c的2-primary component与其5-primary component独立，d的2-primary component与其3-primary component独立；c与d仍独立。这并非声称输出shift在2、3、5三个coordinates无条件独立。r、s本身正是必须保留的相关信息，且八种(r,s)等概率。

## 3. 条件于(r,s)后逐coordinate计算

**PROVED.** 先记录norm density的compatibility。若m∣M，对b modm，

\[
\frac1{M/m}\sum_{\substack{z\bmod M\\z\equiv b\ (m)}}\beta_M(z)=\beta_m(b).
\]

因为每个modm的norm solution有(M/m)²个(u,v) lifts；再按norm residue求和并除以M及lift数量即可。互素模数下β按CRT乘法分解。

**PROVED.** 给定s，5^d在所有≡5^s mod3的units mod3^u上均匀：5²生成1+3Z/3^uZ，且d的3-primary component与2-primary component独立。因此先平均d的3-primary component有

\[
E\big[\beta_{3^u}(a-5^d)\mid r,s,\text{2-primary components}\big]
=\beta_3(a-5^s).
\]

同理，3⁴生成1+5Z/5^vZ；给定r，平均c的5-primary component给

\[
E\big[\beta_{5^v}(a-3^c)\mid r,s,\text{2-primary components}\big]
=\beta_5(a-3^r).
\]

u=1或v=1时相应component是trivial，公式仍成立。

**PROVED.** 对2-primary part，v₂(25−1)=3，且

\[
v_2(25^{2^t}-1)=3+t\quad(t\ge0),
\]

所以〈25〉mod2^k恰为1+8Z/2^kZ（k=3时两者都是{1}）。给定s，d=s+2z让5^d均匀覆盖5^s+8Z/2^kZ。给定r有3^c≡3^r mod8；无论c其余2-primary bits是什么，3^c+5^d均匀于3^r+5^s+8Z/2^kZ。再次用β compatibility，

\[
E\big[\beta_{2^k}(a-3^c-5^d)\mid r,s\big]
=\beta_8(a-3^r-5^s).
\]

**PROVED.** CRT分解β_q后，先积分彼此独立的3-primary、5-primary exponent components，再积分2-primary components，所得conditional mean就是三个β因子的乘积。最后平均八个(r,s)得到boxed公式。右边恰是q=120时的同一计算，故stabilization对所有k,u,v成立，没有任何随q的极限互换。

## 4. 统一正下界及 finite certificate

**PROVED.** 直接norm counts给

\[
\beta_8=(1,2,2,0,1,2,0,0),\quad
\beta_3=(1/3,4/3,4/3),\quad
\beta_5=(9/5,4/5,4/5,4/5,4/5).
\]

八个(r,s)的3^r+5^s mod8均匀覆盖四个even residues；β₈在任一parity class的平均为1。因此

\[
B(a)\ge\frac13\frac45\cdot\frac18\sum_{r,s}\beta_8(a-3^r-5^s)=\frac4{15}.
\]

**FINITE COMPUTATION.** 附属脚本lane_l_base_prime_stabilization.py用Fraction对boxed八项公式计算全部a mod120；得到min B=7/15，恰在a=50,70,80,100。以下八行按连续a的顺序给出全部120个exact rational values，可独立重算。

```text
a=000..014: 16/15, 2/3, 11/20, 16/15, 11/20, 2/3, 7/5, 2/3, 27/40, 16/15, 13/15, 13/12, 7/5, 13/12, 43/40
a=015..029: 16/15, 6/5, 13/12, 7/5, 13/12, 13/15, 16/15, 11/20, 2/3, 7/5, 2/3, 27/40, 16/15, 27/40, 2/3
a=030..044: 16/15, 13/12, 27/40, 26/15, 43/40, 2/3, 7/5, 13/12, 6/5, 26/15, 13/15, 2/3, 7/5, 2/3, 6/5
a=045..059: 16/15, 27/40, 2/3, 7/5, 2/3, 7/15, 26/15, 27/40, 13/12, 7/5, 2/3, 11/20, 26/15, 6/5, 13/12
a=060..074: 16/15, 2/3, 6/5, 16/15, 6/5, 2/3, 7/5, 2/3, 43/40, 16/15, 7/15, 13/12, 7/5, 13/12, 27/40
a=075..089: 16/15, 11/20, 13/12, 7/5, 13/12, 7/15, 16/15, 6/5, 2/3, 7/5, 2/3, 43/40, 16/15, 43/40, 2/3
a=090..104: 16/15, 13/12, 43/40, 26/15, 27/40, 2/3, 7/5, 13/12, 11/20, 26/15, 7/15, 2/3, 7/5, 2/3, 11/20
a=105..119: 16/15, 43/40, 2/3, 7/5, 2/3, 13/15, 26/15, 43/40, 13/12, 7/5, 2/3, 6/5, 26/15, 11/20, 13/12
```

**FINITE COMPUTATION.** Cross-check使用独立算法：直接计数所有(u,v)modq得到β_q，从3、5的modq迭代直接找eventual cycles并对所有cycle pairs卷积；q=120,240,360,600,720,1800,3600的每个residue与boxed公式完全一致。后两个模数特别核验u,v同时大于1时的conditional independence。平均B为1。程序既未寻找A303656 counterexamples，也未把这些有限模数的测试当成stabilization证明；无限结论依靠§2–3的周期及CRT论证。

**UNRESOLVED.** Feed P/B：这个lemma消除了base-prime block随深度增长的一个潜在问题，但没有控制其他primes的共同exponent constraints。最近的closed theorem是N-009；本lemma不选择单个(c,d)，也不从finite/profinite consistency推出R(n)>0。



---

# 附录 G：Single-power negative comparator

## 定理及范围

**PROVED NEGATIVE STRUCTURAL THEOREM.** 令

\[
H_X^{(2)}=\{c\in\mathbb Z_{\ge0}:2^c\le X/2\},\quad
M_X=|H_X^{(2)}|=\lfloor\log_2X\rfloor,
\]

\[
Z_X^{(2)}(n)=\frac1{M_X}\sum_{c\in H_X^{(2)}}r_2(n-2^c),\quad X\le n\le2X.
\]

以μ_q^(2)表示2^c modq的Cesàro limiting distribution，并定义

\[
f_q^{(2)}(a)=\pi\sum_{b\bmod q}\mu_q^{(2)}(b)\beta_q(a-b),\quad q_j=j!.
\]

则f_{q_j}^(2)→f∞^(2) in L²(Ẑ)及a.e.，均值π。然而对每个固定j，

\[
\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}
|Z_X^{(2)}(n)-f_{q_j}^{(2)}(n)|^2
=4\log2+\|f_\infty^{(2)}\|_2^2-\|f_{q_j}^{(2)}\|_2^2.
\]

所以

\[
\boxed{\lim_{j\to\infty}\lim_{X\to\infty}\frac1X
\sum_{X\le n\le2X}|Z_X^{(2)}(n)-f_{j!}^{(2)}(n)|^2=4\log2>0.}
\]

这严格否定把A303656两指数R1-b的结论不加修改推广到一个power的做法。原两指数问题M_X≈log²X的diagonal消失，单幂M_X≈logX的diagonal留下正的常数。

## 1. 单幂local martingale

**PROVED.** 对每个固定q，2^c modq在剥离2-power因素后eventually periodic，故μ_q^(2)存在且compatible。在odd d下它是在2生成的循环子群上的均匀分布；故U,V独立分布为相应profinite测度μ^(2)时

\[
\Pr(U\equiv V\pmod d)=\frac1{\operatorname{ord}_d(2)}\quad(d\text{ odd}).
\]

μ^(2)的2-adic component恒为0（每个固定2^a模数下有限多个c<a的权重趋0）。这里不存在对无限非负整数集合的uniform exponent抽样，只使用固定模数的有限循环极限。

**PROVED.** 经典Romanoff series

\[
\mathcal R_2:=\sum_{d\text{ odd}}\frac1{d\operatorname{ord}_d(2)}<\infty
\]

可由Wang2026 Lemma2.2/共同product证明，约定ord_1(2)=1。具体地ord_d(2)≤T⇒d|∏_{k≤T}(2^k−1)，乘积的log=O(T²)，故Σord≤T1/d≪log(2T)，Abel summation即可。

**PROVED.** 使用已审计的local kernel

\[
\Gamma_q(h)=q^{-1}\sum_a\beta_q(a)\beta_q(a+h),
\]

对odd p有positive expansion

\[
\Gamma_{p^a}(h)=(1-p^{-2})\sum_{j<a}p^{-j}\mathbf1_{p^j\mid h}
+p^{-a}\mathbf1_{p^a\mid h},
\]

而Γ_{2^a}(h)≤2。于是

\[
\|f_q^{(2)}\|_2^2=\pi^2\mathbb E\Gamma_q(U-V)
\le2\pi^2\mathcal R_2.
\]

compatibility给Haar martingale，所以有上述L²及a.e.极限。有限odd-divisor系数沿j!趋∏oddp(1−p^(−2))=8/π²，且可积majorant由R₂提供；2-adic kernel在U−V=0中趋2。因此还得到精确式

\[
\boxed{\|f_\infty^{(2)}\|_2^2=16\mathcal R_2.}
\]

## 2. 非零位移平均及tail

**PROVED.** shifts 2^c全部不同。对odd q，定义

\[
W_X(q)=M_X^{-2}\#\{(c,d)\in(H_X^{(2)})^2:c\ne d,\ q\mid2^c-2^d\}.
\]

固定c后d只能处于同一个ord_q(2) residue class，故

\[
W_X(q)\le\frac1{\operatorname{ord}_q(2)}+\frac1{M_X}.
\]

令Q_X=∏_{c≠d}|2^c−2^d|。logQ_X≪M_X²logX≪log³X，所以Σ_{q|Q_X}1/q≪loglogX。因而

\[
\sum_{\substack{q>Y\\q\text{ odd}}}\frac{W_X(q)}q
\ll\sum_{\substack{q>Y\\q\text{ odd}}}\frac1{q\operatorname{ord}_q(2)}
+\frac{\log\log X}{\log X}.
\]

右侧先X→∞再Y→∞为0。这里所有相关divisors均odd，自动与2互素，不存在nonunit odd-prime处理问题。

**PROVED.** Chamizo2022 Corollary1.5在1≤h≤T给Σ_{n≤T}r₂(n)r₂(n+h)=C(h)T+Oε(T^(17/23+ε))，其中

\[
C(h)=8b_2(h)\sum_{\substack{d\mid h\\d\text{ odd}}}\frac1d.
\]

对u=2^c>v=2^d，h=u−v，A=ceilX−u−1，B=floor2X−u，有A−h=ceilX−2u+v−1≥0；所以h≤A，允许等号，X≥8时A≥1。因此

\[
X^{-1}\sum_{X\le n\le2X}r_2(n-u)r_2(n-v)=C(h)+o(1)
\]

uniform in不同c,d。上节tail及fixed-modulus distribution convergence，与两指数审计相同的finite-divisor/2-adic truncation，给

\[
\lim_{X\to\infty}\frac1{M_X^2}\sum_{c\ne d}C(|2^c-2^d|)
=\|f_\infty^{(2)}\|_2^2=16\mathcal R_2.
\]

## 3. Diagonal的精确常数

**PROVED.** Borwein–Choi2003 Eq.(3.14)给

\[
A(T):=\sum_{1\le n\le T}r_2(n)^2
=4T\log T+4\alpha T+O(T^{2/3}).
\]

对任意u≤X/2，令t=u/X∈[0,1/2]，端点floor/ceil误差可吸收到O(X)中，并有

\[
\begin{aligned}
\frac1X\sum_{X\le n\le2X}r_2(n-u)^2
&=4\log X\\
&\quad+4[(2-t)\log(2-t)-(1-t)\log(1-t)]+4\alpha+O(X^{-1/3})\\
&=4\log X+O(1),
\end{aligned}
\]

最后O(1)对所有u≤X/2统一，因为t处于固定compact interval。实数X的floor/ceil及端点重复修正由r₂(m)²≪εm^ε给Oε(X^(−1+ε))，取固定ε<2/3即吸入上述O(X^(−1/3))；主项端点的改动O(logX/X)也更小。于是diagonal总贡献

\[
\frac1{M_X^2}\sum_{c\in H_X^{(2)}}
\frac1X\sum_{X\le n\le2X}r_2(n-2^c)^2
=\frac{4\log X+O(1)}{M_X}\longrightarrow4\log2.
\]

与offdiagonal合并，

\[
\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}Z_X^{(2)}(n)^2
=4\log2+\|f_\infty^{(2)}\|_2^2.
\]

## 4. Mixed moment及结论

**PROVED.** 固定q，annulus内每个modq lattice coset的计数误差为O_q(√X)，对u≤X/2统一；故与两指数情形一样，

\[
\lim_{X\to\infty}\frac1X\sum_{X\le n\le2X}Z_X^{(2)}(n)f_q^{(2)}(n)
=\|f_q^{(2)}\|_2^2.
\]

固定周期函数(f_q^(2))²的整数平均也趋该norm。展开平方即得定理中的exact identity，再由L² martingale convergence令j→∞。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 更一般，任一固定q-periodic实函数F的极限误差为

\[
4\log2+\|f_\infty^{(2)}\|_2^2-\|f_q^{(2)}\|_2^2
+\|F-f_q^{(2)}\|_2^2\ge4\log2.
\]

因而任意一列periodic predictors，只要每个period先固定再令X→∞，都不能使这一weighted mean-square误差趋0。未排除period与X共同增长的其他极限，也未排除不同统计量的近似。

## 5. 文献及与本题的关系

**PROVED.** 唯一深输入是已全文核查的Chamizo2022 uniform shifted-correlation及Borwein–Choi2003 diagonal主项；Romanoff series、local kernels和全部limit steps在此有自含推导。完整原文信息：Fernando Chamizo, *Mediterr.J.Math.*19(2022),44, DOI10.1007/s00009-021-01959-3；Jonathan M.Borwein and Kwok-Kwong Stephen Choi, *RamanujanJ.*7(2003),95–127, DOI10.1023/A:1026230709945。

**UNRESOLVED.** 这一negative comparator不否定A303656的R1-b：那里M_X≈log²X，diagonal为O(1/logX)并消失。也未断言single-base representable set的精确density；下节只证明upperdensity≤1/2，不能将其误写成density恰为1/2。

## 6. 单幂base2的upper density至多1/2

**PROVED NEGATIVE STRUCTURAL THEOREM.** 设
\[
\mathcal T_2=\{n\ge0:n=m+2^c,\ m\in S2,\ c\ge0\}.
\]
则
\[
\overline d(\mathcal T_2)\le\frac12.
\]

证明。固定K≥1。有限并
\[
E_K=\bigcup_{0\le c<K}(S2+2^c)
\]
的自然密度为0，因为S2自然密度为0。其余表示均有2^c≡0(mod2^K)，所以n mod2^K必须在
\[
\mathcal N_K=\{a^2+b^2\bmod2^K:a,b\in\mathbb Z\}
\]
中。下面直接核查
\[
|\mathcal N_K|=2^{K-1}+1.
\]
除0及2^{K-1}这两个classes外，一个非零class写成2^v u，0≤v≤K−2、u奇数；它是norm class当且仅当u≡1(mod4)。必要性来自除去a,b共同的2-power后，a,b或恰有一个奇数，或均奇数；前者的norm oddpart为1(mod4)，后者的norm除2后为1(mod4)。充分性：u≡1(mod8)是2-adic square，u≡5(mod8)时u−4是2-adic square；再用2(a²+b²)=(a−b)²+(a+b)²乘上2^v。所用“1(mod8)有square root”可逐级提升：若a²≡u(mod2^j)、j≥3，则a或a+2^{j−1}恰有一个满足下一级同余。K=1,2直接核查。故classes总数为
\[
2+\sum_{v=0}^{K-2}2^{K-v-2}=2^{K-1}+1
\]
（K=1时和为空）。由E_K密度0得
\[
\overline d(\mathcal T_2)\le
\frac{|\mathcal N_K|}{2^K}=\frac12+2^{-K}.
\]
最后令固定截断K→∞即得结论。这里的极限顺序是先X→∞、后K→∞；没有令有限并的个数随X增长。

**PROVED.** 上证只需要S2密度0，不必依赖Landau asymptotic的误差项。为自含起见，可如下证明该弱结论：对任意有限集合F⊂{p prime:p≡3(mod4)}，S2包含于每个v_p(n)为偶数的整数集合；CRT及有限valuation截断给该集合密度∏_{p∈F}p/(p+1)。由ζ(s)和L(s,χ₄)的Euler products，
\[
\sum_{p\equiv3(4)}p^{-s}
=\frac12\{\log\zeta(s)-\log L(s,\chi_4)\}+O(1)
\quad(s\downarrow1),
\]
其中prime-power terms统一可和，而L(s,χ₄)→π/4>0，故Σ_{p≡3(4)}1/p发散。因此上述有限乘积可任意小，推出S2自然密度0。



---

# 附录 H：Multiplicative chaos 与 Kesten–Stigum

**PROVED.** 下列两篇均已打开原始全文并核对指定定理，不是 abstract only。

| 完整引用及原始全文 | 精确 hypotheses、结论与本题接口 |
|---|---|
| Ofir Gorodetsky, Mo Dick Wong, *Multiplicative chaos measure for multiplicative functions: the L¹-regime*, arXiv:2503.10555v4，14 Sep 2025，Thm. 1.1、§2.4。[全文](https://arxiv.org/html/2503.10555v4) | **PROVED.** α 是 Steinhaus random multiplicative function：各 α(p) 独立、单位圆均匀，α(p^k)=α(p)^k。f 为确定的 multiplicative function，0<θ<1，并满足下列两组条件。定理对 R 上归一化 Euler-product measures 的区间积分给 L^r convergence，r∈[1,1/θ)∩[1,2]；limit 是非平凡 random Radon measure，a.s. full support、nonatomic。特别 f=1_S2（定义域正整数）、θ=1/2 满足条件，此时仅得 1≤r<2，不含r=2。 |
| Russell Lyons, Robin Pemantle, Yuval Peres, *Conceptual proofs of L log L criteria for mean behavior of branching processes*, Annals of Probability 23(3) (1995), 1125–1138，Thm. A。[作者全文，p.2](https://arxiv.org/pdf/math/0404083) | **PROVED.** Galton–Watson process 从 Z₀=1 开始，每个个体独立按同一个非负整数 offspring law L 生育；1<m=EL<∞，q 是 extinction probability，W=lim Z_n/m^n。则 P(W=0)=q、EW=1、E[L log⁺L]<∞ 三者等价。因此正性在 nonextinction 上成立；不允许删掉 branching structure 或忽略 extinction。 |

**PROVED.** 第一行的全部算术条件为

\[
\sum_{p\le t}|f(p)|^2=\theta\frac t{\log t}+E(t),\qquad
E(t)=o(t/\log t),\qquad\int_2^\infty\frac{|E(t)|}{t^2}\,dt<\infty,
\]

\[
\sum_p\left[\frac{|f(p)|^3\log^3p}{p^{3/2}}+
\left(\frac{|f(p^2)|^2}{p^2}+\sum_{k\ge3}\frac{|f(p^k)|}{p^{k/2}}\right)\log^2p\right]<\infty.
\]

**PROVED.** 其对象精确为

\[
A_y(s)=\prod_{p\le y}\sum_{k\ge0}\frac{\alpha(p^k)f(p^k)}{p^{ks}},\quad
\sigma_t=\frac12\left(1+\frac1{\log t}\right),\quad
m_{y,t}(ds)=\frac{|A_y(\sigma_t+is)|^2}{E|A_y(\sigma_t+is)|^2}\,ds.
\]

对每个有界区间 I、h∈C(I)，m_{y,∞}(h) 与 m_{∞,t}(h) 分别在 y→∞、t→∞ 时 L^r 收敛到同一 m∞(h)。

**PROVED.** 这里的随机性来自素数相位；积分变量 s 是实数。所谓 full support，指每个非空开区间均有正的极限质量；nonatomic 指单点质量为零。这两项分别限制支集与原子，并未陈述极限测度相对于实轴 Lebesgue measure 的 density 逐点为正。更不能把实轴、素数相位的概率空间，以及原题中的 profinite 整数空间混为同一个空间。f=1_S2 这一专例说明所用算术函数相关，却没有识别两个问题的极限对象。

**PROVED.** 第二行的零质量精确等于 q；若 q>0，即使所有矩条件满足，仍有正概率 W=0。该定理把均值是否保留与生育律的矩条件联系起来，所用独立后代树是实质假设。本题的 exponent pairs 没有由此文提供的生育律，也没有可直接对应的 extinction event。仅把一个非负 martingale 称作 branching process，不会建立这种对应。

**UNRESOLVED.** Feed P/B：前者给实频率轴上的随机 measure，后者给 branching martingale；两者都不是本题 Haar(Ẑ) 上的确定 density limit。Full support 与 nonatomic 本身不保证对 Haar 有严格正 density，LPP 的 L log L 条件也不能替代尚未构造的 branching law。本题仍须证明自己的 Hellinger series 收敛，或建立可核的对象与假设对应。

LPP 作者 errata https://rdlyons.pages.iu.edu/errata/k-s.pdf 修正的是 Theorem C(ii)，不涉及本文所用 Theorem A。



---

# 附录 I：Direct profinite literature screening

## 1. Demangos–Longhi 2024

**PROVED.** Luca Demangos, Ignazio Longhi, *Densities on Dedekind domains, completions and Haar measure*, Mathematische Zeitschrift **306**, Article 21 (2024), published9January2024, DOI10.1007/s00209-023-03415-2。出版入口 https://link.springer.com/article/10.1007/s00209-023-03415-2 （期刊版abstract only）；作者final version arXiv2009.04229v6,13December2023，41页全文 https://arxiv.org/html/2009.04229v6 。作者版§4.4、§6.2 已核。

**PROVED.** Theorem4.19（作者版p21）给出不要求prime independence的density=measure iff，但其结论不是density function positive-a.e.。D是global Dedekind domain；d=(d⁺,d⁻)满足§4.2.1的七条density axioms（归一、上下界、单调、互补、有限sub/superadditivity、translation invariance、ideal coset密度）。T是supernatural ideals空间中以0为accumulation point的子集；X⊂Dⁿ；X_σ是X在D̂/σ投影之closure的inverse image。若每个σ∈T有d(X_σ)=Haar(X_σ)，则

\[
d(X)\text{ exists and }d(X)=Haar(\overline X)
\quad\Longleftrightarrow\quad
\lim_{\sigma\to0}d^+(X_\sigma\setminus X)=0.
\]

**PROVED.** 最易直接核对的Z特例：令A⊂Z，A_j={n∈Z:n mod j!∈A mod j!}，d⁺、d⁻取ordinary upper/lower density，则lim_j d⁺(A_j\A)=Haar(closure A)−d⁻(A)。所以finite saturation的tail gap是必须证明的条件，不能由有限同余覆盖本身抹去。

**PROVED.** Proposition6.18（作者版pp37–38）的Poonen–Stoll形式：S_j为穷尽所有prime ideals的递增有限集；U_p⊂D̂_pⁿ满足Haar_p(∂U_p)=0，X=Dⁿ∩∏U_p。如果

\[
\lim_jd^+\!\left(\bigcup_{p\notin S_j}(D^n\setminus U_p)\right)=0,
\]

则d(X)=∏Haar_p(U_p)。没有假定“local factors positive⇒product positive”；结论的product允许为0。

**UNRESOLVED.** FeedP/C，但本题没有上述arithmetic tail estimate，而且R1-b的f∞是weighted convolution density，不能直接视作一个set closure的indicator。Theorem4.19确实不要求X为product set，却把所缺的全局尾部误差明确放进hypothesis；它不填补(POS)，不逃N-009。

## 2. Demangos–Longhi–Saettone 2026

**PROVED.** Luca Demangos, Ignazio Longhi, Francesco Maria Saettone, *Procounting measures and the Bateman–Horn conjecture*, arXiv2606.29250**v2**,29September2026，50页。原PDF https://arxiv.org/pdf/2606.29250v2 已正常下载并读相关全文，作者版全文已核，非 abstract only。作者站旧标题稿 https://www.fmsaettone.com/pdls.pdf 是不同版本，不混用其numbering。

**PROVED.** Proposition2.43（v2 p19，已视觉核closure bars）：ambient profinite X的finite quotients满足每个transition map的fibres等势（Eq19），实数系数；µ_X是相容uniform quotient measures的极限。若S⊂X且µ_X(closure S)>0，则其procounting measure存在并且

\[
\mu_S=\frac{1_{\overline S}}{\mu_X(\overline S)}\,\mu_X.
\]

这仅给closure上的normalized restriction，仍允许其补集上density=0；µ_X(closure S)>0已在hypothesis中。

**PROVED.** Theorem3.3（v2 p26）：nonempty openly Eulerian X⊂D̂ⁿ，即closure X=∏X(p)，各X(p)compact open，则

\[
\mu_X=\bigotimes_p \frac{1_{X(p)}}{Haar_p(X(p))}\,Haar_p.
\]

即使∏Haar_p(X(p))=0，这个product probability measure也存在；例如X=D̂* gives normalizedHaar on the unit group，which is singular to additiveHaar。因此这里避免的是real Euler-product收敛问题，不是证明对additiveHaar的positive density。

**PROVED.** Proposition4.8（v2 pp44–45）仅将2024的tail criterion相对化：µ_Y须存在；relative density d_Y须满足(DnY1–6)，特别每个ideal coset C的d_Y(Y∩C)=µ_Y(closure C)。若X⊂Y且X_a=Y∩π_a^{-1}(π_a(X))满足lim_{a→0}d_Y⁺(X_a\X)=0，则d_Y(X)=µ_Y(closure X)。对自然counting ratios，coset equidistribution (DnY6)不是自动成立的。

**UNRESOLVED.** Conjecture1.2/3.25仍是profinite Bateman–Horn conjecture：prime-value set的procounting limits存在及与local model一致都属于所猜部分。本文没有给A303656 weighted ν=µ_shift*η的procounting identification，也未给非product arithmetic profile positive-a.e. theorem。只宜screened备注，不新增主表。



---

# 附录 J：版本与 counterexample audit

## 1. Banerjee：相近题名不等于 A303656 的 partial result

**PROVED.** Soumyarup Banerjee, *On a conjecture of Sun about sums of restricted squares*, Journal of Number Theory 256 (2024), 253–289, DOI [10.1016/j.jnt.2023.09.004](https://doi.org/10.1016/j.jnt.2023.09.004)。[arXiv:2202.04057v1](https://arxiv.org/pdf/2202.04057v1)，8 February 2022，25页全文已取得；期刊37页版本未取得，**abstract only**。作者 [publications page](https://sites.google.com/site/soumyarupbanerjee190490/publications)也链接此 arXiv 版本。

**PROVED.** 原文研究的 Sun conjecture 是 S2+(2^a3^b)^2+(2^c5^d)^2（OEIS A308734），与原题的 additive shifts 3^c+5^d 不同。其 existence statements 允许 extra almost-prime factors，不能删去这些 factors 后引用为 A303656 的结果。Feed A/V：只作来源筛查。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 2022 preprint Thm.1.1 的附加 quantitative lower bound 在其印出的全范围内不成立：它声称，对所有充分大且非4^q(8ℓ+7)的 m，m=x²+y²+(2^az)²、a≥0、z具有至多118个 prime factors 的表示数至少 c m^{1/2−ε}/log m。取 m=4^k，令 w=2^az。因平方 modulo4 只有0、1，x²+y²+w²≡0 mod4 强制三个变量都为 even。反复下降至1，所有 triples 都是 (±2^k,0,0) 的 permutations，故 r₃(4^k)=6。由于 almost-prime z 非零，w非零，于是 x=y=0、z=±2^{k−a}，且0≤k−a≤118。即使逐(a,z)计数，最多238种。固定0<ε<1/2后，声称的下界随k发散，矛盾。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 同页 Eq.(1.2) 中未经剥离4-part的 r₃(m)≫m^{1/2−ε} 是这个反例直接击中的式子。此检验只否定该 preprint 的 uniform quantitative statement；它没有否定 existence 部分。

**UNRESOLVED.** GAP：未获得2024期刊全文，不能判断其是否已更正该范围，也不能据此宣布正式发表版本错误。报告不把这条未核 quantitative statement 当作任何正向输入。

## 2. Xu–Chen 2026：明确标注 abstract only 的 covering 近邻

**UNRESOLVED.** Ji-Zhen Xu, Yong-Gao Chen, *On integers not of the form p+2^{a²}+2^{b²}*, Periodica Mathematica Hungarica 93 (2026), 127–130，online25April2026，DOI [10.1007/s10998-026-00717-w](https://doi.org/10.1007/s10998-026-00717-w)。[官方页](https://link.springer.com/article/10.1007/s10998-026-00717-w)为 **abstract only**；公开 bibliography 可读，11项 references 没有 Radomskii2504.09954。摘要称：若一个 odd arithmetic progression 完全避开 p+2^{a²}+2^{b²}（p prime，a,b≥1），则 step m≥510 且 ω(m)≥4，两界均 sharp。本报告未核其全文证明，故不把这两条最优性结论标成已审计的定理输入。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 可独立证明示例 n≡293 mod510 全部不可表示，不需依赖未开放的证明。它给 n≡2 mod3、3 mod5、4 mod17。若 a,b 都 even，则两幂之和为2 mod3、2 mod5，residual 被3整除，却为1 mod5，不能等3。若一奇一偶，则和为3 mod5，并且为1或3 mod17，residual 被5整除，却为1或3 mod17，不能等5。若两者都 odd，则和为4 mod17、1 mod3，residual 被17整除，却为1 mod3，不能等17。n odd 又排除 residual prime2；负 residual 不可能是 prime。故无表示。

**PROVED.** Feed C/E：机制依赖 exponent-square residues。将 exponents 改成 unrestricted 时，293=5+2^8+2^5，已经不在同一 exclusion mechanism 中。该文不是 Radomskii 的已核 forward citation。

## 3. Basta 2025：真实卷积恒等式不解决 positivity

**PROVED.** Oussama Basta, *A Convolutional Characterization of the Sun-OEIS A303656 Conjecture*, author-uploaded preprint，12 September 2025，DOI [10.13140/RG.2.2.16902.64323](https://doi.org/10.13140/RG.2.2.16902.64323)，[作者上传全文](https://www.researchgate.net/publication/395445233_A_Convolutional_Characterization_of_the_Sun-OEIS_A303656_Conjecture)。网页提供五页完整文字，本次已读；非 abstract only。其按(c,d)分类得到的 T(n)=Σr(n−3^c−5^d) 是正确的有限计数恒等式，其中r计0≤a≤b的二平方表示。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 后续 explicit formula 混淆 ordered nonnegative count 与 signed integer count：它先定义r₂(1)=#{(a,b)∈Z≥0²:a²+b²=1}=2，随后 divisor formula 却给4。代入其最终式，n=3 仅有(c,d)=(0,0)、residual1，预测T(3)=4/2=2，而真实T(3)=1。这是直接 normalization counterexample。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 文中声称 Σ_{x∈Z}exp(ix²θ) 在一般实θ处通常收敛，也不满足级数各项趋零的必要条件；通常的 theta identity 需要绝对收敛区域或指定的 regularization。

**UNRESOLVED.** 即使修正上述计数，正确恒等式本身没有证明T(n)>0。Feed V：该文不作为 A303656 已解决或 positivity 输入的证据。

---

=== RESULT CARD ===
Lane / variant: L / Literature deep search；原文核验、R1-b weighted L² 审计与 positivity 接口。
Headline (one sentence): 完成 R1-b 的全部极限步骤，并把尚未解决的 almost-all 问题精确留在 arithmetic Hellinger summability。
Strongest claim + tag: R1-b 的 fixed-level exact norm identity — PROVED。
Precise statement of that claim: 对题目给定 H_X、Z_X、μ_q、β_q、f_q 及 q_j=j!，f_{q_j}→f∞ in L²(Ẑ)及 a.e.，积分为π；对每个固定j，lim_{X→∞} X⁻¹Σ_{X≤n≤2X}|Z_X(n)−f_{q_j}(n mod q_j)|²=||f∞||₂²−||f_{q_j}||₂²，故先X后j的 double limit 为0。
Where it breaks / GAP (if any): 该 weighted L² identity 的证明未留 GAP；无条件 almost-all 仍缺 (POS)，即相应 Hellinger series 的 Haar-a.e. summability，并须处理可能的 finite-level zeros；every n 的 pointwise 保证更未获得。
Nearest closed theorem, and why it does not apply: N-001 的 L²≠adversarial L∞ 限制仍适用；N-010 关闭 pointwise minor-arc route，本证明只用 n-average shifted correlations；N-009 不允许由 finite/profinite consistency 选择单个 exponent pair，本报告没有作此推断。
What a verifier should check first (3 items): 1. 排除数值零差后的共同乘积 Q_X 与 composite-divisor tail；2. Chamizo C(h) 的2-adic factor、h≤A窗口及 LTE collision/diagonal normalization；3. fixed-q mixed moment、可积 majorant 与 Hellinger criterion 的测度方向。
Suggested next step for another session: 先独立重放 R1-b 的 tail 与 norm identification，再以已显式确定的 f120 为初始 profile，只研究加入其他 prime coordinates 的 Hellinger increments 或真实 zero set，保留共享 exponent-period constraints。
=== END CARD ===
