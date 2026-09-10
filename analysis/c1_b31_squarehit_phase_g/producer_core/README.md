# Phase G research evidence package

本包是严格限定的路线排除与reference evidence，不是目标squarefree证书。两个Phase G包共用同一证明/代码路径，不代表两套独立作者或独立软件栈复算。

## Files

REPORT.md 为该任务的完整十节报告。PROOFS.md 为共用完整证明与反例。results.json 保存可机读结论。AUTHORITY.json 与 SOURCE_BINDING.json 保存来源路径、观察与未完成事项。certificates.json 包含recursive full n−1 Lucas证书；evidence.json 为实际有限replay结果。

## Replay (Python 3.10+, standard library only)

```bash
python3 reference.py --self-test --output fresh.json
python3 -c "import json; assert json.load(open('fresh.json')) == json.load(open('evidence.json')); print('EVIDENCE MATCH')"
sha256sum -c SHA256SUMS.txt
```

关键检查使用显式异常而非assert，所以也可用 `python3 -O reference.py ...`。上面的短对比命令请不要用-O。

`generate_certificates.py` 是可选的一次性证书提议脚本，需要SymPy；不是必要replay步骤。真正的素性验证只用标准库Lucas判据，不依赖生成阶段的probable-prime结论。脚本没有任何target-q扫描。

本包checksum验证的是交付文件；不等于已独立重放源仓库producer hashes。历史Dorais–Klyve搜索穷尽性来自文献，不由本包重跑。无限域证明未形式化。
