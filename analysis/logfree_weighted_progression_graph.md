# Log-free weighted graph threshold in reduced progressions

In the complete exact setting of [#105](https://github.com/Samsen879/a303656/pull/105), the threshold improves to \(H\ge C Q X^{1/3}\) with a sufficiently large absolute constant \(C\). The \(\gg(\log X)^{5/4}\) true edges and \(\gg(\log X)^{1/4}\) edge-disjoint matchings each of size \(\gg\log X\) survive arbitrary deletion of up to \(\rho\log X\) exponent vertices at a positive fraction of targets in each class. The proof does not assert a numerical value of \(C\), squarefree cores, or pointwise coverage.

Analytic convention: with phase \(e(-x\cdot \xi)\), the disk transform for \(\xi\ne0\) is \(R J_1(2\pi R|\xi|)/|\xi|\), by polar integration. At large argument \(J_1(u)=O(u^{-1/2})\) ([NIST DLMF 10.17.3](https://dlmf.nist.gov/10.17.E3)); at small argument the disk area bound suffices. Hence \(\lvert\widehat{1_{B_R}}(\xi)\rvert\ll R^{1/2}|\xi|^{-3/2}\) for every \(\xi\ne0\). The rest of the proof, including growth in \(q\), follows.

### 二进频率与边界

记 \(N(z)=z_1^2+z_2^2\)、\(e(x)=\exp(2\pi i x)\)，并令
\[
S_j(h;r)=\sum_{\substack{z\bmod 2^j\\N(z)\equiv r\ (2^j)}}e(h\cdot z/2^j),
\qquad r\equiv1\pmod4.
\]
圆上的两坐标奇偶相反。\(j=2\) 直接得到 \(2^{j+1}\) 个点。\(j\ge3\) 时，固定哪一坐标为偶，恰有一半偶数坐标使另一坐标所需的平方为 \(1\bmod8\)，各有四个奇平方根。因此 \(S_j(0;r)=2^{j+1}\)。若 \(h\) 有奇坐标，沿该坐标平移 \(2^{j-1}\) 保持圆方程并把相位乘以 \(-1\)，故 \(S_j(h;r)=0\)。

对 \(h=2^dh'\)、\(h'\) 至少一坐标为奇、\(1\le d\le j-2\)，设 \(j'=j-d+1\)。写 \(z=z_0+2^{j'-1}t\)，固定 \(z_0\bmod 2^{j'-1}\)。有提升的充要条件是 \(N(z_0)\equiv r\bmod 2^{j'}\)。提升至 \(2^j\) 时，\(t\bmod 2^d\) 满足
\[
z_0\cdot t+2^{j'-2}N(t)\equiv
\frac{r-N(z_0)}{2^{j'}}\pmod{2^{d-1}}.
\]
选 \(z_0\) 的奇坐标，固定另一变量。该坐标上两输入的输出差是
\((t-u)(z_{0,a}+2^{j'-2}(t+u))\)，括号为奇，故映射为置换。总计 \(2^{d+1}\) 个提升，初层恰有四个，相位在各自纤维内恒定。所以
\[
S_j(2^dh';r)=2^{d-1}S_{j'}(2h';r).
\]
**最高非零层 \(j'=2\) 要另证。** 此时上述置换论证失效，例如 \(t+t^2\bmod2\) 恒为零。交换坐标使两种奇偶型各有 \(2^j\) 点，直接得到
\[
S_j(2^{j-1}h';r)=2^j\bigl((-1)^{h'_1}+(-1)^{h'_2}\bigr).
\]

最后取 \(m=\lceil j/2\rceil,\ \ell=\lfloor j/2\rfloor\)，写 \(z=z_0+2^m t\)。在 \(S_j(2h';r)\) 中，纤维由一个模 \(2^{\ell-1}\) 的线性方程给出，非空纤维有 \(2^{\ell+1}\) 点。对其核做字符求和，存活要求 \(h'\equiv\lambda z_0\bmod 2^{\ell-1}\)。当 \(\ell\ge2\)，\(\lambda\) 为奇数，且
\[
\lambda^2\equiv N(h')r^{-1}\pmod{2^{\ell-1}}.
\]
至多四个根，每根固定 \(z_0\bmod 2^{\ell-1}\)，再至多有 \(2^{2(m-\ell+1)}\le16\) 个代表。\(j=2,3\) 时 \(\ell=1\)，直接数至多 16 个 \(z_0\)。于是 \(S_j(2h';r)\ll2^{j/2}\)。结合提升、最高层和零频率，再用 CRT 及模 \(3^i\) 的平凡界，得到绝对一致的
\[
|S_q(h;r)|\ll \sqrt q\,\sqrt{\gcd(q,h_1,h_2)} .
\]

### Poisson 与 #105 的实际窗口

令 \(C_{q,r}(R)\) 计数 \(N(z)\le R^2\)、\(N(z)\equiv r\bmod q\) 的整数点，\(\eta_r(q)\) 为模 \(q\) 的圆点数。对 \(R\ge1,\ q\le R^{4/3}\)，取 \(\delta=qR^{-1/3}\le R\)，用支撑半径 \(\delta\) 的非负单位质量光滑核卷积半径 \(R\pm\delta\) 的圆盘，夹住原闭圆盘。零频率误差为 \(O(R\delta/q)\)。圆盘 Fourier 界及核的快速衰减给出非零频率误差
\[
\ll R^{1/2}\!\sum_{h\ne0}
\frac{\sqrt{\gcd(q,h_1,h_2)}}{|h|^{3/2}}
(1+\delta|h|/q)^{-3}.
\]
按公共因子 \(d\mid q\) 上界，再代 \(h=dk\)。二维环带求和给出
\(\sum_{k\ne0}|k|^{-3/2}(1+a|k|)^{-3}\ll a^{-1/2}\) 对所有 \(a>0\) 成立。因此误差至多
\[
O\!\left(R^{1/2}(q/\delta)^{1/2}\sum_{d\mid q}d^{-3/2}\right).
\]
两项均为 \(O(R^{2/3})\)，即
\[
C_{q,r}(R)=\pi R^2\eta_r(q)/q^2+O(R^{2/3}).
\]

在 #105 中，\(Q=27\cdot2^k,\ k\ge3,\ X\le T\le2X\)，标签仍为 \(X^{1/8}\le3^c\le X^{1/4}\)、\(X^{1/3}\le5^d\le X^{1/2}\)。对原相位的 \(D_0\in\{1,2,18\}\)，设 \(q=Q/D_0\)、\(\lambda=3^c+5^d\)、\(x_0=(T-\lambda)/D_0\)。充分大 \(X\) 下，\(x_0\ge X/(2D_0)\)。若 \(J\ge C X^{1/3}\)，由 \(H\le X\) 得
\[
q/x_0^{2/3}\le 2^{2/3}/(CD_0^{1/3}).
\]
所以两个端点都能应用圆盘估计。实际核心类 \(r\) 还是模 3 的单位。模 3 有四个圆点，每次提升有三个，故 \(\eta_r(q)=8q/3\)。两端相减并除以四，得到每条标签一致的首矩
\[
\sum_{\substack{T<n\le T+H\\n\equiv b\ (Q)}}\frac{r_2((n-\lambda)/D_0)}4
=\frac{2\pi}{3}J+O(X^{1/3}).
\]
取 \(C\) 大于该绝对误差所需常数，即得 \(\gg J\)。该换元也适用于非既约的目标类 \(b\bmod Q\)。 [#105 的实际相位](https://github.com/Samsen879/a303656/pull/105/files)

上矩仍用两个次数至多二的原始线性因子的乘积，系数高度 \(O(X^2)\)，区间基点 \(x\asymp X/Q\gg X^{1/3}\)。所以 Henriot 的高度条件 \(x\gg\|U\|^{1/8}\) 与长度条件 \(J\ge x^{1/4}\) 都有余量，若 \(J>x\) 则分成可比的两段。原证明的重权截断和顶点能量提取只需首矩 \(\gg J\)。于是每个指定类中仍有正比例目标，在任删至多 \(\rho\log X\) 个指数顶点后保有 \(\gg(\log X)^{5/4}\) 条真标签边，以及 \(\gg(\log X)^{1/4}\) 轮大小各为 \(\gg\log X\) 的边不交匹配。 [Henriot 原定理](https://arxiv.org/pdf/1102.1643) · [勘误](https://doi.org/10.1017/S0305004114000280) · [#105 的上矩与提取](https://github.com/Samsen879/a303656/pull/105/files)

### 独立整数重放

以下用 \(X^{2^{j-1}}+1\) 约化字符和，逐项精确核对 \(j=2,\ldots,5\) 的频率与全部 216 个目标相位。解析误差由上面的证明给出。


```python
from itertools import product
from functools import lru_cache

@lru_cache(None)
def points(j, r):
    q = 1 << j
    return [(x,y) for x,y in product(range(q), repeat=2)
            if (x*x+y*y-r) % q == 0]

def spec(j, r, h, k):
    q = 1 << j
    v = [0]*(q//2)
    for x,y in points(j, r % q):
        a = (h*x+k*y) % q
        v[a % (q//2)] += 1-2*(a >= q//2)
    return v

for j in range(2,6):
    q = 1 << j
    for r in range(1,q,4):
        assert len(points(j,r)) == 2*q
        for h,k in product(range(q), repeat=2):
            v = spec(j,r,h,k)
            u = h|k
            if u & 1:
                assert not any(v)
            elif u == 0:
                assert v == [2*q]+[0]*(q//2-1)
            else:
                d = (u & -u).bit_length()-1
                f = 1 << (d-1)
                w = spec(j-d+1,r,h//f,k//f)
                assert all(a == (f*w[i//f] if i%f==0 else 0)
                           for i,a in enumerate(v))
assert {(t+t*t)%2 for t in range(2)} == {0}

for b in range(216):
    c = 4+int((b%4==1) if b%2 else (b%8 in (2,6)))
    D = 1 if b%2 else 2
    d = int(b%3==1) if b%2 else int(b%8 in (0,2))
    if D==2 and (b-3**c-5**d)%3==0:
        D = 18
        d, = [k for k in range(18) if (5**k-b+18)%27==0]
        assert d%2 == int(b%8 in (0,2))
    v = b-3**c-5**d
    assert v%D==0 and (v//D)%4==1 and (v//D)%3
print("spectra j=2..5 and all 216 phases checked")

```
