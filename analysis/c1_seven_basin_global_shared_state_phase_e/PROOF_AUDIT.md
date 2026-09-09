# 重点证明审计记录

## 1. 统一状态不是七个局部量词

E1的a_i只用于一次性定义各original row的r_p；D_i两两不交意味着同一p不会收到两个赋值。随后CRT求一个globalR，所有d共享它。七个互斥叶对应的是七个universal conditional duties，不是要求一个d落在七叶交集。

## 2. Branching与高3-depth

least-mismatch选最小actualregularp，依赖所有oddorderfactors>3都为更小的同盆地节点；缺失或非admittedfactor不能默认匹配。允许3^2和3^3，因为a_i与d在整片leafdepth上已经匹配；只对>3的orderfactor用平方自由条件。

## 3. Parity-deletion的关键性

唯一lowerlog使even-order行在反parity彻底inactive。失活helper的owncoordinate可自由用来破坏上游log，沿actualfactorpath一直传到root。off-pathregularrows的safechoices不会倒改lowercoordinates。此证明使用actualrowp，而不是把macro当作prime。

它证明whole-private-fiber profile为空；不声称该盆地对所有点的覆盖集合都为空。这个区分是E4不可省略的前提。

## 4. 外部行

外部regularrow可能同时读取不同盆地的坐标，所以任意typedCSP不能假定全部因子分离。但core闭包不读取外部owncoordinates，给定coreescape后可按素数递增安全延伸。正面构造已经用core完成BOTH，外部positiveevents无害。没有重新定义原U/L。

## 5. E4的三个位置

31和7是两个完整第一层叶A、B；5167一定在第三个第一层分支C内部。反parity失去7和5167后，row3需完整覆盖B与C中指定二级叶，强制中心首位A以及接受valuation1。若31也失去完整profile，row3在A的安全中心给全局escape。K3奇数时localzero仍安全，不能把sentinelK3当fatal。

## 6. 必要性与充分性的量词范围

E4用于任意来源normal-form内的完整frozenstate，不要求事先canonical。E5是可选择合法states的存在性定理，统一取K2,E1。它不声称每个frozenr成功，也不为任意不接受1的预固定E提供状态。

## 7. Pairwise与三阶MUS

七乘七矩阵针对selectedparityleafduties，构造给出同一个globalwitness；不是靠pairwisepass推出Helly性质。row3的三项MUS是实际模9状态，其由盆地导出的强制性只在parity-defective31子类成立。不是普遍的seven-rootMUS。

## 8. Tau、typedmasks和resultants

lastroot必须选全局最大q，tau冻结另外六根及所有helpers。canonicalA1escape投影在原始w_q上至多一个log，因此不需要paired±2或multi-usegcd。未知q未被作为实际SAT行。typedprofile代数是exact；54cell正面检查使用保证A1覆盖的lower-envelope，不声称已枚举未知根全部mask。

## 9. 状态与算术

E1/E5假设每个输入prime、exactorder、regularity/nonregularity及全部closure都实际成立。这些有限输入目前没有一套完整七根实例。正面的条件定理不能用于断言A303656成立或不成立。E4只是新增necessaryarithmeticgate O31，不是已证明该族为空。

## 10. 复审状态

本包提供数学证明与一次独立standalonereference实现。没有proofassistant证书、没有另一作者的独立证明签署、没有repository-nativeintegrationreplay。下一次独立复审最应优先逐条检查E3路径safe-extension与E4完整private-fiber到row3whole-cylinder需求的转换。
