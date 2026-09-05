# Adversarial theorem audit

## Verdict

```text
THEOREM-LEVEL PARTIAL ADVANCE: PASS
SCOPE: one anchor, one final induced ambient system and fixed lower-coordinate fiber
GLOBAL/TWO-ANCHOR COMPLETION: NOT PROVED
PROJECT: PAUSED
ACTIVE PROMOTED ROUTE: NONE
A303656: UNRESOLVED
```

## Audit A — no hidden reuse of a rigid prime

For fixed anchor and lower assignment, one row has at most one active logarithm modulo `w_q`, hence at most one rigid cylinder. The resource proof therefore requires an injection from frontier leaves to distinct primes. The sufficiency construction uses a fresh prime for every leaf.

## Audit B — order divisibility is not confused with lifting

A rigid leaf needs `s_q>=2`; merely having `l^e | w_q` is insufficient. The resource scan stores separate support, order-signature, and active-nonregular lists.

## Audit C — ambient beta is not confused with active leaf depth

A regular row may have exact `v_l(w_q)=beta` and create the coordinate while supplying no rigid fatal leaf. The theorem requires an extra support row only when the frontier itself has no depth-beta leaf.

## Audit D — lower-coordinate consistency

Resource and support rows are selected before the complete lower fiber is
fixed. Their orders, with any explicitly retained rows, determine the final
`U`. For a desired depth-e cylinder, `w_q=u_q l^e` with all prime factors of
`u_q` below `l`. A compatible lower CRT point of this final system determines
the class modulo `u_q`; the desired cylinder determines it modulo `l^e`; CRT
gives one full class modulo `w_q`. A previously prescribed partial lower point
must be extended compatibly to new prime powers. The theorem does not claim
that arbitrary selected resources preserve an externally frozen `U`.

## Audit E — local zero remains fail-closed

The dynamic construction sets the center equal to a local zero modulo `l^(s_l+m)`. It is not accepted. The centered rigid frontier covers it. The rigid leaf construction has valuation exactly one and is never zero modulo `q^2`.

## Audit F — support row does not alter the target event family

For the one-anchor theorem, setting `r_q=3^c` makes the support-row local value `-5^d`, a unit for every exponent. In the explicit two-anchor examples, the regular support rows have `s_q=1` and `beta_q=0`, hence no coarse fatal class at either anchor.

## Audit G — two anchors are not inferred from one anchor

The main iff theorem is not stated simultaneously. A shared residue must pass the rigid minimum-valuation criterion, the dynamic difference-set criterion, one-sided suppression constraints, and common lower-coordinate CRT compatibility.

## Audit H — bounded absence is not universalized

The `q<=10^7` labels `ORDER_BLOCKED`, `LIFTING_BLOCKED`, and `SUPPORT_BLOCKED` are explicitly scoped to that finite resource pool. Outside the bound, candidates return to `UNKNOWN` unless a theorem such as dynamic parity or the `l=31` center obstruction applies.

## Audit I — parameter labels versus unlabelled event systems

The catalog retains `m` and `s_l` parity labels, matching the repository convention. Thus the four realized `l=67, beta=3` labels correspond to only two unlabelled set systems. Both counts are stated separately.

## Audit J — no claim about A303656

A realized or escaped local frontier does not imply a sum-of-two-squares representation. No complete certificate is constructed or excluded. The authority state is unchanged.
