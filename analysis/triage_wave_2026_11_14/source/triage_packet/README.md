# A303656 Triage audit — 2026-11-14

## 范围与状态

A303656 保持 **UNRESOLVED**。本包是本次 triage 的证明与复算附件，不是原猜想的证明，也不包含 STATUS.md 更新文件。没有修改 GitHub 仓库。

本次选定的主线资产是 A2 finite-zero detection、V weighted integer L² transfer，以及本轮在冻结 C21 上新证明的 **C22 / 23-root necessary condition**。原始 Round-1 R1-b/R1-c 完整手稿未取得；V/L 提供的是独立重建，不能据此声称审过缺失原稿。

## 新结果与依赖

1. **C22**：至多22个任意 inert unit targets，加任意 finite external regular norm conditions 与 finite 2-adic norm condition，可同时在正 exponent Haar mass 上满足。固定允许的2-primary cylinder后，7与11的 bad events分别只用odd exponent3-primary与5-primary coordinates，故联合 upper budget 为31/75，而旧core为34/75。其余events仍作未条件化的union bound。所有33个预算小于1，最坏4238011529/4390848000，余量152836471/4390848000。
2. **23-root corollary**：任何 finite eventual-power norm zero f_q(a)=0 至少需要23个不同 p>3，满足p≡3(mod4)、p²|q、3^(p−1)≡5^(p−1)≡1(modp²)。LP仍未证明，不能替换仓库ordinary admitted C=1的seven-root结论。
3. **E2 unit-noise bridge**：对固定canonical λ(x)∈{1,2,18}，lim Δ_Y = Haar(∪_Y{a_Y=0})。因此Δ_Y→0 iff所有finitecanonicalbranches均正。该primitive positivity仍OPEN；它蕴含原norm LP，但反向未证。两份独立证明明确保留joint μ、full lower exponent conditioning、λ18 exact v3=2与piecewise martingale不必mean1。
4. **E1 C32 bridge**：MP-LT iff所有finite C32 primitive profiles为正 iff对应primitive limit在Haar-a.e.为正。新的unit-noise support theorem补上了原报告中finite positivity到quantile的接口；该finite gate仍OPEN。它和E2 canonical gate没有已证的global等价/蕴含。C22另给E1安全corollary：含prime3在内共≤22个inert unit primes时profile全正，故E1 finite zero至少23个distinct inert primes；此处没有joint-nonregular或p²要求。
5. **W6 model bridge**：W∞^(6)=E[f∞/π | bad-prime coordinates]且零集相同a.e.。这不证明unweighted integer SM。

## Reproduction

仅需Python标准库。在本目录运行：

```bash
python checks/root_c22_check.py
python checks/c22_independent_budget.py
python c21_frozen/verify.py
```

前两份独立实现均从80个odd19-smooth h<512重新构造整数products与GCD，认证60个prime factors、46个inert rows及33项rational budgets。第一份同时重放原29项C21预算。脚本可能在自身目录写入JSON复算结果；其中seconds/hash不作为数学证据，确切有理数才是核对对象。

为可移植性，只把第二份脚本的输出目录从本次workspace绝对路径改为脚本所在目录；数学代码未改。root脚本的scope元数据由pending改为accompanying-refereed；此项不参与预算计算。原冻结C21资料保持原样。

## 正文和原始来源

- A2完整报告： https://chatgpt.com/library?file_id=libfile_dd177e741b088191b0ad7fe03fd204ab&account_id=personal
- R1 A2 referee： https://chatgpt.com/library?file_id=libfile_ba5578b5e2e08191b8d11757e100c841&account_id=personal
- R2完整报告： https://chatgpt.com/library?file_id=libfile_9edd8e5abe2c8191a33016d0d8770b66&account_id=personal
- V完整重建： https://chatgpt.com/library?file_id=libfile_1946127b0bf481919411d8da09597d95&account_id=personal
- E2完整报告： https://chatgpt.com/library?file_id=libfile_331d160e6d0481918ddd3cdc69598982&account_id=personal
- L独立重建： https://chatgpt.com/library?file_id=libfile_e2f61f57153081919b0034e143c1b812&account_id=personal
- Pomerance–Shparlinski primary PDF： https://math.dartmouth.edu/~carlp/PDF/paper128.pdf
- Chamizo published paper： https://link.springer.com/article/10.1007/s00009-021-01959-3
- Pinned baseline： https://github.com/Samsen879/a303656/tree/ba7f028bb7bad69885e34549969059c00487380b

Private chat /c/ links没有被当作可读正文；本包审查基于取得的Library报告和冻结证书。旧报告的自述工时、模型标签和PASS字段都不替代证明。新claims的完整scope与proof可在proofs/对应referee记录中核对。

## 必须保留的反推边界

Finite exponent window、finite eventual norm zero、finite canonical unit zero和ordinary admitted row certificate是不同对象。若f_q有zero，删除split factors并把inert precision降到最大偶数后，ordinary witnesses仍可能全部落在有限c-transient rows；不得从modelzero直接宣布原整数反例。

E2 λ18 conditioning会改变271的refined weight，实际conditional bad mass可为1/30，高于C21的未条件化1/81；这否定预算直接移植，不是zero-selector证书。完整catalogue没有joint-nonregular rows也不允许删除这些行，因为归纳会创建regular artificial targets。
