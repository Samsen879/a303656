# Reproduction

## 环境

本轮使用 CPython 3.13.5，standard library only，无需网络或原仓库代码。其他支持所用语法/API 的现代 Python 可运行；byte-identical seeded regression 以 `ENVIRONMENT.json` 中的版本为基准。

**不要使用 `python -O`**，因为 reference laboratory 使用 assertions 作为 fail-closed verification。

## 检查原始 bundle

在目录根部运行：

```bash
sha256sum -c SHA256SUMS.txt
```

## 独立输出到新目录

```bash
replay_dir=$(mktemp -d)
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=0 \
  python3 tools/reference.py --out "$replay_dir/results"
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -v
python3 tools/verify_integration.py --replay-results "$replay_dir/results"
python3 tools/finalize_integration.py --verify
```

比较九个 generated JSON files，不要将人工编写的 source binding、环境记录、报告当作程序 outputs：

```python
from pathlib import Path
expected = Path('results')
actual = Path('/path/from/mktemp/results')
assert {p.name for p in expected.glob('*.json')} == {p.name for p in actual.glob('*.json')}
for p in sorted(expected.glob('*.json')):
    assert p.read_bytes() == (actual / p.name).read_bytes(), p.name
print('All generated JSON outputs are byte-identical.')
```

`REPLAY_RECEIPT.json` 记录本轮第二个输出目录的 byte comparison；它不是第三方独立软件栈审计。

## Mathematical specification

Countermodel events 使用坐标索引、lower CRT conjunction、bitmask slice、anchor、shared row identity 和 provenance。`rectangular` 与 `nested` 的参数 domain 在代码与报告中完整指定；计数仅针对这些 templates。

Arithmetic examples 固定 primes 67、20771，K=2，E={1}，三个 shared residue pairs 为 `(2,13471)`、`(0,4494)`、`(2,20775)`。所有 full periods 均为228470。

Additional audits 固定为报告所列 truth-table domains、seed20260905 的1000个系统、two-adic K=2..8，以及 `5**15-1` 的完整 factorization。没有增加 prime scan，也没有尝试覆盖全部 actual admitted systems。

## Scope guards

不能把 PASS 解释为 actual H1/H2 被反驳、普遍 C=1 no-go、A303656 已解决，或 repository authority 改变。所有 statements 的 exact quantifiers 和附加假设以 `REPORT.md` 为准。
