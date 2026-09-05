# Source basis / reading and replay scope

统一 repository binding：`Samsen879/a303656@0200beede923c56e0284d9555c1dabaf91fa1755`。

## GitHub live reads

通过 connector 读取 main branch object、PR #11/#12/#13 metadata、绑定 SHA 的 STATUS，以及 #12 的 git commit object。结束前再次读取 main，SHA/tree 未变。第一 parent chain 明确包含三个 merge commits。没有 GitHub writes。

## Mathematical texts read

下面是本轮实际 mathematical source basis，不是本地 checkout 清单。通过 `fetch_file` 分段或 `fetch_blob` 读取：

- `STATUS.md`、`docs/THEOREM_INDEX.md`、`docs/ROUTE_MAP.md`。
- `analysis/c1_entangled_coordinate_deficit/FORMAL_CLASS.md`、`THEOREM_AUDIT.md`：boundary-aware class、rigid/dynamic normal forms、DAG、coordinate criterion。
- `analysis/c1_minimal_saturated_coordinate_inverse/source/A303656_MINIMAL_SATURATED_COORDINATE_PHASE_A/DEFINITIONS.md`、`ABSTRACT_CLASSIFICATION.md`、`REALIZABILITY_AUDIT.md`、`REPORT.md`：full-fiber witness、prefix frontier、resource injection、one/two-anchor separation。
- `analysis/c1_contraction_tree_phase_a/DEFINITIONS.md`、`REPORT.md`：rank、actual saturation、semantic contraction、earlier missing closure scope。
- `analysis/c1_two_anchor_common_residue_phase_a/REPORT.md`：全篇分段读取；dynamic exclusion、rigid tax、H1、paired objects、finite counts。
- `analysis/c1_prefix_frontier_realizability_phase_a/REPORT.md`：definitions、Theorems A/B/C、construction、counts、scope及 conclusion；另读取 `THEOREM_AUDIT.md`。
- `analysis/c1_hereditary_shell_phase_a/REPORT.md`：全篇；明确 provenance macros 不成为新 actual arithmetic rows。

部分相关目录的 recursive trees 也已枚举。巨大 generated catalogs、每个程序文件和所有 manifests 没有全部逐行阅读；本轮不声称已完成请求中“完整目录读取”的逐字节版本，也不声称做过 repository-native integration audit。本文的 mathematical deductions 只依赖上述明确文本与本文给出的独立证明。

## Important source blob identifiers

```text
entangled FORMAL_CLASS        2a788348cf9abdce43f47809b7b6fd6cb8f3f04d
entangled THEOREM_AUDIT       33fb391b6547fce68bb7a1964d3757fa5b5c8910
minimal DEFINITIONS          5908a3373a5e8d0997c6df387be59e17239f961a
minimal ABSTRACT_CLASS       7ad233f07750d6baeea4b822fd57e4c12f46f157
minimal REALIZABILITY_AUDIT   27b255f6bedbf983f0d3ba58f64e1af8b7e0061a
minimal REPORT               269ec1f80b694605debd09022591ee64efba34d2
contraction DEFINITIONS      922d31d72f74a8c81f75b5b3a64902c0ad6a0448
contraction REPORT           1a330e6212248c23831fb2f44a9d90f981ed59d1
two-anchor REPORT            2711299b58f5c3b9f67c117af0df4ae3cd3357ec
prefix REPORT                cb2f117f5b2e3f2bdd54f4bfe11f6414eed4570b
prefix THEOREM_AUDIT          e1b727f326d69938f7a316c955e4b595fca1cf77
hereditary REPORT            260d7160f6b2321cdc6f7f1212986b898461980e
```

对每个路径的 frozen source URL 形式是：
`https://github.com/Samsen879/a303656/blob/0200beede923c56e0284d9555c1dabaf91fa1755/<path>`。

## Outside primary sources

Ding, Yuchen (2019), *Non-Wieferich primes under the abc conjecture*, C. R. Acad. Sci. Paris, Ser. I 357, 483–486; DOI `10.1016/j.crma.2019.05.007`。核对 Theorem 1.1，并查看 PDF 对应页面。使用范围仅为 abc conditional non-Wieferich lower bound 的准确说明；不是本文 resource shortage 的证明依据。

Graves, Hester and Weiss, Benjamin (2025), *The abc conjecture implies infinitely many non-Wieferich places for fixed bases in number fields*, `arXiv:2503.19144v1`。核对 introduction 与 theorem statements；primary preprint，不将它描述为已完成 journal peer review。

## Reproduction claims

没有导入或运行 repository 中的 prime scan / mask / matching programs。本包独立复算了 main 的 finite prime panel、selected common-residue pair counts 和两个 full-period examples。没有重新生成 main 的所有巨大 abstract-template catalogs，也没有宣称完成 main 的全部 test suite。

Initial arithmetic discovery 曾使用 symbolic routines；最终随包的 factor generator、polynomial Euclidean resultant、Bareiss verifier 和所有 reference runs 都只依赖 Python standard library。不同 exact formulations 在同一执行环境中相互验证，不称为完全独立 software stacks。
