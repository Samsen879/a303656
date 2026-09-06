# 七-prime证明重新审阅报告

## Verdict

**ACCEPT IN THE STATED FORMAL CLASS — 本轮重新推导未发现致命逻辑缺口。**

审阅对象是源包 `MASTER_THEOREM.md` §1–8 的“至少七个original nonregular primes”必要界，不是对整份Phase B报告的所有新命题、Gate B标签或一般非线性递归closure作全面背书。

我们没有把上一轮结论当作已证明事实直接引用。新文件 `SEVEN_PRIME_INDEPENDENT_PROOF.md` 给出一个不同组织方式的完整重证：反设N≤6，所有p≥7处的linear contraction自动等于full exact contraction，最后只剩3与5。这绕过了一般critical-core提取的必要性。

“独立”仅表示新的推导路线与不导入原reference的检查代码；这仍是同一会话/同一执行环境，不是不同作者、另一个模型或proof assistant验证。

## 输入与custody

- Source ZIP SHA256: `4d75958f51ff27e7a0d4d50811c6f60fb1e0886745eeae1b292e5b9718f0653e`.
- ZIP安全检查：无绝对路径、上跳路径或symlink。
- 原25个payload文件checksum：PASS。
- 原10份mathematical JSON完整重放：PASS，只忽略原规约指定的`seconds`键。
- 原15项regression tests：PASS。
- 冻结原包未修改。原包完整副本保存在evidence下，便于分开识别producer来源和本轮reviewer输出。

## Load-bearing审阅表

| 原论证环节 | 本轮判定 | 重新核实的关键点 |
|---|---|---|
| Lemma2.1，parity-flexible anchor | PASS | 同一个c_*对两种parity均成立；mod8区分；K2=2另处理。没有换anchor。 |
| Cor2.2，two-adic/odd subsystem分离 | PASS | odd-row period的2-valuation≤1；高2-bits可以CRT调整；coarse/full通过private-digit论证连接。 |
| 关闭dynamic3 | PASS | w3=2且s3=1；fixed anchor的positive divisibility至多占一种parity。 |
| Lemma3.1，sparse local cover | PASS | 接受shell0则shell1不接受；中心局部零排除；proper cylinders不能跨first branches。 |
| Linear来源单射 | PASS | 每个seed一个fixed top cylinder，唯一dynamic helper；最多一个child，不按alternative重新选residue。 |
| Fixed ambient | PASS | 全程冻结U、depths、row参数，删除event不删除support。 |
| Least-helper argument | PASS | guard intersection的LCM保留尚未消去的prime powers；最小helper不能依靠更小未记录helper抹掉order因子。 |
| Lemma6.1，rank3浅层8/9 | PASS | 完整factorization限定heads为7/31/19/5167；每个actual helper只有一个fixed logarithm位置。 |
| Cor6.2，七叶税 | PASS | 浅层覆盖不足迫使深度≥3，complete ternary frontier至少七叶；未挪用81-row original-prime税。 |
| Lemma7.1，3-free rank5位置 | PASS | order5/10的完整分解排除raw rigid资源，helper仅11/71；它们最多两个fixed branches。 |
| Lemma7.2，n-4计数 | PASS | 数全部minimal cover witnesses；n5至多1，n6至多2；深叶不可能出现在六叶以内的irredundant5-frontier。 |
| Lemma7.2，排除constant macro | PASS | 非空交为whole要求每个lower guard为whole；五个3-free constituents受两branch约束，不可能full。 |
| Theorem8.1，N≥7 | PASS | 独立重证直接做p≥7精确收缩，剩余rank5分n≤4和n≥5两类，均不能完整。 |

## 特别容易误用但本轮未发现被误用的地方

1. **七个是nonregular original primes，不是总row数。** regular helpers可任意多；这不触犯来源计数，因为helper不是新rigid origin。
2. **固定位置至关重要。** 同一个helper的多个lineages不能各自选一个新logarithm位置。8/9界正依赖这一点。
3. **n-4不是一般macro守恒公式。** 它只对p5、n≤6、无dynamic5这一小class成立。出界后不能继续套用。
4. **无constant macro不是纯几何结论。** 抽象五个first5 branches若lower guards全为whole，确实覆盖且收缩成constant；实际算术通过11/71仅两个可用fixed positions排除这种构造。
5. **finite tests不证明任意depth。** 任意深度下的排除由prefix-tree叶数论证与实际order完整分类完成。

## 检查代码的反向攻击

- 明确构造J={0,1}、p3、β2及一个中心singleton：违反admitted parity时稀疏lemma立刻失败。故parity条件不是装饰。
- 对five-cylinder审阅允许不同来源重复几何；这样不会漏掉第六行造成第二个minimal witness的情形。
- CRT测试同时包含incompatible intersections与祖先/后代嵌套，防止把proper lower guard错误地消成whole。
- abstract linear测试只标作abstract states，未把随机通过率或generic cylinders当作actual prime realization。

## 编辑建议（不构成证明阻塞）

为未来repository integration，建议把§5的guard-modulus invariant单列成lemma，并附上本轮N≤6直接重证。这样读者无需先接受整套canonical exceptional-core机制即可审核七-prime界。源文的“canonically retained original rigid subcover”应读作“完整event subcover中保留的rigid部分”，不是声称rigid部分单独cover；本轮重证完全省去此措辞与pruning。

## 仍未证明

- 七个nonregular primes足够，或该界sharp。
- 任意prime范围的finite-certificate universal no-go。
- 整体A303656的universal representability。
- 一般nonlinear provenance branching后仍存在来源数或Kraft质量的守恒/严格下降量。

Repository状态不修改，GitHub写操作为NONE。
