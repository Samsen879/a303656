# V / R1-b / R1-c 独立交叉审查

## 裁决

已审阅 V 报告的 Sections 2–4、7.1–7.6，并独立重建主要估计。R1-b 的 weighted full-domain integer L² transfer 可接受。R1-c 的准确形式为 POS ⇒ almost-all；该 implication 可接受，POS 尚未证明。未发现这两项的 decisive gap。

## 精确定理

取 ordered signed r2，r2(0)=1，负数处为零，定义 W(n)=|D(n)|^{-1} Σ_{(c,d)∈D(n)} r2(n−3^c−5^d)。W(n)=0 iff R(n)=0。

对每个固定 q，

lim_{X→∞} X^{-1} Σ_{X≤n≤2X}|W(n)−f_q(n mod q)|² = ||f∞||²_2−||f_q||²_2.

进一步令 q=j!→∞，右边趋零。由 weak convergence 或固定正阈值的 Chebyshev estimate，

limsup_X X^{-1} #{n∈[X,2X]:R(n)=0} ≤ Haar{f∞=0}.

只要 POS 成立，dyadic 与 natural-density almost-all 均成立。

## 已核对证明组件

1. Chamizo 原始来源：https://link.springer.com/article/10.1007/s00009-021-01959-3，Theorem 1.1。精确 main term 为 8κ2(h)σ_{−1}(odd h)，κ2(h)=1 for odd h，κ2(h)=2−3·2^{-v2(h)} for even h。代 θ=7/64，在 1≤h≤x 得 uniform error Oε(x^{71/96+ε})。V 的两个 dyadic endpoints 均为 Θ(X)，且显式满足 h≤lower endpoint，故引用范围合法。
2. Numerical collisions：3^c(3^u−1)=5^d(5^v−1) 决定 c=v3(5^v−1)、d=v5(3^u−1)。故 L3×L5 rectangle 的 ordered collision count <3M。Diagonal weighted contribution O(log X/M)=o(1)。
3. 所有 composite divisors（含 prime powers）的 Romanoff series Σ_{(m,5)=1}1/[m ord_m(5)] 收敛。对 ord≤T 的 m，全都整除 Π_{k≤T}(5^k−1)，倒数和 O(log T)，Abel summation 即证。Non-coprime 5-part 可分离为几何级数。
4. Empirical congruence error 1/L5 的 tail 处理保持合法顺序：固定 Y,δ，X→∞，再δ↓0，再Y→∞。没有把随δ增长的 divisor bound 常数视为uniform。
5. β_q compatible；μ_q 由完整 eventual powers 的 joint pushforward 给出 compatible marginals。它通常不按 primes factor。Local autocorrelation kernel 是 β_q 的 Fourier squared magnitude；odd-prime positive divisor expansion 和 2-adic factor与Chamizo main term一致。
6. β_q first moments 由 fixed-q lattice count 给出，无需 primes-in-progressions theorem。Martingale norm C 与 integer second moment C 相同，混合矩因此产生 exact variance identity。
7. Curved domain 与 full D(n) 只有 O(log X) 条额外指数对。每条 shifted r2 的 normalized L² norm O(sqrt(log X))，除以 M≈log²X，Minkowski 给出 O((log X)^−1/2)。这实际控制了weight，不只比较unweighted symmetric difference。

## Zero 与 transient 的精确解释

令 q†=2^{v2(q)} Π_{p≡3 mod4}p^{2 floor(vp(q)/2)}，Cq=2 floor(v3(q)/2)。由local norm support，f_q(a)=0 iff f_{q†}(a)=0。Split-prime β 始终positive，odd inert prime-power exponent 的support可降至前一even exponent。

若f_q(a)=0，则 n≡a modq† 的所有actual witness必须满足 c<Cq。无需d-transient：5是split因子，被support reduction删去。若v3(q)≤1，则Cq=0，该residue class中所有n>1都是真正整数反例。若v3(q)≥2，有限多个ordinary c rows仍可能补齐整数；eventual obstruction本身不排除它们。

## 不可传播的推论

* weighted transfer 不能替代 W6 的 unweighted SM；W与indicator的normalization及moments不同。
* weighted weak convergence只给exceptional upper bound。Positive W(n)可趋0；整数性只提供约log^{-2}n级别下界，亦趋0。converse与indicator saturation仍open。
* LP⇒POS需要A2的额外zero-set theorem。反向POS⇒LP由nonnegative conditional expectation成立。若A2通过，则LP iff POS，但仍只给almost-all，尚无every-n证明。
* 删除split-prime coordinates仅可用于zero-set reduction，不能用于weighted L² profile。V给出||F−F^-||²≥7π²/200；可由f20与f4的精确方差差验证。

## 独立 exact computation

* 368个(p^a,t) autocorrelation identity检查全部通过，p∈{2,3,5,7,11}。
* ||f20||²/π²=207/200，min f20/π=4/5。
* min f120/π=7/15，||f120||²/π²=107/96；以完整eventual periods枚举，未使用prime-wise independence。
* 1722个residues验证p=3,7,11上odd exponent support降到even exponent。
* 10×7,30×20,100×70,300×210 exponent rectangles的collision energy分别为M+2，验证结构但未作为无限证明。

## 后续 gate

R1-b/R1-c无需再次大规模计算。下一份独立referee只需按上述7项做line map与primary-source范围检查。核心未决目标是A2相同μ/β/filtration的zero-set theorem及LP。任何LP反例须附(q,a) exact joint-cycle certificate，再对Cq个ordinary c rows逐一审查，才能升级为integer obstruction。
