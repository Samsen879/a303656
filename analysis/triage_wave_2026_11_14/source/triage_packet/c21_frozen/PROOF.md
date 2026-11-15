# A303656 R2 — Frozen certificate C21

## 1. 结论

**PROVED.** 在 eventual-power model 的 exponent space \(E=\widehat{\mathbb Z}^{,2}\) 中，设 Q、T 是不交的有限 odd inert prime sets，每个 \(q\in Q\setminus\{3\}\) 至少对 base3 或 base5 regular，且 \(|T|\le21\)。给定：

- 每个 \(q\in Q\) 的任意有限 norm precision \(k_q\ge1\) 和 target residue；
- 任意有限 \(2^a\) norm condition；
- 每个 \(p\in T\) 的任意 residue \(z_p\pmod p\)；

则存在 positive-Haar-measure clopen exponent set，同时满足所有 norm conditions，且 \(s(e)\ne z_p\pmod p\) 对每个 \(p\in T\) 成立。

**PROVED NEGATIVE STRUCTURAL THEOREM.** 因此，若某个 finite eventual-power density \(f_q(a)=0\)，则 q 至少含有二十二个不同的 inert primes p，且每个满足

\[
p^2\mid q,\qquad s_3(p)\ge2,\qquad s_5(p)\ge2.
\]

本 certificate 固定 target budget 为21、order cutoff 为512，不继续扩大参数。该结论是有限 eventual-power obstruction 的必要条件；它没有证明 LP、POS 或原整数猜想。

## 2. 分析工具：regular averaging 与 parity

**PROVED.** 对至少一个 base regular 的 inert norm prime q，在其余 norm primes 都小于 q、所有额外 target events 不依赖 q-primary exponent components 时，积分消元满足

\[
\frac1q\int W\mathbf1_A\,d\lambda
\le\int W\mathbf1_A\beta_{q^k}(x_q-s(e))\,d\lambda
\le(1+1/q)\int W\mathbf1_A\,d\lambda.
\]

所选 regular base 的 q-primary component 在固定 mod-q additive ball 内 Haar；局部平均为 \(\beta_q\)，其值处处介于 \(1/q\) 与 \(1+1/q\)。因此删除或恢复该因子保持 positive mass。这里没有把平均误写成1。

**PROVED.** Prime3 condition 可以通过 beta parity 强化为 residual unit：

\[
T_3(\alpha)_3=0,\qquad T_5(\beta)\bmod3=(-1)^\beta.
\]

Q、T不交，prime3至多出现一个条件，所以总可选择一个 parity 避开它的 residue。该步骤不约束任何 odd exponent component。

任意 finite 2-norm condition 都与任一 beta parity 相容。条件于 beta even/odd，shift分别在 mod8 classes `{2,4}` 或 `{6,0}` 内均匀，每个class内部Haar。与

\[
\beta_8=(1,2,2,0,1,2,0,0)
\]

卷积，得到处处正的两个vectors：

\[
(1/2,1,1/2,1,3/2,1,3/2,1),\quad
(3/2,1,3/2,1,1/2,1,1/2,1).
\]

高precision为pullback，低precision为conditional expectation。因此可以固定一个positive-measure允许的2-primary cylinder，并保留全部odd components独立Haar。以下全部概率界对任意已固定的两个parities一致成立。

## 3. 每个prime的统一局部概率界

**PROVED.** 对 p>3 的 inert prime，令

\[
h_{3,p}=\operatorname{oddpart}(\operatorname{ord}_p3),\quad
h_{5,p}=\operatorname{oddpart}(\operatorname{ord}_p5),\quad
H_p=\max(h_{3,p},h_{5,p}).
\]

因为 \(v_2(p-1)=1\)，固定alpha、beta parity后，两个powers分别在

\[
3^{\varepsilon_3}\langle3^2\rangle,\qquad
5^{\varepsilon_5}\langle5^2\rangle
\]

上独立均匀，两个cosets大小分别为 \(h_{3,p},h_{5,p}\)。因此任意target equality的概率至多 \(1/H_p\)。不同primes之间不要求独立。

只对以下三枚primes使用更精确的uniform bound；其余一律使用 \(1/H_p\)：

| p | h3 | h5 | 每个parity pair、每个target的最大solution count | 统一概率上界 |
|---:|---:|---:|---:|---:|
| 11 | 5 | 5 | 3 | 3/25 |
| 71 | 35 | 5 | 4 | 4/175 |
| 271 | 15 | 27 | 5 | 1/81 |

`certificate.json`含四个parity pairs各自全部target residues的solution-count vectors。`verify.py`采用set intersection独立重算：对每个z，计算 \(\#\{x\in A:z-x\in B\}\)。需要检查的pair spaces仅25、175和405。

记上述统一上界为 \(\bar w_p\)。所有未列入有限order inventory的primes将使用 \(1/512\) 作为上界。

## 4. 一个完整catalog覆盖所有需要的order classes

**PROVED.** 取

\[
S=\{h<512:h\text{为odd，且所有prime factors}\le19\}.
\]

S恰有80项。定义

\[
P_3=\prod_{h\in S}(3^{2h}-1),\quad
P_5=\prod_{h\in S}(5^{2h}-1),\quad G=\gcd(P_3,P_5).
\]

若某个inert p>3满足两个base orders的全部prime factors不超过19、且 \(H_p<512\)，则两个odd orders属于S，从而p同时整除P3、P5，因此p整除G。

`certificate.json`给出P3、P5的完整十进制整数、G的完整60-prime factorization，以及整数A、B满足

\[
A(P_3/G)+B(P_5/G)=1.
\]

连同 \(G\mid P_3,P_5\)，这个Bézout identity认证G确为完整GCD。各factor均由deterministic trial division认证为prime。筛除split factors后，完整eligible inert catalog有46枚primes；每一行附exact orders、h3、h5、H及 \(P^+(L_p)\)。Verifier以direct modular iteration重算exact orders，独立于探索阶段的order-by-division算法。

这不是对prime大小作截断的搜索。任意未在catalog中的相关prime必有 \(H_p\ge512\)，所以其uniform probability不超过 \(1/512\)。对于最大order prime为7、11、13、17的子类，只需按exact orders筛选这个完整catalog。

## 5. Top-k预算定义及未知尾项

**PROVED.** 设

\[
L_p=\operatorname{lcm}(\operatorname{ord}_p3,\operatorname{ord}_p5)\quad(p>3),\qquad L_3=2.
\]

对M取7、11、13、17或19，定义：

- \(C_M=\sum_{7\le q\le M,\ q\equiv3\ (4)}\bar w_q\)。
- \(A_M(k)\)：所有catalog内 \(p>M\)、\(P^+(L_p)=M\) 的weights，连同无限多个 \(1/512\) 占位值，取最大的k项之和。
- \(I_M(k)\)：所有catalog内 \(p>M\)、\(P^+(L_p)<M\) 的weights，连同无限多个 \(1/512\) 占位值，取最大的k项之和。

只需实际放入k个尾部占位值，因为top-k最多使用k项。这个处理不会漏掉未知prime，也不会把未知tail误当空集。

所有core primes q<=M的norm condition均可加强为unit condition；若某core prime本身是inactive target，则因为Q、T不交，那里没有重复的norm condition。因此每个core prime至多对应一个bad event，C_M统一覆盖它们。prime3已由parity处理。

## 6. 完整归纳与29个有限不等式

**PROVED.** 对最多21 targets，按

\[
M=\max_{p\in T}P^+(L_p)
\]

归纳，空T使用regular local positivity。

### Base：M<=7

删除q>7的regular norm factors。prime3/parity与2-norm按前述处理。prime7若是norm或target，用C7统一覆盖；其余targets均p>7、orders为7-smooth，最多21枚。总bad mass由C7加该类别top-21 budget控制，certificate给出

\[
\frac{622242277}{762048000}<1.
\]

### 一般fresh-fibre步骤

先删除q>M的norm factors。令 \(T_M=\{p\in T:M\mid L_p\}\)，\(t=|T_M|\ge1\)，\(I=T\setminus T_M\)。

若M是剩余norm prime，从Q删除M，并加入unit target \(S_M\ne x_M\pmod M\)；否则不加。新target数

\[
|T|-t+\delta\le|T|\le21.
\]

新增target的orders整除M−1，故最大order prime严格下降。归纳得到lower choices后，所有这些条件不依赖M-primary components；每个active target在fresh fibre上的bad probability至多1/M。因此t<M时直接得到positive mass。

所有M>=23自动满足t<=21<M。剩下需要有限认证的只有

\[
M\in\{11,13,17,19\},\qquad M\le t\le21.
\]

### Critical direct budgets

在尚未对odd constraints作条件化的free Haar space上，同时union bound：

\[
\Pr(\text{任何bad event})\le C_M+I_M(21-t)+A_M(t).
\]

inactive targets中位于core的部分已被C_M覆盖；仍然使用21−t个outside slots只会使上界变松。active targets必p>M，且与inactive category不交。

Certificate逐一给出28个critical inequalities，加上basecase共29个。各M的最大预算如下：

| M | 最坏t | 最大bad-mass预算 |
|---:|---:|---:|
| 7 | base | 622242277 / 762048000 |
| 11 | 11 | 875703733 / 878169600 |
| 13 | 13 | 4550743 / 4612608 |
| 17 | 17 | 2622994487 / 2940537600 |
| 19 | 19 | 13525969 / 16755200 |

Verifier没有假设最大值一定出现在t=M；它检查所有28个t值。最小剩余质量为

\[
1-\frac{875703733}{878169600}
=\frac{2465867}{878169600}>0.
\]

固定任意允许的2-primary参数后，全部critical cases都留下positive odd-Haar mass。所有约束由finite exponent quotients决定，故得到clopen positive mass。恢复先前删除的regular norm factors仍保持positive mass。归纳完成。

## 7. 二十二-root corollary

**PROVED NEGATIVE STRUCTURAL THEOREM.** 从finite density zero中删除处处正的split factors以及仅一次幂的inert factors。令T为余下joint-nonregular inert primes，Q为其余inert norm primes；p=3对base5 regular，故不在T。

若 \(|T|\le21\)，C21使所有Q-norm factors正、所有T-residuals为units、2-norm factor也正，且发生于positive clopen exponent set。原nonnegative integrand积分必正，与finite zero矛盾。故 \(|T|\ge22\)，且每个T-prime在原modulus中的exponent至少2。

这里没有使用prime inventory的大小上限，也没有从finite/profinite consistency选择一个ordinary integer exponent pair。它与N-009的scope边界保持一致。

## 8. 独立复核入口

**FINITE COMPUTATION.** 运行

```bash
python verify.py
```

不需要network、SymPy或预先提供的prime table。Verifier检查完整products、全部factor primality、Bézout identity、46行exact orders、三个小convolution的完整count vectors、所有top-k尾项和29个rational inequalities。输出写入`verification.json`。

**UNRESOLVED.** 此冻结certificate只证明21-target budget。它不排除22或更多targets，也不提供finite zero example。原作者的十一-root theorem可独立ACCEPT；C21是本轮另列的新强化结果。
