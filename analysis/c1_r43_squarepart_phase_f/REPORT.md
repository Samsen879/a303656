# A303656 C=1 r=43 terminal cofactor square-part closure — Phase F

## 0. 结论

**取得 C1806 的一侧严格缩减，没有取得 square-part closure。** 本轮从独立重建的 337 位 C1806 中找出一个 24 位素因子

\[
p_*=147304138944416276237689,
\qquad C_{1806}=p_*R_{1806}.
\]

p_* 已有递归 Lucas 素性证书；其 exact order 为 1806，p_*≡1 (mod 4)，重数恰为 1。剩余 R1806 是 314 位、1040 bit 的已证明合数。C903 仍为未进一步分解的 333 位合数。

这不是 A、B 或 D；也不满足用户 C 级中“两个 cofactor 都明显缩小”的完整要求。它是 C1806 的单侧 certified cofactor reduction。本文的 NO 都表示“本轮未证明关闭”，不是宣称存在实际 repeated admitted prime 或实际 B7 成员。

推荐执行环境：网页端 Pro 完成数学与 reference computation；普通 Codex CLI 仅用于今后独立重放/仓库集成。本轮未使用 Codex Ultra、未启动生产搜索、未修改 GitHub。

## 1. LIVE AUTHORITY / source custody

```text
Repository: Samsen879/a303656
Repository ID: 1333945235
Live main: fd59aad038a09f2fc6df7039111408fa231c27dd
Live tree: afd34fc936f83867758c827bfcd8b7b9d9b8d5b5
Latest main merge observed: PR #29, Phase D seven-head chain realizability
Commit timestamp: 2026-09-08T03:37:01Z
Read date: 2026-09-08
Final branch-list recheck: same main SHA
```

Live branch、PR list、analysis directory、Phase D B7 report 与最终 branch list 已只读读取。未发现 Phase E merged 主线或命名的 Phase E 分支。

**指定的两份 Phase E ZIP 并未出现在本会话可访问附件中。** 因此没有完成两份 ZIP 的完整阅读、内部 manifest/SHA256 校验、Phase E 既有 factor inventory 或 ECM 预算复核。不得把缺少原包说成已认证的 provisional ZIP authority。当前结果是独立、精确、自足的算术重建；下文的 C903/C1806 按显式商定义。它们与 Phase E 内部同名对象的字节级绑定仍为 NOT VERIFIED。

已读 live Phase D 报告将 r=43 三顶点情形压到 {301,602,903,1806}。用户说明 Phase E 已关闭 301、602；由于原包缺失，本轮没有独立复核这一后续缩减，也没有对这两个非目标 indices 开新分解任务。

Source reads:
- https://api.github.com/repos/Samsen879/a303656/branches/main
- https://api.github.com/repos/Samsen879/a303656/branches?per_page=100
- https://api.github.com/repos/Samsen879/a303656/pulls?state=all&per_page=12&sort=created&direction=desc
- https://api.github.com/repos/Samsen879/a303656/contents/analysis?ref=fd59aad038a09f2fc6df7039111408fa231c27dd
- https://raw.githubusercontent.com/Samsen879/a303656/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_b7_pure3_phase_d/REPORT.md

未进行 repository checkout、repository-native tests 或 Phase E 原始日志 replay。普通网页查找没有提供本轮采用的新 factor；Cunningham 当前标准 base-5 表的通常范围未给出本目标的分解，FactorDB 页面访问未成功。没有把未读数据库状态当作证据。

## 2. EXACT INTEGER RECONSTRUCTION

903=3·7·43，φ(903)=φ(1806)=504。Python Möbius product 与 SymPy cyclotomic polynomial evaluation 独立相符。另一个 C++/GMP 核验器从下面四项商直接重建，未读取 Python 的多项式结果来构造整数：

\[
N_{903}=\Phi_{903}(5)=
\frac{(5^{903}-1)(5^{43}-1)(5^7-1)(5^3-1)}
{(5^{301}-1)(5^{129}-1)(5^{21}-1)(5-1)},
\]
\[
N_{1806}=\Phi_{1806}(5)=
\frac{(5^{903}+1)(5^{43}+1)(5^7+1)(5^3+1)}
{(5^{301}+1)(5^{129}+1)(5^{21}+1)(5+1)}.
\]

以下十进制块中的换行仅用于排版，直接拼接各行。

### Exact Phi903(5)
```text
2367545376743472677614360002430103327622699626677573385410789327713735
7204050161711973822722911350859474206712335504250104078587279811986095
6924765968840270085750096664061970848090142605476290205359395447984689
3526283233818141972683560353552956636484878667682660111208435695321091
9325075423291311210659755386400728007760790433167129531517505645749531
281
```

### Exact Phi1806(5)
```text
1603862120009651811878099868258765876159724170757724092049259565350973
6978635735993953718651068293725342390117820910828174260852228001367143
3343008218485642377901848508116281355298025148945352126995887678493863
6875780948034197539974718428587253885526819214720699319848733722693012
3017463716806478248944564597646030015294400300263077169646739959718437
521
```

## 3. EXACT C903

本轮定义：
\[
C_{903}=N_{903}/(149930509\cdot1562986310551).
\]

```text
1010306441268070857927899935832457293034371824218021175302869215498350
3086177467392042116873512967318971727250450422148707502135815935306541
5181569382565364022938831598360694535351296694485498987615098294119068
0324036514913688412079048500087739219756155494812039202408283368226035
90479976023291492013089930864003055507467966263143859
```

## 4. EXACT C1806

本轮定义：
\[
C_{1806}=N_{1806}/(43\cdot246201060546547).
\]

```text
1514986125047178530961655792622005860757220693588983158202273792599438
0170900553418841687663841979580674757733923316551419998722525982009309
4874128023252206737600850159101571049382512561585004460979140586299261
3591317132690934042598922195534487166571258332216885974893212107831027
050196061265964044957215240017423153454135912753818616001
```

| Integer | Decimal digits | Bit length | Status |
|---|---:|---:|---|
| N903 | 353 | 1171 | Composite, explicit factors |
| N1806 | 353 | 1171 | Composite, explicit factors |
| C903 | 333 | 1103 | Composite; Fermat base-2 witness |
| C1806 | 337 | 1117 | Composite; Fermat base-2 witness and fresh split |
| R1806 | 314 | 1040 | Composite; Fermat base-2 witness |

全部十进制、hex、位数、digits、十进制无换行 SHA256、Fermat residue、isqrt 和 gcd 在 `arithmetic_audit.json` 中。N*.txt、C*.txt、R1806_after_new_factor.txt 是可直接作为程序输入的单行十进制。

## 5. KNOWN FACTORS / MULTIPLICITIES / FRESH FACTORIZATION

| Divides | Prime factor | q mod 4 | Exact order of 5 | Multiplicity in N_n | Role |
|---|---:|---:|---:|---:|---|
| N903 | 149930509 | 1 | 903 | 1 | Reconstructed factor |
| N903 | 1562986310551 | 3 | 903 | 1 | Reconstructed admitted, regular |
| N1806 | 43 | 3 | 42 | 1 | Order-loss exception, not order-1806 root |
| N1806 | 246201060546547 | 3 | 1806 | 1 | Reconstructed admitted, regular |
| C1806 | 147304138944416276237689 | 1 | 1806 | 1 | Fresh split of reconstructed C1806 |

前四个因子是在本轮独立重建过程中得到，并没有证明它们相对 Phase E 是新发现。第五个是本轮对已经固定的 C1806 的新增 exact split；由于 Phase E 原包缺失，不作“此前文献/Phase E 从未知晓该因子”的优先权断言。

新分解为
\[
\Phi_{1806}(5)=43\cdot246201060546547
\cdot147304138944416276237689\cdot R_{1806}.
\]

其 discovery log 为 `ecm1806_tier2b.log`，零起始 curve 47，Suyama σ=810047，B1=100000，nominal B2=5000000；stage-two gcd 返回 p_*。同一条曲线已经单独重放，见 `fresh_factor_replay.log`。

本程序的分段 stage-two coverage 会略越过 nominal B2。该曲线实际枚举的 stage-two primes 在 [100000,5001312)；D=2236。报告没有把 nominal B2 当成严格最后一个 prime。完整界、每条已完成 σ、输入文件 SHA256 均见 `campaign_manifest.json`。

精确核验得到
\[
\gcd(p_*,R_{1806})=1,
\quad \operatorname{ord}_{p_*}(5)=1806,
\quad 5^{1806}\not\equiv1\pmod{p_*^2}.
\]

最后一个 residue 为
```text
18391195815313383399818446129464126673712252094
```
不是 1。每个已列因子均经 exact division、完整 prime certificate、proper-order tests、q² 模幂和商再除法核验，不依赖 ECM stdout 的素性标签。

## 6. PRIMALITY CERTIFICATES / INDEPENDENT VERIFICATION

五个显示的因子均为 **已证明素数**，没有以 probable prime 代替无条件素性证据。共 34 个递归 Lucas certificate nodes，从 2 开始。

对新因子 p_*：
\[
p_*-1=2^3\cdot3^2\cdot7\cdot13\cdot43
\cdot3719\cdot10709\cdot13127967973.
\]
Witness a=23。核验器证明上述分解各因子均素，乘积恰为 p_*-1，并核验
\[
23^{p_*-1}\equiv1\pmod{p_*},
\qquad
\gcd(23^{(p_*-1)/\ell}-1,p_*)=1
\quad(\ell\mid p_*-1,\ \ell\text{ prime}).
\]

证书正确性的简证：若 t 是 p_* 的任一素因子，上述 gcd 条件迫使 ord_t(23) 含 p_*-1 的每个完整 prime power，所以 p_*-1 | t-1，进而 t≥p_*，只能 t=p_*。递归节点使用同一判据，基础节点 2 直接认证。

核验路径：

1. `verify_python.py`：仅 Python 标准库，无 SymPy/gmpy2/primality oracle；验证 JSON 证书、Möbius reconstruction、乘积、proper-order tests、valuation、Fermat 合数见证、非平方见证与 congruence/size records。
2. `verify_native.cpp`：独立实现，使用 GMP；从四项商重建 N_n，读取另一种 TSV 证书格式，验证同一数学事实。

两条路径均已执行 PASS。另有六项 Python mutation rejection tests 和三项 native mutation rejection tests 全通过。两种实现出自同一会话/作者，不是独立作者审稿或 proof-assistant formalization。ECM discovery 与 verifier 的核心逻辑不同；同一曲线 replay 只算重放，不算第二个独立 factorization engine。

## 7. ACTUAL FACTORIZATION CAMPAIGN

本轮无法获知 Phase E 历史试除/rho/P±1/ECM 预算，故以下仅报告实际执行的本轮工作。

### 7.1 Exhaustive arithmetic-progression trial division

对 C903、C1806 分别穷尽检查
\[
a=1807+1806k\le10^{12},\qquad k\ge0.
\]

每个输入检查 553709856 个整数，包含全部该进程中的 primes，也包含 composite candidates；两次均无非平凡因子。利用下节的 exact-order theorem，这严格证明每个 prime divisor q>10^12。R1806 因 R1806|C1806 继承此结论。

原始日志 `trial903_1e12.log`、`trial1806_1e12.log`；代码 `trial.cpp`。这是真正的有限穷尽排除，不是由 ECM 无发现推测出的下界。

### 7.2 Pollard rho and P±1

| Method | Inputs | Bounds / seeds | Actual result |
|---|---|---|---|
| Brent-style Pollard rho | C903, C1806 | seeds 1,3; each requested 1000000 evaluations; actual 1000062 | gcd 1 throughout |
| P−1 stage 1+2 | C903, C1806 | B1=10^6, B2=10^7; bases 2,3,7 | all stage-1 and stage-2 gcds 1 |
| Additional P−1 stage 1+2 | C903, R1806 | B1=10^6, B2=10^8; base 2 | all gcds 1 |
| P+1 stage 1 | C903, C1806 | B1=10^6; P=3,4,16 | all gcds 1; stage 2 NOT RUN |

`methods_reference.cpp` and logs contain complete reproducible parameters. The rho count exceeds the requested cap by 62 because the reference loop completes its current block; actual work is explicitly logged and not rounded down.

### 7.3 ECM after fixing the normalized cofactors

| Input | B1 | Nominal B2 | Completed unique curves | Result |
|---|---:|---:|---:|---|
| C903 | 2000 | 100000 | 120 | no factor |
| C903 | 20000 | 1000000 | 100 | no factor |
| C903 | 100000 | 5000000 | 380 | no factor |
| C903 | 1000000 | 10000000 | 1 | no factor |
| C1806 | 2000 | 100000 | 120 | no factor |
| C1806 | 20000 | 1000000 | 100 | no factor |
| C1806 | 100000 | 5000000 | 68 | p_* found on last curve of second batch |
| C1806 | 1000000 | 10000000 | 1 | no factor |
| R1806 | 100000 | 5000000 | 120 | no further factor |

C903 totals 601 completed unique normalized-cofactor curves. C1806 totals 289; then R1806 has 120. A one-curve positive replay of σ=810047 is not added to the discovery totals. Reconstruction runs on larger initial integers are separately identified in the manifest and not counted in this table.

One C903 B1=100000 batch was interrupted after 11 completed curves; the remaining 9 were rerun and completed. The interrupted curve is not counted twice or labelled completed. Both the partial and resumed logs are retained.

The implementation is **custom C++/GMP reference ECM**, ported from SymPy 1.14.0 organization, not official GMP-ECM. Its source and license provenance are bundled. No NFS/SNFS run, no official GMP-ECM run, no claim of exhausting an expected factor-digit range, and no squarefree inference from negative ECM results.

## 8. SQUAREFREE ANALYSIS

### 8.1 Composite and not-square certificates

C903, C1806 and R1806 each fail the base-2 Fermat congruence. Full exact residues are in `arithmetic_audit.json` and independently reproduced in `verify_native.log`. A failed congruence is a rigorous compositeness witness, not a heuristic PRP label.

Furthermore,
\[
C_{903}\equiv3\pmod4,
\qquad C_{1806}\equiv R_{1806}\equiv5\pmod{13}.
\]

The square residues mod 13 are {0,1,3,4,9,10,12}; hence all three integers are nonsquares. **This only excludes an integer being a square; it does not exclude a proper square divisor.** No claim of squarefreeness follows.

### 8.2 Exact reductions for the square-part question

All displayed factors have valuation exactly 1 and are distinct. Consequently
\[
N_{903}\text{ squarefree}\iff C_{903}\text{ squarefree},
\]
\[
N_{1806}\text{ squarefree}\iff R_{1806}\text{ squarefree}.
\]

Likewise, existence of an admitted exact-order-903 repeated factor of N903 is equivalent to such a factor of C903. For order 1806 the remaining question is exactly the corresponding question for R1806: 43 has order 42 and valuation one; the other removed factors also have valuation one. This is the certified unresolved-object reduction actually obtained.

### 8.3 Size arguments actually reached

Let L=10^12. All remaining prime factors exceed L. Since the three remaining integers are nonsquares, q²|C would imply C/q²>1; that quotient has a prime factor >L. Therefore
\[
L<q\le\left\lfloor\sqrt{C/(L+1)}\right\rfloor.
\]

The exact upper endpoints are in `arithmetic_audit.json`. This is a valid tightening relative to q≤sqrt(C), but still leaves an enormous range.

Counting with multiplicity gives
\[
\Omega(C_{903})\le27,\qquad
\Omega(C_{1806})\le28,\qquad
\Omega(R_{1806})\le26.
\]

For the desired C<L³ route, these remaining cofactors are vastly too large relative to L. The lower bound does not prove that only one or two prime factors remain. Nonsquare plus at most two prime factors would suffice, but the present bounds do not reach that premise.

### 8.4 Certified restrictions on q−1 and q+1

Put M=lcm(1,...,10^6). The P−1 gcds prove, for every prime q|C903 or q|R1806,
\[
q-1\nmid M,
\qquad q-1\nmid M\ell
\quad\text{for every prime }10^6<\ell\le10^8.
\]

Indeed, if q−1 divided one of those exponents, Fermat's theorem would force q into the recorded gcd. This is an exact divisibility restriction, not the stronger and invalid assertion that q−1 has a prime factor above B1: prime powers also matter.

For an admitted q in either target, q≡1 (mod 3), q≡1 (mod 7), and q≡3 (mod 4). Thus (3/q)=(7/q)=−1. The Lucas P=4 and P=16 discriminants are 12 and 252, respectively, and are nonsquares modulo q. Their norm-one roots have orders dividing q+1. If q+1|M, then V_M(P)=2 mod q, contradicting the P+1 gcd of 1. Hence
\[
q+1\nmid M
\quad\text{for every remaining admitted prime }q.
\]

No stage-two P+1 exclusion is claimed. These restrictions describe explicitly excluded factor-shape classes, but do not cover all possible repeated primes and hence do not constitute square-part closure.

### 8.5 C−1/C+1 probes and failed certificate gate

Trial division through 10^6 was performed on C903±1, C1806±1, and the new R1806±1. Exact partial products and residuals are in `neighbor_partial_factorizations.json`. Examples:

- C903−1 contains 2·3²·7·43·26959; C903+1 contains 2²·5·47·283.
- C1806−1 contains 2⁶·3·5³·7·11·43·563; C1806+1 contains 2 and no other prime ≤10^6.
- R1806−1 contains 2³·3·7·29·43; R1806+1 contains 2·5·11·17.

The residual factors in those neighbor decompositions are not promoted as primes. Merely factoring C±1 gives no implication q−1|C−1 or q+1|C+1 for q|C. A Pocklington/Lucas-style argument needs the appropriate modular conditions; C itself already fails the base-2 Fermat condition. No squarefree certificate was obtained from the neighbor probes. There was no heavy search on these neighbors or on other cyclotomic indices.

## 9. EXACT-ORDER FILTER

Exact computations give gcd(C903,903)=1 and gcd(C1806,1806)=gcd(R1806,1806)=1. Every prime divisor q of one of these residuals satisfies q∤n and q|Phi_n(5), so
\[
\operatorname{ord}_q(5)=n.
\]

Proof: over characteristic q with q∤n, X^n−1 is separable and its cyclotomic factors have disjoint roots. A root of Phi_n therefore cannot have order a proper divisor of n. This legitimate polynomial argument determines **order only**; it says nothing about repeated prime factors of the integer Phi_n(5).

Thus the exact-order filter is already automatic on all remaining prime factors. It cannot eliminate a hypothetical repeated factor by reclassifying it as an order-loss exception. The only removed order-loss exception here was 43 in N1806, and its exponent is exactly one.

## 10. MOD-4 / MOD-5 FILTER

All primes dividing either residual are odd and satisfy
\[
q\equiv1\pmod{1806}.
\]
For n=903 this follows from odd q and ord_q(5)=903; for n=1806 it is immediate. Admission therefore gives the same mod-4 combined progression in both cases:
\[
q\equiv1807\pmod{3612}.
\]

The difference between the two orders appears in the quadratic character of 5.

For order 903, odd order implies (5/q)=1. Quadratic reciprocity for 5 then gives q≡1 or 4 (mod 5). Hence an admitted candidate must satisfy
\[
q\equiv5419\ \text{or}\ 9031\pmod{18060}.
\]

For order 1806 and admitted q, (q−1)/1806 is odd, while 5^903=−1 mod q. Therefore (5/q)=−1, so q≡2 or 3 (mod 5), giving
\[
q\equiv1807\ \text{or}\ 12643\pmod{18060}.
\]

Both sets are nonempty arithmetic progressions; neither forces repeated prime factors to be 1 mod 4. In particular C903≡3 mod 4 forces the presence of at least one admitted prime factor of C903 (with odd total exponent contribution). The task cannot be simplified to proving that C903 has no admitted prime factor at all; it is specifically a multiplicity question.

## 11. n=903 versus n=1806

The exact identities are
\[
\Phi_{1806}(x)=\Phi_{903}(-x),
\qquad
\Phi_{903}(x)\Phi_{1806}(x)=\Phi_{903}(x^2).
\]
The Python verifier checks their evaluations at 5 as integer identities.

The polynomial resultant is
\[
\operatorname{Res}(\Phi_{903},\Phi_{1806})=2^{504}.
\]
A self-contained derivation: write f=Phi_903, g=Phi_1806, so f(x²)=f(x)g(x). For a primitive 903rd root α, differentiation at α gives g(α)=2α f'(α²)/f'(α). Squaring permutes the primitive roots; multiplying this expression over all 504 roots cancels the derivative products and leaves 2^504, since the product of those roots is 1. This is a cross-polynomial resultant computation, not an integer squarefreeness shortcut involving a derivative gcd.

There is an even simpler evaluated gcd proof:
\[
N_{903}\mid5^{903}-1,
\qquad N_{1806}\mid5^{903}+1.
\]
A common divisor divides 2, but both values are odd. Therefore
\[
\gcd(N_{903},N_{1806})=
\gcd(C_{903},C_{1806})=1.
\]

If q² divides one side, then 5^903 is respectively +1 or −1 mod q², and the opposite ambient value 5^903±1 is ±2 mod q². This forbids that same q from dividing the other side. It does not forbid q² on its own side. The reciprocal congruence restrictions in Section 10 add filters, not a contradiction. Neither a derivative gcd shortcut nor “simple roots imply squarefree integer values” is used as a closure argument.

## 12. NEW UNRESOLVED COFACTORS

The current unresolved pair is
\[
\boxed{C_{903}\quad\text{and}\quad R_{1806}.}
\]

R1806 is exactly:
```text
1028474919919828722134238643761114062553999968374840741874778936912419
2471189457008861653997312857862454854235310769936673082311036424379487
3356987517586094860210863815513120373573884763255091439841261400831961
5797383593453119010330417698707905270607464356538521383690232786337077
0358541618899954116760507825251209
```

It is 314 digits / 1040 bits; gcd(R1806,p_*)=1; every prime divisor has order 1806 and exceeds 10^12. Its admitted repeated-factor question remains open. C903 is unchanged at 333 digits / 1103 bits.

## 13. NEXT SINGLE COMPUTATIONAL TARGET

**C903, exactly as defined and hashed above.** It did not shrink in this campaign; the first bounded next computational action should be independent native replay of the frozen inputs/certificates and a separately logged stronger ECM tier on this same integer, not expansion to all 48 indices. The present B1=10^6 tier consisted of only one curve, so it is not evidence that this tier was exhausted.

No next-stage job is launched or promoted by this report. Ordinary Codex CLI can integrate or independently replay the supplied reference sources; this report does not authorize a Codex Ultra production campaign.

## 14. FINAL STATUS

```text
903 CLOSED?
NO

1806 CLOSED?
NO

R=43 THREE-VERTEX FAMILY EMPTY?
NO — NOT PROVED BY THIS RUN

NEW UNRESOLVED COFACTORS
C903: 333 digits, 1103 bits, composite, unchanged
R1806: 314 digits, 1040 bits, composite, newly reduced

PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED

GITHUB WRITES PERFORMED:
NONE
```
