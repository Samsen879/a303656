# Formal pole lifts versus polynomial pole obstructions

This refines the boundary in [#98](https://github.com/Samsen879/a303656/pull/98). The four fixed anchors are \(A_i=\ell_i S^2+m_iR^2\), with the coefficients in the replay. The question is whether \(P_i/(S+\lambda R)\) can share the same norm-plus-label identity while keeping \(P_i(S,R,0)=(S+\lambda R)A_i\), and have a true pole. At \(\lambda=\pm3\), complete formal solutions exist over \(\mathbb Z_7[[S+\lambda]]\) after setting \(R=1\). At those slopes a homogeneous cubic jet exists through \(t^2\), but a homogeneous polynomial numerator with only one positive \(t\)-power is impossible at *any* slope. Neither statement gives a full cubic solution, unbounded integer labels, or a pointwise representation theorem.

## 全深度局部解

在 \(R=1\) 置 \(X=S+\lambda\)，记 \(a_i(X)=A_i(X-\lambda,1)\)，令 \(J(x,y)=(-y,x)\)。两个斜率在极点的锚点相同，因为 \(A_i\) 只含 \(S^2,R^2\)。四个锚点的范数模 7 为 \((6,2,2,1)\)，所以
\[
3N(a_i(0))-9\equiv(2,4,4,1)\pmod7.
\]
四项都是非零平方。先提升常数平方根，再逐次解幂级数系数，得到 \(d_i(X)\in\mathbb Z_7[[X]]\)，满足
\[
d_i^2=3N(a_i)-9.
\]
每一步的线性系数都是单位 \(2d_i(0)\)。定义
\[
b_i(X)=\frac{3a_i(X)+d_i(X)J a_i(X)}{N(a_i(X))},
\qquad P_i=Xa_i+t b_i.
\]
则 \(N(b_i)=3,\ a_i\cdot b_i=3\)，从而 **精确地**
\[
N(P_i)=X^2N(a_i)+6Xt+3t^2 .
\]
因此四行满足完整范数差恒等式，且 \(b_i(0)\ne0\) 给出真极点。这个公式也解释了为何继续加深 7-adic 精度不会否决首项。取 \(b_i\) 的 \(X^2\) 截断，齐次化后已在三次分子次数上界内满足全部 \(X^0,X^1,X^2\) 层。

另一个惯性素数 3 也不能仅靠首项否决。用半锚点的范数
\[
D_i=(13725,13626,13241,11034)
\]
取 \(G=2,\ L^2=2D_4=9\cdot2452\)。四个 \(GD_i-L^2\) 为
\((9\cdot598,72^2,4414,0)\)，全是 \(\mathbb Q_3\) 平方。2 进首项也有全深度解，取 \(G=1,L^2=D_3\)，四个差为 \((22^2,385,0,-2207)\)。

## 三次次数限制下的边界

**前两阶 \(t\) 系数有三次多项式解。** 令 \(D=S+\lambda R\)。因每行的 \(\ell_i,m_i\) 线性独立，先解 \(\ell_i\cdot u_i=0,\ m_i\cdot u_i=3\)。选
\[
B_i=R^2u_i+\kappa_i J A_i
\]
使 \(B_i(-\lambda,1)=b_i(0)\)。可以选到 \(\kappa_i\)，因为这两个待匹配向量对 \(A_i(-\lambda,1)\) 的点积都是 3。于是 \(A_i\cdot B_i=3R^4\)，且 \(D\mid(3R^4-N(B_i))\)。再解线性向量 \(C_i(S,R)\) 使
\[
2A_i\cdot C_i=\frac{3R^4-N(B_i)}{D}.
\]
此处线性映射可逆，因为 \(\ell_i,m_i\) 独立，恰好控制 \(S^3,S^2R,SR^2,R^3\) 四项。故 \(P_i=DA_i+tB_i+t^2C_i\) 有真极点，并精确满足模 \(t^3\) 的范数恒等式。更高的 \(t\) 项仍须检验。

**单项分支则无解。** 若 \(P_i=DA_i+t^r B_i\) 且 \(r\ge1\)，比较 \(t^r,t^{2r}\) 得 \(A_i\cdot B_i\) 与 \(N(B_i)\) 各自共同。这两个条件与 \(\lambda\) 无关。在 \(S=-R\) 使用 #98 的模 7 投影障碍，得到四个 \(B_i\) 都被 \(S+R\) 整除。共同除掉该因子后，两条件继续成立。按次数下降得到 \(B_i=0\)。所以形式解与这个严格排除相容，区别在于形式级数和有限多项式。

以下重放同时检查两个斜率，在模 \(7^5,X^3\) 复核形式公式，并核对用于单项排除的旧投影障碍。


```python
E = ((20,7),(21,2),(19,8),(17,6))
F = ((0,87),(21,84),(59,-64),(57,-60))
B = ((1,4),(3,6),(1,4),(1,3))
q = 7**5

def mul(a,b):
    return [sum(a[j]*b[k-j] for j in range(k+1)) % q for k in range(3)]

def add(a,b):
    return [(x+y)%q for x,y in zip(a,b)]

def div(a,b):
    c = []
    for k in range(3):
        rest = sum(b[j]*c[k-j] for j in range(1,k+1))
        c.append((a[k]-rest)*pow(b[0],-1,q)%q)
    return c

for lam in (3,-3):
    for e,f,v in zip(E,F,B):
        a = [lam*lam*x+y for x,y in zip(e,f)]
        x,y = ([z,-2*lam*h,h] for z,h in zip(a,e))
        n = add(mul(x,x),mul(y,y))
        branch = (a[0]*v[1]-a[1]*v[0]) % 7
        assert branch and n[0]%7
        d0 = next(r for r in range(branch,q,7) if (r*r-3*n[0]+9)%q==0)
        inv = pow(2*d0,-1,q)
        d1 = 3*n[1]*inv % q
        d2 = (3*n[2]-d1*d1)*inv % q
        d = [d0,d1,d2]
        u = div(add([3*h for h in x],[-h for h in mul(d,y)]),n)
        w = div(add([3*h for h in y],mul(d,x)),n)
        assert (u[0]%7,w[0]%7) == v
        assert add(mul(u,u),mul(w,w)) == [3,0,0]
        assert add(mul(u,x),mul(w,y)) == [3,0,0]

sq = {0,1,2,4}
d = [sum(((a+b)//2)**2 for a,b in zip(e,f)) for e,f in zip(E,F)]
assert d == [2309,2290,2305,2098]
assert not any(all((g*x-L2)%7 in sq for x in d)
               for g in (1,3) for L2 in sq)
assert all(e[0]*f[1]-e[1]*f[0] for e,f in zip(E,F))
print("PASS")

```
