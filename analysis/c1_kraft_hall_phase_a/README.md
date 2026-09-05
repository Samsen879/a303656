# A303656 Kraft–Hall targeted Phase A research packet

这是从冻结 standalone research/reference bundle 重建的 repository-native integration。

主报告：`REPORT.md`。实际 reading 与 replay 范围：`SOURCE_READING.md`。冻结计算目标：`COMPUTATION_SPEC.md`。

核心结果：无 q 上界的 R_(3,d)=empty (d=1,2,3)，81-row rigid-only / 21-row dynamic-allowed bounds；paired-resource nonzero resultant invariant；zero-lower depth-one ell=5,7 double-resource exclusions；corrected ancestor-aware branch inequality 与 exact configuration accounting。

## 验证文件完整性

在本目录下执行：

```bash
sha256sum -c SHA256SUMS.txt
```

## 重复全部 reference calculations

需要 Python 3.10 或以上；不需网络、repository clone 或第三方 packages。不得使用 `python -O`，程序会拒绝关闭 assertions 的运行。

```bash
replay_dir=$(mktemp -d)
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
python3 tools/run_all.py --output "$replay_dir/replay.json"
```

Runner 在 temporary directory 重新生成8个 result files，并逐字段比较参考结果。仅排除明确名为 `seconds` 的 performance 字段；整数、分类、lists、scope text 都作 exact comparison，不使用 tolerance。输入 bundle 中的 reference results 不会被覆盖。生成的 replay summary 给出 canonical mathematical SHA256。

报告中的初次 timings 保留在 reference JSON；重新执行时不要求 wall-clock time 相同。Raw-file integrity 与 mathematical reproducibility 是两个不同检查。

## 仅核验有限 proof certificates

```bash
python3 tools/verify_theorems.py --output "$replay_dir/theorems.json"
```

该 verifier 使用 deterministic trial division、整数 Bareiss determinant、有限 tree enumeration 和 exact Fractions。它验证 finite certificates 和 finite combinatorial tests；不是 Lean/Coq formal proof，也不替代对 REPORT.md 中一般定理证明的人工审阅。

## 文件

`tools/generate_certificates.py` 用 polynomial Euclidean algorithm 独立生成 resultants，与 verifier 的 Sylvester/Bareiss 算法不同。`panel.py` 只允许冻结的100000和10000000两个 bounds；`paired.py` 给逐 lower class 的完整 pair graph；`replay.py` 复算 main 的两个 actual examples；`counterexamples.py` 检查 actual position 与 blanket-one-sidedness 反例。

## Scope guards

所有 prime-resource bounds 都针对 original actual rows，不把 derived provenance macros 当新 primes。One-anchor 自由 residue 选择与 fixed/common-residue choices 分开。Prime panel 的 absence 保持 bounded。Coordinate-specific obstruction 不等于 arbitrary complete-certificate no-go。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
REPOSITORY INTEGRATION: DRAFT PR ONLY
```
