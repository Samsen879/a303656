# A linear-denominator obstruction for the #88 four-label strand

Freeze the offsets and anchors in [#88](https://github.com/Samsen879/a303656/pull/88). Let \(A_i=\ell_i S^2+m_i R^2\) and \(s_i=a_i S^4+b_i R^4\), using the four rows encoded below. If rational homogeneous cubic vectors \(P_i(S,R,t)\) satisfy \(P_i(S,R,0)=(S+R)A_i\) and all four \(\lvert P_i/(S+R)\rvert^2+s_i\) are identical in \(\mathbb Q(S,R,t)\), then \(P_i=(S+R)A_i\). The proof is at the identity level; it does not prohibit additional four-label integer points.

## 共同分母的模 7 障碍

令 \(X=S+R,\ Y=R\)。保锚点条件给出 \(P_i(X,Y,0)=XA_i(X-Y,Y)\)，而同一目标要求
\[
N(P_i)-N(P_j)=X^2(s_j-s_i).
\]
在 \(X=0,Y=1\) 处，各行的范数和范数对 \(X\) 的一阶导数都相同。

若有一个分子在 \(X=0\) 不恒为零，取极点处首个非零 \(t\) 系数 \(B_i\)。齐次性保证设 \(Y=1\) 不丢掉该系数，实数平方和也保证各行的最低次数相同。比较范数和导数的最低相应系数，得到共同的
\[
N(B_i)=G>0,\qquad B_i\cdot(\ell_i+m_i)/2=L.
\]
将所有 \(B_i\) 同乘一个 7 的幂，使它们在 7 处整且至少一个本原。由于 \(-1\) 在模 7 下非平方，\(G\) 是单位。四个投影恒等式要求
\[
Gd_i-L^2=\det\bigl(B_i,(\ell_i+m_i)/2\bigr)^2,
\qquad (d_i)=(2309,2290,2305,2098).
\]
模 7 的 \(d_i\) 为 \((6,1,2,5)\)。将 \(G\) 按平方类归一为 1 或 3 后，\(L^2\in\{0,1,2,4\}\) 中没有一个使四项同时为平方。故没有极点。这一步只用到分母为简单线性因子和原锚点，**无需限制分子的 \(t\) 次数**。三次上界用于约分后的排除。

## 约分后的二次排除

六条标签差的斜比 \((b_j-b_i)/(a_j-a_i)\) 依次为
\[
18,\quad -1/3,\quad 180/31,\quad -4,\quad 27/5,\quad 182/25.
\]
因此没有一条差有有理线性因子，只有斜比 \(-4\) 的差可约。这里用的是 \(x^4+r\) 的精确判据：有有理根要求 \(-r\) 为四次幂；无有理根时，比较两个首一二次因子的系数，可约只可能是 \(r\) 为负平方或四倍四次幂。

- **\(t\) 一次。** 各行方向的 Gram 矩阵相同，可用常值有理正交变换对齐。秩二时，共同方向 \(F\) 的两个线性分量互素。各行锚点差垂直于 \(F\)，故等于 \(JF\) 乘一个线性式。相应标签差就有线性因子。秩一时，沿固定方向的投影相同，标签差是两个垂直二次投影的平方差。这会要求所有边可约。两种秩都排除。
- **\(t\) 二次。** 除以各行的复数首项系数，再用共同平移消掉实部的 \(t\) 项，可写成 \(t^2+(H-\beta_i^2)/2+\mathrm i(\beta_i t+\gamma_i)\)，其中 \(\beta_i\gamma_i=M\) 共同。若 \(M=0\)，两条 \(\beta_i\ne0\) 的边会有线性因子，所以至少三行 \(\beta_i=0\)，却没有三条可约边供这三行使用。若 \(M\ne0\)，两条不成比例的 \(\beta_i,\beta_j\) 会使 \(\beta_i^2-\beta_j^2\) 整除相应标签差，因为 \(\beta_i\beta_j\mid M\)。因此写成 \(\beta_i=\lambda_i B,\gamma_i=C/\lambda_i\)。四个 \(x_i=\lambda_i^2\) 互异。用 \(1,x_i,x_i^2,1/x_i\) 的可逆求值矩阵，在模去 \(S^4,R^4\) 后比较常数项，得到 \(B^4,HB^2,C^2\) 都是纯四次项。于是 \(B,H\) 在同一轴，\(C\) 在另一轴。一轴的标签系数随 \(x_i\) 严格递增，另一轴是凹二次函数。按递增轴排序，另一轴却是 \((25,1,5,125)\) 或 \((9,81,1,729)\)，均有低于两端的内点，矛盾。

当 \(S=5^u,\ R=3^v,\ v\le u,\ |t|=O(S)\) 时，三次分子除以 \(S+R\) 本可保持 \(O(S^4)=O(T^2)\) 的目标高度。上述排除发生在系数恒等式层面。它仍留下其他分母及非恒等的离散整数构造。

同一个模 7 证书还排除 7 处整的 \(\lambda\) 满足 \(\lambda^2\bmod7\in\{0,1,4\}\) 的 \(S+\lambda R\)。作为边界对照，\(\lambda=3\) 的极点首项条件确实在模 7 可解，下面给出四个向量。它们只验证首项条件。


```python
from fractions import Fraction as Q
from itertools import combinations
from math import isqrt

a,b = (1,5,25,125),(9,81,1,729)
ell = ((20,7),(21,2),(19,8),(17,6))
m = ((0,87),(21,84),(59,-64),(57,-60))
N = lambda z: sum(x*x for x in z)
dot = lambda u,v: sum(x*y for x,y in zip(u,v))

assert all((aa+N(e),2*dot(e,f),bb+N(f)) == (450,1218,7578)
           for aa,bb,e,f in zip(a,b,ell,m))
ratios = [Q(b[j]-b[i],a[j]-a[i]) for i,j in combinations(range(4),2)]
def power(z,k):
    if z <= 0:
        return False
    root = isqrt if k == 2 else lambda n: isqrt(isqrt(n))
    return all(root(n)**k == n for n in (z.numerator,z.denominator))

assert all(not power(-r,4) for r in ratios)
assert [r for r in ratios if power(-r,2) or power(r/4,4)] == [-4]
assert [a[i] for i in sorted(range(4),key=b.__getitem__)] == [25,1,5,125]
assert min(b[1:-1]) < min(b[0],b[-1])

sq = {0,1,2,4}
d = [N(tuple((x+y)//2 for x,y in zip(e,f))) for e,f in zip(ell,m)]
assert d == [2309,2290,2305,2098]
def live(d):
    return [(g,h) for g in (1,3) for h in sq
            if all((g*x-h)%7 in sq for x in d)]

assert live(d) == []
E = lambda s: [N(tuple(s*x+y for x,y in zip(e,f))) for e,f in zip(ell,m)]
assert all(not live(E(s)) for s in (0,1,4))
assert live(E(2)) == [(3,2)]
A = [tuple(9*x+y for x,y in zip(e,f)) for e,f in zip(ell,m)]
B = [(1,4),(3,6),(1,4),(1,3)]
assert all(N(v)%7 == dot(u,v)%7 == 3 for u,v in zip(A,B))
print("PASS")
```
