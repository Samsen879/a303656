# A squarefree two-square graph in shorter progressions

Fix \(0<\varepsilon<1/2\). For sufficiently large \(X\), take \(X\le T\le2X\), \(Q=27\cdot 2^k\), \(k\ge3\), and \(QX^{1/2+\varepsilon}\le H\le X\). For every target class \(b\bmod Q\), a positive proportion of the \(J=H/Q\) targets in \((T,T+H]\) have a robust actual two-square label graph in the original power windows from [#86](https://github.com/Samsen879/a303656/pull/86). More precisely at each such \(n\), deleting any at most \(\rho_\varepsilon\log X\) exponent vertices leaves \(\gg_\varepsilon(\log X)^{3/2}\) true edges and \(\gg_\varepsilon\sqrt{\log X}\) pairwise edge-disjoint matchings of size \(\gg_\varepsilon\log X\). Here an edge corresponds to a genuine positive sum of two squares and has a squarefree split-prime core. The construction gives targets in the specified window, not arbitrary specified integers.
 
### 约化相位

沿用 \(X^{1/8}\le3^c\le X^{1/4}\)、\(X^{1/3}\le5^d\le X^{1/2}\)，充分大时 \(c\ge3\)。奇数 \(b\) 取 \(D_0=1\)，使 \(c\) 为奇数当且仅当 \(b\equiv1\pmod4\)，再选 \(d\) 的奇偶使 \(5^d\not\equiv b\pmod3\)。偶数 \(b\) 依 \(b\bmod8=0,2,4,6\) 依次取 \((c,d)\) 的奇偶为 **偶奇、奇奇、偶偶、奇偶**。这使残差为 \(2\bmod8\)。若 \(5^d\not\equiv b\pmod3\)，取 \(D_0=2\)。

余下恰为 \(b\bmod24=2,4,8,22\)。取 \(D_0=18\)，由 \(5\) 在模 \(27\) 下的阶为 \(18\)，解 \(5^d\equiv b-18\pmod{27}\)。该解自动保留所需的 \(d\) 奇偶。四类的 \(c\) 依次为 **奇、偶、偶、奇**。于是残差为 \(18\bmod216\)。#86 短区间段写反了前两项。在 \(b=2,4\bmod216\) 上，旧奇偶分别给出残差 \(180,72\bmod216\)，除以 \(18\) 后都为偶数。所有修正后的相位均有 \(u\equiv1\pmod4\)、\(3\nmid u\)。 [#86 的短区间相位段及有限检查](https://github.com/Samsen879/a303656/pull/86/files)

### 混合筛与短区间能量

写 \(n=b+Qj\)，对每条实际标签 \(\lambda=3^c+5^d\)，令
\[
u_\lambda(j)=\frac{b-\lambda}{D_0}+\frac Q{D_0}j .
\]
所有标签共用同一个长度为 \(J\) 的半开 \(j\) 区间。斜率在 \(p>3\) 下可逆。对惰性素数 \(p\equiv3\pmod4\) 筛去 \(p\mid u_\lambda\)，对分裂素数 \(p\equiv1\pmod4\) 筛去 \(p^2\mid u_\lambda\)。把每个 \(j\) 送到触发禁项的素数之积，计数作为该积上的非负权。这样平方自由筛标签 \(e=e_3e_1\) 的整除条件恰对应物理模 \(e_3e_1^2\) 中的一个 \(j\) 类，故
\[
A_e=\frac{J}{e_3e_1^2}+r_e,\qquad |r_e|<1 .
\]
筛层级约束的是 **\(e\)**。即使物理模超过 \(J\)，半开区间中单一余类的误差仍小于 \(1\)。

主来源定理 2.1 要求乘性密度 \(0\le g(p)<1\)，以及对 \(2\le w<z\) 一致的
\[
\prod_{w\le p<z}(1-g(p))^{-1}
\le \left(\frac{\log z}{\log w}\right)^\kappa
\left(1+O(1/\log w)\right).
\]
这里惰性因子由模 \(4\) 的 Mertens 公式给出 \(\kappa=1/2\)，分裂因子的尾积为 \(1+O(1/w)\)。因此 \(V(z)\asymp1/\sqrt{\log z}\)。取 \(z=2\sqrt X\)、允许层级 \(D=J/(\log X)^2\)，则 \(s=\log D/\log z\ge1+\varepsilon\)，且 \(\sum_{e\le D}|r_e|\le D\)。半维下界的临界值为 \(1\)。为直接利用来源给出的端点公式 \(f_{1/2}(1+\delta)\asymp\sqrt{\delta}\)，可在允许层级内用 \(D'=z^{1+\delta}\)，其中 \(0<\delta<\varepsilon\) 固定且足够小。定理的相对误差 \(O((\log D')^{-1/6})\) 和余项总和均可吸收，逐标签得到 \(\gg_\varepsilon J/\sqrt{\log X}\)。 [Kurlberg–Lester–Rosenzweig，式 (2.4)–(2.5)、定理 2.1 及式 (2.23) 后](https://www.cambridge.org/core/journals/forum-of-mathematics-sigma/article/superscars-for-arithmetic-point-scatters-ii/3CCB969E058792C1803466AE0EF29136) · [Williams，Mertens 定理](https://doi.org/10.1016/0022-314X(74)90032-8)

筛后条件恰好是所需的平方自由两平方核心。因为 \(0<u_\lambda\le3X<z^2\)，大于或等于 \(z\) 的素数平方不可能整除它，未筛出的惰性素因子按重数至多有一个。\(u_\lambda\equiv1\pmod4\) 排除了这最后一个。乘回 \(D_0\in\{1,2,18\}\) 仍是两平方，且普通残差 \(n-\lambda\ge n/2\) 对充分大的 \(X\) 成立。

**#86 的真实标签差能量可以复用。** 两标签若有差 \(h=\lambda-\lambda'\ne0\)，在每个惰性 \(p>3\) 上的禁类恰于 \(p\mid h\) 时重合。取较小的上界筛截点 \(J^{1/10}\) 和层级 \(J^{1/2}\)，每个平方自由标签的误差至多 \(2^{\omega(e)}\)，总误差 \(O(\sqrt J\log J)\)。故单标签上界为 \(O(J/\sqrt{\log X})\)，标签对上界为
\[
O\!\left(\frac{J}{\log X}\frac{|h|}{\varphi(|h|)}\right).
\]
实际标签差和指数盒均与 #86 相同。固定一条标签以及另一条标签的一轴，余下一轴在模 \(p\) 的命中次数为 \(O(1+\log X/\operatorname{ord}_p(B))\)，其中 \(B=3^2\) 或 \(5^{18}\)，整除 \(B\) 的有限个素数单计。Radomskii 引理 3.1 给出全盒 \(O((\log X)^4)\)、每固定顶点 \(O((\log X)^2)\) 的差权和。因此令 \(L=\log X\)，有
\[
\sum F(n)\asymp_\varepsilon JL^{3/2},\qquad
\sum F(n)^2\ll JL^3,\qquad
\sum_n\sum_v d_v(n)^2\ll JL^2 .
\]
Cauchy–Schwarz 和能量截断保留 \(\gg_\varepsilon J\) 个目标。每个目标删去至多 \(\rho_\varepsilon L\) 个指数顶点后，仍有 \(\gg_\varepsilon L^{3/2}\) 条边和 \(\gg_\varepsilon\sqrt L\) 个大小 \(\gg_\varepsilon L\) 的边不交匹配。 [#86 的差权与图提取](https://github.com/Samsen879/a303656/pull/86/files) · [Radomskii，引理 3.1](https://arxiv.org/html/2504.09954v7#S3)

### 精确正反控

复验覆盖全部 \(216\) 个相位。同一实际目标 \(10000016714\) 的两条标签给出核心 \(555556297\) 和 \(555556309\)。前者为分裂素数，后者的 \(7\)-赋值恰为 \(1\)。同一个混合筛标签 \(e=7\cdot5\) 的物理模为 \(175\)，在两个真实核心类上分别命中 \(j=83,30\bmod175\)。另一个反控是 \(X=100,u=103\)。它通过所有 \(p<20\) 的局部测试，仍有惰性素因子 \(103\)，说明模 \(4\) 条件在截止论证中确有作用。


### Explicit graph extraction

With \(L=\log X\) and \(E(n)=\sum_v d_v(n)^2\), the three displayed moments yield a positive fraction of targets with \(F(n)\ge cL^{3/2}\) and \(E(n)\le CL^2\): first use the second moment on \(F\), then discard large energy by Markov. Deleting at most \(\rho L\) vertices removes at most \(\sqrt{\rho L E(n)}\) edges. Then remove edges incident to vertices of degree \(> A\sqrt L\), at a cost of at most \(CL^{3/2}/A\). Choose small \(\rho\) and large \(A\), preserving \(\gg L^{3/2}\) edges and maximum degree \(O(\sqrt L)\). A maximal matching has at least the number of edges divided by twice the maximum degree. Choose exactly \(\lfloor c' L\rfloor\) of its edges each round; the edge budget gives \(\gg\sqrt L\) rounds. No step combines different target integers.

### Exact replay

```python
from math import gcd, isqrt

def rem(b, c_odd, d):
    return (b - pow(3, 4-c_odd, 216) - pow(5, d, 216)) % 216

assert len({pow(5, d, 27) for d in range(18)}) == 18
for b in range(216):
    if b % 2:
        c, d, D = int(b % 4 == 1), int(b % 3 == 1), 1
    else:
        c, d = {0: (0, 1), 2: (1, 1), 4: (0, 0), 6: (1, 0)}[b % 8]
        D = 2
        if b % 3 == pow(5, d, 3):
            d = next(t for t in range(18) if pow(5, t, 27) == (b-18) % 27)
            D = 18
    r = rem(b, c, d)
    assert (D == 18) == (b % 24 in (2, 4, 8, 22))
    assert r % D == 0 and r//D % 4 == 1 and gcd(r//D, 216//D) == 1
    if D == 18:
        assert r == 18

assert (rem(2, 0, 17), rem(4, 1, 16)) == (180, 72)
def prime(u):
    return u > 1 and all(u % t for t in range(2, isqrt(u)+1))

n, q = 10000016714, (27*2**16)//18
a, b = (n-3**5-5**5)//18, (n-3**3-5**5)//18
assert (a, b) == (555556297, 555556309)
assert 18*a == n-3**5-5**5 == 99111**2 + 13305**2
assert prime(a) and a % 4 == 1 and b % 49 == 42
assert (a % q, b % q) == (40393, 40405)
for r, j0 in ((a % q, 83), (b % q, 30)):
    assert [j for j in range(175) if (r+q*j) % 175 == 0] == [j0]
assert prime(103) and 20 < 103 <= 300 and 103 % 4 == 3
```
