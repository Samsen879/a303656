# Phase E 七盆地共同状态研究包

首先阅读 `REPORT.md`，其 E1–E5 给出本轮新证明与范围；`SOURCES.md` 将源结论和新推导分开；`AUTHORITY.json` 记录live-main绑定；`RESULTS.json` 是本轮实际运行输出。

核心结论：没有排除 exactly-seven。七个 mandatory selected-parity roles 可统一构造。完整 simultaneous C=1 还要求31盆地全奇阶；本报告证明该必要条件，并在它成立时给出任意branching七盆地的完整共同状态。

**没有实例化七个nonregularterminals。** 条件构造允许的actualprime-input不是抽象伪造的prime rows。

复算（仅需Python3标准库）：

```bash
python3 reference.py --output RESULTS.local.json
```

`RESULTS.json` 与重新运行的输出可能在计时字段不同；数学checks应一致。检查不导入仓库实现，不进行联网、大型扫描或GitHub写入。

包内未包含原repo checkout或全量源包。这里的Git blob OIDs来自连接工具返回值，manifest只校验本地新产物。

```text
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
GITHUB WRITES PERFORMED: NONE
```
