## 本轮交接：有限惯性素数的 CRT 截断与跨相位精确计数

**独立复验通过。** [PR #90](https://github.com/Samsen879/a303656/pull/90/files) 的两中心截断可以扩展到任意有限个活跃惯性素数。7/19/23 原生案例确实阻断了旧证明的三个方向，但仍能修复。**本轮新增**是一条跨相位转移：固定一个指数后，不必为另一指数枚举中心素数的联合相位。用广义 CRT 合并带符号的同余类，便能精确计数并找出普通高度内的首个见证。

### 一、有限中心截断

固定保留其他行的矩形相位，写成
\[
S(i,j)=XA^i+YB^j,\qquad i,j\ge0,
\]
其中 \(A,B\equiv1\pmod r\) 对每个中心 \(r\) 成立。要求 \(S<n\)，且每个 \(v_r(n-S)\) 为偶数。基点若已达到或超过 \(n\)，本相位无正余数见证。否则记
\[
s_r=\min\{v_r(A-1),v_r(B-1)\}.
\]
基点赋值低于 \(s_r\) 时，该赋值在全相位恒定。恒奇行排除整个相位，恒偶行可删去。

对剩余各行，奇数 \(s_r\) 要求先满足 \(r^{s_r+1}\mid n-S\)。二项展开把它化为 \(i,j\bmod r\) 的一个非退化仿射方程。偶数 \(s_r\) 无需先解方程。用 CRT 合并初始方程，取 \(0\le i_0,j_0<M\)，其中 \(M\) 是奇深度行的素数乘积。令
\[
(i,j)=(i_0,j_0)+M(u,v).
\]
每行接下来只需避开一条非退化仿射直线。偶深度行避开第 \(s_r\) 位为零，奇深度行避开第 \(s_r+1\) 位为零。两种情形的线性系数均由二项展开给出，至少一个系数非零。

先选 \(u\) 避开不含 \(v\) 的直线，再选 \(v\) 避开其余直线。每一步都是在不同素数下各避开一个剩余类。对一组素数 \(T\)，容斥给出足够的搜索长度
\[
L(T)=1+\left\lfloor
\frac{2^{|T|}-1}{\prod_{r\in T}(1-1/r)}
\right\rfloor.
\]
取两组长度的较大者 \(L\)，所得模截断点的两个指数下标均小于 \(ML\)。沿截断点较大加数所在的坐标切片，其下一步已使该加数超过整个截断移位。因此至多 **\(ML\) 个初始切片**足以保留普通最小值。截断点若超过 \(n\)，同一个论证仍然有效。固定相位内的每条切片，可按 #90 的精确赋值同余类合并；合并后的下一位禁类再次用上述区间界处理。

**原生复验。** 取 \(A=3^{97020}, B=5^{18810}\)，中心为 \(7,19,23\)，固定第 31 行为单位余数。令
\[
n=A+B^2+6(7\cdot19\cdot23)^2.
\]
三个首位系数分别为 \((0,1),(6,0),(13,10)\)，旧的三个方向各有一行阻断。从初始 CRT 点 \((1540,1311)\) 出发，独立枚举 \(3\times3\) 修复格，首个可用修复是 \((u,v)=(0,1)\)，得到截断点 \((1540,4370)\)。普通高度穷举另行确认最小点为 \((1,2)\)，三行赋值都是 2。同余反控 \(122027385755\) 保持模 \(7^3 19^3 23^3\cdot31\) 的数据，但普通高度内只有基点，三行赋值都是 1。

### 二、新增转移：单切片无需固定中心相位

固定一个指数后，将移位写成 \(X+YB^j\)，其中 \(j\ge0\)，且 \(r\nmid YB\)。对每个中心 \(r\)，取 \(K_r\) 使 \(r^{K_r}\ge n\)。在正余数窗口内有恒等式
\[
{\bf1}_{v_r(R)\ {\rm 偶}}
=\sum_{k=0}^{K_r-1}(-1)^k{\bf1}_{r^k\mid R},
\qquad R=n-X-YB^j.
\]
每个整除事件等价于 \(B^j\equiv(n-X)Y^{-1}\pmod{r^k}\)，所以它要么为空，要么是模 \(\operatorname{ord}_{r^k}(B)\) 的**一个**指数同余类。首层在实际模 \(r\) 幂循环中定位，下一层沿该类提升；周期只可能保持不变或乘 \(r\)。

把各行的带符号和相乘，用**广义 CRT**合并每一项。相容项 \(j\equiv a\bmod m\) 对 \([0,J]\) 的贡献是带权计数 \(\max(0,1+\lfloor(J-a)/m\rfloor)\)，不相容项贡献零。计数是精确、非降的，可二分首个见证。这个方法不展开联合相位，但乘积项数仍可能随行数增长。

若一个固定相位已给出模截断点，只要它属于原来的外部矩形 CRT 类，较大加数给出的坐标上界也适用于该**整个外部类**。在这个上界内逐切片使用上述计数，即可不预先固定中心相位。这里没有证明总能找到小截断点。

- **正反控。** 固定 \(c=0,\ d=55j\)，保留第 11 行模 \(121\) 的余数。取 \(n=5^{55}+491\)，在中心 \(7,19\) 下首个见证为 \(j=1\)，余数 \(490\) 的赋值是 \((2,0)\)。基点因第 19 行赋值为 1 而失败。反控 \(1582930\) 保持模 \(7^3 19^2 11^2\) 的数据，普通高度内无见证。
- **跨相位剪枝反控。** 固定 \(c=0,d=2j\)，取 \(n=934243858\)，中心为 \(7,19,271\)。25 的实际模素数阶为 \(3,9,27\)。前三行能排除 \(j=0,1,2,3\) 的每一个点，而 \(j=4\) 三行均为单位余数。因此不能把固定相位中“每个不同素数只禁一个剩余类”的短区间论证直接用到共享周期的跨相位情形。

**边界。** 两项结果都只判断指定有限面板和普通高度中的正余数。它们没有证明任意指定 \(n\) 存在两平方余数，也没有解决孙猜想。

### 独立复验

下面的 JavaScript 用 `BigInt`，已运行通过。有限前沿用直接普通高度枚举交叉核对；跨相位用带符号计数。

```javascript
const mod=(x,m)=>(x%m+m)%m;
function ok(x){if(!x)throw Error("assertion")}
function pow(a,k,m){let b=1n;while(k){if(k%2n)b=b*a%m;a=a*a%m;k/=2n}return b}
function v(x,p){ok(x!==0n);let k=0;while(!(x%p)){x/=p;k++}return k}
function ord(b,p){let h=1n,x=b%p;while(x!==1n){x=x*b%p;h++}return h}
function merge([a,m],[b,n]){
    let g=m,d=n,u=1n,w=0n;
    while(d){const q=g/d;[g,d]=[d,g%d];[u,w]=[w,u-q*w]}
    return (b-a)%g ? null : [a+m*mod(u*((b-a)/g),n/g),m*n/g];
}

const P=[7n,19n,23n],H=97020n,K=18810n,M=3059n;
const A=3n**H,B=5n**K,n=A+B*B+6n*M*M,lo=n%(M**3n*31n);
const rem=(N,i,j,q)=>mod(N-pow(3n,H*i,q)-pow(5n,K*j,q),q);
const good=(N,i,j)=>P.every(p=>{
    const x=rem(N,i,j,p**3n);return x!==0n && x%(p*p)===0n;
});
ok(lo===122027385755n && P.every(p=>v(n-2n,p)===1&&v(lo-2n,p)===1));
ok(A%31n===1n&&B%31n===1n&&(n-2n)%31n!==0n&&(lo-2n)%31n!==0n);
const base=[1540n,1311n];
ok(P.every(p=>rem(n,...base,p*p)===0n)&&!good(n,...base));
for(const [a,b] of [[1n,0n],[0n,1n],[1n,1n]])
    ok(P.some(p=>rem(n,base[0]+M*a,base[1]+M*b,p**3n)===rem(n,...base,p**3n)));
const fixes=[];
for(let u=0n;u<3n;u++)for(let w=0n;w<3n;w++)
    if(good(n,base[0]+M*u,base[1]+M*w))fixes.push([u,w]);
ok(String(fixes[0])==="0,1");
function brute(N){
    let best=null;
    for(let x=1n;x+1n<N;x*=A)for(let y=1n;x+y<N;y*=B)
        if(P.every(p=>v(N-x-y,p)%2===0)&&(best===null||x+y<best))best=x+y;
    return best;
}
ok(brute(n)===A+B*B&&brute(lo)===null);

// First j with 1+B^j < N and even valuations at every row.
function first(N,B,P){
    let J=-1n;
    for(let x=1n;x+1n<N;x*=B)J++;
    let terms=[[0n,1n,1n]];
    for(const p of P){
        let a=0n,m=1n,sign=1n;
        const local=[[0n,1n,1n]];
        for(let q=p;q<N;q*=p){
            const f=q===p?ord(B,p):pow(B,m,q)===1n?1n:p;
            let i=0n;
            while(i<f && (N-1n-pow(B,a+m*i,q))%q)i++;
            if(i===f)break;
            a+=m*i;m*=f;sign=-sign;
            local.push([a,m,sign]);
        }
        terms=terms.flatMap(([a,m,s])=>local.flatMap(([b,k,t])=>{
            const z=merge([a,m],[b,k]);
            return z?[[...z,s*t]]:[];
        }));
    }
    const count=j=>terms.reduce((s,[a,m,w])=>s+(j<a?0n:w*(1n+(j-a)/m)),0n);
    if(!count(J))return null;
    let l=0n,r=J;
    while(l<r){const m=(l+r)/2n;if(count(m)>0n)r=m;else l=m+1n}
    return l;
}

const D=5n**55n,N=D+491n,L=1582930n;
ok(N%(7n**3n*19n**2n*11n**2n)===L&&D%121n===1n);
ok(ord(D,7n)===6n&&ord(D,19n)===9n);
ok(first(N,D,[7n,19n])===1n&&first(L,D,[7n,19n])===null);
ok(v(N-2n,19n)===1&&v(N-1n-D,7n)===2&&v(N-1n-D,19n)===0&&(N-2n)%11n!==0n);

const Q=[7n,19n,271n], T=934243858n;
ok(String(Q.map(p=>ord(25n,p)))==="3,9,27");
ok(first(T,25n,Q)===4n);
for(let j=0n;j<4n;j++)ok(Q.some(p=>v(T-1n-25n**j,p)%2===1));
ok(Q.every(p=>(T-1n-25n**4n)%p!==0n));
```


## 三、跨相位反控：两两有普通见证，三行合并无解

### 反控与同余正控

取中心 \(7,19,23\)，外部矩形类为 \(c\equiv d\equiv0\pmod{55}\)。由于 \(3^{55}\equiv5^{55}\equiv1\pmod{121}\)，这个类保留第 11 行的完整模 \(121\) 余数。设
\[
n=5^{55}+1+2089266102122,\qquad
M=7^3\,19^3\,23^3\,11^2.
\]
这里 \(n\equiv3\pmod{121}\)，所以第 11 行始终是单位余数。由移位的单调性，严格低于 \(n\) 的指数对恰有以下三个：

| \((c,d)\) | \(v_7,v_{19},v_{23}\) | 同一中心相位的模修复 |
|---|---|---|
| \((0,0)\) | \((1,0,0)\) | \((990,0)\) |
| \((55,0)\) | \((0,1,0)\) | \((15895,0)\) |
| \((0,55)\) | \((0,0,1)\) | \((3960,55)\) |

右列各点保留相应行的指数模 \(990\) 数据，且在三个中心的余数赋值均为 0 或 2。三点的移位都大于 \(n\)。因此删去任一中心后恰有一个普通见证，三行合并则为零。这个结论直接检查整个外部矩形类的普通窗口，无需预设小截断点。

作同余正控，取
\[
n_+=3^{990}+1+3092451464759944.
\]
它与 \(n\) 同余模 \(M\)。在 \(n_+\) 下，穷举与带符号 CRT 均数得 **112 个面板见证**。其中 \((990,0)\) 的中心赋值为 \((2,0,0)\)，但其余数在遗漏的素数 31 处赋值恰为 1，所以这个见证的余数不能写成两平方。

同一目标与同一外部矩形类中，两两筛查有普通见证不能推出三行共同见证。仍只涉及有限局部面板。

### 最短独立复验

以下 JavaScript 独立运行， 已用 `BigInt` 运行通过，核对三行与全部删行计数、三个相位外的模修复，以及同余正控。

```javascript
const P=[7n,19n,23n], A=3n**55n, B=5n**55n;
const n=1n+B+2089266102122n, up=3n**990n+1n+3092451464759944n;
const M=121n*P.reduce((m,p)=>m*p**3n,1n);
const mod=(a,m)=>(a%m+m)%m;
function ok(x){if(!x)throw Error("assertion")}
function pow(a,k,m){let x=1n;while(k){if(k%2n)x=x*a%m;a=a*a%m;k/=2n}return x}
function v(x,p){ok(x>0n);let e=0;while(x%p===0n){x/=p;e++}return e}
function merge([a,m],[b,k]){
    let g=m,d=k,u=1n,w=0n;
    while(d){const q=g/d;[g,d]=[d,g%d];[u,w]=[w,u-q*w]}
    return (b-a)%g?null:[a+m*mod(u*((b-a)/g),k/g),m*k/g];
}
function slice(N,x,J,primes){
    let out=[[0n,1n,1n]];
    for(const p of primes){
        let h=1n,z=B%p;
        while(z!==1n){z=z*B%p;h++}
        let a=0n,m=1n,w=1n,local=[[a,m,w]];
        for(let q=p;q<N;q*=p){
            const f=q===p?h:pow(B,m,q)===1n?1n:p;
            let j=0n;
            while(j<f && a+m*j<=J && (N-x-pow(B,a+m*j,q))%q)j++;
            if(j===f||a+m*j>J)break;
            a+=m*j;m*=f;w=-w;
            local.push([a,m,w]);
        }
        out=out.flatMap(([a,m,w])=>local.flatMap(([b,k,z])=>{
            const g=merge([a,m],[b,k]);
            return g&&g[0]<=J?[[...g,w*z]]:[];
        }));
    }
    return out.reduce((s,[a,m,w])=>s+w*(1n+(J-a)/m),0n);
}
function counts(N,primes){
    let brute=0n,crt=0n;
    for(let x=1n;x+1n<N;x*=A){
        let J=-1n;
        for(let y=1n;x+y<N;y*=B){
            J++;
            if(primes.every(p=>v(N-x-y,p)%2===0))brute++;
        }
        crt+=slice(N,x,J,primes);
    }
    ok(brute===crt);
    return crt;
}

ok(A%121n===1n&&B%121n===1n&&n%121n===3n&&(up-n)%M===0n);
ok(1n+B<n&&n<A+B&&n<A*A+1n&&n<1n+B*B);
const s=(c,d)=>3n**c+5n**d;
const points=[[0n,0n],[55n,0n],[0n,55n]];
const repairs=[[990n,0n],[15895n,0n],[3960n,55n]];
for(let i=0;i<3;i++){
    ok(P.every((p,j)=>v(n-s(...points[i]),p)===Number(i===j)));
    ok(repairs[i].every((e,j)=>(e-points[i][j])%990n===0n));
    ok(s(...repairs[i])>n);
    ok(P.every(p=>{
        const r=mod(n-s(...repairs[i]),p**3n);
        return r%p!==0n||(r!==0n&&r%p**2n===0n);
    }));
    ok(counts(n,P.filter((_,j)=>j!==i))===1n);
}
ok(counts(n,P)===0n && counts(up,P)===112n);
const residual=up-s(...repairs[0]);
ok(P.every(p=>v(residual,p)%2===0)&&v(residual,31n)===1);
``` 
