# 固定来源与新推导边界

全部 repository paths 绑定 main commit
`fd59aad038a09f2fc6df7039111408fa231c27dd`，tree
`afd34fc936f83867758c827bfcd8b7b9d9b8d5b5`。

阅读方式为连接的 GitHub GET、固定 SHA 的 fetch_file，以及 PR22/24/26/27/28/29 的完整 diff。没有执行 GitHub writes。历史包自己的 authority header 不替代本轮的 main binding。

## S1 — Order-DAG Phase C

目录：`analysis/c1_order_dag_phase_c/`。
主要使用 `THEOREMS.md` Theorems7.1–7.2、Section12，及该包 REPORT、精确 inventory/实现。
核心支持：N>=7、first nonlinear rank3、七叶 normal form、actual closed disjoint basins、conditional seven-head construction。

固定位置：
`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_order_dag_phase_c/THEOREMS.md`

返回的 Git blob OID：`0c86de426dc932a13a4d7cccb198e4ef3bd7c811`。

## S2 — Global Shared State Phase C

目录：`analysis/c1_global_shared_state_phase_c/`。
主要使用 REPORT C2/C3、safe extension、C7/C8/C9、typed residual semantics、actual fractional/integral gap、multi-use resultant conditions，连同该包实现与输出。
核心支持：一个 actual row 只有一个 shared residue；local zero fail-closed；全域 pooled EITHER 不等于 fixed-anchor 或 BOTH。

固定位置：
`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_global_shared_state_phase_c/REPORT.md`

此索引未单独抄录该 REPORT 的 blob OID；不伪造缺失 hash。

## S3 — Two-Nonregular Phase D

目录：`analysis/c1_two_nonregular_global_shared_state_phase_d/`。
主要使用 REPORT §§4–9、D1/D3/D4/D6、actual31 collision、h67 multi-use resultant gate，以及精确 reference/integration 输出。
核心支持：保留 existential tau 的 J_q(D) iff；完整 primary-coordinate separators；whole-profile consistency；实际 shared-relay state collision。

固定位置：
`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_two_nonregular_global_shared_state_phase_d/REPORT.md`

Git blob OID：`28df427f73da0672d680803452685192c734e0e1`。

## S4 — Provider Charging Phase D

目录：`analysis/c1_private_provider_charging_phase_d/`。
主要使用 REPORT/THEOREMS 的 center-provider ancestry、support confinement、fixed-shadow width、exactly-seven capacity audit；同时阅读该包参考输出及实现。
核心支持：外部 regular rows不能为已有 rigid-origin宏创造额外support；七个capacity1对应七叶，计数无欠账。

固定位置：
`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_private_provider_charging_phase_d/REPORT.md`

Git blob OID：`da6c7b743fd6995895b6ad53f79197b1a6ad0767`。

## S5 — B7 Phase D

目录：`analysis/c1_b7_pure3_phase_d/`。
主要使用 REPORT §§9–10、basal gateway定义、D5 arbitrary-branching filling，并区分 actual-prime集合与待检验 order templates。该包 factorization/primality证书及实现作为来源阅读，不宣称全部重新执行。

固定位置：
`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_b7_pure3_phase_d/REPORT.md`

Git blob OID：`32327b1f799748101febb8222494eed2cf3cda70`。

## S6 — Seven-head Chain Phase D

目录：`analysis/c1_seven_head_chain_realizability_phase_d/`。
主要使用 REPORT §2 two-anchor/CRT/U/L reconstruction、§3 D-ALT、actual regular prefixes与未实例化terminal的边界；阅读其 arithmetic tables、verifier、certificate/integration material。

固定位置：
`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/analysis/c1_seven_head_chain_realizability_phase_d/REPORT.md`

Git blob OID：`731560372ab3cc3aa049bef5df1db7f1143d7150`。

## S7 — Live authority/status

`https://api.github.com/repos/Samsen879/a303656/branches/main`

`https://github.com/Samsen879/a303656/blob/fd59aad038a09f2fc6df7039111408fa231c27dd/STATUS.md`

STATUS Git blob OID：`2ba295c0ada0d19b4e7f7d7871312d0696a785d2`。

main于开始与末段重新读取，均为上面的固定SHA。STATUS仍为PAUSED、NONE、UNRESOLVED。

## 新推导，不是来源既有定理

REPORT E1是S5的branch-filling推广到全部depth1/2/3盆地；E2把它用于全七叶；E3以实际order-path失活/安全延伸证明parity-deletion；E4由7、5167的失活和row3中心几何推出O31；E5给一般branching下的完整BOTH构造。七根last-root singleton trace是这些新构造的推论。

来源已有literal H0 conditional compatibility；本轮只做重建/复算，不冒称新定理。所有source theorem dependencies均保留其admitted-ledger、frozen-state、boundary-anchor范围。

## 复算边界

`RESULTS.json` 仅记录本轮 `reference.py` 真正执行的检查。源runner PASS、CI PASS、全量prime inventory、巨大resultant的构造均未作为本轮fresh replay。一个源resultant因子分解后的整数gcd在本轮复算，但factorization本身仍是源输入。

`MANIFEST.json` 是本轮本地artifact的SHA256，不是下载并重新hash整个repository的收据。
