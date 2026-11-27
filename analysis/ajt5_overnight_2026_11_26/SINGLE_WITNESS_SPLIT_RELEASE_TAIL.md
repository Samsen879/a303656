# 分裂主位释放与可达旧读者尾界

可以严格缩小一类大 \(M\) 候选。**若零观测终端 \(q\) 读取一个分裂素数主位 \(s\)，释放 \(s\) 后仍然全堵，则实际阶图上必须有一个可达的、更早的共同 Wieferich 测试。** 对 \(s\ge q^\gamma,\ \gamma>1/4\)，若该旧测试也是零观测，这类终端的尾部上密度为 \(O_\gamma(Z^{-(4\gamma-1)/3})\)。这个界不使用共同 Wieferich 素数的分布，也不限制 \(M\) 的大小。

### 从完整旧面板释放一个主位

取 \(s>5,\ s\equiv1\pmod4\)，且 \(s\) 整除 \(\operatorname{ord}_q3\) 或 \(\operatorname{ord}_q5\)。旧面板可包含所有小于 \(q\) 的惰性素数及 \(2,3\) 条件。从一个旧面板幸存相位出发，冻结其余主位，改变 \(s\) 主位，使 \(3^c+5^d\not\equiv0\pmod q\)。这一步只须把两项的 \(s\)-主分量选成不匹配。后来改变别的主位也不能恢复匹配，因为模 \(q\) 的乘法群按互素阶分解。

画真实读取边 \(u\to r\)，条件为 \(u<r\) 且 \(u\mid\operatorname{ord}_r3\) 或 \(u\mid\operatorname{ord}_r5\)。从 \(s\) 可达的旧行才可能受影响。按素数升序修复这些行，始终保留 \(s\) 和已经通过的旧条件。对每个旧素数 \(r\)，令
\[
\lambda_r=\min_{a=3,5}v_r(a^{r-1}-1).
\]
若余数已固定为小于 \(\lambda_r\) 的偶赋值，直接保留。若余数模 \(r^{\lambda_r}\) 为零，则用 \(r\) 自己的首个有效位及下一位选出精确偶赋值。唯一可能卡住的情形是余数已有**小于 \(\lambda_r\) 的固定奇赋值**。于是 \(\lambda_r\ge2\)，且这个 \(r\) 是沿真实路径抵达的旧共同 Wieferich 测试。这里保留了路径以外的全部旧测试。

还有一个更强的点态判据。若 \(s>\sqrt q\)，可在自由的 \(s\times s\) 网格上一次避开 \(q\) 及所有直接读取 \(s\) 的旧行。每行的模素数坏集至多有 \(s\) 点，读者数少于 \(s\)。任何直接读者也不可能再读取一个由这次修复改变的更大主位 \(u>s\)，因为 \(su>q\)。所以这个范围内若仍全堵，旧共同 Wieferich 测试必须位于**至少两步**的路径上。这项判据允许旧测试的观测非零。

### 零观测旧读者的尾部可求和

若前述失效旧行 \(r\) 是零观测，则同一个整数满足 \(qr\mid n\)。取 \(X\le q<2X\) 和 \(s\ge X^\gamma\)。路径上的每步写成 \(r_i=k_i r_{i-1}+1\)，其中 \(r_0=s\)，且 \(k_i\equiv2\pmod4\)。令 \(\sigma=4/3\)，则
\[
\sum_{k\equiv2\ (4)} k^{-\sigma}
=2^{-\sigma}(1-2^{-\sigma})\zeta(\sigma)<1.
\]
该严格不等式也可不用数值 ζ：单调积分估计给出上界 \(2^{-4/3}(1+3/2)<1\)，最后一步等价于 \(125<128\)。

又因为 \(s\prod k_i\le r<2X\)，从固定 \(s\) 出发的所有路径终点的 \(1/r\) 权重，连重复路径一起计，至多为
\[
O\!\left(\frac1s(2X/s)^{\sigma-1}\right).
\]
同一 \(s\) 上，\(q\equiv1\pmod s\) 的 \(1/q\) 权重为 \(O(1/s)\)。所以整个二进层的 \(1/(qr)\) 权重为
\[
O\!\left(X^{1/3}\sum_{s\ge X^\gamma}s^{-7/3}\right)
=O_\gamma\!\left(X^{(1-4\gamma)/3}\right).
\]
用 \(\lfloor N/(qr)\rfloor\le N/(qr)\) 直接计整数，再对二进层求和，即得开头的尾界。这里不要求两个读者接近同一尺度。若旧失效行是非零观测，则不能使用 \(r\mid n\)，这正是该平均论证留下的分支。

### 原 \(7,19\to1419643\) 面板的完整旧相位复验

原普通终端 \(q=1419643\) 读取分裂主位 \(s=593\)。冻结 \(s\) 和 \(q\) 自身主位时，确实有一个能延伸到完整旧面板的 133 格低位片，全部满足 \(v_q=1\)。释放 \(s\) 后，**133 格均可改成模 \(q\) 单位**，且可重新通过完整旧面板。单独释放普通终端自己的主位则给出精确 \(v_q=2\)。因此这里的冻结片确实存在，但完整旧面板并未把它锁死。

下方取同一个 \(n=3+1+u^2+v^2\)，保留真平方和，并核对 \(2,3\)。旧素数的检验只做到原来的 \(q\)。其中 \(3\) 轴在旧惰性素数中仅于 \(11,1006003\) 出现异常提升，两处 \(5\) 轴均普通，故升序修复适用于整个旧面板。除 \(2,3,7,19,593,q\) 外的主位不会改变这里的终端模平方。

```python
from math import isqrt

q, s = 1419643, 593
u, v = 178942114138501813, 24553644206153808
n = 4 + u*u + v*v
assert (n % 4, n % 3, n % 133**2, n % q**2) == (1, 2, 0, q)
assert all(q % j for j in range(2, isqrt(q)+1))

P = bytearray(b'\1') * q
P[:2] = b'\0\0'
for r in range(2, isqrt(q-1)+1):
    if P[r]:
        P[r*r::r] = bytes((q-1-r*r)//r+1)
assert P[s] and s % 4 == 1
assert all(any(pow(a, r-1, r*r) != 1 for a in (3, 5))
           for r in range(7, q, 4) if P[r])
assert all(pow(a, (q-1)//r, q) != 1 for a in (3, 5)
           for r in (7, 19, s))

def exponent(digits):
    x, step = 0, 1
    for a, mod in zip(digits, (49, 361, q, (q-1)//133)):
        x += step*((a-x)*pow(step, -1, mod) % mod)
        step *= mod
    return x

def rem(c, d, mod):
    return (n-pow(3, c, mod)-pow(5, d, mod)) % mod

def exact2(c, d, p):
    return rem(c, d, p**3) in range(p*p, p**3, p*p)

for x in range(7):
    for z in range(19):
        c = exponent((x, z, 0, 32319))
        ds = [exponent((x+7*i, (11*z)%19+19*j, 0, 19152))
              for i in (0, 1) for j in (0, 1)]
        d = next(d for d in ds if all(exact2(c, d, p) for p in (7, 19)))
        assert rem(c, d, q*q) == q
        # 改变终端读取的 593 位，保留其余已用主位
        for cc in (c, c + 18*133**2*q):
            assert rem(cc, d, 4) == rem(cc, d, 3) == 1
            assert all(exact2(cc, d, p) for p in (7, 19))
        assert rem(c + 18*133**2*q, d, q) != 0

c = 151199743527567 + 133*(q-1)*841236
d = 149165666260380
assert all(exact2(c, d, p) for p in (7, 19, q))
```

这些是有限 CRT 相位结论。若要求复验指数实际激活，可在 \(u\) 上加足够大的公模倍数，保留所有已选旧行的有限精度、终端精确赋值和真平方和。剩余大 \(M\) 类包括没有足够大分裂阶因子的终端，以及可达旧共同测试只给非零观测的情形。本轮未改变既有数值阈值，也未得到一般密度一结论。
