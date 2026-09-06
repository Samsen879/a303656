# Definitions — original rows, three blocker graphs, and proof scope

所有定义绑定 `Samsen879/a303656` 的 main
`44e522dd6e88504e2b9829f0b27359e6c45a76ff`；原始来源见 `SOURCE_READING.md`。
本包没有更改 admitted arithmetic class。

## 1. 原始行与两个 anchors

P 是有限个不同的素数 p≡3 (mod 4)。每行使用 K_p≥2、一个两 anchors
c=0,1 共用的 r_p modulo p^K_p，以及非空的正奇 accepted valuations
E_p⊂{1,…,K_p−1}。定义

    V_(p,c)(d)=r_p−3^c−5^d,
    w_p=ord_p(5), s_p=v_p(5^w_p−1),
    a_p=max(0,K_p−s_p), ell_p=w_p p^a_p.

`V ≡ 0 (mod p^K_p)` 是 LOCAL_ZERO_UNRESOLVED，不是 valuation K_p，不能接受。
`regular` 指 s_p=1；`nonregular` 指 s_p≥2。原始潜在 rigid resource pool 是
Q={p∈P:s_p≥2}；并不要求其中每行在已冻结的参数下真的 rigid-active。
5 是坐标标签时合法，但永远不是本类中的 row label。

## 2. U、L、beta 与 coarse fatal

可选 sound two-adic row 的周期 t_2，在 K_2=2 时为1，否则为2^(K_2−2)；
没有该行时取1。

    U=lcm(t_2,{w_p:p∈P}), L=lcm(t_2,{ell_p:p∈P}), beta_lambda=v_lambda(U).

一行在 x modulo U 上 coarse fatal，当且仅当 x 的每个 full lift modulo L
都由同一行接受。不能把“至少一个 full lift 被接受”换成该定义。
原仓库的 reverse CRT theorem 给出 coarse escape / full escape 等价。
本包新的 guard-forest 证明也可直接在 L 的 CRT 坐标上构造 full escape，
不需要对 contraction macro 应用 reverse CRT。

## 3. Dynamic / rigid

Dynamic p-row 的 lower guard 是一个 exponent logarithm class modulo w_p。
在自己的 p-coordinate 上，令 m=min(a_p,beta_p)，其 fatal event 是

    union_{0≤j<m, s_p+j∈E_p} {x:v_p(x−zeta)=j}.

它排除 center cylinder x≡zeta (mod p^m)。对应 conditional mass 是
sum (p−1)/p^(j+1)。只有 p 本身这一行能提供该坐标的 dynamic event。

Rigid fatal row q 需要一个 accepted odd h<s_q，所以只能来自 Q。
其 event 是一个 class modulo w_q，rank 是 P⁺(w_q)；固定所有更低坐标后，
它是 depth v_lambda(w_q) 的一个 lambda-adic cylinder。
同一 nonregular row 在另一 anchor 可为 dynamic 或 inert；标签不能跨 anchor 偷换。

## 4. Actual fiber、macro、Kraft 和 paired resource

Actual full fiber 是固定 lower assignment 后，原始 rank-lambda events 的实际
union 等于整个坐标纤维，不是 mass sum≥1。

Provenance macro 是 exact minimal slice-cover witness 的 stripped guards 交；
可能具有 rigid cylinder geometry，但不是新的 prime、row 或独立 residue。

Kraft frontier 是互不嵌套的 complete prefix cylinders；其 depths 满足
sum n_d/lambda^d=1。正的总 mass 不保证某个 prescribed branch 被覆盖。

Paired resource 是一个 actual q 与同一 r_q 产生的完整两个 anchor configurations。
不得把两边各自可行的 cylinders 随意配对；一行在每个固定 anchor/fiber 至多一片。

## 5. 正整除 guard 与 forbidden digits

若 r_q−3^c modulo q 在 <5> 内，定义唯一 b_(q,c) modulo w_q 满足
5^b = r_q−3^c (mod q)；否则该 anchor 没有 positive-divisibility guard。

    q | V_(q,c)(d)  iff  d ≡ b_(q,c) (mod w_q).

因此对任一 odd lambda|w_q，避开 b_(q,c) modulo lambda 就使该行不整除。
若使用完整 lambda-primary congruence，避开 b modulo lambda^e，e=v_lambda(w_q)，
同样使整除不可能。这里阻断的是整除本身，比只阻断 rigid fatal 更强。
两个 anchors 的 V 相差2，一条 odd row 不可能在同一 exponent 上同时正整除。

## 6. Direct blocker graph — 原问题的图

    O(q)={odd primes lambda:lambda|w_q},
    N_P(q)=O(q)\P,
    c_lambda=(lambda−1)/2, h_lambda=lambda−1.

c 是 paired worst-case capacity；h 是 selected-single-anchor capacity。
两者均为整数；本包没有用 floating-point 判定任何容量。

最小 deficient core S 指 S 非空、|S|>C(N_P(S))，且所有 proper subsets Hall-good。
该“最小”仅指 inclusion，不代表按 prime 大小全局最小。

## 7. Transitive panel frontier

对 p∈P，按严格下降的 order support DAG 递归：

    F_P(p)=union_{lambda∈O(p)} ({lambda} if lambda∉P else F_P(lambda)).

这里可能得到空集，例如 p=3。可同时使用 c 或 h 容量。

本包后续先使 row 3 在选定 anchor 上不活跃，然后把3作为预先释放的 terminal。
令 P'=P\{3}，对 p∈P' 用同一递归定义 F^3_P(p)，但遇到3就终止。
这不是删去 row 3，也不改变 U、L；只是证明该行的 guard 在所选 boundary 已经为假。

## 8. Absolute frontiers — 三个符号不要混淆

未预处理的 absolute frontier B(p)：沿每个 admitted odd factor 递归，遇到
lambda≡1 mod4 才停止。因此 B(3)=empty。

主要使用的 boundary-primed absolute frontier T(p)：

    T(3)={3};
    T(p)=union_{lambda∈O(p)}
         ({lambda} if lambda≡1 mod4 else T(lambda)), p>3 admitted.

T(p) 非空且有限，所有 terminals 属于 {3}∪{primes≡1 mod4}。
T(S)=union_{q∈S}T(q)。B(p)⊂T(p)，两者只可能差一个 terminal 3。

这些 absolute descendants 是算术分析对象，不是假装加入了不在 P 中的 rows。
实际释放路径走到第一条不存在的 row label 时就停止；该标签已经是 free coordinate。

## 9. Guard forest / gateway / counting

从每个 q∈Q 选一条有限的下降路径。实际存在的 relay row 必须被更小坐标阻断。
路径可合并；同一 original row 只保留一个 outgoing guard-blocking edge。
`incoming load` 数的是 distinct original rows，不是路径数，也不是 macro 次数。
路径数仅提供这个 load 的上界。

A terminal gateway 是路径最后一条 actual row。最大因子路径到3的 gateway 满足
w=3^e 或2·3^e；pure-{5} 路径到5的 gateway 满足 w=5^e 或2·5^e。
其他 mixed 路径的 gateway 不必满足 pure-order 限制。

## 10. 最终 exceptional class

E 是所有 finite admitted panels P，满足

    |Q|≥7,
    exists nonempty S⊂Q: |S| > sum_{lambda∈F^3_P(S)} (lambda−1).

其中 F^3_P(S) 是 panel-relative boundary-primed frontier 的 union。它还强迫
absolute T 图存在一个 deficient subset（不一定是同一个 minimal subset）。

这是潜在 complete-certificate panels 的一个 explicit necessary arithmetic class，
不是已经构造出的 complete certificates，也不是声称其中所有 panels 都会存活其他测试。

最小 terminal-Hall circuit S 仍可能只有3行；`|Q|≥7` 约束的是完整 panel 的
nonregular 总资源数，不是每个 inclusion-minimal circuit 的大小。
